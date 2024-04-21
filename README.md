# AIOHUESYNCBOX

Asyncio package to communicate with Philips Hue Play HDMI Sync Box.
This package is aimed at basic control of the box. Initial setup and configuration is assumed to done with the official Hue app.


## Installation

```bash
    python3 -m pip install aiohuesyncbox
```

## Usage

Instantiate the HueSyncBox class and access the API.

For more details on the API see the official API documentation on https://developers.meethue.com

### Note on changing bridge

Changing a bridge is a bit more involved than other calls.
After calling `box.hue.set_bridge()` the syncbox will start switching which takes a while (seems to take about 15 seconds).
You will have to wait until the attributes match the expected endstate, but the status displayed on the API can be a bit confusing during the process.

These are the status changes I see when switching from bridge A to bridge B.

* ID: Bridge A, IP: Bridge A, Status: connected
* Call `box.hue.set_bridge()` with info for bridge B
* ID: Bridge B, IP: Bridge A, Status: connecting
* ID: Bridge B, IP: Bridge B, Status: disconnected
* ID: Bridge B, IP: Bridge B, Status: connected or ID: Bridge B, IP: Bridge B, Status: invalidgroup


## Examples

The examples below are available as a runnable script in the repository.
There is also an example on using `zeroconf` for device discovery.

### Registration

```python
    from aiohuesyncbox import HueSyncBox, InvalidState

    # host and id can be obtained through mDNS/zeroconf discovery
    # (or for testing look them up in the official Hue app)
    # The ID is the number that looks like C43212345678
    box = HueSyncBox(host, id)

    print("Press the button on the box for a few seconds until the light blinks green.")

    registration_info = None
    while not registration_info:
        try:
            registration_info = await box.register("Your application", "Your device")
        except InvalidState:
            # Indicates the button was not pressed
            pass
        await asyncio.sleep(1)

    # Save registration_info somewhere and use the 'access_token' when instantiating HueSyncBox next time
    print(registration_info)

    # Unregister by registration ID.
    # HueSyncBox needs to use the associated `access_token` to execute this request.
    await box.unregister(registration_info['registration_id'])
```

### Basic usage

```python

    from aiohuesyncbox import HueSyncBox

    # host and id can be obtained through mDNS/zeroconf discovery
    # (or for testing look them up in the official Hue app)
    box = HueSyncBox(host, id, access_token_from_registration_info)

    # Call initialize before interacting with the box
    await box.initialize()
    print(box.device.name)
    print(box.execution.sync_active)
    print(box.execution.mode)

    # Turn the box on, start syncing with video mode on input 4
    await box.execution.set_state(sync_active=True, mode="video", hdmi_source="input4")

    # Call update() to update with latest status from the box
    await box.execution.update()
    print(box.execution.sync_active)
    print(box.execution.mode)
```
