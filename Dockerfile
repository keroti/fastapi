FROM python

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--port", "80"]