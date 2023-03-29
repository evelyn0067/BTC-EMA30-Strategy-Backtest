# BTC-EMA30-Strategy-Backtest
This repository contains a backtest of an Exponential Moving Average (EMA) trading strategy, which is designed to generate buy and sell signals based on the crossover of two EMAs.

## Strategy
The EMA trading strategy is a trend-following strategy that uses EMAs to generate buy and sell signals. The strategy is based on the crossover of a EMA and closed price.

When the close prcie crosses above the EMA, it generates a buy signal, indicating that the market is in an uptrend. When the EMA crosses below the close price, it generates a sell signal, indicating that the market is in a downtrend.

The EMA trading strategy is a simple yet effective strategy that can be used in a variety of markets and timeframes.

## Backtest
This backtest uses historical price data to simulate the performance of the EMA trading strategy over a specified period of time.

The backtest involves calculating the values of EMA based on the historical price data. The buy and sell signals are generated based on the crossover.

The performance of the strategy is evaluated based on various metrics, including total return, annualized return, Sharpe ratio, maximum drawdown, and win rate.

## Usage
View the results of the backtest in the results folder, which contains a summary of the performance metrics and a plot of the equity curve.
