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

tp = dataset.variables['tp'][:]
tp_mm = tp * 1000

tp_reshape = tp_mm.reshape((-1, 12, tp_mm.shape[1], tp_mm.shape[2]))

tp_annual_avg = tp_reshape.mean(axis=1)

tp_annual_year_avg = np.mean(tp_annual_avg, axis=(1, 2))
years = np.arange(1982, 2021)

slope, intercept, r_value, p_value, std_err = linregress(years, tp_annual_year_avg)

print(f"斜率: {slope:.4f}, 表示每年的平均降水变化量（mm/年）")
print(f"截距: {intercept:.4f}")
print(f"相关系数: {r_value:.4f}")
print(f"p值: {p_value:.4f}")
print(f"标准误差: {std_err:.4f}")

# 绘制年度降水变化和拟合线
plt.figure(figsize=(10, 6))
plt.scatter(years, tp_annual_year_avg, label='实际年度降水')
plt.plot(years, intercept + slope * years, 'r', label='线性拟合趋势线')
plt.xlabel('年份')
plt.ylabel('年度降水变化量（mm）')
plt.title('年度平均降水变化趋势')
plt.legend()
plt.grid(True)
plt.show()
