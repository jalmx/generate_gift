#!/usr/bin/env python

import json
from pathlib import Path
from sys import argv
from os import path
import random


HELP = """
How to use:

    ggift <path_src_questions>.txt prefix_question
    ggift <path_src_questions>.txt prefix_question <random_answer>.json

    ggift exam_p1.txt "P2_"
    ggift exam_p1.txt "P2_" random.json
"""


def _clear_sentence(question: str) -> str:
    """clear the question if contain number to start que sentence

    Args:
        question (str): Sentence string

    Returns:
        str: Sentence clear, without number and any space
    """
    question = question.strip()
    if question[0].isdigit() or question[0].startswith("-"):
        position = question.find(" ")
        return question[position:].strip()

    return question.strip()


def _generate_txt_questions_base(
    txt: str, answer: str, number: int, name_question="question"
) -> str:
    txt_parse = (
        f'// question: {number}  name: {name_question}\n::{name_question}::[html]<p dir\="ltr" style\="text-align\: left;">{_clear_sentence(txt)}<br></p>'
        + "{"
        + answer
        + "}"
    )
    return txt_parse


def _generate_answers(answer: str, answers_wrong: list):

    answer_ok = f'\n\t=<p dir\="ltr" style\="text-align\: left;">{_clear_sentence( answer)}<br></p>\n'

    answer_final = answer_ok

    for answer_wrong in answers_wrong:

        answer_final += f'\t~<p dir\="ltr" style\="text-align\: left;">{_clear_sentence(answer_wrong)}<br></p>\n'

    return answer_final


def _generate_question_multi(
    txt: str, answer: str, number: int, wrong_answer: list, name_question="question"
) -> str:
    answer = _generate_answers(answer=answer, answers_wrong=wrong_answer)

    return _generate_txt_questions_base(
        txt=txt, answer=answer, number=number, name_question=name_question
    )


def _is_true_question(answer: str):
    return "TRUE" if _clear_sentence(answer).upper() == "Verdadero".upper() else "FALSE"


def _generate_question_bool(
    txt: str, answer: str, number: int, name_question="question"
) -> str:
    answer = _is_true_question(answer=answer)

    return _generate_txt_questions_base(
        txt=txt, answer=answer, number=number, name_question=name_question
    )


def parse_question_gift(
    txt: str,
    answer: str,
    number: int,
    number_raw_question: int,
    wrong_answer: dict | None,
    name_question="question",
):

    if wrong_answer and wrong_answer.get(str(number_raw_question)):
        return _generate_question_multi(
            txt=txt,
            answer=answer,
            number=number,
            wrong_answer=wrong_answer.get(str(number_raw_question)),
            name_question=name_question,
        )
    else:
        txt = _generate_question_bool(
            txt=txt, answer=answer, number=number, name_question=name_question
        )
        return txt


def read_file(path_file):
    """Reade file from path and return all content in str"""

    with open(path_file, mode="r") as f:
        return f.read()


def template_header(name_course=None):
    name_course = name_course or "WITHOUT COURSE"

    return f"""// question: 0  name: Switch category to $course$/top/Por defecto en {name_course}
$CATEGORY: $course$/top/Por defecto en {name_course}"""


def _clear_questions(txt):
    content_raw = txt.replace("\t", "").split("\n")
    content_pre = []

    for line in content_raw:
        if len(line) > 0:
            content_pre.append(line)

    start = False
    content = []
    for line in content_pre:
        if str(line)[0].isdigit() or start:
            start = True
            content.append(line)

    return content


def parse_questions(txt: str, prefix_question="Q0", data=dict | None) -> list:
    """Take the content from file with questions to generate a list with questions to load in a new file"""

    content_raw = _clear_questions(txt)
    questions = []

    count = 0

    number_base = random.randint(800, 8000)
    offset = random.randint(20, 50)

    count_question = 1
    while count < len(content_raw):
        question = content_raw[count]
        count += 1
        answer = content_raw[count]
        count += 1
        name_question = f"{prefix_question}_Q{count_question}"
        questions.append(
            parse_question_gift(
                question,
                answer,
                number=(number_base + offset + count_question),
                name_question=name_question,
                wrong_answer=data,
                number_raw_question=count_question,
            )
        )
        count_question += 1

    return questions


def build_file(path, questions):
    """Save the final file

    Args:
        path (str): path to save the file
        questions (list): All questions to save in list
    """
    with open(path, mode="w+") as f:

        for txt in questions:
            f.write(txt + "\n\n\r")

    print(f"File saved: {path}")


def create_name(path_file: str) -> str:
    """Generare the name file will save gift.txt

    Args:
        path_file (str): path from file to input

    Returns:
        str: new name for the file <name>_gift.txt
    """
    name_full = path.basename(path_file)
    name = path.splitext(name_full)[0]
    name += "_gift.txt"
    return name


def main():

    try:
        if len(argv) == 1:
            print("ERROR")
            print(HELP)
            
        elif argv[1] == "-h" or argv[1] == "--help":
            print("help:")
            print(HELP)
            exit(0)
            return

        elif len(argv) >= 2 or len(argv) <= 4:
            json_answer_wrong = None
            path_question = Path(argv[1])
            name_gift_file = create_name(path_question)

            prefix_question = argv[2]

            if len(argv) == 4:
                json_path = argv[3]
                with open(json_path, mode="r") as f:
                    json_answer_wrong = json.load(f)

            text = read_file(path_question)
            questions = parse_questions(
                text, prefix_question=prefix_question, data=json_answer_wrong
            )
            questions.insert(0, template_header(name_gift_file))

            build_file(name_gift_file, questions)
        else:
            print("ERROR")
            print(HELP)
    except:
        pass


if __name__ == "__main__":
    main()
