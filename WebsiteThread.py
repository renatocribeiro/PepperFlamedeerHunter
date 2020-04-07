import threading
from Driver import *
from random import randint, choice
import time
import os
import json

MIN_WAIT = 3
MAX_WAIT = 5

class WebsiteThread(threading.Thread):
    def __init__(self, agent, user, only_dump, debug = False):
        threading.Thread.__init__(self)
        self.agent = agent
        self.user = user
        self._only_dump = only_dump
        self.debug = debug
        self.driver = init_driver(self.user["user"], self.agent.short, True if self.user["gmail_login"] else self.debug)
        self._in_prod_page = False
        self._collection = {}

    def run(self):
        self.display("RUN")
        self._login()
        if self._only_dump:
            self.visit_collection()
        else:
            t_end = time.time() + 60*30
            now = time.time()
            while now < t_end:
                self.find_that_renne()
                self.browse_website()
                now = time.time()
        self.driver.close()

    def visit_collection(self):
        self.driver.get(self.agent.collection)
        try:
            prizes = self.driver.find_elements_by_class_name('mc-background--primary')
            all_cards = {}
            for prize in prizes:
                p = prize.find_elements_by_tag_name('p')
                cards_dict = {}
                if len(p) > 0:
                    #collectable cards
                    prize_name = p[1].text
                    cards = prize.find_elements_by_class_name('mc-card')
                    for card in cards:
                        card_name = card.find_element_by_class_name('mc-festiveFont').text
                        try:
                            counter = card.find_element_by_class_name('mc-card-counter-child').text
                        except Exception as e:
                            counter = 0
                        cards_dict[card_name] = counter
                    all_cards[prize_name] = cards_dict

                else:
                    #immediat cards
                    card = prize.find_element_by_tag_name('img')
                    card_img_url = card.get_attribute('src')
                    card_type = card_img_url[card_img_url.rfind('level')+5:card_img_url.rfind('level')+7].strip('_')
                    card_name = card.get_attribute('alt')
                    cards_dict[card_name] = 0 if int(card_type) == 0 else 1

                    all_cards[card_name] = cards_dict

            all_cards["time"] = time.time()
            self._collection = all_cards
            self._dump_collection()
        except Exception as e:
            print(e)

    def _dump_collection(self):
        folder = self.agent.short
        if not os.path.exists(folder):
            os.makedirs(folder)
        fname = "{short}/{uname}.json".format(short = self.agent.short, uname = self.user["user"])

        with open(fname, 'w') as fp:
            json.dump(self._collection, fp)

    def display(self, other = ""):
        print("{time}:{user}:{site}:{other}".format(time=time.time(), user=self.user["user"], site=self.agent.short, other=other))

    def _login(self):
        self.display("LOGIN")
        self.driver.get(self.agent.login)
        to_login = False
        try:
            conn_btn = WebDriverWait(self.driver, randint(MIN_WAIT, MAX_WAIT)).until(
                       EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/div/div/div[2]/div[3]/div[2]/div/div/ul/li/div/button')))
            to_login = conn_btn.is_displayed()        
        except Exception as e:
            pass

        if(to_login):
            if self.user["gmail_login"]:
                try:
                    WebDriverWait(self.driver, 120).until(
                            EC.presence_of_element_located((By.XPATH, '//input[@type="email"]'))).send_keys(self.user["email"])

                    WebDriverWait(self.driver, 120).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@id="identifierNext"]'))).click()

                    WebDriverWait(self.driver, 120).until(
                            EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))).send_keys(self.user["pw"])


                    WebDriverWait(self.driver, 120).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@id="passwordNext"]'))).click()

                except Exception as e:
                    pass

                self.driver.get(self.agent.url)
            else:
                try:
                    user_field = self.driver.find_element(By.XPATH, '//*[@id="login_form-identity"]')
                    user_field.send_keys(self.user["user"])
                    pw_field = self.driver.find_element(By.XPATH, '//*[@id="login_form-password"]')
                    pw_field.send_keys(self.user["pw"])
                    conn_btn.click()
                    self.driver.get(self.agent.url)
                except Exception as e:
                    print(e)

    def browse_website(self):

        something_to_do = [
                        self._scroll,
                        self._nav_page,
                        self._rand_deal]
        t_end = time.time() + randint(1, 5)
        while time.time() < t_end:
            fcn = choice(something_to_do)
            fcn()
            self.display("BROWSE:{}".format(fcn.__name__))
            self._refresh()
            time.sleep(randint(1,2))

    def _refresh(self):
        self.driver.get(self.agent.url)


    def _rand_deal(self):
        if self._in_prod_page:
            self.driver.get(self.agent.url)
            self._in_prod_page = False
        else:
            try:
                deal_btn = self.driver.find_elements_by_class_name("thread-title--list")
                choice(deal_btn).click()
                self._in_prod_page = True
            except Exception as e:
                pass
                print(e)

    def _nav_page(self):
        next_prev_btns = [
            '//*[@id="pagination"]/nav/div/span[6]/a',
            '//*[@id="pagination"]/nav/div/span[3]/a'
        ]
        try:
            page_btn = self.driver.find_element(By.XPATH, choice(next_prev_btns))
            page_btn.click()
        except Exception as e:
            print(e)


    def _scroll(self):
        self.driver.execute_script("$('html,body').animate({{ scrollTop: {} }}, 'slow');".format(randint(0, 900)))

    def find_that_renne(self):
        try:
            popup, link = None, None
            _min, _max = 5*60, 15*60

            popup = WebDriverWait(self.driver, randint(_min, _max)).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mc-notification-character--peek"))
            )

            link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mc-btn--primary"))
            )

            link.click()
            self.display("FOUND")
            self.visit_collection()
            time.sleep(2)
            self.driver.get(self.agent.url)
        except Exception as e:
            self.display("NOTFOUND")