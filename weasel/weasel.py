import string
import random
import argparse


class Weasel:
    def __init__(self,
                 target='METHINKS IT IS LIKE A WEASEL',
                 mutation_rate=.05,
                 fix_target=False,
                 children_per_generation=100):
        self.target = target
        self.mutation_rate = mutation_rate
        self.fix_target = fix_target,
        self.children_per_generation = children_per_generation

    def generate_weasel(self):
        parent = ''.join(self.random_letter() for i in range(len(self.target)))
        evaluation = self.evaluate_child(parent)
        generation = 0
        generations = [{'generation': generation, 'value': parent, 'evaluation': evaluation}]
        while evaluation != len(self.target):
            generation += 1
            children = [self.reproduce(parent) for i in range(self.children_per_generation)]
            parent = self.best_child(children, parent)
            evaluation = self.evaluate_child(parent)
            generations.append({'generation': generation, 'value': parent, 'evaluation': evaluation})
        return generations

    def generate_weasel_with_output(self):
        generations = self.generate_weasel()
        for generation in generations:
            self.print_generation(generation.generation, generation.value, generation.evaluation)
        print('Evolution to target {} from random initial junk took {} generations with {} children generation and a '
              'mutation rate of {} per letter per generation'.format(self.target, len(generations),
                                                                     self.children_per_generation,
                                                                     self.mutation_rate))

    def reproduce(self, parent):
        child = ''
        for i, letter in enumerate(parent):
            child += letter if self.fix_target and letter == self.target[i] \
                               or random.random() > self.mutation_rate else self.random_letter()
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
    parser = argparse.ArgumentParser(description='Generate a phrase by mutation.')

    parser.add_argument('target', type=str, help='phrase to generate', nargs='?',
                        default='METHINKS IT IS LIKE A WEASEL')
    parser.add_argument('-m', '--mutation_rate', type=float, help='chance of change per letter per generation',
                        default=.05)
    parser.add_argument('-f', '--fix_target', type=bool, help='prevent letter from changing once it matches the target',
                        default=False)
    parser.add_argument('-c', '--children', type=int, help='number of children per generation', default=100)

    args = parser.parse_args()

    Weasel(args.target.upper(), args.mutation_rate, args.fix_target, args.children).generate_weasel()
