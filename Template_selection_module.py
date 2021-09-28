import Ruleset_module as Ruleset
import random
import numpy
from Info_variety_module import InfoVariety

def GeneralTemplateSelection(type, possiblelegend, possibletemplates, gamecourselist, gamestatisticslist, soup, homeaway):
    possibletemplates = InfoVariety(homeaway, possibletemplates)

    if type == 'title':
        #Collect all templates that fit the Ruleset-criteria first
        possibletitles = []
        for idx, event in enumerate(gamecourselist):
            # Check if there was a goal made that fits the conditions of the deciding goal, if so, add it to the title possibilities
            if Ruleset.winninggoal(soup, gamecourselist, idx) == True:
                categorytemplates = possibletemplates[possiblelegend.index("Title (deciding goal)")]
                try:
                    #If the Rule was True, select a random template from the category
                    template = random.choice(categorytemplates)
                    #And add this random choice with a certain weight to it. The higher the weight, the higher the chance the template gets chosen
                    #From all the categories
                    possibletitles.append([template, 0.5])
                #IndexError means that there were no templates to choose from, this means we skip the category
                except IndexError:
                    ''
                break
            # If the focus team made a late equalizer, add that category to the title possibilities
            if (Ruleset.lateequalizerfocusteam(homeaway, gamecourselist, idx) == True) or (Ruleset.lateequalizerotherteam(homeaway, gamecourselist, idx) == True):
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("Title (late equalizer)")]
                    try:
                        template = random.choice(categorytemplates)
                        possibletitles.append([template, 0.5])
                    except IndexError:
                        ''
                except ValueError:
                    ''
                break
            if Ruleset.lateequalizerfocusteam(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("Title (late equalizer focus team)")]
                    try:
                        template = random.choice(categorytemplates)
                        possibletitles.append([template, 0.5])
                    except IndexError:
                        ''
                except ValueError:
                    ''
                break
            # If the other team made a late equalizer, add that category to the title possibilities
            if Ruleset.lateequalizerotherteam(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("Title (late equalizer other team)")]
                    try:
                        template = random.choice(categorytemplates)
                        possibletitles.append([template, 0.5])
                    except IndexError:
                        ''
                except ValueError:
                    ''
                break

            if (Ruleset.latelossfocusteam(homeaway, gamecourselist, idx) == True) or (Ruleset.latewinfocusteam(homeaway, gamecourselist, idx) == True):
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("Title (late win/loss)")]
                    try:
                        template = random.choice(categorytemplates)
                        possibletitles.append([template, 0.5])
                    except IndexError:
                        ''
                except ValueError:
                    ''
                break
            # If the the focus team suffered a late defeat, add this category to the title possibilities
            if Ruleset.latelossfocusteam(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("Title (late loss focus team)")]
                    try:
                        template = random.choice(categorytemplates)
                        possibletitles.append([template, 0.5])
                    except IndexError:
                        ''
                except ValueError:
                    ''
                break

            # If the the focus team booked a late victory, add this category to the title possibilities
            if Ruleset.latewinfocusteam(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("Title (late win focus team)")]
                    try:
                        template = random.choice(categorytemplates)
                        possibletitles.append([template, 0.5])
                    except IndexError:
                        ''
                except ValueError:
                    ''
                break

        # If the final score difference is more than two, add that category to the title possibilities
        if Ruleset.finaltwoplusdifference(soup) == True:
            categorytemplates = possibletemplates[possiblelegend.index("Title (two+ goal difference)")]
            try:
                template = random.choice(categorytemplates)
                possibletitles.append([template, 0.5])
            except IndexError:
                ''
        # If there were more than 5 goals during the game, add that category to the title possibilities
        if Ruleset.manygoals(soup) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (many goals)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
        if (Ruleset.manygoals(soup) == True) and (Ruleset.winner(gamecourselist, homeaway) == True):
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (many goals win)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if (Ruleset.manygoals(soup) == True) and (Ruleset.winner(gamecourselist, homeaway) == False):
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (many goals win)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        # If there were no goals during the game, add that category to the title possibilities
        if Ruleset.nogoals(soup) == True:
            categorytemplates = possibletemplates[possiblelegend.index("Title (no goals)")]
            try:
                template = random.choice(categorytemplates)
                possibletitles.append([template, 0.5])
            except IndexError:
                ''
        # If the focus team or other team suffered at least one red card, add these categories to the title possibilities
        if Ruleset.focusredcards(gamestatisticslist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (focus team player sent off)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
        # If the losing team got a red card, add these categories to the title possibilities
        if Ruleset.otherredcards(gamestatisticslist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (other team player sent off)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
        #If the winning team got a red card, add these categories to the title possibilities
        if Ruleset.winnerredcards(gamecourselist, gamestatisticslist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (winning team player sent off)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
            if Ruleset.loserredcards(gamecourselist, gamestatisticslist, homeaway) == True:
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("Title (losing team player sent off)")]
                    try:
                        template = random.choice(categorytemplates)
                        possibletitles.append([template, 0.5])
                    except IndexError:
                        ''
                except ValueError:
                    ''

        # If the focus team made the final (not own) goal, add that category to the title possibilities
        if Ruleset.finalgoalfocusteam(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (final goal focus team)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
        # If the focus team played away, add that category to the title possibilities
        if Ruleset.focusteamplayedaway(homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (focus team played away)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
        # If the focus team played home, add that category to the title possibilities
        if Ruleset.focusteamplayedaway(homeaway) == False:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (focus team played home)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        # If the focus team made a comeback (but still lost), add that category to the title possibilities
        if Ruleset.comebacklossfocus(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (focus team played home)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        # If the other team made a comeback, add that category to the title possibilities
        if Ruleset.comebackother(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (comeback other team)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        # If the focus team made a comeback, add that category to the title possibilities
        if Ruleset.comebackfocus(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (comeback other team)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if Ruleset.closeloss(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (close loss)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if Ruleset.bigloss(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (big loss)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if Ruleset.closewin(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (close win)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if Ruleset.winner(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (win)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if Ruleset.winner(gamecourselist, homeaway) == False:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (tie)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if (Ruleset.winner(gamecourselist, homeaway) == False) and (Ruleset.finalgoaltitle(gamecourselist, homeaway) == True):
            try:
                categorytemplates = possibletemplates[possiblelegend.index("Title (tie and goals)")]
                try:
                    template = random.choice(categorytemplates)
                    possibletitles.append([template, 0.14])
                except IndexError:
                    ''
            except ValueError:
                ''

        try:
            categorytemplates = possibletemplates[possiblelegend.index("Title (all purpose)")]
            try:
                template = random.choice(categorytemplates)
                possibletitles.append([template, 0.1])
            except IndexError:
                ''
        except ValueError:
            ''

        #Normalize the probabilities
        elems = [i[0] for i in possibletitles]
        probs = [i[1] for i in possibletitles]
        norm = [float(i) / sum(probs) for i in probs]

        #And make a random weighted choice
        template = numpy.random.choice(elems, p=norm)
        return template

    if type == 'general':
        possiblewintieloss = []

        # If the focus team received at least one red card and the other team did not, add this category to the win/tie/loss possibilities
        if Ruleset.focusteamredcard(gamestatisticslist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (red card focus team)")]
                try:
                    template = random.choice(categorytemplates)
                    possiblewintieloss.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        # If the other team received at least one red card and the focus team did not, add this category to the win/tie/loss possibilities
        if Ruleset.otherteamredcard(gamestatisticslist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (red card other team)")]
                try:
                    template = random.choice(categorytemplates)
                    possiblewintieloss.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if Ruleset.winner(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (win)")]
                try:
                    template = random.choice(categorytemplates)
                    possiblewintieloss.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if Ruleset.winner(gamecourselist, homeaway) == False:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (tie)")]
                try:
                    template = random.choice(categorytemplates)
                    possiblewintieloss.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        try:
            categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (all purpose)")]
            try:
                template = random.choice(categorytemplates)
                possiblewintieloss.append([template, 0.5])
            except IndexError:
                ''
        except ValueError:
            ''

        elems = [i[0] for i in possiblewintieloss]
        probs = [i[1] for i in possiblewintieloss]
        norm = [float(i) / sum(probs) for i in probs]
        template = numpy.random.choice(elems, p=norm)
        return template

    if type == 'final_score':
        possiblefinalscore = []

        for idx, event in enumerate(gamecourselist):
            # If the other team made a late equalizer, add that category to the final score possibilities
            if Ruleset.lateequalizerotherteam(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (final score) (late equalizer other team)")]
                    try:
                        template = random.choice(categorytemplates)
                        possiblefinalscore.append([template, 0.5])
                    except IndexError:
                        ''
                    break
                except ValueError:
                    ''

        # If the focus team made the final (not own) goal, add that category to the final score possibilities
        if Ruleset.finalgoalfocusteam(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (final score) (final goal focus team)")]
                try:
                    template = random.choice(categorytemplates)
                    possiblefinalscore.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
        for idx, event in enumerate(gamecourselist):
            if Ruleset.twoplusdifference(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (final score) (focus team equalize after 2+ goals down)")]
                    try:
                        template = random.choice(categorytemplates)
                        possiblefinalscore.append([template, 0.5])
                    except IndexError:
                        ''
                except ValueError:
                    ''
            break

        if Ruleset.comebackfocus(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (final score) (focus team comeback after 2+ goals down)")]
                try:
                    template = random.choice(categorytemplates)
                    possiblefinalscore.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''

        if Ruleset.winner(gamecourselist, homeaway) == True:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (final score) (win)")]
                try:
                    template = random.choice(categorytemplates)
                    possiblefinalscore.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
        if Ruleset.winner(gamecourselist, homeaway) == False:
            try:
                categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (final score) (tie)")]
                try:
                    template = random.choice(categorytemplates)
                    possiblefinalscore.append([template, 0.5])
                except IndexError:
                    ''
            except ValueError:
                ''
        try:
            categorytemplates = possibletemplates[possiblelegend.index("General, win/tie/loss (final score)")]
            try:
                template = random.choice(categorytemplates)
                possiblefinalscore.append([template, 0.5])
            except IndexError:
                ''
        except ValueError:
            ''

        elems = [i[0] for i in possiblefinalscore]
        probs = [i[1] for i in possiblefinalscore]
        norm = [float(i) / sum(probs) for i in probs]

        template = numpy.random.choice(elems, p=norm)
        return template

def GameCourseTemplateSelection(event, legend, templates, gamecourselist, soup, homeaway, idx, previoustemplates):
    # Delete the previously used templates from the possibletemplates, since you do not want duplicate templates

    templates = InfoVariety(homeaway, templates, previoustemplates)
    temptemplatelist = []

    # Check if the current team is the focus team or not
    if event['team'] == homeaway:
        if event['event'] == 'regular goal':
            if Ruleset.winninggoalwithassist(soup, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (winning goal with assist)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (winning goal with assist)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.winninggoal(soup, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (winning goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (winning goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.ergebniskosmetik(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (eretreffer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (eretreffer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.lateequalizer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (late equalizer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (late equalizer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.equalizer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (equalizer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (equalizer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.earlygoal(gamecourselist, idx, homeaway) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (early goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (early goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.anschlusstreffer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (aansluitingstreffer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (aansluitingstreffer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.twoplusdifference(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (two+ goal difference)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (two+ goal difference)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            if Ruleset.fastgoalaftersubstitution(gamecourselist, homeaway, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (fast goal after substitution)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (fast goal after substitution)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.75])
                except IndexError:
                    ''

            if Ruleset.fastassistaftersubstitution(gamecourselist, homeaway, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (fast assist after substitution)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (fast assist after substitution)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.75])
                except IndexError:
                    ''

            if Ruleset.withassist(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (with assist)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (with assist)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.25])
                except IndexError:
                    ''
            if Ruleset.twosuccessive(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (two successive goals one team)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (two successive goals one team)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.1])
                except IndexError:
                    ''

            if Ruleset.freekickgoal(soup, gamecourselist, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (free kick)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (free kick)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            if Ruleset.header(soup, gamecourselist, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal focus team (header)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (header)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            try:
                categorytemplates = templates[legend.index("Game course, regular goal focus team (all purpose)")]
            except ValueError:
                categorytemplates = templates[legend.index("Game course, regular goal (all purpose)")]
            try:
                template = random.choice(categorytemplates)
                temptemplatelist.append([template, 0.1])
            except IndexError:
                ''
        if event['event'] == 'own goal':
            if Ruleset.winninggoal(soup, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal focus team (winning goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (winning goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.finalgoal(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal focus team (final goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (final goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.earlygoal(gamecourselist, idx, homeaway) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal focus team (early goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (early goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.leadgoal(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal focus team (lead goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (lead goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.equalizer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal focus team (equalizer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (equalizer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.twoplusdifference(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal focus team (two+ goal difference)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (two+ goal difference)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.twodifference(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal focus team (two goal difference)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (two goal difference)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            if Ruleset.fastgoalaftersubstitution(gamecourselist, homeaway, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, own goal focus team (fast goal after substitution)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (fast goal after substitution)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.75])
                except IndexError:
                    ''

            try:
                categorytemplates = templates[legend.index("Game course, own goal focus team (all purpose)")]
            except ValueError:
                categorytemplates = templates[legend.index("Game course, own goal (all purpose)")]
            template = random.choice(categorytemplates)
            temptemplatelist.append([template, 0.1])
        if event['event'] == 'penalty goal':
            if Ruleset.ergebniskosmetik(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty focus team (eretreffer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (eretreffer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.finalgoal(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty focus team (final goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (final goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.anschlusstreffer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty focus team (aansluitingstreffer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (aansluitingstreffer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            if Ruleset.fastgoalaftersubstitution(gamecourselist, homeaway, idx):
                try:
                    categorytemplates = templates[
                        legend.index("Game course, goal from penalty focus team (fast goal after substitution)")]
                except ValueError:
                    categorytemplates = templates[
                        legend.index("Game course, goal from penalty (fast goal after substitution)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.75])
                except IndexError:
                    ''

            try:
                categorytemplates = templates[legend.index("Game course, goal from penalty focus team (all purpose)")]
            except ValueError:
                categorytemplates = templates[legend.index("Game course, goal from penalty (all purpose)")]
            try:
                template = random.choice(categorytemplates)
                temptemplatelist.append([template, 0.1])
            except IndexError:
                ''
        if event['event'] == 'missed penalty':
            try:
                categorytemplates = templates[legend.index("Game course, penalty miss focus team")]
            except ValueError:
                try:
                    categorytemplates = templates[legend.index("Game course, penalty miss focus team (all purpose)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, penalty miss (all purpose)")]
            try:
                template = random.choice(categorytemplates)
                temptemplatelist.append([template, 0.1])
            except IndexError:
                ''
        if event['event'] == 'substitution':

            # if Ruleset.tripleneutralsubstitutionfocusteam(gamecourselist, homeaway, idx):
            #     try:
            #         categorytemplates = templates[legend.index("Game course, substitution focus team (triple)")]
            #     except ValueError:
            #         categorytemplates = templates[legend.index("Game course, substitution (triple)")]
            #     try:
            #         template = random.choice(categorytemplates)
            #         temptemplatelist.append([template, 1])
            #     except IndexError:
            #         ''
            #
            # elif Ruleset.doubleneutralsubstitutionfocusteam(gamecourselist, homeaway, idx):
            #     try:
            #         categorytemplates = templates[legend.index("Game course, substitution focus team (double)")]
            #     except ValueError:
            #         categorytemplates = templates[legend.index("Game course, substitution (double)")]
            #     try:
            #         template = random.choice(categorytemplates)
            #         temptemplatelist.append([template, 0.5])
            #     except IndexError:
            #         ''
            #
            # if Ruleset.threeconsecutivesubstitutionsfocusteam(gamecourselist, homeaway, idx):
            #     try:
            #         categorytemplates = templates[legend.index("Game course, substitution focus team (three consecutive)")]
            #     except ValueError:
            #         categorytemplates = templates[legend.index("Game course, substitution (three consecutive)")]
            #     try:
            #         template = random.choice(categorytemplates)
            #         temptemplatelist.append([template, 1])
            #     except IndexError:
            #         ''
            #
            # elif Ruleset.twoconsecutivesubstitutionsfocusteam(gamecourselist, homeaway, idx):
            #     try:
            #         categorytemplates = templates[legend.index("Game course, substitution focus team (two consecutive)")]
            #     except ValueError:
            #         categorytemplates = templates[legend.index("Game course, substitution (two consecutive)")]
            #     try:
            #         template = random.choice(categorytemplates)
            #         temptemplatelist.append([template, 0.5])
            #     except IndexError:
            #         ''
            ## First check if team is winning, then check wat kind of subsitution (double or consecutive etc.)
            if Ruleset.focusteamwinning(gamecourselist, homeaway, idx):

                # If triple substitution (very rare)
                if Ruleset.tripleneutralsubstitutionfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution focus team (triple and winning)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (triple and winning)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If double substitution
                elif Ruleset.doubleneutralsubstitutionfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution focus team (double and winning)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (double and winning)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If three consecutive substitutions (without goals inbetween)
                elif Ruleset.threeconsecutivesubstitutionsfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution focus team (three consecutive and winning)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (three consecutive and winning)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If two consecutive substitutions
                elif Ruleset.twoconsecutivesubstitutionsfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution focus team (two consecutive and winning)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (two consecutive and winning)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''
                # Regular substitution
                else:
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution focus team (winning)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (winning)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

            ## First check if team is losing, then check wat kind of subsitution (double or consecutive etc.)
            elif Ruleset.focusteamlosing(gamecourselist, homeaway, idx):

                # If triple substitution (very rare)
                if Ruleset.tripleneutralsubstitutionfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution focus team (triple and losing)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (triple and losing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If double substitution
                elif Ruleset.doubleneutralsubstitutionfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution focus team (double and losing)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (double and losing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If three consecutive substitutions (without goals inbetween)
                elif Ruleset.threeconsecutivesubstitutionsfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution focus team (three consecutive and losing)")]
                    except ValueError:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (three consecutive and losing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If two consecutive substitutions
                elif Ruleset.twoconsecutivesubstitutionsfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution focus team (two consecutive and losing)")]
                    except ValueError:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (two consecutive and losing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''
                # Regular substitution
                else:
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution focus team (losing)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (losing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

            elif Ruleset.tieing(gamecourselist, homeaway, idx):

                # If triple substitution (very rare)
                if Ruleset.tripleneutralsubstitutionfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution focus team (triple and tieing)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (triple and tieing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If double substitution
                elif Ruleset.doubleneutralsubstitutionfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution focus team (double and tieing)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (double and tieing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If three consecutive substitutions (without goals inbetween)
                elif Ruleset.threeconsecutivesubstitutionsfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution focus team (three consecutive and tieing)")]
                    except ValueError:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (three consecutive and tieing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If two consecutive substitutions
                elif Ruleset.twoconsecutivesubstitutionsfocusteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution focus team (two consecutive and tieing)")]
                    except ValueError:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (two consecutive and tieing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''
                # Regular substitution
                else:
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution focus team (tieing)")]
                    except ValueError:
                        categorytemplates = templates[legend.index("Game course, substitution (tieing)")]
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

            else:
                try:
                    categorytemplates = templates[legend.index("Game course, substitution focus team (all purpose)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, substitution (all purpose)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.001])
                except IndexError:
                    ''
    else:
        #Get the regular goal rules
        if event['event'] == 'regular goal':
            # The templates for the most specific conditions that are true are preferred
            # Like the winning goal of the match
            if Ruleset.secondgoal(gamecourselist, idx) != False:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (second+ goal player)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (second+ goal player)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            #If the goal was the winning goal, use a winning goal template
            if Ruleset.winninggoal(soup, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (winning goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (winning goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            #If the goal was the only goal of the game, use the only goal template
            if Ruleset.onlygoal(soup, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (only goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (only goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            #If the goal was the final goal of the game, use the final goal template
            if Ruleset.finalgoal(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (final goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (final goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            #Now that we have had all varieties of last goals, let's prioritize the special non-last goals first
            if Ruleset.earlygoal(gamecourselist, idx, homeaway) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (early goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (early goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.leadgoal(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (lead goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (lead goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.anschlusstreffer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (aansluitingstreffer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (aansluitingstreffer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.equalizer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (equalizer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (equalizer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.twoplusdifference(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (two+ goal difference)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (two+ goal difference)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.twodifference(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (two goal difference)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (two goal difference)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            if Ruleset.fastgoalaftersubstitution(gamecourselist, homeaway, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (fast goal after substitution)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (fast goal after substitution)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.75])
                except IndexError:
                    ''

            if Ruleset.fastassistaftersubstitution(gamecourselist, homeaway, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (fast assist after substitution)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (fast assist after substitution)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.75])
                except IndexError:
                    ''

            if Ruleset.freekickgoal(soup, gamecourselist, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (free kick)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (free kick)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            if Ruleset.header(soup, gamecourselist, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (header)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (header)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            #If there were no special conditions, we use the regular all-purpose conditions
            if Ruleset.withassist(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (with assist)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (with assist)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.25])
                except IndexError:
                    ''
            if Ruleset.twosuccessive(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, regular goal other team (two successive goals one team)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, regular goal (two successive goals one team)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.1])
                except IndexError:
                    ''
            try:
                categorytemplates = templates[legend.index("Game course, regular goal other team (all purpose)")]
            except ValueError:
                categorytemplates = templates[legend.index("Game course, regular goal (all purpose)")]
            try:
                template = random.choice(categorytemplates)
                temptemplatelist.append([template, 0.1])
            except IndexError:
                ''
        if event['event'] == 'own goal':
            if Ruleset.anschlusstreffer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal other team (aansluitingstreffer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (aansluitingstreffer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.equalizer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal other team (equalizer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (equalizer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.earlygoal(gamecourselist, idx, homeaway) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, own goal other team (early goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (early goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            if Ruleset.fastgoalaftersubstitution(gamecourselist, homeaway, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, own goal other team (fast goal after substitution)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, own goal (fast goal after substitution)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.75])
                except IndexError:
                    ''

            try:
                categorytemplates = templates[legend.index("Game course, own goal other team (all purpose)")]
            except ValueError:
                categorytemplates = templates[legend.index("Game course, own goal (all purpose)")]
            try:
                template = random.choice(categorytemplates)
                temptemplatelist.append([template, 0.1])
            except IndexError:
                ''
        if event['event'] == 'penalty goal':
            if Ruleset.winninggoal(soup, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty other team (winning goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (winning goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.finalgoal(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty other team (final goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (final goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.secondgoal(gamecourselist, idx) != False:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty other team (second+ goal player)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (second+ goal player)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.leadgoal(gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty other team (lead goal)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (lead goal)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.equalizer(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty other team (equalizer)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (equalizer)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.twoplusdifference(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty other team (two+ goal difference)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (two+ goal difference)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''
            if Ruleset.twodifference(homeaway, gamecourselist, idx) == True:
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty other team (two goal difference)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (two goal difference)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.5])
                except IndexError:
                    ''

            if Ruleset.fastgoalaftersubstitution(gamecourselist, homeaway, idx):
                try:
                    categorytemplates = templates[legend.index("Game course, goal from penalty other team (fast goal after substitution)")]
                except ValueError:
                    categorytemplates = templates[legend.index("Game course, goal from penalty (fast goal after substitution)")]
                try:
                    template = random.choice(categorytemplates)
                    temptemplatelist.append([template, 0.75])
                except IndexError:
                    ''

            try:
                categorytemplates = templates[legend.index("Game course, goal from penalty other team (all purpose)")]
            except ValueError:
                categorytemplates = templates[legend.index("Game course, goal from penalty (all purpose)")]
            try:
                template = random.choice(categorytemplates)
                temptemplatelist.append([template, 0.1])
            except IndexError:
                ''
        if event['event'] == 'missed penalty':
            try:
                categorytemplates = templates[legend.index("Game course, penalty miss other team")]
            except ValueError:
                categorytemplates = templates[legend.index("Game course, penalty miss (all purpose)")]
            template = random.choice(categorytemplates)
            temptemplatelist.append([template, 0.1])
        if event['event'] == 'substitution':

            ## First check if team is winning, then check wat kind of subsitution (double or consecutive etc.)
            if Ruleset.otherteamwinning(gamecourselist, homeaway, idx):

                # If triple substitution (very rare)
                if Ruleset.tripleneutralsubstitutionotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution (triple and winning)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If double substitution
                elif Ruleset.doubleneutralsubstitutionotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (double and winning)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If three consecutive substitutions (without goals inbetween)
                elif Ruleset.threeconsecutivesubstitutionsotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (three consecutive and winning)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If two consecutive substitutions
                elif Ruleset.twoconsecutivesubstitutionsotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (two consecutive and winning)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''
                # Regular substitution
                else:
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution (winning)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

            ## First check if team is losing, then check wat kind of subsitution (double or consecutive etc.)
            elif Ruleset.otherteamlosing(gamecourselist, homeaway, idx):

                # If triple substitution (very rare)
                if Ruleset.tripleneutralsubstitutionotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (triple and losing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If double substitution
                elif Ruleset.doubleneutralsubstitutionotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (double and losing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If three consecutive substitutions (without goals inbetween)
                elif Ruleset.threeconsecutivesubstitutionsotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (three consecutive and losing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If two consecutive substitutions
                elif Ruleset.twoconsecutivesubstitutionsotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (two consecutive and losing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''
                # Regular substitution
                else:
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution (losing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

            elif Ruleset.tieing(gamecourselist, homeaway, idx):

                # If triple substitution (very rare)
                if Ruleset.tripleneutralsubstitutionotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (triple and tieing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If double substitution
                elif Ruleset.doubleneutralsubstitutionotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (double and tieing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If three consecutive substitutions (without goals inbetween)
                elif Ruleset.threeconsecutivesubstitutionsotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (three consecutive and tieing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

                # If two consecutive substitutions
                elif Ruleset.twoconsecutivesubstitutionsotherteam(gamecourselist, homeaway, idx):
                    try:
                        categorytemplates = templates[
                            legend.index("Game course, substitution (two consecutive and tieing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''
                # Regular substitution
                else:
                    try:
                        categorytemplates = templates[legend.index("Game course, substitution (tieing)")]
                    except ValueError:
                        categorytemplates = []
                    try:
                        template = random.choice(categorytemplates)
                        temptemplatelist.append([template, 0.5])
                    except IndexError:
                        ''

            if not temptemplatelist:
                temptemplatelist.append(["".strip(), 1])

    elems = [i[0] for i in temptemplatelist]
    probs = [i[1] for i in temptemplatelist]
    norm = [float(i) / sum(probs) for i in probs]

    template = numpy.random.choice(elems, p=norm)

    #Modify the gamecourselist if the template for two successive goals is chosen
    try:
        tstemplate = templates[legend.index("Game course, regular goal focus team (two successive goals one team)")]
    except ValueError:
        tstemplate = []
    try:
        tstemplate.extend(templates[legend.index("Game course, regular goal other team (two successive goals one team)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, regular goal (two successive goals one team)")])
    except ValueError:
        tstemplate.extend([])
    if template in tstemplate:
        newdict = {}
        for key in gamecourselist[idx]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 1': gamecourselist[idx][key]})
            else:
                newdict.update({key: gamecourselist[idx][key]})
        for key in gamecourselist[idx + 1]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 2': gamecourselist[idx + 1][key]})
        gamecourselist[idx] = newdict
        del gamecourselist[idx + 1]
        #And modify the template and legend

    # Modify the gamecourselist if the template for a triple substitution is chosen
    try:
        tstemplate = templates[legend.index("Game course, substitution focus team (triple)")]
    except ValueError:
        tstemplate = []
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (triple and winning)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (triple and losing)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (triple and tieing)")])
    except ValueError:
        tstemplate.extend([])

    try:
        tstemplate.extend(templates[legend.index("Game course, substitution other team (triple)")])
    except ValueError:
        tstemplate.extend([])

    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (triple)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (triple and winning)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (triple and losing)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (triple and tieing)")])
    except ValueError:
        tstemplate.extend([])

    if template in tstemplate:
        newdict = {}
        for key in gamecourselist[idx]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 1': gamecourselist[idx][key]})
            else:
                newdict.update({key: gamecourselist[idx][key]})
        for key in gamecourselist[idx + 1]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 2': gamecourselist[idx + 1][key]})
        for key in gamecourselist[idx + 2]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 3': gamecourselist[idx + 2][key]})
        gamecourselist[idx] = newdict
        del gamecourselist[idx + 1]
        del gamecourselist[idx + 1]
        # And modify the template and legend

    # Modify the gamecourselist if the template for a three consecutive substitution is chosen
    try:
        tstemplate = templates[legend.index("Game course, substitution focus team (three consecutive)")]
    except ValueError:
        tstemplate = []
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (three consecutive and winning)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (three consecutive and losing)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (three consecutive and tieing)")])
    except ValueError:
        tstemplate.extend([])

    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (three consecutive)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (three consecutive and winning)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (three consecutive and losing)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (three consecutive and tieing)")])
    except ValueError:
        tstemplate.extend([])

    if template in tstemplate:
        newdict = {}
        for key in gamecourselist[idx]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 1': gamecourselist[idx][key]})
            else:
                newdict.update({key: gamecourselist[idx][key]})
        for key in gamecourselist[idx + 1]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 2': gamecourselist[idx + 1][key]})
        for key in gamecourselist[idx + 2]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 3': gamecourselist[idx + 2][key]})
        gamecourselist[idx] = newdict
        del gamecourselist[idx + 1]
        del gamecourselist[idx + 1]
        # And modify the template and legend

    #Modify the gamecourselist if the template for a double substitution is chosen
    try:
        tstemplate = templates[legend.index("Game course, substitution focus team (double)")]
    except ValueError:
        tstemplate = []
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (double and winning)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (double and losing)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution focus team (double and tieing)")])
    except ValueError:
        tstemplate.extend([])

    try:
        tstemplate.extend(templates[legend.index("Game course, substitution other team (double)")])
    except ValueError:
        tstemplate.extend([])

    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (double)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (double and winning)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (double and losing)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (double and tieing)")])
    except ValueError:
        tstemplate.extend([])

    if template in tstemplate:
        newdict = {}
        for key in gamecourselist[idx]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 1': gamecourselist[idx][key]})
            else:
                newdict.update({key: gamecourselist[idx][key]})
        for key in gamecourselist[idx + 1]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 2': gamecourselist[idx + 1][key]})
        gamecourselist[idx] = newdict
        del gamecourselist[idx + 1]
        #And modify the template and legend

    #Modify the gamecourselist if the template for a two consecutive substitution is chosen
    try:
        tstemplate = templates[legend.index("Game course, substitution focus team (two consecutive)")]
    except ValueError:
        tstemplate = []
    try:
        tstemplate.extend(
            templates[legend.index("Game course, substitution focus team (two consecutive and winning)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(
            templates[legend.index("Game course, substitution focus team (two consecutive and losing)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(
            templates[legend.index("Game course, substitution focus team (two consecutive and tieing)")])
    except ValueError:
        tstemplate.extend([])

    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (two consecutive)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (two consecutive and winning)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (two consecutive and losing)")])
    except ValueError:
        tstemplate.extend([])
    try:
        tstemplate.extend(templates[legend.index("Game course, substitution (two consecutive and tieing)")])
    except ValueError:
        tstemplate.extend([])

    if template in tstemplate:
        newdict = {}
        for key in gamecourselist[idx]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 1': gamecourselist[idx][key]})
            else:
                newdict.update({key: gamecourselist[idx][key]})
        for key in gamecourselist[idx + 1]:
            if (key != 'event') and (key != 'team'):
                newdict.update({key + ' 2': gamecourselist[idx + 1][key]})
        gamecourselist[idx] = newdict
        del gamecourselist[idx + 1]
        #And modify the template and legend


    return gamecourselist, template


def GameStatisticsTemplateSelection(event, legend, templates, gamestatisticslist, soup, homeaway, idx, previoustemplates):
    templates = InfoVariety(homeaway, templates, previoustemplates)

    templatelist = []
    if event['event'] == 'twice yellow':
        possibletwiceyellowtemplates = []
        if Ruleset.multitwiceyellow(gamestatisticslist, idx) == True:
            categorytemplates = templates[legend.index("Game statistics, twice yellow (two+ players)")]
            try:
                template = random.choice(categorytemplates)
                possibletwiceyellowtemplates.append(template)
            except IndexError:
                ''
        if Ruleset.twicefocus(homeaway, gamestatisticslist, idx) == True:
            categorytemplates = templates[legend.index("Game statistics, twice yellow (focus team)")]
            try:
                template = random.choice(categorytemplates)
                possibletwiceyellowtemplates.append(template)
            except IndexError:
                ''
        if Ruleset.multitwiceyellow(gamestatisticslist, idx) == False:
            categorytemplates = templates[legend.index("Game statistics, twice yellow (one player)")]
            try:
                template = random.choice(categorytemplates)
                possibletwiceyellowtemplates.append(template)
            except IndexError:
                ''

        return template

    elif event['event'] == 'yellow card':
        possibleyellowtemplates = []
        if Ruleset.oneyellowcards(gamestatisticslist) == True:
            categorytemplates = templates[legend.index("Game statistics, yellow cards (one)")]
            try:
                template = random.choice(categorytemplates)
                possibleyellowtemplates.append(template)
            except IndexError:
                ''
        if Ruleset.multiyellowcards(gamestatisticslist, idx) == True:
            categorytemplates = templates[legend.index("Game statistics, yellow cards (multiple)")]
            try:
                template = random.choice(categorytemplates)
                possibleyellowtemplates.append(template)
            except IndexError:
                ''
        return template

    elif event['event'] == 'red card':
        possibleredtemplates = []
        if Ruleset.earlyredcard(gamestatisticslist, idx) == True:
            categorytemplates = templates[legend.index("Game statistics, red cards (early)")]
            try:
                template = random.choice(categorytemplates)
                possibleredtemplates.append(template)
            except IndexError:
                ''
        if Ruleset.redfocus(homeaway, gamestatisticslist, idx) == True:
            try:
                categorytemplates = templates[legend.index("Game statistics, red cards (focus team)")]
                try:
                    template = random.choice(categorytemplates)
                    possibleredtemplates.append(template)
                except IndexError:
                    ''
            except ValueError:
                ''

        categorytemplates = templates[legend.index("Game statistics, red cards")]
        try:
            template = random.choice(categorytemplates)
            possibleredtemplates.append(template)
        except IndexError:
            ''
        return template

    #If the gamestatisticslist is empty (i.e. there were no cards given during the match), use templates from the yellow cards (none) category
    elif event['event'] == None:
        categorytemplates = templates[legend.index("Game statistics, yellow cards (none)")]
        template = random.choice(categorytemplates)

        return template
