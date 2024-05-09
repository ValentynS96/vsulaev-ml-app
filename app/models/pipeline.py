from typing import List, Any, Optional
from pydantic import BaseModel, Field, StrictStr
from enum import Enum

class Models(str, Enum):
    KNearest_Neighbors="KNearest_Neighbors",
    Logistic_Regression="Logistic_Regression",
    Naive_Bayes="Naive_Bayes",
    Support_Vector_Classifier="Support_Vector_Classifier"


class PipelineReq(BaseModel):
    input: Any = Field(..., title="input", description="Input words", example="The quick brown fox jumps over the lazy dog")
    models: Models = Field(..., title="models", description="Model name `KNearest_Neighbors` `Logistic_Regression` `Naive_Bayes` `Support_Vector_Classifier`")
    options: Optional[list] = Field(..., title="options", description="Preprocessing options `use_tokenize` | `use_stopwords` | `use_stemming` | `use_lemmatize` | `use_lowers`", example=["use_tokenize", "use_stopwords", "use_stemming" ,"use_lemmatize" , "use_lowers"])