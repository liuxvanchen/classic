import numpy as np
import rasterio
import xarray as xr
import matplotlib.pyplot as plt

with rasterio.open('Forest.tif') as src:
    forest_mask_array = src.read(1)  # 读取数据
    transform = src.transform  # 获取仿射变换信息
    crs = src.crs  # 获取CRS信息

    # 从图像元数据中获取height和width
    height = src.height
    width = src.width

# 使用height和width计算经纬度坐标
rows, cols = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
xs, ys = transform * (cols, rows)  # 这里需要调整，下面提供正确的方法

# 正确的计算地理坐标的方法
# 注意：上面使用的变换方法是错误的。应使用如下方法：
coords_lon, coords_lat = np.meshgrid(
    np.linspace(transform.c, transform.c + transform.a * (width - 1), num=width),
    np.linspace(transform.f, transform.f + transform.e * (height - 1), num=height)
)

# 创建DataArray，包括经纬度坐标
forest_mask_da = xr.DataArray(
    forest_mask_array,
    dims=('y', 'x'),
    coords={
        'latitude': (('y', 'x'), coords_lat),
        'longitude': (('y', 'x'), coords_lon)
    }
)

print(forest_mask_da)
print()

# ds = xr.open_dataset('download.nc')
# # 转换数据集中所有变量的数据类型
# ds_float32 = ds.astype('float16')
# t2m_celsius = ds_float32['t2m'] - 273.15
#
# annual_avg = ds_float32['t2m'].groupby('time.year').mean('time')
#
# # 重要: 需要确保forest_mask_da与ds在空间分辨率和范围上对齐
# # 如果它们不直接对齐，可能需要使用xarray的interp_like, reindex_like, 或sel方法来调整
# # 以下代码假设已经处理了对齐问题
#
# # 应用掩膜
# # 假设forest_mask_da是一个经纬度编码的掩膜，其中人工林区域标记为1
# t2m_forest = annual_avg.where(forest_mask_da == 1)
# years = np.arange(1982, 2021)
#
# # 绘图
# plt.figure(figsize=(10, 6))
# plt.plot(years, t2m_forest, label='Temperature', marker='^')
# plt.title('Annual Average Temperature Change (1982-2020)')
# plt.xlabel('Year')
# plt.ylabel('Average Temperature (°C)')
# plt.grid(True)
# plt.show()





