import random

def get_top_users(users, n=3):
    sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)
    return sorted_users[:n]

def load_questions(file_name):
    questions = list()
    with open(file_name, 'r') as file:
        for line in file:
            question, answer = line.strip().split(',')
            questions.append((question, answer))
    return questions

def load_users(file_name):
    users = {}
    with open(file_name, 'r') as file:
        for line in file:
            name, score = line.strip().split(',')
            users[name] = int(score)
    return users

def save_users(file_name, users):
    with open(file_name, 'w') as file:
        for name, score in users.items():
            file.write(f"{name},{score}\n")

def is_partial_match(user_answer, correct_answer):
    user_words = user_answer.split()
    correct_words = correct_answer.split()
    return any(word in correct_words for word in user_words)

def main():
    print("Welcome to my quiz!")

    user_name = input("Please enter your name: ")
    
    questions = load_questions("questions.txt")
    users = load_users("users.txt")

    playing = input("Do you want to play? ").lower()
    if playing != "yes":
        quit()

    print("Okay, let's play!")
    score = 0

    random.shuffle(questions) 
    used_questions = set()  

    for _ in range(len(questions)): 
        unused_questions = [q for q in questions if q not in used_questions]
        if not unused_questions:
            print("Nu mai sunt întrebări disponibile. Jocul s-a încheiat.")
            break

        question, correct_answer = random.choice(unused_questions)
        used_questions.add((question, correct_answer))

        print(question)
        answer = input("Your answer: ").lower()
        if answer == "done":
            break  
        elif is_partial_match(answer, correct_answer.lower()):
            print('Correct!\n')
            score += 1
        else:
            print(f"Incorrect! The correct answer is {correct_answer}\n")

        print(f"Your current score is: {score}\n")

    if score > 0:
        print(f"You got {score} questions correct!")

    if user_name in users:
        users[user_name] += score
    else:
        users[user_name] = score

    save_users("users.txt", users)

    top_users = get_top_users(users, n=3)
    print("\nTop Users:")
    for rank, (name, user_score) in enumerate(top_users, start=1):
        print(f"{rank}. {name}: {user_score} points")

if __name__ == "__main__":
    main()

