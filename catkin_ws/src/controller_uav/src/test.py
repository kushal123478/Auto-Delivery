import pickle
with open("uav_op_path.pkl","rb") as f:
    a  = pickle.load(f)
print(a)
