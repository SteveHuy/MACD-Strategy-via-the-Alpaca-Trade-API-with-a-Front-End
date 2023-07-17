# Trading Bot using MACD Strategy via Alpaca Trade API
This is a trading bot using the Alpaca Trade API which uses the MACD Strategy.
The MACD line is (12 - day EMA - 26 day EMA) and the signall line is the 9 day EMA of the MACD line.
The program can determine long and short signals in the chosen stocks. The code contains a dynamic backtesting tool which will pick a take-profit margin and stop-loss based on the winrate and money earned of the previous 5 years of market conditions. However, currently the code only makes Long Orders as shorting is a riskier strategy which requires more back testing.

The react front end can interact with the backend via flask to add and remove stocks, produce graphs, obtain the statisics of the strategy of the selected stocks and execute the program to make long orders via the Alpaca Trade API

Example of the program
https://youtu.be/a18QCHc3Wos
