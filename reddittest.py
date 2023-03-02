import praw
import random
import webbrowser
import sys
import socket
import configparser

config = configparser.ConfigParser()
config.read("modmail.ini")

def receive_connection():
    """
    Wait for and then return a connected socket..
    Opens a TCP connection on port 8080, and waits for a single client.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client


def send_message(client, message):
    """
    Send message to client and close the connection.
    """
    client.send('HTTP/1.1 200 OK\r\n\r\n{}'.format(message).encode('utf-8'))
    client.close()


def main():
    reddit = praw.Reddit(
        client_id=config.get("reddit", "client_id"),
        client_secret=config.get("reddit", "client_secret"),
        username=config.get("reddit", "username"),
        user_agent=config.get("reddit", "user_agent"),
        password=config.get("reddit", "password"),
        redirect_uri='http://localhost:8080',
    )

    try:
        reddit.user.me()
    except Exception as err:
        if (str(err) != 'invalid_grant error processing request'):
            print('LOGIN FAILURE')
        else:
            state = str(random.randint(0, 65000))
            scopes = ['*']
            url = reddit.auth.url(scopes, state, 'permanent')
            print('We will now open a window in your browser to complete the login process to reddit.')
            webbrowser.open(url)

            client = receive_connection()
            data = client.recv(1024).decode('utf-8')
            param_tokens = data.split(' ', 2)[1].split('?', 1)[1].split('&')
            params = {key: value for (key, value) in [token.split('=')
                                                    for token in param_tokens]}

            if state != params['state']:
                send_message(client, 'State mismatch. Expected: {} Received: {}'
                            .format(state, params['state']))
                return 1
            elif 'error' in params:
                send_message(client, params['error'])
                return 1

            refresh_token = reddit.auth.authorize(params["code"])
            send_message(client, "Refresh token: {}".format(refresh_token))

            print(refresh_token)
            return 0

if __name__ == "__main__":
    sys.exit(main())