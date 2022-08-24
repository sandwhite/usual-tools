from PIL import Image
from skimage import io


# img_name = r"C:\Users\Administrator.OH5LC2FJLY4OLHK\Desktop\新建文件夹\21\1 (26).png"

# img = io.imread(img_name)
# print(img.dtype.name)

def is_color_image(url):
    im = Image.open(url)
    pix = im.convert('RGB')
    width = im.size[0]
    height = im.size[1]
    oimage_color_type = "Grey Image"
    is_color = []
    for x in range(width):
        for y in range(height):
            r, g, b = pix.getpixel((x, y))
            r = int(r)
            g = int(g)
            b = int(b)
            if (r == g) and (g == b):
                pass
            else:
                # print(r, g, b)
                oimage_color_type = 'Color Image'
    return oimage_color_type


print(is_color_image(r"E:\plate-recognition\train_images\training-set\chinese-characters\3\debug_chineseMat38.jpg.bmp"))

#is_color_image(r"E:\OCR-platerecog\pictures\1.jpg")

