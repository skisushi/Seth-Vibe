FROM python:3.12-slim

WORKDIR /app

COPY veyant/ ./veyant/

# seed.py uses bare `from database import ...` so it must run from its own dir
WORKDIR /app/veyant/db

CMD ["python", "seed.py"]
