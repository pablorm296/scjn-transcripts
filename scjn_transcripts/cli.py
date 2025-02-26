from typing_extensions import Annotated
import logging
import asyncio
import typer

from scjn_transcripts.collector.transcripts import ScjnSTranscriptsCollector
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

@app.callback()
def callback():
    pass

if __name__ == "__main__":
    app()
