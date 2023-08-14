from fastapi import FastAPI
import api_cardapios
import api_produtos
import api_autenticacao

app = FastAPI()
 
app.include_router(api_cardapios.router)
app.include_router(api_produtos.router)
app.include_router(api_autenticacao.router)