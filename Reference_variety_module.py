import sys
import xlrd
import re
import numpy
from enum import Enum, auto
import pdb
import json
import pprint

class ReferenceType(Enum):
    PRONOUN = auto()
    DEFINITE = auto()
    SEMIDEF = auto()
  

debug = False
pp = pprint.PrettyPrinter(indent=4)

def PlayerPlaceholder(playerinfo, jsongamedata, homeaway, gap, **kwargs):
	mentionedentities = kwargs['mentionedentities']
	currentsentidx = kwargs['idx']
	currentgapidx = kwargs['gapidx']
	nominal = (kwargs['case'] == 'nominal')
	print("Playerinfo:\n", playerinfo)

	#First find the player's information by looking up the player
	playerfullname = playerinfo['c_Person']

	namepossibilities = []

	if (playerfullname not in mentionedentities):
		#If there is no previous mention of the player, use a definite description
		namepossibilities = PlayerDefiniteDescription(playerinfo)
		#mentionedentities[playerfullname] is an array of each time the player is mentioned
		mentionedentities[playerfullname] = {'mentions':[], 'entityinfo':playerinfo}
		mentiontype = ReferenceType.DEFINITE

	# Also attach whether a nominative pronoun should be used if applicable
	mentionedentities[playerfullname]['mentions'].append({ 'sentidx': currentsentidx,
									   'gapidx': currentgapidx, 'nominal': nominal})

	return	'{'+playerfullname+'}'

