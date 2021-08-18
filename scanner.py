import serial
import pandas as pd
import numpy as np
from twilio.rest import Client

#twilio (SMS) account info
account_sid =''
auth_token = ''
account_phone_number= ''
client = Client(account_sid,auth_token)


#pandas interacting with excel sheet
df = pd.read_excel('students_table.xlsx')
approved_ids= np.array(df)


# Setting up serial connection and scanning rfid tag
ser = serial.Serial('COM5', 9600, timeout=None)

# Retrieving rfid and casting as hexidecimal then to numpy int64 data type
id = ser.read(8).hex()
id = np.int64(id)



# Creating variables for text message customization
id_phone = df.loc[df['student_id']== id,['phone_num']]
id_phone= id_phone.to_numpy()
student_name = df.loc[df['student_id']== id,['student_name']]
student_name = np.array(student_name)

# Logic for sms message after scan
if id in approved_ids:
    message = client.messages.create(to=f'+1{id_phone[0,0]}',from_=account_phone_number, body=f'Hello, your student, {student_name[0,0]} has successfully checked into class.')
    print(f'Hello, your student, {student_name[0,0]} has successfully checked into class.')
else:
    print('Sorry ID not found, Please register this ID with administrator')