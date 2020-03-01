# Detecting if a document real or fake
## Water Mark
### PART 1

This converts the document into a 2D ARRAY and loops through all the values. It checks for each RGB value if it is between **239 and 248**. 
If YES then converts it to a green pixel (**[0, 255, 0]**) and if NO then it converts to (**[0, 0, 0]**). 

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

*******************ADD IMAGE HERE


Main Code

    distance = 3
	for thingthing in range(len(array[0])-distance):
	    for thingthingYY in range(len(array)-distance):
	        center_XXX = thingthing
	        center_YYY = thingthingYY
	        partArrDis = [[0 for x in range(distance*2+1)] for y in range(distance*2+1)]
	        center_XX = center_XXX
	        center_YY = center_YYY
	        for uu in range(distance*2+1):
	            for rr in range(distance*2+1):
	                a,b,c = array[uu][rr]
	                theSingleArrayABC = [a,b,c]
	                partArrDis[uu][rr] = theSingleArrayABC
	        countGreen = 0
	        countBlack = 0
	        totalCount = 0
	        for aa in range(len(partArrDis)):
	            for bb in range(len(partArrDis[0])):
	                singleARRAYwPART = partArrDis[aa][bb]
	                rr, gg, bb = singleARRAYwPART
	                if rr == 0 and gg == 255 and bb == 0:
	                    countGreen += 1
	                else:
	                    countBlack += 1
	                totalCount+=1
	        perceBlack = (countBlack/totalCount) * 100
	        perceGreen = (countGreen/totalCount) * 100
	        x = perceBlack+perceGreen
	        if x != 100:
	            print("ERROR")
	        

## Process
|Barcode|Date|Title|
|--|--|--|
|Direct from PDF | Convert PNG Document to text using  `pytesseract.image_to_string`| Base picture of title that document is compared to
|Scan entire document, get 3 barcode results | Extract date from text |![Example of title Image](https://github.com/Kunal2341/fakerealdocument/blob/master/COMPARINGIMAGE.png)
|Using `DynamsoftBarcodeReader` Token (get from Kunal)| Compare year, month, day date. | Convert Document PNG to numpy array
|Convert PNG Document to text using `pytesseract.image_to_string`|-|Compare each value, RGB in array
|Extract written barcode and compare values|-| Threshold value `20`
|`Error` faced when converting image to text -> I or 1|-| `Error` when title is titled


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
