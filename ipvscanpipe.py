from PIL import Image, ImageOps, ImageFilter
from numpy import array, zeros
from math import floor, ceil
from matplotlib import pyplot
from os import listdir, chdir, remove
import getopt, sys

#The getOpt page has shown me a new code style, so I will use it. All credit goes to the person who
#wrote that page:

helpString = '''Usage of ipvscantool:

ipvscantools -h -v -n [filenaming] -t [num+] -e [num+] -m [num+] -s [num+] -r [folder to read] -w [folder to write to]

	-h: Help string for console.
	-v: Version information.
	-n: Prefix for naming of files.
	-t: Threshold counts for page boundary in edge image analysis. Default is 10000.
	-e: Epsilon Margin for crop; is a positive margin that tightens the crop. Default is zero
	-m: numPrefix: a positive number in which we start our image enumeration (naming scheme on saving).
	-s: Skip Step; when histograming, only every xth pixel is considered. Define X with this. Default is 3

Other Notes:
	- Script will autorotate and crop images, based on predefined standard position [<--].
	- if no -n arg given, items will be numbered sequentially (1,2,3....png)
	- images are saved as .pngs
	- if destination folder does not exist, system will automatically create one.

Example Usage(s):
	ipvscantools -n scandocs -t 12000 -e 5 ./input ./Output

'''
versionString = '''

ipvscantools v0.2. Created by Sean al-Baroudi (sean.al.baroudi@gmail.com)
'''

#To avoid heavy global usage, and large argument tuples, I use
#an object to store the command line arguments the user specifies.
class Params:
	def __init__(self):
		self.filePrefix = "" #-n
		self.numStart = 1 #-m
		#Crop algorithm global variables:
		self.threshold = 10000 #-t
		self.epShift = 0 #-e
		self.skipStep = 3 #-s
		#Arguments:
		self.inputDir = ""
		self.outputDir = ""

#Signature: Obj[Params] -> NoneType
#Purpose: This implements our GetOpt Logic, and pulls arguments from
#command line.
def processargs(argObj):
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvn:t:s:e:m:r:w:")
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	if (len(opts) < 1):
		print("No detected arguments. Aborting.")
		sys.exit(2)

	for o, a in opts:
		if o == "-h":
			print(helpString)
			sys.exit(2)
		elif o == "-v":
			print(versionString)
			sys.exit(2)
		elif (o == "-n" and  a != ""):
			argObj.filePrefix = a
		elif (o == "-m" and  a != ""):
			argObj.numStart = int(a)
		elif (o == "-e" and  a != ""):
			argObj.epShift = int(a)
		elif (o == "-t" and  a != ""):
			argObj.threshold = int(a)
		elif (o == "-s" and  a != ""):
			argObj.skipStep = int(a)
		else:
			print("An unrecognized option or format has appeared. Please check your argument string")
			sys.exit(2)

	if (len(args) < 2):
		print("No detected input/output folder arguments. Aborting.")
		sys.exit(2)

	argObj.inputDir = args[0]
	argObj.outputDir = args[1]
	return #Dont need to return object; function already points to original.

#Signature: String -> Obj[Image]
#Purpose: Just open and rotate the image.
def prepimage(imLoc):
	im = Image.open(imLoc)
	im =im.rotate(-90,expand=True) #we need to expand the canvas as image is rectangular
	return im

#Signature: Obj[Image] -> Obj[Image]
#Signature: Highlight edges and enhance, for the histogram alg.
def getworkimage(im):
	im2 = im.filter(ImageFilter.FIND_EDGES)
	im2 = im2.filter(ImageFilter.EDGE_ENHANCE)
	im2 = im2.convert("L")
	return im2

#Signature: Array Array Obj[Params] -> Int Int Int Int
#Purpose: Idea is simple: for a vector, find where the plateau
#starts, given an arbitrary threshold. This gives us
#four numbers, which allows us to form our coordinates.
def findcorners(vVector,hVector,par):
	tVCoord = 0
	thold = par.threshold
	for i in range(0, vVector.size):
		if (vVector[i] >= thold):
			tVCoord = i
			break
	bVCoord = 0
	for i in range((vVector.size -1), 0, -1):
		if (vVector[i] >= thold):
			bVCoord = i
			break
	lHCoord = 0
	for i in range(0,hVector.size):
		if (hVector[i] >= thold):
			lHCoord = i
			break
	rHCoord = 0
	for i in range((hVector.size -1),0,-1):
		if (hVector[i] >= thold):
			rHCoord = i
			break

	#For debugging
	#_checkhistograms(vVector, hVector)
	#_checkcropalgcorners(tVCoord, bVCoord, lHCoord, rHCoord)

	ep = par.epShift
	#We found them
	return (lHCoord + ep,tVCoord + ep,rHCoord - ep,bVCoord - ep)

