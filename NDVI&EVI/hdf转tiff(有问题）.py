import os
import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
import re
import rasterio
from rasterio.transform import from_origin

directory = r'E:\浏览器下载\ndvi-evi'
pattern = re.compile(r"MOD13A3\.A2020001\.h(\d{2})v(\d{2})\..*\.hdf$")

# 确定覆盖中国的瓦片范围
h_start, h_end = 21, 30  # 水平瓦片号从21到30
v_start, v_end = 3, 7    # 垂直瓦片号从3到7

# 创建一个数组，大小根据中国覆盖的瓦片范围来确定
width = (h_end - h_start + 1) * 1200
height = (v_end - v_start + 1) * 1200
china_ndvi = np.full((height, width), fill_value=np.nan)

for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        h_tile, v_tile = map(int, match.groups())
        h_offset = (h_tile - h_start) * 1200
        v_offset = (v_tile - v_start) * 1200

        filepath = os.path.join(directory, filename)
        hdf = SD(filepath, SDC.READ)
        ndvi_dataset = hdf.select('1 km monthly NDVI')
        ndvi_data = ndvi_dataset.get() * 0.0001  # 应用比例因子
        hdf.end()

        china_ndvi[v_offset:v_offset + 1200, h_offset:h_offset + 1200] = ndvi_data

# 定义GeoTIFF的元数据
transform = from_origin(-180, 90, 0.01, 0.01)  # 假设每像素0.01度，需要根据实际调整
crs = {'init': 'epsg:4326'}  # 使用WGS84坐标系统
output_path = r'E:\Data-py\NDVI\NDVI-2020-1.tif'

# 使用rasterio保存数据为GeoTIFF
with rasterio.open(
    output_path, 'w', driver='GTiff',
    height=china_ndvi.shape[0], width=china_ndvi.shape[1],
    count=1, dtype=str(china_ndvi.dtype),
    crs=crs, transform=transform
) as dst:
    dst.write(china_ndvi, 1)

# 显示结果
plt.figure(figsize=(10, 8))
plt.imshow(china_ndvi, cmap='YlGn', vmin=-0.2, vmax=1)
plt.colorbar(label='NDVI_month(1)')
plt.title('NDVI-2020-1')
plt.show()