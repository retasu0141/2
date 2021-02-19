from flask import Flask, request, abort,render_template
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent, TextMessage, TextSendMessage, FlexSendMessage,  PostbackEvent, TemplateSendMessage,ButtonsTemplate,URIAction,QuickReplyButton,QuickReply
)

import time
import math
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import random

from datetime import datetime as dt

import urllib.request, urllib.error

from apiclient.discovery import build
import urllib.parse
import re, requests
app = Flask(__name__)

set = {}
up = {}

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

def syoukai():
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://live.staticflickr.com/65535/50834110728_1395d79f76_n.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Editor‘s Camp",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "text",
            "text": "受付へようこそ！",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは以下のことを行います",
            "weight": "bold",
            "size": "md",
            "align": "center",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "参加ルールの説明",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "自分のTwitterの登録",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center",
                "margin": "none"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "動画編集歴の登録",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "自分のこれからの目標の登録",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "悩み事アンケート",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "参加後ノートに作成する自己紹介文配布",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "動画編集者の森へ招待！",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "text",
            "text": "下のボタンを押して次に進もう！",
            "weight": "bold",
            "size": "md",
            "align": "center",
            "margin": "md"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
              "type": "postback",
              "label": "参加ルールを聞く",
              "data": "注意事項",
              "displayText": "参加ルールを教えて！"
            }
          },
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def attention():
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2015/02/13/10/18/stop-634941_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "参加ルールの説明",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "text",
        "text": "ルールはたったの二つだけです！",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "1.",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "Twitterのアカウント名で参加する。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "2.",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": "モラルに反する発言をしない。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      },
      {
        "type": "text",
        "text": "以上の二つを守れる方は",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "次に進んで下さい",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "none"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "Twitterの登録",
          "data": "twitter",
          "displayText": "Twitterの登録をするよ！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def twitter():
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2018/05/08/08/42/handshake-3382503_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Twitterの登録",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "・あつまれ動画編集の森では信頼を大切にしています。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "start"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "・信頼関係を築く為、Twitter名での参加がルールとなっています。",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "start"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "start",
                "text": "・この後自己紹介用のテンプレートを配布するにあたって自分のTwitter情報を登録して頂きます。"
              }
            ]
          }
        ]
      },
      {
        "type": "text",
        "text": "つまり自分のTwitterアカウントの",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "[リンク]or[id]",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "none"
      },
      {
        "type": "text",
        "text": "を送信して頂きます",
        "weight": "bold",
        "size": "md",
        "align": "center",
        "margin": "none"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "[Twitterリンク例]",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "https://twitter.com/retasu_0141",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "[Twitter id例]",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "@retasu_0141",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          }
        ]
      },
      {
        "type": "text",
        "text": "上の二つの例を参考に",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "自分のTwitter情報を送信してください！",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "none"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data1(twitter):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2018/06/12/15/08/question-mark-3470783_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Twitter登録の確認",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "text",
        "text": "Twitter情報は以下の内容で大丈夫ですか？",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": twitter,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "はい",
          "data": "ok",
          "displayText": "OK!"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "いいえ",
          "data": "no",
          "displayText": "もう一度設定！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data2():
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://cdn.pixabay.com/photo/2016/01/15/12/02/editing-1141505_1280.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "動画編集歴の登録",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "start",
                    "text": "・この後自己紹介用のテンプレートを配布するにあたって自分の動画編集歴を登録して頂きます。"
                  }
                ]
              },
              {
                "type": "text",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "start",
                "text": "・動画編集でなくても活動履歴などを書いて頂いて結構です"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "[動画編集歴 例]",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "2020年6月辺りから",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "ゲーム実況を2019年辺りから",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "最近始めたばかり",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "text",
            "text": "上の例を参考に",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "自分の動画編集歴を送信してください！",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "none"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def data3(data_):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2018/06/12/15/08/question-mark-3470783_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "動画編集歴登録の確認",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "text",
        "text": "動画編集歴は以下の内容で大丈夫ですか？",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": data_,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "はい",
          "data": "ok2",
          "displayText": "OK!"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "いいえ",
          "data": "no2",
          "displayText": "もう一度設定！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data4():
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://cdn.pixabay.com/photo/2016/03/09/09/43/person-1245959_1280.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "目標の登録",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "start",
                    "text": "・この後自己紹介用のテンプレートを配布するにあたって自分の目標を登録して頂きます。"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "[目標 例]",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "案件を獲得する！",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "人脈を増やしたい！",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "まずは編集を経験してみたい！",
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "text",
            "text": "上の例を参考に",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "md"
          },
          {
            "type": "text",
            "text": "自分の目標を送信してください！",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "none"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def data5(text):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2016/01/19/17/53/writing-1149962_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "自己紹介テンプレート配布",
        "weight": "bold",
        "size": "lg",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "下のボタンからテンプレートを受け取れるので、テンプレートを元に参加後オープンチャットのノートに自己紹介を書き込んで下さい！",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "受け取る",
          "data": "受け取る",
          "displayText": text
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data6():
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://cdn.pixabay.com/photo/2016/10/24/23/11/doors-1767562_1280.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover",
        "action": {
          "type": "uri",
          "uri": "http://linecorp.com/"
        }
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "さあ、参加しよう！",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": "登録おつかれ様でした！",
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "下のボタンから参加しましょう！",
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          },
          {
            "type": "text",
            "text": "参加後自己紹介文をノートに貼ろう！",
            "weight": "bold",
            "size": "sm",
            "align": "center",
            "margin": "sm"
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
              "type": "uri",
              "label": "参加！",
              "uri": "https://line.me/ti/g2/lDVbXX6utEKgPM-QB3tylA?utm_source=invitation&amp;utm_medium=link_copy&amp;utm_campaign=default"
            }
          },
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def data7(text):
    data = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://cdn.pixabay.com/photo/2018/06/12/15/08/question-mark-3470783_1280.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "目標登録の確認",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "text",
        "text": "目標は以下の内容で大丈夫ですか？",
        "weight": "bold",
        "size": "xs",
        "align": "center",
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": text,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5,
                "align": "center"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "はい",
          "data": "ok3",
          "displayText": "OK!"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "いいえ",
          "data": "no3",
          "displayText": "もう一度設定！"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}
    return data

