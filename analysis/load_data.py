'''
Created on 27 Mar 2018

@author: Dallan Byrne
@license: MIT See license.txt
@version: Python 3.4
@summary: Module to load house measurements from the 
            "Residential Wearable RSSI and Accelerometer Measurements with Detailed Annotations" repo.
'''
import os
import pandas
import csv
import codecs
import numpy as np; np.random.seed(sum(map(ord, "distributions")))
import seaborn; seaborn.set(color_codes=True)
import matplotlib.pyplot as plt
import house
import scipy
import matplotlib

def read_csv_2_df(filename_):
        ''' read csv to a pandas dataframe'''
        #trim headers for spaces
        with open(filename_, "rU", encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            header =  next(reader)
        
        trimmedHeader = [h.lstrip() for h in header]
          
        
        doc = codecs.open(filename_,'rU','UTF-8') #open for reading with "universal" type set
        
        #read in chunks
        tp = pandas.read_csv(doc, skipinitialspace=True,low_memory=False,iterator=True, chunksize=500)#, error_bad_lines=False)
        table = pandas.concat(tp, ignore_index=True)
        table.columns = trimmedHeader
        
        return table
def load_exp_data(dir_main_):
    exp_file = os.path.join(dir_main_,"rx_wearable_data.dat")
    rssi_df  =read_csv_2_df(exp_file)
    
    ap_ref_df = read_csv_2_df(os.path.join(dir_main_,"ap_mac_ref.dat"))
    wear_ref_dat =  read_csv_2_df(os.path.join(dir_main_,"wear_mac_ref.dat"))
    
    rssi_df = pandas.merge(rssi_df, ap_ref_df, on=["ap_id"])
    rssi_df = pandas.merge(rssi_df, wear_ref_dat, on=["wearable_id"])
    
    rssi_df["timestamp"] = pandas.to_datetime(rssi_df["timestamp"])
                           
    #===========================================================================
    # print(rssi_df.head(5))
    # print(rssi_df.tail(5))
    #===========================================================================
    
    return rssi_df
    
def plot_tag_distribution(rssi_df_, acc_df_,ann_df_, tag_,ap_=1):
    '''plot a distribution for a specific tag'''
    
    #find groups of tags in ann data
    tag_ann_df = ann_df_[ann_df_["tag"]==tag_]
    

    #Match rssi to annotations at tag
    rssi_tag_df = get_closest_to_ann_times(rssi_df_,tag_ann_df,acceptable_delay_ms_=500)
    
    
    
    #timestamps in rssi_tag_df  in acc_df_
    rssi_acc_tag_df = pandas.merge(rssi_tag_df[["timestamp","rssi"]], acc_df_, on = "timestamp")
    
    rssi_tag_df = rssi_tag_df[rssi_tag_df["ap_id"] == ap_]
    
    ap_label = rssi_tag_df["ap_mac_address"].iloc[0]
    f, (ax1, ax2) = plt.subplots(2)
    ax = seaborn.distplot(rssi_tag_df["rssi"],ax=ax1)
    
    acc_plot_df = rssi_acc_tag_df[["acc1x","acc1y","acc1z"]].dropna()
    acc_plot_df.plot(ax = ax2)
    plt.xlabel("Accelerometer Samples")
    plt.ylabel("g (ms$^{-2}$)")
    plt.suptitle("Participant at Grid %d - %s"%(tag_,ap_label))
    plt.tight_layout()

    print("Close plot to continue")
    plt.show()
    plt.close("all")


def plot_room_distribution(rssi_df_,acc_df_, ann_df_,house_o_, room_ = "kitchen",ap_ = 1):
    '''plot a distribution for a specific tag'''
    
  
    #Find tags in room
    room_key = house_o_.findKeyFromDictValue(house_o_.room_names, room_) 
    tags_room = house_o_.room_tags[room_key]
    
    #find groups of tags in ann data
    tag_ann_df = ann_df_[ann_df_["tag"].isin(tags_room)]
    
    
    
    #Match rssi to annotations at tags
    rssi_tag_df = get_closest_to_ann_times(rssi_df_,tag_ann_df,acceptable_delay_ms_=500)
    
    
    #timestamps in rssi_tag_df  in acc_df_
    rssi_acc_tag_df = pandas.merge(rssi_tag_df[["timestamp","rssi"]], acc_df_, on = "timestamp")
    
    rssi_tag_df = rssi_tag_df[rssi_tag_df["ap_id"] == ap_]
    ap_label = rssi_tag_df["ap_mac_address"].iloc[0]
    
    f, (ax1, ax2) = plt.subplots(2)
    ax = seaborn.distplot(rssi_tag_df["rssi"],ax=ax1)

    acc_plot_df = rssi_acc_tag_df[["acc1x","acc1y","acc1z"]].dropna()
    acc_plot_df.plot(ax = ax2)
    #seaborn.tsplot(data=acc_plot_df,ax=ax2)
    plt.xlabel("Accelerometer Samples")
    plt.ylabel("g (ms$^{-2}$)")
    plt.suptitle("Participant in %s  - %s"%(room_,ap_label))
    plt.tight_layout()
    print("Close plot to continue")
    plt.show()
    plt.close("all")
    
    
def plot_room_annotations(rssi_df_,acc_df_, ann_df_,house_o_, room_ = "kitchen"):
    #Find tags in room
    room_key = house_o_.findKeyFromDictValue(house_o_.room_names, room_) 
    tags_room = house_o_.room_tags[room_key]
    
   
    
    #find groups of tags in ann data
    tag_ann_df = ann_df_[ann_df_["tag"].isin(tags_room)]
    tag_ann_df["distance_tag"] =  (tag_ann_df[["tag_coord_x","tag_coord_y"]]-[0.0,0.0]).pow(2).sum(1).pow(0.5)
    mask = (tag_ann_df["distance_tag"] <0.5)
    tag_ann_df = tag_ann_df[mask]
    tag_ann_df = append_house_coords(tag_ann_df, house_o_)
    tag_ann_df.loc[:,'house_coord_x'] *= 100
    tag_ann_df.loc[:,'house_coord_y'] *= 100
    tag_ann_df.loc[:,'house_coord_z'] *= 100
    
    
    
    #===========================================================================
    # print(tag_ann_df.head(5))
    # print(tag_ann_df.tail(5))
    #===========================================================================
    x = tag_ann_df["house_coord_x"].values
    y = tag_ann_df["house_coord_y"].values
    xy = np.vstack([x,y])
    z = scipy.stats.kde.gaussian_kde(xy)(xy)

    fig_arr  = house_o_.plot_tags_aps() 
    floor_of_room = house_o_.findKeyFromDictValue(house_o_.floor_tags, tags_room[0]) 
    fig_floor= fig_arr[floor_of_room-1]
    
    ax = fig_floor.axes[0]
    ax.set_facecolor('#E6E6FA')
    im = ax.scatter(x, y, c=z, s=50, edgecolor='',cmap=matplotlib.cm.magma)
    cb  = fig_floor.colorbar(im)
    #cb.ax.set_yticklabels(['High'])  # horizontal colorbar
    cb.ax.set_ylabel('location density', rotation=270)
    
    
    plt.show()
    print("Close plot to continue")
    plt.close("all")
def append_house_coords(df_, house_o_): 
    
    x_h = []
    y_h = []
    z_h = []
    for ir,row in df_.iterrows():
     
        loc = house_o_.tag_coordinates[int(row["tag"])]
        
        if np.isnan(loc).any():
            print(loc)
    
        x_h.append(loc[0]/100 + row["tag_coord_x"])
        y_h.append(loc[1]/100 + row["tag_coord_y"])
        z_h.append(loc[2]/100 + row["tag_coord_z"])
    
    xyz_df = pandas.DataFrame({
            "house_coord_x": x_h,
            "house_coord_y": y_h,
            "house_coord_z": z_h
            
            })
    df_out = df_.copy()
    df_out.reset_index(drop =True, inplace=True)
    xyz_df.reset_index(drop =True, inplace=True)
    #===========================================================================
    # print(len(xyz_df.index))
    # print(len(df_out.index))
    #===========================================================================
    df_out = pandas.concat([df_out, xyz_df], axis=1)
    
    return(df_out)
def get_closest_to_ann_times(rssi_df_,tag_ann_df_,acceptable_delay_ms_=500):
    times_tag = tag_ann_df_["timestamp"].values
    times_rssi = rssi_df_["timestamp"].values
    tag_inds = []
    acceptable_delay = np.timedelta64(acceptable_delay_ms_, "ms")
    ann_inds = []
    for time in times_tag:
        diffs = np.abs(times_rssi - time)
        min_pos  = np.argmin(diffs)
        time_del =diffs[min_pos]
        #Less than half a second between rssi timestamp and annotation?
        if time_del  < acceptable_delay:
            tag_inds.append(min_pos)
    
    rssi_tag_df = rssi_df_.iloc[tag_inds]
    return rssi_tag_df



def load_annotations(dir_main_):  
    ann_file = os.path.join(dir_main_,"tag_annotations.dat")
    ann_df  =read_csv_2_df(ann_file)
    ann_df["timestamp"] = pandas.to_datetime(ann_df["timestamp"])
    
    
    #===========================================================================
    # print(ann_df.head(5))
    # print(ann_df.tail(5))
    #===========================================================================
    
    return ann_df

    
def load_acc(dir_main_):  
    acc_file = os.path.join(dir_main_,"accelerometer_filtered.dat")
    acc_df  =read_csv_2_df(acc_file)
    acc_df["timestamp"] = pandas.to_datetime(acc_df["timestamp"])
    
    
    #===========================================================================
    # print(ann_df.head(5))
    # print(ann_df.tail(5))
    #===========================================================================
    
    return acc_df


def main():
    
    
    #Get the relative directory of the repo or modify repo_parent_dir
    current_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = os.path.abspath(os.path.split(current_directory)[0])

    c_d = parent_directory
    for i in range(2):
        repo_parent_dir = os.path.split(c_d)[0]
        c_d = repo_parent_dir
        
    print( "Loading from: "+repo_parent_dir)
    #repo_paent_dir = r"F:\residential_wearable_data_repo_with_location_labels"
    
    
    #Examples of loading the data
    living_exp = os.path.join(repo_parent_dir,"house_A","experiments","living_1")
    
    #load all measurement data
    rssi = load_exp_data(living_exp)
    #load unwrapped acc data
    acc = load_acc(living_exp)
    #Load annotations 
    ann = load_annotations(living_exp)


   
    #observe_rssi_data at a tag location
    plot_tag_distribution(rssi,acc,ann,14,ap_=1)
    
    #Create a house object.
    house_dir = os.path.join(repo_parent_dir,"house_A","metadata")
    hO = house.house(house_dir)
    plot_room_annotations(rssi,acc,ann,hO,"living_area")
    #observe_rssi_data at all tags in bedroom
    plot_room_distribution(rssi,acc,ann,hO,"living_area",ap_=1)
    
    #Plot the floor plan of this house
    
    
    hO.plot_tags_aps(os.path.join(parent_directory,"temp_plot","home_A_plots"))
    plt.close("all")
    
    house_dir = os.path.join(repo_parent_dir,"house_B","metadata")
    hO = house.house(house_dir)
    hO.plot_tags_aps(os.path.join(parent_directory,"temp_plot","home_B_plots"))
    plt.close("all")
    house_dir = os.path.join(repo_parent_dir,"house_C","metadata")
    hO = house.house(house_dir)
    hO.plot_tags_aps(os.path.join(parent_directory,"temp_plot","home_C_plots"))
    plt.close("all")
    house_dir = os.path.join(repo_parent_dir,"house_C","metadata")
    hO = house.house(house_dir)
    hO.plot_tags_aps(os.path.join(parent_directory,"temp_plot","home_D_plots"))
    plt.close("all")
if __name__ == '__main__':
    main()