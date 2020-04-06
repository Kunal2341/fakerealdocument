#!/usr/bin/env python
# coding: utf-8

# # Detect Real or Fake Documents
# 
# As my project for Vdart, I created a series of tests to test if a document is real or fake. The user inputs 2 files, and it out puts with a series of values and does a series of checks to compare if document is real. Series of tests:
# 
# Check https://github.com/Kunal2341/fakerealdocument for more information
# 
# As of right now to the working percentage is **73%**
# 
# 
# | Foldername |  Real| Fake| Documents| Percentage Score|
# |-----------|-------|------|-----------|------------------|
# |test_04-05_13|8|2|10|**90%**|
# |testFINALCOLAB_04-05_54|15|13|28|**%**|
# 
# 
# 
# 

# # Import

# In[29]:


import matplotlib.ticker as plticker
import cv2
import pytesseract
from PIL import Image
import PIL
from pdf2image import convert_from_path
import os
import numpy as np
import pandas as pd
from dbr import DynamsoftBarcodeReader
from matplotlib import pyplot as plt
from skimage.measure import compare_ssim
import imutils
import statistics
from scipy import stats
import random
from difflib import SequenceMatcher
from IPython.display import display, Markdown, Latex
import shutil
from google.cloud import vision
import io
get_ipython().run_line_magic('matplotlib', 'inline')
from google.oauth2 import service_account


# # Convert PDF 2 IMAGE

# In[30]:


def convert_pdf_2_image(uploaded_image_path, uploaded_image,img_size):
    project_dir = os.getcwd()
    os.chdir(uploaded_image_path)
    file_name = str(uploaded_image).replace('.pdf','')
    output_file = file_name+'.jpg'
    pages = convert_from_path(uploaded_image, 200,poppler_path='/Users/kunal/Documents/VdartWorking/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/')
    for page in pages:
        page.save(output_file, 'JPEG')
        break
    os.chdir(project_dir)
    img = Image.open(output_file)
    img = img.resize(img_size, PIL.Image.ANTIALIAS)
    img.save(output_file)
    return output_file


# # Small Basic Functions

# In[31]:


def checkEqual1(iterator):
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)
def getText(result, partText,text):
    endindex = result + 80
    partialdetected = text[result:endindex]
    endindex = partialdetected.find("\n")
    fulldetected = partialdetected[:endindex]
    startindex = fulldetected.find(partText)#'er'
    barcodeNumberdetectedname = fulldetected[startindex+3:28]
    return barcodeNumberdetectedname
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# # BARCODE

# In[32]:


