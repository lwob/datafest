import datetime,csv
 
input_string = "distance_band" # set this value yourself
data = [] #let this represent each of the lines or some stream object that i can iterate through
MAX_DATE = 2048
def parse_date(string):
	if string == "NULL": return string
	year, month, day = map(int, string.split("-"))
	return datetime.date(year, month, day)
 
dates_length = [[0 for i in xrange(MAX_DATE)] for j in xrange(MAX_DATE+1)] #find the total of the ratings
dates_users =[[0 for i in xrange(MAX_DATE)] for j in xrange(MAX_DATE+1)] # find the total number of entries at each date to take the avg
 
#prop_starrating
rating_map = {	"prop_starrating": {name: i for i, name in list(enumerate(map(str, xrange(0, 6)))) + 
											list(enumerate(map(lambda x: str(float(x)), xrange(0,6))))},
				"popularity_band": {name: i for i, name in enumerate(["VL", "L", "M", "H", "VH"])}, # popularity_band
				"hist_price_band": {name: i for i, name in enumerate(["VL", "L", "M", "H", "VH"])}, # hist_price_band
				"distance_band": {name: i for i, name in enumerate(["VC", "C", "M", "F", "VF"])} # distance_band
				}
mapping = {} # represents the string and the data
beginning_of_time = parse_date("2014-01-01")
 
with open('../data/data.txt', 'rb') as inp: #open the file
	first_line = inp.readline().strip("\r\n")
	for i, name in enumerate(first_line.split("	")):
		mapping[name] = i
	data = csv.reader(inp, delimiter="	", quotechar="|")
	for line in data:
		# Error checking for NULL
		try:
			start_date = parse_date(line[mapping["srch_ci"]])
			end_date = parse_date(line[mapping["srch_co"]])
		except ValueError:
			print line[mapping["srch_ci"]], line[mapping["srch_co"]]
			continue
		if start_date == "NULL" or end_date == "NULL":
			continue
 
		
		rat = line[mapping[input_string]]
		# Error checking for NULL
		if rat == "NULL" or rat == "0" or rat == "0.0":
			continue
		else:
			rat = rating_map[input_string][line[mapping[input_string]]]
 
		arr_start = (start_date-beginning_of_time).days
		length = (end_date-start_date).days
		# Error checking
		if 0 <= arr_start < MAX_DATE and length >= 0:
			try:
				dates_length[arr_start][length] += rat
				dates_users[arr_start][length] += 1
			except IndexError:
				print arr_start, length
				continue
		else:
			continue
		
 
 
dates_avg_rating = [0 for i in xrange(MAX_DATE)]
dates_total_users = [0 for i in xrange(MAX_DATE)]
for i in xrange(MAX_DATE):
	# this section calculates the total for the ratings
	dates_avg_rating[i] += dates_length[i][0]
	for j in xrange(1, MAX_DATE): 
		dates_avg_rating[i] += dates_length[i][j]
		dates_length[i+1][j-1] += dates_length[i][j]
 
	# this section calculates the total users for the each date
	dates_total_users[i] += dates_users[i][0]
	for j in xrange(1, MAX_DATE):
		dates_total_users[i] += dates_users[i][j]
		dates_users[i+1][j-1] += dates_users[i][j]
 
with open("../data/staying_dates_vs_%s.csv"%input_string, 'w') as output:
	output.write("date,total_users,average_rating\n")
	for i in xrange(MAX_DATE):
		dtu = dates_total_users[i]
		dar = dates_avg_rating[i]
		output.write("%s,%d,%.03f\n"%(str(beginning_of_time), dtu, float(dar)/dtu if dtu != 0 else 0))
		beginning_of_time += datetime.timedelta(1)
