import json
import inspect
from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy
from .typeholder import AnnotationData
from .relationship import RelationshipData, Relationship
from .table import TableData, Table

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

def get_default_table() -> TableData:
	untyped_default_table_a: Any = {
		"name": "DateTableTemplate_5975b0d6-7e08-4fc8-b30a-36e3eba94689",
		"isHidden": True,
		"isPrivate": True,
		"lineageTag": "e21631ac-035c-440b-85ef-3259718d8da4",
		"showAsVariationsOnly": None,
		"columns": [
			{
				"type": "rowNumber",
				"name": "RowNumber-2662979B-1795-4F74-8F37-6A1BA8059B61",
				"dataType": "int64",
				"isHidden": True,
				"isUnique": True,
				"isKey": True,
				"isNullable": False,
				"attributeHierarchy": {
					"state": "ready"
				}
			},
			{
				"type": "calculatedTableColumn",
				"name": "Date",
				"dataType": "dateTime",
				"isNameInferred": True,
				"isDataTypeInferred": True,
				"isHidden": True,
				"sourceColumn": "[Date]",
				"formatString": "General Date",
				"lineageTag": "889a51f9-99f0-4aa3-9e63-278d77d00ee1",
				"dataCategory": "PaddedDateTableDates",
				"summarizeBy": "none",
				"attributeHierarchy": {
					"state": "ready"
				},
				"annotations": [
					{
						"name": "SummarizationSetBy",
						"value": "User"
					}
				]
			},
			{
				"type": "calculated",
				"name": "Year",
				"dataType": "int64",
				"isDataTypeInferred": True,
				"isHidden": True,
				"expression": "YEAR([Date])",
				"formatString": "0",
				"lineageTag": "94dfb75d-4ba9-4b90-b79f-ebfe9cff087b",
				"dataCategory": "Years",
				"summarizeBy": "none",
				"attributeHierarchy": {
					"state": "ready"
				},
				"annotations": [
					{
						"name": "SummarizationSetBy",
						"value": "User"
					},
					{
						"name": "TemplateId",
						"value": "Year"
					}
				]
			},
			{
				"type": "calculated",
				"name": "MonthNo",
				"dataType": "int64",
				"isDataTypeInferred": True,
				"isHidden": True,
				"expression": "MONTH([Date])",
				"formatString": "0",
				"lineageTag": "98761376-1dab-48da-b6ff-b5851336dc89",
				"dataCategory": "MonthOfYear",
				"summarizeBy": "none",
				"attributeHierarchy": {
				"state": "ready"
				},
				"annotations": [
					{
						"name": "SummarizationSetBy",
						"value": "User"
					},
					{
						"name": "TemplateId",
						"value": "MonthNumber"
					}
				]
			},
			{
				"type": "calculated",
				"name": "Month",
				"dataType": "string",
				"isDataTypeInferred": True,
				"isHidden": True,
				"expression": "FORMAT([Date], \"MMMM\")",
				"sortByColumn": "MonthNo",
				"lineageTag": "5b5f8789-885b-493c-a768-416efed357a8",
				"dataCategory": "Months",
				"summarizeBy": "none",
				"attributeHierarchy": {
					"state": "ready"
				},
				"annotations": [
					{
						"name": "SummarizationSetBy",
						"value": "User"
					},
					{
						"name": "TemplateId",
						"value": "Month"
					}
				]
			},
			{
				"type": "calculated",
				"name": "QuarterNo",
				"dataType": "int64",
				"isDataTypeInferred": True,
				"isHidden": True,
				"expression": "INT(([MonthNo] + 2) / 3)",
				"formatString": "0",
				"lineageTag": "30244721-a2b3-4014-81b5-bf95d8f344da",
				"dataCategory": "QuarterOfYear",
				"summarizeBy": "none",
				"attributeHierarchy": {
					"state": "ready"
				},
				"annotations": [
					{
						"name": "SummarizationSetBy",
						"value": "User"
					},
					{
						"name": "TemplateId",
						"value": "QuarterNumber"
					}
				]
			},
			{
				"type": "calculated",
				"name": "Quarter",
				"dataType": "string",
				"isDataTypeInferred": True,
				"isHidden": True,
				"expression": "\"Qtr \" & [QuarterNo]",
				"sortByColumn": "QuarterNo",
				"lineageTag": "5de8ea71-ebc4-4fff-9b6d-3f3e00bf3d20",
				"dataCategory": "Quarters",
				"summarizeBy": "none",
				"attributeHierarchy": {
					"state": "ready"
				},
				"annotations": [
					{
						"name": "SummarizationSetBy",
						"value": "User"
					},
					{
						"name": "TemplateId",
						"value": "Quarter"
					}
				]
			},
			{
				"type": "calculated",
				"name": "Day",
				"dataType": "int64",
				"isDataTypeInferred": True,
				"isHidden": True,
				"expression": "DAY([Date])",
				"formatString": "0",
				"lineageTag": "9070e261-708c-4cb3-96cd-826a7cda38e8",
				"dataCategory": "DayOfMonth",
				"summarizeBy": "none",
				"attributeHierarchy": {
					"state": "ready"
				},
				"annotations": [
					{
						"name": "SummarizationSetBy",
						"value": "User"
					},
					{
						"name": "TemplateId",
						"value": "Day"
					}
				]
			}
		],
		"partitions": [
			{
				"name": "DateTableTemplate_5975b0d6-7e08-4fc8-b30a-36e3eba94689-1d04c13d-f7a1-4dae-aa9a-1a3a3400b609",
				"mode": "import",
				"state": "ready",
				"source": {
					"type": "calculated",
					"expression": "Calendar(Date(2015,1,1), Date(2015,1,1))"
				}
			}
		],
		"hierarchies": [
			{
				"name": "Date Hierarchy",
				"lineageTag": "bbe0ed27-e8ef-4e76-8a14-85f0fcb1d594",
				"state": "ready",
				"levels": [
					{
						"name": "Year",
						"ordinal": 0,
						"column": "Year",
						"lineageTag": "08329d53-fa1d-4986-8a37-f3873dee4e07"
					},
					{
						"name": "Quarter",
						"ordinal": 1,
						"column": "Quarter",
						"lineageTag": "e5d11cdc-593c-43de-996b-b6040b2a678a"
					},
					{
						"name": "Month",
						"ordinal": 2,
						"column": "Month",
						"lineageTag": "9e3fbfab-5920-462c-a4af-236b9952ac84"
					},
					{
						"name": "Day",
						"ordinal": 3,
						"column": "Day",
						"lineageTag": "1b872e0f-440e-4e03-a2b4-4e87841b1489"
					}
				],
				"annotations": [
					{
						"name": "TemplateId",
						"value": "DateHierarchy"
					}
				]
			}
		],
		"annotations": [
			{
				"name": "__PBI_TemplateDateTable",
				"value": "True"
			},
			{
				"name": "DefaultItem",
				"value": "DateHierarchy"
			}
		]
	}
	return untyped_default_table_a