def ReviewReferences(sentences, jsongamedata, homeaway, **kwargs):
	mentionedentities = kwargs['mentionedentities']
	home_team = jsongamedata['MatchInfo'][0]['c_HomeTeam']
	away_team = jsongamedata['MatchInfo'][0]['c_AwayTeam']

	# Determine focus team
	if homeaway == 'home':
		focusteam = home_team
	elif homeaway == 'away':
		focusteam = away_team
	else:
		focusteam = 'neutral'

	#sort players in order of mentions
	all_players = sorted(mentionedentities.keys(), key=lambda player: len(mentionedentities[player]['mentions']), reverse=True)

	# Filter the non-footballers (managers, referees)
	for player in all_players:
		if ((mentionedentities[player]['entityinfo']['n_ActionSet'] != 4) and (mentionedentities[player]['entityinfo']['n_ActionSet'] != 5)):
			all_players.remove(player)

	important_players = all_players.copy()
	players_mention_num = [len(mentionedentities[player]['mentions']) for player in all_players if len(mentionedentities[player]['mentions'])>1]
	#players mentioned 1 time only are moved to another list
	single_mention_players = important_players[len(players_mention_num):]
	del(important_players[len(players_mention_num):])
	current_season_year = jsongamedata['MatchInfo'][0]['c_Season']


	# Get all interesting stats of all players of their previous season
	players_last_season_stats = {}
	player_with_most_goals_last_season = ""
	most_goals = 0
	for player in all_players:
		playerdata = getPlayerData(mentionedentities[player]['entityinfo'], **kwargs)
		for idx in range(len(playerdata['PlayerLeague'])):
			if playerdata['PlayerLeague'][idx]['c_Edition'] == current_season_year and idx == 0:
				current_season = playerdata['PlayerLeague'][idx]
				last_season = False
				break

			elif playerdata['PlayerLeague'][idx]['c_Edition'] == current_season_year and idx > 0:
				current_season = playerdata['PlayerLeague'][idx]
				last_season = playerdata['PlayerLeague'][idx-1]
				break

		last_season_stats = {}
		if last_season is not False:
			last_season_stats['club'] = last_season['c_Team']
			last_season_stats['matches'] = last_season['n_Matches']
			last_season_stats['goals'] = last_season['n_Goals']
			last_season_stats['assists'] = last_season['n_Assists']

		# Save the player with the most goals last season, as he is probably the most interesting to mention. Only do
		# this for the aimed team, and not for neutral
		if mentionedentities[player]['entityinfo']['c_Team'] == focusteam:
			if last_season is not False and last_season['n_Goals'] > most_goals:
				most_goals = last_season['n_Goals']
				player_with_most_goals_last_season = player


		players_last_season_stats[player] = last_season_stats

	# The players that get mentioned only once always get their full name mentioned.
	for player in single_mention_players:

		# Find the sentence and gaps for these players
		placeholder_string_to_change = '{' + player + '}'
		sentence_number = mentionedentities[player]['mentions'][0]['sentidx']
		gap_number = mentionedentities[player]['mentions'][0]['gapidx']
		sentence_to_change = sentences[sentence_number]
		placeholder_name_index = sentence_to_change.find(placeholder_string_to_change)
		potential_sentences = []
		playerinfo = mentionedentities[player]['entityinfo']


		# Check if this is the player with the most goals
		if player == player_with_most_goals_last_season:

			# Make a disambiguating_reference for this player
			potential_disambiguating_references, probabilities = PlayerReferringExpression(playerinfo, jsongamedata, homeaway, 0, **kwargs, idx=(sentence_number+1), gapidx=0, previous_mentions=None, lastseason=True, number_of_total_mentions=1, mention_number=0)
			norm = [float(i) / sum(probabilities) for i in probabilities]
			disambiguating_reference= numpy.random.choice(potential_disambiguating_references, p=norm)

			# Capitalize the reference aswell, as we might need a capitalized version
			# Capitalize first letter only, otherwise it somehow deletes other capital letters
			to_capitalize = list(disambiguating_reference)
			to_capitalize[0] = to_capitalize[0].capitalize()
			disambiguating_reference_capitalized = "".join(to_capitalize)

			# Create potential sentences describing the goals
			if most_goals > 0:
				if most_goals > 29:
					potential_sentences.append(" " + disambiguating_reference_capitalized + " maakte vorig seizoen nog maarliefst " + str(most_goals) + " doelpunten voor " + players_last_season_stats[player]['club'] + ".")
					potential_sentences.append(" " + disambiguating_reference_capitalized + " draaide vorig jaar nog een bizar goed seizoen, waarin hij wel " + str(most_goals) + " keer wist te scoren voor " + players_last_season_stats[player]['club'] + ".")
					potential_sentences.append(" Vorig seizoen nog legde " + disambiguating_reference + " maarliefst " + str(most_goals) + " keer de bal in het net voor " + players_last_season_stats[player]['club'] + ".")
				elif most_goals > 19:
					potential_sentences.append(" " + disambiguating_reference_capitalized + " draaide vorig jaar nog een goed seizoen, waarin hij " + str(most_goals) + " keer wist te scoren voor " + players_last_season_stats[player]['club'] + ".")
					potential_sentences.append(" " + disambiguating_reference_capitalized + " wist vorig seizoen nog " + str(most_goals) + " doelpunten te maken voor " + players_last_season_stats[player]['club'] + ".")
					potential_sentences.append(" Vorig seizoen was " + disambiguating_reference + " nog erg in vorm, toen hij " + str(most_goals) + " doelpunten wist te maken voor " + players_last_season_stats[player]['club'] + ".")
				elif most_goals > 9:
					potential_sentences.append(" " + disambiguating_reference_capitalized + " wist vorig seizoen nog " + str(most_goals) + " doelpunten te maken voor " + players_last_season_stats[player]['club'] + ".")
					potential_sentences.append(" Vorig seizoen nog legde " + disambiguating_reference + " " + str(most_goals) + " keer de bal in het net voor " + players_last_season_stats[player]['club'] + ".")
					potential_sentences.append(" " + disambiguating_reference_capitalized + " scoorde vorig seizoen nog " + str(most_goals) + " keer voor " + players_last_season_stats[player]['club'] + ".")
				else:
					potential_sentences.append(" " + disambiguating_reference_capitalized + " scoorde vorig seizoen nog " + str(most_goals) + " keer voor " + players_last_season_stats[player]['club'] + ".")

				# Pick one of these sentences
				extra_sentence = numpy.random.choice(potential_sentences)

		# Check if placeholder has been found
		if (placeholder_name_index != -1):
			letterlist = list(sentence_to_change)
			# Delete the opening curly bracket
			del letterlist[placeholder_name_index]

			# Delete the closing curly bracket
			del letterlist[placeholder_name_index + len(player)]

			# Add mention of goals last season
			if player == player_with_most_goals_last_season:
				letterlist.extend(list(extra_sentence))

			new_sentence = "".join(letterlist)
			sentence_to_change = new_sentence
			sentences[sentence_number] = sentence_to_change
		else:
			print("Player: " + player + " is not in the sentence! \n")

	# Find which players will need disambiguation
	for player in important_players:
		mentions_without_pronoun = 0
		ambiguousreferents = []
		references_already_used = []
		for mentionidx, mention in reversed(list(enumerate(mentionedentities[player]['mentions']))):
			can_use_pronoun, ambiguousreferentsthissent = AmbiguousReferents(player,mentionidx,sentences,mentionedentities)

			# Find the placeholder name in the sentence
			placeholder_string_to_change = '{' + player + '}'
			sentence_number = mention['sentidx']
			gap_number = mention['gapidx']
			sentence_to_change = sentences[sentence_number]
			placeholder_name_index = sentence_to_change.find(placeholder_string_to_change)
			playerinfo = mentionedentities[player]['entityinfo']

			if 'nominal' in mention:
				nominal = mention['nominal']
			else:
				nominal = False

			# If it is the player's first entry of the report, always use full name
			if mentionidx == 0:

				# Check if this is the player with the most goals
				if player == player_with_most_goals_last_season:

					# Make a disambiguating_reference for this player
					potential_disambiguating_references, probabilities = PlayerReferringExpression(playerinfo, jsongamedata, homeaway, 0, **kwargs, idx=(sentence_number + 1), gapidx=0, previous_mentions=None, lastseason=True, number_of_total_mentions=1, mention_number=0)
					norm = [float(i) / sum(probabilities) for i in probabilities]
					disambiguating_reference = numpy.random.choice(potential_disambiguating_references, p=norm)

					# Capitalize the reference aswell, as we might need a capitalized version
					# Capitalize first letter only, otherwise it somehow deletes other capital letters
					to_capitalize = list(disambiguating_reference)
					to_capitalize[0] = to_capitalize[0].capitalize()
					disambiguating_reference_capitalized = "".join(to_capitalize)

					# Create potential sentences describing the goals
					if most_goals > 0:
						if most_goals > 29:
							potential_sentences.append(" " + disambiguating_reference_capitalized + " maakte vorig seizoen nog maarliefst " + str(most_goals) + " doelpunten voor " + players_last_season_stats[player]['club'] + ".")
							potential_sentences.append(" " + disambiguating_reference_capitalized + " draaide vorig jaar nog een bizar goed seizoen, waarin hij wel " + str(most_goals) + " keer wist te scoren voor " + players_last_season_stats[player]['club'] + ".")
							potential_sentences.append(" Vorig seizoen nog legde " + disambiguating_reference + " maarliefst " + str(most_goals) + " keer de bal in het net voor " + players_last_season_stats[player]['club'] + ".")
						elif most_goals > 19:
							potential_sentences.append(" " + disambiguating_reference_capitalized + " draaide vorig jaar nog een goed seizoen, waarin hij " + str(most_goals) + " keer wist te scoren voor " + players_last_season_stats[player]['club'] + ".")
							potential_sentences.append(" " + disambiguating_reference_capitalized + " wist vorig seizoen nog " + str(most_goals) + " doelpunten te maken voor " + players_last_season_stats[player]['club'] + ".")
							potential_sentences.append(" Vorig seizoen was " + disambiguating_reference + " nog erg in vorm, toen hij " + str(most_goals) + " doelpunten wist te maken voor " + players_last_season_stats[player]['club'] + ".")
						elif most_goals > 9:
							potential_sentences.append(" " + disambiguating_reference_capitalized + " wist vorig seizoen nog " + str(most_goals) + " doelpunten te maken voor " + players_last_season_stats[player]['club'] + ".")
							potential_sentences.append(" Vorig seizoen nog legde " + disambiguating_reference + " " + str(most_goals) + " keer de bal in het net voor " + players_last_season_stats[player]['club'] + ".")
							potential_sentences.append(" " + disambiguating_reference_capitalized + " scoorde vorig seizoen nog " + str(most_goals) + " keer voor " + players_last_season_stats[player]['club'] + ".")
						else:
							potential_sentences.append(" " + disambiguating_reference_capitalized + " scoorde vorig seizoen nog " + str(most_goals) + " keer voor " + players_last_season_stats[player]['club'] + ".")

						# Pick one of these sentences
						extra_sentence = numpy.random.choice(potential_sentences)

				# Check if placeholder is found
				if (placeholder_name_index != -1):
					letterlist = list(sentence_to_change)
					# Delete the opening curly bracket
					del letterlist[placeholder_name_index]

					# Delete the closing curly bracket
					del letterlist[placeholder_name_index + len(player)]

					# Add mention of goals last season
					if player == player_with_most_goals_last_season:
						letterlist.extend(list(extra_sentence))

					new_sentence = "".join(letterlist)
					sentence_to_change = new_sentence
					sentences[sentence_number] = sentence_to_change
				else:
					print("Player: " + player + " is not in the sentence! \n")
				continue

			# If you can use a pronoun, replace placeholder with 'hij' or 'hem'
			if can_use_pronoun:
				print("can use pronoun")

				# If a nominative pronoun should be used
				if nominal:

					# If it is the first entry in a sentence, it should be with a capital
					if placeholder_name_index == 0:
						HijHem_string = "Hij"
					else:
						HijHem_string = "hij"

				# If an objective pronoun should be used
				else:

					# If it is the first entry in a sentence, it should be with a capital
					if placeholder_name_index == 0:
						HijHem_string = "Hem"
					else:
						HijHem_string = "hem"

				if (placeholder_name_index != -1):
					letterlist = list(sentence_to_change)
					# Delete the placeholder playername
					del letterlist[placeholder_name_index:(placeholder_name_index + len(placeholder_string_to_change))]

					# Add 'hij' where the placeholder name was before
					for letter in reversed(HijHem_string):
						letterlist.insert(placeholder_name_index, letter)

					new_sentence = "".join(letterlist)
					sentence_to_change = new_sentence
					sentences[mention['sentidx']] = sentence_to_change
				else:
					print("Player: " + player + " is not in the sentence! \n")
				continue

			# Check if this player has been mentioned in this sentence already
			if gap_number > 0:
				# this is not the first gap in this sentence. Is the previous gap also a person (and not this player)?
				previousgapsthissent = []
				prev_mentions_this_player_this_sent = []
				for entity in mentionedentities[player]['mentions']:
					if entity['sentidx'] == sentence_number and entity['gapidx'] < gap_number:
						prev_mentions_this_player_prev_sent.append(entity)
			else:
				previousgapsthissent = []
				prev_mentions_this_player_this_sent = []

			# Check if this player has been mentioned in the previous sentence
			prev_mentions_this_player_prev_sent = []
			for entity in mentionedentities[player]['mentions']:
				if entity['sentidx'] < sentence_number and entity['sentidx'] > (sentence_number - 2):
						prev_mentions_this_player_prev_sent.append(entity)

			# Add mentions from this and previous sentence together
			prev_mentions_this_player_this_or_prev_sent = prev_mentions_this_player_prev_sent + prev_mentions_this_player_this_sent

			# Check if player has been mentioned in one of the 2 sentences
			player_mentioned_this_or_prev_sentence = (len(prev_mentions_this_player_this_or_prev_sent) > 0)

			# If player has been mentioned in one of the 2 sentences
			if player_mentioned_this_or_prev_sentence:

				mentions_without_pronoun += 1
				ambiguousreferents.extend(ambiguousreferentsthissent)

				# Find the ambiguous players if applicable
				otherplayers = []
				if ambiguousreferentsthissent:
					for other_player in ambiguousreferentsthissent:
						sentidx = other_player['sentidx']
						gapidx = other_player['gapidx']
						for other_other_player in mentionedentities:
							for playermention in mentionedentities[other_other_player]['mentions']:
								if (playermention['sentidx'] == sentidx) and (playermention['gapidx'] == gapidx):
									otherplayers.append(mentionedentities[other_other_player]['entityinfo'])
									break
							break

				potential_disambiguating_references, probabilities = PlayerReferringExpression(playerinfo, jsongamedata, homeaway, 0, **kwargs, idx=sentence_number, gapidx=gap_number, previous_mentions=prev_mentions_this_player_this_or_prev_sent, number_of_total_mentions=len(mentionedentities[player]['mentions']), mention_number=mentionidx)
				norm = [float(i) / sum(probabilities) for i in probabilities]
				disambiguating_reference_raw = numpy.random.choice(potential_disambiguating_references, p=norm)

				# If all possible references have already been picked, one has to be reused, so the already used list
				# should be wiped
				reference_counter = 0
				for reference in potential_disambiguating_references:
					if reference in references_already_used:
						reference_counter += 1
				if (reference_counter == len(potential_disambiguating_references)):
					print("All references have been used!\n")
					references_already_used.clear()


				# If a reference is picked which has already been used, pick another one
				while disambiguating_reference_raw in references_already_used:
					disambiguating_reference_raw = numpy.random.choice(potential_disambiguating_references, p=norm)
				disambiguating_reference = disambiguating_reference_raw
				references_already_used.append(disambiguating_reference)

				# If it is the first entry of the sentence, it should be capitalized
				if placeholder_name_index == 0:

					# Capitalize first letter only, otherwise it somehow deletes other capital letters
					disambiguating_reference_letterlist = list(disambiguating_reference)
					disambiguating_reference_letterlist[0] = disambiguating_reference_letterlist[0].capitalize()
					disambiguating_reference = "".join(disambiguating_reference_letterlist)


				# Replace the placeholder with the new reference
				# Check if placeholder is found
				if (placeholder_name_index != -1):
					letterlist = list(sentence_to_change)
					# Delete the placeholder playername
					del letterlist[placeholder_name_index:(placeholder_name_index + len(placeholder_string_to_change))]

					# Add the disambiguating_reference where the placeholder name was before
					for letter in reversed(disambiguating_reference):
						letterlist.insert(placeholder_name_index, letter)

					new_sentence = "".join(letterlist)
					sentence_to_change = new_sentence
					sentences[mention['sentidx']] = sentence_to_change
				else:
					print("Player: " + player + " is not in the sentence! \n")
				continue

			# If this all doesn't hold, then it means that it is not the first mention, no pronoun can be used,
			# and the player hasn't been mentioned in the previous or current sentence, thus full name needs to
			# be used again
			else:

				# Use either full name or last name
				player_last_name = playerinfo['c_PersonLastName']
				name_options = []
				name_options.append(player)
				name_options.append(player_last_name)
				name_option = numpy.random.choice(name_options)

				# Replace the placeholder with the full or last name
				# Check if placeholder is found
				if (placeholder_name_index != -1):
					letterlist = list(sentence_to_change)
					# Delete the placeholder playername
					del letterlist[placeholder_name_index:(placeholder_name_index + len(placeholder_string_to_change))]

					# Add the full or last name where the placeholder name was before
					for letter in reversed(name_option):
						letterlist.insert(placeholder_name_index, letter)

					new_sentence = "".join(letterlist)
					sentence_to_change = new_sentence
					sentences[mention['sentidx']] = sentence_to_change
				else:
					print("Player: " + player + " is not in the sentence! \n")


		if mentions_without_pronoun>1:
			pprint.pprint(ambiguousreferents)
	print('-------\n')
	
	
