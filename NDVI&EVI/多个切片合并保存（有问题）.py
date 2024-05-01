import os
import re
import numpy as np
from pyhdf.SD import SD, SDC
import h5py

directory = r'E:\浏览器下载\ndvi-evi'
output_directory = r'E:\Data-py\NDVI'
pattern = re.compile(r"MOD13A3\.A2020001\.h(\d{2})v(\d{2})\..*\.hdf$")

# 确保输出目录存在
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# 确定覆盖中国的瓦片范围
h_start, h_end = 21, 30  # 水平瓦片号从21到30
v_start, v_end = 3, 7    # 垂直瓦片号从3到7

# 创建一个数组，大小根据中国覆盖的瓦片范围来确定
tile_width = tile_height = 1200  # 每个瓦片的尺寸
width = (h_end - h_start + 1) * tile_width
height = (v_end - v_start + 1) * tile_height
all_ndvi_data = np.full((height, width), fill_value=np.nan)

# 遍历目录中的文件
for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        h_tile, v_tile = map(int, match.groups())
        if h_start <= h_tile <= h_end and v_start <= v_tile <= v_end:
            h_offset = (h_tile - h_start) * tile_width
            v_offset = (v_tile - v_start) * tile_height

            file_path = os.path.join(directory, filename)
            hdf = SD(file_path, SDC.READ)
            ndvi_dataset = hdf.select('1 km monthly NDVI')
            ndvi_data = ndvi_dataset.get().astype(np.float32) * 0.0001
            hdf.end()

            # 将数据放到正确的位置
            all_ndvi_data[v_offset:v_offset + tile_height, h_offset:h_offset + tile_width] = ndvi_data

# 保存数据到HDF5文件
output_path = os.path.join(output_directory, 'ndvi_2020_1.h5')
with h5py.File(output_path, 'w') as h5f:
    h5f.create_dataset('all_ndvi', data=all_ndvi_data)

print(f"Data saved to {output_path}")
