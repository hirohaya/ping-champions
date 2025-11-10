from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import events, matches, players, ranking

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Adiciona o middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Ou especifique o endereço do frontend, ex: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(events.router)
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(ranking.router)

@app.get("/")
def root():
    return {"message": "Ping Champions Backend API"}
