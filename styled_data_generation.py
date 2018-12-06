import tracery
import numpy as np
import pandas as pd
import json
import os
from tracery.modifiers import base_english
from itertools import chain


# BASE FOR GENERATION
# -------------------

rules = {
	
	# # Words lists
	#   -----------
	#
	#   To be loaded from json files
	#
	#
	# # Harvard phrases categories
	#   --------------------------
	#
	#  'Object', 'Negativ', 'Work', 'Feel', 'Perceiv', 'Intrj', 'Econ@', 'COLL', 'FormLw', 'Othrtags', 'PowOth', 
	#  'Polit@', 'PowGain', 'EnlTot', 'Vice', 'Academ', 'Space', 'NUMB', 'ANI', 'POS', 'Decreas', 'Solve', 'Ovrst', 
	#  'Know', 'TIME', 'Say', 'WlbPt', 'PowDoct', 'SklPt', 'Exprsv', 'AffPt', 'Exch', 'Food', 'PowCoop', 'IAV', 'SocRel', 
	#  'EnlOth', 'Pain', 'Submit', 'Race', 'TrnLoss', 'BldgPt', 'Fetch', 'PowAuth', 'RcGain', 'MALE', 'Legal', 'Stay', 
	#  'Yes', 'Land', 'ABS', 'NotLw', 'Time@', 'Ought', 'Nation', 'Compare', 'IPadj', 'Tool', 'Affil', 'Relig', 'Source', 
	#  'POLIT', 'RspGain', 'RspLoss', 'Our', 'TranLw', 'Route', 'RspTot', 'SureLw', 'CARD', 'Undrst', 'Pleasur', 'Name', 
	#  'AffGain', 'Arousal', 'EndsLw', 'Self', 'Doctrin', 'Weak', 'Persist', 'Ngtv', 'EnlLoss', 'Power', 'WltPt', 'WlbGain', 
	#  'AffOth', 'Try', 'Passive', 'Begin', 'TimeSpc', 'PosAff', 'ArenaLw', 'RcLoss', 'Negate', 'Quan', 'Hostile', 'DIST', 
	#  'Travel', 'Nonadlt', 'Strong', 'WlbPhys', 'SV', 'Causal', 'You', 'Virtue', 'ComnObj', 'Pstv', 'AffLoss', 'Vehicle', 
	#  'Vary', 'PowAren', 'PowLoss', 'NatrPro', 'EnlEnds', 'RcTot', 'NegAff', 'Exert', 'Aquatic', 'Role', 'Region', 'SklOth', 
	#  'WltOth', 'DIM', 'Sky', 'Entry', 'WltTot', 'Social', 'Complet', 'Anomie', 'Need', 'PowAuPt', 'SklTOT', 'Quality', 'PtLw', 
	#  'SklAsth', 'Active', 'EnlPt', 'FREQ', 'WlbLoss', 'COM', 'BodyPt', 'Kin@', 'DAV', 'If', 'Fail', 'RcEthic', 'Ritual', 
	#  'ComForm', 'Think', 'PowCon', 'WltTran', 'EVAL', 'Finish', 'Defined', 'Female', 'RcRelig', 'Goal', 'WlbPsyc', 'Increas', 
	#  'Fall', 'ECON', 'TrnGain', 'Rel', 'RspOth', 'Means', 'Abs@', 'PowTot', 'No', 'EnlGain', 'ORD', 'AffTot', 'COLOR', 'PowPt', 
	#  'EMOT', 'Eval@', 'WlbTot', 'Milit', 'IndAdj', 'Rise', 'PowEnds', 'NatObj', 'HU', 'MeansLw', 'PLACE', 'Positiv', 'RcEnds'
	#
	#
	# # Wikipedia phrases categories
	#   ----------------------------
	
	#  Science miscs
	#  -------------
	#  'Organisations', 'Organisations_123', 'Organisations_345', 'Organisations_567',
	#  'Awards', 'Awards_123', 'Awards_345', 'Awards_567' 
	#  'Challanges',  'Challanges_1',  'Challanges_2', 'Challanges_3'

	#  Pseudo sciences
	#  ---------------
	#  'FalseAuthor', 'FalseAuthor_1', 'FalseAuthor_2', 'FalseAuthor_3',
	#  'SocialMovements',  'SocialMovements_1', 'SocialMovements_3', 'SocialMovements_#',
	#  'PseudoDiagnoses', 'PseudoDiagnoses_1', 'PseudoDiagnoses_2',  'PseudoDiagnoses_3', 
	#  'PseudoSciences', 'PseudoSciences_1', 'PseudoSciences_2', 'PseudoSciences_3'
	#
	#   Space, symbols, heroes and saints (kinda random category)
	#   ----------------
	#  'BiblNames', 'BiblNames_12',  
	#  'HinduSpace','HinduSpace_12', 'HinduSpace_3',
	#  'CosmosNames', 'CosmosNames_12', 'CosmosNames_3', 
	#  'UrbanLegends','UrbanLegends_2', 'UrbanLegends_1', 'UrbanLegends_3'
	#  'Symbols', 'Symbols_1','Symbols_2', 'Symbols_3'
	#
	#   Even more random (fun words)
	#   ----------------------------
	#  'Dances', 'Dances_12', 'Dances_3',
	#  'Hobbies', 'Hobbies_12', 'Hobbies_3'
	#  'Animans',
	# 

	#   ------
	#  'PsychoDisciplines', 'PsychoDisciplines_1', 'PsychoDisciplines_2', 'PsychoDisciplines_3', 
	#  'PsychoResearch', 'PsychoResearch_1', 'PsychoResearch_2', 'PsychoResearch_3',
	
	#  'Statistics', 'Statistics_1', 'Statistics_2', 'Statistics_3', 


	#  'Emotions', 'Emotions_12', 'Emotions_3', 

	#  'Biases', 'Biases_1', 'Biases_2', 'Biases_3', 
	#  'Disorders', 'Disorders_1', 'Disorders_2', 'Disorders_3', 
	#  'NegDisability','NegDisability_1', 'NegDisability_2', 'NegDisability_3',  
	#  
	#  
	
	# # Deep feel phrases categories
	#   ----------------------------
	#
	#  'Anger1', 'Shame1', 'Sadness1', 'Envy1', 'Happiness1', 'Suicidal1', 'Fear1',
	#  'Anger2', 'Shame2', 'Sadness2', 'Envy2', 'Happiness2', 'Suicidal2', 'Fear2',
	#  'Anger3', 'Shame3', 'Sadness3', 'Envy3', 'Happiness3', 'Suicidal3', 'Fear3', 
	#

	# # Polarity model
	#   --------------
	#
	#   CATEGORY					SUB CATEGORIES
	#   ---------------				-----------------------------------------------------------------------------------------
	#
	#   'Atta', 			==>		'_Alone', 		'_Independent', '_Attached', 	'_Codependent', '_Hated', 		'_Loved',
	#   'PoweContResp', 	==>		'_Irresistible','_Powerless', 	'_OutOfControl','_Apathetic', 	'_Adequate',
	#   'SafeSecu', 		==>		'_Fearful', 	'_Anxious', 	'_Fearless',	'_Safe', 		'_Surprise',
	#   'PleaPain', 		==>		'_Angry', 		'_Sad', 		'_Happy', 		'_Ecstatic',
	#   'SociFace', 		==>		'_Belittled', 	'_Embarrassed', '_Average', 	'_Esteemed',
	#   'Just', 			==>		'_Cheated', 	'_SingledOut', 	'_Justified', 	'_Entitled',
	#   'DireFocu', 		==>		'_Derailed', 	'_Lost', 		'_Focused', 	'_Obsessed',
	#   'DesiInte', 		==>		'_Demoralized', '_Bored', 		'_Attracted', 	'_Lustful',
	#   'Free', 			==>		'_Trapped', 	'_Burdened', 	'_Free',
	#

	# # Other models / datasets
	#   -----------------------
	#
	#  'AOD',  ==> of degree
	#
	#  'AllE', ==> all E
	#
	#  'StrW', ==> strong words
	#

	# General use cases:
	# - Text generation
	# - Data agumentation
	# - Data styling

    # # Blueprints (just testing if data loads correctly)

    "blueprint 1": "Students movement for #_Irresistible# #PseudoSciences# phobia overcoming",
    "blueprint 2": "Academic society of #_Esteemed# #Biases# cultivation",
    "blueprint 3": "Students organisation of #AOD# #StrW# #PseudoSciences# promotion",
    "blueprint 4": "Scientific circle of #Statistics# methods to solve #Challanges#",
    "blueprint 5": "Graduates club of #Statistics# applications in #PseudoSciences#",
    "blueprint 6": "New #Happiness3# #SocialMovements# project for #Biases# normalisation",


    }


    # Stop abstractions.
    # Usecases -> easy use vs effect ratio (hacky)
    # Its a DB builder not a final output
    # unadjusted data would hurt the outcome.

    # # #####################################################
    #
    # # Notes
    #   -----
    # 
    # 1. Try some schemas, have fun
    # 2. Get deeper idea where to go with that
    # 3. I aim for styled data generation
    # 4. and funy/useful templates or outcomes
    #
    ########################################################################################################




