from .relationship import Relationship as Relationship, RelationshipData as RelationshipData
from .table import Table as Table, TableData as TableData
from .typeholder import AnnotationData as AnnotationData
from _typeshed import Incomplete
from typing import TypedDict

class AccessOptionsData(TypedDict):
    legacyRedirects: bool
    returnErrorValuesAsNull: bool

class QueryGroupData(TypedDict):
    folder: str
    annotations: list[AnnotationData]

class LinguisticMetadataContent(TypedDict):
    Version: str
    Language: str
    DynamicImprovement: str

class LinguisticMetadata(TypedDict):
    contentType: str
    content: LinguisticMetadataContent

class CultureData(TypedDict):
    name: str
    linguisticMetadata: LinguisticMetadata

class ModelData(TypedDict):
    culture: str
    dataAccessOptions: AccessOptionsData
    defaultPowerBIDataSourceVersion: str
    sourceQueryCulture: str
    tables: list[TableData] | None
    relationships: list[RelationshipData] | None
    cultures: list[CultureData]
    annotations: list[AnnotationData]
    queryGroups: list[QueryGroupData] | None

class DataModelSchemaData(TypedDict):
    name: str
    compatibilityLevel: int
    model: ModelData

def get_default_table() -> TableData: ...
def remove_none_values(dct): ...

class DataModelSchema:
    relationships: list[Relationship]
    tables: list[Table]
    query_groups: list[str]
    reference_data: DataModelSchemaData
    id: Incomplete
    def __init__(self) -> None: ...
    def clear_tables(self) -> None: ...
    def clear_relationships(self) -> None: ...
    def clear_query_groups(self) -> None: ...
    def clear(self) -> None: ...
    def get_table_by_name(self, name: str) -> Table: ...
    def insert_query_group(self, group_name: str): ...
    def new_relationship(self, from_table: str, from_column: str, to_table: str, to_column: str = ...) -> Relationship: ...
    def new_table(self, name: str) -> Table: ...
    def load(self, schema_data: DataModelSchemaData): ...
    def dump(self) -> DataModelSchemaData: ...

def write(schema_file_path: str, data: DataModelSchemaData): ...
def read(schema_file_path: str) -> DataModelSchema: ...
