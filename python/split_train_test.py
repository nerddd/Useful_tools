#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
create a image list to train raw network.
'''

import os
import sys
import random


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


def write_list(image_list):
	for k, v in image_list.iteritems():
		vlist = []
		for l in v:
			vlist.extend(l)
		with open('%s.txt' %k, 'w') as f:
			f.writelines(vlist)

def split_data(image_list, ratio = 0.1):
	train_list = []
	val_list = []
        test_list =[]
	for i in xrange(len(image_list)):
		l = image_list[i]
		random.shuffle(l)
		bound = int(len(l)*ratio)
		train_list.append(l[2*bound:])
		val_list.append(l[:bound])
                test_list.append(l[bound:2*bound])
	
        return {'train': train_list, 'val': val_list,'test':test_list}


if __name__ == "__main__":
	image_list=read_file('imdb.txt')
	split_list=split_data(image_list)
	write_list(split_list)
	print 'Done'
	
