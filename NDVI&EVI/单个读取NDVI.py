from pyhdf.SD import SD, SDC
import numpy as np
import matplotlib.pyplot as plt


def extract_ndvi_from_hdf(hdf_file):
    # 打开 HDF 文件
    hdf = SD(hdf_file, SDC.READ)

    # 读取 NDVI 数据集。在 MOD13A3 文件中，NDVI 数据集的名字是 "1 km monthly NDVI"
    ndvi_dataset = hdf.select('1 km monthly NDVI')

    # 获取 NDVI 数据
    ndvi_data = ndvi_dataset.get()

    # MODIS NDVI 数据由比例因子0.0001缩放，需要恢复到真实值
    ndvi_data = ndvi_data * 0.0001

    # 关闭 HDF 文件
    hdf.end()

    return ndvi_data


hdf_filename = 'E:\\浏览器下载\\ndvi-evi\\MOD13A3.A2020001.h21v03.061.2020328134849.hdf'

ndvi_data = extract_ndvi_from_hdf(hdf_filename)
print(ndvi_data.shape)


# 可视化
plt.imshow(ndvi_data, cmap='YlGn')
plt.colorbar(label='NDVI')
plt.title('NDVI')
plt.show()
