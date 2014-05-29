#!/usr/bin/env python

##########################################################
# A python module to access data from WFDB
# Copyright (C) 2009, 2010  Raja Selvaraj <rajajs@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
##########################################################


"""
A pure python module for accessing and using the waveform data in `Physiobank <http://www.physionet.org/physiobank/>`_. 
Provides `rdsamp` and `rdann` which are the python equivalents of the wfdb applications
of similar names.
A deliberate attempt is made to try to keep names and usage similar to the
original wfdb applications for simplicity of use.

The only dependency that will need to be installed is numpy. However, to use the function
`plot_data`, which is an utility function for interactive use, you need to have matplotlib
also installed.

Example Usage::

    >> from wfdbtools import rdsamp, rdann, plot_data
    >> from pprint import pprint
    
    # Record is a format 212 record from physiobank.
    # Note that name of record does not include extension.
    >> record  = 'samples/format212/100'

    # Read in the data from 0 to 10 seconds
    >> data, info = rdsamp(record, 0, 10)
    
    # returned data is an array. The columns are time(samples),
    # time(seconds), signal1, signal2
    >> print data.shape
    (3600, 4)

    # info is a dictionary containing header information
    >> pprint info
    {'first_values': [995, 1011],
    'gains': [200, 200],
    'samp_count': 650000,
    'samp_freq': 360,
    'signal_names': ['MLII', 'V5'],
    'zero_values': [1024, 1024]}
    
    # And now read the annotation
    >> ann = rdann(record, 'atr', 0, 10)

    # ann has 3 columns - sample number, time (sec) and annotation code
    >> print(ann[:4,:])
       array([[  18.   ,    0.05 ,   28.   ],
              [  77.   ,    0.214,    1.   ],
              [ 370.   ,    1.028,    1.   ],
              [ 662.   ,    1.839,    1.   ]])
    
    
    # Plot the data and the mark the annotations
    >> plot_data(data, info, ann)

"""

## Changelog

# 21-10-2010 rdsamp supports format 16 files with any number of signals
# 21-10-2010 rdhdr now supports multichannel recordings

# ver0.2


# rdsamp based on rddata.m for matlab written by Robert Tratnig
# available at http://physionet.org/physiotools/matlab/rddata.m

from __future__ import division
import re
import warnings
import numpy
#import pylab
#from pprint import pprint

__author__ = 'Raja Selvaraj <rajajs@gmail.com>'
__version__ = '0.2'

## Annotation codes
CODEDICT = {
    0 : 'NOTQRS',	# not-QRS (not a getann/putann codedict) */
    1 : 'NORMAL',	# normal beat */
    2 : 'LBBB',	# left bundle branch block beat */
    3 : 'RBBB',	# right bundle branch block beat */
    4 : 'ABERR',	# aberrated atrial premature beat */
    5 : 'PVC',	# premature ventricular contraction */
    6 : 'FUSION',	# fusion of ventricular and normal beat */
    7 : 'NPC',	# nodal (junctional) premature beat */
    8 : 'APC',	# atrial premature contraction */
    9 : 'SVPB',	# premature or ectopic supraventricular beat */
    10 : 'VESC',	# ventricular escape beat */
    11 : 'NESC',	# nodal (junctional) escape beat */
    12 : 'PACE',	# paced beat */
    13 : 'UNKNOWN',	# unclassifiable beat */
    14 : 'NOISE',	# signal quality change */
    16 : 'ARFCT',	# isolated QRS-like artifact */
    18 : 'STCH',	# ST change */
    19 : 'TCH',	# T-wave change */
    20 : 'SYSTOLE',	# systole */
    21 : 'DIASTOLE',	# diastole */
    22 : 'NOTE',	# comment annotation */
    23 : 'MEASURE',	# measurement annotation */
    24 : 'PWAVE',	# P-wave peak */
    25 : 'BBB',	# left or right bundle branch block */
    26 : 'PACESP',	# non-conducted pacer spike */
    27 : 'TWAVE',	# T-wave peak */
    28 : 'RHYTHM',	# rhythm change */
    29 : 'UWAVE',	# U-wave peak */
    30 : 'LEARN',	# learning */
    31 : 'FLWAV',	# ventricular flutter wave */
    32 : 'VFON',	# start of ventricular flutter/fibrillation */
    33 : 'VFOFF',	# end of ventricular flutter/fibrillation */
    34 : 'AESC',	# atrial escape beat */
    35 : 'SVESC',	# supraventricular escape beat */
    36 : 'LINK',	# link to external data (aux contains URL) */
    37 : 'NAPC',	# non-conducted P-wave (blocked APB) */
    38 : 'PFUS',	# fusion of paced and normal beat */
    39 : 'WFON',	# waveform onset */
    #WFON : 'PQ',	# PQ junction (beginning of QRS) */
    40 : 'WFOFF',	# waveform end */
    #WFOFF : 'JPT',	# J point (end of QRS) */
    41 : 'RONT'	# R-on-T premature ventricular contraction */
    }



