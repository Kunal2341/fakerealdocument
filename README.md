
# Detecting if a document real or fake

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
