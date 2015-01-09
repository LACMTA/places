# Setup SendGrid email  =======================================================
# using SendGrid's Python Library - https://github.com/sendgrid/sendgrid-python

def send_email(subject='Test email', from_email='goodwind@metro.net', from_name='D. Goodwin', recipients=['dgoodwin@gmail.com'], text_body='Hello from Flask', html_body='Hello from <b>Flask</b>'):
	from sendgrid import SendGridClient, Mail
	api_key = 'm3tr0pl4c3s'
	api_user = 'metroplaces'
	sendgrid = SendGridClient(username=api_user, password=api_key, 
		raise_errors=True,
		host='http://api.sendgrid.com',
		port=80,
		)

	message = Mail()
	message.add_to(recipients)
	message.set_from(from_email)
	message.set_from_name(from_name)
	message.set_subject(subject)
	message.set_text(text_body)
	message.set_html(html_body)

	try:
		sendgrid.send(message)
	except Exception as e:
		print "fail: %s" %(e)

