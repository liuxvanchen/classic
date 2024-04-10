import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 读取 NetCDF 文件
data = xr.open_dataset('D:\\WeChat\\WeChat Files\\wxid_lvjv33bjbkg222\\FileStorage\\File\\2024-04\\scPDSI.cru_ts4.05early1.1901.2020.cal_1901_20.bams.2021.GLOBAL.1901.2020.nc')

# 打印所有变量名
print("Variables in the NetCDF file:")
for var in data.variables:
    print(var)

# # 读取下载的 NetCDF 文件
# data = xr.open_dataset('D:\\Python\\pythonProject1\\论文\\download.nc')
#
# # 提取变量数据
# radiation = data['ssrd']
# precipitation = data['tp']
#
# # 提取温度数据
# temperature = data['t2m']
#
# # 绘制温度数据
# plt.figure(figsize=(10, 5))
# temperature.mean(dim='time').plot()
# plt.title('Mean Temperature')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.show()
#
# # 绘制辐射数据
# plt.figure(figsize=(10, 5))
# radiation.mean(dim='time').plot()
# plt.title('Mean Surface Solar Radiation Downwards')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.show()
#
# # 绘制降水数据
# plt.figure(figsize=(10, 5))
# precipitation.mean(dim='time').plot()
# plt.title('Mean Total Precipitation')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.show()
