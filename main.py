from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import paho.mqtt.client as mqtt
import time
import asyncio
import paho.mqtt.client as mqtt
import time  # 메시지 전송 간격을 위해 추가
import atexit
# Broker address
broker_address = "10.150.150.177"
client1 = mqtt.Client("python_pub_1")  # 발행자 역할을 반영하도록 이름 변경

app = FastAPI()

# Callback for successful connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client1.on_connect = on_connect

# # Connect to broker
client1.connect(broker_address, 1883)
client1.loop_start()  # 백그라운드에서 네트워크 루프 시작

# 메시지 발행 루프
def send_direction(direction):
    try:
        # MQTT 연결 상태 확인
        if not client1.is_connected():
            print("Error: MQTT broker not connected. Attempting to reconnect...")
            client1.reconnect()
        
        # 메시지 발행 및 결과 확인
        result = client1.publish("jetson/jetson", direction)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Successfully published direction: {direction}")
            return True
        else:
            print(f"Failed to publish direction: {direction}, Error code: {result.rc}")
            return False
    except Exception as e:
        print(f"Error sending direction: {e}")
        return False


def handle_exit():
    print("발행자 종료")
    client1.loop_stop()
    client1.disconnect()

@app.get("/aaaaa")
def pub(topic_str="jetson/jetson", message_str="hello world"):
    mqttc = mqtt.Client("python_pub")
    try:
        mqttc.connect("10.150.150.177", 1883)
        mqttc.publish(topic_str, message_str)  # 하드코딩된 값 대신 매개변수 사용
    finally:
        mqttc.disconnect()  # 연결 종료
    return {"status": "success", "topic": topic_str, "message": message_str}  # 응답 추가

# 정적 파일 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/stop")
async def read_control():
    send_direction("4")
    return "스탑이요"

@app.get("/control")
async def read_control():
    return FileResponse("static/control.html")

@app.get("/map")
async def read_map():
    return FileResponse("static/map.html")

@app.get("/up")
async def up():
    print("1")
    send_direction("0")
    return JSONResponse(content={"message": "up"})

@app.get("/down")
async def down():
    print("2")
    send_direction("1")
    return JSONResponse(content={"message": "down"})

@app.get("/right")
async def right():
    print("3")
    send_direction("3")
    return JSONResponse(content={"message": "right"})

@app.get("/left")
async def left():
    print("4")
    send_direction("2")
    return JSONResponse(content={"message": "left"})

@app.get("/mapping")
async def mapping():
    print("5")
    return JSONResponse(content={"message": "mapping"})

@app.get("/speed/{speed_value}")
async def set_speed(speed_value: int):
    # 입력값 범위 검증 (20-80)
    if speed_value < 20 or speed_value > 80:
        return JSONResponse(
            status_code=400,
            content={"error": "Speed must be between 20 and 80"}
        )
    # 20-80 범위를 5-9 범위로 변환
    mapped_speed = 5 + ((speed_value - 20) * 4 // 60)
    send_direction(str(mapped_speed))  # 문자열로 변환하여 전송
    return f"스피드는 {speed_value} (변환된 값: {mapped_speed})이에오"

atexit.register(handle_exit) 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
