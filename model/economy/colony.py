from dataclasses import dataclass
import copy 


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

        # Components!
        self.labor_market = LaborMarket(self)
        
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

    def on_monthly_update(self):
        print("starting update...")
        self.labor_market.run_market()
        self.building_manager.produce(colony)
        self.financial_manager.pay_wages(colony)
        self.financial_manager.process_consumption(colony)
        self.market_manager.update_prices(colony)
        print("monthly tick successfully completed.")

class LaborMarket:
    def __init__(self, colony):
        self.colony = colony
        
        # Create a fallback "Unemployment" job that belongs to the market, not a building
        self.unemployment_job = Job(
            name="Unemployed", 
            max_positions=float('inf'),  # Can hold infinite pops
            current_wage=0.0, 
            profession_type="None"
        )
        
        # Master Record: Job Object -> List of Pops
        # Seed it with the unemployment job immediately
        self.employment_map = {self.unemployment_job: []}
        self.unemployment_rate = 0
        self.job_offers = {}

    def update_snapshot(self):
        """Reconciles the job market with the physical colony state."""
        current_jobs = {self.unemployment_job} # Keep unemployment safe from deletion

        # 1. Gather all legitimate jobs from physical buildings
        for building in self.colony.buildings:
            for job in building.jobs:
                current_jobs.add(job)
                if job not in self.employment_map:
                    self.employment_map[job] = []

        # 2. Clean up jobs from buildings that were demolished
        dead_jobs = set(self.employment_map.keys()) - current_jobs
        for dead_job in dead_jobs:
            # Dump displaced pops directly into the unemployment job
            displaced_pops = self.employment_map.pop(dead_job, [])
            self.employment_map[self.unemployment_job].extend(displaced_pops)

        # 3. Clear and rebuild job offers for actual businesses looking to hire
        self.job_offers.clear()
        for job, workers in self.employment_map.items():
            if job == self.unemployment_job:
                continue # Nobody "hires" for unemployment
                
            open_slots = job.max_positions - len(workers)
            if open_slots > 0:
                self.job_offers[job] = {
                    "quantity_to_hire": open_slots,
                    "wage": job.current_wage,
                    "profession": job.profession_type
                }

    def calculate_unemployment(self):
        total_pop = sum(pop.size for pop in self.colony.pops)
        unemployed_pop = sum(pop.size for pop in self.employment_map[self.unemployment_job])
        self.unemployment_rate = (unemployed_pop / total_pop)

    def employer_response(self):
        if self.unemployment_rate < 0.05:
            pass

        if self.unemployment_rate > 0.05:
            for building in self.colony.buildings:
                building.evaluate_labor_market()
                
        # step 1: update structural changes (ie new building is constructed)
        # Step 2: assess unemployment
        # Step 3: calculate employer response and hiring
        # Step 4: shift pops into jobs
        # Step 5: process layoffs #this after step 4 results in structural unemployment

    def run_market(self):
        pass

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
