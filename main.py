import threading
import webbrowser

import rumps


class ServerStarter(threading.Thread):
    def run(self):
        from things_api.app import app
        app.run(debug=False)


class ThingsApp(rumps.App):
    @rumps.clicked("127.0.0.1:5000 ↗")
    def prefs(self, _):
        webbrowser.open("http://127.0.0.1:5000/tasks")


if __name__ == "__main__":
    starter = ServerStarter()

    starter.start()
    ThingsApp("☑️").run()
