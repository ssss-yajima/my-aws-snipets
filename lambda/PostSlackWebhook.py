"""
SlackのIncoming Webhookに通知する。
関数名、ログストリームへのリンクを記載する。
"""
import urllib3
import json

http = urllib3.PoolManager()

def lambda_handler(event, context):
    url = "Slack incoming webhook url"

    function_name = context.function_name
    region = context.invoked_function_arn.split(":")[3]
    request_id = context.aws_request_id
    log_group_name = context.log_group_name
    log_stream_name = context.log_stream_name
    log_url = "https://"+region+".console.aws.amazon.com/cloudwatch/home?region="+region+"#logEvent:group="+log_group_name+";stream="+log_stream_name


    msg = {
        "username": "WEBHOOK_NOTIFICATION",
        "icon_emoji": ":fire:",
        "attachments": [
              {
                  "color": "danger",
                  "title": f"AWS Error notification - {function_name}",
                  "fields": [
                      {
                          "title": "function",
                          "value": function_name,
                          "short": False
                      },
                      {
                          "title": "message",
                          "value": "error message here",
                          "short": False
                      },
                      {
                          "title": "log stream",
                          "value": log_url,
                          "short": False
                      },
                  ],
              }
          ]
      }

    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)

    return "OK"

"""
出力例
※実際Slackのattachmentを利用して少しリッチな見た目で表示される

WEBHOOK_NOTIFICATIONアプリ
AWS Error notification - TestLambdaErrorHandler
function
TestLambdaErrorHandler
message
error message here
log stream
https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#logEvent:group=/aws/lambda/TestLambdaErrorHandler;stream=2022/02/02/[$LATEST]ebb4ff1c04fa4203af1c8e9cf63980d2
"""
