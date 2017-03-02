from PIL import Image, ImageOps, ImageFilter
import numpy
import matplotlib.pyplot as plt

'''
Test code written by Sean al-Baroudi (sean.al.baroudi@gmail.com)

This file tests out our cropping algorithm. It utilizes a simple edge image, and uses array methods
to get 4 corner points in which to accomplish the final crop.

'''

def profiles(arrImg):
	g, axisArr = plt.subplots(2,2)
	axisArr[0,0].plot(arrImg[5,:])
	axisArr[0,0].set_title("10px from top profile")

	axisArr[0,1].plot(arrImg[15,:])
	axisArr[0,1].set_title("400px from top profile")

	axisArr[1,0].plot(arrImg[600,:])
	axisArr[1,0].set_title("600px from top profile")

	axisArr[1,1].plot(arrImg[800,:])
	axisArr[1,1].set_title("800px from top profile")
	plt.show()

im = Image.open("../Standard Setup/standard3.jpg")

#Metadata for this image.
print(im.format,im.size,im.mode)

#rotate the beast:
im =im.rotate(-90,expand=True) #we need to expand the canvas as image is rectangular


#im2 = im2.filter(ImageFilter.EDGE_ENHANCE_MORE)
im2 = im.filter(ImageFilter.FIND_EDGES)
im2 = im2.filter(ImageFilter.EDGE_ENHANCE)
#im2 = im2.filter(ImageFilter.GaussianBlur(radius=3))

im2 = im2.convert("L")
im2.save('output.png')


#Next lets get an array from our image:
arr1 = numpy.array(im2)
#Notation is (Column, row)
#Lets take a look at some of our profiles:
profiles(arr1)


#Other tests and code snippets I tried:
#im3 = ImageOps.invert(im2)
#im4 = im2.convert('1')
#im4.show()
#im5 = im4.filter(ImageFilter.FIND_EDGES)

'''
References:
[1] Basic Pillow: http://docs.python-guide.org/en/latest/scenarios/imaging/
[2] Pillow Tutorial: https://pillow.readthedocs.io/en/3.0.x/handbook/tutorial.html
[3] Convert Images: http://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-image-into-a-pure-black-and-white-image
[4]  Invert Colors: http://stackoverflow.com/questions/2498875/how-to-invert-colors-of-image-with-pil-python-imaging
[5] Very simple PIL image to array: http://code.activestate.com/recipes/577591-conversion-of-pil-image-and-numpy-array/
[6] Subplots code for Matplotlib : http://matplotlib.org/examples/pylab_examples/subplots_demo.html
'''
