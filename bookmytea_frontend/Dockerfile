FROM python:3.9

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "app.main:app", "-b", "0.0.0.0:8000", "--log-level", "debug"]