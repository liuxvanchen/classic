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
    # 调用函数
    create_and_save_mask('Forest.tif', 'Forest_Mask.tif')
    forest_lons, forest_lats = read_forest_coords('Forest_Mask.tif')

    # 释放内存
    gc.collect()

    # 使用 chunks 参数进行分块读取，在读取使对数据不进行处理计算，在需要时再调用计算
    ds = xr.open_dataset('download.nc', chunks={'time': 12})

    # 转换数据集中所有变量的数据类型为float32
    # ds_float32 = ds.map(lambda x: x.astype('float32') if x.dtype == 'float64' else x)

    # 直接计算年平均气温
    annual_avg = ds['t2m'].groupby('time.year').mean('time') - 273.15

    # print(annual_avg.dims)
    # print(annual_avg.coords)

    # 掩膜和nc对应
    t2m_forest = annual_avg.sel(
        latitude=xr.DataArray(forest_lats, dims="points"),
        longitude=xr.DataArray(forest_lons, dims="points"),
        method="nearest"
    )
    print(t2m_forest)

    # 计算每年所有点的平均温度
    yearly_avg_temperature = t2m_forest.mean(dim='points')

    # 计算之前懒加载的数据
    computed_yearly_avg = yearly_avg_temperature.compute()

    # 绘制趋势图
    plt.figure(figsize=(12, 6))
    plt.plot(computed_yearly_avg['year'], computed_yearly_avg, marker='o', linestyle='-', color='b')
    plt.title('Annual Mean Forest Temperature Trend over 39 Years')
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.show()
