# Используем официальный образ Python в качестве базового
FROM python:3.12

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1  # Предотвращаем запись Python .pyc файлов
ENV PYTHONUNBUFFERED 1       # Предотвращаем буферизацию stdout/stderr

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости, указанные в requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта в контейнер
COPY . .

# Открываем порт, на котором будет слушать ваш бот (если применимо - настройте под ваше приложение)
# EXPOSE 8080

# Команда для запуска приложения (настройте 'main.py' под ваш файл запуска)
CMD ["python", "main.py"]