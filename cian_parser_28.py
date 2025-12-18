
import time
import re
import json
import sys
from datetime import datetime
from typing import List, Dict, Optional
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import psycopg2

class MetroParser:
    """Парсер для работы с метро"""
    
    def __init__(self):
        self.metro_stations = [
             "devyatkino",
    "grazhdanskiy-prospekt",
    "akademicheskaya",
    "politehnicheskaya",
    "ploshcad-muzhestva",
    "lesnaya",
    "vyborgskaya",
    "ploshcad-lenina",
    "chernyshevskaya",
    "ploshcad-vosstaniya",
    "vladimirskaya",
    "pushkinskaya",
    "tehnologicheskiy-institut",
    "baltiyskaya",
    "narvskaya",
    "kirovskiy-zavod",
    "avtovo",
    "leninskiy-prospekt",
    "prospekt-veteranov",
    "parnas",
    "prospekt-prosveshcheniya",
    "ozerki",
    "udelnaya",
    "pionerskaya",
    "chernaya-rechka",
    "petrogradskaya",
    "gorkovskaya",
    "nevskiy-prospekt",
    "sennaya-ploshcad",
    "frunzenskaya",
    "moskovskie-vorota",
    "elektrosila",
    "park-pobedy",
    "moskovskaya",
    "zvezdnaya",
    "kupchino",
    "begovaya",
    "zenit",
    "primorskaya",
    "vasileostrovskaya",
    "gostinyy-dvor",
    "mayakovskaya",
    "ploshcad-aleksandra-nevskogo",
    "elizarovskaya",
    "lomonosovskaya",
    "proletarskaya",
    "obuhovo",
    "rybackoe",
    "gorny-institut",
    "spasskaya",
    "dostoevskaya",
    "ligovskiy-prospekt",
    "novocherkasskaya",
    "ladozhskaya",
    "prospekt-bolshevikov",
    "ulica-dybenko",
    "komendantskiy-prospekt",
    "staraya-derevnya",
    "krestovskiy-ostrov",
    "chkalovskaya",
    "sportivnaya",
    "admiralteyskaya",
    "sadovaya",
    "zvenigorodskaya",
    "obvodnyy-kanal",
    "volkovskaya",
    "buharestskaya",
    "mezhdunarodnaya",
    "prospekt-slavy",
    "dunayskaya",
    "shushary",
        ]
        
        self.metro_ids = {
            "devyatkino": 167,
            "grazhdanskiy-prospekt": 168,
            "akademicheskaya": 169,
            "politehnicheskaya": 170,
            "ploshcad-muzhestva": 171,
            "lesnaya": 172,
            "vyborgskaya": 173,
            "ploshcad-lenina": 174,
            "chernyshevskaya": 175,
            "ploshcad-vosstaniya": 176,
            "vladimirskaya": 177,
            "pushkinskaya": 178,
            "tehnologicheskiy-institut": 179,
            "baltiyskaya": 180,
            "narvskaya": 181,
            "kirovskiy-zavod": 182,
            "avtovo": 183,
            "leninskiy-prospekt": 184,
            "prospekt-veteranov": 185,
            "parnas": 186,
            "prospekt-prosveshcheniya": 187,
            "ozerki": 188,
            "udelnaya": 189,
            "pionerskaya": 190,
            "chernaya-rechka": 191,
            "petrogradskaya": 192,
            "gorkovskaya": 193,
            "nevskiy-prospekt": 194,
            "sennaya-ploshcad": 195,
            "frunzenskaya": 197,
            "moskovskie-vorota": 198,
            "elektrosila": 199,
            "park-pobedy": 200,
            "moskovskaya": 201,
            "zvezdnaya": 202,
            "kupchino": 203,
            "begovaya": 355,
            "zenit": 356,
            "primorskaya": 204,
            "vasileostrovskaya": 205,
            "gostinyy-dvor": 206,
            "mayakovskaya": 207,
            "ploshcad-aleksandra-nevskogo": 208,
            "elizarovskaya": 210,
            "lomonosovskaya": 211,
            "proletarskaya": 212,
            "obuhovo": 213,
            "rybackoe": 214,
            "gorny-institut": 215,
            "spasskaya": 232,
            "dostoevskaya": 221,
            "ligovskiy-prospekt": 222,
            "novocherkasskaya": 224,
            "ladozhskaya": 225,
            "prospekt-bolshevikov": 226,
            "ulica-dybenko": 227,
            "komendantskiy-prospekt": 215,
            "staraya-derevnya": 216,
            "krestovskiy-ostrov": 217,
            "chkalovskaya": 218,
            "sportivnaya": 219,
            "admiralteyskaya": 242,
            "sadovaya": 220,
            "zvenigorodskaya": 231,
            "obvodnyy-kanal": 241,
            "volkovskaya": 230,
            "buharestskaya": 247,
            "mezhdunarodnaya": 246,
            "prospekt-slavy": 357,
            "dunayskaya": 358,
            "shushary": 359,
}
    
    def get_metro_url(self, metro_name, page=1):
        """Получить URL для поиска по метро с указанием страницы"""
        metro_slug = metro_name.lower().replace(' ', '-').replace("'", "")
        metro_id = self.metro_ids.get(metro_slug, 167)
        return f"https://spb.cian.ru/cat.php?deal_type=sale&engine_version=2&metro%5B0%5D={metro_id}&offer_type=flat&p={page}"
    
    def display_metro_stations(self):
        """Показать список станций с номерами"""
        print("\n🚇 Список станций метро Санкт-Петербурга:")
        print("-" * 50)
        for i, station in enumerate(self.metro_stations, 1):
            print(f"{i:3}. {station}")
        print("-" * 50)

