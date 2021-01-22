FROM python:3.9
RUN pip install pipenv
COPY Pipfile* /app/
WORKDIR /app
RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r ./requirements.txt
COPY ./src/ /app/src
CMD ["python", "./src/main.py"]