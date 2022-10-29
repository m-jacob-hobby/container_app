## Running the Load Manager application

This application can be run locally or via a docker container

API documentation is viewable by going to localhost:5000/apidocs/ when the app is running local.

# Running locally
Prerequisites to run locally are that you have Python 3+ and [Pipenv](https://pipenv.readthedocs.io/en/latest/) on your local machine. If so:

```bash
# In the root directory
pipenv install
./bootstrap.sh
```

# Running as a Docker container
Using the Dockerfile provided, you can build and deploy your own Docker instance hosting the application. To do this:

```bash
# build the Docker image
docker build -t load_manager .

# run the new Docker container
docker run --name load_manager -d -p 5000:5000 load_manager
```