class IDCollector:
    """Коллектор ID объявлений (этап 1)"""
    
    def __init__(self):
        self.driver = None
        self.metro_parser = MetroParser()
    
    def setup_browser(self):
        """Настройка браузера"""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        options.add_argument("--start-maximized")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            print("✅ Браузер запущен")
            return True
        except Exception as e:
            print(f"❌ Ошибка запуска браузера: {e}")
            return False
    
    def collect_from_metro(self, metro_name: str, max_pages: int = 50) -> List[Dict]:  
        """Собрать ID объявлений для конкретной станции метро"""
        print(f"\n🔍 Сбор ID для станции: {metro_name}")
        
        all_offers = []
        
        for page in range(1, max_pages + 1):
            url = self.metro_parser.get_metro_url(metro_name, page)
            print(f"  📄 Страница {page}")
            
            try:
                self.driver.get(url)
                time.sleep(2.5)
                
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1.5)
                
                offers = self._extract_links_from_page()
                
                if not offers and page > 1:
                    print("  ⚠️ На странице нет объявлений, завершаем")
                    break
                
                new_count = 0
                for offer in offers:
                    if not any(o['id'] == offer['id'] for o in all_offers):
                        all_offers.append(offer)
                        new_count += 1
                
                print(f"  ✅ Найдено: {len(offers)} | Новых: {new_count} | Всего: {len(all_offers)}")
                
                if new_count < 3 and page > 5:  # Уменьшил с 5 до 3, увеличил с 3 до 5 страниц
                    print("  ⚠️ Мало новых объявлений, завершаем")
                    break
                
                time.sleep(1.5)
                
            except Exception as e:
                print(f"  ❌ Ошибка на странице {page}: {e}")
                break
        
        print(f"✅ Для станции {metro_name} собрано {len(all_offers)} ID")
        return all_offers
    
    def _extract_links_from_page(self) -> List[Dict]:
        """Извлечь ссылки с текущей страницы"""
        links = []
        
        try:
            offer_cards = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-name="CardComponent"]')
            for card in offer_cards:
                try:
                    a_tag = card.find_element(By.CSS_SELECTOR, 'a[data-name="LinkArea"]')
                    href = a_tag.get_attribute('href')
                    if href and 'cian.ru/sale/flat' in href:
                        match = re.search(r'/(\d+)/?$', href)
                        if match:
                            offer_id = match.group(1)
                            if not any(l['id'] == offer_id for l in links):
                                links.append({'id': offer_id, 'url': href})
                except:
                    continue
            
            if len(links) < 20:
                offer_cards = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="offer-card"]')
                for card in offer_cards:
                    try:
                        a_tag = card.find_element(By.CSS_SELECTOR, 'a')
                        href = a_tag.get_attribute('href')
                        if href and 'cian.ru/sale/flat' in href:
                            match = re.search(r'/(\d+)/?$', href)
                            if match:
                                offer_id = match.group(1)
                                if not any(l['id'] == offer_id for l in links):
                                    links.append({'id': offer_id, 'url': href})
                    except:
                        continue
            
            if len(links) < 10:
                all_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="cian.ru/sale/flat"]')
                for link in all_links:
                    try:
                        href = link.get_attribute('href')
                        if href and '/sale/flat/' in href:
                            match = re.search(r'/(\d+)/?$', href)
                            if match:
                                offer_id = match.group(1)
                                if not any(l['id'] == offer_id for l in links):
                                    links.append({'id': offer_id, 'url': href})
                    except:
                        continue
        
        except Exception as e:
            print(f"  ⚠️ Ошибка извлечения ссылок: {e}")
        
        return links
    
    def save_ids_to_file(self, offers: List[Dict], filename: str = "cian_ids.pkl"):
        """Сохранить ID в файл"""
        try:
            with open(filename, 'wb') as f:
                pickle.dump(offers, f)
            print(f"✅ ID сохранены в файл: {filename}")
            print(f"📊 Всего ID: {len(offers)}")
            return True
        except Exception as e:
            print(f"❌ Ошибка сохранения в файл: {e}")
            return False
    
    def load_ids_from_file(self, filename: str = "cian_ids.pkl") -> List[Dict]:
        """Загрузить ID из файла"""
        try:
            with open(filename, 'rb') as f:
                offers = pickle.load(f)
            print(f"✅ ID загружены из файла: {filename}")
            print(f"📊 Всего ID: {len(offers)}")
            return offers
        except FileNotFoundError:
            print(f"⚠️ Файл {filename} не найден")
            return []
        except Exception as e:
            print(f"❌ Ошибка загрузки из файла: {e}")
            return []
    
    def run_collection(self, metros_to_process=None, max_pages_per_metro=50, save_filename="cian_ids.pkl"):  # Увеличил с 15 до 50
        """Запустить сбор ID"""
        print("\n" + "="*60)
        print("ЭТАП 1: СБОР ID ОБЪЯВЛЕНИЙ")
        print("="*60)
        
        if not self.setup_browser():
            return
        
        if metros_to_process is None:
            metros_to_process = self.metro_parser.metro_stations
        
        all_offers = []
        
        for metro_idx, metro_name in enumerate(metros_to_process):
            print(f"\n🚇 [{metro_idx+1}/{len(metros_to_process)}] Станция: {metro_name}")
            
            offers = self.collect_from_metro(metro_name, max_pages_per_metro)
            
            for offer in offers:
                offer['source_metro'] = metro_name
                if not any(o['id'] == offer['id'] for o in all_offers):
                    all_offers.append(offer)
            
            if metro_idx < len(metros_to_process) - 1:
                print("  ⏳ Пауза между станциями...")
                time.sleep(3)
        
        if all_offers:
            self.save_ids_to_file(all_offers, save_filename)
            total_collected = len(all_offers)
        
        print(f"\n✅ ЭТАП 1 ЗАВЕРШЕН")
        print(f"📊 Всего собрано уникальных ID: {len(all_offers)}")
        print("="*60)
        
        self.driver.quit()
        return all_offers

