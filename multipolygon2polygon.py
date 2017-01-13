from __future__ import print_function

import sys
import csv

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if len(sys.argv) == 3:
	# Maybe opening/integrity tests could be done beforehand
	sourcefile = sys.argv[1]
	targetfile = sys.argv[2]
else:
	exit("usage: multipolygon2polygon source target")

 
# Write mode creates a new file or overwrites the existing content of the file. 
# Write mode will _always_ destroy the existing contents of a file.
try:
    # This will create a new file or **overwrite an existing file**.
    f = open(targetfile, "w")

    ## In the future open file in this way for flexibility, for instance with quoting styles
	## ofile = open('polygons.csv', 'wb')
	## writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

	# Read mode
    try:

        with open(sourcefile, 'rb') as csvfile:

        	# Use semicolon as delimiter (problem with Excel parsing... some flexibility could be added here)
		    dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=';,')
		    csvfile.seek(0)
		    reader = csv.reader(csvfile, dialect)

		    # Remove header... add flexibility here, ask user to select which fields to keep?
		    reader.next()[0]

		    # Write header (also might need to support sub-polygons though that seems too much for now)
		    f.write("FID, polygonID, pointID, longitude, latitude\n")

		    # Start count of polygons
		    polygonId = 1

		    # Go row by row
		    for line in reader:

		    	# Pick colum that has MULTIPOLYGON field (here 100, but best detect automatically in the future)
		    	# Substring removes the initial declaration of MULTIPOLYGON and the opening and closing parenthesis
		    	# Splits the polygon stucture into its different points
		    	temp = line[100][16:-3]
		    	coords = temp.split(',')

		    	# Start pointID count for this particular line
		    	pointId=1

		    	# The check here is also not great... right now just detecting it's not totally empty but bestter check would be desireable
		    	if len(coords) > 1:

		    		# Iterate through the different coordinate points
			    	for _element in coords:

		    			# Split latitude and longitude
		    			coord = _element.strip().split(" ")
		    			lng = coord[0]
		    			lat = coord[1]

		    			# Add the row to the CSV file
		    			f.write(line[0] + ", " + str(polygonId) + ", " + str(pointId) + ", " + lng + ", " + lat + "\n")

		    			# move on to the next point in the polygon
		    			pointId=pointId+1

		    		# iterate the next polygon
		    		polygonId=polygonId+1
		    csvfile.close
    finally:
        f.close()
except IOError:
    pass
