import numpy as np
import rasterio
import xarray as xr
import matplotlib.pyplot as plt

with rasterio.open('Forest.tif') as src:
    forest_mask_array = src.read(1)
    transform = src.transform
    crs = src.crs
    height = src.height
    width = src.width

# 使用更高效的方式计算经纬度坐标
lon_coords = transform.xoff + transform.a * np.arange(width)
lat_coords = transform.yoff + transform.e * np.arange(height)
# 使用 meshgrid 创建二维坐标数组，确保坐标顺序正确
lon_coords, lat_coords = np.meshgrid(lon_coords, lat_coords)

# 创建 DataArray，确保坐标与维度名称匹配
forest_mask_da = xr.DataArray(
    forest_mask_array,
    dims=('y', 'x'),
    coords={
        'lat': (('y', 'x'), lat_coords),  # 纬度
        'lon': (('y', 'x'), lon_coords)   # 经度
    }
)

# --- 加载并处理 ERA5 数据 ---

# 使用 chunks 参数进行分块读取
ds = xr.open_dataset('download.nc', chunks={'time': 12})  # 按年分块读取

# 直接计算年平均气温，避免生成大的中间结果
annual_avg = ds['t2m'].groupby('time.year').mean('time') - 273.15

# --- 提取人工林区域数据并绘图 ---
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