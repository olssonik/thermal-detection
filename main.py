import numpy as np
import cv2
import os

if not os.path.exists("out"):
    os.makedirs("out")
elif not os.path.exists("logs"):
    os.makedirs("logs")
elif not os.path.exists("raw"):
    os.makedirs("raw")

print("Please choose one of theese options")
print(os.listdir("raw"))
userInput = input()

dir = os.getcwd()

outPath = os.path.join(dir, "out", userInput + '.output.mp4')
logFile = './logs/pointofInterest ' + userInput + '.txt'

def main(inp):

    clip = inp

    cap = cv2.VideoCapture(os.path.join(dir, "raw", clip))
    # output config
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    output = cv2.VideoWriter(outPath, fourcc, fps, (frame_width, frame_height))
    while True:
        ret, frame = cap.read()
        if not ret:
            print("There is no more frame to read, exiting...")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # purple
        lower_purple = np.array([130, 50, 50])
        upper_purple = np.array([145, 255, 255])
        # 2 red colour arrays as hsv red is at the begining and the end
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        #  range for purple
        mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
        # range for red
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        # connect two sides of hsv for red
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        # use two colours for the mask
        mask = cv2.bitwise_or(mask_purple, mask_red)
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            # create a rectangle for each point on the frame
            x, y, w, h = cv2.boundingRect(c)
            # making sure that we ignore out the unimportant spots
            if w > 5 and h > 5:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3 )
                with open(logFile, 'a') as f:
                    f.writelines("X: " + str(x) + " Y: " + str(y) + " W: " + str(w) + " H: " + str(h) + '\n')
                    f.close()
        cv2.imshow('frame', frame)
        output.write(frame)
        # quit on a keypress
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    cap.release()
    output.release()
    cv2.destroyAllWindows()


    

if __name__ == "__main__":
    main(userInput)

def read():
    with open(logFile) as f:
        first_line = f.readline().strip('\n')
    if (len(first_line) > 0):
        return True
    else:
        return False