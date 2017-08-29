import os
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

#本地存放文件地址和存放日志地址
dir_add = r"D:\public\01_公司制度"
log_add = r"D:\logs"
last_time = 0

#发送人（代发人）和接收者邮箱list
sender = 'no-reply@htyunwang.com'
password = 'asd.1234'
receivers = ['liuqiang@htyunwang.com']
server_add = 'smtp.mxhichina.com'

def send_email(log_email):
    for email in receivers:
        message = MIMEText(log_email, 'plain', 'utf-8')
        message['From'] = sender
        message['To'] = email

        subject = 'New File Reminder'
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP(server_add)
            smtpObj.login(sender, password)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")

        except smtplib.SMTPException:
            print ("Error: 无法发送邮件")
        except ConnectionRefusedError:
            print ("Error: 目标计算机未开启SMTP")


def new_file(max_time):
    change = False
    file_paths = os.listdir(dir_add)
    time_list = []
    for fileName in file_paths:
        timestamp = float(os.stat(dir_add + "\\" + fileName).st_ctime)
        time_list.append((fileName, timestamp))

    for pair in time_list:
        if pair[1] > last_time:
            change = True
            print(pair[0])
            log = pair[0] + ' is a new file.' + ' Its create timestamp is ' + str(pair[1])
            log_email = pair[0] + ' is a new file to check.'
            write_log(log)
            send_email(log_email)
            if pair[1] > max_time:
                max_time = pair[1]
    if change:
        change_last_time(str(max_time))


def read_last_time():
    f = open(log_add + '\\last_time.txt', 'r')
    s = f.read()
    if s == '':
        lt = 0.0
    else:
        lt = float(s)
    return lt


def change_last_time(max_time):
    f = open(log_add + '\\last_time.txt', 'w')
    f.write(max_time)


def write_start_log():
    f = open(log_add + '\\start.txt', 'a')
    f.write(time.asctime(time.localtime(time.time())))
    f.write("\n")


def write_log(log):
    f = open(log_add + '\\log.txt', 'a')
    f.write(log)
    f.write("\n")


if __name__ == '__main__':
    write_start_log()
    last_time = read_last_time()
    max_time = last_time
    new_file(max_time)
