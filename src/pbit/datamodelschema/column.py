from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy
from pbit.datamodelschema.dax import DaxType
from pbit.datamodelschema.typeholder import AnnotationData

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

class Column():
	name: str
	id: str
	data_type: str
	source_column: str | None
	reference_data: ColumnData

	def __init__(
		self,
		name: str,
		dataType: str,
		source_column: str | None = None
	):
		self.name = name
		self.id = str(uuid4())
		self.data_type = dataType
		self.source_column = source_column
		self.reference_data: ColumnData = {
			"formatString": None,
			"dataCategory": None,
			"isNameInferred": None,
			"expression": None,
			"isDataTypeInferred": None,
			"sortByColumn": None,
			"type": None,
			"isHidden": None,
			"isUnique": None,
			"isKey": None,
			"isNullable": None,
			"name": self.name,
			"dataType": self.data_type,
			"sourceColumn": self.source_column,
			"lineageTag": self.id,
			"summarizeBy": "none",
			"attributeHierarchy": {
				"state": "ready"
			},
			"annotations": [
				{
					"name": "SummarizationSetBy",
					"value": "Automatic"
				}
			]
		}

	def set_as_bin(self, target_table_name: str, target_column_name: str, increment: float, bin_name: str | None = None, data_type: DaxType="double"):
		final_name: str = ""
		if bin_name:
			final_name = bin_name
		else:
			final_name = target_column_name + "_bin"
		
		reference_data: Any = {
			"type": "calculated",
			"name": final_name,
			"dataType": data_type,
			"isDataTypeInferred": True,
			"expression": [
				"IF(",
				f"\tISBLANK('{target_table_name}'[{target_column_name}]),",
				"\tBLANK(),",
				"\tIF(",
				f"\t\t'{target_table_name}'[{target_column_name}] >= 0,",
				f"\t\tROUNDDOWN('{target_table_name}'[{target_column_name}] / {increment}, 0) * {increment},",
				f"\t\tROUNDUP('{target_table_name}'[{target_column_name}] / {increment}, 0) * {increment}",
				"\t)",
				")"
			],
			"lineageTag": self.id,
			"summarizeBy": "none",
			"attributeHierarchy": {
				"state": "ready"
			},
			"extendedProperties": [
				{
					"type": "json",
					"name": "GroupingMetadata",
					"value": {
						"version": 0,
						"groupedColumns": [
							{
								"Column": {
									"Expression": {
										"SourceRef": {
											"Entity": target_table_name
										}
									},
									"Property": target_column_name
								}
							}
						],
						"binningMetadata": {
							"binSize": {
								"value": 5.0,
								"unit": 0
							}
						}
					}
				}
			],
			"annotations": [
				{
					"name": "GroupingDesignState",
					"value": "{\"Version\":0,\"Sources\":[{\"Name\":\"p\",\"Entity\":\""
						+target_table_name+"\"}],\"GroupedColumns\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"p\"}},\"Property\":\""
						+target_column_name+"\"}}],\"BinItem\":{\"Expression\":{\"Floor\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"p\"}},\"Property\":\""
						+target_column_name+"\"}},\"Size\":"
						+str(increment)+"}}}}"
				},
				{
					"name": "SummarizationSetBy",
					"value": "Automatic"
				},
				{
					"name": "PBI_FormatHint",
					"value": "{\"isGeneralNumber\":true}"
				}
			]
		}
		self.load(reference_data)

	def load(self, data: ColumnData):
		self.reference_data = deepcopy(data)
		self.name = self.reference_data["name"]
		self.data_type = self.reference_data["dataType"]
		if "sourceColumn" in self.reference_data:
			source_column_ref = self.reference_data["sourceColumn"]
			assert source_column_ref
			self.source_column = source_column_ref
		
		if "lineageTag" in self.reference_data:
			lin_tag = self.reference_data["lineageTag"]
			assert lin_tag
			self.id = lin_tag

	def dump(self) -> ColumnData:
		column_data: ColumnData = deepcopy(self.reference_data)
		column_data["name"] = self.name
		column_data["dataType"] = self.data_type
		if column_data["dataType"] == "any":
			column_data["dataType"] = "string"

		column_data["sourceColumn"] = self.source_column
		column_data["lineageTag"] = self.id

		return column_data
