import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np

# 打开原始的TIFF文件
with rasterio.open('D:\\WeChat\\WeChat Files\\wxid_lvjv33bjbkg222\\FileStorage\\File\\2024-04\\人工林数据\\人工林数据\\人工林郭庆华\\pf20.tif') as src:
    # 获取原始投影变换信息和像素数组
    transform = src.transform
    data = src.read(1)

    # 计算新的投影变换信息和形状
    new_left, new_bottom, new_right, new_top = (73, 18, 135, 54)
    width = int((new_right - new_left) / 0.25)  # 根据0.25°分辨率计算宽度
    height = int((new_top - new_bottom) / 0.25)  # 根据0.25°分辨率计算高度
    new_transform, new_width, new_height = calculate_default_transform(
        src.crs, src.crs, width, height, left=new_left, bottom=new_bottom, right=new_right, top=new_top)

    # 创建新的数组
    new_data = np.zeros((new_height, new_width), dtype=data.dtype)

    # 将原始数据重新投影到新的范围和分辨率
    reproject(
        data,
        new_data,
        src_transform=transform,
        src_crs=src.crs,
        dst_transform=new_transform,
        dst_crs=src.crs,
        resampling=Resampling.nearest)

# 写入新的TIFF文件
kwargs = src.meta.copy()
kwargs.update({
    'transform': new_transform,
    'width': new_width,
    'height': new_height,
    'crs': src.crs
})

with rasterio.open('reclassified.tif', 'w', **kwargs) as dst:
    dst.write(new_data, 1)
