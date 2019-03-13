FROM python:3.7.2
ADD . /app
WORKDIR /app
RUN pip install pipenv
# RUN pipenv install --system
COPY Pipfile .
RUN pipenv lock -r > requirements.txt; pip install -U -r requirements.txt
ENTRYPOINT [ "python", "index.py" ]