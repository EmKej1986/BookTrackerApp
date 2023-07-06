FROM python:latest

WORKDIR /API

COPY API/requirements.txt .
COPY Web/modelSQL.py/ .
COPY Web/__init__.py/ .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY API/ .

CMD ["python", "run.py"]
