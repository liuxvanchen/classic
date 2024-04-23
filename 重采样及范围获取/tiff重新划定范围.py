import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np

# 打开原始的TIFF文件
with rasterio.open('E:\\人工林数据\\人工林郭庆华\\pf20.tif') as src:
    # 获取原始投影变换信息和像素数组
    transform = src.transform
    data = src.read(1)

    # 计算新的投影变换信息和形状
    new_left, new_bottom, new_right, new_top = (73, 18, 135, 54)
    width = int((new_right - new_left) / 0.5)  # 确认这是正确的分辨率
    height = int((new_top - new_bottom) / 0.5)
    new_transform, new_width, new_height = calculate_default_transform(
        src.crs, src.crs, width, height, left=new_left, bottom=new_bottom, right=new_right, top=new_top)

    # 确认新的尺寸是否合理
    print(f"New dimensions: {new_width} x {new_height}")

    # 如果尺寸过大，考虑调整分辨率或使用分块处理
    # 创建新的数组，确保尺寸可管理
    if new_height * new_width < 4000 * 4000:  # 例如，设置最大16百万像素
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

        with rasterio.open('', 'w', **kwargs) as dst:
            dst.write(new_data, 1)
    else:
        print("The requested size is too large!")