class DetailParser:
    """Детальный парсер объявлений (этап 2) - использует вашу существующую базу"""
    
    def __init__(self):
        self.driver = None
        self.conn = None
        self.cursor = None
        self.table_name = "cian_offers"
        self.metro_parser = MetroParser()
    
    def setup_browser(self):
        """Настройка браузера"""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=options)
            print("✅ Браузер запущен")
            return True
        except Exception as e:
            print(f"❌ Ошибка запуска браузера: {e}")
            return False
    
    def setup_database(self):
        """Подключение к существующей базе"""
        print("\n🔌 Подключение к существующей базе данных...")
        
        try:
            self.conn = psycopg2.connect(
                host='localhost',
                port='5432',
                database='cian_parser_2',
                user='postgres',
                password='Password',
                client_encoding='UTF8'
            )
            
            self.cursor = self.conn.cursor()
            print("✅ Подключено к существующей базе")
            print(f"📋 Используем таблицу: {self.table_name}")
            
            self.cursor.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = '{self.table_name}'
                )
            """)
            
            if not self.cursor.fetchone()[0]:
                print(f"❌ Таблица '{self.table_name}' не найдена!")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка подключения: {e}")
            return False
    
    def check_if_exists(self, cian_id: str) -> bool:
        """Проверить, существует ли объявление в базе"""
        try:
            self.cursor.execute(
                f"SELECT 1 FROM {self.table_name} WHERE cian_id = %s",
                (cian_id,)
            )
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"   ⚠️ Ошибка проверки существования: {e}")
            return False
    
    def get_offer_metros(self, cian_id: str) -> List[str]:
        """Получить станции метро для существующего объявления"""
        try:
            self.cursor.execute(
                f"SELECT metro_station FROM {self.table_name} WHERE cian_id = %s",
                (cian_id,)
            )
            result = self.cursor.fetchone()
            if result and result[0]:
                stations = [s.strip() for s in result[0].split(',') if s.strip()]
                return stations
            return []
        except Exception as e:
            print(f"   ⚠️ Ошибка получения метро: {e}")
            return []
    
    def _convert_to_numeric(self, value):
        """Конвертировать строку в числовой формат для PostgreSQL numeric полей"""
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        
        value = str(value).strip()
        if not value:
            return None
        
    
        value = value.replace(' ', '').replace(',', '.')
        value = re.sub(r'[^\d.]', '', value)
        
        try:
            return float(value)
        except:
            match = re.search(r'(\d+\.?\d*)', value)
            if match:
                try:
                    return float(match.group(1))
                except:
                    return None
            return None
    
    def _convert_to_int(self, value):
        """Конвертировать в целое число"""
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        
        value = str(value).strip()
        if not value:
            return None
        
        try:
            return int(value)
        except:
            match = re.search(r'(\d+)', value)
            if match:
                try:
                    return int(match.group(1))
                except:
                    return None
            return None
    
    def _clean_string(self, value, max_length=None):
        """Очистить строку и обрезать по максимальной длине"""
        if value is None:
            return None
        
        value = str(value).strip()
        if not value:
            return None
        
        if max_length and len(value) > max_length:
            value = value[:max_length]
        
        return value
    
    def extract_first_metro(self, soup):
        """Извлечь только ПЕРВУЮ станцию метро из HTML-элементов страницы объявления"""
        try:
           
            metro_link = soup.find('a', class_=lambda x: x and 'underground_link' in x)
            
            if metro_link:
                metro_text = metro_link.get_text(strip=True)
                if metro_text:
                    metro_text = re.sub(r'\s+', ' ', metro_text)
                    metro_text = metro_text.replace('метро', '').replace('м.', '').strip()
                    
                    for station in self.metro_parser.metro_stations:
                        if station.lower() in metro_text.lower() or metro_text.lower() in station.lower():
                            return station
                    
                  
                    return metro_text
            
          
            metro_selectors = [
                'a[class*="underground"]',
                'span[class*="underground"]',
                'div[class*="underground"]',
                '[data-name="UndergroundStation"]',
                '[data-name="GeoUnderground"]',
            ]
            
            for selector in metro_selectors:
                try:
                    metro_elem = soup.select_one(selector)
                    if metro_elem:
                        metro_text = metro_elem.get_text(strip=True)
                        if metro_text and len(metro_text) > 2:
                            metro_text = re.sub(r'\s+', ' ', metro_text)
                            metro_text = metro_text.replace('метро', '').replace('м.', '').strip()
                            
                         
                            for station in self.metro_parser.metro_stations:
                                if station.lower() in metro_text.lower() or metro_text.lower() in station.lower():
                                    return station
                            
                            return metro_text
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ Ошибка при извлечении метро: {e}")
            return None
    
    def extract_metro_time_from_page(self, soup):
        """Извлечь время до метро из HTML-элементов страницы объявления"""
        try:
            time_span = soup.find('span', class_=lambda x: x and 'underground_time' in x)
            
            if time_span:
                time_text = time_span.get_text(strip=True)
                time_match = re.search(r'(\d+)\s*мин\w*', time_text, re.IGNORECASE)
                if time_match:
                    minutes = time_match.group(1)
                    return f"{minutes} мин"
                
                num_match = re.search(r'(\d+)', time_text)
                if num_match:
                    minutes = num_match.group(1)
                    if 1 <= int(minutes) <= 120:
                        return f"{minutes} мин"
            
            time_selectors = [
                'span[class*="time"]',
                'div[class*="time"]',
                'span[class*="minute"]',
                'div[class*="minute"]',
            ]
            
            for selector in time_selectors:
                try:
                    time_elem = soup.select_one(selector)
                    if time_elem:
                        time_text = time_elem.get_text(strip=True)
                        time_match = re.search(r'(\d+)\s*мин\w*', time_text, re.IGNORECASE)
                        if time_match:
                            minutes = time_match.group(1)
                            return f"{minutes} мин"
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ Ошибка при извлечении времени до метро: {e}")
            return None
    
    def extract_type_building(self, soup):
        """Извлечь тип дома из HTML-элементов"""
        try:
            type_items = soup.find_all('div', {'data-name': 'OfferSummaryInfoItem'})
            
            for item in type_items:
                title_elem = item.find('p', class_=lambda x: x and 'color_gray60' in x)
                if title_elem and 'Тип дома' in title_elem.get_text():
                    value_elem = item.find('p', class_=lambda x: x and 'color_text-primary-default' in x)
                    if value_elem:
                        building_type = value_elem.get_text(strip=True)
                        if building_type and building_type.strip():
                            return building_type.strip()
            
            building_selectors = [
                'div[data-name="ObjectFactoidsItem"]',
                'div[class*="factoids"]',
                'span[class*="building-type"]',
                'div[class*="house-type"]',
            ]
            
            for selector in building_selectors:
                try:
                    elements = soup.select(selector)
                    for elem in elements:
                        elem_text = elem.get_text(strip=True).lower()
                        if any(keyword in elem_text for keyword in ['кирпичный', 'панельный', 'монолитный', 'блочный', 'деревянный', 'сталинский']):
                            building_type = elem.get_text(strip=True)
                            if building_type and building_type.strip():
                                return building_type.strip()
                except:
                    continue
            
            return "none_type"
            
        except Exception as e:
            print(f"   ⚠️ Ошибка при извлечении типа дома: {e}")
            return "none_type"
    
    def extract_area_living(self, soup):
        """Извлечь жилую площадь из HTML-элементов"""
        try:
            area_divs = soup.find_all('div', class_=lambda x: x and 'text' in x if x else False)
            
            for div in area_divs:
                title_span = div.find('span', class_=lambda x: x and 'color_gray60' in x if x else False)
                if title_span and 'Жилая площадь' in title_span.get_text():
                    value_span = div.find('span', style=lambda x: x and 'letter-spacing:-0.2px' in x if x else False)
                    if value_span:
                        area_text = value_span.get_text(strip=True)
                        if area_text and area_text.strip():
                            
                            match = re.search(r'(\d+[.,]?\d*)', area_text.replace(' ', ''))
                            if match:
                                return match.group(1)
                            else:
                                return area_text.strip()
            
            bold_spans = soup.find_all('span', style=lambda x: x and 'letter-spacing:-0.2px' in x if x else False)
            
            for i, span in enumerate(bold_spans):
                span_text = span.get_text(strip=True)
                if 'м²' in span_text or 'м2' in span_text or re.search(r'\d+[.,]?\d*', span_text):
                    parent = span.parent
                    if parent:
                        prev_spans = parent.find_all('span')
                        for prev_span in prev_spans:
                            if 'Жилая площадь' in prev_span.get_text():
                                return span_text
            
            data_items = soup.find_all('div', {'data-name': 'OfferSummaryInfoItem'})
            for item in data_items:
                title_elem = item.find('p', class_=lambda x: x and 'color_gray60' in x)
                if title_elem and 'Жилая площадь' in title_elem.get_text():
                    value_elem = item.find('p', class_=lambda x: x and 'color_text-primary-default' in x)
                    if value_elem:
                        area_text = value_elem.get_text(strip=True)
                        if area_text and area_text.strip():
                            return area_text
            
            page_text = soup.get_text()
            pattern = r'Жилая\s+площадь[\s:]*([\d.,]+\s*м²?|\d+[.,]?\d*)'
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ Ошибка при извлечении жилой площади: {e}")
            return None
    
    def extract_area_kitchen(self, soup):
        """Извлечь площадь кухни из HTML-элементов"""
        try:
            area_divs = soup.find_all('div', class_=lambda x: x and 'text' in x if x else False)
            
            for div in area_divs:
                title_span = div.find('span', class_=lambda x: x and 'color_gray60' in x if x else False)
                if title_span and 'Площадь кухни' in title_span.get_text():
                    value_span = div.find('span', style=lambda x: x and 'letter-spacing:-0.2px' in x if x else False)
                    if value_span:
                        area_text = value_span.get_text(strip=True)
                        if area_text and area_text.strip():
                            match = re.search(r'(\d+[.,]?\d*)', area_text.replace(' ', ''))
                            if match:
                                return match.group(1)
                            else:
                                return area_text.strip()
            
            bold_spans = soup.find_all('span', style=lambda x: x and 'letter-spacing:-0.2px' in x if x else False)
            
            for i, span in enumerate(bold_spans):
                span_text = span.get_text(strip=True)
                if 'м²' in span_text or 'м2' in span_text or re.search(r'\d+[.,]?\d*', span_text):
                    parent = span.parent
                    if parent:
                        prev_spans = parent.find_all('span')
                        for prev_span in prev_spans:
                            if 'Площадь кухни' in prev_span.get_text():
                                return span_text
            
            data_items = soup.find_all('div', {'data-name': 'OfferSummaryInfoItem'})
            for item in data_items:
                title_elem = item.find('p', class_=lambda x: x and 'color_gray60' in x)
                if title_elem and 'Площадь кухни' in title_elem.get_text():
                    value_elem = item.find('p', class_=lambda x: x and 'color_text-primary-default' in x)
                    if value_elem:
                        area_text = value_elem.get_text(strip=True)
                        if area_text and area_text.strip():
                            return area_text
            
            page_text = soup.get_text()
            pattern = r'Площадь\s+кухни[\s:]*([\d.,]+\s*м²?|\d+[.,]?\d*)'
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ Ошибка при извлечении площади кухни: {e}")
            return None
    
    def extract_floor_info(self, soup):
        """Извлечь информацию о этаже в формате 'X из Y'"""
        try:
            bold_spans = soup.find_all('span', style=lambda x: x and 'letter-spacing:-0.2px' in x if x else False)
            
            for span in bold_spans:
                span_text = span.get_text(strip=True)
                floor_match = re.search(r'(\d+)\s*(?:из|/)\s*(\d+)', span_text)
                if floor_match:
                    current_floor = floor_match.group(1)
                    return f"{current_floor} из {floor_match.group(2)}"
            
            floor_selectors = [
                'span[class*="floor"]',
                'div[class*="floor"]',
                '[data-name="ObjectFactoidsItem"]',
                '[data-name="Floor"]',
            ]
            
            for selector in floor_selectors:
                try:
                    elements = soup.select(selector)
                    for elem in elements:
                        elem_text = elem.get_text(strip=True)
                        floor_match = re.search(r'(\d+)\s*(?:из|/)\s*(\d+)', elem_text)
                        if floor_match:
                            current_floor = floor_match.group(1)
                            return f"{current_floor} из {floor_match.group(2)}"
                        
                        floor_match = re.search(r'(\d+)\s*этаж\s*(?:из|/)\s*(\d+)', elem_text)
                        if floor_match:
                            current_floor = floor_match.group(1)
                            return f"{current_floor} из {floor_match.group(2)}"
                except:
                    continue
            
            return None
                
        except Exception as e:
            print(f"   ⚠️ Ошибка при извлечении информации о этаже: {e}")
            return None
    
    def extract_title(self, soup):
        """Извлечь заголовок"""
        try:
            title = soup.find('h1')
            if title:
                return title.get_text(strip=True)
            return None
        except:
            return None
    
    def extract_price_corrected(self, soup):
        """Корректное извлечение цены"""
        try:
            json_ld = soup.find('script', type='application/ld+json')
            if json_ld and json_ld.string:
                try:
                    data = json.loads(json_ld.string)
                    price_paths = [
                        data.get('offers', {}).get('price'),
                        data.get('offers', {}).get('price', {}).get('price'),
                        data.get('price'),
                        data.get('mainEntity', {}).get('offers', {}).get('price')
                    ]
                    
                    for price in price_paths:
                        if price and isinstance(price, (int, float, str)):
                            try:
                                price_num = int(str(price).replace(' ', '').replace(',', ''))
                                if price_num > 1000:
                                    return price_num
                            except:
                                pass
                except:
                    pass
            
            price_selectors = [
                'div[data-testid="price-amount"]',
                'span[data-mark="MainPrice"]',
                '[data-name="PriceInfo"]',
                'span[itemprop="price"]',
                'meta[itemprop="price"]',
                'div[class*="price"]',
                'span[class*="price"]',
            ]
            
            for selector in price_selectors:
                try:
                    elements = soup.select(selector)
                    for elem in elements:
                        for attr in ['content', 'data-price', 'value']:
                            price_attr = elem.get(attr)
                            if price_attr:
                                try:
                                    price_num = int(str(price_attr).replace(' ', '').replace(',', ''))
                                    if price_num > 1000:
                                        return price_num
                                except:
                                    pass
                        
                        text = elem.get_text()
                        if text:
                            price_match = re.search(r'[\d\s]+(?:\s?₽)?', text.replace('\xa0', ' '))
                            if price_match:
                                price_str = price_match.group().replace(' ', '').replace('₽', '').replace(',', '')
                                if price_str.isdigit():
                                    price_num = int(price_str)
                                    if price_num > 1000:
                                        return price_num
                except:
                    continue
            
            page_source = str(soup)
            patterns = [
                r'"price":\s*"?(\d[\d\s]*)"?',
                r'"priceAmount":\s*"?(\d[\d\s]*)"?',
                r'"mainPrice":\s*"?(\d[\d\s]*)"?',
                r'data-price="(\d[\d\s]*)"',
                r'itemprop="price"\s+content="(\d+)"',
                r'<meta[^>]+itemprop="price"[^>]+content="(\d+)"',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, page_source)
                for match in matches:
                    try:
                        price_str = str(match).replace(' ', '').replace(',', '').replace('"', '')
                        if price_str.isdigit():
                            price_num = int(price_str)
                            if price_num > 1000:
                                return price_num
                    except:
                        continue
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ Ошибка при парсинге цены: {e}")
            return None
    
    def extract_old_price_corrected(self, soup):
        """Корректное извлечение старя цены"""
        try:
            old_price_selectors = [
                'span[data-mark="OldPrice"]',
                's',
                'del',
                'div[class*="old-price"]',
                'span[class*="old-price"]',
                'span[class*="discount"]',
                'div[class*="discount"]',
            ]
            
            for selector in old_price_selectors:
                try:
                    elements = soup.select(selector)
                    for elem in elements:
                        text = elem.get_text()
                        if text and any(ch.isdigit() for ch in text):
                            price_match = re.search(r'(\d[\d\s]*)', text.replace('\xa0', ' '))
                            if price_match:
                                price_str = price_match.group(1).replace(' ', '').replace(',', '')
                                if price_str.isdigit():
                                    price_num = int(price_str)
                                    if price_num > 1000:
                                        return price_num
                except:
                    continue
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ Ошибка при парсинге старой цены: {e}")
            return None
    
    def extract_address(self, soup):
        """Извлечь адрес"""
        try:
            address_selectors = [
                '[data-name="GeoLabel"]',
                '[data-name="AddressContainer"]',
                '[class*="address"]',
                'div[itemprop="address"]',
                'span[itemprop="address"]',
            ]
            
            for selector in address_selectors:
                try:
                    elem = soup.select_one(selector)
                    if elem:
                        text = elem.get_text(strip=True)
                        if text and len(text) > 5:
                            return text
                except:
                    continue
            
            return None
        except:
            return None
    
    def extract_area_total(self, soup):
        """Извлечь общую площадь"""
        try:
            title = soup.find('h1')
            if title:
                title_text = title.get_text()
                match = re.search(r'(\d+[,.]?\d*)\s*м²', title_text)
                if match:
                    area_str = match.group(1)
                    # Конвертируем в числовой формат
                    return self._convert_to_numeric(area_str)
            
            feature_selectors = [
                '[data-name="Features"]',
                '[class*="features"]',
                '[class*="parameters"]',
                'div[itemprop="floorSize"]',
            ]
            
            for selector in feature_selectors:
                try:
                    elem = soup.select_one(selector)
                    if elem:
                        text = elem.get_text()
                        match = re.search(r'(\d+[,.]?\d*)\s*м²', text)
                        if match:
                            area_str = match.group(1)
                            return self._convert_to_numeric(area_str)
                        
                        if 'Площадь' in text:
                            area_match = re.search(r'Площадь[^\d]*(\d+[,.]?\d*)', text)
                            if area_match:
                                area_str = area_match.group(1)
                                return self._convert_to_numeric(area_str)
                except:
                    continue
            
            return None
        except Exception as e:
            print(f"   ⚠️ Ошибка при извлечении общей площади: {e}")
            return None
    
    def extract_rooms(self, soup):
        """Извлечь количество комнат"""
        try:
            title = soup.find('h1')
            if title:
                title_text = title.get_text().lower()
                
                if 'студия' in title_text or 'апартамент' in title_text:
                    return 0
                
                rooms_match = re.search(r'(\d+)[-\s]*(?:комн|комнат)', title_text)
                if rooms_match:
                    return int(rooms_match.group(1))
            
            feature_text = soup.get_text().lower()
            if '1-комн' in feature_text or '1 комн' in feature_text:
                return 1
            elif '2-комн' in feature_text or '2 комн' in feature_text:
                return 2
            elif '3-комн' in feature_text or '3 комн' in feature_text:
                return 3
            elif '4-комн' in feature_text or '4 комн' in feature_text:
                return 4
            elif '5-комн' in feature_text or '5 комн' in feature_text:
                return 5
            elif '6-комн' in feature_text or '6 комн' in feature_text:
                return 6
            elif '7-комн' in feature_text or '7 комн' in feature_text:
                return 7
            elif '8-комн' in feature_text or '8 комн' in feature_text:
                return 8
            elif '9-комн' in feature_text or '9 комн' in feature_text:
                return 9
            elif '10-комн' in feature_text or '10 комн' in feature_text:
                return 10
            elif '11-комн' in feature_text or '11 комн' in feature_text:
                return 11
            elif '12-комн' in feature_text or '12 комн' in feature_text:
                return 12
            
            return None
        except:
            return None
    
    def extract_year_built_improved(self, soup):
        """Извлечь год постройки"""
        try:
            page_text = soup.get_text()
            
            patterns = [
                r'Год постройки[:\s]*(\d{4})',
                r'Построен в[:\s]*(\d{4})',
                r'Сдан в[:\s]*(\d{4})',
                r'Дом\s+(\d{4})\s+года',
                r'(\d{4})\s+год\s+постройки',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    year = int(match.group(1))
                    if 1800 <= year <= datetime.now().year:
                        return year
            
            json_ld = soup.find('script', type='application/ld+json')
            if json_ld and json_ld.string:
                try:
                    data = json.loads(json_ld.string)
                    for field in ['yearBuilt', 'dateBuilt', 'constructionDate', 'buildDate']:
                        if field in data:
                            year_str = str(data[field])
                            match = re.search(r'(\d{4})', year_str)
                            if match:
                                year = int(match.group(1))
                                if 1800 <= year <= datetime.now().year:
                                    return year
                except:
                    pass
            
            return None
            
        except Exception as e:
            print(f"   ⚠️ Ошибка при парсинге года постройки: {e}")
            return None
    
    def extract_district(self, soup):
        """Извлечь район"""
        try:
            address = self.extract_address(soup)
            if address:
                parts = address.split(',')
                for part in parts:
                    part = part.strip()
                    if 'р-н' in part:
                        return part.replace('р-н', '').strip()
                    elif 'район' in part:
                        return part.replace('район', '').strip()
                    
                if len(parts) > 1:
                    return parts[1].strip()
        except:
            pass
        return None
    
    def parse_offer(self, offer: Dict) -> Optional[Dict]:
        """Парсинг одного объявления"""
        print(f"\n📄 Парсим ID: {offer['id']}")
        
        try:
            self.driver.get(offer['url'])
            time.sleep(3)
            
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            exists = False
            
            if self.conn:
                exists = self.check_if_exists(offer['id'])
            
          
            metro_station = self.extract_first_metro(soup)
            metro_time = self.extract_metro_time_from_page(soup)
            type_building = self.extract_type_building(soup)
            area_living = self.extract_area_living(soup)
            area_kitchen = self.extract_area_kitchen(soup)
            floor_info = self.extract_floor_info(soup)
            
            data = {
                'cian_id': offer['id'],
                'url': offer['url'],
                'title': self.extract_title(soup),
                'address': self.extract_address(soup),
                'price': self.extract_price_corrected(soup),
                'old_price': self.extract_old_price_corrected(soup),
                'area_total': self.extract_area_total(soup),
                'area_living': area_living,
                'area_kitchen': area_kitchen,
                'floor_current': floor_info,
                'rooms': self.extract_rooms(soup),
                'year_built': self.extract_year_built_improved(soup),
                'district': self.extract_district(soup),
                'metro_station': metro_station,  # Только первая станция
                'metro_time': metro_time,
                'type_building': type_building,
                'publication_date': datetime.now().strftime('%Y-%m-%d'),
                'is_active': True,
                'last_checked': datetime.now(),
                'exists': exists
            }
            
            self.print_offer_info(data, exists)
            return data
            
        except Exception as e:
            print(f"   ❌ Ошибка парсинга: {e}")
            return None
    
    def print_offer_info(self, data, exists=False):
        """Вывод информации об объявлении"""
        status = "🔄 Обновление" if exists else "🆕 Новое"
        print(f"   {status}")
        
        if data['title']:
            print(f"   📝 {data['title'][:50]}...")
        if data['price']:
            print(f"   💰 Цена: {data['price']:,} ₽")
        if data['metro_station']:
            print(f"   🚇 Метро: {data['metro_station']}")
        if data['metro_time']:
            print(f"   ⏱️  Время до метро: {data['metro_time']}")
    
    def save_to_database(self, data, exists=False):
        """Сохранить в базу данных с учетом типов полей"""
        if not data or not self.conn:
            print("   ⚠️ Нет данных или подключения к БД")
            return False
        
        try:
            now = datetime.now()
            
           
            price = self._convert_to_numeric(data.get('price'))
            old_price = self._convert_to_numeric(data.get('old_price'))
            area_total = self._convert_to_numeric(data.get('area_total')) 
            rooms = self._convert_to_int(data.get('rooms'))  
            year_built = self._convert_to_int(data.get('year_built'))  
            
           
            metro_station = self._clean_string(data.get('metro_station'), 200)  
            district = self._clean_string(data.get('district'), 200)  
            metro_time = self._clean_string(data.get('metro_time'), 50)  
            type_building = self._clean_string(data.get('type_building'))  
            area_living = self._clean_string(data.get('area_living'))  
            area_kitchen = self._clean_string(data.get('area_kitchen'), 100)  
            floor_current = self._clean_string(data.get('floor_current'), 50)  
            address = self._clean_string(data.get('address'))  
            title = self._clean_string(data.get('title'))  
            
            print(f"   🔍 Подготовка данных для БД:")
            print(f"      Цена: {price}")
            print(f"      Общая площадь (numeric): {area_total}")
            print(f"      Метро: {metro_station}")
            
            if exists:
                update_sql = f"""
                    UPDATE {self.table_name} SET
                    price = %s, old_price = %s, updated_at = %s, last_checked = %s,
                    metro_station = %s, metro_time = %s, address = %s, 
                    area_total = %s, area_living = %s, area_kitchen = %s,
                    floor_current = %s, rooms = %s,
                    year_built = %s, district = %s, type_building = %s,
                    title = %s
                    WHERE cian_id = %s
                """
                
                params = (
                    price, old_price, now, now,
                    metro_station, metro_time, address,
                    area_total, area_living, area_kitchen,
                    floor_current, rooms,
                    year_built, district, type_building,
                    title,
                    data['cian_id']
                )
                
                self.cursor.execute(update_sql, params)
                rows_updated = self.cursor.rowcount
                
                if rows_updated > 0:
                    print(f"   ✅ Обновлено записей: {rows_updated}")
                    result = "updated"
                else:
                    print(f"   ⚠️ Запись не найдена для обновления")
                    result = "not_found"
                
            else:
                
                insert_sql = f"""
                    INSERT INTO {self.table_name} 
                    (cian_id, url, title, address, price, old_price,
                    area_total, area_living, area_kitchen, 
                    floor_current, rooms, year_built,
                    district, metro_station, metro_time, type_building, publication_date,
                    is_active, created_at, updated_at, last_checked)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                params = (
                    data['cian_id'], 
                    data['url'], 
                    title, 
                    address,
                    price, 
                    old_price,
                    area_total, 
                    area_living, 
                    area_kitchen,
                    floor_current, 
                    rooms, 
                    year_built,
                    district, 
                    metro_station, 
                    metro_time,
                    type_building,
                    data.get('publication_date'), 
                    data.get('is_active', True),
                    now, now, now
                )
                
                self.cursor.execute(insert_sql, params)
                rows_inserted = self.cursor.rowcount
                
                if rows_inserted > 0:
                    print(f"   ✅ Вставлено новых записей: {rows_inserted}")
                    result = "new"
                else:
                    print(f"   ⚠️ Не вставлено ни одной записи")
                    result = "no_insert"
            
            self.conn.commit()
            print(f"   💾 Транзакция успешно завершена")
            return result
            
        except Exception as e:
            print(f"   ❌ Ошибка базы: {e}")
            import traceback
            traceback.print_exc()
            
            try:
                self.conn.rollback()
                print(f"   ↩️ Откат выполнен")
            except:
                pass
            
            return "error"
    
    def run_parsing(self, offers: List[Dict], max_total=None):
        """Запустить детальный парсинг"""
        print("\n" + "="*60)
        print("ЭТАП 2: ДЕТАЛЬНЫЙ ПАРСИНГ ОБЪЯВЛЕНИЙ")
        print("="*60)
        
        if not self.setup_browser():
            return
        
        use_db = input("\nСохранять в базу данных? (y/n): ").lower() == 'y'
        
        if use_db:
            if not self.setup_database():
                print("\n⚠️ Продолжаем без базы данных")
                use_db = False
        
        stats = {
            'total': 0,
            'new': 0,
            'updated': 0,
            'errors': 0,
            'skipped': 0
        }
        
        print(f"📋 Всего ID для обработки: {len(offers)}")
        
        for i, offer in enumerate(offers):
            if max_total and stats['total'] >= max_total:
                print(f"\n⚠️ Достигнут лимит в {max_total} объявлений")
                break
            
            stats['total'] += 1
            
            if use_db and self.check_if_exists(offer['id']):
                print(f"\n[{i+1}/{len(offers)}] ID {offer['id']} уже в базе")
                stats['skipped'] += 1
                continue
            
            print(f"\n[{i+1}/{len(offers)}] Обрабатываем ID: {offer['id']}")
            
            data = self.parse_offer(offer)
            
            if data:
                if use_db:
                    result = self.save_to_database(data, data['exists'])
                    
                    if result == "new":
                        stats['new'] += 1
                    elif result == "updated":
                        stats['updated'] += 1
                    elif result == "error":
                        stats['errors'] += 1
                else:
                    stats['new'] += 1
            else:
                stats['errors'] += 1
            
            if (i + 1) % 10 == 0:
                print(f"\n📊 Прогресс: {i+1}/{len(offers)} | "
                      f"Новых: {stats['new']} | Обновлено: {stats['updated']} | "
                      f"Ошибок: {stats['errors']} | Пропущено: {stats['skipped']}")
            
            if i < len(offers) - 1:
                time.sleep(3)
        
        print(f"\n✅ ЭТАП 2 ЗАВЕРШЕН")
        print(f"📊 Итоги:")
        print(f"   Всего обработано: {stats['total']}")
        print(f"   Новых: {stats['new']}")
        print(f"   Обновлено: {stats['updated']}")
        print(f"   Ошибок: {stats['errors']}")
        print(f"   Пропущено: {stats['skipped']}")
        print("="*60)
        
        self.driver.quit()
        if self.conn:
            self.conn.close()

