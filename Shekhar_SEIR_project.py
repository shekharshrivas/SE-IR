import os
import math
import sys

# folderPath = "C:/Users/ASUS/Desktop/SEIR_Project/25"

folderPath = sys.argv[1]

def Building_docNo_Dic(folderPath):
	docNo_dic = {}
	doc_id = 1
	for filename in os.listdir(folderPath):
		file_path = os.path.join(folderPath, filename)
		if os.path.isfile(file_path):
			with open(file_path, "r") as file:
				text = file.read()
				docNo_dic[text[text.find("<DOCNO>")+7: text.find("</DOCNO>")]] = doc_id
				doc_id += 1
	return docNo_dic





def doc_term_list(text):
	lst = []
	for word in text.split():
		if word.isalnum():
			lst.append(word)
		else:
			newword = ""
			for char in word:
				if char.isalnum() or char == "_":
					newword += char
				else:
					if newword != "":
						lst.append(newword)
					newword = ""
			if newword != "":
				lst.append(newword)
	return lst


def IndexTerm_Dic_and_doctermList(folderPath):
	index_dic = {}
	doc_dic_term_list = {}
	token_id = 1
	for filename in os.listdir(folderPath):
		file_path = os.path.join(folderPath, filename)
		if os.path.isfile(file_path):
			with open(file_path, "r") as file:
				text = file.read()
				title = text[text.find("<TITLE>")+7: text.find("</TITLE>")].lower()
				titleNtext = title.strip()+" "+text[text.find("<TEXT>")+6: text.find("</TEXT>")].strip().lower()
				docTermsLst = doc_term_list(titleNtext)
				for term in docTermsLst:
					if term not in index_dic:
						index_dic[term] = token_id
						token_id += 1
				docName = text[text.find("<DOCNO>")+7: text.find("</DOCNO>")]
				doc_dic_term_list[docName] = docTermsLst

	return index_dic, doc_dic_term_list

holder = IndexTerm_Dic_and_doctermList(folderPath)



def IDF_of_token(holderTuple):
	idf_dic ={}
	for term in holderTuple[0]:
		dft = 0
		for docName in holderTuple[1]:
			if holderTuple[1][docName].count(term) != 0:
				dft += 1
		idf_dic[term] = math.log(132/dft)	
	return idf_dic

idf_dic = IDF_of_token(holder)



def Building_TfXIdfV(idf_dic, holderTuple):
	tf_Idf_dic = {}
	for docName in holderTuple[1]:
		acc_dic = {}
		for docTerm in holderTuple[1][docName]:
			tf = holderTuple[1][docName].count(docTerm)
			acc_dic[docTerm] = tf * idf_dic[docTerm]
		norm = math.sqrt(sum(acc_dic[v]**2 for v in acc_dic))
		for terms in acc_dic:
			acc_dic[terms] = acc_dic[terms]/norm
		tf_Idf_dic[docName] = acc_dic
	return tf_Idf_dic



tf_Idf_dic = Building_TfXIdfV(idf_dic, holder)


def pairwise_similarity_dic(tf_Idf_dic):
	pairwise_simi_dic = {}
	for docName in tf_Idf_dic:
		acc_lst = []
		for docName2 in tf_Idf_dic:
			if docName == docName2:
			    continue
			if docName2 in pairwise_simi_dic:
				continue
			simi_sum = 0
			for docTerm in tf_Idf_dic[docName]:
				if docTerm in tf_Idf_dic[docName2]:
					simi_sum += tf_Idf_dic[docName][docTerm] * tf_Idf_dic[docName2][docTerm]
			acc_lst.append((docName2, simi_sum*100))
		pairwise_simi_dic[docName] = sorted(acc_lst, key=lambda x: x[1], reverse=True)
	return pairwise_simi_dic

y = pairwise_similarity_dic(tf_Idf_dic)


result_lst = []
for docName in y:
	for simiTuple in y[docName]:
		result_lst.append((docName, simiTuple[0], simiTuple[1]))

result_lst = sorted(result_lst, key=lambda x: x[-1], reverse=True)



for i in range(50):
	print(result_lst[i][0], " --- ", result_lst[i][1], " --- ",result_lst[i][2],"%")
