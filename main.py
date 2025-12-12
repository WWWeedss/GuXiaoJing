from pyexpat.errors import messages

from email_warrpped.email_tool import send_email
from strategies.chuang_ye_ban_temperature_strategy import ChuangYeBanTemperatureStrategy
from strategies.qqq_valuation_strategy import QQQValuationStrategy

if __name__ == "__main__":

    import os
    from dotenv import load_dotenv
    load_dotenv()
    print("🔍 DEBUG ENV:")
    print("SENDER_EMAIL =", repr(os.getenv("SENDER_EMAIL")))
    print("SMTP =", repr(os.getenv("SMTP")))
    print("DEEPSEEK_API_KEY =", repr(os.getenv("DEEPSEEK_API_KEY")))
    print("-" * 50)

    strategies = [
        ChuangYeBanTemperatureStrategy(),
        QQQValuationStrategy(),
    ]

    messages = []
    for strategy in strategies:
        try:
            msg = strategy.get_message()
            if msg is not None:
                messages.append(msg)
        except Exception as e:
            # 可以发一条错误通知
            messages.append(f"[错误] {strategy.__class__.__name__}: {str(e)}")

    recipient = "qiuyan_gu@163.com"
    if messages:
        # 拼接所有消息
        body = "\n".join([
                             "今日触发以下提醒：",
                             "-" * 40,
                         ] + messages + ["-" * 40])

        subject = f"股小警-大盘估值提醒"
        send_email(recipient, subject, body)
    else:
        print("今日无任何策略触发，不发送邮件。")

