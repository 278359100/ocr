import pyautogui
import time

# 给自己一些时间移动鼠标到目标位置
print("请在5秒内将鼠标移动到目标位置...")
time.sleep(5)

# 获取当前鼠标位置
current_position = pyautogui.position()
print(f"当前鼠标坐标: {current_position}")