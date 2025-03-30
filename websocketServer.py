import asyncio
import websockets
import torch
import cv2
import numpy as np
import warnings
warnings.simplefilter("ignore", category=FutureWarning)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.6  # Confidence threshold

def get_natural_description(detections, frame_width):
    positions = {"left": [], "center": [], "right": []}
    
    for _, row in detections.iterrows():
        obj = row['name']
        x_center = (row['xmin'] + row['xmax']) / 2  # Find center of object
        
        # Categorize object position to left, right, center
        if x_center < frame_width * 0.4:
            positions["left"].append(obj)
        elif x_center > frame_width * 0.6:
            positions["right"].append(obj)
        else:
            positions["center"].append(obj)

    descriptions = []

    # Generate description to convert to speech
    for position, objs in positions.items():
        if objs:
            unique_objs = set(objs)
            count = {obj: objs.count(obj) for obj in unique_objs}

            if len(count) == 1:
                obj, num = list(count.items())[0]
                if num == 1:
                    descriptions.append(f"A {obj} is {position} of you.")
                else:
                    descriptions.append(f"{num} {obj}s are {position} of you.")
            else:
                obj_list = [f"{num} {obj}s" if num > 1 else f"a {obj}" for obj, num in count.items()]
                descriptions.append(f"{', '.join(obj_list)} are {position} of you.")

    if descriptions:
        speech = " ".join(descriptions)
        # print("Saying:", speech)
        return speech



async def process_frame(websocket):
    while True:
        frame_data = await websocket.recv()
        np_arr = np.frombuffer(frame_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        frame_width = frame.shape[1]
        # Convert frame to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = model(frame)
        frame_width = frame.shape[1]
        detections = results.pandas().xyxy[0]  # Get results as Pandas DataFrame
        speech = get_natural_description(detections, frame_width)

        # rendered_img = results.render()[0]  # Extract the first image from the list
        # rendered_img = cv2.cvtColor(rendered_img, cv2.COLOR_RGB2BGR)
        if speech is not None:
            await websocket.send(speech)
        else:
            await websocket.send("")
        # cv2.imshow('YOLOv5 Detection', rendered_img)
            
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

async def start_server():
    # uncomment bottom lines for cross device connection
    server = await websockets.serve(process_frame, '10.25.248.243', 8765)  
    print("Server running on ws:// 10.25.248.243:8765")
    # uncomment bottom lines for localhost server
    # server = await websockets.serve(process_frame, "localhost", 8765)
    # print("Server running on ws://localhost:8765")
    await server.wait_closed()  # Keep the server running

# Run the WebSocket server
asyncio.run(start_server())
