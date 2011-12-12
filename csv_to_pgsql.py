import argparse
import sys
import pg_import

parser = argparse.ArgumentParser(description='Convert csv to format suitable for postgis import')

parser.add_argument('--point-columns', '-p', metavar=('latitude_index', 'longitude_index'),
type=int, nargs=2, default=(0, 1), help='Column indexes to be used as latitude and longitude')
 
parser.add_argument('--input', '-i', metavar='name', type=argparse.FileType('r'), default=sys.stdin, help='input csv file')

parser.add_argument('--output', '-o', metavar='name', type=argparse.FileType('w'), default=sys.stdout, help='output csv file')

args = parser.parse_args()

csv_to_csvwkt = pg_import.CSVToCSV_WKT_Point(args.point_columns)
csv_to_csvwkt.translate(args.input, args.output)

