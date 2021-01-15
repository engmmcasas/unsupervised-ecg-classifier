import wfdb
import copy
import numpy as np
import pandas as pd
import os

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


def splitName(file):
    output = 0
    try:
        output = str(int(file.split(".")[0]))
    except:
        output = str("0")

    return output


internalPath = "D:/Users/Manuel/Documentos/masters/UABC/unsupervised-ecg-classifier/"
dataset = "MB/"

listFiles = os.listdir("./MB")
listPatient = [splitName(file) for file in listFiles if "atr" in file]

allInfo = []
for datFile in listPatient:
    try:
    #datFile = "221"
        recordPath = internalPath+dataset+datFile
        recordData = readingRecordData(recordPath)
        tempInfo = recordData["labelsDescription"]
        tempInfo["patient"] = datFile
        allInfo.append(tempInfo)
    except:
        print(f"File {datFile} have some sort of error")
        pass


allInfo = pd.concat(allInfo)
allInfo.reset_index().drop("index", axis = 1).to_csv("summaryBeats.csv")
