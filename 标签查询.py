import netCDF4 as nc

# Open the NetCDF file
ds = nc.Dataset('D:\Python\data\clip_nc.nc', 'r')  # 'r' is for read mode

# Access a specific variable, replace 'variable_name' with the name of your variable
variable = ds.variables['ssrd']

# Print all attributes of the variable
print("Attributes of the variable:")
for attr_name in variable.ncattrs():
    print(f"{attr_name}: {getattr(variable, attr_name)}")

# Optionally, check specific attributes like scale_factor or add_offset
if hasattr(variable, 'scale_factor'):
    print("Scale factor:", variable.scale_factor)

if hasattr(variable, 'add_offset'):
    print("Add offset:", variable.add_offset)

# Close the dataset after done
ds.close()

