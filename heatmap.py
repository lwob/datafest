mapping = {}
 
loc_file = open("../data/locations.txt", "w")
with open("../data/data.txt", 'r') as inp:
	first_line = inp.readline()
	for i, name in enumerate(first_line.split("	")):
		mapping[name] = i
	for line in inp:
		cur = line.split("	")
		#long_lst.append()
		#lat_lst.append(
		loc_file.write(cur[mapping["user_location_latitude"]] + "," + cur[mapping["user_location_longitude"]] + "\n")
loc_file.close()
