import sys
import os.path
import re
import random
from operator import itemgetter

def winninggoalwithassist(jsongamedata, gamecourselist, idx):
    if 'assist' in gamecourselist[idx]:
        #homegoals = jsongamedata.find('highlights').find('home').find('goalscorerslist').findChildren()
        #awaygoals = jsongamedata.find('highlights').find('away').find('goalscorerslist').findChildren()
        homegoals = jsongamedata['MatchInfo'][0]['n_HomeGoals']
        awaygoals = jsongamedata['MatchInfo'][0]['n_AwayGoals']
        # If both teams have scored and the final goal difference was one
        if (homegoals > 0) and (awaygoals > 0) and (abs(homegoals - awaygoals) == 1):
            # If the goal was the last goal by the winning team
            # Check which team has made the most goals
            if homegoals > awaygoals:
                winningteam = 'home'
                losingteam = 'away'
            else:
                winningteam = 'away'
                losingteam = 'home'
            # If this goal is the final goal by the winning team, it is the winning goal as well (since this goal meant they won with the 1 goal difference)
            if idx == len(gamecourselist) - 1:
                return True
            # If not, check if there were any other goals made by this team
            else:
                # First make a list after the event
                afterevents = gamecourselist[idx + 1:]
                # Then search the list for goals for the winning team (penalty goal, regular goal, or own goal by other team)
                for event in afterevents:
                    if ((event['event'] == 'regular goal') and (event['team'] == winningteam)) or ((event['event'] == 'penalty goal') and (event['team'] == winningteam)) or ((event['event'] == 'own goal') and (event['team'] == losingteam)):
                        # If a goal for the winning team is found, the goal is not the winning goal
                        return False
                # If there were no other goals for the winning team found, the goal is the winning goal
                return True
    else:
        return False

def winninggoal(jsongamedata, gamecourselist, idx):
    homegoals = jsongamedata['MatchInfo'][0]['n_HomeGoals']
    awaygoals = jsongamedata['MatchInfo'][0]['n_AwayGoals']
    # If both teams have scored and the final goal difference was one
    if (homegoals > 0) and (awaygoals > 0) and (abs(homegoals - awaygoals) == 1):
        # If the goal was the last goal by the winning team
        # Check which team has made the most goals
        if homegoals > awaygoals:
            winningteam = 'home'
            losingteam = 'away'
        else:
            winningteam = 'away'
            losingteam = 'home'
        # If this goal is the final goal by the winning team, it is the winning goal as well (since this goal meant they won with the 1 goal difference)
        if idx == len(gamecourselist) - 1:
            return True
        # If not, check if there were any other goals made by this team
        else:
            # First make a list after the event
            afterevents = gamecourselist[idx + 1:]
            # Then search the list for goals for the winning team (penalty goal, regular goal, or own goal by other team)
            for event in afterevents:
                if ((event['event'] == 'regular goal') and (event['team'] == winningteam)) or ((event['event'] == 'penalty goal') and (event['team'] == winningteam)) or ((event['event'] == 'own goal') and (event['team'] == losingteam)):
                    # If a goal for the winning team is found, the goal is not the winning goal
                    return False
            # If there were no other goals for the winning team found, the goal is the winning goal
            return True


def onlygoal(jsongamedata, gamecourselist, idx):
    homegoals = jsongamedata['MatchInfo'][0]['n_HomeGoals']
    awaygoals = jsongamedata['MatchInfo'][0]['n_AwayGoals']
    # If the total amount of goals is one, it is the only goal made
    if homegoals + awaygoals == 1:
        return True
    else:
        return False


def finalgoal(gamecourselist, idx):
    #There should be more than one goal scored in the match for this condition to fire
    goalnumber = 0
    for event in gamecourselist:
        if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (event['event'] == 'own goal'):
            if 'player' in event:
                goalnumber += 1
            else:
                goalnumber += 2
    if goalnumber > 1:
        # If the goal is the last entry in the gamecourselist, it is the final goal
        if idx == len(gamecourselist) - 1:
            return True
        # Else, check if there were goals scored after the event
        else:
            # First make a list after the event
            afterevents = gamecourselist[idx + 1:]
            # Then search the list for goals
            for event in afterevents:
                if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (event['event'] == 'own goal'):
                    return False
            return True
    else:
        return False


