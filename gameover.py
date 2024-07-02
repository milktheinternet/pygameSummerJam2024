from menus import Menu

POP_MSGS = {
    0:"YOU HAVE FAILED THE UNIVERSE",
    1:"IT MUST BE LONELY AT THE TOP",
    2:"IS THIS THE NEW ADAM AND EVE?",
    3:"A FEW PEOPLE TO RESTART THE UNIVERSE",
    10:"A FAMILY AFTER THE UNIVERSE",
    25:"THE FINAL VILLAGE?",
    50:"A TIGHTLY KNIT COMMUNE HAS STARTED",
    100:"A TOWN THAT CONSISTS OF THE ONLY LIFE IN THE UNIVERSE",
    200:"REALITY HAS A SECOND CHANCE",
    300:"HUNDREDS OF PEOPLE NOW HAVE HOPE",
    500:"YOU COULD HAVE SAVED MORE",
    1000:"A KINGDOM STANDS AT THE EDGE OF THE UNIVERSE",
    2000:"A REAL CONTENDER FOR A FRESH START",
    3000:"BRING THE UNIVERSE HERE, THEY SAID",
    10000:"MISSION SUCCESS"
}


def get_pop_msg(end_pop):
    for pop, msg in reversed(POP_MSGS.items()):
        if end_pop >= pop:
            return msg


def get_highscore():
    return int(open("assets/highscore").read().strip())


def set_highscore(score):
    return open("assets/highscore",'w').write(str(score))


class GameOver(Menu):
    def __init__(self, dis, end_pop, abandoned, visited):
        hs = get_highscore()
        if end_pop > hs:
            hs = end_pop
            set_highscore(hs)
        options = {
            f"YOU RESCUED {end_pop} LIFE FORMS":self.start,
            get_pop_msg(end_pop):self.start,
            " ":self.start,
            f"HIGH SCORE: {hs}":self.start,
            "  ":self.start,
            f"VISITED {visited} PLANETS":self.start,
            f"ABANDONED {abandoned}":self.start,
            "   ":self.start,
            "CONTINUE":None
        }

        super().__init__(options, dis)
        self.make_btns()