def barcodefromTextDecoded(imgPath):
    """Detects document features in an image."""
    keyDIR = "/Users/kunal/Documents/VdartWorking/GOOGLEAPI/vdartrealfakevision-0f30bdc03946.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # [START vision_python_migration_document_text_detection]
    with io.open(imgPath, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    textDocument = []
    blockConfid = []
    paraConfid = []
    wordConfid = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    textDocument.append(word_text)
                    blockConfid.append(block.confidence)
                    paraConfid.append(paragraph.confidence)
                    wordConfid.append(word.confidence)
                    #if word_text == "Receipt" or word_text == "Number":
                        #print('\nBlock confidence: {}'.format(block.confidence))
                        #print('Paragraph confidence: {}'.format(paragraph.confidence))
                        #print('Word text: {} (confidence: {})'.format(word_text, word.confidence))
                        #print('\n')

                    #bit = word.symbols
                    #print(bit)
                    #for i in bit:
                        #print(i)

                    #for symbol in word.symbols:
                        #print('\tSymbol: {} (confidence: {})'.format(symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    # [END vision_python_migration_document_text_detection]
    # [END vision_fulltext_detection]
    finalOutputArray = []
    count = 0
    for i in textDocument:
        if i == "Receipt":
            #print(i)
            #print(stringTotal[count+2])  
            #print(blockConfid[count+2])
            #print(paraConfid[count+2])
            #print(wordConfid[count+2])
            miniArray = [textDocument[count+2], blockConfid[count+2], paraConfid[count+2], wordConfid[count+2]]
            finalOutputArray.append(miniArray)
        count+=1
    return finalOutputArray


# # Barcode PT 2

# In[33]:


def barcodeDetectionDecoding(MAINPDFFILE, MAINIMAGEFILEPNG):
    barcodeArray = []
    dbr = DynamsoftBarcodeReader()
    dbr.initLicense('t0068MgAAAKRrPFRco9JDd3LAqC/rxW8uc9WY78TcwhKHwZLx6gk6QEs4fVW5LejQYwCeHQwN0OHv3IaI5ENqLbmYKUpP0/o=') # https://www.dynamsoft.com/CustomerPortal/Portal/Triallicense.aspx
    try:
        results = dbr.DecodeFile(MAINPDFFILE)
        textResults = results["TextResults"]
        for textResult in textResults:
            #print(textResult["BarcodeText"])
            barcodeArray.append(textResult["BarcodeText"])
    except TypeError as e:
        barcodeArray = [] 
    barcodeDetected = ""
    #print(barcodeArray)
    if len(barcodeArray) == 0:
        #print("NO BARCODE DETECTED!!!!")
        barcodeDetected = "N/A"
    elif len(barcodeArray) == 1:
        barcodeDetected = barcodeArray[0]
    elif len(barcodeArray) == 2:
        if similar(barcodeArray[0], barcodeArray[1]) > 0.9:
            barcodeDetected = barcodeArray[0]
    else:
        barcodeDetected = "N/A"
    barcodefromText = barcodefromTextDecoded(MAINIMAGEFILEPNG)
    equal = False
    if len(barcodefromText) == 3:
        result1 = barcodefromText[0][0]
        result2 = barcodefromText[1][0]
        result3 = barcodefromText[2][0]
        if result1 == result2 == result3:
            if barcodeDetected == result1:
                #Everything same
                #print("Same")
                equal = True
            elif len(result1) == len(barcodeDetected):
                #Same Length but different characters
                if similar(result1, barcodeDetected) > 0.9:
                    #print("Estimate that it is same for the most part")
                    equal = True
            elif abs(len(result1) - len(barcodeDetected)) > 3:
                #Barcoder is not fully detected
                equal = False
        elif ((result1 == result2 and similar(result3, result2)>0.9) or 
              (result1 == result3 and similar(result2, result1)>0.9) or 
              (result3 == result2 and similar(result1, result2)>0.9)):
            if (result1 == barcodeDetected or result2 == barcodeDetected or result3 == barcodeDetected):
                equal = True 
        elif (result1 != result2 != result3):
            equal = False
        else:
            equal = False
        BARCODEISCORRECT = equal
        result1final = result1
        result2final = result2
    if len(barcodefromText) == 2:
        result1 = barcodefromText[0][0]
        result2 = barcodefromText[1][0]
        if result1 == result2:
            if barcodeDetected == result1:
                #Everything same
                #print("Same")
                equal = True
            elif len(result1) == len(barcodeDetected):
                #Same Length but different characters
                if similar(result1, barcodeDetected) > 0.9:
                    #print("Estimate that it is same for the most part")
                    equal = True
            elif abs(len(result1) - len(barcodeDetected)) > 3:
                #Barcoder is not fully detected
                equal = False
        elif (similar(result1, result2)>0.9):
            if (result1 == barcodeDetected or result2 == barcodeDetected):
                equal = True 
        elif (result1 != result2):
            equal = False
        else:
            equal = False
        BARCODEISCORRECT = equal
        result1final = result1
        result2final = result2
    if len(barcodefromText) == 1:
        result1 = barcodefromText[0][0]
        if barcodeDetected == result1:
            equal = True
        elif len(result1) == len(barcodeDetected):
            #Same Length but different characters
            if similar(result1, barcodeDetected) > 0.9:
                #print("Estimate that it is same for the most part")
                equal = True
        elif abs(len(result1) - len(barcodeDetected)) > 3:
            #Barcoder is not fully detected
            equal = False
        else:
            equal = False
        BARCODEISCORRECT = equal
        result1final = result1
        result2final = ""
    return barcodeDetected, BARCODEISCORRECT, result1final, result2final


# # DATE

# In[34]:


def dateDetection(MAINIMAGEFILEPNG):
    keyDIR = "/Users/kunal/Documents/VdartWorking/GOOGLEAPI/vdartrealfakevision-0f30bdc03946.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(MAINIMAGEFILEPNG, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)
    textDocument = []
    blockConfid = []
    paraConfid = []
    wordConfid = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    textDocument.append(word_text)
                    blockConfid.append(block.confidence)
                    paraConfid.append(paragraph.confidence)
                    wordConfid.append(word.confidence)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    finalOutputArray = []
    count = 0
    for i in textDocument:
        if i == "Valid":
            for i in range(13):
                finalOutputArray.append(textDocument[count+i])
        count+=1
    finalOutputArray.pop(0)
    finalOutputArray.pop(0)
    startArray = finalOutputArray[:5]
    endArray = finalOutputArray[6:]
    count = 0
    for i in startArray:
        if i == "/":
            startArray.pop(count)
        count+=1
    count = 0
    for i in endArray:
        if i == "/":
            endArray.pop(count)
        count+=1
    start = startArray
    end = endArray
    work = False
    reason = ""
    if ((len(start) == 3) and (len(end) == 3)):    
        if(start[2] > end[2]):
            work = False
            reason = "Year is before the starting one"
        if(start[2] == end[2]):
            if(end[0] < start[0]):
                work = False
                reason = "Month Doesn't Work"
            if(end[0] > start[0]):
                work = True
                reason = "Month Works"
            if(end[0] == start[0]):
                if(end[1] < start[1]):
                    work = False
                    reason = "Day Doesn't Work"
                if(end[1] > start[1]):
                    work = True
                    reason = "Day Works"
                if(end[1] == start[1]):
                    work = False
                    reason = "Date Same"
        if(start[2] < end[2]):
            work = True
            reason = "Year Works"
        try: 
            if(int(start[1]) > 31 or int(end[1]) > 31 or int(start[0]) > 12 or int(end[0]) > 12):
                work = False
                reason = "Date out of bounds"
        except ValueError as e:
            print(e)
    else:
        work = False
        reason = "The array is wrong"

    DATEWORKING = work
    WHYDATEISWORKING = reason
    return (DATEWORKING, WHYDATEISWORKING)


# # TITLE COMPARE

# In[35]:


def titleCOMPARE(CLEANARRAYFORMAINIMAGEFILEPNG, CLEANARRAYFORCOMPAREIMAGEFILEPNG):
    titleimgCV = CLEANARRAYFORMAINIMAGEFILEPNG[0:50, 10:650]
    titleimgCV2= CLEANARRAYFORCOMPAREIMAGEFILEPNG[0:50, 10:650]
    original = titleimgCV2 #know real
    duplicate = titleimgCV #dont know
    threshold = 50
    TITLEIMAGECOMPARE = False
    if original.shape == duplicate.shape:
        difference = cv2.subtract(original, duplicate)
        b, g, r = cv2.split(difference)
    x,y = b.shape
    size = x*y
    countb = 0
    countg = 0
    countr = 0
    countb11 = 0
    countg11 = 0
    countr11 = 0
    countb22 = 0
    countg22 = 0
    countr22 = 0
    for startthing1 in b:
        for endthomg1 in startthing1:
            if endthomg1 > 80:
                countb11+=1
            if endthomg1 > 50:
                countb+=1
            if endthomg1 > 30:
                countb22+=1
    for startthing2 in g:
        for endthomg2 in startthing2:
            if endthomg2 > 80:
                countg11+=1
            if endthomg2 > 50:
                countg+=1
            if endthomg2 > 30:
                countg22+=1    

    for startthing3 in r:
        for endthomg3 in startthing3:
            if endthomg3 > 80:
                countr11+=1
            if endthomg3 > 50:
                countr+=1
            if endthomg3 > 30:
                countr22+=1   
    PERCENT_BLUE_DIFFERENCE_TITLE = countb/size*100
    PERCENT_GREEN_DIFFERENCE_TITLE = countg/size*100
    PERCENT_RED_DIFFERENCE_TITLE = countr/size*100
    PERCENT_BLUE_DIFFERENCE_TITLE11 = countb11/size*100
    PERCENT_GREEN_DIFFERENCE_TITLE11 = countg11/size*100
    PERCENT_RED_DIFFERENCE_TITLE11 = countr11/size*100
    PERCENT_BLUE_DIFFERENCE_TITLE22 = countb22/size*100
    PERCENT_GREEN_DIFFERENCE_TITLE22 = countg22/size*100
    PERCENT_RED_DIFFERENCE_TITLE22 = countr22/size*100
    
    if PERCENT_BLUE_DIFFERENCE_TITLE < 15 and PERCENT_GREEN_DIFFERENCE_TITLE < 15 and PERCENT_RED_DIFFERENCE_TITLE < 15:
        TITLEIMAGECOMPARE = True
    return (PERCENT_BLUE_DIFFERENCE_TITLE, PERCENT_GREEN_DIFFERENCE_TITLE, PERCENT_RED_DIFFERENCE_TITLE,
            PERCENT_BLUE_DIFFERENCE_TITLE11, PERCENT_GREEN_DIFFERENCE_TITLE11, PERCENT_RED_DIFFERENCE_TITLE11,
            PERCENT_BLUE_DIFFERENCE_TITLE22, PERCENT_GREEN_DIFFERENCE_TITLE22, PERCENT_RED_DIFFERENCE_TITLE22, 
            TITLEIMAGECOMPARE)


# # TEXT COMPRE

# In[36]:


def textCOMPARE(MAINIMAGEFILEPNG, COMPAREIMAGEFILEPNG):
    keyDIR = "/Users/kunal/Documents/VdartWorking/GOOGLEAPI/vdartrealfakevision-0f30bdc03946.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    with io.open(MAINIMAGEFILEPNG, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    totalString = ''
    for text in texts:
        totalString+=text.description
    totalString = totalString.rsplit(' ', 1)[0]

    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    with io.open(COMPAREIMAGEFILEPNG, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    totalString2 = ''
    for text in texts:
        totalString2+=text.description
    totalString2 = totalString2.rsplit(' ', 1)[0]
    text = totalString
    text2 = totalString2
    yes = 0
    no = 0
    totoal = 0
    for i in range(100):
        startingValueofSTring = random.randint(1,len(text2))
        lengthofString = random.randint(3,10)
        small_string = text2[startingValueofSTring:startingValueofSTring+lengthofString]
        has_small_string = False
        if small_string in text:
            has_small_string = True
        if has_small_string:
            yes+=1
        else:
            no+=1
        totoal+=1
    diffsimiliar = yes/totoal
    diffdifferent = no/totoal
    similiar = similar(text, text2)
    if (similiar < 0.35):
        SIMILARTYBETWEENTEXTINDOCUMENT = False
    else:
        SIMILARTYBETWEENTEXTINDOCUMENT = True
    return SIMILARTYBETWEENTEXTINDOCUMENT, similiar, diffsimiliar, diffdifferent


# # WaterMark 1

# In[37]:


def waterMark1(CLEANARRAYFORMAINIMAGEFILEPNG, CLEANARRAYFORCOMPAREIMAGEFILEPNG):
    down2 = 239
    up2 = 248 
    array = CLEANARRAYFORMAINIMAGEFILEPNG
    arrayNew = CLEANARRAYFORMAINIMAGEFILEPNG
    w, h, j = array.shape
    array2 = CLEANARRAYFORCOMPAREIMAGEFILEPNG
    arrayNew2 = CLEANARRAYFORCOMPAREIMAGEFILEPNG
    w2, h2, j2 = array2.shape
    falsepixel = 0
    correctpixel = 0
    totalpixel = 0
    for x2 in range(w2-1):
        for y2 in range(h2-1):
            singlearray2 = array2[x2, y2]
            r2 = singlearray2[0]
            g2 = singlearray2[1]
            b2 = singlearray2[2]
            if (r2 > down2 and r2 < up2 and g2 > down2 and g2 < up2 and b2 > down2 and b2 < up2):
                arrayNew2[x2, y2] = [0, 255, 0]
                singlearray = array[x2,y2]
                r = singlearray[0]
                g = singlearray[1]
                b = singlearray[2]
                if (r > down2 and r < up2 and g > down2 and g < up2 and b > down2 and b < up2):
                    correctpixel +=1
                elif (r == 0 and g == 0 and b == 0):
                    falsepixel+=1
                totalpixel+=1
            else:
                arrayNew2[x2, y2] = [0, 0, 0]
    img2final = Image.fromarray(arrayNew2)
    im1 = img2final.save("REALImageWaterMark.jpg")
    return (correctpixel, falsepixel, totalpixel)


# # WaterMark2

# In[38]:


def WaterMark2(CLEANARRAYFORMAINIMAGEFILEPNG, CLEANARRAYFORCOMPAREIMAGEFILEPNG):
    down = 239#238 ----- 239 
    up = 248 # ---------248
    array = CLEANARRAYFORMAINIMAGEFILEPNG
    array2 = CLEANARRAYFORCOMPAREIMAGEFILEPNG
    arrayNew = CLEANARRAYFORMAINIMAGEFILEPNG
    arrayNew2 = CLEANARRAYFORCOMPAREIMAGEFILEPNG
    w,h,c = array.shape
    w2,h2,c2 = array2.shape
    NUMOFPIXELSHOULDTHEREBUTNOT = 0
    NUMOFPIXELNOTBUTTHERE = 0
    NUMOFCORRECTPIXEL = 0
    totalCOUNT = 0
    for x in range(w-1):
        for y in range(h-1):
            singlearray = array[x, y]
            r = singlearray[0]
            g = singlearray[1]
            b = singlearray[2]
            if (r > down and r < up and g > down and g < up and b > down and b < up):
                definitivVALUE = True
                totalCOUNT+=1
                arrayNew[x, y] = [0, 255, 0]
            else:
                definitivVALUE = False
                arrayNew[x, y] = [0, 0, 0]
            singlearray2 = array2[x, y]
            r2 = singlearray2[0]
            g2 = singlearray2[1]
            b2 = singlearray2[2]
            if (r2 > down and r2 < up and g2 > down and g2 < up and b2 > down and b2 < up):
                pixelDONTKNOW = True
            else:
                pixelDONTKNOW = False
            if(definitivVALUE and pixelDONTKNOW):
                #WHEN PIXEL SHOULD BE IN RANGE AND IS IN RANGE
                NUMOFCORRECTPIXEL+=1
            elif(definitivVALUE and not pixelDONTKNOW):
                #WHEN PIXEL SHOULD BE IN RANGE BUT ISNT
                NUMOFPIXELSHOULDTHEREBUTNOT+=1
            elif(not definitivVALUE and definitivVALUE):
                #WHEN PIXEL SHOULDN'T BE IN RANGE BUT IS
                NUMOFPIXELNOTBUTTHERE+=1      
    img = Image.fromarray(arrayNew)
    file1 = 'REALImageWaterMark.jpg'
    return array2, file1, NUMOFPIXELSHOULDTHEREBUTNOT, NUMOFPIXELNOTBUTTHERE, NUMOFCORRECTPIXEL, totalCOUNT
    


# # WaterMark Average

# In[39]:


def WaterMarkAverage(file1, array2):
    down = 239#238 ----- 239 
    up = 248
    row = []
    column = []
    array = cv2.imread(file1)
    x_length = len(array[0])
    y_length = len(array)
    for i in range(x_length):
        row.append(str(i))
    for i in range(y_length):
        column.append(str(i))
    df = pd.DataFrame(index=row, columns=column)
    array = cv2.imread(file1)
    arrayNew = cv2.imread(file1)
    NUMOFPIXELSHOULDTHEREBUTNOTAVERAGE = 0
    NUMOFPIXELNOTBUTTHEREAVERAGE = 0
    NUMOFCORRECTPIXELAVERAGE = 0
    totalCOUNTAVERAGE = 0
    definitivVALUEAVERAGE = False
    distance = 4
    dis = distance
    for thingthing in range(len(array[0])-distance):
        for thingthingYY in range(len(array)-distance):
            center_XXX = thingthing
            center_YYY = thingthingYY
            distance = dis
            partArrDis = [[0 for x in range(distance*2+1)] for y in range(distance*2+1)]
            center_XX = center_XXX
            center_YY = center_YYY
            for uu in range(distance*2+1):
                for rr in range(distance*2+1):
                    a,b,c = array[uu+(thingthingYY-distance*2+1)][rr+(thingthing-distance*2+1)]
                    theSingleArrayABC = [a,b,c]
                    partArrDis[uu][rr] = theSingleArrayABC
            countGreen = 0
            countBlack = 0
            totalCount = 0
            theXofARRRAY = len(partArrDis)
            theYofARRRAY = len(partArrDis[0])
            for aa in range(theXofARRRAY):
                for bb in range(theYofARRRAY):
                    singleARRAYwPART = partArrDis[aa][bb]
                    rr, gg, bb = singleARRAYwPART
                    if rr < 40 and gg < 40 and bb < 40:
                        countBlack += 1
                    else:
                        countGreen += 1    
                    totalCount+=1
            perceBlack = (countBlack/totalCount) * 100
            perceGreen = (countGreen/totalCount) * 100
            x = perceBlack+perceGreen
            IDK_X = center_XXX-distance*2+1
            IDK_Y = center_YYY-distance*2+1
            if (perceBlack > 30):
                arrayNew[IDK_Y][IDK_X]=[0,0,0]
                definitivVALUEAVERAGE = False
            else:
                arrayNew[IDK_Y][IDK_X] = [0,255,0]
                definitivVALUEAVERAGE = True
            singlearray2 = array2[thingthingYY, thingthing]
            r2 = singlearray2[0]
            g2 = singlearray2[1]
            b2 = singlearray2[2]
            if (r2 > down and r2 < up and g2 > down and g2 < up and b2 > down and b2 < up):
                pixelDONTKNOWAVERAGE = True
            else:
                pixelDONTKNOWAVERAGE = False
            if(definitivVALUEAVERAGE and pixelDONTKNOWAVERAGE):
                #WHEN PIXEL SHOULD BE IN RANGE AND IS IN RANGE
                NUMOFCORRECTPIXELAVERAGE+=1
            elif(definitivVALUEAVERAGE and not pixelDONTKNOWAVERAGE):
                #WHEN PIXEL SHOULD BE IN RANGE BUT ISNT
                NUMOFPIXELSHOULDTHEREBUTNOTAVERAGE+=1
            elif(not definitivVALUEAVERAGE and definitivVALUEAVERAGE):
                #WHEN PIXEL SHOULDN'T BE IN RANGE BUT IS
                NUMOFPIXELNOTBUTTHEREAVERAGE+=1     
            totalCOUNTAVERAGE+=1
    img = Image.fromarray(arrayNew)
    im1 = img.save("GroupedPixeledIMAGE.jpg")
    return NUMOFCORRECTPIXELAVERAGE, NUMOFPIXELSHOULDTHEREBUTNOTAVERAGE, NUMOFPIXELNOTBUTTHEREAVERAGE, totalCOUNTAVERAGE


# # Per Diff

# In[40]:


def perdifference(CLEANARRAYFORMAINIMAGEFILEPNG, CLEANARRAYFORCOMPAREIMAGEFILEPNG):    
    img1 = CLEANARRAYFORMAINIMAGEFILEPNG
    img2 = CLEANARRAYFORCOMPAREIMAGEFILEPNG
    imageA = CLEANARRAYFORMAINIMAGEFILEPNG
    imageB = CLEANARRAYFORCOMPAREIMAGEFILEPNG
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    bigH, bigW,other = imageA.shape
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype('uint8')
    thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    areaDIFFERENCE = 0
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
        areaDIFFERENCE += (w*h)
    perdiff =  ((areaDIFFERENCE/(bigW*bigH))*100)
    
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)
    NUMBER_OF_KEYPOINST_IMG1 = len(keypoints_1)
    NUMBER_OF_KEYPOINST_IMG2 = len(keypoints_2)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    matches = bf.match(descriptors_1,descriptors_2)
    matches = sorted(matches, key = lambda x:x.distance)
    totalMATCHES = (len(matches))
    if img1 is None or img2 is None:
        exit(0)
    minHessian = 400
    detector = cv2.xfeatures2d_SURF.create(hessianThreshold=minHessian)
    keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
    keypoints2, descriptors2 = detector.detectAndCompute(img2, None)
    matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
    ratio_thresh1 = 0.6
    good_matches1 = []
    for m,n in knn_matches:
        if m.distance < ratio_thresh1 * n.distance:
            good_matches1.append(m)
    ratio_thresh2 = 0.65
    good_matches2 = []
    for m,n in knn_matches:
        if m.distance < ratio_thresh2 * n.distance:
            good_matches2.append(m) 
    ratio_thresh3 = 0.7
    good_matches3 = []
    for m,n in knn_matches:
        if m.distance < ratio_thresh3 * n.distance:
            good_matches3.append(m)
    NUMEBROFMATCHESRATIOTESTFOR06 = len(good_matches1)
    NUMEBROFMATCHESRATIOTESTFOR065 = len(good_matches2)
    NUMEBROFMATCHESRATIOTESTFOR07 = len(good_matches3)
    img_matches = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], 3), dtype=np.uint8)
    img3 = cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches2, img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    im = Image.fromarray(img3)
    im.save('FINALWORKINGIMAGEPT1.png')
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    good1 = []
    for m,n in matches:
        if m.distance < 80:
            good1.append([m])
        if n.distance < 80:
            good1.append([n])
    good2 = []
    for m,n in matches:
        if m.distance < 85:
            good2.append([m])
        if n.distance < 85:
            good2.append([n])
    good3 = []
    for m,n in matches:
        if m.distance < 90:
            good3.append([m])
        if n.distance < 90:
            good3.append([n])         
    NUMEBROFMATCHESDISTANCETESTFOR80 = len(good1)
    NUMEBROFMATCHESDISTANCETESTFOR85 = len(good2)
    NUMEBROFMATCHESDISTANCETESTFOR90 = len(good3)
    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good2,None,flags =2)
    im = Image.fromarray(img3)
    im.save('FINALWORKINGIMAGEPT2.png')
    return (score,
            perdiff, 
            NUMBER_OF_KEYPOINST_IMG1, NUMBER_OF_KEYPOINST_IMG2, # number 1 is unknow image
            totalMATCHES,
            NUMEBROFMATCHESRATIOTESTFOR06, NUMEBROFMATCHESRATIOTESTFOR065, NUMEBROFMATCHESRATIOTESTFOR07,
            NUMEBROFMATCHESDISTANCETESTFOR80, NUMEBROFMATCHESDISTANCETESTFOR85, NUMEBROFMATCHESDISTANCETESTFOR90)


