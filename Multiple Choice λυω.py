import random

# Define categories
verbs = ["λύω"]
voices = ["ενεργητική", "μέση"]
tenses = ["ενεστώτας", "παρατατικός", "μέλλοντας", "αόριστος", "παρακείμενος", "υπερσυντέλικος"]

# Simplify forms: single entry for "μετοχή" and "απαρέμφατο"
forms = [
    "α ενικό", "β ενικό", "γ ενικό", 
    "α πληθυντικό", "β πληθυντικό", "γ πληθυντικό", 
    "απαρέμφατο",  # Infinitive
    "μετοχή"  # Generic participle form
]

correct_answers = {
      # Ενεστώτας Ενεργητική
    ("α ενικό", "ενεργητική", "ενεστώτας"): ["ω"],
    ("β ενικό", "ενεργητική", "ενεστώτας"): ["εις"],
    ("γ ενικό", "ενεργητική", "ενεστώτας"): ["ει"],
    ("α πληθυντικό", "ενεργητική", "ενεστώτας"): ["ομεν"],
    ("β πληθυντικό", "ενεργητική", "ενεστώτας"): ["ετε"],
    ("γ πληθυντικό", "ενεργητική", "ενεστώτας"): ["ουσιν"],
    # Παρατατικός Ενεργητική
    ("α ενικό", "ενεργητική", "παρατατικός"): ["ον"],
    ("β ενικό", "ενεργητική", "παρατατικός"): ["ες"],
    ("γ ενικό", "ενεργητική", "παρατατικός"): ["ε"],
    ("α πληθυντικό", "ενεργητική", "παρατατικός"): ["ομεν"],
    ("β πληθυντικό", "ενεργητική", "παρατατικός"): ["ετε"],
    ("γ πληθυντικό", "ενεργητική", "παρατατικός"): ["ον"],
    # Μέλλοντας Ενεργητική
    ("α ενικό", "ενεργητική", "μέλλοντας"): ["σω"],
    ("β ενικό", "ενεργητική", "μέλλοντας"): ["σεις"],
    ("γ ενικό", "ενεργητική", "μέλλοντας"): ["σει"],
    ("α πληθυντικό", "ενεργητική", "μέλλοντας"): ["σομεν"],
    ("β πληθυντικό", "ενεργητική", "μέλλοντας"): ["σετε"],
    ("γ πληθυντικό", "ενεργητική", "μέλλοντας"): ["σουσι"],
    # Αόριστος Ενεργητική
    ("α ενικό", "ενεργητική", "αόριστος"): ["σα"],
    ("β ενικό", "ενεργητική", "αόριστος"): ["σας"],
    ("γ ενικό", "ενεργητική", "αόριστος"): ["σε"],
    ("α πληθυντικό", "ενεργητική", "αόριστος"): ["σαμεν"],
    ("β πληθυντικό", "ενεργητική", "αόριστος"): ["σατε"],
    ("γ πληθυντικό", "ενεργητική", "αόριστος"): ["σαν"],
    # Παρακείμενος Ενεργητική
    ("α ενικό", "ενεργητική", "παρακείμενος"): ["κα"],
    ("β ενικό", "ενεργητική", "παρακείμενος"): ["κας"],
    ("γ ενικό", "ενεργητική", "παρακείμενος"): ["κε"],
    ("α πληθυντικό", "ενεργητική", "παρακείμενος"): ["καμεν"],
    ("β πληθυντικό", "ενεργητική", "παρακείμενος"): ["κατε"],
    ("γ πληθυντικό", "ενεργητική", "παρακείμενος"): ["κασιν"],
    # Υπερσυντέλικος Ενεργητική
    ("α ενικό", "ενεργητική", "υπερσυντέλικος"): ["κειν"],
    ("β ενικό", "ενεργητική", "υπερσυντέλικος"): ["κεις"],
    ("γ ενικό", "ενεργητική", "υπερσυντέλικος"): ["κει"],
    ("α πληθυντικό", "ενεργητική", "υπερσυντέλικος"): ["κεμεν"],
    ("β πληθυντικό", "ενεργητική", "υπερσυντέλικος"): ["κετε"],
    ("γ πληθυντικό", "ενεργητική", "υπερσυντέλικος"): ["κεσαν"],
    # Ενεστώτας Μέση
    ("α ενικό", "μέση", "ενεστώτας"): ["ομαι"],
    ("β ενικό", "μέση", "ενεστώτας"): ["ει", "ῃ"],
    ("γ ενικό", "μέση", "ενεστώτας"): ["εται"],
    ("α πληθυντικό", "μέση", "ενεστώτας"): ["ομεθα"],
    ("β πληθυντικό", "μέση", "ενεστώτας"): ["εσθε"],
    ("γ πληθυντικό", "μέση", "ενεστώτας"): ["ονται"],
    # Παρατατικός Μέση
    ("α ενικό", "μέση", "παρατατικός"): ["ομην"],
    ("β ενικό", "μέση", "παρατατικός"): ["ου"],
    ("γ ενικό", "μέση", "παρατατικός"): ["ετο"],
    ("α πληθυντικό", "μέση", "παρατατικός"): ["ομεθα"],
    ("β πληθυντικό", "μέση", "παρατατικός"): ["εσθε"],
    ("γ πληθυντικό", "μέση", "παρατατικός"): ["οντο"],
    # Μέλλοντας Μέση
    ("α ενικό", "μέση", "μέλλοντας"): ["σομαι"],
    ("β ενικό", "μέση", "μέλλοντας"): ["σει", "σῃ"],
    ("γ ενικό", "μέση", "μέλλοντας"): ["σεται"],
    ("α πληθυντικό", "μέση", "μέλλοντας"): ["σομεθα"],
    ("β πληθυντικό", "μέση", "μέλλοντας"): ["σεσθε"],
    ("γ πληθυντικό", "μέση", "μέλλοντας"): ["σονται"],
    # Αόριστος Μέση
    ("α ενικό", "μέση", "αόριστος"): ["σαμην"],
    ("β ενικό", "μέση", "αόριστος"): ["σω"],
    ("γ ενικό", "μέση", "αόριστος"): ["σατο"],
    ("α πληθυντικό", "μέση", "αόριστος"): ["σαμεθα"],
    ("β πληθυντικό", "μέση", "αόριστος"): ["σασθε"],
    ("γ πληθυντικό", "μέση", "αόριστος"): ["σαντο"],
    # Παρακείμενος Μέση
    ("α ενικό", "μέση", "παρακείμενος"): ["μαι"],
    ("β ενικό", "μέση", "παρακείμενος"): ["σαι"],
    ("γ ενικό", "μέση", "παρακείμενος"): ["ται"],
    ("α πληθυντικό", "μέση", "παρακείμενος"): ["μεθα"],
    ("β πληθυντικό", "μέση", "παρακείμενος"): ["σθε"],
    ("γ πληθυντικό", "μέση", "παρακείμενος"): ["νται"],
    # Υπερσυντέλικος Μέση
    ("α ενικό", "μέση", "υπερσυντέλικος"): ["μην"],
    ("β ενικό", "μέση", "υπερσυντέλικος"): ["σο"],
    ("γ ενικό", "μέση", "υπερσυντέλικος"): ["το"],
    ("α πληθυντικό", "μέση", "υπερσυντέλικος"): ["μεθα"],
    ("β πληθυντικό", "μέση", "υπερσυντέλικος"): ["σθε"],
    ("γ πληθυντικό", "μέση", "υπερσυντέλικος"): ["ντο"],
    # Απαρέμφατο
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
    ("μετοχή", "ενεργητική", "μέλλοντας", "αρσενικό"): ["σων"],
    ("μετοχή", "ενεργητική", "μέλλοντας", "θηλυκό"): ["σουσα"],
    ("μετοχή", "ενεργητική", "μέλλοντας", "ουδέτερο"): ["σον"],
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
    ("μετοχή", "μέση", "μέλλοντας", "αρσενικό"): ["σομενος"],
    ("μετοχή", "μέση", "μέλλοντας", "θηλυκό"): ["σομενη"],
    ("μετοχή", "μέση", "μέλλοντας", "ουδέτερο"): ["σομενον"],
    ("μετοχή", "μέση", "αόριστος", "αρσενικό"): ["σαμενος"],
    ("μετοχή", "μέση", "αόριστος", "θηλυκό"): ["σαμενη"],
    ("μετοχή", "μέση", "αόριστος", "ουδέτερο"): ["σαμενον"],
    ("μετοχή", "μέση", "παρακείμενος", "αρσενικό"): ["μενος"],
    ("μετοχή", "μέση", "παρακείμενος", "θηλυκό"): ["μενη"],
    ("μετοχή", "μέση", "παρακείμενος", "ουδέτερο"): ["μενον"]
}
used_combinations = set()

