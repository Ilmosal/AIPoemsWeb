#Important util functions for the program

import csv

from .models import PoemSet, Poem

def load_poems_to_db():
    # Erase old things
    for poem_set in PoemSet.objects.all():
        poem_set.delete()

    poems_en = [[],[]]
    poems_fi = [[],[]]
    poems_no = [[],[]]

    poems_en_authors = []
    poems_fi_authors = []
    poems_no_authors = []

    with open('poems/files/Table_1.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        cur_poem = ""
        rows = list(reader)
        for r, i in zip(rows, range(len(rows))):
            poem = ""
            for line in r:
                poem += str(line)

            if i < 70:
                poems_en[0].append(poem)
            elif i < 120:
                poems_fi[0].append(poem)
            else:
                poems_no[0].append(poem)

    with open('poems/files/Table_2.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        cur_poem = ""
        rows = list(reader)
        for r, i in zip(rows, range(len(rows))):
            poem = ""
            for line in r:
                poem += str(line)

            if i < 70:
                poems_en[1].append(poem)
            elif i < 120:
                poems_fi[1].append(poem)
            else:
                poems_no[1].append(poem)

    with open('poems/files/Table_authors.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        cur_poem = ""
        rows = list(reader)
        for r, i in zip(rows, range(len(rows))):
            author = str(r[0])

            if i < 70:
                poems_en_authors.append(author)
            elif i < 120:
                poems_fi_authors.append(author)
            else:
                poems_no_authors.append(author)

    # Create poem sets
    poemset_en = PoemSet(language='en', max_questions=10)
    poemset_fi = PoemSet(language='fi', max_questions=10)
    poemset_no = PoemSet(language='no', max_questions=10)
    poemset_en.save()
    poemset_fi.save()
    poemset_no.save()

    # Create poems for the poem sets
    for p, p_ai, a in zip(poems_en[0], poems_en[1], poems_en_authors):
        poemset_en.poem_set.create(poem_text=p, poem_class=False, author=a)
        poemset_en.poem_set.create(poem_text=p_ai, poem_class=True, author="ChatGPT")

    for p, p_ai, a in zip(poems_fi[0], poems_fi[1], poems_fi_authors):
        poemset_fi.poem_set.create(poem_text=p, poem_class=False, author=a)
        poemset_fi.poem_set.create(poem_text=p_ai, poem_class=True, author="ChatGPT")

    for p, p_ai, a in zip(poems_no[0], poems_no[1], poems_no_authors):
        poemset_no.poem_set.create(poem_text=p, poem_class=False, author=a)
        poemset_no.poem_set.create(poem_text=p_ai, poem_class=True, author="ChatGPT")

def valid_language(values):
    lan = values[0]

    if lan not in ["en", "fi", "no"]:
        raise Exception("{0} not a valid language!".format(lan))

def valid_show_res(values): #Validify for this answer set
    show_res = int(values[1])
    if show_res not in [0, 1]:
        raise Exception("{0} not a valid show_res!".format(show_res))

def valid_questionnaire(values):
    # Add valid questionnaire test
    questionnaire = values[2]

def valid_answerset(values):
    # add valid answerset test
    answerset = values[3]

def valid_question(values):
    # add valid question id test
    question = int(values[4])

def split_int_into_bool_array(val):
    val_string = f'{val:064b}'
    bools = []

    for v in val_string:
        bools.append(bool(int(v)))

    return bools

def merge_bool_array_into_int(arr):
    val = 0
    arr.reverse()
    for a, i in zip(arr, range(len(arr))):
        val += a * 2**(i)

    return val

def valid_answers(values):
    split_int_into_bool_array(int(values[5]))

# Decode the answer code formatted of: la-b-questionnaire-answerset-question-answers
# Raise Exception if not correct
def decode_answer_code(code):
    values = code.split('-')

    if len(values) != 6:
        raise Exception("Incorrect amount of arguments! Arguments gained: {0}".format(len(values)))

    valid_language(values)
    valid_show_res(values)
    valid_questionnaire(values)
    valid_answerset(values)
    valid_question(values)
    valid_answers(values)

    decoded_array = [
        values[0],
        int(values[1]),
        values[2],
        int(values[3]),
        int(values[4]),
        split_int_into_bool_array(int(values[5])),
    ]

    return decoded_array

def encode_answer_code(language, show_res, questionnaire, answerset, question, answers):
    code = "{0}-{1}-{2}-{3}-{4}-{5}".format(
        language, int(show_res), questionnaire, answerset, question, merge_bool_array_into_int(answers)
    )
    return code
