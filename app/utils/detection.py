import cv2
import numpy as np
import os
from flask import current_app

def detect_objects(image_path):
    """
    Detect objects in an image using YOLO
    Returns the filename of the result image
    """
    try:
    
        net = cv2.dnn.readNetFromDarknet(
            current_app.config['YOLO_CONFIG_PATH'],
            current_app.config['YOLO_WEIGHTS_PATH']
        )
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        
      
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
        
        
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
            
        height, width = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
        
       
        net.setInput(blob)
        outputs = net.forward(output_layers)
        
       
        with open(current_app.config['YOLO_NAMES_PATH'], 'r') as f:
            labels = f.read().strip().split('\n')
        
       
        boxes = []
        confidences = []
        class_ids = []
        
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = int(np.argmax(scores))
                confidence = scores[class_id]
                
                if confidence > current_app.config['CONFIDENCE_THRESHOLD']:
                    
                    center_x, center_y, w, h = (detection[0:4] * [width, height, width, height]).astype('int')
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    
                    boxes.append([x, y, int(w), int(h)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
        

        if len(boxes) > 0:
            indexes = cv2.dnn.NMSBoxes(
                boxes, 
                confidences, 
                current_app.config['CONFIDENCE_THRESHOLD'], 
                current_app.config['NMS_THRESHOLD']
            )
            
            
            if len(indexes) > 0:
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    label = str(labels[class_ids[i]])
                    confidence = confidences[i]
                    
                   
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                   
                    text = f'{label} {confidence:.2f}'
                    cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
        result_filename = 'result_' + os.path.basename(image_path)
        result_path = os.path.join(current_app.config['UPLOAD_FOLDER'], result_filename)
        cv2.imwrite(result_path, image)
        
        return result_filename
        
    except Exception as e:
        current_app.logger.error(f"Detection error: {str(e)}")
        raise e