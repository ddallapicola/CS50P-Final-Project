import csv, sys, random, ast
from question import Question

def main():
    # Load questions from csv file:
    questions = _load_questions("questions.csv")
    # Display user menu:
    menu(questions, "questions.csv")

#################################################################################
### User options functions ######################################################
#################################################################################

def menu(questions: list, csv_file: str) -> None:
    while True:
        # Display user menu:
        print("""
#############################################
###### Welcome to your test generator. ######
#############################################

Select what you want to do:
        """)
        print("1. Add a question to the database.") # OK
        print("2. Visualize questions.")            # OK
        print("3. Edit a question.")
        print("4. Delete a question.")
        print("5. Generate a test.")
        print("6. Exit.\n")

        # Call users choice function:
        while True:
            try:
                option = input("Enter the number of the option you want to select: ")
            except ValueError:
                print("Invalid option. Try again.")
                continue
            if option not in ["1", "2", "3", "4", "5", "6"]:
                print("Invalid option. Try again.")
            else:
                break
        match option:
            case "1":
                add_question(questions, csv_file)
            case "2":
                _visualize_questions(questions, csv_file)
                _enter_to_menu()
            case "3":
                edit_question(questions, csv_file)
            case "4":
                delete_question(questions, csv_file)
            case "5":
                generate_test(questions, csv_file)
            case "6":
                sys.exit("Goodbye!")

def add_question(q_list: list, csv_file: str) -> None:
    while True:
        # Get question statement, options and answers:
        question = _input_q_statment()
        options, answers = _get_list_opts_anss()
        new_q = Question(question, options, answers)
        q_list.append(new_q)
        # Append new question to csv file:
        with open(csv_file, "a") as file:
            writer = csv.writer(file)
            writer.writerow([new_q.question, new_q.options, new_q.answer])
        print("\nQuestion added successfully.")
        cont_add = input("\nDo you want to add another question (y/n)? ")
        if cont_add not in ["y", "n"]:
            print("Invalid option. Try again.")
        elif cont_add == "y":
            continue
        else:
            print("Backing to menu...")
            break

def edit_question(q_list: list, csv_file: str) -> None:
    go_to_menu = False # Variable to control if user wants to go back to menu.
    print("Here are the questions in the database:")
    # Choose question to edit:
    q = _choose_question(q_list, csv_file)
    while True:
        # Print the question to be edited:
        print(f"\nQuestion to be edited:\n")
        print(f"{q}")
        # As for the user to choose what to edit.
        print("\nWhat do you want to edit?\n\n1. The question statement\n2. A certain option\n3. The correctness of an answer\n4. Back to menu\n")
        while True:
            try:
                choice = int(input("Enter the number of the option you want to select: "))
            except ValueError:
                print("Invalid option. Try again.")
                continue
            if choice not in [1, 2, 3, 4]:
                print("Invalid option. Try again.")
                pass
            else:
                match choice:
                    case 1:
                        while True:
                            print(f"Actual question statement:\n{q.question}\n")
                            q.question = _input_q_statment(inp="Enter the new question statement: ")
                            cont = _keep_edit(what_to_keep="editing the question statement")
                            if cont == False:
                                break
                    case 2:
                        while True:
                            q = _edit_q_option(q) # Returns q with the edited option.
                            cont = _keep_edit(what_to_keep="editing othes options of the same question")
                            if cont == False:
                                break
                    case 3:
                        while True:
                            q = _edit_q_correctness(q)
                            cont = _keep_edit(what_to_keep="editing correctness of the same question")
                            if cont == False:
                                break
                    case 4:
                        go_to_menu = True
                break
        # Rewrite csv file:
        _csv_rewrite(q_list, csv_file)
        if go_to_menu == False:
            print("\nQuestion edited successfully.")
        else:
            print("\nBacking to menu...")
            break
        cont_edit = input("\nDo you want to edit other features of this question (y/n)? ")
        if cont_edit not in ["y", "n"]:
            print("Invalid option. Try again.")
        elif cont_edit == "y":
            continue
        else:
            print("Backing to menu...")
            break

def delete_question(q_list: list, csv_file: str) -> None:
    print("Here are the questions in the database:")
    # Choose question to deelete:
    q = _choose_question(q_list, csv_file)
    while True:
        # Print the question to be edited:
        print(f"\nQuestion to be deleted:\n")
        print(f"{q}")
        # As for the user to choose what to edit.
        while True:
            choice = input("\nAre you sure you want to delete this question (y/n)?\n")
            if choice not in ["y", "n"]:
                print("Invalid option. Try again.")
                continue
            else:
                break
        if choice == "y":
            q_list.remove(q)
            _csv_rewrite(q_list, csv_file)
            print("\nQuestion deleted successfully.")
            break
        else:
            print("\nQuestion not deleted.")
            break  

