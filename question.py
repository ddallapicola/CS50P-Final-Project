from tabulate import tabulate
import textwrap

class Question:
    
    '''Class to represent a question'''
    def __init__(self, question: str, options: list, answer: list):
        self.question = question
        self.options = options
        self.answer = answer

    def __str__(self):
        list_opt_ans = []
        # Printing statement, breaking line every 80 characters.
        wraped_str = '\n'.join(textwrap.wrap(self.question, width=100))
        wraped_str =  f"\033[1m{wraped_str}\033[0m"
        print(wraped_str)
        # Appending correct options to list, breaking line every 80 characters
        opt_count = 0
        for i, a in enumerate(list(self.answer)):
            wraped_str = '\n'.join(textwrap.wrap(a, width=90))
            list_opt_ans.append((i+1,"Correct", wraped_str))
            opt_count += 1
        # Appending wrong options to list, breaking line every 80 characters.
        for o in list(self.options):
            if o not in list(self.answer):
                wraped_str = '\n'.join(textwrap.wrap(o, width=90))
                list_opt_ans.append((opt_count+1, "Wrong", wraped_str))
                opt_count += 1
        # Returning a table with the question, correct and wrong answers.
        return tabulate(list_opt_ans)

    def __repr__(self):
        return f'{self.question},{self.options},{self.answer}'

    def __eq__(self, other):
        if not isinstance(other, Question):
            return False
        return (self.question == other.question and
                self.options == other.options and
                self.answer == other.answer)

    def get_opt_list(self) -> list:
         # Method to get option lists sorted by correctness. No formatting. Useful for reference when selecting
         # between __str__ list.
        opt_list = []
        for o in self.options:
            if o in self.answer:
                opt_list.append(o)
        for o in self.options:
            if o not in self.answer:
                opt_list.append(o)
        return opt_list

