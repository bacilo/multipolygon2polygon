import argparse
import sys
import csv


def main():

	__author__ = 'bacilo'
	 
	parser = argparse.ArgumentParser(description='Takes a CSV file containing one or many Multipolygon field(s) and creates an auxiliary CSV file where those Multipolygons are stored as rows of points, with a PolygonID field to identify the points belonging to each Polygon')
	parser.add_argument('source_file', help='Source file name')
	parser.add_argument('output_file', help='Target file name')
	parser.add_argument('-b','--begin', help='Row to start parsing Source file from',required=False, type=int, default=0)
	parser.add_argument('-e','--end',help='Row to stop parsint the Source file at', required=False, type=int, default=0)
	args = parser.parse_args()
	 
	outputfile = args.output_file
	sourcefile = args.source_file
	l_begin = args.begin
	l_end = args.end

	# Write mode creates a new file or overwrites the existing content of the file. 
	# Write mode will _always_ destroy the existing contents of a file.
	try:
	    # This will create a new file or **overwrite an existing file**.
	    f = open(outputfile, "w")

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

			    data_list = list(reader)
				
				 
				#Validates and sets the right limits for which row to start from and which row to end at 
				#if limits are not within the limits of the dataset or the start row is after the end row
				#then prints 'error'. If no limits were specified then they will be set to start
				#and end at the beginning and ending

				#@TODO: Exception should be thrown instead of printing 'error'
				
			    if l_end == 0:
			    	l_end = len(data_list)
			    if l_end < l_begin:
			    	print 'error'
			    if l_begin > len(data_list) or l_end > len(data_list):
			    	print 'error'

			    # Write header (also might need to support sub-polygons though that seems too much for now)
			    f.write("FID, polygonID, pointID, longitude, latitude\n")

			    # Start count of polygons
			    polygonId = 1

			    # Go row by row
			    for line in data_list[l_begin:l_end]:

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

	except IOError as err:
	    print("IO error: {0}".format(err))
	except:
	    print("Unexpected error:", sys.exc_info()[0])
	    raise

if __name__ == "__main__":
	main()


