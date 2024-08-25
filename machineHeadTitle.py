import pyautogui
import time
import random
import inspect
import json
import os
from PIL import ImageGrab
from transitions import Machine, State
from config import PLATFORM, PREFIX
import socket
from queue import Empty
# Constants for image paths
image_paths = {
    "toutiao": [PREFIX + "favorite.png", PREFIX + "headfavar.png"],
    "weibo": [PREFIX + "favorite.png", PREFIX + "headfavar.png"],
    "bili": [PREFIX + "favorite.png", PREFIX + "headfavar.png"]
}

image_path, next_pic = image_paths.get(PLATFORM, [None, None])

# OCR failure message image and delay settings
failed_image = 'failedImage.png'

delay = 2

min_delay = 2        # 最小延迟时间为2秒
max_delay = 100      # 最大延迟时间为10分钟（600秒）
delay = random.uniform(min_delay, max_delay)


scroll_time = 30
wait_time = 10 * 60 * 60

def debug_print(message):
    frame = inspect.currentframe().f_back
    line_number = frame.f_lineno
    file_name = inspect.getframeinfo(frame).filename
    print(f"[DEBUG] {file_name}, Line {line_number}: {message}")

def locate_and_click(image):
    try:
        location = pyautogui.locateCenterOnScreen(image)
        if location:
            x, y = location
            pyautogui.click(x, y)
            debug_print(f"Found and clicked on image: {image}")
            return True
        else:
            debug_print(f"Image not found: {image}")
            return False
    except Exception as e:
        debug_print(f"Exception when locating image: {image}, Exception: {e}")
        return False

def random_scroll_and_click(image):
    my_array = [random.randint(-350, -100) for _ in range(scroll_time)]
    for i, scroll_amount in enumerate(my_array):
        try:
            time.sleep(delay)
            pyautogui.scroll(scroll_amount)
            if locate_and_click(image):
                return True
        except Exception as e:
            debug_print(f"Scroll attempt {i+1}/{scroll_time} failed, Exception: {e}")
    return False


def capture_center_screenshot(save_path, crop_width, crop_height):
    screen = ImageGrab.grab()
    debug_print("capture_center_screenshot")
    screen_width, screen_height = screen.size

    left = (screen_width - crop_width) // 2
    top = (screen_height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height

    center_crop = screen.crop((left, top, right, bottom))
    center_crop.save(save_path)
    debug_print("capture_center_screenshot " + save_path)

    return save_path


def send_image_path(img_path, host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        client_socket.send(img_path.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
    finally:
        client_socket.close()

    return response


class ScriptStateMachine:
    states = [
        State(name='click'),
        State(name='ocr_check'),
        State(name='wait')
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=ScriptStateMachine.states, initial='click')

        self.machine.add_transition(trigger='to_ocr_check', source='click', dest='ocr_check')
        self.machine.add_transition(trigger='to_click', source='ocr_check', dest='click')
        self.machine.add_transition(trigger='wait_state', source='ocr_check', dest='wait', after='perform_wait')
        self.machine.add_transition(trigger='restart', source='wait', dest='click')

    def perform_wait(self):
        debug_print(f"Waiting for {wait_time} seconds (10 hours).")
        time.sleep(wait_time)

    def run(self):
        while True:
            if self.is_click():
                debug_print("Click state: Attempting to locate and click image.")
                # locate_and_click(image_path)
                locate_and_click(image_path)
                random_scroll_and_click(image_path)
                self.to_ocr_check()

            elif self.is_ocr_check():
                debug_print("OCR check state.")
                screenshot_path = "pic/screenshot.png"
                if os.path.exists(screenshot_path):
                    os.remove(screenshot_path)
                time.sleep(2)

                crop_width = 300
                crop_height = 100
                capture_center_screenshot(screenshot_path, crop_width, crop_height)

                # Send the image to the OCR server and wait for the result
                ocr_found = send_image_path(screenshot_path)
                if "Found: True" in ocr_found:
                    debug_print("OCR found the target text. Entering wait state.")
                    self.wait_state()
                else:
                    debug_print("OCR did not find the target text. Returning to click state.")
                    self.to_click()

            elif self.is_wait():
                debug_print("Wait state completed. Restarting process.")
                self.restart()


if __name__ == "__main__":
    state_machine = ScriptStateMachine()
    state_machine.run()