def AmbiguousReferents(currentplayer,mentionidx,sentences,mentionedentities):
	mentions = mentionedentities[currentplayer]['mentions']
	currentmention = mentions[mentionidx]
	sentence = sentences[currentmention['sentidx']]
	idxlastmention = mentions[mentionidx-1]['sentidx']
	currentsentidx = currentmention['sentidx']
	currentgapidx = currentmention['gapidx']
	playerinfo = mentionedentities[currentplayer]['entityinfo']
	ambiguousplayers = []
	#Adapted from McCoy and Strube 2002, page 68
	#Figure 3, 1. :
	if abs(idxlastmention-currentsentidx)>2:
		#maybe here is good to re-use the name?
		return False,[]
	#Figure 3, 2. never happens in PASS so not implemented			
	#Figure 3, 3. thread change = different "topic" (title/stuff) - not implemented
	#Figure 3, 4:
	#find if there is a competing antecedent
	competing_antecedent_same_sent = False
	competing_antecedent_prev_sent = False
	first_occur_this_player_this_sent = True
	if currentgapidx>0:
		#this is not the first gap in this sentence. Is the previous gap also a person?
		previousgapsthissent = [mentionedentities[entity] for entity in mentionedentities for mention in mentionedentities[entity]['mentions'] if mention['sentidx']==currentsentidx and mention['gapidx']<currentgapidx and 'c_Person' in mentionedentities[entity]['entityinfo']]
		prev_mentions_this_player_this_sent = [entity for entity in previousgapsthissent if entity['entityinfo']==playerinfo]
		first_occur_this_player_this_sent = len(prev_mentions_this_player_this_sent)==0

		#if previous gaps are not mentions of this player, it is a competing antecedent in same sentence
		if len(previousgapsthissent)!=len(prev_mentions_this_player_this_sent):
			competing_antecedent_same_sent = True
			other_players_this_sent = [mentionedentities[entity]['mentions'] for entity in mentionedentities for mention in mentionedentities[entity]['mentions'] if mention['sentidx']==currentsentidx and mention['gapidx']<currentgapidx and 'c_Person' in mentionedentities[entity]['entityinfo'] and mentionedentities[entity]['entityinfo']!=playerinfo]
			other_players_this_sent = other_players_this_sent[0]
			other_players_this_sent2 = []
			for other_player in other_players_this_sent:
				if other_player['sentidx'] == currentsentidx:
					other_players_this_sent2.append(other_player)
			ambiguousplayers = other_players_this_sent2
	#is there maybe an entity mentioned in a previous sentence?
	previousgaps = [mention for entity in mentionedentities for mention in mentionedentities[entity]['mentions'] if mention['sentidx']<currentsentidx and mention['sentidx']>(currentsentidx-2) and mentionedentities[entity]['entityinfo'] != playerinfo]
	if len(previousgaps)>0:
		competing_antecedent_prev_sent = True
		ambiguousplayers = ambiguousplayers + previousgaps
	#else:
	#	pdb.set_trace()
	
	if debug:
		if currentgapidx>0:
			print('prev_mentions_this_player_this_sent: '+str(prev_mentions_this_player_this_sent))
		print('Index of this gap:'+str(currentgapidx))
		if 'previousgaps' in locals():
			print('Previous gaps this sent'+str(previousgaps))
		print('Previous mentions in general: '+str(mentionedentities))
		print("Is player's first mention in this sent? "+str(first_occur_this_player_this_sent))
		print("Is there a competing antecedent in this sent? "+str(competing_antecedent_same_sent))
		print("Is there a competing antecedent in previous sent? "+str(competing_antecedent_prev_sent))
	
	#Figure 2, 1. 
	if first_occur_this_player_this_sent:
		if competing_antecedent_prev_sent:
			#2.1 (a)
			#TODO: try to use referring expression generation here
			return False, ambiguousplayers
			#namepossibilities = PlayerDefiniteDescription(playerinfo)	
			#mentiontype = ReferenceType.DEFINITE
		if competing_antecedent_same_sent and currentgapidx>0:
			#2.1 (b)
			#TODO: look at the content of previousgapsthissent
			#is it reasonable to resolve to the same pronoun?
			return False, ambiguousplayers
	#Figure 2, 2. 
	else:
		if competing_antecedent_same_sent:
			#2.2(a):
			mentiontype = ReferenceType.DEFINITE
			return False, ambiguousplayers
		else:					
			#2.2(b):
			return True, []
	#this should be Figure 3.5
	return True, []
	

