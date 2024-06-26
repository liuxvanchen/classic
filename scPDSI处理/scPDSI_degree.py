import cartopy
import numpy as np
import rasterio
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import geopandas  as gpd# 添加shp


def read_forest_coords(mask_path):
    # 读取掩膜，标记为指定森林的像素经纬度坐标
    with rasterio.open(mask_path) as src:
        mask = src.read(1)
        transform = src.transform
        # 用2查找人工林位置，用33查找天然林：：mask=2/33
        forest_indices = np.where(mask == 33)
        # 返回坐标
        forest_coords = [transform * (x, y) for x, y in zip(forest_indices[1], forest_indices[0])]
        forest_lons = np.round([coord[0] for coord in forest_coords], decimals=2)
        forest_lats = np.round([coord[1] for coord in forest_coords], decimals=2)
        return forest_lons, forest_lats


# 读取森林坐标和数据
forest_lons, forest_lats = read_forest_coords('D:\\Python\\pythonProject1\\论文\\2020pnf_re1.tif')
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
        selected_2020data_reshaped.loc[{'month': month, 'latitude': lat, 'longitude': lon}] = selected_2020data.sel(
            month=month, points=pt)

# 输出数据以确认
print("Dimensions of selected_2020data_reshaped:", selected_2020data_reshaped.dims)
print("Coordinates of selected_2020data_reshaped:", selected_2020data_reshaped.coords)
# 打印最小值和最大值
min_value = selected_2020data_reshaped.min().values
max_value = selected_2020data_reshaped.max().values
print("最小值:", min_value)
print("最大值:", max_value)

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

# drought_status = xr.full_like(selected_2020data_reshaped, 0)
# drought_status = xr.where(selected_2020data_reshaped >= 4,0, drought_status)
# drought_status = xr.where((selected_2020data_reshaped < 4) & (selected_2020data_reshaped >= 3), 0, drought_status)
# drought_status = xr.where((selected_2020data_reshaped < 3) & (selected_2020data_reshaped >= 2), 0, drought_status)
# drought_status = xr.where((selected_2020data_reshaped < 2) & (selected_2020data_reshaped >= 1),3, drought_status)
# drought_status = xr.where((selected_2020data_reshaped < 1) & (selected_2020data_reshaped > -1), 3, drought_status)
# drought_status = xr.where((selected_2020data_reshaped < -1) & (selected_2020data_reshaped >= -2), 3, drought_status)
# drought_status = xr.where((selected_2020data_reshaped < -2) & (selected_2020data_reshaped >= -3), 3, drought_status)
# drought_status = xr.where((selected_2020data_reshaped < -3) & (selected_2020data_reshaped >= -4), 3, drought_status)
# drought_status = xr.where(selected_2020data_reshaped <= -4, 3, drought_status)

# import xarray as xr
#
# for time_value in drought_status['month'].values:
#     for lat in drought_status['latitude'].values:
#         for lon in drought_status['longitude'].values:
#             if (lon>80)&(lon<100):
#                 status = drought_status.sel(month=time_value, latitude=lat, longitude=lon).values
#                 print(f"Month: {time_value}, Latitude: {lat}, Longitude: {lon}, Drought Status: {status}")

# 选择特定月份的数据，例如1月
data_for_map = drought_status.sel(month=9)
print(data_for_map.dims)
print(data_for_map.coords)

# 加载 Shapefile
gdf = gpd.read_file('D:\\Python\\data\\china.shp')

# 设置色彩映射和规范化对象
colors = [
    'darkred', 'red', 'orange', 'yellow',
    'lightyellow',  # -0.1 到 0.0
    'white',  # 0.0
    'white',
    'lightyellow',  # 0.0 到 0.1
    'darkgreen', 'blue', 'indigo', 'purple'
]
cmap = mcolors.ListedColormap(colors)
bounds = [-4.5, -3.5, -2.5, -1.5, -0.5, -0.1, 0.0, 0.1, 0.5, 1.5, 2.5, 3.5, 4.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# 创建地图
fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([73, 135, 18, 54], crs=ccrs.PlateCarree())  # 设置地图显示范围

# 添加国界和海岸线
# ax.add_feature(cfeature.BORDERS, linestyle=':')
# ax.coastlines()

# 绘制气候数据
data_for_map.plot(ax=ax, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, add_colorbar=True)

# 叠加 Shapefile(WGS84系统下的
gdf.plot(ax=ax, edgecolor='black', facecolor='none', transform=ccrs.PlateCarree())

# 显示图像
plt.show()