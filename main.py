from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.scatter import Scatter
import requests
from flask import Flask, request, jsonify
import threading

# TV control server setup
app = Flask(__name__)

@app.route('/control', methods=['POST'])
def control():
    command = request.json.get('command')
    # Handle the TV control logic here
    print(f"Received command: {command}")
    return jsonify({"status": "success"}), 200

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Mobile app setup
class TouchApp(App):
    gesture_command = StringProperty("")

    def build(self):
        self.tv_ip = 'http://your-tv-ip-address:port/control'  # Replace with your TV's API URL
        self.gesture_command = "No Gesture"
        
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Touch or Gesture')
        layout.add_widget(self.label)
        button = Button(text='Send Test Command')
        button.bind(on_press=self.send_test_command)
        layout.add_widget(button)

        # Start Flask server in a separate thread
        threading.Thread(target=run_flask, daemon=True).start()

        Window.bind(on_touch_move=self.on_touch_move)
        return layout

    def on_touch_move(self, instance, touch):
        if touch.dx > 0:
            self.gesture_command = "Swipe Right"
        elif touch.dx < 0:
            self.gesture_command = "Swipe Left"
        elif touch.dy > 0:
            self.gesture_command = "Swipe Down"
        elif touch.dy < 0:
            self.gesture_command = "Swipe Up"
        
        # Send command to TV
        self.send_command_to_tv(self.gesture_command)

    def send_command_to_tv(self, command):
        try:
            requests.post(self.tv_ip, json={"command": command})
        except Exception as e:
            print(f"Error sending command: {e}")

    def send_test_command(self, instance):
        self.send_command_to_tv("test_command")

if __name__ == '__main__':
    TouchApp().run()
