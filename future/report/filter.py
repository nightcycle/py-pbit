from typing import TypedDict, Literal, Any, Union
from uuid import uuid4
from copy import deepcopy
from pbi.report.typeholder import ValueData, ObjectData, TypeInteger, ExpressionSourceRefData, ExpressionKey, EntityString

# high level patterns
ConditionOrder = Literal["In"]
FilterType = Literal["Categorical"]
CreationInteger = Literal[1]
FilterObjectPropertyNames = Literal["isInvertedSelectionMode"]

class ExpressionSourceData(TypedDict):
	SourceRef: ExpressionSourceRefData

class ExpressionConfigData(TypedDict):
	Expression: ExpressionSourceData
	Property: str

class FilterParamaterConfigData:
	Expressions: list[dict[ExpressionKey, ExpressionConfigData]]
	Values: list[list[ValueData]]

class WhereFilterParameterData(TypedDict):
	Condition: dict[ConditionOrder, FilterParamaterConfigData]

class FromFilterParameterData(TypedDict):
	Name: str
	Entity: EntityString
	Type: TypeInteger

class SubFilterData(TypedDict):
	Version: int
	From: list[FromFilterParameterData]
	Where: list[WhereFilterParameterData]

class FilterExpressionData(TypedDict):
	name: str
	expression: ExpressionSourceData
	filter: SubFilterData

class FilterObjectRegistryData(TypedDict):
	general: ObjectData

class FilterData(TypedDict):
	name: str
	expression: dict[ExpressionKey, FilterExpressionData]
	filter: SubFilterData
	type: FilterType
	howCreated: CreationInteger
	objects: Union[FilterObjectRegistryData, dict[str, ObjectData]]

class Filter():
	def __init__(
		self,
		variable_name: str,
		type: FilterType = "Categorical"
	):

		self.id = str(uuid4())
		self.variable_name = variable_name
		self.type: FilterType = type	
		filter_data: Any = {
			"name": self.id,
			"expression": {},
			"filter": {},
			"type": self.type,
			"howCreated": 1,
			"objects": {
				"general": [
					{
						"properties": {}
					}
				]
			}
		},
		self.reference_data: FilterData = filter_data
	def load(self, data: FilterData):
		self.reference_data = deepcopy(data)
		self.id = self.reference_data["name"]
		self.type = self.reference_data["type"]

	def dump(self) -> FilterData:
		filter_data: FilterData = deepcopy(self.reference_data)
		filter_data["name"] = self.id
		filter_data["type"] = self.type
		return filter_data