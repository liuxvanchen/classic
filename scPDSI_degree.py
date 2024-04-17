import cartopy
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from forest_t2m import read_forest_coords
import matplotlib.colors as mcolors
import cartopy.feature as cfeature
import cartopy.crs as ccrs


# 读取森林坐标和数据
forest_lons, forest_lats = read_forest_coords('Forest_Mask.tif')
ds = xr.open_dataset('scpdsi_reshape.nc')

# 计算整个数据集的月平均值
monthly_mean = ds['scpdsi'].groupby('time.month').mean('time')

# 提取2020年数据并计算月平均值
scpdsi_forest_2020 = ds['scpdsi'].sel(time=slice('2020-01-01', '2020-12-31'))
monthly_20020 = scpdsi_forest_2020.groupby('time.month').mean('time')
print("Dimensions of monthly_20020:", monthly_20020.dims)
print("Coordinates of monthly_20020:", monthly_20020.coords)

# 选择2020年数据中森林区域的最近点
selected_2020data = monthly_20020.sel(
    latitude=xr.DataArray(forest_lats, dims="points"),
    longitude=xr.DataArray(forest_lons, dims="points"),
    method="nearest"
)
print("Dimensions of selected_2020data:", selected_2020data.dims)
print("Coordinates of selected_2020data:", selected_2020data.coords)

# 重新构造 DataArray 以匹配全球经纬度网格
unique_lats = np.unique(selected_2020data.latitude.values)
unique_lons = np.unique(selected_2020data.longitude.values)

selected_2020data_reshaped = xr.DataArray(
    np.nan,
    dims=('month', 'latitude', 'longitude'),
    coords={
        'month': selected_2020data.month,
        'latitude': unique_lats,
        'longitude': unique_lons
    }
)

# 填充新的 DataArray
for month in selected_2020data.month.values:
    for pt in range(len(selected_2020data.points)):
        lat = selected_2020data.latitude.values[pt]
        lon = selected_2020data.longitude.values[pt]
        selected_2020data_reshaped.loc[{'month': month, 'latitude': lat, 'longitude': lon}] = selected_2020data.sel(month=month, points=pt)

# 输出数据以确认
print("Dimensions of selected_2020data_reshaped:", selected_2020data_reshaped.dims)
print("Coordinates of selected_2020data_reshaped:", selected_2020data_reshaped.coords)

drought_status = xr.full_like(selected_2020data_reshaped, 0)
drought_status = xr.where(selected_2020data_reshaped >= 4, 4, drought_status)
drought_status = xr.where((selected_2020data_reshaped < 4) & (selected_2020data_reshaped >= 3), 3, drought_status)
drought_status = xr.where((selected_2020data_reshaped < 3) & (selected_2020data_reshaped >= 2), 2, drought_status)
drought_status = xr.where((selected_2020data_reshaped < 2) & (selected_2020data_reshaped >= 1), 1, drought_status)
drought_status = xr.where((selected_2020data_reshaped < 1) & (selected_2020data_reshaped > -1), 0, drought_status)
drought_status = xr.where((selected_2020data_reshaped < -1) & (selected_2020data_reshaped >= -2), -1, drought_status)
drought_status = xr.where((selected_2020data_reshaped < -2) & (selected_2020data_reshaped >= -3), -2, drought_status)
drought_status = xr.where((selected_2020data_reshaped < -3) & (selected_2020data_reshaped >= -4), -3, drought_status)
drought_status = xr.where(selected_2020data_reshaped <= -4, -4, drought_status)

# 选择特定月份的数据，例如1月
data_for_map = drought_status.sel(month=7)
print(data_for_map.dims)
print(data_for_map.coords)

# 创建色彩映射和规范化对象
# 在 -0.5 到 0.5 之间设置浅黄色，并将 0.0 单独设置为白色
colors = [
    'darkred', 'red', 'orange', 'yellow',
    'lightyellow', # -0.1 到 0.0
    'white',       # 0.0
    'white',
    'lightyellow', # 0.0 到 0.1
    'darkgreen', 'blue', 'indigo', 'purple'
]

cmap = mcolors.ListedColormap(colors)

# 设置 bounds
# 注意：添加额外的界限以确保0.0准确映射到白色
bounds = [-4.5, -3.5, -2.5, -1.5, -0.5, -0.1, 0.0, 0.1, 0.5, 1.5, 2.5, 3.5, 4.5]

# 创建一个颜色规范化对象
norm = mcolors.BoundaryNorm(bounds, cmap.N)
# 创建地图
fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([73, 135, 18, 54], crs=ccrs.PlateCarree())  # 设置地图显示范围
ax.add_feature(cfeature.BORDERS, linestyle=':')

ax.coastlines()  # 添加海岸线

# 绘制数据
data_for_map.plot(ax=ax, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, add_colorbar=True)

# 显示图
plt.show()