def generate_incorrect_options(correct_endings, form, voice, tense):
    relevant_options = {opt for k, v in correct_answers.items()
                        if k[1] == voice and k[2] == tense for opt in v}
    incorrect_options = list(relevant_options - set(correct_endings))
    return random.sample(incorrect_options, min(3, len(incorrect_options))) if incorrect_options else []

def generate_random_question():
    global used_combinations

    attempt_limit = 100
    attempt_count = 0

    while attempt_count < attempt_limit:
        form = random.choice(forms)
        voice = random.choice(voices)
        tense = random.choice(tenses)

        if form == "μετοχή":
            # Add random gender for participles
            gender = random.choice(["αρσενικό", "θηλυκό", "ουδέτερο"])
            key = ("μετοχή", voice, tense, gender)
        else:
            key = (form, voice, tense)

        if key not in used_combinations and key in correct_answers:
            used_combinations.add(key)
            correct_endings = correct_answers[key]
            correct_answer = random.choice(correct_endings)
            
            # Pass all required arguments to generate_incorrect_options
            incorrect_options = generate_incorrect_options(correct_endings, form, voice, tense)

            # Generate final options
            options = incorrect_options + [correct_answer]
            while len(options) < 4:
                options.append(random.choice(incorrect_options))
            random.shuffle(options)

            # Print question (for visual inspection)
            print(f"Form: {form}")
            print(f"Verb: {verbs[0]}")
            print(f"Voice: {voice}")
            print(f"Tense: {tense}")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            # In developer mode, randomly select an option, in user mode we prompt for input
            if is_developer_mode:
                answer_index = random.randint(0, 3)  # Randomly select an option (0, 1, 2, or 3)
                player_answer = options[answer_index]
                print(f"Randomly selected answer: {player_answer}")
            else:
                # User mode: Prompt for answer
                try:
                    answer_index = int(input("Choose the correct option (1-4): ")) - 1
                    if answer_index < 0 or answer_index > 3:
                        print("Οι απαντήσεις μπορούν να είναι από το 1-4. Δοκίμασε πάλι!")
                        return False  # Prevent the answer from being counted as wrong
                    player_answer = options[answer_index]
                except (ValueError, IndexError):
                    print("Οι απαντήσεις μπορούν να είναι από το 1-4. Δοκίμασε πάλι!")
                    return False  # Prevent the answer from being counted as wrong

            # Check if the answer is correct and increment counter
            if player_answer == correct_answer:
                print("Correct!\n")
                return True
            else:
                print(f"Incorrect. The correct answer was: {correct_answer}.\n")
                return False
        attempt_count += 1

    print("No more unique combinations are available.")
    return False

