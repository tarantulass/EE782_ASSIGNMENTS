'''
  * ************************************************************
  *      Program: Vosk Speech Recognition Module
  *      Type: Python
  *      Author: David Velasco Garcia @davidvelascogarcia
  * ************************************************************
  *
  * | INPUT PORT                           | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /voskSpeechRecognition/data:i        | Input audio to recognize                                |
  *
  * | OUTPUT PORT                          | CONTENT                                                 |
  * |--------------------------------------|---------------------------------------------------------|
  * | /voskSpeechRecognition/data:o        | Recognized output text                                 |
  *
'''

# Libraries
import configparser
import datetime
from halo import Halo
import platform
import pyaudio
import time
from vosk import Model, KaldiRecognizer
import yarp


class VoskSpeechRecognition:

    # Function: Constructor
    def __init__(self):

        # Build Halo spinner
        self.systemResponse = Halo(spinner='dots')

    # Function: getSystemPlatform
    def getSystemPlatform(self):

        # Get system configuration
        print("\nDetecting system and release version ...\n")
        systemPlatform = platform.system()
        systemRelease = platform.release()

        print("**************************************************************************")
        print("Configuration detected:")
        print("**************************************************************************")
        print("\nPlatform:")
        print(systemPlatform)
        print("Release:")
        print(systemRelease)

        return systemPlatform, systemRelease

    # Function: getAuthenticationData
    def getAuthenticationData(self):

        print("\n**************************************************************************")
        print("Authentication:")
        print("**************************************************************************\n")

        loopControlFileExists = 0

        while int(loopControlFileExists) == 0:
            try:
                # Get authentication data
                print("\nGetting authentication data ...\n")

                authenticationData = configparser.ConfigParser()
                authenticationData.read('../config/languages.ini')
                authenticationData.sections()

                inputLanguage = authenticationData['Languages']['input-language']

                print("Input language: " + str(inputLanguage))

                # Exit loop
                loopControlFileExists = 1

            except:

                systemResponseMessage = "\n[ERROR] Sorry, languages.ini not founded, waiting 4 seconds to the next check ...\n"
                self.systemResponse.text_color = "red"
                self.systemResponse.fail(systemResponseMessage)
                time.sleep(4)

        systemResponseMessage = "\n[INFO] Data obtained correctly.\n"
        self.systemResponse.text_color = "green"
        self.systemResponse.succeed(systemResponseMessage)

        return inputLanguage

    # Function: getModel
    def getModel(self, inputLanguage):

        print("\n**************************************************************************")
        print("Language model:")
        print("**************************************************************************\n")

        loopControlFileExists = 0

        while int(loopControlFileExists) == 0:
            try:
                # Get model data
                print("\nGetting model data ...\n")

                # Prepare model path
                modelPath = "./../models/model-" + str(inputLanguage)

                # Load model
                model = Model(modelPath)

                # Exit loop
                loopControlFileExists = 1

            except:

                systemResponseMessage = "\n[ERROR] Sorry, model not founded, waiting 4 seconds to the next check ...\n"
                self.systemResponse.text_color = "red"
                self.systemResponse.fail(systemResponseMessage)
                time.sleep(4)

        systemResponseMessage = "\n[INFO] Model obtained correctly.\n"
        self.systemResponse.text_color = "green"
        self.systemResponse.succeed(systemResponseMessage)

        return model

    # Function: buildEngine
    def buildEngine(self, model):

        print("\nBuilding engine ...\n")

        # Build engine
        engine = KaldiRecognizer(model, 16000)

        systemResponseMessage = "\n[INFO] Engine built correctly.\n"
        self.systemResponse.text_color = "green"
        self.systemResponse.succeed(systemResponseMessage)

        return engine

    # Function: initMicrophone
    def initMicrophone(self):

        loopControlFileExists = 0

        while int(loopControlFileExists) == 0:
            try:
                microphoneEngine = pyaudio.PyAudio()

                # Open microphone
                microphone = microphoneEngine.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

                # Init streaming
                microphone.start_stream()

                # Exit loop
                loopControlFileExists = 1

            except:

                systemResponseMessage = "\n[ERROR] Error initializing microphone, 4 seconds to the next try ...\n"
                self.systemResponse.text_color = "red"
                self.systemResponse.fail(systemResponseMessage)
                time.sleep(4)

        systemResponseMessage = "\n[INFO] Microphone initialized correctly.\n"
        self.systemResponse.text_color = "green"
        self.systemResponse.succeed(systemResponseMessage)

        return microphone

    # Function: processRequest
    def processRequests(self, engine, microphone, outputPort):

        # Variable to control loopProcessRequests
        loopProcessRequests = 0

        while int(loopProcessRequests) == 0:

            # Waiting to input data request
            print("**************************************************************************")
            print("Waiting for input data request:")
            print("**************************************************************************")

            systemResponseMessage = "\n[INFO] Waiting for input data request at " + str(datetime.datetime.now()) + " ...\n"
            self.systemResponse.text_color = "yellow"
            self.systemResponse.warn(systemResponseMessage)

            # Receive input audio
            dataToSolve = microphone.read(4000)

            # If dataToSolve is empty
            if len(dataToSolve) == 0:
                break

            else:
                print("\n**************************************************************************")
                print("Processing:")
                print("**************************************************************************\n")

                # If detect final results
                if engine.AcceptWaveform(dataToSolve):

                    # Get dataSolved
                    dataSolved = engine.Result()

                    # Parse dataSolved
                    dataSolved = dataSolved.split('"text" : "')[1].split('"')[0]

                    # Show dataSolved
                    systemResponseMessage = "\n[INFO] Results: " + str(dataSolved) + "...\n"
                    self.systemResponse.text_color = "green"
                    self.systemResponse.succeed(systemResponseMessage)

                # Partial results
                else:

                    # Get dataSolved
                    dataSolved = engine.PartialResult()

                    # Show dataSolved
                    systemResponseMessage = "\n[INFO] Partial results: " + str(dataSolved) + "...\n"
                    self.systemResponse.text_color = "yellow"
                    self.systemResponse.succeed(systemResponseMessage)

                    # Set as no ended
                    dataSolved = "None"

                # Send output results
                outputPort.send(dataSolved)


