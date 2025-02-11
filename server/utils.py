# server/utils.py

import logging
import sys
import traceback

# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования можно изменить на DEBUG для более подробного вывода
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("MarketMind")


def log_exception(exc: Exception):
    """Функция для логирования исключений с traceback."""
    logger.error("Произошла ошибка: %s", str(exc))
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logger.error("Traceback:\n%s", tb)
