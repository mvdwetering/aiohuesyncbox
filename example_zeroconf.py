#!/usr/bin/env python3

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf


class MyListener(ServiceListener):
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print("Service %s removed" % (name,))

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print("Service %s added, service info: %s" % (name, info))


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_huesync._tcp.local.", listener)

try:
    print("Searching for Philips Hue Play HDMI Sync Boxes")
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
