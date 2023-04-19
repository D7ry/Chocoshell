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
["testall", " test the student parser against sample inputs and expected outputs."],
["Pars", " parse a .py file using student parser impl"],
["ParsRef", " parse a .py file using reference parser impl"],
["Lex", " see the sequence of tokens produced by a .py file using student lexer impl"],
["LexRef", " see the sequence of tokens produced by a .py file using reference lexer impl"],
["Verbose", " turn on/off verbose mode"],
["cd", " reset the current working directory to src/test/data/pa1/"],
["cd DIR", " set the current working directory to DIR"],
["exit", " quit the shell"]
]

HELP_STR = bcolors.OKBLUE + "Available commands:\n" + bcolors.ENDC \
	+ "\n".join(colorStr(bcolors.OKCYAN, i[0]) + " - " + i[1] for i in HELP) \

TEST_STR = "java -cp \"chocopy-ref.jar{}target/assignment.jar\" chocopy.ChocoPy --pass=s".format(COLON)
REF_TEST_STR = "java -cp \"chocopy-ref.jar{}target/assignment.jar\" chocopy.ChocoPy --pass=r".format(COLON)

PA1_ROOT = "src/test/data/pa1"

BANNER = \
"\
   ___ _                ___ _        _ _ \n\
  / __| |_  ___  __ ___/ __| |_  ___| | |\n\
 | (__| ' \/ _ \/ _/ _ \__ \ ' \/ -_) | |\n\
  \___|_||_\___/\__\___/___/_||_\___|_|_|\n\
"

                                                        

def runCmd(cmd):
	if cmd == "":
		return
	print2(bcolors.OKCYAN + cmd + bcolors.ENDC)
	os.system(cmd)

def cmd(args : list[str]):
	runCmd(" ".join(args))
 
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
			continue
		t = i.split()
		if t[0] == "h" or t[0] == "help" or t[0] == "?":
			print(HELP_STR)
		elif t[0] == "ls":
			print(colorStr(bcolors.OKBLUE, "CWD: ") + colorStr(bcolors.HEADER, cwd if cwd != "" else "root"))
			for dir in os.listdir(PA1_ROOT + "/" + cwd):
				print(dir)
		elif t[0] == "testall":
			cmd([TEST_STR, "--dir", "src/test/data/pa1/sample", "--test"])
		elif t[0] == "pars" or t[0] == "p":
			cmd([TEST_STR, debugStr(), PA1_ROOT + "/{cwd}/{file_name}".format(file_name=t[1], cwd = cwd)])
		elif t[0] == "parsref" or t[0] == "pr":
			cmd([REF_TEST_STR, debugStr(), PA1_ROOT + "/{cwd}/{file_name}".format(file_name=t[1], cwd = cwd)])
		elif t[0] == "lex" or t[0] == "l":
			cmd(["java", "-cp", "\"chocopy-ref.jar{}target/assignment.jar\"".format(COLON), "chocopy.pa1.ChocoPyLexer", PA1_ROOT + "/{cwd}/{file_name}".format(file_name=t[1], cwd = cwd)])
		elif t[0] == "lexref" or t[0] == "lr":
			cmd(["java", "-cp", "\"chocopy-ref.jar{}target/assignment.jar\"".format(COLON), "chocopy.reference.ChocoPyLexer", PA1_ROOT + "/{cwd}/{file_name}".format(file_name=t[1], cwd = cwd)])
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
			if not os.path.isdir(PA1_ROOT + "/" + t[1]):
				print2("Invalid directory")
				continue
			cwd = t[1]
			print2("Current working directory set to {}/{}".format(PA1_ROOT, cwd))
		elif t[0] == "exit" or t[0] == "quit" or t[0] == "q":
			break



main()