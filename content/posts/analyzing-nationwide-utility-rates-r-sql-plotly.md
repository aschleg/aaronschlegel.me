Title: Analyzing Nationwide Utility Rates with R, SQL and Plotly
Date: 2018-02-09
Tags: R, Plotly, SQL
Category: R
Slug: analyze-nationwide-utility-rates-r-sql-plotly
Author: Aaron Schlegel
Summary: R and SQL make excellent complements for analyzing data due to their respective strengths. The sqldf package provides an interface for working with SQL in R by querying data from a database into an R data.frame. This post will demonstrate how to query and analyze data using the sqldf package in conjunction with the graphing libraries plotly and ggplot2 as well as some other packages that provide useful statistical tests and other functions.


R and SQL make excellent complements for analyzing data due to their respective strengths. The [sqldf package](https://cran.r-project.org/web/packages/sqldf/) provides an interface for working with SQL in R by querying data from a database into an R `data.frame`. This post will demonstrate how to query and analyze data using the sqldf package in conjunction with the graphing libraries [plotly](https://plot.ly/r/) and [ggplot2](http://ggplot2.org/) as well as some other packages that provide useful statistical tests and other functions.

The data that will be examined in this post is the [U.S. Electric Utility Companies and Rates dataset](http://catalog.data.gov/dataset/u-s-electric-utility-companies-and-rates-look-up-by-zipcode-feb-2011-57a7c), compiled by data.gov. The data is described as follows:

>This dataset, compiled by NREL using data from Ventyx and the U.S. Energy Information Administration dataset 861, provides average residential, commercial and industrial electricity rates by zip code for both investor owned utilities (IOU) and non-investor owned utilities. Note: the file includes average rates for each utility, but not the detailed rate structure data found in the OpenEI U.S. Utility Rate Database. A more recent version of this data is also available through the NREL Utility Rate API with more search options. This data was released by NREL/Ventyx in February 2011.

Start by loading the sqldf package and the other packages that will be used.


```r
library(sqldf)
library(plotly)
library(ggplot2)
library(reshape2)
library(dplyr)
library(agricolae)
library(cluster)
```

## Loading the Data Using R and SQL

The dataset comes in two csv files. To load the data to use with SQL, a file connection is created for each csv.


```r
iou <- file('../data/iouzipcodes2011.csv')
nou <- file('../data/noniouzipcodes2011.csv')
```

A combined `data.frame` with both files can be created using a SQL query with the sqldf package. The two datasets are appended using the `UNION ALL` operator. Here is a link to where I found this useful method to [load the data into R using SQL](http://www.cerebralmastication.com/2009/11/loading-big-data-into-r/).


```r
utility_df <- sqldf('SELECT * FROM iou 
                     UNION ALL 
                     SELECT * FROM nou', dbname='utility_db')
```

To quickly test the data was loaded successfully into an R `data.frame` using the SQL query above, inspect the first five rows of the database using the following query.


```r
sqldf('SELECT * FROM utility_df LIMIT 5')
```

```
##     zip eiaid     utility_name state service_type      ownership comm_rate
## 1 35218   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
## 2 35219   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
## 3 35214   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
## 4 35215   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
## 5 35216   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
##     ind_rate  res_rate
## 1 0.06029244 0.1149433
## 2 0.06029244 0.1149433
## 3 0.06029244 0.1149433
## 4 0.06029244 0.1149433
## 5 0.06029244 0.1149433
```

This query is essentially the same as the `head()` function as seen below.


```r
head(utility_df, 5)
```

```
##     zip eiaid     utility_name state service_type      ownership comm_rate
## 1 35218   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
## 2 35219   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
## 3 35214   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
## 4 35215   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
## 5 35216   195 Alabama Power Co    AL      Bundled Investor Owned 0.1057612
##     ind_rate  res_rate
## 1 0.06029244 0.1149433
## 2 0.06029244 0.1149433
## 3 0.06029244 0.1149433
## 4 0.06029244 0.1149433
## 5 0.06029244 0.1149433
```

## Analyzing the Data with R and SQL

Let's say we are interested in finding average electricity rates for each group (commercial, residential, industrial) at a state level. The following query is used to collect the desired data into an R `data.frame`. The `AVG()` aggregation used in the query as we are interested in the overall average of all utilities by state.


```r
state.avg.rates <- sqldf('SELECT state, AVG(comm_rate) as comm_rate, AVG(ind_rate) as ind_rate, AVG(res_rate) as res_rate  
                          FROM utility_df 
                          GROUP BY state 
                          ORDER BY state')

head(state.avg.rates)
```

```
##   state  comm_rate   ind_rate   res_rate
## 1    AK 0.31816373 0.08144623 0.35434410
## 2    AL 0.08038278 0.06528392 0.08398812
## 3    AR 0.07966575 0.06387541 0.09221964
## 4    AZ 0.10138372 0.07438303 0.11264911
## 5    CA 0.10370644 0.07208640 0.13453128
## 6    CO 0.10266863 0.07872797 0.11884693
```

The query outputs a `data.frame` containing each state's average electricity rates for each group. This data can be visualized in a [choropleth graph](https://plot.ly/r/choropleth-maps/) with the plotly library.


```r
# Define what is displayed when hovering over the states in the choropleth graph.

state.avg.rates$hover <- with(state.avg.rates, paste(state, '<br>', 'Commercial Rate', round(comm_rate, 3), 
                              '<br>', 'Industrial Rate', round(ind_rate, 3),
                              '<br>', 'Residential Rate', round(res_rate, 3)))

# Set the state borders to white
state.border <- list(color = toRGB('white'))

# Define how the choropleth graph will be displayed
geo <- list(
  scope = 'usa',
  projection = list(type = 'albers usa'),
  showlakes = TRUE,
  lakecolor = toRGB('white')
)

# Build the graph and plot.
p <- plot_ly(state.avg.rates, z = round(state.avg.rates$res_rate, 3), text = state.avg.rates$hover, locations = state.avg.rates$state, type = 'choropleth',
        locationmode = 'USA-states', colors = 'Blues', marker = list(line = state.border)) %>%
  layout(title = 'Average Electricity Rates by State', geo = geo)

p
```

<!--html_preserve--><div id="153c743848da" style="width:672px;height:480px;" class="plotly html-widget"></div>
<script type="application/json" data-for="153c743848da">{"x":{"visdat":{"153c1b106fb1":["function () ","plotlyVisDat"]},"cur_data":"153c1b106fb1","attrs":{"153c1b106fb1":{"z":[0.354,0.084,0.092,0.113,0.135,0.119,0.133,0.083,0.095,0.117,0.113,0.364,0.111,0.084,0.094,0.106,0.117,0.074,0.088,0.112,0.09,0.11,0.094,0.111,0.1,0.074,0.09,0.097,0.086,0.1,0.121,0.106,0.125,0.061,0.13,0.086,0.1,0.061,0.093,0.105,0.11,0.095,0.052,0.112,0.088,0.107,0.171,0.064,0.13,0.101,0.099],"text":["AK <br> Commercial Rate 0.318 <br> Industrial Rate 0.081 <br> Residential Rate 0.354","AL <br> Commercial Rate 0.08 <br> Industrial Rate 0.065 <br> Residential Rate 0.084","AR <br> Commercial Rate 0.08 <br> Industrial Rate 0.064 <br> Residential Rate 0.092","AZ <br> Commercial Rate 0.101 <br> Industrial Rate 0.074 <br> Residential Rate 0.113","CA <br> Commercial Rate 0.104 <br> Industrial Rate 0.072 <br> Residential Rate 0.135","CO <br> Commercial Rate 0.103 <br> Industrial Rate 0.079 <br> Residential Rate 0.119","CT <br> Commercial Rate 0.112 <br> Industrial Rate 0.088 <br> Residential Rate 0.133","DC <br> Commercial Rate 0.09 <br> Industrial Rate 0.007 <br> Residential Rate 0.083","DE <br> Commercial Rate 0.077 <br> Industrial Rate 0.036 <br> Residential Rate 0.095","FL <br> Commercial Rate 0.102 <br> Industrial Rate 0.08 <br> Residential Rate 0.117","GA <br> Commercial Rate 0.102 <br> Industrial Rate 0.065 <br> Residential Rate 0.113","HI <br> Commercial Rate 0.35 <br> Industrial Rate 0.312 <br> Residential Rate 0.364","IA <br> Commercial Rate 0.087 <br> Industrial Rate 0.055 <br> Residential Rate 0.111","ID <br> Commercial Rate 0.071 <br> Industrial Rate 0.052 <br> Residential Rate 0.084","IL <br> Commercial Rate 0.073 <br> Industrial Rate 0.045 <br> Residential Rate 0.094","IN <br> Commercial Rate 0.094 <br> Industrial Rate 0.066 <br> Residential Rate 0.106","KS <br> Commercial Rate 0.103 <br> Industrial Rate 0.093 <br> Residential Rate 0.117","KY <br> Commercial Rate 0.073 <br> Industrial Rate 0.06 <br> Residential Rate 0.074","LA <br> Commercial Rate 0.087 <br> Industrial Rate 0.064 <br> Residential Rate 0.088","MA <br> Commercial Rate 0.107 <br> Industrial Rate 0.089 <br> Residential Rate 0.112","MD <br> Commercial Rate 0.074 <br> Industrial Rate 0.051 <br> Residential Rate 0.09","ME <br> Commercial Rate 0.078 <br> Industrial Rate 0.015 <br> Residential Rate 0.11","MI <br> Commercial Rate 0.077 <br> Industrial Rate 0.047 <br> Residential Rate 0.094","MN <br> Commercial Rate 0.091 <br> Industrial Rate 0.074 <br> Residential Rate 0.111","MO <br> Commercial Rate 0.085 <br> Industrial Rate 0.054 <br> Residential Rate 0.1","MS <br> Commercial Rate 0.075 <br> Industrial Rate 0.072 <br> Residential Rate 0.074","MT <br> Commercial Rate 0.077 <br> Industrial Rate 0.057 <br> Residential Rate 0.09","NC <br> Commercial Rate 0.081 <br> Industrial Rate 0.062 <br> Residential Rate 0.097","ND <br> Commercial Rate 0.074 <br> Industrial Rate 0.064 <br> Residential Rate 0.086","NE <br> Commercial Rate 0.096 <br> Industrial Rate 0.092 <br> Residential Rate 0.1","NH <br> Commercial Rate 0.106 <br> Industrial Rate 0.104 <br> Residential Rate 0.121","NJ <br> Commercial Rate 0.093 <br> Industrial Rate 0.068 <br> Residential Rate 0.106","NM <br> Commercial Rate 0.111 <br> Industrial Rate 0.072 <br> Residential Rate 0.125","NV <br> Commercial Rate 0.053 <br> Industrial Rate 0.04 <br> Residential Rate 0.061","NY <br> Commercial Rate 0.097 <br> Industrial Rate 0.071 <br> Residential Rate 0.13","OH <br> Commercial Rate 0.076 <br> Industrial Rate 0.045 <br> Residential Rate 0.086","OK <br> Commercial Rate 0.088 <br> Industrial Rate 0.055 <br> Residential Rate 0.1","OR <br> Commercial Rate 0.064 <br> Industrial Rate 0.043 <br> Residential Rate 0.061","PA <br> Commercial Rate 0.072 <br> Industrial Rate 0.07 <br> Residential Rate 0.093","RI <br> Commercial Rate 0.086 <br> Industrial Rate 0.075 <br> Residential Rate 0.105","SC <br> Commercial Rate 0.097 <br> Industrial Rate 0.064 <br> Residential Rate 0.11","SD <br> Commercial Rate 0.084 <br> Industrial Rate 0.057 <br> Residential Rate 0.095","TN <br> Commercial Rate 0.057 <br> Industrial Rate 0.076 <br> Residential Rate 0.052","TX <br> Commercial Rate 0.107 <br> Industrial Rate 0.069 <br> Residential Rate 0.112","UT <br> Commercial Rate 0.075 <br> Industrial Rate 0.053 <br> Residential Rate 0.088","VA <br> Commercial Rate 0.088 <br> Industrial Rate 0.065 <br> Residential Rate 0.107","VT <br> Commercial Rate 0.151 <br> Industrial Rate 0.108 <br> Residential Rate 0.171","WA <br> Commercial Rate 0.06 <br> Industrial Rate 0.046 <br> Residential Rate 0.064","WI <br> Commercial Rate 0.104 <br> Industrial Rate 0.073 <br> Residential Rate 0.13","WV <br> Commercial Rate 0.086 <br> Industrial Rate 0.064 <br> Residential Rate 0.101","WY <br> Commercial Rate 0.086 <br> Industrial Rate 0.063 <br> Residential Rate 0.099"],"locations":["AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"],"locationmode":"USA-states","marker":{"line":{"color":"rgba(255,255,255,1)"}},"colors":"Blues","alpha":1,"sizes":[10,100],"type":"choropleth"}},"layout":{"margin":{"b":40,"l":60,"t":25,"r":10},"title":"Average Electricity Rates by State","geo":{"scope":"usa","projection":{"type":"albers usa"},"showlakes":true,"lakecolor":"rgba(255,255,255,1)"},"xaxis":{"domain":[0,1]},"yaxis":{"domain":[0,1]},"hovermode":"closest","showlegend":false,"legend":{"y":0.5,"yanchor":"top"}},"source":"A","config":{"modeBarButtonsToAdd":[{"name":"Collaborate","icon":{"width":1000,"ascent":500,"descent":-50,"path":"M487 375c7-10 9-23 5-36l-79-259c-3-12-11-23-22-31-11-8-22-12-35-12l-263 0c-15 0-29 5-43 15-13 10-23 23-28 37-5 13-5 25-1 37 0 0 0 3 1 7 1 5 1 8 1 11 0 2 0 4-1 6 0 3-1 5-1 6 1 2 2 4 3 6 1 2 2 4 4 6 2 3 4 5 5 7 5 7 9 16 13 26 4 10 7 19 9 26 0 2 0 5 0 9-1 4-1 6 0 8 0 2 2 5 4 8 3 3 5 5 5 7 4 6 8 15 12 26 4 11 7 19 7 26 1 1 0 4 0 9-1 4-1 7 0 8 1 2 3 5 6 8 4 4 6 6 6 7 4 5 8 13 13 24 4 11 7 20 7 28 1 1 0 4 0 7-1 3-1 6-1 7 0 2 1 4 3 6 1 1 3 4 5 6 2 3 3 5 5 6 1 2 3 5 4 9 2 3 3 7 5 10 1 3 2 6 4 10 2 4 4 7 6 9 2 3 4 5 7 7 3 2 7 3 11 3 3 0 8 0 13-1l0-1c7 2 12 2 14 2l218 0c14 0 25-5 32-16 8-10 10-23 6-37l-79-259c-7-22-13-37-20-43-7-7-19-10-37-10l-248 0c-5 0-9-2-11-5-2-3-2-7 0-12 4-13 18-20 41-20l264 0c5 0 10 2 16 5 5 3 8 6 10 11l85 282c2 5 2 10 2 17 7-3 13-7 17-13z m-304 0c-1-3-1-5 0-7 1-1 3-2 6-2l174 0c2 0 4 1 7 2 2 2 4 4 5 7l6 18c0 3 0 5-1 7-1 1-3 2-6 2l-173 0c-3 0-5-1-8-2-2-2-4-4-4-7z m-24-73c-1-3-1-5 0-7 2-2 3-2 6-2l174 0c2 0 5 0 7 2 3 2 4 4 5 7l6 18c1 2 0 5-1 6-1 2-3 3-5 3l-174 0c-3 0-5-1-7-3-3-1-4-4-5-6z"},"click":"function(gd) { \n        // is this being viewed in RStudio?\n        if (location.search == '?viewer_pane=1') {\n          alert('To learn about plotly for collaboration, visit:\\n https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html');\n        } else {\n          window.open('https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html', '_blank');\n        }\n      }"}],"cloud":false},"data":[{"colorbar":{"title":"","ticklen":2,"len":0.5,"y":1,"lenmode":"fraction","yanchor":"top"},"colorscale":[["0","rgba(247,251,255,1)"],["0.0296474358974359","rgba(241,247,253,1)"],["0.0705128205128205","rgba(233,242,250,1)"],["0.100160256410256","rgba(227,238,249,1)"],["0.104700854700855","rgba(226,238,248,1)"],["0.111645299145299","rgba(225,237,248,1)"],["0.118589743589744","rgba(223,236,247,1)"],["0.125534188034188","rgba(222,235,247,1)"],["0.133547008547009","rgba(220,234,246,1)"],["0.137019230769231","rgba(220,233,246,1)"],["0.143162393162393","rgba(219,233,246,1)"],["0.15357905982906","rgba(217,231,245,1)"],["0.153846153846154","rgba(216,231,245,1)"],["0.170138888888889","rgba(213,229,244,1)"],["0.173611111111111","rgba(213,229,244,1)"],["0.185897435897436","rgba(210,227,243,1)"],["0.189102564102564","rgba(210,227,243,1)"],["0.192307692307692","rgba(209,226,243,1)"],["0.195512820512821","rgba(208,226,242,1)"],["0.208333333333333","rgba(206,224,242,1)"],["0.219017094017094","rgba(204,223,241,1)"],["0.24599358974359","rgba(199,220,239,1)"],["0.258012820512821","rgba(195,218,238,1)"],["0.371794871794872","rgba(159,202,225,1)"],["1","rgba(8,48,107,1)"]],"showscale":true,"z":[0.354,0.084,0.092,0.113,0.135,0.119,0.133,0.083,0.095,0.117,0.113,0.364,0.111,0.084,0.094,0.106,0.117,0.074,0.088,0.112,0.09,0.11,0.094,0.111,0.1,0.074,0.09,0.097,0.086,0.1,0.121,0.106,0.125,0.061,0.13,0.086,0.1,0.061,0.093,0.105,0.11,0.095,0.052,0.112,0.088,0.107,0.171,0.064,0.13,0.101,0.099],"text":["AK <br> Commercial Rate 0.318 <br> Industrial Rate 0.081 <br> Residential Rate 0.354","AL <br> Commercial Rate 0.08 <br> Industrial Rate 0.065 <br> Residential Rate 0.084","AR <br> Commercial Rate 0.08 <br> Industrial Rate 0.064 <br> Residential Rate 0.092","AZ <br> Commercial Rate 0.101 <br> Industrial Rate 0.074 <br> Residential Rate 0.113","CA <br> Commercial Rate 0.104 <br> Industrial Rate 0.072 <br> Residential Rate 0.135","CO <br> Commercial Rate 0.103 <br> Industrial Rate 0.079 <br> Residential Rate 0.119","CT <br> Commercial Rate 0.112 <br> Industrial Rate 0.088 <br> Residential Rate 0.133","DC <br> Commercial Rate 0.09 <br> Industrial Rate 0.007 <br> Residential Rate 0.083","DE <br> Commercial Rate 0.077 <br> Industrial Rate 0.036 <br> Residential Rate 0.095","FL <br> Commercial Rate 0.102 <br> Industrial Rate 0.08 <br> Residential Rate 0.117","GA <br> Commercial Rate 0.102 <br> Industrial Rate 0.065 <br> Residential Rate 0.113","HI <br> Commercial Rate 0.35 <br> Industrial Rate 0.312 <br> Residential Rate 0.364","IA <br> Commercial Rate 0.087 <br> Industrial Rate 0.055 <br> Residential Rate 0.111","ID <br> Commercial Rate 0.071 <br> Industrial Rate 0.052 <br> Residential Rate 0.084","IL <br> Commercial Rate 0.073 <br> Industrial Rate 0.045 <br> Residential Rate 0.094","IN <br> Commercial Rate 0.094 <br> Industrial Rate 0.066 <br> Residential Rate 0.106","KS <br> Commercial Rate 0.103 <br> Industrial Rate 0.093 <br> Residential Rate 0.117","KY <br> Commercial Rate 0.073 <br> Industrial Rate 0.06 <br> Residential Rate 0.074","LA <br> Commercial Rate 0.087 <br> Industrial Rate 0.064 <br> Residential Rate 0.088","MA <br> Commercial Rate 0.107 <br> Industrial Rate 0.089 <br> Residential Rate 0.112","MD <br> Commercial Rate 0.074 <br> Industrial Rate 0.051 <br> Residential Rate 0.09","ME <br> Commercial Rate 0.078 <br> Industrial Rate 0.015 <br> Residential Rate 0.11","MI <br> Commercial Rate 0.077 <br> Industrial Rate 0.047 <br> Residential Rate 0.094","MN <br> Commercial Rate 0.091 <br> Industrial Rate 0.074 <br> Residential Rate 0.111","MO <br> Commercial Rate 0.085 <br> Industrial Rate 0.054 <br> Residential Rate 0.1","MS <br> Commercial Rate 0.075 <br> Industrial Rate 0.072 <br> Residential Rate 0.074","MT <br> Commercial Rate 0.077 <br> Industrial Rate 0.057 <br> Residential Rate 0.09","NC <br> Commercial Rate 0.081 <br> Industrial Rate 0.062 <br> Residential Rate 0.097","ND <br> Commercial Rate 0.074 <br> Industrial Rate 0.064 <br> Residential Rate 0.086","NE <br> Commercial Rate 0.096 <br> Industrial Rate 0.092 <br> Residential Rate 0.1","NH <br> Commercial Rate 0.106 <br> Industrial Rate 0.104 <br> Residential Rate 0.121","NJ <br> Commercial Rate 0.093 <br> Industrial Rate 0.068 <br> Residential Rate 0.106","NM <br> Commercial Rate 0.111 <br> Industrial Rate 0.072 <br> Residential Rate 0.125","NV <br> Commercial Rate 0.053 <br> Industrial Rate 0.04 <br> Residential Rate 0.061","NY <br> Commercial Rate 0.097 <br> Industrial Rate 0.071 <br> Residential Rate 0.13","OH <br> Commercial Rate 0.076 <br> Industrial Rate 0.045 <br> Residential Rate 0.086","OK <br> Commercial Rate 0.088 <br> Industrial Rate 0.055 <br> Residential Rate 0.1","OR <br> Commercial Rate 0.064 <br> Industrial Rate 0.043 <br> Residential Rate 0.061","PA <br> Commercial Rate 0.072 <br> Industrial Rate 0.07 <br> Residential Rate 0.093","RI <br> Commercial Rate 0.086 <br> Industrial Rate 0.075 <br> Residential Rate 0.105","SC <br> Commercial Rate 0.097 <br> Industrial Rate 0.064 <br> Residential Rate 0.11","SD <br> Commercial Rate 0.084 <br> Industrial Rate 0.057 <br> Residential Rate 0.095","TN <br> Commercial Rate 0.057 <br> Industrial Rate 0.076 <br> Residential Rate 0.052","TX <br> Commercial Rate 0.107 <br> Industrial Rate 0.069 <br> Residential Rate 0.112","UT <br> Commercial Rate 0.075 <br> Industrial Rate 0.053 <br> Residential Rate 0.088","VA <br> Commercial Rate 0.088 <br> Industrial Rate 0.065 <br> Residential Rate 0.107","VT <br> Commercial Rate 0.151 <br> Industrial Rate 0.108 <br> Residential Rate 0.171","WA <br> Commercial Rate 0.06 <br> Industrial Rate 0.046 <br> Residential Rate 0.064","WI <br> Commercial Rate 0.104 <br> Industrial Rate 0.073 <br> Residential Rate 0.13","WV <br> Commercial Rate 0.086 <br> Industrial Rate 0.064 <br> Residential Rate 0.101","WY <br> Commercial Rate 0.086 <br> Industrial Rate 0.063 <br> Residential Rate 0.099"],"locations":["AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"],"locationmode":"USA-states","marker":{"line":{"color":"rgba(255,255,255,1)"}},"type":"choropleth","frame":null}],"highlight":{"on":"plotly_click","persistent":false,"dynamic":false,"selectize":false,"opacityDim":0.2,"selected":{"opacity":1}},"base_url":"https://plot.ly"},"evals":["config.modeBarButtonsToAdd.0.click"],"jsHooks":{"render":[{"code":"function(el, x) { var ctConfig = crosstalk.var('plotlyCrosstalkOpts').set({\"on\":\"plotly_click\",\"persistent\":false,\"dynamic\":false,\"selectize\":false,\"opacityDim\":0.2,\"selected\":{\"opacity\":1}}); }","data":null}]}}</script><!--/html_preserve-->

The shading represents the average residential rates by state as specified in the plotting function. Several quick inferences can be made from the choropleth graph:

* Hawaii and Alaska have the highest residential electricity rates by far at about .35, with Vermont next at .17. 
* Most of the Mid and Central United States average between a residential rate of 0.09 to .13.
* Washington, Oregon, Nevada, and Tennesse have the lowest residential electricity rates.

The states can also be clustered using the `kmeans()` function in R and plotted with the `clustplot` function from the [cluster](https://cran.r-project.org/web/packages/cluster/index.html) package. The number of clusters is set at six due to the number of ticks output from the choropleth graph (completely arbitrary and should not be done in practice, for example, purposes only). 


```r
state.avg.rates$state <- as.factor(state.avg.rates$state)
rownames(state.avg.rates) <- state.avg.rates$state
clust <- kmeans(state.avg.rates[,2:4], 6)
clusplot(state.avg.rates[,2:4], clust$cluster, color=TRUE, shade=TRUE, labels=2, lines=0, main = "Cluster Plot of States' Electricity Rates")
```

![](utility_rates_files/figure-html/unnamed-chunk-8-1.png)<!-- -->

As one might expect from the choropleth graph, Hawaii and Alaska are put into their own cluster. The extreme values of Hawaii and Alaska make it harder to visualize the clusters of the other states. Let's perform another query using SQL's `WHERE` clause to remove the states in question.


```r
state.avg.rates2 <- sqldf('SELECT state, AVG(comm_rate) as comm_rate, AVG(ind_rate) as ind_rate, AVG(res_rate) as res_rate  
                           FROM utility_df 
                           WHERE NOT state IN ("AK", "HI") 
                           GROUP BY state 
                           ORDER BY state')
```

With Hawaii and Alaska removed, plot a new choropleth graph to display the state average residential electricity rate.


```r
p <- plot_ly(state.avg.rates2, z = round(state.avg.rates2$res_rate, 3), text = paste('Residential Rate:', round(state.avg.rates2$res_rate, 3)), locations = state.avg.rates2$state, type = 'choropleth',
        locationmode = 'USA-states', colors = 'Blues', marker = list(line = state.border)) %>%
  layout(title = 'Average Residential Electricity Rates by State', geo = geo)

p
```

<!--html_preserve--><div id="153c46e41d7d" style="width:672px;height:480px;" class="plotly html-widget"></div>
<script type="application/json" data-for="153c46e41d7d">{"x":{"visdat":{"153c643b10bb":["function () ","plotlyVisDat"]},"cur_data":"153c643b10bb","attrs":{"153c643b10bb":{"z":[0.084,0.092,0.113,0.135,0.119,0.133,0.083,0.095,0.117,0.113,0.111,0.084,0.094,0.106,0.117,0.074,0.088,0.112,0.09,0.11,0.094,0.111,0.1,0.074,0.09,0.097,0.086,0.1,0.121,0.106,0.125,0.061,0.13,0.086,0.1,0.061,0.093,0.105,0.11,0.095,0.052,0.112,0.088,0.107,0.171,0.064,0.13,0.101,0.099],"text":["Residential Rate: 0.084","Residential Rate: 0.092","Residential Rate: 0.113","Residential Rate: 0.135","Residential Rate: 0.119","Residential Rate: 0.133","Residential Rate: 0.083","Residential Rate: 0.095","Residential Rate: 0.117","Residential Rate: 0.113","Residential Rate: 0.111","Residential Rate: 0.084","Residential Rate: 0.094","Residential Rate: 0.106","Residential Rate: 0.117","Residential Rate: 0.074","Residential Rate: 0.088","Residential Rate: 0.112","Residential Rate: 0.09","Residential Rate: 0.11","Residential Rate: 0.094","Residential Rate: 0.111","Residential Rate: 0.1","Residential Rate: 0.074","Residential Rate: 0.09","Residential Rate: 0.097","Residential Rate: 0.086","Residential Rate: 0.1","Residential Rate: 0.121","Residential Rate: 0.106","Residential Rate: 0.125","Residential Rate: 0.061","Residential Rate: 0.13","Residential Rate: 0.086","Residential Rate: 0.1","Residential Rate: 0.061","Residential Rate: 0.093","Residential Rate: 0.105","Residential Rate: 0.11","Residential Rate: 0.095","Residential Rate: 0.052","Residential Rate: 0.112","Residential Rate: 0.088","Residential Rate: 0.107","Residential Rate: 0.171","Residential Rate: 0.064","Residential Rate: 0.13","Residential Rate: 0.101","Residential Rate: 0.099"],"locations":["AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"],"locationmode":"USA-states","marker":{"line":{"color":"rgba(255,255,255,1)"}},"colors":"Blues","alpha":1,"sizes":[10,100],"type":"choropleth"}},"layout":{"margin":{"b":40,"l":60,"t":25,"r":10},"title":"Average Residential Electricity Rates by State","geo":{"scope":"usa","projection":{"type":"albers usa"},"showlakes":true,"lakecolor":"rgba(255,255,255,1)"},"xaxis":{"domain":[0,1]},"yaxis":{"domain":[0,1]},"hovermode":"closest","showlegend":false,"legend":{"y":0.5,"yanchor":"top"}},"source":"A","config":{"modeBarButtonsToAdd":[{"name":"Collaborate","icon":{"width":1000,"ascent":500,"descent":-50,"path":"M487 375c7-10 9-23 5-36l-79-259c-3-12-11-23-22-31-11-8-22-12-35-12l-263 0c-15 0-29 5-43 15-13 10-23 23-28 37-5 13-5 25-1 37 0 0 0 3 1 7 1 5 1 8 1 11 0 2 0 4-1 6 0 3-1 5-1 6 1 2 2 4 3 6 1 2 2 4 4 6 2 3 4 5 5 7 5 7 9 16 13 26 4 10 7 19 9 26 0 2 0 5 0 9-1 4-1 6 0 8 0 2 2 5 4 8 3 3 5 5 5 7 4 6 8 15 12 26 4 11 7 19 7 26 1 1 0 4 0 9-1 4-1 7 0 8 1 2 3 5 6 8 4 4 6 6 6 7 4 5 8 13 13 24 4 11 7 20 7 28 1 1 0 4 0 7-1 3-1 6-1 7 0 2 1 4 3 6 1 1 3 4 5 6 2 3 3 5 5 6 1 2 3 5 4 9 2 3 3 7 5 10 1 3 2 6 4 10 2 4 4 7 6 9 2 3 4 5 7 7 3 2 7 3 11 3 3 0 8 0 13-1l0-1c7 2 12 2 14 2l218 0c14 0 25-5 32-16 8-10 10-23 6-37l-79-259c-7-22-13-37-20-43-7-7-19-10-37-10l-248 0c-5 0-9-2-11-5-2-3-2-7 0-12 4-13 18-20 41-20l264 0c5 0 10 2 16 5 5 3 8 6 10 11l85 282c2 5 2 10 2 17 7-3 13-7 17-13z m-304 0c-1-3-1-5 0-7 1-1 3-2 6-2l174 0c2 0 4 1 7 2 2 2 4 4 5 7l6 18c0 3 0 5-1 7-1 1-3 2-6 2l-173 0c-3 0-5-1-8-2-2-2-4-4-4-7z m-24-73c-1-3-1-5 0-7 2-2 3-2 6-2l174 0c2 0 5 0 7 2 3 2 4 4 5 7l6 18c1 2 0 5-1 6-1 2-3 3-5 3l-174 0c-3 0-5-1-7-3-3-1-4-4-5-6z"},"click":"function(gd) { \n        // is this being viewed in RStudio?\n        if (location.search == '?viewer_pane=1') {\n          alert('To learn about plotly for collaboration, visit:\\n https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html');\n        } else {\n          window.open('https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html', '_blank');\n        }\n      }"}],"cloud":false},"data":[{"colorbar":{"title":"","ticklen":2,"len":0.5,"y":1,"lenmode":"fraction","yanchor":"top"},"colorscale":[["0","rgba(247,251,255,1)"],["0.0756302521008403","rgba(232,241,250,1)"],["0.184873949579832","rgba(211,227,243,1)"],["0.260504201680672","rgba(195,218,238,1)"],["0.26890756302521","rgba(192,216,237,1)"],["0.285714285714286","rgba(187,214,235,1)"],["0.302521008403361","rgba(181,212,233,1)"],["0.319327731092437","rgba(176,210,231,1)"],["0.34453781512605","rgba(168,206,228,1)"],["0.352941176470588","rgba(165,205,227,1)"],["0.361344537815126","rgba(162,204,227,1)"],["0.394957983193277","rgba(150,197,223,1)"],["0.403361344537815","rgba(147,196,223,1)"],["0.411764705882353","rgba(144,194,222,1)"],["0.453781512605042","rgba(127,184,218,1)"],["0.46218487394958","rgba(123,182,217,1)"],["0.487394957983193","rgba(113,177,215,1)"],["0.495798319327731","rgba(109,175,214,1)"],["0.504201680672269","rgba(106,173,213,1)"],["0.512605042016807","rgba(103,171,212,1)"],["0.546218487394958","rgba(93,164,208,1)"],["0.579831932773109","rgba(82,156,204,1)"],["0.65546218487395","rgba(59,138,194,1)"],["0.680672268907563","rgba(53,131,190,1)"],["1","rgba(8,48,107,1)"]],"showscale":true,"z":[0.084,0.092,0.113,0.135,0.119,0.133,0.083,0.095,0.117,0.113,0.111,0.084,0.094,0.106,0.117,0.074,0.088,0.112,0.09,0.11,0.094,0.111,0.1,0.074,0.09,0.097,0.086,0.1,0.121,0.106,0.125,0.061,0.13,0.086,0.1,0.061,0.093,0.105,0.11,0.095,0.052,0.112,0.088,0.107,0.171,0.064,0.13,0.101,0.099],"text":["Residential Rate: 0.084","Residential Rate: 0.092","Residential Rate: 0.113","Residential Rate: 0.135","Residential Rate: 0.119","Residential Rate: 0.133","Residential Rate: 0.083","Residential Rate: 0.095","Residential Rate: 0.117","Residential Rate: 0.113","Residential Rate: 0.111","Residential Rate: 0.084","Residential Rate: 0.094","Residential Rate: 0.106","Residential Rate: 0.117","Residential Rate: 0.074","Residential Rate: 0.088","Residential Rate: 0.112","Residential Rate: 0.09","Residential Rate: 0.11","Residential Rate: 0.094","Residential Rate: 0.111","Residential Rate: 0.1","Residential Rate: 0.074","Residential Rate: 0.09","Residential Rate: 0.097","Residential Rate: 0.086","Residential Rate: 0.1","Residential Rate: 0.121","Residential Rate: 0.106","Residential Rate: 0.125","Residential Rate: 0.061","Residential Rate: 0.13","Residential Rate: 0.086","Residential Rate: 0.1","Residential Rate: 0.061","Residential Rate: 0.093","Residential Rate: 0.105","Residential Rate: 0.11","Residential Rate: 0.095","Residential Rate: 0.052","Residential Rate: 0.112","Residential Rate: 0.088","Residential Rate: 0.107","Residential Rate: 0.171","Residential Rate: 0.064","Residential Rate: 0.13","Residential Rate: 0.101","Residential Rate: 0.099"],"locations":["AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"],"locationmode":"USA-states","marker":{"line":{"color":"rgba(255,255,255,1)"}},"type":"choropleth","frame":null}],"highlight":{"on":"plotly_click","persistent":false,"dynamic":false,"selectize":false,"opacityDim":0.2,"selected":{"opacity":1}},"base_url":"https://plot.ly"},"evals":["config.modeBarButtonsToAdd.0.click"],"jsHooks":{"render":[{"code":"function(el, x) { var ctConfig = crosstalk.var('plotlyCrosstalkOpts').set({\"on\":\"plotly_click\",\"persistent\":false,\"dynamic\":false,\"selectize\":false,\"opacityDim\":0.2,\"selected\":{\"opacity\":1}}); }","data":null}]}}</script><!--/html_preserve-->

The new graph is much more clear in visualizing how the average residential electricity rates differ by state. Plotting a new cluster plot with the re-queried data provides a better view of how the states are clustered.


```r
state.avg.rates2$state <- as.factor(state.avg.rates2$state)
rownames(state.avg.rates2) <- state.avg.rates2$state
clust2 <- kmeans(state.avg.rates2[,2:4], 6)
clusplot(state.avg.rates2[,2:4], clust2$cluster, color=TRUE, shade=TRUE, labels=2, lines=0)
```

![](utility_rates_files/figure-html/unnamed-chunk-11-1.png)<!-- -->

As suspected from our original inferences, the states with the lowest rates (Oregon, Washington, Tennesse and Nevada) are placed in their own respective cluster. Vermont is set in its own cluster. Most of the states are arranged in clusters five and six, with mostly Northeastern states occupying separate clusters. 

The data includes rate by the type of ownership of a particular utility. Are there any significant differences in rates depending on the type of ownership?

To see the different classifications of ownership, a quick query can be run.


```r
sqldf('SELECT DISTINCT ownership FROM utility_df')
```

```
##               ownership
## 1        Investor Owned
## 2           Cooperative
## 3             Municipal
## 4 Political Subdivision
## 5                 State
## 6 Retail Power Marketer
## 7               Federal
```

The query shows there are seven types of ownership classification. Let's write another query to pull the rates by state and ownership type. 


```r
ownership.rate <- sqldf('SELECT state, ownership, utility_name, 
                         AVG(comm_rate) as comm_rate, AVG(ind_rate) as ind_rate, AVG(res_rate) as res_rate 
                         FROM utility_df 
                         GROUP BY state, ownership, utility_name  
                         ORDER BY state')
```

With the data queried into an R `data.frame`, it can then be melted and reshaped using the [reshape2](https://cran.r-project.org/web/packages/reshape2/reshape2.pdf) and [dplyr](https://cran.r-project.org/web/packages/dplyr/index.html) packages to reshape into the format we need to plot.


```r
ownership.melted <- melt(ownership.rate, id.vars = 'ownership', 
                         measure.vars = c('res_rate', 'comm_rate', 'ind_rate'), variable.name = 'rate')

ownership.rates2 <- dcast(ownership.melted, formula = ownership ~ rate, fun.aggregate = mean)
ownership.rates2 <- ownership.rates2[order(-ownership.rates2$res_rate),]

p <- plot_ly(ownership.rates2, x=ownership.rates2$ownership, y=round(ownership.rates2$res_rate, 3), type='bar') %>%
  layout(title = 'Average Residential Electricity Rates by Utility Ownership', yaxis = list(title = 'Electricity Rate'))

p
```

<!--html_preserve--><div id="153c83d3aa6" style="width:672px;height:480px;" class="plotly html-widget"></div>
<script type="application/json" data-for="153c83d3aa6">{"x":{"visdat":{"153c20283a72":["function () ","plotlyVisDat"]},"cur_data":"153c20283a72","attrs":{"153c20283a72":{"x":["Investor Owned","Retail Power Marketer","Cooperative","Municipal","State","Political Subdivision","Federal"],"y":[0.128,0.124,0.119,0.117,0.115,0.11,0.028],"alpha":1,"sizes":[10,100],"type":"bar"}},"layout":{"margin":{"b":40,"l":60,"t":25,"r":10},"title":"Average Residential Electricity Rates by Utility Ownership","yaxis":{"domain":[0,1],"title":"Electricity Rate"},"xaxis":{"domain":[0,1],"type":"category","categoryorder":"array","categoryarray":["Cooperative","Federal","Investor Owned","Municipal","Political Subdivision","Retail Power Marketer","State"]},"hovermode":"closest","showlegend":false},"source":"A","config":{"modeBarButtonsToAdd":[{"name":"Collaborate","icon":{"width":1000,"ascent":500,"descent":-50,"path":"M487 375c7-10 9-23 5-36l-79-259c-3-12-11-23-22-31-11-8-22-12-35-12l-263 0c-15 0-29 5-43 15-13 10-23 23-28 37-5 13-5 25-1 37 0 0 0 3 1 7 1 5 1 8 1 11 0 2 0 4-1 6 0 3-1 5-1 6 1 2 2 4 3 6 1 2 2 4 4 6 2 3 4 5 5 7 5 7 9 16 13 26 4 10 7 19 9 26 0 2 0 5 0 9-1 4-1 6 0 8 0 2 2 5 4 8 3 3 5 5 5 7 4 6 8 15 12 26 4 11 7 19 7 26 1 1 0 4 0 9-1 4-1 7 0 8 1 2 3 5 6 8 4 4 6 6 6 7 4 5 8 13 13 24 4 11 7 20 7 28 1 1 0 4 0 7-1 3-1 6-1 7 0 2 1 4 3 6 1 1 3 4 5 6 2 3 3 5 5 6 1 2 3 5 4 9 2 3 3 7 5 10 1 3 2 6 4 10 2 4 4 7 6 9 2 3 4 5 7 7 3 2 7 3 11 3 3 0 8 0 13-1l0-1c7 2 12 2 14 2l218 0c14 0 25-5 32-16 8-10 10-23 6-37l-79-259c-7-22-13-37-20-43-7-7-19-10-37-10l-248 0c-5 0-9-2-11-5-2-3-2-7 0-12 4-13 18-20 41-20l264 0c5 0 10 2 16 5 5 3 8 6 10 11l85 282c2 5 2 10 2 17 7-3 13-7 17-13z m-304 0c-1-3-1-5 0-7 1-1 3-2 6-2l174 0c2 0 4 1 7 2 2 2 4 4 5 7l6 18c0 3 0 5-1 7-1 1-3 2-6 2l-173 0c-3 0-5-1-8-2-2-2-4-4-4-7z m-24-73c-1-3-1-5 0-7 2-2 3-2 6-2l174 0c2 0 5 0 7 2 3 2 4 4 5 7l6 18c1 2 0 5-1 6-1 2-3 3-5 3l-174 0c-3 0-5-1-7-3-3-1-4-4-5-6z"},"click":"function(gd) { \n        // is this being viewed in RStudio?\n        if (location.search == '?viewer_pane=1') {\n          alert('To learn about plotly for collaboration, visit:\\n https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html');\n        } else {\n          window.open('https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html', '_blank');\n        }\n      }"}],"cloud":false},"data":[{"x":["Investor Owned","Retail Power Marketer","Cooperative","Municipal","State","Political Subdivision","Federal"],"y":[0.128,0.124,0.119,0.117,0.115,0.11,0.028],"type":"bar","marker":{"fillcolor":"rgba(31,119,180,1)","color":"rgba(31,119,180,1)","line":{"color":"transparent"}},"xaxis":"x","yaxis":"y","frame":null}],"highlight":{"on":"plotly_click","persistent":false,"dynamic":false,"selectize":false,"opacityDim":0.2,"selected":{"opacity":1}},"base_url":"https://plot.ly"},"evals":["config.modeBarButtonsToAdd.0.click"],"jsHooks":{"render":[{"code":"function(el, x) { var ctConfig = crosstalk.var('plotlyCrosstalkOpts').set({\"on\":\"plotly_click\",\"persistent\":false,\"dynamic\":false,\"selectize\":false,\"opacityDim\":0.2,\"selected\":{\"opacity\":1}}); }","data":null}]}}</script><!--/html_preserve-->

The plot shows most ownership classifications are similar regarding average residential electricity rates. Federal rates are by far the lowest, which could be due to these rates representing low-income housing or other federally sponsored housing projects.

To see if there are any significant differences between the residential rates of the ownership classifications, we can run a [Kruskal-Wallis post-hoc test](http://www.aaronschlegel.com/notebook/post-hoc-tests-kruskal-wallis/) using the [agricolae](https://cran.r-project.org/web/packages/agricolae/index.html) package.


```r
ownership.res <- filter(ownership.melted, rate == 'res_rate') # First filter all rate types except for Residential
kruskal(ownership.res$value, ownership.res$ownership, console = TRUE)
```

```
## 
## Study: ownership.res$value ~ ownership.res$ownership
## Kruskal-Wallis test's
## Ties or no Ties
## 
## Critical Value: 83.92807
## Degrees of freedom: 6
## Pvalue Chisq  : 5.551115e-16 
## 
## ownership.res$ownership,  means of the ranks
## 
##                       ownership.res.value   r
## Cooperative                      939.7176 857
## Federal                          217.2857   7
## Investor Owned                   724.7676 185
## Municipal                        814.1767 566
## Political Subdivision            565.5976  82
## Retail Power Marketer           1284.5000   2
## State                            765.4286   7
## 
## Post Hoc Analysis
## 
## t-Student: 1.961361
## Alpha    : 0.05
## Groups according to probability of treatment differences and alpha level.
## 
## Treatments with the same letter are not significantly different.
## 
##                       ownership.res$value groups
## Retail Power Marketer           1284.5000      a
## Cooperative                      939.7176      a
## Municipal                        814.1767      a
## State                            765.4286     ab
## Investor Owned                   724.7676     ab
## Political Subdivision            565.5976     bc
## Federal                          217.2857      c
```

The Kruskal-Wallis test output corresponds to the quick inferences made above on the graph. Utilities owned by Retail Power Marketers, Cooperatives and Municipalities are not significantly different from each other. State and Investor Owned utilities are not significantly distinct from the former three types and Political Subdivisions. Federally owned services are significantly different than each other ownership classification, as was expected.

## Further Exploration of the Data

Suppose one is interested in finding the utilities with the highest residential electricity rates. We can write a query to pull this data from the database and plot. The query returns the top 20 utilities to preserve readability as specified with the `LIMIT` clause. 


```r
utilities <- sqldf('SELECT utility_name, state, res_rate 
                    FROM utility_df 
                    GROUP BY utility_name, state 
                    ORDER BY res_rate DESC 
                    LIMIT 20')

p <- plot_ly(utilities, x=utilities$utility_name, y=round(utilities$res_rate, 3), type='bar', group = utilities$state) %>%
  layout(title = 'Highest Residential Rates by Utility', yaxis = list(title = 'Electricity Rate'))
```

```
## Warning in plot_ly(utilities, x = utilities$utility_name, y = round(utilities$res_rate, : The group argument has been deprecated. Use `group_by()` or split instead.
## See `help('plotly_data')` for examples
```

```r
p
```

<!--html_preserve--><div id="153c57d4491f" style="width:672px;height:480px;" class="plotly html-widget"></div>
<script type="application/json" data-for="153c57d4491f">{"x":{"visdat":{"153cc982e88":["function () ","plotlyVisDat"]},"cur_data":"153cc982e88","attrs":{"153cc982e88":{"x":["Matinicus Plantation Elec Co","Middle Kuskokwim Elec Coop Inc","Napakiak Ircinraq Power Co","Ipnatchiaq Electric Company","Nelson Lagoon Elec Coop Inc","Tuntutuliak Comm Services Assn","City of White Mountain","Hughes Power & Light Co","City of Atka","G & K Inc","Kwig Power Company","Inside Passage Elec Coop Inc","City of Chefornak","I-N-N Electric Coop Inc","Block Island Power Co","Alaska Village Elec Coop Inc","Tanana Power Co Inc","Kuiggluum Kallugvia","City of Saint Paul","Bethel Utilities Corp"],"y":[0.98,0.852,0.85,0.804,0.764,0.75,0.721,0.712,0.706,0.681,0.648,0.626,0.619,0.572,0.571,0.569,0.545,0.521,0.519,0.519],"alpha":1,"sizes":[10,100],"type":"bar"}},"layout":{"margin":{"b":40,"l":60,"t":25,"r":10},"title":"Highest Residential Rates by Utility","yaxis":{"domain":[0,1],"title":"Electricity Rate"},"xaxis":{"domain":[0,1],"type":"category","categoryorder":"array","categoryarray":["Alaska Village Elec Coop Inc","Bethel Utilities Corp","Block Island Power Co","City of Atka","City of Chefornak","City of Saint Paul","City of White Mountain","G & K Inc","Hughes Power & Light Co","I-N-N Electric Coop Inc","Inside Passage Elec Coop Inc","Ipnatchiaq Electric Company","Kuiggluum Kallugvia","Kwig Power Company","Matinicus Plantation Elec Co","Middle Kuskokwim Elec Coop Inc","Napakiak Ircinraq Power Co","Nelson Lagoon Elec Coop Inc","Tanana Power Co Inc","Tuntutuliak Comm Services Assn"]},"hovermode":"closest","showlegend":false},"source":"A","config":{"modeBarButtonsToAdd":[{"name":"Collaborate","icon":{"width":1000,"ascent":500,"descent":-50,"path":"M487 375c7-10 9-23 5-36l-79-259c-3-12-11-23-22-31-11-8-22-12-35-12l-263 0c-15 0-29 5-43 15-13 10-23 23-28 37-5 13-5 25-1 37 0 0 0 3 1 7 1 5 1 8 1 11 0 2 0 4-1 6 0 3-1 5-1 6 1 2 2 4 3 6 1 2 2 4 4 6 2 3 4 5 5 7 5 7 9 16 13 26 4 10 7 19 9 26 0 2 0 5 0 9-1 4-1 6 0 8 0 2 2 5 4 8 3 3 5 5 5 7 4 6 8 15 12 26 4 11 7 19 7 26 1 1 0 4 0 9-1 4-1 7 0 8 1 2 3 5 6 8 4 4 6 6 6 7 4 5 8 13 13 24 4 11 7 20 7 28 1 1 0 4 0 7-1 3-1 6-1 7 0 2 1 4 3 6 1 1 3 4 5 6 2 3 3 5 5 6 1 2 3 5 4 9 2 3 3 7 5 10 1 3 2 6 4 10 2 4 4 7 6 9 2 3 4 5 7 7 3 2 7 3 11 3 3 0 8 0 13-1l0-1c7 2 12 2 14 2l218 0c14 0 25-5 32-16 8-10 10-23 6-37l-79-259c-7-22-13-37-20-43-7-7-19-10-37-10l-248 0c-5 0-9-2-11-5-2-3-2-7 0-12 4-13 18-20 41-20l264 0c5 0 10 2 16 5 5 3 8 6 10 11l85 282c2 5 2 10 2 17 7-3 13-7 17-13z m-304 0c-1-3-1-5 0-7 1-1 3-2 6-2l174 0c2 0 4 1 7 2 2 2 4 4 5 7l6 18c0 3 0 5-1 7-1 1-3 2-6 2l-173 0c-3 0-5-1-8-2-2-2-4-4-4-7z m-24-73c-1-3-1-5 0-7 2-2 3-2 6-2l174 0c2 0 5 0 7 2 3 2 4 4 5 7l6 18c1 2 0 5-1 6-1 2-3 3-5 3l-174 0c-3 0-5-1-7-3-3-1-4-4-5-6z"},"click":"function(gd) { \n        // is this being viewed in RStudio?\n        if (location.search == '?viewer_pane=1') {\n          alert('To learn about plotly for collaboration, visit:\\n https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html');\n        } else {\n          window.open('https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html', '_blank');\n        }\n      }"}],"cloud":false},"data":[{"x":["Matinicus Plantation Elec Co","Middle Kuskokwim Elec Coop Inc","Napakiak Ircinraq Power Co","Ipnatchiaq Electric Company","Nelson Lagoon Elec Coop Inc","Tuntutuliak Comm Services Assn","City of White Mountain","Hughes Power & Light Co","City of Atka","G & K Inc","Kwig Power Company","Inside Passage Elec Coop Inc","City of Chefornak","I-N-N Electric Coop Inc","Block Island Power Co","Alaska Village Elec Coop Inc","Tanana Power Co Inc","Kuiggluum Kallugvia","City of Saint Paul","Bethel Utilities Corp"],"y":[0.98,0.852,0.85,0.804,0.764,0.75,0.721,0.712,0.706,0.681,0.648,0.626,0.619,0.572,0.571,0.569,0.545,0.521,0.519,0.519],"type":"bar","marker":{"fillcolor":"rgba(31,119,180,1)","color":"rgba(31,119,180,1)","line":{"color":"transparent"}},"xaxis":"x","yaxis":"y","frame":null}],"highlight":{"on":"plotly_click","persistent":false,"dynamic":false,"selectize":false,"opacityDim":0.2,"selected":{"opacity":1}},"base_url":"https://plot.ly"},"evals":["config.modeBarButtonsToAdd.0.click"],"jsHooks":{"render":[{"code":"function(el, x) { var ctConfig = crosstalk.var('plotlyCrosstalkOpts').set({\"on\":\"plotly_click\",\"persistent\":false,\"dynamic\":false,\"selectize\":false,\"opacityDim\":0.2,\"selected\":{\"opacity\":1}}); }","data":null}]}}</script><!--/html_preserve-->

Interestingly, 18 of the 20 utilities queried are in Alaska.

Which states have the most utilities? Intuition would say larger states such as Texas and California would have the most utilities.


```r
owned <- sqldf('SELECT state, COUNT(DISTINCT utility_name) as utilities 
                FROM utility_df 
                GROUP BY state 
                ORDER BY utilities DESC 
                LIMIT 10')

p <- plot_ly(owned, x=owned$state, y=owned$utilities, type='bar') %>%
  layout(title = 'States with the Most Utilities', yaxis = list(title = 'Count of Utilities'))

p
```

<!--html_preserve--><div id="153c4e55b9b" style="width:672px;height:480px;" class="plotly html-widget"></div>
<script type="application/json" data-for="153c4e55b9b">{"x":{"visdat":{"153c11cb63e0":["function () ","plotlyVisDat"]},"cur_data":"153c11cb63e0","attrs":{"153c11cb63e0":{"x":["TX","IA","TN","NC","IN","GA","MN","MO","WI","OH"],"y":[84,69,69,66,64,62,61,56,56,54],"alpha":1,"sizes":[10,100],"type":"bar"}},"layout":{"margin":{"b":40,"l":60,"t":25,"r":10},"title":"States with the Most Utilities","yaxis":{"domain":[0,1],"title":"Count of Utilities"},"xaxis":{"domain":[0,1],"type":"category","categoryorder":"array","categoryarray":["GA","IA","IN","MN","MO","NC","OH","TN","TX","WI"]},"hovermode":"closest","showlegend":false},"source":"A","config":{"modeBarButtonsToAdd":[{"name":"Collaborate","icon":{"width":1000,"ascent":500,"descent":-50,"path":"M487 375c7-10 9-23 5-36l-79-259c-3-12-11-23-22-31-11-8-22-12-35-12l-263 0c-15 0-29 5-43 15-13 10-23 23-28 37-5 13-5 25-1 37 0 0 0 3 1 7 1 5 1 8 1 11 0 2 0 4-1 6 0 3-1 5-1 6 1 2 2 4 3 6 1 2 2 4 4 6 2 3 4 5 5 7 5 7 9 16 13 26 4 10 7 19 9 26 0 2 0 5 0 9-1 4-1 6 0 8 0 2 2 5 4 8 3 3 5 5 5 7 4 6 8 15 12 26 4 11 7 19 7 26 1 1 0 4 0 9-1 4-1 7 0 8 1 2 3 5 6 8 4 4 6 6 6 7 4 5 8 13 13 24 4 11 7 20 7 28 1 1 0 4 0 7-1 3-1 6-1 7 0 2 1 4 3 6 1 1 3 4 5 6 2 3 3 5 5 6 1 2 3 5 4 9 2 3 3 7 5 10 1 3 2 6 4 10 2 4 4 7 6 9 2 3 4 5 7 7 3 2 7 3 11 3 3 0 8 0 13-1l0-1c7 2 12 2 14 2l218 0c14 0 25-5 32-16 8-10 10-23 6-37l-79-259c-7-22-13-37-20-43-7-7-19-10-37-10l-248 0c-5 0-9-2-11-5-2-3-2-7 0-12 4-13 18-20 41-20l264 0c5 0 10 2 16 5 5 3 8 6 10 11l85 282c2 5 2 10 2 17 7-3 13-7 17-13z m-304 0c-1-3-1-5 0-7 1-1 3-2 6-2l174 0c2 0 4 1 7 2 2 2 4 4 5 7l6 18c0 3 0 5-1 7-1 1-3 2-6 2l-173 0c-3 0-5-1-8-2-2-2-4-4-4-7z m-24-73c-1-3-1-5 0-7 2-2 3-2 6-2l174 0c2 0 5 0 7 2 3 2 4 4 5 7l6 18c1 2 0 5-1 6-1 2-3 3-5 3l-174 0c-3 0-5-1-7-3-3-1-4-4-5-6z"},"click":"function(gd) { \n        // is this being viewed in RStudio?\n        if (location.search == '?viewer_pane=1') {\n          alert('To learn about plotly for collaboration, visit:\\n https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html');\n        } else {\n          window.open('https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html', '_blank');\n        }\n      }"}],"cloud":false},"data":[{"x":["TX","IA","TN","NC","IN","GA","MN","MO","WI","OH"],"y":[84,69,69,66,64,62,61,56,56,54],"type":"bar","marker":{"fillcolor":"rgba(31,119,180,1)","color":"rgba(31,119,180,1)","line":{"color":"transparent"}},"xaxis":"x","yaxis":"y","frame":null}],"highlight":{"on":"plotly_click","persistent":false,"dynamic":false,"selectize":false,"opacityDim":0.2,"selected":{"opacity":1}},"base_url":"https://plot.ly"},"evals":["config.modeBarButtonsToAdd.0.click"],"jsHooks":{"render":[{"code":"function(el, x) { var ctConfig = crosstalk.var('plotlyCrosstalkOpts').set({\"on\":\"plotly_click\",\"persistent\":false,\"dynamic\":false,\"selectize\":false,\"opacityDim\":0.2,\"selected\":{\"opacity\":1}}); }","data":null}]}}</script><!--/html_preserve-->

Contrary to our intuition, several states with smaller areas such as Georgia, Iowa and Tennesse are those with the most utilities.

Of those states in the above chart, are there significant differences in the ownership classification of the utilities?


```r
owned.type <- sqldf('SELECT state, ownership, COUNT(DISTINCT utility_name) as utilities 
                FROM utility_df 
                WHERE state IN ("TX", "IA", "TN", "NC", "IN", "GA", "MN", "MO", "WI", "OH")
                GROUP BY state, ownership 
                ORDER BY utilities DESC')

ggplot(owned.type, aes(state, utilities)) + 
  geom_bar(aes(fill=ownership), position='dodge', stat='identity') + 
  labs(title = 'Utilities by Ownership Type', ylab = 'Count of Utilities')
```

![](utility_rates_files/figure-html/unnamed-chunk-18-1.png)<!-- -->

Cooperative and municipal-owned utilities are the most common type of ownership in the states considered. To see the proportions of the different types of ownership, the following query can be used. The query includes all states as we are curious to see if cooperative and municipal-owned utilities are indeed representative of the majority of ownership types.


```r
utility.type <- sqldf('SELECT ownership, COUNT(DISTINCT utility_name) as count
                       FROM utility_df 
                       GROUP BY ownership 
                       ORDER BY count DESC')

utility.type$percent <- utility.type$count / sum(utility.type$count) * 100 # Create ratio to find proportions of ownership classifications

p <- plot_ly(utility.type, x=utility.type$ownership, y=round(utility.type$percent, 2), type='bar') %>% 
  layout(title = 'Proportion of Utilities by Ownership Classification', yaxis = list(title = '% of Total Utilities'))

p
```

<!--html_preserve--><div id="153c1ef66673" style="width:672px;height:480px;" class="plotly html-widget"></div>
<script type="application/json" data-for="153c1ef66673">{"x":{"visdat":{"153c3cb57b7d":["function () ","plotlyVisDat"]},"cur_data":"153c3cb57b7d","attrs":{"153c3cb57b7d":{"x":["Cooperative","Municipal","Investor Owned","Political Subdivision","State","Federal","Retail Power Marketer"],"y":[49.59,35.5,9.16,5.12,0.32,0.19,0.13],"alpha":1,"sizes":[10,100],"type":"bar"}},"layout":{"margin":{"b":40,"l":60,"t":25,"r":10},"title":"Proportion of Utilities by Ownership Classification","yaxis":{"domain":[0,1],"title":"% of Total Utilities"},"xaxis":{"domain":[0,1],"type":"category","categoryorder":"array","categoryarray":["Cooperative","Federal","Investor Owned","Municipal","Political Subdivision","Retail Power Marketer","State"]},"hovermode":"closest","showlegend":false},"source":"A","config":{"modeBarButtonsToAdd":[{"name":"Collaborate","icon":{"width":1000,"ascent":500,"descent":-50,"path":"M487 375c7-10 9-23 5-36l-79-259c-3-12-11-23-22-31-11-8-22-12-35-12l-263 0c-15 0-29 5-43 15-13 10-23 23-28 37-5 13-5 25-1 37 0 0 0 3 1 7 1 5 1 8 1 11 0 2 0 4-1 6 0 3-1 5-1 6 1 2 2 4 3 6 1 2 2 4 4 6 2 3 4 5 5 7 5 7 9 16 13 26 4 10 7 19 9 26 0 2 0 5 0 9-1 4-1 6 0 8 0 2 2 5 4 8 3 3 5 5 5 7 4 6 8 15 12 26 4 11 7 19 7 26 1 1 0 4 0 9-1 4-1 7 0 8 1 2 3 5 6 8 4 4 6 6 6 7 4 5 8 13 13 24 4 11 7 20 7 28 1 1 0 4 0 7-1 3-1 6-1 7 0 2 1 4 3 6 1 1 3 4 5 6 2 3 3 5 5 6 1 2 3 5 4 9 2 3 3 7 5 10 1 3 2 6 4 10 2 4 4 7 6 9 2 3 4 5 7 7 3 2 7 3 11 3 3 0 8 0 13-1l0-1c7 2 12 2 14 2l218 0c14 0 25-5 32-16 8-10 10-23 6-37l-79-259c-7-22-13-37-20-43-7-7-19-10-37-10l-248 0c-5 0-9-2-11-5-2-3-2-7 0-12 4-13 18-20 41-20l264 0c5 0 10 2 16 5 5 3 8 6 10 11l85 282c2 5 2 10 2 17 7-3 13-7 17-13z m-304 0c-1-3-1-5 0-7 1-1 3-2 6-2l174 0c2 0 4 1 7 2 2 2 4 4 5 7l6 18c0 3 0 5-1 7-1 1-3 2-6 2l-173 0c-3 0-5-1-8-2-2-2-4-4-4-7z m-24-73c-1-3-1-5 0-7 2-2 3-2 6-2l174 0c2 0 5 0 7 2 3 2 4 4 5 7l6 18c1 2 0 5-1 6-1 2-3 3-5 3l-174 0c-3 0-5-1-7-3-3-1-4-4-5-6z"},"click":"function(gd) { \n        // is this being viewed in RStudio?\n        if (location.search == '?viewer_pane=1') {\n          alert('To learn about plotly for collaboration, visit:\\n https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html');\n        } else {\n          window.open('https://cpsievert.github.io/plotly_book/plot-ly-for-collaboration.html', '_blank');\n        }\n      }"}],"cloud":false},"data":[{"x":["Cooperative","Municipal","Investor Owned","Political Subdivision","State","Federal","Retail Power Marketer"],"y":[49.59,35.5,9.16,5.12,0.32,0.19,0.13],"type":"bar","marker":{"fillcolor":"rgba(31,119,180,1)","color":"rgba(31,119,180,1)","line":{"color":"transparent"}},"xaxis":"x","yaxis":"y","frame":null}],"highlight":{"on":"plotly_click","persistent":false,"dynamic":false,"selectize":false,"opacityDim":0.2,"selected":{"opacity":1}},"base_url":"https://plot.ly"},"evals":["config.modeBarButtonsToAdd.0.click"],"jsHooks":{"render":[{"code":"function(el, x) { var ctConfig = crosstalk.var('plotlyCrosstalkOpts').set({\"on\":\"plotly_click\",\"persistent\":false,\"dynamic\":false,\"selectize\":false,\"opacityDim\":0.2,\"selected\":{\"opacity\":1}}); }","data":null}]}}</script><!--/html_preserve-->

As one might anticipate from the previous graph, cooperative and municipal-owned utilities roughly 85% of all utilities in the United States as recorded by the dataset.

## Summary

SQL and R make a great combination when exploring and analyzing datasets using the [sqldf package](https://cran.r-project.org/web/packages/sqldf/) package and other packages available in R. Although the dataset examined in this post was only about 5mb and therefore doesn't need to be loaded into a database for analysis, it provides a good starting point for working with SQL and R in unison. I hope to do more posts shortly using SQL and R on larger datasets.
