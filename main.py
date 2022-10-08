# -*- coding: UTF-8 -*-
import requests
import time
import sys
import base64
import http.cookiejar as cookielib
import ddddocr
from urllib.parse import urlparse, parse_qs
#以下为需手动配置的信息
openid = "" #微信openid
username = "" #工软校园用户名
password = "" #工软校园密码（默认同用户名）
schoolname = "hebgydxwh"#学校名称，自己人不用改（哈威之光）
submitted_form = [      #要喂给平台啥信息，如果表格内容更新这个也要跟着更新否则会产生严重后果。
  {
    "value": [
      "c002"            #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "校内",
        "column": "c001"
      },
      {
        "content": "校外",
        "column": "c002"
      }
    ]
  },
  {
    "value": "",
    "zjlx": 5,
    "list": [
      {
        "content": "山东省",#有需要改这里
        "column": "gSheng"
      },
      {
        "content": "威海市",#有需要改这里
        "column": "gShi"
      },
      {
        "content": "环翠区",#有需要改这里
        "column": "gQu"
      }
    ]
  },
  {
    "value": [
      "c010"              #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "37.2℃及以下",
        "column": "c010"
      },
      {
        "content": "37.3℃-38.4℃（请及时就医并在3天内进行3次核酸检测）",
        "column": "c012"
      },
      {
        "content": "38.5℃及以上（请及时就医并在3天内进行3次核酸检测）",
        "column": "c013"
      }
    ]
  },
  {
    "value": [
      "c014"              #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "没有出现不适症状",
        "column": "c014"
      },
      {
        "content": "乏力、咳嗽、流涕等感冒症状",
        "column": "c015"
      },
      {
        "content": "呕吐、腹泻等消化道不适",
        "column": "c016"
      },
      {
        "content": "与传染病无关的不适症状",
        "column": "c017"
      }
    ]
  },
  {
    "value": [
      "c018"              #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "未被隔离",
        "column": "c018"
      },
      {
        "content": "居家隔离观察（需要医护人员上门核酸采样）",
        "column": "c019"
      },
      {
        "content": "校外集中隔离点隔离观察",
        "column": "c020"
      }
    ]
  },
  {
    "value": [
      "c006"              #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "未接种",
        "column": "c003"
      },
      {
        "content": "已接种第一针",
        "column": "c004"
      },
      {
        "content": "已接种第二针",
        "column": "c005"
      },
      {
        "content": "已接种第三针",
        "column": "c006"
      }
    ]
  },
  {
    "value": [
      "c007"              #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "绿码",
        "column": "c007"
      },
      {
        "content": "灰码（请在到威海后第1、第2、第4天各完成1次核酸检测）",
        "column": "c008"
      },
      {
        "content": "黄码",
        "column": "c009"
      },
      {
        "content": "红码",
        "column": "c010"
      }
    ]
  },
  {
    "value": [
      "c030"              #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "未出校",
        "column": "c028"
      },
      {
        "content": "出校，未离开威海（须填报出行方式和外出地点）",
        "column": "c029"
      },
      {
        "content": "离威",
        "column": "c030"
      }
    ]
  },
  {
    "value": "",
    "zjlx": 2,
    "list": [
      {
        "content": "",
        "column": "c031"
      }
    ]
  },
  {
    "value": [
      "c022"              #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "是",
        "column": "c021"
      },
      {
        "content": "否",
        "column": "c022"
      }
    ]
  },
  {
    "value": "",
    "zjlx": 1,
    "list": [
      {
        "content": "",
        "column": "c023"
      }
    ]
  },
  {
    "value": [
      "c025"              #有需要改这里
    ],
    "zjlx": 3,
    "list": [
      {
        "content": "是",
        "column": "c024"
      },
      {
        "content": "否",
        "column": "c025"
      }
    ]
  },
  {
    "value": "",
    "zjlx": 1,
    "list": [
      {
        "content": "",
        "column": "c026"
      }
    ]
  },
  {
    "value": "",
    "zjlx": 2,
    "list": [
      {
        "content": "",
        "column": "c027"
      }
    ]
  }
]
#以上为需要手动配置的信息
requests.packages.urllib3.disable_warnings()
mysession = requests.session()
mysession.cookies = cookielib.MozillaCookieJar(filename = "jktb_cookies.txt")
def getverifycode():
    url = "http://xy.4009955.com/sfrzwx/wxsq/getYzm"

    headers = {
        "Origin": "http://xy.4009955.com",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001031) NetType/WIFI Language/zh_CN",
        "Connection": "keep-alive",
        "Referer": f"http://xy.4009955.com/sfrzwx/auth/login?openid={openid}&dlfs=zhmm",
        "Host": "xy.4009955.com",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Content-Length": "0"
    }
    try:
        response = mysession.post(url, headers=headers, verify=False, timeout=5)
        if response.status_code == 200:
            body = response.json()
            mysession.cookies.save()
            return body["data"]["content"]
        return ""
    except:
        return ""


