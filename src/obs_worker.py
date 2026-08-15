import os
import obsws_python as obs

class OBSWorker:
    def __init__(self):
        # Pull credentials from the .env file loaded by the GUI
        self.host = os.getenv("OBS_HOST", "localhost")
        self.port = os.getenv("OBS_PORT", "4455")
        self.password = os.getenv("OBS_PASSWORD", "")

    def _get_client(self):
        # Establish a fresh connection to the OBS WebSocket Server
        return obs.ReqClient(host=self.host, port=self.port, password=self.password, timeout=3)

    def save_replay(self):
        client = self._get_client()
        client.save_replay_buffer()

    def toggle_mic_mute(self, mic_name="Mic/Aux"):
        client = self._get_client()
        client.toggle_input_mute(mic_name)
