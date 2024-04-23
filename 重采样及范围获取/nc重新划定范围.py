import xarray as xr
import rioxarray

# 打开NetCDF文件
ds = xr.open_dataset('D:\\WeChat\\WeChat Files\\wxid_lvjv33bjbkg222\\FileStorage\\File\\2024-04\\scPDSI.cru_ts4.05early1.1901.2020.cal_1901_20.bams.2021.GLOBAL.1901.2020.nc')

# 使用rioxarray将xarray数据集转换为具有地理信息的数据集
ds_geo = ds.rio.write_crs("EPSG:4326")  # 假设NetCDF数据使用WGS84坐标系统

# 定义GeoTIFF范围
geo_bounds = {
    "left": 73,
    "right": 136,
    "bottom": 10,
    "top": 54
}

# 裁剪数据集到指定的范围
ds_clipped = ds_geo.rio.clip_box(minx=geo_bounds["left"], miny=geo_bounds["bottom"],
                                 maxx=geo_bounds["right"], maxy=geo_bounds["top"])

# （可选）保存裁剪后的数据集到新的NetCDF文件
ds_clipped.to_netcdf('scpdsi_reshape.nc')
