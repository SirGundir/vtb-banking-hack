# UsersApi

All URIs are relative to *http://localhost:4000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**getMeApiV1UsersMeGet**](UsersApi.md#getmeapiv1usersmeget) | **GET** /api/v1/users/me/ | Get Me |



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

