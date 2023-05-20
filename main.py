import mesa
import numpy as np

class Sugar(mesa.Agent):
    '''
    Sugar:
    - contains an amount of sugar
    - grows one amont of sugar at each turn
    '''
    
    def __init__(self, unique_id, model, pos, max_sugar):
        super().__init(unique_id, model)
        self.pos = pos
        self.amount = max_sugar
        self.max_sugar = max_sugar

class Spice(mesa.Agent):
    '''
    Spice:
    - contains an amount of spice
    - grows one amount of spice
    '''

    def __init__(self, unique_id, model, pos, max_spice):
        super().__init__(unique_id, model)
        self.pos = pos
        self.amount = max_spice
        self.max_spice = max_spice
        
class Trader(mesa.Agent):
    '''
    Trader:
    - has a metabolism for sugar and spice
    - harvest and trade sugar and spice
    '''

    def __init__(self, unique_id, model, pos, moore=False,
                 sugar = 0, spice = 0, metabolism_sugar=0,
                 metabolism_spice=0, vision=0):
        super().__init__(unique_id, model)
        self.pos=pos
        self.moore=moore
        self.sugar=sugar
        self.spice = spice 
        self.metabolism_sugar= metabolism_sugar
        self.metabolism_spice=metabolism_spice
        self.vision=vision
        

class SugarscapeG1mt(mesa.Model):
    '''
    A model class to manage Sugarscape with Traders (G1m)
    grom Growing Artificial Societies by Axtell and Epstein
    '''

    def __init__(
        self, file_address, width=50, height=50,
        initial_population = 200, 
        endowment_min = 25, 
        endowment_max = 50,
        metabolism_min = 1,
        metabolism_max = 50,
        vision_min = 1,
        vision_max = 5
        ):
        
        self.width = width
        self.height = height
        self.initial_population = initial_population
        self.endowment_min = endowment_min
        self.endowment_max = endowment_max
        self.metabolism_min = metabolism_min
        self.metabolism_max = metabolism_max
        self.vision_min = vision_min
        self.vision_max = vision_max

        self.grid = mesa.space.MultiGrid(self.width, self.height, torus = False)
        
        self.schedule = mesa.time.RandomActivationbyType(self)
    
        self.sugar_distribution = np.genfromtxt(file_address)
        self.spice_distribution = np.flip(self.sugar_distribution,1)
        
        agent_id = 0
        for _,x,y in self.grid.coord_iter():
            max_sugar = self.sugar_distribution[x,y]
            if max_sugar > 0: 
                sugar = Sugar(agent_id, self, (x,y), max_sugar)
                self.grid.place_agent(sugar, (x,y))
                self.schedule.add(sugar)
                agent_id +=1

        for _,x,y in self.grid.coord_iter():            
            max_spice = self.spice_distribution[x,y]
            if max_spice >0:
                spice = Spice(agent_id, self, (x,y), max_spice)
                self.grid.place_agent(spice, (x,y))
                self.schedule.add(spice)
                agent_id +=1 # we need a unique id
        
        for i in range(self.initial_population):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            # p108 growing artificial societies
            sugar = int(self.random.uniform(self.endowment_min, self.endowment_max+1))
            spice = int(self.random.uniform(self.endowment_min, self.endowment_max+1))
            
            metabolism_sugar = int(self.random.uniform(self.metabolism_min, self.metabolism_max+1))
            metabolism_spice = int(self.random.uniform(self.metabolism_min, self.metabolism_max+1))
            
            vision = int(self.random.uniform(self.vision_min, self.vision_max+1))
            trader = Trader(
                agent_id,
                self,
                (x,y),
                moore = False,
                sugar = sugar,
                spice = spice,
                metabolism_sugar = metabolism_sugar,
                metabolism_spice = metabolism_spice,
                vision = vision)
            self.grid.place_agent(trader, (x,y))
            self.schedule.add(trader)
            agent_id +=1
            
            
    


if __name__=="__main__":
    model = SugarscapeG1mt()
    model.sugar_distribution("sugar-map.txt")