def passInfo():
    url = "http://xy.4009955.com/sfrzwx/wx/login"
    headers = {
        "Origin": "http://xy.4009955.com",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001031) NetType/WIFI Language/zh_CN",
        "Referer": f"http://xy.4009955.com/sfrzwx/auth/login?openid={openid}&dlfs=zhmm",
        "Connection": "keep-alive",
        "Host": "xy.4009955.com",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Content-Length": "134",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    yzmcode = getverifycode().split(",", 1)
    yzmbytes = base64.standard_b64decode(yzmcode[1])
    ocr = ddddocr.DdddOcr()
    yzmanswer = ocr.classification(yzmbytes)
    print("验证码识别为",yzmanswer)
    data = f"dlfs=zhmm&openid={openid}&sjschool=&sjh=&yzm=&zhschool={schoolname}&username={username}&password={password}&code={yzmanswer}"
    response = mysession.post(url, data=data, headers=headers, verify=False, timeout=5, allow_redirects=False)
    mysession.cookies.save()
    return response.headers["Location"]

def getlogincode():
    url = "http://xy.4009955.com/sfrzwx/oauth/authorize?response_type=code&scope=read&client_id=jktb&redirect_uri=http://xy.4009955.com/jktb/&state=tysfrz"
    headers = {
        "Origin": "http://xy.4009955.com",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001031) NetType/WIFI Language/zh_CN",
        "Connection": "keep-alive",
        "Referer": f"http://xy.4009955.com/sfrzwx/auth/login?openid={openid}&dlfs=zhmm",
        "Host": "xy.4009955.com",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Upgrade-Insecure-Requests": "1"
    }
    response = mysession.get(url, headers=headers, verify=False, timeout=5, allow_redirects=False)
    mysession.cookies.save()
    return response.headers["Location"]

if __name__ == "__main__":
    #passInfo()
    print("欢迎使用全自动健康填报，请在程序开头配置相关信息")
    mysession.cookies.save()
    mysession.cookies.load()
    parsed = urlparse(passInfo())
    while parsed.path == "/sfrzwx/auth/login":
      print("登录失败，可能为验证码识别错误，3秒后重试")
      time.sleep(3)
      parsed = urlparse(passInfo())
    backurl=getlogincode()
    parsed = urlparse(backurl)
    auth_code=parse_qs(parsed.query).get('code')[0]
    print(auth_code)
    headers = {
        "Origin": "http://xy.4009955.com",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001031) NetType/WIFI Language/zh_CN",
        "Referer": backurl,
        "Connection": "keep-alive",
        "token": "",
        "Host": "xy.4009955.com",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/json"
    }
    url = "http://xy.4009955.com/jktb-api/jktb_01_01/login/loginYdBycode"
    data={
      "code": auth_code
    }
    response = mysession.post(url, json=data, headers=headers, verify=False, timeout=5, allow_redirects=False)
    #print(response.status_code,response.headers)
    body=response.json()
    token=body["data"]["content"]["token"]
    realname=body["data"]["content"]["xm"]
    url = "http://xy.4009955.com/jktb-api/jktb_01_01/homePage/getToadyForms"
    headers = {
        "Origin": "http://xy.4009955.com",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001031) NetType/WIFI Language/zh_CN",
        "Referer": "http://xy.4009955.com/jktb/",
        "Connection": "keep-alive",
        "token": token,
        "Host": "xy.4009955.com",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2"
    }
    response = mysession.post(url, headers=headers, verify=False, timeout=5, allow_redirects=False)
    body=response.json()
    formid=body["data"]["content"][0]["bdtbslid"]
    url = "http://xy.4009955.com/jktb-api/jktb_01_01/homePage/getFormDetail"
    data = {"bdtbslid": formid}
    response = mysession.post(url, json=data, headers=headers, verify=False, timeout=5, allow_redirects=False)
    body=response.json()
    index=0
    for item in body["data"]["content"]["list"]:
      subindex=0
      for subitem in item["list"]:
        if subitem["column"] != submitted_form[index]["list"][subindex]["column"]:
          with open('jktb_error.txt', 'w') as errf:
            errf.write("表格校验失败，程序中止，表单需要更新")
          print("表格校验失败，程序中止，表单需要更新")
          quit()
        subindex = subindex + 1
      index = index + 1
    url = "http://xy.4009955.com/jktb-api/jktb_01_01/homePage/saveForm"
    data={
          "isEdit": 1,
          "syxgcs": 3,
          "zzjgmc": body["data"]["content"]["zzjgmc"],
          "bdtbslid": formid,
          "bdmc": "学生每日健康填报",
          "tbzt": 0,
          "xm": realname,
          "list": submitted_form,
      "tbrq": time.strftime('%Y-%m-%d',time.localtime(time.time())),
      "mrtbjzsj": "22:10"
    }
    response = mysession.post(url, json=data, headers=headers, verify=False, timeout=5, allow_redirects=False)
    mysession.cookies.save()
    if response.status_code == 200:
      print("填报完成")
