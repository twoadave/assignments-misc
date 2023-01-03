# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 14:42:22 2022

@author: David Gayowsky

Try to keep functions to ~70 lines max... otherwise pull out and inherit.
"""

#Dice rolling program.

#e. Write a program which calculates the sample mean, median, mode, and 
#standard deviation for an arbitrary list of data. 
#Note: do not use premade functions, write code cleanly, etc.

#f. Use your program to calculate the mean, median, mode, and standard dev.
#for your results, as well as the results from the first class.

#g. Build a histogram of your results, as well as one for the results from 
#the whole class. Normalize the histograms such that the total area under the 
#histograms is unity.

#h. Comment on the values you obtained in f., as well as on the two 
#histograms. Compare them to each other and to the values you calculated
#in d. and the histogram you created in c.

#######################################################################

#Import all of the wonderful things we like and need to manage data and make plots.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pds
import pathlib 
import math
from scipy import stats

#######################################################################

#Now we write functions!

#Write function to read csv file of data into a list, taking file path as input.
#NOTE: This function assumes the data file is in the same folder as THIS FILE.
def import_data(filename):
    #Find the folder we're working in...
    data_file_path = pathlib.Path(__file__)
    #Make sure we're grabbing the correct file...
    filepath = data_file_path.with_name(filename)
    #Create dataframe of csv data.
    filedata = pds.read_csv(filepath, header = None) 
    #Converts dataframe data to list so we can work with numbers.
    filedata_list = filedata[0].tolist() 
    #Return list of our data.
    return filedata_list

#Write function to calculate sample mean, taking list of data as input.
def sample_mean(list_data):
    #Sample mean: summation of all data, divided by number of data points.
    
    #Firstly, find the number of measurements.
    number_measurements = len(list_data)
    
    #Sigh.. have to write our own summation function. Fine.
    #Declare a sumtotal value which will be the total value of our summation.
    sumtotal = 0
    
    for i in range(number_measurements):
        #For each value in the list of data, add it to a sumtotal.
        addval = list_data[i]
        sumtotal = sumtotal + addval
        
    #Now divide by number of measurements...
    list_sample_mean = sumtotal/number_measurements
    
    #Return mean of data list.
    return list_sample_mean

#Write function to sort our list of given values.
def sort_data(list_data):
    
    #First, we don't want to actually modify our imported list, so we're going to make a dupe.
    list_data_tosort = list_data.copy()
    
    #Next, define a "temp variable" to store a value.
    temp_dataval = 0
    
    #Want to iterate over each list value, compare it to all others, and swap places
    #if compared value is smaller than value at lower index in array.
    #Note this does some wacky stuff and rearranges half the list before getting it in order...
    for i in range(len(list_data_tosort)):
        for j in range(len(list_data_tosort)):
            
            #If value at spot i is less than value at spot j;
            if list_data_tosort[i] < list_data_tosort[j]:
                #Assign i val to temp variable;
                temp_dataval = list_data_tosort[i]
                #Assign j val to spot at i;
                list_data_tosort[i] = list_data_tosort[j]
                #Assign temp val = i val to spot j;
                list_data_tosort[j] = temp_dataval
                #Now we've swapped the two values.
            
            #If the values are the same, do nothing.
            elif list_data_tosort[i] == list_data_tosort[j]:
                pass
    
    #Return the sorted list.
    return list_data_tosort

#Write function to calculate sample median, taking list of data as input.
def sample_median(list_data):
    #Sample median: median value of all data, "middle" value so to speak.
    #Need to do this with no sort, max, or min. Well we have our sorting function above, so we can use that.
    
    #Firstly, sort our data.
    list_data_sorted = sort_data(list_data)
    
    #Now we're going to pick the value out of the middle.
    #If the number of elements in the list is even, will be 0 when mod 2...
    if (len(list_data_sorted) % 2) == 0:
        #Need to find the two middle array values and take the average of them.
        #Find exact middle: note we need to subtract 1 from len because arrays index from 0! 
        middle_array_index = (len(list_data_sorted)-1)/2
        
        #Take the nearest integer indices next to the exact middle index:
        middle_index_low = math.floor(middle_array_index)
        middle_index_upper = math.ceil(middle_array_index)
        
        #Now find the exact median by averaging the values at these two indices:
        median_val = (list_data_sorted[middle_index_low] + list_data_sorted[middle_index_upper])/2
    
    #Now consider the case where we have only one middle index:
    else: 
        #Repeat from previous, just don't need to average values this time.
        middle_array_index = (len(list_data_sorted)-1)/2
        
        #Make sure this is an integer...
        middle_array_index = int(middle_array_index)
        
        #Now calculate the median value.
        median_val = list_data_sorted[middle_array_index]
    
    #Return median value.
    return median_val
    
#Write function to calculate sample mode, taking list of data as input.
def sample_mode(list_data):
    #Sample mode: most common value. 
    #Note: a given data set may have more than one mode!
    #Want to count number of each value, i.e. find frequency of each value in array.
    
    #Make an empty values array and frequency array to store each value and the
    #number of times it appears in our list of data.
    values_array = []
    frequency_array = []
    
    #Firstly, sort our data.
    list_data_sorted = sort_data(list_data)
    
    #Iterate over each value - if it's not in our list of values, add it, otherwise pass.
    for i in range(len(list_data_sorted)):
        if list_data_sorted[i] in values_array:
            pass
        else:
            values_array.append(list_data_sorted[i])
            #Declare number of times this data appears in our list.
            value_frequency = 0
            #Check all other array values - count the number of times the value at 
            #[i] appears in our list of data.
            for j in range(len(list_data_sorted)):
                if list_data_sorted[i] == list_data_sorted[j]:
                    #Every time we see this value, we add 1 to the value frequency number.
                    value_frequency = value_frequency + 1
                else:
                    pass
            #Add the number of times the value appears to the values array.
            frequency_array.append(value_frequency)
    
    #Now we need to find the most common value(s)... sort a copy of our list of frequency values.
    #Pop the top value off, which in the sorted list, is just the last value.
    #This is just the number of times the mode(s) appear.
    frequency_array_sorted = sort_data(frequency_array)
    largestfreq = frequency_array_sorted[len(frequency_array_sorted)-1]
    
    #Declare empty array of mode values - recall we may have more than one mode.
    mode_values = []
    
    #Now we go through and say any value which has the most common frequency
    #ie. appears the largest number of times is a mode.
    #Note that the indices of the frequency array and values array correspond 
    #directly - so we can just iterate through the frequency array, and pull
    #values out of the values array. Clever me! :) 
    for i in range(len(frequency_array)):
        if frequency_array[i] == largestfreq:
            mode_values.append(values_array[i])
        else:
            pass
    
    #Return all possible modes as an array.
    return mode_values
            
#Write function to calculate sample stdev, taking list of data as input.
def sample_stdev(list_data):
    #Sample stdev is the square root of the sample variance. 
    #Sample variance: sum over (all values - sample mean)**2, mult. by 1/(no of measurements - 1)
    #Okay, not too bad. Basically do a similar thing to our mean.
    
    #Again, take number of measurements.
    number_measurements = len(list_data)
    
    #Declare a sumtotal value which will be the total value of our summation.
    sumtotal = 0
    
    #Now also calculate the sample mean:
    smean = sample_mean(list_data)
    
    for i in range(number_measurements):
        #For each value in the list of data, subtract mean, square it, add it to a sumtotal.
        addval = (list_data[i] - smean)**2
        sumtotal = sumtotal + addval
        
    #Now divide by number of measurements - 1...
    list_sample_stdev = sumtotal/(number_measurements - 1)
    #And take the square root...
    list_sample_stdev = math.sqrt(list_sample_stdev)
    
    #Return sample stdev.
    return list_sample_stdev

#Write a function to plot normalized histogram, taking list of data as input.
def make_histogram(list_data, datasettitle):
    
    #Gonna go ahead and assume we can't use plt.hist... oh well. 
    #Anyway. 
    #Redo a similar thing to mode: get values and frequencies, divide frequencies 
    #by total number of measurements to get the height of the bar, and make a bar graph.
    
    #Make an empty values array and frequency array to store each value and the
    #number of times it appears in our list of data.
    values_array = []
    frequency_array = []
    
    #Firstly, sort our data.
    list_data_sorted = sort_data(list_data)
    
    #Iterate over each value - if it's not in our list of values, add it, otherwise pass.
    for i in range(len(list_data_sorted)):
        if list_data_sorted[i] in values_array:
            pass
        else:
            values_array.append(list_data_sorted[i])
            #Declare number of times this data appears in our list.
            value_frequency = 0
            #Check all other array values - count the number of times the value at 
            #[i] appears in our list of data.
            for j in range(len(list_data_sorted)):
                if list_data_sorted[i] == list_data_sorted[j]:
                    #Every time we see this value, we add 1 to the value frequency number.
                    value_frequency = value_frequency + 1
                else:
                    pass
            #Add the number of times the value appears to the values array.
            frequency_array.append(value_frequency)
            
    #Again, take number of measurements.
    number_measurements = len(list_data)
    
    #Normalize our frequency values.
    for i in range(len(frequency_array)):
        frequency_array[i] = frequency_array[i]/number_measurements
        
    plt.bar(values_array, frequency_array, color='cornflowerblue', edgecolor='royalblue')
    plt.xticks(values_array)
    plt.ylabel('Frequency \n')
    plt.xlabel('\n Sum of 2 Dice Rolls (Face Values)')
    plt.title('Sample Dice Rolls Histogram ' + datasettitle + ' \n')
    plt.show()
    

#######################################################################
    
#Main

#Import data rolls from our class.
class_data_rolls = import_data('lab_1_data_class.csv')

#Import 'my' data rolls (by which I mean I forget which set of data was actually mine)
#So we're just going to grab 30 random values from the file.
my_data_rolls = import_data('lab_1_data_mine.csv')

#Calculate sample mean given data rolls from class.
smean_class = sample_mean(class_data_rolls)
print('My calculated mean of class dice rolls: ' + str(smean_class))
smeancheck_class = np.mean(class_data_rolls)
print('Numpy calculated mean of class dice rolls: ' + str(smeancheck_class))

print('####################')

#Calculate sample mean given data rolls from me.
smean_mine = sample_mean(my_data_rolls)
print('My calculated mean of my dice rolls: ' + str(smean_mine))
smeancheck_mine = np.mean(my_data_rolls)
print('Numpy calculated mean of my dice rolls: ' + str(smeancheck_mine))

print('####################')

#Calculate sample median given data rolls from class.
smedian_class = sample_median(class_data_rolls)
print('My calculated median of class dice rolls: ' + str(smedian_class))
smediancheck_class = np.median(class_data_rolls)
print('Numpy calculated median of class dice rolls: ' + str(smediancheck_class))

print('####################')

#Calculate sample median given data rolls from me.
smedian_mine = sample_median(my_data_rolls)
print('My calculated median of my dice rolls: ' + str(smedian_mine))
smediancheck_mine = np.median(my_data_rolls)
print('Numpy calculated median of my dice rolls: ' + str(smediancheck_mine))

print('####################')

#Calculate sample mode given data rolls from class.
smode_class = sample_mode(class_data_rolls)
print('My calculated mode(s) of class dice rolls: ' + str(smode_class))
smodecheck_class = stats.mode(class_data_rolls)
print('Numpy calculated mode(s) of class dice rolls: ' + str(smodecheck_class))

print('####################')

#Calculate sample mode given data rolls from me.
smode_mine = sample_mode(my_data_rolls)
print('My calculated mode(s) of my dice rolls: ' + str(smode_mine))
smodecheck_mine = stats.mode(my_data_rolls)
print('Numpy calculated mode(s) of my dice rolls: ' + str(smodecheck_mine))

print('####################')

#Calculate sample stdev given data rolls from class.
sstdev_class = sample_stdev(class_data_rolls)
print('My calculated standard deviation of class dice rolls: ' + str(sstdev_class))
#NOTE: By default ddof = 0, meaning numpy's std function divides the summation by 1/N, 
#NOT 1/(N-1). Thus, must set ddof = 1 to get same result from class definition of stdev.
sstdevcheck_class = np.std(class_data_rolls, ddof=1)
print('Numpy calculated standard deviation of class dice rolls: ' + str(sstdevcheck_class))

print('####################')

#Calculate sample stdev given data rolls from me.
sstdev_mine = sample_stdev(my_data_rolls)
print('My calculated standard deviation of my dice rolls: ' + str(sstdev_mine))
#NOTE: By default ddof = 0, meaning numpy's std function divides the summation by 1/N, 
#NOT 1/(N-1). Thus, must set ddof = 1 to get same result from class definition of stdev.
sstdevcheck_mine = np.std(my_data_rolls, ddof=1)
print('Numpy calculated standard deviation of class dice rolls: ' + str(sstdevcheck_mine))

print('####################')

make_histogram(my_data_rolls, '(My Dice Rolls)')
make_histogram(class_data_rolls, '(Class Dice Rolls)')

