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

# The next few steps follow the exact same steps from the first tutorial. 

# Students should then proceed to use specdal to create a specdal "collection" (here, WoodlandEndMembers, but can be anything the student wants) object containing the spectra
waste = Collection(name='WasteEndMembers', directory ='Data')

# Averaging -- students average the data prior to  correction
waste_groups = waste.groupby(separator='_', indices=[0])
group_names = list(waste_groups.keys())
waste_means = Collection(name='means')
for group_key, group_collection in waste_groups.items():
    waste_means.append(group_collection.mean())

# No correction other than to absolute reflectance is needed at all. It's an ASD, so interpolation is automatic, it's measured in a lab so water bands aren't present, and the preamble states that the instrument has been configured to remove overlap and jumps.

# Absolute reflectance:

reference_panel = pd.read_csv("SRT_44.csv", index_col = "wavelength")
Absolute_waste_means = waste_means.data.mul(reference_panel['Reflectance'], axis = 0)

# Plotting and csv export
Absolute_waste_means.plot(title='Group means', figsize=(15, 6), ylim=(0, 1),xlim=(350, 2500))
xlabel("Wavelength (nm)")
ylabel("Absolute Spectral Reflectance")
plt.tight_layout()
plt.savefig("Average_corrected_waste_means.pdf")
plt.show()

Absolute_waste_means.to_csv("Mean_plot_spectra.csv")

# Convolution to S2 bands follows the same coding as with the main tutorial. The student needs to remember that they are prompted for water band removal in the code, they must correctly say "No" to that option.
from FieldSpecUtils import Convolution
Bands = pd.read_csv("Sentinel 2 SRF.csv", index_col=0, header=0)
Convolution.S2(Absolute_waste_means, Bands)

# The final step is the main goal of the tutorial -- to work with indices. They should use the final cell of the main tutorial as the template, to produce the following code:

collated_convolved = pd.read_csv("Plots_with_convolved_bands.csv", index_col = 0)

collated_convolved.loc['FMI'] = ((collated_convolved.loc['Band 12 - 2190'] / 
                                 collated_convolved.loc['Band 8a - 865']) 
                               +
                               (collated_convolved.loc['Band 3 - 560'] /
                                collated_convolved.loc['Band 4 - 665'])) 

print(collated_convolved.loc['FMI'])


