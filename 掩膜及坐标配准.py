import numpy as np
import rasterio
import xarray as xr
import matplotlib.pyplot as plt
import gc  # 导入垃圾收集器


def create_and_save_mask(input_path, output_path):
    #掩膜创建，提供输入输出文件
    with rasterio.open(input_path) as src:
        #读取第一波段的数据
        mask_array = src.read(1)
        #获取文件属性，transform，height，width
        transform = src.transform
        height = src.height
        width = src.width
        crs = src.crs

        # 创建掩膜（依照具体的标记值而定
        mask_array[mask_array == 1] = 0
        mask_array[mask_array != 0] = 2

        # 保存掩膜
        with rasterio.open(output_path, 'w', driver='GTiff', height=height, width=width, count=1,
                           dtype=mask_array.dtype, crs=crs, transform=transform) as dst:
            dst.write(mask_array, 1)


def read_forest_coords(mask_path):
    #读取掩膜，标记为指定森林的像素经纬度坐标
    with rasterio.open(mask_path) as src:
        mask = src.read(1)
        transform = src.transform
        #查找森林位置
        forest_indices = np.where(mask == 0)
        #返回坐标
        forest_coords = [transform * (x, y) for x, y in zip(forest_indices[1], forest_indices[0])]
        forest_lons = np.round([coord[0] for coord in forest_coords], decimals=2)
        forest_lats = np.round([coord[1] for coord in forest_coords], decimals=2)
        return forest_lons, forest_lats

if __name__ == "__main__":
    create_and_save_mask('Forest0.5.tif','Forest0.5_mark.tif')