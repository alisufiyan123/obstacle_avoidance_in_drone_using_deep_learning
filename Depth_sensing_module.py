# #import Dependencies
import  cv2
import torch
import matplotlib.pyplot as plt



#Downloads the MiDas


midas =torch.hub.load('intel-isl/MIdaS' ,'MiDaS_small')
midas.to('cpu')
midas.eval()


#Input transformationa pipline




transforms= torch.hub.load ('intel-isl/MiDaS' , 'transforms')
transform= transforms.small_transform


# hook into opencv

cap =cv2.VideoCapture("dronefeed.mp4")
while cap.isOpened():
    ret,frame =cap.read()


    img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    imgbatch =transform(img).to('cpu')

    with torch.no_grad():
        prediction =midas(imgbatch)
        prediction =torch.nn.functional.interpolate(prediction.unsqueeze(1),size=img.shape[:2],mode='bicubic',align_corners=False).squeeze()
        output =prediction.cpu().numpy()
        print(output)

    plt.imshow(output)



    cv2.imshow('CV2Frame' ,frame)
    plt.pause(0.00001)
    if cv2.waitKey(10) & 0XFF ==ord('q'):
        cap.release()
        cv2.destroyAllWindows()


plt.show()






# import cv2 as cv
# import matplotlib.pyplot as plt
# config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
# frozen_model = 'frozen_inference_graph.pb'

# # #Path Environment
# # config_file ='sultan@sultan-dell:~/Documents/FYP_Staffs/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
# # frozen_model ='sultan@sultan-dell:~/Documents/FYP_Staffs/frozen_inference_graph.pb'




# #
# # load the model 
# model= cv.dnn_DetectionModel(frozen_model,config_file)


# # # define the classes which we are going to detect, i will provide the file 
# classlables=[]
# # file_name='sultan@sultan-dell:~/Documents/FYP_Staffs/Lables.txt'
# file_name='Lables.txt'


# with open(file_name,'rt')as fpt:
#     classLables=fpt.read().rstrip('\n').split('\n')



# # # lets see the class how many class we can detect from coco lables
# print(len(classLables))



# # # now see which class name we can have inthe file
# print(classLables)




# # # define the configuration for these object
# model.setInputSize(320,320)
# model.setInputScale(1.0/127.5)#255/2=127.5
# model.setInputMean((127.5, 127.5, 127.5)) #miblenet=[-1,1]
# model.setInputSwapRB(True)




# # # now read the video
# # # Vedio configuration
# # cap =cv.VideoCapture('sultan@sultan-dell:~/Documents/FYP_Staffs/06.mp4')
# cap =cv.VideoCapture('06.mp4')



# # # now check the video work or not 
# if not cap.isOpened():
#     cap=cv.VideoCapture(0)
# if not cap.isOpened():
#     raise IOError("cannot open the video")
# font_scale=3
# font=cv.FONT_HERSHEY_PLAIN

# while True:
#     ret,frame = cap.read()
    
#     ClassIndex, confidece, bbox = model.detect(frame,confThreshold=0.55)
    
#     print(ClassIndex)
#     if(len(ClassIndex)!=0):
#         for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidece.flatten(), bbox):
#             if(ClassInd<=80):
#                 #cv2.rectangle(frame, (x,y),(x+w , y+h),(255,0,0),2)
#                 #cv2.putText(img, text, (text_offset_x, text_offset_y), font, fontScale = font_scale, color = (0,0,0), thickness=1) 
#                 cv.rectangle(frame,boxes,(255,0,0),2)
#                 cv.putText(frame,classLables[ClassInd-1],(boxes[0]+10,boxes[1]+40), font, fontScale=font_scale,color=(0,255,0),thickness=3)
                
                
#     cv.imshow('object Detection Tutorial',frame)
    
#     if cv.waitKey(2) & 0XFF == ord('q'):
#         break
        
# cap.release()
# cv.destroyAllWindows()



# ____________________________________Code_02_____________________________________________



                             
                             





