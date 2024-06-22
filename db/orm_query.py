from db.models import Questions
from sqlalchemy import delete, select

async def create_question(chat_id, text, session):
    obj = Questions(
        chat_id = chat_id,
        question = text
    )
    session.add(obj)
    await session.commit()

async def create_answer(text, session):
    query = select(Questions.chat_id).where(Questions.question == text)
    data = await session.execute(query)
    chat_id = data.scalar()

    query2 = delete(Questions).where(Questions.question == text)
    data = await session.execute(query2)
    await session.commit()

    return chat_id