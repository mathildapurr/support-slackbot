import os
import threading
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.util.utils import create_web_client
from slack_sdk.web import client

# define channel IDs. These are ID values in my test slack space. These values should be replaced with IDs for support-aaa and support-dashboard-dataviz
graphing_id = "C034Y6EN77Z"
aaa_id = "C035F450KA8"

# Initializes app with bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Listens to incoming messages that contain anything related to customers
@app.message(re.compile(r"customer|IHAC|cake|tier", flags=re.IGNORECASE))
def message_customer(message, ack, say):
    ack()

    # send different links based on channel. Message fields here: https://api.slack.com/events/message
    text = f""
    if message['channel'] == graphing_id:
        text = f":wave: Hey <@{message['user']}>! Please take a moment to *go through <https://datadoghq.atlassian.net/wiki/spaces/TS/pages/2245853726/Escalation+workflow+for+troubleshooting+dashboard+dataviz+notebooks+issues|our escalation workflow wiki> first*. When you are finished, react to your own post with:"
    if message['channel'] == aaa_id:
        text = f":wave: Hey <@{message['user']}>! Please take a moment to *go through <https://datadoghq.atlassian.net/wiki/spaces/TS/pages/2260729945/Escalation+workflow+for+AAA+Authentication+Access+Control+and+Auditability+Issues|our escalation workflow wiki> first*. When you are finished, react to your own post with:"

    if 'thread_ts' not in message:
        # say() sends a message to the channel where the event was triggered
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{text}"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "• :white_check_mark: if you no longer need help\n• :hand: if you still need help\n"
                    }
                }
            ],
            text=f":wave: Hey <@{message['user']}>! Please take a moment to *go through <https://datadoghq.atlassian.net/wiki/spaces/TS/pages/2245853726/Escalation+workflow+for+troubleshooting+dashboard+dataviz+notebooks+issues|our escalation workflow wiki> first*.",
            thread_ts=message['ts']
        )

@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()