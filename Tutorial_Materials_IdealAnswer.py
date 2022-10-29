# The answers are:
#1 - Pressboard
#2 - Jarosite
#3 - Kalonite
#4 - Acetate
#5 - Mylar
#6 - Black paint sample
#7 - Alunite
#8 - Talc
# Each of the technical descriptions are taken from real documents and papers describing the reflectance properties of the materials. The "handwritten" notes are supposed to give extra hints to the student. Feel free to encourage the students to use search engines to look for spectra. Hematite, for example, will help the identification of sample 2. 

# The libraries needed are:
from specdal import Collection, Spectrum, read 
import pandas as pd   
from matplotlib import pyplot as plt  
from matplotlib.pyplot import ylabel, xlabel, title, legend  
import numpy as np 

# The student should start by organizing as a collection:
Materials = Collection(name='Materials', directory ='Data')

# To identify each sample, the student should make judicious use of matplotlib, changing what is plotted, and the ylim and xlim to center in on regions of interest. For example:
Materials[5].plot(figsize=(15, 6), legend = True, ylim=(0,1), xlim=(1600, 1650))
xlabel("Wavelength (nm)")
ylabel("Relative Reflectance")
plt.legend(bbox_to_anchor=(1.05, 1), loc = "upper left")
plt.show()

# As such, not really a coding challenge, but a puzzle! Students should produce a table matching the number of the sample with what they think is the material, and will be asked later in the session for answers