def PlayerReferenceModelWithPronouns(playerinfo, jsongamedata, homeaway, gap, **kwargs):
	# mentionedentities is a dict with all the entities that were already mentioned
	# Name (TODO: ID) is the key 
	# The value is an array, and every time I mention an entity I add to this array
	# a dict such that :
	# {
	#  sentidx : sentence idx of this mention
	#  gapidx : which gap of the sentence
	#  mention : string of the current mention (e.g. 'Francesco Totti')
	#  entityinfo : information about the club or player mentioned
	#  mentiontype : ReferenceType ('definite'|'semi'|'pronoun')
	# }
	mentionedentities = kwargs['mentionedentities']
	currentsentidx = kwargs['idx']
	currentgapidx = kwargs['gapidx']
	#First find the player's information by looking up the player

	playerfullname = playerinfo['c_Person']

	namepossibilities = []

	if debug:
		print('\n###Pronoun generation algo:###')
		print('Current template: '+kwargs['templatetext'])
		print('Current player: '+playerfullname)
		print('Current event: '+str(kwargs['event']))

	
	if (playerfullname not in mentionedentities):
		if debug:
			print("First mention of this player")
		#If there is no previous mention of the player, use a definite description
		namepossibilities = PlayerDefiniteDescription(playerinfo)
		#mentionedentities[playerfullname] is an array of each time the player is mentioned
		mentionedentities[playerfullname] = {'mentions':[], 'entityinfo':playerinfo}
		mentiontype = ReferenceType.DEFINITE
	else:
		#otherwise check WHEN it was mentioned last time as a definite entity
		previousmentions = mentionedentities[playerfullname]['mentions']
		idxlastmention = previousmentions[-1]['sentidx']
		
		#Adapted from McCoy and Strube 2002, page 68
		#Figure 3, 1. :
		if abs(idxlastmention-currentsentidx)>2:
			namepossibilities = PlayerDefiniteDescription(playerinfo)	
			mentiontype = ReferenceType.DEFINITE
		#Figure 3, 2. never happens in PASS so not implemented			
		#Figure 3, 3. thread change = different "topic" (title/stuff) - not implemented
		#Figure 3, 4:
		else:
			#find if there is a competing antecedent
			competing_antecedent_same_sent = False
			competing_antecedent_prev_sent = False
			first_occur_this_player_this_sent = True
			if currentgapidx>0:
				#this is not the first gap in this sentence. Is the previous gap also a person?
				previousgapsthissent = [mentionedentities[entity] for entity in mentionedentities for mention in mentionedentities[entity]['mentions'] if mention['sentidx']==currentsentidx and mention['gapidx']<currentgapidx and 'c_Person' in mentionedentities[entity]['entityinfo']]
				prev_mentions_this_player_this_sent = [entity for entity in previousgapsthissent if entity['entityinfo']==playerinfo]
				first_occur_this_player_this_sent = len(prev_mentions_this_player_this_sent)==0
				#if previous gaps are not mentions of this player, it is a competing antecedent in same sentence
				if len(previousgapsthissent)!=len(prev_mentions_this_player_this_sent):
					competing_antecedent_same_sent = True
			
			#is there maybe an entity mentioned in a previous sentence?
			previousgaps = [mention for entity in mentionedentities for mention in mentionedentities[entity]['mentions'] if mention['sentidx']<currentsentidx and mention['sentidx']>(currentsentidx-2) and mentionedentities[entity]['entityinfo'] != playerinfo]
			if len(previousgaps)>0:
				competing_antecedent_prev_sent = True
			#else:
			#	pdb.set_trace()
			
			if debug:
				if currentgapidx>0:
					print('prev_mentions_this_player_this_sent: '+str(prev_mentions_this_player_this_sent))
				print('Index of this gap:'+str(currentgapidx))
				if 'previousgaps' in locals():
					print('Previous gaps this sent'+str(previousgaps))
				print('Previous mentions in general: '+str(mentionedentities))
				print("Is player's first mention in this sent? "+str(first_occur_this_player_this_sent))
				print("Is there a competing antecedent in this sent? "+str(competing_antecedent_same_sent))
				print("Is there a competing antecedent in previous sent? "+str(competing_antecedent_prev_sent))
			
			#Figure 2, 1. 
			if first_occur_this_player_this_sent:
				if competing_antecedent_prev_sent:
					#2.1 (a)
					#TODO: try to use referring expression generation here
					namepossibilities = PlayerDefiniteDescription(playerinfo)	
					mentiontype = ReferenceType.DEFINITE
				if competing_antecedent_same_sent and currentgapidx>0:
					#2.1 (b)
					#TODO: look at the content of previousgapsthissent
					#is it reasonable to resolve to the same pronoun?
					namepossibilities = PlayerReferringExpression(playerinfo, jsongamedata, homeaway, gap, **kwargs)
					
					#namepossibilities = PlayerDefiniteDescription(playerinfo)	
					mentiontype = ReferenceType.DEFINITE
			#Figure 2, 2. 
			else:
				if competing_antecedent_same_sent:
					#2.2(a):
					namepossibilities = PlayerReferringExpression(playerinfo, jsongamedata, homeaway, gap, **kwargs)
					
					#namepossibilities = PlayerDefiniteDescription(playerinfo)	
					mentiontype = ReferenceType.DEFINITE
				else:					
					#2.2(b):
					#TODO: check that the template just before the gap does not contain "het"?
					#example: Na 47 minuten spelen was het hij die op aangeven van Atiba Hutchinson
					pronoun = 'hem'
					if 'case' in kwargs and kwargs['case'] == 'nominal':
						pronoun = 'hij'
					if debug:
						namepossibilities = [[pronoun+' ['+playerfullname+']'], [1]]
					else:
						namepossibilities = [[pronoun], [1]]
					mentiontype = ReferenceType.PRONOUN
	
	#this should be Figure 3.5
	if len(namepossibilities)==0:
		pronoun = 'hem'
		#pdb.set_trace()
		#TODO: check that the template just before the gap does not contain "het"?
		if 'case' in kwargs and kwargs['case'] == 'nominal':
			pronoun = 'hij'
		if debug:
			namepossibilities = [[pronoun+' ['+playerfullname+']'], [1]]
		else:
			namepossibilities = [[pronoun], [1]]
		mentiontype = ReferenceType.PRONOUN
	namechoice = numpy.random.choice(namepossibilities[0], p=namepossibilities[1])
	nametuple = (playerfullname, namechoice)
	mentionedentities[playerfullname]['mentions'].append({ 'sentidx': currentsentidx,
									   'gapidx': currentgapidx,
									   'mention': namechoice,
									   'mentiontype': mentiontype})
	if debug:
		print ('I will use: '+str(nametuple))
	return nametuple


