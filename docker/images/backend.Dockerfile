FROM python:3.12.8-slim

WORKDIR /service

COPY ./services/backend/.meta /service/.meta
RUN pip install -r /service/.meta/packages

COPY ./services/backend /service

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--reload"]