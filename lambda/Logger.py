"""
LambdaなどAWS全般からCloudWatch Logsにログ出力するときのLogger
"""
import json
import logging
import os

class JsonFormatter:
    def format(self, record):
      return json.dumps(vars(record))

# ルートロガーの設定
logging.basicConfig() # 標準エラーに出力するハンドラーをセット
 # ハンドラーの出力フォーマットを自作のものに変更
logging.getLogger().handlers[0].setFormatter(JsonFormatter())
# 以降は普通にloggerを取得して処理を関数を書く
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

def lambda_handler(event, context):
    logger.info("message", extra={"foo":"bar"})

"""
----
出力例
参考：https://qiita.com/tonluqclml/items/780370a4575781eb19df
----

START RequestId: 3ba9c9dd-0758-482e-8aa4-f5496fa49f04 Version: $LATEST
{
    "name": "lambda_function",
    "msg": "sample",
    "args": [],
    "levelname": "INFO",
    "levelno": 20,
    "pathname": "/var/task/lambda_function.py",
    "filename": "lambda_function.py",
    "module": "lambda_function",
    "exc_info": null,
    "exc_text": null,
    "stack_info": null,
    "lineno": 23,
    "funcName": "lambda_handler",
    "created": 1577152740.1250498,
    "msecs": 125.04982948303223,
    "relativeCreated": 64.58139419555664,
    "thread": 140315591210816,
    "threadName": "MainThread",
    "processName": "MainProcess",
    "process": 7,
    "foo": 12,
    "bar": "Hello World!",
    "aws_request_id": "3ba9c9dd-0758-482e-8aa4-f5496fa49f04"
}
END RequestId: 3ba9c9dd-0758-482e-8aa4-f5496fa49f04
REPORT RequestId: 3ba9c9dd-0758-482e-8aa4-f5496fa49f04  Duration: 1.76 ms   Billed Duration: 100 ms Memory Size: 128 MB Max Memory Used: 55 MB  Init Duration: 113.06 ms
"""
