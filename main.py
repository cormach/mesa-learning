import mesa
import numpy as np

class Sugar(mesa.Agent):
    '''
    Sugar:
    - contains an amount of sugar
    - grows one amont of sugar at each turn
    '''
    
    def __init__(self):
        pass

class Spice(mesa.Agent):
    '''
    Spice:
    - contains an amount of spice
    - grows one amount of spice
    '''

    def __init__(self):
        pass

class Trader(mesa.Agent):
    '''
    Trader:
    - has a metabolism for sugar and spice
    - harvest and trade sugar and spice
    '''

    def __init__(self):
        pass

class SugarscapeG1mt(mesa.Model):
    '''
    A model class to manage Sugarscape with Traders (G1m)
    grom Growing Artificial Societies by Axtell and Epstein
    '''

    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height

        self.grid = mesa.space.MultiGrid(self.width, self.height, torus = False)
    
    def sugar_distribution(self, file_address):
        sugar_distribution = np.genfromtxt(file_address)



if __name__=="__main__":
    model = SugarscapeG1mt()
    model.sugar_distribution("sugar-map.txt")
