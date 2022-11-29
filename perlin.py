import random

class Perlin:
    def __init__(self):
        self.gradients = []
        self.lowerBound = 0
        
    def __ease(self, x):
        """ 
        This is an ease function that smoothes out the curve at integer points 
        Returns the interpolaton amount
        """
        return 6*x**5-15*x**4+10*x**3
    
    def __lerp(self, start, stop, amt):
        """ Linear interpolation """
        return amt*(stop-start)+start
    
    def discard(self, amount):
        """ """
        gradientsToDiscard = int(amount+self.lowerBound%1)
        self.gradients = self.gradients[gradientsToDiscard:]
        self.lowerBound += amount
    
    def valueAt(self, t):
        if(t<self.lowerBound):
            print("ERROR: Input parameter out of bounds!")
            return
        
        # Add to gradients until it covers t
        while t >= len(self.gradients)-1+self.lowerBound:
            self.gradients.append(random.uniform(-1, 1))

        discarded = int(self.lowerBound) # getting number of gradients that have been discarded
        # Compute products between surrounding gradients and distances from them
        d1 = (t-t//1)
        d2 = d1-1
        a1 = self.gradients[(int)(t//1)-discarded]*d1
        a2 = self.gradients[(int)(t//1+1)-discarded]*d2

        amt = self.__ease(d1) #amt is the interpolation amount

        return self.__lerp(a1,a2,amt)