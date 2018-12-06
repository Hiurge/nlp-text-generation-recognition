# Main libraries
import pandas as pd

# Scraping libraries
from mediawiki import MediaWiki
import re

# Support libaries
from scipy.stats import itemfreq
from itertools import chain
import collections
from collections import Counter
import numpy as np
import random

# File management
import json
import csv
import os



# INITIAL SETTING
# ---------------

# Exploration parameters
display_items = 3		# int
random_sample = True 	# bool
save_path = None        # None / str

# Save output to (or create) new folder in currend directory
save_path = "/WikiPhrases"
if save_path:
	save_path = "".join([os.path.dirname(os.path.realpath(__file__)), save_path])



# WHERE TO SCRAP FROM
# -------------------
# Keys:    categories defined by me
# Vals:    list of title(s) of specific wikipages of list-type

WIKI_LISTS_TITLES = {
	"Statistics" : ['List of statistics articles', 'List of analyses of categorical data', 'Classification algorithms'],
	"Challanges" : ['List of unsolved problems in neuroscience', 'List of unsolved problems in statistics', 'Philosophical problems', 'Decision-making paradoxes', 'Economics paradoxes', 'List of unsolved problems in mathematics', 'List of unsolved problems in computer science'],
	"Biases" : ['List of fallacies', 'List of memory_biases'],
	"Organisations" : ['List of learned societies', 'List of think tanks', 'List of mathematical societies', 'List of psychology organizations'],
	"Awards" : ["List of awards in intellectual freedom"],
	"FalseAuthor" : ["List of examples of Stigler's law"],
	"Disorders" : ['List of neurological conditions and disorders', 'List of mental_disorders'],
	"NegDisability" : ['List of disability related terms with negative connotations'],
	"PsychoResearch" : ['List of psychological research methods'],
	"PsychoDisciplines" : ['List of psychology disciplines'],
	"SocialMovements" : ['List of social movements'],
	"PseudoDiagnoses" : ['List of diagnoses characterized as pseudoscience'],
	"UrbanLegends" : ['List of urban legends'],
	"Animans" : ['List of animal names'],
	"Dances" : ['List of dances'],
	"Hobbies" : ['List of hobbies'],
	"Emotions" : ['List of emotions'],
	"Symbols" : ['List of symbols'],
	"PseudoSciences" : ['List of pseudosciences'],
	"BiblNames" : ['List of biblical names starting with A'],
	"HinduSpace" : ['List of Nakshatras'],
	"CosmosNames" : ['List of adjectivals and demonyms of astronomical bodies', 'Lists of stars by constellation'],
	}



# INITIAL INFO:    1 function
# ---------------------------

def init_info():
	listpages_num = sum([len(v) for v in WIKI_LISTS_TITLES.values()])
	print("\nStarting to scrap wikipedia phrases:\n- from {} wiki list-pages.".format(listpages_num))
	print("- to {} phrase categories.".format(len(WIKI_LISTS_TITLES)))
	print("\n\nCurrent phrase categories are:\n------------------------------\n{}\n".format(", ".join(WIKI_LISTS_TITLES)))
	this_file_path = os.path.abspath(__file__)
	if save_path:
		print("\nLinks:\n------\nBig JSON  -->  {}/wiki_phrases.csv\nBig CSV   -->  {}/wiki_phrases.json".format(save_path,save_path))
		print("Small CSV -->  {}/{}.csv".format(save_path, list(WIKI_LISTS_TITLES)[0]))
		print("\n(CSV/JSON locations are automatically generated in respect to folder you place this script in. Current location:\n-->  {}\n".format(this_file_path))
	else:
		print("\nPhrases won't be stored as a files. To do so, set path at line 32 of\n-->  {}".format(this_file_path))
	print("\nResults display will contain:\n- {} phrases displayed per each of {} categories.".format(display_items, len(WIKI_LISTS_TITLES)))
	print("- Phrases displayed in random order: {}\n\n".format(random_sample))



# SAVE AS BIG JSON, CSV & SMALL CSV'S:    3 functions
# ---------------------------------------------------

def list_to_csv(category, phrases_dict):
	csv_path = "{}/{}.csv".format(save_path, category)
	s = pd.Series(phrases_dict[category], name=category)
	s.to_csv(csv_path, index=False)

def all_lists_to_csv(phrases_dict):
	big_csv_path = "{}/wiki_phrases.csv".format(save_path)
	big_df = pd.DataFrame(columns=['Phrases','Category','NumWords']) #
	for k, l in phrases_dict.items():
		temp_df = pd.DataFrame(l, columns=['Phrases'])
		temp_df["Category"] = k
		temp_df["NumWords"] = temp_df['Phrases'].str.split(' ').apply(len)
		big_df = pd.concat([big_df, temp_df])
	big_df.to_csv(big_csv_path, index=False)

def dict_to_json(phrases_dict):
	json_path = '{}/wiki_phrases.json'.format(save_path)
	with open(json_path, "w") as f:
		json.dump(phrases_dict, f, indent=4)



# SCRAPER:    2 functions
# -----------------------

def get_phrases(wikipage):
	# Keywords gathered from wikipage links substring
	wikipage_links_titles = [ l.split(" (")[0] for l in wikipage.links ]
	
	# Not-so-clean wikipage names starts with one of words listed below
	link_stop_words = ("list", "glossary", "index", "catalog", "portal", "contents", "overview", "indice", "categor", "outline")
	
	# Get keywords from 'clean' list pages only
	linked_phrases = [p for p in wikipage_links_titles if not p.lower().startswith(link_stop_words)]
	return linked_phrases

