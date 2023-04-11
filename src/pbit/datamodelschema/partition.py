from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy
from pbit.datamodelschema.column import DaxType
from pbit.datamodelschema.powerquery import PowerQuery, MType, from_dax_type_to_m_type

class PartitionSourceData(TypedDict):
	type: str
	expression: list[str] | str

class PartitionData(TypedDict):
	name: str | None
	mode: str
	state: str
	queryGroup: str | None
	source: PartitionSourceData

class Partition():
	name: str | None
	language: str
	power_query: PowerQuery
	query_group: str | None
	reference_data: PartitionData

	def __init__(
		self,
		name: str | None = None,
		language: str = "m",
		query_group: str | None = None
	):
		self.name = name
		self.language = language
		self.power_query = PowerQuery()
		self.query_group = query_group
		self.reference_data: PartitionData = {
			"name": self.name,
			"mode": "import",
			"state": "ready",
			"queryGroup": self.query_group,
			"source": {
				"type": self.language,
				"expression": []
			}
		}

	def set_to_json_reader(
		self,
		relative_json_path: str,
		dax_types: dict[str, DaxType]
	):
		self.power_query.insert_read_file_cmd(relative_json_path)
		self.power_query.insert_load_as_json_cmd()
		self.power_query.insert_table_from_list_cmd()
		self.power_query.insert_expand_from_record_cmd(
			target_column="Column1",
			conversion_table=list(from_dax_type_to_m_type(dax_types).keys())
		)
		m_dax_types = from_dax_type_to_m_type(dax_types)
		self.power_query.insert_transform_dax_types_cmd(m_dax_types)

	def load(self, data: PartitionData):
		self.reference_data = deepcopy(data)
		if "name" in self.reference_data:
			self.name = self.reference_data["name"]
		if "queryGroup" in self.reference_data:
			self.query_group = self.reference_data["queryGroup"]
		else:
			self.query_group = None
		self.language =self.reference_data["source"]["type"]
		
	def dump(self) -> PartitionData:
		partition_data = deepcopy(self.reference_data)
		partition_data["name"] = self.name
		partition_data["queryGroup"] = self.query_group
		partition_data["source"]["type"] = self.language
		if len(self.power_query.commands) > 0:
			partition_data["source"]["expression"] = self.power_query.dump()

		return partition_data