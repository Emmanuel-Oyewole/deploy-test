#Stage 1: Builder
FROM python:3.10-alpine as builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

#Stage 2: Runtime
FROM python:3.10-alpine
WORKDIR /app
COPY --from=builder /install /usr/local

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]