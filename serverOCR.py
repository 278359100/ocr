import socket
import threading
import socket
import threading
import time
import os
from queue import Queue
from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID
from config import WECHAT_OCR_DIR, WECHAT_DIR, TARGET_TEXT,OUTPUT_SUFFIX
#wechat_ocr_dir = r"C:\Users\Sam\AppData\Roaming\Tencent\WeChat\XPlugin\Plugins\WeChatOCR\7079\extracted\WeChatOCR.exe"
#wechat_dir = r"C:\Program Files\Tencent\WeChat\[3.9.11.25]"
#OUTPUT_SUFFIX = "8-11.json"
#TARGET_TEXT = "操作失败，请稍后重试"
image_paths = Queue()
ocr_results = Queue()
# 创建一个全局的 OcrManager 实例
ocr_manager = None

def ocr_result_callback(img_path: str, results: dict):
    found = any(result['text'] == TARGET_TEXT for result in results.get('ocrResult', []))
    result_file = img_path + OUTPUT_SUFFIX
    print(f"OCR completed, img_path: {img_path}, result_file: {result_file}, found: {found}")
    ocr_results.put(found)
def ocr_task_processor():
    global ocr_manager
    while True:
        img_path = image_paths.get()
        if img_path is None:
            print(f"img_path is None: {img_path}")
            ocr_results.put(False)  # 返回False
            break

        if not os.path.isfile(img_path):
            print(f"Invalid image path: {img_path}")
            ocr_results.put(False)  # 返回False
            break
            # continue

        print(f"Processing image: {img_path}")
        try:
            ocr_manager.DoOCRTask(img_path)
            time.sleep(1)
            while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
                pass
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")

    # ocr_manager.KillWeChatOCR()

def start_ocr_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    def client_handler(client_socket):
        while True:
            img_path = client_socket.recv(1024).decode('utf-8')
            if not img_path:
                break

            print(f"Received image path: {img_path}")
            # Process the image and respond to the client
            found = process_single_image(img_path)
            client_socket.send(f"Processed: {img_path}, Found: {found}".encode('utf-8'))

        client_socket.close()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=client_handler, args=(client_socket,)).start()

def add_image_to_queue(img_path):
    image_paths.put(img_path)

def process_single_image(img_path):
    # 启动OCR处理线程
    threading.Thread(target=ocr_task_processor, daemon=True).start()
    add_image_to_queue(img_path)
    time.sleep(1)  # 等待OCR处理
    while image_paths.qsize() > 0:
        time.sleep(1)  # 等待OCR完成处理

    # 等待OCR结果
    result = ocr_results.get()  # 从队列中获取OCR结果
    return result  # 根据OCR结果返回True或False

if __name__ == "__main__":
    # 初始化 OcrManager 并启动 WeChatOCR
    ocr_manager = OcrManager(WECHAT_DIR)
    ocr_manager.SetExePath(WECHAT_OCR_DIR)
    ocr_manager.SetUsrLibDir(WECHAT_DIR)
    ocr_manager.SetOcrResultCallback(ocr_result_callback)
    ocr_manager.StartWeChatOCR()
    # 启动服务器
    start_ocr_server()

