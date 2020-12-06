from tkinter import *
from tkinter import messagebox
from sql import output_true_results, output_randomized_results



def frontend():
	root = Tk()


	dataset_label = Label(root, text="Select Dataset")

	query_label = Label(root, text="SELECT ")

	entry_q = Entry(root)

	query_label_2 = Label(root, text=" FROM haberman WHERE ")

	entry_c = Entry(root)



	dataset_label.grid(row=0)
	query_label.grid(row=1, column=0)
	entry_q.grid(row=1, column=1)
	query_label_2.grid(row=1, column=2)
	entry_c.grid(row=1, column=3)





	def callback():
		q_true_results = output_true_results(entry_q.get(), entry_c.get())
		q_results = output_randomized_results(entry_q.get(), entry_c.get())
		if "Error" not in q_true_results:
			messagebox.showinfo("True", message=q_true_results)

		else:
			messagebox.showerror("Error", message=q_true_results)

		if 'Error' not in q_results:
			messagebox.showinfo("False", message=q_results)
		# else:
		# 	messagebox.showerror("Error", message=q_results)

	button = Button(root, text="Submit", command=callback)
	button.grid(row=2, column=2)
	#root.bind('<Return>', callback)


	root.mainloop()

	# SELECT COUNT(Survival) FROM haberman WHERE  ;

frontend()