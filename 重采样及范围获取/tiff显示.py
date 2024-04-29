from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# 打开图像
img = Image.open('E:\\人工林数据\\2020pnf.tif')

# 使用 PIL 来显示图像
img.show()

# 或者使用 matplotlib 显示，如果你需要更复杂的图形处理
plt.imshow(img)
plt.title('TIFF Image')
plt.show()

image_arr=np.array(img)

print(image_arr)