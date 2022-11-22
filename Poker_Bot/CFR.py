from Model import DeepCFRModel 
class CFR():
    def __init__(self,players):
        self.m_v = [[] for p in range(len(players))]
        self.m_p = []
        self.value_model = DeepCFRModel()
        self.strat_model = DeepCFRModel()


    # TODO 
    # figure out how to split infoset to be cards in hand, cards on board and betting postions
    # may need to change how we pass network parametrs through traversal
    # may need infoset map as well
    # find out if models are already initialized to return 0 


    def deepcfr(self,T,player,K):
        for t in range(1000):
            for p in range(len(player)):
                for k in range(K):
                    self.traversal([],p,[pl.card() for pl in player], self.m_v[p], self.m_p)
                # train model  

        # train model b 
        
        pass            

    def traversal(self,h = [], p ,cards,m_v,m_p,t):
        pass
