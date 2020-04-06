# Detect Real or Fake Documents
As my project for Vdart, I created a series of tests to test if a document is real or fake. The user inputs 2 files, and it out puts with a series of values and does a series of checks to compare if document is real. Series of tests:
Check https://github.com/Kunal2341/fakerealdocument for more information
As of right now to the working percentage is **58%**
| Foldername |  Real| Fake| Documents| Percentage Score|Weighted Threshold| Normal Threshold|
|-----------|-------|------|-----------|------------------|---------------|-----------------|
|test_04-05_13|8|2|10|**90%**|-|*Guess*|
|testFINALCOLAB_04-05_54|15|13|28|**55%**|-|*Guess*|
|-----------|-------|------|-----------|------------------|---------------|----------------|
|on colab run 4 and 5|45|0|45|**60.37%**|-|43.75
|on colab run 4 and 5|45|0|45|**53.33%**|-|50|\n",
|on colab run 4 and 5|45|0|45|**59.25%**|93.75|-|
|on colab run 4 and 5|45|0|45|**96.29%**|90|-|
|-----------|-------|------|-----------|------------------|---------------|-----------------|
|on colab run 1|0|6|6|**33.33%**|-|43.75|
|on colab run 1|0|6|6|**33.33%**|-|50|
|on colab run 1|0|6|6|**0%**|93.75|-|
|on colab run 1|0|6|6|**50%**|90|-
|-----------|-------|------|-----------|------------------|---------------|-----------------|
|on colab run 2|0|22|22|**21.16%**|-|43.75|
|on colab run 2|0|22|22|**30.43%**|-|50|
|on colab run 2|0|22|22|**50%**|93.75|-|
|on colab run 2|0|22|22|**0%**|90|-|
# Weightage 
As an attempt to make the code better. I added a weightage to the numbers. As the numbers are further from the threshold, the higher weighted it is to the final score and hence a more powerful test. Still in development.

# Values
- MAINIMAGEFILEPNG = path for detecting image png
- MAINPDFFILE = path for detecting image pdf
- COMPAREIMAGEFILEPNG = path for real image
- result1Final = barcode from the tesseract text detected
- result2Final = barcode from the tesseract text detected part 2
- barcodeDetected = barcode value from decoding barcode
- DATEWORKING = final True/False of date
- WHYDATEISWORKING = reason why date is true or false
- The following follow the same basic idea
	- It takes the title part of both images and subtracts each array (if they were the same picture then the subtracted array will be 0). Each one of these percents is a different threshold. Max is 255 and min is 0. 
	- **50**
		- PERCENT_BLUE_DIFFERENCE_TITLE, 
		- PERCENT_GREEN_DIFFERENCE_TITLE,
	    - PERCENT_RED_DIFFERENCE_TITLE, 												
	- **80**
		- PERCENT_BLUE_DIFFERENCE_TITLE11, 
		- PERCENT_GREEN_DIFFERENCE_TITLE11, 
		- PERCENT_RED_DIFFERENCE_TITLE11, 
	- **30**
	- PERCENT_BLUE_DIFFERENCE_TITLE22, 
	- ERCENT_GREEN_DIFFERENCE_TITLE22, 
	- PERCENT_RED_DIFFERENCE_TITLE22,
- TITLEIMAGECOMPARE = final compare with a threshold of 15 percent (only for the orginal 50)
- similar = uses SequenceMatcher to compare similarty between the texts
- diffsimiliar = personal way to check if the texts are similar
- diffdifferent = personal way to check if the texts are similar
- The following follow the same basic idea
- This is the watermark comparision. It compares both of the images watermarks.
    - coorect, worng, error, **Basic Watermark compare**
    - aveCorrect, aveWRONG, aveERROR, **Using average pixels Watermark compare**
    - correctPT2,wrongPT2, errorPT2 **Basic Watermark compare part 2 method**
- WATERMARKOUTPUTFINAL = Final output of the watermark
- score = SSIM score
- perdiff = Percent difference between them
- NumberKeyPointsIMG1 = keypoints count unknown image
- NumberKeyPointsIMG2 = keypoints count known image
- TotalMatches = total matches between the images
- MatchesRatioTest 0.6 = ratio test with 0.6 number of matches
- MatchesRatioTest 0.65 = ratio test with 0.65 number of matches
- MatchesRatioTest 0.7 = ratio test with 0.7 number of matches
- MatchesDistanceTest 80 = distance test with 80 number of matches
- MatchesDistanceTest 85 = distance test with 85 number of matches
- MatchesDistanceTest 90 = distance test with 90 number of matches

