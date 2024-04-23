
import cv2

cap = cv2.VideoCapture('./runs/detect/predict4/test.avi')

# 동영상의 전체 프레임 수입니다.
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(frame_count)