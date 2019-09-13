import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects
import matplotlib.patches as patches
import csv
import string
import seaborn as sns

class house():
    '''
    Describes the house using the data from the input directory
    '''
    def __init__(self,house_dir_=None,experiment_dir_=None):
        '''
        Constructor
        '''
        if house_dir_ is not None:
            self.experiment_dir_ = experiment_dir_
            self.house_dir = house_dir_
            self.init_house_vars()

    def init_house_vars(self):
        ''' '''
        self.ap_coords = self.readCSV2Dict(os.path.join(self.house_dir,"ap_coordinates.dat"))
        self.ap_mac = self.readCSV2Dict(os.path.join(self.house_dir,"ap_mac_addresses.dat"))
        self.ap_rooms = self.readCSV2Dict(os.path.join(self.house_dir,"ap_rooms.dat"))
        self.floor_tags = self.readCSV2Dict(os.path.join(self.house_dir,"floor_tags.dat"))
        self.room_names= self.readCSV2Dict(os.path.join(self.house_dir,"room_names.dat"))
        self.room_tags = self.readCSV2Dict(os.path.join(self.house_dir,"room_tags.dat"))
        self.tag_adjacency = self.readCSV2Dict(os.path.join(self.house_dir,"tag_adjacency.dat"))
        self.tag_coordinates = self.readCSV2Dict(os.path.join(self.house_dir,"tag_coordinates.dat"))
        self.act_tag_descriptions = self.readCSV2Dict(os.path.join(self.house_dir,"act_desc.dat"))
        self.floor_aps = self.readCSV2Dict(os.path.join(self.house_dir,"floor_aps.dat"))


        # experiments
        print("tag_annotations.dat")
        self.tag_annotations = self.readCSV2Dict_tagCoor(os.path.join(self.experiment_dir_,"tag_annotations.dat"))
        self.RSSI = self.readCSV2Dict_RSSI(os.path.join(self.experiment_dir_,"rx_wearable_data.dat"))

        # debug
        print("self.ap_coords")
        print(self.ap_coords)

        print("self.tag_coordinates")
        print(self.tag_coordinates)

        print("self.tag_annotations")
        print(self.tag_annotations[0])

        print("self.RSSI")
        print(self.RSSI[0])

    def getRSSIData(self):
        return self.RSSI

    def match_tagAnno_RSSI(self,time_RSSI,IDLast_tagAnno):
        '''
        Match the RSSI and tag annotation, by the time stamp recorded in both files.
        '''
        # Get time stamp from the RSSI file
        hour_RSSI = float(time_RSSI[11])*10.+float(time_RSSI[12])
        minu_RSSI = float(time_RSSI[14])*10.+float(time_RSSI[15])
        seco_RSSI = float(time_RSSI[17])*10.+float(time_RSSI[18])
        mili_RSSI = float(time_RSSI[20])*100.+float(time_RSSI[21])*10.+float(time_RSSI[22])
        value_RSSI = mili_RSSI + seco_RSSI*1e3 + minu_RSSI*1e3*60. + hour_RSSI*1e3*3600.

        # Get time stamps from the tag annotation file, and fo the matching
        ID_time = {}
        timeInterval = 5.*1e3 # 0.5 seconds
        for ID in range(IDLast_tagAnno,IDLast_tagAnno+200):
            #print(len(self.tag_annotations))

            if ID>=len(self.tag_annotations):
            # if some IDs is out of the range of the self.tag_annotations
				print("if some IDs is out of the range of the self.tag_annotations")
				break

            time_tagAnno = self.tag_annotations[ID][0]
            #print("ID {}, time_tagAnno {}".format(ID, time_tagAnno))
            hour_tagAnno = float(time_tagAnno[11])*10.+float(time_tagAnno[12])
            minu_tagAnno = float(time_tagAnno[14])*10.+float(time_tagAnno[15])
            seco_tagAnno = float(time_tagAnno[17])*10.+float(time_tagAnno[18])
            mili_tagAnno = float(time_tagAnno[20])*100.+float(time_tagAnno[21])*10.+float(time_tagAnno[22])
            value_tagAnno = mili_tagAnno + seco_tagAnno*1e3 + minu_tagAnno*1e3*60. + hour_tagAnno*1e3*3600.

            time_deference = abs(value_tagAnno-value_RSSI)
            if ID==IDLast_tagAnno:
            # if ID equas to IDLast_tagAnno, add it into the dict nomatter if the time deference is smaller than the time interval 
                ID_time[time_deference] = ID

            elif time_deference<=timeInterval:
                ID_time[time_deference] = ID


        time_anno_key = ID_time[sorted(ID_time)[0]]
        time_anno_deference = sorted(ID_time)[0]
#        print("ID_time {}".format(ID_time))
#        print("sorted(ID_time) {}".format(sorted(ID_time)))
#        print("time_anno_key {}".format(time_anno_key))

        return time_anno_key, time_anno_deference

    def readCSV2Dict_RSSI(self,filenameStr):
        '''
        Read the lines of the csv file to a dictionary. Col 1 is the key, col 2 is the value.
        '''
        mydict = {}
        with open(filenameStr, "rt") as csvfile:
            readerO = csv.reader(csvfile)
            lineID = 0
            IDLast_tagAnno = 0
            for rows in readerO:
                # debug
                #if lineID>10:
                #    break

                if lineID==0:
                    lineID += 1
                    continue
