from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 정적 파일 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/control")
async def read_control():
    return FileResponse("static/control.html")

@app.get("/map")
async def read_map():
    return FileResponse("static/map.html")

@app.get("/up")
async def up():
    print("1")
    return JSONResponse(content={"message": "up"})

@app.get("/down")
async def down():
    print("2")
    return JSONResponse(content={"message": "down"})

@app.get("/right")
async def right():
    print("3")
    return JSONResponse(content={"message": "right"})

@app.get("/left")
async def left():
    print("4")
    return JSONResponse(content={"message": "left"})

@app.get("/mapping")
async def mapping():
    print("5")
    return JSONResponse(content={"message": "mapping"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
