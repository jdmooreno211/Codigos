from Sources.system_os import OperationsSystem
obj_os = OperationsSystem()
data = obj_os.get_json(option=4)
w_xor = obj_os.w_xor(data_json=data)
print(w_xor)