import json
import os

from marshmallow import fields, post_load

from .box import Box, BoxSchema
from .box_rotation_type import BoxRotationType


class Package(Box):
    PACKAGE_JSON = os.path.join(os.path.dirname(os.path.realpath(__file__)), "package.json")

    def __init__(self, id: str, width: int, length: int, depth: int, container_id: str=None, position: tuple((int, int, int))=(0, 0, 0), rotation_orientation: int = BoxRotationType.WLD):
        super(Package, self).__init__(width, length, depth)
        self.id: str = id
        self.container_id: str = container_id
        self.rotation_orientation: int = rotation_orientation
        self.position: list = position

    def __str__(self):
        return f"Package [{self.id}]: Oriented {self.print_dimensions()} in Container {self.container_id} at position {self.position}"

    def data(self) -> dict:
        return {
            "id": self.id,
            "container_id": self.container_id,
            "rotation_orientation": self.rotation_orientation,
            "position": self.position,
            "length": self.length,
            "width": self.width,
            "depth": self.depth
        }

    def publish_data(self) -> dict:
        return {
            "container_id": self.container_id,
            "rotation_orientation": self.rotation_orientation,
            "position": self.position,
            "length": self.length,
            "width": self.width,
            "depth": self.depth
        }

    def save(self):
        with open(self.PACKAGE_JSON, "r") as f:
            packages_dict: dict = json.load(f)

        packages_dict[self.id] = self.publish_data()
        
        with open(self.PACKAGE_JSON, "w") as f:
            json.dump(packages_dict, f)

    @classmethod
    def get_all(cls) -> list:
        with open(cls.PACKAGE_JSON, "r") as f:
            packages_dict: dict = json.load(f)
            print(packages_dict)
        packages_list: list = []
        for item in packages_dict.items():
            data = item[1]
            data["id"] = item[0]
            packages_list.append(cls(**data))
        return packages_list

    @classmethod
    def get_by_id(cls, id: str):
        with open(cls.PACKAGE_JSON, "r") as f:
            packages_dict: dict = json.load(f)
        if not packages_dict.get(id):
            return None
        return cls(id, **packages_dict[id])


class PackageSchema(BoxSchema):
    id = fields.Str()
    container_id = fields.Str()
    rotation_orientation = fields.Int()
    position = fields.List(fields.Int())

    @post_load
    def make_package(self, data):
        return Package(**data)