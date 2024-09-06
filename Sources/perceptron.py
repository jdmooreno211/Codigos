from .formulas import Formulas
from .compuertas import Compuertas
class Perceptron:
    def __init__(self):
        self.obj_formulas = Formulas()
        self.obj_compuertas = Compuertas()
        self.y0 = []
    def intermediate(self,option,weigth):
        print(option)
        if option < 4:
            self.obj_compuertas.option = option
            self.obj_formulas.logical = self.obj_compuertas.comp()
            self.y0 = self.last_column(list_d=self.obj_formulas.logical)
            error = self.perceptron(list_weigth=weigth)
        else:
            e = []
            for i in range(3):
                if i == 2:
                    self.obj_formulas.logical = self.obj_compuertas.xor()
                elif i == 1:
                    self.obj_formulas.logical = self.obj_compuertas.y2()
                elif i == 0:
                    self.obj_formulas.logical = self.obj_compuertas.y1()
                self.y0 = self.last_column(list_d=self.obj_formulas.logical)
                e.append(self.perceptron(list_weigth=weigth[i]))
            error = e
            error = self.reconver(list_=error)
        return error
    def perceptron(self,list_weigth):
        self.obj_formulas.list_w = list_weigth
        index = 0
        list_error = []
        while index < 4:#se recorre la matriz de las compuertas desde el primer patron hasta el ultimo
            # se llama ala funcion de sumatoria para sacar al suma ponderada  neta
            sumatoria =self.obj_formulas.sum_net(index=index)
            # se hace la validacion de la sumatoria, por si sumatoria es mayo o igual a 0, para asignar el YDp
            if sumatoria > 0:
                sumatoria = 1
            else:
                sumatoria = 0
            #asignamos el valor del error al diccionario
            e = self.obj_formulas.actual_error(ob=sumatoria,esp=self.y0[index])
            list_error.append(e)
            index += 1
        return list_error
    def last_column(self,list_d):
        return [x[-1] for x in list_d]
    def reconver(self,list_):
        dat = []
        for i in range(3):
            for j in range(4):
                dat.append(list_[i][j])
        return dat