def main():
    """Главная функция с увеличенными лимитами"""
    print("="*60)
    print("ПАРСЕР ЦИАН - ДВУХЭТАПНАЯ АРХИТЕКТУРА")
    print("(СОХРАНЕНИЕ СУЩЕСТВУЮЩЕЙ БАЗЫ ДАННЫХ)")
    print("="*60)
    
    metro_parser = MetroParser()
    
    while True:
        print("\nВыберите действие:")
        print("1. Собрать ID объявлений (этап 1)")
        print("2. Загрузить ID из файла и парсить (этап 2)")
        print("3. Полный цикл (собрать и сразу парсить)")
        print("4. Проверить статистику базы")
        print("5. Выход")
        
        choice = input("\nВаш выбор (1-5): ").strip()
        
        if choice == "1":
            collector = IDCollector()
            
            print("\nВыберите станции:")
            metro_parser.display_metro_stations()
            print("0. Все станции")
            
            station_choice = input("\nНомера станций через запятую (или 0 для всех): ").strip()
            
            if station_choice == "0":
                metros = metro_parser.metro_stations
            else:
                metros = []
                for num in station_choice.split(','):
                    try:
                        idx = int(num.strip()) - 1
                        if 0 <= idx < len(metro_parser.metro_stations):
                            metros.append(metro_parser.metro_stations[idx])
                    except:
                        pass
            
            if not metros:
                print("Не выбрано ни одной станции")
                continue
            
            try:
                
                max_pages = int(input("Максимум страниц на станцию (10-100): ") or "50")
                filename = input("Имя файла для сохранения ID (cian_ids.pkl): ") or "cian_ids.pkl"
            except:
                max_pages = 50  
                filename = "cian_ids.pkl"
            
            collector.run_collection(metros, max_pages, filename)
        
        elif choice == "2":
            parser = DetailParser()
            
            try:
                filename = input("Имя файла с ID (cian_ids.pkl): ") or "cian_ids.pkl"
                
                batch_size = int(input("Сколько парсить (10-5000): ") or "2000")
                use_limit = input("Ограничить общее количество? (y/n): ").lower() == 'y'
                max_total = None
                if use_limit:
                    max_total = int(input("Максимум объявлений (до 5000): ") or "2000")
            except:
                filename = "cian_ids.pkl"
                batch_size = 2000  
                max_total = None
            
            collector = IDCollector()
            offers = collector.load_ids_from_file(filename)
            
            if offers:
                
                if batch_size > len(offers):
                    batch_size = len(offers)
                    print(f"⚠️ В файле только {len(offers)} ID, будем парсить все")
                
                parser.run_parsing(offers[:batch_size], max_total=max_total)
            else:
                print("❌ Нет ID для парсинга")
        
        elif choice == "3":
            collector = IDCollector()
            parser = DetailParser()
            
            print("\n=== ЭТАП 1: СБОР ID ===")
            offers = collector.run_collection()
            
            if offers:
                print("\n=== ЭТАП 2: ПАРСИНГ ===")
                try:
                    
                    batch_size = int(input(f"Сколько парсить из {len(offers)}? (10-{len(offers)}): ") or str(min(2000, len(offers))))
                except:
                    batch_size = min(2000, len(offers))  
                
                parser.run_parsing(offers[:batch_size])
        
        elif choice == "4":
            try:
                parser = DetailParser()
                if parser.setup_database():
                    parser.cursor.execute(f"SELECT COUNT(*) FROM {parser.table_name}")
                    total = parser.cursor.fetchone()[0]
                    
                    parser.cursor.execute(f"SELECT COUNT(*) FROM {parser.table_name} WHERE metro_station LIKE '%,%'")
                    multi_metro = parser.cursor.fetchone()[0]
                    
                    print(f"\n📊 СТАТИСТИКА БАЗЫ:")
                    print(f"   Всего объявлений: {total}")
                    print(f"   С несколькими станциями метро: {multi_metro}")
                    
                    parser.conn.close()
            except Exception as e:
                print(f"❌ Ошибка получения статистики: {e}")
        
        elif choice == "5":
            print("\n👋 Выход...")
            break
        
        else:
            print("❌ Неверный выбор")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {str(e)}")
        import traceback
        traceback.print_exc()
    
    input("\nНажмите Enter для выхода...")
