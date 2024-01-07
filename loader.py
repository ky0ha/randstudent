from module import Class
import pickle


def load_data():
    with open("class_data.dat", "rb") as f:
        class_data = pickle.loads(f)
    return class_data

