# multipolygon2polygon
Short python script that creates a csv file with Polygons described in the format of one row per point, from a CSV file containing a field for Multipolygon, where a whole Polygon is described in one Multipolygon field

## Usage

python multipolygon2polygon source_file output_file [-b --begin BEGIN] [-e --end END]

The script takes column 100 of the CSV 'source_file', which contains the Multipolygon field, and breaks it down into a Rows of points that describe the polygons and replicates the ID (first column of the 'source_file') of which those rows pertain to (for later merging when visualizing the data for instance).

Possiblility to limit the first and last rows of the source_file to be parsed by setting the limits using the -b and -e optional flags in the command line.

## Header row of 'output_file'

FID, PolygonID, PointID, longitude, latitude

FID - From the original file, replicated so that in later usage it can be merged with the source file
Polygon ID - So that we know which rows pertain to which polygon
Point ID - Orders the polygon
longitude, latitude - Coordinates for that specific point

## Warning and Future Updates

This was developed quickly to solve a specific problem. I may spend more time on improvements (for instance detecting which column has the Multipolygon field, or allowing the user to specify which columns should be 