def generate_test(q_list: list, csv_file: str) -> None:
    print("\nChoose a option:\n\n1. Select questions manually.\n2. Generate a test with random questions.")
    while True: # Loop to check if user input is valid.
        choice = input("\nEnter the number of the option you want to select: ")
        if choice == "1":
            # Display questions to choose from:
            _visualize_questions(q_list, csv_file)
            while True:
                print("Choose the questions you want to add to the test in order, separated by commas.")
                print("Example: 1, 3, 5, 7")
                test_qs = input("Enter the selected questions: ").split(",")
                try:
                    for i in range(len(test_qs)):
                        test_qs[i] = int(test_qs[i].strip())
                except Exception as e:
                    print("\nInvalid option. Try again.\nCertify you are entering only numbers separated by commas and values that are in the list.\n")
                    continue
                # Check if all values of test_qs are in the list questions.
                if all(elem in range(1, len(q_list)+1) for elem in test_qs):
                    break
                else:
                    print("Invalid option. You probably selected a question number that is not in the list. Try again.")
                    continue

            # Creating list with selected questions, randomizing options and turning answers into letters.
            test_statements = []
            test_options = []
            test_answers = []
            for n in test_qs:
                q = q_list[n-1]
                statement = q.question
                options = list(q.options)
                random.shuffle(options)
                answers_letters = []
                for i in range(len(options)):
                    if options[i] in q.answer:
                        answers_letters.append(chr(65+i))
                test_statements.append(statement)
                test_options.append(options)
                test_answers.append(answers_letters)
            # Generating test to a file.
            _test_generator(test_statements, test_options, test_answers)
            while True:
                cont = input("\nDo you want to generate another test (it will erase the actual test) (y/n)? ")
                if cont == "y" or cont == "n":
                    break
                else:
                    print("\nInvalid option. Try again.")
                    continue
            if cont == "y":
                print("\nChoose a option:\n\n1. Select questions manually.\n2. Generate a test with random questions.")
                continue
            else:
                print("\nBacking to menu...")
                break

        elif choice == "2":
            print(f"\nTotal of {len(q_list)} questions in database...")
            while True:
                try:
                    num_qs = int(input(f"\nHow many questions do you want to add to the test? "))
                    if num_qs > len(q_list):
                        print("\nYou can't select more questions than the ones in the database. Try again.")
                        continue
                    elif num_qs <= 0 or num_qs == "":
                        print("\nYou need to select at least one question. Try again.")
                        continue
                    else:
                        break
                except ValueError:
                    print("\nInvalid option. Try again.")
                    continue
            list_q_test = random.sample(q_list, num_qs)
            # Creating list with selected questions, randomizing options and turning answers into letters.
            test_statements = []
            test_options = []
            test_answers = []
            for q in list_q_test:
                test_statements.append(q.question)
                shuffle_options = q.options
                random.shuffle(shuffle_options)
                test_options.append(shuffle_options)
                answers_letters = []
                for i in range(len(shuffle_options)):
                    if shuffle_options[i] in q.answer:
                        answers_letters.append(chr(65+i))
                test_answers.append(answers_letters)
            # Generating test to a file.
            _test_generator(test_statements, test_options, test_answers)
            while True:
                cont = input("\nDo you want to generate another test (it will erase the actual test) (y/n)? ")
                if cont == "y" or cont == "n":
                    break
                else:
                    print("\nInvalid option. Try again.")
                    continue
            if cont == "y":
                print("\nChoose a option:\n\n1. Select questions manually.\n2. Generate a test with random questions.")
                continue
            else:
                print("\nBacking to menu...")
                break
        else:
            print("\nInvalid option. Try again.")

#################################################################################
### Auxiliar functions ##########################################################
#################################################################################

def _input_q_option(inp="\nEnter option: ") -> str:
    while True:
        option = input(inp)
        if option == "":
            print("Option cannot be empty. Try again.")
        else:
            break
    return option

def _input_q_statment(inp='\nEnter the question statement: ') -> str:
# Ask for question statement.
    while True:
        question = input(inp)
        if question == "" or question == " ":
            print("\nQuestion cannot be empty. Try again.")
        else:
            break
    return question

def _edit_q_option(q: Question) -> Question:
    print(f"\nQuestion to be edited:\n")
    print(f"{q}\n") # Print sepparated to avoid spacing bugs.
    opt_list = q.get_opt_list() # List of options as shown in __str__ but without formatting.
    while True:
        try:
            opt_num = int(input("Which option do you want to edit? "))
        except ValueError:
            print("Invalid option. Try again.")
            continue
        if opt_num not in range(1, len(q.options)+1):
            print("Invalid option. Try again.")
        else:
            to_edit = opt_list[opt_num-1]
            new_opt = _input_q_option("\nWhat is the edited version of option? ")
            for i in range(len(q.options)):
                if q.options[i] == to_edit:
                    q.options[i] = new_opt
            for i in range(len(q.answer)):
                if q.answer[i] == to_edit:
                    q.answer[i] = new_opt
                pass
            return q

