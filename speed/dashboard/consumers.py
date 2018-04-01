import json
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http

@channel_session_user_from_http
def ws_connect(message):

	group = message.user.username
	print(group)

	message.reply_channel.send({
		'accept': True
	})

	Group(group).add(message.reply_channel)
	message.channel_session['parent-group'] = group


@channel_session_user
def ws_receive(message):
	return

@channel_session_user
def ws_disconnect(message):
	user_group = message.channel_session['parent-group']
	Group(user_group).discard(message.reply_channel)