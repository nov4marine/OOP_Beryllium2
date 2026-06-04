from dataclasses import dataclass

@dataclass
class ResourceSlot:
    name: str
    quantity: float = 0.0
    max_capacity: float = 1000.0
    base_price: float = 10.0
    current_price: float = 10.0

class Colony:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        
        # The "Filing Cabinet" of Resources (Dictionary of Dataclasses)
        self.stockpile = {
            "Food": ResourceSlot("Food", base_price=1.0),
            "Energy": ResourceSlot("Energy", base_price=1.0),
            "Minerals": ResourceSlot("Minerals", base_price=1.0),
            "Alloys": ResourceSlot("Alloys", base_price=10.0),
            "Consumer Goods": ResourceSlot("Consumer Goods", base_price=5.0)
        }

        # The Lists (Standardized Forms)
        self.buildings = {}  # Now a Dict per your Victoria 3 plan!
        self.pops = []       # Stays a list for diversity
        self.construction_queue = [] 
        
        # Essential Meta-Data
        self.stability = 100

    def add_building_to_colony(self, colony, building_name, levels=1):
        if building_name not in BUILDING_PROTOTYPES:
            print(f"Error: {building_name} not found.")
            return

        # 1. Create a unique instance from the prototype
        new_building = copy.deepcopy(BUILDING_PROTOTYPES[building_name])

        # 2. Set the instance-specific data
        new_building.levels = levels
        new_building.cash_reserves = 1000.0  # Starting seed money

        # 3. Add to the colony dictionary
        colony.buildings[building_name] = new_building


class LaborMarketManager:
    def __init__(self):
        # Maps Job -> List of AggregatePops
        self.employment_map = {}

    def move_workers(self, from_job, to_job, amount):
        """
        The Manager coordinates the transition between the jobs
        without doing any of the internal pop math.
        """
        # 1. Find the source pop working at the old job
        source_pop = self.employment_map[from_job][0]  # Simplified for example

        # 2. Tell the pop to split itself. The pop does the internal math!
        moving_pop = source_pop.split_off_workers(amount)

        # 3. Check if the destination job already has a pop of this type
        existing_pop = self._find_matching_pop_at_job(to_job, moving_pop.profession)

        if existing_pop:
            # Tell the existing pop to absorb the moving group
            existing_pop.absorb_pop(moving_pop)
        else:
            # No matching pop exists, just add this new one to the job's list
            self.employment_map[to_job].append(moving_pop)
