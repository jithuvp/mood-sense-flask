FROM python:3.9

WORKDIR /mood-sense

ENV FLASK_APP=./app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH "${PYTHONPATH}:/app/"
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


COPY ./app .

EXPOSE 3000

ENTRYPOINT FLASK_APP=./app/app.py flask run --host=0.0.0.0 -p 3000
#CMD flask run -p 3000
