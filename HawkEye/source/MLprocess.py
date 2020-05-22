from sklearn.cluster import KMeans
import numpy as np

with open(".hawk/datasets/SV.txt","r+") as SV: #only Saturation and Value
    for line in open(".hawk/datasets/hsv.txt"):
        if line.strip():
            SV.write("\t".join(line.split()[1:]) + "\n")
    dataset = np.loadtxt(".hawk/datasets/SV.txt")
clusters = KMeans(n_clusters=3)
clusters.fit(dataset) #cluster all points to 3 main clusters
labels = clusters.labels_

selectedCluster = []
Scluster = [] #saturation cluster
Vcluster = [] #value cluster

print("Dataset: ")
print(dataset)
print("Centers: ")
print(labels)

mostCommon = np.argmax(np.bincount(labels)) #find the biggest cluster label

for i in range(len(labels)): #collect all biggest cluster points
    if(labels[i] == mostCommon):
        selectedCluster.append(dataset[i])

for i in range(len(selectedCluster)): # seperate them into Saturation and Value arrays
    selected = selectedCluster[i]
    Scluster.append(selected[0])
    Vcluster.append(selected[1])

_maxSat_ = np.amax(Scluster)
_minSat_ = np.amin(Scluster)

_maxVal_ = np.amax(Vcluster)
_minVal_ = np.amin(Vcluster)

print("success, The results are:")
print("Saturation: \n Min: " + str(_minSat_) + "\n" + " Max: " + str(_maxSat_))
print("Value: \n Min:" + str(_minVal_) + "\n" + " Max: " + str(_maxVal_))

