# game-of-life
Project I wrote to learn flask. Also uses redis.

The engine and web server are separately invoked. Their width and height should be the same.

The engine updates every second unless turned off. Even if turned off, it pushes its state to redis.

The web server polls the current game state whenever asked to be a web client (or other HTTP requester).
The web server caches game state so it only requests once a second at most.

The web client tries to draw every 50 milliseconds but only request state every second or when it sends an update.
Like the web server, the web client caches the game state for drawing. It only draws when it needs to.

# usage

With engine installed in the virtualenv:

        game-of-life-engine --tick-period 100 --random

With web server installed in the virtualenv:

        game-of-life-web-server --tick-period 100


These are examples. Use "-h" on each command for more details.
