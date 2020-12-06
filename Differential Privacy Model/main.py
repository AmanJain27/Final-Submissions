
import decision_trees_model as dp
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from diffpriv import diffpriv


# import haberman dataset
filename = 'C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\haberman.csv'
names= ['Age', 'Year Of Operation 19', 'No. of Positive axillary nodes', 'Survival Status']
hb = pd.read_csv(filename,names=names, header=None)

# set up x and y for training and testing

class_attrib = hb[names[3]] # class attributes for haberman is column 3 starting from 0
pred_attrib = hb.drop(names[3], axis=1)

y = class_attrib # class attributes for y
x = pred_attrib # predictor attributes for x
import numpy as np

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

# Class attributes
y_arr = np.array(np.unique(y))


#from sklearn.metrics import accuracy_score

#
#from sklearn.tree import export_text


#different epislon values
epsilons = [0.25, 0.5, 1,2]
import matplotlib.pyplot as plt
#plt.title("Taxonomy tree depth Accuracy graph")
plt.xlabel('epsilons')
plt.ylabel('accuracy')
color = {2:'red', 4:'green', 6:'yellow', 8:'purple', 10:'blue', 12:'orange', 14:'black', 16:'indigo'}
color_l = []
decision = None


# anonymize the dataset before writing a differentially private dataset
filename_generalized = "C:\\Users\\AmanH\\Downloads\\2haberman.csv"

hb_g = pd.read_csv(filename_generalized)
#print(hb_g)
# drop the class attributes from the generalized version to replace it with the new ones
x_g = hb_g.drop(hb_g.columns[3], axis=1)
y_g = hb_g[hb_g.columns[3]]



# dot_data = tree.export_graphviz(dec_t, out_file=None, feature_names={0:x.keys()[0],1:x.keys()[1],2:x.keys()[2]},  filled=True, rounded=True,class_names=np.array(['survived after 5 years','survived upto 5 years']), special_characters=True)
# graph = graphviz.Source(dot_data)
# graph.save(filename='graph')
#
#
# dot_data2 = tree.export_graphviz(dec, out_file=None, feature_names={0:x.keys()[0],1:x.keys()[1],2:x.keys()[2]},  filled=True, rounded=True,class_names=np.array(['survived after 5 years','survived upto 5 years']), special_characters=True)
# graph2 = graphviz.Source(dot_data2)
# graph.save(filename='graph2')





# calculate average accuracies using KFold and get the new survival status
from diffpriv import cross_val_average_and_plot

cross_val_average_and_plot(hb, epsilons, dp, y, x, y_arr,color, color_l, plt)

survival = diffpriv(epsilons, dp, X_train, y_train, X_test, y_test, y_arr, y, x)[1]




# write the datasets in the files
from writeToFiles import update_contents_in_files

col_names = ['Age', 'Year of operation', 'Positive Aux nodes']
path = f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\diff privacy"
depth_start = 2
depth_end = 12
step = 2
acc = update_contents_in_files(path, depth_start, depth_end, step, epsilons,  col_names, x_g, y, survival)
import os
if not os.path.isdir(f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\Privacy_concerned"):
	os.mkdir(f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\Privacy_concerned")

if not os.path.isdir(f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\IndustrialVal_concerned"):
	os.mkdir(f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\IndustrialVal_concerned")


avg = sum(acc) / len(acc)

alt_depth_start = depth_start
alt_depth_end = depth_end

import shutil


for i in range(len(acc)):
	if acc[i] < avg and i < alt_depth_start * 2:
		if not os.path.isfile(f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\Privacy_concerned\\haberman{i+1}.csv"):
			shutil.copyfile(f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\diff privacy\\Depth={alt_depth_start}\\haberman_generalized{(i%4) + 1}.csv", f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\Privacy_concerned\\haberman{i+1}.csv")

	elif acc[i] >= avg and i < alt_depth_start * 2:
		if not os.path.isfile(f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\Privacy_concerned\\haberman{i+1}.csv"):
			shutil.copyfile(
		f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\diff privacy\\Depth={alt_depth_start}\\haberman_generalized{(i%4) + 1}.csv",
		f"C:\\Users\\AmanH\\PycharmProjects\PPDM\\venv\\DefTech-Hackathon\\IndustrialVal_concerned\\haberman{i+1}.csv")

	if  i >= alt_depth_start * 2:
		alt_depth_start += 2

from gui import frontend
frontend()