from http import HTTPStatus

from flask_restful import Resource
from webargs.fields import Int, Str
from webargs.flaskparser import use_kwargs

from api.model.container import Container
from api.model.package import Package, PackageSchema


def rect_intersect(item1, item2, x, y):
    d1 = item1.get_dimensions()
    d2 = item2.get_dimensions()

    cx1 = item1.position[x] + d1[x]/2
    cy1 = item1.position[y] + d1[y]/2
    cx2 = item2.position[x] + d2[x]/2
    cy2 = item2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


class Axis:
    WIDTH = 0
    LENGTH = 1
    DEPTH = 2

    ALL = [WIDTH, LENGTH, DEPTH]


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.LENGTH) and
        rect_intersect(item1, item2, Axis.LENGTH, Axis.DEPTH) and
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )


def load_package(container: Container, package: Package, pivot_point: list) -> bool:
    loaded: bool = False
    initial_package_position: list = package.position
    package.position = list(pivot_point)
    for rotation_code in package.get_rotation_items():
        package.rotation_orientation = rotation_code
        dimensions = package.get_dimensions()

        # 1) Ensure package placed in rotation will not exceed container boundaries
        if container.width < pivot_point[0] + dimensions[0] or \
            container.length < pivot_point[1] + dimensions[1] or \
                container.depth < pivot_point[2] + dimensions[2]:
            continue
        loaded = True

        # 2) Check if new package placement will collide with already loaded packages
        for loaded_package_id in container.packages:
            loaded_package: Package = Package.get_by_id(loaded_package_id)
            if intersect(loaded_package, package):
                loaded = False
                break
        
    if not loaded:
        package.position = initial_package_position
    
    return loaded


def load_package_to_container(container: Container, package: Package) -> bool:
    loaded: bool = False
    if not container.packages:
        loaded = load_package(container, package, [0,0,0])
        if loaded:
            return loaded
    
    for axis in Axis.ALL:
        for preloaded_package_id in container.packages:
            preloaded_package: Package = Package.get_by_id(preloaded_package_id)
            pivot = preloaded_package.position
            w, l, d = preloaded_package.get_dimensions()
            if axis == Axis.WIDTH:
                pivot[0] = pivot[0] + w
            elif axis == Axis.LENGTH:
                pivot[1] = pivot[1] + l
            elif axis == Axis.DEPTH:
                pivot[2] = pivot[2] + d
            loaded = load_package(container, package, pivot)
            if loaded:
                return loaded
    return loaded


class PackageListResource(Resource):
    def get(self):
        """
        View all packages
        Get the list of all currently created packages
        ---
        responses:
          200:
            description: Returns a list of all currently created packages
        """
        packages: list = Package.get_all()
        data = []
        if packages:
            for package in packages:
                data.append(package.data())
            return {"data": data}, HTTPStatus.OK
        return {"msg": "no packages available"}, HTTPStatus.BAD_REQUEST


class PackageGetResource(Resource):
    @use_kwargs({"package_id": Int(location="path")})
    def get(self, package_id):
        """
        Search for a specific package by ID
        Looks through all available packages and attempts to return the details on the one matching the provided ID
        ---
        parameters:
          - in: path
            name: package_id
            type: string
            required: true
            example: A1
        responses:
          200:
            description: Looks up a Package record by ID value
            schema:
              id: Package
              properties:
                id:
                  type: string
                  description: Customer provided package ID
                length:
                  type: integer
                width:
                  type: integer
                depth:
                  type: integer
                container_id:
                  type: string
                  description: ID for container package has been loaded
                rotation_orientation:
                  type: integer
                  description: package rotation orientation code id which correlates to values in BoxRotationType model
                position:
                  type: array
                  description: coordinate position within container where the package rotation orientation pivot point is located
        """
        package: Package = Package.get_by_id(package_id)
        if package is None:
            return {"message": f"Package not found with ID {package_id}"}, HTTPStatus.NOT_FOUND
        return {"msg": f"{package.data()}"}, HTTPStatus.OK


class PackageCreateResource(Resource):
    @use_kwargs(
        {
            "id": Str(required=True, location="json"),
            "length": Int(required=True, location="json"),
            "width": Int(required=True, location="json"),
            "depth": Int(required=True, location="json"),
            "container_id": Str(required=False, location="json")
        }
    )
    def post(self, id: str, length: int, width: int, depth: int, container_id: str=None):
        """
        Creates a new package record
        Provided a package's ID and dimensions (and optionally a container_id), a new package record will be created and loaded onto the first available container
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
          - in: body
            name: container_id
            type: string
            required: false
            example: A1
        responses:
          200:
            description: Creates a new Package record
        """
        package: Package = Package.get_by_id(id=id)
        if package:
            return {"message": f"A package with that ID already exists: {package.data()}"}, HTTPStatus.BAD_REQUEST
        
        package: Package = Package(id, width, length, depth, container_id)
        loaded_container: Container = None
        if container_id:
            container: Container = Container.get_by_id(container_id)
            if not container:
                return {"message": f"No container exists with id {container_id}"}, HTTPStatus.BAD_REQUEST
            loaded_container = container if load_package_to_container(container, package) else None
        else:
            containers: list = list(Container.get_by_id(container_id)) if container_id else Container.get_all()
            if not containers:
                return {"message": f"No containers created yet to load package to"}, HTTPStatus.BAD_REQUEST

            for container in containers:
                loaded_container = container if load_package_to_container(container, package) else None
                if loaded_container:
                    break
        
        if loaded_container:
            package.container_id = loaded_container.id
            package.save()
            loaded_container.packages.append(package.id)
            loaded_container.save()
            return {"msg": f"Package loaded successfully - {package.data()}"}, HTTPStatus.CREATED
        return {"message": f"Could not find suitable container for {package.data()}"}, HTTPStatus.BAD_REQUEST
