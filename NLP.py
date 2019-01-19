'''
FRAMES
======

frame() to look up a frame by its exact name or ID
frames() to get frames matching a name pattern
frames_by_lemma() to get frames containing an LU matching a name pattern
frame_ids_and_names() to get a mapping from frame IDs to names

FRAME ELEMENTS
==============

fes() to get frame elements (a.k.a. roles) matching a name pattern, optionally constrained
  by a frame name pattern

LEXICAL UNITS
=============

lu() to look up an LU by its ID
lus() to get lexical units matching a name pattern, optionally constrained by frame
lu_ids_and_names() to get a mapping from LU IDs to names

'''

from nltk.corpus import framenet as fn
import collections
import numpy as np
import math

import networkx as nx
import matplotlib.pyplot as plt

result1 = []
result2 = []
simres1 = []
simres2 = []

def getFrame_by_Name(frame_name):
	f = fn.frame_by_name(frame_name)
	pass


def getFE(frame_name):
	f = fn.frame_by_name(frame_name)
	FE = f.FE
	pass


def fekeys(frame_name):
	f = fn.frame_by_name(frame_name)
	FE = f.FE
	keys = FE.keys()
	pass


def items():
	f = fn.frame_by_name(frame_name)
	FE = f.FE
	items = FE.items()
	pass


def fe_coreTypes(frame_name):
    f = fn.frame_by_name(frame_name)
    fedict = {}
    for feName, fe in f.FE.items():
        fedict[feName] = fe.coreType
        print(feName)
        print(fe)
        return fedict

def exemplars1(frame_name, feR=False):
	expls = []
	for i in lu_ids(frame_name):
		e = fn.lu(i).exemplars
		for j in range(len(e)):
			#print('+++++++', e[j].FE)
			expls.append(e[j])
			pass
		pass


	annotation1(expls,frame_name)
	return simres1
	pass

def exemplars2(frame_name, feR=False):
	expls = []
	for i in lu_ids(frame_name):
		e = fn.lu(i).exemplars
		for j in range(len(e)):
			#print('+++++++', e[j].FE)
			expls.append(e[j])
			pass
		pass


	annotation2(expls,frame_name)
	return simres2
	pass

# get all lu id of a frame
def lu_ids(frame_name):
    f = fn.frame_by_name(frame_name)
    ids = []
    for v in f.lexUnit.values():
        ids.append(v.ID)
    return ids


def annotation1(exemplars,frame_name):

	num = 0
	for sentence in exemplars:
		num = num+1
		_exemplar_of_POS1(sentence,False)
		pass

	#res = set()
	for feName1 in result1:
		count = 0
		for feName2 in result1:
			if feName1.__getitem__('FEName') == feName2.__getitem__('FEName') and feName1.__getitem__('POS') == feName2.__getitem__('POS'):
				count=count+1
				pass
			pass
		#res.add(str(feName1.__getitem__('FEName'))+" "+str(feName1.__getitem__('POS'))+" "+str(count))
		pair = {"FEName" : feName1.__getitem__('FEName'), "POS" : feName1.__getitem__('POS'), "Count" : count}
		if pair not in simres1:
			simres1.append(pair)
			pass

		pass

	'''
	file = open('report.txt', 'a')
	file.write(str(frame_name) + " " + "Total sentences: "+str(num))
	file.write("\n")
	file.write(str(res))
	file.write("\n")
	file.write("\n")
	file.close()
	'''
	pass

