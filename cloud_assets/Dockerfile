FROM python:3.10

RUN apt update && apt install nodejs -y

RUN python -m pip install gunicorn flask numpy pandas requests

EXPOSE 8080

WORKDIR /workspace

COPY app.py /workspace

COPY aidc-2.0.zip ./

RUN python -m pip install aidc-2.0.zip

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]