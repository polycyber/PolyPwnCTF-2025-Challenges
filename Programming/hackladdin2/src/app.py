import random
import string
import signal

class Hackladdin2:
    """Hackladdin 2 Server for CTF"""
    banner_filename = "./asciiart.txt"
    timeout = 10  # seconds
    flag = "polycyber{V1v3l4Pr0Gr4m4m710nP4rC0nTr41nT3}"
    max_guesses = 20
    passcode_length = 6   
    n_passcodes = 5

    ### I/O functions ###

    def welcome(self) -> None:
        with open(self.banner_filename, 'r') as f:
            print(f.read())
        print()
        print("You think it will that easy to enter the cave of Jhackfar?")
        print("I am going to make it harder for you!")
        print(f"Since I am so generous, you will have {self.max_guesses} attempts for each passcodes.")
        print()

    def game_over(self) -> None:
        print("You have angered Jhackfar!")

    def bad_response(self, correct_letters: list[str], misplaced_letters: list[str]) -> None:
        print(f"Number of correctly placed letters: {len(correct_letters)}")
        print(f"Number of misplaced letters: {len(misplaced_letters)}")

    def good_response(self, n) -> None:
        print(f"Impressive! {'You have found all the passcodes!' if n == 0 else f'{n} passcode(s) left to find.'}")

    def win(self) -> None:
        print("You have proven yourself worthy!")
        print(f"The flag is: {self.flag}")

    def invalid_response(self) -> None:
        print(f"You waste an attempt! The passcode must be {self.passcode_length} characters long.")

    def check_guess(self, passcode: str, guess: str) -> tuple[list[str], list[str]]:
        correct_positions = []
        misplaced_letters = []

        for j in range(self.passcode_length):
            if guess[j] == passcode[j]:
                correct_positions.append(guess[j])
        
        for letter in guess:
            if letter in passcode and letter not in correct_positions:
                misplaced_letters.append(letter)
    
        return correct_positions, misplaced_letters

    def renew_passcode(self) -> list[str]:
        return "".join(random.sample(string.ascii_lowercase, k=self.passcode_length))

    def recv_response(self) -> str:
        signal.alarm(self.timeout)
        response = input(">> ")
        signal.alarm(0)
        return response

    #####################

    def chall(self) -> None:
        self.welcome()
        defeat = False

        for i in range(self.n_passcodes):
            passcode = self.renew_passcode()

            for _ in range(self.max_guesses):
                response = self.recv_response()

                if response == passcode:
                    self.good_response(self.n_passcodes - (i + 1))
                    break

                if len(response) != self.passcode_length:
                    self.invalid_response()
                    continue
                
                correct_letters, misplaced_letters = self.check_guess(passcode, response)
                self.bad_response(correct_letters, misplaced_letters)

            else:
                defeat = True
                break

        if defeat:
            # Game Over
            self.game_over()
            exit(0)
        else:
            self.win()


def timeout_handler(signum, frame):
    print("You took too long!")
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGALRM, timeout_handler)
    server = Hackladdin2()
    server.chall()
