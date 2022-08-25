from PIL import Image

img_path = 'E:/A_master_learning/done/batch_processing_tool/data/M_N_S_1.jpg'
img = Image.open(img_path)
print(img)
img = img.resize((150, 150), Image.ANTIALIAS)