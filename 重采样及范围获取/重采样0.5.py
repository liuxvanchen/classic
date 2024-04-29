from osgeo import gdal

# 输入和输出文件路径
input_raster = ''
output_raster = 'Forest_new.tif'

# 设置重采样的目标分辨率（以度为单位）
x_res = 0.5  # 新的水平分辨率（度）
y_res = 0.5  # 新的垂直分辨率（度）

# 使用gdal.Warp进行重采样
ds = gdal.Warp(output_raster, input_raster, xRes=x_res, yRes=y_res, resampleAlg=gdal.GRA_NearestNeighbour)
ds = None  # 关闭数据集，保存文件