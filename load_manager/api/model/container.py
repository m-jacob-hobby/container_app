import json
import os

from marshmallow import fields, post_load

from .box import Box, BoxSchema


class Container(Box):
    CONTAINER_JSON = os.path.join(os.path.dirname(os.path.realpath(__file__)), "container.json")

    def __init__(self, id: str, width: int, length: int, depth: int, packages: list=[]):
        super(Container, self).__init__(width, length, depth)
        self.id: str = id
        self.packages: list = packages

    def __str__(self):
        return f"Container [{self.id}]: {self.print_dimensions()} holding Packages {[package.id for package in self.packages]}"

    def data(self) -> dict:
        return {
            "id": self.id,
            "length": self.length,
            "width": self.width,
            "depth": self.depth,
            "packages": self.packages
        }

    def publish_data(self) -> dict:
        return {
            "packages": self.packages,
            "length": self.length,
            "width": self.width,
            "depth": self.depth
        }

    def save(self):
        with open(self.CONTAINER_JSON, "r") as f:
            containers_dict: dict = json.load(f)
        
        containers_dict[self.id] = self.publish_data()
        
        with open(self.CONTAINER_JSON, "w") as f:
            json.dump(containers_dict, f)

    @classmethod
    def get_all(cls) -> list:
        with open(cls.CONTAINER_JSON, "r") as f:
            containers_dict: dict = json.load(f)
        containers_list: list = []
        for item in containers_dict.items():
            data = item[1]
            data["id"] = item[0]
            containers_list.append(cls(**data))
        return containers_list

    @classmethod
    def get_by_id(cls, id: str):
        with open(cls.CONTAINER_JSON, "r") as f:
            containers_dict: dict = json.load(f)
        if not containers_dict.get(id):
            return None
        return cls(id, **containers_dict[id])


class ContainerSchema(BoxSchema):
    id = fields.Str()
    packages = fields.List(fields.Str())
    active = fields.Bool()

    @post_load
    def make_container(self, data):
        return Container(**data)
