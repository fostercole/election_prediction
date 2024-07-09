Goal: 

Because elections are coming up, I thought it would be cool to see how well (or how poorly) different types of models predict the outcome of elections. One struggle was the limited amount of data (there have only been 11 elections between 1976 and today), so I decided to predict which party would win each state instead, which would give me around 50 times as many data points. To infer who which party would win an election, I'd run data from all 50 states through a prediction model, calculate the percentage chance that party X would win the election in each state, and then run a Monte Carlo simulation to determine the probability that party X would win >270 electoral votes given these output probabilities. We can't determine the exact probability that party X wins because all states are not IID, but we can calculate the expected number of votes for party X.


Dataset Design Choices: 

In general, I set republican to 0 and democrat to 1. I assumed these are the only two parties that can win the presidency. I dropped all (year, state) combinations out of the dataset without polling data (about 20% of them), with the assumption that polling data was the best predictor of voting patterns. When computing the dem_prop_x_years_prior variables, we wouldn’t be able to calculate at least one of the variable values for any elections from 1976 to 1984. In this case, I just used the current year’s polling data. 


Credits:

https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX 
https://www.census.gov/data/tables/time-series/dec/popchange-data-text.html
https://github.com/fivethirtyeight/data/tree/master/polls 
