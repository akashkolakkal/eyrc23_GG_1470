'''
*****************************************************************************************
*
*        		===============================================
*           		GeoGuide(GG) Theme (eYRC 2023-24)
*        		===============================================
*
*  This script is to implement Task 1A of GeoGuide(GG) Theme (eYRC 2023-24).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			GG_1470
# Author List:		Akash Kolakkal, Anikesh Kulal, Parth jain, Keshav Jha
# Filename:			task_1a.py
# Functions:	    [`ideantify_features_and_targets`, `load_as_tensors`,
# 					 `model_loss_function`, `model_optimizer`, `model_number_of_epochs`, `training_function`,
# 					 `validation_functions` ]

####################### IMPORT MODULES #######################
import pandas
import torch
import numpy as np
###################### Additional Imports ####################
'''
You can import any additional modules that you require from 
torch, matplotlib or sklearn. 
You are NOT allowed to import any other libraries. It will 
cause errors while running the executable
'''
from torch.utils.data import TensorDataset, DataLoader
import torch.nn.functional as F
from sklearn.preprocessing import StandardScaler
from torch import nn
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

##############################################################

################# ADD UTILITY FUNCTIONS HERE #################

def min_max_scaling(df: pandas.DataFrame):
  scaled_df = (df - df.min())/(df.max() - df.min())
  return scaled_df



##############################################################

def data_preprocessing(task_1a_dataframe):

	''' 
	Purpose:
	---
	This function will be used to load your csv dataset and preprocess it.
	Preprocessing involves cleaning the dataset by removing unwanted features,
	decision about what needs to be done with missing values etc. Note that 
	there are features in the csv file whose values are textual (eg: Industry, 
	Education Level etc)These features might be required for training the model
	but can not be given directly as strings for training. Hence this function 
	should return encoded dataframe in which all the textual features are 
	numerically labeled.
	
	Input Arguments:
	---
	`task_1a_dataframe`: [Dataframe]
						  Pandas dataframe read from the provided dataset 	
	
	Returns:
	---
	`encoded_dataframe` : [ Dataframe ]
						  Pandas dataframe that has all the features mapped to 
						  numbers starting from zero

	Example call:
	---
	encoded_dataframe = data_preprocessing(task_1a_dataframe)
	'''

	#################	ADD YOUR CODE HERE	##################


	
	
	encoded_dataframe = task_1a_dataframe.copy()


	encoded_dataframe['Gender']= encoded_dataframe['Gender'].map({'Male': 1, 'Female': 0})

	encoded_dataframe['Education'] = encoded_dataframe['Education'].map({'Bachelors': 0, 'Masters': 1, 'PHD': 2})

	bool_columns = encoded_dataframe.select_dtypes(include='bool').columns
	encoded_dataframe[bool_columns] = encoded_dataframe[bool_columns].astype(int)

	encoded_dataframe = encoded_dataframe.dropna().drop_duplicates()

	encoded_dataframe = min_max_scaling(encoded_dataframe)

	encoded_dataframe = encoded_dataframe.sample(frac= 1)
	print(encoded_dataframe.info())


	##########################################################

	return encoded_dataframe

def identify_features_and_targets(encoded_dataframe):
	'''
	Purpose:
	---
	The purpose of this function is to define the features and
	the required target labels. The function returns a python list
	in which the first item is the selected features and second 
	item is the target label

	Input Arguments:
	---
	`encoded_dataframe` : [ Dataframe ]
						Pandas dataframe that has all the features mapped to 
						numbers starting from zero
	
	Returns:
	---
	`features_and_targets` : [ list ]
							python list in which the first item is the 
							selected features and second item is the target label

	Example call:
	---
	features_and_targets = identify_features_and_targets(encoded_dataframe)
	'''

	#################	ADD YOUR CODE HERE	##################

	target_col = encoded_dataframe['LeaveOrNot']
	feature_cols = encoded_dataframe.drop('LeaveOrNot', axis = 1)

	feature_cols = pandas.DataFrame(StandardScaler().fit_transform(feature_cols))

	features_and_targets = [feature_cols, target_col]
	# print(target_col)
	
	##########################################################

	return features_and_targets


def load_as_tensors(features_and_targets):

	''' 
	Purpose:
	---
	This function aims at loading your data (both training and validation)
	as PyTorch tensors. Here you will have to split the dataset for training 
	and validation, and then load them as as tensors. 
	Training of the model requires iterating over the training tensors. 
	Hence the training sensors need to be converted to iterable dataset
	object.
	
	Input Arguments:
	---
	`features_and targets` : [ list ]
							python list in which the first item is the 
							selected features and second item is the target label
	
	Returns:
	---
	`tensors_and_iterable_training_data` : [ list ]
											Items:
											[0]: X_train_tensor: Training features loaded into Pytorch array
											[1]: X_test_tensor: Feature tensors in validation data
											[2]: y_train_tensor: Training labels as Pytorch tensor
											[3]: y_test_tensor: Target labels as tensor in validation data
											[4]: Iterable dataset object and iterating over it in 
												 batches, which are then fed into the model for processing

	Example call:
	---
	tensors_and_iterable_training_data = load_as_tensors(features_and_targets)
	'''

	#################	ADD YOUR CODE HERE	##################
	
	split = int(features_and_targets[0].shape[0] * 0.95)
	
	X_train_df, X_test_df = features_and_targets[0][:split], features_and_targets[0][split:]

	Y_train_df, Y_test_df = features_and_targets[1][:split], features_and_targets[1][split:]

	X_train_tensor = torch.tensor(X_train_df.values, dtype=torch.float32)
	X_test_tensor = torch.tensor(X_test_df.values, dtype=torch.float32)
	Y_train_tensor = torch.tensor(Y_train_df.values, dtype=torch.float32).unsqueeze(1)
	Y_test_tensor = torch.tensor(Y_test_df.values, dtype=torch.float32).unsqueeze(1)


	dataset = TensorDataset(X_train_tensor, Y_train_tensor)

	iterable_training_data = DataLoader(dataset, batch_size = 1)



	tensors_and_iterable_training_data = [X_train_tensor, X_test_tensor, Y_train_tensor, Y_test_tensor, iterable_training_data]

	print(Y_test_tensor.shape)

	##########################################################

	return tensors_and_iterable_training_data

class Salary_Predictor(torch.nn.Module):
	'''
	Purpose:
	---
	The architecture and behavior of your neural network model will be
	defined within this class that inherits from nn.Module. Here you
	also need to specify how the input data is processed through the layers. 
	It defines the sequence of operations that transform the input data into 
	the predicted output. When an instance of this class is created and data
	is passed through it, the `forward` method is automatically called, and 
	the output is the prediction of the model based on the input data.
	
	Returns:
	---
	`predicted_output` : Predicted output for the given input data
	'''
	def __init__(self):
		super(Salary_Predictor, self).__init__()
		'''
		Define the type and number of layers
		'''
		#######	ADD YOUR CODE HERE	#######
		self.linear1 = nn.Linear(6, 100)
		self.linear2 = nn.Linear(100, 50)
		self.linear3 = nn.Linear(50, 1)
		self.relu = nn.ReLU()
		self.sigmoid = nn.Sigmoid()

		
		###################################	

	def forward(self, x):
		'''
		Define the activation functions
		'''
		#######	ADD YOUR CODE HERE	#######


		x = self.l1(x)
		x = self.relu(x)
		x = self.l2(x)
		x = self.relu(x)
		x = self.l3(x)
		predicted_output = self.sigmoid(x)
		
		x = self.relu(self.linear1(x))
		x = self.relu(self.linear2(x))
		x = self.linear3(x)
		predicted_output = self.sigmoid(x)
		
		###################################

		return predicted_output

def model_loss_function():
	'''
	Purpose:
	---
	To define the loss function for the model. Loss function measures 
	how well the predictions of a model match the actual target values 
	in training data.
	
	Input Arguments:
	---
	None

	Returns:
	---
	`loss_function`: This can be a pre-defined loss function in PyTorch
					or can be user-defined

	Example call:
	---
	loss_function = model_loss_function()
	'''
	#################	ADD YOUR CODE HERE	##################

	loss_function = torch.nn.BCELoss()
	
	##########################################################
	
	return loss_function

def model_optimizer(model):
	'''
	Purpose:
	---
	To define the optimizer for the model. Optimizer is responsible 
	for updating the parameters (weights and biases) in a way that 
	minimizes the loss function.
	
	Input Arguments:
	---
	`model`: An object of the 'Salary_Predictor' class

	Returns:
	---
	`optimizer`: Pre-defined optimizer from Pytorch

	Example call:
	---
	optimizer = model_optimizer(model)
	'''
	#################	ADD YOUR CODE HERE	##################

	optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

	##########################################################

	return optimizer

def model_number_of_epochs():
	'''
	Purpose:
	---
	To define the number of epochs for training the model

	Input Arguments:
	---
	None

	Returns:
	---
	`number_of_epochs`: [integer value]

	Example call:
	---
	number_of_epochs = model_number_of_epochs()
	'''
	#################	ADD YOUR CODE HERE	##################

	number_of_epochs = 100

	##########################################################

	return number_of_epochs

def training_function(model, number_of_epochs, tensors_and_iterable_training_data, loss_function, optimizer):
	'''
	Purpose:
	---
	All the required parameters for training are passed to this function.

	Input Arguments:
	---
	1. `model`: An object of the 'Salary_Predictor' class
	2. `number_of_epochs`: For training the model
	3. `tensors_and_iterable_training_data`: list containing training and validation data tensors 
											 and iterable dataset object of training tensors
	4. `loss_function`: Loss function defined for the model
	5. `optimizer`: Optimizer defined for the model

	Returns:
	---
	trained_model

	Example call:
	---
	trained_model = training_function(model, number_of_epochs, iterable_training_data, loss_function, optimizer)

	'''	
	#################	ADD YOUR CODE HERE	##################

	for epoch in range(number_of_epochs):
		for inputs, targets in tensors_and_iterable_training_data[4]:
			optimizer.zero_grad()

			predictions = model(inputs)

			loss = loss_function(predictions, targets)

			loss.backward()
			optimizer.step()
		
		if epoch % 10 == 0:
			print(f'Epoch {epoch} / {number_of_epochs} : Loss = {loss.item()}')
			
	
	trained_model = model
	print("Training Complete")
		
	##########################################################

	return trained_model

def validation_function(trained_model, tensors_and_iterable_training_data):
	'''
	Purpose:
	---
	This function will utilise the trained model to do predictions on the
	validation dataset. This will enable us to understand the accuracy of
	the model.

	Input Arguments:
	---
	1. `trained_model`: Returned from the training function
	2. `tensors_and_iterable_training_data`: list containing training and validation data tensors 
											 and iterable dataset object of training tensors

	Returns:
	---
	model_accuracy: Accuracy on the validation dataset

	Example call:
	---
	model_accuracy = validation_function(trained_model, tensors_and_iterable_training_data)

	'''	
	#################	ADD YOUR CODE HERE	##################

	with torch.no_grad():
		predictions = trained_model(tensors_and_iterable_training_data[1])
		correct = (predictions > 0.5) == tensors_and_iterable_training_data[3]
		model_accuracy = correct.float().mean().item()

	##########################################################

	return model_accuracy

########################################################################
########################################################################
######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS FUNCTION #########	
'''
	Purpose:
	---
	The following is the main function combining all the functions
	mentioned above. Go through this function to understand the flow
	of the script

