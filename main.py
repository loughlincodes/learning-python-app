import json
import os
import random
from rich import *
from rich.table import Table
from rich.console import Console
from rich import box


class Quiz():
    """ Represents a Quiz based on the compiled data and a specified topic """
    
    def __init__(self, topic_id, compiled_data, questions):
        """ Initialise the Quiz instance """
        self.topic_id = topic_id
        self.compiled_data = compiled_data
        self.questions = questions
        self.questions_to_ask = compiled_data[topic_id]['question-ids']

        random.shuffle(self.questions_to_ask)

    def run_quiz(self):
        """ Class method to run the Quiz instance and returns the score """

        score = 0
        range_size = min(10, len(self.questions_to_ask))
        for index in range(range_size):
            current_question = self.questions.get(self.questions_to_ask[index])
            clear()
            # The ask_question function runs and returns True/False
            if ask_question(current_question, index + 1, range_size):
                score += 1
            input('Enter any key to continue')
        
        return score, range_size
    
def ask_question(question, question_number, total_questions):
        """ Ask the question passed in to the user and returns True/False """

        # create an empty list
        options = []
        for option in question['options'].values():
            options.append(option)
        random.shuffle(options)
        
        # Create an empty list that will be populated with the question's options and then shuffled
        letters = ('a','b','c','d','e','f','g')

        # the shuffled_options dictionary will have the options in random order
        shuffled_options = {}
        for index in range(len(options)):
            shuffled_options[letters[index]] = options[index]

        # Print the question prompt
        print(f' - ({question_number}/{total_questions}) {question["question"]}')

        # Print shuffled_options for the user to choose from
        for key, value in shuffled_options.items():
            print(f'\t{key}. {value}')
        
        # Define the correct_answer from the questions object
        correct_answer = question['options'][question['answer']]
        # Prompt user for input by usingthe validated_input function
        user_input = validated_input('Enter your answer (\'q\' to quit): ', list(shuffled_options.keys()))
        # Define the user_anser from suffled_options
        user_answer = shuffled_options[user_input]

        # Compare answers and return True/False
        if user_answer == correct_answer:
            print('\nThat\'s correct! GOod job!\n')
            return True
        else:
            print(f'\nYou almost got it! The right answer is "{correct_answer}".\n')
            return False




def load_json_files(*file_names):
    """ Receives one or more file names and returns the content of each file as a list """

    resulting_loads = []
    for file in file_names:
        with open(file) as file_object:
            current_load = json.load(file_object)
            resulting_loads.append(current_load)
    
    return resulting_loads

def create_compiled_data(questions, topics, past_scores):
    """ Create compiled data from the contents loaded from the 
    questions, topics and past_scores files """

    compiled_data = {}
    for number, topic in topics.items():
        compiled_data[number] = { 'topic': topic }
    
    compiled_data[str(len(compiled_data) + 1)] = { 'topic': 'all'}
    for data_key, data_value in compiled_data.items():

        data_value["question-ids"] = []
        if data_value["topic"] != 'all':
            for key, value in questions.items():
                if data_value["topic"] in value["topics"]:
                    data_value["question-ids"].append(key)
        else:
            print("in else")
            for key, value in questions.items():
                data_value["question-ids"].append(key)
        
        data_value['questions-count'] = len(data_value['question-ids'])
        data_value['past-score'] = past_scores.get(data_key)

    return compiled_data

def clear():
    arg = 'cls' if os.name == 'nt' else 'clear'
    os.system(arg) 

# Function to generate the ASCII progress bar
def get_ascii_progress_bar(score, total_blocks=10):
    # Retrieve and strip the percentage sign, then convert to an integer
    score = str(score).replace('%', '')  # Strip '%' if present
    try:
        score = int(score)  # Convert to integer
    except ValueError:
        score = 0  # Handle invalid values

    filled_blocks = int(score / 100 * total_blocks)  # Calculate the number of solid blocks
    empty_blocks = total_blocks - filled_blocks      # Remaining lighter blocks
    solid_block = "█"  # Solid block
    light_block = "░"  # Lighter block
    return solid_block * filled_blocks + light_block * empty_blocks

def print_welcome_page(compiled_data):
    """ Print the welcome page """

    print('Welcome to your Python Learning App!\n')
    print('Select a topic to review and you will be asked a mox of 10 questions per run. Good luck!')


    console = Console()

    table = Table(box=box.HEAVY_EDGE, width=90, show_lines=True)

    # Table title
    table.add_column("Topic", style="cyan")
    table.add_column("Questions", style="magenta")
    table.add_column("% Score", style="green")
    table.add_column("Visual Score", style="cyan")

    
    #print table rows
    for key, value in compiled_data.items():
        score = value.get('past-score', 0)
        score = str(score).replace('%', '')
        if score == "None":
            score = 0

        progress_bar = get_ascii_progress_bar(score)  # Generate ASCII progress bar
        table.add_row(
            f'{key}. {value["topic"].title()}',  
            str(value['questions-count']),
            f'{score}%',
            f'{progress_bar}'                         
        )
    
    console.print(table)



def validated_input(prompt, valid_options, value_to_quit='q'):
    user_input = input(prompt)
    flag = True
    while flag:
        if user_input == value_to_quit:
            raise SystemExit
        elif user_input not in valid_options:
            user_input = input(f'Please enter a valid option or \'{value_to_quit}\' to quit: ')
        else:
            return user_input
    

   

def main():
    """ Runs main code """

    while True:
        questions_file = 'questions.json'
        topics_file = 'topics.json'
        past_scores_file = 'past_scores.json'

        questions, topics, past_scores = load_json_files(questions_file, topics_file, past_scores_file)

        compiled_data = create_compiled_data(questions, topics, past_scores)

        clear()

        print_welcome_page(compiled_data)

        topic_id = validated_input('\nEnter the topic you want to review (\'q\' to quit): ', list(compiled_data.keys()))

        chosen_quiz = Quiz(topic_id, compiled_data, questions)

        # Execute the run_quiz method
        score, range_size = chosen_quiz.run_quiz()

        clear()

        final_score = int(100 * score / range_size)

        past_scores[topic_id] = str(final_score) + '%'

        console = Console()

        with open('past_scores.json', 'w') as file_object:
            json.dump(past_scores, file_object)

        if final_score == 100:
            console.print(f'\n[bold green]Unbelievable![/bold green] You scored {final_score}%!\n')
        elif final_score >= 90:
            console.print(f'\n[bold yellow]Excellent job![/bold yellow] You scored {final_score}%!\n')
        elif final_score >= 80:
            console.print(f'\n[bold cyan]Awesome![/bold cyan] You scored {final_score}%!\n')
        else:
            console.print(f'\n[bold red]You scored {final_score}%.[/bold red] Time to visit LeetCode for more practice!\n')
            
        another_try = input('Enter \'Y\' to run the app again, any other key to exit: ').lower()
        if another_try != 'y':
            break


if __name__ == '__main__':
    main()
