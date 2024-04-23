import rasterio

# 打开GeoTIFF文件
with rasterio.open('Forest.tif') as dataset:
    # 获取边界
    bounds = dataset.bounds

    # 打印边界信息
    print("Left:", bounds.left)
    print("Right:", bounds.right)
    print("Bottom:", bounds.bottom)
    print("Top:", bounds.top)

    # 或者直接打印全部边界
    print("Bounds:", bounds)