def _edit_q_correctness(q: Question) -> Question:
    print(f"\nQuestion to be edited:\n")
    print(f"{q}\n") # Print sepparated to avoid spacing bugs.
    opt_list = q.get_opt_list() # List of options as shown in __str__ but without formatting.
    while True:
        try:
            opt_num = int(input("Which option do you want to change the correctness? "))
        except ValueError:
            print("Invalid option. Try again.")
            continue
        if opt_num not in range(1, len(q.options)+1):
            print("Invalid option. Try again.")
        else:
            to_edit = opt_list[opt_num-1]
            if to_edit in q.answer:
                q.answer.remove(to_edit)
                print(f"\nNow the following option is incorrect:\nR.:{to_edit}")
            else:
                q.answer.append(to_edit)
                print(f"\nNow the following option is correct:\nR.:{to_edit}")
                pass
            return q

def _get_list_opts_anss(options=[], answers=[]) -> tuple:
    while True:
        try:
            qnt = int(input("\nHow many options do you want to add? "))
            if qnt <= 0:
                print("\nYou need to add at least one option. Try again.")
                continue
            else:
                break
        except ValueError:
            print("\nInvalid option. Try again.")
            continue
    for _ in range(qnt):
        opt = _input_q_option()
        options.append(opt)
        while True:
            ans = input("Is this a correct answer? (y/n): ")
            if ans == "y":
                answers.append(opt)
                break
            elif ans == "n":
                break
            else:
                print("Invalid input. Try again.")

    return options, answers

def _load_questions(csv_file: str) -> list:
    ''' Checks if the csv file exists. If not, creates it.'''
    try:
        '''Read and filter csv file.'''
        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            next(reader, None) # Skip the header
            raw_list = list(reader) 
            raw_list = [row for row in raw_list if row]
    except FileNotFoundError:
        with open(csv_file, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["question", "options", "answer"])

    '''Create a list of Question objects.'''
    questions = []
    try:
        for row in raw_list:
            # Convert "[a, b, c]" strings to lists [a, b, c]
            try:
                row[1] = ast.literal_eval(row[1])
            except ValueError:
                pass
            try:
                row[2] = ast.literal_eval(row[2])
            except ValueError:
                pass

            questions.append(Question(row[0], row[1], row[2]))
        return questions
    except IndexError:
            sys.exit("CSV does not have the required pattern, Closing program...")

def _visualize_questions(q_list, csv_file) -> None:
    print('\n', end='')
    for q in q_list:
        print(f'--- \033[1mQuestion {q_list.index(q)+1}\033[0m -----------------------------------------------------------------------------------')
        print(f'{q}\n\n')

def _choose_question(q_list, csv_file) -> Question:
    _visualize_questions(q_list, csv_file)
    while True:
        try:
            choice = int(input("Which question do you want to edit? "))
            if choice not in list(range(1, len(q_list)+1)):
                print(f"Invalid option. Try again.{list(range(1, len(q_list)+1))}")
            else:
                return q_list[choice-1]
        except ValueError:
            print("Invalid option. Try again.")
            continue

def _csv_rewrite(q_list: list, csv_file: str) -> None:
    with open(csv_file, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["question", "options", "answer"])
        for q in q_list:
            writer.writerow([q.question, q.options, q.answer])

def _enter_to_menu() -> None:
    while True:
        action = input("Press Enter to back do menu...")
        if action == "":
            print("Backing to menu...")
            break
        else:
            continue

def _keep_edit(what_to_keep: str) -> bool:
    while True:
        cont_edit = input(f"\nDo you want to keep {what_to_keep} (y/n)? ")
        if cont_edit not in ["y", "n"]:
            print("Invalid option. Try again.")
        elif cont_edit == "y":
            return True
        else:
            return False

def _test_generator(test_statements: list, test_options: list, test_answers: list) -> None:
    # Writing test to a file.
    try:
        with open("test.txt", "w") as test:
            test.write("Selected questions:\n\n")
            for i in range(len(test_statements)):
                test.write(f"Question {i+1}: {test_statements[i]}\n")
                for j in range(len(test_options[i])):
                    test.write(f"{chr(65+j)}. {test_options[i][j]}\n")
                test.write("\n")
            test.write("####################################################################\n####################################################################")
            test.write("\n\nAnswers:\n\n")
            for i in range(len(test_answers)):
                test.write(f"Question {i+1}: {test_answers[i]}\n")
        print("\nTest generated successfully. Check the file test.txt.")
    except Exception as e:
        print("\nAn error occurred while generating the test.")

#################################################################################
### if __name__ function ########################################################
#################################################################################

if __name__ == "__main__":
    main()