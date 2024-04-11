import numpy as np
import rasterio
import xarray as xr
import matplotlib.pyplot as plt
import gc  # 导入垃圾收集器

# 使用 rasterio 读取栅格数据
with rasterio.open('Forest.tif') as src:
    forest_mask_array = src.read(1)  # 读取第一波段的数据
    transform = src.transform
    height = src.height
    width = src.width

# 找出所有森林（标签为1）的像素位置
forest_indices = np.where(forest_mask_array == 1)

# 计算这些像素对应的经纬度坐标
forest_lons, forest_lats = transform * (forest_indices[1], forest_indices[0])

# 将坐标和掩膜值转换为xarray DataArray
# 注意：由于这里我们只关注森林区域，所以我们创建了一个包含森林区域坐标和掩膜值（均为1）的DataArray
forest_mask_da = xr.DataArray(
    np.ones(len(forest_lons)),  # 为所有森林区域创建值为1的数组
    dims=['forest_points'],
    coords={
        'lat': ('forest_points', forest_lats),
        'lon': ('forest_points', forest_lons)
    }
)

# 释放不再需要的内存
del forest_mask_array
gc.collect()

# 使用 chunks 参数进行分块读取 NetCDF 数据
ds = xr.open_dataset('download.nc', chunks={'time': 12})

# 转换数据集中所有变量的数据类型为float32
ds_float32 = ds.map(lambda x: x.astype('float32') if x.dtype == 'float64' else x)

# 直接计算年平均气温
annual_avg = ds_float32['t2m'].groupby('time.year').mean('time') - 273.15

# 提取人工林区域的年平均气温
t2m_forest = annual_avg.where(forest_mask_da == 1)

# 绘制时间序列图
plt.figure(figsize=(10, 6))
plt.plot(t2m_forest.year, t2m_forest.mean(dim=('latitude', 'longitude')), label='Temperature', marker='^')
plt.title('Annual Average Temperature Change (1982-2020)')
plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.grid(True)
plt.show()

# 清理
del ds, annual_avg, t2m_forest
gc.collect()
