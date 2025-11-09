# UsersApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**getMeApiV1UsersMeGet**](UsersApi.md#getmeapiv1usersmeget) | **GET** /api/v1/users/me/ | Get Me |
| [**getMeTransactionsApiV1UsersMeTransactionsGet**](UsersApi.md#getmetransactionsapiv1usersmetransactionsget) | **GET** /api/v1/users/me/transactions/ | Get Me Transactions |



## getMeApiV1UsersMeGet

> UserSchema getMeApiV1UsersMeGet()

Get Me

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetMeApiV1UsersMeGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new UsersApi(config);

  try {
    const data = await api.getMeApiV1UsersMeGet();
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

[**UserSchema**](UserSchema.md)

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


## getMeTransactionsApiV1UsersMeTransactionsGet

> Array&lt;UserTransactionsSchema&gt; getMeTransactionsApiV1UsersMeTransactionsGet(dateFrom, dateTo, direction)

Get Me Transactions

### Example

```ts
import {
  Configuration,
  UsersApi,
} from '';
import type { GetMeTransactionsApiV1UsersMeTransactionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new UsersApi(config);

  const body = {
    // Date (optional)
    dateFrom: 2013-10-20,
    // Date (optional)
    dateTo: 2013-10-20,
    // string (optional)
    direction: direction_example,
  } satisfies GetMeTransactionsApiV1UsersMeTransactionsGetRequest;

  try {
    const data = await api.getMeTransactionsApiV1UsersMeTransactionsGet(body);
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
| **dateFrom** | `Date` |  | [Optional] [Defaults to `undefined`] |
| **dateTo** | `Date` |  | [Optional] [Defaults to `undefined`] |
| **direction** | `string` |  | [Optional] [Defaults to `undefined`] |

### Return type

[**Array&lt;UserTransactionsSchema&gt;**](UserTransactionsSchema.md)

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

