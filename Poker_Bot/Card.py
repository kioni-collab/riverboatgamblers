from xmlrpc.client import boolean



class card:
    def __init__(self,suit,rank): 
        self.suit = suit
        self.rank = rank
    def __repr__(self) -> str:
        return f"card({self.suit}, {self.rank})"
    def __eq__(self,other) -> bool:
        if isinstance(other,card):
            return (self.suit == other.suit) and (self.rank == other.rank)
        else:
            return False
    def __neq__(self,other) -> bool:
        return not self.__eq__(other)
    def __hash__(self):
        return hash(self.__repr__())
    def __str__(self) -> str:
        return self.__repr__()

