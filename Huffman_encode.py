import sys
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
	read_file=open(name, "r")
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
	to_encode=open(name, "r")
	encoded=open(name[:-4]+"_encoded.txt", 'wb')
	encoded.write(" ".encode("ascii"))
	for i in range (128):
		if (freq[i]!=0):
			encoded.write(('\x01'+chr(i)+str(freq[i])).encode("ascii"))
			# print((chr('\x01')+chr(i)+str(freq[i])).encode("utf-8"))
	encoded.write("\x02".encode("ascii"))
	





#вызовы 
freq=count_freq("C:/Users/User/Desktop/read.txt")
tree=make_tree(freq)

codes=tree.preorder()

encode("C:/Users/User/Desktop/read.txt", freq, codes)

