from collections import deque
import time
from smbus2 import SMBus

I2C_BUS = 1
MAX30100_ADDR = 0x57

REG_INT_STATUS = 0x00
REG_INT_ENABLE = 0x01
REG_FIFO_WR_PTR = 0x02
REG_FIFO_OVF_COUNTER = 0x03
REG_FIFO_RD_PTR = 0x04
REG_FIFO_DATA = 0x05
REG_MODE_CONFIG = 0x06
REG_SPO2_CONFIG = 0x07
REG_LED_CONFIG = 0x09
REG_PART_ID = 0xFF

MODE_HR_ONLY = 0x02
MODE_SPO2 = 0x03
MODE_RESET = 0x40


class MAX30100HeartRate:

  def __init__(self, bus_num=I2C_BUS, address=MAX30100_ADDR):
    self.bus = SMBus(bus_num)
    self.address = address

  def reset(self):
    self.bus.write_byte_data(self.address, REG_MODE_CONFIG, MODE_RESET)
    time.sleep(0.05)

  def init_sensor(self, mode=MODE_SPO2, ir_current=0x24, red_current=0x24):
    self.reset()

    self.bus.write_byte_data(self.address, REG_INT_ENABLE, 0x00)

    self.bus.write_byte_data(self.address, REG_FIFO_WR_PTR, 0x00)
    self.bus.write_byte_data(self.address, REG_FIFO_OVF_COUNTER, 0x00)
    self.bus.write_byte_data(self.address, REG_FIFO_RD_PTR, 0x00)

    led_cfg = ((red_current & 0x0F) << 4) | (ir_current & 0x0F)
    self.bus.write_byte_data(self.address, REG_LED_CONFIG, led_cfg)

    self.bus.write_byte_data(self.address, REG_SPO2_CONFIG, 0x47)

    self.bus.write_byte_data(self.address, REG_MODE_CONFIG, mode)

  def read_fifo(self):
    wr_ptr = self.bus.read_byte_data(self.address, REG_FIFO_WR_PTR) & 0x0F
    rd_ptr = self.bus.read_byte_data(self.address, REG_FIFO_RD_PTR) & 0x0F

    num_samples = (wr_ptr - rd_ptr) & 0x0F
    samples = []

    for _ in range(num_samples):
      raw = self.bus.read_i2c_block_data(self.address, REG_FIFO_DATA, 4)
      ir = (raw[0] << 8) | raw[1]
      red = (raw[2] << 8) | raw[3]
      samples.append((ir, red))

    return samples

  def close(self):
    self.bus.close()


class SimpleBPMDetector:

  def __init__(self, window_size=50):
    self.ir_history = deque(maxlen=window_size)
    self.last_beat_time = None
    self.bpm = None

  def update(self, ir_value):
    if ir_value < 5000:
      self.ir_history.clear()
      self.bpm = None
      return None

    self.ir_history.append(ir_value)
    if len(self.ir_history) < 10:
      return self.bpm

    avg_ir = sum(self.ir_history) / len(self.ir_history)
    now = time.monotonic()
    if ir_value > avg_ir * 1.003:
      if self.last_beat_time is None or (now - self.last_beat_time) > 0.45:
        if self.last_beat_time is not None:
          ib_interval = now - self.last_beat_time
          candidate_bpm = 60.0 / ib_interval
          if 40 <= candidate_bpm <= 200:
            self.bpm = round(candidate_bpm, 1)
        self.last_beat_time = now

    return self.bpm


def main():
  sensor = MAX30100HeartRate()
  detector = SimpleBPMDetector(window_size=60)

  try:
    part_id = sensor.bus.read_byte_data(MAX30100_ADDR, REG_PART_ID)
    print(f"Povezan sa MAX30100 (Part ID: 0x{part_id:02X})")
    sensor.init_sensor(mode=MODE_SPO2, ir_current=0x24, red_current=0x24)
    print("Stavi prst lagano na senzor (bez jakog pritiska)...\n")

    while True:
      samples = sensor.read_fifo()
      for ir, red in samples:
        bpm = detector.update(ir)
        finger_present = ir >= 5000
        status = f"BPM: {bpm}" if (finger_present and bpm) else "Merim..."
        if not finger_present:
          status = "Nema prsta na senzoru"

        print(f"IR: {ir:6d} | RED: {red:6d} | {status}")

      time.sleep(0.02)  

  except KeyboardInterrupt:
    print("\nZaustavljeno očitavanje.")
  finally:
    sensor.close()


if __name__ == "__main__":
  main()