#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:17:48 2018

@author: koenig.g
"""

#################################
# Analysis and correlation of #
# Sea level and current data  #
# By Guillaume Koenig, #
# 14/02/2018 #
# Modified the 15/02/2018 to add#
# Echo, Mean speed and Time_Lag#
# And some loops #
# Modified the 20/02/2018 to #
# Make it cleaner and removing #
# The loops of functions,except#
# When really needed #
# I leave some scripted things#
# As functions because I feel  #
# Like reusing them later #
# Modified the 22/02/2018 for #
# Helping the readability of the#
# Output csv files #
##################################

#*******Packages import**********#

import numpy as np
import matplotlib.pyplot as plt
import scipy
import pandas as pd
import Lib_Data_Analysis # This is my own library
import Lib_Data_Import  # Same thing
import pandas.plotting as pd_plt

#*******Boolean for the script***#
Untide=False
Smoothing=True
First_plot=False
Intra_Station_Correlation=False
Common_Stations_plot=False
Correlation=False
Time_Lag=False


Path='../../FEVRIER_18/16_02/CURRENT_SEALEVEL/2015/DonneesPropres_2015/'# Path to the directory containing the data

Plots_Path='../../FEVRIER_18/16_02/CURRENT_SEALEVEL/2015/Tided/Plots/'# Directory to store data
Table_Path='../../FEVRIER_18/16_02/CURRENT_SEALEVEL/2015/Tided/Tables/'

Time_Shift=15 # This is the maximum number of time step that can be used in the time_lag measurement loop
# Used to increase physical meaning and computational efficiency

# Smoothing parameters
Win_len=60
Win_type='boxcar' # This is equivalent to a rolling mean, without any padding

Nbr_Stat=9 # It's gonna be useful

# Defining our list of Data

Data=[None]*Nbr_Stat

# We use a list for the names and a dictionnary because it will #
# Be more efficient for the loops #

List_Stations=['GDigo','Isie','Nord','Ouarai','PDigo','PtFixe','Recif1','Recif2','Tenia']
Dict_Stations={'GDigo':Data[0],'Isie':Data[1],'Nord':Data[2],'Ouarai':Data[3],'PDigo':Data[4],'PtFixe':Data[5],
               'Recif1':Data[6],'Recif2':Data[7],'Tenia':Data[8]}

# And another list for datanames, it forces us to declare everything

# And so we can get even lazier, we are going to create...
# A LIST ! And a loop on that list,that will be easier and less work
List_Variables=['Depth','Temperature','Surface reef perpendicular Speed','Surface reef parallel Speed',
                'Mean_Echo','U_Mean','V_Mean']

Label_Dictionnary={'Depth':'Hauteur d eau (m)','Temperature':'Temperature (C)',
                   'Surface reef perpendicular Speed':'Vitesse (mm/s)','Surface reef parallel Speed':'Vitesse (mm/s)',
                   'Mean_Echo':'No unit','U_Mean':'Vitesse (mm/s)','V_Mean':'Vitesse (mm/s)'}

Dir_Dictionnary={'Depth':'Niveau','Temperature':'Temperature','Surface reef perpendicular Speed':'U'
                 ,'Surface reef parallel Speed':'V','Mean_Echo':'Echo','U_Mean':'U_Mean','V_Mean':'V_Mean'}
#*********Data loading***********#



for VAR in List_Stations:
    Dict_Stations[VAR]=GDigo=Lib_Data_Import.Import_Data_Cristele(Path+'Temp_'+VAR+'.mat',
                 Path+'VitProj_'+VAR+'.mat',Path+'Echo_'+VAR+'.mat')


#********Data PreTreatment**********#
# In the doubt, we can work with some things to untide our data

if Untide:
  for BAR in List_Stations: 
      for FOO in List_Variables:
       Time=(Dict_Stations[BAR].index.view('int64')//pd.Timedelta(1,unit='m'))/1440. # We must give time inputs in days
       Dict_Stations[BAR][FOO]=Lib_Data_Analysis.Untide_Signal(Time,Dict_Stations[BAR][FOO],Dict_Stations[BAR].Latitude[0])

  Plots_Path='../../16_02/CURRENT_SEALEVEL/2015/Untided/Plots/'# Directory to store data
  Table_Path='../../16_02/CURRENT_SEALEVEL/2015/Untided/Tables/'
  
if Smoothing :
    for BAR in List_Stations: 
      for FOO in List_Variables:
       Dict_Stations[BAR][FOO]=Dict_Stations[BAR][FOO].rolling(window=Win_len,
                    win_type=Win_type).mean()

#******First Visualisation**************#
# Now we do a little plotting and save it #

if First_plot:
  for BAR in List_Stations :
      for FOO in List_Variables:
        Lib_Data_Analysis.Few_Quick_Plots(Dict_Stations[BAR],BAR,FOO,Dir_Dictionnary,
                                          Label_Dictionnary,Plots_Path)
 
#******Data Analysis***************#
# Now we  can start the correlation #
# Analysis. However, there #
# Might be some added complexity #
# When it will come to interstation#
# Comparisons #

if Intra_Station_Correlation:
    for BAR in List_Stations :
     for i in np.arange(0,np.size(List_Variables)):
      for j in np.arange(i,np.size(List_Variables)): 
           Lib_Data_Analysis.Intra_Station_Scatter_Plots(Dict_Stations[BAR],BAR,
                                List_Variables[i],List_Variables[j],Plots_Path)
     
     
# We could still make it into a function, but well, isn't that already well done ?
if Common_Stations_plot:     
 for VAR  in List_Variables:
    #####Removing the mean component##########
    for BAR in List_Stations:
        Dict_Stations[BAR][VAR]-=Dict_Stations[BAR][VAR].mean()
    #### Making an exception in case of temperature ########
    if VAR=='Temperature':
     Dict_Stations['GDigo'][VAR]/=100.
     Dict_Stations['Isie'][VAR]/=100.
     Dict_Stations['Ouarai'][VAR]/=100.
     Dict_Stations['Tenia'][VAR]/=100.
     Dict_Stations['PDigo'][VAR]/=100.
     Dict_Stations['PtFixe'][VAR]/=100.

    ###And now we let the music do the plotting ########
    for BAR in List_Stations :
      if BAR==List_Stations[0]:
          ax1=Dict_Stations[BAR].plot(y=VAR,figsize=[20,10],legend=False)
      else :
          Dict_Stations[BAR].plot(y=VAR,ax=ax1,legend=False)
     
    ax1.set_ylabel(Label_Dictionnary[VAR])
    ax1.legend(List_Stations)
    fig1=ax1.get_figure()
    fig1.savefig(Plots_Path+Dir_Dictionnary[VAR]+'/'+Dir_Dictionnary[VAR]+'_9_Stations.png')
    plt.close(fig1)
    
# Ok, right now we get into the complicated part of the script #
# We're going to do the correlation between different variables of#
# Different time series. And of course, the eventual time lag #
    
#And now we can measure correlations

if Correlation:
 for i in np.arange(0,np.size(List_Variables)):
    for j in np.arange(i,np.size(List_Variables)): 
           #First I open my file with a name related to the computed variables
           Corr=open(Table_Path+'Correlation/'+List_Variables[i]+'_'+List_Variables[j]+'.csv','w')
           Corr.write('Table de correlation \n')
           Corr.write('  ,')
           for BAR in List_Stations:
               #Writing columns headers
              Corr.write(BAR+',')

              for BAR in List_Stations:
                  #Writing line headers
                 Corr.write('\n')
                 Corr.write(BAR+',')
                 for BAR2 in List_Stations:
                 #Compute the correlation while reintepolating
                 # I do that in one line to avoid rewriting on my data
                   Correlation=Dict_Stations[BAR][List_Variables[i]].corr(
                     Dict_Stations[BAR2][List_Variables[j]].reindex(Dict_Stations[BAR].index,method='nearest'))
                 #Saving Data
                 Corr.write(str(Correlation)+',')
        
           Corr.close()
# But now that we have saved all those lines #
# It is clearly time to analyze the time lag #
        
# We're going to stick to the loop for variables and function for station architecture given above #
# To analyze our Time lag. Then we're gonna get the max value of time lag and put it in .csv file #
# In a parallel csv file we are going to put the correlation coefficients of those time lag, just
# To see if they are relevant

if Time_Lag:
 for i in np.arange(0,np.size(List_Variables)):
    for j in np.arange(i,np.size(List_Variables)):
     #Opening the file that will contain the Time lag
     # With the best correlation
     File=open(Table_Path+'Time_Lag/'+
               List_Variables[i]+'_'+List_Variables[j]+'Time_Lag.csv','w')
     #Opening the file that will contain the best correlation
     File2=open(Table_Path+'Time_Lag/'+
                List_Variables[i]+'_'+List_Variables[j]+'Time_Lag_Correlation.csv','w')
     
     # Writing a nice intro to our files
     File.write('Lag time in minutes\n')
     File2.write('Correlation coefficient ( with the time lag of the associatied csv file)\n')
                 
     
     # We write the stations name#
     for BAR in List_Stations:
      #Writing the column header
      File.write(BAR+',')
      #Same thing for the second file

      File2.write(BAR+',')
     
     File.write('\n')
     File2.write('\n')
      
     for BAR in List_Stations :
         #Writing the row headers
         File.write('\n')
         File.write(BAR+',')
         #Same thing for the second file   
         File2.write('\n')
         File2.write(BAR+',')
         for BAR2 in List_Stations :
             #We call the  function to get the correlation as a function
             # Of time lag and if wanted, make plots of it
             print(i,j,BAR,BAR2)
             Cross_Corr=Lib_Data_Analysis.Cross_Correlation_Time_Shifted(Plots_Path+'Time_Lag/',
              List_Variables[i],List_Variables[j],BAR,BAR2,Dict_Stations,False,Time_Shift)
             
             # Wr write the Time lag with the best correlation coefficient
             File.write(str(Cross_Corr.Time_Lag[Cross_Corr.Corr_Coeff.idxmax()]/60.)+',')
             # We write the corresponding correlation coefficient
             File2.write(str(Cross_Corr.Corr_Coeff.max())+',')
     File.close()
     File2.close()


# End of script #

