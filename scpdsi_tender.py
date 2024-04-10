import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# 读取下载的 NetCDF 文件
data = nc.Dataset('D:\\WeChat\\WeChat Files\\wxid_lvjv33bjbkg222\\FileStorage\\File\\2024-04\\scPDSI.cru_ts4.05early1.1901.2020.cal_1901_20.bams.2021.GLOBAL.1901.2020.nc')

scpdsi = data.variables['scpdsi'][:]

time_len = data.dimensions['time'].size
lat_len = data.dimensions['latitude'].size
lon_len = data.dimensions['longitude'].size

# 检查time_len是否能被12整除（即每年12个月）
if time_len % 12 != 0:
    print("时间维度不是12的整数倍，检查数据！")
else:
    # 计算每年的平均值
    years_len = time_len // 12
    # 重新整形数组为(years, months, latitude, longitude)，然后计算沿着月份的平均值
    annual_avg_scpdsi = scpdsi.reshape((years_len, 12, lat_len, lon_len)).mean(axis=1)

    china_avg_scpdsi = np.mean(annual_avg_scpdsi, axis=(1, 2))

    years = np.arange(1901, 2021)

    plt.figure(figsize=(14, 7))
    plt.plot(years, china_avg_scpdsi, label='SCPDSI', marker='+')
    plt.title('Annual China Average SCPDSI Change (1901-2020)')
    plt.xlabel('Year')
    plt.ylabel('SCPDSI')
    plt.legend()
    plt.show()
