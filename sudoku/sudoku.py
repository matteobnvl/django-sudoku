import random
import json

class SudokuEntity:
    def __init__(self, niveau="easy"):
        self._tableau = []
        self._solution = []
        self._niveau = niveau

    @property
    def tableau(self):
        return self._tableau

    @tableau.setter
    def tableau(self, value):
        self._tableau = value

    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, value):
        self._solution = value

    @property
    def niveau(self):
        return self._niveau

    @niveau.setter
    def niveau(self, value):
        self._niveau = value

    def generate(self):
        tab = [[0] * 9 for _ in range(9)]
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for j in range(9):
            shift = (j % 3) * 3
            for i in range(9):
                tab[j][i] = numbers[(shift + i + (j // 3)) % 9]
        grille = [row.copy() for row in tab]
        if self._niveau == "easy":
            case_vide = 30
        elif self._niveau == "medium":
            case_vide = 40
        elif self._niveau == "hard":
            case_vide = 50
            
        k = 1
        while (k != case_vide):
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if tab[j][i] == 0:
                continue
            tab[j][i] = 0
            k += 1
        self._tableau = json.dumps(tab, separators=(',', ':'))
        self._solution = json.dumps(grille, separators=(',', ':'))
        print(len(self.tableau))

    #logique de résolution de Sudoku 
    def solve_sudoku(self, grille):
        
        return grille


