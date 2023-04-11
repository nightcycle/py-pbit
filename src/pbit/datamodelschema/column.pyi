from .dax import DaxType as DaxType
from .typeholder import AnnotationData as AnnotationData
from _typeshed import Incomplete
from typing import TypedDict

SummaryType: Incomplete

class ColumnAttributeHierarchyData(TypedDict):
    state: str

class ColumnData(TypedDict):
    type: DaxType | None
    lineageTag: str | None
    summarizeBy: str | None
    sourceColumn: str | None
    name: str
    dataType: str
    formatString: str | None
    dataCategory: str | None
    isNameInferred: bool | None
    expression: str | list[str] | None
    isDataTypeInferred: bool | None
    isHidden: bool | None
    isUnique: bool | None
    sortByColumn: str | None
    isKey: bool | None
    isNullable: bool | None
    attributeHierarchy: ColumnAttributeHierarchyData
    annotations: list[AnnotationData] | None

class Column:
    name: str
    id: str
    data_type: str
    source_column: str | None
    reference_data: ColumnData
    def __init__(self, name: str, dataType: str, source_column: str | None = ...) -> None: ...
    def set_as_bin(self, target_table_name: str, target_column_name: str, increment: float, bin_name: str | None = ..., data_type: DaxType = ...): ...
    def set_as_normalized(self, numerator_table_name: str, numerator_column_name: str, denominator_table_name: str, denominator_column_name: str, name: None | str = ..., data_type: DaxType = ..., summarize_by: SummaryType = ...): ...
    def set_dax(self, dax: str, name: str, data_type: DaxType = ..., summarize_by: SummaryType = ...): ...
    def load(self, data: ColumnData): ...
    def dump(self) -> ColumnData: ...
