import os
import time
import requests
import bs4 as bs
import re
from builtins import input


def remove_last_line():
    print('\x1b[1A' +'\x1b[2K' + '\x1b[1A')

def get_page(soup,pr,po):
    soup = soup.prettify()
    with open("{}/{}/{}.html".format(pr,po,po), "w" , encoding="utf-8") as handler:
            handler.write(str(soup))

    with open("{}/{}/{}_all.txt".format(pr,po,po), "w" , encoding="utf-8") as handler:
            handler.write(str(soup))

def get_text(soup,pr,po):
    with open("{}/{}/{}_text.txt".format(pr,po,po), "w" , encoding="utf-8") as handler:
        for x in soup.find_all('p'):
            handler.write(x.get_text()+"\n")

    with open("{}/{}/{}_paragrarphs.html".format(pr,po,po), "w" , encoding="utf-8") as handler:
        for x in soup.find_all('p'):
            handler.write(str(x))

def get_img(soup,base_url,pr,po):
    img = soup.find_all("img")

    with open("{}/{}/{}_img_links.txt".format(pr,po,po), "w" , encoding="utf-8") as handler:
        for x in img:
            if x.get("src") == None:
                continue
            if x.get("src").endswith("svg"):
                continue
            if x.get("src").startswith("/"):
                handler.write(base_url+x.get("src")+"\n")
            elif x.get("src").startswith("http") == False:
                handler.write(base_url+"/"+x.get("src"))
            elif x.get("src").startswith(".."):
                handler.write(base_url+x.get("src")[2:]+"\n")
            else:
                handler.write(x.get("src")+"\n")

def download_img(soup,base_url,pr,po):
    img = soup.find_all("img")
    if img == None:
        return "No images found"

    try:
        os.mkdir("{}/{}/img".format(pr,po))
    except:
        pass

    numfix = 0
    for n,x in enumerate(img):
        if x.get("src") == None:
            continue
        if x.get("src").startswith("/"):
            req = (base_url+x.get("src"))
        elif x.get("src").startswith("http") == False:
            req = (base_url+"/"+x.get("src"))
        elif x.get("src").startswith(".."):
            req = (base_url+x.get("src")[2:])
        else:
            req = (x.get("src"))

        extension = re.findall(r".*(\.\w*$)",x.get("src"))
        if extension == []:
            numfix += 1
            continue
        else:
            extension = extension[0]
        req = requests.get(req)
        output = open("{}/{}/img/{}{}".format(pr,po,n-numfix,extension),"wb")
        output.write(req.content)
        output.close()

def get_all(soup,base_url,pr,po):
        get_page(soup,pr,po)
        get_text(soup,pr,po)
        download_img(soup,base_url,pr,po)
        get_img(soup,base_url,pr,po)

def main():
    while True:
        url = input("\nEnter website url to srcape > ")
        print("\nurl validation in progress...")
        if url.startswith("http") == False:
            url = "https://" + url
        try:
            web = requests.get(url).content
            break
        except:
            os.system('cls' if os.name in "nt" else "clear")
            print("\nInvalid url entered.")
            continue

    soup = bs.BeautifulSoup(web,"lxml")
    base_url = re.match(r"^(^https?://[^/]*)",url)[0]
    prefix = re.findall(r"^https?://([^/]*)",url)[0]
    postfix = re.findall(r"^https?://[^/].*(/.*)",url)
    if postfix == []:
        postfix = "main"
    elif postfix[0] == "/":
        postfix = "main"
    else:
        postfix = postfix[0]

    try:
        os.makedirs("{}/{}".format(prefix,postfix))
    except:
        pass

    print("\nurl valid")
    time.sleep(0.8)
    os.system('cls' if os.name in "nt" else "clear")
    print("\nWhat do you want to scrape?\n\n1. complete html\n2. paragraphs\n3. img download links\n4. download img\n5. all of the above\n\nEnter q or blank line to change url\n")

    while True:
        x = input("> ")
        if x == "1":
            get_page(soup,prefix,postfix)
            print("\nDone\nContents were saved to {}/{}/\n".format(prefix,postfix))

            time.sleep(1)
            for x in range(5):
                remove_last_line()

        elif x == "2":
            get_text(soup,prefix,postfix)
            print("\nDone\nContents were saved to {}/{}/\n".format(prefix,postfix))

            time.sleep(1)
            for x in range(5):
                remove_last_line()

        elif x == "3":
            get_img(soup,base_url,prefix,postfix)
            print("\nDone\nContents were saved to {}/{}/\n".format(prefix,postfix))

            time.sleep(1)
            for x in range(5):
                remove_last_line()

        elif x == "4":
            print("\nDownload in progress, it might take a while.")
            download_img(soup,base_url,prefix,postfix)
            print("\nDone\nContents were saved to {}/{}/img/\n".format(prefix,postfix))

            time.sleep(1)
            for x in range(7):
                remove_last_line()

        elif x == "5":
            print("\nDownload in progress, it might take a while.")
            get_all(soup,base_url,prefix,postfix)
            print("\nDone\nContents were saved to {}/{}/\n".format(prefix,postfix))

            time.sleep(1)
            for x in range(7):
                remove_last_line()

        elif x == "q" or x == "":
            os.system('cls' if os.name in "nt" else "clear")
            main()
        else:
            continue

if __name__ == '__main__':
    main()
