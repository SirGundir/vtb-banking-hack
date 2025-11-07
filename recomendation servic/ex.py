import time
import requests

BASE_URL = "https://sbank.open.bankingapi.ru"


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


def get_consent_status(consent_request_id: str, team_id: str):
    url = f"{BASE_URL}/account-consents/{consent_request_id}"
    headers = {
        "accept": "application/json",
        "x-fapi-interaction-id": team_id,
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["data"]
    else:
        print(f"❌ Ошибка при получении статуса согласия: {response.status_code}")
        print(response.text)
        return None


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


if __name__ == "__main__":
    CLIENT_ID = "team221"
    CLIENT_SECRET = "uLICRPukXIX7EvwS49xgEuDEByZXfMVw"
    REQUESTING_BANK = "team221"
    TARGET_CLIENT_ID = "team221-1"

    bank_token = get_bank_token(CLIENT_ID, CLIENT_SECRET)
    if not bank_token:
        exit()

    request_id = create_consent(bank_token, REQUESTING_BANK, TARGET_CLIENT_ID)
    if not request_id:
        exit()

    print("\n⏳ Проверяем статус согласия (пока клиент не одобрит)...\n")
    consent_info = None
    while True:
        consent_info = get_consent_status(request_id, REQUESTING_BANK)
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

    accounts = get_accounts(bank_token, REQUESTING_BANK, consent_id, TARGET_CLIENT_ID)
    if accounts:
        print(accounts)
