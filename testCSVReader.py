# Get: autoIncrementID, correct answer, topic_id, difficulty, question text, a answer_text,
# Get (cont.): b answer_text, c_answer_text, d_answer_text, quizID
# Given: Question, correct_answer number 0-3, answer a, b, c, d
import csv
# After user submits csv file
file = open("sample.csv", "r")
reader = csv.reader(file)
questionArray = []
quizID = 4
for line in reader:
    questionLine = '', line[0], line[1], line[2], line[3], line[4], line[5], quizID
    questionArray.append(questionLine)
print(questionArray)
