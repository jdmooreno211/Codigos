import os
import json
class OperationsSystem:
    def __init__(self):
        self.path = os.path.join(os.getcwd(),'historials')
    def get_json(self,option):
        name_path = self.return_option_name(option=option)
        print(self.path+name_path)
        with open(self.path + name_path, 'r') as file:
            data = json.load(file)
        return data
    def search_doc(self,name):
        return os.path.join(os.getcwd(),name)
    def return_option_name(self,option):
        name = '\historial_'
        if option == 1:
            name += 'or'
        elif option == 2:
            name += 'and'
        elif option == 3:
            name += 'nan'
        elif option == 4:
            name += 'xor'
        return name + '.json'
    def w_xor(self,data_json):
        w = []
        for compuerta in data_json.values():
            for key,data in compuerta.items():
                if 'Pesos ideales: ' == key:
                    list_w = [x for x in data.values()]
                    w.append(list_w)
        return w



    