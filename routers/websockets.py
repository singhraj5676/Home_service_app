
# from typing import List, Dict
# from fastapi import WebSocket, WebSocketDisconnect

# class WebSocketManager:
#     def __init__(self):
#         self.connections: Dict[uuid.UUID, List[WebSocket]] = {}



#     async def connect(self, chat_id: id , websocket: WebSocket):
#         await websocket.accept()
#         if chat_id not in self.connections:
#             self.connections[chat_id] = []
#         self.connections[chat_id].append(websocket)

    
#     async def disconnect(self, chat_id: id, websocket: WebSocket):
#         if chat_id in self.connections:
#             self.connections[chat_id].remove(websocket)
#             if not self.connections[chat_id]:
#                 del self.connections[chat_id]

#     async def broadcast(self, chat_id: id, message: str):
#         if chat_id in self.connections:
#             for websocket in self.connections[chat_id]:
#                 await websocket.send_text(message)

# manager = WebSocketManager()


# @app.websocket("/ws/chat/{chat_id}")
# async def websocket_endpoint(chat_id: id, websocket: WebSocket):
#     await manager.connect(chat_id, websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()

#             message_create = MessageCreate(
#                 chat_id = chat_id,
#                 sender_id =  , 
#                 text = data
#             )
#             response = await create_message(message_create)
#             await manager.broadcast(chat_id, f"Message from {websocket.client[0]}: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(chat_id,websocket)
#         await manager.broadcast(chat_id, "A user has left the chat. ")

