# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:18:10 2020

@author: kocok
"""

import numpy as np
import pandas as pd
import netCDF4 
import itertools
import statistics
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import colors
pd.set_option('display.max_columns',30)
pd.set_option('display.width', 1000)
###############################
# get netcdf4 dataset as f
f = netCDF4.Dataset(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\GRIDCRO2D_2017-01-01.nc") 
DF=pd.read_csv(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\tabulka_surova_NO2_2017.csv",delimiter=',')
#########
#get dictonary, which contain arrays of different supplementary quantities of shape (241,172), arrays are 2D
dic_polia={}
for i in list(f.variables.keys()):
    if i not in ['MSFX2','TFLAG','LWMASK', 'LAT', 'LON']: 
    #if i not in ['MSFX2','TFLAG','LWMASK', 'LAT', 'LON','LUFRAC_11','LUFRAC_07']:
    #if i in ['HT']:
       dic_polia[i]=np.array(f.variables[i][0,0,:,:])

dic_polia['TOTALNO2']=np.float32(np.load(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\total_NO2.npy"))
dic_polia['HUSTOTA_OBYVATELSTVA']=np.float32(np.load(r"C:\Users\kocok\Desktop\Bakalarska praca hlavne programy\inputs\HUSTOTA_OBYVATELSTVA.npy"))

########
# get disctonary, which contains LAT an LON arrays of shape (241,172), arrays are 2D
dic_latlon={}
for i in list(f.variables.keys()):
    if i in ['LAT','LON']:
       dic_latlon[i]=np.array(f.variables[i][0,0,:,:])
################################################################
def getclosest_ij(lats,lons,latpt,lonpt):
    # find squared distance of every point on grid
    dist_sq = (lats-latpt)**2 + (lons-lonpt)**2  
    # 1D index of minimum dist_sq element
    minindex_flattened = dist_sq.argmin()    
    # Get 2D index for latvals and lonvals arrays from 1D index
    return np.unravel_index(minindex_flattened, lats.shape)
################################################################   
for key,value in dic_polia.items():
    zoznam_vsetky=[]
    zoznam_UB_RB_SB=[]
    zoznam_UT_RB_SB=[]
    zoznam_UB_UT_SB=[]
    zoznam_UB_UT_RB=[]
    zoznam_UB=[]
    zoznam_UT=[]
    zoznam_RB=[]
    for n in range (0,4):
            z=[]
            for k, row in DF.iterrows():
                ix, iy = getclosest_ij(dic_latlon['LAT'],dic_latlon['LON'],row['lat_x'],row['lon_x'])
                listname=[]
            
                i=list(range(ix-n,ix+n+1,1))
                j=list(range(iy-n,iy+n+1,1))
                for each in list(itertools.product(i,j)):
                    listname.append(value[each])
                pd.Series(listname).fillna(0).tolist()
                upraveny_list=pd.Series(listname,dtype=object).fillna(0).tolist()
                z.append(sum(upraveny_list))
        
#            DF[key]=z
#            korelacia_vsetky=DF['NO2'].corr(DF[key])
#            zoznam_vsetky.append(korelacia_vsetky)
#            DF_filteredUT = DF[(DF.typ != 'UT')]
#            korelacia_UB_RB_SB=DF_filteredUT['NO2'].corr(DF_filteredUT[key])
#            zoznam_UB_RB_SB.append(korelacia_UB_RB_SB)
#            DF_filteredUB = DF[(DF.typ != 'UB')]
#            korelacia_UT_RB_SB=DF_filteredUB['NO2'].corr(DF_filteredUB[key])
#            zoznam_UT_RB_SB.append(korelacia_UT_RB_SB)
#            DF_filteredRB = DF[(DF.typ != 'RB')]
#            korelacia_UB_UT_SB=DF_filteredRB['NO2'].corr(DF_filteredRB[key])
#            zoznam_UB_UT_SB.append(korelacia_UB_UT_SB)
#            DF_filteredSB = DF[(DF.typ != 'SB')]
#            korelacia_UB_UT_RB=DF_filteredSB['NO2'].corr(DF_filteredSB[key])
#            zoznam_UB_UT_RB.append(korelacia_UB_UT_RB)
#            DF_filter = DF[(DF.typ != 'SB')& (DF.typ != 'RB')& (DF.typ != 'UT')]
#            korelacia_UB = DF_filter['NO2'].corr(DF_filter[key])
#            zoznam_UB.append(korelacia_UB)
#            DF_filter1 = DF[(DF.typ != 'SB')& (DF.typ != 'RB')& (DF.typ != 'UB')]
#            korelacia_UT=DF_filter1['NO2'].corr(DF_filter1[key])
#            zoznam_UT.append(korelacia_UT)
#            DF_filter2 = DF[(DF.typ != 'SB')& (DF.typ != 'UT')& (DF.typ != 'UB')]
#            korelacia_RB=DF_filter2['NO2'].corr(DF_filter2[key])
#            zoznam_RB.append(korelacia_RB)
            
            DF[key]=z
            korelacia_vsetky=np.log(DF['NO2']).corr(DF[key])
            zoznam_vsetky.append(korelacia_vsetky)
            DF_filteredUT = DF[(DF.typ != 'UT')]
            korelacia_UB_RB_SB=np.log(DF_filteredUT['NO2']).corr(DF_filteredUT[key])
            zoznam_UB_RB_SB.append(korelacia_UB_RB_SB)
            DF_filteredUB = DF[(DF.typ != 'UB')]
            korelacia_UT_RB_SB=np.log(DF_filteredUB['NO2']).corr(DF_filteredUB[key])
            zoznam_UT_RB_SB.append(korelacia_UT_RB_SB)
            DF_filteredRB = DF[(DF.typ != 'RB')]
            korelacia_UB_UT_SB=np.log(DF_filteredRB['NO2']).corr(DF_filteredRB[key])
            zoznam_UB_UT_SB.append(korelacia_UB_UT_SB)
            DF_filteredSB = DF[(DF.typ != 'SB')]
            korelacia_UB_UT_RB=np.log(DF_filteredSB['NO2']).corr(DF_filteredSB[key])
            zoznam_UB_UT_RB.append(korelacia_UB_UT_RB)
            DF_filter = DF[(DF.typ != 'SB')& (DF.typ != 'RB')& (DF.typ != 'UT')]
            korelacia_UB = np.log(DF_filter['NO2']).corr(DF_filter[key])
            zoznam_UB.append(korelacia_UB)
            DF_filter1 = DF[(DF.typ != 'SB')& (DF.typ != 'RB')& (DF.typ != 'UB')]
            korelacia_UT=np.log(DF_filter1['NO2']).corr(DF_filter1[key])
            zoznam_UT.append(korelacia_UT)
            DF_filter2 = DF[(DF.typ != 'SB')& (DF.typ != 'UT')& (DF.typ != 'UB')]
            korelacia_RB=np.log(DF_filter2['NO2']).corr(DF_filter2[key])
            zoznam_RB.append(korelacia_RB)  
            
            
            
            
            




################################################################################################
#OBLAST KORELACIE (GRID BOD ALEBO VIAC)       
################################################################################################        
    plocha=[]
    for oblast in np.arange(1.5,13.5,3):
            plocha.append(oblast*oblast)
    tabulka=pd.DataFrame({'oblast km^2': plocha,'Vsetky':zoznam_vsetky, 'UB_RB_SB':zoznam_UB_RB_SB, 'UT_RB_SB':zoznam_UT_RB_SB,'UB_UT_SB':zoznam_UB_UT_SB, 'UB_UT_RB':zoznam_UB_UT_RB,'zoznam_UB':zoznam_UB, 'zoznam_UT':zoznam_UT,'zoznam_RB':zoznam_RB})
    
    tabulka_zaokruhlena=tabulka.round({'Vsetky': 3, 'UB_RB_SB': 3,'UT_RB_SB':3,'UB_UT_SB':3,'UB_UT_RB':3,'zoznam_UB':3,'zoznam_UT':3,'zoznam_RB':3})
    #mala tabulka 
    primerna_korelacia_vsetky=statistics.mean(tabulka['Vsetky'])
    primerna_korelacia_UB_RB_SB=statistics.mean(tabulka['UB_RB_SB'])
    primerna_korelacia_UT_RB_SB=statistics.mean(tabulka['UT_RB_SB'])
    primerna_korelacia_UB_UT_SB=statistics.mean(tabulka['UB_UT_SB'])
    primerna_korelacia_UB_UT_RB=statistics.mean(tabulka['UB_UT_RB'])
    primerna_korelacia_zoznam_UB=statistics.mean(tabulka['zoznam_UB'])
    primerna_korelacia_zoznam_UT=statistics.mean(tabulka['zoznam_UT'])
    primerna_korelacia_zoznam_RB=statistics.mean(tabulka['zoznam_RB'])
    
    # initialize list of lists 
    data = [['Vsetky',primerna_korelacia_vsetky ], ['UB_RB_SB', primerna_korelacia_UB_RB_SB], ['UT_RB_SB', primerna_korelacia_UT_RB_SB],['UB_UT_SB', primerna_korelacia_UB_UT_SB], ['UB_UT_RB', primerna_korelacia_UB_UT_RB],['zoznam_UB', primerna_korelacia_zoznam_UB], ['zoznam_UT', primerna_korelacia_zoznam_UT],['zoznam_RB', primerna_korelacia_zoznam_RB]]  
    # Create the pandas DataFrame 
    df = pd.DataFrame(data, columns = ['Zahrnuté typy staníc ', 'Priemerná korelácia'])   
   
    print("##################################")
    print(key)
    print("##################################")
    print(tabulka_zaokruhlena)
    print(df)
    dfzaokruhlene=df.round({'Priemerná korelácia': 3})
    print(dfzaokruhlene)
    print("##################################")
    plt.rcParams['figure.figsize'] =20,7
    meridians = np.arange(16.,35.,1.)
    pararels = np.arange(46.,50.,1.)
    mapb=Basemap(projection='lcc',lat_1=48,lat_2=48,lat_0=48.7,lon_0=19.7,width=500000,height=300000,resolution='i')
    mapb.drawcountries()
    mapb.pcolormesh(dic_latlon['LON'],dic_latlon['LAT'],value,cmap=plt.cm.jet,latlon=True) 
    # drawing locations of stations in maps
    x,y = mapb(list(DF['lon_x']), list(DF['lat_x']))
    mapb.plot(x, y, 'ro', markersize=2)
    plt.colorbar(label= key)
    plt.title(key,fontsize=15)
    plt.show()       
          
          

