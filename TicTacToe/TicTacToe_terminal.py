import random,time

class TicTacToe:
    def __init__(self, with_comp=False):
        self.with_comp = with_comp
        self.board = [' ' for i in range(10)]
        self.players = {0: 'X', 1: 'O'}
        self.current_player = 0
        self.win_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        self.moves = 0

    def print_board(self):
        print(f'{self.board[1]} | {self.board[2]} | {self.board[3]}')
        print(f'--|---|--')
        print(f'{self.board[4]} | {self.board[5]} | {self.board[6]}')
        print(f'--|---|--')
        print(f'{self.board[7]} | {self.board[8]} | {self.board[9]}')

    def player_switch(self):
        self.current_player ^= 1

    def comp_move(self):
        self.player_switch()
        corners = [1,3,7,9]

        if self.moves == 1:
            for corner in corners:
                if self.board[corner] != ' ':
                    return 5

        available_moves = [index for index in range(1,10) if self.board[index] == ' ']

        for player in ['O', 'X']:
            for move in available_moves:
                self.board[move] = player
                if self.is_winner(check=True):
                    self.board[move] = ' '
                    return move
                else:
                    self.board[move] = ' '

        available_corners = []
        available_edges = []
        for move in available_moves:
            if move in corners:
                available_corners.append(move)
            else:
                available_edges.append(move)

        if available_corners:
            return random.choice(available_corners)

        if 5 in available_moves:
            return 5

        if available_edges:
            return random.choice(available_edges)

    def make_move(self,inp=None):
        if not inp:
            inp = int(input(f'player {self.current_player} =>>'))
            while not self.space_is_free(inp) or inp == 0:
                self.print_board()
                print('Please try another')
                inp = int(input(f'player {self.current_player} =>>'))
        self.board[inp] = self.players[self.current_player]
        self.moves += 1

    def space_is_free(self,pos):
        return False if self.board[pos] != ' ' else True

    def is_winner(self,check=False):
        for i,j,k in self.win_board:
            if self.board[i] == self.board[j] == self.board[k] and self.board[i] != ' ':
                if not check:
                    for v in (i,j,k):
                        self.board[v] = '\033[91m'+self.board[i]+'\033[00m'
                return True
        return False

    def is_board_full(self):
        return True if self.moves >= 9 else False

    def check(self):
        if self.is_winner():
            self.print_board()
            if self.with_comp and self.current_player != 0:
                print('Compluter Win')
            else:
                print(f'Player {self.current_player} win')
            return True
        if self.is_board_full():
            print('Draw')
            return True

    def play(self):
        while True:
            self.print_board()
            self.make_move()
            if self.check():
                break
            if self.with_comp:
                self.print_board()
                move = self.comp_move()
                print(f'computer => {move}')
                time.sleep(1)
                self.make_move(move)
                if self.check():
                    break
            self.player_switch()

def main():
    while True:
        print('Select Mode\n-----------')
        print('1. Multiplayer')
        print('2. Single Player')
        mode = True if int(input('(1/2) => ')) == 2 else None
        ttc = TicTacToe(mode)
        ttc.play()
        inp = input('Restart?(y/n)')
        if inp == 'y' or inp == 'Y':
            continue
        else:
            print('Thank you')
            break

if __name__ == '__main__':
    main()