import sounddevice as sd
import numpy as np

class NoiseGateTester:
    def __init__(self):
        self.stream = None
        self.threshold = 0.02
        self.is_running = False

    def audio_callback(self, indata, outdata, frames, time, status):
        # Calculate the real-time volume level (RMS)
        volume = np.sqrt(np.mean(indata**2))
        
        # The Gate Logic: If volume is lower than the slider threshold, mute output
        if volume < self.threshold:
            outdata[:] = np.zeros_like(indata)
        else:
            # If volume is higher, let the voice pass through to the headphones
            outdata[:] = indata

    def start(self, threshold_value):
        self.threshold = threshold_value
        self.is_running = True
        # channels=1 ensures mono mic input plays back correctly in both ears
        self.stream = sd.Stream(channels=1, callback=self.audio_callback)
        self.stream.start()

    def stop(self):
        self.is_running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            
    def update_threshold(self, new_threshold):
        self.threshold = new_threshold
