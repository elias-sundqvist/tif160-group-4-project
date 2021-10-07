from agent.agent import Agent
from serial_communication.pi_test import SerialCommunicator
from speech.speech import Speech


if __name__ == "__main__":
    agent = Agent()
    sc = SerialCommunicator(agent)

    speech = Speech()

    speech.add_listener(lambda msg: agent.handle_message(msg))
    # input("Press Enter to continue...")

    sc.thread_write.join()
