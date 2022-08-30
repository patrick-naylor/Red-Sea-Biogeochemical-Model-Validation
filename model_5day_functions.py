# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 14:12:01 2020

@author: Patrick
"""
import numpy as np
from scipy import stats

def depth_mean(data, time_start, ymin, ymax, xmin, xmax):
    temp = []
    for i in range(len(data[0,:,ymin,ymax])):
        temp.append(stats.tmean(data[time_start:,i,ymin:ymax,xmin:xmax], (0.0, 1000)))
    return temp

def time_mean(data, time_start,depth_ind, ymin, ymax, xmin, xmax, drF):
    temp = []
    sum_weights = np.empty([len(data[:,0,0,0]) - time_start, ymax-ymin, xmax-xmin])
    sum_weights[:,:,:] = 0
    for i in range(depth_ind):
        sum_weights += (data[time_start:,i,ymin:ymax,xmin:xmax] * drF[i])
    sum_weights = sum_weights / np.sum(drF[:depth_ind])
    sum_weights[sum_weights == 0] = np.float('NaN')
    for i in range(len(data[time_start:,0,0,0])):
        temp.append(np.nanmean(sum_weights[i,:,:]))
    return temp

def depth_avgs(data, time_start, depth_ind, ymin, ymax, xmin, xmax):
    depth = depth_ind+1
    time = len(data[time_start:,0,0,0])
    temp = np.empty([depth,time])
    for i in range(time):
        for j in range(depth):
            temp[j,i] = stats.tmean(data[time_start + i,j,ymin:ymax, xmin:xmax], (0.00000000000000000000000001, 1000))
    return temp

def average_map(data, weights, depth_ind, time_start, ymin, ymax, xmin, xmax, time_end = -1):
    x_size = xmax - xmin
    y_size = ymax - ymin
    mean = np.empty([y_size,x_size])
    t_mean = np.empty([depth_ind,y_size,x_size])
    sum_array = np.empty([depth_ind,y_size,x_size])
    sum_array[:,:,:] = 0
    for i in range(len(data[time_start:time_end,0,0,0])):
        sum_array += data[i+time_start,:depth_ind,ymin:ymax,xmin:xmax]
    t_mean = sum_array/(len(data[time_start:time_end,0,0,0]))
    weighted_7 = t_mean[:depth_ind,:,:]*weights[:depth_ind,ymin:ymax,xmin:xmax]
    weight_sum_7 = np.empty([y_size,x_size])
    weight_sum_7[:,:] = 0
    weight_7 = np.empty([y_size,x_size])
    weight_7[:,:] = 0
    for i in range(depth_ind):
        weight_7 += weighted_7[i,:,:]
        weight_sum_7 += weights[i,ymin:ymax,xmin:xmax]
    mean = weight_7/weight_sum_7 
    return(mean)