# Игра "Крестики-нолики"
def display_board(board):
    """Вывод на экран игрового поля с форматированием"""
    print("\n    0   1   2")
    print("  ┌───┬───┬───┐")
    for i in range(3):
        print(f"{i} │ {board[i][0]} │ {board[i][1]} │ {board[i][2]} │")
        if i < 2:
            print("  ├───┼───┼───┤")
    print("  └───┴───┴───┘")

def check_winner(board, player):
    """Проверка выигрыша текущего игрока"""
    # По строкам
    for row in range(3):
        if all(board[row][col] == player for col in range(3)):
            return True
    # По столбцам
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # По диагонали сверху вниз
    if all(board[i][i] == player for i in range(3)):
        return True
    # По диагонали снизу вверх
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True

def get_player_step(board, player):
    while True:
        try:
            print(f"\nИгрок {player}, ваш ход.")
            step_input = input("Введите ЧЕРЕЗ ПРОБЕЛ клетку в формате \"Номер строки (0-2) и номер столбца (0-2)\": ")
            row, col = map(int, step_input.split())

            if row < 0 or row > 2 or col < 0 or col > 2:
                print("ОШИБКА: введите числа от 0 до 2!")
            elif board[row][col] != " ":
                print("ОШИБКА: эта клетка уже занята!")
            else:
                return row, col
        except (ValueError, IndexError):
            print("ОШИБКА: введите два числа через пробел (например: 1 2)!")


def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("=" * 50)
    print(" ХХХ ООО      ИГРА 'КРЕСТИКИ-НОЛИКИ'      ООО ХХХ")
    print("=" * 50)
    print("Перед Вами игровое поле")
    print("Строки и столбцы нумеруются от 0 до 2")
    print("Ваша задача: собрать линию в трех соседних клетках")
    print("Игрок-Крестик (X) всегда начинает ходить первым")
    print("=" * 50)

    current_player = "X"

    while True:
        display_board(board)
        row, col = get_player_step(board, current_player)
        board[row][col] = current_player

        if check_winner(board, current_player):
            display_board(board)
            print(f"\n УРА! ИГРОК {current_player} ПОБЕДИЛ! ")
            break

        if is_board_full(board):
            display_board(board)
            print("\n НИЧЬЯ! ")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    play_game()

    while True:
        play_again = input("\nХотите сыграть еще? (да/нет): ").lower()
        if play_again == "да":
            play_game()
        elif play_again == "нет":
            print("Спасибо за игру! До свидания!")
            break
        else:
            print("Пожалуйста, введите 'да' или 'нет'")