# Counter-API

This repository contains a simple HTTP API server application written in Python that wraps a counter and exposes three
operations:

## API Endpoints

- GET '/get' - returns the current counter value, 0 by default.
- POST '/increase' - adds 1 to the counter value and returns it.
- POST '/decrease' - decreases 1 from the counter value and returns it.
- GET '/metadata' - return all the metadata about the counter API calls.

## Implementations

The counter value is persisted in a SQLite database.
Each request made to the API is logged to the database, including the timestamp, IP address of the requester, the
action (increase, decrease, or get).
The counter actions are guarded with locking mechanism.
The metadata is paginated because of the size and can be filtered by:

- page
- limit
- from_timestamp
- to_timestamp
- ip
- action_type

### Running the Application
The application is dockerized and can be easily run using docker-compose.

Run the following command to start the API server:

```bash
- Clone the repository to your local machine.

- Get the .env file for the connection string params (from author).

- Open a terminal window and navigate to the root directory of the cloned repository.

  $ docker-compose up
  
- This command will start the application server and the database. 
- Open the browser and navigate to http://localhost:5050.
```