def rdsamp(record, start=0, end=-1, interval=-1):
    """
    Read signals from a format 212 record from Physionet database.

    Only 2 channel records in format 212 are supported.
    This is the most common record in the
    Physionet database(http://www.physionet.org/physiobank/).
    
    Parameters
    ----------
    record : str
            Full path to record. No extension to be used for record name.
    start  : int, optional
            time to begin in seconds, default 0
    end    : int, optional
            time to end in seconds, defaults to end of record
    interval : int, optional
            interval of data to be read in seconds
            If both interval and end are given, earlier limit is used.

    Returns
    -------
    data : (N, 4) ndarray
          numpy array with 4 columns
          col 1 - Elapsed time in samples
          col 2 - Elapsed time in milliseconds
          col 3,4 - The two signals
          Signal amplitude is in physical units (mV)          
    info : dict
          Dictionary containing header information
          keys :
          'signal_names' - Names of each signal
          'samp_freq' - Sampling freq (samples / second)
          'samp_count' - Total samples in record
          'first_values' - First value of each signal
          'gains' - Gain for each signal
          'zero_values' - Zero value for each signal
    
    """
    # read the header file - output is a dict
    info = rdhdr(record)
    # establish start and end in samples
    start, end = _get_read_limits(start, end, interval, info)

    # read the data
    signal_format = info['file_format'][0] # assume all sig have same format

    # TODO: 
    if signal_format == '212':
        data = _read_data_212(record, start, end, info)
    elif signal_format == '16':
        data = _read_data_16(record, start, end, info)
        
    return data, info

def rdann(record, annotator, start=0, end=-1, types=[]):
    """
    Reads annotations for given record by specified annotator.

    Parameters
    ----------
    record : str
            Full path to record. Record name has no extension.
    annotator : str
            Name of annotator, eg. 'atr'.
            This is the extension for the annotation file.
    start  : int, optional
            time to begin in seconds, default 0
    end    : int, optional
            time to end in seconds, defaults to end of record
    types   : list, optional
            list of annotation types that will be returned.
            Types are input as annotation code (integer from 0 to 49)
            Annotation types not in list will be ignored.
            Default is empty list, which results in all types being read.
            
    Returns
    -------
    data : (N, 3) ndarray
          numpy array with 3 columns
          col 1 - Elapsed time in samples for each annotation.
          col 2 - Elapsed time in seconds for each annotation.
          col 3 - The annotation code.

    """
    # get header data
    info = rdhdr(record)
    
    annfile = ''.join((record, '.', annotator))
    with open(annfile, 'rb') as f:
        arr = numpy.fromstring(f.read(), dtype = numpy.uint8).reshape((-1, 2))

    rows = arr.shape[0]
    annot = []
    annot_time = []
    i = 0

    while i < rows:
        anntype = arr[i, 1] >> 2
        if anntype == 59:
            annot.append(arr[i+3, 1] >> 2)
            annot_time.append(arr[i+2, 0] + (arr[i+2, 1] << 8) +
                              (arr[i+1, 0] << 16) + arr[i+1, 1] << 24)
            i += 3
        elif anntype in [60, 61, 62]:
            pass
        elif anntype == 63:
            hilfe = arr[i, 0] + ((arr[i, 1] & 3) << 8)
            hilfe += hilfe % 2
            i += hilfe / 2
        else:
            annot_time.append(arr[i, 0] + ((arr[i, 1] & 3) << 8))
            annot.append(arr[i, 1] >> 2)
        i += 1

    # last values are EOF indicator
    annot_time = annot_time[:-1]
    annot = annot[:-1]
    
    # annot_time should be total elapsed samples
    annot_time = numpy.cumsum(annot_time)
    annot_time_ms = annot_time / info['samp_freq'] # in seconds
    
    # limit to requested interval
    start, end = _get_read_limits(start, end, -1, info)
    ann = numpy.array([annot_time, annot_time_ms, annot]).transpose()
    
    # filter by annot_time in interval
    ann =  ann[start <= ann[:, 0]]
    ann = ann[ann[:, 0] <= end]

    # filter by type
    if types != []:
        ann = ann[numpy.logical_or.reduce([ann[:, 2] == x for x in types])]
        #ann = ann[numpy.array([ann[x, 2] in types for x in range(len(ann))])]

    return ann
    
