from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy

class RelationshipData(TypedDict):
	name: str
	fromTable: str
	fromColumn: str
	toTable: str
	toColumn: str
	joinOnDateBehavior: str
	crossFilteringBehavior: str | None
	state: str

class Relationship():
	name: str
	from_table: str
	from_column: str
	to_table: str
	to_column: str
	is_both_directions: bool
	reference_data: RelationshipData

	def __init__(
		self,
		from_table: str,
		from_column: str,
		to_table: str,
		to_column: str,
		is_both_directions=True
	):
		self.name = str(uuid4())
		self.from_table = from_table
		self.from_column = from_column
		self.to_table = to_table
		self.to_column = to_column
		self.is_both_directions=is_both_directions

		self.reference_data: RelationshipData = {
			"name": self.name,
			"fromTable": self.from_table,
			"fromColumn": self.from_column,
			"toTable": self.to_table,
			"toColumn": self.to_column,
			"crossFilteringBehavior": "bothDirections",
			"joinOnDateBehavior": "datePartOnly",
			"state": "ready"
		}

		if not self.is_both_directions:
			self.reference_data["crossFilteringBehavior"] = "oneDirection"
		else:
			self.reference_data["crossFilteringBehavior"] = "bothDirections"

	def load(self, data: RelationshipData):
		self.reference_data = deepcopy(data)
		self.name = self.reference_data["name"]
		self.from_table = self.reference_data["fromTable"]
		self.from_column = self.reference_data["fromColumn"]
		self.to_table = self.reference_data["toTable"]
		self.to_column = self.reference_data["toColumn"]
		if "crossFilteringBehavior" in self.reference_data:
			if self.reference_data["crossFilteringBehavior"] == "bothDirections":
				self.is_both_directions = True
			else:
				self.is_both_directions = False
		else:
			self.is_both_directions = True

	def dump(self) -> RelationshipData:
		relationship_data = deepcopy(self.reference_data)
		relationship_data["name"] = self.name
		relationship_data["fromTable"] = self.from_table
		relationship_data["fromColumn"] = self.from_column
		relationship_data["toTable"] = self.to_table
		relationship_data["toColumn"] = self.to_column

		if not self.is_both_directions:
			relationship_data["crossFilteringBehavior"] = "oneDirection"
		else:
			relationship_data["crossFilteringBehavior"] = "bothDirections"

		return relationship_data
