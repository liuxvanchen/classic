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

# 重新组织数据为(年份, 月份, 纬度, 经度)
t2m_reshaped = t2m_celsius.reshape((-1, 12, t2m_celsius.shape[1], t2m_celsius.shape[2]))

# 计算每年的平均值
t2m_annual_avg = t2m_reshaped.mean(axis=1)

# 使用np.diff()计算连续元素的差值，即得到每个像元上面年度变化量,第一维是年份-1，二三维是地理位置坐标
annual_temp_change = np.diff(t2m_annual_avg, axis=0)

# print(annual_temp_change)
# 计算平均的年度温度变化
mean_annual_temp_change = np.mean(annual_temp_change, axis=(1, 2))

# 生成年份数据，从1983年开始（因为1982年没有前一年的数据进行对比）
years = np.arange(1983, 1983 + mean_annual_temp_change.shape[0])

# 进行线性拟合
slope, intercept, r_value, p_value, std_err = linregress(years, mean_annual_temp_change)

# 打印拟合结果
print(f"斜率: {slope:.4f}, 表示每年的平均温度变化量（摄氏度/年）")
print(f"截距: {intercept:.4f}")
print(f"相关系数: {r_value:.4f}")
print(f"p值: {p_value:.4f}")
print(f"标准误差: {std_err:.4f}")

# 绘制年度温度变化和拟合线
plt.figure(figsize=(10, 6))
plt.scatter(years, mean_annual_temp_change, label='实际年度温度变化')
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
