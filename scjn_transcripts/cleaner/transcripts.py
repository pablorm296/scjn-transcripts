from markdownify import markdownify
import datetime
import re

from scjn_transcripts.models.collector.response.document import DocumentDetailsResponse
from scjn_transcripts.utils.base_data_handler import BaseDataHandler
from scjn_transcripts.models.cleaner.transcript import Transcript
from scjn_transcripts.logger import logger

class ScjnSTranscriptsCleaner(BaseDataHandler):

    def __init__(self):
        super().__init__()

    def clean_text(self, text: str) -> str:
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
            "asuntos": [asunto["num_expediente"] for asunto in document_details.asuntos] if document_details.asuntos else None
        }

        date_day = document_details.dia
        date_month = document_details.mes["numero"]
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