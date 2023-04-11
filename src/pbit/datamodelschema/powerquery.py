from typing import TypedDict, Literal, Any, Callable
from uuid import uuid4
from pbit.datamodelschema.column import DaxType
import os

PRIOR_PREFIX: str = "~!PRIOR_TABLE_KEY!~"

MType = Literal[
	"Int64.Type",
	"Currency.Type",
	"Percentage.Type",
	"type datetime", 
	"type date",
	"type time",
	"type datetimezone",
	"type duration",
	"type logical",
	"type binary",
	"type number",
	"type any",
	"type text"
]

M_TYPE_TO_COLUMN_TYPE: dict[MType, DaxType] = {
	"type text": "string",
	"type logical": "boolean",
	"type datetime": "dateTime",
	"type any": "string",
	"Int64.Type": "int64",
	"type number": "double",
}

def from_m_type_to_dax_type(m_type_dict: dict[str, MType]) -> dict[str, DaxType]:
	out: dict[str, DaxType] = {}
	for key in m_type_dict:
		out[key] = M_TYPE_TO_COLUMN_TYPE[m_type_dict[key]]
	return out

def from_dax_type_to_m_type(dax_type_dict: dict[str, DaxType]) -> dict[str, MType]:
	out: dict[str, MType] = {}
	for key in dax_type_dict:

		if dax_type_dict[key] == "any":
			out[key] = "type any"
		else:
			for m_type, col_type in M_TYPE_TO_COLUMN_TYPE.items():
				if dax_type_dict[key] == col_type:
					out[key] = m_type
	return out

def list_to_m_str(list: list, wrap_values_as_str: bool) -> str:
	out = "{"
	for i, val in enumerate(list):
		if wrap_values_as_str:
			out += "\""+str(val)+"\""
		else:
			out += str(val)
		if i < len(list)-1:
			out += ", "
	out += "}"
	return out

def dict_to_m_str(dict: dict, wrap_keys_as_str: bool, wrap_values_as_str: bool) -> str:
	out = "{"
	key_index = 0
	key_length = len(list(dict.keys()))
	for k, v in dict.items():
		key_index += 1
		key_entry = k
		val_entry = v
		if wrap_keys_as_str:
			key_entry = "\"" + k + "\""

		if wrap_values_as_str:
			val_entry = "\"" + v + "\""

		out += list_to_m_str([key_entry, val_entry], False)
		if key_index < key_length:
			out += ","

	out += "}"
	return out

class Command():
	id: str
	name: str
	function_text: str
	parameter_order: list[str]
	parameters: dict[str, str | int | None]
	get_command_name: Callable[[str], str]
	def __init__(
		self,
		function_text: str,
		parameter_order: list[str],
		parameters: dict[str, str | int | None],
		name: str | None = None
	):
		self.id = str(uuid4())
		self.function_text = function_text
		if name == None:
			self.name = self.function_text.replace(".", " ")
		else:
			assert name
			self.name = name
		self.parameter_order = parameter_order
		self.parameters = parameters

	def dump(self, command_name: str | None = None, include_comma: bool = True) -> str:
		command_str = self.function_text + "("
		for i, key in enumerate(self.parameter_order):
			command_str += " "
			if key in self.parameters and self.parameters[key] != None:
				val: str | int | None = self.parameters[key]
				assert val

				command_str += str(val)

			else:
				command_str += "null"

			if i < len(self.parameter_order)-1:
				command_str += ","

		command_str += ")"

		if include_comma:
			command_str += ","

		if command_name != None:
			return f"#\"{command_name}\" = " + command_str
		else:
			return command_str

