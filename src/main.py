import threading
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from conf import conf


class Core:
    def __init__(self):
        self.buffer = []
        self.send_error = False
        self.auth = HTTPBasicAuth(conf.login, conf.password)

    def send_logs(self, msg: str, e: Exception | None = None) -> None:
        conf.logger.send_log(
            url=conf.url, location_name=conf.location_name, auth=self.auth,
            error_message=msg, e=e
        )

    @staticmethod
    def save_temp(weights: list[dict]) -> None:
        for data in weights:
            conf.db.add_temp(datetime.fromisoformat(data['date']), data['weight'])

    def send_weights(self, buffer: list[dict]) -> None:
        try:
            temp_data = []
            if self.send_error:
                if self.ping():
                    self.send_error = False
                    temp_data = [{"date": temp.date.isoformat(), "weight": temp.weight} for temp in conf.db.get_temp()]

            if not buffer and not temp_data:
                return

            try:
                response = requests.post(
                    conf.url,
                    auth=self.auth,
                    json={"location_name": conf.location_name, "ok": True, "results": temp_data + buffer},
                    timeout=(10, 30)
                )
                if response.status_code != 200:
                    raise Exception(f"Request failed with status code {response.status_code}")

                elif temp_data:
                    conf.db.clear_temp()

            except Exception as e:
                self.send_error = True
                self.save_temp(buffer)
                conf.logger.write_log("Request error", e=e)

        except Exception as e:
            conf.logger.write_log(f"Error sending consumption", e=e)

    def ping(self) -> bool:
        try:
            response = requests.post(
                conf.url,
                auth=self.auth,
                json={"location_name": conf.location_name, "ok": True, "results": []},
                timeout=(10, 30)
            )
            if response.status_code == 200:
                return True

            else:
                return False

        except Exception as _:  # noqa
            return False

    def run(self) -> None:
        send_time = datetime.now()

        for data in conf.meter.get_data():
            if isinstance(data, Exception):
                threading.Thread(target=self.send_logs, args=["Error get data from scales"], kwargs={"e": data}).start()

            else:
                now = datetime.now().isoformat()
                for weight in data:
                    weight = int(weight[0:-1])
                    if weight > conf.minimal_weight:
                        self.buffer.append({"date": now, "weight": weight})

                if (datetime.now() - send_time).seconds >= conf.send_interval:
                    send_time = datetime.now()
                    threading.Thread(target=self.send_weights, args=[self.buffer]).start()
                    self.buffer = []


if __name__ == '__main__':
    sender = Core()
    sender.run()
