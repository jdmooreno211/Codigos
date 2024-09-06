class Formulas:
    def __init__(self,w = [],list_logical = [], alpha = 0.2):
        self.list_w = w
        self.alfa = alpha
        self.logical = list_logical
# la formula usada para la sumatoria total neta es: [x0*w0+x1*w11+x2*w12]
    def sum_net(self,index):
        z_toria = 0
        ind = 0
        #print(self.logical)
        com_logical_reverse = self.logical[index][::-1]
        #print(self.list_w)
        while ind < len(self.logical)-1:
            z_toria += com_logical_reverse[ind+1] * self.list_w[ind]
            ind += 1
        return z_toria
    #funcion para calcular el error del patron
    def actual_error(self,ob,esp):
        return esp - ob
    #esta funcion es la necargada de reasignar los pesos nuevos, pedimos el error por el cual
    # se reasignaran pesos, y la lista del patron actual de la matriz de compuertas logicas
    def reasing_weigth(self,err_actual,list_x):
        index = 0
        new_weigth = []
        while  index < len(self.list_w):     
            #formula de la reasignacion de pesos   newPeso = wactual + x * alfa * error_actual
            new_weigth.append(round(self.list_w[index] + (list_x[index+1] * self.alfa * err_actual),2))
            index += 1
        return new_weigth
    
        
