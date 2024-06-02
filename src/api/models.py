from pydantic import BaseModel


class Question(BaseModel):
    question: str
    answer_1: str
    answer_2: str
    answer_3: str
    answer_4: str
    correct_answer: str


class Test(BaseModel):
    test_name: str
    quest_1: Question
    quest_2: Question
    quest_3: Question
    quest_4: Question
    quest_5: Question
    quest_6: Question
    quest_7: Question
    quest_8: Question
    quest_9: Question
    quest_10: Question
