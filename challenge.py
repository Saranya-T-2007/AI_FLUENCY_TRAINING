from config import COURSE_FEES

budget = 30000

courses = list(COURSE_FEES.keys())

print("Budget: Rs.", budget)

for i in range(len(courses)):
    for j in range(i + 1, len(courses)):

        c1 = courses[i]
        c2 = courses[j]

        total = COURSE_FEES[c1] + COURSE_FEES[c2]

        if total <= budget:
            print(
                f"You can take {c1} + {c2} "
                f"for Rs. {total:,}"
            )