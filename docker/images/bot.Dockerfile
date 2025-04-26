FROM python:3.12.8-slim

WORKDIR /service

COPY ./services/bot/.meta /service/.meta
RUN pip install -r /service/.meta/packages

COPY ./services/bot /service

CMD ["python", "/service/src/run.py"]