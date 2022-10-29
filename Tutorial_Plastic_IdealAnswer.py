# Students should first of all import their modules, which are the same as that from the main tutorial. 
!pip install git+https://github.com/NERC-FSF/FieldSpecUtils.git -U
import os    #a module that allows us to "talk" with our operating system, neccessary for handling paths, files and so on
from pathlib import Path #a more specific path handling module that allows us to quickly create path names
from specdal import Collection, Spectrum, read #We import our main package, specdal, and ask to only import certain key functions
import pandas as pd   #Pandas is a powerful module for the handling of data sets
from matplotlib import pyplot as plt   #matplotlib emulates the functions of MATLAB. Here, we tell matplotlib to only import one of it's functions, the pyplot function, and to import it with the identifier 'plt'
from matplotlib.pyplot import ylabel, xlabel, title, legend   #We go even further by asking pyplot to only import some of it's subfunctions
from scipy.signal import savgol_filter   #We will use this to smooth our data
import numpy as np #We require numpy for integration functions that will be used during convolution
import FieldSpecUtils


# Students should then proceed to use specdal to create a specdal "collection" (here, WoodlandEndMembers, but can be anything the student wants) object containing the spectra
PlasticsEndMembers = Collection(name='PlasticEndMembers', directory ='Data')

# Averaging -- students average the data prior to  correction
plastic_groups = PlasticsEndMembers.groupby(separator='_', indices=[0])
group_names = list(plastic_groups.keys())
plastic_means = Collection(name='means')
for group_key, group_collection in plastic_groups.items():
    plastic_means.append(group_collection.mean())

# Interpolation -- as this is SVC data, the student should interpolate. 
plastic_means.interpolate(spacing=1, method='linear')

#As with the main tutorial, stitching and jump correction are required, and follow the same code:
plastic_means.stitch(method='mean')
plastic_means.jump_correct(splices=[1000, 1800], reference=0)


# Absolute reflectance -- students must import the SRT_44 calibration coefficents, and then multiply the data frame of spectra by it. 
reference_panel = pd.read_csv("SRT_44.csv", index_col = "wavelength")
Absolute_Plastics = plastic_means.data.mul(reference_panel['Reflectance'], axis = 0)

#Water bands do need to be removed, as this data was collected outside
Absolute_Plastics = Absolute_Plastics.iloc[9:2160]
Absolute_Plastics = pd.DataFrame(savgol_filter(Absolute_Plastics, 41, 2, axis=0),
                             columns=Absolute_Plastics.columns,
                             index=Absolute_Plastics.index)

Absolute_Plastics.loc[1790:1970] = 1
Absolute_Plastics.replace(1,np.nan, inplace= True)

# Second objective -- save the output to a PDF file
Absolute_Plastics.plot(figsize=(12, 6), legend = True, ylim=(0.0,1), xlim=(350, 2500))
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
xlabel("Wavelength (nm)")
ylabel("Absolute Reflectance")
plt.tight_layout()
plt.savefig("Corrected Spectra.pdf")
plt.show()

# Final objective -- convolute to ASTER SRF

# Using help("FieldSpecUtils.Convolution"), the student should learn that Convolution.ASTER is a function that works like Convolution.S2
from FieldSpecUtils import Convolution
Bands = pd.read_csv("ASTER_SRF-1.csv", index_col=0, header=0)
Convolution.ASTER(Absolute_Plastics, Bands)
