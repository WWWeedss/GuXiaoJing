from ai_warpped.ai_tool import get_response
from crawler_wrapped.crawler_tool import fetch_url_markdown
from strategies.base_strategy import BaseStrategy


class ChuangYeBanTemperatureStrategy(BaseStrategy):
    def get_message(self):
        # 创业板温度消息逻辑
        url_content = fetch_url_markdown("https://youzhiyouxing.cn/data/indices/399006.SZ")
        question = ("请帮我从以下文本中提取创业板的今日温度，仅仅返回数字部分，不要任何其他文字，文本内容如下:"
                    f"\n\n{url_content}\n\n")
        temperature = int(get_response(question))

        temperatures_to_alert = [10, 20, 30, 50, 57, 60, 70, 80, 90]
        if temperature in temperatures_to_alert:
            return self.build_message(temperature)
        return None

    def build_message(self, temperature: int) -> str:
        return f"创业板昨日收盘后温度为 {temperature}，请注意加减仓。"


if __name__ == "__main__":
    strategy = ChuangYeBanTemperatureStrategy()
    message = strategy.get_message()
    if message:
        print(message)
    else:
        print("今日无创业板温度预警消息。")
