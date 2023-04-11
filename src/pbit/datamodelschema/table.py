from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy
import pandas as pd
from .dax import DaxType
from .column import Column, ColumnData, SummaryType
from .partition import Partition, PartitionData
from .measure import Measure, MeasureData
from .typeholder import AnnotationData
from .powerquery import MType

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

class Table():
	name: str
	id: str
	columns: list[Column]
	partitions: list[Partition]
	measures: list[Measure]
	reference_data: TableData

	def __init__(
		self,
		name: str
	):
		self.name = name
		self.id = str(uuid4())
		self.columns: list[Column] = []
		self.partitions: list[Partition] = []
		self.measures: list[Measure] = []
		ref_data: Any = {
			"name": self.name,
			"lineageTag": self.id,
			"isHidden": None,
			"isPrivate": None,
			"showAsVariationsOnly": None,
			"hierarchies": None,
			"columns": [
				{
					"formatString": None,
					"dataCategory": None,
					"isNameInferred": None,
					"expression": None,
					"isDataTypeInferred": None,
					"sortByColumn": None,
					"type": "rowNumber",
					"name": "RowNumber-2662979B-1795-4F74-8F37-6A1BA8059B61",
					"dataType": "int64",
					"isHidden": True,
					"isUnique": True,
					"isKey": True,
					"isNullable": False,
					"lineageTag": None,
					"summarizeBy": None,
					"sourceColumn": None,
					"annotations": [
						{
							"name": "PBI_ResultType",
							"value": "Table"
						}
					],
					"attributeHierarchy": {
						"state": "ready"
					},
				},
			],
			"partitions": [],
			"measures": None,
			"annotations": [
				{
					"name": "PBI_ResultType",
					"value": "Table"
				}
			]
		}
		self.reference_data: TableData = ref_data

	def bind_to_json(
		self, 
		relative_json_path: str, 
		type_dictionary: dict[str, DaxType], 
		group_name: str | None = None
	):
		self.new_partition(group_name).set_to_json_reader(relative_json_path, type_dictionary)
		
		# add columns
		for name, col_type in type_dictionary.items():
			self.new_column(name, col_type, name)

	def new_partition(self, name="", language="m", query_group: str | None = None) -> Partition:
		if name == "":
			name = self.name

		partition = Partition(name, language, query_group)
		self.partitions.append(partition)
		return partition

	def get_if_column_exists(self, name: str) -> bool:
		for column in self.columns:
			# print(name, " =? ", column.name)
			if column.name == name:
				return True
		return False

	def get_column_by_name(self, name: str) -> Column:
		final_column: Column | None = None
		# print("column count: ", len(self.columns))
		for column in self.columns:
			# print(name, " =? ", column.name)
			if column.name == name:
				final_column = column
				break

		assert final_column, f"column {name} does not exist in table {self.name}"
		return final_column

	def new_column(
		self,
		name: str,
		data_type: DaxType,
		source_column: None | str = None
	) -> Column:
		if source_column == None and name != "":
			source_column = name

		assert self.get_if_column_exists(name) == False, f"column with name {name} in table {self.name} already exists!"

		column = Column(name, data_type, source_column)
		self.columns.append(column)
		return column

	def new_bin(self, target_column_name: str, increment: float, target_table_name: str | None = None,  bin_name: str | None = None, data_type: DaxType ="double") -> Column:
		final_table_name = ""
		if target_table_name:
			final_table_name = target_table_name
		else:
			final_table_name = self.name

		column = self.new_column(final_table_name, data_type)
		column.set_as_bin(final_table_name, target_column_name, increment, bin_name, data_type)
		return column

	def new_dax_column(self, dax: str, name: str, data_type: DaxType="double", summarize_by: SummaryType="sum") -> Column:
		column = self.new_column(name, data_type)
		column.set_dax(dax, name, data_type, summarize_by)
		return column
	
	def new_normalized_column(
		self,
		numerator_column_name: str,  
		denominator_column_name: str,
		denominator_table_name: None | str = None,
		name: None | str = None,
		data_type: DaxType="double",
		summarize_by: SummaryType="sum"
	):
		final_name: str = ""
		if name:
			final_name = name
		else:
			final_name = numerator_column_name+"_per_"+denominator_column_name
		
		final_denominator_table_name: str = ""
		if denominator_table_name == None:
			final_denominator_table_name = self.name
		else:
			final_denominator_table_name = denominator_table_name

		column = self.new_column(final_name, data_type)
		column.set_as_normalized(self.name, numerator_column_name, final_denominator_table_name, denominator_column_name, final_name, data_type, summarize_by)
		return column

	def new_measure(self, name: str) -> Measure:
		measure = Measure(name, "any")
		self.measures.append(measure)
		return measure

	def load(self, data: TableData):
		self.reference_data = deepcopy(data)
		if "name" in self.reference_data:
			name = self.reference_data["name"]
			assert name
			self.name = name

		self.id = self.reference_data["lineageTag"]

		for column_data in self.reference_data["columns"]:
			column = self.new_column("", "any")
			column.load(column_data)
		self.reference_data["columns"] = []

		for partition_data in self.reference_data["partitions"]:
			partition = self.new_partition("")
			partition.load(partition_data)

		self.reference_data["partitions"] = []

	def dump(self) -> TableData:
		table_data: TableData = deepcopy(self.reference_data)

		for column in self.columns:
			table_data["columns"].append(column.dump())

		for partition in self.partitions:
			table_data["partitions"].append(partition.dump())

		if len(self.measures) > 0:
			measure_list = []
			for measure in self.measures:
				measure_list.append(measure.dump())
			table_data["measures"] = measure_list

		return table_data
