from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ResumeResponseSchema(BaseModel):
    id: int
    file_name: str
    stored_file_name: str
    file_path: str
    candidate_id: int
    created_at: datetime
    
    # this tells pydantic that Read the values from the objects attributes instead of expecting a dictionary 
    model_config = ConfigDict(
        from_attributes=True,
    )