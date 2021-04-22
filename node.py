import numpy as np
import random
from model import Model
from enum import Enum


class DelegateRule(Enum):
    MOST_COMPETENT = 1
    RANDOM = 2


class Node:
    def __init__(self, name, model):
        self.name = name # integer
        self.model = model
        
        self.edges = []  # social network
        self.weight = 1  # strength of vote
        self.delegate = None  # which node this node has delegated to
        self.eligible_delegates = []  # possible nodes this node can delegate to
        self.delegation_degree = self.model.delegation_degree
        # self.followers = []  # nodes who have delegated to this node
        # self.final_vote = None # if they delegated, what the final delegate votes

        self.delegation_rule = DelegateRule(self.model.delegation_rule)

        self.weight_limit = model.weight_limit
        self.current_weight = 1

        # parameters:
        self.threshold = self.model.threshold_diff  # how much more competent another voter needs to be
        self.competence = self.sample_competence()  # drawn IID from N(mean, SD)
        self.vote = self.sample_vote()  # candidate that voter prefers

    def __str__(self):
        return f"node: {self.name}, competence: {self.competence}, delegate to: {self.delegate.name if self.delegate is not None else None}, vote: {self.vote}"

    def sample_competence(self):
        # return between 0 and 1 inclusive
        mean = self.model.competence_mean
        sd = self.model.competence_sd
        c = np.random.normal(mean, sd)
        if c > 1:
            c = 1
        elif c < 0:
            c = 0

        return c 
    
    def sample_vote(self):
        p = random.random()
        if p < self.competence:
            v = 1  # correct candidate
        else:
            v = 0  # incorrect candidate

        return v

    def _find_root_weight(self, node):
        if node.delegate:
            return self._find_root_weight(node.delegate)
        else:
            return node.current_weight


    # Fills out self.eligible_delegates
    def _find_eligible_delegates(self):
        for neighbor in self.edges:
            if neighbor.competence > self.competence + self.threshold:
                if self._find_root_weight(neighbor) + self.current_weight <= neighbor.weight_limit:
                    self.eligible_delegates.append(neighbor)

    def _add_weight_to_chain(self, weight, node):
        node.current_weight += 1
        if node.delegate:
            node._add_weight_to_chain(1, node.delegate)

    def assign_delegate(self):
        '''
        delegate vote based on self.eligible_delegates and any delegation rules
        rules could be: pick randomly, pick most competent, set default for now

        if self.eligible_delegates is empty, make weight 0
        '''

        rule = self.delegation_rule

        self._find_eligible_delegates()
        chosen = None
        if rule == DelegateRule.MOST_COMPETENT:
            max_competence = 0
            most_competent = None
            
            for d in self.eligible_delegates:
                if d.competence > max_competence:
                    max_competence = d.competence
                    chosen = d
        elif rule == DelegateRule.RANDOM:
            length = len(self.eligible_delegates)
            if length:
                i = np.random.randint(0,length)
                chosen = self.eligible_delegates[i]
        else:
            raise NotImplemented()
        
        if chosen:
            self.delegate = chosen
            self._add_weight_to_chain(1, chosen)

            # d.followers.append(self) # may get rid of or move to graph function
        else:
            self.delegate = None
                
    # def vote(self):
    #     '''
    #     vote for whoever u like most, if your vote was delegated, your weight is 0
    #     '''
    #     # return (v, weight)
    #     pass
