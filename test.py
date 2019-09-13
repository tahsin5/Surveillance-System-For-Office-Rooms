import time
import sqlite3
import serial
import smtplib
import cv2
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

TO = 'azkhanom@gmail.com'
GMAIL_USER = 'officesystem360@gmail.com'
GMAIL_PASS = 'officesystem360@'

SUBJECT = 'Intrusion!!'
TEXT = 'Your PIR sensor detected movement'

ser = serial.Serial('COM8', 9600)      #change com if it doesn't work

def send_email():

    msg = MIMEMultipart()

    msg['From'] = GMAIL_USER
    msg['To'] = TO
    msg['Subject'] = "INTRUSION!!!"

    body = "There has been an intrusion in your office"

    msg.attach(MIMEText(body, 'plain'))

    filename = capture_image()

    year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')
    name = str(day) + "_" + str(month) + "_" + str(year) + "," + str(hour) + "_" + str(minute) + ".png"

    attachment = open(filename, "rb")
    database_save(filename)

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % name)

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_PASS)
    text = msg.as_string()
    print("Sending Email")
    server.sendmail(GMAIL_USER, TO, text)
    server.quit()

def capture_image():
    # Number of frames to throw away while the camera adjusts to light levels
    #ramp_frames = 30

    camera = cv2.VideoCapture(0) #camera port
    print("Taking image...")
    retval, im = camera.read()
    camera_capture = im
    year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')
    file_name = str(day)+"_"+str(month)+"_"+str(year)+","+str(hour)+"_"+str(minute)+".png"
    path = r"C:\xampp\htdocs\Office Security\pictures\\"
    file_name = path+file_name
    cv2.imwrite(file_name, camera_capture)

    del(camera)
    return file_name

def database_save(fileName):
    conn = sqlite3.connect(r'C:\xampp\htdocs\Office Security\example.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS intruders
                (id integer primary key, date text, time text, img text)''')

    year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')
    current_date = str(day)+"-"+str(month)+"-"+str(year)
    current_time = str(hour)+":"+str(minute)
    values = (current_date, current_time, fileName)
    c.execute("INSERT INTO intruders(date, time, img) VALUES (?,?,?)", values)

    conn.commit() # Save (commit) the changes

    #for row in c.execute('SELECT * FROM intruders ORDER BY id'):
        #row3 = row[3]
        #print row3
    conn.close()

while True:
    message = ser.readline()
    if message[0] == 'S':
       send_email()
    time.sleep(3)
