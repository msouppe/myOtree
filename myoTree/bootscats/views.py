from ._builtin import Page, WaitPage
from . import models

from datetime import timedelta


class Introduction(Page):
    pass

# Player 1
class Send_INIT(Page):
    form_model = models.Group
    form_fields = ['p1_num']

    def is_displayed(self):
        return self.player.id_in_group == 1 

class Send(Page):
    form_model = models.Group
    form_fields = ['p1_num', 'p1_response']

    def is_displayed(self):
        return self.player.id_in_group == 1   

# Wait Page
class Wait(WaitPage):
    def vars_for_template(self):
        return {'body_text': "Waiting for the other participant."} 

# Player 2
class SendBack(Page):
    form_model = models.Group
    form_fields = ['p2_num', 'p2_response']  
    
    def is_displayed(self):
        return self.player.id_in_group == 2  
    
class ResultsWaitPage(WaitPage):
    
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    pass

page_sequence = [
    Introduction,
    Send_INIT,
    Wait,
    SendBack, 
    Wait,
    Send,
    ResultsWaitPage, 
    Results,
]