#
# Make sure to pip install scikit-learn and joblib before running this code.
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import joblib
from configs import data_dir


def train():
    iris = load_iris()  # Getting the training dataset
    data_x = iris['data']
    data_y = iris['target']
    rfc = RandomForestClassifier()
    rfc.fit(data_x, data_y)  # Training the model
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, 'model.joblib'), 'wb') as f:
        joblib.dump(rfc, f)  # Writing the model to file


if __name__ == '__main__':
    train()
