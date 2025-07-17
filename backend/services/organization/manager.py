from services.organization.repository import Organization as OrganizationRepository

class OrganizationManager:
    def __init__(self):
        self._initialized = False
        self.organization_repository = None

    async def initialize(self):
        if not self._initialized:
            self.organization_repository = OrganizationRepository()
            await self.organization_repository.initialize()
            # Initialize other services/models here
            self._initialized = True

# Singleton instance
org_manager: OrganizationManager = OrganizationManager()
