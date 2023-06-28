from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class Game:
    id: int = 0
    player1: Optional[str] = None
    player2: Optional[str] = None
    board: Optional[dict] = None
    is_filled: bool = False

    def __new__(cls, *args, **kwargs):
        cls.id += 1
        return super().__new__(cls)


class GameManager:
    _instance = None
    ready_players = {}
    games: Dict[str, Game] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
