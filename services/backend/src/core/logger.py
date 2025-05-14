import logging
import sys

from config import settings


logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=settings.logging_level
)

logger = logging.getLogger(__name__)
