# Build context: veyant/  (one level above this file)
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the db package and the api package
COPY db/ db/
COPY api/ api/

WORKDIR /app/api

ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
ENV FLASK_DEBUG=false
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
