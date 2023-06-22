from enum import Enum


class EventType(str, Enum):
    MOVE = 'MOVE'
    ONLINE_PLAYERS = 'ONLINE_PLAYERS'
    START_GAME = 'START_GAME'
