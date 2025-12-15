from abc import ABC, abstractmethod
from typing import List, Optional
from shared.models.crumb import Crumb

class Database(ABC):
    
    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def create_crumb(self, crumb: Crumb) -> Crumb:
        pass
    
    @abstractmethod
    def get_crumb(self, crumb_id: str) -> Optional[Crumb]:
        pass
    
    @abstractmethod
    def get_all_crumbs(self) -> List[Crumb]:
        pass
    
    @abstractmethod
    def update_crumb(self, crumb_id: str, crumb: Crumb) -> Optional[Crumb]:
        pass
    
    @abstractmethod
    def delete_crumb(self, crumb_id: str) -> bool:
        pass