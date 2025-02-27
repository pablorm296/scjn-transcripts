from pymongo import AsyncMongoClient
from markdownify import markdownify
from redis import Redis
import datetime
import re

from scjn_transcripts.models.collector.response.document import DocumentDetailsResponse
from scjn_transcripts.cleaner.managers import CacheManager, MongoManager
from scjn_transcripts.models.cleaner.transcript import Transcript
from scjn_transcripts.utils.mongo import MongoClientFactory
from scjn_transcripts.utils.redis import RedisFactory
from scjn_transcripts.logger import logger

class ScjnSTranscriptsCollector:
    cache_client: Redis | None = None
    mongo_client: AsyncMongoClient | None = None
    cache_manager: CacheManager
    mongo_manager: MongoManager

    def __init__(self):
        pass

    def __init_cache_client(self):
        """Initialize the Redis cache client and CacheManager."""
        self.cache_client = RedisFactory.create()
        self.cache_manager = CacheManager(self.cache_client)

    async def __init_mongo_client(self):
        """Initialize the MongoDB client and MongoManager."""
        self.mongo_client = await MongoClientFactory.create()
        self.mongo_manager = MongoManager(self.mongo_client)

    def __check_cache_client(self):
        """Check if the cache client is initialized."""
        if self.cache_client is None:
            raise ValueError("Cache client not initialized")
        
    def __check_mongo_client(self):
        """Check if the MongoDB client is initialized."""
        if self.mongo_client is None:
            raise ValueError("Mongo client not initialized")
        
    def __check_connection_clients(self):
        """Check if both the cache and MongoDB clients are initialized."""
        self.__check_cache_client()
        self.__check_mongo_client()

    async def connect(self):
        """Connect to DB and cache clients.

        This method should be called before any other method that requires
        a connection to the DB or cache.

        This method should be called only once, as it initializes the
        DB and cache clients.

        This implementation is a workaround to the fact that the
        __init__ method cannot be async.
        """

        logger.debug("Connecting to DB and cache clients")

        await self.__init_mongo_client()
        self.__init_cache_client()

    async def close(self):
        """Close the connection to the DB and cache clients.

        This method should be called when the application is shutting down.
        """

        logger.debug("Closing DB and cache clients")

        self.__check_connection_clients()

        await self.mongo_client.close()
        self.cache_client.close()

    def clean_text(text: str) -> str:
        """Clean the text of a transcript.

        This method should be called before saving the transcript to the DB.
        """

        # First, remove the HTML tags from the text, using markdown to keep the
        # text formatting.
        result = markdownify(text)

        # Now, remove excess whitespace from the text.
        # Double spaces are replaced with single spaces.
        # Two or more newlines are replaced with two newlines.
        
        # Regex for two or more spaces
        result = re.sub(r" {2,}", " ", result)

        # Regex for two or more newlines
        result = re.sub(r"\n{2,}", "\n\n", result)

        return result
    
    def build_transcript(self, document_details: DocumentDetailsResponse) -> Transcript:
        """Build a Transcript object from a DocumentDetailsResponse object."""

        new_transcript = {
            "id": document_details.id,
            "organo_jurisdiccional": document_details.organo_jurisdiccional,
            "contenido": document_details.contenido,
            "url_video": document_details.url_video,
            "url_documento": document_details.url_vt,
            "asuntos": [asunto.num_expediente for asunto in document_details.asuntos],
        }

        date_day = document_details.dia
        date_month = document_details.mes.numero
        date_year = document_details.anio

        new_transcript["fecha_sesión"] = datetime.datetime(date_year, date_month, date_day)

        return Transcript(**new_transcript)
    
    async def clean(self):

        # Check that the DB and cache clients are connected
        self.__check_connection_clients()

        # Get all the documents from the DB
        logger.debug("Getting all documents from the DB")
        documents = await self.mongo_manager.get_documents({})

        # Init loop variables
        cleaned = 0

        # Iterate over the documents
        logger.debug("Starting the main cleaning loop")
        for document in documents:

            logger.info(f"Cleaning document {document.id}")

            # Check if the document has already been cleaned
            if self.cache_manager.document_is_cleaned(document.id):
                logger.info(f"Document {document.id} has already been cleaned. Skipping")
                continue

            # Clean the text of the transcript
            cleaned_text = self.clean_text(document.contenido)
            document.contenido = cleaned_text

            # Build the new transcript object
            new_transcript = self.build_transcript(document)

            # Save the new transcript to the DB
            await self.mongo_manager.save_document(new_transcript)

            # Update the cleaning status in the cache
            self.cache_manager.update_cleaning_status(document.id, True)

            cleaned += 1

        return {
            "cleaned": cleaned,
            "total": len(documents)
        }