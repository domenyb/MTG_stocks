Problem statement for this folder:

MTG (Magic: The Gathering) is primarily a game, but some of its cards have huge value behind them. The strength of individual cards in the metagame can greatly influence their (or other cards's) market value.
I've decided to monitor the price of cards in standard-legal sets for a period in time to then use them for a project, since these prices should work very similarly to stock prices. - They can move up or down depending on real-life events or just some cards showing up on tournaments.

A baseline to reading the project: 
  - All the data manipulation is in the notebooks that have a naming convention: <number>_name.ipynb where <number> estabilishes the continuity between them while the name attemts to describe the contents of the notebook.
  - Every notebook (except 00, which is hardly a notebook) has a foreword that was written looking back at the notebook and briefly describing the contents and results. 
  - The notebooks have two type of commenting, the markdown cells typically describe my thought process going into the cells before/after them, while the standard python commenting in the code cells was created while writing the actual code and have a narrower scope.
  
 
 

The simplifications while 'mathematically' make sense, most likely also make the real-world application of this code impossible. I'm aware of this, and the code was never intended to be made to produce financial gain, but rather to explore an interesting space - the card market - and provide insight about my development with data. 




***Update 2020 Oct 09.***

An update with a number of new notebooks:

Basic data exploration, clustering of cards, and a very basic - albeit successful - trading strategy executed over 4 months to generate profit.

Next commit I intend to use the Scikit-learn library to try a few ML algorithms to compare their result with this simplistic baseline strategy

