from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import datetime
import uuid

class Crumb:
    def __init__(self, crumb_id=None, content='', image_url=None, created_at=None):
        self.crumb_id = crumb_id or str(uuid.uuid4())
        self.content = content
        self.image_url = image_url
        self.created_at = created_at or datetime.utcnow()