# # labelDetect

# In[41]:


def labelDetect(MAINIMAGEFILEPNG):
    with io.open(MAINIMAGEFILEPNG, 'rb') as image_file:
        content = image_file.read()
    keyDIR = "/Users/kunal/Documents/VdartWorking/GOOGLEAPI/vdartrealfakevision-0f30bdc03946.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    LabelDetectionArray = []
    for label in response.label_annotations:
        textandConfArray = []
        textandConfArray.append(label.description)
        textandConfArray.append(label.score*100)
        LabelDetectionArray.append(textandConfArray)
    real = 0
    fake = 0
    for i in range(len(LabelDetectionArray)):
        name = LabelDetectionArray[i][0]
        confid = LabelDetectionArray[i][1]
        if name == "Text":
            if confid > 95:
                real+=1
            else:
                fake+=1
        if name == "Font":
            if confid > 73:
                real+=1
            else:
                fake+=1 
        if name == "Font":
            if confid > 70:
                real+=1
            else:
                fake+=1 
        if name == "Font":
            if confid > 70:
                real+=1
            else:
                fake+=1
    LLabel1 = ""
    LConfid1 = 0
    LLabel2 = ""
    LConfid2 = 0
    LLabel3 = ""
    LConfid3 = 0
    
    if len(LabelDetectionArray) == 0:
        LLabel1 = ""
        LConfid1 = 0
        LLabel2 = ""
        LConfid2 = 0
        LLabel3 = ""
        LConfid3 = 0
    elif len(LabelDetectionArray) == 1:
        LLabel1 = LabelDetectionArray[0][0]
        LConfid1 = LabelDetectionArray[0][1] 
        LLabel2 = ""
        LConfid2 = 0
        LLabel3 = ""
        LConfid3 = 0
    elif len(LabelDetectionArray) == 2:
        LLabel1 = LabelDetectionArray[0][0]
        LConfid1 = LabelDetectionArray[0][1] 
        LLabel2 = LabelDetectionArray[1][0]
        LConfid2 = LabelDetectionArray[1][1]
        LLabel3 = ""
        LConfid3 = 0
    elif len(LabelDetectionArray) >= 3:
        LLabel1 = LabelDetectionArray[0][0]
        LConfid1 = LabelDetectionArray[0][1] 
        LLabel2 = LabelDetectionArray[1][0]
        LConfid2 = LabelDetectionArray[1][1]
        LLabel3 = LabelDetectionArray[2][0]
        LConfid3 = LabelDetectionArray[2][1]
    else: 
        print("Something wrong with Label")
        
    return (LLabel1, LConfid1, LLabel2, LConfid2, LLabel3, LConfid3)