class YarpDataPort:

    # Function: Constructor
    def __init__(self, portName):

        # Build Halo spinner
        self.systemResponse = Halo(spinner='dots')

        # Build port and bottle
        self.yarpPort = yarp.Port()
        self.yarpBottle = yarp.Bottle()

        systemResponseMessage = "\n[INFO] Opening Yarp data port " + str(portName) + " ...\n"
        self.systemResponse.text_color = "yellow"
        self.systemResponse.warn(systemResponseMessage)

        # Open Yarp port
        self.portName = portName
        self.yarpPort.open(self.portName)

    # Function: receive
    def receive(self):

        self.yarpPort.read(self.yarpBottle)
        dataReceived = self.yarpBottle.toString()
        dataReceived = dataReceived.replace('"', '')

        systemResponseMessage = "\n[RECEIVED] Data received: " + str(dataReceived) + " at " + str(datetime.datetime.now()) + ".\n"
        self.systemResponse.text_color = "blue"
        self.systemResponse.info(systemResponseMessage)

        return dataReceived

    # Function: send
    def send(self, dataToSend):

        self.yarpBottle.clear()
        self.yarpBottle.addString(str(dataToSend))
        self.yarpPort.write(self.yarpBottle)

    # Function: close
    def close(self):

        systemResponseMessage = "\n[INFO] " + str(self.portName) + " port closed correctly.\n"
        self.systemResponse.text_color = "yellow"
        self.systemResponse.warn(systemResponseMessage)

        self.yarpPort.close()


# Function: main
def main():

    print("**************************************************************************")
    print("**************************************************************************")
    print("                   Program: Vosk Speech Recognition                       ")
    print("                     Author: David Velasco Garcia                         ")
    print("                             @davidvelascogarcia                          ")
    print("**************************************************************************")
    print("**************************************************************************")

    print("\nLoading Vosk Speech Recognition engine ...\n")

    # Build voskSpeechRecognition object
    voskSpeechRecognition = VoskSpeechRecognition()

    # Get system platform
    systemPlatform, systemRelease = voskSpeechRecognition.getSystemPlatform()

    # Get input language
    inputLanguage = voskSpeechRecognition.getAuthenticationData()

    # Get model
    model = voskSpeechRecognition.getModel(inputLanguage)

    # Build engine
    engine = voskSpeechRecognition.buildEngine(model)

    # Init microphone
    microphone = voskSpeechRecognition.initMicrophone()

    # Init Yarp network
    yarp.Network.init()

    # Create Yarp ports
    outputPort = YarpDataPort("/voskSpeechRecognition/data:o")

    # Process input requests
    voskSpeechRecognition.processRequests(engine, microphone, outputPort)

    # Close Yarp ports
    outputPort.close()

    print("**************************************************************************")
    print("Program finished")
    print("**************************************************************************")
    print("\nvoskSpeechRecognition program finished correctly.\n")


if __name__ == "__main__":

    # Call main function
    main()