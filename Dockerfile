FROM python:3.13.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5020

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5020"]
