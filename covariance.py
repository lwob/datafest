import gmplot
 
long_lst, lat_lst, mapping = [],[], {"user_location_latitude":0, "user_location_longitude":1}
with open("../data/locations.txt", 'r') as inp:
	cnt = 0
	for line in inp:
		if line == "NULL,NULL\n": continue
		line.strip("\n")
		lat, lng = line.split(",")
		lat_lst.append(float(lat))
		long_lst.append(float(lng))
 
		cnt += 1
		if cnt == 100000: break
		
gmap = gmplot.GoogleMapPlotter(0, 0, 2)
 
gmap.heatmap(lat_lst, long_lst)
gmap.draw("user_location_heatmap.html")