def main():
    global used_combinations
    print("Welcome to the Ancient Greek Grammar Quiz!\n")
    
    num_questions = 10  # Number of questions for the quiz
    correct_needed = int(num_questions * 0.80)  # 80% success rate
    
    correct_count = 0
    used_combinations = set()

    # Developer mode flag: Set to True for random answers testing, False for user interaction
    global is_developer_mode
    is_developer_mode = False  # Set to True when you want to test, False when you don't

    # Loop through the number of questions
    for _ in range(num_questions):
        if generate_random_question():
            correct_count += 1

    # Evaluate the result
    if correct_count >= correct_needed:
        print(f"Congratulations! You answered {correct_count} out of {num_questions} correctly and passed the quiz.")
    else:
        print(f"You answered {correct_count} out of {num_questions} correctly. You need at least {correct_needed} to pass. Try again!")

# Run the main function
main()

# Developer flag to control whether the function should run or not
is_developer_mode = False  # Set to True when you want to test, False when you don't


def find_undefined_combinations(forms, voices, tenses, correct_answers):
    undefined_combinations = []

    for form in forms:
        for voice in voices:
            for tense in tenses:
                # Skip invalid combinations for μετοχή and απαρέμφατο
                if form == "μετοχή" and tense in ["παρατατικός", "υπερσυντέλικος"]:
                    continue
                elif form == "απαρέμφατο" and tense in ["παρατατικός", "υπερσυντέλικος"]:
                    continue

                # Build the key structure based on form type
                if form == "μετοχή":
                    # Loop through genders for participles
                    for gender in ["αρσενικό", "θηλυκό", "ουδέτερο"]:
                        key = ("μετοχή", voice, tense, gender)
                        if key not in correct_answers:
                            undefined_combinations.append(key)
                elif form == "απαρέμφατο":
                    key = (form, voice, tense)
                    if key not in correct_answers:
                        undefined_combinations.append(key)
                else:
                    key = (form, voice, tense)
                    if key not in correct_answers:
                        undefined_combinations.append(key)

    return undefined_combinations

# Only run the function if in developer mode
if is_developer_mode:
    # Check undefined combinations only if you are in developer mode
    undefined_combinations = find_undefined_combinations(forms, voices, tenses, correct_answers)
    if undefined_combinations:
        print("Undefined combinations:")
        for combo in undefined_combinations:
            print(combo)
    else:
        print("All combinations are defined.")
