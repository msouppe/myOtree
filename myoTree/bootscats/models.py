import csv
import random

from otree.api import models
from django.contrib.contenttypes.models import ContentType
from otree.constants import BaseConstants
from otree.models import BaseGroup, BasePlayer, BaseSubsession

doc = """
This is a bootscats game.
"""
global p1_check, p2_check 
global p1_response, p2_response

class Constants(BaseConstants):
	name_in_url = 'bootscats'
	players_per_group = 2
	num_rounds = 2

	instructions_template = 'bootscats/Instructions.html'

class Subsession(BaseSubsession):
	pass

class Group(BaseGroup):
	p1_num = models.CharField(doc="""Number from p1 to p2""")
	p1_response = models.CharField(doc="""p1 response""")
	p1_check = models.CharField()
	p2_num = models.CharField(doc="""Number from p2 to p1""")
	p2_response = models.CharField(doc="""p2 response""")
	p2_check = models.CharField()
	is_winner = models.BooleanField(initial=True)
	p1_score = models.IntegerField(default=0)
	p2_score = models.IntegerField(default=0)

	def set_payoffs(self):
		# Init players	
		p1 = self.get_player_by_id(1)
		p2 = self.get_player_by_id(2)

		# Comparing Player's 2 output to Player's 1 input
		if self.p1_num.isdigit():
			self.p1_check = ""
			if (int(self.p1_num) % 3) == 0 or ("3" in str(self.p1_num)):
				self.p1_check += "boots"
			if (int(self.p1_num) % 5) == 0 or ("5" in str(self.p1_num)):
				self.p1_check += "cats"
			if self.p1_check is "":
				self.p1_check = str(self.p1_num)
			if str(self.p1_check) != str(self.p2_response):
				p1.is_winner = False
				self.p1_score = 0
				p2.is_winner = True
			self.p1_num = ""
			self.p1_response = ""
			self.p1_score += 1

		# Comparing Player's 1 output to Player's 2 input
		if self.p2_num.isdigit():
			self.p2_check = ""
			if (int(self.p2_num) % 3) == 0 or ("3" in str(self.p2_num)):
				self.p2_check += "boots"
			if (int(self.p2_num) % 5) == 0 or ("5" in str(self.p2_num)):
				self.p2_check += "cats"
			if self.p2_check is "":
				self.p2_check = str(self.p2_num)
			if str(self.p2_check) != str(self.p1_response):
				p2.is_winner = False
				self.p2_score = 0
				p1.is_winner = True
			self.p2_num = ""
			self.p2_response = ""
			self.p2_score += 1
		
		p1.payoff = self.p1_score;
		p2.payoff = self.p2_score;

class Player(BasePlayer):
	pass