import fs

print "\nTESTING GETCWD() \n"

try:
	fs.getcwd()
except:
	print "ERROR: fs.getcwd()"

print "DONE"

print "\nTESTING MKDIR() \n"

try:
	fs.mkdir('a') 
except:
	print "ERROR : fs.mkdir('a')"

try:
	fs.mkdir('a/ab') 
except:
	print "ERROR : fs.mkdir('a/ab')"

try:
	fs.mkdir('a/ab/../ac') 
except:
	print "ERROR : fs.mkdir('a/ab/ab/ac')"

try:
	fs.mkdir('a/../../f') 
except:
	print "ERROR : fs.mkdir('a/../../f')"

try:
	fs.mkdir('a/../../..') 
except:
	print "ERROR : fs.mkdir('a/../../..')"

try:
	fs.mkdir('a/./././././././..')
except:
	print "ERROR : fs.mkdir('a/./././././././..')"

try:
	fs.mkdir('a/ab/abc')
except:
	print "ERROR : fs.mkdir('a/ab/abc')"

print "\nNOW IN DIRECTORY 'a'\n"

fs.chdir('a')

try:
	fs.mkdir('a/ab/abc')
except:
	print "ERROR : fs.mkdir('a/ab/abc')"

try:
	fs.mkdir('/a/ab/abc')
except:
	print "ERROR : fs.mkdir('/a/ab/abc')"

fs.chdir('..')

print "\nDONE"

print "\nTESTING CHDIR() \n"

try:
	fs.chdir('a') 
except:
	print "ERROR : fs.chdir('a')"

try:
	fs.chdir('..') 
except:
	print "ERROR : fs.chdir('..') "

try:
	fs.chdir('a/../a/ab/') 
except:
	print "ERROR : fs.chdir('a/../a/ab/') "

try:
	fs.chdir('/') 
except:
	print "ERROR : fs.chdir('/')"

try:
	fs.chdir('/..') 
except:
	print "ERROR : fs.chdir('/..')"

try:
	fs.chdir('/a/ab/././../../a/ac')
except:
	print "ERROR : fs.chdir('/a/ab/././../../a/ac')"






