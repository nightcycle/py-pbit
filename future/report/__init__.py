import inspect
import json
import os
import shutil
import zipfile
from typing import Any, TypedDict, Literal
from uuid import uuid4
from copy import deepcopy
from pbi.report.typeholder import ObjectData
from pbi.report.filter import FilterData, Filter, FilterType
from pbi.report.section import Section
from pbi.report.util import remove_none_values

ResourcePackageType = Literal[1, 2]
LinguisticSchemaSyncVersions = Literal[1, 2]
ExportDataMode = Literal[1]
ThemeType = Literal[1, 2]
ThemeNames = Literal["baseTheme"]
ReportObjectNames = Literal["section", "outspacePane"]
LayoutOptimization = Literal[0]

class ThemeData(TypedDict):
	name: str
	version: str
	type: ThemeType

class ResourcePackageItem(TypedDict):
	type: int
	path: str
	name: str

class ResourcePackage(TypedDict):
	name: str
	type: ResourcePackageType
	items: list[ResourcePackageItem]
	disabled: bool

class SlowDataSourceSettingsData(TypedDict):
	isCrossHighlightingDisabled: bool
	isSlicerSelectionsButtonEnabled: bool
	isFilterSelectionsButtonEnabled: bool
	isFieldWellButtonEnabled: bool
	isApplyAllButtonEnabled: bool

class ReportSettingsData(TypedDict):
	useNewFilterPaneExperience: bool
	allowChangeFilterTypes: bool
	useStylableVisualContainerHeader: bool
	exportDataMode: ExportDataMode
	useDefaultAggregateDisplayName: bool

class ReportConfigData(TypedDict):
	version: str
	themeCollection: dict[ThemeNames, ThemeData]
	activeSectionIndex: int
	defaultDrillFilterOtherVisuals: bool
	slowDataSourceSettings: SlowDataSourceSettingsData | None
	linguisticSchemaSyncVersion: LinguisticSchemaSyncVersions | None
	settings: ReportSettingsData
	objects: dict[ReportObjectNames, list[ObjectData]]

class ReportData(TypedDict):
	id: int
	filters: list[FilterData] | None
	resourcePackages: list
	sections: list
	config: ReportConfigData | str
	layoutOptimization: LayoutOptimization
	publicCustomVisuals: list[str] | None

DATA_ENCODING = "utf-16-le"

def read_json_from_utf16_bytes(utf16_bytes: bytes) -> dict | list:
	utf16_text = utf16_bytes.decode(DATA_ENCODING)
	json_data = json.loads(utf16_text)
	return json_data

def dump_json_to_utf16_bytes(json_data: dict | list) -> bytes:
	utf16_text = json.dumps(json_data, separators=(',', ':'))
	utf16_bytes = utf16_text.encode(DATA_ENCODING)
	return utf16_bytes

def read(layout_file_path: str) -> ReportData:

	file_bytes = open(layout_file_path, "rb").read()
	# json_data = file_bytes.decode("utf-16")
	json_dict = read_json_from_utf16_bytes(open(layout_file_path, "rb").read())

	def expand_tree(source: dict | list | str | int) -> dict | list | str | int:
		if type(source) == dict:
			for k, v in source.items():
				source[k] = expand_tree(v)
			return source

		elif type(source) == list:
			final_source = []
			for v in source:
				final_source.append(expand_tree(v))
			return final_source

		elif type(source) == str:
			try:
				final_source = json.loads(source)
				return expand_tree(final_source)
			except:
				return source

		return source

	report_data: Any = expand_tree(json_dict)

	return report_data


def unpack_report_file(file_path: str, out_path: str):
	base = os.path.split(out_path)[0]
	zip_path = base + ".zip"

	# convert to zip file
	if os.path.exists(zip_path):
		os.remove(zip_path)
	shutil.copy(file_path, zip_path)

	# unzip and extract data
	if os.path.exists(out_path):
		shutil.rmtree(out_path)
	zip_ref = zipfile.ZipFile(zip_path, 'r')
	zip_ref.extractall(out_path)
	zip_ref.close()


