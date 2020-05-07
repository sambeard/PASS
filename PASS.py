from Governing_module import TopicWalk
import re
import os
import sys
import pickle
from Info_dict_module import InfoDict

def main(file, savestate='n'):
    templatetexthome, templatetextaway, templatetextneutral, templatedict, jsongamedata = TopicWalk(file)
    infodict = InfoDict(jsongamedata)
    print(templatetexthome)
    print(templatetextaway)
    print(templatetextneutral)
    print(templatedict)
    print(infodict)
    if savestate == 'y':
        newfile = os.path.splitext(os.path.basename(file))[0]
        newfile = re.sub(r'goal', '', newfile)

        with open('./SavedReports/' + newfile + 'home.txt', 'wb') as f:
            print(newfile + 'home.txt saved')
            f.write(bytes(templatetexthome, 'UTF-8'))

        with open('./SavedReports/' + newfile + 'away.txt', 'wb') as f:
            print(newfile + 'away.txt saved')
            f.write(bytes(templatetextaway, 'UTF-8'))

        with open('./SavedReports/' + newfile + 'neutral.txt', 'wb') as f:
            print(newfile + 'neutral.txt saved')
            f.write(bytes(templatetextneutral, 'UTF-8'))

        with open('./SavedReports/' + newfile + 'matchdict.p', 'wb') as f:
            print(newfile + 'matchdict.p saved')
            pickle.dump(templatedict, f)

        with open('./SavedReports/' + newfile + 'infodict.p', 'wb') as f:
            print(newfile + 'infodict.p saved')
            pickle.dump(infodict, f)

def selectreport1819(filename, savestate = 'n'):
    currentpath = os.getcwd()
    if filename.endswith('.json'):
        main(currentpath + '/JSONGameData/Eredivisie/2018-2019/' + filename, savestate)
    else:
        print("file doesn't exist, did you add .json to the end?")

def selectreport1516(filename, savestate = 'n'):
    currentpath = os.getcwd()
    if filename.endswith('.json'):
        main(currentpath + '/JSONGameData/Eredivisie/2015-2016/' + filename, savestate)
    else:
        print("file doesn't exist, did you add .json to the end?")


currentpath = os.getcwd()
print("Current path = ", currentpath)
#textpath = os.path.dirname(currentpath) + '/Europa_League/TestInfoXMLs'
#onlyfiles = [textpath + '/' + f for f in os.listdir(textpath) if os.path.isfile(os.path.join(textpath, f))]
#for file in onlyfiles:
    #main(file, 'y')

###selectreport1819('ado_aja_20190224.json','y')
#selectreport1819('az_emm_20190202.json','y')
selectreport1516('gra_psv_20151031.json','y')
#main(os.path.dirname(currentpath) + '/Europa_League/NewInfoXMLs/rea_aja_5032019.xml', 'y')
###main(currentpath + '/JSONGameData/2goals_1scorer_succession.json', 'y')
#if __name__ == '__main__':
    #main(sys.argv[1:])