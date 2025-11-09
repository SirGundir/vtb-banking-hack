# DefaultApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**recommendStubApiV1RecommendClientIdPost**](DefaultApi.md#recommendstubapiv1recommendclientidpost) | **POST** /api/v1/recommend/{client_id} | Recommend Stub |



## recommendStubApiV1RecommendClientIdPost

> Array&lt;ProductRecommendation&gt; recommendStubApiV1RecommendClientIdPost(clientId, topN, useMl)

Recommend Stub

### Example

```ts
import {
  Configuration,
  DefaultApi,
} from '';
import type { RecommendStubApiV1RecommendClientIdPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DefaultApi();

  const body = {
    // string
    clientId: clientId_example,
    // number (optional)
    topN: 56,
    // boolean (optional)
    useMl: true,
  } satisfies RecommendStubApiV1RecommendClientIdPostRequest;

  try {
    const data = await api.recommendStubApiV1RecommendClientIdPost(body);
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
| **clientId** | `string` |  | [Defaults to `undefined`] |
| **topN** | `number` |  | [Optional] [Defaults to `3`] |
| **useMl** | `boolean` |  | [Optional] [Defaults to `true`] |

### Return type

[**Array&lt;ProductRecommendation&gt;**](ProductRecommendation.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

