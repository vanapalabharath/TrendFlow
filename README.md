# EMA/DMA Crossover Indicator

## Overview

This script analyzes stock data using the Upstox API to identify crossover events between the 50-day and 200-day Exponential Moving Averages (EMAs) or Simple Moving Averages (DMAs). Crossovers can serve as potential buy or sell signals, making this tool valuable for traders and investors employing technical analysis.

## Upstox API 

- **Historical Candle Data**: [Get Historical Candle Data](https://upstox.com/developer/api-documentation/get-historical-candle-data)
- **Instrument Keys**: [Instrument Keys](https://upstox.com/developer/api-documentation/instruments/)

## Symbol Mapping

The symbol and instrument keys mapping is available in `symbols.json`. Ensure this file contains the correct stock symbols and their corresponding instrument keys.

## Usage

- **python [dma.py/ema.py] [symbol]**
- [symbol]: (optional) Specify a stock symbol for analysis, or leave it blank to process all symbols in symbols.json.

