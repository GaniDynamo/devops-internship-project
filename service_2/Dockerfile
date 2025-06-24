FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y curl --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN pip install Flask
COPY . .
EXPOSE 8082
CMD ["python", "app.py"]
