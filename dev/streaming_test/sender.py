from vidstream import ScreenShareClient

sender = ScreenShareClient("192.168.1.111", 4424)

sender.start_stream()