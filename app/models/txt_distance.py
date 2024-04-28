from pydantic import BaseModel, Field, StrictStr
from enum import Enum
from typing import Union

class AlgNameEnum(str, Enum):
    HAMMING             = 'hamming'
    MLIPNS              = 'mlipns'
    LEVENSHTEIN         = 'levenshtein'
    DAMERAU_LEVENSHTEIN = 'damerau_levenshtein'
    JARO_WINKLER        = 'jaro_winkler'
    JARO                = 'jaro'
    STRCMP95            = 'strcmp95'
    NEEDLEMAN_WUNSCH    = 'needleman_wunsch'
    GOTOH               = 'gotoh'
    SMITH_WATERMAN      = 'smith_waterman'

class TxtDistanceRequest(BaseModel):
    alg: AlgNameEnum = Field(default=AlgNameEnum.STRCMP95, title="algorithm_name", description="Назва алгоритму за яким буде проведено порівняння")
    text_1: StrictStr = Field(..., title="text_1", description="Перше слово", example="leviathan")
    text_2: StrictStr = Field(..., title="text_2", description="Друге слово", example="leviamur")

class TxtDistanceResponse(BaseModel):
    similarity: Union[int, float] = Field(..., title="result", description="Результат обчислення", example=1)
    alg: AlgNameEnum = Field(default=AlgNameEnum.STRCMP95, title="algorithm_name", description="Назва алгоритму за яким буде проведено порівняння")
    text_1: StrictStr = Field(..., title="text_1", description="Перше слово", example="leviathan")
    text_2: StrictStr = Field(..., title="text_2", description="Друге слово", example="leviamur")