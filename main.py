import mesa
import numpy as np
import math

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
    
    def step(self):
        '''
        Sugar Growth function
        '''
        self.amount = min([self.max_sugar, self.amount+1])

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
        
    def step(self):
        self.amount = min([self.max_spice, self.amount +1])
        
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
    
    def sugar(self, pos):
        '''
        used in self.get_sugar_amount()
        '''
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent
        return None
    
    def get_sugar_amount(self, pos):
        '''
        used in self.move() as part of self.calculate_welfare
        '''
        sugar_patch = self.get_sugar(pos)
        if sugar_patch:
            return sugar_patch.amount
        return 0
        
    def spice(self, pos):
        '''
        used in self.get_spice_amount()
        '''
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for agent in this_cell:
            if type(agent) is Spice:
                return agent
        return None
    
    def get_spice_amount(self, pos):
        '''
        used in self.move() as part of self.calculate_welfare
        '''
        spice_patch = self.get_spice(pos)
        if spice_patch:
            return spice_patch.amount
        return 0
    
    def is_occupied_by_other(self, pos):
        '''
        helper function to identify whether the target cell is occupied
        '''
        if pos == self.pos:
            return False
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for a in this_cell:
            if isinstance(a, Trader):
                return True
        return False
    
    def welfare(self, sugar, spice):
        '''
        helper function part 2 self.move()
        '''
        m_total = self.metabolism_sugar + self.metabolism_spice
        return sugar**(self.metabolism_sugar/m_total)*spice**(self.metabolism_spice/m_total)
    
    def move(self):
        '''
        identifies the optimal move for the trader agent
        for each step
        1 - identify all possible moves
        2 - determine which move maximises welfare
        3 - identify the nearest best option
        4 - move
        '''
        
        neighbours = [ i for i in self.model.grid.get_neighborhood(
            self.pos, self.moore, include_center =True, radius = self.vision
        ) if not self.is_occupied_by_other(i)]
        
        welfare_grid = [
            self.calculate_welfare(
                self.sugar + self.get_sugar_amount(pos), 
                self.spice + self.get_spice_amount(pos)) 
            for pos in neighbours
        ]
        
        max_welfare = max(welfare_grid)
        candidate_indices = [i for i in len(welfare_grid)
                          if math.isclose(welfare_grid[i], max_welfare, rel_tol=1e-02)]
        candidate_move = [neighbours[i] for i in candidate_indices]
        current_position = np.array(self.pos)
        distance = [
            np.linalg.norm(current_position - np.array(pos)) for pos in candidate_move
        ]
        min_distance = min(distance)
        candidates_min_max = [
            neighbours[i] for i in range(len(distance)) if 
            math.isclose(distance[i], min_distance, 1e-02)
            ]
        
        self.model.grid.move_agent(self, self.random.choice(candidates_min_max))
        

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
        
    def step(self):
        '''
        Unique step function that does staged activation of sugar and spice
        and then randomly activates traders
        '''
        [sugar.step() for sugar in self.schedule.agents_by_type[Sugar].values()]
        [spice.step() for spice in self.schedule.agents_by_type[Spice].values()]
        trader_shuffle = list(self.schedule.agents_by_type[Trader].values())
        self.random.shuffle(trader_shuffle)
        [agent.move() for agent in trader_shuffle]
        
        
        self.schedule.steps +=1
            
    def run_model(self, step_count = 1000):
        
        for i in range(step_count):
            self.step()


if __name__=="__main__":
    model = SugarscapeG1mt()
    model.sugar_distribution("sugar-map.txt")
