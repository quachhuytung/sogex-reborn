def handle_log_cookie(*args, **kwargs):
    with open('cookie.txt', 'w') as f:
        f.write(kwargs['cookies'])
