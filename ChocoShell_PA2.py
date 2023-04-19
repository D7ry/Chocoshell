# lazy script for chocopy testing
import platform
import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CHOCOLATE = '\033[38;5;214m'

def colorStr(color, msg):
	return color + msg + bcolors.ENDC

LINE = "=================================================================================="
COLON = ":" if platform.system() != "Windows" else ";"


def print2(*msg):
	print(bcolors.CHOCOLATE + "[ChocoShell]" + bcolors.ENDC + " ".join(msg))


HELP = \
[
["Compile", " recompile the project"],
["testall", " test the student parser against all sample inputs and expected outputs."],
["test", " test the student parser against one sample input and expected output."],
["ana", " parse a .py file using student parser impl"],
["debug", " parse a .py file using student parser impl in debug mode on port 5005"],
["anaref", " parse a .py file using reference parser impl"],
["Verbose", " turn on/off verbose mode"],
["cd", " reset the current working directory to src/test/data/pa1/"],
["cd DIR", " set the current working directory to DIR"],
["exit", " quit the shell"]
]

HELP_STR = bcolors.OKBLUE + "Available commands:\n" + bcolors.ENDC \
	+ "\n".join(colorStr(bcolors.OKCYAN, i[0]) + " - " + i[1] for i in HELP) \

TEST_STR = "java -cp \"chocopy-ref.jar{}target/assignment.jar\" chocopy.ChocoPy --pass=.s".format(COLON)
ANA_STR = "java -cp \"chocopy-ref.jar{}target/assignment.jar\" chocopy.ChocoPy --pass=rs".format(COLON)
DEBUG_STR = "java -agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5005 -cp \"chocopy-ref.jar{}target/assignment.jar\" chocopy.ChocoPy --pass=rs".format(COLON)
ANA_REF_STR = "java -cp \"chocopy-ref.jar{}target/assignment.jar\" chocopy.ChocoPy --pass=rr".format(COLON)

PA2_OUT_FILE = "out.py.ast.typed"
PA1_ROOT = "src/test/data/pa1"
PA2_ROOT = "src/test/data/pa2"
BANNER = \
"\
   ___ _                ___ _        _ _ \n\
  / __| |_  ___  __ ___/ __| |_  ___| | |\n\
 | (__| ' \/ _ \/ _/ _ \__ \ ' \/ -_) | |\n\
  \___|_||_\___/\__\___/___/_||_\___|_|_|\n\
"

                                                        
lastCMD = ""
def runCmd(cmd):
	if cmd == "":
		return
	print2(bcolors.OKCYAN + cmd + bcolors.ENDC)
	global lastCMD
	lastCMD = cmd
	os.system(cmd)

def cmd(args : list[str]):
	runCmd(" ".join(args))

def chocoPyFile(name: str):
	if name.endswith(".py"):
		return name
	return name + ".py"

def chocoPyAst(name: str):
	if name.endswith(".py.ast"):
		return name
	return name + ".py.ast"
 
def main():
	print(colorStr(bcolors.CHOCOLATE, BANNER))
	bDebug = False
	def debugStr():
		return "--debug" if bDebug else ""
		
	cwd = ""

	while 1:
		print2("Enter command (? for help):")
		i = input().lower()
		if i == "":
			runCmd(lastCMD)
			continue
		t = i.split()
		if t[0] == "h" or t[0] == "help" or t[0] == "?":
			print(HELP_STR)
		elif t[0] == "ls":
			print(colorStr(bcolors.OKBLUE, "CWD: ") + colorStr(bcolors.HEADER, cwd if cwd != "" else "root"))
			for dir in os.listdir(PA2_ROOT + "/" + cwd):
				print(dir)
		elif t[0] == "testall":
			cmd([TEST_STR, "--dir", "src/test/data/pa2/sample", "--test"])
		elif t[0] == "test" or t[0] == "t":
			if len(t) == 1:
				print2("Please specify a test case.")
				continue
			cmd([TEST_STR, "src/test/data/pa2/{}/{}".format(cwd, chocoPyAst(t[1])), "--test"])
		elif t[0] == "ana" or t[0] == "a":
			cmd([ANA_STR, "--out", PA2_OUT_FILE, debugStr(), PA2_ROOT + "/{cwd}/{file_name}".format(file_name=chocoPyFile(t[1]), cwd = cwd)])
		elif t[0] == "debug" or t[0] == "d":
			cmd([DEBUG_STR, debugStr(), PA2_ROOT + "/{cwd}/{file_name}".format(file_name=chocoPyFile(t[1]), cwd = cwd)])
		elif t[0] == "anaref" or t[0] == "ar":
			cmd([ANA_REF_STR, debugStr(), PA2_ROOT + "/{cwd}/{file_name}".format(file_name=chocoPyFile(t[1]), cwd = cwd)])
		elif t[0] == "c" or t[0] == "compile":
			cmd(["mvn clean package"])
		elif t[0] == "verbose" or t[0] == "v":
			if len(t) == 1:
				print2("verbose mode is currently " + ("on" if bDebug else "off"))
				continue
			if t[1] == "1" or t[1] == "on":
				bDebug = True
				print2("verbose mode turned on.")
			elif t[1] == "0" or t[1] == "off":
				bDebug = False
				print2("verbose mode turned off.")
			else:
				print2("Invalid verbose option. Use 0 or 1.")
		elif t[0] == "cd":
			if len(t) == 1:
				print2("Reset current working directory to " + PA1_ROOT)
				cwd = ""
				continue
			if not os.path.isdir(PA2_ROOT + "/" + t[1]):
				print2("Invalid directory")
				continue
			cwd = t[1]
			print2("Current working directory set to {}/{}".format(PA1_ROOT, cwd))
		elif t[0] == "exit" or t[0] == "quit" or t[0] == "q":
			break
main()