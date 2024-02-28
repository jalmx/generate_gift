import json 
from pathlib import Path
from sys import argv
from os import path


HELP = """
How to use:

    ggift <path_src_questions>.txt 
    ggift <path_src_questions>.txt <random_answer>.json

    ggift exam_p1.txt
    ggift exam_p1.txt  random.json
"""

def get_bank_answers(path: Path) -> list[str]:
    pass


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


def _is_true_question(answer: str):
    return "TRUE" if _clear_sentence(answer).upper() == "Verdadero".upper() else "FALSE"


def parse_question_gift(
    txt, answer: str, number=8000, name_question="question", db_answer=None
):

    answer = _is_true_question(answer=answer)

    txt_parse = (
        f'// question: {number}  name: {name_question}\n::{name_question}::[html]<p dir\="ltr" style\="text-align\: left;">{_clear_sentence(txt)}<br></p>'
        + "{"
        + answer
        + "}"
    )

    # print(f"The answer parsed: {txt_parse}")
    return txt_parse


def read_file(path_file):
    """Reade file from path and return all content in str"""

    with open(path_file, mode="r") as f:
        return f.read()


def template_header(name_course=None):
    name_course = name_course or "6 SLM 602 24-24 Electrónica Industrial"

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


def parse_questions(txt, type=None, name_question=None) -> list:
    """Take the content from file with questions to generate a list with questions to load in a new file"""
    content_raw = _clear_questions(txt)
    questions = (
        []
    )  # después sera un dict con las preguntas y respuestas, junto con las respuestas aleatorias
    count = 0
    number_base = (
        8000  # este numero inventado con base al que viene en el archivo descargado
    )
    count_question = 1
    while count < len(content_raw):
        question = content_raw[count]
        count += 1
        answer = content_raw[count]
        count += 1
        name_question = f"P1_P{count_question}"
        questions.append(
            parse_question_gift(
                question,
                answer,
                number=(number_base + 30 + count_question),
                name_question=name_question,
            )
        )
        count_question += 1

    return questions


def build_file(path, questions):
    with open(path, mode="w+") as f:

        for txt in questions:
            f.write(txt + "\n\n\r")

def create_name(path_file: str)-> str:
    """Generare the name file will save gift.txt

    Args:
        path_file (str): path from file to input

    Returns:
        str: new name for the file <name>_gift.txt
    """
    name_full =path.basename(path_file)
    name = path.splitext(name_full)[0]
    name += "_gift.txt"
    return name
    


def main():

    if len(argv) == 2 or len(argv) == 3:

        json_answer_wrong = None
        path_question = Path(argv[1])
        path_to_save = create_name(path_question)
        
        if len(argv) == 3:
            json_path = argv[2]
            with open(json_path, mode="r") as f:
                json_answer_wrong = json.load(f)
                print(json_answer_wrong)

        exit(0)
        text = read_file(path_question)
        questions = parse_questions(text)
        questions.insert(0, template_header())

        build_file(path_to_save, questions)
    else:
        # TODO: agregar el help
        print("ERROR")
        print(HELP)


if __name__ == "__main__":
    main()
