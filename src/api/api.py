from ninja import NinjaAPI
from django.conf import settings

# Create the API instance
api = NinjaAPI(
    title="Petition Management API",
    version="1.0.0",
    description="API for managing petitions and signatures",
    docs_url="/docs" if settings.DEBUG else None,
)

# Import and include routers from endpoints
from src.api.endpoints.petitions import router as petitions_router

# Add routers to the API
api.add_router("/petitions/", petitions_router)
