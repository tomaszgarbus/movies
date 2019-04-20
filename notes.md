# Notes and ideas
## 1. Numbers vectors
I'm using GoogleNews pretrained w2v vectors. They do not contain embeddings for numbers, which could contribute to the
context.

As a motivation consider the same value (90) in OMDb json and Wikipedia article:
OMDb Json: `number: 90 context: Ratings Metacritic / 100`
Wiki: `score of 90 out of 100 ( based on 24 reviews')`