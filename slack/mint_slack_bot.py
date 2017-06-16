#!/usr/bin/env python

SLACK_BOT_TOKEN = 'xxxx-121212121-xxxxxxxxxx'

import os
import time
from slackclient import SlackClient
import requests
import json
import base64
from pymongo import MongoClient
import json
# from bson import json_util, ObjectId
from bson.json_util import dumps
import copy

import logging

logging.basicConfig(level=logging.DEBUG)



## Name of Slack Blot
BOT_NAME = "erp"

## Initialize the Slack Client with Token
slack_client = SlackClient(SLACK_BOT_TOKEN)


## Initialize MongoDb Connection
#uri = "localhost"
uri = "mongod"
port = 27017
client = MongoClient(uri, port)
db = client.my_tasks


## Task Title Dictionary
task_title_dict = { 'Task_ID' : '0,1','Name' : '1,3', 'Subject' :'3,-9', 'Company' : '-9,-7', 'Category': '-7,-6', 'Type': '-6,-4', 'Accepted Status': '-4,-3', 'Start Data': '-3,-2', 'End Date': '-2,-1'}



## DB function: Refresh DB and clean it up
def empty_db():
    return db.my_tasks.delete_many({})

## DB function: Decode input received from selenium and convert it into of list_all_tasks
def decode_s(encoded_from_selenium):
    return base64.b64decode(encoded_from_selenium).decode("utf-8").split("\n")
    #return str(base64.b64decode(encoded_from_selenium)).split("\n")

## DB function: Put titles to all the tasks received from the json Object
def jsonify_object(task_title_dict,tasks):
    jsonified = {}
    data = {}
    for keys,values in task_title_dict.items():
        p=slice(int(values.split(",")[0]),int(values.split(",")[1]))

        jsonified.update({keys : ' '.join(tasks[p])})
    return jsonified


# DB function: Write to MongoDB All new tasks
def refresh_db(taskl):
    for i in range(len(taskl))[1:]:
        if   taskl[i].split(" ")[-3]=="Pending":
             tasku = taskl[i].encode("ascii").decode('utf-8').split(' ')
             tasku.insert(-2, "NULL")
             db.my_tasks.insert_one(jsonify_object(task_title_dict,tasku)).inserted_id
        elif taskl[i].split(" ")[-3]=="Accepted":
             tasku = taskl[i].encode("ascii").decode('utf-8').split(' ')
             tasku.insert(-2, "NULL")
             db.my_tasks.insert_one(jsonify_object(task_title_dict,tasku)).inserted_id
        else:
            tasku = taskl[i].encode("ascii").decode('utf-8').split(' ')
            db.my_tasks.insert_one(jsonify_object(task_title_dict,tasku)).inserted_id

#DB function:
def list_all_tasks():
    list_of_tasks = db.my_tasks.find()
    return list_of_tasks

#DB function:
def list_accepted_tasks_with_status(status):
    list_of_tasks = db.my_tasks.find({"Accepted Status": status})
    return list_of_tasks


#DB function:
def task_with_taskid(taskid):
    list_of_tasks = db.my_tasks.find({"Task_ID": taskid})
    return list_of_tasks

#Slack Function, format the output to json before putting it on slack channel: Test
def format_tasks_for_slack(list_of_tasks):
    response = [
        {
            "fallback": "broken",
            "author_name": "Rob Michaelis",
            "text": "<cmsurl=925617|925617>",
            "fields": [
                {
                    "title": "Category",
                    "value": "Task",
                    "short": "true"
                    },
                {
                    "title": "Company",
                    "value": "Slack Inc",
                    "short": 'true'
                    },
                {
                    "title": "Accepted Status",
                    "value": "Accepted",
                    "short": 'true'
                    },
                {
                    "title": "Due Date",
                    "value": "11/25/2016",
                    "short": 'true'
                    },
                {
                    "title": "Subject",
                    "value": "<cmsurl=925617|Install Demo of Tintri HW in OPenStack P [...]>",
                    "short": 'false'
                    }
                ],
            "color": "#F35A00"
            }
        ]

    ## For loop that fill ins in the field values in the Json operator
    count = 0
    for task in json.loads(dumps(list_of_tasks)):

        response[count]['author_name'] = 'Thomas Edison'
        response[count]['text']=cmsurl+task['Task_ID']+"|"+task['Task_ID']+">"
        response[count]['fields'][0]['value']=task['Category']
        response[count]['fields'][1]['value']=task['Company']
        response[count]['fields'][2]['value']=task['Accepted Status']
        response[count]['fields'][3]['value']=task['End Date']
        response[count]['fields'][4]['value']=cmsurl+task['Task_ID']+"|"+task['Subject']+">"
        if task['Accepted Status'] == "Accepted":
            response[count]['color'] = '#28f100'
        else:
            response[count]['color'] = '#f03000'
        count = count + 1
        response.append(copy.deepcopy(response[0]))
    return response[1:]



#SLACK function:
## Retrieve all users so we can find our bot
def get_bot_id(BOT_NAME):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                return user.get('id')
    else:
        print("could not find bot user with the name " + BOT_NAME)

# starterbot's ID as an environment variable
BOT_ID = get_bot_id(BOT_NAME)

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "@erp"


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith("test"):
        response = requests.get('http://selenium:5000/get_activities').text

    elif command.startswith("refresh"):
        empty_db()
        refresh_db(decode_s(requests.get('http://selenium:5000/get_activities').text))
        response = format_tasks_for_slack(list_all_tasks())
    elif command.startswith('accepted'):
        response = format_tasks_for_slack(list_accepted_tasks_with_status("Accepted"))
    elif command.startswith('pending'):
        response = format_tasks_for_slack(list_accepted_tasks_with_status("Pending"))

    elif command.startswith("testformating"):
        response = [
        {
            "fallback": "broken",
			"author_name": "Steve Hawkins",
            "text": "<cmsurl=925617|925617>",
            "fields": [
                {
                    "title": "Category",
                    "value": "Task",
                    "short": "true"
                },
                {
                    "title": "Company",
                    "value": "Slack Inc",
                    "short": 'true'
                },
				{
                    "title": "Accepted Status",
                    "value": "Accepted",
                    "short": 'true'
                },
				{
                    "title": "Due Date",
                    "value": "11/25/2016",
                    "short": 'true'
                },
				{
                    "title": "Subject",
                    "value": "<cmsurl=925617|Install Demo of Tintri HW in OPenStack P [...]>",
                    "short": 'false'
                }
            ],
            "color": "#F35A00"
        }
    ]
    # response.append(response[0])
    slack_client.api_call("chat.postMessage", channel=channel, text='', attachments=response, as_user=True)
    # slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True, parse='full')




def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    # print("#######THIS IS A TEST ########")
    # print(refresh_db(decode_s(requests.get('http://selenium:5000/etest').text)))
    # print(list_all_tasks())
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
