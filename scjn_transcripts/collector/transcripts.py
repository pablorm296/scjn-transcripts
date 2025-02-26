from pymongo import AsyncMongoClient
from redis import Redis
from math import ceil

from scjn_transcripts.models.collector.response.document import DocumentDetailsResponse
from scjn_transcripts.clients.buscador_jurídico import BuscadorJurídicoApiClient
from scjn_transcripts.models.collector.response.búsqueda import BúsquedaResponse
from scjn_transcripts.collector.managers import CacheManager, MongoManager
from scjn_transcripts.utils.mongo import MongoClientFactory
from scjn_transcripts.utils.redis import RedisFactory
from scjn_transcripts.logger import logger

import scjn_transcripts.utils.requests as clients_utils
import scjn_transcripts.utils.digest as digest_utils

class ScjnSTranscriptsCollector:
    client: BuscadorJurídicoApiClient
    cache_client: Redis | None = None
    mongo_client: AsyncMongoClient | None = None
    cache_manager: CacheManager
    mongo_manager: MongoManager

    def __init__(self):
        """Initialize the ScjnSTranscriptsCollector instance."""
        self.__init_client()

    def __init_client(self):
        """Initialize the BuscadorJurídicoApiClient."""
        logger.debug("Initializing BuscadorJurídicoApiClient")
        self.client = BuscadorJurídicoApiClient()

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

        self.mongo_client.close()
        self.cache_client.close()

    def check_and_set_transcript(self, document_details: DocumentDetailsResponse) -> DocumentDetailsResponse:
        """Check and set the transcript for a given document.

        Args:
            document_details (DocumentDetailsResponse): The document details.

        Returns:
            DocumentDetailsResponse: The updated document details.
        """
        logger.debug(f"Checking and setting transcript for document {document_details.id}")

        if not document_details.contenido and document_details.archivo:
            logger.info(f"Document {document_details.id} has no transcript. Trying to get it from the file endpoint")
            print_response = self.client.get_print(document_details.archivo)

            # Check if the response is empty
            if len(print_response.content) == 0:
                logger.warning(f"Document {document_details.id} has an empty transcript")
                return document_details

            is_response_text = clients_utils.response_is_text(print_response)
            if is_response_text:
                print_text_content = print_response.text
                is_base64 = clients_utils.text_is_base64(print_text_content)
                document_details.contenido = print_text_content if not is_base64 else clients_utils.base64_to_text(print_text_content)
            else:
                logger.warning(f"Document {document_details.id} has a binary file. Transcript cannot be extracted")

        elif not document_details.contenido and not document_details.archivo:
            logger.warning(f"Document {document_details.id} has no transcript and no file. Transcript cannot be extracted")
            
        return document_details

    async def collect(self):
        """Collect transcripts from the SCJN website.

        This method collects transcripts from the SCJN website and stores
        them in the DB.

        This method should be called after the connect method has been called.
        """

        # Check that the DB and cache clients are connected
        self.__check_connection_clients()

        # Get the search page from the cache
        page = self.cache_manager.get_search_page()
        
        # Init collector variables
        page_size = 20
        total_pages = 0
        total_items = 0
        requests = 0
        saved = 0
        patched = 0

        # Loop through the search results
        logger.info(f"Starting collection from page {page}")
        while True:

            logger.info(f"Requesting page {page}")
            search_response = self.client.get_búsqueda("*", index = "vtaquigraficas", page = page, size = page_size)
            parsed_search_response = BúsquedaResponse(**search_response.json())

            # If it's the first page, set the total pages
            if requests == 0:
                total_items = parsed_search_response.total
                total_pages = ceil(total_items / page_size)

                logger.info(f"Total items: {total_items}; Total pages: {total_pages}")

            # Loop through the search results
            for item in parsed_search_response.resultados:
                # Get the document_details id
                id = item.id
                logger.info(f"Processing document {id}")

                # Request the full document details
                document_response = self.client.get_documento(id)
                parsed_document_response = DocumentDetailsResponse(**document_response.json())

                # Check and set the transcript
                parsed_document_response = self.check_and_set_transcript(parsed_document_response)

                parsed_document_response_dump = parsed_document_response.model_dump()
                parsed_document_response_digest = digest_utils.get_digest(parsed_document_response_dump)

                # Get the document digest from the cache
                digest = self.cache_manager.check_document_details(id)

                if digest:
                    logger.info(f"Document {id} already exists in the DB")
                    # Check if the document has changed
                    if parsed_document_response_digest == digest:
                        # If the document hasn't changed, skip it
                        continue

                    logger.info(f"Document {id} has changed. Patching it")

                    # If the document has changed, patch it
                    patched += await self.mongo_manager.patch_document_details(parsed_document_response_dump)

                    # Update the digest in the cache
                    self.cache_manager.set_document_details(id, parsed_document_response_digest)
                else:
                    logger.info(f"Document {id} does not exist in the DB. Saving it")
                    # Save the document in the DB
                    new_id = await self.mongo_manager.save_document_details(parsed_document_response)

                    # Save the digest in the cache
                    self.cache_manager.set_document_details(id, parsed_document_response_digest)

                    saved += 1
                
            requests += 1
            page += 1

            # Check if we've reached the total pages
            if requests >= total_pages:
                logger.info("Reached the last page")
                break

            # Set the search page in the cache
            self.cache_manager.set_search_page(page)

        return {
            "total_items": total_items,
            "saved": saved,
            "patched": patched
        }


if __name__ == "__main__":
    async def main():
        """Main entry point for the script."""
        collector = ScjnSTranscriptsCollector()
        await collector.connect()
        result = await collector.collect()
        await collector.close()
        print(result)

    import asyncio
    asyncio.run(main())