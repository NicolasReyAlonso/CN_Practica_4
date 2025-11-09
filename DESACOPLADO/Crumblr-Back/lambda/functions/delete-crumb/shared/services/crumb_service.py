from shared.db.factory import DatabaseFactory
from shared.models.crumb import Crumb

class CrumbService:
    def __init__(self):
        self.db = DatabaseFactory.create()

    def create_crumb(self, data: dict) -> Crumb:
        crumb = Crumb(**data)
        return self.db.create_crumb(crumb)

    def get_crumb(self, crumb_id: str) -> Crumb:
        crumb = self.db.get_crumb(crumb_id)
        if not crumb:
            raise ValueError("Crumb not found")
        return crumb

    def get_all_crumbs(self):
        return self.db.get_all_crumbs()

    def update_crumb(self, crumb_id: str, data: dict) -> Crumb:
        data.pop('crumb_id', None)
        data.pop('created_at', None)
        crumb = Crumb(**data)
        updated = self.db.update_crumb(crumb_id, crumb)
        if not updated:
            raise ValueError("Crumb not found")
        return updated

    def delete_crumb(self, crumb_id: str) -> bool:
        deleted = self.db.delete_crumb(crumb_id)
        if not deleted:
            raise ValueError("Crumb not found")
        return deleted