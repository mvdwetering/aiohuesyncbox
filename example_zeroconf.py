#!/usr/bin/env python3

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf


class MyListener(ServiceListener):
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"\nService {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"\nService {name} added")

        if info := zc.get_service_info(type_, name):
            print(f" - IP addresses: {info.parsed_addresses()}")
            print(f" - Raw service info: {info}")


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_huesync._tcp.local.", listener)

try:
    print("Searching for Philips Hue Play HDMI Sync Boxes")
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
