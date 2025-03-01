import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import tools
import splitters
import representations
import re
import sys

# Read command-line arguments
K = int(sys.argv[1])
infile = sys.argv[2]

# Read the input file
with open(infile, "r", encoding="utf-8") as f:
    txt = f.read()

# Define regular expressions
punctuation_pat = re.compile(r"""([!"#$%&\'()*+,-./:;<=>?@[\\\]^_`{|}~])""")
hyphenline_pat = re.compile(r"-\s*\n\s*")
multiwhite_pat = re.compile(r"\s+")
cid_pat = re.compile(r"\(cid:\d+\)")
nonlet = re.compile(r"([^A-Za-z0-9 ])")

# Function to clean text
def clean_text(txt):
    txt = txt.lower()
    txt = cid_pat.sub(" UNK ", txt)
    txt = hyphenline_pat.sub("", txt)
    txt = punctuation_pat.sub(r" \1 ", txt)
    txt = re.sub("\n", " NL ", txt)
    txt = nonlet.sub(r" \1 ", txt)
    txt = multiwhite_pat.sub(" ", txt)
    return " ".join(["START", txt.strip(), "END"])

# Clean and split the text
txt = clean_text(txt).split()

# Load word vectors and vocab
#vecs = np.load("/home/aaa244/storage/arxiv_glove/bigrun/data/mats/vecs.npy")
#words = np.load("/home/aaa244/storage/arxiv_glove/bigrun/data/mats/vocab.npy")

# use our own stuff
#words = np.genfromtxt("text8.txt")
#vecs = np.loadtxt("glove.42B.300d.txt")

#word_lookup = {w: c for c, w in enumerate(words)}

word_lookup = {}
with open("glove.42B.300d.txt", "r", encoding="utf-8") as file:
    for line in file:
        # Split the line into parts
        parts = line.split()
        
        # The first part is the string (key)
        key = parts[0]
        
        # The remaining parts are the floats (values)
        values = list(map(float, parts[1:]))
        
        # Add the key-value pair to the dictionary
        word_lookup[key] = values
"""
# This prints some of the word embeddings
for i, (key, value) in enumerate(word_lookup.items()):
    if i == 5:
        break
    print(f"{key}: {value}")
"""

print("article length:", len(txt))

# Create the list of vectors (X) and the mapper for word indices
X = []
mapper = {}
count = 0
for i, word in enumerate(txt):
    if word in word_lookup:
        mapper[i] = count
        count += 1
        X.append(word_lookup[word])

# Reverse the mapping of indices
mapperr = {v: k for k, v in mapper.items()}

# Convert X into a numpy array
X = np.array(X)
print("X length:", X.shape[0])

# Generate the sigma function for segmentation
sig = splitters.gensig_model(X)

# Perform the greedy split
print("Splitting...")
splits, e = splitters.greedysplit(X.shape[0], K, sig)
print(splits)

# Refine the splits
print("Refining...")
splitsr = splitters.refine(splits, sig, 20)
print(splitsr)

# Print the refined splits
print("Printing refined splits...")
for i, s in enumerate(splitsr[:-1]):
    k = mapperr[s]
    print(f"\n{i} {s}")
    print(" ".join(txt[k - 100:k]), "\n\n", " ".join(txt[k:k + 100]))

# Write the result to a file
with open(f"result{K}.txt", "w", encoding="utf-8") as f:
    prev = 0
    for s in splitsr:
        k = mapperr.get(s, len(txt))
        f.write(" ".join(txt[prev:k]).replace("NL", "\n"))
        f.write("\nBREAK\n")
        prev = k

print("Done")