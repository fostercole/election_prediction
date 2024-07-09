
Dataset Design Choices: 

In general, I set republican to 0 and democrat to 1. I assumed these are the only two parties that can win the presidency. I dropped all (year, state) combinations out of the dataset without polling data (about 20% of them), with the assumption that polling data was the best predictor of voting patterns. When computing the dem_prop_x_years_prior variables, we wouldn’t be able to calculate at least one of the variable values for any elections from 1976 to 1984. In this case, I just used the current year’s


Credits:

https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX 
https://www.census.gov/data/tables/time-series/dec/popchange-data-text.html
https://github.com/fivethirtyeight/data/tree/master/polls 
