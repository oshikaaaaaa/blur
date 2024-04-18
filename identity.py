import preprocess
import pytesseract
import numpy as np
import cv2


strings_to_check = ["name", "address", "addres", "adress", "age", "gender", "sex", "mane"]

string_dict = {string: 0 for string in strings_to_check}

def resetter(string_dict):
    for key in string_dict:
        string_dict[key] = 0


def black_box(image, x, y, w, h):
    black_region = np.zeros((h, w, 3), dtype=np.uint8)
    black_region.fill(0)  
    image[y:y+h, x:x+w] = black_region
    
    return image

def blurrer(image):
    height,width,_=image.shape
    text_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    print(text_data['text'])
    for i in range(len(text_data['text'])):
        text = text_data['text'][i]
        for str in strings_to_check:
            if string_dict[str]==0:
                if str in text.lower():
                    incx=5000
                    incy=200
                    decx=1000
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
                    image = black_box(image, x, y, w, h)
                    string_dict[str]=1
                    string_dict['name']=string_dict['mane']
                    string_dict['address']=string_dict['addres']=string_dict['adress']
                    string_dict['sex']=string_dict['gender']
                    print(string_dict)
                    
    return image


def identityremover(input_image_path,output_image_path):
    image=cv2.imread(input_image_path)
    image=blurrer(image)
    #image=preprocess.preprocess_for_ocr(image)
    #image=blurrer(image)                            #ek choti preprocess nagari image blur garne ani tyo blur gareko lai feri preprocess garera blur garne
    resetter(string_dict)
    cv2.imwrite(output_image_path,image)
    return image                                       #aile lai euta pass le nai pugyo last ma lol





