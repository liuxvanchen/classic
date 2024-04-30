from pyhdf.SD import SD, SDC
import re

# 打开 HDF 文件
file_path = "E:\\浏览器下载\\ndvi-evi\\MOD13A3.A2020001.h21v03.061.2020328134849.hdf"
hdf = SD(file_path, SDC.READ)

# 列出文件中的数据集
datasets_dict = hdf.datasets()
for idx, sds in enumerate(datasets_dict.keys()):
    print(idx, sds)

# 获取并打印所有属性
attrs = hdf.attributes(full=True)
print("Available attributes:")
for attr in attrs:
    print(attr)

# # 读取 CoreMetadata.0
# core_metadata = hdf.attributes()['CoreMetadata.0']
#
# # 使用正则表达式查找日期
# date_match = re.search(r'RANGEBEGINNINGDATE\s*=\s*"(.*?)"', core_metadata)
#
# if date_match:
#     start_date = date_match.group(1)
#     print("Data start date:", start_date)
# else:
#     print("Start date not found in CoreMetadata.0")

# 关闭文件
hdf.end()