def plot_data(data, info, ann=None):
    """
    Plot the signal with annotations if available.

    Parameters
    ----------
    data : (N, 4) ndarray
         Output array from rdsamp.
    info : dict
         Header information as a dictionary.
         Output from rdsamp
    ann : (N, 2) ndarray, optional
         Output from rdann

    Returns
    -------
    None
    Matplotlib figure is plotted with the signals and annotations.
    """
    try:
        import pylab
    except ImportError:
        warnings.warn("Could not import pylab. Abandoning plotting")
        return
    
    nsignals = info['signal_count']
    time = data[:, 1] #in seconds. use data[:, 0] to use sample no.
    
    print 'have %d signals...' % (nsignals)
    for sig in range(nsignals):
        sigdata = data[:, sig+2]
        
        pylab.subplot(nsignals, 1, sig+1)
        pylab.plot(time, sigdata, 'k')
        #pylab.xticks([])
        pylab.ylabel('%s (mV)' %(info['signal_names'][sig]))
        pylab.xlabel('Time (seconds)')
    
        if ann != None:
            # annotation time in samples from start
            ann_x = (ann[:, 0] - data[0, 0]).astype('int')
            pylab.plot(ann[:, 1], data[ann_x, sig+2], 'xr')

    pylab.show()


def rdhdr(record):
    """
    Returns the information read from the header file

    Header file for each record has suffix '.hea' and
    contains information about the record and each signal.

    Parameters
    ----------
    record : str
            Full path to record. Record name has no extension.

    Returns
    -------
    info : dict
          Information read from the header as a dictionary.
          keys :
          'signal_count' - Number of signals
          'signal_names' - Names of each signal
          'samp_freq' - Sampling freq (samples / second)
          'samp_count' - Total samples in record
          'first_values' - First value of each signal
          'gains' - Gain for each signal
          'zero_values' - Zero value for each signal
          'signal_names' - Name/Descr for each signal
          'file_format' - format for each signal
    
    """
    info = {'signal_names':[], 'gains':[], 'units':[],
            'first_values':[], 'zero_values':[], 'file_format':[]}
    
    RECORD_REGEX = re.compile(r''.join([
            #"(?P<record>\d+)\/*(?P<seg_ct>\d*)\s",
            "(?P<record>[0-9a-zA-Z\._/-]+)\/*(?P<seg_ct>\d*)\s", #record name can be any alphanumeric, surely?
            "(?P<sig_ct>\d+)\s*",
            "(?P<samp_freq>\d*)\/?(?P<counter_freq>\d*)\(?(?P<base_counter>\d*)\)?\s*",
            "(?P<samp_count>\d*)\s*",
            "(?P<base_time>\d{,2}:*\d{,2}:*\d{,2})\s*",
            "(?P<base_date>\d{,2}\/*\d{,2}\/*\d{,4})"]))

    SIGNAL_REGEX = re.compile(r''.join([
            "(?P<file_name>[0-9a-zA-Z\._/-]+)\s+",
            "(?P<format>\d+)x{,1}(?P<samp_per_frame>\d*):*",
            "(?P<skew>\d*)\+*(?P<byte_offset>\d*)\s*",
            "(?P<adc_gain>\d*)\(?(?P<baseline>\d*)\)?\/?",
            "(?P<units>\w*)\s*(?P<resolution>\d*)\s*",
            "(?P<adc_zero>\d*)\s*(?P<init_value>[\d-]*)\s*",
            "(?P<checksum>[0-9-]*)\s*(?P<block_size>\d*)\s*",
            "(?P<description>[a-zA-Z0-9\s]*)"]))

    header_lines, comment_lines = _getheaderlines(record)
    (record_name, seg_count, signal_count, samp_freq,
     counter_freq, base_counter, samp_count,
     base_time, base_date) = RECORD_REGEX.findall(header_lines[0])[0]

    # use 250 if missing
    if samp_freq == '':
        samp_freq = 250
    if samp_count == '':
        samp_count = 0
        

    info['signal_count'] = int(signal_count)
    info['samp_freq'] = float(samp_freq)
    info['samp_count'] = int(samp_count)
    
    for sig in range(info['signal_count']):
        (file_name, file_format, samp_per_frame, skew,
         byte_offset, gain, baseline, units,
         resolution, zero_value, first_value,
         checksum, blocksize, signal_name) = SIGNAL_REGEX.findall(
                                             header_lines[sig+1])[0]

        # replace with defaults for missing values
        if gain == '' or gain == 0:
            gain = 200
        if units == '':
            units = 'mV'
        if zero_value == '':
            zero_value = 0
        if first_value == '':
            first_value = 0   # do not use to check
        
        info['gains'].append(float(gain))
        info['units'].append(units)
        info['zero_values'].append(float(zero_value))
        info['first_values'].append(float(first_value))
        info['signal_names'].append(signal_name)
        info['file_format'].append(file_format)

    return info
        
