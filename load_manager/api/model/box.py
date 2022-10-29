from marshmallow import Schema, fields


class Box():
    # Rotation Itemization Code Constants
    WLD = 0
    WDL = 1
    LWD = 2
    LDW = 3
    DWL = 4
    DLW = 5

    def __init__(self, width: int, length: int, depth: int):
        self.width: int = width
        self.length: int = length
        self.depth: int = depth
        self.rotation_orientation: int = self.WLD

    def __str__(self) -> str:
        return f"A Box of dimensions {self.width}W x {self.length}L x {self.depth}D currently oriented in {self._rotation_orientation_to_str()}"

    def _rotation_orientation_to_str(self) -> str:
        if self.rotation_orientation == self.WLD:
            return "Width x Length x Depth"
        elif self.rotation_orientation == self.WDL:
            return "Width x Depth x Length"
        elif self.rotation_orientation == self.LWD:
            return "Length x Width x Depth"
        elif self.rotation_orientation == self.LDW:
            return "Length x Depth x Width"
        elif self.rotation_orientation == self.DWL:
            return "Depth x Width x Lenght"
        elif self.rotation_orientation == self.DLW:
            return "Depth x Length x Width"
        else:
            # TODO: Raise exception for invalid rotation orientation value
            return ""

    def get_dimensions(self) -> tuple((int, int, int)):
        if self.rotation_orientation == self.WLD:
            return (self.width, self.length, self.depth)
        elif self.rotation_orientation == self.WDL:
            return (self.width, self.depth, self.length)
        elif self.rotation_orientation == self.LWD:
            return (self.length, self.width, self.depth)
        elif self.rotation_orientation == self.LDW:
            return (self.length, self.depth, self.width)
        elif self.rotation_orientation == self.DLW:
            return (self.depth, self.length, self.width)
        elif self.rotation_orientation == self.DWL:
            return (self.depth, self.width, self.length)
        else:
            # TODO: Raise exception due to invalid rotation code set
            return (0, 0, 0)

    def print_dimensions(self) -> str:
        if self.rotation_orientation == self.WLD:
            return f"{self.width}W x {self.length}L x {self.depth}D"
        elif self.rotation_orientation == self.WDL:
            return f"{self.width}W x {self.depth}D x {self.length}L"
        elif self.rotation_orientation == self.LWD:
            return f"{self.length}L x{self.width}W x {self.depth}D"
        elif self.rotation_orientation == self.LDW:
            return f"{self.length}L x {self.depth}D x {self.width}D"
        elif self.rotation_orientation == self.DLW:
            return f"{self.depth}D x {self.length}L x {self.width}D"
        elif self.rotation_orientation == self.DWL:
            return f"{self.depth}D x {self.width}W x {self.length}L"
        else:
            # TODO: Raise exception due to invalid rotation code set
            return ""

    def get_rotation_items(self):
        return [self.WLD, self.WDL, self.LWD, self.LDW, self.DWL, self.DLW]

    def get_volume(self):
        return(self.width * self.length * self.depth)


class BoxSchema(Schema):
    width = fields.Int()
    length = fields.Int()
    depth = fields.Int()