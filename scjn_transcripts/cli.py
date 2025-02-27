from typing_extensions import Annotated
import logging
import asyncio
import typer

from scjn_transcripts.collector.transcripts import ScjnSTranscriptsCollector
from scjn_transcripts.cleaner.transcripts import ScjnSTranscriptsCleaner
from scjn_transcripts.io.transcripts import TranscriptIoHandler
from scjn_transcripts.logger import logger

app = typer.Typer(no_args_is_help = True)

@app.command()
def collect(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help = "Increase verbosity")] = False,
    ignore_page_cache: Annotated[bool, typer.Option("--ignore-page-cache", "-i", help = "Ignore the last requested page cache")] = False 
):
    """Start the collection process."""
    if verbose:
        logger.setLevel(logging.DEBUG)

    async def main():
        collector = ScjnSTranscriptsCollector()
        await collector.connect()
        result = await collector.collect(ignore_page_cache = ignore_page_cache)
        await collector.close()
        
        logger.info(f"Collected {result} transcripts")

    asyncio.run(main())

@app.command()
def clean(
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help = "Increase verbosity")] = False,
):
    """Start the cleaning process."""
    if verbose:
        logger.setLevel(logging.DEBUG)

    async def main():
        cleaner = ScjnSTranscriptsCleaner()
        await cleaner.connect()
        result = await cleaner.clean()
        await cleaner.close()
        
        logger.info(f"Cleaned {result} transcripts")

    asyncio.run(main())

@app.command()
def dump(
    output_dir: Annotated[str, typer.Argument(..., help = "Output directory")],
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help = "Increase verbosity")] = False,
):
    """Start the dumping process."""
    if verbose:
        logger.setLevel(logging.DEBUG)

    async def main():
        io_handler = TranscriptIoHandler()
        await io_handler.connect()
        result = await io_handler.dump(output_dir)
        await io_handler.close()
        
        logger.info(f"Dumped {result} transcripts to {output_dir}")

    asyncio.run(main())

@app.callback()
def callback():
    pass

if __name__ == "__main__":
    app()