def data8():
    data = {
      "type": "carousel",
      "contents": [
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2017/05/02/10/01/checklist-2277702_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "アンケート",
                "wrap": True,
                "weight": "bold",
                "size": "xxl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "にご協力ください！",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "右にある4つの悩みのうち",
                    "wrap": True,
                    "weight": "bold",
                    "size": "xs",
                    "align": "center",
                    "margin": "none"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "wrap": True,
                    "weight": "bold",
                    "size": "xs",
                    "align": "center",
                    "text": "自分に当てはまるものを選択してください！"
                  }
                ]
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://charbase.com/images/glyph/10137",
                "size": "lg",
                "aspectMode": "cover"
              }
            ]
          }
        },
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2016/01/31/20/20/frightened-1172122_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "今の編集スキルで",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "案件を最後までこなせるか不安...",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://static.thenounproject.com/png/76988-200.png",
                "size": "lg",
                "aspectMode": "cover"
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "これを選ぶ",
                  "data": "1",
                  "displayText": "1番目を選んだよ！"
                }
              }
            ]
          }
        },
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2020/08/31/00/29/man-5531026_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "実績がないから",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "クラウドソーシングに応募しても",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              },
              {
                "type": "text",
                "text": "なかなか案件を獲得できない...",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://static.thenounproject.com/png/76988-200.png",
                "size": "lg",
                "aspectMode": "cover"
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "これを選ぶ",
                  "data": "2",
                  "displayText": "2番目を選んだよ！"
                }
              }
            ]
          }
        },
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2014/07/12/14/55/bus-stop-391242_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "営業文の",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "書き方がわからない...",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://static.thenounproject.com/png/76988-200.png",
                "size": "lg",
                "aspectMode": "cover"
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "これを選ぶ",
                  "data": "3",
                  "displayText": "3番目を選んだよ！"
                }
              }
            ]
          }
        },
        {
          "type": "bubble",
          "hero": {
            "type": "image",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "url": "https://cdn.pixabay.com/photo/2017/08/25/21/46/upset-2681502_1280.jpg"
          },
          "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "発注者と",
                "wrap": True,
                "weight": "bold",
                "size": "xl",
                "align": "center"
              },
              {
                "type": "text",
                "text": "上手くコミュニケーションが",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              },
              {
                "type": "text",
                "text": "取れるか心配...",
                "wrap": True,
                "weight": "bold",
                "size": "md",
                "align": "center"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "image",
                "url": "https://static.thenounproject.com/png/76988-200.png",
                "size": "lg",
                "aspectMode": "cover"
              },
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "postback",
                  "label": "これを選ぶ",
                  "data": "4",
                  "displayText": "4番目を選んだよ！"
                }
              }
            ]
          }
        }
      ]
    }
    return data



