#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 14:18:49 2018

@author: koenig.g
"""

#######################################
# Library of functions used for corr- #
# elations analysis, made by Guillaume#
# The 15/02/2018                      #
# This is mostly based on Panda       #
#######################################

#******Import Packages****************#
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Lib_Data_Analysis import * # This is my own library
import utide # To treat tides


# Now we're going to use the Utide package so that  we can treat our tides
# Components, yey !  Input time must be in days          
def Untide_Signal(Time,Signal,Lat):
    #First we determine the tide,
    Coeff=utide.solve(Time,Signal,lat=Lat,nodal=True,trend=True,method='robust',conf_int='linear',Rayleigh_min=.95)
    # And now we smoothly detide it
    Reconstructed_Signal=utide.reconstruct(Time,Coeff)
    
    return Signal-Reconstructed_Signal['h'] 

# Something to quickly plot all the variables in a Dataframe#
# For that we need a list of variables, a dictionnary of repertory
# To store the plots, and a dictionnary of labels

def Few_Quick_Plots(Dataframe,Name,Variable,Dict_Dir,Label_Dict,Path):
    # We're going to use panda for plotting because the plots are nice #
    # Then we will transfer it to matplotlib for saving it #
      ax=Dataframe.plot(y=Variable,legend=False,figsize=[20,10])
      ax.set_ylabel(Label_Dict[Variable])
      ax.set_title(Name)
      fig=ax.get_figure()
      fig.savefig(Path+Dict_Dir[Variable]+'/'+Name+'.png')  
      plt.close(fig)
      return

 # A function that is used to scatter data of two variables
 # Of the same station, so that we have an idea of the
 # existing correlation. We may think of adding a part for
 # Computing a linear regression and computing the chi-squared
def Intra_Station_Scatter_Plots(Dataframe,Name,Var1,Var2,Path):
    
     # We're going to use panda once again #
     # To do the intra station scatter plots #
     # However for the real correlation analysis #
     # A little smoothing or detiding could be interesting #
     ax=Dataframe.plot.scatter(x=Var1,y=Var2,figsize=[20,10])
     ax.set_title(Name)
     fig=ax.get_figure()
     fig.savefig(Path+Name+Var1+'_'+Var2+'.png')
     plt.close(fig)
     return

#This is a function that compute the correlations of two variables in two 
# Different stations for different time shift. It returns the DataFrame of 
# Time shift and correlation so that we can look for the max in them. It 
# has an optionnal flag 'plot' to plot or not data.
def Cross_Correlation_Time_Shifted(Name,Var1,Var2,Stat1,Stat2,Dict_Stat,plot,Max_Lag):
                
           # We initialize the DataFrame that will be used for plotting Data#
           # We define the sampling period
            Time_Lag=pd.Timedelta(Dict_Stat[Stat1].index[1]-
                    Dict_Stat[Stat1].index[0]).seconds
           # We initialize our return dataframe
            Cross_Corr=pd.DataFrame({'Time_Lag':Time_Lag,'Corr_Coeff':np.zeros(Max_Lag)})
           # We set the first time lag as 0 
            Cross_Corr.Time_Lag[0]=0
            for k in range(1,Max_Lag):
                # And we add the last value of the time lag to have the total time lag
                Cross_Corr.Time_Lag[k]+=Cross_Corr.Time_Lag[k-1]
                print(Cross_Corr.Time_Lag[k])
                
                Cross_Corr.Corr_Coeff[k]=Dict_Stat[Stat1][Var1].corr(Dict_Stat[Stat2][Var2].reindex(
                        Dict_Stat[Stat1].index,method='pad').shift(k))
            if plot:    
             # And now we plot just to see #
             ax=Cross_Corr.plot(x='Time_Lag',y='Corr_Coeff',figsize=[20,10])
             fig=ax.get_figure()
             fig.savefig(Path+'_'+Var1+'_'+Var2+'_'+Stat1+'_'+Stat2+'.png')
             plt.close(fig)
            # And we're done #
            return Cross_Corr
 
