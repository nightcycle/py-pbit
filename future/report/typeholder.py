from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy

TypeInteger = Literal[0]
AggregationFunction = Literal[1,2]
ExpressionKey = Literal["Column"]
EntityString = Literal["issues"]
EntitySource = Literal["i"]
OrderDirection = Literal[1,2]

class ColumnProperty(TypedDict):
	displayName: str

class LiteralValueData(TypedDict):
	Value: bool | str | int | float

class ValueData(TypedDict):
	Literal: LiteralValueData

class EntityData(TypedDict):
	Name: str
	Entity: str
	Type: TypeInteger

class ExpressionSourceRefData(TypedDict):
	Entity: EntityString | None
	Source: EntitySource | None

class MeasureData(TypedDict):
	Expression: ExpressionSourceRefData
	Property: str

class AggregationData(TypedDict):
	Function: AggregationFunction
	Expression: dict[ExpressionKey, MeasureData]

class ObjectPropertyData(TypedDict):
	expr: ValueData

class ObjectData(TypedDict):
	properties: dict[str, ObjectPropertyData]

class DimensionData(TypedDict):
	x: float
	y: float
	z: float
	width: float
	height: float

class SelectionData(TypedDict):
	Name: str
	Aggregation: AggregationData | None
	Measure: MeasureData

class OrderData(TypedDict):
	Direction: OrderDirection
	Expression: SelectionData

