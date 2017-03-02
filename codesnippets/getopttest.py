import getopt
import sys


'''

Test code by Sean al-Baroudi (sean.al.baroudi@gmail.com)

The getOpt page has shown me a standard code style, so I will use it. All credit goes to the person who
wrote that page: [1]

'''

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
 
ipvscantools version XX.Y. Created by Sean al-Baroudi (sean.al.baroudi@gmail.com)
'''

deleteSwitch = False
invertSwitch = False
filePrefix = ""

inputDir = "./"
oputputDir = "./"


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvdin:")
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)
		
	if (len(args) != 2):
		print("Two folder destinations (input and output) need to be given. Check argument string.")
		sys.exit(2)

	inputDir = args[0]
	outputDir = args[1]

	for o, a in opts:
		if o == "-h":
			print(helpString)
		elif o == "-v":
			print(versionString)
		elif o == "-i":
			invertSwitch = True
			print("InvertSwitch Triggered")
		elif o == "-d":
			deleteSwitch = True
			print("DeleteSwitch Triggered")
		elif (o == "-n" and  a != ""	): #!!!
			filePrefix = a
		else:
			print("An unrecognized option or format has appeared. Please check your argument string")
			sys.exit(2)

	print("first arg was:" + inputDir)
	print("second arg was" + outputDir)
	print("file prefix is", filePrefix)

if __name__ == "__main__":
	main()


#References:
#[1]: GetOpt for Python3: https://docs.python.org/3.1/library/getopt.html
