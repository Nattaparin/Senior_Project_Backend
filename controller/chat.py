import json
from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import word_tokenize
from pythainlp.tokenize import word_tokenize
from pythainlp.util import dict_trie
from pythainlp.corpus import thai_words
from pythainlp.spell import NorvigSpellChecker
from pythainlp.util import normalize




import json
import openai
# DISTANCE_LAST = None  # ระยะทางล่าสุด
# DISTANCE_NOW = None  # ระยะทางตอนนี้
import git

# กำหนด repository ที่ต้องการทำงาน
repo_path = "C:/Users/ASUS TUF FA506/OneDrive/เดสก์ท็อป/project/Senior_Project_Backend"
repo = git.Repo(repo_path)

# เพิ่มไฟล์ที่มีการเปลี่ยนแปลง
repo.git.add(update=True)

# Commit การเปลี่ยนแปลง
repo.git.commit("-m", "Update from OpenAI API")

# Push การเปลี่ยนแปลงไปยัง remote
origin = repo.remote(name='origin')
origin.push()
import os
API_KEY = os.environ.get('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')

# Load the car issues dictionary from the JSON file
with open('C:/Users/ASUS TUF FA506/OneDrive/เดสก์ท็อป/project/Senior_Project_Backend/controller/car_issues.json', 'r', encoding='utf-8') as f:
    car_issues_loaded = json.load(f)

# Set up the OpenAI API key
openai.api_key = API_KEY

def remove_stopwords(text):
    tokens = word_tokenize(text, engine="newmm")
    return ' '.join([word for word in tokens if word not in thai_stopwords()])

custom_dict = set(thai_words())
for issue in car_issues_loaded:
    custom_dict.add(issue)
trie = dict_trie(dict_source=custom_dict)
checker = NorvigSpellChecker(custom_dict=custom_dict)

def correct_car_issues(text):
    tokens = word_tokenize(text, engine="newmm", custom_dict=trie)
    corrected_tokens = [checker.correct(normalize(token)) for token in tokens]
    return ' '.join(corrected_tokens)

# Define the get_car_issue_solution function
def get_car_issue_solution(question):
    # Check for specific strings without preprocessing
    if question.startswith("สอบถามเกี่ยวกับอาการรถ"):
        return "แจ้งอาการของรถ:"

    # Preprocess the question for more generic matching
    cleaned_question = correct_car_issues(remove_stopwords(question))

    for issue, solutions in car_issues_loaded.items():
        if issue in question:
            return f"สำหรับปัญหา '{issue}' ตรวจสอบงาน\n" + "\n".join(solutions)

    return "ขอภัย, คำถามของท่านไม่ถูกต้อง กรุณาตั้งคำถามที่มี อาการของรถ ด้วย"

test_question = "รถสตาร์ทไม็ติด"
corrected_text = correct_car_issues(test_question)
print("Original:", test_question)
print("Corrected:", corrected_text)
MAX_LENGTH = 700
# Define the chat_with_gpt4 function
def chat_with_gpt4(question):
    # ตรวจสอบว่าคำถามมีคำว่า "รถมี" หรือ "อาการ" หรือไม่
    if get_car_issue_solution:
        answer = get_car_issue_solution(question)
    else:
        answer = "ขอภัย"

    # ถ้าไม่พบคำตอบใน dictionary ให้ถาม GPT-4
    if answer == "ขอภัย" or ("รถมี" in question or "อาการ" in question):
        prompt = f"User: {question}\nChatGPT: "
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": ""}
                ]
            )
            answer = response['choices'][0]['message']['content'].strip()
            if len(answer) > MAX_LENGTH:
                answer = answer[:MAX_LENGTH] + "..."
        except openai.error.RateLimitError:
            answer = "I've exceeded my rate limit for the OpenAI API. Please try again later."

    return answer
