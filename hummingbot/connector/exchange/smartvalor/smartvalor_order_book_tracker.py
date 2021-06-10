ach Exchange class contains an OrderBookTracker to maintain a real-time order book of one/multiple trading pairs and is responsible for applying the order book snapshots and diff messages to the corresponding OrderBook.

An OrderBookTracker contains a Dictionary of OrderBook for each trading pair it is maintaining.
APIOrderBookTrackerDataSource class contains either API requests or WebSocket feeds to pull order book data from the exchange.
The OrderBook class contains methods which convert raw order book snapshots/diff messages from exchanges into usable dictionaries of active bids and asks.
