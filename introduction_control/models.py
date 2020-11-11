from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import itertools
import random

author = 'Charlotte'

doc = """
        The instructions and consent for the control treatment.
        I decided to have them in a separate app so that there can be a waiting page at the beginning of the game app
        where participants wait for an opponent to play (online).
        So the pairing cannot happen before then. Hence a separate app.
"""


class Constants(BaseConstants):
    name_in_url = 'introduction_control'
    players_per_group = 2
    num_rounds = 1

    min_rounds = 2
    proba_next_round = 0.5

    b_high = c(500)
    c_high = c(200)
    dd_high = c(0)

    b_low = c(555)
    c_low = c(222)
    dd_low = c(0)


class Subsession(BaseSubsession):
    """
        This is for the 50% chance of another round. We create a function for clarity below in the creating_session().
        We create a list of different number of rounds that is as long as there are groups.
    """
    def get_random_number_of_rounds(self):
        arbitrary_high_number = 100
        list_num_rounds = []
        for _ in range(arbitrary_high_number):
            number = Constants.min_rounds
            while Constants.proba_next_round < random.random():
                number += 1
            list_num_rounds.append(number)
        return list_num_rounds

    """
    Assigns treatments to pairs of two. First create the treatments (high, low),
    for each groups, assign one treatment to a pair, then the other, then the first one again.
    Then for each player, store the treatment in participant.vars.
    """
    def creating_session(self):
        treatments = itertools.cycle(['high', 'low'])
        for g in self.get_groups():
            g.treatment = next(treatments)
        for p in self.get_players():
            p.participant.vars['treatment'] = p.group.treatment
            print('vars treatment is', p.participant.vars['treatment'])
            # print('id in session', p.participant.id_in_session)  # what the hell does that print??

        """ random last round code. With the function from above, 
                we attribute the different elements in the list to each group."""
        list_num_rounds = self.get_random_number_of_rounds()
        group_number_of_rounds = itertools.cycle(list_num_rounds)
        for g in self.get_groups():
            g.last_round = next(group_number_of_rounds)
            print('New number of rounds', g.last_round)
        for p in self.get_players():
            p.participant.vars['last_round'] = p.group.last_round
            print('vars last_round is', p.participant.vars['last_round'])

# when this is finalised merge together treatment and last_round as they are the same


class Group(BaseGroup):
    """ treatment needs to be defined at the group level so that both player in the group have the same.
       if defined at the player level, then each player will have a different one regardless of pairs/groups """
    treatment = models.StringField()

    """Field of the number of rounds. Each group gets attributed a number of rounds"""
    last_round = models.IntegerField()


class Player(BasePlayer):
    """
        These are all variables that depend on a real person's action.
        The options for the demographics survey & the decisions in the game.
        Any variable defined in Player class becomes a new field attached to the player.
        """
    q1 = models.IntegerField(
        choices=[
            [1, '0 other participants'],
            [2, '1 other participants'],
            [3, '2 other participants']
        ],
        verbose_name='With how many other participant(s) will you be interacting in this study?',
        widget=widgets.RadioSelect
    )

    q2 = models.IntegerField(
        choices=[
            [1, 'There is no bonus possible in this study.'],
            [2, 'My bonus payment depends only on my decisions.'],
            [3, 'My bonus payment depends only on my decision and the decision of the other participant.']
        ],
        verbose_name='What will your bonus payment depend on?',
        widget=widgets.RadioSelect
    )

    q3 = models.IntegerField(
        choices=[
            [1, 'You will earn b-c_high points.'],
            [2, 'You will earn 100 points.'],
            [3, 'Neither will earn additional points.']
        ],
        verbose_name='What amount will you earn if Participant 2 chooses to pay c_high points in order for you to receive b_high points?',
        widget=widgets.RadioSelect
    )

    q4 = models.IntegerField(
        choices=[
            [1, '10%'],
            [2, '50%'],
            [3, '100%']
        ],
        verbose_name='What are the chances that there will be another round after the 20th round?',
        widget=widgets.RadioSelect
    )
    # put these as one??
    q5 = models.IntegerField(
        choices=[
            [1, '10%'],
            [2, '50%'],
            [3, '100%']
        ],
        verbose_name='What are the chances that there will be another round after the 21th round?',
        widget=widgets.RadioSelect
    )

    q6 = models.IntegerField(
        choices=[
            [1, '0 points'],
            [2, '0+b-c points'],  # this need to be benefit high
            [3, '100 points']
        ],
        verbose_name='In Example 1, how many points did Participant 1 earn in total?',
        widget=widgets.RadioSelect
    )

    q7 = models.IntegerField(
        choices=[
            [1, '0 points'],
            [2, '50 points'],
            [3, 'b-c points']  # this need to be benefit high
        ],
        verbose_name='In Example 1, how many points did Participant 2 earn?',
        widget=widgets.RadioSelect
    )

    q8 = models.IntegerField(
        choices=[
            [1, '0 points'],
            [2, '50 points'],
            [3, 'b-c points']  # this need to be benefit low
        ],
        verbose_name='In Example 2, how many points did Participant 2 earn?',
        widget=widgets.RadioSelect
    )