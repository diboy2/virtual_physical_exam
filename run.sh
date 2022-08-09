#!/bin/bash
fuser -k 9000/tcp
fuser -k 9001/tcp
fuser -k 9002/tcp
fuser -k 9003/tcp
fuser -k 9004/tcp
fuser -k 9998/tcp
fuser -k 9999/tcp
python3 -m storeDailyMetrics.py &
python3 -m storeMedicalHistory.py &
python3 -m storePatientConcerns.py &
python3 -m storePhysicianNotes.py &
python3 -m storeImage.py &
python3 -m testImageRecognition.py &
python3 -m testTextRecognition.py &
wait