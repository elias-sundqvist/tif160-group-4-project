from agent.agent import Agent
from serial_communication.pi_test import SerialCommunicator
from speech.speech import Speech
import time

if __name__ == "__main__":
    agent = Agent()
    sc = SerialCommunicator(agent)
    time.sleep(5) # Need to wait for the read thread to finish

    speech = Speech()

    speech.add_listener(lambda msg: agent.handle_speech(msg))
    # input("Press Enter to continue...")
    #agent.handle_speech("red")

    sc.thread_write.join()
    agent.camera.release()
