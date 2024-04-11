import xarray as xr
import rioxarray

# 打开NetCDF文件
ds = xr.open_dataset('download.nc')

# 使用rioxarray将xarray数据集转换为具有地理信息的数据集
ds_geo = ds.rio.write_crs("EPSG:4326")  # 假设NetCDF数据使用WGS84坐标系统

# 定义GeoTIFF范围
geo_bounds = {
    "left": 73.600612577997,
    "right": 134.850612577997,
    "bottom": 18.061187251482664,
    "top": 53.561187251482664
}

# 裁剪数据集到指定的范围
ds_clipped = ds_geo.rio.clip_box(minx=geo_bounds["left"], miny=geo_bounds["bottom"],
                                 maxx=geo_bounds["right"], maxy=geo_bounds["top"])

# （可选）保存裁剪后的数据集到新的NetCDF文件
ds_clipped.to_netcdf('reshape.nc')
