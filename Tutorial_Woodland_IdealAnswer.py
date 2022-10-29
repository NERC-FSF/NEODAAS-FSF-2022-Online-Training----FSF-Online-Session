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
WoodlandEndMembers = Collection(name='WoodlandEndMembers', directory ='Data')

# Averaging -- students average the data prior to  correction
woodland_groups = WoodlandEndMembers.groupby(separator='_', indices=[0])
group_names = list(woodland_groups.keys())
woodland_means = Collection(name='means')
for group_key, group_collection in woodland_groups.items():
    woodland_means.append(group_collection.mean())

#The next steps are in correction
# Correction, from the main tutorial, goes through a set process of interpolation to overlap stitching to jump correction to absolute reflectance to water band removal. 
# Ideally, the student should consider each of these steps in turn, and ask themselves "Do I need to do this? If so, how do I do it, and for which regions?"

# Interpolation -- the student should realise that for ASD data, interpolation is NOT required! This will be outright said in the lecture in the morning, and strongly hinted at in the main tutorial.
# Even if the student misses this information, they should, ideally, notice this when inspecting the data. As a hint, the following code can be given

print(type(WoodlandEndMembers.spectra))
for s in WoodlandEndMembers.spectra[0:3]:
    print(s)
    
# Here, ask the student "What do you notice about the wavelength scale?" (It will be in 1 nm increments from 350.0 to 351.0 to 352.0 etc.). Ask "What does interpolation of the wavelength scale do?" this should reveal to the student of why interpolation here is unccessary

# Overlap stitching -- it will be told outright in the lecture that an ASD requires overlap stitching. The student can inspect the regions between 1000 nm and 1800 nm where the joins are to see this:

woodland_means.plot(title='Group means', figsize=(15, 6), ylim=(0, 1),xlim=(900, 1100))
xlabel("Wavelength (nm)")
ylabel("Relative Spectral Reflectance")
plt.show()

woodland_means.plot(title='Group means', figsize=(15, 6), ylim=(0, 1),xlim=(1700, 1900))
xlabel("Wavelength (nm)")
ylabel("Relative Spectral Reflectance")
plt.show()

#To stitch, this code should be used:
woodland_means.stitch(method='mean')

# Jump correction -- likely to cause some confusion. The main tutorial asks for jump correction at 1000 and 1800 nm. Students will realise that jumps occur at different regions dependning on spectrometer. For this ASD, the jump is actually at 1830 nm. 
# It can be hinted that the student should inspect the spectra. can they see any sudden jumps in the data? Draw attention to the "hump" feature at 1830 nm. The following code can help them visualize this better:
woodland_means.plot(title='Group means', figsize=(15, 6), ylim=(0, 1),xlim=(350, 2500))
xlabel("Wavelength (nm)")
ylabel("Relative Spectral Reflectance")
plt.show()

#Once they realise that it is at 1830 nm, the following code can be used:
woodland_means.jump_correct(splices=[1000, 1830], reference=0)

# Absolute reflectance -- students must import the SRT_44 calibration coefficents, and then multiply the data frame of spectra by it. 
reference_panel = pd.read_csv("SRT_44.csv", index_col = "wavelength")
Absolute_woodland_means = woodland_means.data.mul(reference_panel['Reflectance'], axis = 0)

# Waterband removals -- it is mentioned in the first cell that the measurements were taken indoors with a plant contact probe. Therefore, water bands are not present and do not need to be removed. 
# Ask the students, if stuck on this issue, to compare the data in the first tutorial with the data in this tutorial. In the WB regions, can they see any regions of noise?


# Rhododendron plot -- this will require the student to look closely at how individual columns in a datframe are plotted.
# They should be able to note that in the main tutorial, the seaweed group can be plotted seperately using groups['seaweed'].plot
# If stuck, ask them to inspect this code. Can it be replicated with woodland_means?
# They should arrive at code such as this. Note the labels need to be in Absolute Reflectance, and they also need to save the plot as an answer to the question.
Absolute_woodland_means ['rhododendron_mean'].plot(title='Rhododendron', figsize=(15, 6), ylim=(0, 1),xlim=(350, 2500))
xlabel("Wavelength (nm)")
ylabel("Absolute Spectral Reflectance")
plt.tight_layout()
plt.savefig("Rhododendron Spectra.png")
plt.show()

# Modified Chlorophyll Absorption Ratio Index -- this is a function in FieldSpecUtils. 
# As suggested in the markdown code, they should look at the help file for FieldSpecUtils. This will reveal that MCARI is a function of FieldSpecUtils.
from FieldSpecUtils import Vegetation_Indices
help("FieldSpecUtils.Vegetation_Indices")
Vegetation_Indices.MCARI(Absolute_woodland_means)


# Students should be reminded to save the rhododendron plot, and save copy paste the table of MCARI. They will be asked questions on the tutorial. 
