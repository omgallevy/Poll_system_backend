from repository.database import database

TABLE_NAME_USER_ANSWERS = "user_answer"
TABLE_NAME_OPTIONS = "options"
TABLE_NAME_QUESTIONS = "questions"


async def get_option_counts_by_question(question_id: int):
    query = f"""
        SELECT
            {TABLE_NAME_QUESTIONS}.question_text, 
            {TABLE_NAME_OPTIONS}.option_text, 
            {TABLE_NAME_USER_ANSWERS}.chosen_option_id
        FROM {TABLE_NAME_USER_ANSWERS}
        JOIN {TABLE_NAME_OPTIONS} 
        ON {TABLE_NAME_USER_ANSWERS}.chosen_option_id = {TABLE_NAME_OPTIONS}.option_id
        JOIN {TABLE_NAME_QUESTIONS}
        ON {TABLE_NAME_USER_ANSWERS}.question_id = {TABLE_NAME_QUESTIONS}.question_id
        WHERE {TABLE_NAME_USER_ANSWERS}.question_id = :question_id
    """
    return await database.fetch_all(query, values={"question_id": question_id})


async def get_total_answers(question_id: int):
    query = f"""
        SELECT 
            {TABLE_NAME_QUESTIONS}.question_text,
            {TABLE_NAME_OPTIONS}.option_text,
            {TABLE_NAME_USER_ANSWERS}.user_id,
            {TABLE_NAME_USER_ANSWERS}.chosen_option_id
        FROM {TABLE_NAME_USER_ANSWERS}
        JOIN {TABLE_NAME_QUESTIONS} 
        ON {TABLE_NAME_USER_ANSWERS}.question_id = {TABLE_NAME_QUESTIONS}.question_id
        JOIN {TABLE_NAME_OPTIONS}
        ON {TABLE_NAME_USER_ANSWERS}.chosen_option_id = {TABLE_NAME_OPTIONS}.option_id
        WHERE {TABLE_NAME_USER_ANSWERS}.question_id = :question_id
    """
    return await database.fetch_all(query, values={"question_id": question_id})


async def get_user_answers(user_id: int):
    query = f"""
        SELECT 
            {TABLE_NAME_QUESTIONS}.question_text, 
            {TABLE_NAME_OPTIONS}.option_text
        FROM {TABLE_NAME_USER_ANSWERS}
        JOIN {TABLE_NAME_QUESTIONS} ON {TABLE_NAME_USER_ANSWERS}.question_id = {TABLE_NAME_QUESTIONS}.question_id
        JOIN {TABLE_NAME_OPTIONS} ON {TABLE_NAME_USER_ANSWERS}.chosen_option_id = {TABLE_NAME_OPTIONS}.option_id
        WHERE {TABLE_NAME_USER_ANSWERS}.user_id = :user_id
    """
    return await database.fetch_all(query, values={"user_id": user_id})


async def get_total_questions_answers_by_user(user_id: int):
    query = f"""
            SELECT 
                {TABLE_NAME_QUESTIONS}.question_id,
                {TABLE_NAME_QUESTIONS}.question_text
            FROM {TABLE_NAME_USER_ANSWERS}
            JOIN {TABLE_NAME_QUESTIONS} 
            ON {TABLE_NAME_USER_ANSWERS}.question_id = {TABLE_NAME_QUESTIONS}.question_id
            WHERE {TABLE_NAME_USER_ANSWERS}.user_id = :user_id
        """
    return await database.fetch_all(query, values={"user_id": user_id})
