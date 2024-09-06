
class Compuertas:
    def __init__(self,n = 1) :
        self.option = n
    #con esta funcion y con el parametro pasado por el constructor se escoge la matriz que refleja
    # las compiertas logicas or ,And, nan,xor
    def comp(self):
        com = []
        if self.option == 1:
            com = [[0,0,-1,0],[0,1,-1,1],[1,0,-1,1],[1,1,-1,1]]
        elif self.option == 2:
            com = [[0,0,-1,0],[0,1,-1,0],[1,0,-1,0],[1,1,-1,1]]
        elif self.option == 3:
            com = [[0,0,-1,1],[0,1,-1,1],[1,0,-1,1],[1,1,-1,0]]
        return com
    def xor(self):
        return [[0,0,-1,0],
                [1,0,-1,1],
                [0,1,-1,1],
                [0,0,-1,0]]
    def y1(self):
        return [[0,0,-1,0],
                [0,1,-1,1],
                [1,0,-1,0],
                [1,1,-1,0]]
    def y2(self):
        return [[0,0,-1,0],
                [0,1,-1,0],
                [1,0,-1,1],
                [1,1,-1,1]]



        
