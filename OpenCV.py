import pyautogui
import time
import random

# 定义常量
import pyperclip

TRIGGER = 'pic/weitoutiao/trigger_area_template.png'
TEXTBOX_TEMPLATE = 'pic/weitoutiao/new_thing.png'
PUBLISH_BUTTON_TEMPLATE = 'pic/weitoutiao/publish_button_template.png'
VOID = 'pic/weitoutiao/void.png'

# 定义区域坐标和大小
area_x = 699  # 区域左上角 x 坐标
area_y = 258  # 区域左上角 y 坐标
area_width = 300  # 区域宽度
area_height = 100  # 区域高度

# 定义要填入的内容列表
texts_to_input = [
    "AI创造财富",
    "未来由我创造",
    "智慧改变生活",
    "技术赋能新未来",
    "探索未知的可能"
]

def click_trigger_or_void_area():
    # 等待触发区域出现
    time.sleep(2)  # 根据需要调整等待时间
    try:
        # 寻找触发区域的位置
        # 寻找触发区域的位置
        trigger_location = pyautogui.locateOnScreen(TRIGGER, confidence=0.7)

        if trigger_location is not None:
            x, y = pyautogui.center(trigger_location)
            pyautogui.click(x, y)  # 点击触发区域
            print("已点击触发区域，等待文本框出现。")
            return True

        print("未找到触发区域或 VOID 区域。")
        return False
    except pyautogui.ImageNotFoundException:
        print("未找到指定的图像，继续寻找...")
        return True  # 返回 False 继续循环


def click_in_area_and_type(text):
    # 等待一段时间以确保界面稳定
    time.sleep(2)  # 根据需要调整等待时间

    # 点击指定区域
    click_x = area_x + area_width // 2
    click_y = area_y + area_height // 2
    pyautogui.click(click_x, click_y)  # 点击文本框区域
    time.sleep(0.5)  # 等待文本框获得焦点

    # 将文本复制到剪贴板
    pyperclip.copy(text)

    # 确保文本框获得焦点
    time.sleep(1)  # 等待你切换到文本框

    # 粘贴文本
    pyautogui.hotkey('ctrl', 'v')

    print(f"已输入内容: {text}")
    return True

def find_and_click_publish_button():
    # 等待发布按钮出现
    time.sleep(2)  # 根据需要调整等待时间

    # 寻找发布按钮的位置
    publish_button_location = pyautogui.locateOnScreen(PUBLISH_BUTTON_TEMPLATE, confidence=0.8)
    if publish_button_location is not None:
        x, y = pyautogui.center(publish_button_location)
        pyautogui.click(x, y)  # 点击发布按钮
        print("已点击发布按钮。")
    else:
        print("未找到发布按钮。")


# 主循环
while True:
    if click_trigger_or_void_area():
        # 随机选择一条内容
        text_to_input = random.choice(texts_to_input)
        if click_in_area_and_type(text_to_input):
            find_and_click_publish_button()
    time.sleep(5)  # 每5秒循环一次（可以根据需要调整）