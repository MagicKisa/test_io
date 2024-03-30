# Используйте официальный образ Python
FROM python:3.10

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файл requirements.txt в контейнер
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --index-url https://pypi.python.org/simple/ -r requirements.txt

# Скопируйте все остальное в контейнер
COPY . .

# Запустите ваше приложение
CMD ["python", "main.py"]
