import core.player
import core.board
import core.dice
import core.checkers

def play():
    print("The game will start now!")
    print("... (game in progress) ...")

while True:
    print("\nWelcome to Backgammon!")
    print("Please choose an option:")
    print("1. Start a new game")
    print("2. Exit")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        play()
    elif choice == "2":
        print("Exiting the game. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")

def numplayers():
    if choice == "1":
        print("How many players? 1 or 2:")
        num_players = input("Enter 1 or 2: ")
    
    if num_players == "1":
        print("You selected 1-player mode.")
    elif num_players == "2":
        print("You selected 2-player mode.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

if numplayers == "1":
    print("Enter the player's name: ")
    player_name = input("Name: ")
    print(f"Welcome, {player_name}!")
elif numplayers == "2":
    print("Enter Player 1's name: ")
    player1_name = input("Name: ")
    print(f"Welcome, {player1_name}!")
    
    print("Enter Player 2's name: ")
    player2_name = input("Name: ")
    print(f"Welcome, {player2_name}!")

