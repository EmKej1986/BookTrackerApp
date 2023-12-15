FROM python:latest

WORKDIR /api

COPY api/requirements.txt .
COPY web/modelSQL.py/ .
COPY web/__init__.py/ web.py

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY api/ .

CMD ["python", "run.py"]
