import zipfile
import os
import shutil
import json
from pbit.report.__init__ import load as load_report
from pbit.report.__init__ import save as save_report
from pbit.report.__init__ import read_json_from_utf16_bytes, dump_json_to_utf16_bytes
from pbit.datamodelschema.__init__ import load as load_data_model_schema
from pbit.datamodelschema.__init__ import save as save_data_model_schema
from tempfile import TemporaryDirectory
from pbit.report.__init__ import Report, ReportData
from pbit.datamodelschema.__init__ import DataModelSchema, DataModelSchemaData
from typing import TypedDict
from copy import deepcopy

PBIT_TEMPLATE_PATH = "scripts/pbi/template.pbit"

class TemplateData(TypedDict):
	ReportData: ReportData
	DataModelSchema: DataModelSchemaData

def pack_pbti_file(dir_path: str, out_path: str):
	zip_path = dir_path + ".zip"

	# zip directory back up
	if os.path.exists(zip_path):
		os.remove(zip_path)
	zip_out = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
	for root, _, files in os.walk(dir_path):
		for file in files:
			# Construct the full file path
			file_path = os.path.join(root, file)
			# Construct the relative file path (relative to the directory being zipped)
			relative_path = os.path.relpath(file_path, dir_path)
			# Add the file to the ZIP file with the relative path as the archive name
			zip_out.write(file_path, arcname=relative_path)
	zip_out.close()

	# convert to pbit file in final position
	if os.path.exists(out_path):
		os.remove(out_path)
	shutil.move(zip_path, out_path)

def unpack_pbti_file(file_path: str, out_path: str):
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
		
def save(pbit_file_path: str, data: TemplateData):
	with TemporaryDirectory() as temp_dir_path:
		# clone file
		pbit_copy_file_path = temp_dir_path+"/file.pbit"
		shutil.copy(PBIT_TEMPLATE_PATH, pbit_copy_file_path)
		pbit_unpack_dir_path: str = temp_dir_path+"/pbit_file"
		unpack_pbti_file(pbit_copy_file_path, pbit_unpack_dir_path)

		# save to report and schema
		save_data_model_schema(pbit_unpack_dir_path+"/DataModelSchema", data["DataModelSchema"])
		# save_report(pbit_unpack_dir_path+"/Report/Layout", data["ReportData"])
		report_layout_file = open(pbit_unpack_dir_path+"/Report/Layout", "wb")
		report_layout_file.write(dump_json_to_utf16_bytes(data["ReportData"]))
		report_layout_file.close()

		pack_pbti_file(pbit_unpack_dir_path, pbit_file_path)

		shutil.rmtree(pbit_unpack_dir_path)
		os.remove(pbit_copy_file_path)

class Template():
	# report: Report
	data_model_schema: DataModelSchema
	original_report_data: ReportData | None
	def __init__(
		self,
		height=720,
		width=1280.0
	):
		# self.report = Report(height, width)
		self.data_model_schema = DataModelSchema()
		self.original_report_data = None

	def dump(self) -> TemplateData:
		return {
			"ReportData": deepcopy(self.original_report_data),
			"DataModelSchema": self.data_model_schema.dump()
		}

	def load(self, data: TemplateData):
		self.original_report_data = deepcopy(data["ReportData"])
		# self.report.load(data["ReportData"])
		self.data_model_schema.load(data["DataModelSchema"])

	def save(self, pbit_file_path: str):
		data = self.dump()
		# print("currently report-data can't be edited, previous version is used")
		# if self.original_report_data != None:
			# data["ReportData"] = deepcopy(self.original_report_data)
		save(pbit_file_path, data)


def load(pbit_file_path: str) -> Template:
	with TemporaryDirectory() as temp_dir_path:

		# clone file
		pbit_copy_path = temp_dir_path+"/copy.pbit"
		shutil.copy(pbit_file_path, pbit_copy_path)
		pbit_unpack_dir_path: str = temp_dir_path+"/pbit_file"
		unpack_pbti_file(pbit_copy_path, pbit_unpack_dir_path)

		template = Template()
		data: TemplateData = {
			"ReportData": read_json_from_utf16_bytes(open(pbit_unpack_dir_path+"/Report/Layout", "rb").read()),
			"DataModelSchema": load_data_model_schema(pbit_unpack_dir_path+"/DataModelSchema").dump(),
		}
		template.load(data)

		shutil.rmtree(pbit_unpack_dir_path)
		os.remove(pbit_copy_path)

		return template
