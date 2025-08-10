from playwright.sync_api import sync_playwright
import time
import os
import zipfile
from flask import Flask, redirect, url_for, request, send_file

pe = os.path.abspath('./hakoton/Violentmonkey')

password = ''
username = ''
email = ''
def pw(u,e,p):
    username = u
    email = e
    password = p
    def run(playwright):
        browser = playwright.chromium.launch_persistent_context(
            user_data_dir='./chromium',
            args=[
                f"--disable-extensions-except={pe}",
                f"--load-extension={pe}",
                "--allow-file-access-from-files"
            ],
            headless=False)
        page = browser.new_page()
        page.goto('https://x.com/i/flow/login')
    
        #login 
        page.fill('input[type="text"]', username)  
        buttons = page.locator('button.css-175oi2r')
        buttons.nth(2).click()
        time.sleep(1)
        if(page.get_by_text("There was unusual login activity on your account. To help keep your account safe, please enter your phone number (start with country code, e.g. +1) or email address to verify it’s you.").is_visible()):
            page.fill('input[type="text"]', email)
            buttons.nth(2).click()

        page.fill('input[type="password"]', password)

        buttons = page.locator('button.css-175oi2r')
        buttons.nth(2).click()
        
        page.locator('a[href="/'+username+'"]').nth(1).click()
        time.sleep(2)


        #tweets by User
        twets = page.locator("article.css-175oi2r")
        for t in twets.all():
            t.click()
            time.sleep(1)
            page.go_back()
        page.locator("div[data-theme='system']").click()
        page.locator("button.p-0").nth(6).click()
        page.locator("button.btn-primary").click()
        page.locator('select.w-32').select_option('HTML')
        
        with page.expect_download() as download_info:
            page.get_by_text('Start Export').click()
        download = download_info.value
        download.save_as(path = "./"+username+"/tweets.html")

        for i in range(3,0,-1): page.locator('div.w-9').nth(i).click()


        #following
        page.goto(page.url+"/following")
        time.sleep(2)
        page.locator("div[data-theme='system']").click()
        page.locator("button.p-0").nth(1).click()
        page.locator("button.btn-primary").click()
        page.locator('select.w-32').select_option('HTML')
        
        with page.expect_download() as download_info:
            page.get_by_text('Start Export').click()
        download = download_info.value
        download.save_as(path = "./"+username+"/following.html")
        for i in range(3,0,-1): page.locator('div.w-9').nth(i).click()
        page.locator('a[href="/'+username+'"]').nth(0).click()

        #follower
        page.goto(page.url+"/followers")
        time.sleep(2)
        page.locator("div[data-theme='system']").click()
        page.locator("button.p-0").nth(0).click()
        page.locator("button.btn-primary").click()
        page.locator('select.w-32').select_option('HTML')
        
        with page.expect_download() as download_info:
            page.get_by_text('Start Export').click()
        download = download_info.value
        download.save_as(path = "./"+username+"/followers.html")
        for i in range(3,0,-1): page.locator('div.w-9').nth(i).click()
        page.locator('a[href="/'+username+'"]').nth(0).click()


        #likes
        page.goto(page.url+"/likes")
        time.sleep(2)
        page.locator("div[data-theme='system']").click()
        page.locator("button.p-0").nth(3).click()
        page.locator("button.btn-primary").click()
        time.sleep(2)
        page.locator('select.w-32').select_option('HTML')
        with page.expect_download() as download_info:
            page.get_by_text('Start Export').click()
        download = download_info.value
        download.save_as(path = "./"+username+"/likes.html")
        for i in range(3,0,-1): page.locator('div.w-9').nth(i).click()
        page.locator('a[href="/'+username+'"]').nth(0).click()


        #logout
        page.goto('https://x.com/logout')
        page.locator('button.css-175oi2r').nth(0).click()
        time.sleep(5)
        browser.close()

        b = []
        with open("./"+username+"/tweets.html",'r') as f:
            i = f.read().index('<tr>',710) + 4
            f.seek(i)
            a = f.readline()[:-17]
            lt = a.split('<tr>')
            for ct in lt:
                if "</tbody></table>"in ct:
                    print(ct)
            b = list(set(lt))
            f.seek(0)
            s = f.read(i) +'<tr>' + '<tr>'.join(b)+"</tbody></table>"+"\n</body>\n</html>"
        with open("./"+username+"/tweets.html",'w') as f:
            f.write(s)


        #zipfile
        with zipfile.ZipFile(f'./X.zip', 'w', zipfile.ZIP_DEFLATED) as myzip:
            myzip.write(f'./{username}/following.html')
            os.remove(f'./{username}/following.html')
            myzip.write(f'./{username}/followers.html')
            os.remove(f'./{username}/followers.html')
            myzip.write(f'./{username}/tweets.html')
            os.remove(f'./{username}/tweets.html')
            myzip.write(f'./{username}/likes.html')
            os.remove(f'./{username}/likes.html')
            os.rmdir(f'./{username}')

    with sync_playwright() as playwright:
        run(playwright)