#Signature: String Obj[Params] -> Void
#Purpose: Main Alg method. Side-Effect: Image opened, processed
#and then saved.
def cropimagealg(imLoc,par):
	#get image
	print(imLoc)
	openIm = prepimage(imLoc)
	#we need to create a separate image, in which to do analysis.
	workIm = getworkimage(openIm)
	imArr = array(workIm)

	#Idea: Lets bin everything into one vector, and see if the signal overtakes the noise after summing.
	#first, lets get the vertical binning:
	#[3]
	(hLim, vLim) = workIm.size
	vVector = zeros(vLim)
	for i in range(0, vLim):
		for j in range (0, hLim, par.skipStep):
			vVector[i] = imArr[i,j] + vVector[i]

	hVector = zeros(hLim)
	for i in range(0, hLim):
		for j in range (0, vLim,par.skipStep):
			hVector[i] = imArr[j,i] + hVector[i]

	#Now that we have gotten the histograms, lets deal find the corners
	coord4Tup = findcorners(vVector,hVector,par)

	#Local bindings:
	place = par.outputDir + "/" + par.filePrefix
	#Finaly, do a crop and save!
	tempImg = openIm.crop(coord4Tup).save(place + str(par.numStart) + ".png")
	print("Cropping of Image " + place + str(par.numStart) + ".png" + " is complete.")
	par.numStart = par.numStart + 1 #Because the field is immutable, nStart doesnt matter anymore.
	return

#Diagnostic Functions for inspecting/development are below.
#Signature: Void -> Void
#Purpose (Side-Effect): Print out input parameters (diagnostic).
def _printparameters(argObj):
	print("filePrefix:" + str(argObj.filePrefix))
	print("numStart:" + str(argObj.numStart))
	print("inputDir:" + str(argObj.inputDir))
	print("outputDir:" + str(argObj.outputDir))
	print("threshold:" + str(argObj.threshold))
	print("epShift:" + str(argObj.epShift))
	print("skipStep:" + str(argObj.skipStep))
	return

#Signature: Array, Array -> Void
#Purpose (Side-Effect): Produce two plots to inspect histogram.
def _checkhistograms(vVector,hVector):
	pyplot.plot(vVector)
	pyplot.show()
	pyplot.plot(hVector)
	pyplot.show()
	return

#Signature: Void -> Void
#Purpose (Side-Effect): Print out crop alg parameters (diagnostic).
def _checkcropalgcorners(tVCoord,bVCoord,lHCoord,rHCoord):
	print("tVCoord:" + str(tVCoord))
	print("bVCoord:" + str(bVCoord))
	print("lHCoord:" + str(lHCoord))
	print("rHCoord:" + str(rHCoord))
	return

def begin():
	params = Params()
	processargs(params)
	_printparameters(params)

	dirList = listdir(params.inputDir)
	jpgList = []
	for item in dirList:
		if (".jpg" in item):
			jpgList.append(item)

	if (len(jpgList) == 0):
		print("No JPGs were found in input directory. Aborting.")
		sys.exit(2)
	jpgList.sort()

	#get a list of all .jpg files (pumped out by IPEVO software)
	#The directory has JPGS, lets move on.
	for imgName in jpgList:
		inPath = params.inputDir + "/" + imgName
		cropimagealg(inPath,params)
	return

#Our "Main" or start point.
if __name__ == "__main__":
	begin()




'''
#References:
#[1]: GetOpt for Python3: https://docs.python.org/3.1/library/getopt.html
[2]: global usage is frowned upon, but passing upto 8 variables via a function call is also ugly.
[3]: An older algorithm following horizontal and vertical lines along hte image to probe for the edge of the paper
it was found that the SNR due to reflectivity off the background surface was causing issues. By summing 1D histograms,
our SNR gets pushed up, the the boundaries become much more defined. There is a a larger computational penalty,
as our time is now O(mn), where m and n are the dimensions of the image (which is very large ). I tried skipping every
pth point in order to get O(mn/p) time. If an image takes 10 seconds, thats not too bad.
[4]: CopyTree: http://pythoncentral.io/how-to-recursively-copy-a-directory-folder-in-python/
This code was just ripped directly from the page.
[5]: https://docs.python.org/2/library/shutil.html

'''
