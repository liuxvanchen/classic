from osgeo import gdal

# 输入和输出文件路径
input_raster = 'D:\\WeChat\\WeChat Files\\wxid_lvjv33bjbkg222\\FileStorage\\File\\2024-04\\人工林数据\\人工林数据\\人工林郭庆华\\pf20.tif'
output_raster = 'Forest.tif'

# 设置重采样的目标分辨率（以度为单位）
x_res = 0.25  # 新的水平分辨率（度）
y_res = 0.25  # 新的垂直分辨率（度）

# 使用gdal.Warp进行重采样
ds = gdal.Warp(output_raster, input_raster, xRes=x_res, yRes=y_res, resampleAlg=gdal.GRA_NearestNeighbour)
ds = None  # 关闭数据集，保存文件

