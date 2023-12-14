"""
Blackjack game created in Python for up to 5 players.
Latest update: 13.12.2023
A console-based Blackjack card game to play solo or with up to 5 friends.
"""

# Import necessary modules
import random
import time
import sys

BALANCE = 50  # Initial balance for each player

class Player:
    def __init__(self, name, cards, balance: float, bet: float) -> None:
        self.name = name
        self.cards = cards
        self.balance = balance
        self.bet = bet

    def deal_cards(self, cards):
        self.cards = cards

    def calculate_hand_value(self):
        # Calculate the total value of the player's hand, considering Aces as 1 or 11
        total_value = 0
        num_aces = 0

        for card in self.cards:
            total_value += self.calculate_card_value(card['value'], total_value)

            if card['value'] == 'A':
                num_aces += 1

        while total_value > 21 and num_aces:
            total_value -= 10
            num_aces -= 1

        return total_value

    @staticmethod
    def calculate_card_value(card_value, current_hand_value):
        # Helper method to calculate the value of a card
        if card_value in {'K', 'Q', 'J'}:
            return 10
        elif card_value == 'A':
            if current_hand_value + 11 <= 21:
                return 11
            else:
                return 1
        else:
            return int(card_value)

def create_deck():
    # Create and return a deck of cards
    values = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']
    suits = ['spades', 'hearts', 'diamonds', 'clubs']
    deck = [{'value': value, 'suit': suit} for value in values for suit in suits]
    return deck

def create_player():
    # Create a list of player objects based on user input for the number of players
    while True:
        try:
            player_count = int(input("How many players (1-5): "))
            if 1 <= player_count <= 5:
                print()
                players = []
                for i in range(1, player_count + 1):
                    player = Player(f"Player {i}", None, BALANCE, None)
                    players.append(player)
                return players
            else:
                print("Please enter a valid number of players (1-5).")
                print()
        except ValueError:
            print("Please enter a valid integer.")
            print()

def shuffle_deck(deck):
    # Shuffle the deck of cards
    random.shuffle(deck)

def first_turn(players, TABLE, deck):
    # Conduct the first turn of the game, including player bets and initial card dealing
    for player in players[:]:
        while True:
            print(f"{player.name}'s turn")
            play = input("Do you want to play? (y/n): ")
            if play.lower() == "n":
                players.remove(player)
                print("")
                break
            elif play.lower() == "y":
                print("How much would you like to bet?")
                try:
                    bet = float(input(""))
                    player.bet = bet
                    if player.bet < player.balance + 1:
                        player.balance -= player.bet
                        print("")
                        break
                    else:
                        print("Bet can't be higher than your balance")
                        print(f"Your balance is {player.balance}")
                        print()
                except ValueError:
                    print("Please enter a valid number.")
                    print()
            else:
                print("Invalid input.")
                print()

    print("Cards on the table:")
    print(f"   {TABLE.cards[0]['value']} {TABLE.cards[0]['suit']}")
    print(f"   X X")
    print(" ")
    for player in players:
        player.deal_cards(deck[:2])
        del deck[:2]

    for player in players:
        print(f"{player.name}")
        print(f"BALANCE: {player.balance}")
        for card in player.cards:
            print(f"  {card['value']} {card['suit']}")
        print(f"Hand value: {player.calculate_hand_value()}")
        print()

    next_turns(players, deck, TABLE)

