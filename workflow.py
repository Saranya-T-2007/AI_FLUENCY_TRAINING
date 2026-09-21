import re
from config import COURSE_FEES, QUESTIONS


def get_course_code(text):
    match = re.search(r"\b(CS101|AI202|DS303)\b", text.upper())
    return match.group(1) if match else None


def workflow(question):
    q = question.lower()

    if "fee" in q:
        course = get_course_code(question)

        if course:
            return f"The fee for {course} is Rs. {COURSE_FEES[course]:,}."

    if "total" in q and "scholarship" in q:
        courses = re.findall(r"\b(CS101|AI202|DS303)\b", question.upper())

        if len(courses) >= 2:
            total = COURSE_FEES[courses[0]] + COURSE_FEES[courses[1]]
            final_fee = total * 0.90
            return f"After 10% scholarship, the total fee is Rs. {final_fee:,.0f}."

    return "I cannot handle this question using my fixed rules."


for question in QUESTIONS:
    print("\nQuestion:", question)
    print("Answer:", workflow(question))