def get_blueprints(rules):
	# For further generation: get, prepare and save blueprint names
	return [str("#"+blueprint+"#") for blueprint in rules.keys()]

loaded_blueprints = get_blueprints(rules)

# LOAD DATA
# ---------

LoadDIR = "".join([os.path.dirname(os.path.realpath(__file__)), '/GeneratorDataIn'])

harv_file = LoadDIR + '/HDD.json'
wiki_file = LoadDIR + '/wiki_phrases_clean.json'
feel_file = LoadDIR + '/deep_feeling.json'
unif_file = LoadDIR + '/harvard_unified.csv'

datain_files  = [harv_file, wiki_file, feel_file]
for file in datain_files:
	
	# Load JSON with words lists
	with open(file, "r") as read_file:
		phrases = json.load(read_file)

	# Ffeed tracy rules with phrase dicts
	for key, value in phrases.items():
		if "test" in rules:
			print("Exists:", key)
		rules[key] = phrases[key]




# GENERATOR 
# ---------	
# Create a grammar object from the rules and pre-programmed modifiers
grammar = tracery.Grammar(rules) 
grammar.add_modifiers(base_english)

# Generate sentences
Sentences_chronology = []
generations_per_blueprint = 1
generated_sentences = {}
n = 0
for blueprint in loaded_blueprints:
	generated_sentences[blueprint] = []
	for i in range(generations_per_blueprint):
		s = grammar.flatten(blueprint)
		generated_sentences[blueprint].append(grammar.flatten(s))
		Sentences_chronology.append((s, grammar.flatten(s)))
		n += 1
		#print(n, s) # and flatten, starting with origin rule

generated_sentences["all"] = list(chain.from_iterable(generated_sentences.values()))




# DISPLAY
# -------

for i, s in enumerate(generated_sentences["all"]):
	print(i, s)


# -------------------------------------------------------

# Not much finesy, just testing if data loads
# -------------------------------------------
# 0 Academic society of worshiped cultural bias cultivation
# 1 Students movement for powerful Feng shui phobia overcoming
# 2 Students organisation of just timorous reflexology promotion
# 3 Graduates club of Quasi-experiment applications in christian science
# 4 New overconfident project for fearful & guilt-ridden social democracy seduction training
# 5 Scientific circle of Maximum likelihood methods to solve Zeno's paradoxes
