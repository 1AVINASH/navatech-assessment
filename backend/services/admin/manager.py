from services.admin.repository import Admin as AdminRepository

class AdminManager:
    def __init__(self):
        self._initialized = False
        self._admin_repository = None

    async def initialize(self):
        if not self._initialized:
            self._admin_repository = AdminRepository()
            await self._admin_repository.initialize()
            # Initialize other services/models here
            self._initialized = True

    @property
    def repository(self):
        if self._admin_repository is None:
            raise ValueError("Admin repository is not initialized")
        return self._admin_repository

# Singleton instance
admin_manager: AdminManager = AdminManager()
