# Movies (NumberContext structure)
In this repository I have conducted some simple experiments with embedding numerical values found in documents. The only
purpose (for now) of the experiments is to help me find a direction for my MSc thesis.

The experiments revolve around a simple idea of fetching the description of the same movie from 2 different sources
(OMDb and Wikipedia), vectorizing the context around every numerical value and measuring how close are the same values
from different sources.

## Datasets
No data needs to be downloaded to run the experiments. I have experimented with
[DBPedia infoboxes dataset](http://downloads.dbpedia.org/2016-10/core-i18n/en/infobox_properties_mapped_en.tql.bz2)
a bit, but found that fetching raw Wikipedia articles over HTTP (and caching them) was much more convenient.

The code in `experiments.py` uses two sources of data: `omdbapi.com` and the Wikipedia API.

The list of movies on which the experiments are ran is in `movies_to_download.csv`.

## Context vectorization
For each document (omdb json or Wikipedia article) a list of NumberContexts is constructed, where NumberContext is a
triplet:

* numerical value
* vectorized context
* raw context (for human interpretation) 

### (number, context) pairs contruction
#### OMDb
`omdbapi.com` is a REST API that returns Json responses. I use several rules for transforming a Json response into a
(number, context) pair:

* First, I use some knowledge of the response structure and slightly reorder fields so that more information is capture
in next steps (e.g. the source of rating is captured in the context of the rating value).
* If the value of a field is a number or a string that can be interpreted as a number, the corresponding key is the
context.
* If the value is nested, all parent keys are concatenated into a context.
* If the value of a field is a string, but after tokenization some tokens are found to be numeric, those tokens are
extracted with context: concatenated all parent keys + all other tokens in this string.

#### Wikipedia articles
Wikipedia articles are first cut before the "Citations" section, then tokenized. All tokens that are found to be numeric
are listed together with the context, where the context is concatenation of `2 * window_size` neighboring tokens. In
experiments, `window_size` (radius would be more accurate name) varies from 1 to 10.

#### Used word embeddings
I have used word2vec embeddings pretrained on Google News dataset and BERT embeddings from [Zalando Flair](
https://github.com/zalandoresearch/flair
) package.

To vectorize a list of words, I computed the mean of individual word vectors, which is a baseline solution to improve
upon.

## Experiment results
### Finding closest contexts.
First, I would turn the OMDb jsons into NumberContexts lists and for each field, find the closest (by cosine similarity)
context in corresponding Wikipedia article. Below are examples how this worked out on two movies: Star Wars: A New Hope
and Lemonade Joe.

#### Star Wars: A New Hope
Here, most values from the json, which occur in the Wikipedia article, have been found within the 15 closest contexts.
In each block, the first (number, context) pair originates from OMDb json, the list below it are top 15 Wikipedia pairs,
where the first value in the triplet is cosine similarity of contexts, the second is the number token and the third is
raw context.
```
number: 1977 context: Year
(0.6274531, '15', 'Registry years')
(0.6266401, '120', 'year ; [ ] in 1978')
(0.57944757, '100', 'Years ... Movie Quotes')
(0.5685197, '1978', 'year , and in added the worldwide record')
(0.56802386, '100', 'Years ... Movies (')
(0.5629744, '100', 'on Years')
(0.5614178, '100', '39th on Years ...')
(0.5604906, '2', 'Country United States [ ] Language English Budget $')
(0.55787086, '100', '] 15th on Years ... 100')
(0.5576993, '100', 'greatest heroes respectively on Years ... 100 Heroes')
(0.55461365, '100', '] 27th on Years ... 100')
(0.5537538, '100', '238 ] AFI Years ... series')
(0.5534656, '100', 'and 39th on Years ... 100')
(0.553272, '100', '27th on Years ...')
(0.5524283, '100', 'Years ... Movies [')

number: 25 context: Released May 1977
(0.76810896, '25', 'Fox Release date May , 1977 (')
(0.73251915, '10', 're-release of April , 1981 ,')
(0.71620786, '25', 'date May , 1977')
(0.7033177, '25', 'Distributed by20th Century Fox Release date May , 1977 ( 1977-05-25 ) (')
(0.699353, '25', 'Century Fox Release date May , 1977 ( 1977-05-25')
(0.687095, '1977', 'Fox Release date May 25 , ( 1977-05-25 ) ( United')
(0.68492067, '25', 'Lucasfilm Distributed by20th Century Fox Release date May , 1977 ( 1977-05-25 ) ( United')
(0.68199927, '25', 'on May , 1977')
(0.67965686, '25', 'by20th Century Fox Release date May , 1977 ( 1977-05-25 )')
(0.67815286, '25', ', May , 1977')
(0.67572176, '27', 'UK on December , 1977 .')
(0.6729232, '1978', 're-released theatrically in , 1979 ,')
(0.65871996, '10', 'theatrical re-release of April , 1981 , [')
(0.6561564, '25', 'Chew Productioncompany Lucasfilm Distributed by20th Century Fox Release date May , 1977 ( 1977-05-25 ) ( United States )')
(0.65476394, '25', 'Productioncompany Lucasfilm Distributed by20th Century Fox Release date May , 1977 ( 1977-05-25 ) ( United States')

number: 1977 context: Released 25 May
(0.6449002, '25', 'release date to May , the Wednesday before')
(0.6210397, '1973', 'June completed')
(0.6196894, '1977', 'Fox Release date May 25 , ( 1977-05-25 ) ( United')
(0.6104732, '1978', 're-release in July . ( Hearn')
(0.60683775, '10', 'download on April , 2015 and')
(0.599302, '25', 'the release date to May , the Wednesday before Memorial')
(0.59742206, '2015', 'download on April 10 , and Walt Disney Studios Home')
(0.5970848, '12', 'DVD sets from September to December 31 ,')
(0.5958368, '25', 'Fox Release date May , 1977 (')
(0.5956067, '1977', 'In March , Williams')
(0.59194154, '7', 'On April , 2015')
(0.59194154, '10', 'on April , 2015')
(0.59166825, '1977', 'sold in April . Roy Thomas')
(0.589049, '1978', 'February and June . [ 6')
(0.5885813, '1977', 'in March to shoot')

number: 121 context: Runtime min
(0.66387594, '0', '{ min-width:100 % ; margin:0 0.8em ! important ; float')
(0.6427549, '0', '.mw-parser-output .quotebox { min-width:100 % ; margin:0 0.8em ! important ; float : none')
(0.64268625, '0', '.quotebox { min-width:100 % ; margin:0 0.8em ! important ; float :')
(0.6300921, '0', 'min-width:100 % ; margin:0 0.8em ! important ;')
(0.6247136, '0', 'overflow : hidden ; margin:1em ; padding:0 40px } .mw-parser-output')
(0.6228326, '0', '{ .mw-parser-output .quotebox { min-width:100 % ; margin:0 0.8em ! important ; float : none !')
(0.61824405, '0', ': hidden ; margin:1em ; padding:0 40px }')
(0.6155083, '150,000', 'Lucas $ to write')
(0.6139095, '121', 'time minutes')
(0.6084998, '0', '.quotebox.floatright { margin:0.5em 0.8em 1.4em }')
(0.6057391, '0', '{ overflow : hidden ; margin:1em ; padding:0 40px } .mw-parser-output .templatequote')
(0.6038708, '2,000', 'approximately film')
(0.60197204, '0', 'max-width:360px ) { .mw-parser-output .quotebox { min-width:100 % ; margin:0 0.8em ! important ; float : none ! important }')
(0.60092425, '121', 'Running time minutes [')
(0.596331, '0', 'margin:0.5em 1.4em 0.8em } .mw-parser-output .quotebox.floatright')

number: 6 context: Awards Won Oscars . Another 50 wins & 28 nominations .
(0.7326859, '1973', 'Accolades [ edit ] Alec Guinness , shown here in , received multiple award nominations , including one from the')
(0.73126614, '2011', 'Greatest Films poll ; [ 249 ] in , it ranked as Best Sci-Fi Film on')
(0.72959256, '197', "won in the latter two categories . [ ] John Williams 's soundtrack album won the")
(0.7284895, '2011', '100 Greatest Films poll ; [ 249 ] in , it ranked as Best Sci-Fi Film on Best')
(0.7277514, '195', 'engineering of the Electronic Motion Control System ) . [ ] Additional nominations included Alec Guinness for Best Actor in')
(0.7267525, '1973', 'edit ] Alec Guinness , shown here in , received multiple award nominations , including one')
(0.725064, '196', 'Best Score . [ ] It received six')
(0.72482234, '195', 'Motion Control System ) . [ ] Additional nominations included Alec Guinness')
(0.72365606, '197', "film won in the latter two categories . [ ] John Williams 's soundtrack album won the Grammy")
(0.72314286, '1973', '[ edit ] Alec Guinness , shown here in , received multiple award nominations , including one from')
(0.72131646, '100', 'Films , [ 245 ] 15th on Years ... 100 Movies [ 239 ]')
(0.72068584, '1', 'two anthology films . Contents Plot 2 Cast 3 Production')
(0.7179215, '100', "– # 1 [ 84 ] AFI 's Years ... 100 Cheers ( 2006 ) –")
(0.71756876, '1973', 'Alec Guinness , shown here in , received multiple award nominations ,')
(0.7156452, '2011', 'Films poll ; [ 249 ] in , it ranked as Best Sci-Fi Film')

number: 50 context: Awards Won 6 Oscars . Another wins & 28 nominations .
(0.7545522, '2011', '100 Greatest Films poll ; [ 249 ] in , it ranked as Best Sci-Fi Film on Best')
(0.7537559, '2011', 'Greatest Films poll ; [ 249 ] in , it ranked as Best Sci-Fi Film on')
(0.7470195, '196', 'Best Score . [ ] It received six')
(0.744158, '1973', 'Accolades [ edit ] Alec Guinness , shown here in , received multiple award nominations , including one from the')
(0.74242765, '1', 'two anthology films . Contents Plot 2 Cast 3 Production')
(0.7385813, '1973', 'edit ] Alec Guinness , shown here in , received multiple award nominations , including one')
(0.73734236, '195', 'Control System ) . [ ] Additional nominations included Alec')
(0.7368036, '1', 'anthology films . Contents Plot 2 Cast 3')
(0.7363152, '197', "won in the latter two categories . [ ] John Williams 's soundtrack album won the")
(0.73474646, '2011', 'Films poll ; [ 249 ] in , it ranked as Best Sci-Fi Film')
(0.73208636, '195', 'Motion Control System ) . [ ] Additional nominations included Alec Guinness')
(0.73182976, '100', '37th greatest heroes respectively on Years ... 100 Heroes &')
(0.7313395, '100', 'Films , [ 245 ] 15th on Years ... 100 Movies [ 239 ]')
(0.7313326, '250', "decennial critics poll `` Critics ' Top Films '' , ranking at 171st on")
(0.7310125, '187', 'it is universally loved . `` [ ] Cinema Score reported that audiences for Star')

number: 28 context: Awards Won 6 Oscars . Another 50 wins & nominations .
(0.739734, '2011', '100 Greatest Films poll ; [ 249 ] in , it ranked as Best Sci-Fi Film on Best')
(0.7381549, '2011', 'Greatest Films poll ; [ 249 ] in , it ranked as Best Sci-Fi Film on')
(0.7333988, '100', "– # 1 [ 84 ] AFI 's Years ... 100 Cheers ( 2006 ) –")
(0.72872293, '1973', 'Accolades [ edit ] Alec Guinness , shown here in , received multiple award nominations , including one from the')
(0.72689235, '197', "won in the latter two categories . [ ] John Williams 's soundtrack album won the")
(0.72660565, '100', "# 39 [ 243 ] AFI 's Years ... 100 Movies ( 10th Anniversary")
(0.72595257, '250', "decennial critics poll `` Critics ' Top Films '' , ranking at 171st on")
(0.7253821, '197', "film won in the latter two categories . [ ] John Williams 's soundtrack album won the Grammy")
(0.7248118, '196', 'Best Score . [ ] It received six')
(0.72403014, '1973', 'edit ] Alec Guinness , shown here in , received multiple award nominations , including one')
(0.7237351, '100', 'Top 10 Sci-Fi Films , [ 245 ] 15th on Years ... 100 Movies [ 239 ] ( ranked 13th')
(0.72280484, '100', '37th greatest heroes respectively on Years ... 100 Heroes &')
(0.7215667, '239', 'Years ... 100 Movies [ ] ( ranked 13th on')
(0.7205267, '195', 'engineering of the Electronic Motion Control System ) . [ ] Additional nominations included Alec Guinness for Best Actor in')
(0.71918297, '100', 'Films , [ 245 ] 15th on Years ... 100 Movies [ 239 ]')

number: 93 context: Ratings Rotten Tomatoes %
(0.81896776, '93', 'Rotten Tomatoes indicates a % approval rating based')
(0.79643774, '93', 'website Rotten Tomatoes indicates a % approval rating based on')
(0.78905416, '93', 'aggregator website Rotten Tomatoes indicates a % approval rating based on 116')
(0.76431865, '93', 'review aggregator website Rotten Tomatoes indicates a % approval rating based on 116 reviews')
(0.7603664, '93', 'film review aggregator website Rotten Tomatoes indicates a % approval rating based on 116 reviews with')
(0.74713373, '93', 'The film review aggregator website Rotten Tomatoes indicates a % approval rating based on 116 reviews with an')
(0.7413862, '93', 'Tomatoes indicates a % approval rating')
(0.72921973, '93', '. The film review aggregator website Rotten Tomatoes indicates a % approval rating based on 116 reviews with an overall')
(0.69242907, '116', 'Rotten Tomatoes indicates a 93 % approval rating based on reviews with an overall rating of 8.71/10 . Its consensus')
(0.6734488, '116', 'Tomatoes indicates a 93 % approval rating based on reviews with an overall rating of 8.71/10 . Its')
(0.63773537, '9.2', 'Box office Critical response')
(0.63047135, '9.3', 'Critical response Accolades 10')
(0.6245948, '39', "Cheers ( 2006 ) – # [ 243 ] AFI 's 100")
(0.62259096, '116', '93 % approval rating based on reviews with an overall rating of')
(0.6218858, '1', "Scores ( 2005 ) – # [ 84 ] AFI 's 100")

number: 90 context: Ratings Metacritic / 100
(0.76789296, '90', '] Metacritic reports an aggregate score of out of 100 ( based on 24')
(0.7600951, '90', '183 ] Metacritic reports an aggregate score of out of 100 ( based on 24 reviews')
(0.7448875, '100', 'aggregate score of 90 out of ( based on 24 reviews )')
(0.7401429, '116', 'approval rating based on reviews with an overall')
(0.73943603, '90', '[ 183 ] Metacritic reports an aggregate score of out of 100 ( based on 24 reviews )')
(0.73510444, '90', 'Metacritic reports an aggregate score of out of 100 ( based on')
(0.7347263, '93', 'Rotten Tomatoes indicates a % approval rating based')
(0.7326696, '90', '`` [ 183 ] Metacritic reports an aggregate score of out of 100 ( based on 24 reviews ) ,')
(0.7294005, '116', '% approval rating based on reviews with an overall rating')
(0.72696984, '93', 'Tomatoes indicates a % approval rating')
(0.7220317, '93', 'aggregator website Rotten Tomatoes indicates a % approval rating based on 116')
(0.7192769, '116', '93 % approval rating based on reviews with an overall rating of')
(0.7187389, '90', 'aggregate score of out of 100')
(0.71813226, '24', '90 out of 100 ( based on reviews ) , indicating `` universal acclaim')
(0.7163541, '24', "aggregate score of 90 out of 100 ( based on reviews ) , indicating `` universal acclaim '' . [")

number: 100 context: Ratings Metacritic 90 /
(0.7899039, '90', '] Metacritic reports an aggregate score of out of 100 ( based on 24')
(0.78644526, '100', 'aggregate score of 90 out of ( based on 24 reviews )')
(0.7797539, '90', '183 ] Metacritic reports an aggregate score of out of 100 ( based on 24 reviews')
(0.76678485, '116', 'approval rating based on reviews with an overall')
(0.7642754, '100', 'an aggregate score of 90 out of ( based on 24 reviews ) ,')
(0.7578935, '90', 'Metacritic reports an aggregate score of out of 100 ( based on')
(0.75765085, '100', 'score of 90 out of ( based on 24 reviews')
(0.7523173, '100', '] Metacritic reports an aggregate score of 90 out of ( based on 24 reviews ) , indicating `` universal')
(0.74628055, '9.3', 'Critical response Accolades 10')
(0.74452114, '93', 'Rotten Tomatoes indicates a % approval rating based')
(0.74372774, '93', 'Tomatoes indicates a % approval rating')
(0.7437072, '116', '% approval rating based on reviews with an overall rating')
(0.74355227, '90', 'reports an aggregate score of out of 100 ( based')
(0.7370361, '100', 'Metacritic reports an aggregate score of 90 out of ( based on 24 reviews ) , indicating ``')
(0.7359257, '100', 'reports an aggregate score of 90 out of ( based on 24 reviews ) , indicating')

number: 90 context: Metascore
(0.55961823, '5', '3.5 Post-production 4 Soundtrack Cinematic and literary allusions')
(0.5527144, '1976', 'Matter of Time ( ) instead , which')
(0.54802144, '1968', 'A Space Odyssey ( ) , to conceptualize')
(0.5377474, '1968', ': A Space Odyssey ( ) , to conceptualize the')
(0.52983975, '6', 'and literary allusions Title 7 Marketing')
(0.5287625, '1976', 'of Time ( ) instead ,')
(0.5283923, '10.3', 'Cinematic influence Recognition 11')
(0.52754575, '10.1', '10 Legacy In popular')
(0.52541536, '6', 'Cinematic and literary allusions Title 7 Marketing 8')
(0.5235431, '5', 'Filming 3.5 Post-production 4 Soundtrack Cinematic and literary allusions 6')
(0.52289385, '1978', "the Mind 's Eye ( ) to be adapted as")
(0.5224783, '10.2', 'In popular culture Cinematic influence 10.3')
(0.52233887, '11', 'Cinematic influence 10.3 Recognition Merchandising 12 See also')
(0.5215699, '1138', 'completion of THX , Lucas was')
(0.52004445, '7', 'literary allusions 6 Title Marketing 8 Release 8.1')

number: 8.6 context: imdb Rating
(0.6107412, '12', 'Merchandising See')
(0.60706216, '238', 'cover . [ ] AFI 100')
(0.60403574, '93', 'Rotten Tomatoes indicates a % approval rating based')
(0.60128284, '8.2', 'release Theatrical')
(0.59174097, '93', 'website Rotten Tomatoes indicates a % approval rating based on')
(0.5870087, '633', 'film Squadron')
(0.5838181, '241', "# 37 Hero [ ] AFI 's 100")
(0.5835469, '247', 'Interactive . [ ] Star Wars')
(0.5792172, '240', "– # 27 [ ] AFI 's 100")
(0.5786286, '243', "– # 39 [ ] AFI 's 100")
(0.5783482, '84', "– # 1 [ ] AFI 's 100")
(0.5771066, '1998', 'Movies ( ) –')
(0.57694626, '262', 'plot . [ ] Lucasfilm adapted')
(0.576708, '93', 'aggregator website Rotten Tomatoes indicates a % approval rating based on 116')
(0.57623565, '239', "– # 15 [ ] AFI 's 100")

number: 1,109,357 context: imdb Votes
(0.6240424, '1997', 'audience polls : in , it ranked as')
(0.6128545, '12', 'Merchandising See')
(0.59626555, '238', 'cover . [ ] AFI 100')
(0.5931519, '195', 'Control System ) . [ ] Additional nominations included Alec')
(0.5905305, '249', 'Greatest Films poll ; [ ] in 2011 , it')
(0.5902933, '15', 'reading External')
(0.5886035, '2010', '[ edit ] In , George Lucas announced')
(0.5865531, '250', "decennial critics poll `` Critics ' Top Films '' , ranking at 171st on")
(0.58648586, '2008', 'films lists : in , Empire magazine ranked')
(0.58447313, '4', "in Channel 's 100")
(0.5834713, '262', 'plot . [ ] Lucasfilm adapted')
(0.583455, '1998', 'Movies ( ) –')
(0.5824435, '1997', 'high-profile audience polls : in , it ranked as the')
(0.5821528, '84', 'Film Scores , [ ] second on Top')
(0.58082485, '1997', 'polls : in , it ranked')

number: 21 context: DVD Sep 2004
(0.744596, '141', 'Laser Disc , [ ] Video 2000')
(0.7320378, '21', 'DVD on September , 2004 ,')
(0.72919464, '141', '] Laser Disc , [ ] Video 2000 ,')
(0.7180731, '4', 'edition tin box set on November , 2008 ; [ 147 ]')
(0.71721077, '21', 'on DVD on September , 2004 , in')
(0.71262586, '141', '[ 140 ] Laser Disc , [ ] Video 2000 , and VHS')
(0.70760465, '142', 'Video 2000 , and VHS [ ] [ 143 ] between the')
(0.70658505, '21', 'time on DVD on September , 2004 , in a')
(0.7064913, '142', '] Video 2000 , and VHS [ ] [ 143 ] between the 1980s')
(0.7063004, '4', 'tin box set on November , 2008 ; [ 147')
(0.70611554, '31', 'DVD sets from September 12 to December , 2006 , and again in a')
(0.7012844, '147', '4 , 2008 ; [ ] the original versions of')
(0.70117116, '1978', "'s re-release in July . ( Hearn 2005")
(0.70071197, '12', 'edition DVD sets from September to December 31 , 2006')
(0.69577855, '142', '141 ] Video 2000 , and VHS [ ] [ 143 ] between the 1980s and')

number: 2004 context: DVD 21 Sep
(0.71157664, '2000', '[ 141 ] Video , and VHS [')
(0.7098944, '2000', '141 ] Video , and VHS')
(0.70912147, '1978', '120 ] in , Lucasfilm distributed')
(0.69323266, '2000', 'Laser Disc , [ 141 ] Video , and VHS [ 142 ]')
(0.69276166, '141', 'Laser Disc , [ ] Video 2000')
(0.69086856, '141', '] Laser Disc , [ ] Video 2000 ,')
(0.68761694, '141', '[ 140 ] Laser Disc , [ ] Video 2000 , and VHS')
(0.6860588, '2000', ', [ 141 ] Video , and VHS [ 142')
(0.6827676, '2000', '] Laser Disc , [ 141 ] Video , and VHS [ 142 ] [')
(0.681306, '141', '140 ] Laser Disc , [ ] Video 2000 , and')
(0.6794164, '21', 'DVD on September , 2004 ,')
(0.677904, '142', '141 ] Video 2000 , and VHS [ ] [ 143 ] between the 1980s and')
(0.67735505, '2000', 'Video ,')
(0.67671096, '142', 'Video 2000 , and VHS [ ] [ 143 ] between the')
(0.6765259, '2008', 'box set on November 4 , ; [ 147 ] the original')
```

#### Lemonade Joe
Only 1 or 2 values have been matched correctly. Please see the Wikipedia article for Lemonade Joe to see that the values
from OMDb json either do not occur or are different (running time 84 vs 99 minutes!). Note that even the release year
mismatches by 3 years.
```
number: 1964 context: Year
(0.5646273, '99', 'time minutes Country Czechoslovakia Language Czech')
(0.5395047, '99', ') Running time minutes Country Czechoslovakia Language Czech Lemonade Joe')
(0.5389266, '99', 'Running time minutes Country Czechoslovakia Language Czech Lemonade')
(0.5173051, '1964', 'date October ( 1964-10')
(0.5152718, '99', 'Czechoslovakia ) Running time minutes Country Czechoslovakia Language Czech Lemonade Joe ,')
(0.5071691, '2', '. Contents 1 Plot Cast 3 Themes 4')
(0.50287014, '99', '( Czechoslovakia ) Running time minutes Country Czechoslovakia Language Czech Lemonade Joe , or')
(0.49650106, '2', '1 Plot Cast 3')
(0.492867, '99', ') ( Czechoslovakia ) Running time minutes Country Czechoslovakia Language Czech Lemonade Joe , or the')
(0.49069744, '8', 'also Notes')
(0.48947898, '7', 'Legacy See')
(0.48901492, '1', 'Contents Plot')
(0.48840657, '2', 'cowboys . Contents 1 Plot Cast 3 Themes 4 Production')
(0.48742795, '6', '5 Release and reception Legacy 7 See also')
(0.4855385, '7', 'reception 6 Legacy See also 8')

number: 25 context: Released Nov 1967
(0.7397592, '1964', 'Release date October ( 1964-10 )')
(0.7214769, '1964', ') Release date October ( 1964-10 ) (')
(0.7015945, '1964', 'US release ) Release date October ( 1964-10 ) ( Czechoslovakia )')
(0.6963198, '1964', 'release ) Release date October ( 1964-10 ) ( Czechoslovakia')
(0.69453716, '1964', '( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running')
(0.6687225, '1964', 'Corporation ( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running time')
(0.64987123, '1964', 'Pictures Corporation ( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running time 99')
(0.6383624, '1964', 'date October ( 1964-10')
(0.62621635, '4.3', '4.1 Sources 4.2 Filming Music 5 Release and')
(0.6202314, '1964', 'Artists Pictures Corporation ( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running time 99 minutes Country Czechoslovakia Language Czech')
(0.61222804, '6', 'Release and reception Legacy 7 See')
(0.6113436, '6', '5 Release and reception Legacy 7 See also')
(0.60402477, '2', 'Contents 1 Plot Cast 3 Themes')
(0.59816414, '7', '5 Release and reception 6 Legacy See also 8 Notes 8.1 References')
(0.5973694, '4.3', 'Sources 4.2 Filming Music 5 Release')

number: 1967 context: Released 25 Nov
(0.6567352, '1964', 'Release date October ( 1964-10 )')
(0.6438042, '1964', ') Release date October ( 1964-10 ) (')
(0.6143935, '5', '4.2 Filming 4.3 Music Release and reception 6')
(0.61103547, '4.3', 'Sources 4.2 Filming Music 5 Release')
(0.6065428, '4.3', '4.1 Sources 4.2 Filming Music 5 Release and')
(0.6022624, '1964', 'release ) Release date October ( 1964-10 ) ( Czechoslovakia')
(0.59891117, '1964', 'US release ) Release date October ( 1964-10 ) ( Czechoslovakia )')
(0.5977691, '1964', 'date October ( 1964-10')
(0.5926874, '5', 'Filming 4.3 Music Release and reception')
(0.5920097, '1964', '( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running')
(0.5844116, '2', 'Contents 1 Plot Cast 3 Themes')
(0.58214283, '6', 'Release and reception Legacy 7 See')
(0.5816821, '6', 'Filming 4.3 Music 5 Release and reception Legacy 7 See also 8 Notes 8.1')
(0.58023417, '6', '5 Release and reception Legacy 7 See also')
(0.57959974, '4.2', '3 Themes 4 Production 4.1 Sources Filming 4.3 Music 5 Release and')

number: 84 context: Runtime min
(0.5373734, '4.3', '4.2 Filming Music 5')
(0.5328407, '8', 'Release and reception 6 Legacy 7 See also Notes 8.1 References 8.2')
(0.5305959, '1964', 'Pictures Corporation ( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running time 99')
(0.5302553, '99', ') Running time minutes Country Czechoslovakia Language Czech Lemonade Joe')
(0.52286255, '2', '. Contents 1 Plot Cast 3 Themes 4')
(0.5227399, '99', 'Czechoslovakia ) Running time minutes Country Czechoslovakia Language Czech Lemonade Joe ,')
(0.5223019, '6', 'Release and reception Legacy 7 See')
(0.5221857, '8', '5 Release and reception 6 Legacy 7 See also Notes 8.1 References 8.2')
(0.5206162, '8.1', 'Release and reception 6 Legacy 7 See also 8 Notes References 8.2')
(0.52056015, '1964', 'Corporation ( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running time')
(0.5185567, '1964', ') Release date October ( 1964-10 ) (')
(0.5178572, '1964', 'Release date October ( 1964-10 )')
(0.5175464, '6', 'reception Legacy')
(0.51692647, '3', '1 Plot 2 Cast Themes 4 Production 4.1')
(0.51666, '1964', 'a Czechoslovak')

number: 1963 context: Plot Straight shooting Lemonade Joe cleans up Stetson City , in this musical parody of early Westerns , after shooting the pants off villain Old Pistol . Joe 's endorsement of Kolaloka ( Crazy Cola ) lemonade as the refresher that assures deadly aim , convinces the Arizona sin-town to abstain from alcohol . Based on the Czech stage production . But Trigger Whiskey maker Duke Badman 's brother the devious gunslinger Hogofogo , comes to save his sibling 's saloon from Joe 's allies , father and daughter temperance revivalists , the Goodmans .
(0.7897135, '1', 'town full of whiskey-drinking cowboys . Contents Plot 2 Cast 3 Themes 4 Production')
(0.7886049, '1', 'takes on a town full of whiskey-drinking cowboys . Contents Plot 2 Cast 3 Themes 4 Production 4.1 Sources 4.2')
(0.78114915, '1', 'on a town full of whiskey-drinking cowboys . Contents Plot 2 Cast 3 Themes 4 Production 4.1 Sources')
(0.78078234, '1', 'a town full of whiskey-drinking cowboys . Contents Plot 2 Cast 3 Themes 4 Production 4.1')
(0.7558417, '1', 'of whiskey-drinking cowboys . Contents Plot 2 Cast 3 Themes')
(0.7556356, '2', 'town full of whiskey-drinking cowboys . Contents 1 Plot Cast 3 Themes 4 Production 4.1 Sources 4.2 Filming')
(0.75095356, '1', 'full of whiskey-drinking cowboys . Contents Plot 2 Cast 3 Themes 4')
(0.74193263, '2', 'a town full of whiskey-drinking cowboys . Contents 1 Plot Cast 3 Themes 4 Production 4.1 Sources 4.2 Filming 4.3')
(0.73840404, '2', 'full of whiskey-drinking cowboys . Contents 1 Plot Cast 3 Themes 4 Production 4.1 Sources 4.2')
(0.73107886, '3', 'full of whiskey-drinking cowboys . Contents 1 Plot 2 Cast Themes 4 Production 4.1 Sources 4.2 Filming 4.3 Music 5')
(0.7307168, '2', 'of whiskey-drinking cowboys . Contents 1 Plot Cast 3 Themes 4 Production 4.1 Sources')
(0.72096467, '4', 'whiskey-drinking cowboys . Contents 1 Plot 2 Cast 3 Themes Production 4.1 Sources 4.2 Filming 4.3 Music 5 Release and')
(0.7156992, '3', 'of whiskey-drinking cowboys . Contents 1 Plot 2 Cast Themes 4 Production 4.1 Sources 4.2 Filming 4.3 Music')
(0.7156687, '2', 'whiskey-drinking cowboys . Contents 1 Plot Cast 3 Themes 4 Production 4.1')
(0.7083813, '1', 'whiskey-drinking cowboys . Contents Plot 2 Cast 3')

number: 1 context: Awards win .
(0.669394, '1', 'cowboys . Contents Plot 2 Cast')
(0.6488962, '2', '1 Plot Cast 3')
(0.6481873, '2', 'Plot Cast')
(0.6340687, '2', 'of whiskey-drinking cowboys . Contents 1 Plot Cast 3 Themes 4 Production 4.1 Sources')
(0.6328293, '1', 'whiskey-drinking cowboys . Contents Plot 2 Cast 3')
(0.6321132, '3', 'Cast Themes')
(0.6318526, '3', '2 Cast Themes 4')
(0.6316573, '2', 'whiskey-drinking cowboys . Contents 1 Plot Cast 3 Themes 4 Production 4.1')
(0.6314158, '2', 'cowboys . Contents 1 Plot Cast 3 Themes 4 Production')
(0.6313412, '5', '4.2 Filming 4.3 Music Release and reception 6')
(0.630249, '2', '. Contents 1 Plot Cast 3 Themes 4')
(0.6295801, '1', 'full of whiskey-drinking cowboys . Contents Plot 2 Cast 3 Themes 4')
(0.6278691, '6', 'reception Legacy')
(0.6276366, '1', 'of whiskey-drinking cowboys . Contents Plot 2 Cast 3 Themes')
(0.6271796, '5', 'Filming 4.3 Music Release and reception')

number: 7.7 context: imdb Rating
(0.531606, '1964', 'a Czechoslovak')
(0.52849174, '7', 'Legacy See')
(0.5085591, '1964', 'Pictures Corporation ( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running time 99')
(0.50745237, '5', 'Music Release')
(0.5046401, '1', 'cowboys . Contents Plot 2 Cast')
(0.5039185, '5', '4.3 Music Release and')
(0.5021826, '4.3', 'Filming Music')
(0.4936765, '1964', 'US release ) Release date October ( 1964-10 ) ( Czechoslovakia )')
(0.49108756, '2', 'Plot Cast')
(0.4908761, '1964', '( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running')
(0.48949575, '1964', 'Corporation ( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running time')
(0.48744637, '1964', 'Artists Pictures Corporation ( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running time 99 minutes Country Czechoslovakia Language Czech')
(0.48664472, '3', 'Cast Themes')
(0.48212066, '4.2', 'Sources Filming')
(0.4812002, '2', '1 Plot Cast 3')

number: 2,135 context: imdb Votes
(0.5434488, '7', 'Legacy See')
(0.5427239, '3', 'Cast Themes')
(0.53993213, '4.3', 'Filming Music')
(0.53849053, '1964', 'a Czechoslovak')
(0.53730416, '1', 'cowboys . Contents Plot 2 Cast')
(0.5351827, '4.2', 'Sources Filming')
(0.530169, '8', 'also Notes')
(0.5216398, '8.2', 'References')
(0.5209181, '2', 'Plot Cast')
(0.5199207, '3', '2 Cast Themes 4')
(0.5164531, '8.1', 'Notes References')
(0.5153364, '2', '1 Plot Cast 3')
(0.5132729, '1', 'Contents Plot')
(0.50611955, '1', 'whiskey-drinking cowboys . Contents Plot 2 Cast 3')
(0.49939927, '6', 'reception Legacy')

number: 25 context: DVD Apr 2006
(0.6731271, '1964', ') Release date October ( 1964-10 ) (')
(0.66740876, '1964', 'Release date October ( 1964-10 )')
(0.6510836, '4.3', 'Sources 4.2 Filming Music 5 Release')
(0.6492004, '4.3', '4.1 Sources 4.2 Filming Music 5 Release and')
(0.646116, '3', 'Plot 2 Cast Themes 4 Production')
(0.6436533, '3', '2 Cast Themes 4')
(0.6431719, '5', '4.2 Filming 4.3 Music Release and reception 6')
(0.6431459, '1964', 'US release ) Release date October ( 1964-10 ) ( Czechoslovakia )')
(0.64265513, '1964', 'release ) Release date October ( 1964-10 ) ( Czechoslovakia')
(0.64098996, '6', 'Release and reception Legacy 7 See')
(0.6409106, '6', '5 Release and reception Legacy 7 See also')
(0.63879573, '2', '1 Plot Cast 3')
(0.6377917, '4.2', '3 Themes 4 Production 4.1 Sources Filming 4.3 Music 5 Release and')
(0.6377268, '2', 'Contents 1 Plot Cast 3 Themes')
(0.6372522, '2', '. Contents 1 Plot Cast 3 Themes 4')

number: 2006 context: DVD 25 Apr
(0.6326968, '1964', 'Release date October ( 1964-10 )')
(0.62044173, '1964', ') Release date October ( 1964-10 ) (')
(0.6176647, '1964', 'date October ( 1964-10')
(0.61373806, '4.3', 'Sources 4.2 Filming Music 5 Release')
(0.6134107, '1964', 'release ) Release date October ( 1964-10 ) ( Czechoslovakia')
(0.6090139, '5', '4.2 Filming 4.3 Music Release and reception 6')
(0.6070088, '1964', 'US release ) Release date October ( 1964-10 ) ( Czechoslovakia )')
(0.6050754, '4.3', '4.1 Sources 4.2 Filming Music 5 Release and')
(0.6018759, '4.3', '4.2 Filming Music 5')
(0.59813905, '6', 'Filming 4.3 Music 5 Release and reception Legacy 7 See also 8 Notes 8.1')
(0.5950212, '6', '5 Release and reception Legacy 7 See also')
(0.59296507, '1964', '( US release ) Release date October ( 1964-10 ) ( Czechoslovakia ) Running')
(0.5923099, '6', 'Release and reception Legacy 7 See')
(0.5891311, '4.2', '3 Themes 4 Production 4.1 Sources Filming 4.3 Music 5 Release and')
(0.5858533, '6', 'Music 5 Release and reception Legacy 7 See also 8')
```

### Locating OMDb values in Wikipedia articles
The main experiment followed the procedure:

* Choose a movie (iteratively from the list)
* Build the NumberContext list for OMDb json and Wikipedia article.
* For each value in OMDb json, find `k = 15` closest (by cosine similarity) contexts among Wikipedia NumberContexts
* Filter only the pairs where the numeric value matches (note that it must be the in the same format as well).

#### Matched pairs count (w2v):
```
Movie: Star Wars IV
8/15 fields matched with Wiki
Movie: Star Wars V
6/16 fields matched with Wiki
Movie: Star Wars VI
5/15 fields matched with Wiki
Movie: Star Wars I
6/16 fields matched with Wiki
Movie: Star Wars II
7/16 fields matched with Wiki
Movie: Star Wars III
6/15 fields matched with Wiki
Movie: Forrest Gump
5/16 fields matched with Wiki
Movie: Back To The Future
5/17 fields matched with Wiki
Movie: David And Lisa
2/12 fields matched with Wiki
Movie: Marley And Me
4/16 fields matched with Wiki
Movie: 101 Dalmatians
3/16 fields matched with Wiki
Movie: Lassie
3/11 fields matched with Wiki
Movie: Titanic
6/19 fields matched with Wiki
Movie: Shawshank Redemption
5/15 fields matched with Wiki
Movie: Se7en
6/15 fields matched with Wiki
Movie: True Detective
2/13 fields matched with Wiki
Movie: Big Lebowski
1/14 fields matched with Wiki
Movie: Death Proof
4/10 fields matched with Wiki
Movie: Slumdog Millionaire
4/19 fields matched with Wiki
Movie: Lemonade Joe
1/10 fields matched with Wiki
```

#### Matched pairs count (BERT):
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

## Room for improvement and development (sorted by urgency)
### Numbers as words
GoogleNews vectors do not treat numbers as words, or at least not distinguished between, hence all numbers occurring in
contexts are treated as a string in `{'#', '##', '###', '####', ...}` depending on the number of digit.
### Month names into numbers
The set of rules for choosing "hard values" could be extended beyond numbers, even at this point, to get more feedback
from experiment results.
### Experiments with Question Answering
I believe that even at this stage it would be interesting to see how well it performs on Question Answering task - in a
limited scope of course: the documents is provided and the questions is a numeric value. If I choose to proceed with
this topic for Msc thesis, I would like to combine it with document selection based on question topic. 
### Training contexts
This is probably the key part of the project. If we find a matching value in two documents, we would like to strenghten
the connection between its contexts in different sources. Similarly, if we have a false positive case, we would like to
"draw aside" the two contexts vectorizations. Three questions arise at this point:

* How to vectorize the context. The choices vary from averaging single word embeddings to [bidirectional LSTMs](
https://www.aclweb.org/anthology/K16-1006)
* How to obtain the dataset. Marking the same values in distinct sources manually will be very slow and mundane. Instead
a dataset could be generated with a set of heuristics and trustworthy sources. Using the OMDb + Wiki example, I could
generate k = 15 closest pairs for each field in OMDb jsons, just as in experiments above. In the pairs where the values
match, the distance between contexts should be reduced, if the values are distinct - increased. Of course there will be
some false positives (the same value, but contexts are semantically different, e.g. year 2006, movie premiere vs DVD
release) and false negatives (the context matches but Wikipedia is inconsistent with IMDb and the value mismatches).
* Say we want to reduce or increase the distance between two contexts. How to choose a cost function? If the contexts
are semantically the same, it is simple - we want the distance to be as close to 0 as possible, and the distance can be
any function from which gradients are computable. It's easy to back-propagate in this scenario.
What if the contexts should be distanced apart? Choosing an arbitrary expected value for distance doesn't sound like a
good idea. Maybe negative sampling can somehow be applied here? TODO: think about it
### Two-way context
Depending on how the context will be vectorized in future, it may be important to distinguish between left-side and
right-side context (e.g. for some kind of RNN architecture).
### Values aggregation
This problem hasn't occurred in the movies experiments, but a nice goal for future would be to handle cases where one
source contains some aggregated value and the other has it split into compounds, e.g.:
```
Source1:
Marketing costs: 500$

Source2:
Linkedin Ads: 300
Facebook Ads: 100
Gumtree Ads: 100
```
An example idea would be to created new NumberContexts from existing ones if they are close enough, using several
aggregating functions (`sum, avg, mul`).
Another approach would be to build trees of NumberContexts instead of lists. Leaves would be the same pairs as in
original lists, and they could be joined into trees with hierarchical clustering.