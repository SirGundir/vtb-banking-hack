# AuthApi

All URIs are relative to *http://localhost:8000*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**changePasswordApiV1AuthChangePasswordPost**](AuthApi.md#changepasswordapiv1authchangepasswordpost) | **POST** /api/v1/auth/change-password/ | Change Password |
| [**loginApiV1AuthLoginPost**](AuthApi.md#loginapiv1authloginpost) | **POST** /api/v1/auth/login/ | Login |
| [**logoutApiV1AuthLogoutPost**](AuthApi.md#logoutapiv1authlogoutpost) | **POST** /api/v1/auth/logout/ | Logout |
| [**refreshApiV1AuthRefreshPost**](AuthApi.md#refreshapiv1authrefreshpost) | **POST** /api/v1/auth/refresh/ | Refresh |
| [**resetPasswordApiV1AuthResetFinishUidb64TokenPost**](AuthApi.md#resetpasswordapiv1authresetfinishuidb64tokenpost) | **POST** /api/v1/auth/reset/finish/{uidb64}/{token}/ | Reset Password |
| [**signupApiV1AuthSignupPost**](AuthApi.md#signupapiv1authsignuppost) | **POST** /api/v1/auth/signup/ | Signup |
| [**startResetPasswordApiV1AuthResetStartPost**](AuthApi.md#startresetpasswordapiv1authresetstartpost) | **POST** /api/v1/auth/reset/start/ | Start Reset Password |



## changePasswordApiV1AuthChangePasswordPost

> OkResponseSchema changePasswordApiV1AuthChangePasswordPost(changePasswordDTO)

Change Password

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { ChangePasswordApiV1AuthChangePasswordPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({ 
    // Configure HTTP bearer authorization: HTTPBearer
    accessToken: "YOUR BEARER TOKEN",
  });
  const api = new AuthApi(config);

  const body = {
    // ChangePasswordDTO
    changePasswordDTO: ...,
  } satisfies ChangePasswordApiV1AuthChangePasswordPostRequest;

  try {
    const data = await api.changePasswordApiV1AuthChangePasswordPost(body);
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
| **changePasswordDTO** | [ChangePasswordDTO](ChangePasswordDTO.md) |  | |

### Return type

[**OkResponseSchema**](OkResponseSchema.md)

### Authorization

[HTTPBearer](../README.md#HTTPBearer)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## loginApiV1AuthLoginPost

> JwtTokensSchema loginApiV1AuthLoginPost(loginDTO)

Login

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { LoginApiV1AuthLoginPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthApi();

  const body = {
    // LoginDTO
    loginDTO: ...,
  } satisfies LoginApiV1AuthLoginPostRequest;

  try {
    const data = await api.loginApiV1AuthLoginPost(body);
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
| **loginDTO** | [LoginDTO](LoginDTO.md) |  | |

### Return type

[**JwtTokensSchema**](JwtTokensSchema.md)

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


## logoutApiV1AuthLogoutPost

> OkResponseSchema logoutApiV1AuthLogoutPost(jwtTokensDTO)

Logout

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { LogoutApiV1AuthLogoutPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthApi();

  const body = {
    // JwtTokensDTO
    jwtTokensDTO: ...,
  } satisfies LogoutApiV1AuthLogoutPostRequest;

  try {
    const data = await api.logoutApiV1AuthLogoutPost(body);
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
| **jwtTokensDTO** | [JwtTokensDTO](JwtTokensDTO.md) |  | |

### Return type

[**OkResponseSchema**](OkResponseSchema.md)

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


## refreshApiV1AuthRefreshPost

> JwtTokensSchema refreshApiV1AuthRefreshPost(refreshTokenDTO)

Refresh

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { RefreshApiV1AuthRefreshPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthApi();

  const body = {
    // RefreshTokenDTO
    refreshTokenDTO: ...,
  } satisfies RefreshApiV1AuthRefreshPostRequest;

  try {
    const data = await api.refreshApiV1AuthRefreshPost(body);
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
| **refreshTokenDTO** | [RefreshTokenDTO](RefreshTokenDTO.md) |  | |

### Return type

[**JwtTokensSchema**](JwtTokensSchema.md)

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


## resetPasswordApiV1AuthResetFinishUidb64TokenPost

> OkResponseSchema resetPasswordApiV1AuthResetFinishUidb64TokenPost(uidb64, token, setPasswordDTO)

Reset Password

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { ResetPasswordApiV1AuthResetFinishUidb64TokenPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthApi();

  const body = {
    // string
    uidb64: uidb64_example,
    // string
    token: token_example,
    // SetPasswordDTO
    setPasswordDTO: ...,
  } satisfies ResetPasswordApiV1AuthResetFinishUidb64TokenPostRequest;

  try {
    const data = await api.resetPasswordApiV1AuthResetFinishUidb64TokenPost(body);
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
| **uidb64** | `string` |  | [Defaults to `undefined`] |
| **token** | `string` |  | [Defaults to `undefined`] |
| **setPasswordDTO** | [SetPasswordDTO](SetPasswordDTO.md) |  | |

### Return type

[**OkResponseSchema**](OkResponseSchema.md)

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


## signupApiV1AuthSignupPost

> JwtTokensSchema signupApiV1AuthSignupPost(createUserDTO)

Signup

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { SignupApiV1AuthSignupPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthApi();

  const body = {
    // CreateUserDTO
    createUserDTO: ...,
  } satisfies SignupApiV1AuthSignupPostRequest;

  try {
    const data = await api.signupApiV1AuthSignupPost(body);
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
| **createUserDTO** | [CreateUserDTO](CreateUserDTO.md) |  | |

### Return type

[**JwtTokensSchema**](JwtTokensSchema.md)

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


## startResetPasswordApiV1AuthResetStartPost

> OkResponseSchema startResetPasswordApiV1AuthResetStartPost(resetPasswordDTO)

Start Reset Password

### Example

```ts
import {
  Configuration,
  AuthApi,
} from '';
import type { StartResetPasswordApiV1AuthResetStartPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AuthApi();

  const body = {
    // ResetPasswordDTO
    resetPasswordDTO: ...,
  } satisfies StartResetPasswordApiV1AuthResetStartPostRequest;

  try {
    const data = await api.startResetPasswordApiV1AuthResetStartPost(body);
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
| **resetPasswordDTO** | [ResetPasswordDTO](ResetPasswordDTO.md) |  | |

### Return type

[**OkResponseSchema**](OkResponseSchema.md)

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

