from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy

class AnnotationData(TypedDict):
	name: str
	value: str
