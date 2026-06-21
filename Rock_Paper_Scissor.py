import random
from datetime import datetime

CHOICES = ["rock", "paper", "scissors"]


# ---------------- FUNCTIONS ---------------- #

def smart_move(last_move):
    """AI tries to beat player's last move"""
    if last_move == "rock":
        return "paper"
    elif last_move == "paper":
        return "scissors"
    elif last_move == "scissors":
        return "rock"
    return random.choice(CHOICES)


def get_computer_move(difficulty, last_player_move):
    """Pick the computer's move based on difficulty."""
    if difficulty == "1":  # Easy
        return random.choice(CHOICES)

    elif difficulty == "2":  # Medium - 50% smart
        if last_player_move and random.randint(1, 100) <= 50:
            return smart_move(last_player_move)
        return random.choice(CHOICES)

    else:  # Hard - 80% smart
        if last_player_move and random.randint(1, 100) <= 80:
            return smart_move(last_player_move)
        return random.choice(CHOICES)


def decides_winner(move_a, move_b):
    """Return 'a', 'b', or 'tie' depending on who wins."""
    if move_a == move_b:
        return "tie"
    beats = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    }
    return "a" if beats[move_a] == move_b else "b"


def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except Exception:
        return 0


def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))


# ---------------- MAIN MENU ---------------- #

def main_menu():
    while True:
        print("\n===== MAIN MENU =====")
        print("1. Play Game")
        print("2. View Leaderboard")
        print("3. View High Score")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            return
        elif choice == "2":
            print("\n===== LEADERBOARD =====")
            try:
                with open("leaderboard.txt", "r") as file:
                    content = file.read()
                    print(content if content else "Leaderboard is empty!")
            except Exception:
                print("No leaderboard found!")
        elif choice == "3":
            print("\n===== HIGH SCORE =====")
            print("High Score:", load_high_score())
        elif choice == "4":
            print("Thanks for playing!")
            exit()
        else:
            print("❌ Invalid choice!")


# ---------------- PvC MODE ---------------- #

