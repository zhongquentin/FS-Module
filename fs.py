import pickle
from __builtin__ import open as open_
import os

class fs:
	# root directory
	root = {'path': '/', 'abspath': '/', 'subdirs': [], 'isdir': True, 'fsname': ''}
	root['subdirs'].append(root)
	cwd = root
	file_descriptor = 0
	opened_files = []
	fs_content = []	
	
	def __init__(self):
		fs.file_descriptor = 0

	@staticmethod
	def init(fsname):
		fs.root['fsname'] = fsname
		size = os.path.getsize(fsname)
		fs.root['allocation'] = [0]*size # initially free space = fsname's size
		fs.fs_content = ['\x00']*size # initially no content
        # print fs.root['fsname'], len(fs.root['allocation'])

	@staticmethod
	def mkdir(name):
		old = fs.cwd
		dirname = dirHelper(name,old)
		for d in fs.cwd['subdirs'][1:]:
			if dirname == d['path'] and d['isdir']:
				fs.cwd = old
				raise ValueError('directory %s already exists' %dirname)
		newdir = {'path': dirname, 'abspath': fs.cwd['abspath']+dirname+'/', 'subdirs': [], 'isdir': True}
		# appending .. dir to new dir
		newdir['subdirs'].append(fs.cwd)
		# appending new dir to current dir
		fs.cwd['subdirs'].append(newdir)
		fs.cwd = old

	@staticmethod
	def deldir(name):
		old = fs.cwd
		garbage = dirHelper(name,old,True)
		subdirs = fs.cwd['subdirs']
		gsd = None
		p = 0
		for i,sd in enumerate(subdirs):
			if garbage == sd['path'] and sd['isdir']:
				gsd = sd
				p = i
				break

		if gsd == None: # directory name not found
			fs.cwd = old
			raise ValueError('directory %s does not exist' %name)

		if old['abspath'] == gsd['abspath']: # cannot delete self
			fs.cwd = old
			raise ValueError('currently inside specified directory')
			
		if len(gsd['subdirs']) > 1: # if directory not empty
			fs.cwd = old
			raise ValueError('directory is not empty')
		
		del fs.cwd['subdirs'][p]
		fs.cwd = old
		return None		

	@staticmethod
	def delfile(name):
		old = fs.cwd
		garbage = dirHelper(name,old,True)
		subdirs = fs.cwd['subdirs']
		gsd = None
		p = 0

		for i,sd in enumerate(subdirs):
			if garbage == sd['path'] and not sd['isdir']:
				gsd = sd
				p = i
				break

		if gsd == None:
			fs.cwd = old
			raise ValueError('File %s does not exist' % name)

		if gsd['open'] is True:
			fs.cwd = old
			raise ValueError('File %s is current open' % name)
		
		for i in gsd['content']:
			fs.root['allocation'][i] = 0

		del fs.cwd['subdirs'][p]
		fs.cwd = old
		return None

	@staticmethod
	def chdir(name):
		old = fs.cwd 
		dirHelper(name,old,False)	

	@staticmethod
	def getcwd():
		if fs.cwd['path'] == '/':
			return '/'
		else:	 
			return fs.cwd['abspath'][:-1]

	@staticmethod
	def listdir(dirname = None):
		old = fs.cwd
		if dirname != None and dirname != '.':
			dirHelper(dirname,old,False)
		ret = [d['path'] for d in fs.cwd['subdirs'][1:]]
		fs.cwd = old
		return ' '.join(ret)
	
	@staticmethod
	def isdir(filename):
		old = fs.cwd
		try:
			dirname = dirHelper(filename,old,False)
			fs.cwd = old
			return True
		except:
			fs.cwd = old
			return False

	@staticmethod
	def create(filename,nbytes):
		old = fs.cwd
		dirname = dirHelper(filename,old)
		for d in fs.cwd['subdirs'][1:]:
			if dirname == d['path'] and not d['isdir']:
				fs.cwd = old
				raise ValueError('create error: file %s already exists' %dirname)		
		content = allocate(nbytes)		
		newfile = {'path': dirname, 'abspath': fs.cwd['abspath']+dirname+'/','isdir': False, 
		'content': content, 'length': 0, 'open': False, 'mode': '', 'pos': 0, 'fd': -1}
		fs.cwd['subdirs'].append(newfile)
		fs.cwd = old

	@staticmethod
	def open(filename,mode):
		old = fs.cwd
		fname = dirHelper(filename,old)
		for d in fs.cwd['subdirs'][1:]:
			if fname == d['path'] and d['isdir'] == False: 
				if mode not in d['mode']: # if not yet opened in this mode
					d['mode'] += mode
				if d['open']: # if already opened
					fs.cwd = old
					return d['fd']
				d['open'] = True
                                d['pos'] = 0
				fs.file_descriptor += 1
				d['fd'] = fs.file_descriptor
				fs.opened_files.append(d) # add to opened files list
				fs.cwd = old
				return fs.file_descriptor
		fs.cwd = old
		raise ValueError('open error: no such file %s' %fname)		

	@staticmethod
	def close(fd):
		old = fs.cwd
		for d in fs.opened_files:
			if d['fd'] == fd:
				name = dirHelper(d['abspath'],old)
				for f in fs.cwd['subdirs'][1:]:
					if f['path'] == name:
						f['open'] = False
						f['pos'] = 0
						f['fd'] = -1
						fs.opened_files.remove(d)
						fs.cwd = old
						return None
		fs.cwd = old
		raise ValueError('invalid fd')

	@staticmethod
	def length(fd):
		for f in fs.opened_files:
			if fd == f['fd']:
				return f['length']
		raise ValueError('fd is not valid')
	
	@staticmethod
	def pos(fd):
		for f in fs.opened_files:
			if fd == f['fd']:
				return f['pos']
		raise ValueError('fd is not valid')
		
	@staticmethod
	def seek(fd,pos):
		if pos < 0:
			raise ValueError('seek error: pos cannot be negative')
		for f in fs.opened_files:
			if fd == f['fd']:
				if pos > len(f['content']):
					raise ValueError('seek error: pos is greater than file size')
				if pos > f['length']:
					raise ValueError('seek error: pos is greater than file length')
				f['pos'] = pos
				return None					
		raise ValueError('seek error: fd is not valid')		

	@staticmethod
	def write(fd,writebuf):
		for f in fs.opened_files:
			if f['fd'] == fd: # found opened file
				if 'w' not in f['mode']: # not write mode
					raise ValueError('write error: file is not opened for write')
				if len(writebuf) > len(f['content']): # buffer too big
					raise ValueError('write error: write buffer is bigger than file size') 
				tmp = []
				tmp.extend(writebuf)
				for b in f['content']: # clear file content
					fs.fs_content[b] = '\x00'
				for i,b in enumerate(tmp): # write by byte(character)
					fs.fs_content[f['content'][i]] = b
				f['length'] = len(tmp)	
				return None
		raise ValueError('write error: fd is not valid')		

	@staticmethod
	def read(fd,nbytes):
		for f in fs.opened_files:
			if f['fd'] == fd: # found opened file
				if  'r' not in f['mode']: # not read mode
					raise ValueError('read error: file is not opened for read')
				if nbytes > f['length'] - f['pos']: # reading beyond file length
					raise ValueError('read error: cannot read beyond file length')
				s = []
				for i in f['content'][f['pos']:f['pos']+nbytes]:
					s.append(str(fs.fs_content[i]))	
				f['pos'] += nbytes
				return ''.join(s)
		raise ValueError('read error: fd is not valid')		

	@staticmethod
	def readlines(fd):
		for f in fs.opened_files:
			if f['fd'] == fd: # found opened file
				if  'r' not in f['mode']: # not read mode
					raise ValueError('readlings error: file is not opened for read')
				s = []
				for i in f['content'][:f['length']]:
					s.append(str(fs.fs_content[i]))
				return ''.join(s)
		raise ValueError('readlines error: fd is not valid')		

	@staticmethod
	def dirHelper(path,old,strip = True): # strip is true for all functions but listdir and chdir
		#change cwd by following the path tokens
		dirname = None

		tokens = path.split('/')
		tokens = [t for t in tokens if t != '.'] # ignore '.'
		if len(tokens) == 0:
			return
		if tokens[-1] == '': # if path ends with '/' ignore it
			tokens = tokens[:-1]
			
		if len(tokens) == 1 and strip: # if token length is 1 and not listdir or chdir, do nothing
			if tokens[0] == '.':
				return fs.cwd['path']
			return path 
		elif strip: # if not listdir and chdir and len > 1, store last token separately 
			dirname = tokens[-1]
			tokens = tokens[:-1]
		
		if len(tokens) == 0:
			return
		if tokens[0] == '': # if path starts with '/' go to root
			fs.cwd = fs.root
			tokens = tokens[1:]		

		for t in tokens:
			flag = False

			if t == '..':
				if fs.cwd == fs.root:
					fs.cwd = old
					raise ValueError('invalid path %s' %path)

				fs.cwd = fs.cwd['subdirs'][0]
				continue
			
			for d in fs.cwd['subdirs'][1:]:
				if d['path'] == t and d['isdir']:
					fs.cwd = d
					flag = True
					break
			
			if flag == False:
				fs.cwd = old
				raise ValueError('invalid path %s' %path)
		
		return dirname

	@staticmethod
	def allocate(n):
		free = [] #list of free indices
		for i,e in enumerate(fs.root['allocation']):
			if e == 0:
				free.append(i)
			if len(free) == n:
				break	

		if len(free) < n:
			raise ValueError('create eror: not enough space in %s' %fs.root['fsname'])

		content = [] #list of indices of length n

		for i,e in enumerate(free):
			fs.root['allocation'][e] = 1 # index e no longer free
			content.append(e) # append index for file to write to

		return content				

	@staticmethod
	def suspend():
		# print 'suspending'
		if len(fs.opened_files) > 0:
			raise ValueError('suspend error: there are still opened files')    
		f = open_(fs.root['fsname'], 'w')
		for b in fs.fs_content:
			f.write(str(b))
		f.close()		        

		with open_(fs.root['fsname']+'.fssave','wb') as handle:
			pickle.dump(fs.root,handle,protocol=pickle.HIGHEST_PROTOCOL)

	@staticmethod
	def resume(fname):
		with open_(fname,'rb') as handle:
			fs.root = pickle.load(handle) # load in root
			fs.cwd = fs.root # set cwd to root
		f = open_(fs.root['fsname'],'r') # open content file
		fs.fs_content = []
		for l in f:
			fs.fs_content.extend(l) # read content into memory


init = fs.init
mkdir = fs.mkdir
chdir = fs.chdir
deldir = fs.deldir
delfile = fs.delfile
create = fs.create
open = fs.open
close = fs.close
length = fs.length
pos = fs.pos
seek = fs.seek
getcwd = fs.getcwd
listdir = fs.listdir
isdir = fs.isdir
write = fs.write
read = fs.read
readlines = fs.readlines
dirHelper = fs.dirHelper
allocate = fs.allocate
resume = fs.resume
suspend = fs.suspend
