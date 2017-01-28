import getopt
import sys

#The getOpt page has shown me a new code style, so I will use it. All credit goes to the person who
#wrote that page:

helpString = '''Usage of ipvscantool:

ipvscantools -h -v -d -i -n [filenaming] [folder to read] [folder to write to]

	-h: Help string for console.
	-v: Version information.
	-d: Delete temp files in folder, after you are done (stupidly hunts for all .jpg files, and kills them). 
	-n: Prefix for naming of files.
	-i: Invert image colors.

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

#Our getopt options.
deleteSwitch = False
invertSwitch = False
filePrefix = ""

inputDir = "~/"
outputDir = "~/"

#[1]
def processargs():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvdin:")
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)

	if (len(args) != 2):
		print("Two folder destinations (input and output) need to be given. Check argument string.")
		sys.exit(2)

	inputDir = inputDir + args[0]
	outputDir = outputDir +  args[1]

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
		else:
			print("An unrecognized option or format has appeared. Please check your argument string")
			sys.exit(2)


def main():
	processargs() #everything is global anyways.

	#We have our arguements, lets load our files.
	
	dirList = os.listdir(inputDir)
	jpgList = []
	for item in dirList:
		if (".jpg" in item):
			jpgList.append(item)
			
	if (length(jpgList) == 0):
		print("No JPGs in input directory. Aborting.")
		sys.exit(2)
	
	#presumably the directory has JPGS, lets move on.
	for imgName in jpgList:
		cropImage(inputDir + "/" + imgName)
		
		
		
		
	

	os.chdir(inputDir)
	#get a list of all .jpg files (pumped out by IPEVO software)
	

if __name__ == "__main__":
	main()


#References:
#[1]: GetOpt for Python3: https://docs.python.org/3.1/library/getopt.html
