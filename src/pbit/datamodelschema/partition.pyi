from .column import DaxType as DaxType
from .powerquery import MType as MType, PowerQuery as PowerQuery, from_dax_type_to_m_type as from_dax_type_to_m_type
from typing import TypedDict
from uuid import uuid4 as uuid4

class PartitionSourceData(TypedDict):
    type: str
    expression: list[str] | str

class PartitionData(TypedDict):
    name: str | None
    mode: str
    state: str
    queryGroup: str | None
    source: PartitionSourceData

class Partition:
    name: str | None
    language: str
    power_query: PowerQuery
    query_group: str | None
    reference_data: PartitionData
    def __init__(self, name: str | None = ..., language: str = ..., query_group: str | None = ...) -> None: ...
    def set_to_json_reader(self, relative_json_path: str, dax_types: dict[str, DaxType]): ...
    def load(self, data: PartitionData): ...
    def dump(self) -> PartitionData: ...
