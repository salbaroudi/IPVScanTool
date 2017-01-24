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
ipvscantools version XX.Y. Created by Sean al-Baroudi (sean.al.baroudi@gmail.com)
'''

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvdin:")
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)
		
	
	if (len(args) != 2):
		print("Two folder destinations (input and output) need to be given. Check argument string.")

	for o, a in opts:
		if o == "-h":
			print(helpString)
		if o == "-v":
			print(versionString)

if __name__ == "__main__":
	main()





#References:
#[1]: GetOpt for Python3: https://docs.python.org/3.1/library/getopt.html