# # Weight Code

# In[42]:


def weightage(Numberoutputed, threshold, weight3pos, weight5pos, weight7pos, weight1pos, weight3neg, weight5neg, weight7neg, weight1neg):
    difference = Numberoutputed - threshold
    if difference > weight1pos: return 1 
    if difference < weight1neg: return 1
    if difference > weight7pos: return 0.7
    if difference < weight7neg: return 0.7
    if difference > weight5pos: return 0.5
    if difference < weight5neg: return 0.5
    if difference > weight3pos: return 0.3
    if difference < weight3neg: return 0.3
    


# In[43]:


def weightageneg(Numberoutputed, threshold, weight3pos, weight5pos, weight7pos, weight1pos, weight3neg, weight5neg, weight7neg, weight1neg):
    difference = threshold- Numberoutputed
    if difference > weight1pos: return 1 
    if difference < weight1neg: return 1
    if difference > weight7pos: return 0.7
    if difference < weight7neg: return 0.7
    if difference > weight5pos: return 0.5
    if difference < weight5neg: return 0.5
    if difference > weight3pos: return 0.3
    if difference < weight3neg: return 0.3
    


# # REAL FAKE

# In[45]:


def realfake(testingPNG, testingPDF, realPNG):
    
    MAINIMAGEFILEPNG = testingPNG
    MAINPDFFILE = testingPDF
    CLEANARRAYFORMAINIMAGEFILEPNG = cv2.imread(MAINIMAGEFILEPNG)
    x11, y11, z11 = CLEANARRAYFORMAINIMAGEFILEPNG.shape
    CLEANARRAYFORMAINIMAGEFILEPNG = cv2.resize(CLEANARRAYFORMAINIMAGEFILEPNG, dsize=(698, 910), interpolation=cv2.INTER_CUBIC)
    COMPAREIMAGEFILEPNG = realPNG
    CLEANARRAYFORCOMPAREIMAGEFILEPNG = cv2.imread(COMPAREIMAGEFILEPNG) 
    x2, y2, z2 = CLEANARRAYFORCOMPAREIMAGEFILEPNG.shape
    CLEANARRAYFORCOMPAREIMAGEFILEPNG = cv2.resize(CLEANARRAYFORCOMPAREIMAGEFILEPNG, dsize=(698, 910), interpolation=cv2.INTER_CUBIC)
    imageCV = CLEANARRAYFORMAINIMAGEFILEPNG
    
    
    
    countREAL = 0
    countFAKE = 0
    weightedScore = 0
    #**********************************************************************
    try:
        barcodeDetected, BARCODEISCORRECT, result1Final, result2Final = barcodeDetectionDecoding(MAINPDFFILE, MAINIMAGEFILEPNG)
        if BARCODEISCORRECT:
            countREAL += 1
            weightedScore +=1
        else:
            countFAKE += 1
        print("BARCODE:\t\t\t", BARCODEISCORRECT)
    except UnboundLocalError as e:
        print(e)
        countFAKE += 1
        barcodeDetected, BARCODEISCORRECT, result1Final, result2Final = "n/a",False,"n/a","n/a"
    #**********************************************************************
    
    
    #**********************************************************************
    DATEWORKING,WHYDATEISWORKING = dateDetection(MAINIMAGEFILEPNG)
    if DATEWORKING:
        countREAL += 1
        weightedScore+=1
    else:
        countFAKE += 1
    print("Date Working:\t\t\t", DATEWORKING)
    #**********************************************************************
    
    
    PERCENT_BLUE_DIFFERENCE_TITLE, PERCENT_GREEN_DIFFERENCE_TITLE, PERCENT_RED_DIFFERENCE_TITLE,PERCENT_BLUE_DIFFERENCE_TITLE11, PERCENT_GREEN_DIFFERENCE_TITLE11, PERCENT_RED_DIFFERENCE_TITLE11,PERCENT_BLUE_DIFFERENCE_TITLE22, PERCENT_GREEN_DIFFERENCE_TITLE22, PERCENT_RED_DIFFERENCE_TITLE22, TITLEIMAGECOMPARE = titleCOMPARE(CLEANARRAYFORMAINIMAGEFILEPNG, CLEANARRAYFORCOMPAREIMAGEFILEPNG)
    
    #**********************************************************************
    percentBlueTitleScore = weightage(PERCENT_BLUE_DIFFERENCE_TITLE, 24.9, 1, 1.5, 3.5, 4, 1, 2, 3.5, 5)
    weightedScore += percentBlueTitleScore
    if (PERCENT_BLUE_DIFFERENCE_TITLE > 24.9): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Blue Title 50:\t\t\t", round(PERCENT_BLUE_DIFFERENCE_TITLE,2), "\t24.9\t ", PERCENT_BLUE_DIFFERENCE_TITLE > 24.9)
    #**********************************************************************
    
    
    #**********************************************************************
    percentRedTitleScore = weightage(PERCENT_RED_DIFFERENCE_TITLE, 25.5, 1, 2, 4, 5.5, 1, 2.5, 3.5, 5)
    weightedScore += percentRedTitleScore
    if (PERCENT_RED_DIFFERENCE_TITLE > 25.5): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Red Title 50:\t\t\t", round(PERCENT_RED_DIFFERENCE_TITLE,2), "\t25.5\t ", PERCENT_RED_DIFFERENCE_TITLE > 25.5)#31
    #**********************************************************************
    
    
    #**********************************************************************
    percentBlueTitleScore11 = weightage(PERCENT_BLUE_DIFFERENCE_TITLE11, 16.9, 2,2.5, 3,4,0.5,2,3,4)
    weightedScore += percentBlueTitleScore11    
    if (PERCENT_BLUE_DIFFERENCE_TITLE11 > 16.9): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Blue Title 80:\t\t\t", round(PERCENT_BLUE_DIFFERENCE_TITLE11,2), "\t16.9\t ", PERCENT_BLUE_DIFFERENCE_TITLE > 16.9)
    #**********************************************************************
    
    
    #**********************************************************************
    percentRedTitleScore11 = weightage(PERCENT_RED_DIFFERENCE_TITLE11, 16.4,1,2,3,4.5,0.5,1,2,4)
    weightedScore += percentRedTitleScore11
    if (PERCENT_RED_DIFFERENCE_TITLE11 > 16.4): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Red Title 80:\t\t\t", round(PERCENT_RED_DIFFERENCE_TITLE11,2), "\t16.4\t ", PERCENT_RED_DIFFERENCE_TITLE11 > 16.4)
    #**********************************************************************
    
    
    #**********************************************************************
    percentRedTitleScore22 = weightage(PERCENT_RED_DIFFERENCE_TITLE22, 32.5,1,1.7,2.3,3.5,1,2,3,4.5)
    weightedScore += percentRedTitleScore22
    if (PERCENT_RED_DIFFERENCE_TITLE22 > 32.5): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Red Title 30:\t\t\t", round(PERCENT_RED_DIFFERENCE_TITLE22,2), "\t34\t ", PERCENT_RED_DIFFERENCE_TITLE22 > 32.5)
    #**********************************************************************
    
    
    SIMILARTYBETWEENTEXTINDOCUMENT, similiar, diffsimiliar, diffdifferent = textCOMPARE(MAINIMAGEFILEPNG, COMPAREIMAGEFILEPNG)
    #**********************************************************************
    #**********************************************************************
    
    correctpixel, falsepixel, totalpixel = waterMark1(CLEANARRAYFORMAINIMAGEFILEPNG, CLEANARRAYFORCOMPAREIMAGEFILEPNG)
    array2, file1, NUMOFPIXELSHOULDTHEREBUTNOT, NUMOFPIXELNOTBUTTHERE, NUMOFCORRECTPIXEL, totalCOUNT = WaterMark2(CLEANARRAYFORMAINIMAGEFILEPNG, CLEANARRAYFORCOMPAREIMAGEFILEPNG)                                                                                                  
    NUMOFCORRECTPIXELAVERAGE, NUMOFPIXELSHOULDTHEREBUTNOTAVERAGE, NUMOFPIXELNOTBUTTHEREAVERAGE, totalCOUNTAVERAGE = WaterMarkAverage(file1, array2)
    
    #**********************************************************************
    WATERMARKOUTPUTFINAL=False
    WATERMARKOUTPUTave=False
    WATERMARKOUTPUT2=False
    WATERMARKOUTPUTFINAL=False
    coorect = correctpixel/totalpixel*100
    worng = falsepixel/totalpixel*100
    #**********************************************************************
    
    #**********************************************************************
    watermark1 = weightageneg(coorect, 8.1,1,2,3.5,4,1,2,3.5,4)
    weightedScore += watermark1
    if (coorect < 8.1): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Watermark 1:\t\t\t", round(coorect,2), "\t 8.1 \t ", coorect < 8.1)
    #**********************************************************************
    
    
    
    #**********************************************************************
    aveCorrect = NUMOFCORRECTPIXELAVERAGE/totalCOUNTAVERAGE *100
    aveWRONG = NUMOFPIXELSHOULDTHEREBUTNOTAVERAGE/totalCOUNTAVERAGE *100
    aveERROR = NUMOFPIXELNOTBUTTHEREAVERAGE
    correctPT2 = NUMOFCORRECTPIXEL/totalCOUNT *100
    wrongPT2= NUMOFPIXELSHOULDTHEREBUTNOT/totalCOUNT*100
    errorPT2 = NUMOFPIXELNOTBUTTHERE
    #**********************************************************************
    
    
    if coorect > 9:
        WATERMARKOUTPUT1 = True 
    else:
        WATERMARKOUTPUT1 = False
    if aveCorrect < 10:
        WATERMARKOUTPUTave = False
    else:
        WATERMARKOUTPUTave = True
    if correctPT2 > 8:
        WATERMARKOUTPUT2 = True
    else:
        WATERMARKOUTPUT2 = False
    if WATERMARKOUTPUT1 == True and WATERMARKOUTPUTave == True and WATERMARKOUTPUT2 == True: 
        WATERMARKOUTPUTFINAL = True
    elif WATERMARKOUTPUT1 == True and WATERMARKOUTPUTave == True and WATERMARKOUTPUT2 == False: 
        WATERMARKOUTPUTFINAL = True
    elif WATERMARKOUTPUT1 == False and WATERMARKOUTPUTave == True and WATERMARKOUTPUT2 == True: 
        WATERMARKOUTPUTFINAL = True
    elif WATERMARKOUTPUT1 == True and WATERMARKOUTPUTave == False and WATERMARKOUTPUT2 == True: 
        WATERMARKOUTPUTFINAL = True
    
                                                                                                          
    score, perdiff, NUMBER_OF_KEYPOINST_IMG1, NUMBER_OF_KEYPOINST_IMG2, totalMATCHES, NUMEBROFMATCHESRATIOTESTFOR06, NUMEBROFMATCHESRATIOTESTFOR065, NUMEBROFMATCHESRATIOTESTFOR07, NUMEBROFMATCHESDISTANCETESTFOR80, NUMEBROFMATCHESDISTANCETESTFOR85, NUMEBROFMATCHESDISTANCETESTFOR90 = perdifference(CLEANARRAYFORMAINIMAGEFILEPNG, CLEANARRAYFORCOMPAREIMAGEFILEPNG)                                        

    #**********************************************************************
    percentDifference1 = weightage(perdiff, 101.65,0.3,0.5,1,1.5,0.3,0.5,1,1.5)
    weightedScore += percentDifference1
    if (perdiff > 101.65): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Percent DIFF:\t\t\t", round(perdiff,2), "\t101.65\t", perdiff > 101.65)
    #**********************************************************************
    
    
    #**********************************************************************
    keypoints1 = weightage(NUMBER_OF_KEYPOINST_IMG1, 4530, 150,300,600,800,200,300,600,800)
    weightedScore += keypoints1
    if (NUMBER_OF_KEYPOINST_IMG1 > 4530): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Keypoints 1:\t\t\t", round(NUMBER_OF_KEYPOINST_IMG1,2), "\t 4530 \t ", NUMBER_OF_KEYPOINST_IMG1 > 4530)
    #**********************************************************************
    
    
    #**********************************************************************
    matches1 = weightage(totalMATCHES,2950, 50,200,300,450,50,200,300,450)
    weightedScore += matches1
    if ( totalMATCHES > 2950): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("TotalMatches:\t\t\t", round(totalMATCHES,2), "\t 2950 \t ", totalMATCHES > 2950)
    #**********************************************************************
    
    
    #**********************************************************************
    ratio07test = weightageneg(NUMEBROFMATCHESRATIOTESTFOR07, 52.5,1,5,8,10,1,5,8,10)
    weightedScore += ratio07test
    if (NUMEBROFMATCHESRATIOTESTFOR07 < 52.5): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Matches Ratio 07:\t\t", round(NUMEBROFMATCHESRATIOTESTFOR07,2), "\t 52.5 \t ",  NUMEBROFMATCHESRATIOTESTFOR07 < 52.5)  
    #**********************************************************************
    
    
    #**********************************************************************
    ratio65test = weightageneg(NUMEBROFMATCHESRATIOTESTFOR065, 31.5,4,8,8,10,4,8,8,10)
    weightedScore += ratio65test
    if (NUMEBROFMATCHESRATIOTESTFOR065 < 31.5): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Matches Ratio 65:\t\t", round(NUMEBROFMATCHESRATIOTESTFOR065,2), "\t 31.5 \t ",  NUMEBROFMATCHESRATIOTESTFOR065 < 31.5)      
    #**********************************************************************
    
    
    #**********************************************************************
    ratio06 = weightage(PERCENT_RED_DIFFERENCE_TITLE, 23.5,5,8,9,10,5,8,9,10)
    weightedScore += ratio06
    if (NUMEBROFMATCHESRATIOTESTFOR06 > 23.5): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Matches Ratio 06:\t\t", round(NUMEBROFMATCHESRATIOTESTFOR06,2), "\t 23.5 \t ",  NUMEBROFMATCHESRATIOTESTFOR06 > 23.5)      
    #**********************************************************************
    
    
    #**********************************************************************
    distance85 = weightageneg(NUMEBROFMATCHESDISTANCETESTFOR85, 44, 1,2,4,8,1,2,4,8)
    weightedScore += distance85
    if (NUMEBROFMATCHESDISTANCETESTFOR85 < 44): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Matches Distance 85:\t\t", round(NUMEBROFMATCHESDISTANCETESTFOR85,2), "\t 44 \t ",  NUMEBROFMATCHESDISTANCETESTFOR85 > 44)   
    #**********************************************************************
    
    
    #**********************************************************************
    distance90 = weightageneg(NUMEBROFMATCHESDISTANCETESTFOR90, 49.5,1,2,3,6,1,2,3,6)
    weightedScore += distance90
    if (NUMEBROFMATCHESDISTANCETESTFOR90 < 49.5): 
        countREAL+=1 
    else: 
        countFAKE+=1
    print("Matches Distance 90:\t\t", round(NUMEBROFMATCHESDISTANCETESTFOR90,2), "\t 50 \t ", NUMEBROFMATCHESDISTANCETESTFOR90 > 50)   
    #**********************************************************************
    
    
    LLabel1, LConfid1, LLabel2, LConfid2, LLabel3, LConfid3 = "n/a","n/a","n/a","n/a","n/a","n/a"

    
    totalCountREALFAKE = countFAKE + countREAL
    realFAKEDocument = countREAL/totalCountREALFAKE * 100
    documentanswer = False
    display(Markdown('**{}**'.format(realFAKEDocument)))
    if countREAL >= 65:
        documentanswer = True
    if documentanswer:
        display(Markdown('**Document is REAL**'))
    else:
        display(Markdown('**Document is FAKE**'))
        
    print("Weighted Score: ", weightedScore)
    print("Weighted Score: ", weightedScore/totalCountREALFAKE * 100)
    

    return (MAINIMAGEFILEPNG, MAINPDFFILE, COMPAREIMAGEFILEPNG, 
            result1Final, result2Final, barcodeDetected, 
            DATEWORKING, WHYDATEISWORKING,
            PERCENT_BLUE_DIFFERENCE_TITLE, PERCENT_GREEN_DIFFERENCE_TITLE, PERCENT_RED_DIFFERENCE_TITLE, #50
            PERCENT_BLUE_DIFFERENCE_TITLE11, PERCENT_GREEN_DIFFERENCE_TITLE11, PERCENT_RED_DIFFERENCE_TITLE11, #80
            PERCENT_BLUE_DIFFERENCE_TITLE22, PERCENT_GREEN_DIFFERENCE_TITLE22, PERCENT_RED_DIFFERENCE_TITLE22, #30
            TITLEIMAGECOMPARE,
            similiar, diffsimiliar, diffdifferent,
            coorect, worng,
            aveCorrect, aveWRONG, aveERROR,
            correctPT2,wrongPT2, errorPT2,
            WATERMARKOUTPUTFINAL,
            score,
            perdiff, 
            NUMBER_OF_KEYPOINST_IMG1, NUMBER_OF_KEYPOINST_IMG2, # number 1 is unknow image
            totalMATCHES,
            NUMEBROFMATCHESRATIOTESTFOR06, NUMEBROFMATCHESRATIOTESTFOR065, NUMEBROFMATCHESRATIOTESTFOR07,
            NUMEBROFMATCHESDISTANCETESTFOR80, NUMEBROFMATCHESDISTANCETESTFOR85, NUMEBROFMATCHESDISTANCETESTFOR90, 
            LLabel1, LConfid1, LLabel2, LConfid2, LLabel3, LConfid3, realFAKEDocument)#47


