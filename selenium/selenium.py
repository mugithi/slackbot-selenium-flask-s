#!/usr/bin/env python

from flask import Flask
from flask import make_response
import threading
from selenium import webdriver
from pyvirtualdisplay import Display
import time
import base64


username="username"
password="password"
cmsurl="http://cms.company.com/login.asp"
app = Flask(__name__)



@app.route('/test')
def test():
    return 'Flask Dockerized'

@app.route('/etest')
def test_encoded():
    return('QWN0aXZdHlJRCBPd25lciBTdWJqZWN0IENvbXBhbnkgTmFtZSBPcHB0eSBOYW1lIENhdGVnb3J5IFR5cGUgQXNzaWduIFN0YXR1cyBTdGFydCBEYXRlIEVuZCBEYXRlIEhyCjkyNDY3MyBJc2FhY2sgS2FyYW5qYSBJbnN0YWxsIERlbW8gb2YgVGludHJpIEhXIGluIE9QZW5TdGFjayBQIFsuLi5dIERhc2hlciBUZWNobm9sb2dpZXMgVGFzayBJbnRlcm5hbCBQcm9qZWN0IEFjY2VwdGVkIDExLzI1LzIwMTYgMjAKOTI0OTI4IElzYWFjayBLYXJhbmphIGNyZWF0ZSBTT1cgYW5kIHF1b3RlIFBhcmFtaXQgQ29ycG9yYXRpb24gVGFzayBDcmVhdGUgU09XIEFjY2VwdGVkIDExLzMwLzIwMTYgMgo5MjU1MzcgSXNhYWNrIEthcmFuamEgQ3JlYXRlIFNPVyAtIHZTQU4gcHJvamVjdCBBbm9tYWxpIFRhc2sgQ3JlYXRlIFNPVyBBY2NlcHRlZCAxMi8yMS8yMDE2IDIKOTI1NjE3IElzYWFjayBLYXJhbmphIFNldHVwIGEgVk1XYXJlIEVudmlyb25tZW50IHRvIGFjY2VzcyB0aGUgWy4uLl0gRGFzaGVyIFRlY2hub2xvZ2llcyBUYXNrIEludGVybmFsIFByb2plY3QgQWNjZXB0ZWQgMS8yMC8yMDE3IDQKOTI1Nzc1IElzYWFjayBLYXJhbmphIENyZWF0ZSBWTSBiYWNrdXAvcmVzdG9yZSBhbmQgQ2xvdWQgb3B0aW8gWy4uLl0gQmFsYml4IFRhc2sgUHJlc2FsZXMgRW5naW5lZXJpbmcgQWNjZXB0ZWQgMTIvOC8yMDE2IDMKOTI1ODE3IElzYWFjayBLYXJhbmphIENlbnRyYWwgRkxvcmlkYSBFeHByZXNzd2F5IENGWCBPcHBvcnR1bmkgWy4uLl0gQ2VudHJhbCBGbG9yaWRhIEV4cHJlc3N3YXkgQXV0aG9yaXR5IFJYMjgwMCBNU0EyMDQwIGFuZCBGQyBTd2l0Y2hlcyBUYXNrIFByZXNhbGVzIEVuZ2luZWVyaW5nIEFjY2VwdGVkIDEyLzEzLzIwMTYgMQo5MjU4MjQgSXNhYWNrIEthcmFuamEgTmVhciBMaW5lIFN0b3JhZ2UgUmV2aWV3IFIuUy4gSHVnaGVzIEV2ZW50IFByZXNhbGVzIEVuZ2luZWVyaW5nIEFjY2VwdGVkIDEyLzEzLzIwMTYgMTIvMTMvMjAxNiAxCjkyNjAwOCBJc2FhY2sgS2FyYW5qYSBzdXBwb3J0IEVudGVmeSBDaGFuZ2VzIEVudGVmeSBJbmZyYXN0cnVjdHVyZSBVcGdyYWRlcyBUYXNrIFByZXNhbGVzIEVuZ2luZWVyaW5nIEFjY2VwdGVkIDEyLzIwLzIwMTYgMQo5MjYwMzUgSXNhYWNrIEthcmFuamEgSW50ZXJtb2xlY3VsYXIgfCBEYXNoZXIgLSBFbmRwb2ludCAmIERSIFsuLi5dIEludGVybW9sZWN1bGFyIEVuZHBvaW50IFByb3RlY3Rpb24gRXZlbnQgQ2xpZW50IE1lZXRpbmcgQWNjZXB0ZWQgMS81LzIwMTcgMS81LzIwMTcgMgo5MjYwNzMgSXNhYWNrIEthcmFuamEgQ2FsbCB0byBEaXNjdXNzIEFXUyBDb25zdWx0aW5nIFNlcnZpY2VzIFsuLi5dIFZlbG9keW5lIEV2ZW50IENsaWVudCBNZWV0aW5nIFBlbmRpbmcgMTIvMjEvMjAxNiAxMi8yMS8yMDE2IDAuNQo5MjYwODQgSXNhYWNrIEthcmFuamEgQ3JlYXRlIFNPVyAtIEFXUyBDb25zdWx0aW5nIFNlcnZpY2VzIFZlbG9keW5lIFRhc2sgQ3JlYXRlIFNPVyBQZW5kaW5nIDEyLzIzLzIwMTYgMg==')

@app.route('/get_activities')
def get_all_activities():
    display = Display(visible=0, size=(1366, 768))
    display.start()
    browser = webdriver.Chrome()
    browser.set_window_size(1366, 768)
    browser.get(cmsurl)
    browser.save_screenshot('vionblog.png')
    time.sleep(3)
    username = browser.find_element_by_id('username')
    username.send_keys(username)
    password = browser.find_element_by_id('password')
    password.send_keys(password)
    browser.find_element_by_id("wp-submit").click()
    time.sleep(5)
    browser.save_screenshot('vionblog1.png')
    activity = browser.find_element_by_id('tblActivity_wrapper')
    open_activity = activity.text.split('\n')
    response = make_response(base64.b64encode(activity.text))
    browser.quit()
    return response


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
