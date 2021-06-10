//his class is responsible for generating the appropriate authentication headers for the restricted REST endpoints to be used by the Exchange and UserStreamTracker class. Generally, this would mean that constructing the appropriate HTTP headers and authentication payload(as specified by the exchange's API documentation)

Some arguments tend to include:

  HTTP Request Type
Endpoint URL
Mandatory parameters to pass on to the exchange (e.g. API key, secret, passphrase, request body)
Depending on the specific exchange, different information may be needed for authentication. Typically, the Auth class will:

Generate a timestamp/nonce.
Generate a signature based on the time, access method, endpoint, provided parameters, and private key of the user.
Compile the public key, timestamp, provided parameters, and signature into a dictionary to be passed via an http or ws request.
