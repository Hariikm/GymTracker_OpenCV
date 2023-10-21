from src.gymtracker.pipeline import execution_pipeline
from src.gymtracker import logger

try:
    major_class= execution_pipeline
    major_class.main()

except Exception as e:
    logger.exception(e)
    raise e