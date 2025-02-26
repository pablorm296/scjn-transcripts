import logging

# Set up a custom 'scjn-transcripts' logger
logger = logging.getLogger("scjn-transcripts")

# Set up info as the default log level
logger.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()

# Create a formatter and add it to the handler
formatter = logging.Formatter("%(asctime)s, %(levelname)8s, %(message)s, %(module)s")

# Set the formatter for the handler
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)