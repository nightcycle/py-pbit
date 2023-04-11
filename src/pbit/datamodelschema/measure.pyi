from .column import DaxType as DaxType
from pandas import DataFrame as DataFrame
from typing import TypedDict

class MeasureProperty(TypedDict):
    property: str

class MeasureData(TypedDict):
    name: str
    expression: str
    formatString: str
    lineageTag: str
    dataType: DaxType

class Measure:
    name: str
    id: str
    expression: str
    data_type: DaxType
    format_string: str
    reference_data: MeasureData
    def __init__(self, name: str, data_type: DaxType) -> None: ...
    def set_format(self, format: str): ...
    def set_expression(self, expression: str, data_type: DaxType): ...
    def set_to_retention_rate_tracker(self, user_table_name: str, is_retained_column_name: str): ...
    def load(self, data: MeasureData): ...
    def dump(self) -> MeasureData: ...
