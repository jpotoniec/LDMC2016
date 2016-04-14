# Introduction

In order to support our claims about DBpedia being an insufficient or even misleading source for solving the challenge task, we conduced a set of experiments using various sets of features.
The rest of the ML process was kept exactly the same as described in the paper: 10-fold cross-validation with normalization, replacing missing values and logistic regression.

# LOD Features 

For each of the URIs from the challenge dataset, we retrieved from DBpedia all triples having the URI as a subject. 
Below, we refeer to these triples as *level1* triples.
From these triples, a new set of URIs was build, that contains URIs occuring in an object position for any of these triples.
For all of these URIs, we also retrieved from DBpedia all triples having the URI as a subject.
Below, we call them *level2* triples.

To simplify our workflow, we decided to build a joined set of triples, joining both *level1* and *level2* sets in a specific way.
The joined set contains all triples from *level1* and for any triple `(s, p1, o)` in *level1* and any triple `(o, p2, u)` in *level2*, a triple `(s, p1/p2, u)` is added to the final set.
The idea here is to mimick SPARQL property paths, that is to provide a direct link between `s` and `u`.
Note that in the final set, triple subjects are always URIs from the challenge dataset.
Please note, the final set contains also triples with predicate `dbp:mc`, which correspond to a [Metacritic](metacritic.com) review score, so strictly speaking the set is *not* in line with the challenge rules.

First, we considered all predicated `p` such that a triple `(s,p,o)` occurs in the final set for any `s` and `o`.
Let `S` be a set al URIs, such that they occur in some triple `(s,p,o)` from the final set for any `o`.
If size of `S` was at least 80 (that is 5% of the number of URIs from the challenge dataset), but no more than 1513 (95%), a binary feature `p` was created.
The feature value was set to 1 for every URI in the set S and 0 for the rest.

Further, we considered all pairs `p,o` such that `(s,p,o)` occur in the final set for any `s` and `o` is either an URI or a literal with a lexical representation shorter than 30 characters.
Let `S` be a set consisting of all such `s`.
With the set `S` defined as such, we proceed as described above with constructing a binary feature `p=o`.

Finally, we considered all pairs `p,l` such that `(s,p,l)` occur in the final set for any `s` and `l` is a numeric literal.
Let `S` be a set of all URIs, such that there is a triple `(s,p,m)` in the final set, `m` is a numeric literal and `m<=l`.
With the set `S` defined as such, we proceed as described above with constructing a binary feature `p<=l`.

This way we obtained a tremendous number of 13175 binary features.
The corresponding dataset is available in [result.csv.gz](result.csv.gz)
**The file must be decompressed before it can be used in RapidMiner**


# Experiment 1

We combined an original workflow described in the paper with the dataset described above. Its execution took 25m27s and the cross-validation result was reported to be 86.74%±2.09%, which is lower than 91.7%±2.17\% repoted in the paper.
Furthermore, analysis of the weights assigned by logistic regression to the features revealed that the algorithm still relied heavily on the scraped features from the paper.
The highest weight 1.177 was again assigned to [Pitchfork](pitchfork.com) review score.

The first LOD feature is on 11th position in ordering by absolute value of weight, with the weight being -0.33. It is a feature from the first category `rdfs:label`, that is a feature concerned only about presence or absence of a triple with `rdfs:label` as a predicate.

Below, with weights -0.299 and -0.273 respectively are two more complex features: `dbp:artist/dbp:genre=dbr:Indie_rock` and `dbp:artist/dbo:genre=dbr:Indie_rock`.
Apparently, being labeled as an indie rock artist may be slightly against you.
On the other hand, for an album to be labeled as indie rock is good: `dbp:label/dcterms:subject=dbr:Category:Indie_rock_record_labels` was assigned a possitive weight of 0.22.

Unsurprisingly, some features with `dbp:mc` property ([Metacritic](metacritic.com) review score) are assigned a non-zero weight: `dbp:mc<=62` was assigned a weight -0.179, `dbp:mc<=63` up to `dbp:mc<=66` were assigned a weight -0.177 and `dbp:mc<=67` up to `dbp:mc<=75` were assigned a weight -0.161.
Further, `dbp:mc<=76` up to `dbp:mc<=78` were assigned a weight -0.157.
This is consistent with the challenge setup: in the training dataset labels *good* start with the Metacritic score 79 and above and *bad* with the score *63* and below.

The weights for all attributes are available in file [experiment1/model.csv](experiment1/model.csv)


# Experiment 2

In this experiment, we used only the final dataset described above.
The machine learning workflow (normalization, missing value replacement, logistic regression) was kept the same.

The cross-validation accuracy was 76.02%±1.98%.
The highest absolute value of weight was only 0.392 and was assigned to the attribute mentioned above: `dbp:label/dcterms:subject=dbr:Category:Indie_rock_record_labels`.
Next attribute in the absolute value order was `rdfs:label` with a weight -0.384.

The weights for all attributes are available in file [experiment2/model.csv](experiment2/model.csv)


