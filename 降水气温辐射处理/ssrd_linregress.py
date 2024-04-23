import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import linregress
import netCDF4 as nc

matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['font.size'] = 10

dataset = nc.Dataset('download.nc')

longitudes = dataset.variables['longitude'][:]
latitudes = dataset.variables['latitude'][:]

ssrd = dataset.variables['ssrd'][:]

ssrd_reshape = ssrd.reshape((-1, 12, ssrd.shape[1], ssrd.shape[2]))

ssrd_annual_avg = ssrd_reshape.mean(axis=1)

# 一年的秒数
seconds_per_year = 365.25 * 24 * 3600

# 转换为 W/m²
ssrd_annual_avg_wm2 = ssrd_annual_avg / seconds_per_year

ssre_annual_year_avg = np.mean(ssrd_annual_avg_wm2, axis=(1, 2))

years = np.arange(1982,2021)

slope, intercept, r_value, p_value, std_err = linregress(years, ssre_annual_year_avg)

print(f"斜率: {slope:.4f}, 表示每年的平均辐射变化量（（W/m^2）/年）")
print(f"截距: {intercept:.4f}")
print(f"相关系数: {r_value:.4f}")
print(f"p值: {p_value:.4f}")
print(f"标准误差: {std_err:.4f}")

plt.figure(figsize=(10, 6))
plt.scatter(years, ssre_annual_year_avg, label='实际年度辐射')
plt.plot(years, intercept + slope * years, 'r', label='线性拟合趋势线')
plt.xlabel('年份')
plt.ylabel('年度辐射变化量（W/m^2）')
plt.title('年度平均辐射变化趋势')
plt.legend()
plt.grid(True)
plt.show()
