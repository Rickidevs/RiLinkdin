#If you want to improve it, fork it, don't steal!

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import logging
import json
from datetime import datetime
import os
import pickle

class LinkedInBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.action = None
        self.setup_logging()
        self.connection_count = 0
        self.daily_limit = 100
        self.cookies_file = 'linkedin_cookies.pkl'

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('linkedin_bot.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 15)  
            self.action = ActionChains(self.driver)
            self.logger.info("Chrome driver successfully started")
            return True
        except Exception as e:
            self.logger.error(f"Driver setup error: {str(e)}")
            return False

    def load_cookies(self):
        if os.path.exists(self.cookies_file):
            try:
                self.driver.get("https://www.linkedin.com/")
                time.sleep(random.uniform(2, 4))
                
                with open(self.cookies_file, 'rb') as cookiesfile:
                    cookies = pickle.load(cookiesfile)
                    for cookie in cookies:
                        self.driver.add_cookie(cookie)
                
                self.driver.get("https://www.linkedin.com/feed/")
                time.sleep(random.uniform(3, 5))
                

                if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                    self.logger.info("Successfully logged in with cookies")
                    return True
                else:
                    self.logger.warning("Cookies invalid, performing normal login")
                    return False
            except Exception as e:
                self.logger.error(f"Cookie loading error: {str(e)}")
                return False
        return False

    def save_cookies(self):
        try:
            with open(self.cookies_file, 'wb') as cookiesfile:
                pickle.dump(self.driver.get_cookies(), cookiesfile)
            self.logger.info("Cookies saved")
        except Exception as e:
            self.logger.error(f"Cookie saving error: {str(e)}")

    def login(self, username=None, password=None):
        if self.load_cookies():
            return True
        
        if not username or not password:
            print("📧 LinkedIn Login Information (First time only)")
            print("-" * 30)
            username = input("Email or Phone: ").strip()
            password = input("Password: ").strip()
        
        if not username or not password:
            self.logger.error("Username and password required!")
            return False

        try:
            self.logger.info("Logging in to LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))

            try:
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.ID, "username"))
                )
            except:
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "session_key"))
                )
            email_input.clear()
            for char in username:
                email_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            self.logger.info("Username entered")

            try:
                password_input = self.driver.find_element(By.ID, "password")
            except:
                password_input = self.driver.find_element(By.NAME, "session_password")
            password_input.clear()
            for char in password:
                password_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            self.logger.info("Password entered")

            try:
                sign_in_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and (contains(text(), 'Sign in') or contains(text(), 'Oturum aç'))]"))
                )
            except:
                sign_in_button = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-litms-control-urn='login-submit']"))
                )
            self.action.move_to_element(sign_in_button).pause(random.uniform(0.1, 0.3)).click().perform()

            self.wait.until(EC.url_contains("feed") or EC.url_contains("mynetwork"))
            self.logger.info("Successfully logged in")
            
            self.save_cookies()
            return True

        except Exception as e:
            self.logger.error(f"Login error: {str(e)}")
            return False

    def go_to_my_network(self):
        try:
            self.logger.info("Going to My Network page...")

            self.driver.get("https://www.linkedin.com/mynetwork/")
            time.sleep(random.uniform(3, 5))
            if "mynetwork" in self.driver.current_url:
                self.logger.info("Reached My Network page via direct URL")
                return True

            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(random.uniform(2, 4))

            selectors = [
                "//span[contains(text(), 'My Network') or contains(text(), 'Ağım')]",  
                "//a[contains(@href, '/mynetwork/')]",
                "//span[contains(text(), 'Network')]",
                "//*[contains(@title, 'My Network') or contains(@title, 'Ağım')]"
            ]

            for selector in selectors:
                try:
                    element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    self.action.move_to_element(element).pause(random.uniform(0.1, 0.3)).click().perform()
                    time.sleep(random.uniform(2, 4))
                    if "mynetwork" in self.driver.current_url:
                        self.logger.info(f"Reached My Network page via {selector}")
                        return True
                except:
                    continue

            try:
                search_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-global-typeahead__input")))
                search_input.send_keys("My Network")
                search_input.send_keys(Keys.ENTER)
                time.sleep(random.uniform(2, 4))
                network_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/mynetwork/')]")))
                network_link.click()
                if "mynetwork" in self.driver.current_url:
                    self.logger.info("Reached My Network page via search")
                    return True
            except:
                pass

            self.logger.error("Failed to reach My Network page")
            return False

        except Exception as e:
            self.logger.error(f"Error going to My Network page: {str(e)}")
            return False

    def search_people(self, search_term):
        try:
            self.logger.info(f"Searching for '{search_term}'...")

            try:
                search_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-global-typeahead__input"))
                )
            except:
                search_input = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search' or @aria-label='Search' or @placeholder='Ara' or @aria-label='Ara']"))
                )
            search_input.clear()
            for char in search_term:
                search_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            search_input.send_keys(Keys.ENTER)
            time.sleep(random.uniform(3, 5))

            try:
                people_filter = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'People') or contains(text(), 'Kişiler')]"))
                )
                self.action.move_to_element(people_filter).pause(random.uniform(0.1, 0.3)).click().perform()
                time.sleep(random.uniform(2, 4))
                self.logger.info("People filter applied")
            except:
                self.logger.warning("People filter not found, continuing...")

            return True

        except Exception as e:
            self.logger.error(f"Search error: {str(e)}")
            return False

    def send_connection_requests(self, max_requests):
        sent_count = 0
        page = 1
        max_pages = 10

        while sent_count < max_requests and page <= max_pages:
            try:
                self.logger.info(f"Processing page {page}...")
                time.sleep(random.uniform(3, 5))

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))

                connect_buttons = self.driver.find_elements(
                    By.XPATH, "//button[contains(@aria-label, 'Invite') and contains(@aria-label, 'to connect')]"
                )

                if not connect_buttons:
                    connect_buttons = self.driver.find_elements(
                        By.XPATH, "//button[.//span[text()='Connect' or text()='Bağlan' or text()='Bağlantı kur']]"
                    )

                if not connect_buttons:
                    connect_buttons = self.driver.find_elements(
                        By.XPATH, "//button[.//svg[@id='connect-small']]"
                    )

                if not connect_buttons:
                    self.logger.info("No connect buttons found on this page")
                    break

                for button in connect_buttons:
                    if sent_count >= max_requests:
                        break

                    try:
                        self.action.move_to_element(button).pause(random.uniform(0.5, 1.5)).perform()
                        time.sleep(random.uniform(0.5, 1))
                        button.click()
                        sent_count += 1
                        self.connection_count += 1

                        self.logger.info(f"Connection request sent ({sent_count}/{max_requests})")

                        time.sleep(random.uniform(2, 5))

                        if sent_count % 5 == 0:
                            self.logger.info("5 requests sent, waiting 20-40 seconds...")
                            time.sleep(random.uniform(20, 40))
                            self.driver.execute_script("window.scrollBy(0, -500);")

                    except Exception as e:
                        self.logger.warning(f"Error clicking connect button: {str(e)}")
                        continue

                if sent_count < max_requests:
                    try:
                        next_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next' or contains(text(), 'Next') or @aria-label='Sonraki' or contains(text(), 'Sonraki')]"))
                        )
                        if next_button.is_enabled():
                            self.action.move_to_element(next_button).click().perform()
                            page += 1
                            time.sleep(random.uniform(3, 5))
                        else:
                            break
                    except:
                        self.logger.info("Next page button not found")
                        break

            except Exception as e:
                self.logger.error(f"Page processing error: {str(e)}")
                break

        return sent_count

    def send_random_connections(self, max_requests):
        try:
            if not self.go_to_my_network():
                return 0

            sent_count = 0
            refresh_count = 0
            max_refreshes = 5

            while sent_count < max_requests and refresh_count < max_refreshes:
                time.sleep(random.uniform(3, 5))

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))

                connect_buttons = self.driver.find_elements(
                    By.XPATH, "//button[contains(@aria-label, 'Invite') and contains(@aria-label, 'to connect')]"
                )

                if not connect_buttons:
                    connect_buttons = self.driver.find_elements(
                        By.XPATH, "//button[.//span[text()='Connect' or text()='Bağlan' or text()='Bağlantı kur']]"
                    )

                if not connect_buttons:
                    connect_buttons = self.driver.find_elements(
                        By.XPATH, "//button[.//svg[@id='connect-small']]"
                    )

                if not connect_buttons:
                    self.logger.info("No connect buttons found, refreshing page...")
                    self.driver.refresh()
                    refresh_count += 1
                    time.sleep(random.uniform(5, 8))
                    continue

                for button in connect_buttons:
                    if sent_count >= max_requests:
                        break

                    try:
                        self.action.move_to_element(button).pause(random.uniform(0.5, 1.5)).perform()
                        time.sleep(random.uniform(0.5, 1))
                        button.click()
                        sent_count += 1
                        self.connection_count += 1

                        self.logger.info(f"Random connection request sent ({sent_count}/{max_requests})")

                        time.sleep(random.uniform(3, 6))

                        if sent_count % 3 == 0:
                            self.logger.info("3 requests sent, waiting 15-30 seconds...")
                            time.sleep(random.uniform(15, 30))

                    except Exception as e:
                        self.logger.warning(f"Random connect error: {str(e)}")
                        continue

                if sent_count < max_requests:
                    self.driver.refresh()
                    refresh_count += 1
                    time.sleep(random.uniform(5, 8))

            return sent_count

        except Exception as e:
            self.logger.error(f"Random connection sending error: {str(e)}")
            return 0

    def save_stats(self):
        try:
            stats = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_connections_sent': self.connection_count
            }

            with open('bot_stats.json', 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Statistics saved: {self.connection_count} connections")

        except Exception as e:
            self.logger.error(f"Statistics saving error: {str(e)}")

    def close(self):
        if self.driver:
            self.save_stats()
            self.driver.quit()
            self.logger.info("Bot closed")

def main():
    print("=" * 60)
    print(" LinkedIn Connection Automation")
    print("=" * 60)
    print()

    bot = LinkedInBot()

    try:
        if not bot.setup_driver():
            print("❌ Driver setup failed!")
            return

        if not bot.login():
            print("❌ Login failed! Check your information.")
            return

        print("✅ Successfully logged in!")

        print("\n📊 Connection Settings")
        print("-" * 25)
        try:
            max_connections = int(input("How many connections to send? (Max 50): "))
            if max_connections > 50:
                max_connections = 50
                print("⚠️ Limited to maximum 50 for safety.")
        except ValueError:
            max_connections = 10
            print("⚠️ Invalid number, using default 10.")

        print("\n🎯 Connection Type Selection")
        print("-" * 25)
        print("1. Random people (My Network)")
        print("2. Search by keyword")

        choice = input("Make your choice (1 or 2): ").strip()

        sent_count = 0

        if choice == "1":
            print(f"\n🔄 Sending {max_connections} random connections...")
            sent_count = bot.send_random_connections(max_connections)

        elif choice == "2":
            search_term = input("\nSearch keyword (e.g., CEO, Developer): ").strip()
            if not search_term:
                print("❌ Keyword required!")
                return

            print(f"\n🔍 Searching '{search_term}' and sending {max_connections} connections...")

            if bot.search_people(search_term):
                time.sleep(random.uniform(3, 5))
                sent_count = bot.send_connection_requests(max_connections)
            else:
                print("❌ Search failed!")
                return
        else:
            print("❌ Invalid choice!")
            return

        print("\n" + "=" * 60)
        print(" SUMMARY REPORT")
        print("=" * 60)
        print(f"✅ Total connections sent: {sent_count}")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📝 Detailed log: linkedin_bot.log file")
        print("📊 Statistics: bot_stats.json file")
        print("\n⚠️ Note: Pay attention to LinkedIn daily limits!")
        print("💡 Recommended: 20-30 connections per day for safe usage.")

    except KeyboardInterrupt:
        print("\n\n⏹️ Bot stopped!")
    except Exception as e:
        print(f"\n❌ General error: {str(e)}")
        bot.logger.error(f"Main program error: {str(e)}")
    finally:
        bot.close()

if __name__ == "__main__":
    main()
