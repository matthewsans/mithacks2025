from break_into_questions import break_down_financial_question

API_KEY = "gk-lg2FEI1z_oknwrbbbuya"

user_question = "ALT5 Sigma Corp revenue compared to Aeluma_ Inc"
sub_questions = break_down_financial_question(user_question, API_KEY)

for i, q in enumerate(sub_questions, 1):
    print(f"{i}. {q}")
