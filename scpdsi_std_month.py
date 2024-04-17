import cartopy
import numpy as np
import rasterio
import xarray as xr
import matplotlib.pyplot as plt
import gc  # 导入垃圾收集器
from forest_t2m import read_forest_coords
import cartopy.crs as ccrs
import matplotlib.colors as mcolors
import cartopy.feature as cfeature



forest_lons, forest_lats = read_forest_coords('Forest_Mask.tif')
# 释放内存
gc.collect()

# 分块读取nc数据
ds=xr.open_dataset('scpdsi_reshape.nc',
                   chunks={'time': 12}
                   )

# 计算步骤，增加.compute()以获取实际的结果
# 平均值每个月
monthly_means = ds['scpdsi'].groupby('time.month').mean('time').compute()
# 计算标准差
monthly_std_dev = ds['scpdsi'].groupby('time.month').std('time').compute()

# 掩膜提取按月份计算平均值之后的人工林
scpdsi_forest = monthly_means.sel(
    latitude=xr.DataArray(forest_lats, dims="points"),
    longitude=xr.DataArray(forest_lons, dims="points"),
    method="nearest"
)
# 下面是修改scpdsi_forest维度的方法（从month，points到month和经纬度三个维度
# 创建经纬度的网格
unique_lats = np.unique(scpdsi_forest.latitude.values)
unique_lons = np.unique(scpdsi_forest.longitude.values)

# 使用广播创建一个新的 DataArray，该数组的维度为 ('month', 'latitude', 'longitude')
latitude, longitude = xr.broadcast(xr.DataArray(unique_lats, dims=["latitude"]), xr.DataArray(unique_lons, dims=["longitude"]))

# 初始化一个新的 DataArray，其结构将匹配想要的维度
new_forest = xr.DataArray(np.nan, dims=('month', 'latitude', 'longitude'), coords={'month': scpdsi_forest.month, 'latitude': unique_lats, 'longitude': unique_lons})

# 填充新的 DataArray
for month in scpdsi_forest.month:
    for pt in range(len(scpdsi_forest.points)):
        lat = scpdsi_forest.latitude.values[pt]
        lon = scpdsi_forest.longitude.values[pt]
        new_forest.loc[month, lat, lon] = scpdsi_forest.sel(month=month, points=pt)

# 这样，new_forest 就具有了正确的维度
print(new_forest.dims)

scpdsi_2020 = ds['scpdsi'].sel(time=slice('2020-01-01', '2020-12-31'))

monthly_means_2020 = scpdsi_2020.groupby('time.month').mean('time').compute()
# print(monthly_means_2020.dims)
# print(monthly_means_2020.coords)


# 按月计算平均值，并应用掩膜2020年
# 使用最近邻方法选择数据
selected_2020data = monthly_means_2020.sel(
    latitude=xr.DataArray(forest_lats, dims=["latitude"], coords={"latitude": forest_lats}),
    longitude=xr.DataArray(forest_lons, dims=["longitude"], coords={"longitude": forest_lons}),
    method="nearest"
).compute()
# print("123",selected_2020data.dims)
# print(selected_2020data.coords)


# print(scpdsi_2020)

# 将 selected_2020data 转换为与 new_forest 相同的维度
selected_2020data_reshaped = xr.DataArray(
    np.nan,
    dims=('month', 'latitude', 'longitude'),
    coords={'month': selected_2020data.month, 'latitude': unique_lats, 'longitude': unique_lons}
)

# 直接使用索引的方式访问数据
selected_2020data_reshaped.loc[dict(month=selected_2020data.month, latitude=selected_2020data.latitude, longitude=selected_2020data.longitude)] = selected_2020data

# 现在维度匹配，可以进行相减操作
difference = selected_2020data_reshaped - new_forest
# print(difference.dims)
# print(difference.coords)

# 释放内存
gc.collect()

# 初始化结果数组
drought_status = xr.full_like(difference, 0)

# 计算干旱程度，使用阈值：标准差的1倍、2倍、3倍
drought_status = xr.where(difference > 3 * monthly_std_dev, 3, drought_status)
drought_status = xr.where((difference > 2 * monthly_std_dev) & (difference <= 3 * monthly_std_dev), 2, drought_status)
drought_status = xr.where((difference > 1 * monthly_std_dev) & (difference <= 2 * monthly_std_dev), 1, drought_status)

# 计算湿润程度，同样使用阈值
drought_status = xr.where(difference < -3 * monthly_std_dev, -3, drought_status)
drought_status = xr.where((difference < -2 * monthly_std_dev) & (difference >= -3 * monthly_std_dev), -2, drought_status)
drought_status = xr.where((difference < -1 * monthly_std_dev) & (difference >= -2 * monthly_std_dev), -1, drought_status)

# total_pixels = drought_status.size
# print("Total number of pixels in drought_status:", total_pixels)
#
# # 获取各维度的详细形状
# print("Shape of drought_status:", drought_status.shape)
# months, latitudes, longitudes = drought_status.shape
#
# pixels_per_month = latitudes * longitudes
# print("Number of pixels per month:", pixels_per_month)

# 选择特定月份的数据，例如1月
data_for_map = drought_status.sel(month=7)

# 创建地图
fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})
ax.add_feature(cartopy.feature.BORDERS, linestyle=':')

# 设置地图范围
extent = [73, 135, 18, 54]  # 中国的大致范围

# 创建色彩映射
cmap = mcolors.ListedColormap(['deepskyblue', 'green', 'darkgreen', 'lightyellow', 'yellow', 'orange', 'red'])
# 将 nan 值设置为灰色
cmap.set_bad('white')

bounds = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# 创建地图
fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})
data_for_map.plot(ax=ax, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, add_colorbar=True)
ax.coastlines()
# 添加国界线，自定义线条样式为点线
ax.add_feature(cfeature.BORDERS, linestyle=':')
# ax.set_global()  # 无需设置全局范围

# 显示图
plt.show()