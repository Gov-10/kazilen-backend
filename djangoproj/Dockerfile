FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
RUN python manage.py collectstatic --no-input
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "djangoproj.asgi:application"]
