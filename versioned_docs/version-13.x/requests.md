<!-- # HTTP Requests -->
# HTTP Requests

- [Introduction](#introduction)
- [Interacting With The Request](#interacting-with-the-request)
    - [Accessing the Request](#accessing-the-request)
    - [Request Path, Host, and Method](#request-path-and-method)
    - [Request Headers](#request-headers)
    - [Request IP Address](#request-ip-address)
    - [Content Negotiation](#content-negotiation)
    - [PSR-7 Requests](#psr7-requests)
- [Input](#input)
    - [Retrieving Input](#retrieving-input)
    - [Input Presence](#input-presence)
    - [Merging Additional Input](#merging-additional-input)
    - [Old Input](#old-input)
    - [Cookies](#cookies)
    - [Input Trimming and Normalization](#input-trimming-and-normalization)
- [Files](#files)
    - [Retrieving Uploaded Files](#retrieving-uploaded-files)
    - [Storing Uploaded Files](#storing-uploaded-files)
- [Configuring Trusted Proxies](#configuring-trusted-proxies)
- [Configuring Trusted Hosts](#configuring-trusted-hosts)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's `Illuminate\Http\Request` class provides an object-oriented way to interact with the current HTTP request being handled by your application as well as retrieve the input, cookies, and files that were submitted with the request. -->
Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션에서 현재 처리 중인 HTTP 요청과 상호작용하고, 요청과 함께 제출된 입력값, 쿠키, 파일을 가져올 수 있는 객체 지향 방식을 제공합니다.

<a name="interacting-with-the-request"></a>
<!-- ## Interacting With The Request -->
## Interacting With The Request

<a name="accessing-the-request"></a>
<!-- ### Accessing the Request -->
### Accessing the Request

<!-- To obtain an instance of the current HTTP request via dependency injection, you should type-hint the `Illuminate\Http\Request` class on your route closure or controller method. The incoming request instance will automatically be injected by the Laravel [service container](/docs/13.x/container): -->
의존성 주입을 통해 현재 HTTP 요청 인스턴스를 얻으려면 라우트 클로저나 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스 타입을 지정해야 합니다. 들어오는 요청 인스턴스는 Laravel [service container](/docs/13.x/container)에 의해 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // Store the user...

        return redirect('/users');
    }
}
```

<!-- As mentioned, you may also type-hint the `Illuminate\Http\Request` class on a route closure. The service container will automatically inject the incoming request into the closure when it is executed: -->
앞서 언급했듯이 라우트 클로저에서도 `Illuminate\Http\Request` 클래스 타입을 지정할 수 있습니다. 서비스 컨테이너는 클로저가 실행될 때 들어오는 요청을 클로저에 자동으로 주입합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
<!-- #### Dependency Injection and Route Parameters -->
#### Dependency Injection and Route Parameters

<!-- If your controller method is also expecting input from a route parameter you should list your route parameters after your other dependencies. For example, if your route is defined like so: -->
컨트롤러 메서드가 라우트 파라미터의 입력도 기대한다면, 다른 의존성 뒤에 라우트 파라미터를 나열해야 합니다. 예를 들어 라우트가 다음과 같이 정의되어 있다고 가정해 보겠습니다.

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` route parameter by defining your controller method as follows: -->
다음처럼 컨트롤러 메서드를 정의하면 여전히 `Illuminate\Http\Request` 타입을 지정하면서 `id` 라우트 파라미터에도 접근할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the specified user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
<!-- ### Request Path, Host, and Method -->
### Request Path, Host, and Method

<!-- The `Illuminate\Http\Request` instance provides a variety of methods for examining the incoming HTTP request and extends the `Symfony\Component\HttpFoundation\Request` class. We will discuss a few of the most important methods below. -->
`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 살펴볼 수 있는 다양한 메서드를 제공하며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 아래에서는 가장 중요한 메서드 몇 가지를 살펴보겠습니다.

<a name="retrieving-the-request-path"></a>
<!-- #### Retrieving the Request Path -->
#### Retrieving the Request Path

<!-- The `path` method returns the request's path information. So, if the incoming request is targeted at `http://example.com/foo/bar`, the `path` method will return `foo/bar`: -->
`path` 메서드는 요청의 경로 정보를 반환합니다. 따라서 들어오는 요청이 `http://example.com/foo/bar`를 대상으로 한다면 `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
<!-- #### Inspecting the Request Path / Route -->
#### Inspecting the Request Path / Route

<!-- The `is` method allows you to verify that the incoming request path matches a given pattern. You may use the `*` character as a wildcard when utilizing this method: -->
`is` 메서드를 사용하면 들어오는 요청 경로가 주어진 패턴과 일치하는지 확인할 수 있습니다. 이 메서드를 사용할 때 `*` 문자를 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

<!-- Using the `routeIs` method, you may determine if the incoming request has matched a [named route](/docs/13.x/routing#named-routes): -->
`routeIs` 메서드를 사용하면 들어오는 요청이 [named route](/docs/13.x/routing#named-routes)와 일치했는지 확인할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
<!-- #### Retrieving the Request URL -->
#### Retrieving the Request URL

<!-- To retrieve the full URL for the incoming request you may use the `url` or `fullUrl` methods. The `url` method will return the URL without the query string, while the `fullUrl` method includes the query string: -->
들어오는 요청의 전체 URL을 조회하려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리 문자열을 제외한 URL을 반환하고, `fullUrl` 메서드는 쿼리 문자열을 포함합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

<!-- If you would like to append query string data to the current URL, you may call the `fullUrlWithQuery` method. This method merges the given array of query string variables with the current query string: -->
현재 URL에 쿼리 문자열 데이터를 추가하고 싶다면 `fullUrlWithQuery` 메서드를 호출할 수 있습니다. 이 메서드는 주어진 쿼리 문자열 변수 배열을 현재 쿼리 문자열과 병합합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

<!-- If you would like to get the current URL without a given query string parameter, you may utilize the `fullUrlWithoutQuery` method: -->
주어진 쿼리 문자열 파라미터를 제외한 현재 URL을 가져오고 싶다면 `fullUrlWithoutQuery` 메서드를 사용할 수 있습니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
<!-- #### Retrieving the Request Host -->
#### Retrieving the Request Host

<!-- You may retrieve the "host" of the incoming request via the `host`, `httpHost`, and `schemeAndHttpHost` methods: -->
`host`, `httpHost`, `schemeAndHttpHost` 메서드를 통해 들어오는 요청의 "host"를 조회할 수 있습니다.

```php
// http://localhost:8000
$request->host(); // localhost
$request->httpHost(); // localhost:8000
$request->schemeAndHttpHost(); // http://localhost:8000
```

<a name="retrieving-the-request-method"></a>
<!-- #### Retrieving the Request Method -->
#### Retrieving the Request Method

<!-- The `method` method will return the HTTP verb for the request. You may use the `isMethod` method to verify that the HTTP verb matches a given string: -->
`method` 메서드는 요청의 HTTP 동사를 반환합니다. `isMethod` 메서드를 사용하면 HTTP 동사가 주어진 문자열과 일치하는지 확인할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
<!-- ### Request Headers -->
### Request Headers

<!-- You may retrieve a request header from the `Illuminate\Http\Request` instance using the `header` method. If the header is not present on the request, `null` will be returned. However, the `header` method accepts an optional second argument that will be returned if the header is not present on the request: -->
`header` 메서드를 사용하여 `Illuminate\Http\Request` 인스턴스에서 요청 헤더를 조회할 수 있습니다. 요청에 해당 헤더가 없으면 `null`이 반환됩니다. 하지만 `header` 메서드는 선택적인 두 번째 인수를 받으며, 요청에 해당 헤더가 없을 때 이 값이 반환됩니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

<!-- The `hasHeader` method may be used to determine if the request contains a given header: -->
`hasHeader` 메서드를 사용하면 요청에 주어진 헤더가 포함되어 있는지 확인할 수 있습니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

<!-- For convenience, the `bearerToken` method may be used to retrieve a bearer token from the `Authorization` header. If no such header is present, an empty string will be returned: -->
편의를 위해 `bearerToken` 메서드를 사용하여 `Authorization` 헤더에서 Bearer 토큰을 조회할 수 있습니다. 해당 헤더가 없으면 빈 문자열이 반환됩니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
<!-- ### Request IP Address -->
### Request IP Address

<!-- The `ip` method may be used to retrieve the IP address of the client that made the request to your application: -->
`ip` 메서드를 사용하면 애플리케이션에 요청을 보낸 클라이언트의 IP 주소를 조회할 수 있습니다.

```php
$ipAddress = $request->ip();
```

<!-- If you would like to retrieve an array of IP addresses, including all of the client IP addresses that were forwarded by proxies, you may use the `ips` method. The "original" client IP address will be at the end of the array: -->
프록시를 통해 전달된 모든 클라이언트 IP 주소를 포함하여 IP 주소 배열을 조회하고 싶다면 `ips` 메서드를 사용할 수 있습니다. "원래" 클라이언트 IP 주소는 배열의 끝에 위치합니다.

```php
$ipAddresses = $request->ips();
```

<!-- In general, IP addresses should be considered untrusted, user-controlled input and be used for informational purposes only. -->
일반적으로 IP 주소는 신뢰할 수 없는 사용자 제어 입력값으로 간주해야 하며, 정보 제공 목적으로만 사용해야 합니다.

<a name="content-negotiation"></a>
<!-- ### Content Negotiation -->
### Content Negotiation

<!-- Laravel provides several methods for inspecting the incoming request's requested content types via the `Accept` header. First, the `getAcceptableContentTypes` method will return an array containing all of the content types accepted by the request: -->
Laravel은 `Accept` 헤더를 통해 들어오는 요청이 요구하는 콘텐츠 타입을 검사할 수 있는 여러 메서드를 제공합니다. 먼저 `getAcceptableContentTypes` 메서드는 요청이 허용하는 모든 콘텐츠 타입을 담은 배열을 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

<!-- The `accepts` method accepts an array of content types and returns `true` if any of the content types are accepted by the request. Otherwise, `false` will be returned: -->
`accepts` 메서드는 콘텐츠 타입 배열을 받고, 그중 하나라도 요청에서 허용되면 `true`를 반환합니다. 그렇지 않으면 `false`가 반환됩니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

<!-- You may use the `prefers` method to determine which content type out of a given array of content types is most preferred by the request. If none of the provided content types are accepted by the request, `null` will be returned: -->
`prefers` 메서드를 사용하면 주어진 콘텐츠 타입 배열 중 요청이 가장 선호하는 콘텐츠 타입을 확인할 수 있습니다. 제공된 콘텐츠 타입 중 요청에서 허용하는 것이 없다면 `null`이 반환됩니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

<!-- Since many applications only serve HTML or JSON, you may use the `expectsJson` method to quickly determine if the incoming request expects a JSON response: -->
많은 애플리케이션이 HTML 또는 JSON만 제공하므로, `expectsJson` 메서드를 사용하면 들어오는 요청이 JSON 응답을 기대하는지 빠르게 확인할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<!-- If you need to determine whether the request specifically prefers Markdown or will accept Markdown among other content types, such as when serving AI agents or other clients that consume Markdown responses, you may use the `wantsMarkdown` and `acceptsMarkdown` methods: -->
AI 에이전트나 Markdown 응답을 소비하는 다른 클라이언트에 응답을 제공하는 경우처럼, 요청이 특별히 Markdown을 선호하는지 또는 다른 콘텐츠 타입과 함께 Markdown을 허용하는지 확인해야 한다면 `wantsMarkdown` 및 `acceptsMarkdown` 메서드를 사용할 수 있습니다.

```php
if ($request->wantsMarkdown()) {
    // The client's most preferred content type is text/markdown...
}

if ($request->acceptsMarkdown()) {
    // The client accepts Markdown responses...
}
```

<a name="psr7-requests"></a>
<!-- ### PSR-7 Requests -->
### PSR-7 Requests

<!-- The [PSR-7 standard](https://www.php-fig.org/psr/psr-7/) specifies interfaces for HTTP messages, including requests and responses. If you would like to obtain an instance of a PSR-7 request instead of a Laravel request, you will first need to install a few libraries. Laravel uses the *Symfony HTTP Message Bridge* component to convert typical Laravel requests and responses into PSR-7 compatible implementations: -->
[PSR-7 standard](https://www.php-fig.org/psr/psr-7/)은 요청과 응답을 포함한 HTTP 메시지 인터페이스를 정의합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻고 싶다면 먼저 몇 가지 라이브러리를 설치해야 합니다. Laravel은 일반적인 Laravel 요청과 응답을 PSR-7 호환 구현으로 변환하기 위해 *Symfony HTTP Message Bridge* 컴포넌트를 사용합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

<!-- Once you have installed these libraries, you may obtain a PSR-7 request by type-hinting the request interface on your route closure or controller method: -->
이 라이브러리들을 설치한 뒤에는 라우트 클로저나 컨트롤러 메서드에서 요청 인터페이스 타입을 지정하여 PSR-7 요청을 얻을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 이를 자동으로 Laravel 응답 인스턴스로 다시 변환하여 표시합니다.

<a name="input"></a>
<!-- ## Input -->
## Input

<a name="retrieving-input"></a>
<!-- ### Retrieving Input -->
### Retrieving Input

<a name="retrieving-all-input-data"></a>
<!-- #### Retrieving All Input Data -->
#### Retrieving All Input Data

<!-- You may retrieve all of the incoming request's input data as an `array` using the `all` method. This method may be used regardless of whether the incoming request is from an HTML form or is an XHR request: -->
`all` 메서드를 사용하면 들어오는 요청의 모든 입력 데이터를 `array`로 조회할 수 있습니다. 이 메서드는 들어오는 요청이 HTML 폼에서 온 것인지 XHR 요청인지와 관계없이 사용할 수 있습니다.

```php
$input = $request->all();
```

<!-- Using the `collect` method, you may retrieve all of the incoming request's input data as a [collection](/docs/13.x/collections): -->
`collect` 메서드를 사용하면 들어오는 요청의 모든 입력 데이터를 [collection](/docs/13.x/collections)으로 조회할 수 있습니다.

```php
$input = $request->collect();
```

<!-- The `collect` method also allows you to retrieve a subset of the incoming request's input as a collection: -->
`collect` 메서드를 사용하면 들어오는 요청 입력값의 일부만 컬렉션으로 조회할 수도 있습니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
<!-- #### Retrieving an Input Value -->
#### Retrieving an Input Value

<!-- Using a few simple methods, you may access all of the user input from your `Illuminate\Http\Request` instance without worrying about which HTTP verb was used for the request. Regardless of the HTTP verb, the `input` method may be used to retrieve user input: -->
몇 가지 간단한 메서드를 사용하면 요청에 어떤 HTTP 동사가 사용되었는지 신경 쓰지 않고 `Illuminate\Http\Request` 인스턴스에서 모든 사용자 입력값에 접근할 수 있습니다. HTTP 동사와 관계없이 `input` 메서드를 사용하여 사용자 입력값을 조회할 수 있습니다.

```php
$name = $request->input('name');
```

<!-- You may pass a default value as the second argument to the `input` method. This value will be returned if the requested input value is not present on the request: -->
`input` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 요청에 조회하려는 입력값이 없으면 이 값이 반환됩니다.

```php
$name = $request->input('name', 'Sally');
```

<!-- When working with forms that contain array inputs, use "dot" notation to access the arrays: -->
배열 입력을 포함하는 폼을 다룰 때는 "dot" 표기법을 사용하여 배열에 접근합니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

<!-- You may call the `input` method without any arguments in order to retrieve all of the input values as an associative array: -->
모든 입력값을 연관 배열로 조회하려면 아무 인수 없이 `input` 메서드를 호출할 수 있습니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
<!-- #### Retrieving Input From the Query String -->
#### Retrieving Input From the Query String

<!-- While the `input` method retrieves values from the entire request payload (including the query string), the `query` method will only retrieve values from the query string: -->
`input` 메서드는 전체 요청 페이로드(쿼리 문자열 포함)에서 값을 조회하지만, `query` 메서드는 쿼리 문자열에서만 값을 조회합니다.

```php
$name = $request->query('name');
```

<!-- If the requested query string value data is not present, the second argument to this method will be returned: -->
요청한 쿼리 문자열 값 데이터가 없으면 이 메서드의 두 번째 인수가 반환됩니다.

```php
$name = $request->query('name', 'Helen');
```

<!-- You may call the `query` method without any arguments in order to retrieve all of the query string values as an associative array: -->
모든 쿼리 문자열 값을 연관 배열로 조회하려면 아무 인수 없이 `query` 메서드를 호출할 수 있습니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
<!-- #### Retrieving JSON Input Values -->
#### Retrieving JSON Input Values

<!-- When sending JSON requests to your application, you may access the JSON data via the `input` method as long as the `Content-Type` header of the request is properly set to `application/json`. You may even use "dot" syntax to retrieve values that are nested within JSON arrays / objects: -->
애플리케이션에 JSON 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 설정되어 있다면 `input` 메서드를 통해 JSON 데이터에 접근할 수 있습니다. "dot" 문법을 사용하여 JSON 배열 / 객체 안에 중첩된 값을 조회할 수도 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
<!-- #### Retrieving Stringable Input Values -->
#### Retrieving Stringable Input Values

<!-- Instead of retrieving the request's input data as a primitive `string`, you may use the `string` method to retrieve the request data as an instance of [Illuminate\Support\Stringable](/docs/13.x/strings): -->
요청의 입력 데이터를 원시 `string`으로 조회하는 대신, `string` 메서드를 사용하여 요청 데이터를 [Illuminate\Support\Stringable](/docs/13.x/strings) 인스턴스로 조회할 수 있습니다.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
<!-- #### Retrieving Integer Input Values -->
#### Retrieving Integer Input Values

<!-- To retrieve input values as integers, you may use the `integer` method. This method will attempt to cast the input value to an integer. If the input is not present or the cast fails, it will return the default value you specify. This is particularly useful for pagination or other numeric inputs: -->
입력값을 정수로 조회하려면 `integer` 메서드를 사용할 수 있습니다. 이 메서드는 입력값을 정수로 casting하려고 시도합니다. 입력값이 없거나 casting에 실패하면 지정한 기본값을 반환합니다. 이 메서드는 특히 페이지네이션이나 기타 숫자 입력값에 유용합니다.

```php
$perPage = $request->integer('per_page');
```
<a name="retrieving-boolean-input-values"></a>
<!-- #### Retrieving Boolean Input Values -->
#### Retrieving Boolean Input Values

<!-- When dealing with HTML elements like checkboxes, your application may receive "truthy" values that are actually strings. For example, "true" or "on". For convenience, you may use the `boolean` method to retrieve these values as booleans. The `boolean` method returns `true` for 1, "1", true, "true", "on", and "yes". All other values will return `false`: -->
체크박스와 같은 HTML 요소를 다룰 때 애플리케이션은 실제로는 문자열인 "truthy"(참으로 평가되는) 값을 받을 수 있습니다. 예를 들어 "true" 또는 "on" 같은 값입니다. 편의를 위해 `boolean` 메서드를 사용하여 이러한 값을 불리언으로 조회할 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes"에 대해 `true`를 반환합니다. 그 외의 모든 값은 `false`를 반환합니다:

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
<!-- #### Retrieving Array Input Values -->
#### Retrieving Array Input Values

<!-- Input values containing arrays may be retrieved using the `array` method. This method will always cast the input value to an array. If the request does not contain an input value with the given name, an empty array will be returned: -->
배열을 포함하는 입력 값은 `array` 메서드를 사용하여 조회할 수 있습니다. 이 메서드는 항상 입력 값을 배열로 형 변환합니다. 요청에 주어진 이름의 입력 값이 포함되어 있지 않으면 빈 배열이 반환됩니다:

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
<!-- #### Retrieving Date Input Values -->
#### Retrieving Date Input Values

<!-- For convenience, input values containing dates / times may be retrieved as Carbon instances using the `date` method. If the request does not contain an input value with the given name, `null` will be returned: -->
편의를 위해 날짜 / 시간을 포함하는 입력 값은 `date` 메서드를 사용하여 Carbon 인스턴스로 조회할 수 있습니다. 요청에 주어진 이름의 입력 값이 포함되어 있지 않으면 `null`이 반환됩니다:

```php
$birthday = $request->date('birthday');
```

<!-- The second and third arguments accepted by the `date` method may be used to specify the date's format and timezone, respectively: -->
`date` 메서드가 받는 두 번째와 세 번째 인수는 각각 날짜의 형식과 시간대를 지정하는 데 사용할 수 있습니다:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

<!-- If the input value is present but has an invalid format, an `InvalidArgumentException` will be thrown; therefore, it is recommended that you validate the input before invoking the `date` method. -->
입력 값이 존재하지만 형식이 유효하지 않으면 `InvalidArgumentException`이 발생합니다. 따라서 `date` 메서드를 호출하기 전에 입력 값을 유효성 검증하는 것이 좋습니다.

<a name="retrieving-interval-input-values"></a>
<!-- #### Retrieving Interval Input Values -->
#### Retrieving Interval Input Values

<!-- Input values containing durations may be retrieved as `CarbonInterval` instances using the `interval` method. If the request does not contain an input value with the given name, `null` will be returned: -->
기간을 포함하는 입력 값은 `interval` 메서드를 사용하여 `CarbonInterval` 인스턴스로 조회할 수 있습니다. 요청에 주어진 이름의 입력 값이 포함되어 있지 않으면 `null`이 반환됩니다:

```php
$duration = $request->interval('duration');
```

<!-- If the input value is numeric, you may provide a unit as the second argument. The unit may be a string such as `second`, `minute`, or `day`, or a `Carbon\Unit` enum instance: -->
입력 값이 숫자인 경우 두 번째 인수로 단위를 제공할 수 있습니다. 단위는 `second`, `minute`, `day` 같은 문자열이거나 `Carbon\Unit` enum 인스턴스일 수 있습니다:

```php
use Carbon\Unit;

$timeout = $request->interval('timeout', 'second');

$delay = $request->interval('delay', Unit::Minute);
```

<!-- If the input value is present but has an invalid format, an `InvalidArgumentException` will be thrown; therefore, it is recommended that you validate the input before invoking the `interval` method. -->
입력 값이 존재하지만 형식이 유효하지 않으면 `InvalidArgumentException`이 발생합니다. 따라서 `interval` 메서드를 호출하기 전에 입력 값을 유효성 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
<!-- #### Retrieving Enum Input Values -->
#### Retrieving Enum Input Values

<!-- Input values that correspond to [PHP enums](https://www.php.net/manual/en/language.types.enumerations.php) may also be retrieved from the request. If the request does not contain an input value with the given name or the enum does not have a backing value that matches the input value, `null` will be returned. The `enum` method accepts the name of the input value and the enum class as its first and second arguments: -->
[PHP enums](https://www.php.net/manual/en/language.types.enumerations.php)에 해당하는 입력 값도 요청에서 조회할 수 있습니다. 요청에 주어진 이름의 입력 값이 포함되어 있지 않거나, enum에 입력 값과 일치하는 backing value(백킹 값)가 없으면 `null`이 반환됩니다. `enum` 메서드는 첫 번째 인수로 입력 값의 이름을, 두 번째 인수로 enum 클래스를 받습니다:

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

<!-- You may also provide a default value that will be returned if the value is missing or invalid: -->
값이 없거나 유효하지 않을 때 반환할 기본값을 제공할 수도 있습니다:

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

<!-- If the input value is an array of values that correspond to a PHP enum, you may use the `enums` method to retrieve the array of values as enum instances: -->
입력 값이 PHP enum에 해당하는 값들의 배열이라면, `enums` 메서드를 사용하여 값 배열을 enum 인스턴스 배열로 조회할 수 있습니다:

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
<!-- #### Retrieving Input via Dynamic Properties -->
#### Retrieving Input via Dynamic Properties

<!-- You may also access user input using dynamic properties on the `Illuminate\Http\Request` instance. For example, if one of your application's forms contains a `name` field, you may access the value of the field like so: -->
`Illuminate\Http\Request` 인스턴스의 동적 속성을 사용하여 사용자 입력에 접근할 수도 있습니다. 예를 들어 애플리케이션의 폼 중 하나에 `name` 필드가 있다면, 다음과 같이 해당 필드의 값에 접근할 수 있습니다:

```php
$name = $request->name;
```

<!-- When using dynamic properties, Laravel will first look for the parameter's value in the request payload. If it is not present, Laravel will search for the field in the matched route's parameters. -->
동적 속성을 사용할 때 Laravel은 먼저 요청 페이로드에서 해당 파라미터 값을 찾습니다. 값이 없으면 Laravel은 일치한 라우트의 파라미터에서 해당 필드를 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
<!-- #### Retrieving a Portion of the Input Data -->
#### Retrieving a Portion of the Input Data

<!-- If you need to retrieve a subset of the input data, you may use the `only` and `except` methods. Both of these methods accept a single `array` or a dynamic list of arguments: -->
입력 데이터의 하위 집합을 조회해야 한다면 `only`와 `except` 메서드를 사용할 수 있습니다. 두 메서드 모두 단일 `array` 또는 동적인 인수 목록을 받습니다:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청한 모든 키 / 값 쌍을 반환합니다. 다만 요청에 존재하지 않는 키 / 값 쌍은 반환하지 않습니다.

<a name="input-presence"></a>
<!-- ### Input Presence -->
### Input Presence

<!-- You may use the `has` method to determine if a value is present on the request. The `has` method returns `true` if the value is present on the request: -->
요청에 값이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 요청에 값이 존재하면 `true`를 반환합니다:

```php
if ($request->has('name')) {
    // ...
}
```

<!-- When given an array, the `has` method will determine if all of the specified values are present: -->
배열이 주어지면 `has` 메서드는 지정된 값이 모두 존재하는지 확인합니다:

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

<!-- The `hasAny` method returns `true` if any of the specified values are present: -->
`hasAny` 메서드는 지정된 값 중 하나라도 존재하면 `true`를 반환합니다:

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

<!-- The `whenHas` method will execute the given closure if a value is present on the request: -->
`whenHas` 메서드는 요청에 값이 존재하면 주어진 클로저를 실행합니다:

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

<!-- A second closure may be passed to the `whenHas` method that will be executed if the specified value is not present on the request: -->
지정된 값이 요청에 존재하지 않을 때 실행할 두 번째 클로저를 `whenHas` 메서드에 전달할 수도 있습니다:

```php
$request->whenHas('name', function (string $input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```

<!-- If you would like to determine if a value is present on the request and is not an empty string, you may use the `filled` method: -->
요청에 값이 존재하고 빈 문자열이 아닌지 확인하려면 `filled` 메서드를 사용할 수 있습니다:

```php
if ($request->filled('name')) {
    // ...
}
```

<!-- If you would like to determine if a value is missing from the request or is an empty string, you may use the `isNotFilled` method: -->
요청에서 값이 누락되었거나 빈 문자열인지 확인하려면 `isNotFilled` 메서드를 사용할 수 있습니다:

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

<!-- When given an array, the `isNotFilled` method will determine if all of the specified values are missing or empty: -->
배열이 주어지면 `isNotFilled` 메서드는 지정된 값이 모두 누락되었거나 비어 있는지 확인합니다:

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

<!-- The `anyFilled` method returns `true` if any of the specified values is not an empty string: -->
`anyFilled` 메서드는 지정된 값 중 하나라도 빈 문자열이 아니면 `true`를 반환합니다:

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

<!-- The `whenFilled` method will execute the given closure if a value is present on the request and is not an empty string: -->
`whenFilled` 메서드는 요청에 값이 존재하고 빈 문자열이 아니면 주어진 클로저를 실행합니다:

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

<!-- A second closure may be passed to the `whenFilled` method that will be executed if the specified value is not "filled": -->
지정된 값이 "filled" 상태가 아닐 때 실행할 두 번째 클로저를 `whenFilled` 메서드에 전달할 수도 있습니다:

```php
$request->whenFilled('name', function (string $input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```

<!-- To determine if a given key is absent from the request, you may use the `missing` and `whenMissing` methods: -->
주어진 키가 요청에 없는지 확인하려면 `missing`과 `whenMissing` 메서드를 사용할 수 있습니다:

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // The "name" value is missing...
}, function () {
    // The "name" value is present...
});
```

<a name="merging-additional-input"></a>
<!-- ### Merging Additional Input -->
### Merging Additional Input

<!-- Sometimes you may need to manually merge additional input into the request's existing input data. To accomplish this, you may use the `merge` method. If a given input key already exists on the request, it will be overwritten by the data provided to the `merge` method: -->
때로는 요청의 기존 입력 데이터에 추가 입력을 수동으로 병합해야 할 수 있습니다. 이를 위해 `merge` 메서드를 사용할 수 있습니다. 주어진 입력 키가 요청에 이미 존재하면 `merge` 메서드에 제공된 데이터로 덮어씁니다:

```php
$request->merge(['votes' => 0]);
```

<!-- The `mergeIfMissing` method may be used to merge input into the request if the corresponding keys do not already exist within the request's input data: -->
해당 키가 요청의 입력 데이터에 아직 존재하지 않을 때만 입력을 병합하려면 `mergeIfMissing` 메서드를 사용할 수 있습니다:

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
<!-- ### Old Input -->
### Old Input

<!-- Laravel allows you to keep input from one request during the next request. This feature is particularly useful for re-populating forms after detecting validation errors. However, if you are using Laravel's included [validation features](/docs/13.x/validation), it is possible that you will not need to manually use these session input flashing methods directly, as some of Laravel's built-in validation facilities will call them automatically. -->
Laravel은 한 요청의 입력을 다음 요청 동안 유지할 수 있게 해 줍니다. 이 기능은 유효성 검증 오류를 감지한 후 폼을 다시 채울 때 특히 유용합니다. 하지만 Laravel에 포함된 [validation features](/docs/13.x/validation)을 사용하고 있다면, Laravel의 일부 내장 유효성 검증 기능이 이러한 세션 입력 플래시 메서드를 자동으로 호출하므로 직접 사용할 필요가 없을 수 있습니다.

<a name="flashing-input-to-the-session"></a>
<!-- #### Flashing Input to the Session -->
#### Flashing Input to the Session

<!-- The `flash` method on the `Illuminate\Http\Request` class will flash the current input to the [session](/docs/13.x/session) so that it is available during the user's next request to the application: -->
`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력을 [session](/docs/13.x/session)에 플래시하여, 사용자의 다음 애플리케이션 요청 중에 사용할 수 있게 합니다:

```php
$request->flash();
```

<!-- You may also use the `flashOnly` and `flashExcept` methods to flash a subset of the request data to the session. These methods are useful for keeping sensitive information such as passwords out of the session: -->
`flashOnly`와 `flashExcept` 메서드를 사용하여 요청 데이터의 하위 집합만 세션에 플래시할 수도 있습니다. 이 메서드는 비밀번호 같은 민감한 정보를 세션에 저장하지 않도록 할 때 유용합니다:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
<!-- #### Flashing Input Then Redirecting -->
#### Flashing Input Then Redirecting

<!-- Since you often will want to flash input to the session and then redirect to the previous page, you may easily chain input flashing onto a redirect using the `withInput` method: -->
입력을 세션에 플래시한 다음 이전 페이지로 리다이렉트하고 싶은 경우가 많으므로, `withInput` 메서드를 사용하여 리다이렉트에 입력 플래시를 쉽게 체이닝할 수 있습니다:

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
<!-- #### Retrieving Old Input -->
#### Retrieving Old Input

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/13.x/session): -->
이전 요청에서 플래시된 입력을 조회하려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출합니다. `old` 메서드는 이전에 플래시된 입력 데이터를 [session](/docs/13.x/session)에서 가져옵니다:

```php
$username = $request->old('username');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/13.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
Laravel은 전역 `old` 헬퍼도 제공합니다. [Blade template](/docs/13.x/blade) 안에서 이전 입력을 표시하는 경우, 폼을 다시 채우기 위해 `old` 헬퍼를 사용하는 것이 더 편리합니다. 주어진 필드에 대한 이전 입력이 없으면 `null`이 반환됩니다:

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
<!-- ### Cookies -->
### Cookies

<a name="retrieving-cookies-from-requests"></a>
<!-- #### Retrieving Cookies From Requests -->
#### Retrieving Cookies From Requests

<!-- All cookies created by the Laravel framework are encrypted and signed with an authentication code, meaning they will be considered invalid if they have been changed by the client. To retrieve a cookie value from the request, use the `cookie` method on an `Illuminate\Http\Request` instance: -->
Laravel 프레임워크가 생성한 모든 쿠키는 암호화되고 인증 코드로 서명됩니다. 따라서 클라이언트가 쿠키를 변경했다면 유효하지 않은 것으로 간주됩니다. 요청에서 쿠키 값을 조회하려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용합니다:

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
<!-- ## Input Trimming and Normalization -->
## Input Trimming and Normalization

<!-- By default, Laravel includes the `Illuminate\Foundation\Http\Middleware\TrimStrings` and `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` middleware in your application's global middleware stack. These middleware will automatically trim all incoming string fields on the request, as well as convert any empty string fields to `null`. This allows you to not have to worry about these normalization concerns in your routes and controllers. -->
기본적으로 Laravel은 애플리케이션의 전역 미들웨어 스택에 `Illuminate\Foundation\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 미들웨어는 요청으로 들어오는 모든 문자열 필드를 자동으로 트리밍하고, 빈 문자열 필드를 `null`로 변환합니다. 덕분에 라우트와 컨트롤러에서 이러한 정규화 문제를 신경 쓰지 않아도 됩니다.

<!-- #### Disabling Input Normalization -->
#### Disabling Input Normalization

<!-- If you would like to disable this behavior for all requests, you may remove the two middleware from your application's middleware stack by invoking the `$middleware->remove` method in your application's `bootstrap/app.php` file: -->
모든 요청에 대해 이 동작을 비활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드를 호출하여 두 미들웨어를 애플리케이션의 미들웨어 스택에서 제거할 수 있습니다:

```php
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```

<!-- If you would like to disable string trimming and empty string conversion for a subset of requests to your application, you may use the `trimStrings` and `convertEmptyStringsToNull` middleware methods within your application's `bootstrap/app.php` file. Both methods accept an array of closures, which should return `true` or `false` to indicate whether input normalization should be skipped: -->
애플리케이션으로 들어오는 요청 중 일부에 대해서만 문자열 트리밍과 빈 문자열 변환을 비활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `trimStrings`와 `convertEmptyStringsToNull` 미들웨어 메서드를 사용할 수 있습니다. 두 메서드 모두 클로저 배열을 받으며, 각 클로저는 입력 정규화를 건너뛸지 여부를 나타내기 위해 `true` 또는 `false`를 반환해야 합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->convertEmptyStringsToNull(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);

    $middleware->trimStrings(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);
})
```

<a name="files"></a>
<!-- ## Files -->
## Files

<a name="retrieving-uploaded-files"></a>
<!-- ### Retrieving Uploaded Files -->
### Retrieving Uploaded Files

<!-- You may retrieve uploaded files from an `Illuminate\Http\Request` instance using the `file` method or using dynamic properties. The `file` method returns an instance of the `Illuminate\Http\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file: -->
`file` 메서드나 동적 속성을 사용하여 `Illuminate\Http\Request` 인스턴스에서 업로드된 파일을 조회할 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 클래스의 인스턴스를 반환합니다. 이 클래스는 PHP `SplFileInfo` 클래스를 확장하며, 파일과 상호작용하기 위한 다양한 메서드를 제공합니다:

```php
$file = $request->file('photo');

$file = $request->photo;
```

<!-- You may determine if a file is present on the request using the `hasFile` method: -->
요청에 파일이 존재하는지 확인하려면 `hasFile` 메서드를 사용할 수 있습니다:

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<!-- If the uploaded file is an image that you need to manipulate before storing, you may use the `image` method to retrieve an `Illuminate\Image\Image` instance, or `null` if the file is not present: -->
업로드한 파일이 이미지이며 저장하기 전에 조작해야 한다면 `image` 메서드를 사용해 `Illuminate\Image\Image` 인스턴스를 가져올 수 있습니다. 파일이 없으면 `null`을 반환합니다:

```php
$image = $request->image('photo');
```

<!-- For more information on manipulating images, please consult the complete [image manipulation documentation](/docs/13.x/images). -->
이미지 조작에 대한 자세한 내용은 전체 [image manipulation documentation](/docs/13.x/images)를 참조하세요.

<a name="validating-successful-uploads"></a>
<!-- #### Validating Successful Uploads -->
#### Validating Successful Uploads

<!-- In addition to checking if the file is present, you may verify that there were no problems uploading the file via the `isValid` method: -->
파일이 존재하는지 확인하는 것 외에도, `isValid` 메서드를 통해 파일 업로드 중 문제가 없었는지 확인할 수 있습니다:

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
<!-- #### File Paths and Extensions -->
#### File Paths and Extensions

<!-- The `UploadedFile` class also contains methods for accessing the file's fully-qualified path and its extension. The `extension` method will attempt to guess the file's extension based on its contents. This extension may be different from the extension that was supplied by the client: -->
`UploadedFile` 클래스에는 파일의 정규화된 전체 경로와 확장자에 접근하는 메서드도 포함되어 있습니다. `extension` 메서드는 파일의 내용을 기반으로 파일 확장자를 추측하려고 시도합니다. 이 확장자는 클라이언트가 제공한 확장자와 다를 수 있습니다:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
<!-- #### Other File Methods -->
#### Other File Methods

<!-- There are a variety of other methods available on `UploadedFile` instances. Check out the [API documentation for the class](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php) for more information regarding these methods. -->
`UploadedFile` 인스턴스에서 사용할 수 있는 다양한 다른 메서드가 있습니다. 이러한 메서드에 대한 자세한 내용은 [API documentation for the class](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 확인하십시오.

<a name="storing-uploaded-files"></a>
<!-- ### Storing Uploaded Files -->
### Storing Uploaded Files

<!-- To store an uploaded file, you will typically use one of your configured [filesystems](/docs/13.x/filesystem). The `UploadedFile` class has a `store` method that will move an uploaded file to one of your disks, which may be a location on your local filesystem or a cloud storage location like Amazon S3. -->
업로드된 파일을 저장하려면 일반적으로 설정된 [filesystems](/docs/13.x/filesystem) 중 하나를 사용합니다. `UploadedFile` 클래스에는 업로드된 파일을 디스크 중 하나로 이동하는 `store` 메서드가 있습니다. 이 디스크는 로컬 파일 시스템의 위치일 수도 있고 Amazon S3 같은 클라우드 스토리지 위치일 수도 있습니다.

<!-- The `store` method accepts the path where the file should be stored relative to the filesystem's configured root directory. This path should not contain a filename, since a unique ID will automatically be generated to serve as the filename. -->
`store` 메서드는 파일 시스템에 설정된 루트 디렉터리를 기준으로 파일을 저장할 경로를 받습니다. 이 경로에는 파일명이 포함되어서는 안 됩니다. 파일명으로 사용할 고유 ID가 자동으로 생성되기 때문입니다.

<!-- The `store` method also accepts an optional second argument for the name of the disk that should be used to store the file. The method will return the path of the file relative to the disk's root: -->
`store` 메서드는 파일을 저장하는 데 사용할 디스크 이름을 선택적인 두 번째 인수로 받을 수도 있습니다. 이 메서드는 디스크의 루트를 기준으로 한 파일 경로를 반환합니다:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

<!-- If you do not want a filename to be automatically generated, you may use the `storeAs` method, which accepts the path, filename, and disk name as its arguments: -->
파일명이 자동으로 생성되지 않게 하려면 `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로, 파일명, 디스크 이름을 인수로 받습니다:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```
> [!NOTE]
> Laravel의 파일 저장소에 대한 자세한 내용은 전체 [file storage documentation](/docs/13.x/filesystem)를 확인하세요.

<a name="configuring-trusted-proxies"></a>
<!-- ## Configuring Trusted Proxies -->
## Configuring Trusted Proxies

<!-- When running your applications behind a load balancer that terminates TLS / SSL certificates, you may notice your application sometimes does not generate HTTPS links when using the `url` helper. Typically this is because your application is being forwarded traffic from your load balancer on port 80 and does not know it should generate secure links. -->
TLS / SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼를 사용하면 애플리케이션이 가끔 HTTPS 링크를 생성하지 않는 것을 볼 수 있습니다. 일반적으로 이는 애플리케이션이 로드 밸런서로부터 포트 80을 통해 트래픽을 전달받고 있어, 보안 링크를 생성해야 한다는 사실을 알지 못하기 때문입니다.

<!-- To solve this, you may enable the `Illuminate\Http\Middleware\TrustProxies` middleware that is included in your Laravel application, which allows you to quickly customize the load balancers or proxies that should be trusted by your application. Your trusted proxies should be specified using the `trustProxies` middleware method in your application's `bootstrap/app.php` file: -->
이 문제를 해결하려면 Laravel 애플리케이션에 포함된 `Illuminate\Http\Middleware\TrustProxies` Middleware를 활성화할 수 있습니다. 이를 통해 애플리케이션이 신뢰해야 하는 로드 밸런서나 프록시를 빠르게 사용자 정의할 수 있습니다. 신뢰할 수 있는 프록시는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` Middleware 메서드를 사용하여 지정해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

<!-- In addition to configuring the trusted proxies, you may also configure the proxy headers that should be trusted: -->
신뢰할 수 있는 프록시를 설정하는 것 외에도, 신뢰해야 하는 프록시 헤더를 설정할 수도 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
        Request::HEADER_X_FORWARDED_HOST |
        Request::HEADER_X_FORWARDED_PORT |
        Request::HEADER_X_FORWARDED_PROTO |
        Request::HEADER_X_FORWARDED_AWS_ELB
    );
})
```

> [!NOTE]
> AWS Elastic Load Balancing을 사용하고 있다면 `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`이어야 합니다. 로드 밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)의 표준 `Forwarded` 헤더를 사용한다면 `headers` 값은 `Request::HEADER_FORWARDED`이어야 합니다. `headers` 값에 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [trusting proxies](https://symfony.com/doc/current/deployment/proxies.html) 문서를 확인하세요.

<a name="trusting-all-proxies"></a>
<!-- #### Trusting All Proxies -->
#### Trusting All Proxies

<!-- If you are using Amazon AWS or another "cloud" load balancer provider, you may not know the IP addresses of your actual balancers. In this case, you may use `*` to trust all proxies: -->
Amazon AWS 또는 다른 "클라우드" 로드 밸런서 제공자를 사용하고 있다면 실제 로드 밸런서의 IP 주소를 알 수 없을 수 있습니다. 이 경우 `*`를 사용하여 모든 프록시를 신뢰할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
<!-- ## Configuring Trusted Hosts -->
## Configuring Trusted Hosts

<!-- By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request. -->
기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 관계없이 수신한 모든 요청에 응답합니다. 또한 웹 요청 중 애플리케이션에 대한 절대 URL을 생성할 때 `Host` 헤더의 값이 사용됩니다.

<!-- Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given hostname. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain hostnames, you may do so by enabling the `Illuminate\Http\Middleware\TrustHosts` middleware for your application. -->
일반적으로 Nginx나 Apache 같은 웹 서버를 설정하여 지정된 호스트명과 일치하는 요청만 애플리케이션으로 보내도록 해야 합니다. 하지만 웹 서버를 직접 사용자 정의할 수 없고, Laravel이 특정 호스트명에만 응답하도록 지시해야 한다면 애플리케이션에서 `Illuminate\Http\Middleware\TrustHosts` Middleware를 활성화하여 처리할 수 있습니다.

<!-- To enable the `TrustHosts` middleware, you should invoke the `trustHosts` middleware method in your application's `bootstrap/app.php` file. Using the `at` argument of this method, you may specify the hostnames that your application should respond to. The hostname string is treated as a regular expression. Incoming requests with other `Host` headers will be rejected: -->
`TrustHosts` Middleware를 활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` Middleware 메서드를 호출해야 합니다. 이 메서드의 `at` 인수를 사용하여 애플리케이션이 응답해야 하는 호스트명을 지정할 수 있습니다. 호스트명 문자열은 정규 표현식으로 처리됩니다. 다른 `Host` 헤더를 가진 들어오는 요청은 거부됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$']);
})
```

<!-- By default, requests coming from subdomains of the application's URL are also automatically trusted. If you would like to disable this behavior, you may use the `subdomains` argument: -->
기본적으로 애플리케이션 URL의 서브도메인에서 오는 요청도 자동으로 신뢰됩니다. 이 동작을 비활성화하려면 `subdomains` 인수를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
})
```

<!-- If you need to access your application's configuration files or database to determine your trusted hosts, you may provide a closure to the `at` argument: -->
신뢰할 수 있는 호스트를 결정하기 위해 애플리케이션의 설정 파일이나 데이터베이스에 접근해야 한다면 `at` 인수에 클로저를 제공할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```
