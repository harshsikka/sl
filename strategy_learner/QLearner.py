"""
Template for implementing QLearner  (c) 2015 Tucker Balch
"""
## Name: Harsh Sikka UserID: hsikka3
import numpy as np
import random as rand

class QLearner(object):

    def author(self):
        return 'hsikka3'

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.num_states, self.num_actions,self.alpha, self.gamma = num_states, num_actions, alpha, gamma
        self.rar, self.radr, self.s, self.a, self.dyna = rar, radr, 0, 0, dyna
        self.verbose = verbose
        self.Qtable = np.zeros((self.num_states, self.num_actions))

        ## setup for Dyna
        self.Tcount = np.ones((self.num_states, self.num_actions, self.num_states)) * .00001

        #test professors experience way
        self.experience = []

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """

        possible_a = self.num_actions - 1
        self.s = s

        random_action = rand.randint(0, possible_a)

        max_a_value = np.amax(self.Qtable[s, :])
        count = 0

        for i in self.Qtable[s, :]:
            if i == max_a_value:
                determined_action = count
            count+=1

        random_chance = np.random.uniform(0.0, 1.0)

        if (self.rar > random_chance):
            self.a = random_action
            action = random_action
        else:
            self.a = determined_action
            action = determined_action
        

        if self.verbose: print "s =", s,"a =",action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """

        dyna_count = self.dyna
        previous_s = self.s
        previous_a = self.a
        possible_a = self.num_actions - 1

        max_a_value = np.amax(self.Qtable[s_prime, :])

        count = 0
        for i in self.Qtable[s_prime, :]:
            if i == max_a_value:
                a_prime = count
            count+=1

        random_action = rand.randint(0, possible_a)
        random_chance = np.random.uniform(0.0, 1.0)
        
        if (self.rar > random_chance):
            action = random_action
        else:
            action = a_prime
        

        self.Qtable[previous_s,previous_a] = (1 - self.alpha) * self.Qtable[previous_s,previous_a] + self.alpha * (r + self.gamma * self.Qtable[s_prime, action])
        
        if dyna_count > 0:
            self.Tcount[previous_s, previous_a, s_prime] += 1

            if(self.Tcount.sum() > 1000):
                for i in range(0,dyna_count):

                    dyna_tuple = np.random.randint(0, len(self.experience))
                    dyna_state = self.experience[dyna_tuple][0]
                    dyna_action = self.experience[dyna_tuple][1]
                    dyna_s_prime = self.experience[dyna_tuple][2]
                    dyna_reward = self.experience[dyna_tuple][3]

                    
                    # dyna_old_value = (1 - self.alpha) * self.Qtable[dyna_state,dyna_action]
                    # dyna_new_value = self.alpha * (dyna_reward + self.gamma * np.max(self.Qtable[dyna_s_prime]))
                    
                    self.Qtable[dyna_state, dyna_action] = (1 - self.alpha) * self.Qtable[dyna_state,dyna_action] + self.alpha * (dyna_reward + self.gamma * np.max(self.Qtable[dyna_s_prime]))
        
        self.experience.append((previous_s,previous_a,s_prime,r))

        self.s = s_prime # setting new state
        self.a = action # setting new action

        self.rar = self.rar * self.radr # decaying rar

        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
    
    
    
    
    
    
