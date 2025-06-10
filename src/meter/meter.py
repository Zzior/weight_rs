import serial


class WeightReader:
    def __init__(
            self, port: str = "/dev/ttyUSB0", baudrate: int = 9600, timeout=1
    ):
        self.client = serial.Serial(
            port=port,                       # Specify the serial port
            baudrate=baudrate,               # Data Baud rate
            timeout=timeout,                 # Timeout connection
            bytesize=serial.EIGHTBITS,       # Bytesize
            parity=serial.PARITY_NONE,       # Parity
            stopbits=serial.STOPBITS_ONE,    # Stop bits
        )
        self.buffer = b""

    def get_data(self) -> list[str] | Exception:
        try:
            while True:
                if self.client.in_waiting:
                    self.buffer += self.client.read(self.client.in_waiting)
                    yield self.decode_buffer()

        except Exception as e:
            yield e

        finally:
            self.client.close()

    def decode_buffer(self) -> list[str] | Exception:
        frames = []
        while True:
            start = self.buffer.find(b'\x02')
            end = self.buffer.find(b'\x03', start)

            if start != -1 and end != -1 and end > start:
                frame = self.buffer[start + 1:end]
                frames.append(frame.decode('ascii').strip())

                self.buffer = self.buffer[end + 1:]
            else:
                break

        return frames


if __name__ == "__main__":

    weights = WeightReader()
    for data in weights.get_data():
        print(*data, sep="\n")
