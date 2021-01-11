# unsupervised-ecg-classifier
This is the improved version of my master's thesis Unsupervised ECG Classifier

# Datasets

The main website to download data is <a href="https://physionet.org/">Physionet </a>. <br>However in order to donwload the datasets directly they can be found in:
* MIT-BIH Arrhythmia Database: https://physionet.org/content/mitdb/1.0.0/
* MIT-BIH Supraventricular Arrhythmia Database: https://physionet.org/content/svdb/1.0.0/
* St Petersburg INCART 12-lead Arrhythmia Database: https://physionet.org/content/incartdb/1.0.0/

ToDo:

- [x] Read data (by download
wfdb-python)
- [ ] some visualizations and explore dataset
- [ ] Remove baseline.
- [x] Cut beats from raw signal using QRS peaks from annotation.
- [x] ~~Oversample data.~~ No necessary
- [ ] Take features from beats.
- [x] Calculate R-R signals.
- [ ] Identify ATB and BTB.
