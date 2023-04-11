from typing import TypedDict

class RelationshipData(TypedDict):
    name: str
    fromTable: str
    fromColumn: str
    toTable: str
    toColumn: str
    joinOnDateBehavior: str
    crossFilteringBehavior: str | None
    state: str

class Relationship:
    name: str
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    is_both_directions: bool
    reference_data: RelationshipData
    def __init__(self, from_table: str, from_column: str, to_table: str, to_column: str, is_both_directions: bool = ...) -> None: ...
    def load(self, data: RelationshipData): ...
    def dump(self) -> RelationshipData: ...