# # Array Managment

# In[46]:


def appendthefiles(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1,u1,v1):
    aARRAY.append(a)
    bARRAY.append(b)
    cARRAY.append(c)
    dARRAY.append(d)
    eARRAY.append(e)
    fARRAY.append(f)
    gARRAY.append(g)
    hARRAY.append(h)
    iARRAY.append(i)
    jARRAY.append(j)
    kARRAY.append(k)
    lARRAY.append(l)
    mARRAY.append(m)
    nARRAY.append(n)
    oARRAY.append(o)
    pARRAY.append(p)
    qARRAY.append(q)
    rARRAY.append(r)
    sARRAY.append(s)
    tARRAY.append(t)
    uARRAY.append(u)
    vARRAY.append(v)
    wARRAY.append(w)
    xARRAY.append(x)
    yARRAY.append(y)
    zARRAY.append(z)
    a1ARRAY.append(a1)
    b1ARRAY.append(b1)
    c1ARRAY.append(c1)
    d1ARRAY.append(d1)
    e1ARRAY.append(e1)
    f1ARRAY.append(f1)
    g1ARRAY.append(g1)
    h1ARRAY.append(h1)
    i1ARRAY.append(i1)
    j1ARRAY.append(j1)
    k1ARRAY.append(k1)
    l1ARRAY.append(l1)
    m1ARRAY.append(m1)
    n1ARRAY.append(n1)
    o1ARRAY.append(o1)
    p1ARRAY.append(p1)
    q1ARRAY.append(q1)
    r1ARRAY.append(r1)
    s1ARRAY.append(s1)
    t1ARRAY.append(t1)
    u1ARRAY.append(u1)
    v1ARRAY.append(v1)