def scrap_wiki_phrases(categories_to_scrap_num):
	# Returns dict
	# ------------
	# Keys:  categories from WIKI_LISTS_TITLES
	# Vals:  1 big list of all category phrases as a list
	# 
	# Produces files (set save_path at line 32 to path string or None)
	# -----------------------------------------
	# big JSON  :  out of whole phrases_dict.
	# big CSV   :  out of whole phrases_dict. 33 cols: Phrase, Category, WordNum 
	# small CSVs:  for each category one column csv out of pd.Series(phrases_dict[category])

	# Load wiki scraping library
	wiki = MediaWiki()
	
	# Dict to store phrases
	phrases_dict = WIKI_LISTS_TITLES.copy()
	
	# Scraping sript
	for category, lists_titles in WIKI_LISTS_TITLES.items():

		# Depending on the amount of lists in category
		n_of_lists = len(lists_titles)

		# For multi-list categories fg. "Biases" : ['List of fallacies', 'List_of_memory_biases']
		if n_of_lists > 1:
			wiki_pages = [wiki.page(title) for title in lists_titles]
			phrases_lists = [get_phrases(wikipage) for wikipage in wiki_pages]
			phrases = list(chain.from_iterable(phrases_lists))

		# For single list categories:
		elif n_of_lists is 1: 
			wiki_page = wiki.page(lists_titles[0])
			phrases = get_phrases(wiki_page)		
		
		# Get rid of unusual nonstring phrases & store them in our main dict of phrases
		phrases_dict[category] = list(filter(lambda phrase: isinstance(phrase, str), phrases))
		
		# line 32: path string / None
		if save_path:

			# If there is no such folder, create it
			if not os.path.exists(save_path):
				os.makedirs(save_path)

			# store EACH category as separate pd series CSV file
			list_to_csv(category, phrases_dict)

			# Checkpoint report
			print("{:3}. Scraped {:4} phrases to {} category".format(categories_to_scrap_num, len(phrases_dict[category]), category))
			categories_to_scrap_num -= 1
			
			# When counter hits 0, phrases_dict is ready to create big JSON and CSV
			if categories_to_scrap_num is 0:

				all_lists_to_csv(phrases_dict)
				dict_to_json(phrases_dict)
				
				print("\nScraping & Saving files finished.\n\n")

	return phrases_dict



# EXPLORATION (FINAL INFO):    1 function
# ---------------------------------------

def display_fraction_of_scraped_phrases(phrases_dict, display_items):

	for k, l in phrases_dict.items():
		phrases_dict[k] = df = pd.DataFrame(l)
		if not display_items:
			display_items = len(df)

		# Show random example phrases
		if random_sample:
			examples = random.sample(list(df.values), display_items)
		else:
			examples = df.values[:display_items]
		
		# Display
		print("\n{}\n{}".format(k,("-"*len(k))))
		for i, row in enumerate(examples): 
			print("{}. {:4}".format(i+1,row[0]))

	# Display phrases from categories
	s = "Number of phrases by category:"
	print("\n{}\n{}".format(s,("-"*len(s))))
	phrase_lists_info = [(k, len(df)) for k, df in phrases_dict.items()]
	for info in phrase_lists_info:
		print("{:<20}{}".format(info[0],info[1]))



# PROGRAM STARTS HERE
# -------------------

if __name__ == "__main__":

	# Initial info
	categories_to_scrap_num = len(WIKI_LISTS_TITLES) 
	init_info()	

	# Scrap phrases
	phrases_dict = scrap_wiki_phrases(categories_to_scrap_num)

	# Exploration
	if display_items and random_sample:
		display_fraction_of_scraped_phrases(phrases_dict, display_items)



# Organisation names
# Words  Counts   Dist
#   1.0    46.0   4.19
#   2.0   185.0  16.83
#   3.0   290.0  26.39
#   4.0   219.0  19.93
#   5.0   162.0  14.74
#   > 6   197.0  17.93
# Sample:  1099

# # more:
# # https://en.wikipedia.org/wiki/Category:Philosophy-related_lists
# # https://en.wikipedia.org/wiki/Contrasting_and_categorization_of_emotions # table
# # https://en.wikipedia.org/wiki/Outline_of_self#Virtues # wtyc=zysc
# # https://en.wikipedia.org/wiki/Category:Misconceptions !!!
# # https://en.wikipedia.org/wiki/Outline_of_artificial_intelligence # ai, potem
# # https://en.wikipedia.org/wiki/Category:Cognitive_science_lists # agregat list
# # https://en.wikipedia.org/wiki/Category:Indexes_of_science_articles # nauka

# # https://en.wikipedia.org/wiki/Outline_of_psychology # listssss
# # https://en.wikipedia.org/wiki/Category:Words_and_phrases
# # https://en.wikipedia.org/wiki/Category:Plagiarism

# # test = get_wikipage_titles_by_name("Category:Engineering societies based in the United States") # with ambition to
# # #test = get_wikipage_titles_by_name("Category:Statistical societies") # with ambition to
# # for i in test:
# # 	print(i)
# # print(len(test))
# # print(test)

# def problems_update(problems):
# 	# paradox, puzzle
# 	real_problems = []
# 	for p in problems:
# 		if p.endswith('problem'):
# 			real_problems.append(p)
# 		else:
# 			p = p + ' problem'
# 			real_problems.append(p)
# 	return real_problems