FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app ./app

ENV LLM_BACKEND=MOCK
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
