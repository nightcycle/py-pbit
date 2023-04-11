
from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy
from pbi.report.filter import ExpressionSourceRefData, ExpressionKey, FilterData, Filter, FilterType
from pbi.report.visualcontainer import VisualContainerData, DisplayOption, VisualContainer, VisualType
from pbi.report.typeholder import EntityData, ObjectPropertyData
from pbi.report.util import remove_none_values
import json
SectionObjectNames = Literal["background", "outspace", "outspacePane"]
SectionSolidColorPropertyNames = Literal["color"]

class SectionObjectColorData(TypedDict):
	solid: dict[SectionSolidColorPropertyNames, ObjectPropertyData]

class SectionObjectPropertyRegistryData(TypedDict):
	color: SectionObjectColorData | None
	width: ObjectPropertyData

class SectionConfigData(TypedDict):
	objects: dict[SectionObjectNames, list[SectionObjectPropertyRegistryData]]

class SectionData(TypedDict):
	id: int
	name: str
	displayName: str
	filters: list[FilterData] | None
	ordinal: int
	visualContainers: list[VisualContainerData]
	config: SectionConfigData | str
	displayOption: DisplayOption
	width: float
	height: float


class Section():
	def __init__(
		self,
		name: str,
		layout_order: int,
		width: float,
		height: float,
		display_name="",
	):
		if display_name == "":
			display_name = name

		self.id = uuid4().int
		self.name = name
		self.display_name = display_name
		self.filters: list[Filter] = []
		self.layout_order = layout_order
		self.visual_containers: list[VisualContainer] = []
		self.width = width
		self.height = height
		self.reference_data: SectionData = {
			"id": self.id,
			"name": self.name,
			"displayName": self.display_name,
			"filters": [],
			"ordinal": self.layout_order,
			"visualContainers": [],
			"config": {},
			"displayOption": 1,
			"width": self.height,
			"height": self.width
		}

	def new_visual_container(self, type: VisualType, x: float, y: float, z: float, width: float, height: float) -> VisualContainer:
		visual_container = VisualContainer(type, x, y, z, width, height)
		self.visual_containers.append(visual_container)
		return visual_container

	def new_filter(self, variable_name: str, type: FilterType = "Categorical") -> Filter:
		data_filter = Filter(variable_name, type)
		self.filters.append(data_filter)
		return data_filter

	def load(self, data: SectionData):
		self.reference_data = deepcopy(data)
		self.id = self.reference_data["id"]
		self.name = self.reference_data["name"]
		self.display_name = self.reference_data["displayName"]
		self.layout_order = self.reference_data["ordinal"]
		self.width = self.reference_data["width"]
		self.height = self.reference_data["height"]
		self.visual_containers = []
		self.filters = []

		for container_data in self.reference_data["visualContainers"]:
			visual_container = self.new_visual_container("multiRowCard", 0, 0, 0, 0, 0)
			visual_container.load(container_data)
		self.reference_data["visualContainers"] = []

		if "filters" in self.reference_data:
			filter_list = []
			if type(self.reference_data["filters"]) == str:
				filter_list = json.loads(self.reference_data["filters"])
			else:
				filter_list = self.reference_data["filters"]
			if filter_list and len(filter_list) > 0:
				assert filter_list
				print(json.dumps(self.reference_data, indent=4))
				for filter_data in filter_list:
					
					data_filter = self.new_filter("", filter_data["type"])
					data_filter.load(filter_data)

				self.reference_data["filters"] = []

	def dump(self) -> SectionData:
		section_data: SectionData = deepcopy(self.reference_data)
		section_data["id"] = self.id
		section_data["name"] = self.name
		section_data["displayName"] = self.display_name
		section_data["ordinal"] = self.layout_order
		section_data["width"] = self.width
		section_data["height"] = self.height

		for visual_container in self.visual_containers:
			section_data["visualContainers"].append(visual_container.dump())
	
		filter_list = []

		for data_filter in self.filters:
			filter_list.append(data_filter.dump())

		section_data["filters"] = filter_list

		section_data["config"] = json.dumps(remove_none_values(section_data["config"]), indent=None)
		
		return section_data