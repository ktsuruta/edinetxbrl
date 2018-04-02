from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.select import Select
import time


def edinet_downloader(edinet_code='', period='全期間', download_dir=None):
    '''

    :param edinet_code: E02505
    :param period: 当日、 過去３日、過去１週間、過去１か月、過去６か月、過去１年、全期間
    :param download_dir:
    :return:
    '''
    caps = DesiredCapabilities.FIREFOX.copy()
    caps['acceptInsecureCerts'] = True
    ff_binary = FirefoxBinary("/usr/bin/firefox")

    profile = FirefoxProfile()
    if download_dir is None:
        profile.set_preference('browser.download.folderList', 1)
    else:
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.dir',download_dir)
    profile.set_preference("browser.download.panel.shown", False);
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', ('application/octet-stream'))
    profile.set_preference('browser.helperApps.alwaysAsk.force', False)
    profile.set_preference('browser.download.manager.showWhenStarting', False)

    browser = WebDriver(firefox_profile=profile, firefox_binary=ff_binary, capabilities=caps)
    browser.implicitly_wait(10)
    browser.get('%s%s' % ('http://disclosure.edinet-fsa.go.jp/EKW0EZ0001.html?lgKbn=2&dflg=0&iflg=null', ''))
    browser.find_element_by_css_selector('li.kensaku a').click()
    browser.find_element_by_id('mul_t').send_keys(edinet_code)

    browser.find_element_by_css_selector('div.panel-up').click()
    s = Select(browser.find_element_by_name('pfs'))

    for opt in s.options:
        s.select_by_visible_text(period)

    browser.find_element_by_id('sch').click()
    browser.find_element_by_id('xbrlbutton').click()

    try:
        WebDriverWait(browser, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')

        alert = browser.switch_to.alert
        time.sleep(2)
        alert.accept()
        print("alert accepted")
        time.sleep(5)

        browser.close()

    except TimeoutException:
        print("no alert")

if __name__ == '__main__':
    edinet_downloader('E04024')