from typing import Any

from fastapi import APIRouter, Request

from app.models.txt_distance import TxtDistanceRequest, TxtDistanceResponse

from app.services.compare_text import compare_text

txt_distance_router = APIRouter()

@txt_distance_router.post("/txt_compare", response_model=TxtDistanceResponse, description="Ендпоінт приймає три параметри перший це назва алгоритму, другий та третій це слова для поріняння за алгоритмом `hamming` `mlipns` `levenshtein` `damerau_levenshtein` `jaro_winkler` `jaro` `strcmp95` `needleman_wunsch` `gotoh` `smith_waterman`")
async def compare(request: Request, payload: TxtDistanceRequest) -> Any:
    result = compare_text(payload.alg, payload.text_1, payload.text_2)
    return TxtDistanceResponse(result=result)