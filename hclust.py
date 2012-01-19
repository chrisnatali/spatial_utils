import argparse
import sys
import util
import cluster_r
import csv

parser = argparse.ArgumentParser(description='Create hierarchical clusters for a point list')

parser.add_argument('--input', '-i', metavar='name', type=argparse.FileType('r'), default=sys.stdin, help='input csv file of points')

parser.add_argument('--output', '-o', metavar='name', type=argparse.FileType('w'), default=sys.stdout, help='output file')

parser.add_argument('--method', '-m', metavar='name', default='single', help='hclust method to be used.  See hclust R doc.')

parser.add_argument('--distance', '-d', metavar='value', type=int, help='length (in meters) of radius to slice clusters')

parser.add_argument('--centroids', '-e', action='store_true', default=False, help='output centroids')

parser.add_argument('--stats', '-s', action='store_true', default=False, help='output stats')

parser.add_argument('--clusters', '-c', action='store_true', default=False, help='output points')

args = parser.parse_args()

# convert csv to array of float tuples
rows = csv.reader(args.input)
pts = map(lambda row: (float(row[0]), float(row[1])), rows)

if(len(pts) < 1):
    sys.stderr.write("No input points found")
    exit()

# convert meters to kilometers since hclust assumes km
km = args.distance / 1000.0

clusters = cluster_r.hclust(pts, km, args.method)
clusters.sort(key=len, reverse=True)
centroids = []
for cluster in clusters:
    unzipped = zip(*cluster)
    centroids.append(util.points_to_centroid(unzipped))

if args.clusters:
    print('clusters')
    for cluster in clusters:
        print cluster

if args.centroids:
    print('centroids')
    for centroid in centroids:
        print centroid

if args.stats:
    print('stats')
    for i in range(0, len(clusters)):
        cluster = clusters[i]
        centroid = centroids[i]
        dists = util.dists_to_pt(cluster, centroid)
        avg_dist = sum(dists) / len(dists)
        print avg_dist
    
