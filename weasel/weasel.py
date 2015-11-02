import string
import random


class Weasel:
    chance_of_change = .05
    change_target = True
    children_per_generation = 100
    target = 'METHINKS IT IS LIKE A WEASEL'

    def generate_weasel(self):
        parent = ''.join(self.random_letter() for i in range(len(self.target)))
        evaluation = self.evaluate_child(parent)
        generation = 0
        while evaluation != len(self.target):
            self.print_generation(generation, parent, evaluation)
            generation += 1
            children = [self.reproduce(parent) for i in range(self.children_per_generation)]
            parent = self.best_child(children, parent)
            evaluation = self.evaluate_child(parent)
        self.print_generation(generation, parent, evaluation)
        print('Evolution to target {} from random initial junk took {} generations with {} children generation and a '
              'mutation rate of {} per letter per generation'.format(self.target, generation,
                                                                     self.children_per_generation,
                                                                     self.chance_of_change))

    def reproduce(self, parent):
        child = ''
        for i, letter in enumerate(parent):
            child += letter if (not self.change_target and letter == self.target[i]) \
                               or random.random() > self.chance_of_change else self.random_letter()
        return child

    def evaluate_child(self, child):
        score = 0
        for a, b in zip(child, self.target):
            if a == b:
                score += 1
        return score

    def best_child(self, children, parent):
        return max(children + [parent], key=(lambda x: self.evaluate_child(x)))

    @staticmethod
    def random_letter():
        return random.choice(string.ascii_uppercase + ' ')

    @staticmethod
    def print_generation(generation, value, evaluation):
        print('{}: {} -- score {}'.format(generation, value, evaluation))

if __name__ == '__main__':
    Weasel().generate_weasel()
