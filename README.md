Goal: 

Because elections are coming up, I thought it would be cool to see how well (or how poorly) different types of models predict the outcome of elections. One struggle was the limited amount of data (there have only been 11 elections between 1976 and today), so I decided to predict which party would win each state instead, which would give me around 50 times as many data points. A major setback of this process was trying to determine overall general election odds when dealing with dependent state results. Regardless, I tried a few different methods to model the dependence between states (even if they may not be entirely accurate in predicting the overall electiton outcome).

Feel free to run the classification and regression notebooks to view some of these outcomes. As soon as general election polling numbers are released I plan to add a third notebook.

Dataset Design Choices: 

In general, I arbirtrarily set republican to 0 and democrat to 1. I assumed these are the only two parties that can win the presidency. I dropped all (year, state) combinations out of the dataset without polling data (about 20% of them), with the assumption that polling data was the best predictor of voting patterns. When computing the dem_prop_x_years_prior variables, we wouldn’t be able to calculate at least one of the variable values for any elections from 1976 to 1984. In this case, I just used the current year’s polling data. 

Credits:

https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX 
https://www.census.gov/data/tables/time-series/dec/popchange-data-text.html
https://github.com/fivethirtyeight/data/tree/master/polls 
