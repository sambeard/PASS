from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web.server import NOT_DONE_YET

	
from xml.etree.ElementTree import ElementTree
import os
import fnmatch
import time
import html
import cgi
import json
import glob
import pdb
import re

from Governing_module import TopicWalk
from Info_dict_module import InfoDict

class IndexPage(Resource):
	isLeaf = True
	def render_GET(self, request):

		#open index page template
		with open('HTML/index.html', 'r') as htmlfile:
			responsePage=htmlfile.read()
		
		home_teams = set()
		away_teams = set()
		teams_away_saw = dict()
		teams_home_saw = dict()
		filenames = dict()
		#check all available games
		for jsonFileName in glob.glob('JSONGameData/*.json'):
			jsonFileName = jsonFileName.replace("\\","/");
			#skip file without a date 1900-202* in the filename
			if not re.match(".*(19\d\d|2[01][012]\d).*",jsonFileName):
				continue
			with open(jsonFileName, 'rb') as f:
				jsongamedata = json.load(f)
				infodict = InfoDict(jsongamedata)
				home_team = infodict['home_team']
				away_team = infodict['away_team']
				date = infodict['match_date'].strftime('%d/%m/%Y')

				home_teams.add(home_team)
				away_teams.add(away_team)

				if home_team not in teams_home_saw:
					teams_home_saw[home_team] = []
				teams_home_saw[home_team].append(away_team+' ('+date+')')
				
				if away_team not in teams_away_saw:
					teams_away_saw[away_team] = []
				teams_away_saw[away_team].append(home_team+' ('+date+')')
				
				filenames[home_team+'_'+away_team+'_'+date]=jsonFileName
		
		home_teams = list(home_teams)
		away_teams = list(away_teams)
		
		responsePage = responsePage.replace('"[]"//###HOMETEAMS###',"'"+json.dumps(home_teams)+"'")
		responsePage = responsePage.replace('"[]"//###AWAYTEAMS###',"'"+json.dumps(away_teams)+"'")
		responsePage = responsePage.replace('"[]"//###TEAMSHOMESAW###',"'"+json.dumps(teams_home_saw)+"'")
		responsePage = responsePage.replace('"[]"//###TEAMSAWAYSAW###',"'"+json.dumps(teams_away_saw)+"'")
		responsePage = responsePage.replace('"[]"//###AVAILABLEFILES###',"'"+json.dumps(filenames)+"'")
		request.write(responsePage.encode('utf-8'))
		return 


class Generation(Resource):
	isLeaf = True
	
	def generate_Reports(self, request):
		#generate reports with PASS
		try:
			templatetexthome, templatetextaway, templatetextneutral, templatedict, gamedata = TopicWalk(self.filename)
		except Exception as err:
			print("Error generating report for "+self.filename)
			print(type(err))
			print(err.args)
			print(err)
			with open('HTML/results-error.html', 'r') as htmlfile:
				responsePage=htmlfile.read()
			request.write(responsePage.encode('utf-8'))
			request.finish()
			return
			
		with open('HTML/results-end.html', 'r') as htmlfile:
			responsePage=htmlfile.read()
		homereport = templatetexthome.strip().splitlines( )
		homereport.pop(0) #remove "Report for the supporters of $team"
		hometitle =  homereport.pop(0)
		awayreport = templatetextaway.strip().splitlines( )
		awayreport.pop(0) #remove "Report for the supporters of $team"
		awaytitle = awayreport.pop(0)
		responsePage = responsePage.replace('#TITLEHOME#',hometitle,1).replace('#TITLEAWAY#',awaytitle,1)
		homereporthtml = ""
		for line in homereport:
			homereporthtml = homereporthtml + "<p>"+line+"</p>"+"\n"
		awayreporthtml = ""
		for line in awayreport:
			awayreporthtml = awayreporthtml + "<p>"+line+"</p>"+"\n"		
		responsePage = responsePage.replace('#HOMEREPORT#',homereporthtml,1).replace('#AWAYREPORT#',awayreporthtml,1)
		responsePage = responsePage.replace('#JSONREPORTFILE#',self.filename)
		request.write(responsePage.encode('utf-8'))
		request.finish()
				
	def render_POST(self, request):
		filename = request.args[b"filename"][0].decode("utf-8")
		self.filename = filename
		arg1 = request.args[b"selectHome"][0].decode("utf-8")
		arg2 = request.args[b"selectAway"][0].decode("utf-8")
		resubmitted = b"resubmitted" in request.args
		

		#load resultsfile
		with open(filename, 'rb') as f:
			jsongamedata = json.load(f)
			infodict = InfoDict(jsongamedata)
			home_team = infodict['home_team']
			away_team = infodict['away_team']
			league = infodict['league']
			date = infodict['match_date'].strftime('%d/%m/%Y %HH:%MM')
			finalscore = infodict['final_score']
		
		#penalties
		if 'p' in finalscore:
			finalscore = re.sub(r'^(\d+)-(\d+) ?[-0-9,() ]*( (\d+)-(\d+)p)?$','\\1 (\\4 pen.)-\\2 (\\5 pen.)',finalscore)
		else:
			#if in doubt nuke everything after the first two numbers
			finalscore = re.sub(r'^(\d+)-(\d+).*','\\1-\\2',finalscore)
		
		teamhomegoals,teamawaygoals = finalscore.split('-')

		with open('HTML/results-start.html', 'r') as htmlfile:
			responsePage=htmlfile.read()
		
		responsePage = responsePage.replace('#FORMVALUE1#',arg1).replace('#FORMVALUE2#',arg2).replace('#FORMVALUE3#',filename)				
		responsePage = responsePage.replace('#LEAGUE#',league,1).replace('#DATETIME#',date)
		responsePage = responsePage.replace('#TEAMHOMEENCODED#',home_team).replace('#TEAMAWAYENCODED#',away_team)
		responsePage = responsePage.replace('#TEAMHOME#',home_team).replace('#TEAMAWAY#',away_team)
		responsePage = responsePage.replace('#RESULTHOME#',teamhomegoals).replace('#RESULTAWAY#',teamawaygoals)
		request.write(responsePage.encode('utf-8'))
		if not resubmitted:
			reactor.callLater(0.1, self.generate_Reports, request)
		else:
			reactor.callLater(0, self.generate_Reports, request)
		return NOT_DONE_YET
		
		
root = File('./HTML')

indexPage = IndexPage()
root.putChild(b"",indexPage)

generation = Generation()
root.putChild(b"generate", generation)

jsonGameData = File('./JsonGameData')
root.putChild(b"JSONGameData", jsonGameData)


factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8888)
endpoint.listen(factory)
print("listening on port 8888")
reactor.run()
