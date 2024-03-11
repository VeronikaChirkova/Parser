import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Parser:

    def __init__(self):
        options = Options()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)



    def get_domain(self, url: str) -> str:
        """
        Разделяет строку URL-адреса на компоненты.
        Получение netloc (часть сетевого местоположения) URL-адреса.

        Args:
            url (str): URL-адрес сайта

        Returns:
            str: netloc (часть сетевого местоположения) URL-адреса.
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain


    def get_freepic(self, url: str) -> dict:
        """Получает ссылки на картинки кошек и текст описания к ним

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict: словарь со списком картинок и текстом описания
        """
        headers = Headers(os="win", headers=True).generate()
        resp = requests.get(url=url, headers=headers)
        soup = bs(resp.content)
        card_els = soup.select(selector="div a img[src]")

        cards = []
        for card in card_els:
            card_src = card.attrs.get("src")
            if not card_src:
                continue
            text = card.attrs.get("alt")
            cards.append({"img": card_src, "text": text})

        result = {}
        result[self.get_domain(url=url)] = cards  # {"url": [{}, {}]}
        return result


    def get_cian(self, url: str) -> dict[list[str], str]:
        """Получает ссылки на картинки квартир и текст описания к ним

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict[list[str], str]: словарь со списком картинок и текстом описания
        """
        headers = Headers(os="win", headers=True).generate()
        resp = requests.get(url=url, headers=headers)
        soup = bs(resp.content)
        card_els = soup.select(selector="div article[data-name]")

        cards = []
        for card in card_els:
            src_list = []
            for img_block in card.select("li img"):
                src_list.append(img_block.attrs.get("src"))
            if not src_list:
                continue
            text = card.select_one("div a span span").text  # type:ignore
            cards.append({"img": src_list, "text": text})

        result = {}
        result[self.get_domain(url=url)] = cards
        return result


    def get_tez(self, url: str) -> dict:
        """Получает ссылки на картинки отелей и текст описания к ним

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict: словарь со списком картинок отелей и текстом описания
        """
        try:
            self.driver.get(url)
            card_els = []

            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-hid]"))
                )
            except TimeoutException:
                # self.driver.quit()
                return {}

            soup = bs(self.driver.page_source, "lxml")
            card_els = soup.select(selector="div[data-hid]")

            cards = []
            for card in card_els:

                if not card.select_one("img"):
                    continue
                card_src = card.select_one("img").attrs.get("src")  # type:ignore
                text = card.select_one("img").attrs.get("alt")  # type:ignore
                cards.append({"img": card_src, "text": text})

            result = {}
            result[self.get_domain(url=url)] = cards

        finally:
            # self.driver.quit()
            pass

        return result


    def get_wb(self, url: str) -> dict[str, str]:
        """Получает ссылки на картинки женских футболок и текст описания к ним

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict[str, str]: словарь со списком картинок и текстом описания
        """

        try:
            self.driver.get(url)
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article div>img[src]"))
            )
        except TimeoutException:
            # self.driver.quit()
            return {}

        soup = bs(self.driver.page_source, "lxml")
        card_els = soup.select(selector="article div>img[src]")

        cards = []
        for card in card_els:
            card_src = card.attrs.get("src")
            if not card_src:
                continue
            text = card.attrs.get("alt")
            cards.append({"img": card_src, "text": text})

        result = {}
        result[self.get_domain(url=url)] = cards

        return result


    def get_avidread(self, url: str) -> dict[str, str]:
        """Получает ссылки на картинки книг и текст описания к ним

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict[str, str]: словарь со списком картинок и текстом описания
        """
        try:
            self.driver.get(url)
            time.sleep(10)
            card_els = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, 'item_block')]"
            )

            cards = []
            for card in card_els:
                card_src = card.find_element(By.TAG_NAME, "img").get_attribute("src")
                if not card_src:
                    continue
                text = card.find_element(By.TAG_NAME, "img").get_attribute("alt")
                cards.append({"img": card_src, "text": text})

            result = {}
            result[self.get_domain(url=url)] = cards
        finally:
            # self.driver.quit()
            pass

        return result


    def get_kino(self, url: str) -> dict[str, str]:
        """Получает ссылки на картинки фильмов и текст описания к ним

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict[str, str]: словарь со списком картинок и текстом описания
        """
        try:
            self.driver.get(url)
            time.sleep(5)

            soup = bs(self.driver.page_source, "lxml")
            card_els = soup.select(selector="div img[src]")

            cards = []
            for card in card_els:
                card_src = card.attrs.get("src")
                if not card_src:
                    continue
                text = card.attrs.get("alt")
                cards.append({"img": card_src, "text": text})

            result = {}
            result[self.get_domain(url=url)] = cards

        finally:
            # self.driver.quit()
            pass

        return result


    def get_rose(self, url: str) -> dict[str, str]:
        """Получает ссылки на картинки букетов и текст описания к ним

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict[str, str]: словарь со списком картинок и текстом описания
        """
        try:
            self.driver.get(url)

            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//div[contains(@class, 'catalog-card catalog-grid__catalog-card')]",
                        )
                    )
                )
            except TimeoutException:
                # self.driver.quit()
                return {}

            card_els = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'catalog-card catalog-grid__catalog-card')]",
            )

            cards = []
            for card in card_els:
                card_src = card.find_element(By.TAG_NAME, "img").get_attribute("src")
                if not card_src:
                    continue
                text = card.find_element(By.TAG_NAME, "img").get_attribute("alt")
                cards.append({"img": card_src, "text": text})

            result = {}
            result[self.get_domain(url=url)] = cards

        finally:
            # self.driver.quit()
            pass

        return result


    def get_toys(self, url: str) -> dict[str, str]:
        """Получает ссылки на картинки настольных игр и текст описания к ним

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict[str, str]: словарь со списком картинок и текстом описания
        """
        try:
            self.driver.get(url)

            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(@class, 'item product sku')]")
                    )
                )
            except TimeoutException:
                # self.driver.quit()
                return {}

            card_els = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, 'item product sku')]"
            )

            cards = []
            for card in card_els:
                card_src = card.find_element(By.TAG_NAME, "img").get_attribute("src")
                if not card_src:
                    continue
                text = card.find_element(By.TAG_NAME, "img").get_attribute("alt")
                cards.append({"img": card_src, "text": text})

            result = {}
            result[self.get_domain(url=url)] = cards

        finally:
            # self.driver.quit()
            pass

        return result


    def get_wine(self, url: str) -> dict[str, str]:
        """Получает ссылки на картинки вин и их названия

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict[str, str]: словарь со списком картинок и текстом описания
        """
        try:
            self.driver.get(url)

            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "form a img[src]"))
                )
            except TimeoutException:
                # self.driver.quit()
                return {}

            card_els = self.driver.find_elements(
                By.XPATH, "//form[contains(@class, 'item-block')]"
            )
            cards = []
            for card in card_els:
                card_src = card.find_element(By.TAG_NAME, "img").get_attribute("src")
                if not card_src:
                    continue
                text = card.find_element(By.TAG_NAME, "p").text
                cards.append({"img": card_src, "text": text})

            result = {}
            result[self.get_domain(url=url)] = cards

        finally:
            # self.driver.quit()
            pass

        return result


    def get_sensorik(self, url: str) -> dict[str, str]:
        """Получает ссылки на картинки развивающих игр для детей и их названия

        Args:
            url (str): URL-адрес сайта

        Returns:
            dict[str, str]: словарь со списком картинок и текстом описания
        """
        try:
            self.driver.get(url)
            time.sleep(10)
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div>img[src]"))
                )
            except TimeoutException:
                # self.driver.quit()
                return {}

            soup = bs(self.driver.page_source, "lxml")
            card_els = soup.select(selector="div>img[src]")

            cards = []
            for card in card_els:
                card_src = card.attrs.get("src")
                if not card_src:
                    continue
                text = card.attrs.get("alt")
                cards.append({"img": card_src, "text": text})

            result = {}
            result[self.get_domain(url=url)] = cards

        finally:
            # self.driver.quit()
            pass

        return result


if __name__ == "__main__":
    wb_url = "https://www.wildberries.ru/catalog/dom-i-dacha/vannaya/aksessuary"
    freepic_url = "https://ru.freepik.com/free-photos-vectors/кот/2"
    cian_url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&maxprice=10000000&object_type%5B0%5D=2&offer_type=flat&region=1&room2=1"
    tez_url = "https://tourist.tez-tour.com/toursearch/f360a9c10471bb75aff03ea0acea74ef/tourType/1/cityId/2190/before/17.04.2024/after/10.04.2024/countryId/1104/minNights/6/maxNights/14/adults/2/flexdate/0/flexnight/0/hotelTypeId/-9006275/mealTypeId/-9006284/rAndBBetter/yes/isTableView/0/lview/cls/noTicketsTo/no/noTicketsFrom/no/hotelInStop/no/recommendedFlag/no/onlineConfirmFlag/no/tourMaxPrice/1500000/categoryGreatThan/yes/currencyId/18864/dtype/period/promoFlag/yes.ru.html"
    ared_url = "https://avidreaders.ru/books/"
    kino_url = "https://www.tvigle.ru/collection/novinki/"
    rose_url = "https://skazkaflora.ru/catalog/bukety/bukety_s_rozami/"
    toys_url = "https://ghtoys.ru/"
    wine_url = "https://nsk.winestyle.ru/wine/all/"
    sensorik_url = "https://sensorikagame.ru/shop"
    parser = Parser()
    avidread_info = parser.get_avidread(url=ared_url)
    freepic_info = parser.get_freepic(url=freepic_url)
    wb_info = parser.get_wb(url=wb_url)
    cian_info = parser.get_cian(url=cian_url)
    tez_info = parser.get_tez(url=tez_url)
    avidread_info = parser.get_avidread(url=ared_url)
    kino_info = parser.get_kino(url=kino_url)
    rose_info = parser.get_rose(url=rose_url)
    toys_info = parser.get_toys(url=toys_url)
    wine_info = parser.get_wine(url=wine_url)
    sensorik_info = parser.get_sensorik(url=sensorik_url)
    parser.driver.quit()
    info = {}
    info.update(freepic_info)
    info.update(wb_info)
    info.update(cian_info)
    info.update(tez_info)
    info.update(avidread_info)
    info.update(kino_info)
    info.update(rose_info)
    info.update(toys_info)
    info.update(wine_info)
    info.update(sensorik_info)
    print()