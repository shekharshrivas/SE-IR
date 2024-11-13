import requests
import sys

def getUrlContent(url):
    body = []
    for url in url:
        page = requests.get(url)
        pageLine = page.text.splitlines()
        links = []
        bodyArray = []
        bodycheck = False
        scriptlist = [False]
        inside_tag = False
        inside_script_tag = False

        for line in pageLine:
            line = line.strip().lower()
            if line.find("<body") != -1:
                bodycheck = True
            
            if bodycheck:
                text = ""
                for char in line:
                    if char == '<':
                        inside_tag = True
                        if text.endswith('<script'):
                            inside_script_tag = True
                    elif char == '>':
                        inside_tag = False
                        if text.endswith('</script'):
                            inside_script_tag = False
                    elif not inside_tag and not inside_script_tag:
                        text += char
                bodyArray.append(text.replace('^ "',""))
        body.append(bodyArray)
    wordArray = []
    for allLines in body:
        wordlst = []
        for subline in allLines:
            if subline == "" or subline == "\n" or subline.find("{")!= -1 or subline.count(";") >= 2 or subline.find("العربي") !=-1 or subline.find("한국어Հայերենहिन्द") != -1 or subline.find("https:")!=-1 or subline.find("MediaWiki") !=-1 or subline.find(")") != -1 or subline.find("}") != -1:
                continue
            word = ""
            for chare in subline:
                if chare == "^" or chare =='"':
                    word+=""
                else:
                    word+=chare
            
            wordlst.append(word)
        wordArray.append(wordlst)
    return wordArray


urls = sys.argv[1:]
# print(getUrlContent(urls))



def poly_hash(word):
    p = 53
    m = (1 << 64) - 1
    hash_value = 0
    
    for i in range(len(word)):
        hash_value += ord(word[i])*(p**i)
    hash_value = hash_value % 2**64
    binary_hash = bin(hash_value)[2:].zfill(64)
    return binary_hash

#########################################################
def Dic_Of_grams():
    linesOfBodys = getUrlContent(urls)
    web1_words = [word for line in linesOfBodys[0] for word in line.split()]
    web2_words = [word for line in linesOfBodys[1] for word in line.split()]
    
    web1_5Gram = []
    for i in range(0, len(web1_words) - 4, 3):
        web1_5Gram.append(" ".join(web1_words[i:i+5]))
    
    web2_5Gram = []
    for i in range(0, len(web2_words) - 4, 3):
        web2_5Gram.append(" ".join(web2_words[i:i+5]))

    web1_weight_dic = {}
    for gram in web1_5Gram:
        if gram in web1_weight_dic:
            web1_weight_dic[gram] += 1
        else:
            web1_weight_dic[gram] = 1

    web2_weight_dic = {}
    for gram in web2_5Gram:
        if gram in web2_weight_dic:
            web2_weight_dic[gram] += 1
        else:
            web2_weight_dic[gram] = 1

    return web1_weight_dic, web2_weight_dic

#########################################################
def Hashing_of_grams():
    dic_tuple = Dic_Of_grams()
    hashing_of_web1 = {}
    for i in dic_tuple[0]:
        hash_value = poly_hash(i)
        hashing_of_web1[hash_value] = dic_tuple[0][i]
    
    hashing_of_web2 = {}
    for j in dic_tuple[1]:
        hash_value = poly_hash(j)
        hashing_of_web2[hash_value] = dic_tuple[1][j]
    
    return hashing_of_web1, hashing_of_web2
#########################################################

def FingerPrint_of_webs():
    hash_web_tuple = Hashing_of_grams()
    fig_Array = []
    for hash_dic in hash_web_tuple:
        str_fig = ""
        for i in range(64):
            up = 0
            down = 0
            for keys in hash_dic:
                if str(keys)[i] == "0":
                    down -= hash_dic[keys]
                else:
                    up += hash_dic[keys]
            str_fig += "0" if up+down < 0 else "1"
        fig_Array.append(str_fig)
    print("SimHash of url_1:- ", fig_Array[0])
    print("SimHash of url_2:- ", fig_Array[1])
    count = 0
    for m in range(64):
        if fig_Array[0][m] == fig_Array[1][m]:
            count+=1
    print("Total no of common bit is:- ",count)

FingerPrint_of_webs()
#########################################################
