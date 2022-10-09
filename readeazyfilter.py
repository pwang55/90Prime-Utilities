import numpy as np

latest = '/Users/brianwang76/bin/eazy-photoz/inputs/FILTER.RES.latest'
info = '/Users/brianwang76/bin/eazy-photoz/inputs/FILTER.RES.latest.into'

lines = []

with open(latest) as f:
    for l in f:
        lines.append(l.strip())

idxs = []
lens = []

for i in range(len(lines)):
    if lines[i].split(' ')[0]=='1':
        idxs.append(i)
        lens.append(lines[i-1].split(' ')[0])



def filt(fid):
    '''

    Enter the index number in the beginning of the filter you want in FILTER.RES.latest.into
    
    For example, if you want:
    16    125 hst/wfpc2_f814w.dat synphot-calcband lambda_c= 7.9960e+03 AB-Vega= 0.412 w95=2366.3

    Then enter filt(16)

    '''

    fid = fid - 1

    idx = int(idxs[fid])
    flen = int(lens[fid])

    print(lines[idx-1])

    line = lines[idx:idx+flen]
    lams = []
    res = []
    for j in range(len(line)):
        #print(line[j])
        linesplit = line[j].split()
        lams.append(float(linesplit[1]))
        res.append(float(linesplit[2]))

    lams = np.array(lams)
    res = np.array(res)
    return lams, res



