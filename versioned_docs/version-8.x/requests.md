<!-- # HTTP Requests -->
# HTTP Requests

- [Introduction](#introduction)
- [Interacting With The Request](#interacting-with-the-request)
    - [Accessing The Request](#accessing-the-request)
    - [Request Path & Method](#request-path-and-method)
    - [Request Headers](#request-headers)
    - [Request IP Address](#request-ip-address)
    - [Content Negotiation](#content-negotiation)
    - [PSR-7 Requests](#psr7-requests)
- [Input](#input)
    - [Retrieving Input](#retrieving-input)
    - [Determining If Input Is Present](#determining-if-input-is-present)
    - [Merging Additional Input](#merging-additional-input)
    - [Old Input](#old-input)
    - [Cookies](#cookies)
    - [Input Trimming & Normalization](#input-trimming-and-normalization)
- [Files](#files)
    - [Retrieving Uploaded Files](#retrieving-uploaded-files)
    - [Storing Uploaded Files](#storing-uploaded-files)
- [Configuring Trusted Proxies](#configuring-trusted-proxies)
- [Configuring Trusted Hosts](#configuring-trusted-hosts)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's `Illuminate\Http\Request` class provides an object-oriented way to interact with the current HTTP request being handled by your application as well as retrieve the input, cookies, and files that were submitted with the request. -->
Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션에서 현재 처리 중인 HTTP 요청을 객체지향적으로 다루고, 해당 요청을 통해 전송된 입력값, 쿠키, 파일 등을 쉽게 가져올 수 있도록 지원합니다.

<a name="interacting-with-the-request"></a>
<!-- ## Interacting With The Request -->
## Interacting With The Request

<a name="accessing-the-request"></a>
<!-- ### Accessing The Request -->
### Accessing The Request

<!-- To obtain an instance of the current HTTP request via dependency injection, you should type-hint the `Illuminate\Http\Request` class on your route closure or controller method. The incoming request instance will automatically be injected by the Laravel [service container](/docs/8.x/container): -->
HTTP 요청 객체를 의존성 주입(Dependency Injection)을 통해 얻으려면, 라우트 클로저나 컨트롤러 메서드의 인자에 `Illuminate\Http\Request` 타입을 명시하면 됩니다. Laravel의 [service container](/docs/8.x/container)가 자동으로 해당 요청 객체를 주입해줍니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $name = $request->input('name');

        //
    }
}
```

<!-- As mentioned, you may also type-hint the `Illuminate\Http\Request` class on a route closure. The service container will automatically inject the incoming request into the closure when it is executed: -->
위 예시와 같이, 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트로 명시할 수 있습니다. 서비스 컨테이너가 해당 요청을 자동으로 클로저로 전달해줍니다.

```
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    //
});
```

<a name="dependency-injection-route-parameters"></a>
<!-- #### Dependency Injection & Route Parameters -->
#### Dependency Injection & Route Parameters

<!-- If your controller method is also expecting input from a route parameter you should list your route parameters after your other dependencies. For example, if your route is defined like so: -->
컨트롤러 메서드에서 라우트 파라미터 값도 같이 받아야 할 경우엔, 다른 의존성 인자 다음에 라우트 파라미터를 나열하면 됩니다. 예를 들어 아래와 같이 라우트를 정의했다면,

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` route parameter by defining your controller method as follows: -->
컨트롤러 메서드에서 `Illuminate\Http\Request` 타입과 함께 `id` 파라미터도 받을 수 있습니다.

```
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the specified user.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  string  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }
}
```

<a name="request-path-and-method"></a>
<!-- ### Request Path & Method -->
### Request Path & Method

<!-- The `Illuminate\Http\Request` instance provides a variety of methods for examining the incoming HTTP request and extends the `Symfony\Component\HttpFoundation\Request` class. We will discuss a few of the most important methods below. -->
`Illuminate\Http\Request` 인스턴스는 들어온 HTTP 요청을 확인하기 위한 여러 메서드를 제공합니다. 또한 이 클래스는 `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 자주 사용하는 몇 가지 핵심 메서드는 아래와 같습니다.

<a name="retrieving-the-request-path"></a>
<!-- #### Retrieving The Request Path -->
#### Retrieving The Request Path

<!-- The `path` method returns the request's path information. So, if the incoming request is targeted at `http://example.com/foo/bar`, the `path` method will return `foo/bar`: -->
`path` 메서드는 요청 경로 정보를 반환합니다. 예를 들어, 요청 URL이 `http://example.com/foo/bar`라면 `path` 메서드는 `foo/bar`를 반환합니다.

```
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
<!-- #### Inspecting The Request Path / Route -->
#### Inspecting The Request Path / Route

<!-- The `is` method allows you to verify that the incoming request path matches a given pattern. You may use the `*` character as a wildcard when utilizing this method: -->
`is` 메서드는 들어온 요청 경로가 주어진 패턴과 일치하는지 확인할 수 있습니다. 이때 `*` 문자를 와일드카드로 사용할 수 있습니다.

```
if ($request->is('admin/*')) {
    //
}
```

<!-- Using the `routeIs` method, you may determine if the incoming request has matched a [named route](/docs/8.x/routing#named-routes): -->
`routeIs` 메서드를 사용하면 요청이 [named route](/docs/8.x/routing#named-routes)와 일치하는지 확인할 수 있습니다.

```
if ($request->routeIs('admin.*')) {
    //
}
```

<a name="retrieving-the-request-url"></a>
<!-- #### Retrieving The Request URL -->
#### Retrieving The Request URL

<!-- To retrieve the full URL for the incoming request you may use the `url` or `fullUrl` methods. The `url` method will return the URL without the query string, while the `fullUrl` method includes the query string: -->
요청의 전체 URL을 얻으려면 `url` 또는 `fullUrl` 메서드를 사용합니다. `url` 메서드는 쿼리 문자열을 제외한 URL을, `fullUrl`은 쿼리 문자열까지 포함한 전체 URL을 반환합니다.

```
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

<!-- If you would like to append query string data to the current URL, you may call the `fullUrlWithQuery` method. This method merges the given array of query string variables with the current query string: -->
현재 URL에 쿼리 문자열 정보를 추가하고 싶다면 `fullUrlWithQuery` 메서드를 사용할 수 있습니다. 이 메서드는 전달한 배열을 현재 쿼리 문자열과 병합해서 반환합니다.

```
$request->fullUrlWithQuery(['type' => 'phone']);
```

<a name="retrieving-the-request-method"></a>
<!-- #### Retrieving The Request Method -->
#### Retrieving The Request Method

<!-- The `method` method will return the HTTP verb for the request. You may use the `isMethod` method to verify that the HTTP verb matches a given string: -->
`method` 메서드를 사용하면 요청의 HTTP 메서드(예: GET, POST 등)를 얻을 수 있습니다. 또한 `isMethod` 메서드를 사용해 원하는 HTTP 메서드와 일치하는지 검사할 수 있습니다.

```
$method = $request->method();

if ($request->isMethod('post')) {
    //
}
```

<a name="request-headers"></a>
<!-- ### Request Headers -->
### Request Headers

<!-- You may retrieve a request header from the `Illuminate\Http\Request` instance using the `header` method. If the header is not present on the request, `null` will be returned. However, the `header` method accepts an optional second argument that will be returned if the header is not present on the request: -->
`Illuminate\Http\Request` 인스턴스에서 `header` 메서드로 특정 요청 헤더 값을 가져올 수 있습니다. 해당 헤더가 없으면 `null`이 반환되고, `header` 메서드의 두 번째 인자로 기본값을 지정할 수도 있습니다.

```
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

<!-- The `hasHeader` method may be used to determine if the request contains a given header: -->
특정 헤더가 존재하는지만 확인하고 싶다면 `hasHeader` 메서드를 사용합니다.

```
if ($request->hasHeader('X-Header-Name')) {
    //
}
```

<!-- For convenience, the `bearerToken` method may be used to retrieve a bearer token from the `Authorization` header. If no such header is present, an empty string will be returned: -->
편리하게 `bearerToken` 메서드를 통해 `Authorization` 헤더의 베어러 토큰을 바로 가져올 수도 있습니다. 이 헤더가 없으면 빈 문자열을 반환합니다.

```
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
<!-- ### Request IP Address -->
### Request IP Address

<!-- The `ip` method may be used to retrieve the IP address of the client that made the request to your application: -->
요청을 보낸 클라이언트의 IP 주소를 알아내려면 `ip` 메서드를 사용합니다.

```
$ipAddress = $request->ip();
```

<a name="content-negotiation"></a>
<!-- ### Content Negotiation -->
### Content Negotiation

<!-- Laravel provides several methods for inspecting the incoming request's requested content types via the `Accept` header. First, the `getAcceptableContentTypes` method will return an array containing all of the content types accepted by the request: -->
Laravel은 요청의 `Accept` 헤더를 통해 클라이언트가 수용 가능한 콘텐츠 타입을 쉽게 확인할 수 있는 여러 메서드를 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청에서 허용된 모든 콘텐츠 타입을 배열로 반환합니다.

```
$contentTypes = $request->getAcceptableContentTypes();
```

<!-- The `accepts` method accepts an array of content types and returns `true` if any of the content types are accepted by the request. Otherwise, `false` will be returned: -->
`accepts` 메서드는 콘텐츠 타입 배열을 받아 요청이 해당 타입들 중 하나라도 수락하는지 확인해 `true` 또는 `false`를 반환합니다.

```
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

<!-- You may use the `prefers` method to determine which content type out of a given array of content types is most preferred by the request. If none of the provided content types are accepted by the request, `null` will be returned: -->
`prefers` 메서드는 제공한 콘텐츠 타입 배열 중에서 요청이 가장 선호하는 타입을 반환합니다. 어느 것도 허용하지 않으면 `null`을 반환합니다.

```
$preferred = $request->prefers(['text/html', 'application/json']);
```

<!-- Since many applications only serve HTML or JSON, you may use the `expectsJson` method to quickly determine if the incoming request expects a JSON response: -->
애플리케이션에서 주로 HTML 또는 JSON만 제공한다면, `expectsJson` 메서드를 통해 요청이 JSON 응답을 기대하는지 빠르게 확인할 수 있습니다.

```
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
<!-- ### PSR-7 Requests -->
### PSR-7 Requests

<!-- The [PSR-7 standard](https://www.php-fig.org/psr/psr-7/) specifies interfaces for HTTP messages, including requests and responses. If you would like to obtain an instance of a PSR-7 request instead of a Laravel request, you will first need to install a few libraries. Laravel uses the *Symfony HTTP Message Bridge* component to convert typical Laravel requests and responses into PSR-7 compatible implementations: -->
[PSR-7 standard](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청/응답)를 위한 인터페이스를 정의합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 사용하고 싶다면, 몇 가지 라이브러리 설치가 필요합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 사용해 PSR-7 호환 요청/응답으로 변환합니다.

```
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

<!-- Once you have installed these libraries, you may obtain a PSR-7 request by type-hinting the request interface on your route closure or controller method: -->
라이브러리를 설치한 후, 라우트 클로저나 컨트롤러 메서드의 타입힌트에 PSR-7 요청 인터페이스를 사용할 수 있습니다.

```
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    //
});
```

> [!TIP]
> 라우트 또는 컨트롤러에서 PSR-7 응답 객체를 반환하면, 프레임워크가 자동으로 Laravel 응답 객체로 변환해 클라이언트에 반환합니다.

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
들어온 요청의 전체 입력값을 `all` 메서드로 `array` 형태로 가져올 수 있습니다. 이는 HTML 폼이나 XHR 요청 등 요청 방식과 관계없이 사용할 수 있습니다.

```
$input = $request->all();
```

<!-- Using the `collect` method, you may retrieve all of the incoming request's input data as a [collection](/docs/8.x/collections): -->
`collect` 메서드를 사용하면 모든 입력값을 [collection](/docs/8.x/collections)으로 가져올 수 있습니다.

```
$input = $request->collect();
```

<!-- The `collect` method also allows you to retrieve a subset of the incoming request input as a collection: -->
`collect` 메서드에 키를 지정하면 부분 집합만 컬렉션으로 받을 수도 있습니다.

```
$request->collect('users')->each(function ($user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
<!-- #### Retrieving An Input Value -->
#### Retrieving An Input Value

<!-- Using a few simple methods, you may access all of the user input from your `Illuminate\Http\Request` instance without worrying about which HTTP verb was used for the request. Regardless of the HTTP verb, the `input` method may be used to retrieve user input: -->
HTTP 메서드에 상관없이, `Illuminate\Http\Request` 인스턴스의 다양한 메서드를 통해 모든 입력값을 쉽게 조회할 수 있습니다. 가장 기본적으로 `input` 메서드를 사용해 입력값을 가져올 수 있습니다.

```
$name = $request->input('name');
```

<!-- You may pass a default value as the second argument to the `input` method. This value will be returned if the requested input value is not present on the request: -->
`input` 메서드의 두 번째 인자로 입력값이 없을 경우 반환할 기본값을 전달할 수도 있습니다.

```
$name = $request->input('name', 'Sally');
```

<!-- When working with forms that contain array inputs, use "dot" notation to access the arrays: -->
배열 형태의 입력값이 있는 폼에서 값에 접근할 때는 "dot" 표기법을 사용할 수 있습니다.

```
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

<!-- You may call the `input` method without any arguments in order to retrieve all of the input values as an associative array: -->
인자 없이 `input` 메서드를 호출하면 모든 입력값을 연관 배열로 반환합니다.

```
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
<!-- #### Retrieving Input From The Query String -->
#### Retrieving Input From The Query String

<!-- While the `input` method retrieves values from the entire request payload (including the query string), the `query` method will only retrieve values from the query string: -->
`input` 메서드는 전체 요청 데이터에서 값을 가져오지만, 쿼리 스트링에서만 값을 가져오고 싶을 땐 `query` 메서드를 사용합니다.

```
$name = $request->query('name');
```

<!-- If the requested query string value data is not present, the second argument to this method will be returned: -->
마찬가지로, 값이 없을 때 반환할 기본값을 두 번째 인자로 지정할 수 있습니다.

```
$name = $request->query('name', 'Helen');
```

<!-- You may call the `query` method without any arguments in order to retrieve all of the query string values as an associative array: -->
`query` 메서드를 인자 없이 호출하면 모든 쿼리 스트링 값을 연관 배열로 반환합니다.

```
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
<!-- #### Retrieving JSON Input Values -->
#### Retrieving JSON Input Values

<!-- When sending JSON requests to your application, you may access the JSON data via the `input` method as long as the `Content-Type` header of the request is properly set to `application/json`. You may even use "dot" syntax to retrieve values that are nested within JSON arrays: -->
애플리케이션에 JSON 요청이 들어올 경우, 요청 헤더의 `Content-Type`이 `application/json`으로 제대로 설정되어 있다면 `input` 메서드로 JSON 데이터에 접근할 수 있습니다. "dot" 표기법으로 중첩된 배열의 값을 쉽게 조회할 수도 있습니다.

```
$name = $request->input('user.name');
```

<a name="retrieving-boolean-input-values"></a>
<!-- #### Retrieving Boolean Input Values -->
#### Retrieving Boolean Input Values

<!-- When dealing with HTML elements like checkboxes, your application may receive "truthy" values that are actually strings. For example, "true" or "on". For convenience, you may use the `boolean` method to retrieve these values as booleans. The `boolean` method returns `true` for 1, "1", true, "true", "on", and "yes". All other values will return `false`: -->
체크박스처럼 HTML 폼에서 실제로는 문자열로 넘어오는 "truthy" 값(예: "true", "on" 등)을 편리하게 처리하려면 `boolean` 메서드를 사용할 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes"에 대해 `true`를 반환하며, 그 외에는 모두 `false`를 반환합니다.

```
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
<!-- #### Retrieving Date Input Values -->
#### Retrieving Date Input Values

<!-- For convenience, input values containing dates / times may be retrieved as Carbon instances using the `date` method. If the request does not contain an input value with the given name, `null` will be returned: -->
입력값이 날짜/시간이라면, `date` 메서드를 통해 Carbon 인스턴스로 받을 수 있습니다. 값이 없으면 `null`을 반환합니다.

```
$birthday = $request->date('birthday');
```

<!-- The second and third arguments accepted by the `date` method may be used to specify the date's format and timezone, respectively: -->
`date` 메서드는 두 번째와 세 번째 인자를 받아 포맷과 타임존을 지정할 수 있습니다.

```
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

<!-- If the input value is present but has an invalid format, an `InvalidArgumentException` will be thrown; therefore, it is recommended that you validate the input before invoking the `date` method. -->
입력값이 있지만 형식이 올바르지 않으면 `InvalidArgumentException`이 발생하므로, `date` 메서드를 호출하기 전에 입력 유효성 검사(Validation)를 수행하는 것이 좋습니다.

<a name="retrieving-input-via-dynamic-properties"></a>
<!-- #### Retrieving Input Via Dynamic Properties -->
#### Retrieving Input Via Dynamic Properties

<!-- You may also access user input using dynamic properties on the `Illuminate\Http\Request` instance. For example, if one of your application's forms contains a `name` field, you may access the value of the field like so: -->
`Illuminate\Http\Request` 인스턴스의 동적 속성을 활용해 입력값에 접근할 수도 있습니다. 예를 들어, 폼에 `name` 필드가 있다면 다음과 같이 값을 얻을 수 있습니다.

```
$name = $request->name;
```

<!-- When using dynamic properties, Laravel will first look for the parameter's value in the request payload. If it is not present, Laravel will search for the field in the matched route's parameters. -->
동적 속성을 사용할 경우, 우선 요청 데이터에서 해당 값을 찾고 없으면 일치하는 라우트 파라미터 값에서 찾게 됩니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
<!-- #### Retrieving A Portion Of The Input Data -->
#### Retrieving A Portion Of The Input Data

<!-- If you need to retrieve a subset of the input data, you may use the `only` and `except` methods. Both of these methods accept a single `array` or a dynamic list of arguments: -->
입력값 중 필요한 일부만 추출하고 싶다면, `only` 또는 `except` 메서드를 사용할 수 있습니다. 두 메서드는 하나의 `array` 또는 여러 인자를 받습니다.

```
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!NOTE]
> `only` 메서드는 요청에 실제로 존재하는 키에 대한 값만 반환합니다. 요청에 없는 키는 반환하지 않습니다.

<a name="determining-if-input-is-present"></a>
<!-- ### Determining If Input Is Present -->
### Determining If Input Is Present

<!-- You may use the `has` method to determine if a value is present on the request. The `has` method returns `true` if the value is present on the request: -->
`has` 메서드를 사용하면 특정 값이 요청에 포함되어 있는지 검사할 수 있습니다. 값이 있으면 `has` 메서드는 `true`를 반환합니다.

```
if ($request->has('name')) {
    //
}
```

<!-- When given an array, the `has` method will determine if all of the specified values are present: -->
배열을 인자로 전달하면, 지정된 모든 값이 모두 존재하는지 `has` 메서드가 검사합니다.

```
if ($request->has(['name', 'email'])) {
    //
}
```

<!-- The `whenHas` method will execute the given closure if a value is present on the request: -->
`whenHas` 메서드를 사용하면 특정 값이 존재할 때만 클로저를 실행할 수 있습니다.

```
$request->whenHas('name', function ($input) {
    //
});
```

<!-- A second closure may be passed to the `whenHas` method that will be executed if the specified value is not present on the request: -->
`whenHas`에 두 번째 클로저를 전달하면, 지정한 값이 없을 경우 대신 실행됩니다.

```
$request->whenHas('name', function ($input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```

<!-- The `hasAny` method returns `true` if any of the specified values are present: -->
`hasAny` 메서드는 전달한 값들 중 하나라도 요청에 존재하면 `true`를 반환합니다.

```
if ($request->hasAny(['name', 'email'])) {
    //
}
```

<!-- If you would like to determine if a value is present on the request and is not empty, you may use the `filled` method: -->
값이 요청에 존재하고 비어있지 않은지 확인하려면 `filled` 메서드를 사용합니다.

```
if ($request->filled('name')) {
    //
}
```

<!-- The `whenFilled` method will execute the given closure if a value is present on the request and is not empty: -->
`whenFilled` 메서드를 사용하면 값이 존재하고 비어있지 않을 때만 작업을 수행할 수 있습니다.

```
$request->whenFilled('name', function ($input) {
    //
});
```

<!-- A second closure may be passed to the `whenFilled` method that will be executed if the specified value is not "filled": -->
마찬가지로, `whenFilled` 메서드에 두 번째 클로저를 전달하면 값이 비어있을 때 실행됩니다.

```
$request->whenFilled('name', function ($input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```

<!-- To determine if a given key is absent from the request, you may use the `missing` method: -->
특정 키가 요청에 없는지 확인하고 싶다면 `missing` 메서드를 사용하면 됩니다.

```
if ($request->missing('name')) {
    //
}
```

<a name="merging-additional-input"></a>
<!-- ### Merging Additional Input -->
### Merging Additional Input

<!-- Sometimes you may need to manually merge additional input into the request's existing input data. To accomplish this, you may use the `merge` method: -->
때로는 현재 요청에 추가적으로 값을 수동으로 병합하고 싶을 때가 있습니다. `merge` 메서드를 이용하면 기존 입력 데이터에 새 값을 쉽게 합칠 수 있습니다.

```
$request->merge(['votes' => 0]);
```

<!-- The `mergeIfMissing` method may be used to merge input into the request if the corresponding keys do not already exist within the request's input data: -->
`mergeIfMissing` 메서드는 해당 키가 아직 존재하지 않을 때만 값을 병합해줍니다.

```
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
<!-- ### Old Input -->
### Old Input

<!-- Laravel allows you to keep input from one request during the next request. This feature is particularly useful for re-populating forms after detecting validation errors. However, if you are using Laravel's included [validation features](/docs/8.x/validation), it is possible that you will not need to manually use these session input flashing methods directly, as some of Laravel's built-in validation facilities will call them automatically. -->
Laravel은 한 번의 요청에서 입력된 값을 다음 요청에서도 보존할 수 있도록 도와줍니다. 이는 주로 폼 유효성 검사(validation) 실패 시 값을 다시 채워주는 데 유용합니다. 다만, Laravel의 [validation features](/docs/8.x/validation)을 사용하면 이 세션 입력 플래싱(flash) 작업을 직접 수행하지 않아도 되며, 내부적으로 자동 처리되는 경우가 많습니다.

<a name="flashing-input-to-the-session"></a>
<!-- #### Flashing Input To The Session -->
#### Flashing Input To The Session

<!-- The `flash` method on the `Illuminate\Http\Request` class will flash the current input to the [session](/docs/8.x/session) so that it is available during the user's next request to the application: -->
`Illuminate\Http\Request`의 `flash` 메서드는 현재 입력값을 [session](/docs/8.x/session)에 플래시하여, 사용자의 다음 요청에도 이 입력값을 사용할 수 있게 합니다.

```
$request->flash();
```

<!-- You may also use the `flashOnly` and `flashExcept` methods to flash a subset of the request data to the session. These methods are useful for keeping sensitive information such as passwords out of the session: -->
`flashOnly`, `flashExcept` 메서드를 사용하면, 일부 데이터만 세션에 플래시할 수 있습니다. 비밀번호 등 민감한 정보는 세션에 남지 않게 할 때 사용하면 좋습니다.

```
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
<!-- #### Flashing Input Then Redirecting -->
#### Flashing Input Then Redirecting

<!-- Since you often will want to flash input to the session and then redirect to the previous page, you may easily chain input flashing onto a redirect using the `withInput` method: -->
입력을 세션에 플래시하고 곧바로 이전 페이지로 리다이렉트하는 경우가 많으므로, `withInput` 메서드를 체이닝하여 쉽게 처리할 수 있습니다.

```
return redirect('form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
<!-- #### Retrieving Old Input -->
#### Retrieving Old Input

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/8.x/session): -->
이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request`의 `old` 메서드를 사용하면 됩니다. `old` 메서드는 [session](/docs/8.x/session)에서 이전에 플래시된 입력값을 꺼내옵니다.

```
$username = $request->old('username');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/8.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
또한 Laravel은 전역 `old` 헬퍼 함수도 제공합니다. [Blade template](/docs/8.x/blade)에서 이전 입력값으로 폼을 채울 때 `old` 헬퍼를 사용하는 것이 더 편리합니다. 만약 해당 필드의 이전 입력값이 없으면 `null`을 반환합니다.

```
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
<!-- ### Cookies -->
### Cookies

<a name="retrieving-cookies-from-requests"></a>
<!-- #### Retrieving Cookies From Requests -->
#### Retrieving Cookies From Requests

<!-- All cookies created by the Laravel framework are encrypted and signed with an authentication code, meaning they will be considered invalid if they have been changed by the client. To retrieve a cookie value from the request, use the `cookie` method on an `Illuminate\Http\Request` instance: -->
Laravel 프레임워크에서 생성된 모든 쿠키는 암호화와 인증 코드 서명이 되어 있기 때문에, 클라이언트 쪽에서 수정되면 무효로 간주합니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request`의 `cookie` 메서드를 사용합니다.

```
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
<!-- ## Input Trimming & Normalization -->
## Input Trimming & Normalization

<!-- By default, Laravel includes the `App\Http\Middleware\TrimStrings` and `App\Http\Middleware\ConvertEmptyStringsToNull` middleware in your application's global middleware stack. These middleware are listed in the global middleware stack by the `App\Http\Kernel` class. These middleware will automatically trim all incoming string fields on the request, as well as convert any empty string fields to `null`. This allows you to not have to worry about these normalization concerns in your routes and controllers. -->
기본적으로 Laravel은 애플리케이션의 글로벌 미들웨어 스택에 `App\Http\Middleware\TrimStrings`와 `App\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 미들웨어들은 `App\Http\Kernel` 클래스의 미들웨어 스택에 등록되어 있습니다. 이 미들웨어들은 모든 들어오는 문자열 필드를 자동으로 다듬고(trim), 비어 있는 문자열은 `null`로 변환해줍니다. 덕분에 라우트나 컨트롤러에서 이런 정규화 처리를 따로 신경 쓸 필요가 없습니다.

<!-- If you would like to disable this behavior, you may remove the two middleware from your application's middleware stack by removing them from the `$middleware` property of your `App\Http\Kernel` class. -->
이 기능을 비활성화하고 싶다면, `App\Http\Kernel` 클래스의 `$middleware` 속성에서 두 미들웨어를 제거하면 됩니다.

<a name="files"></a>
<!-- ## Files -->
## Files

<a name="retrieving-uploaded-files"></a>
<!-- ### Retrieving Uploaded Files -->
### Retrieving Uploaded Files

<!-- You may retrieve uploaded files from an `Illuminate\Http\Request` instance using the `file` method or using dynamic properties. The `file` method returns an instance of the `Illuminate\Http\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file: -->
`Illuminate\Http\Request` 인스턴스에서 `file` 메서드나 동적 속성으로 업로드된 파일을 가져올 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 클래스의 인스턴스를 반환하며, 이 클래스는 PHP의 `SplFileInfo` 클래스를 상속해서 다양한 파일 관련 메서드를 제공합니다.

```
$file = $request->file('photo');

$file = $request->photo;
```

<!-- You may determine if a file is present on the request using the `hasFile` method: -->
요청에 파일이 존재하는지 확인하려면 `hasFile` 메서드를 사용할 수 있습니다.

```
if ($request->hasFile('photo')) {
    //
}
```

<a name="validating-successful-uploads"></a>
<!-- #### Validating Successful Uploads -->
#### Validating Successful Uploads

<!-- In addition to checking if the file is present, you may verify that there were no problems uploading the file via the `isValid` method: -->
파일이 존재하는 것 외에, 업로드 과정에 문제가 없었는지도 `isValid` 메서드로 확인할 수 있습니다.

```
if ($request->file('photo')->isValid()) {
    //
}
```

<a name="file-paths-extensions"></a>
<!-- #### File Paths & Extensions -->
#### File Paths & Extensions

<!-- The `UploadedFile` class also contains methods for accessing the file's fully-qualified path and its extension. The `extension` method will attempt to guess the file's extension based on its contents. This extension may be different from the extension that was supplied by the client: -->
`UploadedFile` 클래스에는 파일의 전체 경로와 확장자를 확인하는 다양한 메서드가 포함되어 있습니다. `extension` 메서드는 파일 내용을 기반으로 확장자를 추정하므로, 클라이언트가 보낸 확장자와 다를 수 있습니다.

```
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
<!-- #### Other File Methods -->
#### Other File Methods

<!-- There are a variety of other methods available on `UploadedFile` instances. Check out the [API documentation for the class](https://api.symfony.com/master/Symfony/Component/HttpFoundation/File/UploadedFile.html) for more information regarding these methods. -->
이 외에도 `UploadedFile` 인스턴스에는 다양한 메서드가 존재합니다. 더 자세한 내용은 [API documentation for the class](https://api.symfony.com/master/Symfony/Component/HttpFoundation/File/UploadedFile.html)를 참고하세요.

<a name="storing-uploaded-files"></a>
<!-- ### Storing Uploaded Files -->
### Storing Uploaded Files

<!-- To store an uploaded file, you will typically use one of your configured [filesystems](/docs/8.x/filesystem). The `UploadedFile` class has a `store` method that will move an uploaded file to one of your disks, which may be a location on your local filesystem or a cloud storage location like Amazon S3. -->
업로드된 파일을 저장하려면, 보통 [filesystems](/docs/8.x/filesystem) 중 하나를 사용하게 됩니다. `UploadedFile` 클래스의 `store` 메서드를 통해 파일을 디스크(로컬 디스크, Amazon S3 등)에 저장할 수 있습니다.

<!-- The `store` method accepts the path where the file should be stored relative to the filesystem's configured root directory. This path should not contain a filename, since a unique ID will automatically be generated to serve as the filename. -->
`store` 메서드는 저장할 경로(디스크의 설정된 루트 디렉터리를 기준으로 한 상대 경로)를 받으며, 파일명은 자동으로 고유 값으로 생성됩니다.

<!-- The `store` method also accepts an optional second argument for the name of the disk that should be used to store the file. The method will return the path of the file relative to the disk's root: -->
`store` 메서드의 두 번째 인자로 사용할 디스크 이름을 지정할 수도 있습니다. 반환 값은 저장된 파일의 경로(지정한 디스크 기준)입니다.

```
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

<!-- If you do not want a filename to be automatically generated, you may use the `storeAs` method, which accepts the path, filename, and disk name as its arguments: -->
파일명을 직접 지정하고 싶다면 `storeAs` 메서드를 사용합니다. 경로, 파일명, 디스크명을 순서대로 전달합니다.

```
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!TIP]
> Laravel의 파일 저장에 대한 더 자세한 내용은 [file storage documentation](/docs/8.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
<!-- ## Configuring Trusted Proxies -->
## Configuring Trusted Proxies

<!-- When running your applications behind a load balancer that terminates TLS / SSL certificates, you may notice your application sometimes does not generate HTTPS links when using the `url` helper. Typically this is because your application is being forwarded traffic from your load balancer on port 80 and does not know it should generate secure links. -->
TLS/SSL 인증서가 끝단 로드 밸런서에서 처리되는 환경에서, 애플리케이션이 `url` 헬퍼 사용 시 HTTPS 링크를 생성하지 않는 문제를 겪을 수 있습니다. 이는 보통 로드 밸런서가 80 포트에서 트래픽을 전달하고 있기 때문입니다.

<!-- To solve this, you may use the `App\Http\Middleware\TrustProxies` middleware that is included in your Laravel application, which allows you to quickly customize the load balancers or proxies that should be trusted by your application. Your trusted proxies should be listed as an array on the `$proxies` property of this middleware. In addition to configuring the trusted proxies, you may configure the proxy `$headers` that should be trusted: -->
이 문제를 해결하려면, Laravel에 기본 포함된 `App\Http\Middleware\TrustProxies` 미들웨어를 활용할 수 있습니다. 이 미들웨어를 통해 신뢰할 수 있는 프록시나 로드 밸런서를 손쉽게 지정할 수 있습니다. 신뢰할 프록시는 이 미들웨어의 `$proxies` 속성에 배열로 나열하면 됩니다. 또한 신뢰할 프록시 헤더도 `$headers` 속성으로 지정할 수 있습니다.

```
<?php

namespace App\Http\Middleware;

use Illuminate\Http\Middleware\TrustProxies as Middleware;
use Illuminate\Http\Request;

class TrustProxies extends Middleware
{
    /**
     * The trusted proxies for this application.
     *
     * @var string|array
     */
    protected $proxies = [
        '192.168.1.1',
        '192.168.1.2',
    ];

    /**
     * The headers that should be used to detect proxies.
     *
     * @var int
     */
    protected $headers = Request::HEADER_X_FORWARDED_FOR | Request::HEADER_X_FORWARDED_HOST | Request::HEADER_X_FORWARDED_PORT | Request::HEADER_X_FORWARDED_PROTO;
}
```

> [!TIP]
> AWS Elastic Load Balancing을 사용할 경우, `$headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`로 지정해야 합니다. `$headers`에서 사용할 수 있는 상수에 대한 자세한 설명은 Symfony의 [trusting proxies](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
<!-- #### Trusting All Proxies -->
#### Trusting All Proxies

<!-- If you are using Amazon AWS or another "cloud" load balancer provider, you may not know the IP addresses of your actual balancers. In this case, you may use `*` to trust all proxies: -->
Amazon AWS 등 클라우드 로드 밸런서를 사용할 경우 실제 밸런서의 IP를 모를 수 있습니다. 이럴 땐, `*`로 모든 프록시를 신뢰하도록 설정할 수 있습니다.

```
/**
 * The trusted proxies for this application.
 *
 * @var string|array
 */
protected $proxies = '*';
```

<a name="configuring-trusted-hosts"></a>
<!-- ## Configuring Trusted Hosts -->
## Configuring Trusted Hosts

<!-- By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request. -->
기본적으로 Laravel은 HTTP 요청의 `Host` 헤더와 관계없이 모든 요청에 응답하며, 절대 URL 생성 시에도 `Host` 헤더 값을 참고합니다.

<!-- Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given host name. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain host names, you may do so by enabling the `App\Http\Middleware\TrustHosts` middleware for your application. -->
보통은 Nginx나 Apache 같은 웹 서버에서 접근 허용 호스트를 제한해야 하지만, 웹 서버를 직접 제어할 수 없는 경우 Laravel을 통해 특정 호스트 이름만 응답하도록 설정할 수 있습니다. 이를 위해 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화하면 됩니다.

<!-- The `TrustHosts` middleware is already included in the `$middleware` stack of your application; however, you should uncomment it so that it becomes active. Within this middleware's `hosts` method, you may specify the host names that your application should respond to. Incoming requests with other `Host` value headers will be rejected: -->
`TrustHosts` 미들웨어는 이미 `$middleware` 스택에 포함되어 있지만, 실제로 적용하려면 주석을 해제해야 합니다. 이 미들웨어의 `hosts` 메서드에서 허용할 호스트 패턴을 배열로 지정할 수 있습니다. 다른 `Host` 값으로 들어온 요청은 모두 거부됩니다.

```
/**
 * Get the host patterns that should be trusted.
 *
 * @return array
 */
public function hosts()
{
    return [
        'laravel.test',
        $this->allSubdomainsOfApplicationUrl(),
    ];
}
```

<!-- The `allSubdomainsOfApplicationUrl` helper method will return a regular expression matching all subdomains of your application's `app.url` configuration value. This helper method provides a convenient way to allow all of your application's subdomains when building an application that utilizes wildcard subdomains. -->
`allSubdomainsOfApplicationUrl` 헬퍼 메서드는 애플리케이션의 `app.url` 설정 값에 해당하는 모든 서브도메인을 정규식으로 반환합니다. 와일드카드 서브도메인을 사용하는 애플리케이션에서는 이 메서드를 활용해 모든 서브도메인을 허용할 수 있습니다.
