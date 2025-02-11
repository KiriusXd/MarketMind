import logging

# Настройка логирования
LOG_FILE = "client.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Функция для логирования ошибок


def log_error(message):
    logger.error(message)

# Функция для логирования информации


def log_info(message):
    logger.info(message)
