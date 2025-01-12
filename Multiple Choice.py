from flask import Flask, request, jsonify, render_template
import random
import uuid
import json
import os
import socket

app = Flask(__name__)


# Default settings
NUM_QUESTIONS = 30
DEFAULT_QUIZ_TIME = 90
DEFAULT_LIVES = 3

NUM_QUESTIONS = 30  # Default number of questions
QUIZ_TIME = 90  # Default time in seconds
# Define categories
# Define verbs, voices, tenses, and forms
verbs = ["λύω"]  # Add more verbs as needed
voices = ["ενεργητική", "μέση"]
tenses = ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"]
# Restrict valid tenses for special forms
valid_tenses = ["ενεστώτας", "μέλλοντας", "αόριστος", "παρακείμενος"]
valid_genders = ["αρσενικό", "θηλυκό", "ουδέτερο"]  # For μετοχή only
forms = [
    "α ενικό", "β ενικό", "γ ενικό",
    "α πληθυντικό", "β πληθυντικό", "γ πληθυντικό"
]
special_forms = ["απαρέμφατο", "μετοχή"]

tenses_by_level = {
    1: {"tenses": ["ενεστώτας", "μέλλοντας"], "voices": ["ενεργητική"]},
    2: {"tenses": ["παρατατικός", "αόριστος"], "voices": ["ενεργητική"]},
    3: {"tenses": ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος"], "voices": ["ενεργητική"]},
    4: {"tenses": ["παρακείμενος", "υπερσυντέλικος"], "voices": ["ενεργητική"]},
    5: {"tenses": ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"], "voices": ["ενεργητική"]},
    6: {"tenses": ["ενεστώτας", "μέλλοντας"], "voices": ["μέση"]},
    7: {"tenses": ["αόριστος", "παρατατικός"], "voices": ["μέση"]},
    8: {"tenses": ["ενεστώτας", "αόριστος", "μέλλοντας", "παρατατικός"], "voices": ["μέση"]},
    9: {"tenses": ["παρακείμενος", "υπερσυντέλικος"], "voices": ["μέση"]},
    10: {"tenses": ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"], "voices": ["μέση"]},
    11: {"tenses": ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"], "voices": ["ενεργητική", "μέση"]},
    12: {"tenses": ["απαρέμφατο", "μετοχή"], "voices": ["ενεργητική"]},  # New Level 12 (active)
    13: {"tenses": ["απαρέμφατο", "μετοχή"], "voices": ["μέση"]},  # New Level 13 (middle)
    14: {"tenses": ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"], "voices": ["ενεργητική", "μέση", "απαρέμφατο", "μετοχή"]},  # New Level 14 (everything)
    15: {"tenses": tenses, "voices": voices},  # Level 15
}


correct_answers = { 
    # Ενεστώτας Ενεργητική (Present Active)
    ("α ενικό", "ενεργητική", "ενεστώτας"): ["ω"],
    ("β ενικό", "ενεργητική", "ενεστώτας"): ["εις"],
    ("γ ενικό", "ενεργητική", "ενεστώτας"): ["ει"],
    ("α πληθυντικό", "ενεργητική", "ενεστώτας"): ["ομεν"],
    ("β πληθυντικό", "ενεργητική", "ενεστώτας"): ["ετε"],
    ("γ πληθυντικό", "ενεργητική", "ενεστώτας"): ["ουσιν"],

    # Παρατατικός Ενεργητική (Imperfect Active)
    ("α ενικό", "ενεργητική", "παρατατικός"): ["ον"],
    ("β ενικό", "ενεργητική", "παρατατικός"): ["ες"],
    ("γ ενικό", "ενεργητική", "παρατατικός"): ["ε"],
    ("α πληθυντικό", "ενεργητική", "παρατατικός"): ["ομεν"],
    ("β πληθυντικό", "ενεργητική", "παρατατικός"): ["ετε"],
    ("γ πληθυντικό", "ενεργητική", "παρατατικός"): ["ον"],

    # Μέλλοντας Ενεργητική (Future Active)
    ("α ενικό", "ενεργητική", "μέλλοντας"): ["σω"],
    ("β ενικό", "ενεργητική", "μέλλοντας"): ["σεις"],
    ("γ ενικό", "ενεργητική", "μέλλοντας"): ["σει"],
    ("α πληθυντικό", "ενεργητική", "μέλλοντας"): ["σομεν"],
    ("β πληθυντικό", "ενεργητική", "μέλλοντας"): ["σετε"],
    ("γ πληθυντικό", "ενεργητική", "μέλλοντας"): ["σουσιν"],

    # Αόριστος Ενεργητική (Aorist Active)
    ("α ενικό", "ενεργητική", "αόριστος"): ["σα"],
    ("β ενικό", "ενεργητική", "αόριστος"): ["σας"],
    ("γ ενικό", "ενεργητική", "αόριστος"): ["σε"],
    ("α πληθυντικό", "ενεργητική", "αόριστος"): ["σαμεν"],
    ("β πληθυντικό", "ενεργητική", "αόριστος"): ["σατε"],
    ("γ πληθυντικό", "ενεργητική", "αόριστος"): ["σαν"],

    # Παρακείμενος Ενεργητική (Perfect Active)
    ("α ενικό", "ενεργητική", "παρακείμενος"): ["κα"],
    ("β ενικό", "ενεργητική", "παρακείμενος"): ["κας"],
    ("γ ενικό", "ενεργητική", "παρακείμενος"): ["κε"],
    ("α πληθυντικό", "ενεργητική", "παρακείμενος"): ["καμεν"],
    ("β πληθυντικό", "ενεργητική", "παρακείμενος"): ["κατε"],
    ("γ πληθυντικό", "ενεργητική", "παρακείμενος"): ["κασιν"],

    # Υπερσυντέλικος Ενεργητική (Pluperfect Active)
    ("α ενικό", "ενεργητική", "υπερσυντέλικος"): ["κειν"],
    ("β ενικό", "ενεργητική", "υπερσυντέλικος"): ["κεις"],
    ("γ ενικό", "ενεργητική", "υπερσυντέλικος"): ["κει"],
    ("α πληθυντικό", "ενεργητική", "υπερσυντέλικος"): ["κεμεν"],
    ("β πληθυντικό", "ενεργητική", "υπερσυντέλικος"): ["κετε"],
    ("γ πληθυντικό", "ενεργητική", "υπερσυντέλικος"): ["κεσαν"],

    # Ενεστώτας Μέση (Present Middle)
    ("α ενικό", "μέση", "ενεστώτας"): ["ομαι"],
    ("β ενικό", "μέση", "ενεστώτας"): ["ῃ", "ει"],
    ("γ ενικό", "μέση", "ενεστώτας"): ["εται"],
    ("α πληθυντικό", "μέση", "ενεστώτας"): ["ομεθα"],
    ("β πληθυντικό", "μέση", "ενεστώτας"): ["εσθε"],
    ("γ πληθυντικό", "μέση", "ενεστώτας"): ["ονται"],

    # Παρατατικός Μέση (Imperfect Middle)
    ("α ενικό", "μέση", "παρατατικός"): ["ομην"],
    ("β ενικό", "μέση", "παρατατικός"): ["ου"],
    ("γ ενικό", "μέση", "παρατατικός"): ["ετο"],
    ("α πληθυντικό", "μέση", "παρατατικός"): ["ομεθα"],
    ("β πληθυντικό", "μέση", "παρατατικός"): ["εσθε"],
    ("γ πληθυντικό", "μέση", "παρατατικός"): ["οντο"],

    # Μέλλοντας Μέση (Future Middle)
    ("α ενικό", "μέση", "μέλλοντας"): ["σομαι"],
    ("β ενικό", "μέση", "μέλλοντας"): ["σῃ", "σει"],
    ("γ ενικό", "μέση", "μέλλοντας"): ["σεται"],
    ("α πληθυντικό", "μέση", "μέλλοντας"): ["σομεθα"],
    ("β πληθυντικό", "μέση", "μέλλοντας"): ["σεσθε"],
    ("γ πληθυντικό", "μέση", "μέλλοντας"): ["σονται"],

    # Αόριστος Μέση (Aorist Middle)
    ("α ενικό", "μέση", "αόριστος"): ["σαμην"],
    ("β ενικό", "μέση", "αόριστος"): ["σω"],
    ("γ ενικό", "μέση", "αόριστος"): ["σατο"],
    ("α πληθυντικό", "μέση", "αόριστος"): ["σαμεθα"],
    ("β πληθυντικό", "μέση", "αόριστος"): ["σασθε"],
    ("γ πληθυντικό", "μέση", "αόριστος"): ["σαντο"],

    # Παρακείμενος Μέση (Perfect Middle)
    ("α ενικό", "μέση", "παρακείμενος"): ["μαι"],
    ("β ενικό", "μέση", "παρακείμενος"): ["σαι"],
    ("γ ενικό", "μέση", "παρακείμενος"): ["ται"],
    ("α πληθυντικό", "μέση", "παρακείμενος"): ["μεθα"],
    ("β πληθυντικό", "μέση", "παρακείμενος"): ["σθε"],
    ("γ πληθυντικό", "μέση", "παρακείμενος"): ["νται"],

    # Υπερσυντέλικος Μέση (Pluperfect Middle)
    ("α ενικό", "μέση", "υπερσυντέλικος"): ["μην"],
    ("β ενικό", "μέση", "υπερσυντέλικος"): ["σο"],
    ("γ ενικό", "μέση", "υπερσυντέλικος"): ["το"],
    ("α πληθυντικό", "μέση", "υπερσυντέλικος"): ["μεθα"],
    ("β πληθυντικό", "μέση", "υπερσυντέλικος"): ["σθε"],
    ("γ πληθυντικό", "μέση", "υπερσυντέλικος"): ["ντο"],

    # Απαρέμφατο (Infinitives)
    ("απαρέμφατο", "ενεργητική", "ενεστώτας"): ["ειν"],
    ("απαρέμφατο", "ενεργητική", "μέλλοντας"): ["σειν"],
    ("απαρέμφατο", "ενεργητική", "αόριστος"): ["σαι"],
    ("απαρέμφατο", "ενεργητική", "παρακείμενος"): ["κεναι"],
    ("απαρέμφατο", "μέση", "ενεστώτας"): ["εσθαι"],
    ("απαρέμφατο", "μέση", "μέλλοντας"): ["σεσθαι"],
    ("απαρέμφατο", "μέση", "αόριστος"): ["σασθαι"],
    ("απαρέμφατο", "μέση", "παρακείμενος"): ["σθαι"],

    # Μετοχή Ενεργητική (Active Participles)
    ("μετοχή", "ενεργητική", "ενεστώτας", "αρσενικό"): ["ων"],
    ("μετοχή", "ενεργητική", "ενεστώτας", "θηλυκό"): ["ουσα"],
    ("μετοχή", "ενεργητική", "ενεστώτας", "ουδέτερο"): ["ον"],
    ("μετοχή", "ενεργητική", "αόριστος", "αρσενικό"): ["σας"],
    ("μετοχή", "ενεργητική", "αόριστος", "θηλυκό"): ["σασα"],
    ("μετοχή", "ενεργητική", "αόριστος", "ουδέτερο"): ["σαν"],
    ("μετοχή", "ενεργητική", "παρακείμενος", "αρσενικό"): ["κως"],
    ("μετοχή", "ενεργητική", "παρακείμενος", "θηλυκό"): ["κυια"],
    ("μετοχή", "ενεργητική", "παρακείμενος", "ουδέτερο"): ["κος"],

    # Μετοχή Μέση (Middle Participles)
    ("μετοχή", "μέση", "ενεστώτας", "αρσενικό"): ["ομενος"],
    ("μετοχή", "μέση", "ενεστώτας", "θηλυκό"): ["ομενη"],
    ("μετοχή", "μέση", "ενεστώτας", "ουδέτερο"): ["ομενον"],
    ("μετοχή", "μέση", "αόριστος", "αρσενικό"): ["σαμενος"],
    ("μετοχή", "μέση", "αόριστος", "θηλυκό"): ["σαμενη"],
    ("μετοχή", "μέση", "αόριστος", "ουδέτερο"): ["σαμενον"],
    ("μετοχή", "μέση", "παρακείμενος", "αρσενικό"): ["μενος"],
    ("μετοχή", "μέση", "παρακείμενος", "θηλυκό"): ["μενη"],
    ("μετοχή", "μέση", "παρακείμενος", "ουδέτερο"): ["μενον"]
}
# Store for questions answered incorrectly
incorrect_questions = []

# Route to get the game home screen
@app.route("/")
def home():
    return render_template("index.html")

# Helper function to generate general questions
def generate_general_question(level):
    form = random.choice(forms)
    voice = random.choice(voices)
    tense = random.choice(tenses)
    verb = random.choice(verbs)

    key = (form, voice, tense)
    correct_answer = correct_answers.get(key, ["ω"])

    if correct_answer:
        options = [correct_answer[0]] + generate_incorrect_options(correct_answer, voice, tense)
        random.shuffle(options)

        return {
            "question_text": f"Ποια είναι η σωστή κατάληξη για το ρήμα '{verb}' στον {tense} ({voice}) και {form};",
            "options": options,
            "correct": correct_answer[0]
        }
    return None


def generate_valid_questions(voices, tenses, forms):
    valid_questions = []
    for key, correct_list in correct_answers.items():
        form, voice, tense = key[:3]
        # Skip if the voice or tense isn't in the selected filters
        if voice not in voices or tense not in tenses:
            continue

        # Check forms: Skip if form isn't in selected or default forms
        if form not in forms:
            continue

        # Generate a question if valid
        question = generate_question(voice, tense, form)
        if question:
            valid_questions.append(question)

    print(f"[DEBUG] Valid questions generated: {len(valid_questions)}")
    return valid_questions


# Function to generate a question for "απαρέμφατο"
def generate_aparemfato_question(level):
    voice = "ενεργητική" if level == 12 else "μέση"
    available_keys = [
        k for k in correct_answers.keys()
        if k[0] == "απαρέμφατο" and k[1] == voice
    ]
    if not available_keys:
        return None

    selected_key = random.choice(available_keys)
    form, voice, tense = selected_key[:3]
    correct_answer = correct_answers.get(selected_key, [])

    # Generate incorrect options
    incorrect_options = generate_level_incorrect_options(correct_answer, "απαρέμφατο", voice, tense)
    options = [correct_answer[0]] + incorrect_options
    random.shuffle(options)

    question_text = f"Ποια είναι η σωστή κατάληξη για το απαρέμφατο ({voice}, {tense})?"

    return {
        "question_text": question_text,
        "options": options,
        "correct": correct_answer[0],
    }


# Function to generate a question for "μετοχή"
def generate_metoxi_question(level):
    """
    Generate a question for 'μετοχή' based on the level.
    """
    voice = "ενεργητική" if level == 12 else "μέση"
    available_keys = [
        k for k in correct_answers.keys()
        if k[0] == "μετοχή" and k[1] == voice
    ]
    if not available_keys:
        return None

    selected_key = random.choice(available_keys)
    form, voice, tense, gender = selected_key
    correct_answer = correct_answers.get(selected_key, [])

    # Generate incorrect options
    incorrect_options = generate_incorrect_options(correct_answer, voice, tense, "μετοχή", gender)
    options = [correct_answer[0]] + incorrect_options
    random.shuffle(options)

    question_text = f"Ποια είναι η σωστή κατάληξη για τη μετοχή ({voice}, {tense}, {gender})?"

    return {
        "question_text": question_text,
        "options": options,
        "correct": correct_answer[0],
    }
# Function to generate a question for Level 12 (απαρέμφατο and μετοχή in ενεργητική)
def generate_level_12_question():
    voice = "ενεργητική"
    available_keys = [k for k in correct_answers.keys() if k[0] in ["απαρέμφατο", "μετοχή"] and k[1] == voice]

    if not available_keys:
        print("[DEBUG] No available keys for Level 12.")
        return None

    selected_key = random.choice(available_keys)
    form, voice, tense, *gender = selected_key

    correct_option = correct_answers[selected_key][0]
    incorrect_options = generate_incorrect_options(correct_answers[selected_key], voice, tense, form, gender[0] if gender else None)
    options = [correct_option] + incorrect_options
    random.shuffle(options)

    question_text = f"Ποια είναι η σωστή κατάληξη για το {form} ({voice}, {tense})"
    if form == "μετοχή" and gender:
        question_text += f", {gender[0]}"

    return {
        "question_text": question_text,
        "options": options,
        "correct": correct_option,
    }

def generate_level_13_question():
    voice = "μέση"
    available_keys = [k for k in correct_answers.keys() if k[0] in ["απαρέμφατο", "μετοχή"] and k[1] == voice]

    if not available_keys:
        print("[DEBUG] No available keys for Level 13.")
        return None

    selected_key = random.choice(available_keys)
    form, voice, tense, *gender = selected_key

    correct_option = correct_answers[selected_key][0]
    incorrect_options = generate_incorrect_options(correct_answers[selected_key], voice, tense, form, gender[0] if gender else None)
    options = [correct_option] + incorrect_options
    random.shuffle(options)

    question_text = f"Ποια είναι η σωστή κατάληξη για το {form} ({voice}, {tense})"
    if form == "μετοχή" and gender:
        question_text += f", {gender[0]}"

    return {
        "question_text": question_text,
        "options": options,
        "correct": correct_option,
    }

def generate_level_14_question():
    """
    Generate a question for Level 14 (all forms, voices, and tenses combined).
    """
    all_forms = ["απαρέμφατο", "μετοχή", "α ενικό", "β ενικό", "γ ενικό", "α πληθυντικό", "β πληθυντικό", "γ πληθυντικό"]
    all_voices = ["ενεργητική", "μέση"]
    all_tenses = ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"]

    available_questions = []

    for form in all_forms:
        for voice in all_voices:
            for tense in all_tenses:
                if form == "απαρέμφατο":
                    question = generate_aparemfato_question_level_15(voice, tense)
                elif form == "μετοχή":
                    # Ensure proper filtering for Metoxi
                    available_keys = [
                        k for k in correct_answers.keys()
                        if k[0] == "μετοχή" and k[1] == voice and k[2] == tense and k[3] in valid_genders
                    ]
                    if available_keys:
                        selected_key = random.choice(available_keys)
                        _, voice, tense, gender = selected_key
                        correct_answer = correct_answers[selected_key][0]

                        incorrect_options = generate_incorrect_options([correct_answer], voice, tense, "μετοχή", gender)
                        options = [correct_answer] + incorrect_options
                        random.shuffle(options)

                        question_text = f"Ποια είναι η σωστή κατάληξη για τη μετοχή ({voice}, {tense}, {gender});"
                        available_questions.append({
                            "question_text": question_text,
                            "options": options,
                            "correct": correct_answer,
                        })
                else:
                    question = generate_question(voice, tense, form)
                    if question:
                        available_questions.append(question)

    if not available_questions:
        print("[DEBUG] No available questions for Level 14.")
        return None

    selected_question = random.choice(available_questions)
    print(f"[DEBUG] Selected Level 14 Question: {selected_question}")
    return selected_question


def generate_level_incorrect_options(correct, forms, voice):
    relevant_options = set()

    # Gather all possible answers for the given forms and voice
    for k, v_list in correct_answers.items():
        if k[0] in forms and k[1] == voice:
            relevant_options.update(v_list)

    # Exclude the correct answer
    incorrect_options = list(relevant_options - set(correct))

    # Debugging logs
    print(f"[DEBUG] Relevant options for forms={forms}, voice={voice}: {relevant_options}")
    print(f"[DEBUG] Incorrect options after excluding correct: {incorrect_options}")

    # Return up to 3 incorrect options
    return random.sample(incorrect_options, min(3, len(incorrect_options))) if incorrect_options else []


# Global variable to store the last selected question
last_question = None


@app.route("/get_question", methods=["GET"])
def get_question():
    global last_question
    try:
        level = int(request.args.get("level", 1))
        print(f"[DEBUG] Fetching question for level {level}")

        if level == 15:
            # Fetch filters
            voices = request.args.get("voices", "").split(",") if request.args.get("voices") else ["ενεργητική", "μέση"]
            tenses = request.args.get("tenses", "").split(",") if request.args.get("tenses") else ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"]
            forms = request.args.get("forms", "").split(",") if request.args.get("forms") else ["α ενικό", "β ενικό", "γ ενικό", "α πληθυντικό", "β πληθυντικό", "γ πληθυντικό"]

            print(f"[DEBUG] Received Filters - Voices: {voices}, Tenses: {tenses}, Forms: {forms}")

            # Filter matching keys from `correct_answers`
            valid_keys = [
                key for key in correct_answers
                if key[1] in voices and key[2] in tenses and (key[0] in forms or "Ρηματικά Πρόσωπα" in forms)
            ]

            print(f"[DEBUG] Valid keys filtered: {valid_keys}")

            # Generate valid questions
            valid_questions = [generate_question(key[1], key[2], key[0]) for key in valid_keys]

            if valid_questions:
                question = random.choice(valid_questions)
                if question != last_question:
                    last_question = question
                    return jsonify(question)
                else:
                    print("[DEBUG] Duplicate question detected for Level 15.")
                    return jsonify({"error": "Duplicate question detected. Try again."}), 400
            else:
                print("[DEBUG] No valid questions for Level 15.")
                return jsonify({"error": "No valid questions available for Level 15."}), 400

        print("[DEBUG] Unsupported level provided.")
        return jsonify({"error": "Unsupported level."}), 400

    except Exception as e:
        print(f"[DEBUG] Exception occurred: {e}")
        return jsonify({"error": str(e)}), 500



def generate_question(voice, tense, form):
    """
    Generate a question for a given voice, tense, and form.
    Special handling for απαρέμφατα and μετοχές.
    """
    if form == "μετοχή" and tense in ["ενεστώτας", "μέλλοντας", "αόριστος", "παρακείμενος"]:
        # Filter valid keys for the given voice and tense
        valid_keys = [
            k for k in correct_answers.keys()
            if k[0] == "μετοχή" and k[1] == voice and k[2] == tense
        ]

        if not valid_keys:
            print("[DEBUG] No valid μετοχή keys found.")
            return None

        # Select a random key
        selected_key = random.choice(valid_keys)
        correct_answer = correct_answers[selected_key][0]
        gender = selected_key[3]

        # Generate incorrect options from other genders
        incorrect_options = [
            correct_answers[k][0] for k in valid_keys if k != selected_key
        ]
        # Ensure we have exactly 3 incorrect options
        if len(incorrect_options) > 3:
            incorrect_options = random.sample(incorrect_options, 3)

        options = [correct_answer] + incorrect_options
        random.shuffle(options)

        return {
            "question_text": f"Ποια είναι η σωστή κατάληξη για τη μετοχή ({voice}, {tense}, {gender});",
            "options": options,
            "correct": correct_answer
        }

    # For other forms, continue with the original logic
    key = (form, voice, tense)
    if key in correct_answers:
        correct_option = correct_answers[key][0]
        incorrect_options = generate_incorrect_options(correct_answers[key], voice, tense, form)
        options = [correct_option] + incorrect_options
        random.shuffle(options)

        return {
            "question_text": f"Ποια είναι η σωστή κατάληξη για το {form} στον {tense} ({voice});",
            "options": options,
            "correct": correct_option
        }

    return None

asked_questions = []

def generate_level_15_question(voices, tenses, forms):
    """
    Generate a Level 15 question strictly based on selected voices, tenses, and forms.
    """
    global asked_questions

    # Ensure inputs are valid
    if not voices or not tenses or not forms:
        return {
            "error": "Πρέπει να επιλέξετε τουλάχιστον μία φωνή, έναν χρόνο και έναν τύπο."
        }, 200

    # Expand "Ρηματικά Πρόσωπα" to specific forms
    expanded_forms = []
    for form in forms:
        if form == "Ρηματικά Πρόσωπα":
            expanded_forms.extend(["α ενικό", "β ενικό", "γ ενικό", "α πληθυντικό", "β πληθυντικό", "γ πληθυντικό"])
        else:
            expanded_forms.append(form)

    print(f"[DEBUG] Expanded forms for Level 15: {expanded_forms}")

    # Filter strictly based on criteria
    valid_keys = [
        k for k in correct_answers.keys()
        if k[1] in voices and k[2] in tenses and k[0] in expanded_forms and k not in asked_questions
    ]

    print(f"[DEBUG] Filtered valid_keys for Level 15: {valid_keys}")

    # Check if valid keys exist after filtering
    if not valid_keys:
        print("[DEBUG] No valid keys found after applying filters.")
        return {
            "error": "Δεν υπάρχουν διαθέσιμες ερωτήσεις για τα επιλεγμένα φίλτρα."
        }, 200

    # Randomly select a valid key
    selected_key = random.choice(valid_keys)
    asked_questions.append(selected_key)

    form, voice, tense = selected_key[:3]
    gender = selected_key[3] if len(selected_key) == 4 else None

    # Generate question based on the form type
    if form == "απαρέμφατο":
        question = generate_aparemfato_question_level_15(voice, tense)
    elif form == "μετοχή":
        question = generate_metoxi_question_level_15(voice, tense, gender)
    else:  # Handle "Ρηματικά Πρόσωπα"
        question = generate_rimatika_prosopa_question_level_15(voice, tense, form)

    if question:
        print(f"[DEBUG] Generated Level 15 Question: {question}")
        return question

    print("[DEBUG] Failed to generate a valid Level 15 question.")
    return {
        "error": "Δεν υπάρχουν ερωτήσεις διαθέσιμες για τα επιλεγμένα φίλτρα."
    }, 200

def generate_aparemfato_question_level_15(voice, tense):
    """
    Generate a question for Απαρέμφατο in Level 15.
    """
    key = ("απαρέμφατο", voice, tense)
    if key in correct_answers:
        correct_answer = correct_answers[key]
        incorrect_options = generate_incorrect_options(correct_answer, voice, tense, "απαρέμφατο")
        options = [correct_answer[0]] + incorrect_options
        random.shuffle(options)

        return {
            "question_text": f"Ποια είναι η σωστή κατάληξη για το απαρέμφατο ({voice}, {tense});",
            "options": options,
            "correct": correct_answer[0],
        }
    return None

def generate_metoxi_question_level_15(voice, tense, gender=None):
    """
    Generate a question for Μετοχή in Level 15.
    """
    available_keys = [
        k for k in correct_answers.keys()
        if k[0] == "μετοχή" and k[1] == voice and k[2] == tense and (gender is None or k[3] == gender)
    ]
    if not available_keys:
        return None

    selected_key = random.choice(available_keys)
    correct_answer = correct_answers[selected_key]

    incorrect_options = generate_incorrect_options(correct_answer, voice, tense, "μετοχή", gender)
    options = [correct_answer[0]] + incorrect_options
    random.shuffle(options)

    return {
        "question_text": f"Ποια είναι η σωστή κατάληξη για τη μετοχή ({voice}, {tense}, {gender});",
        "options": options,
        "correct": correct_answer[0],
    }

def generate_rimatika_prosopa_question_level_15(voice, tense, form):
    """
    Generate a question for Ρηματικά Πρόσωπα in Level 15.
    """
    key = (form, voice, tense)
    if key in correct_answers:
        correct_option = correct_answers[key][0]
        incorrect_options = generate_incorrect_options(correct_answers[key], voice, tense, form)
        options = [correct_option] + incorrect_options
        random.shuffle(options)

        return {
            "question_text": f"Ποια είναι η σωστή κατάληξη για το {form} στον {tense} ({voice});",
            "options": options,
            "correct": correct_option
        }
    print(f"[DEBUG] Ρηματικά Πρόσωπα Key Not Found: {key}")
    return None

def generate_incorrect_options(correct_answers_list, voice, tense, form=None, gender=None, broad_randomization=False):
    """
    Generate incorrect options for answers with optional broader randomization.

    Parameters:
        correct_answers_list (list): The correct answers to exclude.
        voice (str): The voice for filtering options (e.g., ενεργητική, μέση).
        tense (str): The tense for filtering options (e.g., ενεστώτας, παρατατικός).
        form (str): The form type (e.g., "απαρέμφατο", "μετοχή", or specific forms like "α ενικό").
        gender (str): The gender for participles ("αρσενικό", "θηλυκό", "ουδέτερο"), if applicable.
        broad_randomization (bool): Whether to include options unrelated to the current context.

    Returns:
        list: A list of up to 3 incorrect options.
    """
    relevant_options = set()

    # Determine the relevant incorrect options
    for key, v_list in correct_answers.items():
        # Handle "μετοχή" cases
        if form == "μετοχή" and key[0] == "μετοχή" and key[1] == voice and key[2] == tense and (gender is None or key[3] != gender):
            relevant_options.update(v_list)

        # Handle "απαρέμφατο" cases
        elif form == "απαρέμφατο" and key[0] == "απαρέμφατο" and key[1] == voice and key[2] == tense:
            relevant_options.update(v_list)

        # Handle all other forms
        elif key[1] == voice and key[2] == tense and key[0] != form:
            relevant_options.update(v_list)

    # Include unrelated options for broad randomization or if relevant options are insufficient
    if broad_randomization or len(relevant_options) < 3:
        all_possible_options = set.union(*[set(v) for v in correct_answers.values()])
        unrelated_options = list(all_possible_options - set(correct_answers_list))
        random_unrelated = random.sample(unrelated_options, min(3, len(unrelated_options)))
        relevant_options.update(random_unrelated)

    # Exclude correct answers from the final incorrect options
    incorrect_options = list(relevant_options - set(correct_answers_list))

    # Handle cases with insufficient incorrect options
    if len(incorrect_options) < 3:
        fallback_options = list(set.union(*[set(v) for v in correct_answers.values()]) - set(correct_answers_list))
        additional_options = random.sample(fallback_options, min(3 - len(incorrect_options), len(fallback_options)))
        incorrect_options.extend(additional_options)

    # Return up to 3 incorrect options
    return random.sample(incorrect_options, min(3, len(incorrect_options)))

def generate_incorrect_options_level_15(correct_answers_list, voice, tense, form, gender=None):
    """
    Generate incorrect options relevant to Level 15 filters.
    """
    # Leverage the generalized incorrect options function
    return generate_incorrect_options(correct_answers_list, voice, tense, form, gender, broad_randomization=True)

def get_valid_filters(voices, tenses, forms):
    if not voices:
        voices = ["ενεργητική", "μέση"]
    if not tenses:
        tenses = ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"]
    if not forms:
        forms = ["α ενικό", "β ενικό", "γ ενικό", "α πληθυντικό", "β πληθυντικό", "γ πληθυντικό"]
    return voices, tenses, forms


def retry_level_15(voices, tenses, forms, max_retries=10):
    """
    Retry generating a Level 15 question until successful or retries are exhausted.
    """
    for attempt in range(max_retries):
        question = generate_level_15_question(voices, tenses, forms)
        if question:
            print(f"[DEBUG] Successfully generated Level 15 question on attempt {attempt + 1}")
            return question
        print(f"[DEBUG] Retrying Level 15 question generation... (Attempt {attempt + 1}/{max_retries})")

    # If retries are exhausted, handle the failure gracefully
    print("[DEBUG] Failed to generate a Level 15 question after maximum retries.")
    return {"error": "No valid questions available for Level 15 after multiple attempts."}, 400

def check_remaining_questions(level):
    valid_keys = [
        k for k in correct_answers.keys()
        if (level not in [12, 13, 14] or k[0] in special_forms)  # Include special forms for 12, 13, 14
    ]
    print(f"[DEBUG] Remaining keys for level {level}: {len(valid_keys)}")
    return len(valid_keys) > 0


def check_answer():
    data = request.json
    form = data.get("form")
    voice = data.get("voice")
    tense = data.get("tense")
    gender = data.get("gender") if form == "μετοχή" else None
    answer = data.get("answer")
    level = data.get("level")

    key = (form, voice, tense) if form == "απαρέμφατο" else (form, voice, tense, gender)
    correct_answers_list = correct_answers.get(key, [])
    correct = answer.strip() in (a.strip() for a in correct_answers_list)

    if not correct:
        incorrect_questions.append({
            "form": form,
            "voice": voice,
            "tense": tense,
            "gender": gender,
            "correct_answer": correct_answers_list
        })

    if level == 12:
        question = generate_aparemfato_question(level)
    elif level == 13:
        question = generate_metoxi_question(level)
    else:
        question = generate_general_question(level)

    if question:
        return jsonify({
            "message": "Next question",
            "question": question,
            "correct": correct
        })
    else:
        return jsonify({"error": "Could not generate next question."}), 400

# Route to start the game
@app.route("/start_game", methods=["POST"])
def start_game():
    data = request.json
    level = data.get("level", 1)
    lives = data.get("lives", DEFAULT_LIVES)
    timer = data.get("timer", DEFAULT_QUIZ_TIME)

    # Generate the appropriate question based on the level
    if level == 12:
        question = generate_aparemfato_question(level)
    elif level == 13:
        question = generate_metoxi_question(level)
    else:
        question = generate_general_question(level)

    if question:
        return jsonify({
            "message": "Game started",
            "question": question,
            "game_state": {"level": level, "lives": lives, "timer": timer}
        })
    else:
        return jsonify({"error": "Could not generate question."}), 400

# Route to finish the game and show incorrect answers
@app.route("/end_game", methods=["POST"])
def end_game():
    data = request.json
    score = data.get("score", 0)
    num_questions = data.get("num_questions", NUM_QUESTIONS)
    percentage = (score / num_questions) * 100

    return jsonify({
        "score": score,
        "num_questions": num_questions,
        "percentage": round(percentage, 2),
        "incorrect_answers": incorrect_questions,
        "message": f"You scored {score}/{num_questions} ({round(percentage, 2)}%)!"
    })

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
