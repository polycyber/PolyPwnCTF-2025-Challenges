from playwright.sync_api import sync_playwright
import random as r
from time import sleep
from string import ascii_lowercase, digits, ascii_uppercase


class Bot:
    def __init__(self):
        self.flag1 = "polycyber{Jones_1s_us1ng_a_we1rd_br0wser}"
        self.flag2 = "polycyber{Th1s_c00k1e_w0nt_h3lp_t0_g3t_th3_pr1v4te_n0tes}"
        self.flag3 = "polycyber{Luck7_h3_ch3ck3d_h1s_n0t3s_b3f0r3}"
        self.OTP = "".join(r.choices(ascii_lowercase + digits + ascii_uppercase, k=16))
        self.nginx_host = "127.0.0.1"
        self.urls_to_visit = []

    def change_OTP(self):
        self.OTP = "".join(r.choices(ascii_lowercase + digits + ascii_uppercase, k=16))

    def run(self):
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            context = browser.new_context(user_agent=self.flag1)
            page = context.new_page()
            while True:
                try:
                    while self.urls_to_visit:
                        context.clear_cookies()
                        context.add_cookies(
                            [
                                {
                                    "name": "flag",
                                    "value": self.flag2,
                                    "domain": self.nginx_host,
                                    "path": "/",
                                }
                            ]
                        )
                        page.goto(f"http://{self.nginx_host}/journal?OTP={self.OTP}")
                        self.change_OTP()
                        param_value = self.urls_to_visit.pop()
                        page.goto(f"http://{self.nginx_host}/?name={param_value}")
                except Exception as e:
                    print(e)
                    break
                sleep(30)
