class MyAppException(Exception):
    pass


class MyAppAlreadyINException(MyAppException):
    def __init__(self, player_ine):
        """Initialize message."""
        msg = f"{player_ine} Already in this tournament"
        super().__init__(msg)


class MyAppPlayerNotFound(MyAppException):
    def __init__(self, player_ine):
        """Initialize message."""
        msg = f"{player_ine} Player not in the database"
        super().__init__(msg)


class MyAppBadPlayerCount(MyAppException):
    def __init__(self):
        """Initialize message."""
        msg = f"Need to have a pair number of player for launch the tournament"
        super().__init__(msg)
