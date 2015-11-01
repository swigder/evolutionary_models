import string
from weasel.weasel import Weasel


class TestWeasel:
    weasel = Weasel()

    def test_random_letter(self):
        # this test has a chance of failing, but will pass most of the time if we properly distribute
        letters = [self.weasel.random_letter() for i in range((len(string.ascii_uppercase)+1) * 100)]
        for letter in string.ascii_uppercase:
            assert letters.count(letter) >= 75
        assert letters.count(' ') >= 75

    def test_evaluate_child(self):
        assert self.weasel.evaluate_child('METHINKS IT IS LIKE A WEASEL') == len('METHINKS IT IS LIKE A WEASEL')
        assert self.weasel.evaluate_child('METHINKSSIT IS LIKE A WEASEL') == len('METHINKS IT IS LIKE A WEASEL')-1
        assert self.weasel.evaluate_child('LMETHINKS IT IS LIKE A WEASE') == 0

    def test_best_child(self):
        assert self.weasel.best_child(['METHINKS IT IS LIKE A WEASEL', 'METHINKSSIT IS LIKE A WEASEL'],
                                      'LMETHINKS IT IS LIKE A WEASE') == 'METHINKS IT IS LIKE A WEASEL'
