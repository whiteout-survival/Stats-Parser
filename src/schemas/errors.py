from typing import List, Optional, Union
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    loc: Optional[List[Union[str, int]]] = Field(default=None, description="Location of the error")
    msg: Optional[str] = Field(default=None, description="Error message for this field")
    type: Optional[str] = Field(default=None, description="Error type identifier")


class ErrorResponse(BaseModel):
    code: str = Field("error", description="Error code")
    detail: str = Field(..., description="Human-readable error message")
    errors: Optional[List[ErrorDetail]] = Field(default=None, description="Optional list of errors")
