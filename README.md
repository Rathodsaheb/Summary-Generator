# Summary-Generator

## Introduction:
This application provides three types of services viz. Video to the summary, Speech to summary, and pdf to summary. So these services work on a deep learning-based transformer model which will does most of the NLP steps to give a summary from input text data. And to feed text to this model different libraries like google's speech_recognition to record speech and generate text,moviepy to get voice form video, PyPDF2 to implement OCR technique on the pdf file and other libraries are used. This system integrates with HTML and CSS web page through Flask framework and this project is deployed on AWS EC2 DL1 instance servers.
## Dashboard:
![whole-sum2](https://user-images.githubusercontent.com/86550391/154644552-a482ac0f-000b-4748-b11f-3828141cf218.gif)
## Services view:
![Screenshot (91)](https://user-images.githubusercontent.com/86550391/154650332-1753a772-aa43-447b-956e-da54abdff404.png)
![Screenshot (90)](https://user-images.githubusercontent.com/86550391/154645069-830ab837-6fbc-49db-b68c-e70a57ad6421.png)
![Screenshot (84)](https://user-images.githubusercontent.com/86550391/154644874-d4d9763f-7bb3-401f-a1f0-8303fa7586b1.png)
## Results:
![Screenshot (89)](https://user-images.githubusercontent.com/86550391/154645111-1e1ff545-ebdf-481b-9d7c-08011ee481b6.png)
![Screenshot (92)](https://user-images.githubusercontent.com/86550391/154649820-e4c7b4d6-a0e5-4fea-a9ca-31341b83a804.png)
![Screenshot (85)](https://user-images.githubusercontent.com/86550391/154645144-9cc80fcf-5e20-4242-a0b9-7b6d931a6848.png)

## Installation:
run: pip install -r requirements.txt in your shell.

## Deployment Instructions:
1. Create An EC2 instance on any AMI machine, I have used ubuntu.
2. Select instance type as dl1.24xlarge (this requires 96 vCPU capacity),create private pem key and lauch the instance.
3. Create ppk key pair using puttygen software.
4. Copy the private ipv4 address paste it on putty software and provide ppk file on authentication section.
5. Open WinSCP login by entering username, IPV4 address and ppk file and upload the required documents on the server.
6. The run the following command on putty terminal one-by-one:
    sudo apt-get update
    sudo apt install python3-pip
    pip3 install -r requirement.txt
    python3 app.py
7. Then at aws window click on connect button and copy the url at the end of url type :8080 an you are ready to go.

## Demostration video:
https://youtu.be/8UPoJdB2vt8
### Author:
Mayur Rathod
