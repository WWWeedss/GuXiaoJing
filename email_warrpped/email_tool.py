def send_email(recipient: str, subject: str, body: str) -> None:
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SMTP")

    if not sender_email or not sender_password:
        raise ValueError("请在环境变量中设置 SENDER_EMAIL 和 SMTP")

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = Header(sender_email)
    msg['To'] = Header(recipient)
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP_SSL('smtp.163.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [recipient], msg.as_string())
        server.quit()
        print(f"邮件已成功发送至 {recipient}")
    except Exception as e:
        print(f"发送邮件时出错: {e}")
        raise

if __name__ == "__main__":
    email_body = """
    【每日市场温度提醒 - 2025/12/06】

    📈 创业板指：
    - 指数点位：3109
    - 温度：57°（适中）

    🌍 纳斯达克估值：
    - PE：34.2
    - 状态：略高估

    规则判断：当前无触发阈值，无需操作。
        """

    send_email(
        recipient="qiuyan_gu@163.com",
        subject="股小警-大盘估值提醒",
        body=email_body
    )
