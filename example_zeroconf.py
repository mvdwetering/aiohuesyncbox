#!/usr/bin/env python3

from zeroconf import ServiceBrowser, Zeroconf


class MyListener:
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_huesync._tcp.local.", listener)

try:
    print("Searching for Philips Hue Play HDMI Sync Boxes")
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