def play_pvc():
    high_score = load_high_score()

    player_name = ""
    while not player_name:
        player_name = input("\nEnter your name: ").strip()
        if not player_name:
            print("❌ Name cannot be empty!")

    print(f"\nWelcome, {player_name}!")

    # Difficulty
    while True:
        print("\n===== DIFFICULTY =====")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        difficulty = input("Choose difficulty: ")
        if difficulty in ["1", "2", "3"]:
            break
        print("❌ Invalid choice!")

    difficulty_name = {"1": "Easy", "2": "Medium", "3": "Hard"}[difficulty]

    # Tournament length
    while True:
        print("\n===== TOURNAMENT MODE =====")
        print("1. Best of 3")
        print("2. Best of 5")
        print("3. Best of 7")
        choice = input("Choose tournament: ")
        if choice == "1":
            target_score = 2
            break
        elif choice == "2":
            target_score = 3
            break
        elif choice == "3":
            target_score = 4
            break
        else:
            print("❌ Invalid choice!")

    # Stats
    player_score = 0
    computer_score = 0
    wins = 0
    losses = 0
    ties = 0
    current_streak = 0
    best_streak = 0
    last_player_move = None

    # Achievements
    first_win = False
    streak_3 = False

    print("\nHigh Score:", high_score)

    # ---------------- GAME LOOP ---------------- #
    while player_score < target_score and computer_score < target_score:

        computer = get_computer_move(difficulty, last_player_move)

        print("\n(Type 'hint', 'cheat', or 'gun')")
        player = input("Enter rock, paper, or scissors: ").lower()

        if player == "hint":
            print(f"💡 Hint: Starts with {computer[0].upper()}")
            player = input("Now enter your move: ").lower()

        if player == "cheat":
            print("🕵️ Computer will play:", computer)
            player = input("Now enter your move: ").lower()

        if player == "gun":
            print("🔫 Secret Weapon Activated! Automatic Win!")
            player_score += 1
            wins += 1
            current_streak += 1
            best_streak = max(best_streak, current_streak)
            continue

        if player not in CHOICES:
            print("❌ Invalid choice!")
            continue

        last_player_move = player
        print("Computer chose:", computer)

        result = decides_winner(player, computer)

        if result == "tie":
            print("🤝 It's a tie!")
            ties += 1
            current_streak = 0

        elif result == "a":  # player wins
            print("🎉 You win this round!")
            player_score += 1
            wins += 1
            current_streak += 1

            if not first_win:
                print("🏅 Achievement: First Win!")
                first_win = True

            if current_streak == 3 and not streak_3:
                print("🔥 Achievement: 3 Win Streak!")
                streak_3 = True

            best_streak = max(best_streak, current_streak)

        else:  # computer wins
            print("💻 Computer wins this round!")
            computer_score += 1
            losses += 1
            current_streak = 0

        print("\n===== SCORE =====")
        print("Player:", player_score)
        print("Computer:", computer_score)
        print("Current Streak:", current_streak)
        print("Best Streak:", best_streak)

    # ---------------- MATCH OVER ---------------- #
    print("\n===== MATCH OVER =====")

    if player_score == target_score:
        winner = player_name
        print("🏆 You won the tournament!")
    else:
        winner = "Computer"
        print("💻 Computer won the tournament!")

    if wins > high_score:
        high_score = wins
        save_high_score(high_score)
        print("🏆 New High Score!")

    print("\n===== STATISTICS =====")
    print("Wins:", wins)
    print("Losses:", losses)
    print("Ties:", ties)

    print("\n===== STREAKS =====")
    print("Best Streak:", best_streak)
    print("\nHigh Score:", high_score)

    current_time = datetime.now()
    date = current_time.strftime("%d-%m-%Y")
    time_str = current_time.strftime("%I:%M %p")

    with open("stats.txt", "w") as file:
        file.write("===== STATS =====\n")
        file.write(f"Wins: {wins}\n")
        file.write(f"Losses: {losses}\n")
        file.write(f"Ties: {ties}\n")
        file.write(f"Best Streak: {best_streak}\n")
        file.write(f"High Score: {high_score}\n")

    with open(f"{player_name}.txt", "w") as file:
        file.write(f"Player: {player_name}\n")
        file.write(f"Wins: {wins}\n")
        file.write(f"Losses: {losses}\n")
        file.write(f"Ties: {ties}\n")
        file.write(f"Best Streak: {best_streak}\n")
        file.write(f"High Score: {high_score}\n")

    with open("leaderboard.txt", "a") as file:
        file.write(f"{player_name} - {wins} Wins\n")
    print("🏆 Score added to leaderboard!")

    with open("match_history.txt", "a") as file:
        file.write("========================\n")
        file.write("Mode: PvC\n")
        file.write(f"Player: {player_name}\n")
        file.write(f"Winner: {winner}\n")
        file.write(f"Score: {player_score}-{computer_score}\n")
        file.write(f"Ties: {ties}\n")
        file.write(f"Difficulty: {difficulty_name}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time_str}\n")
        file.write("========================\n\n")
    print("📜 Match history saved!")


# ---------------- PvP MODE ---------------- #

