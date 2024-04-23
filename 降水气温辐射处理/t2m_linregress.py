import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import linregress
import netCDF4 as nc


# 指定字体路径
matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
matplotlib.rcParams['font.size'] = 10

# 加载NetCDF文件
dataset = nc.Dataset('download.nc')

# 读取经度和纬度数据
longitudes = dataset.variables['longitude'][:]
latitudes = dataset.variables['latitude'][:]

# 读取温度数据
t2m = dataset.variables['t2m'][:]

# 将温度从开尔文转换为摄氏度,降水从m转换为mm
t2m_celsius = t2m - 273.15

# 确定时间维度的大小
time_size = t2m_celsius.shape[0]

# 确保时间维度是12的倍数
assert time_size % 12 == 0, "时间维度不是12的整数倍，检查数据！"

timesteps_per_year = 12
t2m_reshaped = t2m_celsius.reshape((-1, timesteps_per_year, t2m_celsius.shape[1], t2m_celsius.shape[2]))

# 计算每年的平均值
t2m_annual_avg = t2m_reshaped.mean(axis=1)

# 对每年平均值的空间维度进行平均
t2m_annual_year_avg = t2m_annual_avg.mean(axis=(1, 2))

years=np.arange(1982,2021)

# 进行线性拟合
slope, intercept, r_value, p_value, std_err = linregress(years, t2m_annual_year_avg)


# 打印拟合结果
print(f"斜率: {slope:.4f}, 表示每年的平均温度变化量（摄氏度/年）")
print(f"截距: {intercept:.4f}")
print(f"相关系数: {r_value:.4f}")
print(f"p值: {p_value:.4f}")
print(f"标准误差: {std_err:.4f}")

# 绘制年度温度变化和拟合线
plt.figure(figsize=(10, 6))
plt.scatter(years, t2m_annual_year_avg, label='实际年度温度')
plt.plot(years, intercept + slope * years, 'r', label='线性拟合趋势线')
plt.xlabel('年份')
plt.ylabel('年度温度变化量（摄氏度）')
plt.title('年度平均温度变化趋势')
plt.legend()
plt.grid(True)
plt.show()


# # 线性回归分析
# slope, intercept, r_value, p_value, std_err = linregress(years, temperature)
#
# # 打印趋势信息
# print(f"斜率（每年的变化量）: {slope:.4f}")
# print(f"p值: {p_value:.4f}")
#
# # 绘制数据点和趋势线
# plt.scatter(years, temperature, label='实际数据')
# plt.plot(years, intercept + slope * years, 'r', label='趋势线')
# plt.legend()
# plt.xlabel('年份')
# plt.ylabel('气温')
# plt.title('气温趋势分析')
# plt.show()
