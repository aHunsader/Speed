import os
import channels.asgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'speed.settings')
channel_layer = channels.asgi.get_channel_layer()