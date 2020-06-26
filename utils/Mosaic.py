# http://mibix.de/wp-content/uploads/2017/08/mosaic.py_.txt
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import natsort 
import numpy as np

width      = 290 #684
height     = 229 #1024

B_width=int(width/4)

rows       = 10
columns    = 10
def Mosaic(img_path,outfile):
    img_list   = []



    filelist=[]
    for file in os.listdir(img_path):
        if file.endswith(".png"):
            filelist.append( file ) 


    sorted_files=natsort.natsorted(filelist)

    for file in sorted_files:    
        img_list.append( Image.open(img_path+ file ) )

    for image in img_list:
        # resize images
        image.thumbnail( (width, height) )

    columns = len(img_list)/rows

    #creates a new empty image, RGB mode
    mosaic = Image.new( 'RGB', (  int(columns * (width+B_width)), int(rows * height) ),color = 'black')

    # Prepare draw and font objects to render text
    draw   = ImageDraw.Draw(mosaic)

    k=0
    


    for j in range( 0, int(rows * height), height ):
        for i in range( 0, int(columns * (width+B_width)), width+B_width ):
            print(k, i, j)
            
            
            blanks = Image.new( 'RGB', (  int(B_width), int(height) ) , color = 'black')
            d = ImageDraw.Draw(blanks)
            font = ImageFont.truetype("Times New Roman Bold.ttf", 60)
            d.text((0,0), str(k), fill="white",font=font)            
            mosaic.paste( blanks, (i,j) )

            mosaic.paste( img_list[k], (i+B_width,j) )
            k = k + 1

    # Save image to file
    mosaic.save(outfile)