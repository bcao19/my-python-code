from removebg import RemoveBg
from PIL import Image


# Change_picture_background('2.jpg','2.png','#66CC99')
# https://blog.csdn.net/qq_45365214/article/details/122321656

def Change_picture_background(old_file,new_file,color):
    rmbg = RemoveBg("zdj7j4ZLkTrKSxc5dn6MAy8c", "error.log") # 引号内是你获取的API
    rmbg.remove_background_from_img_file(r"E:/"+old_file) #图片地址
    
    path = r"E:/"+ old_file + '_no_bg.png'  
    im = Image.open(path)
    x, y = im.size
    
    # 填充背景
    p = Image.new('RGBA', im.size, color)
    p.paste(im, (0, 0, x, y), im)
    # 保存填充后的图片
    p.save(r"E:/"+new_file)
    
Change_picture_background('2.jpg','2.png','#66CC99')
