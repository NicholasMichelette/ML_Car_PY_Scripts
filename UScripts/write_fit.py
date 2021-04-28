import argparse
parser = argparse.ArgumentParser(description='Test')
parser.add_argument('fit', type=float, help="Fitness")
args = parser.parse_args()

f = open("J:/Documents/UScripts/UScripts/UScripts/data/qv1.txt", "a+")
f.write(str(args.fit) + "\n")
f.close()