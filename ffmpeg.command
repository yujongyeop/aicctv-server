USB 디바이스를 통한 스트리밍(RTMP)
ffmpeg -f dshow -video_size 1920x1080 -i video="c922 Pro Stream Webcam" -b:v 4000k -f flv rtmp://localhost:1935/live/test

USB 디바이스를 통한 스트리밍(RSTP)
ffmpeg -f dshow -video_size 1920x1080 -i video="c922 Pro Stream Webcam" -b:v 4000k -f rtsp -rtsp_transport tcp rtsp://localhost:8554/stream

ffmpeg -f dshow -framerate 5 -pixel_format yuyv422 -i video="c922 Pro Stream Webcam" -c:v libx264 -preset ultrafast -f rtsp -rtsp_transport tcp rtsp://localhost:8554/test

mp4 파일 RTSP 스트리밍
ffmpeg -re -stream_loop -1 -i model_test.mp4 -map 0:v -c:v libx264 -f rtsp -rtsp_transport tcp rtsp://localhost:8554/stream
ffmpeg -re -stream_loop -1 -i model_test.mp4 -map 0:v -c:v libx264 -f flv rtmp://localhost:1935/live/test

ffmpeg -re -stream_loop -1 -i model_test.mp4 -map 0:v -c:v libx264 -f flv rtmp://localhost:1935/live/test -map 0:v -c:v libx264 -f rtsp -rtsp_transport tcp rtsp://localhost:8554/stream