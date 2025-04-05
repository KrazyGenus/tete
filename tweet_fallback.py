#!/usr/bin/env python3
import socket
"""This module exist as a fallback when the the send_tweet fails to send a tweet due to a lack of internet access"""
"""This is meant to negate it and fix it when it can or when the internet connection is back on..."""


def network_status():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=7)
        return True
    except OSError:
        return False
if network_status():
    print("Man's plugged")
else:
    print("Man slacking!")

def peform_fallback():
    pass