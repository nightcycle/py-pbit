from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy
from pandas import DataFrame
from pbit.datamodelschema.column import DaxType

class MeasureProperty(TypedDict):
	property: str

class MeasureData(TypedDict):
	name: str
	expression: str
	formatString: str
	lineageTag: str
	dataType: DaxType

class Measure():
	name: str
	id: str
	expression: str
	data_type: DaxType
	format_string: str
	reference_data: MeasureData

	def __init__(
		self,
		name: str,
		data_type: DaxType
	):
		self.name = name
		self.id = str(uuid4())
		self.expression = ""
		self.data_type = data_type
		self.format_string = ""
		self.reference_data: MeasureData = {
			"name": self.name,
			"expression": self.expression,
			"formatString": self.format_string,
			"lineageTag": self.id,
			"dataType": self.data_type,
		}

	def set_format(self, format: str):
		self.format_string = format

	def set_expression(self, expression: str, data_type: DaxType):
		self.expression = expression
		self.data_type = data_type

	def set_to_retention_rate_tracker(self, user_table_name: str, is_retained_column_name: str):
		expression = f"COUNTROWS(FILTER({user_table_name}, {user_table_name}[{is_retained_column_name}]=True))/COUNTROWS({user_table_name})"
		self.set_expression(expression, "double")
		self.set_format("0.00%;-0.00%;0.00%")

	def load(self, data: MeasureData):
		self.reference_data = deepcopy(data)
		self.name = self.reference_data["name"]
		self.expression = self.reference_data["expression"]
		self.format_string = self.reference_data["formatString"]
		self.id = self.reference_data["lineageTag"]
		self.data_type = self.reference_data["dataType"]

	def dump(self) -> MeasureData:
		measure_data = deepcopy(self.reference_data)
		measure_data["name"] = self.name
		measure_data["expression"] = self.expression
		measure_data["formatString"] = self.format_string
		measure_data["lineageTag"] = self.id
		measure_data["dataType"] = self.data_type

		return measure_data
