import yfinance as yf
import requests
import os
from datetime import datetime


# =====================
# Telegram配置
# =====================

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


# =====================
# 获取股票数据
# =====================

def get_change(code):

    data = yf.download(
        code,
        period="5d",
        progress=False,
        auto_adjust=False
    )


    close = data["Close"]


    # 兼容新版yfinance多层数据
    if hasattr(close, "columns"):

        close = close.iloc[:,0]


    if len(close) < 2:

        return 0


    last = float(close.iloc[-1])

    prev = float(close.iloc[-2])


    change = (last / prev - 1) * 100


    return round(change,2)



# =====================
# 获取市场数据
# =====================

nvda = get_change("NVDA")
msft = get_change("MSFT")
aapl = get_change("AAPL")
qqq = get_change("QQQ")


# =====================
# 简单量化评分
# =====================

score = 50


if qqq > 0:
    score += 15

if nvda > 0:
    score += 15

if msft > 0:
    score += 10

if aapl > 0:
    score += 5


if score > 85:
    trend="强烈看涨"

elif score > 65:
    trend="偏多"

elif score > 45:
    trend="震荡"

else:
    trend="偏空"



# =====================
# 生成报告
# =====================

report = f"""

📊159509 纳指ETF AI晨报

日期:
{datetime.now().strftime("%Y-%m-%d")}


美股核心:

QQQ:
{qqq}%


NVDA:
{nvda}%


MSFT:
{msft}%


AAPL:
{aapl}%


-----------------

市场评分:

{score}/100


今日方向:

{trend}


未来判断:

根据科技股表现、
纳指趋势、
市场风险偏好综合判断。


注意：
此为量化模型分析，
不是投资建议。


"""


# =====================
# 推送Telegram
# =====================

url = (
f"https://api.telegram.org/"
f"bot{TOKEN}/sendMessage"
)


requests.post(
    url,
    data={
        "chat_id":CHAT_ID,
        "text":report
    }
)


print(report)
