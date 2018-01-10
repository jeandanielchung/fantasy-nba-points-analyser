from __future__ import print_function
import sys
import urllib2
from bs4 import BeautifulSoup
from game import Game
import datetime

def is_row(tag):
	return 'evenrow' in tag['class'] or 'oddrow' in tag['class']

def print_games(games, scoring = None):
	if (len(games) == 0):
		print('No games meet this criteria')
	else:
		for game in games:
			if (scoring):
				print(game.print_with_fpts(scoring))
			else:
				print(game)

def find_ave(games, scoring):
	# sum of fpts of each game / number of games
	games = filter(lambda x: x.min, games) # get rid of the games not played
	if (len(games) == 0):
		return -1.0
	return sum(map(lambda x: x.get_fpts(scoring), games)) / float(len(games))
	# return filter(lambda x: x.min, games)

# could also do a binary search for starting and ending points because should already be sorted, but would still have to grab all of those games O(n)
def filter_by_date(games, start, end):
	return filter(lambda x: start <= x.date <= end, games)

def filter_by_min(games, operator, value):
	if (operator == '<'):
		return filter(lambda x: x.min < value, games)
	elif (operator == '='):
		return filter(lambda x: x.min == value, games)
	else:
		return filter(lambda x: x.min > value, games)

def filter_by_recent(games, number):
	return games if len(games) <= number else games[number * -1:]

def scrape(page):
	try:
		soup = BeautifulSoup(page, 'html.parser')

		stat_table = soup.find("div", class_="mod-player-stats")

		regular_stats = stat_table.find(lambda x: x.name == "tr" and "stathead" in x['class'] and "REGULAR" in x.string.upper()) # TODO: verify format of regular

		games = []

		for cur_row in regular_stats.next_siblings:
			if 'stathead' in cur_row['class'] or cur_row.contents[0].string in ['Averages', 'Totals']: # stop before preseason or Averages/Totals row
				break
			elif ('evenrow' in cur_row['class'] or 'oddrow' in cur_row['class']) and '/' in cur_row.contents[0].string: # make sure that first value is a date
				games.append(cur_row)


		# games = regular_stats.find_all("tr", class_=["evenrow", "oddrow"]) # going to need to 

		# print(games)


		# gets the column names to see what the stats correspond with
		col_head = soup.find(class_='colhead')
		heads = [head.string if head.string != '3PM-3PA' else '3PM' for head in col_head.find_all("td")]

		wanted_stats = ['DATE', 'MIN', '3PM', 'REB', 'AST', 'BLK', 'STL', 'TO', 'PTS'] # can generalise this
		scoring = {'date': 0, 'min': 0, 'threes': 1, 'reb': 2, 'ast': 2, 
		'blk': 4, 'stl': 3, 'to': -1, 'pts': 1, 'dd': 5, 'td': 10}

		game_objs = []

		for game in games:
			stats = game.find_all('td')

			if stats[0].string == 'Averages':
				break

			statVals = []

			for i, stat in enumerate(stats):
				if (heads[i] in wanted_stats):
					statStr = stat.string if stat.string else 'N/A'
					if heads[i] == '3PM': statStr = statStr.split('-')[0]
					if heads[i] == 'DATE': statStr = statStr.split(' ')[1]
					# TODO: change the 3pm stat
					statVals.append(statStr)

			game_obj = Game(statVals)
			print(str(game_obj) + ' || ' + '{:>3}'.format(str(game_obj.get_fpts(scoring))))
			game_objs.append(game_obj)

		print('Average: ' + str(find_ave(game_objs, scoring)))
		print()
		user_prompt(game_objs, scoring)
	except:
		print("there was an error reading the given url, make sure that the page is a valid ESPN NBA player's gamelog e.g. (http://www.espn.com/nba/player/gamelog/_/id/3908845/john-collins)")

def user_prompt(game_objs, scoring):
	while (True):
		try:
			query = raw_input('Enter filter type (date/min/recent) or q to quit: ').strip()
			if (query == 'q'):
				break

			result = 0
			filtered_games = []
			if (query == 'date'):
				query = raw_input('Enter dates separated by space: ').strip()
				query_list = query.split(' ') # TODO: need to do input checking
				date1 = query_list[0].split('-')
				date2 = query_list[1].split('-')
				beforeDate = datetime.date(int(date1[0]), int(date1[1]), int(date1[2]))
				afterDate = datetime.date(int(date2[0]), int(date2[1]), int(date2[2]))
				filtered_games = filter_by_date(game_objs, beforeDate, afterDate)
				result = find_ave(filtered_games, scoring)

			elif (query == 'min'):
				query = raw_input('Enter one of {=,<,>} then value separated by space (e.g < 30): ').strip()
				query_list = query.split(' ')
				operator = query_list[0]
				value = int(query_list[1]) # need to use as int
				filtered_games = filter_by_min(game_objs, operator, value)
				result = find_ave(filtered_games, scoring)

			elif (query == 'recent'):
				query = raw_input('Enter number of most recent games: ').strip()
				filtered_games = filter_by_recent(game_objs, int(query))
				result = find_ave(filtered_games, scoring)

			else:
				print('invalid query')
				continue

			# print query results
			print_games(filtered_games, scoring)
			print('Average: ' + str(result) + ' in ' + str(len(filtered_games)) + ' games')
		except:
			print("incorrect input")

	print('bye!')

def main():
	player_page_url = raw_input("enter link to player's game log: ") if len(sys.argv) < 2 else sys.argv[1]
	try:
		page = urllib2.urlopen(player_page_url)
		scrape(page)
	except:
		print("given url is not valid")

if __name__ == "__main__":
	main()