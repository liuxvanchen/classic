from netCDF4 import Dataset

# 打开.nc文件
nc_file = 'download.nc'
nc_dataset = Dataset(nc_file, mode='r')

variable_name = 't2m'
nc_variable = nc_dataset.variables[variable_name]

# 获取最大值和最小值
max_value = nc_variable[:].max()-273.15
min_value = nc_variable[:].min()-273.15

print(f"最大值: {max_value}")
print(f"最小值: {min_value}")

# 关闭.nc文件
nc_dataset.close()
