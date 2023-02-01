import pickle

with open("html_content.pickle", "rb") as f:
    x = pickle.load(f)

print(x)