def text(user_id):
    data = '名前:自分の名前を入力\n自分のTwitter:{twitter}\n動画編集歴:{d_n}\nこれからの目標:{d_t}\nポートフォリオのURL:\nみんなへ一言:'.format(twitter=set[user_id]['twitter'],d_n=set[user_id]['d_n'],d_t=set[user_id]['d_t'])
    return data

#------------------------情報アップ-------------------------------------------------#

def up1():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "情報アップへようこそ",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは編集者の情報をアップします",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "自分で打ち込む情報",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・自分の強み",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "自分の強みを3つアップ",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・一言",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "クライアントへ一言",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ポートフォリオ",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "YouTubeのURL",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・Twitter",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                  },
                  {
                    "type": "text",
                    "text": "自分のTwitterのURL",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "text",
                "text": "選択する情報",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "xxl",
                "contents": [
                  {
                    "type": "text",
                    "text": "・動画編集ジャンル",
                    "size": "sm",
                    "color": "#555555"
                  },
                  {
                    "type": "text",
                    "text": "5択×2",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・希望単価",
                    "size": "sm",
                    "color": "#555555"
                  },
                  {
                    "type": "text",
                    "text": "4択",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・週あたりの納品数",
                    "size": "sm",
                    "color": "#555555"
                  },
                  {
                    "type": "text",
                    "text": "4択",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "次へ進む",
                  "data": "up1",
                  "displayText": "自分の強みをアップ"
                },
                "height": "md",
                "style": "secondary"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def updata(up,id):
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "あなたの情報",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "あなたの編集者情報を確認します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "自分で打ち込む情報",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・自分の強み",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['one_text'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・一言",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['text'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ポートフォリオ",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['y_url'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "ここから見れるか確認",
                  "uri": up[id]['y_url']
                },
                "style": "link",
                "margin": "none"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・Twitter",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['t_url'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "ここから見れるか確認",
                  "uri": up[id]['t_url']
                },
                "style": "link",
                "margin": "none"
              },
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "text",
                "text": "選択する情報",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "xxl",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ジャンル1",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['s_g1'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ジャンル2",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['s_g2'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・希望単価",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['s_m'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・週あたりの納品数",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['s_n'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "次へ進む",
                  "data": "up1",
                  "displayText": "自分の強みをアップ"
                },
                "height": "md",
                "style": "secondary"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def up2():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "あなたの強みを書きましょう",
            "weight": "bold",
            "size": "lg",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは編集者としての強みをアップします",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "アップのやり方",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・自分の強みを3つ縦に箇条書きします",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・それを送信します",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "〜例〜",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ],
                "spacing": "none",
                "margin": "lg"
              },
              {
                "type": "image",
                "url": "https://live.staticflickr.com/65535/50959371258_eda1eeb962_o_d.jpg",
                "margin": "none",
                "size": "full",
                "aspectMode": "fit"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "上の例のように送信してみてください",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "margin": "none",
                    "weight": "bold"
                  }
                ]
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def uptest(text,ok,no):
    data = {
      "type": "bubble",
      "hero": {
        "type": "image",
        "url": "https://cdn.pixabay.com/photo/2018/06/12/15/08/question-mark-3470783_1280.jpg",
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "cover"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "登録の確認",
            "weight": "bold",
            "size": "xl",
            "align": "center"
          },
          {
            "type": "text",
            "text": "以下の内容で大丈夫ですか？",
            "weight": "bold",
            "size": "xs",
            "align": "center",
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "lg",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": text,
                    "wrap": True,
                    "color": "#666666",
                    "size": "sm",
                    "flex": 5,
                    "align": "center"
                  }
                ]
              }
            ]
          }
        ]
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "style": "primary",
            "height": "sm",
            "action": {
              "type": "postback",
              "label": "はい",
              "data": ok,
              "displayText": "OK"
            }
          },
          {
            "type": "button",
            "style": "secondary",
            "height": "sm",
            "action": {
              "type": "postback",
              "label": "いいえ",
              "data": no,
              "displayText": "もう一度設定"
            }
          },
          {
            "type": "spacer",
            "size": "sm"
          }
        ],
        "flex": 0
      }
    }
    return data