# write to DataModelSchema
def remove_none_values(dct):
	# Create a list of keys to be removed (to avoid changing dictionary size during iteration)
	keys_to_remove = []
	for key_val in dct:
		value = key_val
		key = key_val
		if type(dct) != list and type(key_val) == str:
			value = dct[key_val]

		if value is None and type(dct) != list:
			keys_to_remove.append(key)
		elif inspect.isclass(value) or type(value) == list or type(value) == dict:
			remove_none_values(value)
	# Remove keys with None values
	for key in keys_to_remove:
		dct.pop(key)
	return dct


class DataModelSchema():
	relationships: list[Relationship]
	tables: list[Table]
	query_groups: list[str]
	reference_data: DataModelSchemaData
	def __init__(
		self
	):
		self.relationships = []
		self.tables = []
		self.query_groups = []	
		self.id = str(uuid4())
		self.reference_data = {
			"name": self.id,
			"compatibilityLevel": 1550,
			"model": {
				"culture": "en-US",
				"dataAccessOptions": {
					"legacyRedirects": True,
					"returnErrorValuesAsNull": True
				},
				"defaultPowerBIDataSourceVersion": "powerBI_V3",
				"sourceQueryCulture": "en-US",
				"tables": [],
				"relationships": [],
				"cultures": [
					{
						"name": "en-US",
						"linguisticMetadata": {
							"content": {
								"Version": "1.0.0",
								"Language": "en-US",
								"DynamicImprovement": "HighConfidence"
							},
							"contentType": "json"
						},
					},
				],
				"queryGroups": None,
				"annotations": [
					{
						"name": "PBI_QueryOrder",
						"value": "[\"31_2023-3-29-04c00c00p000000\"]"
					},
					{
						"name": "__PBI_TimeIntelligenceEnabled",
						"value": "1"
					},
					{
						"name": "PBIDesktopVersion",
						"value": "2.115.842.0"
					}
				]
			},
		}

		self.reference_data["model"]["tables"].append(get_default_table())

	def clear_tables(self):
		self.tables = []
		if "model" in self.reference_data:
			model_data = self.reference_data["model"]
			if "tables" in model_data:
				model_data["tables"] = []

	def clear_relationships(self): 
		self.relationships = []
		if "model" in self.reference_data:

			model_data = self.reference_data["model"]
			if "relationships" in model_data:
				model_data["relationships"] = []

	def clear_query_groups(self):
		self.query_groups = []
		if "model" in self.reference_data:
			model_data = self.reference_data["model"]
			if "queryGroups" in model_data:
				model_data["queryGroups"] = []

	def clear(self):
		self.clear_tables()
		self.clear_relationships()
		self.clear_query_groups()			

	def get_table_by_name(self, name: str) -> Table:
		final_table: Table | None
		for table in self.tables:
			if table.name == name:
				final_table = table
				break
		assert final_table, f"table {name} does not exist"
		return final_table
	
	def insert_query_group(self, group_name: str):
		self.query_groups.append(group_name)

	def new_relationship(
			self,
			from_table: str,
			from_column: str,
			to_table: str,
			to_column=""
		) -> Relationship:

		if to_column == "":
			to_column = from_column

		is_safe = True
		for relationship in self.relationships:
			if relationship.from_table == from_table and relationship.to_table == to_table:
				is_safe = False
			elif relationship.to_table == from_table and relationship.from_table == to_table:
				is_safe = False

		assert is_safe == True, f"there's already an active relationship between table {from_table} and {to_table}"
			
		relationship = Relationship(from_table, from_column, to_table, to_column)
		self.relationships.append(relationship)

		return relationship

	def new_table(self, name: str) -> Table:
		table = Table(name)
		self.tables.append(table)
		return table

	def load(self, schema_data: DataModelSchemaData):
		self.reference_data = deepcopy(schema_data)
		
		# print(json.dumps(self.reference_data, indent=4))

		ref_model_data: ModelData | None = None

		untyped_ref: Any = self.reference_data
		untyped_ref_data = untyped_ref["model"]
		dict_mod_data: ModelData = untyped_ref_data
		ref_model_data = dict_mod_data

		assert ref_model_data

		self.relationships = []
		self.tables = []
		self.query_groups = []

		if "relationships" in ref_model_data:
			rel_list = ref_model_data["relationships"]
			assert rel_list
			for relationship_data in rel_list:
				relationship = self.new_relationship("", "", "")
				relationship.load(relationship_data)
			ref_model_data["relationships"] = []

		if "tables" in ref_model_data:
			tab_list = ref_model_data["tables"]
			assert tab_list
			for i , table_data in enumerate(tab_list):
				table = self.new_table("")
				table.load(table_data)
			# ref_model_data["tables"] = [get_default_table()]

		if "queryGroups" in ref_model_data and ref_model_data["queryGroups"] != None:
			ref_groups = ref_model_data["queryGroups"]
			assert ref_groups
			for query_group_data in ref_groups:
				self.query_groups.append(query_group_data["folder"])
			ref_model_data["queryGroups"] = None

	def dump(self) -> DataModelSchemaData:
		data_model_schema = deepcopy(self.reference_data)

		model_data: ModelData | None = None
	
		untyped_ref: Any = data_model_schema
		untyped_ref["name"] = self.id
		untyped_ref_data = untyped_ref["model"]
		dict_mod_data: ModelData = untyped_ref_data
		model_data = dict_mod_data

		assert model_data

		if not "dataAccessOptions" in model_data:
			model_data["dataAccessOptions"] = {}

		model_data["dataAccessOptions"]["legacyRedirects"] = True
		model_data["dataAccessOptions"]["returnErrorValuesAsNull"] = True
		model_data["defaultPowerBIDataSourceVersion"] = "powerBI_V3"
		model_data["sourceQueryCulture"] = "en-US"
		if len(self.query_groups) > 0:
			query_group_data_list = []
			for i, group_name in enumerate(self.query_groups):
				query_group_data: QueryGroupData = {
					"folder": group_name,
					"annotations": [
						{
							"name": "PBI_QueryGroupOrder",
							"value": str(i)
						}
					]
				}
				query_group_data_list.append(query_group_data)

			model_data["queryGroups"] = query_group_data_list

		table_list = []

		for table in self.tables:
			table_list.append(table.dump())

		if len(table_list) > 0 or "tables" in model_data:
			model_data["tables"] = table_list

		relationship_list = []

		for relationship in self.relationships:
			relationship_list.append(relationship.dump())

		if len(relationship_list) > 0 or "relationships" in model_data:
			model_data["relationships"] = relationship_list

		return remove_none_values(data_model_schema)

def write(schema_file_path: str, data: DataModelSchemaData):
	file = open(schema_file_path, "w", encoding="utf-16-le")
	file.write(json.dumps(data, indent=4))
	file.close()

def read(schema_file_path: str) -> DataModelSchema:
	return json.loads(open(schema_file_path, "r", encoding="utf-16-le").read())

