import datetime
class Game:

	counting_stats = ['reb', 'ast','blk', 'stl', 'pts']

	def convert_date(self, date_str):
		month, day = date_str.split('/')
		year = 2017 if month >= 10 else 2018
		return datetime.date(year, int(month), int(day))

	def __init__(self, stats):
		self.date = self.convert_date(stats[0])
		self.min = int(stats[1])
		self.threes = int(stats[2])
		self.reb = int(stats[3])
		self.ast = int(stats[4])
		self.blk = int(stats[5])
		self.stl = int(stats[6])
		self.to = int(stats[7])
		self.pts = int(stats[8])

	def get_pts(self):
		return self.pts if self.pts is not None else 0

	def get_fpts(self, scoring):
		fpts = 0
		i = 0
		doubles = 0
		for stat, val in self.__dict__.iteritems():
			if stat != 'date':
				fpts += scoring[stat] * val
			if stat in Game.counting_stats:
				if val >= 10:
					doubles += 1
			i += 1

		if doubles >= 2:
			fpts += scoring['dd']

		if doubles >= 3:
			fpts += scoring['td']

		return fpts

	def get_stats(self):
		return self.__dict__.values()

	def print_with_fpts(self, scoring):
		return str(self) + ' || ' + '{:>3}'.format(str(self.get_fpts(scoring)))

	def __str__(self):
		output = "DATE: {:>10} | MIN: {self.min:>2} | 3PM: {self.threes:>2} | REB: {self.reb:>2} | AST: {self.ast:>2} | BLK: {self.blk:>2} | STL: {self.stl:>2} | TO: {self.to:>2} | PTS: {self.pts:>2}".format(str(self.date), self=self)
		return output