def up3():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "あなたのアピールを書きましょう",
            "weight": "bold",
            "size": "md",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは編集者としての一言をアップします",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "アップのやり方",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・自分のアピールを簡単に書きます",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・それを送信します",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "〜例〜",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ],
                "spacing": "none",
                "margin": "lg"
              },
              {
                "type": "image",
                "url": "https://live.staticflickr.com/65535/50959489933_8538ffbe98_o_d.jpg",
                "margin": "none",
                "size": "full",
                "aspectMode": "fit"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "上の例のように送信してみてください",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "margin": "none",
                    "weight": "bold"
                  }
                ]
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def up4():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "ポートフォリオを登録しましょう",
            "weight": "bold",
            "size": "md",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここではポートフォリオをアップします",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "アップのやり方",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ポートフォリオのurlをコピペします",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・それを送信します",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "【注意】",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・YouTubeのURLを送信してください",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・例のように動画が出ることを確認してください",
                    "size": "xxs",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "〜例〜",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ],
                "spacing": "none",
                "margin": "lg"
              },
              {
                "type": "image",
                "url": "https://live.staticflickr.com/65535/50959522453_7b2415bec5_o_d.jpg",
                "margin": "none",
                "size": "full",
                "aspectMode": "fit"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "上の例のように送信してみてください",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "margin": "none",
                    "weight": "bold"
                  }
                ]
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def up5():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Twitterを登録しましょう",
            "weight": "bold",
            "size": "lg",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここではTwitterを登録します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "アップのやり方",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ユーザーIDを確認します",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "例 : @retasu_0141",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・https://twitter.com/ の後に",
                    "size": "xs",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "　'@'を抜いたユーザーIDを入れます",
                    "size": "xs",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "例 : https://twitter.com/retasu_0141",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "【注意】",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・TwitterのURLを送信してください",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・例のように表示が出ることを確認してください",
                    "size": "xxs",
                    "color": "#555555",
                    "align": "center",
                    "flex": 0
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "〜例〜",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ],
                "spacing": "none",
                "margin": "lg"
              },
              {
                "type": "image",
                "url": "https://live.staticflickr.com/65535/50960352827_b820c28432_o_d.jpg",
                "margin": "none",
                "size": "full",
                "aspectMode": "fit"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "上の例のように送信してみてください",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center",
                    "margin": "none",
                    "weight": "bold"
                  }
                ]
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def up6():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "動画編集ジャンルを登録しましょう",
            "weight": "bold",
            "size": "md",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは動画編集ジャンル[1]を登録します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "下から[得意]または[やりたい]ジャンルを",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "text",
                "text": "選択しタップしてください",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center",
                "margin": "none"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "ゲーム実況",
                  "data": "up6ゲーム実況"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "エンタメ",
                  "data": "up6エンタメ"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "ビジネス",
                  "data": "up6ビジネス"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "Vlog",
                  "data": "up6Vlog"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "その他",
                  "data": "up6その他"
                },
                "style": "secondary"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def upg1_Other():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "動画編集ジャンルを登録しましょう",
            "weight": "bold",
            "size": "md",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは動画編集ジャンル[1]を登録します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "その他を選択しました",
                "size": "lg",
                "wrap": True,
                "align": "center",
                "weight": "bold"
              },
              {
                "type": "text",
                "text": "動画編集のジャンルを任意で書いて送信してください",
                "size": "md",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center",
                "margin": "none"
              },
              {
                "type": "text",
                "text": "〜例〜",
                "size": "md",
                "wrap": True,
                "align": "center",
                "margin": "none"
              },
              {
                "type": "image",
                "url": "https://live.staticflickr.com/65535/50959637123_69b268b7e1_o_d.jpg",
                "size": "5xl"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def up7():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "動画編集ジャンルを登録しましょう",
            "weight": "bold",
            "size": "md",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは動画編集ジャンル[2]を登録します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "下から[得意]または[やりたい]ジャンルを",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "text",
                "text": "選択しタップしてください",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center",
                "margin": "none"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "かっこいい",
                  "data": "up8かっこいい"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "面白い",
                  "data": "up8面白い"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "オシャレ",
                  "data": "up8オシャレ"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "可愛い",
                  "data": "up8可愛い"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "その他",
                  "data": "up6その他"
                },
                "style": "secondary"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def upg2_Other():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "動画編集ジャンルを登録しましょう",
            "weight": "bold",
            "size": "md",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは動画編集ジャンル[2]を登録します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "その他を選択しました",
                "size": "lg",
                "wrap": True,
                "align": "center",
                "weight": "bold"
              },
              {
                "type": "text",
                "text": "動画編集のジャンルを任意で書いて送信してください",
                "size": "md",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center",
                "margin": "none"
              },
              {
                "type": "text",
                "text": "〜例〜",
                "size": "md",
                "wrap": True,
                "align": "center",
                "margin": "none"
              },
              {
                "type": "image",
                "url": "https://live.staticflickr.com/65535/50960378651_2d2629ca6b_o_d.jpg",
                "size": "5xl"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def up8():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "希望単価を登録しましょう",
            "weight": "bold",
            "size": "lg",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは希望単価を登録します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "下から希望する単価を",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "text",
                "text": "選択しタップしてください",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center",
                "margin": "none"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "~3000円",
                  "data": "up10~3000円"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "3000~5000円",
                  "data": "up103000~5000円"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "5000円~1万円",
                  "data": "up105000円~1万円"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "1万円以上",
                  "data": "up101万円以上"
                },
                "style": "secondary"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def up9():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "希望する週の納品数を登録しましょう",
            "weight": "bold",
            "size": "sm",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "ここでは希望する週の納品数を登録します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "下から希望する週の納品数を",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "text",
                "text": "選択しタップしてください",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center",
                "margin": "none"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "週7本",
                  "data": "up12週7本"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "週5~7本",
                  "data": "up12週5~7本"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "週3~5本",
                  "data": "up12週3~5本"
                },
                "style": "secondary"
              },
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "週3本以下",
                  "data": "up12週3本以下"
                },
                "style": "secondary"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