def _getheaderlines(record):
    """Read the header file and separate comment lines
    and header lines"""
    hfile = record + '.hea'
    all_lines = open(hfile, 'r').readlines()
    comment_lines = []
    header_lines = []
    # strip newlines
    all_lines = [l.rstrip('\n').rstrip('\r') for l in all_lines]
    # comments
    for l in all_lines:
        if l.startswith('#'):
            comment_lines.append(l)
        elif l.strip() != '':
            header_lines.append(l)
    
    return header_lines, comment_lines

    
def _get_read_limits(start, end, interval, info):
    """
    Given start time, end time and interval
    for reading data, determines limits to use.
    info is the dict returned by rdhdr
    end of -1 means end of record.
    If both end and interval are given, choose
    earlier limit of two.
    start and end are returned as samples.
    Example:
    >>> _get_read_limits(0, 2, -1, {'samp_count':100, 'samp_freq':10})
    (0, 20)
    >>> _get_read_limits(0, 2, 3, {'samp_count':100, 'samp_freq':10})
    (0, 20)
    >>> _get_read_limits(0, 4, 2, {'samp_count':100, 'samp_freq':10})
    (0, 20)
    >>> _get_read_limits(0, 105, -1, {'samp_count':100, 'samp_freq':10})
    (0, 100)
    >>> _get_read_limits(-1, -1, -1, {'samp_count':100, 'samp_freq':10})
    (0, 100)
    """
    start *= info['samp_freq']
    end *= info['samp_freq']
    
    if start < 0:         # If start is negative, start at 0
        start = 0
    if end < 0:           # if end is negative, use end of record
        end = info['samp_count']
    if end < start:       # if end is before start, swap them
        start, end = end, start
    interval_end = start + interval * info['samp_freq'] # end det by interval
    if interval_end < start:
        interval_end = info['samp_count']
    end = min(end, interval_end, info['samp_count']) # use earlier end
    return int(start), int(end)