# In[47]:


aARRAY,bARRAY,cARRAY,dARRAY,eARRAY,fARRAY,gARRAY,hARRAY,iARRAY,jARRAY,kARRAY,lARRAY,mARRAY,nARRAY,oARRAY,pARRAY,qARRAY, rARRAY,sARRAY,tARRAY,uARRAY,vARRAY,wARRAY,xARRAY,yARRAY,zARRAY,a1ARRAY,b1ARRAY,c1ARRAY,d1ARRAY,e1ARRAY,f1ARRAY,g1ARRAY,h1ARRAY,i1ARRAY,j1ARRAY,k1ARRAY,l1ARRAY,m1ARRAY,n1ARRAY,o1ARRAY,p1ARRAY,q1ARRAY, r1ARRAY, s1ARRAY, t1ARRAY, u1ARRAY, v1ARRAY  = ([] for i in range(48))


# # Actual Run

# In[48]:


get_ipython().run_cell_magic('time', '', 'FILEREAL = \'/Users/kunal/Documents/VdartWorking/realFake/Document.jpg\'\n\ntestingDIR = "/Users/kunal/Documents/VdartWorking/NEWDOCUMENTS/Working/test_04-05_13/"\n\nos.chdir(testingDIR)\ncount = 0\n\nfor i in os.listdir(testingDIR):\n    pathName = testingDIR + i.replace(\'.pdf\', \'\')\n    os.mkdir(pathName)\n    shutil.move(i, pathName)\n    finalDir = pathName + "/" + i\n    PicForI = i\n    finalDirPIC = pathName + "/" + PicForI.replace(\'.pdf\', \'.jpg\')\n    os.chdir(pathName)\n    convert_pdf_2_image(pathName, i,(698,910))\n    pngFile = finalDirPIC\n    print(pngFile)\n    #print(finalDir)\n    a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1,u1,v1 = realfake(pngFile, finalDir, FILEREAL)\n    appendthefiles(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,a1,b1,c1,d1,e1,f1,g1,h1,i1,j1,k1,l1,m1,n1,o1,p1,q1,r1,s1,t1,u1,v1)\n    print("DONE", count)\n    os.chdir(testingDIR)\n    count+=1')


