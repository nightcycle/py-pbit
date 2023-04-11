import shutil
import os
import zipfile
from tempfile import TemporaryDirectory
from .datamodelschema import read as read_pbit
from .datamodelschema import write as write_pbit
from .datamodelschema import DataModelSchema, DataModelSchemaData

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
		
def write_model(pbit_file_path: str, source: DataModelSchemaData | DataModelSchema):
	with TemporaryDirectory() as temp_dir_path:
		pbti_dir = temp_dir_path + "/pbit"
		unpack_pbti_file(pbit_file_path, pbti_dir)
		if type(source) == DataModelSchema:
			write_pbit(pbti_dir+"/DataModelSchema", source.dump())
		elif type(source) == DataModelSchemaData:
			write_pbit(pbti_dir+"/DataModelSchema", source)
		pack_pbti_file(pbti_dir, pbit_file_path)	

def read_model(pbit_file_path: str) -> DataModelSchemaData:
	with TemporaryDirectory() as temp_dir_path:
		pbti_dir = temp_dir_path + "/pbit"
		unpack_pbti_file(pbit_file_path, pbti_dir)
		return read_pbit(pbti_dir+"/DataModelSchema")

def load_model(pbit_file_path: str) -> DataModelSchema:
	return DataModelSchema(read_model(pbit_file_path))
