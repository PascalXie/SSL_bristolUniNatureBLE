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

def main():
	# read file
	f = open("data_step1_rssi_ap.txt")
	lines = f.readlines()

	# get line
	DataRSSI = {} # dictionary
	for line in lines:
		line = line.strip().split()

		ID = int(line[0])
		#time_stamp_ap	=       line[1]
		#ap_id			=   int(line[2]) # anchor node, i.e. AP, Acess Point
		#rssi			= float(line[3])
		#ap_loc_x		= float(line[4])
		#ap_loc_y		= float(line[5])
		#ap_loc_z		= float(line[6])
		#time_stamp_tar	=       line[7]  # target node, i.e. person
		#tar_loc_x		= float(line[8])
		#tar_loc_y		= float(line[9])
		#tar_loc_z		= float(line[10])
		#time_deference	= float(line[11]) # time deference, milliseconds
		#target_tag_dist	= float(line[12]) # distance between target and tag, m
		#data = [time_stamp_ap,ap_id,rssi,ap_loc_x,ap_loc_y,ap_loc_z,time_stamp_tar,tar_loc_x,tar_loc_y,tar_loc_z,time_deference,target_tag_dist]

		ap_id			=   int(line[1]) # anchor node, i.e. AP, Acess Point
		rssi			= float(line[2])
		ap_loc_x		= float(line[3])
		ap_loc_y		= float(line[4])
		ap_loc_z		= float(line[5])
		tag_id			=   int(line[6]) # target node, i.e. person
		tar_loc_x		= float(line[7])
		tar_loc_y		= float(line[8])
		tar_loc_z		= float(line[9])
		time_deference	= float(line[10]) # time deference, milliseconds
		target_tag_dist	= float(line[11]) # distance between target and tag, m
		data = [ap_id,rssi,ap_loc_x,ap_loc_y,ap_loc_z,tag_id,tar_loc_x,tar_loc_y,tar_loc_z,time_deference,target_tag_dist]
		DataRSSI[int(line[0])] = data
	
	# pandas dataFrame

	# debug
	print(DataRSSI[0])

	#
	# plot : anchor 
	#
	ap_loc_xs = [DataRSSI[ele][3] for ele in DataRSSI]
	ap_loc_ys = [DataRSSI[ele][4] for ele in DataRSSI]
	#print(ap_loc_xs)

	fig = plt.figure(figsize=(4,3))
	color = ['tab:blue', 'tab:orange', 'tab:green']
	plt.scatter(ap_loc_xs, ap_loc_ys, marker='s',s=150,c=color[0],alpha=0.8,edgecolors='none',label='Anchor')
	plt.legend(frameon=True)
	plt.xlabel('X / m',fontdict={'family' : 'Times New Roman', 'size': 12})
	plt.ylabel("Y / m",fontdict={'family' : 'Times New Roman', 'size': 12})
	#plt.xlim(-105,170)
	#plt.ylim(-110,110)
	plt.title('Anchor Distribution')
	plt.savefig('figure-AnchorDistribution.png',dpi=300)

	#
	# plot : target
	#
	tar_loc_xs = [DataRSSI[ele][6] for ele in DataRSSI]
	tar_loc_ys = [DataRSSI[ele][7] for ele in DataRSSI]
	for ID in range(10):
		print("Target ID {}, Loc {}, {}".format(ID, tar_loc_xs[ID],tar_loc_ys[ID]))

	fig = plt.figure(figsize=(7,6))
	color = ['tab:blue', 'tab:orange', 'tab:green']
	plt.scatter(tar_loc_xs, tar_loc_ys, marker='s',s=10,c=color[0],alpha=0.1,edgecolors='none',label='Anchor')
	plt.legend(frameon=True)
	plt.xlabel('X / m',fontdict={'family' : 'Times New Roman', 'size': 12})
	plt.ylabel("Y / m",fontdict={'family' : 'Times New Roman', 'size': 12})
	#plt.xlim(-105,170)
	#plt.ylim(-110,110)
	plt.title('Target Distribution')
	plt.savefig('figure-TargetDistribution.png',dpi=300)


	##
	## plot : target, kenel density 
	##
	#df = pd.DataFrame(DataRSSI)
	#print(df)
	#print(df.T)

	#dfSampled = df.T.sample(n=1000)

	#sns.jointplot(x=dfSampled[7], y=dfSampled[8], kind='kde', color="grey", space=0)
	#plt.xlabel('X / m',fontdict={'family' : 'Times New Roman', 'size': 12})
	#plt.ylabel("Y / m",fontdict={'family' : 'Times New Roman', 'size': 12})
	##plt.xlim(-105,170)
	##plt.ylim(-110,110)
	#plt.title('Target Distribution')
	#plt.savefig('figure-TargetDistribution-kde.png',dpi=300)
	plt.show()

#	fig = plt.figure(figsize=(4,3))
#	color = ['tab:blue', 'tab:orange', 'tab:green']
#	plt.scatter(dists, RSSIs, marker='o',s=150,c=color[0],alpha=0.1,edgecolors='none',label='RSSI')
#	plt.legend(frameon=True)
#	plt.xlabel('Distance / m',fontdict={'family' : 'Times New Roman', 'size': 12})
#	plt.ylabel("RSSI / dB",fontdict={'family' : 'Times New Roman', 'size': 12})
#	plt.title('Relationship Between RSSI and Distance')
#	plt.savefig('figure-RSSIAndDistance.png',dpi=300)
#	plt.show()

	return

if __name__ == '__main__':
	print("hello")
	main()

#	mydict = {"A":[1,2],"B":[1,2],"C":[1,2]}
#	df = pd.DataFrame(mydict)
#	print(df)
