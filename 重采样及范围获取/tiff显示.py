from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# 打开图像
img = Image.open('D:\Python\pythonProject1\论文\Forest0.5_mark.tif')

# 使用 PIL 来显示图像
img.show()

# 或者使用 matplotlib 显示，如果你需要更复杂的图形处理
plt.imshow(img)
plt.title('TIFF Image')
plt.show()

image_arr=np.array(img)

print(image_arr)