def RefereeReferenceModel(refereeinfo, jsongamedata, homeaway, gap, **kwargs):
	# mentionedentities is a dict with all the entities that were already mentioned
	# Name (TODO: ID) is the key 
	# The value is an array, and every time I mention an entity I add to this array
	# a dict such that :
	# {
	#  sentidx : sentence idx of this mention
	#  gapidx : which gap of the sentence
	#  mention : string of the current mention (e.g. 'Francesco Totti')
	#  entityinfo : information about the club or player mentioned
	#  mentiontype : ReferenceType ('definite'|'semi'|'pronoun')
	# }
	mentionedentities = kwargs['mentionedentities']
	currentsentidx = kwargs['idx']
	currentgapidx = kwargs['gapidx']

	refereefullname = refereeinfo['c_Person']
	
	namepossibilities = []

	if debug:
		print('\n###Referee naming algo:###')
		print('Current template: '+kwargs['templatetext'])
		print('Referee: '+refereefullname)
	
	if (refereefullname not in mentionedentities):
		if debug:
			print("First mention of the referee")
		#If there is no previous mention of the player, use a definite description
		namepossibilities = [['arbiter '+refereefullname, 'scheidsrechter '+refereefullname], [0.5, 0.5]]
		mentionedentities[refereefullname] = {'mentions':[], 'entityinfo':refereeinfo}
	else:
		lastname = refereeinfo['c_PersonLastName']
		namepossibilities = [['arbiter '+lastname, 'scheidsrechter '+lastname, lastname, 'de arbiter', 'de scheidsrechter'], [0.2, 0.2, 0.2, 0.2, 0.2]]
	mentiontype = ReferenceType.DEFINITE
	namechoice = numpy.random.choice(namepossibilities[0], p=namepossibilities[1])
	nametuple = (refereefullname, namechoice)
	mentionedentities[refereefullname]['mentions'].append({ 'sentidx': currentsentidx,
									   'gapidx': currentgapidx,
									   'mention': namechoice,
									   'mentiontype': mentiontype})
	if debug:
		print ('I will use: '+str(nametuple))
	return nametuple
	
