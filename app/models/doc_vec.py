from typing import List, AnyStr
from pydantic import BaseModel, Field

EXAMPLE = [
        "The computer needs to be repaired because it's running very slowly.",
        "I recently bought a new smartphone, and I'm very happy with its performance.",
        "The latest update to the software includes several bug fixes and new features.",
        "The book provides a comprehensive overview of the history of artificial intelligence.",

        "The government has introduced new policies to combat climate change.",
        "Many people are concerned about the economic impact of the pandemic.",
        "The new tax regulations will affect small businesses significantly.",
        "A recent study showed that the unemployment rate is steadily decreasing.",

        "The new restaurant in town has received excellent reviews.",
        "The movie was very entertaining and had a lot of action scenes.",
        "The concert last night was amazing, and the band played all their hit songs.",
        "The latest fashion show featured designs from top international designers."
]

class SentencesReq(BaseModel):
    sentences: List[AnyStr] = Field(..., title="list of sentences", description="Input list of sentences", example=EXAMPLE)
