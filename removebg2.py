from removebg import RemoveBg
from PIL import Image


# Change_picture_background('2.jpg','2.png','#66CC99')

def Change_picture_background(old_file,new_file,color):
    rmbg = RemoveBg("zdj7j4ZLkTrKSxc5dn6MAy8c", "error.log") # 引号内是你获取的API
    rmbg.remove_background_from_img_file(r"E:\py\python3.7\test\test45/"+old_file) #图片地址
    
    path = r"E:\py\python3.7\test\test45/"+ old_file + '_no_bg.png'  
    im = Image.open(path)
    x, y = im.size
    
    # 填充背景
    p = Image.new('RGBA', im.size, color)
    p.paste(im, (0, 0, x, y), im)
    # 保存填充后的图片
    p.save(r"E:\py\python3.7\test\test45/"+new_file)