# # Final Touches

# In[49]:


aARRAYNEW = []
bARRAYNEW = []
cARRAYNEW = []
for i in aARRAY:
    last_char = i[-30:]
    aARRAYNEW.append(last_char)
for i in bARRAY:
    last_char = i[-30:]
    bARRAYNEW.append(last_char)
for i in cARRAY:
    last_char = i[-12:]
    cARRAYNEW.append(last_char)


# # Conver to Excel

# In[56]:



data = {"Testing PNG": aARRAYNEW,
        "Testing PDF": bARRAYNEW,
        "Real PNG" : cARRAYNEW,
        "Barcode Decoded(1) TXT" : dARRAY,
        "Barcode Decoded(2) TXT" : eARRAY,
        "Barcode Decoded Barcode" : fARRAY,
        "Date Working(T/F)": gARRAY,
        "Reason for Date" : hARRAY,
        "Title Blue 50" : iARRAY,
        "Title Green 50" : jARRAY,
        "Title Red 50" : kARRAY,
        "Title Blue 80" : lARRAY,
        "Title Green 80" : mARRAY,
        "Title Red 80" : nARRAY,
        "Title Blue 30" : oARRAY,
        "Title Green 30" : pARRAY,
        "Title Red 30" : qARRAY,
        "Final Title (T/F)" :rARRAY,
        "Similarty SequenceMatcher TXT": sARRAY,
        "Similarty Correct TXT": tARRAY,
        "Similarty Incorrect TXT" : uARRAY,
        "WaterMark Correct 1": vARRAY,
        "WaterMark False 1": wARRAY,
        #"WaterMark Error 1": yARRAY,
        "WaterMark Ave Correct 2": yARRAY,
        "WaterMark Ave False 2": zARRAY,
        #"WaterMark Ave Error 2": b1ARRAY, zARRAY
        "WaterMark Correct 3": a1ARRAY,
        "WaterMark False 3": b1ARRAY,
        "WaterMark Error 3": c1ARRAY,
        "WaterMark Final (T/F)": d1ARRAY,
        "SSIM Score": e1ARRAY,
        "Percent Difference": f1ARRAY,
        "Testing KeyPoints": g1ARRAY,
        "Known KeyPoints": h1ARRAY,
        "Total Matches": i1ARRAY,
        "Matches Ratio 0.6" :j1ARRAY,
        "Matches Ratio 0.65": k1ARRAY,
        "Matches Ratio 0.7": l1ARRAY,
        "Matches Distance 80": m1ARRAY,
        "Matches Distance 85": n1ARRAY,
        "Matches Distance 90": o1ARRAY,
        "Label 1 Detected" : p1ARRAY,
        "Label 1 Confidence" : q1ARRAY,
        "Label 2 Detected" : r1ARRAY,
        "Label 2 Confidence" : t1ARRAY,
        "Label 3 Detected" : u1ARRAY,
        "FINAL GRADE" : v1ARRAY
       }


