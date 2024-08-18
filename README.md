
![image](pic/5.png) 

support service and client to "Parse the text in OCR using the server-client mode.
Multi-threading is specifically used to inject images. Because this introduced OCR library needs to be called in this way to enable multiple calls.
To solve the problem of multiple calls. Create a thread-safe queue to store image paths and results.
1. The image variables passed in by the client also need to be free from thread interference. image_paths = Queue()
2. The status of whether the OCR is successful notified to the client needs to be free from thread interference. ocr_results = Queue()
Server side:
Client side:




 
