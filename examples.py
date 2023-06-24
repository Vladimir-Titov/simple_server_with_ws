online_message = {
    'event_type': 'ONLINE_PLAYERS',
    'payload': None,
}
online_message_response = {
    'event_type': 'ONLINE_PLAYERS',
    'payload': {
        'count_online_players': 4,
        'online_players': '{"{player_name}: websocket"}'
    }
}

start_game_message = {
    'event_type': 'START_GAME',
    'payload': None,
}
start_game_response = {
    'event_type': 'GAME_STARTED',
    'payload': {
        'you': 'player1_name',
        'opponent': 'player2_name',
        'game_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    }
}

start_board_message = {
    'event_type': 'START_BOARD',
    'payload': {},
}

start_board_response = {
    'event_type': 'START_BOARD',
    'payload': {
        'board': [
            {
                "piece": "king",
                "color": "white",
                "square": "e1",
                "id": "1",
            },
        ]
    }
}
