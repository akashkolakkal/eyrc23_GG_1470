import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

# Function to load and preprocess the dataset
def data_preprocessing(task_1a_dataframe):
    # Drop non-numeric columns (if any)
    task_1a_dataframe = task_1a_dataframe.select_dtypes(include=['float64', 'float32', 'float16', 'complex64', 'complex128', 'int64', 'int32', 'int16', 'int8', 'uint8', 'bool'])

    # Convert the target variable to a binary format (0 or 1)
    task_1a_dataframe['LeaveOrNot'] = task_1a_dataframe['LeaveOrNot'].astype(int)

    return task_1a_dataframe




# Function to identify features and targets
def identify_features_and_targets(encoded_dataframe):
    features = encoded_dataframe.drop(columns=['LeaveOrNot'])
    target = encoded_dataframe['LeaveOrNot']
    return [features.values, target.values]

# Function to load data as tensors
def load_as_tensors(features_and_targets):
    features, target = features_and_targets

    # Split the dataset into training and validation sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Convert data to PyTorch tensors
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    return [X_train_tensor, X_test_tensor, y_train_tensor, y_test_tensor]


# Define the neural network architecture
class EmployeeClassifier(nn.Module):
    def __init__(self, input_size):
        super(EmployeeClassifier, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.sigmoid(out)
        return out

# Function to define the loss function
def model_loss_function():
    return nn.BCELoss()

# Function to define the optimizer
def model_optimizer(model):
    return optim.Adam(model.parameters(), lr=0.001)

# Function to define the number of epochs
def model_number_of_epochs():
    return 10

# Function for training the model
def training_function(model, number_of_epochs, tensors_and_iterable_training_data, loss_function, optimizer):
    X_train_tensor, _, y_train_tensor, train_loader = tensors_and_iterable_training_data

    for epoch in range(number_of_epochs):
        model.train()
        total_loss = 0.0
        for i, (inputs, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_function(outputs, labels.unsqueeze(1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f'Epoch [{epoch + 1}/{number_of_epochs}], Loss: {total_loss / (i + 1):.4f}')

    return model

# Function for model validation
def validation_function(trained_model, tensors_and_iterable_training_data):
    _, X_test_tensor, _, y_test_tensor, _ = tensors_and_iterable_training_data
    trained_model.eval()
    with torch.no_grad():
        outputs = trained_model(X_test_tensor)
        predicted = (outputs >= 0.5).squeeze().cpu().numpy()
        accuracy = np.mean((predicted == y_test_tensor.numpy()))
    return accuracy

# Main function
def main():
    # Load the dataset
    task_1a_dataframe = pd.read_csv('task_1a_dataset.csv')

    # Data preprocessing
    encoded_dataframe = data_preprocessing(task_1a_dataframe)

    # Identify features and targets
    features_and_targets = identify_features_and_targets(encoded_dataframe)

    # Load data as tensors
    tensors_and_iterable_training_data = load_as_tensors(features_and_targets)

    # Initialize the model
    input_size = features_and_targets[0].shape[1]
    model = EmployeeClassifier(input_size)

    # Define loss function and optimizer
    loss_function = model_loss_function()
    optimizer = model_optimizer(model)

    # Define the number of training epochs
    number_of_epochs = model_number_of_epochs()

    # Train the model
    trained_model = training_function(model, number_of_epochs, tensors_and_iterable_training_data, loss_function, optimizer)

    # Validate the model
    accuracy = validation_function(trained_model, tensors_and_iterable_training_data)
    print(f'Validation Accuracy: {accuracy * 100:.2f}%')

    # Save the trained model
    torch.jit.save(trained_model, 'task_1a_trained_model.pth')

if __name__ == '__main__':
    main()
