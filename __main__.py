from agent.agent import Agent
from serial_communication.pi_test import SerialCommunicator
from speech.speech import Speech

if __name__ == "__main__":
    agent = Agent()
    sc = SerialCommunicator(agent)

    speech = Speech()

    def handle_speech(msg):
        msg = msg.lower()
        if 'red' in msg:
            agent.fetch('red')

        if 'green' in msg:
            agent.fetch('green')

        if 'blue' in msg:
            agent.fetch('blue')

    speech.add_listener(handle_speech)
    #input("Press Enter to continue...")

    sc.thread_write.join()
