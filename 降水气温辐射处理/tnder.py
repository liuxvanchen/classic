import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# 加载nc文件
ds = nc.Dataset('D:\Python\data\clip_nc.nc')

# 假设t2m变量包含了一个(time, latitude, longitude)的数据结构
t2m = ds.variables['t2m'][:]
ssrd = ds.variables['ssrd'][:]  # 地表太阳辐射
tp = ds.variables['tp'][:]  # 总降水量

#对t2m变量应用缩放因子和偏移量
# scale_factor = ds.variables['t2m'].scale_factor
# add_offset = ds.variables['t2m'].add_offset
# actual_t2m = t2m* scale_factor + add_offset


# 将温度从开尔文转换为摄氏度
t2m_celsius = t2m - 273.15

# 对tp变量应用缩放因子和偏移量
# scale_factor = ds.variables['tp'].scale_factor
# add_offset = ds.variables['tp'].add_offset
# actual_precipitation = tp * scale_factor + add_offset

#单位转换
# tp_mm = actual_precipitation * 1000
tp_mm = tp * 1000


# 对ssrd应用缩放因子和偏移量
# scale_factor = ds.variables['ssrd'].scale_factor
# add_offset = ds.variables['ssrd'].add_offset
# actual_ssrd = ssrd * scale_factor + add_offset

# 知道总的时间长度，以及经纬度的维度大小
time_len = ds.dimensions['time'].size
lat_len = ds.dimensions['latitude'].size
lon_len = ds.dimensions['longitude'].size

# 检查time_len是否能被12整除（即每年12个月）
if time_len % 12 != 0:
    print("时间维度不是12的整数倍，检查数据！")
else:
    print(time_len)
    # 计算每年的平均值
    years_len = time_len // 12
    # 重新整形数组为(years, months, latitude, longitude)，然后计算沿着月份的平均值
    annual_avg_t2m_celsius = t2m_celsius.reshape((years_len, 12, lat_len, lon_len)).mean(axis=1)
    annual_avg_tp = tp_mm.reshape((years_len, 12, lat_len, lon_len)).mean(axis=1)
    annual_avg_ssrd = ssrd.reshape((years_len, 12, lat_len, lon_len)).mean(axis=1)

    # 计算每年的全球平均气温
    china_avg_t2m_celsius = np.mean(annual_avg_t2m_celsius, axis=(1, 2))

    years = np.arange(1982, 2021)

    plt.figure(figsize=(10, 6))
    plt.plot(years, china_avg_t2m_celsius, label='Temperature', marker='o')
    plt.title('Annual China Average Temperature Change (1982-2020)')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.legend()
    plt.show()

    # 降水
    china_avg_tp = np.mean(annual_avg_tp, axis=(1, 2))
    years = np.arange(1982, 2021)

    plt.figure(figsize=(10, 6))
    plt.plot(years, china_avg_tp, label='precipitation', marker='^')
    plt.title('Annual China Average Precipitation Change (1982-2020)')
    plt.xlabel('Year')
    plt.ylabel('Precipitation (mm)')
    plt.legend()
    plt.show()

    china_avg_ssrd = np.mean(annual_avg_ssrd, axis=(1, 2))
    years = np.arange(1982, 2021)

    # 辐射
    plt.figure(figsize=(14, 7))
    plt.plot(years, china_avg_ssrd, label='Radiation', marker='^')
    plt.title('Annual China Average Radiation Change (1982-2020)')
    plt.xlabel('Year')
    plt.ylabel('Radiation (J/m²)')

    plt.legend()
    plt.show()
