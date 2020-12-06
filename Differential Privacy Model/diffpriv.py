from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn.metrics import accuracy_score


# define a function that returns new updated class attributes

def diffpriv(epsilons, dp, X_train, y_train, X_test, y_test, y_arr, y, x):
	survival_status_updated = []
	acc_2d = []
	for d in range(2,12,2):
		acc = []
		survival_status_for_each_depth = []
		for e in epsilons:

			decision = dp.DecisionTreeClassifier(max_depth=d, e=e, s=1, min_samples_leaf=1)
			decision.fit(X_train, y_train)
			a_n = decision.score(X_test, y_test)
			survival_for_each_epsilon =  []
			for z in range(len(np.array(y))):
				survival_for_each_epsilon.append(y_arr[np.argmax(decision.tree_.predict(np.array(x, dtype=np.float32))[z])])
			survival_status_for_each_depth.append(survival_for_each_epsilon)


			a_t = DecisionTreeClassifier(max_depth=d, min_samples_leaf=1).fit(X_train,y_train).predict(X_test)
			a = decision.score(X_test, y_test)
			acc_sc = accuracy_score(y_test, decision.predict(X_test))
			acc_sc_t = accuracy_score(y_test, a_t)
			acc.append(acc_sc)
		acc_2d.append(acc)
		survival_status_updated.append(survival_status_for_each_depth)
		#print(d, decision.tree_.weighted_n_node_samples.shape, decision.tree_.n_node_samples[decision.tree_.children_left != -1], decision.tree_.node_count)


		#plt.plot(epsilons, acc, color=color[d])

	return acc_2d, survival_status_updated
	# plt.legend(color_l)
	# plt.show()

# K cross validation for Differential Privacy



# Plot the average accuracies in the graph
def plot_avg(s_l, ep, k,color, color_l, plt):

	for i in range(len(s_l)):
		plt.plot(ep, s_l[i], color=color[(i+1)*2])
		color_l.append((i+1)*2)
	plt.title(f"for K = {k}")
	plt.legend(color_l)
	plt.show()


def cross_val_average_and_plot(hb, epsilons, dp, y, x,y_arr,color, color_l, plt):
	from sklearn.model_selection import KFold
	for k in range(5, 11):
		acc = []

		kf = KFold(k, shuffle=True, random_state=1)
		for train, test in kf.split(hb):
			X_train = hb.iloc[train, :-1]
			y_train = hb.iloc[train, -1]
			# print(train ,test)
			X_test = hb.iloc[test, :-1]
			y_test = hb.iloc[test, -1]
			acc.append(diffpriv(epsilons, dp, X_train, y_train, X_test, y_test, y_arr, y, x)[0])
		acc_re = np.array(acc)
		# print(acc_re.shape)
		# print(acc_re)
		s_main = []
		for i in range(acc_re.shape[1]):
			# s_i = []
			s_l = []
			for j in range(acc_re.shape[2]):
				s_j = 0

				for m in range(acc_re.shape[0]):
					s_j += acc[m][i][j]

				s_l.append(s_j / k)
			s_main.append(s_l)

		#plot_avg(s_main, epsilons, k,color, color_l, plt)

