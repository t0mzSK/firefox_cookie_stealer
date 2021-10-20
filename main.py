import os
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-j", "--json", action='store_true', help="Save cokies as a JSON file")   
args = parser.parse_args()

ROAMING = os.environ["APPDATA"]
PROFILES = "\\Mozilla\\Firefox\\Profiles"
PWD = os.getcwd()

os.chdir(ROAMING + PROFILES)

def CookiesCount():
    connection = sqlite3.connect("cookies.sqlite")
    cursor = connection.cursor()

    count_query = cursor.execute("SELECT COUNT(name) from moz_cookies").fetchall()
    cookies_count = str(count_query).replace("(", "").replace(",)", "")[1:-1]

    print(f"[+] Successfully retrieved {cookies_count} cookies from profile: {profile}")

def SaveToJSONFile(profile):
    connection = sqlite3.connect("cookies.sqlite")
    cursor = connection.cursor()

    file_name = PWD + "\\cookies_" + profile + ".json"

    f = open(file_name, "w")
    f.write("[")

    q = open(PWD + "\\query.txt", "r")
    query_from_file = q.readline()

    for name in cursor.execute(query_from_file):
        f.write(''.join(name))
    f.write("]")

    CookiesCount()
    print(f"[+] Cookies saved to: {file_name}")


for profile in os.listdir():
    try:
        os.chdir(profile)
    except Exception as e:
        print(e)

    for file in os.listdir():
        if file == "cookies.sqlite":
            try:
                os.chdir(profile)

                if args.json == True:
                    SaveToJSONFile(profile)
                else:
                    connection = sqlite3.connect("cookies.sqlite")
                    cursor = connection.cursor()
                    query = cursor.execute("SELECT name, value, host from moz_cookies")

                    print("Cookie format: Name Value Host")

                    for cookie in query.fetchall():
                        print(' '.join(cookie))

                    CookiesCount()

            except Exception as e:
                print(f"[-] Couldn't retreive cookies for profile: {profile}")
        else:
            pass

        os.chdir(ROAMING + PROFILES)

