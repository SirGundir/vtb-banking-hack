import time
import requests

BASE_URL = "https://sbank.open.bankingapi.ru"


# -------------------- Шаг 1: Токен --------------------
def get_bank_token(client_id: str, client_secret: str) -> str:
    url = f"{BASE_URL}/auth/bank-token"
    params = {"client_id": client_id, "client_secret": client_secret}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Получен bank_token:", token)
        return token
    print(f"❌ Ошибка при получении токена: {response.status_code}")
    print(response.text)
    return None


# -------------------- Шаг 2: Согласие на счета --------------------
def create_account_consent(bank_token: str, requesting_bank: str, client_id: str):
    url = f"{BASE_URL}/account-consents/request"
    headers = {
        "Authorization": f"Bearer {bank_token}",
        "X-Requesting-Bank": requesting_bank,
        "Content-Type": "application/json",
        "accept": "application/json",
    }
    payload = {
        "client_id": client_id,
        "permissions": [
            "ReadAccountsDetail",
            "ReadBalances",
            "ReadTransactionsDetail",
        ],
        "reason": "Агрегация счетов для HackAPI",
        "requesting_bank": requesting_bank,
        "requesting_bank_name": "Team 221 App",
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        print("📦 Ответ сервера (согласие на счета):", data)
        return data.get("request_id")
    print(f"❌ Ошибка при создании согласия на счета: {response.status_code}")
    print(response.text)
    return None


def get_account_consent_status(request_id: str, team_id: str):
    url = f"{BASE_URL}/account-consents/{request_id}"
    headers = {
        "accept": "application/json",
        "x-fapi-interaction-id": team_id,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        status = data["data"]["status"]
        consent_id = data["data"]["consentId"]
        print(f"📊 Статус согласия на счета: {status}, consentId: {consent_id}")
        return status, consent_id
    print(f"❌ Ошибка при проверке согласия на счета: {response.status_code}")
    print(response.text)
    return None, None


def get_accounts(bank_token: str, requesting_bank: str, consent_id: str, client_id: str):
    url = f"{BASE_URL}/accounts"
    headers = {
        "Authorization": f"Bearer {bank_token}",
        "X-Requesting-Bank": requesting_bank,
        "X-Consent-Id": consent_id,
        "accept": "application/json",
    }
    params = {"client_id": client_id}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print("✅ Счета клиента успешно получены:")
        return response.json()
    print(f"❌ Ошибка при получении счетов: {response.status_code}")
    print(response.text)
    return None


# -------------------- Шаг 3: Согласие на продукты --------------------
def create_product_consent(bank_token: str, requesting_bank: str, client_id: str):
    """
    Создать согласие на работу с продуктами клиента
    """
    url = f"{BASE_URL}/product-agreement-consents/request"
    headers = {
        "Authorization": f"Bearer {bank_token}",
        "X-Requesting-Bank": requesting_bank,
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    payload = {
        "requesting_bank": requesting_bank,
        "client_id": client_id,
        "read_product_agreements": True,
        "open_product_agreements": False,
        "close_product_agreements": False,
        "allowed_product_types": ["deposit", "card"],
        "max_amount": 1000000,
        "valid_until": "2025-12-31T23:59:59",
        "reason": "Агрегация продуктов для HackAPI",
    }

    # Передаем client_id в query-параметре
    params = {"client_id": client_id}

    response = requests.post(url, headers=headers, json=payload, params=params)
    if response.status_code == 200:
        data = response.json()
        print("📦 Ответ сервера (согласие на продукты):", data)
        return data  # ✅ вернуть весь словарь
    else:
        print(f"❌ Ошибка при создании согласия на продукты: {response.status_code}")
        print(response.text)
        return None


def get_product_consent_status(request_id: str, team_id: str):
    url = f"{BASE_URL}/product-agreements-consents/{request_id}"
    headers = {
        "accept": "application/json",
        "x-fapi-interaction-id": team_id,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        status = data["data"]["status"]
        consent_id = data["data"]["consentId"]
        print(f"📊 Статус согласия на продукты: {status}, consentId: {consent_id}")
        return status, consent_id
    print(f"❌ Ошибка при проверке согласия на продукты: {response.status_code}")
    print(response.text)
    return None, None


def get_product_agreements(bank_token: str, requesting_bank: str, consent_id: str, client_id: str):
    url = f"{BASE_URL}/product-agreements"
    headers = {
        "Authorization": f"Bearer {bank_token}",
        "X-Requesting-Bank": requesting_bank,
        "X-Product-Agreement-Consent-Id": consent_id,  # используем consent_id из ответа создания
        "accept": "application/json",
    }
    params = {"client_id": client_id}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print("✅ Продукты клиента успешно получены:")
        return response.json()
    print(f"❌ Ошибка при получении продуктов: {response.status_code}")
    print(response.text)
    return None



# -------------------- Основная логика --------------------
if __name__ == "__main__":
    CLIENT_ID = "team221"
    CLIENT_SECRET = "uLICRPukXIX7EvwS49xgEuDEByZXfMVw"
    REQUESTING_BANK = "team221"
    TARGET_CLIENT_ID = "team221-1"

    # 1️⃣ Токен
    bank_token = get_bank_token(CLIENT_ID, CLIENT_SECRET)
    if not bank_token:
        exit()

    # 2️⃣ Согласие на счета
    account_request_id = create_account_consent(bank_token, REQUESTING_BANK, TARGET_CLIENT_ID)
    if not account_request_id:
        exit()

    # Ждём одобрения счета
    while True:
        status, account_consent_id = get_account_consent_status(account_request_id, REQUESTING_BANK)
        if status == "Authorized":
            print("✅ Согласие на счета одобрено")
            break
        time.sleep(5)

    # Получаем счета
    accounts = get_accounts(bank_token, REQUESTING_BANK, account_consent_id, TARGET_CLIENT_ID)
    if accounts:
        print(accounts)

    response = create_product_consent(bank_token, REQUESTING_BANK, TARGET_CLIENT_ID)

    if response:
        # Берём consent_id из ответа
        product_consent_id = response.get("consent_id")  # pagc-066543877bcb
        print("Используем consent_id:", product_consent_id)

        # ⚡ Сразу получаем продукты
        products = get_product_agreements(bank_token, REQUESTING_BANK, product_consent_id, TARGET_CLIENT_ID)
        if products:
            print(products)