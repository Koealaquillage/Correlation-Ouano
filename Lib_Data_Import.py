#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 09:17:34 2018

@author: koenig.g
"""

############################################
# External library to contain the functions#
# Of data import and pre-treatment         #
# By Guillaume Koenig, the 16/02/2018      #
############################################

#******Packages import*********************#

import numpy as np
import scipy
import pandas as pd

# Routine used to import pretreated Cristele's 
# Data from the Ouano lagoon

#**********************************#
# We have to precise the data #
# formatting #
#**********************************#

# So in Echo*** We have different #
# Data : Temps, P,P_Adcp,echo #
# Their structures are different #
# To access any of these, use #
# Echo***['Data'], then you can #
# Access the arrays of Data with #
# Echo***['Data'][0,0][i][j]#
# [i][j] are data depending #
# For example, in P_Adcp,i#
# determine if you want to see  #
# The depth of the Adcp cell or #
# its distance to the bottom #
# While j is the index of the #
# Measurement, which is related #
# To the time index #
#################################


def Import_Data_Cristele(Temp_Data,Speed_Data,Echo_Data) :
    
    # We load data from the Matlab files "
    Speed=scipy.io.loadmat(Speed_Data)
    Temp=scipy.io.loadmat(Temp_Data)
    Echo=scipy.io.loadmat(Echo_Data)
    # Now we format the time, so that it is easier to read #
    
    df = pd.DataFrame({'year':Speed['Temps']['year'][0][0][:,0],
                  'month':Speed['Temps']['month'][0][0][:,0],
                   'day':Speed['Temps']['day'][0][0][:,0],
                    'hour':Speed['Temps']['hour'][0][0][:,0],
                    'minute':Speed['Temps']['minute'][0][0][:,0],
                     'second':Speed['Temps']['year'][0][0][:,0]})
    
    # It seems that the measurement cells of the ADCP have the same
    # Amplitude, that is going to help a lot
    # Because we do not have the latest numpy version, we have to use 
    # A scipy function
    
    U_Mean=scipy.nanmean(Speed['vitesse'][0][0][0],axis=1)
    V_Mean=scipy.nanmean(Speed['vitesse'][0][0][1],axis=1)
    Mean_Echo=scipy.nanmean(Echo['echo'],axis=1) # Ok, may be it does not take into account possible vertical variations
    
    # And we prepare the final array
    
    return pd.DataFrame({'Latitude' : Speed['P'][0,0][0][0][0],
                          'Longitude' : Speed['P'][0,0][1][0][0],
                          'Temperature':Temp['temperature'][:,0],
                          'Depth' : Speed['P'][0,0][2][:,0],
                          'Surface reef perpendicular Speed':Speed['vitesse'][0,0][0][:,0],
                          'Surface reef parallel Speed':Speed['vitesse'][0,0][1][:,0],
                          'Deviation from the North':Speed['tetaMoy'][0,0],
                          'U_Mean':U_Mean,
                          'V_Mean':V_Mean,
                          'Mean_Echo':Mean_Echo
                          },index=pd.to_datetime(df))
    
    
# We're gonna use and independant dataframe for the swell 
# Because it is highly unlikely that it has the same 
# Time index as other data (NR: as or like ?)
def Import_Data_Swell(Swell_Data):
    
    # Loading the .mat file
    Swell=scipy.io.loadmat(Swell_Data)
    
    
    # Now we're going to create the dataframe
    # We commented those that are empty
    
    return pd.DataFrame({'Direction':Swell['Dir'][:,0],
                        # 'Th0':Swell['Th0'],
                        # 'Th1':Swell['Th1'],
                        # 'Dp':Swell['Dp'],
                         'Hs':Swell['Hs'][:,0],
                        # 'Hs0':Swell['Hs0'],
                        # 'Hs1':Swell['Hs1'],
                         'Tp':Swell['Tp'][:,0]},index=Swell['T_Hs'][:,0])#,
                        # 'Tp0':Swell['Tp0'],
                         #'Tp0':Swell['Tp1'],})
                         #'T02':Swell['T02'][:,0]
    