def updata2():
    data = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "あなたの情報",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "align": "center"
          },
          {
            "type": "text",
            "text": "あなたの編集者情報を確認します",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": True,
            "align": "center"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "margin": "xxl",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "自分で打ち込む情報",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・自分の強み",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['one_text'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・一言",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['text'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ポートフォリオ",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['y_url'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "ここから見れるか確認",
                  "uri": up[id]['y_url']
                },
                "style": "link",
                "margin": "none"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・Twitter",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['t_url'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "button",
                "action": {
                  "type": "uri",
                  "label": "ここから見れるか確認",
                  "uri": up[id]['t_url']
                },
                "style": "link",
                "margin": "none"
              },
              {
                "type": "separator",
                "margin": "xxl"
              },
              {
                "type": "text",
                "text": "選択する情報",
                "size": "xs",
                "color": "#aaaaaa",
                "wrap": True,
                "align": "center"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "xxl",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ジャンル1",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['s_g1'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": "・ジャンル2",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['s_g2'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・希望単価",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['s_m'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "text",
                    "text": "・週あたりの納品数",
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "horizontal",
                "margin": "none",
                "contents": [
                  {
                    "type": "text",
                    "text": up[id]['s_n'],
                    "size": "sm",
                    "color": "#555555",
                    "align": "center"
                  }
                ]
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "md",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "登録を終わる",
                  "data": "up14",
                  "displayText": "登録完了"
                },
                "height": "md",
                "style": "secondary"
              }
            ]
          }
        ]
      },
      "styles": {
        "footer": {
          "separator": True
        }
      }
    }
    return data

