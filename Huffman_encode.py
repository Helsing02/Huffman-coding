import sys
import os
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

def count_freq(name):
	freq=[0 for i in range(128)]
	try:
		read_file=open(name, "r")
	except:
		print("Указанный файл не может быть открыт")
		exit()
	sym=read_file.read(1)
	while(sym!=''):
		try:
			freq[ord(sym)]+=1
		except:
			print('Символ "'+sym+'" не из семибитной кодировки ASCII')
			sys.exit()
		sym=read_file.read(1)
	read_file.close()
	return freq

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

def encode(name, freq, codes):
	try:
		to_encode=open(name, "r")
		encoded=open(name[:-4]+"(encoded).txt", 'wb')
	except:
		print("Указанный файл не может быть открыт")
		exit()
	encoded.write(" ".encode("ascii"))
	for i in range (128):
		if (freq[i]!=0):
			encoded.write(('\x01'+chr(i)+str(freq[i])).encode("ascii"))
	encoded.write("\x02".encode("ascii"))
	sym=to_encode.read(1)
	i=0
	j=0
	count=0
	char=0
	while True:
		char=char<<1
		if (codes[sym])[j]=='1':
			char=char|1
		i+=1
		j+=1
		if (i==8):
			i=0
			encoded.write(bytes([char]))
			char=0
		if j==len(codes[sym]):
			j=0
			count+=1
			sym=to_encode.read(1)
			
		if sym=='':
			break
	if i>0:
		char=char<<8-i
		encoded.write(bytes([char]))
	encoded.seek(0)
	encoded.write(str(8-i).encode("ascii"))
	encoded.close()
	to_encode.close()


#вызовы 
name=input("Введите путь файла для кодировки: ")
os.chdir("c:")
p=os.path.abspath(name)
if p not in sys.path: 
	os.chdir("d:")
	p=os.path.abspath(p)

freq=count_freq(p)
tree=make_tree(freq)

codes=tree.preorder()

encode(p, freq, codes)

