import os
import obsws_python as obs

class OBSWorker:
    def __init__(self):
        # Pull credentials from the .env file loaded by the GUI
        self.host = os.getenv("OBS_HOST", "localhost")
        self.port = int(os.getenv("OBS_PORT", 4455))
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
        
    def unmute_mic(self, mic_name="Mic/Aux"):
        client = self._get_client()
        client.set_input_mute(mic_name, False)

    def change_scene(self, scene_name):
        client = self._get_client()
        client.set_current_program_scene(scene_name)
        
    def start_stream(self):
        client = self._get_client()
        client.start_stream()
