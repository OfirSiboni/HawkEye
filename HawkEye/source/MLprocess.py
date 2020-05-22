from sklearn.cluster import KMeans
import numpy as np
import sys
sys.path.append('/root/.hawk/grips/')
from mlgrip import GripPipeline


selectedSVcluster = []
Hcluster = [] #hue cluster
Scluster = [] #saturation cluster
Vcluster = [] #value cluster

with open(".hawk/datasets/SV.txt","r+") as SV: #only Saturation and Value
    for line in open(".hawk/datasets/hsv.txt"):
        Hcluster.append(float(line.partition(" ")[0]))
        if line.strip():
            SV.write("\t".join(line.split()[1:]) + "\n")
    dataset = np.loadtxt(".hawk/datasets/SV.txt")

clusters = KMeans(n_clusters=3)
clusters.fit(dataset) #cluster all points to 3 main clusters
labels = clusters.labels_
print("Dataset: ")
print(dataset)
print("Hue Dataset: ")
print(Hcluster)
print("Centers: ")
print(labels)

mostCommon = np.argmax(np.bincount(labels)) #find the biggest cluster label

for i in range(len(labels)): #collect all biggest cluster points
    if(labels[i] == mostCommon):
        selectedSVcluster.append(dataset[i])

for i in range(len(selectedSVcluster)): # seperate them into Saturation and Value arrays
    selected = selectedSVcluster[i]
    Scluster.append(selected[0])
    Vcluster.append(selected[1])

_maxSat_ = np.amax(Scluster)
_minSat_ = np.amin(Scluster)

_maxVal_ = np.amax(Vcluster)
_minVal_ = np.amin(Vcluster)

#calculate Hue range
Hcluster.sort()
wall = int(len(Hcluster)/3)
_minHue_ = Hcluster[wall]
_maxHue_ = Hcluster[2 * wall]

print("calculation succeed, The results are:")
print("Hue: \n Min: " + str(_minHue_) + "\n" + " Max: " + str(_maxHue_))
print("Saturation: \n Min: " + str(_minSat_) + "\n" + " Max: " + str(_maxSat_))
print("Value: \n Min:" + str(_minVal_) + "\n" + " Max: " + str(_maxVal_))

try:
    grip_pipe = GripPipeline()
    grip_pipe.__init__()
    grip_pipe.setHSV(H= [_minHue_,_maxHue_],S = [_minSat_,_maxSat_],V = [_minVal_,_maxVal_])
    print(grip_pipe.getHSV())
except Exception as e:
    print("Setup values Error!")
    print(e)

