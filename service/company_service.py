from repository import company_repository


async def get_option_counts_by_question(question_id: int):
    data = await company_repository.get_option_counts_by_question(question_id)

    if not data:
        raise ValueError(f"No data found for question ID {question_id}")

    question_text = data[0]["question_text"] if data else None

    unique_options = []

    for record in data:
        option_text = record["option_text"]

        for option in unique_options:
            if option["Option text"] == option_text:
                option["Count all users who answered"] += 1
                break
        else:
            unique_options.append({"Option text": option_text, "Count all users who answered": 1})

    return {
        "Question": {"Question ID": question_id, "Question text": question_text},
        "options": unique_options,
    }


async def get_total_answers(question_id: int):
    records = await company_repository.get_total_answers(question_id)

    if not records:
        raise ValueError(f"No answers found for question ID {question_id}")

    question_text = records[0]["question_text"] if records else None

    user_count = len(set(record["user_id"] for record in records))

    option_counts = {}
    for record in records:
        option_id = record["chosen_option_id"]
        option_text = record["option_text"]

        if option_id not in option_counts:
            option_counts[option_id] = {
                "option_text": option_text,
                "count": 0
            }
        option_counts[option_id]["count"] += 1

    option_counts_list = [
        {"option_id": option_id, "option_text": data["option_text"], "count": data["count"]}
        for option_id, data in option_counts.items()
    ]

    return {
        "question": question_text,
        "Total of all users who answered this question": user_count,
        "options": option_counts_list
    }


async def get_user_answers(user_id: int):
    records = await company_repository.get_user_answers(user_id)

    if not records:
        raise ValueError(f"No answers found for user ID {user_id}")

    formatted_answers = []
    for record in records:
        formatted_answers.append({
            "Question": record["question_text"],
            "Chosen Option": record["option_text"]
        })

    return {
        "User ID": user_id,
        "Total Answers": len(formatted_answers),
        "Answers": formatted_answers
    }


async def get_total_questions_answers_by_user(user_id: int):
    records = await company_repository.get_total_questions_answers_by_user(user_id)

    if not records:
        raise ValueError(f"No questions answered by user ID {user_id}")

    unique_questions = []
    question_ids = []

    for record in records:
        question_id = record["question_id"]
        question_text = record["question_text"]

        if question_id not in question_ids:
            question_ids.append(question_id)
            unique_questions.append({"Question id": question_id, "Question text": question_text})

    return {
        f"Total of all questions answered by the user with the ID {user_id} ": len(unique_questions),
        "questions": unique_questions
    }
