from flask import Flask, render_template, url_for
from flask import request
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"


@app.route("/", methods=['GET'])
def home():
    #return render_template("upload.php")

    return render_template("index.html")



import speech_recognition as sr
from moviepy.editor import AudioFileClip
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("t5-base")

model = AutoModelWithLMHead.from_pretrained("t5-base")

device = torch.device('cpu')

import os,wave, math, contextlib

def capital(cap):
    str = cap.split('.')
    b = []
    c = '.'
    for x in range(len(str)):
        letter=str[x].strip().capitalize()  #strip is use to remove white spaces befor and after full stop and capitalize used to capital first word of sentence.
        b.append(letter)
    final = (c.join(b))
    return final

def summary(raw):
    #file_name = raw  #Taking input from user
    #file_name = os.path.dirname(__file__) + '\\' + raw  # Taking input from user
    file_name = f"uploads/{raw}"
    path = file_name #.replace(os.sep, '/')
    print(path)
    transcribe_file = "new_converted.wav"
    opt_file = "transcription.txt"

    audioclip = AudioFileClip(path)
    audioclip.write_audiofile("new_converted.wav")  #convert video file into audio
    with contextlib.closing(wave.open(transcribe_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)

    r = sr.Recognizer()
    for i in range(0, total_duration):
        with sr.AudioFile(transcribe_file) as source:
            audio = r.record(source, offset=i * 60, duration=60)
        f = open("transcription.txt", "a")
        f.write(r.recognize_google(audio))
        f.write(" ")
    f.close()
    z = open(opt_file, 'r')
    result= z.read()
    #audio = sr.AudioFile("new_converted.wav")
    #with audio as source:
    #    audio_file = r.record(source)
    #result = r.recognize_google(audio_file)  #using speech recognition converting into text
    # encode the text into tensor of integers using the appropriate tokenizer
    inputs = tokenizer.encode("summarize: " + str(result), return_tensors="pt", truncation=True)
    #Generate summary from training given text data on t5-base model
    outputs = model.generate(inputs, max_length=1500, min_length=50, length_penalty=2.0, num_beams=5,
                             early_stopping=True)
    out = tokenizer.decode(outputs[0])
    o = out.split('>',1)
    out1 = o[1].split('<')
    final_out = capital(out1[0])
    # print(tokenizer.decode(outputs[0]))
    #l = Label(text=out1[0], wraplength= 500,justify="center" ,font="comicsansms 13 bold", pady=15)
    #l.pack(fill=Y)
    #return out1[0].capitalize()
    return final_out

from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os

def fold(line):
    line = line.rstrip()
    start = 0
    z = ''
    # get the length of long line
    line_length = len(line)
    # loop through the long line using the desired line
    # width
    while line_length - start >= 150:
        b= line[start:(start + 150)]
        start += 150
        z = "{}\n".format(z) + b
    z = "{}\n".format(z) + line[start:]
    return z
import PyPDF2

def pdftext(pdf):
    #pages = convert_from_path(pdf, 500)
    #image_counter = 1
    # Iterate through all the pages stored above
    #for page in pages:
    #    filename = "page_" + str(image_counter) + ".jpg"
        # Save the image of the page in system
    #    page.save(filename, 'JPEG')
        # Increment the counter to update filename
     #   image_counter = image_counter + 1
    # Variable to get count of total number of pages
    #filelimit = image_counter - 1
    # Creating a text file to write the output
    #outfile = "out_text.txt"
    # Open the file in append mode so that
    # All contents of all images are added to the same file
    #f = open(outfile, "a")
        #for i in range(1, filelimit + 1):
       # filename = "page_" + str(i) + ".jpg"
        # Recognize the text as string in image using pytesserct
        #text = str(((pytesseract.image_to_string(Image.open(filename)))))
        #text = text.replace('-\n', '')
        # encode the text into tensor of integers using the appropriate tokenizer
    # creating a pdf file object
    #pdfFileObj = open(pdf, 'rb')
    #file_name = os.path.dirname(__file__) + '\\' + pdf  # Taking input from user
    file_name = f"uploads/{pdf}"
    path = file_name#.replace(os.sep, '/')
    pdfFileObj = open(path,'rb')
    # print(path)

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # printing number of pages in pdf file
    #print(pdfReader.numPages)
    n = pdfReader.numPages
    text=''
    for i in range(0, n):
        pageObj = pdfReader.getPage(i)
        t = pageObj.extractText()
        str1 = ' '.join([line.strip() for line in t.strip().splitlines() if line.strip()])

        inputs = tokenizer.encode("summarize: " + str(str1), return_tensors="pt", truncation=True)
        outputs = model.generate(inputs, max_length=1500, min_length=50, length_penalty=2.0, num_beams=5,
                                 early_stopping=True)
        out = tokenizer.decode(outputs[0])
        o = out.split('>', 1)
        out1 = o[1].split('<')
        #c = capital(out1[0])
        r = fold(out1[0])
        final_r = capital(r)
        # Finally, write the processed text to the file.
        #final_r
        text+= final_r
        # Close the file after writing all the text.
    #f.close()
    pdfFileObj.close()
    #final_b = b
    return(text)
    #return b

@app.route("/home1", methods=['Get', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            #num = request.form['myfile']
            num = request.files['myfile']
            num.save(os.path.join(UPLOAD_FOLDER, secure_filename(num.filename)))
            r= num.filename
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('home.html', errors=errors)
        if r:
            print(r)
            results1 = summary(r)
    return render_template('index.html',results1=results1, errors=errors)

@app.route('/home2', methods=['GET','POST'])
def index1():
    errors = []
    results = {}
    if request.method == "POST":
        if request.form['voice'] =='voice':
            import speech_recognition as sr
            # Initialize recognizer class (for recognizing the speech)
            r = sr.Recognizer()
            # Reading Microphone as source
            # listening the speech and store in audio_text variable
            with sr.Microphone() as source:
                print("Talk")
                audio_text = r.listen(source)
                print("Time over, thanks")
                # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
                # try:
                # using google speech recognition
                text = r.recognize_google(audio_text)
                # except:
                #    print("Sorry, I did not get that")
                inputs = tokenizer.encode("summarize: " + str(text), return_tensors="pt", truncation=True)
                outputs = model.generate(inputs, max_length=100, min_length=30, length_penalty=2.0, num_beams=5,
                                         early_stopping=True)
                out = tokenizer.decode(outputs[0])
                o = out.split('>', 1)
                out2 = o[1].split('<')
                results = capital(out2[0])
            return render_template('index.html', results2=results, errors=errors)
        else:
            errors.append(
                "Unable to get voice. Please make sure it's valid and try again."
              )
            return render_template('home.html', errors=errors)
@app.route("/home3", methods=['Get', 'POST'])
def index2():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            num = request.files['pdf_file']
            num.save(os.path.join(UPLOAD_FOLDER, secure_filename(num.filename)))
            df = num.filename
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('home.html', errors=errors)
        if df:
            results3 = pdftext(df)
            #os.remove('out_text.txt')
    return render_template('index.html',results3=results3, errors=errors)

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080)
     app.run(debug=True)