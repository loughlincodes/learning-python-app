
# Python Quiz App

This Python application is an interactive quiz tool that allows users to select topics and answer questions. The app tracks previous scores and displays a progress bar for each score, giving visual feedback based on performance.

## Features

- Topic-based quizzes with randomized questions.
- ASCII visual progress bars for scores.
- Tracking of past scores in JSON files.
- Dynamic question shuffling.
- Feedback on correct and incorrect answers.
- User-friendly interface with Rich library styling.

## Requirements

- Python 3.x
- `rich` library for table formatting and progress bars.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repo-name
    ```

3. Install the required dependencies from the `requirements.txt` file (ensure the Rich library is installed):

    ```bash
    pip install rich
    ```

4. Ensure you have the necessary JSON files:
   - `questions.json`: Contains quiz questions.
   - `topics.json`: Contains the available topics.
   - `past_scores.json`: Tracks user scores for each topic.

## Usage

1. Run the app by executing the following command:

    ```bash
    python3 main.py
    ```

2. You will be presented with a welcome screen that lists all available topics, the number of questions, and past scores with a visual progress bar.

3. Select a topic to start the quiz. The app will ask up to 10 randomly shuffled questions from the selected topic.

4. After answering each question, you'll receive feedback on whether your answer was correct, followed by your final score at the end of the quiz.

5. The app will save your score to `past_scores.json` and display a personalized message based on your performance.

6. You can opt to take another quiz or exit the app.

## Example JSON Structure

### `questions.json`

```json
{
    "1": {
        "question": "What is the capital of France?",
        "options": {
            "a": "Paris",
            "b": "London",
            "c": "Rome",
            "d": "Berlin"
        },
        "answer": "a",
        "topics": ["geography"]
    }
}
```

### `topics.json`

```json
{
    "1": "geography",
    "2": "math"
}
```

### `past_scores.json`

```json
{
    "1": "80%",
    "2": "90%"
}
```

## Code Structure

- **`Quiz` Class**: Handles quiz logic, including question shuffling, running the quiz, and scoring.
- **`ask_question` Function**: Asks questions to the user, randomizes options, and evaluates the user's response.
- **`load_json_files` Function**: Loads data from JSON files (`questions.json`, `topics.json`, `past_scores.json`).
- **`create_compiled_data` Function**: Compiles questions, topics, and scores into a single data structure.
- **`get_ascii_progress_bar` Function**: Generates an ASCII progress bar based on the percentage score.
- **`print_welcome_page` Function**: Displays the welcome screen with available topics and past scores.
- **`validated_input` Function**: Ensures valid input is provided by the user.



## License

This project is open source and available under the LMS license which means that if you actually use any of the above code I will call to your home and ask you (very politely) why?
