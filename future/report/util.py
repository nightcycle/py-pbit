import inspect
# write to DataModelSchema
def remove_none_values(dct):
	# Create a list of keys to be removed (to avoid changing dictionary size during iteration)
	keys_to_remove = []
	for key_val in dct:
		value = key_val
		key = key_val
		if type(dct) != list and inspect.isclass(dct):
			value = dct[key_val]		

		if value is None and type(dct) != list:
			keys_to_remove.append(key)
		elif inspect.isclass(value) or type(value) == list or type(value) == dict:
			remove_none_values(value)
			
	# Remove keys with None values
	for key in keys_to_remove:
		dct.pop(key)
	return dct