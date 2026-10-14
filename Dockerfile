FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY cells/ ./cells/
COPY synapses/ ./synapses/
COPY retina_engine.py .

CMD ["python", "retina_engine.py"]
