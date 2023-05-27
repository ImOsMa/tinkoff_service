from fastapi import FastAPI
from operations.router import router as user_router
from instruments.router import router as instruments_router
from orders.router import router as orders_router
from robot.router import router as robot_router

app = FastAPI(
    title="Tinkoff Service"
)


@app.get("/")
def get_hello():
    return "Tinkoff Service"

app.include_router(user_router)
app.include_router(instruments_router)
app.include_router(orders_router)
app.include_router(robot_router)
