# Main profiles service.
FROM python:3.10

WORKDIR /
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src .

ENTRYPOINT ["python", "profiles_server.py"]
# ENTRYPOINT ["tail", "-F", "anything"]
# ENTRYPOINT ["python"]