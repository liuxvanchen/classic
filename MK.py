import pymannkendall as mk
import numpy as np
import netCDF4 as nc

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
# 进行Mann-Kendall趋势测试
result = mk.original_test(mean_annual_temp_change)

# 打印测试结果
print(f"趋势: {'增加' if result.trend == 'increasing' else '减少'}")
print(f"p值: {result.p:.4f}")
