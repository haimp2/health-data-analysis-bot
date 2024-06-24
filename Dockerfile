FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --ignore-pipfile
COPY . .
CMD ["pipenv", "run", "python", "main.py"]
