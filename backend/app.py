"""
Entry point for the app
"""

# Let's create a FastAPI app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routes.agent.main import router as agent_router
from api.v1.routes.project.main import router as project_router
from api.v1.routes.node.main import router as node_router


app = FastAPI()

# Let's enable cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router, prefix="/api/v1")
app.include_router(node_router, prefix="/api/v1")
app.include_router(agent_router, prefix="/api/v1")
