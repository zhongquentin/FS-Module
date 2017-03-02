import fs

def main():
    fs.init('fs')
    fs.mkdir('a')
    fs.mkdir('b')
    fs.mkdir('a/c')
    fs.create('a/d.txt',20)
    fs.create('a/c/e.txt',20)
    fd1 = fs.open('a/d.txt','rw')
    fd2 = fs.open('a/c/e.txt','rw')
    fs.write(fd1,'hello\nbye\n')
    fs.write(fd2,'goodbye\n')
    print fs.read(fd2,4)
    print fs.readlines(fd1)
    for f in fs.readlines(fd1):
        print(f),
    fs.close(fd1)
    fs.close(fd2)
    fs.suspend()

main()
