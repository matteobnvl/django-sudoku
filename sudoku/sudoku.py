import random

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

    def generate(self, niveau):
        tab = [[0] * 9 for _ in range(9)]
        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for j in range(9):
            shift = (j % 3) * 3
            for i in range(9):
                tab[j][i] = numbers[(shift + i + (j // 3)) % 9]

        grille = [row.copy() for row in tab]

        #case vide en fonction des niveaux
        if niveau == "easy":
            case_vide = 30
        elif niveau == "medium":
            case_vide = 40
        elif niveau == "difficult":
            case_vide = 50

        for k in range(case_vide):
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            tab[j][i] = 0

        self.tableau = tab
        self.solution = self.solve_sudoku(tab)
        self.niveau = niveau

    #appeler generate niveau "difficult" / niveau "difficult"
    def generate_medium(self):
        
        self.generate_medium("medium")

    def generate_difficult(self):
       
        self.generate("difficult")

    #logique de résolution de Sudoku 
    def solve_sudoku(self, grille):
        
        return grille


if __name__ == "__main__":
    # Générer Sudoku avec le niveau "easy"
    sudoku_easy = SudokuEntity()
    sudoku_easy.generate("easy")

    print("Sudoku Easy")
    print("========================")
    for ligne in sudoku_easy.tableau:
        print(ligne)

    print("\nSolution:")
    for i in sudoku_easy.solution:
        print(i)
    print("========================")
    print(sudoku_easy.tableau)


