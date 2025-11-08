# BankApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**addBankApiV1BanksPost**](BankApi.md#addbankapiv1bankspost) | **POST** /api/v1/banks/ | Add Bank |
| [**connectUserBankApiV1BanksBankIdAddConsentPost**](BankApi.md#connectuserbankapiv1banksbankidaddconsentpost) | **POST** /api/v1/banks/{bankId}/add-consent/ | Connect User Bank |
| [**getBanksApiV1BanksGet**](BankApi.md#getbanksapiv1banksget) | **GET** /api/v1/banks/ | Get Banks |
| [**rejectConsentApiV1BanksBankIdRejectConsentPost**](BankApi.md#rejectconsentapiv1banksbankidrejectconsentpost) | **POST** /api/v1/banks/{bankId}/reject-consent/ | Reject Consent |



## addBankApiV1BanksPost

> BankSchema addBankApiV1BanksPost(addBankDTO)

Add Bank

### Example

```ts
import {
  Configuration,
  BankApi,
} from '';
import type { AddBankApiV1BanksPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new BankApi();

  const body = {
    // AddBankDTO
    addBankDTO: ...,
  } satisfies AddBankApiV1BanksPostRequest;

  try {
    const data = await api.addBankApiV1BanksPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **addBankDTO** | [AddBankDTO](AddBankDTO.md) |  | |

### Return type

[**BankSchema**](BankSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## connectUserBankApiV1BanksBankIdAddConsentPost

> OkResponseSchema connectUserBankApiV1BanksBankIdAddConsentPost(bankId)

Connect User Bank

### Example

```ts
import {
  Configuration,
  BankApi,
} from '';
import type { ConnectUserBankApiV1BanksBankIdAddConsentPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new BankApi(config);

  const body = {
    // number
    bankId: 56,
  } satisfies ConnectUserBankApiV1BanksBankIdAddConsentPostRequest;

  try {
    const data = await api.connectUserBankApiV1BanksBankIdAddConsentPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **bankId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**OkResponseSchema**](OkResponseSchema.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getBanksApiV1BanksGet

> Array&lt;BankSchema&gt; getBanksApiV1BanksGet()

Get Banks

### Example

```ts
import {
  Configuration,
  BankApi,
} from '';
import type { GetBanksApiV1BanksGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new BankApi(config);

  try {
    const data = await api.getBanksApiV1BanksGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**Array&lt;BankSchema&gt;**](BankSchema.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## rejectConsentApiV1BanksBankIdRejectConsentPost

> OkResponseSchema rejectConsentApiV1BanksBankIdRejectConsentPost(bankId)

Reject Consent

### Example

```ts
import {
  Configuration,
  BankApi,
} from '';
import type { RejectConsentApiV1BanksBankIdRejectConsentPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new BankApi(config);

  const body = {
    // number
    bankId: 56,
  } satisfies RejectConsentApiV1BanksBankIdRejectConsentPostRequest;

  try {
    const data = await api.rejectConsentApiV1BanksBankIdRejectConsentPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **bankId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**OkResponseSchema**](OkResponseSchema.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

