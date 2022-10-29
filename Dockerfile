# Python image
FROM python:3.8-alpine

# Install packages
RUN apk update
RUN pip install --no-cache-dir pipenv

# Setup working directory and copy in source code
WORKDIR /usr/load_manager/app
COPY Pipfile Pipfile.lock bootstrap.sh ./
COPY load_manager ./load_manager
RUN echo "{}" > ./load_manager/api/model/container.json
RUN echo "{}" > ./load_manager/api/model/package.json

# Install the dependencies
RUN pipenv install

# Launch the app and have it communicate through port 5000
EXPOSE 5000
ENTRYPOINT ["/usr/load_manager/app/bootstrap.sh"]