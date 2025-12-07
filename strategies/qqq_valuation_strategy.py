import requests

from strategies.base_strategy import BaseStrategy


class QQQValuationStrategy(BaseStrategy):
    def get_message(self):
        qqq_valuation = self.get_qqq_valuation()
        valuation_to_alert = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        if qqq_valuation is not None and int(qqq_valuation) in valuation_to_alert:
            return self.build_message(qqq_valuation)
        return None

    def get_qqq_valuation(self):
        url = "https://danjuanfunds.com/djapi/index_eva/detail/NDX"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 如果状态码不是 2xx，会抛出异常

            data = response.json()

            # 提取 pe_over_history
            pe_over_history = data["data"]["pe_over_history"]
            # 将形如 0.1206 转换为 88.00
            rounded_pe = round(pe_over_history, 2)
            return 100 - 100 * rounded_pe
        except requests.exceptions.RequestException as e:
            print("请求失败:", e)
        except KeyError as e:
            print("字段缺失:", e)

    def build_message(self, valuation: float) -> str:
        return f"QQQ 当前 PE 超过历史上 %{valuation:.2f} 的时刻，请注意加减仓。"

if __name__ == "__main__":
    strategy = QQQValuationStrategy()
    print(strategy.get_message())