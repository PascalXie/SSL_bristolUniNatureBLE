#include <fstream>
#include <iostream>
#include <string>
#include <cmath>

#include "Histogram.hh"
#include "Histogram2D.hh"

using namespace std;

int NumberAnchors = 0;
int NumberNodes = 0;

vector<int> AP_IDs, Target_IDs, Wearable_IDs;
vector<double> RSSIs;
vector<double> axs, ays, azs, xxs, xys, xzs;
vector<double> time_deferences, distances_toTag;

bool ImportObservation(string filename);
void Distance_target_tag();
void hist2D_target_x_y();
void hist2D_apID_tagID();

string GetAPRoom(int AP_ID);
string GetTagRoom(int Tag_ID);

int main()
{
	cout<<"Hello "<<endl;

	//
	ImportObservation("../../data_step1_rssi_ap.txt");

	//
	// x axis : distance
	// y axis : rssi 
	int bin[2] = {50,50};
	double min[2] = {0,-120};
	double max[2] = {10,-20};

	Histogram2D *rssi2d = new Histogram2D("RSSI",bin[0],min[0],max[0],bin[1],min[1],max[1]);
	for(int i=0;i<AP_IDs.size();i++)
	{
		int ID = i;
		double distance_ToAP =			(axs[ID]-xxs[ID])*(axs[ID]-xxs[ID]);
		distance_ToAP = distance_ToAP + (ays[ID]-xys[ID])*(ays[ID]-xys[ID]);
		distance_ToAP = distance_ToAP + (azs[ID]-xzs[ID])*(azs[ID]-xzs[ID]);
		distance_ToAP = sqrt(distance_ToAP);

		if(distances_toTag[ID]<0.3)
		if(AP_IDs[ID]>=1&&AP_IDs[ID]<=5)
		//if(GetAPRoom(AP_IDs[ID])=="living_room")
		//if(GetTagRoom(Target_IDs[ID])=="living_room")
		{
			// debug
			//if(RSSIs[ID]>-65&&RSSIs[ID]<-50)
			if(distances_toTag[ID]>0)
				rssi2d->Fill(distance_ToAP,RSSIs[ID],distances_toTag[ID]);
			//cout<<"ID "<<ID<<", AP_IDs[ID] "<<AP_IDs[ID]<<", Target_IDs[ID] "<<Target_IDs[ID]<<", RSSI "<<RSSIs[ID]<<", distance_ToAP "<<distance_ToAP<<", Wearable_IDs[ID] "<<Wearable_IDs[ID]<<endl;
		}


		/*
		// debug
		if(i==100) break;
		cout<<"ID "<<ID<<", distance_ToAP "<<distance_ToAP<<endl;
		*/
	}


	// write date into a file
	ofstream write("data_step3_rssi_distance.txt");
	for(int i=0;i<bin[0];i++)
	for(int j=0;j<bin[1];j++)
	{
		int distID = i;
		int rssiID = j;
		double dist = 0;
		double rssi = 0;
		rssi2d->GetBinCentor2D(distID,rssiID,dist,rssi);
		double content = rssi2d->GetBinContent(distID,rssiID);
		//cout<<"distID "<<distID<<", rssiID "<<rssiID<<", content "<<content<<endl;
		write<<dist<<" "<<rssi<<" "<<content<<endl;
	}
	write.close();

	//
	Distance_target_tag();
	//
	hist2D_target_x_y();
	//
	hist2D_apID_tagID();

	return 1;
}

void Distance_target_tag()
{
	//
	// distance to 
	//
	int bin = 100;
	double min = 0;
	double max = 2;
	Histogram *hDist = new Histogram("Distance",bin,min,max);
	for(int i=0;i<AP_IDs.size();i++)
	{
		int ID = i;
		hDist->Fill(distances_toTag[ID],1);
	}
	// write date into a file
	ofstream write2("data_step3_distance_target_tag.txt");
	for(int i=0;i<bin;i++)
	{
		int ID = i;
		double dist = hDist->GetBinCenter(ID);
		double content = hDist->GetBinContent(ID);
		write2<<dist<<" "<<content<<endl;
	}
	write2.close();
}

