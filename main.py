import mesa

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

    def __init__(self):
        self.spice = Spice()
        self.sugar = Sugar()
        self.trader = Trader()

if __name__=="__main__":
    model = SugarscapeG1mt()