def next_turns(players, deck, TABLE):
    # Handle subsequent turns for each player
    for player in players[:]:
        while True:
            print(f"{player.name}'s turn")
            print("Type W-Wait, D-Double your bet, C-Get one card")
            call = input().lower()
            print()
            if call == "w":
                break
            elif call == "d":
                new_balance = player.balance - player.bet
                if new_balance < 0:
                    print("Can't bet outside of your balance")
                    print(f"Your balance is {player.balance}")
                    while True:
                        print("Would you like to W-Wait or C-Get one card: ")
                        call = input().lower()
                        if call == "w":
                            break
                        elif call == "c":
                            while True:
                                player.cards.append(deck.pop(0))
                                print(f"Your deck")
                                if player.calculate_hand_value() > 21:
                                    print(f"Hand value: {player.calculate_hand_value()} - BUSTED")
                                    print()
                                    break
                                elif player.calculate_hand_value() == 21:
                                    print(f"Hand value: {player.calculate_hand_value()} - BLACKJACK!")
                                    print()
                                    break
                                else:
                                    for card in player.cards:
                                        print(f"   {card['value']} {card['suit']}")
                                    print()
                                    check = input("Would you like to get another card? (y/n): ")
                                    if check == "n":
                                        print()
                                        break
                            break
                else:
                    player.cards.append(deck.pop(0))
                    player.balance -= player.bet
                    break
            elif call == "c":
                while True:
                    player.cards.append(deck.pop(0))
                    print(f"Your deck")
                    for card in player.cards:
                        print(f"   {card['value']} {card['suit']}")
                    hand_value = player.calculate_hand_value()
                    print()
                    while True:
                        check = input("Would you like to get another card? (y/n): ")
                        if check.lower() == "n":
                            break
                        elif check.lower() == "y":
                            break
                        else:
                            print("Invalid input")

                    if hand_value > 21:
                        print(f"Hand value: {hand_value} - BUSTED")
                        print()
                        break
                    elif hand_value == 21:
                        print(f"Hand value: {hand_value} - BLACKJACK!")
                        print()
                        break
                    elif check == "n":
                        print(f"Hand value {hand_value}")
                        break

            else:
                print("Invalid input.")
            break

    for player in players:
        print(f"{player.name}")
        print(f"BALANCE: {player.balance}")
        for card in player.cards:
            print(f"  {card['value']} {card['suit']}")
        print(f"Hand value: {player.calculate_hand_value()}")
        print()

    finale(players, TABLE, deck)

def finale(players, TABLE, deck):
    # Conclude the game, revealing the dealer's cards and determining winners
    while TABLE.calculate_hand_value() < 17:
        TABLE.cards.append(deck.pop(0))
    print("Dealer cards!")

    for card in TABLE.cards:
        print(f"   {card['value']} {card['suit']}")
    print(f"   Hand value: {TABLE.calculate_hand_value()}")
    print()

    TABLE_VALUE = TABLE.calculate_hand_value()

    for player in players[:]:
        print(f"{player.name}'s cards")
        print(f"BALANCE: {player.balance}")
        for card in player.cards:
            print(f"   {card['value']} {card['suit']}")
        print(f"   Hand value: {player.calculate_hand_value()}")
        print()

    for player in players[:]:
        hand_value = player.calculate_hand_value()

        if hand_value > 21:
            pass
        elif hand_value >= TABLE_VALUE and hand_value < 21:
            player.balance += player.bet*1.5
        elif hand_value == 21:
            player.balance += player.bet*2

    for player in players[:]:
        print(f"{player.name} BALANCE: {player.balance}")
        print()

    # Clearing hands and TABLE and starting new game
    print("GAME ENDS NEXT TURN STARTS IN 5 SEC")
    time.sleep(5)

    for player in players[:]:
        if player.balance <= 0:
            print(f"{player.name} run out of balance!")
            players.remove(player)

    if not players:
        print("All players are out!")
        time.sleep(2)
        sys.exit()

    deck = create_deck()
    shuffle_deck(deck)

    TABLE.cards = []

    for player in players:
        player.cards = []

    TABLE.deal_cards(deck[:2])
    del deck[:2]

    for player in players:
        player.deal_cards(deck[:2])
        del deck[:2]

    first_turn(players, TABLE, deck)

def main():
    # Main function initializing the game
    TABLE = Player("TABLE", None, 0, None)

    deck = create_deck()
    shuffle_deck(deck)

    TABLE.deal_cards(deck[:2])
    del deck[:2]

    players = create_player()

    first_turn(players, TABLE, deck)

if __name__ == "__main__":
    main()