def annotation2(exemplars,frame_name):

	num = 0
	for sentence in exemplars:
		num = num+1
		_exemplar_of_POS2(sentence,False)
		pass

	#res = set()
	for feName1 in result2:
		count = 0
		for feName2 in result2:
			if feName1.__getitem__('FEName') == feName2.__getitem__('FEName') and feName1.__getitem__('POS') == feName2.__getitem__('POS'):
				count=count+1
				pass
			pass
		#res.add(str(feName1.__getitem__('FEName'))+" "+str(feName1.__getitem__('POS'))+" "+str(count))
		pair = {"FEName" : feName1.__getitem__('FEName'),"POS" : feName1.__getitem__('POS'), "Count" : count}
		if pair not in simres2:
			simres2.append(pair)
			pass

		pass

	'''
	file = open('report.txt', 'a')
	file.write(str(frame_name) + " " + "Total sentences: "+str(num))
	file.write("\n")
	file.write(str(res))
	file.write("\n")
	file.write("\n")
	file.close()
	'''
	pass

'''
def aggregate_names(errors,pair):
 	pair = {"FEName" : feName1.__getitem__('FEName'), "POS" : feName1.__getitem__('POS'), "Count" : count}
    result = collections.defaultdict(lambda: collections.defaultdict(pair))
    for real_name, false_name, location in errors:
        result[real_name][false_name].append(location)
    return result
'''

def _exemplar_of_POS1(sentence, fe_only = True):
	#fe = sentence.FE[0]
	#print(list(zip(*sentence.FE[0]))[2] if sentence.FE[0] else set())  #  [(0, 68, 'Responsible_party'), (84, 89, 'Responsible_party'), (90, 95, 'Station')]
	#num = len(fe)
	#print(">>>>>>flagged: ", sentence.PT)  #sentence.POS
	overtNames = list(zip(*sentence.FE[0]))[2] if sentence.FE[0] else ""  # {'Station', 'Responsible_party'}
	Pos_Tag = list(zip(*sentence.PT))[2] if sentence.PT else ""  		  # {'NP', 'Poss'}
	Gram_Tag = list(zip(*sentence.GF))[2] if sentence.GF else "" 		  # {'Ext', 'Gen'}

	minlength = min(len(overtNames),len(Pos_Tag),len(Gram_Tag))
	for i in range(minlength):
		#print(i)  #overtNames[0] = Responsible_party, overtNames[1] = Responsible_party, overtNames[2] = station
		try:
			pair = {"FEName" : overtNames[i], "POS" : str(Pos_Tag[i])+"."+str(Gram_Tag[i])}
			result1.append(pair)
		except IndexError:
			pass
		pass

	pass

def _exemplar_of_POS2(sentence, fe_only = True):
	#fe = sentence.FE[0]
	#print(list(zip(*sentence.FE[0]))[2] if sentence.FE[0] else set())  #  [(0, 68, 'Responsible_party'), (84, 89, 'Responsible_party'), (90, 95, 'Station')]
	#num = len(fe)
	#print(">>>>>>flagged: ", sentence.PT)  #sentence.POS
	overtNames = list(zip(*sentence.FE[0]))[2] if sentence.FE[0] else ""  # {'Station', 'Responsible_party'}
	Pos_Tag = list(zip(*sentence.PT))[2] if sentence.PT else ""  		  # {'NP', 'Poss'}
	Gram_Tag = list(zip(*sentence.GF))[2] if sentence.GF else "" 		  # {'Ext', 'Gen'}

	minlength = min(len(overtNames),len(Pos_Tag),len(Gram_Tag))
	for i in range(minlength):
		#print(i)  #overtNames[0] = Responsible_party, overtNames[1] = Responsible_party, overtNames[2] = station
		try:
			pair = {"FEName" : overtNames[i], "POS" : str(Pos_Tag[i])+"."+str(Gram_Tag[i])}
			result2.append(pair)
		except IndexError:
			pass
		pass
		
	pass

