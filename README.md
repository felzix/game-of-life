# game-of-life
Project I wrote to learn flask. Also uses redis and sqlalchemy.

The engine and web server are separately invoked. Their width and height should be the same.

The engine updates every second unless turned off. Even if turned off, it pushes its state to redis.

The web server polls the current game state whenever asked to be a web client (or other HTTP requester).
The web server caches game state so it only requests once a second at most.

The web client tries to draw every 50 milliseconds but only request state every second or when it sends an update.
Like the web server, the web client caches the game state for drawing... though now that I think about it, it should
just not draw when it has the latest state...
