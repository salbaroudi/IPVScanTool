from PIL import Image, ImageOps, ImageFilter
from numpy import array, zeros
from math import floor, ceil
from matplotlib import pyplot



'''
Experimental Script coded by Sean al-Baroudi sean.al.baroudi@gmail.com

Note: The below represents a "Failed Idea" for the algorithm. I did Horizontal and Vertical Binning as the final
solution to this problem.

This script utilizes the fact that edge noise on our black background seems to be below 50-80 pixel intensity,
when our image is transformed and converted to greyscale.
I use thresholding to detect when the "page edge" is found.
A number of lines are drawn in H and V directions, to find this edge. It is then averaged, and the corner points
for the crop is found.
'''

#global variables:
imgLoc = "../Standard Setup/standard3.jpg"
noiseThreshold = 100
epsilonBack = 5 #Once we find a point, we step back a few pixels, to reduce overcrop.
rasterPercentage = 0.003
depthPercentage = 0.5 
 
def prepimage():
	im = Image.open(imgLoc)
	im =im.rotate(-90,expand=True) #we need to expand the canvas as image is rectangular
	return im

def workimage(im):
	im2 = im.filter(ImageFilter.FIND_EDGES)
	im2 = im2.filter(ImageFilter.EDGE_ENHANCE)
	im2 = im2.convert("L")
	return im2

#In this method, we calculate our probing lines
def getrasterarray(Lim):
	increment = int(floor(Lim*rasterPercentage)) #doesnt matter if its a few pixels under its true value.
	curPos = 0
	rastArray = zeros(int(floor(1/rasterPercentage)))
	for i in range(0,rastArray.size - 1):
		curPos = curPos + increment
		rastArray[i] = curPos
	return rastArray

def main():
	#get the damn image
	im = prepimage()

	#we need to create a separate image, in which to do analysis.
	im2 = workimage(im)

	imArr = array(im2)

	#Now its time to run our corner finding algorithm, in stages:
	(hLim, vLim) = im.size #note that this follows array notation; thats nice.
	rastArrH = getrasterarray(hLim)
	rastArrV = getrasterarray(vLim)

	#Gary's Idea: Lets bin everything into one vector, and see if the signal overtakes the noise after summing.
	#first, lets get the vertical binning:
	vVector = zeros(vLim)

	for i in range(0, vLim):
		for j in range (0, hLim,4):
			vVector[i] = imArr[i,j] + vVector[i]

	hVector = zeros(hLim)
	for i in range(0, hLim):
		for j in range (0, vLim,4):
			hVector[i] = imArr[j,i] + hVector[i]

	#Lets look at the beast.
	pyplot.plot(vVector)
	pyplot.show()
	pyplot.plot(hVector)
	pyplot.show()
	
	#Lets try histogram binning, to expose the peak.
	vHist = zeros(ceil(vVector.size/4) + 1)
	for i in range(0, vVector.size, 4):
		vHist[int(i/4)] = vVector[int(i/4)] + vVector[int(i/4) + 1] + vVector[int(i/4) + 2] + vVector[int(i/4) + 3]
	
	pyplot.plot(vHist)
	pyplot.show()
	
	#what does our image look like?

	imgfinal = Image.fromarray(imArr)
	imgfinal.save('output.png')


'
	print(imArr.shape)
	
	k = 0
	for i in rastArrV:
		for j in rastArrH:
			vVector[k] = imArr[i,j] + vVector[k]
		k = k+1

	hVector = zeros(500)
	k = 0
	for i in rastArrH:
		for j in rastArrV:
			hVector[k] = imArr[j,i] + hVector[k]
		k = k + 1

	#We will probe from the top, and left of the image. This folllows array notation naturally.
	maxHDepth = int(floor(depthPercentage*hLim))
	maxVDepth = int(floor(depthPercentage*vLim))


	edgePointV = zeros(rastArrV.size)
	i = 0
	#lets start vertically:
	for pos in rastArrV:
		for j in range(0,maxHDepth):
			if (imArr[pos,j] >= noiseThreshold):
				edgePointV[i] = j
				break
			imArr[pos,j] = 230
		i = i+1
	print(edgePointV)
	print(imArr[1:10,rastArrV[0]])
	
	imgfinal = Image.fromarray(imArr)
	imgfinal.save('output.png')


if __name__ == "__main__":
	main()


'''
References:
[1] Basic Pillow: http://docs.python-guide.org/en/latest/scenarios/imaging/
[2] Pillow Tutorial: https://pillow.readthedocs.io/en/3.0.x/handbook/tutorial.html
[3] Convert Images: http://stackoverflow.com/questions/9506841/using-python-pil-to-turn-a-rgb-image-into-a-pure-black-and-white-image
[4]  Invert Colors: http://stackoverflow.com/questions/2498875/how-to-invert-colors-of-image-with-pil-python-imaging
[5] Very simple PIL image to array: http://code.activestate.com/recipes/577591-conversion-of-pil-image-and-numpy-array/
[6] Subplots code for Matplotlib : http://matplotlib.org/examples/pylab_examples/subplots_demo.html

'''
