# LDMC2016
A solution for Linked Data Mining Challenge 2016

# Data format

The data used for mining are available as Turtle file `data.ttl`.
A property `:has_metric` connects album to its metrics.
Every metric is represented as a blank node with a textual `:name` and numeric `:value`.

An example below states that album http://dbpedia.org/resource/The_Tight_Connection has 9 reviews on Amazon with an average review score 4.1. Prefix `:` corresponds to the namespace `https://github.com/jpotoniec/LDMC2016#`
```<http://dbpedia.org/resource/The_Tight_Connection> :has_metric [ :name "amazon_nusers"; :value "9"^^xsd:double ], [ :name "amazon_rating"; :value "4.1"^^xsd:double ].```

For convenience, the same data are available as CSV files.
The mining workflow in directory `RapidMiner` uses the CSV files.
