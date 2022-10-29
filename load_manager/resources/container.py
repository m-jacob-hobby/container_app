from http import HTTPStatus

from flask_restful import Resource
from webargs.fields import Int, Str, List
from webargs.flaskparser import use_kwargs

from api.model.container import Container, ContainerSchema


class ContainerListResource(Resource):
    def get(self):
        """
        View all containers
        Get the list of all currently created containers and their contents
        ---
        responses:
          200:
            description: Returns a list of all currently created containers
        """
        containers: list = Container.get_all()
        data = []
        if containers:
            for container in containers:
                data.append(container.data())
            return {"data": data}, HTTPStatus.OK
        return {"msg": "no containers available"}, HTTPStatus.BAD_REQUEST


class ContainerGetResource(Resource):
    @use_kwargs({"container_id": Int(required=True, location="path")})
    def get(self, container_id):
        """
        Search for a specific container by ID
        Looks through all available containers and attempts to return the details on the one matching the provided ID
        ---
        parameters:
          - in: path
            name: container_id
            type: string
            required: true
            example: A1
        responses:
          200:
            description: Looks up a Container record by ID value
            schema:
              id: Container
              properties:
                id:
                  type: string
                  description: Customer provided container ID
                length:
                  type: integer
                width:
                  type: integer
                depth:
                  type: integer
                packages:
                  type: array
                  items: 
                    type: integer
        """
        container: Container = Container.get_by_id(container_id)
        if container is None:
            return {"message": f"Container not found with ID {container_id}"}, HTTPStatus.NOT_FOUND
        return {"msg": f"{container.data()}"}, HTTPStatus.OK


class ContainerCreateResource(Resource):
    @use_kwargs(
        {
            "id": Str(required=True, location="json"),
            "length": Int(required=True, location="json"),
            "width": Int(required=True, location="json"),
            "depth": Int(required=True, location="json")
        }
    )
    def post(self, id: str, length: int, width: int, depth: int):
        """
        Creates a new container record
        Provided a container's ID and dimensions, a new container record will be created
        ---
        parameters:
          - in: body
            name: id
            type: string
            required: true
            example: A1
          - in: body
            name: length
            type: integer
            required: true
            example: 10
          - in: body
            name: width
            type: integer
            required: true
            example: 4
          - in: body
            name: depth
            type: integer
            required: true
            example: 5
        responses:
          200:
            description: Creates a new Container record
        """
        container: Container = Container.get_by_id(id)
        if container:
            return {"message": f"A container with that ID already exists: {container.data()}"}, HTTPStatus.BAD_REQUEST

        container: Container = Container(id, width, length, depth)
        container.save()

        return {"msg": f"Container successfully created - {container.data()}"}, HTTPStatus.CREATED