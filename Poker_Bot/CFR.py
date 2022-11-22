from Model import DeepCFRModel 
class CFR():
    def __init__(self,players):
        self.m_v = [DeepCFRModel for p in range(len(players))]
        self.m_p = DeepCFRModel


    def deepcfr(T,player,K):
        for t in range(1000):
            for p in range(len(player)):
                for k in range(K):
                    
                    traversal([],p,p.cards(),) 
                    



    def traversal(h =[],p,cards,m_v,m_p,t):
        pass
