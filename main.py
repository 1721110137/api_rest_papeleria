from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from databases import Database

DATABASE_URL = "postgresql://admin:FHOlwnc9iPy9snMnazZhtS1IcTZa389Z@dpg-csgkh8btq21c73etcabg-a.oregon-postgres.render.com/db_papeleria"

database = Database(DATABASE_URL)
metadata = MetaData()

productos = Table(
    "productos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nombre", String(100)),
    Column("categoria", String(100)),
    Column("precio", Float),
    Column("cantidad", Integer),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Bienvenido a la API de la papelería. Visita /api/productos para ver los productos."}

@app.on_event("startup")
async def startup():
    await database.connect()
    
    query = productos.select()
    existing_products = await database.fetch_all(query)
    
    if not existing_products:
        query = productos.insert().values([
            {"nombre": "Lápiz HB", "categoria": "Útiles Escolares", "precio": 5.00, "cantidad": 100},
            {"nombre": "Cuaderno A5", "categoria": "Cuadernos", "precio": 30.00, "cantidad": 50}
        ])
        await database.execute(query)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/api/productos")
async def get_productos():
    query = productos.select()
    return await database.fetch_all(query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