def play_pvp():
    player1 = input("Enter Player 1 name: ").strip() or "Player 1"
    player2 = input("Enter Player 2 name: ").strip() or "Player 2"

    while True:
        print("\n===== TOURNAMENT MODE =====")
        print("1. Best of 3")
        print("2. Best of 5")
        print("3. Best of 7")
        choice = input("Choose tournament: ")
        if choice == "1":
            target_score = 2
            break
        elif choice == "2":
            target_score = 3
            break
        elif choice == "3":
            target_score = 4
            break
        else:
            print("❌ Invalid choice!")

    player1_score = 0
    player2_score = 0
    player1_streak = 0
    player2_streak = 0
    ties = 0

    # Achievements
    p1_streak_award = False
    p2_streak_award = False

    while player1_score < target_score and player2_score < target_score:
        print(f"\n--- Round (P1: {player1_score}, P2: {player2_score}) ---")

        player1_move = input(f"{player1}, enter your move (privately): ").lower()
        # Clear the screen-ish so player2 doesn't see player1's move
        print("\n" * 30)
        player2_move = input(f"{player2}, enter your move (privately): ").lower()
        print("\n" * 30)

        if player1_move not in CHOICES or player2_move not in CHOICES:
            print("❌ Invalid choice! Round skipped.")
            continue

        result = decides_winner(player1_move, player2_move)

        print(f"{player1} chose: {player1_move}")
        print(f"{player2} chose: {player2_move}")

        if result == "tie":
            print("🤝 It's a tie!")
            ties += 1
            player1_streak = 0
            player2_streak = 0

        elif result == "a":
            print(f"🎉 {player1} wins this round!")
            player1_score += 1
            player1_streak += 1
            player2_streak = 0

            if player1_streak == 3 and not p1_streak_award:
                print(f"🔥 {player1} Achievement: 3 Round Streak!")
                p1_streak_award = True

        else:
            print(f"🎉 {player2} wins this round!")
            player2_score += 1
            player2_streak += 1
            player1_streak = 0

            if player2_streak == 3 and not p2_streak_award:
                print(f"🔥 {player2} Achievement: 3 Round Streak!")
                p2_streak_award = True

        print("\n===== SCORE =====")
        print(f"{player1}: {player1_score}")
        print(f"{player2}: {player2_score}")
        print("Ties:", ties)

    print("\n===== MATCH OVER =====")
    print("\n===== PvP STATISTICS =====")
    print(f"{player1} Round Wins:", player1_score)
    print(f"{player2} Round Wins:", player2_score)
    print("Ties:", ties)

    if player1_score == target_score:
        winner = player1
    else:
        winner = player2

    print(f"🏆 {winner} wins the tournament!")
    print(f"👑 {winner} Achievement: PvP Champion!")

    if player1_score == target_score and player2_score == 0:
        print(f"⚡ {player1} Achievement: Perfect Tournament!")
    elif player2_score == target_score and player1_score == 0:
        print(f"⚡ {player2} Achievement: Perfect Tournament!")

    current_time = datetime.now()
    date = current_time.strftime("%d-%m-%Y")
    time_str = current_time.strftime("%I:%M %p")

    with open("leaderboard.txt", "a") as file:
        file.write(f"{winner} - Tournament Win\n")
    print("🏆 Score added to leaderboard!")

    with open("match_history.txt", "a") as file:
        file.write("========================\n")
        file.write("Mode: PvP\n")
        file.write(f"Player 1: {player1}\n")
        file.write(f"Player 2: {player2}\n")
        file.write(f"Winner: {winner}\n")
        file.write(f"Score: {player1_score}-{player2_score}\n")
        file.write(f"Ties: {ties}\n")
        file.write(f"Date: {date}\n")
        file.write(f"Time: {time_str}\n")
        file.write("========================\n\n")
    print("📜 Match history saved!")


# ---------------- GAME MODE SELECTION ---------------- #

def choose_game_mode():
    while True:
        print("\n===== GAME MODE =====")
        print("1. Player vs Computer")
        print("2. Player vs Player")
        mode = input("Choose mode: ")
        if mode in ["1", "2"]:
            return mode
        print("❌ Invalid choice!")


# ---------------- MAIN PROGRAM ---------------- #

def main():
    main_menu()

    while True:
        mode = choose_game_mode()

        if mode == "1":
            play_pvc()
        else:
            play_pvp()

        while True:
            play_again = input("\nPlay Again? (yes/no): ").lower()
            if play_again == "yes":
                break
            elif play_again == "no":
                print("Thanks for playing!")
                exit()
            else:
                print("❌ Invalid input!")


if __name__ == "__main__":
    main()