# Detecting if a document real or fake

What it does, is that it **compares 2 files**. The user inputs 2 files, and it out puts with a series of values and does a series of checks to compare if document is real. 
Series of tests:

- Barcode
	- Score Down For More Info
- Date detection 
	- Score Down For More Info
- Title Comparision
	- Score Down For More Info
- Text Comparision
	- Compares the two texts that are detected from the PNG using tesseract
- WaterMark
	- 3 tests
		- Average WaterMark
		- Normal Watermark
		- Detail Watermark
 - Shape of image
	 - The image is taken in by `cv2.imread` which converts image to a numpy array. 
	 - Some times the images are different sizes which can mess up the comparision
	 - Every image is converted into a `698` by `910` size. 
 - The SSIM score 
	 - Stands for *Structural Similarity Index*.
		 - The mean structural similarity over the image.
	 - This is the average similiarty between both images.
	 - For real documents comapres
		 - between `0.3` and `0.5`
	 - For fake documents compares
		 - between `0.1` and `0.28`
 - The Percent Difference
	 - This is the overall difference between the images
	 - Unlike the SSIM this is a direct comparision in the numpy array. It uses patterns in the numpy array and draw boxes around the values. 
	 - Usually, the document comparision ouputs with values over 100% which means parts of the images are overlayed, which is expected 
 - The number of key points
	 - Using  `cv2.xfeatures2d.SIFT_create()` and `sift.detectAndCompute()` this creates a series of **Critical points** in the image. This is later used to draw comparisions
 - The total number of matches
	 - Using the critical points, it compared the two images, and matches each critical point to its closest, value in the other image
 - Matches for the distance test
	 - When comparing the images, some of the vectors drawn may be false, so using a **distance parameter**, we can detect (for the most part) if the lines are **horizontal** (we want, since documents are right next to each other) or if they have a **slope** (dont want).
 - Matches for the ratio test
	 - Using the **Lowe's ratio test** it will be able to remove the some of the values. 
	 - In order to get the exact ratio number, I did a series of test, drew a graph, and a table, and using the average, amount of good_matches, I can acurattly detect the perfect ratio number. 

## Water Mark
### PART 1

