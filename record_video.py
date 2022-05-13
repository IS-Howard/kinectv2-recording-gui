from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import os
import cv2
import copy
import time

def record(video_path, depth_filename, color_filename, width, height):
    depth_fourcc = cv2.VideoWriter_fourcc('F','F','V','1')
    color_fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_depth = cv2.VideoWriter(os.path.join(video_path,depth_filename + '.avi'), depth_fourcc, 30, (512, 424))
    out_color = cv2.VideoWriter(os.path.join(video_path,color_filename + '.avi'), color_fourcc, 30, (width, height))
    
    while True:
        if kinect.has_new_color_frame():
            frame = kinect.get_last_color_frame()
            gbra = frame.reshape([height, width, 4])
            color_frame = gbra[:, :, 0:3]
            b = cv2.resize(color_frame,(960,540),interpolation=cv2.INTER_CUBIC)
            cv2.imshow('KINECT Video Stream_RGB', b)
            
        if kinect.has_new_depth_frame():
            frame = kinect.get_last_depth_frame()
            frame = np.reshape(frame, (424, 512))

            B = (frame / 256).astype(np.uint8)
            R = (frame % 256).astype(np.uint8)
            G = np.zeros((424, 512)).astype(np.uint8)

            a = cv2.merge((B,G,R))
            cv2.imshow('KINECT Video Stream_Depth', a)
            
        out_color.write(color_frame)
        color_frame = None
        out_depth.write(a)
        frame = None
        a = None
        b = None

        key = cv2.waitKey(1)
        if key == 27:
            out_depth.release()
            out_color.release()
            cv2.destroyAllWindows()
            break


# def map_depth_point_to_color_point(depth_point):
#     # depth_ori = None
#     depth_point_to_color  = copy.deepcopy(depth_point)
#     print(depth_point_to_color[1])
#     print(depth_point_to_color.shape[1])
#     # print(len(depth_point_to_color[1]))
#     # print(depth_point_to_color[1])
#     n = 0
#     while 1:
#         # if depth_ori is None:
#         #     continue
#         color_point = kinect._mapper.MapDepthPointToColorSpace(
#             _DepthSpacePoint(511-depth_point_to_color[1], depth_point_to_color[0]), depth_ori[depth_point_to_color[0], 511-depth_point_to_color[1]])

#         if math.isinf(float(color_point.y)):
#             n += 1
#             if n >= 50000:
#                 print('深度映射彩色，无效点')
#                 color_point = [0, 0]
#                 break
#         else:
#             color_point = [np.int0(color_point.y), 1920-np.int0(color_point.x)]  # 图像坐标，人眼视角
#             break
#     return color_point

if __name__ == "__main__":
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth | PyKinectV2.FrameSourceTypes_Color)
    depth_width, depth_height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height # Default: 512, 424
    color_width, color_height = kinect.color_frame_desc.Width,kinect.color_frame_desc.Height
    while True:
        if kinect.has_new_color_frame():
            frame = kinect.get_last_color_frame()
            gbra = frame.reshape([color_height, color_width, 4])
            color_frame = gbra[:, :, 0:3]
            color_frame = cv2.resize(color_frame,(960,540),interpolation=cv2.INTER_CUBIC)
            cv2.imshow('KINECT Video Stream_RGB',color_frame)
            color_frame = None

        if kinect.has_new_depth_frame():
            frame = kinect.get_last_depth_frame()
            frame = np.reshape(frame, (424, 512))
            B = (frame / 256).astype(np.uint8)
            R = (frame % 256).astype(np.uint8)
            G = np.zeros((424, 512)).astype(np.uint8)

            a = cv2.merge((B,G,R))
            cv2.imshow('KINECT Video Stream_Depth', a)
            frame = None

        if cv2.waitKey(1) == ord('q'):
            frame = kinect.get_last_depth_frame()
            frame = np.reshape(frame, (424, 512))
            B = (frame / 256).astype(np.uint8)
            R = (frame % 256).astype(np.uint8)
            G = np.zeros((424, 512)).astype(np.uint8)

            a = cv2.merge((B,G,R))

            frame = None
            video_path = input('輸入影片位置：')
            depth_filename = input('深度影像名稱：')
            color_filename = input('彩色影像名稱：')
            record(video_path,depth_filename,color_filename,color_width,color_height)   

        key = cv2.waitKey(1)
        if key == 27: break 