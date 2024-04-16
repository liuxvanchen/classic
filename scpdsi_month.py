import numpy as np
import rasterio
import xarray as xr
import matplotlib.pyplot as plt
import gc  # 导入垃圾收集器
import gc  # 导入垃圾收集器
from forest_t2m import read_forest_coords
import cartopy.crs as ccrs
import matplotlib.colors as mcolors


forest_lons, forest_lats = read_forest_coords('Forest_Mask.tif')
# 释放内存
gc.collect()

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

# 初始化一个新的 DataArray，其结构将匹配我们想要的维度
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


# # 按月计算平均值，并应用掩膜2020年
# 使用最近邻方法选择数据
selected_2020data = monthly_means_2020.sel(
    latitude=xr.DataArray(forest_lats, dims=["latitude"], coords={"latitude": forest_lats}),
    longitude=xr.DataArray(forest_lons, dims=["longitude"], coords={"longitude": forest_lons}),
    method="nearest"
).compute()
print("123",selected_2020data.dims)
print(selected_2020data.coords)


# print(scpdsi_2020)

# 释放内存
gc.collect()

#计算差值
difference = selected_2020data - new_forest
print("Difference dimensions:", difference.dims)
print("Monthly Std Dev dimensions:", monthly_std_dev.dims)

# # 初始化结果数组
# drought_status = xr.full_like(difference, 0)
#
# # 计算干旱程度，使用阈值：标准差的1倍、2倍、3倍
# drought_status = xr.where(difference > 3 * monthly_std_dev, 3, drought_status)
# drought_status = xr.where((difference > 2 * monthly_std_dev) & (difference <= 3 * monthly_std_dev), 2, drought_status)
# drought_status = xr.where((difference > 1 * monthly_std_dev) & (difference <= 2 * monthly_std_dev), 1, drought_status)
#
# # 计算湿润程度，同样使用阈值，但应当检查逻辑并确保使用正确的比较运算符
# drought_status = xr.where(difference < -3 * monthly_std_dev, -3, drought_status)
# drought_status = xr.where((difference < -2 * monthly_std_dev) & (difference >= -3 * monthly_std_dev), -2, drought_status)
# drought_status = xr.where((difference < -1 * monthly_std_dev) & (difference >= -2 * monthly_std_dev), -1, drought_status)
# # 选择特定月份的数据，例如1月
# data_for_map = drought_status.sel(month=1)
#
# # 创建色彩映射
# cmap = mcolors.ListedColormap(['deepskyblue', 'green', 'darkgreen', 'white', 'yellow', 'orange', 'red'])
# bounds = [-3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5]
# norm = mcolors.BoundaryNorm(bounds, cmap.N)
#
# # 创建地图
# fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})
# data_for_map.plot(ax=ax, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, add_colorbar=True)
# ax.coastlines()
# ax.set_global()
#
# # 显示图
# plt.show()