def PlayerDefiniteDescription(playerinfo):
	#these references all contain the proper name
	namepossibilities = []
	fullname = playerinfo['c_Person']
	namepossibilities.append([fullname, 10])
	firstname = playerinfo['c_PersonFirstName']
	lastname = playerinfo['c_PersonLastName']
	namepossibilities.append([lastname, 10])
	if not isManager(playerinfo):
		role = playerinfo['n_FunctionCode']
		if role&1: #keeper
			namepossibilities.append(['doelman ' + lastname, 5])
			namepossibilities.append(['doelman ' + fullname, 5])
		elif role&2: #defender
			namepossibilities.append(['verdediger ' + lastname, 5])
			namepossibilities.append(['verdediger ' + fullname, 5])
		elif role&4: #midfielder
			namepossibilities.append(['middenvelder ' + lastname, 5])
			namepossibilities.append(['middenvelder ' + fullname, 5])
		elif role&8: #attacker
			namepossibilities.append(['aanvaller ' + lastname, 5])
			namepossibilities.append(['aanvaller ' + fullname, 5])
	else:
		namepossibilities.append(['manager ' + lastname, 5])
		namepossibilities.append(['manager ' + fullname, 5])

	elems = [i[0] for i in namepossibilities]
	probs = [i[1] for i in namepossibilities]
	norm = [float(i) / sum(probs) for i in probs]

	return (elems, norm)
	

def PlayerReferenceIndefinite(playerinfo):
	
	#these references are more than a pronoun, but do not contain a proper name
	referentpossibilities = []
	if not isManager(playerinfo):
		role = playerinfo['n_FunctionCode']
		if role&1: #keeper
			referentpossibilities.append(['de doelman', 5])
			referentpossibilities.append(['de keeper', 5])
		elif role&2: #defender
			referentpossibilities.append(['de verdediger', 5])
			referentpossibilities.append(['de achterhoedespeler', 3])
		elif role&4: #midfielder
			referentpossibilities.append(['de middenvelder', 5])
		elif role&8: #attacker
			referentpossibilities.append(['de aanvaller', 5])
			referentpossibilities.append(['de spits', 5])
	else:
		referentpossibilities.append(['de manager', 10])
		referentpossibilities.append(['de trainer', 10])
		referentpossibilities.append(['de keuzeheer', 1]) #this is from Merijn :) 

	return referentpossibilities
	
