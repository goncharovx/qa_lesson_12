import os

import allure
from allure_commons.types import AttachmentType
from dotenv import load_dotenv

load_dotenv()

selenoid_url = os.getenv("SELENOID_URL")


def add_screenshot(browser):
    png = browser.driver.get_screenshot_as_png()
    allure.attach(body=png, name='screenshot', attachment_type=AttachmentType.PNG, extension='.png')


def add_logs(browser, browser_type):
    if browser_type == "firefox":
        log = "Логи браузера недоступны для Firefox через WebDriver API."
    else:
        try:
            log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
        except Exception:
            log = "Ошибка при получении логов браузера."
    allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')


def add_html(browser):
    html = browser.driver.page_source
    allure.attach(html, 'page_source', AttachmentType.HTML, '.html')


# def add_video(browser):
#     video_url = f"https://selenoid.autotests.cloud/video/{browser.driver.session_id}.mp4"
#     html = f"<html><body><video width='100%' height='100%'controls autoplay><source src='{video_url}' type='video/mp4'></video></body></html>"
#     allure.attach(html, f'video_{browser.driver.session_id}', AttachmentType.HTML, '.html')

#
# def add_video(browser):
#     video_url = f"{selenoid_url}/video/" + browser.driver.session_id + ".mp4"
#     html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
#            + video_url \
#            + "' type='video/mp4'></video></body></html>"
#     allure.attach(html, 'video_' + browser.driver.session_id, AttachmentType.HTML, '.html')


def add_video(browser):
    session_id = browser.driver.session_id
    video_url = f"https://selenoid.autotests.cloud/video/{session_id}.mp4"

    print(f"\n📌 VIDEO SESSION ID: {session_id}")  # Выводим session_id в логи
    print(f"🎥 VIDEO URL: {video_url}\n")

    html = f"""
    <html>
    <body>
    <p>Если видео не воспроизводится, попробуйте <a href="{video_url}" target="_blank">скачать его</a>.</p>
    <video width="800" height="600" controls>
        <source src="{video_url}" type="video/mp4">
        Ваш браузер не поддерживает видео.
    </video>
    </body>
    </html>
    """
    allure.attach(html, f'Video {session_id}', AttachmentType.HTML, '.html')