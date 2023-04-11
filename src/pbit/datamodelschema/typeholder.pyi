from copy import deepcopy as deepcopy
from typing import TypedDict
from uuid import uuid4 as uuid4

class AnnotationData(TypedDict):
    name: str
    value: str
