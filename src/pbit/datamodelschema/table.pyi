from .column import Column as Column, ColumnData as ColumnData
from .dax import DaxType as DaxType
from .measure import Measure as Measure, MeasureData as MeasureData
from .partition import Partition as Partition, PartitionData as PartitionData
from .powerquery import MType as MType
from .typeholder import AnnotationData as AnnotationData
from typing import TypedDict

class HierarchyLevelData(TypedDict):
    name: str
    ordinal: int
    column: str
    linageTag: str

class HierarchyData(TypedDict):
    name: str
    lineageTag: str
    state: str
    levels: list[HierarchyLevelData]

class TableData(TypedDict):
    name: str | None
    isHidden: bool | None
    isPrivate: bool | None
    showAsVariationsOnly: bool | None
    lineageTag: str
    columns: list[ColumnData]
    partitions: list[PartitionData]
    hierarchies: list[HierarchyData] | None
    annotations: list[AnnotationData]
    measures: list[MeasureData] | None

class Table:
    name: str
    id: str
    columns: list[Column]
    partitions: list[Partition]
    measures: list[Measure]
    reference_data: TableData
    def __init__(self, name: str) -> None: ...
    def bind_to_json(self, relative_json_path: str, type_dictionary: dict[str, DaxType], group_name: str | None = ...): ...
    def new_partition(self, name: str = ..., language: str = ..., query_group: str | None = ...) -> Partition: ...
    def get_column_by_name(self, name: str) -> Column: ...
    def new_column(self, name: str, data_type: DaxType, source_column: None | str = ...) -> Column: ...
    def new_bin(self, target_column_name: str, increment: float, target_table_name: str | None = ..., bin_name: str | None = ..., data_type: DaxType = ...): ...
    def new_measure(self, name: str) -> Measure: ...
    def load(self, data: TableData): ...
    def dump(self) -> TableData: ...
