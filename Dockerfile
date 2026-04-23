FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]