from argparse import ArgumentParser
from redis import Redis

from game_of_life_common import constants
from game_of_life_common.board import GameOfLife

from game_of_life_web_server import app, board, redis_client, tick_period


def parse():
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--width', type=int, default=constants.DEFAULT_WIDTH)
    parser.add_argument('--height', type=int, default=constants.DEFAULT_HEIGHT)
    parser.add_argument('--tick-period', type=int, default=constants.TICK_PERIOD)
    parser.add_argument('--redis-server', default=constants.DEFAULT_REDIS_SERVER)

    return parser.parse_args()


def setup_tick_period(period):
    tick_period.__subject__ = period


def setup_redis(server=constants.DEFAULT_REDIS_SERVER):
    redis_client.__subject__ = Redis(server)


def setup_board(width, height):
    board.__subject__ = GameOfLife(width, height)  # blank default


def start(debug=False):
    app.run(debug=debug)


def main():
    namespace = parse()
    setup_tick_period(namespace.tick_period)
    setup_redis(namespace.redis_server)
    setup_board(namespace.width, namespace.height)
    start(namespace.debug)


if __name__ == '__main__':
    main()