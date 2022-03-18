#time:2022/3/12  17:13
#author:Hu_Guangliang
#
from PIL import Image
import numpy as np
from typing import List
#用户操作区###############################
IMG_PATH='雾.png'
YU_ZHI=20          #阈值越大亮度越低
FAN_ZHUAN=1         #黑白反转
#图像大小，裁剪前
PIX_H=30            #图像高
PIX_W=32            #图像宽
#裁剪属性
W_START=0           #裁剪x开始位置
W_END= PIX_W - 0       #裁剪x结束位置
H_START=0           #裁剪y开始位置
H_END= PIX_H - 0       #裁剪y结束位置
#输出格式
MODE='W'            #H/W，纵向扫描/横向扫描
NAME='mai'          #const变量命名
NUM_W=16            #每行数据个数



def Print_C51(C51_list,name,height_t,width_t):
    count = 0
    print('const unsigned char BMP_' + name + '_' + str(width_t) + 'X' + str(height_t) + '[] U8X8_PROGMEM= { ')
    for i in C51_list:
        print('0x{:02x},'.format(i),end='')
        count += 1
        if (count % NUM_W == 0):
            print('')
    print('};\n')
def CkeckBMP(bmp_list,width_t,height_t):
    if MODE=='W':
        if width_t % 8 != 0:
            width_t = width_t + (8 - width_t % 8)
        ck_array = np.empty(shape=(height_t, width_t), dtype=np.uint8)
        width_t=int(width_t/8)
        for i in range(0,height_t):
            for k in range(0,width_t):
                for p in range(0,8):
                    ck_array[i][k*8+p]=bmp_list[i*width_t+k]%2
                    bmp_list[i * width_t + k] /= 2
    elif MODE=='H':
        if height_t%8!=0:
            height_t = height_t + (8 - height_t % 8)
        ck_array = np.empty(shape=(height_t, width_t), dtype=np.uint8)
        height_t = int(height_t /8)
        print(height_t)
        for i in range(0,height_t):
            for k in range(0,width_t):
                for p in range(0,8):
                    ck_array[i*8+p][k]=bmp_list[i*width_t+k]%2
                    bmp_list[i * width_t + k] /= 2
    ck_img = Image.fromarray(255 * ck_array)
    ck_img.save('CkeckBMP.bmp')  # 预览

def jinzhi_16(pp:List[int]):
    temp111=np.uint8(0);
    for i in range(7,-1,-1):
        temp111=temp111<<1
        if i<(len(pp)):
            temp111+=pp[i]
        else:
            temp111+=1-FAN_ZHUAN
    # print(temp111)
    return np.uint8(temp111)

# 创建大小缩放图片
img_file=Image.open(IMG_PATH)
if img_file.format=='PNG':
    for yh in range(img_file.size[1]):
        for xw in range(img_file.size[0]):
            dot=(xw,yh)
            color_d=img_file.getpixel(dot)
            if(color_d[3]==0):
                color_d=(255,255,255,255)
                img_file.putpixel(dot,color_d)
img_file=img_file.resize((PIX_W, PIX_H))
print('img_file:    ',img_file.format, img_file.mode, img_file.size, img_file.palette)
#创建灰度图
img_L=img_file.convert('L')
# img_L.show()
img_L.save('huidu.bmp')
print('img_L:       ',img_L.mode,img_L.size)
#创建图像转数组
img_array=np.array(img_L)
print(img_array.shape, W_START, W_END, H_START, H_END)
img_array= img_array[H_START:H_END, W_START:W_END]
print(img_array.shape)
#创建%8扩容存储二值化的数组np.empty
height,width=img_array.shape
height_2=height%8
height_8=int(height/8)+(1 if height_2!=0 else 0)
width_2=width%8
width_8=int(width/8)+(1 if width_2!=0 else 0)

#二值化数组,反转
for i in range(0, height):
    for k in range(0,width):
        if(img_array[i][k]>YU_ZHI):
            img_array[i][k]= 1 - FAN_ZHUAN
        else:
            img_array[i][k]=FAN_ZHUAN
        img_array[i][k] = img_array[i][k]
        print(img_array[i][k], end='')
    print('')

new_img = Image.fromarray(255 * img_array)
new_img.save('生成.bmp')#预览


#输出C51格式
out_list=[]
if(MODE=='W'):
    for i in range(0, height):
        # print(i)
        for k in range(0,width_8):
            out_list.append(int(jinzhi_16(img_array[i][k * 8:k * 8 + 8 if k * 8 + 8<width else width] )))
elif(MODE=='H'):
    for i in range(0,height_8):
        for k in range(0,width):
            fw_list = []
            for p in range(i*8,(i*8+8 if i*8+8<height else height)):
                fw_list.append(img_array[p][k])
            out_list.append(int(jinzhi_16(fw_list)))



Print_C51(out_list,NAME,height,width)
CkeckBMP(out_list,width,height)


img_file.close()