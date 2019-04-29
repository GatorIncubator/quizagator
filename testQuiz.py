import csv
creatorID = {query creator_id}
# After use clicks add quiz and names quiz
classID = {query TopicID}  # Could also get this from html
INSERT INTO quizzes VALUES
# autoIncrementID (quizID), TopicID (classID), num (easy, med, hard), creator_id, Name
(, , , , , 1, Master Quiz 1);

quizID = {query quiz id}
# After user submits csv file
file = open(pathToCSV, "r")
reader = csv.reader(file)
questionArray = []
for line in reader
    questionLine = '', line[0], line[1], line[2], line[3], line[4], QuizID
    questionArray.append(questionLine)
for i in questionArray:
    INSERT INTO questions VALUES
    # autoIncrementID, correct answer, topic_id, difficulty, question text, a answer_text, b answer_text, c_answer_text, d_answer_text, quizID
            i;
# After use clicks add class and names class
INSERT INTO classes VALUES
# autoIncrementID, creator_id, Name
    (, creatorID, CS481);
