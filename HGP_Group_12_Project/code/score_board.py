from PyQt6.QtWidgets import (
    QDockWidget,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import pyqtSignal, pyqtSlot

class ScoreBoard(QDockWidget):
    """Base the score_board on a QDockWidget"""

    passTurnSignal = pyqtSignal()
    resetGameSignal = pyqtSignal()
    endGameSignal = pyqtSignal(int)  # Signal to end the game with the winner's player number

    def __init__(self):
        super().__init__()
        self.initUI()
        self.pass_count = 0  # Counter for consecutive passes
        self.last_player_passed = None  # Track the last player who passed
        self.board = None  # Attribute to store the Board object

    def initUI(self):
        """Initiates ScoreBoard UI"""
        self.resize(300, 400)
        self.setWindowTitle("ScoreBoard")

        # Create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # Create labels and buttons
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.label_player1 = QLabel("Player 1: ")
        self.label_player2 = QLabel("Player 2: ")
        self.label_prisoners_p1 = QLabel("Prisoners P1: 0")
        self.label_prisoners_p2 = QLabel("Prisoners P2: 0")
        self.label_territory_p1 = QLabel("Territory P1: 0")
        self.label_territory_p2 = QLabel("Territory P2: 0")
        self.label_turn = QLabel("Turn: ")

        self.button_pass = QPushButton("Pass")
        self.button_reset = QPushButton("Reset Game")
        self.button_rules = QPushButton("Rules of Ko and Suicide")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)

        playerLayout = QHBoxLayout()
        playerLayout.addWidget(self.label_player1)
        playerLayout.addWidget(self.label_player2)
        self.mainLayout.addLayout(playerLayout)

        prisonersLayout = QHBoxLayout()
        prisonersLayout.addWidget(self.label_prisoners_p1)
        prisonersLayout.addWidget(self.label_prisoners_p2)
        self.mainLayout.addLayout(prisonersLayout)

        territoryLayout = QHBoxLayout()
        territoryLayout.addWidget(self.label_territory_p1)
        territoryLayout.addWidget(self.label_territory_p2)
        self.mainLayout.addLayout(territoryLayout)

        self.mainLayout.addWidget(self.label_turn)
        self.mainLayout.addWidget(self.button_pass)
        self.mainLayout.addWidget(self.button_reset)
        self.mainLayout.addWidget(self.button_rules)

        self.setWidget(self.mainWidget)

        self.button_rules.clicked.connect(self.showKoSuicideRules)

        # Navigation buttons for pending moves
        self.button_prev = QPushButton("Previous Move")
        self.button_next = QPushButton("Next Move")

        # Add navigation buttons
        navigationLayout = QHBoxLayout()
        navigationLayout.addWidget(self.button_prev)
        navigationLayout.addWidget(self.button_next)
        self.mainLayout.addLayout(navigationLayout)

    def make_connection(self, board):
        """This handles a signal sent from the board class"""
        self.board = board  # Store the Board object
        # When the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # When the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        self.button_pass.clicked.connect(self.pass_turn)
        self.button_reset.clicked.connect(self.resetGameSignal.emit)

        # Connect navigation buttons to board methods
        self.button_prev.clicked.connect(self.board.PreviousPendingMove)
        self.button_next.clicked.connect(self.board.NextPendingMove)

    @pyqtSlot(
        str
    )  # Checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        """Updates the label to show the click location"""
        self.label_clickLocation.setText("Click Location: " + clickLoc)
        # print("slot " + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        """Updates the time remaining label to show the time remaining"""
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        # print("slot " + str(timeRemaining))
        # self.redraw()

    def updatePrisoners(self, prisoners_p1, prisoners_p2):
        self.label_prisoners_p1.setText(f"Prisoners P1: {prisoners_p1}")
        self.label_prisoners_p2.setText(f"Prisoners P2: {prisoners_p2}")

    def updateTerritory(self, territory_p1, territory_p2):
        self.label_territory_p1.setText(f"Territory P1: {territory_p1}")
        self.label_territory_p2.setText(f"Territory P2: {territory_p2}")

    def updateTurn(self, player_turn):
        color = "black" if player_turn == 2 else "white"
        self.label_turn.setText(f"Turn: Player {player_turn} ({color}) to play")

    def pass_turn(self):
        self.passTurnSignal.emit()

    def showKoSuicideRules(self):
        rules = (
            'Rules of Ko and Suicide in Go:\n'
            '1. Ko Rule: A player cannot play a move that returns the board to the exact same position as it was after the previous move.\n\n'
            '2. Suicide Rule: A player cannot play a move that results in the immediate capture of their own stone(s) unless it also results in the capture of one or more of the opponent\'s stones.\n'
        )
        QMessageBox.information(self, "Rules of Ko and Suicide", rules)

    def updatePlayerNames(self, player1, player2):
        self.label_player1.setText(f"Player 1: {player1}")
        self.label_player2.setText(f"Player 2: {player2}")
