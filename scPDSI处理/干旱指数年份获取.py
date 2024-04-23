import netCDF4 as nc
from datetime import datetime, timedelta

# 加载nc文件
ds = nc.Dataset('D:\\WeChat\\WeChat Files\\wxid_lvjv33bjbkg222\\FileStorage\\File\\2024-04\\scPDSI.cru_ts4.05early1.1901.2020.cal_1901_20.bams.2021.GLOBAL.1901.2020.nc')

# 读取时间变量
times = ds.variables['time'][:]

# 尝试获取时间单位
time_units = ds.variables['time'].units

# 使用netCDF4的num2date函数将时间从数值转换为日期对象
dates = nc.num2date(times, units=time_units)

# 从日期对象中提取年份和月份
years = [date.year for date in dates]
months = [date.month for date in dates]

# 打印出开始和结束的年份和月份，确认时间范围
print("开始年份:", years[0], "月份:", months[0])
print("结束年份:", years[-1], "月份:", months[-1])

# 关闭文件
ds.close()
