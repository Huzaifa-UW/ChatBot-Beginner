# This is import section
#--------------------------------------------------

import csv
import string
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer  
nlp = spacy.load("en_core_web_sm")
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

#---------------------------------------------------


try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# This helps filter understand which words to keep and which to not

stop_words = set(stopwords.words('english'))
stop_words -= {"how", "what", "why", "when", "where", "want", "learn", "help", "popular" , "best"}
stop_words.update(["do", "am", "is", "are", "a", "to"])
tokenizer = TreebankWordTokenizer()


# Main are where we ask question and do all the process
#-------------------------------------------------------------------------------------


data_dic = {}
with open("basic_clean_dataset_3000.csv", encoding="utf-8") as file:
    next(file)
    for line in file:
        line = line.strip()
        question ,answer = line.split(",", 1)
        data_dic[question] = answer

print("Hi! How can I help you?")
while True:
    score = {}
    question = input("> ")
    exact_answer_found = False

    
    # If direct match question 

    for q in data_dic:
        if question.lower().rstrip("?!.") == q.lower().rstrip("?!."):
            print(data_dic[q])
            exact_answer_found = True
            break

    if exact_answer_found:
        continue  

    # for noun match and others

    doc = nlp(question)
    nouns = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    important_words = nouns + [token.text for token in doc if token.pos_ in ["VERB", "ADJ"]]

    # To close chat

    if question.lower() in ["goodbye", "bye", "exit", "good bye"]:
        print("Goodbye!")
        break


    breaking_words = tokenizer.tokenize(question.lower())
    main_words = [word for word in breaking_words if word not in stop_words]
    num_words = len(main_words)

   

    # nested loops 


    for words in main_words:
        for question_word in data_dic:      
            sentence = " "
            # sentence = tokenizer.tokenize(question_word.lower())
            for splition in question_word.split(" "):
                sentence  += splition + " "
                clean_sentence = question_word.lower().translate(str.maketrans('', '', string.punctuation)).split()
                            
            
            # for making sure user typed word match if there is like s with word

                lemmatized_nouns = [lemmatizer.lemmatize(n.lower()) for n in nouns]
                lemmatized_sentence = [lemmatizer.lemmatize(w) for w in clean_sentence]


                for word_in_sentence in lemmatized_sentence:
                    if word_in_sentence in lemmatized_nouns:


                        if question_word not in score:
                            score[question_word] = 0

                        clean_sentence = [w.lower().translate(str.maketrans('', '', string.punctuation)) for w in sentence]
                        clean_word = words.lower().translate(str.maketrans('', '', string.punctuation))
                        if any(clean_word in w or w in clean_word for w in clean_sentence) or any(n.lower() in clean_sentence for n in nouns):
                            score[question_word] += 1

                    # bonus points on additions

                        verbs_adjs = [token.text for token in doc if token.pos_ in ["VERB", "ADJ"]]
                        lemmatized_verbs_adjs = [lemmatizer.lemmatize(v.lower()) for v in verbs_adjs]

                        # Now check if any verb/adjective in CSV sentence
                        for v in lemmatized_verbs_adjs:
                            if v in lemmatized_sentence:
                                score[question_word] += 0.5



    # score will help us distinguish what user want to say:

    try:
        reasonable_question = max(score, key=score.get)
    except ValueError:
        reasonable_question = None
   
    score_val = score.get(reasonable_question, 0)
    if reasonable_question is not None:
        print(data_dic[reasonable_question])
    else:
        print("Sorry! I don't have enough information on that. Try asking differently.")



# -----------------------------------------------------------------------------------------------------
# NOTE: FIXES WILL BE DONE SOON AND MORE DATA WILL BE ADDED ALSO
