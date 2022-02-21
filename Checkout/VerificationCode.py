from email.mime import image
import sys, os
from PIL import Image, ImageDraw
import pytesseract


class VerificationCode():
    def __init__(self,FilePath):
        self.FilePath = FilePath
        self.image = None
        self.t2val = {}
        self.replaceList = list('\n\t,./\\?;:，。\'\"|-=+()*&^%$#@!~`_— ')
        self.Result = None
    def __str__(self):
        print(f'FilePath:{self.FilePath}\nResult:{self.Result}')
        
    def Delete_Background_Colour(self):
        img=Image.open(self.FilePath)
        w,h=img.size
        for x in range(w):
            for y in range(h):
                # print(img.getpixel((x,y))[0])
                RGBa = img.getpixel((x,y))
                r,g,b=RGBa[0],RGBa[1],RGBa[2]
                if 190<=r<=255 and 170<=g<=255 and 0<=b<=140:
                    img.putpixel((x,y),(0,0,0))
                if 0<=r<=90 and 210<=g<=255 and 0<=b<=90:
                    img.putpixel((x,y),(0,0,0))
        img=img.convert('L').point([0]*150+[1]*(256-150),'1')
        self.image = img.convert('L')
        
 
    def twoValue(self, G=100):
        image = self.image
        for y in range(0, image.size[1]):
            for x in range(0, image.size[0]):
                g = image.getpixel((x, y))
                if g > G:
                    self.t2val[(x, y)] = 1
                else:
                    self.t2val[(x, y)] = 0


    # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
    # G: Integer 图像二值化阀值
    # N: Integer 降噪率 0 <N <8
    # Z: Integer 降噪次数
    # 输出
    #  0：降噪成功
    #  1：降噪失败
    def ClearNoise(self, N=3, Z=2):
        image = self.image
        for i in range(0, Z):
            self.t2val[(0, 0)] = 1
            self.t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    nearDots = 0
                    L = self.t2val[(x, y)]
                    if L == self.t2val[(x - 1, y - 1)]:
                        nearDots += 1
                    if L == self.t2val[(x - 1, y)]:
                        nearDots += 1
                    if L == self.t2val[(x - 1, y + 1)]:
                        nearDots += 1
                    if L == self.t2val[(x, y - 1)]:
                        nearDots += 1
                    if L == self.t2val[(x, y + 1)]:
                        nearDots += 1
                    if L == self.t2val[(x + 1, y - 1)]:
                        nearDots += 1
                    if L == self.t2val[(x + 1, y)]:
                        nearDots += 1
                    if L == self.t2val[(x + 1, y + 1)]:
                        nearDots += 1

                    if nearDots < N:
                        self.t2val[(x, y)] = 1

        
    def ClearNoiseProcess(self):
        image = self.image
        size = image.size
        image = Image.new("1", size)
        draw = ImageDraw.Draw(image)

        for x in range(0, size[0]):
            for y in range(0, size[1]):
                draw.point((x, y), self.t2val[(x, y)])

        # image.save(filename)
        self.image = image
    
    def recognize_captcha(self):
        # im = Image.open(img_path)
        im = self.image

        num = pytesseract.image_to_string(im)
        for i in self.replaceList:
            num = num.replace(i,'')
        print(num)
        return num


if __name__ == '__main__':
    object = VerificationCode(r'pic\2.jpg')
    object.Delete_Background_Colour()
    object.twoValue()
    object.ClearNoise()
    object.ClearNoiseProcess()
    object.recognize_captcha()
    