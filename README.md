# Test Generator  

#### Video Demo: <[https://www.youtube.com/watch?v=vZrxWDC5iAs]>  

## Description  

### Motivation  

As of March 2025, I am pursuing a master's degree in psychology. One of my responsibilities as a student is assisting my advisor in classes. In a recent class, I helped plan tests for students and had an idea: *"It would be useful to have a database of questions to build and generate customized or random tests automatically."* With that in mind, I decided to develop a prototype as my final project for CS50.  

### General Description  

The program is built primarily using Object-Oriented Programming (OOP) principles. It relies on a single `class` to handle questions to generate the test in a txt file `test.txt`. 

The `main()` function starts by loading the question database from `questions.csv`. By default, the program includes an example dataset with simple test questions. If the `questions.csv` file does not exist, the program creates it. If the file exists but contains no questions, the program starts with an empty database that can be filled by the user.  

Once the database is loaded or created, the program calls the `menu()` function, which runs in a loop and serves as the main interface, ensuring that different functionalities can be accessed without causing a stack overflow. The menu presents six main options:  

## Features  

1. **Add a Question**  
   - Allows users to add a new question to the database (`questions.csv`).  
   - Prompts the user to enter the question statement, the number of answer options, and the correct option(s).  
   - After adding a question, the program asks if the user wants to add another one. If not, it returns to the main `menu()`.  

2. **View Questions**  
   - Displays all stored questions in an enumerated ASCII table format.  
   - Shows the question statement, available options, and the correct answer(s).  
   - Pressing `Enter` returns to the main `menu()`.  

3. **Edit a Question**  
   - Lists all questions and allows the user to select one for editing.  
   - The user can modify:  
     1. The question statement  
     2. A specific answer option  
     3. The correctness of an answer option  
   - After each edit, the program asks whether the user wants to continue editing the same question. If not, it returns to the main `menu()`.  

4. **Delete a Question**  
   - Lists all questions and allows the user to select one for deletion.  
   - The user can confirm or decline the deletion.  
   - If confirmed, the question is removed, and the program asks if the user wants to delete another question. If not, it returns to the main `menu()`.  

5. **Generate a Test**  
   - Creates a test from the question database, either manually or randomly.  
   - **Manual Selection:** The program lists all available questions, and the user selects the ones to include in the test.  
   - **Random Selection:** The program asks for the number of questions to include and selects them randomly.  
   - The generated test is saved in a `test.txt` file, where:  
     - Answer options are randomly ordered and labeled (A., B., C., etc.).  
     - Correct answers are listed at the end of the file (e.g., Question 1: ['A', 'B']).  
   - After generating the test, the program asks if the user wants to create another test, replacing the previous one. If not, it returns to the main `menu()`.  

6. **Exit Program**  
   - Closes the program.  