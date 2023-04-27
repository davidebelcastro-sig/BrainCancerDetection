import cv2
import random
import numpy as np

def get_contourn(immagine_segmentata):
    for x in range(len(immagine_segmentata)):
        for y in range(len(immagine_segmentata)):
            try:
                if immagine_segmentata[x][y][0] == 0 and  immagine_segmentata[x][y][1] == 255  and  immagine_segmentata[x][y][2] == 0:
                    immagine_segmentata[x][y][0] = 255
                    immagine_segmentata[x][y][1] = 255
                    immagine_segmentata[x][y][2] = 255
                else:
                    immagine_segmentata[x][y][0] = 0
                    immagine_segmentata[x][y][1] = 0
                    immagine_segmentata[x][y][2] = 0
            except:
                pass
    immagine_segmentata =  cv2.cvtColor(immagine_segmentata, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(immagine_segmentata,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours[0]

def remove_border(immagine_iniziale):
    return immagine_iniziale

def modify_light_contorno(immagine_iniziale,contorno,percentuale,segno):
    #immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    copia = immagine_iniziale.copy()
    lista_pixel = []
    cv2.drawContours(copia, [contorno], -1, 255, -1)
    for i in range(0,immagine_iniziale.shape[0]):
        for y in range(0,immagine_iniziale.shape[1]):
            try:
                if copia[i][y] == 255:
                    lista_pixel.append((i,y))
            except:
                pass
    if segno == 1:
        for pixel in lista_pixel:
            immagine_iniziale[pixel[0]][pixel[1]]=min(immagine_iniziale[pixel[0]][pixel[1]] + (immagine_iniziale[pixel[0]][pixel[1]]*percentuale)/100,255)
    else:
        for pixel in lista_pixel:
            immagine_iniziale[pixel[0]][pixel[1]] = max(immagine_iniziale[pixel[0]][pixel[1]] - (immagine_iniziale[pixel[0]][pixel[1]]*percentuale)/100,0)
    return immagine_iniziale

def get_only_contorno(immagine_iniziale,contorno):
    #immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(immagine_iniziale.shape[:2], np.uint8)
    cv2.drawContours(mask, [contorno], -1, 255, -1)
    result = cv2.bitwise_and(immagine_iniziale, immagine_iniziale, mask=mask)
    return result
    
def get_colore(img,x,y):
    i = 0
    while 1:
        i+=1
        try:
            cl_sx = img[x-i][y]
            cl_dx = img[x+i][y]
            if cl_sx == 150:
                if cl_dx != 150:
                    return cl_dx
            else:
                if cl_dx == 150:
                    return cl_sx
                else:
                    return min(cl_sx,cl_dx)
        except:
            pass

def leva_contorno(immagine_iniziale,contorno):
    #immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    for x in range(len(immagine_iniziale)):
        for y in range(len(immagine_iniziale)):
            try:
                if immagine_iniziale[x][y] == 150:
                    colore = get_colore(immagine_iniziale,x,y)
                    immagine_iniziale[x][y] = colore
            except:
                pass
    return immagine_iniziale

def color_contourn(immagine_iniziale,contorno):
    im_copy = immagine_iniziale.copy()
    im_copy = cv2.drawContours(im_copy, [contorno], -1, (0, 0, 255), -1)
    im = cv2.addWeighted(im_copy, 0.4, immagine_iniziale, 1 - 0.2, 0)
    im = cv2.drawContours(im, [contorno], -1, (0, 0, 255), 0)
    return im
    
'''
Main entry point for the filter script
'''
def main(data,path):
    print(data)
    contorno = get_contourn(cv2.imread(path))
    processed = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY)
    if len(data) == 0 or len(data) == 1 or len(data) == 2 or len(data) == 3:
        #* DONE
        print("Error: missing data")
        return []
    elif data[0] != '0':
        check = int(data[0])
        if check>0: 
            segno = 1 
        else: segno = -1
        result = modify_light_contorno(processed,contorno,check,segno)
        if data[1]== 'No' and data[2]== 'No' and data[3]== 'No': 
            #* DONE
            return result
        elif data[1] == 'No' and data[2] == 'Yes' and data[3] == 'No':
            #* DONE
            result = get_only_contorno(result,contorno)
            return result
        elif data[1] == 'No' and data[2] == 'No' and data[3] == 'Yes':
            #* DONE
            result = leva_contorno(result,contorno)
            return result
        elif data[1] == 'Yes':
            print('Non puoi selezionare la colorazione in questa combinazione di filtri')
            return []
        elif data[2] == 'Yes' and data[3] == 'Yes':
            print("Non puoi selezionare il tumore soltanto e l immagine senza contorno")
            return []
        else:
            return []
    elif data[0] == '0' and data[1] == 'Yes' and data[2] == 'Yes' and data[3] == 'No':
        #* DONE
        result = color_contourn(cv2.imread(path),contorno)
        result = get_only_contorno(result,contorno)
        return result
    elif data[0] == '0' and data[1] == 'Yes' and data[2] == 'No' and data[3] == 'No':
        #* DONE
        result = color_contourn(cv2.imread(path),contorno)
        return result
    elif data[0] == '0' and data[1] == 'No' and data[2] == 'Yes' and data[3] == 'No':
        #* DONE
        result = get_only_contorno(processed,contorno)
        return result
    elif data[0] == '0' and data[1] == 'No' and data[2] == 'No' and data[3] == 'Yes':
        #* DONE
        result = leva_contorno(processed,contorno)
        return result
    else:
        print("porcamadonna")
        return []