import websocket
import threading

data = 0
locked = False

def ML_calculation(ws):
    global data
    global locked

    local_data = 0
    while (True):
        local_data = local_data + 1
        if not locked:
            locked = True
            data = local_data
            locked = False


def run_ml_calculation(ws):
    ml_thread = threading.Thread(target=ML_calculation, args=(ws,))
    ml_thread.start()

def on_message(ws, message):
    print("Received message from server:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, x, y):
    print("Connection closed")

def on_open(ws):
    print("Connected to server!")

    # Start ML calculation in a separate thread
    run_ml_calculation(ws)

if __name__ == "__main__":
    # WebSocket client
    ws = websocket.WebSocketApp("ws://localhost:8080",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.on_open = on_open
    
    # Run the WebSocket client
    ws.run_forever()
