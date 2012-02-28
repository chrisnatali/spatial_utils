import argparse
import sys
import nn_qt
import csv

# helper function
def csv_to_pts(csv_file):
    csv_reader = csv.reader(csv_file)
    pts = [] 
    for row in csv_reader:
        pts.append([float(row[0]), float(row[1])])

    return pts

parser = argparse.ArgumentParser(description='Create nearest neighbor associations between points')

parser.add_argument('--pop-pts', '-p', metavar='name', type=argparse.FileType('r'), help='pop pt csv file')

parser.add_argument('--fac-pts', '-f', metavar='name', type=argparse.FileType('r'), help='fac pt csv file')

args = parser.parse_args()

# convert csv's to points
pop_pts = csv_to_pts(args.pop_pts)
fac_pts = csv_to_pts(args.fac_pts)

edges = nn_qt.generate_nearest_neighbor(pop_pts, fac_pts)

# print out edges
for edge in edges:
    print "%d,%d,%f" % (edge[0], edge[1], edge[2])


