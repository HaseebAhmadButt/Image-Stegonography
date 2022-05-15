import encryption as enc, os
from gtts import gTTS
encrypt = enc.Encrypt()
def textToSpeech(myText):
    try:
        print("Creating Audio")
        myobj = gTTS(text=myText, lang='en', slow=False)
        myobj.save("outPut.mp3")
        os.system("outPut.mp3")
        print("File Saved Successfully")
    except:
        raise Exception("Select Extraction Type Appropriately")
def svae_file(data):
   try:
        print("Creating Text File")
        file = open("outPut.txt","w")
        file.write(data)
        file.close()
        os.system("outPut.txt")
        print("File Saved Successfully")
   except:
       raise Exception("Select Extraction Type Appropriately")

if __name__ == "__main__":
    while True:
        img_name = input("Enter Name/Address of Image From Which You Want Extract Data: ")
        if not os.path.isfile(img_name):
            print("Enter Path/Name Not Correct")
            exit(1)
        else:
            print("Select Extraction Type To Retrieve Data.")
            print("Enter 1 For Grayscale")
            print("Enter 2 For RGB")
            value = input()
            if int(value) == 1:
                data = encrypt.img_gray_to_data(img_name)
                print("Select One Option")
                print("Enter 3 To Create Text File Of Retrieved Data")
                print("Enter 4 To Create Audio File Of Retrieved Data")
                option = input()
                if int(option) == 3:
                    svae_file(data)
                elif int(option) == 4:
                    textToSpeech(data)
                else:
                    print("Please Select Appropriate Option")
            elif int(value) == 2:
                data = encrypt.img_rgb_to_data(img_name)
                print("Select One Option")
                print("Enter 3 To Create Text File Of Retrieved Data")
                print("Enter 4 To Create Audio File Of Retrieved Data")
                option = input()
                if int(option) == 3:
                    svae_file(data)
                elif int(option) == 4:
                    textToSpeech(data)
                else:
                    print("Please Select Appropriate Option")
            else:
                print("Please Select Appropriate Option")
