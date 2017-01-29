from PIL import Image, ImageOps, ImageFilter
from numpy import array, zeros
from math import floor, ceil
from matplotlib import pyplot
from os import listdir, chdir
import getopt, sys


#The getOpt page has shown me a new code style, so I will use it. All credit goes to the person who
#wrote that page:

helpString = '''Usage of ipvscantool:

ipvscantools -h -v -d -i -n [filenaming] [folder to read] [folder to write to]

	-h: Help string for console.
	-v: Version information.
	-d: Delete temp files in folder, after you are done (stupidly hunts for all .jpg files, and kills them). 
	-n: Prefix for naming of files.
	-i: Invert image colors.
	-t: threshold counts for page boundary in Edge image analysis. Default is 10000.
	-e: Epsilon Margin for crop; can be positive (bigger crop) or negative (smaller crop). Default is zero
	-s: Skip Step; when histograming, only every xth pixel is considered. Define X with this. Default is 3

Other Notes:
	- Script will autorotate and crop images, based on predefined standard.
	- if no -n arg given, items will be numbered sequentially (1,2,3....png) 
	- images are saved as .pngs
	- Max scan area assumed: European A4 letter paper.
	- if destination folder does not exist, system will automatically create one.

'''

versionString = '''
 
ipvscantools version 0.1. Created by Sean al-Baroudi (sean.al.baroudi@gmail.com)
'''

#Our getopt global variables:
deleteSwitch = False
invertSwitch = False
filePrefix = ""

inputDir = ""
outputDir = ""

#Crop algorithm global variables:
threshold = 10000
epShift = 0 #Once we find a point, we step back a few pixels, to reduce overcrop.
skipStep = 3
#[1]

def printparameters():
	print("threshold:" + str(threshold))
	print("epShift:" + str(epShift))
	print("skipStep:" + str(skipStep))
	return

def processargs():
	global deleteSwitch, invertSwitch, filePrefix, inputDir, outputDir #[2]
	global threshold, skipStep
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvdin:t:s:")
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	if (len(args) != 2):
		print("Two folder destinations (input and output) need to be given. Check argument string.")
		sys.exit(2)

	inputDir = args[0]
	outputDir = args[1]
	
	print("inputDir is:" + inputDir)
	print("outputDir is:" + outputDir)

	#I could be a lot more robust in error checking. This will follow in a later version.
	for o, a in opts:
		if o == "-h":
			print(helpString)
		elif o == "-v":
			print(versionString)
		elif o == "-i":
			invertSwitch = True
		elif o == "-d":
			deleteSwitch = True
		elif (o == "-n" and  a != ""): 
			filePrefix = a
		elif (o == "-t" and  a != ""):  #target threshold
			threshold = int(a)
		elif (o == "-s" and  a != ""):  #skipstep (to speed up histogram calcs)
			skipStep = int(a)
		else:
			print("An unrecognized option or format has appeared. Please check your argument string")
			sys.exit(2)

	printparameters()
	return

def prepimage(imLoc):
	im = Image.open(imLoc)
	im =im.rotate(-90,expand=True) #we need to expand the canvas as image is rectangular
	return im

def getworkimage(im):
	im2 = im.filter(ImageFilter.FIND_EDGES)
	im2 = im2.filter(ImageFilter.EDGE_ENHANCE)
	im2 = im2.convert("L")
	return im2

def checkhistograms(vVector,hVector):
	pyplot.plot(vVector)
	pyplot.show()
	pyplot.plot(hVector)
	pyplot.show()
	return

#Idea is simple: for a vector, find where the plateau starts, given an arbitrary threshold. This gives us
#4 numbers, which allows us to form our coordinates.
def findcorners(vVector,hVector): 
	tVCoord = 0
	for i in range(0, vVector.size):
		if (vVector[i] >= threshold):
			tVCoord = i
			break
	bVCoord = 0
	for i in range((vVector.size -1), 0, -1):
		if (vVector[i] >= threshold):
			bVCoord = i
			break
	lHCoord = 0
	for i in range(0,hVector.size):
		if (hVector[i] >= threshold):
			lHCoord = i
			break
	rHCoord = 0
	for i in range((hVector.size -1),0,-1):
		if (hVector[i] >= threshold):
			rHCoord = i
			break

	print("tVCoord:" + str(tVCoord))
	print("bVCoord:" + str(bVCoord))
	print("lHCoord:" + str(lHCoord))
	print("rHCoord:" + str(rHCoord))
	
	#We found them
	return (lHCoord - epShift,tVCoord - epShift,rHCoord + epShift,bVCoord + epShift)

def cropimagealg(imLoc):
	#get image
	openIm = prepimage(imLoc)
	#we need to create a separate image, in which to do analysis.
	workIm = getworkimage(openIm)
	imArr = array(workIm)
	
	#Gary's Idea: Lets bin everything into one vector, and see if the signal overtakes the noise after summing.
	#first, lets get the vertical binning:
	#[3]
	(hLim, vLim) = workIm.size 
	vVector = zeros(vLim)
	for i in range(0, vLim):
		for j in range (0, hLim,skipStep):
			vVector[i] = imArr[i,j] + vVector[i]

	hVector = zeros(hLim)
	for i in range(0, hLim):
		for j in range (0, vLim,skipStep):
			hVector[i] = imArr[j,i] + hVector[i]
	
	#checkhistograms(vVector,hVector)
	
	#Now that we have gotten the histograms, lets deal find the corners
	coord4Tup = findcorners(vVector,hVector)
	
	#Finaly, do a crop and save!
	openIm.crop(coord4Tup).save("result.png")
	
	return
	
def main():
	processargs() #everything is global anyways.

	#We have our arguments, lets load our files.
	
	dirList = listdir(inputDir)
	jpgList = []
	for item in dirList:
		if (".jpg" in item):
			jpgList.append(item)
			
	if (len(jpgList) == 0):
		print("No JPGs were found in input directory. Aborting.")
		sys.exit(2)
	
	chdir(inputDir)
	#get a list of all .jpg files (pumped out by IPEVO software)
	#The directory has JPGS, lets move on.
	for imgName in jpgList:
		cropimagealg(imgName)

if __name__ == "__main__":
	main()

'''
#References:
#[1]: GetOpt for Python3: https://docs.python.org/3.1/library/getopt.html
[2]: global usage is frowned upon, but passing 5 variables via a function is also ugly.
[3]: An older algorithm following horizontal and vertical lines along hte image to probe for the edge of the paper
it was found that the SNR due to reflectivity off the background surface was causing issues. By summing 1D histograms,
our SNR gets pushed up, the the boundaries become much more defined. There is a a larger computational penalty,
as our time is now O(mn), where m and n are the dimensions of the image (which is very large ). I tried skipping every
pth point in order to get O(mn/p) time. If an image takes 10 seconds, thats not too bad.
'''
