FROM python:alpine3.7

WORKDIR /app

COPY . $WORKDIR

RUN pip install --upgrade pip && pip install pipenv && \
    pipenv --python 2.7 install --dev

ENTRYPOINT ["pipenv", "run", "python", "app.py"]