def _read_data_16(record, start, end, info):
    """Read binary data from format 16 files"""
    datfile = record + '.dat'
    samp_to_read = end - start
    signal_count = info['signal_count']
    
    # verification
    
    with open(datfile, 'rb') as f:
        firstvals = numpy.fromstring(f.read(2*signal_count),
                                     dtype=numpy.int16).reshape(1,signal_count)
        firstvals = list(firstvals[0,:].astype('float'))
        
    if firstvals != info['first_values']:
        warnings.warn(
            'First value from dat file does not match value in header')

        
    # read the values into an array
    with open(datfile, 'rb') as f:
        f.seek(start*signal_count*2)
        arr = numpy.fromstring(f.read(2*signal_count*samp_to_read),
                               dtype=numpy.int16).reshape(samp_to_read, signal_count)

    # adjust zero_value and gain
    # TODO: make this common code handling any number of channels
    data = arr.astype('float')
    rows, cols = data.shape
    for c in range(cols):
        data[:, c] = (data[:, c] - info['zero_values'][c]) / info['gains'][c]


    # add time columns
    timecols = numpy.zeros((rows, 2), dtype = 'float')
    
    timecols[:, 0] = numpy.arange(start, end)
    timecols[:, 1] = (numpy.arange(samp_to_read) + start) / info['samp_freq']

    # concat
    data = numpy.concatenate((timecols, data), axis=1)
        
    return data

        
def _read_data_212(record, start, end, info):
    """Read the binary data for each signal"""
    def _arr_to_data(arr):
        """Use bit level operations to read the binary data"""
        second_col = arr[:, 1].astype('int')
        bytes1 = second_col & 15 # bytes belonging to first sample
        bytes2 = second_col >> 4 # belongs to second sample
        sign1 = (second_col & 8) << 9 # sign bit for first sample
        sign2 = (second_col & 128) << 5 # sign bit for second sample
        # data has columns - samples, time(ms), signal1 and signal2
        data = numpy.zeros((arr.shape[0], 4), dtype='float')
        data[:, 2] = (bytes1 << 8) + arr[:, 0] - sign1
        data[:, 3] = (bytes2 << 8) + arr[:, 2] - sign2
        return data
    
    datfile = record + '.dat'
    samp_to_read = end - start

    # verify against first value in header
    with open(datfile, 'rb') as f:
        data = _arr_to_data(numpy.fromstring(f.read(3),
                        dtype=numpy.uint8).reshape(1,3))

    if [data[0, 2], data[0, 3]] != info['first_values']:
        warnings.warn(
            'First value from dat file does not match value in header')
    
    # read into an array with 3 bytes in each row
    with open(datfile, 'rb') as f:
        f.seek(start*3)
        arr = numpy.fromstring(f.read(3*samp_to_read),
                dtype=numpy.uint8).reshape((samp_to_read, 3))

    data = _arr_to_data(arr)

    # adjust zerovalue and gain
    data[:, 2] = (data[:, 2] - info['zero_values'][0]) / info['gains'][0]
    data[:, 3] = (data[:, 3] - info['zero_values'][1]) / info['gains'][1]

    # time columns
    data[:, 0] = numpy.arange(start, end)  # elapsed time in samples
    data[:, 1] = (numpy.arange(samp_to_read) + start
                  ) / info['samp_freq'] # in sec
    return data

# def _arr_to_data(arr):
#     """From the numpy array read from the dat file
#     using bit level operations, extract the 12-bit data"""
#     second_col = arr[:, 1].astype('int')
#     bytes1 = second_col & 15 # bytes belonging to first sample
#     bytes2 = second_col >> 4 # belongs to second sample
#     sign1 = (second_col & 8) << 9 # sign bit for first sample
#     sign2 = (second_col & 128) << 5 # sign bit for second sample
#     # data has columns - samples, time(ms), signal1 and signal2
#     data = numpy.zeros((arr.shape[0], 4), dtype='float')
#     data[:, 2] = (bytes1 << 8) + arr[:, 0] - sign1
#     data[:, 3] = (bytes2 << 8) + arr[:, 2] - sign2
#     return data

def get_annotation_code(code=None):
    """Returns the symbolic definition for the wfdb annotation code.

    See http://www.physionet.org/physiotools/wpg/wpg_31.htm for details.
    Based on ecgcodes.h from wfdb.
    
    Parameters
    ----------
    code : int
           Integer from 0 to 49 (ACMAX).

    Returns
    -------
    Definition : str
                 The definition for the code.

    """
    return CODEDICT[code]

def main():
    """Run tests when called directly"""
    import nose
    print "-----------------"
    print "Running the tests"
    print "-----------------"
    nose.main()
        
if __name__ == '__main__':
    main()
        
