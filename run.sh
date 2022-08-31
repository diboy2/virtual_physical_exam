#!/bin/bash
fuser -k 9000/tcp
fuser -k 9001/tcp
fuser -k 9002/tcp
fuser -k 9003/tcp
fuser -k 9004/tcp
fuser -k 9005/tcp
fuser -k 9997/tcp
fuser -k 9998/tcp
fuser -k 9999/tcp

python3 -m storeDailyMetrics &
python3 -m storeImage &
python3 -m storeVideo &
python3 -m storeMedicalHistory &
python3 -m storePatientConcerns &
python3 -m storePhysicianNotes &
python3 -m testVideoRecognition &
python3 -m testImageRecognition &
python3 -m testTextRecognition &
wait