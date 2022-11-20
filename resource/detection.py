import cv2
import numpy as np

weightsFile_mpi = "/image_detection/yolov3.weights"

def stringToRGB(base64_string):
    imgdata = base64.b64decode(base64_string)
    dataBytesIO = io.BytesIO(imgdata)
    img = Image.open(dataBytesIO)
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

# Yolo 로드
net = cv2.dnn.readNet(weightsFile_mpi, "/image_detection/yolov3.cfg")
# net = cv2.dnn.readNet("/image_detection/yolov3.weights",
                    #   "/image_detection/yolov3.cfg")
classes = []
with open("/image_detection/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# 이미지 가져오기
#img = stringToRGB(b64_string)
img = cv2.imread("/home/workspace/talk-kiosk-flask_server/resource/018.jpeg") #to decode erase this line
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False) #for slow 320, 320 middle 416, 517
net.setInput(blob)
outs = net.forward(output_layers) #여기가 문제이구만



# 정보를 화면에 표시
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            # 좌표
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)


indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        print(label)
        if(label=="person"):
            print(x,y)
            print(w, h)

# outputImg = img[y:y+h, x:x+w] #cut the image with detection result
# cv2.imshow("Image", img)
# cv2.imshow("output",outputImg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

