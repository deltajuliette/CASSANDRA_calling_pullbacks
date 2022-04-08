# CASSANDRA
The *Cassandra* dilemma occurs when valid warnings or concerns are dismissed or not believed. The term originates in Greek mythology. Cassandra was a daughter of Priam, the King of Troy. Struck by her beauty, Apollo provided her with the gift of prophecy, but when Cassandra refused Apollo's romantic advances, he placed a curse ensuring that nobody would believe her warnings. Cassandra was left with the knowledge of future events, but could neither alter these events nor convince others of the validity of her predictions.

---

## Problem Statement
Timing is absolutely key in financial markets. The ability to predict market peaks (both near-term and long-term) can help protect investors from significant drawdowns and elevated volatility. Of course, most of us do not have the luck of being endowed with such prophetic abilities. However, we may be able to leverage on the advances made in machine learning to create a more advanced barometer of risk (especially for US equity markets) to help investors navigate through the noise.

We define a *pullback* as whether the S&P 500 index will be lower in a month's time (i.e. rolling 4 weeks). The model we are looking to build should be able to do the following:
* Predict the likelihood that the S&P 500 index will fall over the coming month
* Explain which variables matter and how they interact

---

## Organisation of codebooks
1. Data collection, EDA, Feature Engineering
2. Pre-processing, model tuning and conclusions

## Data collection
The bulk of our data has been sourced from Bloomberg via its API on excel. We will write a loop to pull every sheet and store in a dictionary for future use / manipulation. As with any model / algorithm, selecting which variables to include is one of the most important aspects of the workflow. I would like to think that my experience in financial markets should count for something here.

### Constructing our model
Fundamentals are definitely a key driver of equity market returns, especially over longer-term horizons, but near-term changes in flows, technicals, as well as sentiment also have an important role to play in near-term price action. With investors fluctuating between *Greed* and *Fear*, this often causes equity markets to overshoot. The data we've pulled can be broadly classified into the following categories:

![data_collection](https://user-images.githubusercontent.com/66930921/162497459-2b896584-1bfd-4ec6-a9df-9d8d26d05f9c.PNG)

### Data dictionary
![data_dict](https://user-images.githubusercontent.com/66930921/162497654-cd8db4d1-241d-47dc-a2b3-f8ce60dc1d2e.PNG)

We will train the model from the period of 2005-2018 and use 2019-2021 as our testing set.

## Summary of findings
**Initial results**

![compare_models](https://user-images.githubusercontent.com/66930921/162498035-9d22199e-668e-420c-8336-b715a29fe9b0.PNG)

We'll go with *lightgbm* given the reasonably high accuracy + precision. It is also way faster.

Light GBM grows tree vertically while other algorithm grows trees horizontally meaning that Light GBM grows tree leaf-wise while other algorithm grows level-wise. It will choose the leaf with max delta loss to grow. When growing the same leaf, Leaf-wise algorithm can reduce more loss than a level-wise algorithm.

Light GBM is prefixed as ‘Light’ because of its high speed. Light GBM can handle the large size of data and takes lower memory to run. Another reason of why Light GBM is popular is because it focuses on accuracy of results. Our dataset may be considered small here though!

**Confusion matrix - Training set**

![confusion_matrix_train](https://user-images.githubusercontent.com/66930921/162498110-b777cd38-3b74-4e89-a997-c9fa3678e1db.PNG)

**Confusion matrix - Test set**

![confusion_matrix_holdout](https://user-images.githubusercontent.com/66930921/162498169-98d8be9b-3736-408e-aebd-16508450a498.PNG)

There is definitely some overfit here, but that's the best we can do for now...

![roc_auc](https://user-images.githubusercontent.com/66930921/162498219-895e784a-1d79-4969-98a4-5673c44e15d7.PNG)

## Explaining CASSANDRA
SHAP values highlight the value to which a feature has contributed to the model’s prediction; It makes correlations transparent. Interpretability of a model is of utmost importance in finance; Keep it simple!

Our focus is on the top features: Industrial metals + gold 13-week % change, MOVE / SKEW indices, earnings revision indices, and commodities.

![shap_summary](https://user-images.githubusercontent.com/66930921/162498376-6266da70-fab8-431c-ae82-e5bc91036f90.PNG)

### Current readings
The latest readings suggest the risk of a market decline is now at around 40% (Rising slightly in recent weeks). The big criticism here is that CASSANDRA did not manage to predict the broad risk-off moves across markets, spurred by Russia's invasion of Ukraine.

The readings prior to the invasion were fairly mixed....

![image](https://user-images.githubusercontent.com/66930921/162498710-2abc83a8-3042-45b5-8878-d717b112322e.png)

### Quant insights
**Don't shrug off fundamentals**: Earnings revision (eri) and economic surprise indices (cesiusd); US economic data has been surprising to the upside… but that has raised fears of a more hawkish Fed… An earnings revision ratio below 0 - typically increases the likelihood of a decline in equities

**Watch the Fed**: Given the flood of liquidity on the back of QE over the past decade, whatever the Fed decides to do over the coming months is key; Higher rates = Lower multiples = Tighter liquidity.

**Pay attention to the SKEW**: The SKEW index is often overlooked by most people (myself included). It is a measure of perceived tail risk in the S&P 500 based on deep OTM options. Unlike other sentiment indicators, the direction of travel does not appear to be contrarian.

Whenever the cost of tail-risk protection rises, CASSANDRA believes there is an increased likelihood of a drawdown in equity markets

**Commodities and Reflation**: They’re known to be important drivers of equity markets contemptuously. A fall in the price of industrial metals increases the likelihood of a drawdown in equity markets whereas the safe-haven properties of gold are illustrated below.

## Further improvements to consider
I've had a lot of fun dipping into the data and playing around with the models I've learnt in class. While CASSANDRA will likely not work in an almost-efficient market, this was a great learning experience.

* Benoit Mandlebrot's fractal market hypothesis (Fractal Dimensions) could be incorporated here (maybe in smaller timeframes).
* A generic risk-on-risk-off indicator could be developed in conjunction with CASSANDRA via PCA decomposition; If PC1 exceeds 50% and past x-day returns have been negative, we can safely assume the risk-off regime could continue for a while longer
* More analysis around technical oscillators
* A more timely geopolitcial uncertainty proxy could be introduced here (maybe mining text sentiment from key financial agencies)

