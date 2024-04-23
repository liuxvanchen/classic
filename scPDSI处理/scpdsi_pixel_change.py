import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import netCDF4 as nc
import cartopy.feature as cfeature

# 加载NetCDF文件
dataset = nc.Dataset('D:\\WeChat\\WeChat Files\\wxid_lvjv33bjbkg222\\FileStorage\\File\\2024-04\\scPDSI.cru_ts4.05early1.1901.2020.cal_1901_20.bams.2021.GLOBAL.1901.2020.nc')

# 读取经度和纬度数据
longitudes = dataset.variables['longitude'][:]
latitudes = dataset.variables['latitude'][:]

# 读取温度数据
scpdsi = dataset.variables['scpdsi'][:]

# 确定时间维度的大小
time_size = scpdsi.shape[0]

# 确保时间维度是12的倍数
assert time_size % 12 == 0, "时间维度不是12的整数倍，检查数据！"

# 重新组织数据为(年份, 月份, 纬度, 经度)
scpdsi_reshaped = scpdsi.reshape((-1, 12, scpdsi.shape[1], scpdsi.shape[2]))

# 计算每年的平均值
scpdsi_annual_avg = scpdsi_reshaped.mean(axis=1)

# 计算气温、降水、辐射变化量
scpdsi_change = scpdsi_annual_avg[-1, :, :] - scpdsi_annual_avg[0, :, :]

# 创建地图
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.coastlines()

# 绘制中国的轮廓线，solid是实线样式
ax.add_feature(cfeature.BORDERS, linestyle='solid', edgecolor='black')

# 设置颜色映射
cmap = plt.get_cmap('YlOrBr')

# 绘制气温变化量
temperature_plot = ax.pcolormesh(longitudes, latitudes, scpdsi_change, cmap=cmap, shading='auto')

# 创建颜色栏并设置标签
cbar = plt.colorbar(temperature_plot, orientation='vertical', pad=0.02, aspect=50)
cbar.set_label('Drought Index')  # 设置干旱指数的标签文本

# 设置图形标题
plt.title('Drought Index Change (1901-2020)')  # 设置图形的标题为干旱指数变化

plt.show()