#                print(rows)
                RSSI = []
                # Data part 1 : informations about RSSI 
                RSSI.append(rows[0]) # time stamp
                RSSI.append(int(rows[1])) # ap id
                RSSI.append(int(rows[3])) # rssi
                RSSI.append(float(self.ap_coords[int(rows[1])][0])) # location x
                RSSI.append(float(self.ap_coords[int(rows[1])][1])) # location y
                RSSI.append(float(self.ap_coords[int(rows[1])][2])) # location z
                # Data part 2 : informations about person, i.e. tag annotaion
                IDLast_tagAnno, time_anno_deference = self.match_tagAnno_RSSI(rows[0],IDLast_tagAnno)
                #print("IDLast_tagAnno {}, matching {},\n".format(IDLast_tagAnno, self.tag_annotations[IDLast_tagAnno]))
                RSSI.append(self.tag_annotations[IDLast_tagAnno][0]) # time stamp
                RSSI.append(float(self.tag_annotations[IDLast_tagAnno][1])) # location x
                RSSI.append(float(self.tag_annotations[IDLast_tagAnno][2])) # location y
                RSSI.append(float(self.tag_annotations[IDLast_tagAnno][3])) # location z
                RSSI.append(time_anno_deference) # time difference, milliseconds
                mydict[lineID-1] = RSSI
                lineID += 1
                #print("RSSI ID {}, RSSI {},\n".format(lineID, RSSI))

        return mydict   

    def readCSV2Dict_tagCoor(self,filenameStr):
        '''
        Read the lines of the csv file to a dictionary. Col 1 is the key, col 2 is the value.
        '''
        mydict = {}
#        mydict[-1] = 2
        #print(filenameStr)
        with open(filenameStr, "rt") as csvfile:
            
            readerO = csv.reader(csvfile)
            lineID = 0
            for rows in readerO:
                if lineID==0:
                    lineID += 1
                    continue
#                print(rows)
                pos_person = []
                tagID =    int(rows[2])
                pos_person.append(rows[0])
                pos_person.append(float(rows[3]) + self.tag_coordinates[tagID][0])
                pos_person.append(float(rows[4]) + self.tag_coordinates[tagID][1])
                pos_person.append(float(rows[5]) + self.tag_coordinates[tagID][2])
                mydict[lineID-1] = pos_person
                lineID += 1

        return mydict   

    def readCSV2Dict(self,filenameStr):
        '''
        Read the lines of the csv file to a dictionary. Col 1 is the key, col 2 is the value.
        '''
        mydict = {};
        #print(filenameStr)
        with open(filenameStr, "rt") as csvfile:
            
            readerO = csv.reader(csvfile)
            firstRow = next(readerO)
            
            firstElement = firstRow[0]
            #Check if digit and if so do not reset the iterator, otherwise continue as the first line is just a header.
            if(firstElement.isdigit()):
                csvfile.seek(0)
                readerO = csv.reader(csvfile)
                #check type of values.
                if firstRow[1].isdigit():
                    typeStr = "int"
                elif firstRow[1].replace('.','',1).isdigit():
                    typeStr = "float"
                else:
                    typeStr = "string"

            print("typeStr {}".format(typeStr))       

            if(typeStr=="int"):
                mydict = {int(rows[0]):[int(i) for i in rows[(1):]] for rows in readerO}
            elif (typeStr=="string"):
                mydict = {int(rows[0]):rows[(1):] for rows in readerO}
            else:
                mydict = {int(rows[0]):[float(i) for i in rows[(1):]] for rows in readerO}
        
        length_dict = [len(mydict[key]) for key in mydict]
        single_vals = all(len_v == 1 for len_v in length_dict)
        if single_vals:
            mydict = {key:mydict[key][0] for key in mydict}
            
        return mydict   


def main():
 #==============================================================================
 #    h = house(r"F:\rss_acc_data_paper\house_b\metadata")
 # 
 #    h.plot_tags_aps( r"F:\temp\b")
 #==============================================================================
    
#    h = house(r"../ble-accelerometer-indoor-localisation-measurements/house_A/metadata")
#    h.plot_tags_aps( r"./a")

    house_dir = r"../ble-accelerometer-indoor-localisation-measurements/house_B/metadata"
    experiment_dir = r"../ble-accelerometer-indoor-localisation-measurements/house_B/experiments/fingerprint_floor"
    h = house(house_dir_=house_dir,experiment_dir_=experiment_dir)
    RSSI = h.getRSSIData()

    # write
    f = open("data_rssi_ap.txt","w")
    for k in RSSI:
        line = ""
        line += (str(k) + " ")
        for ele in RSSI[k]:
            line += (str(ele) + " ")
        line += "\n"
        f.write(line)
    f.close()


#
#    h = house(r"../ble-accelerometer-indoor-localisation-measurements/house_C/metadata")
#    h.plot_tags_aps( r"./c")
#
#    h = house(r"../ble-accelerometer-indoor-localisation-measurements/house_D/metadata")
#    h.plot_tags_aps( r"./d")

if __name__ == '__main__':
    print("hello")
    main()
