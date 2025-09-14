from break_into_questions import build_semantic_rag_queries

API_KEY = "gk-lg2FEI1z_oknwrbbbuya"

user_question = "Compare Apple and Google's financial performance."
sub_questions = build_semantic_rag_queries(user_question, API_KEY)

for i, q in enumerate(sub_questions, 1):
    print(f"{i}. {q}")
