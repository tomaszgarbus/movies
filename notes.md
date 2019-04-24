# Notes and ideas
## 1. Numbers vectors
I'm using GoogleNews pretrained w2v vectors. They do not contain embeddings for numbers, which could contribute to the
context.

As a motivation consider the same value (90) in OMDb json and Wikipedia article:

OMDb Json: `number: 90 context: Ratings Metacritic / 100`

Wiki: `score of 90 out of 100 ( based on 24 reviews')`

## 2. Left and right context.
Another thing to implement is distinguishing left-side and right-side context.

## Results
### Google news:
```
Processing movie: Star Wars IV
7/15 fields matched with Wiki
Processing movie: Star Wars V
6/16 fields matched with Wiki
Processing movie: Star Wars VI
7/15 fields matched with Wiki
Processing movie: Star Wars I
6/16 fields matched with Wiki
Processing movie: Star Wars II
8/16 fields matched with Wiki
Processing movie: Star Wars III
8/15 fields matched with Wiki
Processing movie: Forrest Gump
6/16 fields matched with Wiki
Processing movie: Back To The Future
7/17 fields matched with Wiki
Processing movie: David And Lisa
4/12 fields matched with Wiki
Processing movie: Marley And Me
4/16 fields matched with Wiki
Processing movie: 101 Dalmatians
4/16 fields matched with Wiki
Processing movie: Lassie
5/11 fields matched with Wiki
Processing movie: Titanic
6/19 fields matched with Wiki
Processing movie: Shawshank Redemption
5/15 fields matched with Wiki
Processing movie: Se7en
7/15 fields matched with Wiki
Processing movie: True Detective
3/13 fields matched with Wiki
Processing movie: Big Lebowski
3/14 fields matched with Wiki
Processing movie: Death Proof
4/10 fields matched with Wiki
Processing movie: Slumdog Millionaire
9/19 fields matched with Wiki
Processing movie: Lemonade Joe
2/10 fields matched with Wiki
```
### Bert:
```
Processing movie: Star Wars IV
7/15 fields matched with Wiki
Processing movie: Star Wars V
6/16 fields matched with Wiki
Processing movie: Star Wars VI
7/15 fields matched with Wiki
Processing movie: Star Wars I
6/16 fields matched with Wiki
Processing movie: Star Wars II
8/16 fields matched with Wiki
Processing movie: Star Wars III
8/15 fields matched with Wiki
Processing movie: Forrest Gump
6/16 fields matched with Wiki
Processing movie: Back To The Future
7/17 fields matched with Wiki
Processing movie: David And Lisa
4/12 fields matched with Wiki
Processing movie: Marley And Me
4/16 fields matched with Wiki
Processing movie: 101 Dalmatians
4/16 fields matched with Wiki
Processing movie: Lassie
5/11 fields matched with Wiki
Processing movie: Titanic
6/19 fields matched with Wiki
Processing movie: Shawshank Redemption
5/15 fields matched with Wiki
Processing movie: Se7en
7/15 fields matched with Wiki
Processing movie: True Detective
3/13 fields matched with Wiki
Processing movie: Big Lebowski
3/14 fields matched with Wiki
Processing movie: Death Proof
4/10 fields matched with Wiki
Processing movie: Slumdog Millionaire
9/19 fields matched with Wiki
Processing movie: Lemonade Joe
2/10 fields matched with Wiki
```

### Window_size = 5
```
number: 1977 context: Year
Not found

number: 25 context: Released May 1977
3


number: 1977 context: Released 25 May
4

number: 121 context: Runtime min
Not found

number: 6 context: Awards Won Oscars . Another 50 wins & 28 nominations .
Not found

number: 50 context: Awards Won 6 Oscars . Another wins & 28 nominations .
Not found

number: 28 context: Awards Won 6 Oscars . Another 50 wins & nominations .
Not found

number: 93 context: Ratings Rotten Tomatoes %
1

number: 90 context: Ratings Metacritic / 100
Not found

number: 100 context: Ratings Metacritic 90 /
4

number: 90 context: Metascore
9

number: 8.6 context: imdb Rating
Not found

number: 1,109,357 context: imdb Votes
Not found

number: 21 context: DVD Sep 2004
21

number: 2004 context: DVD 21 Sep
2004
```

### Window_size in [1...10]
```
number: 1977 context: Year
Not found

number: 25 context: Released May 1977
3,6

number: 1977 context: Released 25 May
3

number: 121 context: Runtime min
Not found

number: 6 context: Awards Won Oscars . Another 50 wins & 28 nominations .
Not found

number: 50 context: Awards Won 6 Oscars . Another wins & 28 nominations .
Not found

number: 28 context: Awards Won 6 Oscars . Another 50 wins & nominations .
Not found

number: 93 context: Ratings Rotten Tomatoes %
1,2,3,6,7,8,9

number: 90 context: Ratings Metacritic / 100
3,4,5,6,8

number: 100 context: Ratings Metacritic 90 /
5,7

number: 90 context: Metascore
8,10,11,12,13

number: 8.6 context: imdb Rating
Not found

number: 1,109,357 context: imdb Votes
Not found

number: 21 context: DVD Sep 2004
1,7,11

number: 2004 context: DVD 21 Sep
7
```