This converts the document into a 2D ARRAY and loops through all the values. It checks for each RGB value if it is between **239 and 248**. 
If YES then converts it to a green pixel (**[0, 255, 0]**) and if NO then it converts to (**[0, 0, 0]**). 
```python
    down = 239 #238 ----- 239 
	up = 248 # ---------248
	array = cv2.imread(file1)
	arrayNew = cv2.imread(file1)
	img = Image.open(file1)
	w, h = img.size
	rgb_im = img.convert('RGB')
	print(w, h)
	for x in range(909):
	    for y in range(697):
	        try:
	            singlearray = array[x, y]
	            r = singlearray[0]
	            g = singlearray[1]
	            b = singlearray[2]
	            if (r > down and r < up and g > down and g < up and b > down and b < up):
	                arrayNew[x, y] = [0, 255, 0]
	            else:
	                arrayNew[x, y] = [0, 0, 0]
	        except:
	            print(x, y)
	img = Image.fromarray(arrayNew)
	img
```
![Image](https://github.com/Kunal2341/fakerealdocument/blob/master/Editedasof2-28removedAgain.jpg)


As you can see in this picture, there are many green pixels that shouldn't be there. They are randomly around the document. We will fix this in part 2. 
### PART 2
Loops through all `618800` pixels.  For each pixel it creates a square around it based on the distance :

| -|  DISTANCE | OF| 2| -|
|--|--|--|-- |--|
| [0,0,0] | [0, 255,0] | [0,0,0]| [0, 0, 0] | [0,0,0] |
| [0,0,0] | [0,0,0]| [0, 255,0]| [0,0,0] | [0, 255,0]|
| [0,0,0] | [0,0,0]| **center [0, 255, 0]** | [0,0,0]| [0, 255,0]|
| [0, 255,0] | [0,0,0] | [0, 255,0]| [0, 255,0] | [0,0,0]|
| [0,0,0]| [0,0,0] | [0,0,0]| [0,0,0] | [0, 255,0] |

This is an example of an array for one of the pixels. As you can see there are **16** black pixels (`[0,0,0]`) and there are **8** green pixels ( `[0,255,0]` ) around the center pixel.
PERCENT BLACK = **66.6%**
PERCENT GREEN = **33.3%**
Since the percent black is over a threshold, it converts the center pixel to **BLACK**. 


As a result the final picture will look like 



Main Code
```python
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
```	        

## Process
|Barcode|Date|Title|
|--|--|--|
|Direct from PDF | Convert PNG Document to text using  `pytesseract.image_to_string`| Base picture of title that document is compared to
|Scan entire document, get 3 barcode results | Extract date from text |![Example of title Image](https://github.com/Kunal2341/fakerealdocument/blob/master/COMPARINGIMAGE.png)
|Using `DynamsoftBarcodeReader` Token (get from Kunal)| Compare year, month, day date. | Convert Document PNG to numpy array
|Convert PNG Document to text using `pytesseract.image_to_string`|-|Compare each value, RGB in array
|Extract written barcode and compare values|-| Threshold value `20`
|`Error` faced when converting image to text -> I or 1|-| `Error` when title is titled

# Pdf2image

So for my project I really struggled in converting a pdf to a image so here is a step by step instuction\

1. Install pdf2image 
	1. `pip install pdf2image`
2.  Install poppler
	1. This is very important
	2. [https://poppler.freedesktop.org/](https://poppler.freedesktop.org/)
		3. Click on "https://poppler.freedesktop.org/poppler-0.86.1.tar.xz" 
		4.  This will install a compressed file of poppler so then you use 7zip (must install seperatly)
		5.  Once you extract it, move the file to your specific location
		6. Now you know the poppler location path
3. Make sure you have these libaries imported. Use `pip install` if not working
	4. `import PIL`
	5. `from PIL import Image`
	6. `from pdf2image import convert_from_path`	
	7. `import os`
4. Code
**Make sure you change your poppler path**
```python
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

os.chdir("/Users/kunal/Documents/")
convert_pdf_2_image("/Users/kunal/Documents/", "invite.pdf", (200,200))
```

# As of Feb 20
- Detection of barcode using an API from dynamsoft. (Contact Kunal for the API token). 
	- This detection goes directly through the PDF so no worry about compression of the document when conviriting PNG to JPG or other.
	- The token has a date it will end, but I can extend it
- Date working with comparision. 
	- It converts entire PNG Document to text, and extracts the date and then compares it with each other
- Title 
	- It works sometimes but working on making it stronger for rotated documents.
- Will be working on watermark - IDK

https://www.dynamsoft.com/CustomerPortal/Portal/Triallicense.aspx

## Previous problems faced, 
In order to decode the barcode, I need to crop the image (of the document). There are 2 ways to crop it. Using a numpy array crop or using the PIL image library. Both ways, there is a compression of the image, to a point where barcode can’t be decoded by pyzbar decoder. If I manually crop the image, then the pyzbar decoder will work. I have also attempted to convert the image into black rectangles, to make a more defined barcode but that causes the barcode number to change. I have also tried grayscale but that doesn’t help the outcome. I have tried not cropping all the way and giving some margin but that doesn’t help. In the process of cropping the image and resaving there is a data lose in quality and I have researched and there is no way to fix this. One last way to fix this is to crop the pdf and not convert it to an image and decode the pdf but I am still working on that because that required adding to path variable. Other than this, the date, is working, the title comparison is working, and I have made bigger strides in the text font detection but not fully completed. I am working on creating the detection of real vs fake overall better

# As of Feb 12

- It detects the barcode and the date and compares the date
- Still need to turn pdf to png
- Still need to extract image from png

# Features
 - Dotted line in background
 - Background watermark
 - Check if date matches start and finish
 - 2 pages?
 - Tesseract
	 - 	Font name
	 - Font type
	 - Capital letters Vs non-capital
	 - Font size
	 - Bold
	 - Italic 
	 - Monospace
	 - Point size
	 - Underlined
# Author
Contact me for any questions

 © Vdart 2020
 Kunal Aneja
 kunal.aneja101@gmail.com
