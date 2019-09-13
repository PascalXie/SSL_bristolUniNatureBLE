import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects
import matplotlib.patches as patches
import csv
import string
import seaborn as sns
import pandas as pd
import random
import math

def plot_rssi_distance():
	# read file
	f = open("data_step3_rssi_distance.txt")
	lines = f.readlines()

	# get line
	DataRSSI = {} # dictionary
	ID = 0
	for line in lines:
		line = line.strip().split()
		
		dist	= float(line[0])
		rssi	= float(line[1])
		content = float(line[2])

		DataRSSI[ID] = [dist,rssi,content]

		ID += 1

	# debug
	print(DataRSSI[0])

	#
	# plot :  RSSI and distance
	#
	RSSIs = []
	dists = []
	weights = []

	for ID in range(len(DataRSSI)):
		dists.	append(DataRSSI[ID][0])
		RSSIs.	append(DataRSSI[ID][1])
		weights.append(DataRSSI[ID][2])

	df = pd.DataFrame({'RSSI':RSSIs,'Distance': dists, 'values':weights})
	pt = df.pivot_table(index='RSSI', columns='Distance', values='values', aggfunc=np.sum)
	print("df : \n{}".format(df))
	print("pt : \n{}".format(pt))

	sns.heatmap(pt, linewidths = 0.0, cmap='RdPu')
	plt.savefig('figure-RSSIAndDistance.png',dpi=300)
	plt.show()

def plot_distance_target_tag():
	# 1D histgram
	# read file
	f = open("data_step3_distance_target_tag.txt")
	lines = f.readlines()

	# get line
	DataDist = {} # dictionary
	ID = 0
	for line in lines:
		line = line.strip().split()
		
		dist	= float(line[0])
		count	= float(line[1])

		DataDist[ID] = [dist,count]

		ID += 1

	#
	# plot :  RSSI and distance
	#
	dists  = []
	counts = []
	for ID in range(len(DataDist)):
		dists.	append(DataDist[ID][0])
		counts.	append(DataDist[ID][1])
	
	plt.plot(dists,counts,marker='.', mec='r', mfc='w',label='Distance between target and tag')
	plt.savefig('figure-DistanceTargetToTag.png',dpi=300)
	plt.show()

def plot_target_position():
	# read file
	f = open("data_step3_target_x_y.txt")
	lines = f.readlines()

	# get line
	DataPos = {} # dictionary
	ID = 0
	for line in lines:
		line = line.strip().split()
		
		x	= round(float(line[0]),2)
		y	= round(float(line[1]),2)
		content = float(line[2])

		if content<1:
			content = 0
		else:
			content = math.log10(content)

		DataPos[ID] = [x,y,content]

		ID += 1

	#
	# plot :  position
	#
	xs = []
	ys = []
	counts = []
	for ID in range(len(DataPos)):
		xs.		append(DataPos[ID][0])
		ys.		append(DataPos[ID][1])
		counts.	append(DataPos[ID][2])

	df = pd.DataFrame({'X / m':xs,'Y / m': ys, 'Counts':counts})
	pt = df.pivot_table(index='Y / m', columns='X / m', values='Counts', aggfunc=np.sum)

	sns.heatmap(pt, linewidths = 0.0, cmap='RdPu')
	plt.savefig('figure-TargetPostions.png',dpi=300)
	plt.show()

def plot_apID_tagID():
	# read file
	f = open("data_step3_apID_tagID.txt")
	lines = f.readlines()

	# get line
	DataIDs = {} # dictionary
	ID = 0
	for line in lines:
		line = line.strip().split()
		
		apid	= int(line[0])
		tagid	= int(line[1])
		content = float(line[2])

		DataIDs[ID] = [apid,tagid,content]

		ID += 1

	#
	# plot :  position
	#
	xs = []
	ys = []
	counts = []
	for ID in range(len(DataIDs)):
		xs.		append(DataIDs[ID][0])
		ys.		append(DataIDs[ID][1])
		counts.	append(DataIDs[ID][2])

	df = pd.DataFrame({'AP ID':xs,'Tag ID': ys, 'Counts':counts})
	pt = df.pivot_table(index='AP ID', columns='Tag ID', values='Counts', aggfunc=np.sum)

	sns.heatmap(pt, linewidths = 0.0, cmap='RdPu')
	plt.savefig('figure-APID-TagID.png',dpi=300)
	plt.show()

if __name__ == '__main__':
	print("hello")
	#plot_rssi_distance()
	#plot_distance_target_tag()
	#plot_target_position()
	plot_apID_tagID()
