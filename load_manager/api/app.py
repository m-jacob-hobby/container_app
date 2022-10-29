from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flasgger import Swagger
from webargs.flaskparser import abort, parser
from werkzeug import exceptions

from api.config import env_config
from resources.container import ContainerCreateResource, ContainerGetResource, ContainerListResource
from resources.default import DefaultResource
from resources.package import PackageCreateResource, PackageGetResource, PackageListResource
from utils import errors


api = Api()


def create_app(config_name):
    import resources

    app = Flask(__name__)
    app.config.from_object(env_config[config_name])
    api.init_app(app)

    CORS(app)
    Swagger(app)

    app.register_error_handler(exceptions.NotFound, errors.handle_404_error)
    app.register_error_handler(exceptions.InternalServerError, errors.handle_500_error)
    app.register_error_handler(exceptions.BadRequest, errors.handle_400_error)
    app.register_error_handler(FileNotFoundError, errors.handle_400_error)
    app.register_error_handler(TypeError, errors.handle_400_error)
    app.register_error_handler(KeyError, errors.handle_404_error)
    app.register_error_handler(AttributeError, errors.handle_400_error)
    app.register_error_handler(ValueError, errors.handle_400_error)
    app.register_error_handler(AssertionError, errors.handle_400_error)

    @parser.error_handler
    def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
        abort(error_status_code, errors=err.messages)

    return app

api.add_resource(DefaultResource, "/", endpoint="home")
api.add_resource(ContainerCreateResource, "/new_container/", endpoint="create_container")
api.add_resource(ContainerGetResource, "/get_container/<int:container_id>", endpoint="get_container")
api.add_resource(ContainerListResource, "/containers/", endpoint="list_containers")
api.add_resource(PackageCreateResource, "/new_package/", endpoint="create_package")
api.add_resource(PackageGetResource, "/get_package/<int:package_id>", endpoint="get_package")
api.add_resource(PackageListResource, "/packages/", endpoint="list_packages")