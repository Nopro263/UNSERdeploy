FROM python:3.12-bookworm

EXPOSE 80


WORKDIR /app

COPY requirements.txt .
COPY testing_requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -r testing_requirements.txt



ENTRYPOINT [ "bash" ]