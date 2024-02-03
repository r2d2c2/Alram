
from flask import Flask, render_template, request, url_for, flash, redirect
import threading
import time
import webbrowser
from gtts import gTTS
import pyglet
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # flash 메시지를 사용하기 위한 시크릿 키 설정
alarms = []  # 알람 시간을 저장하는 리스트
isEnd=True
def alarm_ring(alarm_time):#시간 확인
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == alarm_time:
            print_hi()
            alarms.remove(alarm_time)  # 알람 울린 후 리스트에서 해당 시간 제거
            break
        time.sleep(1)  # 1분마다 확인하는 것이 아니라, 10초마다 확인하도록 변경


def print_hi():#소리추력
    text = f"It's a break time."
    tts = gTTS(text=text)

    try:
        tts.save("helloEN.mp3")
    finally:
        song = pyglet.media.load('helloEN.mp3')
        song.play()
        pyglet.app.run()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    alarm_time = request.form['time']
    if alarm_time not in alarms:  # 중복된 알람 시간이 아닐 경우에만 추가
        alarms.append(alarm_time)
        threading.Thread(target=alarm_ring, args=(alarm_time,)).start()
        flash(f'{alarm_time}에 알람이 설정되었습니다.')
    else:
        flash(f'{alarm_time}에 대한 알람이 이미 설정되어 있습니다.')
    return redirect(url_for('index'))



webbrowser.open('http://127.0.0.1:5000')
if __name__ == '__main__':
    app.run()