def ClubReferenceModel(club, jsongamedata, homeaway, gap, **kwargs):
	previousgaps = kwargs['previousgaplist']
	previousreference = []
	# Get all the tuples, since these are the previous processed named entities
	for idx, previousgap in enumerate(previousgaps):
		if isinstance(previousgap, tuple):
			# If the named entity is the same as the club of the current event, save the named entity and how far back the reference was
			if previousgap[0] == club:
				previousreference.append(previousgap[1])
	# If there is no mention of the club in the last sentence, just use the name of the club
	namepossibilities = []
	if (len(previousreference) == 0):
		namepossibilities.append([club, 10])
	else:
		if club not in previousreference:
			namepossibilities.append([club, 50])
		if jsongamedata['MatchInfo'][0]['c_HomeTeam']==club:
			homeOrAway = 1
			if 'de thuisploeg' not in previousreference:
				namepossibilities.append(['de thuisploeg', 10])
		else:
			homeOrAway = -1
			if ('de uitploeg') not in previousreference:
				namepossibilities.append(['de uitploeg', 10])

		for person in jsongamedata['MatchLineup']:
			if isManager(person) and person['n_HomeOrAway']==homeOrAway:
				manager = person['c_Person']
				managerinfo = person
				break
		if ('de ploeg van manager ' + manager) not in previousreference:
			namepossibilities.append(['de ploeg van manager ' + manager, 10])
		citydict = {}
		workbook = xlrd.open_workbook(r'Clubs and Nicknames.xlsx')
		worksheets = workbook.sheet_names()[0]
		worksheet = workbook.sheet_by_name(worksheets)
		for curr_row in range(worksheet.nrows):
			curr_cell = 1
			excelclub = worksheet.cell_value(curr_row, curr_cell)
			curr_cell = 3
			excelcity = worksheet.cell_value(curr_row, curr_cell)
			citydict.update({excelclub: excelcity})
		if club in citydict:
			if ('de club uit ' + citydict[club]) not in previousreference:
				namepossibilities.append(['de club uit ' + citydict[club], 10])

	elems = [i[0] for i in namepossibilities]
	probs = [i[1] for i in namepossibilities]
	norm = [float(i) / sum(probs) for i in probs]
	namechoice = numpy.random.choice(elems, p=norm)
	
	#add manager to mentioned entities to avoid ambiguous pronouns
	if "van manager" in namechoice:
		mentionedentities = kwargs['mentionedentities']
		if manager not in mentionedentities:
			mentionedentities[manager] = {'mentions':[], 'entityinfo':managerinfo}
		mentionedentities[manager]['mentions'].append(
									{ 'sentidx': kwargs['idx'],
									   'gapidx': kwargs['gapidx'],
									   'mention': namechoice,
									   'mentiontype': ReferenceType.DEFINITE}
								)		
	
	nametuple = (club, namechoice)
	return nametuple
	
#TODO: seems like PlayerReferringExpression and disambiguatingReferringExpression could
#      either be joined or at least renamed to be more clear
def PlayerReferringExpression(playerinfo, jsongamedata, homeaway, gap, **kwargs):
	mentionedentities = kwargs['mentionedentities']
	currentsentidx = kwargs['idx']
	currentgapidx = kwargs['gapidx']
	previous_mentions = kwargs['previous_mentions']
	number_of_total_mentions = kwargs['number_of_total_mentions']
	mention_number = kwargs['mention_number']

	if 'lastseason' in kwargs:
		lastseason = kwargs['lastseason']
	else:
		lastseason = False

	playerfullname = playerinfo['c_Person']

	#Format: [(Possibility1, ChoiceProb), (Possibility2, ChoiceProb) 
	namepossibilities = []

	if debug:
		print('\n###Referring expression generation:###')
		print('Current template: '+kwargs['templatetext'])
		print('Current player: '+playerfullname)

	#find the competing antecedent
	competing_antecedent_same_sent = False
	competing_antecedent_prev_sent = False
	first_occur_this_player_this_sent = True
	if currentgapidx>0:
		#this is not the first gap in this sentence. Is the previous gap also a person (and not this player)?
		previousgapsthissent = [mentionedentities[entity] for entity in mentionedentities for mention in mentionedentities[entity]['mentions'] if mention['sentidx']==currentsentidx and mention['gapidx']<currentgapidx and 'c_Person' in mentionedentities[entity]['entityinfo'] and  mentionedentities[entity]['entityinfo']!=playerinfo]
		prev_mentions_this_player_this_sent = [entity for entity in previousgapsthissent if entity['entityinfo']==playerinfo]
		first_occur_this_player_this_sent = len(prev_mentions_this_player_this_sent)==0
		#if previous gaps are not mentions of this player, it is a competing antecedent in same sentence
		if len(previousgapsthissent)>0:
			competing_antecedent_same_sent = True
	else:
		previousgapsthissent = []
	#TODO: If this is NOT the first occurrence of this player in this sent, 
	#      and there is a competing antecedent, I can disambiguate these two players
	
	#Is there maybe an entity mentioned in a previous sentence?
	previoussentgaps = [mentionedentities[entity] for entity in mentionedentities for mention in mentionedentities[entity]['mentions'] if mention['sentidx']<currentsentidx and mention['sentidx']>(currentsentidx-2) and mentionedentities[entity]['entityinfo'] != playerinfo]
	if len(previoussentgaps)>0:
		competing_antecedent_prev_sent = True
	
	if debug:
		if currentgapidx>0:
			print('prev_mentions_this_player_this_sent: '+str(prev_mentions_this_player_this_sent))
		print('Index of this gap:'+str(currentgapidx))
		print('Prev gaps in the current sentence: ')
		pp.pprint(previousgapsthissent)
#		if 'previoussentgaps' in locals():
		print('Gaps in the previous sentence: ')
		pp.pprint(previoussentgaps)
		#print('Previous mentions in general: ')
		#pp.pprint([{player: mentionedentities[player]['mentions']} for player in mentionedentities])
		print("Is player's first mention in this sent? "+str(first_occur_this_player_this_sent))
		print("Is there a competing antecedent in this sent? "+str(competing_antecedent_same_sent))
		print("Is there a competing antecedent in previous sent? "+str(competing_antecedent_prev_sent))
	otherplayersinfo = previousgapsthissent + previoussentgaps
	return disambiguatingReferringExpression(playerinfo,otherplayersinfo, lastseason=lastseason, previous_mentions=previous_mentions, number_of_total_mentions=number_of_total_mentions, mention_number=mention_number)
	
	
def isManager(playerinfo):
	return playerinfo['n_FunctionCode']&16