void hist2D_target_x_y()
{
	//
	// x axis : x
	// y axis : y
	int    bin[2] = {200,200};
	double min[2] = {0,0};
	double max[2] = {10,5};

	Histogram2D *target = new Histogram2D("target",bin[0],min[0],max[0],bin[1],min[1],max[1]);

	for(int i=0;i<AP_IDs.size();i++)
	{
		int ID = i;
		target->Fill(xxs[ID],xys[ID],1);
	}

	// write date into a file
	ofstream write("data_step3_target_x_y.txt");
	for(int i=0;i<bin[0];i++)
	for(int j=0;j<bin[1];j++)
	{
		int xID = i;
		int yID = j;
		double x = 0;
		double y = 0;
		target->GetBinCentor2D(xID,yID,x,y);
		double content = target->GetBinContent(xID,yID);
		write<<x<<" "<<y<<" "<<content<<endl;
	}
	write.close();
}

void hist2D_apID_tagID()
{
	//
	// x axis : APID
	// y axis : TAGID
	int    bin[2] = {13,85};
	double min[2] = {-0.5,-0.5};
	double max[2] = {12.5,84.5};

	Histogram2D *hid = new Histogram2D("id",bin[0],min[0],max[0],bin[1],min[1],max[1]);
	for(int i=0;i<AP_IDs.size();i++)
	{
		int ID = i;

		// debug
		if(RSSIs[ID]>-65&&RSSIs[ID]<-50)
			hid->Fill(AP_IDs[ID],Target_IDs[ID],1);

		//
		//hid->Fill(AP_IDs[ID],Target_IDs[ID],1);
	}

	// write date into a file
	ofstream write("data_step3_apID_tagID.txt");
	for(int i=0;i<bin[0];i++)
	for(int j=0;j<bin[1];j++)
	{
		int xID = i;
		int yID = j;
		double x = 0;
		double y = 0;
		hid->GetBinCentor2D(xID,yID,x,y);
		double content = hid->GetBinContent(xID,yID);
		write<<x<<" "<<y<<" "<<content<<endl;
	}
	write.close();
}

bool ImportObservation(string filename)
{
	ifstream file(filename.c_str());

	if(file.fail())
	{
		cout<<"Can not find the file \" "<<filename<<" \""<<endl;
		return 0;
	}

	string temp;
	string time_ap, time_targe;

	int ID = 0;
	int AP_ID = 0;
	int Tar_ID = 0;
	int Wearable_ID = 0;
	double rssi = 0; 
	double ax = 0; 
	double ay = 0; 
	double az = 0;
	double xx = 0;
	double xy = 0;
	double xz = 0;
	double time_deference = 0; // time difference, milliseconds
	double distance = 0; // distance between tag and target

	while(!file.eof())
	{
		file>>ID>>AP_ID>>rssi>>ax>>ay>>az>>Tar_ID>>xx>>xy>>xz>>time_deference>>distance>>Wearable_ID;

		if(file.eof()) break;

		//cout<<"AP_ID "<<AP_ID<<", rssi "<<rssi<<", ax "<<ax<<", ay "<<ay<<", az "<<az<<", xx "<<xx<<", xy "<<xy<<", xz "<<xz<<"; distance "<<distance<<endl;

		AP_IDs.push_back(AP_ID);
		RSSIs.push_back(rssi);
		axs.push_back(ax);
		ays.push_back(ay);
		azs.push_back(az);
		Target_IDs.push_back(Tar_ID);
		xxs.push_back(xx);
		xys.push_back(xy);
		xzs.push_back(xz);
		time_deferences.push_back(time_deference);
		distances_toTag.push_back(distance);
		Wearable_IDs.push_back(Wearable_ID);
	}

	file.close();

	return 1;
}

string GetAPRoom(int AP_ID)
{
	if(AP_ID==1)  return "hallway_lower";
	if(AP_ID==2)  return "living_room"  ;
	if(AP_ID==3)  return "dining_room"  ;
	if(AP_ID==4)  return "dining_room"  ;
	if(AP_ID==5)  return "kitchen"      ;
	if(AP_ID==6)  return "kitchen"      ;
	if(AP_ID==7)  return "bathroom"     ;
	if(AP_ID==8)  return "hallway_upper";
	if(AP_ID==9)  return "bedroom_2"    ;
	if(AP_ID==10) return "bedroom_1";
	if(AP_ID==11) return "toilet"   ;

	return "NONE_AP";
}

string GetTagRoom(int Tag_ID)
{
	if(Tag_ID>=27&&Tag_ID<=36)	return "dining_room";
	if(Tag_ID==79)				return "dining_room";

	if(Tag_ID>=16&&Tag_ID<=26)	return "living_room";
	if(Tag_ID==80)				return "living_room";

	return "NONE_Tag";
}
