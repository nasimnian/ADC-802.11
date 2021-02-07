dict_of_binary_letter=dict()
binary_file=[]
list_of_letter=[]

def text_to_binary(url):
    global binary_file , dict_of_binary_letter
    f=open(url,"r")
    read_file=f.read()
    for i in read_file:
        binary_file.append(format(ord(i),'b'))
        dict_of_binary_letter[format(ord(i),'b')]=i
    return (binary_file , dict_of_binary_letter)

def convert_binary_to_text(binary_file,dict_of_binary_letter):
    global list_of_letter
    for i in binary_file:
        list_of_letter.append(dict_of_binary_letter[i])
    text=''.join(list_of_letter)
    return text
        
    
