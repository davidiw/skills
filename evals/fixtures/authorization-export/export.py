def export_readings(state, device, sink):
    account = state.account
    if not device.permission_granted():
        return "denied"
    if not state.consent_for(account):
        return "denied"
    for window in device.windows():
        readings = device.read(window)
        sink.write(account, readings)
    return "complete"