# In[57]:


df = pd.DataFrame(data) 
pd.set_option('display.max_columns', 500)
df




df = pd.DataFrame(data) 
df.to_excel("FINALOUTPUTxx.xlsx")  
df


# # Done

# In[ ]:


dfxx = pd.read_excel("/Users/kunal/Documents/VdartWorking/NEWDOCUMENTS/Working/Cut10/TestingFinalBothDir/FINALOUTPUTLOOKSGOOD.xlsx")


# In[ ]:





# In[ ]:





# In[ ]:


dfx = dfxx
df = dfxx
"""dfx = dfx.drop("Testing PNG", axis=1)
dfx = dfx.drop("Real PNG", axis=1)
dfx = dfx.drop("Barcode Decoded(1) TXT", axis=1)
dfx = dfx.drop("Barcode Decoded(2) TXT", axis=1)
dfx = dfx.drop("Barcode Decoded Barcode", axis=1)
dfx = dfx.drop("Date Working(T/F)", axis=1)
dfx = dfx.drop("Testing PNG", axis=1)
dfx = dfx.drop("Testing PNG", axis=1)
dfx = dfx.drop("Testing PNG", axis=1)
dfx = dfx.drop("Testing PNG", axis=1)"""


# In[ ]:


df


# In[ ]:


drop1 = ["Final Title (T/F)","Reason for Date","Testing PDF","Testing PNG", "Real PNG","Barcode Decoded(1) TXT","Barcode Decoded(2) TXT","Barcode Decoded Barcode","Date Working(T/F)"]
drop2 = ["Label 1 Detected","Label 1 Confidence","Label 2 Detected","Label 2 Confidence","Label 3 Detected","Label 3 Confidence"]
drop3 = [ "Matches Ratio 0.7", "Matches Ratio 0.6","Matches Ratio 0.65"]
drop4 = ["Matches Distance 80", "Matches Distance 85", "Matches Distance 90"]
drop5 = ["SSIM Score"]
drop6 = ["Percent Difference"]
drop7 = ["Testing KeyPoints"]
drop8 = ["Known KeyPoints"]
drop9 = ["Total Matches"]
drop10 = ["WaterMark Correct 1","WaterMark False 1","WaterMark Error 1","WaterMark Ave Correct 2","WaterMark Ave False 2","WaterMark Ave Error 2","WaterMark Correct 3","WaterMark False 3","WaterMark Error 3","WaterMark Final (T/F)"]
drop11 = ["Similarty SequenceMatcher TXT","Similarty Correct TXT","Similarty Incorrect TXT"]
dropa1 = ["Title Green 50","Title Green 80","Title Green 30"]
dropa2 = ["Title Red 50","Title Red 80","Title Red 30"]
dropa3 = ["Title Blue 50","Title Blue 80","Title Blue 30"]


# In[ ]:


ax = dfx[drop3].plot(kind='bar', title ="Ratio Test", figsize=(11.25, 7.5), legend=True, fontsize=12)
ax = dfx[drop4].plot(kind='bar', title ="Distance Test", figsize=(11.25, 7.5), legend=True, fontsize=12)
ax = dfx[drop5].plot(kind='bar', title ="SSIM Score", figsize=(11.25, 7.5), legend=True, fontsize=12)


plt.show()


# In[ ]:


ax = dfx[drop6].plot(kind='bar', title ="Percent difference", figsize=(11.25, 7.5), legend=True, fontsize=12)
ax = dfx[drop7].plot(kind='bar', title ="Testing Key Points", figsize=(11.25, 7.5), legend=True, fontsize=12)
ax = dfx[drop8].plot(kind='bar', title ="Known Key Points", figsize=(11.25, 7.5), legend=True, fontsize=12)

plt.show()


# In[ ]:


ax = dfx[drop10].plot(kind='bar', title ="WaterMark", figsize=(11.25, 7.5), legend=True, fontsize=12)
ax = dfx[drop11].plot(kind='bar', title ="Similarty", figsize=(11.25, 7.5), legend=True, fontsize=12)

plt.show()


# In[ ]:





# In[ ]:





# In[ ]:


dfx = dfx.drop(drop1, axis = 1)
dfx = dfx.drop(drop2, axis = 1)
dfx = dfx.drop(drop3, axis = 1)
dfx = dfx.drop(drop4, axis = 1)
dfx = dfx.drop(drop5, axis = 1)
dfx = dfx.drop(drop6, axis = 1)
dfx = dfx.drop(drop7, axis = 1)
dfx = dfx.drop(drop8, axis = 1)
dfx = dfx.drop(drop9, axis = 1)
dfx = dfx.drop(drop10, axis = 1)
dfx = dfx.drop(drop11, axis = 1)
dfx


# In[ ]:





# In[ ]:


dfgreentitle = dfx.drop(dropa2, axis = 1)
dfgreentitle = dfgreentitle.drop(dropa3, axis = 1)

dfredtitle = dfx.drop(dropa1, axis = 1)
dfredtitle = dfredtitle.drop(dropa3, axis = 1)

dfbluetitle = dfx.drop(dropa1, axis = 1)
dfbluetitle = dfbluetitle.drop(dropa2, axis = 1)


# In[ ]:


ax = dfgreentitle.plot.bar(rot=0)


# In[ ]:


ax = dfredtitle.plot.bar(rot=0)


# In[ ]:


ax = dfbluetitle.plot.bar(rot=0)


# In[ ]:


ax = dfx[dropa1].plot(kind='bar', title ="V comp", figsize=(15, 10), legend=True, fontsize=12)


# In[ ]:


