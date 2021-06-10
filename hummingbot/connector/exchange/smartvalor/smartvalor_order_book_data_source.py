The OrderBookTrackerDataSource class is responsible for order book data retrieval. It simply collects, parses and queues the data stream to be processed by OrderBookTracker. Generally, this would mean pulling data from the exchange's API/WebSocket servers.

To maintain a consistent and up-to-date order book, it is necessary to track the timestamp/nonce of each message received from the exchange API servers. Depending on the exchange responses, we can maintain an order book in the following ways:

Presence of Timestamp/Nonce
In this ideal scenario, we will only 'apply' delta messages onto the order book if and only if the timestamp/nonce of the message received is above or +1 of _last_diff_uid in the order book.
Absence of Timestamp/Nonce
In this scenario, we would have to assign a timestamp to every message received from the exchange and similarly apply the delta messages sequentially only if it is received after the snapshot message and greater than the _last_diff_uid.
