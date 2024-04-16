import numpy as np
import rasterio
import xarray as xr
import matplotlib.pyplot as plt
import gc  # 导入垃圾收集器
from forest_t2m import read_forest_coords

forest_lons, forest_lats = read_forest_coords('Forest_Mask.tif')
# 释放内存
gc.collect()

# 使用 chunks 参数进行分块读取，在读取使对数据不进行处理计算，在需要时再调用计算
ds = xr.open_dataset(
    'D:\\WeChat\\WeChat Files\\wxid_lvjv33bjbkg222\\FileStorage\\File\\2024-04\\scPDSI.cru_ts4.05early1.1901.2020.cal_1901_20.bams.2021.GLOBAL.1901.2020.nc',
    chunks={'time': 12})

# 转换数据集中所有变量的数据类型为float32
# ds_float32 = ds.map(lambda x: x.astype('float32') if x.dtype == 'float64' else x)
annual_avg = ds['scpdsi'].groupby('time.year').mean('time')

scpdsi_forest = annual_avg.sel(
    latitude=xr.DataArray(forest_lats, dims="points"),
    longitude=xr.DataArray(forest_lons, dims="points"),
    method="nearest"
)
print(scpdsi_forest)

# 计算每年所有点的平均温度
yearly_avg_temperature = scpdsi_forest.mean(dim='points')

# 计算之前懒加载的数据
computed_yearly_avg = yearly_avg_temperature.compute()

# 绘制趋势图
plt.figure(figsize=(12, 6))
plt.plot(computed_yearly_avg['year'], computed_yearly_avg, marker='o', linestyle='-', color='b')
plt.title('Annual Mean Forest Scpdsi')
plt.xlabel('Year')
plt.ylabel('Temperature (°C)')
plt.grid(True)
plt.show()
