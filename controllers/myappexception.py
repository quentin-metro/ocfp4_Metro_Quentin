class MyAppException(Exception):
    pass


class MyAppAlreadyInException(MyAppException):
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


class MyAppDontPlayThisMatch(MyAppException):
    def __init__(self):
        """Initialize message."""
        msg = f"This player don't play in this match"
        super().__init__(msg)


class MyAppPlayerAlreadyExist(MyAppException):
    def __init__(self):
        """Initialize message."""
        msg = f"This Player INE already use"
        super().__init__(msg)


class MyAppBadPlayerINE(MyAppException):
    def __init__(self):
        """Initialize message."""
        msg = f"This INE is in the wrong format. Correct format: \'AA12345\'"
        super().__init__(msg)
