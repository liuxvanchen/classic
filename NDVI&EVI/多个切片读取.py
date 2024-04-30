import os
import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD, SDC
import re

directory = r'E:\浏览器下载\ndvi-evi'
pattern = re.compile(r"MOD13A3\.A2020001\.h(\d{2})v(\d{2})\..*\.hdf$")

# 确定覆盖中国的瓦片范围
h_start, h_end = 21, 30  # 假设水平瓦片号从21到30
v_start, v_end = 3, 7    # 假设垂直瓦片号从3到6

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

plt.figure(figsize=(10, 8))
plt.imshow(china_ndvi, cmap='YlGn', vmin=-0.2, vmax=1)
plt.colorbar(label='NDVI')
plt.title('China NDVI Map')
plt.show()