class Report():
	filters: list[Filter]
	id: int
	sections: list[Section]
	height: float
	width: float
	reference_data: ReportData

	def __init__(
		self,
		height=720,
		width=1280.0
	):
		self.id = uuid4().int
		self.filters = []
		self.sections = []
		self.height = height
		self.width = width
		self.reference_data = {
			"id": self.id,
			"filters": [],
			"publicCustomVisuals": None,
			"resourcePackages": [
				{
					"resourcePackage": {
						"name": "SharedResources",
						"type": 2,
						"items": [
							{
							"type": 202,
							"path": "BaseThemes/CY22SU11.json",
							"name": "CY22SU11"
							}
						],
						"disabled": False
					}
				}
			],
			"sections": [],
			"config": {
				"version": "5.40",
				"slowDataSourceSettings": None,
				"linguisticSchemaSyncVersion": None,
				"themeCollection": {
					"baseTheme": {
						"name": "CY22SU11",
						"version": "5.42",
						"type": 2
					}
				},
				"activeSectionIndex": 0,
				"defaultDrillFilterOtherVisuals": True,
				"settings": {
					"useNewFilterPaneExperience": True,
					"allowChangeFilterTypes": True,
					"useStylableVisualContainerHeader": True,
					"exportDataMode": 1,
					"useDefaultAggregateDisplayName": True
				},
				"objects": {
					"section": [
						{
							"properties": {
								"verticalAlignment": {
									"expr": {
										"Literal": {
											"Value": "'Top'"
										}
									}
								}
							}
						}
					]
				}
			},
			"layoutOptimization": 0
		}

	def new_section(self, name: str, layout_order: int, display_name="") -> Section:
		section = Section(name, layout_order, self.width, self.height, display_name)
		self.sections.append(section)
		return section

	def new_filter(self, variable_name: str, type: FilterType = "Categorical") -> Filter:
		data_filter = Filter(variable_name, type)
		self.filters.append(data_filter)
		return data_filter

	def dump(self) -> ReportData:

		report_data: ReportData = deepcopy(self.reference_data)
		report_data["id"] = self.id

		for section in self.sections:
			report_data["sections"].append(section.dump())

		filter_list = []
		for data_filter in self.filters:
			filter_list.append(data_filter.dump())
		report_data["filters"] = filter_list

		report_data["config"] = json.dumps(remove_none_values(report_data["config"]), indent=None)
		report_data["config"] = report_data["config"]

		return deepcopy(report_data)

	def load(self, data: ReportData):
		self.reference_data = deepcopy(data)
		self.id = 0 ##self.reference_data["id"]
		self.height = 0
		self.width = 0
		self.filters = []
		self.sections = []

		if "filters" in self.reference_data:
			filter_list = self.reference_data["filters"]
			if filter_list and len(filter_list) > 0:
				assert filter_list
				for filter_data in filter_list:
					data_filter = self.new_filter("", filter_data["type"])
					data_filter.load(filter_data)
			self.reference_data["filters"] = []

		for i, section_data in enumerate(self.reference_data["sections"]):
			section = self.new_section("", i)
			section.load(section_data)
			self.height = max(self.height, section.height)
			self.width = max(self.height, section.width)
		self.reference_data["sections"] = []

	def save(self, out_path: str):
		out_file = open(out_path, "wb")
		report_data: ReportData = self.dump()


		# write to DataModelSchema
		report_data = remove_none_values(report_data)

		data_bytes_in = open("template/Report/Layout", "rb").read()
		data = read_json_from_utf16_bytes(data_bytes_in)
		# data["sections"].append(json.loads(open("visual_test.json", "r").read()))
		# data["sections"] = deepcopy(report_data["sections"])
		# report_data["config"] = data["config"]

		out_file.write(dump_json_to_utf16_bytes(report_data))
		out_file.close()	

def save(layout_file_path: str, report_data: ReportData):
	report = Report()
	report.load(report_data)
	report.save(layout_file_path)

def load(layout_file_path: str) -> Report:
	# print("P A T H", layout_file_path)
	data = read(layout_file_path)
	report = Report(0, 0)
	report.load(data)

	return report		