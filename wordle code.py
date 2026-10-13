
import requests
import pandas as pd
import random

endpoint_url = "https://api.datamuse.com/words?sp="

#colors
green = "\033[42m\033[30m"
yellow = "\033[43m\033[30m"
black = "\033[40m\033[37m"
reset = "\033[0m"

def validate_word_api(url: str, word: str) -> dict:
    """
    שולחת בקשה ל-URL ובודקת את התשובה לפי פרמטרים מוגדרים מראש.
    """
    # 1. הגדרת פרמטרים לבקשה (Query Parameters)
    key="&md=d"
    new_url=url+word+key
    
        # שליחת בקשת GET לקישור (ניתן לשנות ל-requests.post במידת הצורך)
    response = requests.get(new_url, timeout=10)
        
        # 2. בדיקת תקינות קוד תגובת HTTP
    if response.status_code != 200:
        return {
            "success": False,
            "error": f"HTTP Error: {response.status_code}"
        }
        
        # 3. פענוח התשובה (בהנחה שה-API מחזיר JSON)
    data = response.json()
    return data
    


def does_word_exist(wordToTest):
    res = validate_word_api(endpoint_url, wordToTest)
    if isinstance(res, list):
        for item in res:
            if item.get("word") == wordToTest and "defs" in item:
                return True
    return False

class game:

    def __init__(self):

        self.df = pd.read_csv(r"E:\Coding\Python\yud bet\wordle project\wordle.csv")
        self.random_word = str(random.choice(self.df["word"])).lower()
        self.guesses = 6

    def guess(self, user_guess=None):
        if self.guesses <= 0:
            print("no guesses remaining => you lost!")
            return True
        
        if user_guess is None:
            user_guess = input("enter your guess: ")

        if len(user_guess) != 5:
            print("word must be 5 letters long. try again")
            return False

        if not does_word_exist(user_guess):
            print("Invalid word. try again")
            return False

        self.guesses -= 1

        feedback = []
        for i, char in enumerate(user_guess):
            letter = f" {char.upper()} "
            if char == self.random_word[i]:
                feedback.append(f"{green}{letter}{reset}")
            elif char in self.random_word:
                feedback.append(f"{yellow}{letter}{reset}")
            else:
                feedback.append(f"{black}{letter}{reset}")
        
        print(" ".join(feedback))
        print(f"guesses left: {self.guesses}")
        
        if user_guess == self.random_word:
            print(f"You win! you have won in {7 - self.guesses} guesses")
            return True

        return False

    def play(self):
        while self.guesses > 0:
            won = self.guess()
            if won:
                break
        else:
            print(f"You lost! the correct word was: {self.random_word}")

if __name__ == "__main__":

    g1 = game()
    g1.play()

#https://wordsrated.com/solvers/wordle/ for solver of the wordle