def disambiguatingReferringExpression(targetplayerinfo,otherplayersinfo, **kwargs):
	#captain, role, shirt number, nationality
	listoffeatures = ['b_Captain', 'c_Function', 'n_ShirtNr', 'c_PersonNatioShort']
	featureisdisambiguating = [True, True, True, True]
	prevteamdisambiguates = True
	formerteamtarget = ""
	lastseason = kwargs['lastseason']
	previous_mentions = kwargs['previous_mentions']
	number_of_total_mentions = kwargs['number_of_total_mentions']
	mention_number = kwargs['mention_number']

	targetplayerdata = getPlayerData(targetplayerinfo,**kwargs)

	# Get the last team of the player
	currentteamtarget = targetplayerinfo['c_Team']
	league_list = targetplayerdata['PlayerLeague']

	# Check all seasons that this player played so far
	for season in reversed(league_list):

		# Find the season that the player played in at the time of the report
		if season['c_Team'] == currentteamtarget:
			index = league_list.index(season)

			# Find the team the player played before this one (if possible)
			for season_index in reversed(range(index)):
				if league_list[season_index]['c_Team'] != currentteamtarget:
					formerteamtarget = league_list[season_index]['c_Team']
					break
			break

	# If we have no info...
	if formerteamtarget == '':
		prevteamdisambiguates = False
	
	# If our targetplayer is not a captain, this is not a good feature
	if targetplayerinfo['b_Captain']==False:
		listoffeatures.pop(0)
		featureisdisambiguating.pop(0)
	
	for player in otherplayersinfo:
		for idx,feature in enumerate(listoffeatures):
			if targetplayerinfo[listoffeatures[idx]]==player['entityinfo'][listoffeatures[idx]]:
				featureisdisambiguating[idx] = False
		playerdata = getPlayerData(player['entityinfo'],**kwargs)
		previousteams = [seasons['c_Team'] for seasons in playerdata['PlayerLeague']]
		if formerteamtarget in previousteams:
			prevteamdisambiguates = False
	
	#Format: [(Referent1, ChoiceProbWeight), ...]
	disambiguatedReferents = []
	roles = [reference[0] for reference in PlayerReferenceIndefinite(targetplayerinfo)]
	for idx,featureworks in enumerate(featureisdisambiguating):
		if featureworks:
			featurename = listoffeatures[idx]
			if featurename=='b_Captain':
				disambiguatedReferents.append(['de aanvoerder', 10])
			if featurename=='n_ShirtNr':
				if not otherplayersinfo:
					disambiguatedReferents.append(['de nummer '+str(targetplayerinfo['n_ShirtNr'])+'',2])
			if featurename=='c_Function':
				disambiguatedReferents = disambiguatedReferents + PlayerReferenceIndefinite(targetplayerinfo)
			if featurename=='c_PersonNatioShort':
				countryInfo = getCountryNames(targetplayerinfo[featurename],**kwargs)
				if countryInfo:
					disambiguatedReferents.append(['de '+countryInfo['Demonym'], 5]) #de Duitser
					if number_of_total_mentions < 4:
						disambiguatedReferents.append(['de '+countryInfo['Adjective']+'e speler', 3])
					#TODO: This is actually disambiguating on TWO characteristics
					#de Duitse middenvelder
					for role in roles:
						if number_of_total_mentions < 4:
							disambiguatedReferents.append([role.replace('de ','de '+countryInfo['Adjective']+'e ',1), 10])
	if prevteamdisambiguates and not lastseason:
		disambiguatedReferents.append(['de voormalig '+ formerteamtarget + ' speler', 5])
		disambiguatedReferents.append(['de voormalig speler van ' + formerteamtarget, 5])
		for role in roles:
			role = role.replace('de ','',1)
			disambiguatedReferents.append(['de voormalig ' + role + ' van ' + formerteamtarget, 5])
			disambiguatedReferents.append(['de voormalig '+formerteamtarget+' '+role, 5])
	
	elems = [i[0] for i in disambiguatedReferents]
	probs = [i[1] for i in disambiguatedReferents]
	norm = [float(i) / sum(probs) for i in probs]
	
	if debug:
		for idx,elem in enumerate(elems):
			elems[idx] = "|"+elem+"| ["+targetplayerinfo['c_Person']+"]"
	
	return (elems, norm)


#loads the player data (former clubs and previous seasons) from file if not already in kwargs
#otherwise just returns it
def getPlayerData(playerinfo,**kwargs):
	if 'jsonplayerdata' not in kwargs:
			kwargs['jsonplayerdata'] = {}
	if playerinfo['n_PersonID'] not in kwargs['jsonplayerdata']:
		#read file and put it in there
		playerfile = "./JSONPlayerData/player_"+str(playerinfo['n_PersonID'])+".json"
		try:
			with open(playerfile, 'rb') as f:
				jsonplayerdata = json.load(f)
				#remove duplicate info
				del jsonplayerdata['PlayerInfo'] 
				kwargs['jsonplayerdata']['n_PersonID'] = jsonplayerdata
		except:
			print ("Error while opening "+playerfile+" ", sys.exc_info()[0])
			kwargs['jsonplayerdata']['n_PersonID'] = {  "PlayerCup": [],
												        "PlayerInternational": [],
														"PlayerInternationalclub": [],
														"PlayerLeague": []
													 }
	return kwargs['jsonplayerdata']['n_PersonID']
	
	
def getCountryNames(countryShortForm,**kwargs):
	if 'countryData' not in kwargs:
		kwargs['countryData'] = {}
		try:
			with open('./Databases/Nationalities.tsv','r') as f:
				for line in f:
					ShortForm,CountryName,Adjective,Demonym = line.strip().split('\t')
					info = { 	'CountryName': CountryName, 
						'Adjective': Adjective,
						'Demonym': Demonym
					}
					kwargs['countryData'][ShortForm] = info
		except:
			print("Error while opening ./Databases/Nationalities.tsv", sys.exc_info()[1])
	if countryShortForm not in kwargs['countryData']:
		kwargs['countryData'][countryShortForm] = {}
	return kwargs['countryData'][countryShortForm]
	