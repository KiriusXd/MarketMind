# Указываем интерпретатор Python (по умолчанию python3, но можно поменять)
PYTHON := python

# Определяем виртуальное окружение
VENV_DIR := .env
VENV_BIN := $(VENV_DIR)/bin
PIP := $(VENV_BIN)/pip
UVICORN := $(VENV_BIN)/uvicorn

# Файл базы данных
DB_FILE := marketmind.db

# Функция для проверки и установки виртуального окружения
$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Запуск сервера
run-server: $(VENV_DIR)
	$(UVICORN) server.app:app --host 0.0.0.0 --port 8000 --reload

# Запуск клиента (CLI)
run-client: $(VENV_DIR)
	$(PYTHON) client/main.py

# Удаление базы данных
clean-db:
	rm -f $(DB_FILE)
	echo "База данных удалена."

# Форматирование кода с помощью black
format:
	$(VENV_BIN)/black server client

# Установка зависимостей
install: $(VENV_DIR)
	$(PIP) install -r requirements.txt

# Очистка окружения
clean:
	rm -rf $(VENV_DIR) __pycache__

# Полная переустановка окружения
reinstall: clean
	make install

# Справка по командам
help:
	@echo "Доступные команды:"
	@echo "  make run-server   - Запустить сервер"
	@echo "  make run-client   - Запустить клиент"
	@echo "  make clean-db     - Удалить базу данных"
	@echo "  make install      - Установить зависимости"
	@echo "  make clean        - Удалить виртуальное окружение и временные файлы"
	@echo "  make reinstall    - Полностью переустановить окружение"
	@echo "  make format       - Отформатировать код с помощью black"
