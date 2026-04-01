import pandas as pd
import spacy
from rapidfuzz import fuzz

class SymptomChecker:

    # Emergency keywords
    EMERGENCY_KEYWORDS = [
        "severe", "sudden", "unbearable", "crushing", "intense",
        "extreme", "high", "acute", "persistent", "emergency", "difficulty breathing"
    ]

    # Synonym dictionary
    SYNONYMS = {
        # Common Viral Infection
        "feverish": "fever",
        "temperature": "fever",
        "high temperature": "fever",
        "coughing": "cough",
        "throat pain": "sore throat",
        "runny nose": "runny nose",
        "body aches": "body ache",
        "aches": "body ache",

        # Respiratory Issue
        "wheeze": "wheezing",
        "short of breath": "shortness of breath",
        "breathlessness": "shortness of breath",
        "tight chest": "chest tightness",
        "tired": "fatigue",
        "blue lips": "blue lips",

        # Severe Chest Problem
        "chest discomfort": "chest pain",
        "arm numbness": "arm pain",
        "lightheaded": "dizziness",
        "nauseated": "nausea",
        "sweating heavily": "sweating",

        # Digestive Problem
        "stomach ache": "abdominal pain",
        "bloating": "bloating",
        "loose stools": "diarrhea",
        "constipated": "constipation",
        "nauseated": "nausea",
        "loss of appetite": "loss of appetite",

        # Kidney/Urinary Problem
        "pee frequently": "frequent urination",
        "back ache": "back pain",
        "blood in my urine": "blood in urine",
        "swollen": "swelling",
        "stomach pain": "abdominal pain",

        # Skin Condition
        "itchy": "itching",
        "red skin": "redness",
        "dry skin": "dry skin",
        "blisters": "blisters",

        # Joint/Muscle Pain
        "joint ache": "joint pain",
        "stiff": "stiffness",
        "restricted movement": "limited movement",
        "muscle weakness": "muscle weakness",

        # Eye Problem
        "blurred vision": "blurry vision",
        "eye hurts": "eye pain",
        "red eyes": "red eyes",
        "double vision": "double vision",
        "loss of sight": "loss of vision",

        # Ear/Nose/Throat Issue
        "throat hurts": "sore throat",
        "stuffy nose": "nasal congestion",
        "ear hurts": "ear pain",
        "hearing loss": "hearing loss",

        # Allergic Reaction
        "sneeze": "sneezing",
        "trouble breathing": "breathing difficulty",
        "hives": "hives",

        # Mental Health Concern
        "sad": "sadness",
        "anxious": "anxiety",
        "irritable": "irritability",
        "can't sleep": "sleep problems",
        "sleep poorly": "sleep problems",
        "loss of interest": "loss of interest",

        # Women's Health Issue
        "missed period": "missed period",
        "irregular period": "irregular periods",
        "bloated": "bloating",

        # General Weakness
        "weight change": "weight changes",
        "dizzy": "dizziness",
        "pale skin": "pale skin",
        "weak": "weakness",

        # Blood-related Issue
        "bruised easily": "bruising",
        "bleeding gums": "bleeding gums",
    }

    def __init__(self, csv_path=r"F:\Project\Data\symptoms_dataset.csv"):
        self.data = pd.read_csv(csv_path)
        self.nlp = spacy.load("en_core_web_sm")

    def preprocess(self, text):
        """Tokenize, lemmatize, and apply synonym mapping"""
        doc = self.nlp(text.lower())
        words = [token.lemma_ for token in doc if token.is_alpha]
        mapped_words = []
        for word in words:
            mapped_words.append(self.SYNONYMS.get(word, word))
        return mapped_words

    def check_symptoms(self, user_input):
        user_input_lower = user_input.lower()
        emergency_flag = any(word in user_input_lower for word in self.EMERGENCY_KEYWORDS)
        user_words = self.preprocess(user_input)

        best_match = None
        max_matches = 0
        matched_list = []

        for _, row in self.data.iterrows():
            condition_symptoms = [s.strip().lower() for s in str(row["Symptoms"]).split(",")]
            current_matched = []

            for symptom in condition_symptoms:
                # Preprocess symptom phrase
                symptom_words = self.preprocess(symptom)
                # Join to string for fuzzy matching
                symptom_str = " ".join(symptom_words)
                user_str = " ".join(user_words)

                if fuzz.partial_ratio(symptom_str, user_str) >= 80:
                    current_matched.append(symptom)

            match_count = len(current_matched)
            if match_count > max_matches:
                max_matches = match_count
                matched_list = current_matched
                best_match = {
                    "Condition": row["Condition"],
                    "Doctor": row["Doctor"],
                    "Emergency": emergency_flag,
                    "Matches": match_count,
                    "Matched_Symptoms": matched_list
                }

        if best_match:
            return best_match
        else:
            return {
                "Condition": "Not Found",
                "Doctor": "General Physician",
                "Emergency": emergency_flag,
                "Matches": 0,
                "Matched_Symptoms": []
            }
