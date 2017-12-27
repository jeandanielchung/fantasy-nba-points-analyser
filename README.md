# Fantasy NBA Points Analyser 
### a simple CLI tool to help analyse an NBA player's game log in terms of fantasy points
##### Brief Overview
This tool is specifically for fantasy basektball points leagues where each category is given a fantasy point weighting. I quickly built this tool because I was evaluating a trade proposal and wanted to see how a player performed playing alongside a star teammate who got injured, but both ESPN's web and mobile apps only allow you to see a game log with fantasy point tallies only for a limited number of most recent games. I also wanted to get some more experience developing in Python and learn some basic web scraping (for the first time).

This extremely basic tool uses BeautifulSoup to pull all of a player's regular season games given an ESPN link to the player's game log (can be for previous years too). You will then see all of their stats along with their fantasy point total for each game and their fantasy point total average (excluding the games they didn't play of course). You can then filter by date or minutes played (the two criteria I found most useful to analyse) and see a filtered list of games along with the average fantasy points for those games.

##### Future Improvements
	- making points scoring system generic so that different ones can be used
	- adding different filters (e.g. rebounds) and desired anaylsis (e.g. totals instead of averages)
	- being able to search for players using their name and year wanted rather than supplying link
	- adding front-end

##### Running
###### 1. Clone the repository
`git clone https://github.com/jeandanielchung/fantasy-nba-points-analyser.git`
###### 2. Navigate to the uw_achievement_club folder
`cd fantasy-nba-points-analyser`
###### 3. Install the requirements 
`pip install -r requirements.txt`
###### 4. Run the tool
`python ESPNScraping.py`
