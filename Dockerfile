FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY TRL_calculator.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP TRL_calculator.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]