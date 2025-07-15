FROM python:3.13-slim

WORKDIR /app

COPY Pipfile* ./
RUN pip install pipenv && pipenv install

COPY . .

CMD ["pipenv", "run", "python3", "app.py"]