'''
if __name__ == "__main__":

	# reading the provided dataset csv file using pandas library and 
	# converting it to a pandas Dataframe
	task_1a_dataframe = pandas.read_csv('task_1a_dataset.csv')

	# data preprocessing and obtaining encoded data
	encoded_dataframe = data_preprocessing(task_1a_dataframe)

	# selecting required features and targets
	features_and_targets = identify_features_and_targets(encoded_dataframe)

	# obtaining training and validation data tensors and the iterable
	# training data object
	tensors_and_iterable_training_data = load_as_tensors(features_and_targets)
	
	# model is an instance of the class that defines the architecture of the model
	model = Salary_Predictor()

	# obtaining loss function, optimizer and the number of training epochs
	loss_function = model_loss_function()
	optimizer = model_optimizer(model)
	number_of_epochs = model_number_of_epochs()

	# training the model
	trained_model = training_function(model, number_of_epochs, tensors_and_iterable_training_data, 
					loss_function, optimizer)

	# validating and obtaining accuracy
	model_accuracy = validation_function(trained_model,tensors_and_iterable_training_data)
	print(f"Accuracy on the test set = {model_accuracy}")

	X_train_tensor = tensors_and_iterable_training_data[0]
	x = X_train_tensor[0]
	jitted_model = torch.jit.save(torch.jit.trace(model, (x)), "task_1a_trained_model.pth")
