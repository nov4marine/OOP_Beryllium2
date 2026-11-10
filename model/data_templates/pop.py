

class Pop:
    def __init__(self, size, wealth=10, profession=None):
        self.size = size
        self.wealth = wealth # Total wealth, not per capita
        self.wealth_per_capita = wealth
        self.profession = profession

    def split_off_workers(self, amount):
        """
        Encapsulated Logic: The Pop handles its own math.
        It slices off a piece of itself and hands back a shiny new Pop object.
        """
        if amount >= self.size:
            raise ValueError("Cannot split off more workers than exist in this pop!")

        # 1. Reduce my own size
        self.size -= amount

        # 2. Calculate proportional wealth to pass along to the split-off group
        # (If 20% of the pop leaves, they take 20% of the accumulated wealth)
        proportional_wealth = (amount / (self.size + amount)) * self.wealth
        self.wealth -= proportional_wealth

        # 3. Create and return the new aggregate pop
        return Pop(
            size=amount,
            wealth=proportional_wealth
        )
    #TODO: add it to the colony pop registry

    def absorb_pop(self, other_pop):
        """
        Encapsulated Logic: Safely merge another pop into this one.
        """
        self.size += other_pop.size
        self.wealth += other_pop.wealth
        # Explicitly clear the old pop to help prevent bugs
        other_pop.size = 0
        other_pop.wealth = 0
        #TODO: remove from colony pop registry