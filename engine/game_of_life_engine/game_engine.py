from argparse import ArgumentParser
from datetime import datetime, timedelta
import pickle
from random import getrandbits
from redis import Redis
from time import sleep

from game_of_life_common import constants
from game_of_life_common.board import GameOfLife


def running_state_from_redis(redis_client):
    return redis_client.get(constants.REDIS_KEY_RUNNING_STATE) == constants.REDIS_TRUE


def added_tiles_from_redis(redis_client):
    additions = []
    for _ in xrange(constants.THROUGHPUT):
        addition = redis_client.lpop(constants.REDIS_KEY_ADDITIONS)
        if addition:
            additions.append(addition)
        else:
            break
    return additions


def removed_tiles_from_redis(redis_client):
    removals = []
    for _ in xrange(constants.THROUGHPUT):
        removal = redis_client.lpop(constants.REDIS_KEY_REMOVALS)
        if removal:
            removals.append(removal)
        else:
            break
    return removals


def push_board_to_redis(redis_client, board):
    redis_client.set(constants.REDIS_KEY_BOARD, pickle.dumps(board.tiles))


def parse():
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--width', type=int, default=constants.DEFAULT_WIDTH)
    parser.add_argument('--height', type=int, default=constants.DEFAULT_HEIGHT)
    parser.add_argument(
        '--tick-period', type=int, default=constants.TICK_PERIOD, help='milliseconds')
    parser.add_argument('--redis-server', default=constants.DEFAULT_REDIS_SERVER)
    parser.add_argument('--random', action='store_true', help='begin random instead of blank')

    return parser.parse_args()


def setup_redis(server=constants.DEFAULT_REDIS_SERVER):
    redis_client = Redis(server)

    redis_client.delete(
        constants.REDIS_KEY_RUNNING_STATE,
        constants.REDIS_KEY_ADDITIONS,
        constants.REDIS_KEY_REMOVALS,
        constants.REDIS_KEY_BOARD,
    )
    redis_client.set(constants.REDIS_KEY_RUNNING_STATE, constants.REDIS_TRUE)

    return redis_client


def extract_coordinates(redis_string):
    x, y = redis_string.split(',')
    return int(x), int(y)


def randomize_board(board):
    for y in xrange(board.height):
        for x in xrange(board.width):
            board[y][x] = getrandbits(1)


def mainloop(board, period, redis_client, debug=False):
    period = timedelta(milliseconds=period)

    while True:
        t0 = datetime.now()

        running_state = running_state_from_redis(redis_client)
        additions = added_tiles_from_redis(redis_client) or []
        if debug:
            print 'additions: ({}) {}'.format(type(additions), additions)
        for addition in additions:
            x, y = extract_coordinates(addition)
            board[y][x] = True
        removals = removed_tiles_from_redis(redis_client) or []
        if debug:
            print 'removals: ({}) {}'.format(type(removals), removals)
        for removal in removals:
            x, y = extract_coordinates(removal)
            board[y][x] = False

        if running_state:
            if debug:
                print str(board)
            board.evolve()
        else:
            if debug:
                print 'Not Running'

        # pushes even if board isn't evolving because it can still be modified
        push_board_to_redis(redis_client, board)

        sleep_seconds = (period - (datetime.now() - t0)).microseconds / 1000000.0
        sleep(sleep_seconds)


def main():
    namespace = parse()

    redis_client = setup_redis()
    board = GameOfLife(namespace.width, namespace.height)
    if namespace.random:
        randomize_board(board)
    mainloop(board, namespace.tick_period, redis_client, namespace.debug)


if __name__ == '__main__':
    main()