FROM python:alpine3.7

WORKDIR /app

COPY . $WORKDIR

RUN pip install --upgrade pip && pip install pipenv

ENTRYPOINT ["pipenv", "run", "ufwq.py", "start"]
