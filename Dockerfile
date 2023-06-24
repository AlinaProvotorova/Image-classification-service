FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

CMD ["flask", "run"]