class PowerQuery():
	commands: list[Command]
	def __init__(self):
		self.commands = []

	def dump(self) -> list[str]:
		bases: dict[str, int] = {}
		query = "let"
		final_command_name = ""

		for i, command in enumerate(self.commands):
			command_name = command.name
			if not command_name in bases:
				bases[command_name] = 1
				command_name += "1"
			else:
				bases[command_name] += 1
				command_name += str(bases[command_name]+1)
			command_str = command.dump(command_name, i < len(self.commands)-1)
			command_str = command_str.replace(PRIOR_PREFIX, final_command_name)
			final_command_name = command_name
			query += "\n\t"+command_str
			
		query += "\nin"
		query += f"\n\t#\"{final_command_name}\""

		return query.split("\n")

	def insert_cmd(
		self,
		function_text: str,
		parameter_order: list[str],
		parameters: dict[str, str | int | None],
		name: str | None = None) -> Command:
		command = Command(function_text, parameter_order, parameters, name)
		self.commands.append(command)
		return command


	def insert_read_file_cmd(
		self,
		relative_path: str,
		name: str | None = None
	) -> Command:
		command = self.insert_cmd(
			function_text = "File.Contents",
			parameter_order = ["path", "options"],
			parameters = {
				"path": ("\"" + os.path.abspath(relative_path) + "\"").replace("\\", "/")
			},
			name = name
		)
		return command

	def insert_load_as_json_cmd(
		self,
		source = "#\""+PRIOR_PREFIX+"\"",
		encoding: int | None = None,
		name: str | None = None
	) -> Command:
		command = self.insert_cmd(
			function_text = "Json.Document",
			parameter_order = ["source", "encoding"],
			parameters = {
				"source": source,
				"encoding": encoding,
			},
			name = name
		)
		return command
	def insert_load_as_csv_cmd(
		self,
		source = "#\""+PRIOR_PREFIX+"\"",
		column_names: list | None = None,
		delimiter: str | None = None,
		extra_values: str | None = "ExtraValues.Error",
		encoding: int | None = None,
		name: str | None = None
	) -> Command:

		column_list_string: str | None = None
		if column_names and len(column_names) > 0:
			assert column_names
			column_list_string = list_to_m_str(column_names, True)

		command = self.insert_cmd(
			function_text = "Csv.Document",
			parameter_order = [
				"source", 
				"columns", 
				"delimiter", 
				"extra_values", 
				"encoding"
			],
			parameters = {
				"source": source,
				"columns": column_list_string,
				"delimiter": delimiter,
				"extra_values": extra_values,
				"encoding": encoding,
			},
			name = name
		)
		return command

	def insert_table_from_list_cmd(
		self,
		source = "#\""+PRIOR_PREFIX+"\"",
		splitter = "Splitter.SplitByNothing()",
		columns: str | None = None,
		default: str | None = None,
		extra_values: str | None = "ExtraValues.Error",
		name: str | None = None
	) -> Command:
		command = self.insert_cmd(
			function_text = "Table.FromList",
			parameter_order = [
				"source", 
				"splitter", 
				"columns", 
				"default", 
				"extra_values"
			],
			parameters = {
				"source": source,
				"splitter": splitter,
				"columns": columns,
				"default": default,
				"extra_values": extra_values,
			},
			name = name
		)
		return command

	def insert_expand_from_record_cmd(
		self,
		target_column: str,
		conversion_table: dict[str, str] | list[str],
		source = "#\""+PRIOR_PREFIX+"\"",
		name: str | None = None
	) -> Command:
		field_names_str: str = "{}"
		column_names_str: str | None = None
		if type(conversion_table) == dict:
			field_names = list(conversion_table.keys())
			new_column_names = []
			
			for field_name in field_names:
				new_column_names.append(conversion_table[field_name])
			
			field_names_str = list_to_m_str(field_names, True)
			column_names_str = list_to_m_str(new_column_names, True)

		else:
			assert type(conversion_table) == list
			field_names_str = list_to_m_str(conversion_table, True)

		command = self.insert_cmd(
			function_text = "Table.ExpandRecordColumn",
			parameter_order = [
				"source", 
				"column",
				"field_names",
				"new_column_names"
			],
			parameters = {
				"source": source,
				"column": "\""+target_column+"\"",
				"field_names": field_names_str,
				"new_column_names": column_names_str
			},
			name = name
		)
		return command	

	def insert_transform_dax_types_cmd(
		self,
		transformations: dict[str, MType],
		source = "#\""+PRIOR_PREFIX+"\"",
		culture: str | None = None,
		name: str | None = None
	) -> Command:
		command = self.insert_cmd(
			function_text = "Table.TransformColumnTypes",
			parameter_order = [
				"source", 
				"type_transformations",
				"culture"
			],
			parameters = {
				"source": source,
				"type_transformations": dict_to_m_str(transformations, True, False),
				"culture": culture
			},
			name = name
		)
		return command	