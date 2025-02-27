from enum import Enum
import pathlib

from scjn_transcripts.utils.base_data_handler import BaseDataHandler
from scjn_transcripts.io.managers import CacheManager, MongoManager
from scjn_transcripts.models.cleaner.transcript import Transcript
from scjn_transcripts.logger import logger

class TranscriptIoHandler(BaseDataHandler):

    def __init__(self):
        super().__init__(CacheManager, MongoManager)

    def build_frontmatter(self, transcript: Transcript) -> dict:
        
        # Given a transcript object, build a frontmatter with the following format:
        # ---
        # key: value
        # key: value
        # ---
        # All transcript properties are included in the frontmatter, except for the "contenido" property.

        # Get a model dump of the transcript object
        transcript_dict = transcript.model_dump()

        # Remove the "contenido" property from the transcript object
        transcript_dict.pop("contenido")

        # Build the frontmatter string
        frontmatter = "---\n"
        for key, value in transcript_dict.items():
            frontmatter += f"{key}: {value if not isinstance(value, Enum) else value.value}\n"
        frontmatter += "---\n\n"

        return frontmatter

    def build_markdown(self, transcript: Transcript) -> str:
        
        # Given a transcript object, build a markdown string with the following format:
        # Frontmatter
        # transcript.contenido

        # Build the frontmatter string
        frontmatter = self.build_frontmatter(transcript)

        # Build the markdown string
        markdown = frontmatter + transcript.contenido

        return markdown
    
    def check_output_dir(self, output_dir: str):
        # Check if the output directory exists
        output_dir_as_path = pathlib.Path(output_dir)
        if not output_dir_as_path.exists():
            logger.warning(f"Output directory {output_dir} does not exist. Creating it.")
            output_dir_as_path.mkdir(parents = True)
        
        return output_dir_as_path

    def load(self):
        raise NotImplementedError("This method is not implemented yet.")
    
    async def dump(self, output_dir: str):

        # Check if the output directory exists
        output_dir_as_path = self.check_output_dir(output_dir)

        # First, get all the cleaned transcripts from the database
        logger.info("Getting all cleaned transcripts from the database")
        transcripts = await self.mongo_manager.get_documents({})

        # Init loop variables
        count = 0
        total = len(transcripts)

        # Iterate over all the transcripts
        for transcript in transcripts:

            # Build the markdown string
            markdown = self.build_markdown(transcript)

            # The output file name will be the date (YYY-MM-DD) of the transcript, followed by the organo jurisdiccional
            # property of the transcript, then the id property of the transcript, and finally the .md extension
            file_name = f"{transcript.fecha_sesión.year}-{transcript.fecha_sesión.month:02d}-{transcript.fecha_sesión.day:02d}_{transcript.organo_jurisdiccional.value}_{transcript.id}.md"
            file_path = output_dir_as_path / file_name

            # Write the markdown string to the output file
            logger.info(f"Writing transcript {transcript.id} to file {file_path}")
            with open(file_path, "w") as file:
                file.write(markdown)

            # Increment the count
            count += 1

        return {"total": total, "dumped": count}