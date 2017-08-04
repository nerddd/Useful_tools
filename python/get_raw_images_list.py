#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
create a image list to train raw network.
'''

import os
import sys
import random

# actually 96 x 112
data_root = "/home/yf/data/umdfaces/all_umdfaces_256_256/"
triplet_size = 80
batch_size = {'all_umdfaces_train': 2, 'all_umdfaces_val':1}

def read_file(filename, num=4932655):
	image_list = []		# id->images
	for i in xrange(num):
		image_list.append([])
	assert len(image_list) == num
	
	with open(filename) as f:
		lines = f.readlines()
		for line in lines:
			id = int(line.strip().split()[1])
			image_list[id].append(line)
			
	return image_list

def remove_empty(image_list):
	try:
		while True:
			image_list.remove([])
	except:
		return image_list
	
def histogram(image_list):
	max = 0
	for l in image_list:
		if max < len(l):
			max = len(l)

	hist = []	# num -> class count
	for i in xrange(max+1):
		hist.append(0)
	for l in image_list:
		hist[len(l)] += 1
	
	for i in xrange(max+1):
		print i, hist[i]

def write_list(image_list):
	for k, v in image_list.iteritems():
		vlist = []
		for l in v:
			vlist.extend(l)
		with open('%s.txt' %k, 'w') as f:
			f.writelines(vlist)

def split_data(image_list, ratio = 0.2):
	train_list = []
	val_list = []
	for i in xrange(len(image_list)):
		l = image_list[i]
		random.shuffle(l)
		bound = int(len(l)*ratio)
		train_list.append(l[bound:])
		val_list.append(l[:bound])
	
	return {'train': train_list, 'val': val_list}

## triplet: (anchor positive negatives)
# triplet_size = num_negatives + 2
def generate_triplets(filename, epochs = 1, triplet_size=triplet_size):
	image_list = read_file(filename)
	_len = len(image_list)
	split_list = split_data(image_list)
	
	triplets = {}
	for k,v in batch_size.iteritems():
		triplets[k] = []
		for epoch in xrange(epochs):
			for i in xrange(_len):
				for j in xrange(v):
					## add anchor and positive
					random.shuffle(split_list[k][i])
					triplets[k].extend(split_list[k][i][:2])
					## add negatives
					randlist = range(_len)
					random.shuffle(randlist)
					negs = randlist[:triplet_size-2]
					if i in negs:
						randlist[negs.index(i)] = randlist[triplet_size-2]
					for ix in negs:
						triplets[k].append(random.choice(split_list[k][ix]))
				sys.stdout.write('\r%s: %d' %(k, i+1))
		print '\nlen: %d' %len(triplets[k])
		with open('%s_raw.txt'%k, 'w') as f:
			f.writelines(triplets[k])
			
## read filenames in custom dir
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join(filepath, allDir)
        print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题
	print len(pathDir)

if __name__ == "__main__":
	image_list=read_file('all_umdfaces_clean.txt')
	split_list=split_data(image_list)
	write_list(split_list)
	print 'Done'
	
