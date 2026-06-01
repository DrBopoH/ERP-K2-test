import logging

from app.core.config import settings
from app.core.services import GreetingService

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



def main():
	logger.info(f"Запуск застосунку в режимі: {settings.ENVIRONMENT}")
	
	service = GreetingService(settings.GREETING_MESSAGE)	
	greeting = service.generate_greeting("K2")
	
	logger.info(greeting)



if __name__ == "__main__":
	main()