def bipartie_match(frame_name1,frame_name2):
	G = nx.Graph()#

	for feName1 in simres1:
		for feName2 in simres2:
			str1 = "F1" + " "+feName1.__getitem__('FEName')
			str2 = "F2" + " "+feName2.__getitem__('FEName')
			edge_weight = calc_sim(feName1,feName2)
			G.add_edge(str1,str2,weight = edge_weight)
			pass
		pass


	res=nx.max_weight_matching(G, maxcardinality=True, weight='weight')
	print(str(frame_name1) + "  " + str(frame_name2))
	print(res)

	total_weight=0
	for edges in res:
		total_weight = total_weight + (G[edges[0]][edges[1]]['weight']) #get edge weight value
		pass

	print(total_weight)

	file = open('Frame_Similarity.txt', 'a')
	file.write(str(frame_name1) + "  " + str(frame_name2))
	file.write("\n")
	file.write(str(total_weight))
	file.write("\n")
	file.write(str(res))
	file.write("\n")
	file.write("\n")
	file.write("\n")
	file.close()

	pass


def calc_sim(feName1,feName2):
	sim_value = 0
	#case1 name match, pos match, then calc the sim corelated to the Count
	if feName1.__getitem__('FEName') == feName2.__getitem__('FEName') and feName1.__getitem__('POS') == feName2.__getitem__('POS'):
		sim_value = 2*(prob_distribution1(feName1))*(prob_distribution2(feName2))
		#sim_value = 2*(feName1.__getitem__('Count')+feName2.__getitem__('Count'))
		return sim_value
		pass

	#case2 name match, pos not match
	if feName1.__getitem__('FEName') == feName2.__getitem__('FEName') and feName1.__getitem__('POS') != feName2.__getitem__('POS'):
		sim_value = 1*(prob_distribution1(feName1))*(prob_distribution2(feName2))
		#sim_value = 1*(feName1.__getitem__('Count')+feName2.__getitem__('Count'))
		return sim_value
		pass

	#case3 name not match, pos match
	if feName1.__getitem__('FEName') != feName2.__getitem__('FEName') and feName1.__getitem__('POS') == feName2.__getitem__('POS'):
		sim_value = 0.5*(prob_distribution1(feName1))*(prob_distribution2(feName2))
		#sim_value = 0.5*(feName1.__getitem__('Count')+feName2.__getitem__('Count'))
		return sim_value
		pass

	#case4 name not match, pos not match
	if feName1.__getitem__('FEName') != feName2.__getitem__('FEName') and feName1.__getitem__('POS') != feName2.__getitem__('POS'):
		sim_value = 0
		return sim_value
		pass

	return sim_value
	pass

def cosine_sim(fileid1,fileid2):#calc cosine simlirity
	vec1 = fileid1.__getitem__('Pos_Dist') #get tf-idf vec for fileid1
	vec2 = fileid2.__getitem__('Pos_Dist') #get tf-idf vec for fileid1
	norm1 = normalizer(vec1) #normalize vec1
	norm2 = normalizer(vec2) #normalize vec2 
	sim = np.dot(vec1, vec2) / (norm1*norm2) #calc cosine simlirity
	return sim
	pass

def normalizer(self,vec): # vector normalize
	denom = np.sum([el**2 for el in vec])
	return math.sqrt(denom)
	pass
	
def prob_distribution1(FEName_Target):
	target_count = 0
	total_count = 0
	for feName1 in simres1:
		if feName1.__getitem__('FEName') == FEName_Target.__getitem__('FEName'):
			total_count = total_count + feName1.__getitem__('Count')
			pass
		if feName1.__getitem__('FEName') == FEName_Target.__getitem__('FEName') and feName1.__getitem__('POS') == FEName_Target.__getitem__('POS'):
			target_count = feName1.__getitem__('Count')
			pass
		pass

	prob = target_count/total_count
	return prob
	pass

def prob_distribution2(FEName_Target):
	target_count = 0
	total_count = 0
	for feName1 in simres2:
		if feName1.__getitem__('FEName') == FEName_Target.__getitem__('FEName'):
			total_count = total_count + feName1.__getitem__('Count')
			pass
		if feName1.__getitem__('FEName') == FEName_Target.__getitem__('FEName') and feName1.__getitem__('POS') == FEName_Target.__getitem__('POS'):
			target_count = feName1.__getitem__('Count')
			pass
		pass

	prob = target_count/total_count
	return prob
	pass










