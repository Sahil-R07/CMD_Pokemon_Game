import random
import pickle

class Move:
    def __init__(self, name, mtype, power, accuracy, category, effect=None):
        self.name = name
        self.mtype = mtype
        self.power = power
        self.accuracy = accuracy
        self.category = category
        self.effect = effect

    def apply_effect(self, target):
        if self.effect:
            self.effect(target)

#For full code please mail me to : githubspam07@gmail.com

