import wfdb
import copy
import numpy as np
import pandas as pd
import scipy.signal as sp_signal
import matplotlib.pyplot as plt

#Functions.

def readingRecordData(path):
    record = wfdb.rdrecord(path, physical=False)
    annotation = wfdb.rdann(path, 'atr')

    sigNames = record.sig_name
    signals = record.dac()

    period = 1.0/record.fs
    timeToSample = 0.600
    samplesPerBeat = np.floor(timeToSample/period).astype(int)
    sidesSamples = samplesPerBeat // 2

    annotation.get_contained_labels()
    annotation.wrann()

    labelsDescription = annotation.contained_labels
    labels = annotation.label_store
    labelsSample = annotation.sample

    recordData = {"signals": signals, "signalsNames": sigNames,
     "labelsDescription": labelsDescription, "label_store":labels,
     "labelsSample":labelsSample,  "sidesSamples": sidesSamples}


    return recordData

def get_labelsDf(recordData):

    labelsDf = pd.DataFrame(columns = ["sample", "label_store"])
    labelsDf["sample"] = recordData["labelsSample"]
    labelsDf["label_store"] = recordData["label_store"]
    labelsDf = pd.merge(labelsDf, recordData["labelsDescription"].drop("n_occurrences", axis=1),
                        on = "label_store", how="inner")
    labelsDf = labelsDf[labelsDf["symbol"].apply(lambda x: x in ["N", "A", "V"])]
    labelsDf = labelsDf.sort_values("sample")

    return labelsDf


def taking_rr(labelsDf):
    labelsDf["sampleShifted"] = labelsDf["sample"].shift(1)
    labelsDf["RR"] = labelsDf["sample"] - labelsDf["sampleShifted"]
    gaussianSignal = sp_signal.gaussian(13, 5)
    gaussianSignal = gaussianSignal/gaussianSignal.sum()
    labelsDf["RRFiltered"] = np.convolve(labelsDf["RR"], gaussianSignal, "sanme")

    return labelsDf

def getBeatRange(labelsDf, recordData):
    labelsDf = labelsDf.dropna()
    labelsDf["sampleBeatRange"] = labelsDf["sample"].apply(lambda x: [x-recordData["sidesSamples"], x+recordData["sidesSamples"]])
    return labelsDf

def getBeats(labelsDf, recordData):
    beats = []
    for index in labelsDf.index:
        fromLeft, toRight = labelsDf.loc[index, "sampleBeatRange"]
        beatData = recordData["signals"][fromLeft:toRight, 0]
        beats.append(beatData)
    beats = np.array(beats)
    return beats


"""
Sample data
"""

internalPath = "D:/Users/Manuel/Documentos/masters/UABC/unsupervised-ecg-classifier/"
dataset = "MB/"
datFile = "222"
recordPath = internalPath+dataset+datFile


recordData = readingRecordData(recordPath)
labelsDf = get_labelsDf(recordData)
labelsDf = taking_rr(labelsDf)
labelsDf = getBeatRange(labelsDf, recordData)
beats = getBeats(labelsDf, recordData)
