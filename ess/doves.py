import random

WASTE_TIME_POINTS = -10
INJURY_POINTS = -100
WIN_FOOD_POINTS = 50

TOTAL = 100


class Entity:
    def __init__(self):
        self.score = 0

    def update_score(self, points):
        self.score += points

    def fight(self, other):
        pass

    def __repr__(self):
        return "Type: {}, Score: {}".format(type(self).__name__, self.score)

    def __str__(self):
        return self.__repr__()


class Dove(Entity):
    def fight(self, other):
        if type(other) is Dove:
            self.update_score(WASTE_TIME_POINTS)
            other.update_score(WASTE_TIME_POINTS)
            winner = random.choice([self, other])
            winner.update_score(WIN_FOOD_POINTS)
        elif type(other) is Hawk:
            other.update_score(WIN_FOOD_POINTS)


class Hawk(Entity):
    def fight(self, other):
        if type(other) is Hawk:
            winner = random.choice([self, other])
            winner.update_score(WIN_FOOD_POINTS)
            loser = other if self == winner else self
            loser.update_score(INJURY_POINTS)
        elif type(other) is Dove:
            other.fight(self)


class Experiment:
    def __init__(self, entities, kind):
        self.entities = [kind() for _ in range(entities)]

    def round(self):
        for _ in range(100):
            self.fight()
        self.update()

    def fight(self):
        to_fight = list(self.entities)
        while to_fight:
            entity1 = to_fight.pop()
            entity2 = to_fight.pop(random.randrange(len(to_fight)))
            entity1.fight(entity2)

    def update(self):
        # todo the exact update strategy is yet to be defined
        min_score = min(entity.score for entity in self.entities)
        epsilon = 0 if min_score > 0 else -min_score + 1
        dove_score = sum(entity.score + epsilon for entity in self.entities if type(entity) is Dove)
        hawk_score = sum(entity.score + epsilon for entity in self.entities if type(entity) is Hawk)
        total_score = dove_score + hawk_score
        self.entities = [Dove() if random.randrange(total_score) < dove_score else Hawk() for _ in range(TOTAL)]
        doves = sum(1 for entity in self.entities if type(entity) is Dove)
        hawks = TOTAL - doves
        print("Doves: {}, Hawks: {}".format(doves, hawks))

    def invade(self, kind):
        self.entities[0] = kind()


if __name__ == "__main__":
    experiment = Experiment(TOTAL, Dove)
    experiment.round()
    experiment.invade(Hawk)
    for _ in range(1000):  # todo should repeat until an ESS is found
        experiment.round()
