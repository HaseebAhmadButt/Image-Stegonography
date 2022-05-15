# This side of code can only be used by systems having Python 3.6 and below
# Above versions does not sport speech_recognition library.

import encryption as enc
import cv2
import os.path
from gtts import gTTS
import speech_recognition as sr
import  concurrent.futures
import time


# Function that Converts Text to Audio using gTTS Module of gtts
def textToSpeech(myText):
    myobj = gTTS(text=myText, lang='en', slow=False)
    myobj.save("outPut.mp3")
    os.system("outPut.mp3")

# function That counts the Number of Seconds Provided by the user 
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

# function That records the audio Voice from Microphone using speech_recognition
def speechToText(time):
        r = sr.Recognizer()
        print("\nListening")
        with sr.Microphone() as source:
            # listen for the data (load audio to memory)
            audio_data = r.record(source,duration=time)
            # recognize (convert from speech to text)
            print('recognizing the Text.....')
            try:
                    text = r.recognize_google(audio_data,language="en-US")
            except sr.UnknownValueError as e:
                    print("Error (in recognizing...):", str(e))
                    exit(1)
            else:
                return text

# Main function
if __name__ == '__main__': 
    # User Choices
    inputImagePath= input("Enter the Input Image File Name/Path = ")
    if(not os.path.isfile(inputImagePath)):
        print("NO Such File")
    else:
        encrypt = enc.Encrypt()
        data=""
        Type = input("what Type of Image is?\n1 GrayScale\n2 RGB\n")
        if(int(Type)==1):
            inputType = input("Enter Message Format:\n1 = Voice Note\n2 = Text File\n")
            if(int(inputType)==1):
                t = input("Enter Time(Seconds): ")
                # Threads Creation 1 For Recording Voice and Other for Timer
                with concurrent.futures.ThreadPoolExecutor(2) as executor:
                    executor.submit(countdown,int(t))
                    result = executor.submit(speechToText,int(t))
                    data = result.result()
                getLs=encrypt.data_to_gray_image(inputImagePath,data)
                print(data)
                if(getLs[1]==True):
                    while True:
                        extension = input("Choose Format to save the Image:\n1 = BMP\n2 = PNG\n3 = Tiff\n")
                        if(int(extension)==1):
                            cv2.imwrite("outputImg.bmp",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)
                        
                        elif(int(extension)==2):
                            cv2.imwrite("outputImg.png",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)

                        elif(int(extension)==3):
                            cv2.imwrite("outputImg.tiff",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)
                        else:
                            print("Invalid Selection\nTry Again.....!!\n")
            elif(int(inputType)==2):
                inputTxt= input("Enter the Input Text File Name = ")
                if(not os.path.isfile(inputImagePath)):
                    print("NO Such File")
                else:
                    with open(inputTxt) as file:
                        lines = file.readlines()
                getLs=encrypt.data_to_gray_image(inputImagePath,lines)
                if(getLs[1]==True):
                    while True:
                        extension = input("Choose Format to save the Image:\n1 = BMP\n2 = PNG\n3 = Tiff\n")
                        if(int(extension)==1):
                            cv2.imwrite("outputImg.bmp",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)
                        
                        elif(int(extension)==2):
                            cv2.imwrite("outputImg.png",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)

                        elif(int(extension)==3):
                            cv2.imwrite("outputImg.tiff",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)
                        else:
                            print("Invalid Selection\nTry Again.....!!\n")

            else:
                print("whole Text has not been encrypted in Image")
            exit(1)
        if(int(Type)==2):
            inputType = input("Enter Message Format:\n1 = Voice Note\n2 = Text File\n")
            if(int(inputType)==1):
                t = input("Enter Time(Seconds): ")
                with concurrent.futures.ThreadPoolExecutor(2) as executor:
                    executor.submit(countdown,int(t))
                    result = executor.submit(speechToText,int(t))
                    data = result.result()
                getLs=encrypt.data_to_img_rgb(inputImagePath,data)
                print(data)
                if(getLs[1]==True):
                    while True:
                        extension = input("Choose Format to save the Image:\n1 = BMP\n2 = PNG\n3 = Tiff\n")
                        if(int(extension)==1):
                            cv2.imwrite("outputImg.bmp",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)
                        
                        elif(int(extension)==2):
                            cv2.imwrite("outputImg.png",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)

                        elif(int(extension)==3):
                            cv2.imwrite("outputImg.tiff",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)
                        else:
                            print("Invalid Selection\nTry Again.....!!\n")
            elif(int(inputType)==2):
                inputTxt= input("Enter the Input Text File Name = ")
                if(not os.path.isfile(inputImagePath)):
                    print("NO Such File")
                else:
                    with open(inputTxt) as file:
                        lines = file.readlines()
                getLs=encrypt.data_to_img_rgb(inputImagePath,lines)
                if(getLs[1]==True):
                    while True:
                        extension = input("Choose Format to save the Image:\n1 = BMP\n2 = PNG\n3 = Tiff\n")
                        if(int(extension)==1):
                            cv2.imwrite("outputImg.bmp",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)
                        
                        elif(int(extension)==2):
                            cv2.imwrite("outputImg.png",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)

                        elif(int(extension)==3):
                            cv2.imwrite("outputImg.tiff",getLs[0])
                            print("Whole Text Has been Added to Image")
                            print("Image Has Been Saved\nPlease Do not Change format of the Image to Lossy Compression Formats")
                            exit(1)
                        else:
                            print("Invalid Selection\nTry Again.....!!\n")

            else:
                print("whole Text has not been encrypted in Image")
            exit(1)
        else:
            print("Error...\nInvalid Option")
