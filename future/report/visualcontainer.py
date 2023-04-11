
from typing import TypedDict, Literal, Any
from uuid import uuid4
from copy import deepcopy
from pbi.report.filter import FilterData, Filter, FilterType
from pbi.report.typeholder import ObjectPropertyData, EntityData, SelectionData, OrderData, ColumnProperty, DimensionData

DisplayOption = Literal[1,2]
VisualType = Literal["multiRowCard", "lineChart"]
LayerObjectPropertyNames = Literal["mode", "show", "fontSize", "bold", "keepLayerOrder"]
LayerObjectMode = Literal["'Between'"]
SingleLayerObjectNames = Literal["categoryLabels", "dataLabels"]
SingleVCLayerObjectNames = Literal["visualHeader", "title", "general"]
SingleVisualProjectionPropertyNames = Literal["Y", "Category", "Values"]
PrototypeQueryVersion = Literal[1,2]

class PrototypeQueryData(TypedDict):
	Version: PrototypeQueryVersion
	From: list[EntityData]
	Select: list[SelectionData]
	OrderBy: list[OrderData]

class QueryReference(TypedDict):
	queryRef: str

class LayerObjectData(TypedDict):
	properties: dict[LayerObjectPropertyNames, ObjectPropertyData]

class SingleVisualData(TypedDict):
	visualType: VisualType
	projects: dict[SingleVisualProjectionPropertyNames, list[QueryReference]]
	prototypeQuery: PrototypeQueryData
	columnProperties: dict[str, ColumnProperty]
	drillFilterOtherVisuals: bool
	hasDefaultSort: bool
	objects: dict[SingleLayerObjectNames, LayerObjectData]
	vcObjects: dict[SingleVCLayerObjectNames, LayerObjectData]

class VisualContainerLayoutData(TypedDict):
	id: int
	position: DimensionData

class VisualContainerConfigData(TypedDict):
	name: str
	layouts: list[VisualContainerLayoutData]
	singleVisual: SingleVisualData

class VisualContainerData(DimensionData):
	config: VisualContainerConfigData
	filters: list[FilterData] | None

class VisualContainer():
	def __init__(
		self,
		type: VisualType,
		x: float,
		y: float,
		z: float,
		width: float,
		height: float
	):
		self.name = str(uuid4())
		self.x = x
		self.y = y
		self.z = z
		self.type = type
		self.width = width
		self.height = height
		self.filters: list[Filter] = []

		default_ref_data: Any = {
			"x": self.x,
			"y": self.y,
			"z": self.z,
			"width": self.width,
			"height": self.height,
			"config": {
				"name": str(self.name),
				"layouts": [
					{
						"id": 0,
						"position": {
							"x": self.x,
							"y": self.y,
							"z": self.z,
							"width": self.width,
							"height": self.height
						}
					}
				],
				"singleVisual": {
					"visualType": self.type,
					"projections": {
						"Values": []
					},
					"prototypeQuery": {
						"Version": 2,
						"From": [],
						"Select": [],
						"OrderBy": []
					},
					"columnProperties": {},
					"drillFilterOtherVisuals": True,
					"hasDefaultSort": True,
					"objects": {},
					"vcObjects": {}
				}
			},
			"filters": []
		},

		self.reference_data: VisualContainerData = default_ref_data

	def load(self, data: VisualContainerData):
		self.reference_data = deepcopy(data)
		self.name = self.reference_data["config"]["name"]
		self.width = self.reference_data["width"]
		self.height = self.reference_data["height"]
		self.x = self.reference_data["config"]["layouts"][0]["position"]["x"]
		self.y = self.reference_data["config"]["layouts"][0]["position"]["y"]
		self.z = self.reference_data["config"]["layouts"][0]["position"]["z"]
		self.filters = []

		if "filters" in self.reference_data:
			filter_list = self.reference_data["filters"]
			if filter_list and len(filter_list) > 0:
				for filter_data in filter_list:
					data_filter = self.new_filter("", filter_data["type"])
					data_filter.load(filter_data)

				self.reference_data["filters"] = []

	def new_filter(self, variable_name: str, type: FilterType = "Categorical") -> Filter:
		data_filter = Filter(variable_name, type)
		self.filters.append(data_filter)
		return data_filter

	def dump(self) -> VisualContainerData:
		visual_container_data = deepcopy(self.reference_data)
		visual_container_data["x"] = self.x
		visual_container_data["y"] = self.y
		visual_container_data["z"] = self.z
		visual_container_data["width"] = self.width
		visual_container_data["height"] = self.height
		visual_container_data["config"]["name"] = str(self.name)
		visual_container_data["config"]["layouts"][0] = {
			"id": 0,
			"position": {
				"x": self.x,
				"y": self.y,
				"z": self.z,
				"width": self.width,
				"height": self.height
			}
		}
		visual_container_data["config"]["singleVisual"]["visualType"] = self.type
		
		filter_list = []
		for data_filter in self.filters:
			filter_list.append(data_filter.dump())

		visual_container_data["filters"] = filter_list

		return visual_container_data

