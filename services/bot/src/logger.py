import logging
import os
import sys

logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=os.getenv('LOGGING_LEVEL')
)

logger = logging.getLogger(__name__)