def secondgoal(gamecourselist, idx):
    # Check the name of the goalscorer
    player = gamecourselist[idx]['player']
    # First event of the game can never be the second+ goal of a player
    if idx == 0:
        return False
    # Check the events before the current events
    beforeevents = gamecourselist[:idx]
    numbergoals = 0
    for event in beforeevents:
        if (type(event) == dict) and ((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')):
            # Get all the values for keys containing 'player'
            players = [value for key, value in event.items() if 'player' in key]
            for player in players:
                if player == gamecourselist[idx]['player']:
                    numbergoals += 1
    if numbergoals > 1:
        return 'goal ' + str(numbergoals)
    else:
        return False


def earlygoal(gamecourselist, idx, homeaway):
    #For now, I only use the first goal of the match
    if idx == 0:
        # Check the events before the current events
        beforeevents = gamecourselist[:idx]
        for event in beforeevents:
            if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (event['event'] == 'own goal'):
                return False
        # Check the minute the goal is scored
        minute = gamecourselist[idx]['minute_asFloat']
        # For now, the goals that are scored in the first 10 minutes of the first or second half are marked as early goals
        if (minute <= 10) or ((minute >= 45) and (minute <= 55)):
            return True
        else:
            return False


def leadgoal(gamecourselist, idx):
    # For now, I only mark the first goal in the game as the lead goal (I could revise this: every goal that changes the equal score to a lead
    if idx == 0:
        return True
    # Check the events before the current events
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (event['event'] == 'own goal'):
            return False
    return True


def anschlusstreffer(homeaway, gamecourselist, idx):
    # First two goals can never be an anschlusstreffer
    if idx <= 1:
        return False
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if ((event['event'] == 'regular goal') and (event['team'] == focus)) or ((event['event'] == 'penalty goal') and (event['team'] == focus)) or ((event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif ((event['event'] == 'regular goal') and (event['team'] == other)) or ((event['event'] == 'penalty goal') and (event['team'] == other)) or ((event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                focusgoals += 2
    # There should have been a lead of two goals for one team for this goal to be the anschlusstreffer
    if abs(focusgoals - othergoals) == 2:
        # And this goal should be a goal that brings the difference back to one
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) == 1:
            return True
        else:
            return False
    else:
        return False

def lateequalizer(homeaway, gamecourselist, idx):
    # First goal can never be an equalizer
    if idx == 0:
        return False
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or ((event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or ((event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # There should have been a lead of 1 goal for the focus team for this goal to be the equalizer
    if abs(focusgoals - othergoals) == 1:
        # And this goal should be a goal that brings the difference to zero
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) == 0:
            #And the minute should be at least the 80th to be a late equalizer
            if gamecourselist[idx]['minute_asFloat'] >= 80:
                return True
            else:
                return False
        else:
            return False
    else:
        return False



def equalizer(homeaway, gamecourselist, idx):
    # First goal can never be an equalizer
    if idx == 0:
        return False
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or (
            (event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or (
            (event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # There should have been a lead of 1 goal for the focus team for this goal to be the equalizer
    if abs(focusgoals - othergoals) == 1:
        # And this goal should be a goal that brings the difference to zero
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) == 0:
            return True
        else:
            return False
    else:
        return False


def twoplusdifference(homeaway, gamecourselist, idx):
	# TODO: consider that this template will activate multiple times,
	# i.e. for a game that has a 6-0. It would be more suited for a final score of 2+?
    # First two goals can never result in a 2+ goal difference
    if idx <= 1:
        return False
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or (
                    (event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or (
            (event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                focusgoals += 2
    # There should have been a lead of at least 2 goals already for the other team for this goal to be the two+ goal difference
    difference = abs(focusgoals - othergoals)
    if difference >= 2:
        # And this goal should make it more
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) > difference:
            return True
        else:
            return False
    else:
        return False


def twodifference(homeaway, gamecourselist, idx):
    # First goal can never result in a 2 goal difference
    if idx == 0:
        return False
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or ((event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or (
            (event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # There should have been a lead of 1 goal already for one team for this goal to be the two goal difference
    if abs(focusgoals - othergoals) == 1:
        # And this goal should be a goal that brings the difference to two
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) == 2:
            return True
        else:
            return False
    else:
        return False

def withassist(gamecourselist, idx):
    if 'assist' in gamecourselist[idx]:
        return True
    else:
        return False


def twosuccessive(gamecourselist, idx):
    if idx == len(gamecourselist) - 1:
        return False
    #do not activate the template if the same player did both goals
    if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx + 1]['event'] == 'regular goal')) and (gamecourselist[idx]['player'] != gamecourselist[idx + 1]['player']) and (gamecourselist[idx]['team'] == gamecourselist[idx + 1]['team']):
        return True
    else:
        return False

def ergebniskosmetik(homeaway, gamecourselist, idx):
    # First two goals can never result in an ergebniskosmetik
    if idx <= 1:
        return False
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or (
            (event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or (
            (event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # There should have been a lead of at least 2 goals for one team for this goal to be the ergebniskosmetik
    difference = abs(focusgoals - othergoals)
    if difference >= 2:
        #And this goal should make the difference one less
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) < difference:
            # Besides that, this goal should be the last goal of the game
            # Which is the case if this is the last event of the game
            if idx == len(gamecourselist) - 1:
                return True
            # If the event is not the last event, look at the afterevents
            afterevents = gamecourselist[idx + 1:]
            # And see if one of those events is a goal
            for event in afterevents:
                if ((event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (
                    event['event'] == 'own goal')):
                    return False
            return True
        else:
            return False
    else:
        return False

def multitwiceyellow(gamestatisticslist, idx):
    #There should be more than one gamestatistics event to have multiple yellow/reds
    yellowredcount = 0
    for event in gamestatisticslist:
        if type(event) == dict:
            if event['event'] == 'twice yellow':
                if 'player 1' in event:
                    return True
                else:
                    yellowredcount += 1
    if yellowredcount < 2:
        return False
    else:
        newdict = {'event': 'twice yellow'}
        num = 0
        for idx2, event in enumerate(gamestatisticslist):
            if (type(gamestatisticslist[idx2]) == dict) and (gamestatisticslist[idx2]['event'] == 'twice yellow'):
                num += 1
                for key in gamestatisticslist[idx2]:
                    if key != 'event':
                        newdict.update({key + ' ' + str(num): gamestatisticslist[idx2][key]})
                gamestatisticslist[idx2] = ''
                gamestatisticslist[idx] = newdict
        return True

def twicefocus(homeaway, gamestatisticslist, idx):
    if (type(gamestatisticslist) == dict) and (gamestatisticslist[idx]['team'] == homeaway):
        return True
    else:
        return False

def multiyellowcards(gamestatisticslist, idx):
    yellowcount = 0
    for event in gamestatisticslist:
        if type(event) == dict:
            if event['event'] == 'yellow card':
                if 'player 1' in event:
                    return True
                else:
                    yellowcount += 1
    if yellowcount <= 1:
        return False
    else:
        newdict = {'event': 'yellow card'}
        num = 0
        for idx2, event in enumerate(gamestatisticslist):
            if gamestatisticslist[idx2]['event'] == 'yellow card':
                num += 1
                for key in gamestatisticslist[idx2]:
                    if key != 'event':
                        newdict.update({key + ' ' + str(num): gamestatisticslist[idx2][key]})
                gamestatisticslist[idx2] = ''
        gamestatisticslist[idx] = newdict
        return True

def oneyellowcards(gamestatisticslist):
    #For now, every yellow card from 1 until infinity is using this rule, in the future this should possibly apply to multiple yellow cards only
    yellowcount = 0
    for event in gamestatisticslist:
        if type(event) == dict:
            if event['event'] == 'yellow card':
                if 'player' in event:
                    yellowcount += 1
    if yellowcount == 1:
        return True
    else:
        return False

def earlyredcard(gamestatisticslist, idx):
    #For now, I only use the first red card of the match
    if idx == 0:
        # Check the events before the current events
        beforeevents = gamestatisticslist[:idx]
        for event in beforeevents:
            if (event['event'] == 'red card'):
                return False
        # Check the minute the goal is scored
        minute = gamestatisticslist[idx]['minute_asFloat']
        # For now, the goals that are scored in the first 10 minutes of the first half are marked as early reds
        if minute <= 10:
            return True
        else:
            return False

def redfocus(homeaway, gamestatisticslist, idx):
    if gamestatisticslist[idx]['team'] == homeaway:
        return True
    else:
        return False

def finaltwoplusdifference(jsongamedata):
    homegoals = jsongamedata['MatchInfo'][0]['n_HomeGoals']
    awaygoals = jsongamedata['MatchInfo'][0]['n_AwayGoals']
    finaldifference = abs(homegoals-awaygoals)
    if finaldifference > 2:
        return True
    else:
        return False

def manygoals(jsongamedata):
    homegoals = jsongamedata['MatchInfo'][0]['n_HomeGoals']
    awaygoals = jsongamedata['MatchInfo'][0]['n_AwayGoals']
    if homegoals + awaygoals > 5:
        return True
    else:
        return False

def nogoals(jsongamedata):
    homegoals = jsongamedata['MatchInfo'][0]['n_HomeGoals']
    awaygoals = jsongamedata['MatchInfo'][0]['n_AwayGoals']
    if homegoals + awaygoals == 0:
        return True
    else:
        return False

def focusredcards(gamestatisticslist, homeaway):
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    for idx, event in enumerate(gamestatisticslist):
        if ((event['event'] == 'red card') or (event['event'] == 'twice yellow')) and (event['team'] == focus):
            return True
    return False

def otherredcards(gamestatisticslist, homeaway):
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    for idx, event in enumerate(gamestatisticslist):
        if ((event['event'] == 'red card') or (event['event'] == 'twice yellow')) and (event['team'] == other):
            return True
    return False

def winnerredcards(gamecourselist, gamestatisticslist, homeaway):
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'

    focusgoals = 0
    othergoals = 0
    # Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or (
            (event['event'] == 'penalty goal') and (event['team'] == homeaway)) or ((event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or (
            (event['event'] == 'penalty goal') and (event['team'] != homeaway)) or ((event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    #The winner has scored more goals
    if othergoals > focusgoals:
        winner = other
    if focusgoals > othergoals:
        winner = focus
    else:
        return False
    for idx, event in enumerate(gamestatisticslist):
        if ((event['event'] == 'red card') or (event['event'] == 'twice yellow')) and (event['team'] == focus) and (winner == focus):
            return True
        if ((event['event'] == 'red card') or (event['event'] == 'twice yellow')) and (event['team'] == other) and (winner == other):
            return True
    return False

def loserredcards(gamecourselist, gamestatisticslist, homeaway):
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'

    focusgoals = 0
    othergoals = 0
    # Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or (
                    (event['event'] == 'penalty goal') and (event['team'] == homeaway)) or (
            (event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or (
                    (event['event'] == 'penalty goal') and (event['team'] != homeaway)) or (
            (event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # The winner has scored more goals
    if othergoals > focusgoals:
        winner = other
    if focusgoals > othergoals:
        winner = focus
    for idx, event in enumerate(gamestatisticslist):
        if ((event['event'] == 'red card') or (event['event'] == 'twice yellow')) and (event['team'] == focus) and (winner != focus):
            return True
        if ((event['event'] == 'red card') or (event['event'] == 'twice yellow')) and (event['team'] == other) and (winner != other):
            return True
    return False

def finalgoalfocusteam(gamecourselist, homeaway):
    #There should be more than one goal scored in the match for this condition to fire
    goalnumber = 0
    goaleventteam = []
    for event in gamecourselist:
        if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal'):
            goalnumber += 1
            goaleventteam.append(event['team'])
    if goalnumber > 1:
        # If the goal is the last entry in the goaleventlist, it is the final goal
        if goaleventteam[-1] == homeaway:
            return True
        else:
            return False
    else:
        return False

    '''
    num = len(gamecourselist)-1
    while num >= 0:
        #Don't work with own goals
        if gamecourselist[num]['event'] == 'own goal':
            return False
        if (gamecourselist[num]['event'] == 'regular goal') or (gamecourselist[num]['event'] == 'penalty goal'):
            if gamecourselist[num]['team'] == homeaway:
                return True
            else:
                return False
        num -= 1
    return False
    '''

def finalgoaltitle(gamecourselist, homeaway):
    #There should be more than one goal scored in the match for this condition to fire
    goalnumber = 0
    goaleventteam = []
    for event in gamecourselist:
        if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal'):
            goalnumber += 1
            goaleventteam.append(event['team'])
    if goalnumber > 1:
        return True
    else:
        return False

def focusteamplayedaway(homeaway):
    if homeaway == 'away':
        return True
    else:
        return False

def lateequalizerfocusteam(homeaway, gamecourselist, idx):
    # First goal can never be an equalizer
    if idx == 0:
        return False
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    #And no goals have been made after this goal
    afterevents = gamecourselist[idx + 1:]
    for event in afterevents:
        if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (event['event'] == 'own goal'):
            return False
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or (
                    (event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or (
            (event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # There should have been a lead of 1 goal for the focus team for this goal to be the equalizer
    if abs(focusgoals - othergoals) == 1:
        # And this goal should be a goal that brings the difference to zero
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) == 0:
            #And the minute should be at least the 80th to be a late equalizer
            if gamecourselist[idx]['minute_asFloat'] >= 80:
                #And the goal should be made by the focus team
                if gamecourselist[idx]['team'] == homeaway:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def lateequalizerotherteam(homeaway, gamecourselist, idx):
    # First goal can never be an equalizer
    if idx == 0:
        return False
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    #And no goals have been made after this goal
    afterevents = gamecourselist[idx + 1:]
    for event in afterevents:
        if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (event['event'] == 'own goal'):
            return False
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or \
                ((event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or (
            (event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # There should have been a lead of 1 goal for the focus team for this goal to be the equalizer
    if abs(focusgoals - othergoals) == 1:
        # And this goal should be a goal that brings the difference to zero
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) == 0:
            #And the minute should be at least the 80th to be a late equalizer
            if gamecourselist[idx]['minute_asFloat'] >= 80:
                #And the goal should be made by the focus team
                if gamecourselist[idx]['team'] != homeaway:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

# ===== START SUBSTITUTIONS ============= 

def substitution(gamecourselist, focusteam , idx):
    if(gamecourselist[idx]['event'] != 'substitution'):
        raise Exception("Wrong event for this rule")

    current_event = gamecourselist[idx]
    current_team = current_event['team']
    consecutive = False
    #  start with next event
    i = 1
    while(i < 3):
        # check if there is a next event
        if (idx + i >= len(gamecourselist)):
            break
        next_event = gamecourselist[idx+i]
        # check whether it's a substitution and for the same team
        if(next_event['event'] != 'substitution' or next_event['team'] != current_team):
            break
        # break if they were consecutive but not any more
        if((next_event['minute'] == current_event['minute']) != consecutive):
            # make exception if they become consecutive
            if(not consecutive):
                consecutive = True
            else:
                break
        i+=1
    return (i,current_team==focusteam, consecutive)

# Check if the goal was scored by someone just subbed on
def fastgoalaftersubstitution(gamecourselist, homeaway, idx):
    # If the goal is the first event of the game, there can never be a substitution before it
    if (idx != 0) and gamecourselist[idx]['event'] == 'regular goal' or gamecourselist[idx]['event'] == 'goal from penalty' :
        goal = gamecourselist[idx]
        goalminute = goal['minute_asFloat']
        playername = goal['player']
        beforeevents = gamecourselist[:idx]
        # Check for all events that happened before the goal
        for event in beforeevents:
            # Go on if the event is a substitution
            if (event['event'] == 'substitution'):
                sub = event
                # Check if this player was subbed on
                if 'player' in sub:
                    if sub['player'] == playername:
                        subminute = sub['minute_asFloat']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True
                elif 'player 3' in sub:
                    if sub['player 1'] == playername:
                        subminute = sub['minute_asFloat 1']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True

                    elif sub['player 2'] == playername:
                        subminute = sub['minute_asFloat 2']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True

                    elif sub['player 3'] == playername:
                        subminute = sub['minute_asFloat 3']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True


                elif 'player 2' in sub:
                    if sub['player 1'] == playername:
                        subminute = sub['minute_asFloat 1']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True

                    elif sub['player 2'] == playername:
                        subminute = sub['minute_asFloat 2']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True

        return False
    else:
        return False

# Check if the assist was provided by someone just subbed on
def fastassistaftersubstitution(gamecourselist, homeaway, idx):
    # If the assisted goal is the first event of the game, there can never be a substitution before it, also a penalty
    # is obviously never assisted, so also not taken into account.
    if (idx != 0) and gamecourselist[idx]['event'] == 'regular goal' and 'assist' in gamecourselist[idx]:
        goal = gamecourselist[idx]
        goalminute = goal['minute_asFloat']
        assistplayername = goal['assist']
        beforeevents = gamecourselist[:idx]
        # Check for all events that happened before the goal
        for event in beforeevents:
            # Go on if the event is a substitution
            if (event['event'] == 'substitution'):
                sub = event
                # Check if this player was subbed on
                if 'player' in sub:
                    if sub['player'] == assistplayername:
                        subminute = sub['minute_asFloat']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True
                elif 'player 3' in sub:
                    if sub['player 1'] == assistplayername:
                        subminute = sub['minute_asFloat 1']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True

                    elif sub['player 2'] == assistplayername:
                        subminute = sub['minute_asFloat 2']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True

                    elif sub['player 3'] == assistplayername:
                        subminute = sub['minute_asFloat 3']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True


                elif 'player 2' in sub:
                    if sub['player 1'] == assistplayername:
                        subminute = sub['minute_asFloat 1']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True

                    elif sub['player 2'] == assistplayername:
                        subminute = sub['minute_asFloat 2']
                        # Check if this happened within 10 minutes
                        if (goalminute - subminute) <= 10:
                            return True
        return False
    else:
        return False

# Check if the new substitute has made a direct contribution to the score (goal or assist)
def positivesubstitutionfocusteam(gamecourselist, homeawawy, idx):
    raise NotImplementedError()

# Check if the new substitute has made a direct contribution to the score (goal or assist)
def positivesubstitutionotherteam(gamecourselist, homeaway, idx):
    raise NotImplementedError()


def negativesubstitutionfocusteam(gamecourselist, homeaway, idx):
    raise NotImplementedError()


def negativesubstitutionotherteam(gamecourselist, homeaway, idx):
    raise NotImplementedError()

# ========== END SUBSTITUTION


def latelossfocusteam(homeaway, gamecourselist, idx):
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    #And no goals have been made after this goal
    afterevents = gamecourselist[idx + 1:]
    for event in afterevents:
        if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (event['event'] == 'own goal'):
            return False
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or (
                    (event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or (
            (event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # The standings should be equal for this goal to be a late defeat, and goals should be scored
    if (abs(focusgoals - othergoals) == 0) and (focusgoals != 0) and (othergoals != 0):
        # And this goal should be a goal that gives the other team a one goal lead
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) == 1:
            #And the minute should be at least the 80th to be a late equalizer
            if gamecourselist[idx]['minute_asFloat'] >= 80:
                #And the goal should be made by the other team
                if gamecourselist[idx]['team'] != homeaway:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def latewinfocusteam(homeaway, gamecourselist, idx):
    # Assign who is the focus team and who the other
    if homeaway == 'home':
        focus = homeaway
        other = 'away'
    else:
        focus = homeaway
        other = 'home'
    #And no goals have been made after this goal
    afterevents = gamecourselist[idx + 1:]
    for event in afterevents:
        if (event['event'] == 'regular goal') or (event['event'] == 'penalty goal') or (event['event'] == 'own goal'):
            return False
    # Get the score before the current goal
    focusgoals = 0
    othergoals = 0
    beforeevents = gamecourselist[:idx]
    for event in beforeevents:
        if (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == focus)) or (
                    (event['event'] == 'own goal') and (event['team'] == other)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        elif (((event['event'] == 'regular goal') or (event['event'] == 'penalty goal')) and (event['team'] == other)) or (
            (event['event'] == 'own goal') and (event['team'] == focus)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    # The standings should be equal for this goal to be a late win
    if (abs(focusgoals - othergoals) == 0) and (focusgoals != 0) and (othergoals != 0):
        # And this goal should be a goal that gives the focus team a one goal lead
        if ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == focus)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == other)):
            focusgoals += 1
        elif ((gamecourselist[idx]['event'] == 'regular goal') and (gamecourselist[idx]['team'] == other)) or ((event['event'] == 'penalty goal') and (gamecourselist[idx]['team'] == other)) or ((gamecourselist[idx]['event'] == 'own goal') and (gamecourselist[idx]['team'] == focus)):
            othergoals += 1
        if abs(focusgoals - othergoals) == 1:
            #And the minute should be at least the 80th to be a late equalizer
            if gamecourselist[idx]['minute_asFloat'] >= 80:
                #And the goal should be made by the other team
                if gamecourselist[idx]['team'] == homeaway:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def focusteamredcard(gamestatisticslist, homeaway):
    focusteamreds = 0
    otherteamreds = 0
    for idx, event in enumerate(gamestatisticslist):
        if (event['event'] == 'red card') or (event['event'] == 'twice yellow'):
            if event['team'] == homeaway:
                focusteamreds += 1
            else:
                otherteamreds += 1
    if (focusteamreds > 0) and (otherteamreds == 0):
        return True
    else:
        return False

def otherteamredcard(gamestatisticslist, homeaway):
    focusteamreds = 0
    otherteamreds = 0
    for idx, event in enumerate(gamestatisticslist):
        if (event['event'] == 'red card') or (event['event'] == 'twice yellow'):
            if event['team'] == homeaway:
                focusteamreds += 1
            else:
                otherteamreds += 1
    if (focusteamreds == 0) and (otherteamreds > 0):
        return True
    else:
        return False

def comebacklossfocus(gamecourselist, homeaway):
    differencelist = []
    focusgoals = 0
    othergoals = 0
    #Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] == homeaway)) or ((event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] != homeaway)) or ((event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
        #And see how much more (or less) goals the other team has made
        differencelist.append(othergoals - focusgoals)
    try:
        maxdifference = max(differencelist)
    except ValueError:
        return False
    #If the difference at one point was 3 goals or more in favor of the other team, it opens up the possibility for a comeback
    if maxdifference >= 3:
        #Get the differences after the maximum difference
        maxidx = differencelist.index(max(differencelist))
        afterdifference = differencelist[maxidx + 1:]
        #If there were changes to the score after the maximum difference
        if len(afterdifference) > 0:
            #And the difference was at one point one goal or less, there was a comeback
            if min(afterdifference) <= 1:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def comebackother(gamecourselist, homeaway):
    differencelist = []
    focusgoals = 0
    othergoals = 0
    #Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] == homeaway)) or ((event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] != homeaway)) or ((event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
        #And see how much more (or less) goals the other team has made
        differencelist.append(othergoals - focusgoals)
    try:
        mindifference = min(differencelist)
    except ValueError:
        #A ValueError means a goalless match
        return False
    #If the difference at one point was 2 goals or more in favor of the focus team, it opens up the possibility for a comeback
    if mindifference <= -2:
        #If the other team has won, it is a comeback for the other team
        if differencelist[-1] > 0:
            return True
        else:
            return False
    else:
        return False

def comebackfocus(gamecourselist, homeaway):
    differencelist = []
    focusgoals = 0
    othergoals = 0
    #Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] == homeaway)) or ((event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] != homeaway)) or ((event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
        #And see how much more (or less) goals the other team has made
        differencelist.append(othergoals - focusgoals)
    try:
        maxdifference = max(differencelist)
    except ValueError:
        #A ValueError means a goalless match
        return False
    #If the difference at one point was 2 goals or more in favor of the other team, it opens up the possibility for a comeback
    if maxdifference >= 2:
        #If the focus team has won, it is a comeback for the focus team
        if differencelist[-1] < 0:
            return True
        else:
            return False
    else:
        return False

def closeloss(gamecourselist, homeaway):
    differencelist = []
    focusgoals = 0
    othergoals = 0
    #Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] == homeaway)) or ((event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] != homeaway)) or ((event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
        #And see how much more (or less) goals the other team has made
        differencelist.append(othergoals - focusgoals)
    #If the other team has won with a one goal difference, it is a close loss
    try:
        if differencelist[-1] == 1:
            return True
        else:
            return False
    except IndexError:
        #A goalless match
        return False

def closewin(gamecourselist, homeaway):
    differencelist = []
    focusgoals = 0
    othergoals = 0
    #Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] == homeaway)) or ((event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] != homeaway)) or ((event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
        #And see how much more (or less) goals the other team has made
        differencelist.append(othergoals - focusgoals)
    #If the focus team has won with a one goal difference, it is a close win
    try:
        if differencelist[-1] == -1:
            return True
        else:
            return False
    except IndexError:
        #A goalless match
        return False

def bigloss(gamecourselist, homeaway):
    differencelist = []
    focusgoals = 0
    othergoals = 0
    #Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] == homeaway)) or ((event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] != homeaway)) or ((event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
        #And see how much more (or less) goals the other team has made
        differencelist.append(othergoals - focusgoals)
    #If the other team has won with more than a three goal difference, it is a big loss
    try:
        if differencelist[-1] > 2:
            return True
        else:
            return False
    except IndexError:
        #A goalless match
        return False

def winner(gamecourselist, homeaway):
    differencelist = []
    focusgoals = 0
    othergoals = 0
    #Get the goals for the focus team and other team
    for eventidx, event in enumerate(gamecourselist):
        if ((event['event'] == 'regular goal') and (event['team'] == homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] == homeaway)) or ((event['event'] == 'own goal') and (event['team'] != homeaway)):
            if 'player' in event:
                focusgoals += 1
            else:
                focusgoals += 2
        if ((event['event'] == 'regular goal') and (event['team'] != homeaway)) or ((event['event'] == 'penalty goal') and (event['team'] != homeaway)) or ((event['event'] == 'own goal') and (event['team'] == homeaway)):
            if 'player' in event:
                othergoals += 1
            else:
                othergoals += 2
    if (focusgoals > othergoals) or (othergoals > focusgoals):
        return True
    else:
        return False

def otherTeam(focusTeam):
    return "away" if focusTeam == "home" else "home"

def isTeamWinning(gameCourseList, focusTeam, idx):
    other = otherTeam(focusTeam)
    goals = {focusTeam:0, other:0 }
    # Get the goals for the focus team and other team so far
    previousEvents = gameCourseList[:idx]
    for eventidx, event in enumerate(previousEvents):
        if (event['event'] == 'regular goal' or event['event'] == 'penalty goal' or event['event'] == 'own goal'):
            team = event['team']
            # add score to other team if own goal
            if(event['event'] == 'own goal'):
                team = otherTeam(team)
            # add two because of merging of events
            goals[team] += 1 if 'player' in event else 2
    return goals[focusTeam] > goals[other]

def isTeamTieing(gameCourseList, focusTeam, idx):
    return not isTeamWinning(gameCourseList, focusTeam, idx) and not isTeamWinning(gameCourseList, otherTeam(focusTeam), idx)

def freekickgoal(jsongamedata, gamecourselist, idx):
    # The event should of course be a goal
    if gamecourselist[idx]['event'] == 'regular goal':
        goal = gamecourselist[idx]
        # Go through all match actions trying to find the freekick goal
        for goaltocompare in jsongamedata['MatchActions']:
            if goaltocompare['c_Action'] == 'Doelpunt' and goaltocompare['c_ActionMinute'].rstrip("'") == goal['minute'] and goaltocompare['c_Person'] == goal['player']:
                foundgoal = goaltocompare
                if foundgoal['c_ActionReason'] == 'Vrije trap':
                    return True
                else:
                    return False
        return False
    else:
        return False

def header(jsongamedata, gamecourselist, idx):
    # The event should of course be a goal
    if gamecourselist[idx]['event'] == 'regular goal':
        goal = gamecourselist[idx]
        # Go through all match actions trying to find the header goal
        for goaltocompare in jsongamedata['MatchActions']:
            if goaltocompare['c_Action'] == 'Doelpunt' and goaltocompare['c_ActionMinute'].rstrip("'") == goal['minute'] and goaltocompare['c_Person'] == goal['player']:
                foundgoal = goaltocompare
                if foundgoal['c_ActionInfo'] == 'Kopbal':
                    return True
                else:
                    return False
        return False
    else:
        return False

