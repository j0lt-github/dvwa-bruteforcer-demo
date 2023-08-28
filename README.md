# DVWA Login Brute-Forcer Demo
This script demonstrates how a brute-force attack can be performed against the login page of the Damn Vulnerable Web Application (DVWA), specifically targeting its actual login page and not the brute-force challenge.

## Usage


```
python main.py --url [DVWA URL] --usernamelist [USERLIST PATH] --passwordlist [PASSLIST PATH] --output [OUTPUT FILE PATH]
```

###Arguments:

1. `--url / -u`: The base URL of DVWA (e.g., `http://localhost/DVWA/login.php`).
2. `--usernamelist / -ul`: Path to the file containing usernames to be tested.
3. `--passwordlist / -pl`: Path to the file containing passwords to be tested.
4. `--output / -o` (optional): Path to the output file where valid credentials will be saved.


## Disclaimer:

This script is meant for educational and demonstration purposes only. Always use it in an environment where you have permission. Unauthorized access to computer systems is illegal and could result in severe penalties.

