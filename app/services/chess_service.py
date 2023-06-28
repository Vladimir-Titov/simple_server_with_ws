from dataclasses import dataclass

from app.services.game_manager import GameManager, Game
from board import BOARD


@dataclass
class Player:
    name: str
    ready_to_game: bool = False


class ChessService:

    def __init__(self):
        self.game_manager = GameManager()

    async def search_game(self, name: str):
        if name in self.game_manager.games:
            return self.game_manager.games[name]
        games_copy = self.game_manager.games.copy()
        for player_name, game in games_copy.items():
            if player_name != name:
                game.player2 = name
                game.board = BOARD
                game.is_filled = True
                self.game_manager.games[name] = game
                return self.game_manager.games[name]

        self.game_manager.games[name] = Game(player1=name)
        return self.game_manager.games[name]

    async def found_games(self, name: str):
        return self.game_manager[name]
