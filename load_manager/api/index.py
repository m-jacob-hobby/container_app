from flask import Flask, jsonify, request
from flasgger import Swagger

from api.dao.container_dao import ContainerDao
from api.dao.package_dao import PackageDao
from api.model.container import Container, ContainerSchema
from api.model.package import Package, PackageSchema


app = Flask(__name__)
Swagger(app)

@app.route("/package")
def get_packages():
    packages: list = PackageSchema(many=True).dump(PackageDao().get_all_packages())
    return jsonify(packages)


@app.route("/package", methods=['POST'])
def add_package():
    package: Package = PackageSchema().load(request.get_json())
    # Add check to insert into Containers
    PackageDao().add_package(package.id, package.get_package_details())
    return "", 204

@app.route("/container")
def get_containers():
    containers: list = ContainerSchema(many=True).dump(ContainerDao().get_all_containers())
    return jsonify(containers)

@app.route("/container", methods=['POST'])
def add_container():
    container: Container = ContainerSchema().load(request.get_json())
    ContainerDao().add_container(container.id, container.get_container_details())
    return "", 204