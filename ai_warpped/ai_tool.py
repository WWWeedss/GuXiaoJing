from crawler_wrapped.crawler_tool import fetch_url_markdown


def get_response (question : str) -> str:
    import os
    from openai import OpenAI

    client = OpenAI(
        api_key=os.getenv('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

    messages = [
        {"role": "system", "content": "你是一个精通结构化文本分析的助手，擅长从文本中提取关键信息并进行总结。"},
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    content = fetch_url_markdown("https://youzhiyouxing.cn/data/indices/399006.SZ")
    question = ("请帮我从以下文本中提取创业板的今日温度，仅仅返回数字部分，不要任何其他文字，文本内容如下:"
                f"\n\n{content}\n\n")
    answer = int(get_response(question))
    if answer < 50 :
        print("创业板温度正常")
    else :
        print("创业板温度过高，请注意风险")

