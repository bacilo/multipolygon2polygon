import argparse
import sys
import csv

def get_id_col(header, idcol):
	"""
	Finds the number for the column in the CSV file that contains the ID value to be used in the target file as well 

	Parameters:
	-----------
	header:
		The array corresponding to the first line of the CSV file (containing the column names)

	idcol:
		The specified id column name (or a default empty string if one is not specified)

	Returns:
	--------
	The number corresponding to the id column (0 by default if one is not specified)
	
	Exceptions:
	-----------
	Throws ValueError exception if the specified id column cannot be found
	"""

	if idcol == '':
		return 0

	return header.index(idcol)

def get_multipolygon_col(header, idcol):
	"""
	Finds the number for the column in the CSV file that contains the Multipolygon value to be used in the target file as well 

	Parameters:
	-----------
	header:
		The array corresponding to the first line of the CSV file (containing the column names)

	idcol:
		The specified multipolygon column name (or a default empty string if one is not specified)

	Returns:
	--------
	The number corresponding to the multipolygon column
		- Right now returns 100 if nothing is specified as it fits with the specific example I built this for
		@TODO : Autodetect Multipolygon field
	
	Exceptions:
	-----------
	Throws ValueError exception if the specified multipolygon column cannot be found
	"""

	if idcol == '':
		return 100

	return header.index(idcol)

def main():

	__author__ = 'bacilo'
	 
	parser = argparse.ArgumentParser(description='Takes a CSV file containing one or many Multipolygon field(s) and creates an auxiliary CSV file where those Multipolygons are stored as rows of points, with a PolygonID field to identify the points belonging to each Polygon')
	parser.add_argument('source_file', help='Source file name')
	parser.add_argument('output_file', help='Target file name')
	parser.add_argument('-b','--begin', help='Row to start parsing Source file from',required=False, type=int, default=0)
	parser.add_argument('-e','--end',help='Row to stop parsint the Source file at', required=False, type=int, default=0)
	parser.add_argument('-i','--idcol', help='Column that contains ID to be perserved in the output_file',required=False, default='')
	parser.add_argument('-m','--multipolcol',help='Column that contains Multipolygon field', required=False, default='')
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
			    header = reader.next()
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
			    	temp = line[get_multipolygon_col(header, args.multipolcol)][16:-3]
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
			    			f.write(line[get_id_col(header, args.idcol)] + ", " + str(polygonId) + ", " + str(pointId) + ", " + lng + ", " + lat + "\n")

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


