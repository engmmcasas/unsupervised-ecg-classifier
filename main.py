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

    annotation.get_contained_labels()
    annotation.wrann()

    labelsDescription = annotation.contained_labels
    labels = annotation.label_store
    labelsSample = annotation.sample

    recordData = {"signals": signals, "signalsNames": sigNames,
     "labelsDescription": labelsDescription, "label_store":labels,
     "labelsSample":labelsSample}

    #recordData["labelsDescription"] = recordData["labelsDescription"][["label_store", "symbol", "description"]].reset_index().drop("index", axis=1)


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

    labelsDf["RR"] = labelsDf["sample"] - labelsDf["sampleShifted"]
    gaussianSignal = sp_signal.gaussian(13, 5)
    gaussianSignal = gaussianSignal/gaussianSignal.sum()
    labelsDf["RRFiltered"] = np.convolve(labelsDf["RR"], gaussianSignal, "sanme")

    return labelsDf


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
