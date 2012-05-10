import csv
import psycopg2.extras
import shapely.wkb

class ShapelyLoader(object):

    def __init__(self, connection, query_string, geom_column):
        self.connection = connection
        self.query = query_string
        self.geom_column = geom_column

    def fetchall(self):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(self.query)
        result = cursor.fetchall()
        geoms = []
        for row in result:
            geom_wkb = row[self.geom_column]
            geoms.append(shapely.wkb.loads(geom_wkb.decode('hex')))

        cursor.close()
        return geoms

class PGImport(object):

    def __init__(self, connection, table_name, columns):
        self.connection = connection
        self.table_name = table_name
        self.columns = columns

    def do_import(self, io_stream):
        cursor = self.connection.cursor()
        cursor.copy_from(io_stream, self.table_name, sep=',', columns=self.columns)
        cursor.close()


class CSVToCSV_WKT_Point(object):

    def __init__(self, point_columns, new_columns={}):
        """ initialise with point_columns, which represents the column
        number of the x, y coordinates within the input csv (x is
        index 0, y is index 1).
        new_columns is a hash of column_number -> repeated_value to
        be added for each row."""
        self.point_columns = point_columns
        self.new_columns = new_columns

    def translate(self, in_file_stream, out_file_stream, srid):
        """ Translates csv with lat,lon as separate columns into a csv
        with lat,lon as a single WKT POINT column.  
        writes to an IO stream the csv as lines to be stored."""
        # csv_file should be open in read 'Universal' mode
        csv_reader = csv.reader(in_file_stream)
        for row in csv_reader:
            if (len(row) == 0):
                continue

            point = 'SRID=%s;POINT(%s %s)' % (srid, row[self.point_columns[0]],
                    row[self.point_columns[1]])
 
            for key in self.new_columns:
                if(self.new_columns[key].has_key('value')):
                    out_file_stream.write(self.new_columns[key]['value'])
                else:
                    out_file_stream.write(row[self.new_columns[key]['column']])
                out_file_stream.write(',')
                 
            out_file_stream.write('%s\n' % point)
        
