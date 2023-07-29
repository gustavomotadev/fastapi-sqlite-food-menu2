from fastapi import FastAPI
import api_cardapios
import api_produtos

app = FastAPI()
 
app.include_router(api_cardapios.router)
app.include_router(api_produtos.router)