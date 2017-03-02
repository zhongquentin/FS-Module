import fs
fs.init('myfs')

# if __name__ == '__main__':
fs.init('myfs')
fs.getcwd() # /
fs.mkdir('a0')
fs.mkdir('a0/a1')
fs.mkdir('a0/a1/a2')
fs.listdir()
fs.listdir('a0')
fs.mkdir('a0/b1')
fs.listdir('a0')
fs.chdir('a0/b1') # /a0/b1
fs.create('../a1/a2.txt',10)
fs.listdir('../a1')
fs.chdir('/a0/a1') # /a0/a1
fs.getcwd()
try:
	fs.mkdir('../a1')
except Exception, e:
	print e
try:
	fs.chdir('../c1')
except Exception, e:
	print e
fs.getcwd()
try:
	fs.deldir('/a0/a1')
except Exception, e:
	print e
	try:
		fs.deldir('../a1')
	except Exception, e:
		print e
fs.chdir('..') # /a0
try:
	fs.deldir('a1')
except Exception, e:
	print e
try:
	fs.create('a1/a2.txt', 5)
except Exception, e:
	print e
try:
	fs.deldir('b1')
except Exception, e:
	print e
fs.listdir()
fs.listdir('a1')		
try:
	fs.deldir('c1')
except Exception, e:
	print e
						
fs.getcwd()
fd = fs.open('a1/a2.txt', 'r')
try:
	fd2 = fs.open('a1/b.txt', 'r')
except Exception, e:
	print e	
try:
	fs.write(fd,'hello\n')
except Exception, e:
	print e
try:
	fs.write(fd+1,'hello\n')
except Exception, e:
	print e
fd3 = fs.open('/a0/a1/a2.txt', 'w')
print fd == fd3
fs.write(fd,'hello\n')
print fs.read(fd,6)
fs.seek(fd,0)
print fs.read(fd,6)
try:
	fs.seek(fd,7)
except Exception, e:
	print e
	try:
		fs.seek(fd,11)
	except Exception, e:
		print e
fs.seek(fd,0)		
try: 
	fs.write(fd,'12345678900')
except Exception, e:
	print e
print fs.read(fd,6)
fs.seek(fd,0)
fs.write(fd,'1234567890')
fs.readlines(fd)
print fs.read(fd,2)

fs.getcwd()	
fs.mkdir('x')
fs.mkdir('x/y1')
fs.mkdir('x/y2')
fs.listdir('x')
fs.deldir('x/y1')
fs.listdir('x')
fs.deldir('x/y2')
fs.deldir('x')
try:
	fs.chdir('x')
except Exception, e:
	print e
print 'creating a b c'	
print fs.getcwd()
fs.create('a',1)
fs.create('b',1)
fs.create('c',1)
try:
	fs.create('d',8)
except Exception,e:
	print e
a = fs.open('a','wr')
b = fs.open('b','wr')
c = fs.open('c','wr')
fs.write(a,'a')
fs.write(b,'b')
fs.write(c,'c')
print fs.read(a,1)
print fs.read(b,1)
try:
	fs.read(c,2)
except Exception,e:
	print e	
fs.close(a)
fs.close(b)
fs.close(c)
fs.close(fd)

# print 'suspending'
fs.suspend()
fs.resume('myfs.fssave')
print fs.listdir()
print fs.getcwd()
a = fs.open('a0/a','wr')
b = fs.open('a0/b','wr')
print fs.read(a,1)
print fs.read(b,1)