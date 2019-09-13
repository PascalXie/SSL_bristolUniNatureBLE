'''
Created on 27 Mar 2018

@author: Dallan Byrne
@license: MIT See license.txt
@version: Python 3.4
@summary: Class that loads the relevent house metadata.
            From the "Residential Wearable RSSI and Accelerometer Measurements with Detailed Annotations" repo.
'''
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
    def __init__(self,dir_=None):
        '''
        Constructor
        '''
        if dir_ is not None:
            self.house_dir = dir_
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

        self.tags = list(self.tag_coordinates.keys())
        self.tags_activity  = list(self.act_tag_descriptions.keys())
        self.tags_floor = [t for t in self.tags if t not in self.tags_activity]
        self.tags_floor_coordinates={}
        for t in self.tags_floor:
            self.tags_floor_coordinates[t] = self.tag_coordinates[t]
        
        self.num_tags_activity = len( self.tags_activity)
        self.num_tags_floor = len(self.tags) - self.num_tags_activity
        self.num_floors = len(self.floor_tags.keys())
        self.num_aps = len(self.ap_mac.keys())


        print("self.ap_coords")
        print(self.ap_coords)

        print("self.tag_coordinates")
        print(self.tag_coordinates)
        
        
    def plot_tags_aps(self, dir_write_ = None):
        ''' plot the floor plans with the ap locs'''
        
        #plt.style.use('seaborn-paper')
        plt.close("all")
        sns.set()
        if dir_write_ is not None:
            self.mk_dir(dir_write_)
        d_letters = dict(enumerate(string.ascii_lowercase, 1))
        distance_thresh = 200
        dis_range = 30
        theta_range = 10
        
        fig_array = []
        
        vecAxis = np.array([1,0]) - np.array([0,0])
        
        loc_floor_array = list(self.tags_floor_coordinates.values())
        loc_floor_array = np.array(loc_floor_array)
        


        axisX, axisY = self.get_plot_limits(loc_floor_array)
        
        #Colours - define in array.
        colourList = ['k','b','r','g','y',[.5,.6, .7],[.8, .2, .6]]
        colourList = colourList + colourList
        figFloorList = []
        
        
        print("Plotting tag layout...")
        #Loop through floors
        for iF in self.floor_tags:
            figFloor = plt.figure(iF,figsize=(16/1.5, 9/1.5))
            figFloorList.append(figFloor)
            ax = figFloor.gca()
            ax.set_facecolor('#E6E6FA')
            #ax.grid(True)
            tags_on_current_level = self.floor_tags[iF]
            
            #omit activities for this plot
            tags_on_current_level = [t for t in tags_on_current_level if t not in self.tags_activity]
            colour_room_legend={}
            for iS in tags_on_current_level:
                current_tag = iS
                current_tag_adjacency = self.tag_adjacency[current_tag]
                current_tag_coord = self.tag_coordinates[current_tag]
                current_room_index = self.returnKey(self.room_tags,current_tag)
                
                #get closest tags (not necessarily adjacent)
                closest_tags = self.get_closest_coord(distance_thresh, self.tags_floor_coordinates ,current_tag_coord,tags_on_current_level)
                
                plt.plot(current_tag_coord[0],current_tag_coord[1],'bo')
                txt = ax.text(current_tag_coord[0]+5, current_tag_coord[1]+5, str(current_tag), fontsize=12)
                txt.set_path_effects([matplotlib.patheffects.withStroke(linewidth=4, foreground='w')])
                
                boxXStart, boxYStart, boxXStop, boxYStop = self.get_tag_grid_limits(
                                                                                   closest_tags,
                                                                                   current_tag_coord,
                                                                                   vecAxis,
                                                                                   current_tag_adjacency,
                                                                                   theta_range,
                                                                                   dis_range)
                if iS ==1 and "house_d" in self.house_dir:
                    boxYStop = current_tag_coord[1]+50
                if iS ==22 and "house_c" in self.house_dir:
                    boxXStart = current_tag_coord[0]-50
                if iS ==34 and "house_c" in self.house_dir:
                    boxYStop = current_tag_coord[1]+27
                if iS ==28 and "house_c" in self.house_dir:
                    boxXStop = current_tag_coord[0]+35
                if iS ==27 and "house_c" in self.house_dir:
                    boxXStop = current_tag_coord[0]+35    
                if iS ==29 and "house_c" in self.house_dir:
                    boxXStart = current_tag_coord[0]-60   
                if iS ==40 and "house_c" in self.house_dir:
                    boxXStart = current_tag_coord[0]-30   
                if iS ==43 and "house_c" in self.house_dir:
                    boxXStart = current_tag_coord[0]-30     
                if iS ==32 and "house_c" in self.house_dir:
                    boxXStop = current_tag_coord[0]+60  
                if iS ==49 and "house_c" in self.house_dir:
                    boxXStart = current_tag_coord[0]-50   
                rectangleCoordinates = [boxXStart, boxYStart, boxXStop-boxXStart, boxYStop-boxYStart]
                
                if self.room_names[current_room_index] not in colour_room_legend:
                    colour_room_legend[self.room_names[current_room_index]] = colourList[current_room_index-1]
                rect = patches.Rectangle((rectangleCoordinates[0:2]),rectangleCoordinates[2],rectangleCoordinates[3],linewidth=1,edgecolor=colourList[current_room_index-1],facecolor='none')
                ax.add_patch(rect)
                
            for ap in self.floor_aps[iF]:
                ap_loc = self.ap_coords[ap]
                ap_loc = np.array(ap_loc)
                ap_room = self.ap_rooms[ap]
                ap_room_key = self.findKeyFromDictValue(self.room_names, ap_room)
                ax.text(ap_loc[0], ap_loc[1], d_letters[ap], color=colourList[ap_room_key-1], 
                        bbox=dict(facecolor="#F0F8FF",alpha=0.75, edgecolor=colourList[ap_room_key-1], boxstyle='round,pad=0.5'))   
            
            custom_lines = [] 
            
            for  room_legend in colour_room_legend:
                colour = colour_room_legend[room_legend]
                custom_lines.append(matplotlib.lines.Line2D([0], [0], color=colour, lw=4))

            room_list = colour_room_legend.keys()
            
            #ax.legend(custom_lines, room_list,loc='best')
            ax.set_xlim(axisX)
            ax.set_ylim(axisY)
            ax.grid(color='w')
            #figFloor.suptitle("Floor %d"%(iF))
            plt.xlabel('X(cm)')
            plt.ylabel('Y(cm)')
            #===================================================================
            # lgd = ax.legend(custom_lines, room_list,
            #           bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            #===================================================================
            
            lgd_args = dict(ncol=3,loc='upper center',
                       framealpha=1, borderaxespad=0, frameon=False)
            
            
            lgd = ax.legend(custom_lines, room_list
                       , bbox_to_anchor=(0.5,-0.1),
                       **lgd_args)
         
            #plt.show()
            #input(" enter")
            if dir_write_ is not None:
                figFloor.savefig(os.path.join(dir_write_,"floor_"+str(iF)+".png"), bbox_extra_artists=(lgd,), bbox_inches='tight',dpi=300)
            #dIo.writePngFigure( self.floorplanFiles[iF], plt)
            #plt.close()
            
        return figFloorList
    def get_tag_grid_limits(self, closest_tags_,current_tag_coord_,vec_axis_,
                            current_tag_adjacency_,theta_range_,dis_range_):     
        #closest_tags = closestStates   currentStateCoor= current_tag_coord
        
        ''' plot box around tag location '''
        midX = []
        midY = []
        adjacentState = []
        for neighbState in closest_tags_:
            adjacentState.append(neighbState)
            adjacentCoord = self.tag_coordinates[neighbState]
            
            vecLine = np.array(adjacentCoord) - np.array(current_tag_coord_)
            neighAngle = np.arctan2(vecLine[1] - vec_axis_[1],vecLine[0] - vec_axis_[0])*(180/np.pi)
            
            xDis = vecLine[0]
            yDis = vecLine[1]
            
            midX.append(xDis/2)
            midY.append(yDis/2)
            
        midPointCoordX = [x+current_tag_coord_[0] for x in midX]
        midPointCoordY = [x+current_tag_coord_[1] for x in midY]
        westCoordsInd = self.findIf(midPointCoordX, lambda x: x < current_tag_coord_[0]-3)
        eastCoordsInd = self.findIf(midPointCoordX, lambda x: x > current_tag_coord_[0]+3)
        southCoordsInd = self.findIf(midPointCoordY, lambda x: x < current_tag_coord_[1]-3)
        northCoordsInd = self.findIf(midPointCoordY, lambda x: x > current_tag_coord_[1]+3)
                    
        xVecAxis = np.array([1000,0])
        yVecAxis = np.array([0,1000])  
                        
        sides = [1,2,3,4]
        for sideI in sides:
            if(sideI==1):
                coordInds = eastCoordsInd
                axisLine = xVecAxis
            elif(sideI==2):
                coordInds = westCoordsInd
                axisLine = xVecAxis
            elif(sideI==3):
                coordInds = southCoordsInd
                axisLine = yVecAxis
            else:
                coordInds = northCoordsInd
                axisLine = yVecAxis
                
            coordsSideX=[midPointCoordX[i] for i in coordInds]
            coordsSideY=[midPointCoordY[i] for i in coordInds]    
            
            if coordsSideX:
                vecLineA =  [x-current_tag_coord_[0] for x in coordsSideX]
                vecLineB =  [x-current_tag_coord_[1] for x in coordsSideY]
                thetas = []
                for iV,vA in enumerate(vecLineA):
                    dotP = np.dot(axisLine,[vA,vecLineB[iV]])
                    normP = np.linalg.norm(axisLine)*np.linalg.norm([vecLineA[iV],vecLineB[iV]])
                    cosTheta = dotP/normP
                    theta_ = np.arccos(cosTheta)*(180/np.pi)
                    if(abs(theta_) > 90):
                        theta_ = 180 - abs(theta_)
                    #print(theta_)    
                    thetas.append(theta_)    
                    
                indValid = self.findIf(thetas, lambda x: abs(x)<60)
                thetaValid = [thetas[i] for i in indValid]
                validX= [coordsSideX[i] for i in indValid]
                validY= [coordsSideY[i] for i in indValid]
                coordIndsValid = [coordInds[i] for i in indValid]
                adjacentStateValid = [adjacentState[i] for i in coordIndsValid]
                
                neighboursPresent  = np.nonzero(np.in1d(adjacentStateValid, current_tag_adjacency_))[0]
                if neighboursPresent.size >0:
                    validX = [validX[i] for i in neighboursPresent]
                    validY = [validY[i] for i in neighboursPresent]
                    thetaNeighbours = [thetaValid[i] for i in neighboursPresent]
                    sizeX = len(validX)
                    sizeY = len(validY)
                    if(sizeX>1):
                        dx = np.asarray(validX) - np.tile(current_tag_coord_[0],sizeX)
                        dy = np.asarray(validY) - np.tile(current_tag_coord_[1],sizeY)
                        dx2 = dx**2    #Power
                        dy2 = dy**2    #Power
                        distanceNeighbours = np.sqrt(dx2 + dy2)
                        
                        sortedThetaInds = np.argsort(thetaNeighbours) 
                        thetaNeighbours = [thetaNeighbours[i] for i in sortedThetaInds]
                        validX = [validX[i] for i in sortedThetaInds]
                        validY = [validY[i] for i in sortedThetaInds]
                        
                        indDirect = self.findIf(thetaNeighbours, lambda x : x<theta_range_)
                        allIndices = list(range(distanceNeighbours.size))
                        
                        for iD in indDirect:
                            otherInds = np.setdiff1d(np.asarray(allIndices),np.asarray(iD))
                            distanceNeighboursOI = [distanceNeighbours[i] for i in otherInds]
                                        
                            distOthers =[abs(disI -distanceNeighbours[iD])  for disI in distanceNeighboursOI]
                            indsWithinRange = self.findIf(distOthers, lambda x : x<dis_range_)
                            allWithinRange = [len(indsWithinRange)==len(distOthers)]
                            if(allWithinRange):
                                validX =validX[iD] 
                                validY= validY[iD]
                                break;
                validX = np.asarray(validX)
                validY = np.asarray(validY)  
                if(sideI==1):
                    if validX.size==0:
                        boxXStop = current_tag_coord_[0]+50
                    else:
                        boxXStop = np.amin(validX)
                        
                elif(sideI==2):  
                    if validX.size==0:
                        boxXStart = current_tag_coord_[0]-50
                    else:
                        boxXStart = np.amax(validX)
                       
                elif(sideI==3):
                    if validY.size==0:
                        boxYStart = current_tag_coord_[1]-50
                    else:
                        boxYStart = np.amax(validY)
                       
                else:
                    if validY.size==0:
                        boxYStop = current_tag_coord_[1]+50
                    else:
                        boxYStop = np.amin(validY)
                       
                    
            else:
                if(sideI==1):
                    boxXStop = current_tag_coord_[0]+50
                elif(sideI==2):  
                    boxXStart = current_tag_coord_[0]-50
                elif(sideI==3):
                    boxYStart = current_tag_coord_[1]-50
                else:
                    boxYStop = current_tag_coord_[1]+50
        if(boxXStart<10):
            boxXStart =10
        if(boxYStart<10):
            boxYStart =10
            
        #=======================================================================
        # if(abs(boxXStop- boxXStart)>150):
        #     boxXStart = current_tag_coord_[0]-50
        #=======================================================================
        if(abs(boxXStop- boxXStart)>130):
            if  abs(boxXStop  - current_tag_coord_[0])>65 :
                boxXStop = current_tag_coord_[0]+50
       
            if  abs(boxXStart  - current_tag_coord_[0])>65 : 
                boxXStart = current_tag_coord_[0]-50
                
        if(abs(boxYStop- boxYStart)>130):   
            if  abs(boxYStart  - current_tag_coord_[1])>65 :   
                boxYStart= current_tag_coord_[1]-50
            if  abs(boxYStop - current_tag_coord_[1])>65 :  
                 boxYStop= current_tag_coord_[1]+50
             
        #=======================================================================
        # if(abs(boxYStop- boxYStart)>150):
        #     boxXStop = current_tag_coord_[0]+50
        #=======================================================================
            
        
            
        return   boxXStart,  boxYStart, boxXStop, boxYStop
    def findIf(self,list_, func):
        '''Matlab style find
        a = [1, 2, 3, 1, 2, 3, 1, 2, 3]
        inds = findIf(a, lambda x: x > 2)
        '''
        return [i for (i, val) in enumerate(list_) if func(val)]   
    def findKeyFromDictValue(self, dict_,value):
        
        for key in dict_:
            values = dict_[key]
            if( isinstance(values, list)):
                if( value in values):
                    return(key)
            else:
                if(value == values):
                    return(key)
       
        #If we get this far then there is no key.
        return(None) 
    def get_closest_coord(self,distance_thresh_, loc_dict_ ,current_tag_coord_,tags_on_level_):
        ''' get closest tags withing a threshold'''
        
        def dist(x,y):   
            return np.sqrt(np.sum((x-y)**2))
        
        current_tag_coord_ = np.asarray(current_tag_coord_)
        nearInd = []
        for iL in tags_on_level_:
            tag_loc_l = loc_dict_[iL]
            if dist(tag_loc_l[0:2],current_tag_coord_[0:2])<=distance_thresh_:
                nearInd.append(iL)
                
        closest_tags = [self.tags[i] for i in nearInd]     
        return closest_tags
    def get_plot_limits(self, loc_array_):  
        #=======================================================================
        # Plot Limits
        #=======================================================================
        maxVals = np.amax(loc_array_, axis=0)   # Maxima along the first axis
        minVals = np.amin(loc_array_, axis=0)  
        
        maxAX = 0
        minAX = 1000
        
        maxAY = 0
        minAY = 1000
        for ap in self.ap_coords:
            ap_loc  = self.ap_coords[ap]
            
            if ap_loc[0] > maxAX:
                maxAX = ap_loc[0]
            if ap_loc[1] > maxAY:
                maxAY = ap_loc[1]    
                
            if ap_loc[0] < minAX:
                minAX = ap_loc[0]
            if ap_loc[1] < minAY:
                minAY = ap_loc[1]   
                
     
        minY = np.min([minVals[1]-60, minAY-30])   
        minX = np.min([minVals[0]-60, minAX-30])
        maxY = np.max([maxVals[1]+60, maxAY+30])   
        maxX = np.max([maxVals[0]+60, maxAX+30]) 
        axisY = np.array([minY,maxY]);
        axisX = np.array([minX,maxX]);
        
        
        axisY[0] = (0 if axisY[0]<0 else axisY[0])
        axisX[0] = (0 if axisX[0]<0else axisX[0])
       
        return   axisX, axisY
              
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
    
    def returnKey(self,dictIn,search_value):
        '''Find key of value in dictionary'''
        correctKey = -1
        for key_ in dictIn:
            values = dictIn[key_]
            if search_value in values:
                correctKey = key_
                break
            
    
        return(correctKey)
    
    def mk_dir(self,dirname):
        try:
            os.stat(dirname)
        except:
            os.makedirs(dirname,exist_ok=True)
def main():
 #==============================================================================
 #    h = house(r"F:\rss_acc_data_paper\house_b\metadata")
 # 
 #    h.plot_tags_aps( r"F:\temp\b")
 #==============================================================================
    
#    h = house(r"../ble-accelerometer-indoor-localisation-measurements/house_A/metadata")
#    h.plot_tags_aps( r"./a")

    h = house(r"../ble-accelerometer-indoor-localisation-measurements/house_B/metadata")
    h.plot_tags_aps( r"./b")
#
#    h = house(r"../ble-accelerometer-indoor-localisation-measurements/house_C/metadata")
#    h.plot_tags_aps( r"./c")
#
#    h = house(r"../ble-accelerometer-indoor-localisation-measurements/house_D/metadata")
#    h.plot_tags_aps( r"./d")
    
 #==============================================================================
 #    h = house(r"F:\rss_acc_data_paper\house_d\metadata")
 # 
 #    h.plot_tags_aps( r"F:\temp\d")
 #    
 #    h = house(r"F:\rss_acc_data_paper\house_a\metadata")
 # 
 #    h.plot_tags_aps( r"F:\temp\a")
 #==============================================================================
if __name__ == '__main__':
    main()