'''
def updata():
    data = {}
    return data
'''

def idcheck(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
    cur.execute('SELECT * FROM db')

    for row in cur:
        if id in row:
            #user_id = row[0],one_text=row[1]...s_n=row[8]
            up[id] = {'user_id':id,'n':1,'one_text':row[1],'text':row[2],'y_url':row[3],'t_url':row[4],'s_g1':row[5],'s_g2':row[6],'s_m':row[7],'s_n':row[8]}
            data = True
            return up,data

    text = '・納期厳守\n・即レス\n・視聴維持率up'
    text_ = '○○はお任せください！'

    cur.execute("insert into db values('{user_id}','{one_text}','{text}','{y_url}','{t_url}','{s_g1}','{s_g2}','{s_m}','{s_n}')".format(user_id=id,one_text=text,text=text_,y_url='なし',t_url='なし',s_g1='0',s_g2='0',s_m='0',s_n='0'))
    conn.commit()
    up[id] = {'user_id':id,'n':1,'one_text':text,'text':text_,'y_url':'なし','t_url':'なし','s_g1':'0','s_g2':'0','s_m':'0','s_n':'0'}
    data = False
    return up,data

def seve(id,up):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        conn.commit()
        cur.execute('SELECT * FROM db')
        for row in cur:
            if id in row:
                cur.execute("UPDATE db SET one_text = '{text}' WHERE user_id='{user_id}';".format(text=up[id]['one_text'],user_id=id))
                conn.commit()
                cur.execute("UPDATE db SET text = '{text}' WHERE user_id='{user_id}';".format(text=up[id]['text'],user_id=id))
                conn.commit()
                cur.execute("UPDATE db SET y_url = '{text}' WHERE user_id='{user_id}';".format(text=up[id]['y_url'],user_id=id))
                conn.commit()
                cur.execute("UPDATE db SET t_url = '{text}' WHERE user_id='{user_id}';".format(text=up[id]['t_url'],user_id=id))
                conn.commit()
                cur.execute("UPDATE db SET s_g1 = '{text}' WHERE user_id='{user_id}';".format(text=up[id]['s_g1'],user_id=id))
                conn.commit()
                cur.execute("UPDATE db SET s_g2 = '{text}' WHERE user_id='{user_id}';".format(text=up[id]['s_g2'],user_id=id))
                conn.commit()
                cur.execute("UPDATE db SET s_m = '{text}' WHERE user_id='{user_id}';".format(text=up[id]['s_m'],user_id=id))
                conn.commit()
                cur.execute("UPDATE db SET s_n = '{text}' WHERE user_id='{user_id}';".format(text=up[id]['s_n'],user_id=id))
                conn.commit()
                return True
        #cur.execute("UPDATE db SET name = '{name}' WHERE user_id='{user_id}';".format(name=ID2,user_id=ID+'Ms'))
        conn.commit()
        return False
    except Exception as e:
        print (str(e))
        return

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
'''@handler.add(JoinEvent)
def join(event):
    reply_token = event.reply_token
    data = syoukai()
    flex = {"type": "flex","altText": "自己紹介","contents":data}
    container_obj = FlexSendMessage.new_from_json_dict(flex)
    line_bot_api.reply_message(reply_token,messages=container_obj)'''


@handler.add(PostbackEvent)
def on_postback(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    postback_msg = event.postback.data

    if "注意事項" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 1:
        set[user_id]['n'] = 2
        data = attention()
        flex = {"type": "flex","altText": "注意事項","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "twitter" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 2:
        set[user_id]['n'] = 3
        data = twitter()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "no" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 4:
        set[user_id]['n'] = 3
        data = twitter()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "ok" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 4:
        set[user_id]['n'] = 5
        data = data2()
        flex = {"type": "flex","altText": "動画編集歴","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "no2" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 6:
        set[user_id]['n'] = 5
        data = data2()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "ok2" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 6:
        set[user_id]['n'] = 7
        data = data4()
        flex = {"type": "flex","altText": "目標","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "no3" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 8:
        set[user_id]['n'] = 7
        data = data4()
        flex = {"type": "flex","altText": "twitter登録","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "ok3" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 8:
        set[user_id]['n'] = 9
        data = data8()
        flex = {"type": "flex","altText": "アンケート","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if postback_msg in ['1','2','3','4'] and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 9:
        set[user_id]['n'] = 10
        text_ = text(user_id)
        q = postback_msg
        line_bot_api.multicast(['U76d18383a9b659b9ab3d0e43d06c1e78','U6884dfdb4c4091381363d84965956f2f'],TextSendMessage(text='誰かが参加しようとしています！\n[詳細]\nTwitter:{twitter}\n動画編集歴:{d_n}\n目標:{d_t}\n悩み:{q}'.format(twitter=set[user_id]['twitter'],d_n=set[user_id]['d_n'],d_t=set[user_id]['d_t'],q=q)))
        data = data5(text_)
        flex = {"type": "flex","altText": "テンプレート配布","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "受け取る" in postback_msg and user_id == set[user_id]['user_id'] and set[user_id]['n'] == 10:
        data = data6()
        flex = {"type": "flex","altText": "入ろう！","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

#------------------------情報アップ-------------------------------------------------#

    if "up1" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 1 or up[user_id]['n'] == 3):
        up[user_id]['n'] = 2
        data = up2()
        flex = {"type": "flex","altText": "書き方","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "up2" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 3 or up[user_id]['n'] == 5):
        up[user_id]['n'] = 4
        data = up3()
        flex = {"type": "flex","altText": "書き方","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "up3" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 5 or up[user_id]['n'] == 7):
        up[user_id]['n'] = 6
        data = up4()
        flex = {"type": "flex","altText": "書き方","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)

    if "up4" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 7 or up[user_id]['n'] == 9):
        up[user_id]['n'] = 8
        data = up5()
        flex = {"type": "flex","altText": "書き方","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up5" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 9 or up[user_id]['n'] == 12):
        up[user_id]['n'] = 10
        data = up6()
        flex = {"type": "flex","altText": "選択","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up6" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 10 or up[user_id]['n'] == 12):
        text_ = postback_msg.split('up6')
        if text_[1] == 'その他':
            up[user_id]['n'] = 11
            data = upg1_Other()
            flex = {"type": "flex","altText": "その他","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(reply_token,messages=container_obj)
        else:
            up[user_id]['n'] = 12
            up[user_id]['s_g1'] = text_[1]
            data = uptest(up[user_id]['s_g1'],'up7','up5')
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up7" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 12 or up[user_id]['n'] == 15):
        up[user_id]['n'] = 13
        data = up7()
        flex = {"type": "flex","altText": "選択","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up8" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 13 or up[user_id]['n'] == 15):
        text_ = postback_msg.split('up8')
        if text_[1] == 'その他':
            up[user_id]['n'] = 14
            data = upg2_Other()
            flex = {"type": "flex","altText": "その他","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(reply_token,messages=container_obj)
        else:
            up[user_id]['n'] = 15
            up[user_id]['s_g2'] = text_[1]
            data = uptest(up[user_id]['s_g2'],'up9','up7')
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up9" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 15 or up[user_id]['n'] == 17):
        up[user_id]['n'] = 16
        data = up8()
        flex = {"type": "flex","altText": "選択","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up10" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 16 or up[user_id]['n'] == 18):
        text_ = postback_msg.split('up10')
        up[user_id]['n'] = 17
        up[user_id]['s_m'] = text_[1]
        data = uptest(up[user_id]['s_m'],'up11','up9')
        flex = {"type": "flex","altText": "確認","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up11" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 17 or up[user_id]['n'] == 19):
        up[user_id]['n'] = 18
        data = up9()
        flex = {"type": "flex","altText": "選択","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up12" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 18 or up[user_id]['n'] == 20):
        text_ = postback_msg.split('up12')
        up[user_id]['n'] = 19
        up[user_id]['s_n'] = text_[1]
        data = uptest(up[user_id]['s_n'],'up13','up11')
        flex = {"type": "flex","altText": "確認","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(reply_token,messages=container_obj)
    if "up13" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 19 or up[user_id]['n'] == 21):
        sevedata = seve(user_id,up)
        if sevedata:
            up[user_id]['n'] = 20
            data = updata2(up,user_id)
            flex = {"type": "flex","altText": "あなたの情報","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(reply_token,messages=container_obj)
        else:
            up[user_id]['n'] = 18
            line_bot_api.reply_message(reply_token,TextSendMessage(text="保存中にエラーが起きました"))
    if "up14" in postback_msg and user_id == up[user_id]['user_id'] and (up[user_id]['n'] == 20 or up[user_id]['n'] == 22):
        line_bot_api.reply_message(reply_token,TextSendMessage(text="保存が完了しました！"))


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global set_
    global stoptime
    global stoppoint
    msg_from = event.reply_token
    msg_text = event.message.text
    msg_id = event.message.id
    user_id = event.source.user_id

    if msg_text == 'Editor‘s Campに入る':
        data = syoukai()
        set[user_id] = {'user_id':user_id,'n':1,'twitter':'','d_n':'','d_t':'','text':''}
        flex = {"type": "flex","altText": "ようこそ！","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(msg_from,messages=container_obj)
        return

    if msg_text == 'user_id':
        line_bot_api.reply_message(msg_from,TextSendMessage(text=user_id))
        return

    if msg_text == "情報アップ":
        up,user_data = idcheck()
        up[user_id]['n'] = 1
        if user_data:
            data = updata(up,user_id)
            flex = {"type": "flex","altText": "あなたの情報","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(reply_token,messages=container_obj)
        else:
            data = up1()
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(reply_token,messages=container_obj)
        return
        '''
        data = up1()
        up[user_id] = {'user_id':user_id,'n':1,'one_text':'','text':'','y_url':'','t_url':'','s_g1':'','s_g2':'','s_m':'','s_n':''}
        flex = {"type": "flex","altText": "情報アップ","contents":data}
        container_obj = FlexSendMessage.new_from_json_dict(flex)
        line_bot_api.reply_message(msg_from,messages=container_obj)
        '''




    else:
        if user_id == set[user_id]['user_id'] and set[user_id]['n'] == 3:
            set[user_id]['n'] = 4
            set[user_id]['twitter'] = msg_text
            data = data1(set[user_id]['twitter'])
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == set[user_id]['user_id'] and set[user_id]['n'] == 5:
            set[user_id]['n'] = 6
            set[user_id]['d_n'] = msg_text
            data = data3(set[user_id]['d_n'])
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == set[user_id]['user_id'] and set[user_id]['n'] == 7:
            set[user_id]['n'] = 8
            set[user_id]['d_t'] = msg_text
            data = data7(set[user_id]['d_t'])
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == up[user_id]['user_id'] and up[user_id]['n'] == 2:
            up[user_id]['n'] = 3
            up[user_id]['one_text'] = msg_text
            data = uptest(up[user_id]['one_text'],'up2','up1')
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == up[user_id]['user_id'] and up[user_id]['n'] == 4:
            up[user_id]['n'] = 5
            up[user_id]['text'] = msg_text
            data = uptest(up[user_id]['text'],'up3','up2')
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == up[user_id]['user_id'] and up[user_id]['n'] == 6:
            up[user_id]['n'] = 7
            up[user_id]['y_url'] = msg_text
            data = uptest(up[user_id]['y_url'],'up4','up3')
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == up[user_id]['user_id'] and up[user_id]['n'] == 8:
            up[user_id]['n'] = 9
            up[user_id]['t_url'] = msg_text
            data = uptest(up[user_id]['t_url'],'up5','up4')
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == up[user_id]['user_id'] and up[user_id]['n'] == 11:
            up[user_id]['n'] = 12
            up[user_id]['s_g1'] = msg_text
            data = uptest(up[user_id]['s_g1'],'up7','up5')
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return
        if user_id == up[user_id]['user_id'] and up[user_id]['n'] == 14:
            up[user_id]['n'] = 15
            up[user_id]['s_g2'] = msg_text
            data = uptest(up[user_id]['s_g2'],'up9','up7')
            flex = {"type": "flex","altText": "確認","contents":data}
            container_obj = FlexSendMessage.new_from_json_dict(flex)
            line_bot_api.reply_message(msg_from,messages=container_obj)
            return



if __name__ == "__main__":
#    app.run()
    port =  int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
