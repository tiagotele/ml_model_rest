FROM python:3.7

RUN pip install fastapi uvicorn sklearn numpy

EXPOSE 8000

COPY ./app /app
ADD ./app/iris.mdl iris.mdl

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]