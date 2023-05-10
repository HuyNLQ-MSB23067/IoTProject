import speech_recognition as sr
import pyttsx3

# Khai bao object dung de goi nhan dien giong noi
r = sr.Recognizer()

def speech_detector():
# while True:
    try:
        # Dung micro de lam nguon input
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # Lang nghe data input tu user
            audio2 = r.listen(source2)

            # Su dung Google de nhan dien am thanh va chuyen sang text
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            result = {}

            print("Voice: ", MyText)
            if "light" in MyText:
                result['type'] = "publish"
                result['feed'] = "led-button"
                if "turn on" in MyText:
                    #Gui lenh mo led len Adafruit
                    print("Sending 'Turn on LED' comamnd to Adafruit-IO...")
                    result['command'] = "ON"
                elif "turn off" in MyText:
                    #Gui len tat led len Ada fruit
                    print("Sending 'Turn off LED' comamnd to Adafruit-IO...")
                    result['command'] = "OFF"
            elif "motor" in MyText or "fan" in MyText:
                result['feed'] = "pump-button"
                if "turn on" in MyText:
                    #Gui lenh mo led len Adafruit
                    print("Sending 'Turn on Pump' comamnd to Adafruit-IO...")
                    result['command'] = "ON"
                elif "turn off" in MyText:
                    #Gui len tat led len Ada fruit
                    print("Sending 'Turn off Pump' comamnd to Adafruit-IO...")
                    result['command'] = "OFF"
            elif "temperature" in MyText:
                # Lay data hien tai cua nhiet do + vao chuoi ben duoi de hien thi
                # print("The current temperature is ...")
                result['type'] = "get"
                result['get'] = "temperature"
                result['feed'] = "publish-temp"
            elif "humidity" in MyText:
                # Lay data hien tai cua do am + vao chuoi ben duoi de hien thi
                # print("The current humidity is ...")
                result['type'] = "get"
                result['get'] = "humidity"
                result['feed'] = "publish-humid"

            return result

    except sr.RequestError as e:
        print("Khong the xu ly; {0}".format(e))

    except sr.UnknownValueError:
        print("Unexpected error/ Unknown command")
