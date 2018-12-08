import pickle
with open("ugv_op_path.pkl","rb") as f:
    a  = pickle.load(f)
print(a)
