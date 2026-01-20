## V2 ##

from fastapi import FastAPI
from app.api.routes import auth_routes, order_routes, root_routes
from app.core.config import settings
from app.core.middlewares import setup_cors
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Delivery API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
setup_cors(app)

app.include_router(root_routes.root_routes)
app.include_router(auth_routes.auth_router)
app.include_router(order_routes.order_router)

# para rodar: uvicorn main:app --reload (Cria um servidor local para o arquivo main.py)

# Rest APIS (CRUD)
# Get -> leitura/pegar
# Post -> criar/enviar
# Put/Patch -> edição
# Delete -> deletar/remover
