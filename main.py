from pyexpat.errors import messages

from email_warrpped.email_tool import send_email
from strategies.chuang_ye_ban_temperature_strategy import ChuangYeBanTemperatureStrategy

if __name__ == "__main__":
    strategies = [
        ChuangYeBanTemperatureStrategy(),
    ]

    messages = []
    for strategy in strategies:
        try:
            msg = strategy.get_message()
            if msg is not None:
                messages.append(msg)
        except Exception as e:
            # 可选：也可以发一条错误通知
            messages.append(f"[错误] {strategy.__class__.__name__}: {str(e)}")

    recipient = "qiuyan_gu@163.com"
    if messages:
        # 拼接所有消息
        body = "\n".join([
                             "今日触发以下提醒：",
                             "-" * 40,
                         ] + messages + ["-" * 40])

        subject = f"股小警-大盘估值提醒)"
        send_email(recipient, subject, body)
    else:
        print("今日无任何策略触发，不发送邮件。")

