import time
import requests

BASE_URL = "https://sbank.open.bankingapi.ru"

# ----------------------------
# Получение токена банка
# ----------------------------
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

# ----------------------------
# Создание согласия
# ----------------------------
def create_consent(bank_token: str, requesting_bank: str, client_id: str):
    url = f"{BASE_URL}/account-consents/request"
    headers = {
        "Authorization": f"Bearer {bank_token}",
        "Content-Type": "application/json",
        "X-Requesting-Bank": requesting_bank,
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
        print("📦 Ответ от сервера:", data)
        request_id = data.get("request_id")
        print("✅ Согласие создано:", request_id)
        print("⚠️ Клиент должен одобрить согласие в своём банке перед использованием.")
        return request_id
    print(f"❌ Ошибка при создании согласия: {response.status_code}")
    print(response.text)
    return None

# ----------------------------
# Проверка статуса согласия
# ----------------------------
def get_consent_status(consent_request_id: str, team_id: str, bank_token: str):
    url = f"{BASE_URL}/account-consents/{consent_request_id}"
    headers = {
        "accept": "application/json",
        "x-fapi-interaction-id": team_id,
        "Authorization": f"Bearer {bank_token}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        print(f"❌ Ошибка при получении статуса согласия: {response.status_code}")
        print(response.text)
        return None

# ----------------------------
# Получение списка счетов
# ----------------------------
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
    elif response.status_code == 403:
        print("⚠️ Нет доступа — убедитесь, что клиент одобрил согласие.")
        print(response.text)
        return None
    else:
        print(f"❌ Ошибка при получении счетов: {response.status_code}")
        print(response.text)
        return None

# ----------------------------
# Получение транзакций по счету
# ----------------------------
def get_transactions(
    bank_token: str,
    requesting_bank: str,
    consent_id: str,
    client_id: str,
    account_id: str,
    from_booking_date_time: str = None,
    to_booking_date_time: str = None,
    page: int = 1,
    limit: int = 50,
):
    url = f"{BASE_URL}/accounts/{account_id}/transactions"
    headers = {
        "Authorization": f"Bearer {bank_token}",
        "X-Requesting-Bank": requesting_bank,
        "X-Consent-Id": consent_id,
        "accept": "application/json",
    }
    params = {
        "client_id": client_id,
        "page": page,
        "limit": limit,
    }
    if from_booking_date_time:
        params["from_booking_date_time"] = from_booking_date_time
    if to_booking_date_time:
        params["to_booking_date_time"] = to_booking_date_time

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print(f"✅ Транзакции по счёту {account_id} успешно получены")
        return response.json()
    else:
        print(f"❌ Ошибка при получении транзакций: {response.status_code}")
        print(response.text)
        return None

# ----------------------------
# Основной скрипт
# ----------------------------
if __name__ == "__main__":
    CLIENT_ID = "team221"
    CLIENT_SECRET = "uLICRPukXIX7EvwS49xgEuDEByZXfMVw"
    REQUESTING_BANK = "team221"
    TARGET_CLIENT_ID = "team221-1"

    # 1. Получаем bank_token
    bank_token = get_bank_token(CLIENT_ID, CLIENT_SECRET)
    if not bank_token:
        exit()

    # 2. Создаём согласие
    request_id = create_consent(bank_token, REQUESTING_BANK, TARGET_CLIENT_ID)
    if not request_id:
        exit()

    # 3. Ждём одобрения согласия
    print("\n⏳ Проверяем статус согласия (пока клиент не одобрит)...\n")
    consent_info = None
    while True:
        consent_info = get_consent_status(request_id, REQUESTING_BANK, bank_token)
        if not consent_info:
            exit()
        status = consent_info.get("status")
        print(f"📊 Статус согласия ({request_id}): {status}")
        if status == "Authorized":
            print("✅ Согласие одобрено! Переходим к получению счетов.")
            break
        time.sleep(5)

    consent_id = consent_info.get("consentId")
    print("🔑 Используем consentId:", consent_id)

    # 4. Получаем список счетов
    accounts = get_accounts(bank_token, REQUESTING_BANK, consent_id, TARGET_CLIENT_ID)
    account_list = accounts.get("data", {}).get("account", [])
    for account in account_list:
        account_id = account["accountId"]
        currency = account["currency"]
        nickname = account.get("nickname", "")
        print(f"\n💳 Счёт: {account_id}, Валюта: {currency}, Название: {nickname}")

        # Получаем транзакции
        transactions = get_transactions(
            bank_token=bank_token,
            requesting_bank=REQUESTING_BANK,
            consent_id=consent_id,
            client_id=TARGET_CLIENT_ID,
            account_id=account_id,
            from_booking_date_time="2025-01-01T00:00:00Z",
            to_booking_date_time="2025-12-31T23:59:59Z",
            limit=100,
        )
        if transactions:
            print("📄 Транзакции:")
            print(transactions)
