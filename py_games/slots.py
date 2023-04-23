## Simple slot machine game.

import random ## Import random module

MAX_LINES = 3 ## max number of lines
MAX_BET = 100 ## maximum bet
MIN_BET = 1 ## minimum bet
balance = int(0) ##global balance variable

ROWS = 3
COLS = 3

symbol_count = { ## Symbol count dictionary
    "A": 2, 
    "B": 4, 
    "C": 6, 
    "D": 6
}

symbol_value = { ## Symbol value dictionary
    "A": 5, 
    "B": 4, 
    "C": 3, 
    "D": 2
}

def check_winnings(columns, lines, bet, values): ## Check winnings function
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols): ## Slot machine spin function
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    
    columns = []
    for _ in range(cols):
        column = [ ]
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot_machine(columns): ## Print slot machine function
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) -1:
                print(column[row], end=" | ")
            else: 
                print(column[row], end="")

        print()
   
def deposit(): ## Deposit function
    global balance # Use the global balance variable

    while True:
        amount = input("Enter amount to deposit: $")
        if amount.isdigit() and int(amount) > 0:
            amount = int(amount)
            balance += amount # Add the deposited amount to the balance
            break
        else:
            print("Amount must be a positive number.")

    return balance

def number_of_lines(): ## Number of lines function
    while True:
        lines = input("Enter number of lines to bet on (1-3): ")
        if lines.isdigit():
            lines = int(lines)
            if lines > 0 and lines <= MAX_LINES:
                break
            else:
                print ("Number of lines must be between 1 and 3.")
        else:
            print ("Number of lines must be a number.")
    return lines

def get_bet(): ## Get bet function
    while True:
        amount = (input("Enter amount to bet on each line: $"))
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                 break
            else:
                print (f"Amount must be between {MIN_BET} -{MAX_BET}.")
        else:
            print ("Amount must be a number.")
    return amount

def spin():  ## Spin function
    global balance
    lines = number_of_lines()
    while True:
        bet = get_bet()
        total_bet = lines * bet

        if total_bet > balance:
            print("You do not have enough money to make that bet.")
        else:
            break
    
    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots) 
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    
    remaining_bet = total_bet - winnings # calculate the remaining bet amount after subtracting winnings
    
    balance -= remaining_bet # subtract the remaining bet amount from the balance
    
    if winnings >= 0:
        balance += winnings # add the winnings to the balance
    
    print(f"You won ${winnings}.")
    return balance

def keep_playing():
    global balance # Use the global balance variable

    while True:
        if balance == 0:
            print("You ran out of money.")
            deposit_choice = input("Do you want to deposit more money? (y/n)")
            if deposit_choice.lower() == "y":
                balance = deposit()
                print(f"Current balance is ${balance}")
            else:
                print("Thanks for playing!")
                return False
        else:
            play_choice = input("Press enter to play (q to quit).")
            if play_choice.lower() == "q":
                print(f"Thanks for playing! Your final balance is ${balance}")
                return False
            else:
                return True
def main(): ## Main function
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin() # Call the spin function and update the balance (add winnings to b
        keep_playing() # Call the continue function here

main()

