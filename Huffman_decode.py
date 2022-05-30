import sys
import os
import filecmp
class Tree:
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left  = left
        self.right = right
        if (left and right):
        	self.value=left.get_value()+right.get_value()

    def __str__(self):
        return str(self.value)+" "+str(self.key)

    def get_key(self):
    	return self.key

    def get_value(self):
    	return self.value

    def preorder(self):
    	dict_codes={}
    	self.preor(dict_codes)
    	return dict_codes

    def preor(self, dict_codes, code=''):
    	if (self.key!=''):
    		dict_codes[self.key]=code
    	else:	
	    	code+='0'
	    	self.left.preor(dict_codes, code)
	    	code=code[:-1]
	    	code+='1'
	    	self.right.preor(dict_codes, code)

def sort(l):
    for i in range(1, len(l)):
        for j in range(len(l)-i):
            if (l[j].get_value()>l[j+1].get_value()):
                l[j], l[j+1]=l[j+1], l[j]

def make_tree(freq):
    list_tree=[]
    for i in range(128):
        if freq[i]!=0:
            list_tree.append(Tree(chr(i), freq[i]))

    while(len(list_tree)!=1):
        sort(list_tree)
        list_tree[0]=Tree("", 0, list_tree[0], list_tree[1])
        list_tree.pop(1)

    return list_tree[0]

def decode(name_code):
    try:
        decoded=open(name_code[:-13]+"(decoded).txt", "w")
        code=open(name_code, "rb")
    except:
        print("Указанный файл не может быть открыт")
        exit()
    last_bits=int(code.read(1))
    freq=[0 for i in range(256)]
    sym=code.read(1)
    sym=int.from_bytes(sym, "big")
    while sym!=2:
        sym=code.read(1)
        sym=int.from_bytes(sym, "big")
        char=sym
        num=0
        sym=code.read(1)
        sym=int.from_bytes(sym, "big")
        while sym!=1 and sym!=2:
            num*=10
            num+=sym-48
            sym=code.read(1)
            sym=int.from_bytes(sym, "big")
        freq[char]=num

    tree=make_tree(freq)

    mask=1<<7
    sym=code.read(1)
    sym=int.from_bytes(sym, "big")
    next_s=code.read(1)
    curr=tree
    end=False
    if next_s==b'':
        end=True
    count=0
    while True:
        if curr.key!='':
            decoded.write(curr.key)
            count+=1
            curr=tree
        if (mask&sym)!=0:
            curr=curr.right
        else:
            curr=curr.left
        mask=mask>>1
        if end and mask==2**(last_bits-1):
            decoded.write(curr.key)
            break
        if mask==0:
            mask=1<<7
            sym=next_s
            sym=int.from_bytes(sym, "big")
            next_s=code.read(1)
            if next_s==b'':
                end=True
    code.close()
    decoded.close()

def cmp(name, orig):
    if filecmp.cmp(name, orig):
        print("Идентичны")
    else:
        print("Неидентичны")



name=input("Введите путь файла для декодировки: ")
os.chdir("c:")
p=os.path.abspath(name)
if p not in sys.path: 
    os.chdir("d:")
p=os.path.abspath(p)

decode(p)

name=input("Введите путь оригинального файла: ")
os.chdir("c:")
orig=os.path.abspath(name)
if p not in sys.path: 
    os.chdir("d:")
orig=os.path.abspath(orig)

cmp(p[:-13]+"(decoded).txt", orig)





