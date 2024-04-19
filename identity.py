import preprocess
import pytesseract
import numpy as np
import cv2


strings_to_check = ["name", "address", "addres", "adress", "age", "gender", "sex", "mane"]

string_dict = {string: 0 for string in strings_to_check}  #yo dict ko indiviual key ko value change garera repitions herna milxa. aile chai sab ko 0 xa. eg ma name:0 (ani mane:0) vaesi    
                                                            #euta name vetesi arko name blur gardaina (so aru kunai important data ma ni 'name' xa vane blur nahos vanera) aba name=mane:-1 rakhyo
def resetter(string_dict):                                  #vane duita samma herxa and so on 
    for key in string_dict: 
        string_dict[key] = 0


def black_box(image, x, y, w, h,_):
    if _!=0:
       black_region= np.zeros((h, w, 3), dtype=np.uint8)
    else: 
        black_region=np.zeros((h,w), dtype=np.uint8)
    black_region.fill(0)  
    image[y:y+h, x:x+w] = black_region
    
    return image

def blurrer(image):
    height, width, _ = image.shape if len(image.shape) == 3 else (*image.shape, 0)
    text_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    print(text_data['text'])
    for i in range(len(text_data['text'])):
        text = text_data['text'][i]
        for str in strings_to_check:
            if string_dict[str]<=0:                    
                if str in text.lower():
                    incx=5000                           #tweak these values to change the size of the blur
                    incy=200                            #inc x,incy=widhth, heigt of rectangle
                    decx=1000                           #decx, decy=changes(decreases) the coordinates of kata bata suru garne hamro rectangle
                    decy=100
                    x=text_data['left'][i]
                    y=text_data['top'][i]
                    if x-decx<=0:
                        decx=x
                    if x+incx>=width:
                        incx=width-x+decx
                    if y-decy<=0:
                        decy=y
                    if y+incy>=height:
                        incy=height-y+decy
                
                    x, y, w, h = text_data['left'][i]-decx, text_data['top'][i]-decy, incx, incy
                    image = black_box(image, x, y, w, h,_)
                    string_dict[str]=1
                    string_dict['name']=string_dict['mane']
                    string_dict['address']=string_dict['addres']=string_dict['adress']
                    string_dict['sex']=string_dict['gender']
                    print(string_dict)
                    
    return image


def identityremover(input_image_path,output_image_path):
    image=cv2.imread(input_image_path)
    image=blurrer(image)
    image=preprocess.preprocess_for_ocr(image)      #comment out this line and line 65 for faster loading tara kunai kunai xutna sakne chance badi hunxaa
    image=blurrer(image)                            #ek choti preprocess nagari image blur garne ani tyo blur gareko lai feri preprocess garera blur garne
    image=preprocess.skew_image(image,-2)           #2 degree left gareraa scan gareko feri 2 degree right garera scan gareko
    image=blurrer(image)                            #comment out garda ni hunxa speed badxa dherai jaso ta yettikai scanned hunxa
    image=preprocess.skew_image(image,+4)           #line 66-70 comment out garda speed badxa
    image=blurrer(image)
    image=preprocess.skew_image(image,-2)           #afai skew angle patta launa sake jhan ramro tara garoo layo tyo 
    resetter(string_dict)
    cv2.imwrite(output_image_path,image)
    return image                                       





identityremover("nijiya.jpg","helo.jpg")