#!/usr/bin/env python3

import argparse
import logging
import asyncio
import time

from aiohuesyncbox import HueSyncBox, InvalidState

async def main(args):
    registration_info = None

    if args.token:
        box = HueSyncBox(args.host, args.id, access_token=args.token)
        if not await box.is_registered():
            await box.close()
            print("Token is not valid")
            return
    else:
        print("No token provided, starting registration process with huesyncbox.")
        # This is basically the "Registration" example from the readme except for the unregister step which is at the end
        box = HueSyncBox(args.host, args.id)
        print("Press the button on the box for 3 seconds until the light blinks green.")

        registration_info = None
        while not registration_info:
            try:
                registration_info = await box.register("Your application", "Your device")
                time.sleep(1)
            except InvalidState:
                # Indicates the button was not pressed
                pass

        # Save registration_info somewhere and use the 'access_token' when instantiating HueSyncBox next time
        print(registration_info)

    # This part is the "Basic usage" example in the readme
    await box.initialize()
    print(box.device.name)
    print(box.execution.sync_active)
    print(box.execution.mode)
    print(box.execution.hdmi_source)

    # Turn the box on (assuming it was off), start syncing on input 3
    await box.execution.set_state(sync_active=True, mode="video", hdmi_source="input3")

    # Call update() to update with latest status of the box
    await box.execution.update()
    print(box.execution.sync_active)
    print(box.execution.mode)
    print(box.execution.hdmi_source)

    # Cleanup in case the registration was done this run
    if registration_info:
        # Unregister by registration ID. HueSyncBox needs to have a valid accessToken to execute this request
        await box.unregister(registration_info['registration_id'])

    await box.close()

if __name__ == '__main__':

    ## Commandlineoptions
    parser = argparse.ArgumentParser(description='Example application for aiohuesyncbox.')

    parser.add_argument( 'host',
                         help='Hostname or IP Address of the syncbox' )
    parser.add_argument( 'id',
                         help='ID of the syncbox' )
    parser.add_argument( '--token',
                         help='Token for the  hue syncbox')

    parser.add_argument( '--loglevel',
                         choices= ['DEBUG', 'INFO','WARNING','ERROR','CRITICAL'],
                         default='INFO',
                         help='Define loglevel, default is INFO.' )

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))

    loop.close()
