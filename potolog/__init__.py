import os
from flask import Flask, render_template, request, url_for

def print_settings(config):
    print('========================================================')
    print('SETTINGS for PHOTOLOG APPLICATION')
    print('========================================================')
    for key, value in config:
        print('%s=%s' % (key, value))
    print('========================================================')