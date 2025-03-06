import requests
import random
import json
from io import BytesIO
from PIL import Image, ImageTk

BACKEND_URL = ""  # TODO: fill in correct URL


def load_questions(file_path='source/fetchQA/questions.json'):
    """Loads questions from a local JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Questions file not found at {file_path}.")
        return []

def fetch_qa_temp(lvl):
    questions = load_questions()
    questions = [q for q in questions if q['level'] == lvl]
    print(f"Fetched {len(questions)} questions for level {lvl}.")
    return questions if questions else []

def fetch_questions_from_backend(level):
    """
    Fetches all questions for a specific level from the backend.
    """
    try:
        response = requests.get(f'{BACKEND_URL} level={level}', timeout=5)  # TODO: is the level chosen here?
        if response.status_code == 200:  # TODO: check actual value with backend team
            data = response.json()
            return data.get('questions', [])
    except requests.RequestException as e:
        print(f'An error occurred while fetching questions: {e}')
        return []


def generate_random_question(level):
    """
    Randomly selects a question for the specific level.
    """
    questions = fetch_qa_temp(level)
    if questions:
        return random.choice(questions)
    else:
        return {'query': "No questions available", 'ans': ""}


def load_image_from_url(url, size=(350, 350)):
    """Fetch an image from a URL and return a PhotoImage object."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an error if the request fails

        image_data = BytesIO(response.content)  # Convert response content to a file-like object
        image = Image.open(image_data)  # Open the image using PIL
        image = image.resize(size, Image.LANCZOS)  # Resize to 350x350 using high-quality resampling
        return ImageTk.PhotoImage(image)  # Convert it to a Tkinter-compatible format
    except requests.RequestException as e:
        print(f"Failed to load image: {e}")
        return None  # Return None if there's an issue