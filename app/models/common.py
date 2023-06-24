from enum import Enum


class EventType(str, Enum):
    MOVE = 'MOVE'
    START_BOARD = 'START_BOARD'
    ONLINE_PLAYERS = 'ONLINE_PLAYERS'
    START_GAME = 'START_GAME'
