<!-- # HTTP Requests -->
# HTTP Requests

- [Introduction](#introduction)
- [Interacting With The Request](#interacting-with-the-request)
    - [Accessing The Request](#accessing-the-request)
    - [Request Path, Host, & Method](#request-path-and-method)
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
Laravel의 `Illuminate\Http\Request` 클래스는 여러분의 애플리케이션에서 처리 중인 현재 HTTP 요청에 대해 객체 지향적으로 접근할 수 있도록 하며, 요청과 함께 전달된 입력값, 쿠키, 파일 등을 쉽게 조회할 수 있게 도와줍니다.

<a name="interacting-with-the-request"></a>
<!-- ## Interacting With The Request -->
## Interacting With The Request

<a name="accessing-the-request"></a>
<!-- ### Accessing The Request -->
### Accessing The Request

<!-- To obtain an instance of the current HTTP request via dependency injection, you should type-hint the `Illuminate\Http\Request` class on your route closure or controller method. The incoming request instance will automatically be injected by the Laravel [service container](/docs/9.x/container): -->
의존성 주입(dependency injection)을 활용하여 현재 HTTP 요청 인스턴스를 얻으려면, 라우트 클로저 또는 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입힌트로 지정하면 됩니다. Laravel의 [service container](/docs/9.x/container)가 자동으로 해당 요청 인스턴스를 주입해 줍니다.

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
위 예시와 같이, 라우트 클로저에도 `Illuminate\Http\Request`를 타입힌트로 지정할 수 있습니다. 서비스 컨테이너가 클로저 실행 시 자동으로 요청을 주입해줍니다.

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
컨트롤러 메서드에서 라우트 파라미터 입력값도 함께 받을 경우, 라우트 파라미터는 다른 의존성 인자들 뒤에 나열해야 합니다. 예를 들어, 아래처럼 라우트가 정의되어 있다면,

```
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` route parameter by defining your controller method as follows: -->
컨트롤러 메서드에서 `Illuminate\Http\Request`는 타입힌트로, 라우트 파라미터인 `id`는 뒤쪽 인자로 받을 수 있습니다.

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
<!-- ### Request Path, Host, & Method -->
### Request Path, Host, & Method

<!-- The `Illuminate\Http\Request` instance provides a variety of methods for examining the incoming HTTP request and extends the `Symfony\Component\HttpFoundation\Request` class. We will discuss a few of the most important methods below. -->
`Illuminate\Http\Request` 인스턴스를 이용하면 다양한 메서드를 통해 들어온 HTTP 요청 정보를 조회할 수 있습니다. 이 클래스는 `Symfony\Component\HttpFoundation\Request`를 확장하고 있습니다. 이 중 주요 메서드들을 아래에서 살펴보겠습니다.

<a name="retrieving-the-request-path"></a>
<!-- #### Retrieving The Request Path -->
#### Retrieving The Request Path

<!-- The `path` method returns the request's path information. So, if the incoming request is targeted at `http://example.com/foo/bar`, the `path` method will return `foo/bar`: -->
`path` 메서드는 요청의 경로(path) 정보를 반환합니다. 예를 들어, 요청 주소가 `http://example.com/foo/bar`라면, `path` 메서드는 `foo/bar`를 반환합니다.

```
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
<!-- #### Inspecting The Request Path / Route -->
#### Inspecting The Request Path / Route

<!-- The `is` method allows you to verify that the incoming request path matches a given pattern. You may use the `*` character as a wildcard when utilizing this method: -->
`is` 메서드를 활용하면, 들어오는 요청 경로가 특정 패턴과 일치하는지 확인할 수 있습니다. 이때 `*` 문자를 와일드카드로 사용할 수 있습니다.

```
if ($request->is('admin/*')) {
    //
}
```

<!-- Using the `routeIs` method, you may determine if the incoming request has matched a [named route](/docs/9.x/routing#named-routes): -->
또한, `routeIs` 메서드를 이용하면, 현재 요청이 [named route](/docs/9.x/routing#named-routes)와 일치하는지 확인할 수 있습니다.

```
if ($request->routeIs('admin.*')) {
    //
}
```

<a name="retrieving-the-request-url"></a>
<!-- #### Retrieving The Request URL -->
#### Retrieving The Request URL

<!-- To retrieve the full URL for the incoming request you may use the `url` or `fullUrl` methods. The `url` method will return the URL without the query string, while the `fullUrl` method includes the query string: -->
요청의 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리 문자열을 제외한 URL을, `fullUrl` 메서드는 쿼리 문자열을 포함한 전체 URL을 반환합니다.

```
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

<!-- If you would like to append query string data to the current URL, you may call the `fullUrlWithQuery` method. This method merges the given array of query string variables with the current query string: -->
현재 URL에 쿼리 문자열 데이터를 추가하고 싶다면, `fullUrlWithQuery` 메서드를 사용할 수 있습니다. 이 메서드는 기존 쿼리 스트링에 주어진 배열의 값들을 합쳐서 반환합니다.

```
$request->fullUrlWithQuery(['type' => 'phone']);
```

<a name="retrieving-the-request-host"></a>
<!-- #### Retrieving The Request Host -->
#### Retrieving The Request Host

<!-- You may retrieve the "host" of the incoming request via the `host`, `httpHost`, and `schemeAndHttpHost` methods: -->
`host`, `httpHost`, `schemeAndHttpHost` 메서드를 사용하면 들어온 요청의 "호스트" 정보를 각각 가져올 수 있습니다.

```
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
<!-- #### Retrieving The Request Method -->
#### Retrieving The Request Method

<!-- The `method` method will return the HTTP verb for the request. You may use the `isMethod` method to verify that the HTTP verb matches a given string: -->
`method` 메서드는 요청의 HTTP 메서드(동사)를 반환합니다. 또한 `isMethod` 메서드를 사용해 요청의 HTTP 메서드가 특정 문자열과 일치하는지 확인할 수 있습니다.

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
`Illuminate\Http\Request` 인스턴스의 `header` 메서드로 요청 헤더 정보를 가져올 수 있습니다. 해당 헤더가 요청에 없으면 `null`이 반환됩니다. 하지만 `header` 메서드의 두 번째 값으로 기본값을 전달할 수 있으며, 헤더가 없을 경우 이 값이 반환됩니다.

```
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

<!-- The `hasHeader` method may be used to determine if the request contains a given header: -->
특정 헤더가 요청에 포함되었는지 확인하려면 `hasHeader` 메서드를 사용할 수 있습니다.

```
if ($request->hasHeader('X-Header-Name')) {
    //
}
```

<!-- For convenience, the `bearerToken` method may be used to retrieve a bearer token from the `Authorization` header. If no such header is present, an empty string will be returned: -->
편리하게 `Authorization` 헤더에서 Bearer 토큰 값을 꺼내려면 `bearerToken` 메서드를 사용할 수 있습니다. 해당 헤더가 없을 경우 빈 문자열이 반환됩니다.

```
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
<!-- ### Request IP Address -->
### Request IP Address

<!-- The `ip` method may be used to retrieve the IP address of the client that made the request to your application: -->
`ip` 메서드로 요청을 보낸 클라이언트의 IP 주소를 확인할 수 있습니다.

```
$ipAddress = $request->ip();
```

<a name="content-negotiation"></a>
<!-- ### Content Negotiation -->
### Content Negotiation

<!-- Laravel provides several methods for inspecting the incoming request's requested content types via the `Accept` header. First, the `getAcceptableContentTypes` method will return an array containing all of the content types accepted by the request: -->
Laravel은 들어오는 요청의 `Accept` 헤더를 이용해 클라이언트가 원하는 콘텐츠 타입을 검사할 수 있는 여러 메서드를 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청에서 허용된 모든 콘텐츠 타입의 배열을 반환합니다.

```
$contentTypes = $request->getAcceptableContentTypes();
```

<!-- The `accepts` method accepts an array of content types and returns `true` if any of the content types are accepted by the request. Otherwise, `false` will be returned: -->
`accepts` 메서드는 전달받은 콘텐츠 타입 배열 중 하나라도 요청에서 허용된다면 `true`를 반환합니다. 그렇지 않으면 `false`를 반환합니다.

```
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

<!-- You may use the `prefers` method to determine which content type out of a given array of content types is most preferred by the request. If none of the provided content types are accepted by the request, `null` will be returned: -->
`prefers` 메서드는 주어진 여러 콘텐츠 타입 중 요청 측에서 가장 선호하는 타입을 반환합니다. 만약 전달한 타입들이 모두 허용되지 않으면 `null`이 반환됩니다.

```
$preferred = $request->prefers(['text/html', 'application/json']);
```

<!-- Since many applications only serve HTML or JSON, you may use the `expectsJson` method to quickly determine if the incoming request expects a JSON response: -->
많은 애플리케이션에서 HTML이나 JSON만 제공하는 경우, 요청이 JSON 응답을 기대하고 있는지 빠르게 확인하려면 `expectsJson` 메서드를 사용할 수 있습니다.

```
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
<!-- ### PSR-7 Requests -->
### PSR-7 Requests

<!-- The [PSR-7 standard](https://www.php-fig.org/psr/psr-7/) specifies interfaces for HTTP messages, including requests and responses. If you would like to obtain an instance of a PSR-7 request instead of a Laravel request, you will first need to install a few libraries. Laravel uses the *Symfony HTTP Message Bridge* component to convert typical Laravel requests and responses into PSR-7 compatible implementations: -->
[PSR-7 standard](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청/응답)에 대한 인터페이스를 정의합니다. Laravel의 기본 요청이 아닌 PSR-7 요청 인스턴스를 사용하려면 몇 가지 라이브러리를 먼저 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 활용해 Laravel의 요청/응답 객체를 PSR-7 구현체로 변환해줍니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

<!-- Once you have installed these libraries, you may obtain a PSR-7 request by type-hinting the request interface on your route closure or controller method: -->
라이브러리 설치 후, 라우트 클로저나 컨트롤러에서 PSR-7의 인터페이스를 타입힌트로 지정해 PSR-7 요청 인스턴스를 사용할 수 있습니다.

```
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    //
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, Laravel에서 자동으로 Laravel 응답 인스턴스로 다시 변환되어 화면에 출력됩니다.

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
`all` 메서드를 사용하면 요청에 담긴 모든 입력값을 `array` 형태로 가져올 수 있습니다. 이 메서드는 요청이 HTML 폼이든, XHR 요청이든 상관없이 사용 가능합니다.

```
$input = $request->all();
```

<!-- Using the `collect` method, you may retrieve all of the incoming request's input data as a [collection](/docs/9.x/collections): -->
`collect` 메서드는 요청의 모든 입력값을 [collection](/docs/9.x/collections) 형태로 가져옵니다.

```
$input = $request->collect();
```

<!-- The `collect` method also allows you to retrieve a subset of the incoming request input as a collection: -->
또한 `collect` 메서드는 전달한 키의 입력값 일부만 컬렉션으로 받아올 수도 있습니다.

```
$request->collect('users')->each(function ($user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
<!-- #### Retrieving An Input Value -->
#### Retrieving An Input Value

<!-- Using a few simple methods, you may access all of the user input from your `Illuminate\Http\Request` instance without worrying about which HTTP verb was used for the request. Regardless of the HTTP verb, the `input` method may be used to retrieve user input: -->
HTTP 메서드 종류와 무관하게, `Illuminate\Http\Request` 인스턴스의 `input` 메서드를 사용하면 사용자가 전송한 값을 간편하게 가져올 수 있습니다.

```
$name = $request->input('name');
```

<!-- You may pass a default value as the second argument to the `input` method. This value will be returned if the requested input value is not present on the request: -->
`input` 메서드 두 번째 인수로 기본값을 전달할 수 있으며, 요청에 해당 값이 존재하지 않을 경우 이 값이 반환됩니다.

```
$name = $request->input('name', 'Sally');
```

<!-- When working with forms that contain array inputs, use "dot" notation to access the arrays: -->
배열 형태의 입력값은 "점(.) 표기법"을 써서 접근할 수 있습니다.

```
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

<!-- You may call the `input` method without any arguments in order to retrieve all of the input values as an associative array: -->
인수를 생략하고 `input` 메서드를 호출하면, 모든 입력값을 연관 배열로 가져옵니다.

```
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
<!-- #### Retrieving Input From The Query String -->
#### Retrieving Input From The Query String

<!-- While the `input` method retrieves values from the entire request payload (including the query string), the `query` method will only retrieve values from the query string: -->
`input` 메서드는 전체 요청 페이로드(쿼리 스트링 포함)에서 값을 가져오지만, `query` 메서드는 쿼리 스트링에서만 값을 조회합니다.

```
$name = $request->query('name');
```

<!-- If the requested query string value data is not present, the second argument to this method will be returned: -->
쿼리 스트링 값이 없을 때 반환할 기본값을 두 번째 인수로 지정할 수 있습니다.

```
$name = $request->query('name', 'Helen');
```

<!-- You may call the `query` method without any arguments in order to retrieve all of the query string values as an associative array: -->
인수 없이 `query`를 호출하면, 모든 쿼리 스트링 값을 연관 배열로 가져옵니다.

```
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
<!-- #### Retrieving JSON Input Values -->
#### Retrieving JSON Input Values

<!-- When sending JSON requests to your application, you may access the JSON data via the `input` method as long as the `Content-Type` header of the request is properly set to `application/json`. You may even use "dot" syntax to retrieve values that are nested within JSON arrays / objects: -->
애플리케이션에 JSON 요청이 들어오는 경우, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 지정되어 있다면 `input` 메서드로 JSON 데이터를 가져올 수 있습니다. 점 표기법을 사용해 깊숙이 중첩된 JSON 값도 접근 가능합니다.

```
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
<!-- #### Retrieving Stringable Input Values -->
#### Retrieving Stringable Input Values

<!-- Instead of retrieving the request's input data as a primitive `string`, you may use the `string` method to retrieve the request data as an instance of [`Illuminate\Support\Stringable`](/docs/9.x/helpers#fluent-strings): -->
기본 `string` 값으로 입력값을 가져오는 대신, `string` 메서드를 사용하면 입력값을 [`Illuminate\Support\Stringable`](/docs/9.x/helpers#fluent-strings) 인스턴스로 받아 다양한 문자열 메서드와 조합해서 사용할 수 있습니다.

```
$name = $request->string('name')->trim();
```

<a name="retrieving-boolean-input-values"></a>
<!-- #### Retrieving Boolean Input Values -->
#### Retrieving Boolean Input Values

<!-- When dealing with HTML elements like checkboxes, your application may receive "truthy" values that are actually strings. For example, "true" or "on". For convenience, you may use the `boolean` method to retrieve these values as booleans. The `boolean` method returns `true` for 1, "1", true, "true", "on", and "yes". All other values will return `false`: -->
HTML 체크박스와 같이 실제로는 문자열 형태의 "참" 값을 받을 수 있습니다(예: "true", "on"). 이런 경우 `boolean` 메서드를 쓰면 여러 타입("1", 1, true, "true", "on", "yes") 모두에 대해 `boolean` 메서드가 `true`를 반환하며, 이 외에는 `false`를 반환합니다.

```
$archived = $request->boolean('archived');
```

<a name="retrieving-date-input-values"></a>
<!-- #### Retrieving Date Input Values -->
#### Retrieving Date Input Values

<!-- For convenience, input values containing dates / times may be retrieved as Carbon instances using the `date` method. If the request does not contain an input value with the given name, `null` will be returned: -->
날짜/시간이 입력값에 포함된 경우, `date` 메서드를 사용하면 해당 값을 Carbon 인스턴스로 간편하게 변환할 수 있습니다. 요청에 해당 입력값이 없으면 `null`이 반환됩니다.

```
$birthday = $request->date('birthday');
```

<!-- The second and third arguments accepted by the `date` method may be used to specify the date's format and timezone, respectively: -->
`date` 메서드의 두 번째, 세 번째 인자로 날짜 형식(format)과 타임존을 지정할 수 있습니다.

```
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

<!-- If the input value is present but has an invalid format, an `InvalidArgumentException` will be thrown; therefore, it is recommended that you validate the input before invoking the `date` method. -->
해당 값이 입력되어 있지만 형식이 유효하지 않으면 `InvalidArgumentException` 예외가 발생하므로, `date` 메서드를 호출하기 전에 입력값 유효성 검증을 하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
<!-- #### Retrieving Enum Input Values -->
#### Retrieving Enum Input Values

<!-- Input values that correspond to [PHP enums](https://www.php.net/manual/en/language.types.enumerations.php) may also be retrieved from the request. If the request does not contain an input value with the given name or the enum does not have a backing value that matches the input value, `null` will be returned. The `enum` method accepts the name of the input value and the enum class as its first and second arguments: -->
[PHP enums](https://www.php.net/manual/en/language.types.enumerations.php)과 매칭되는 입력값도 요청에서 직접 꺼낼 수 있습니다. 해당 이름의 값이 없거나 enum의 백킹 값과 일치하지 않으면 `null`이 반환됩니다. `enum` 메서드는 첫 번째로 입력명, 두 번째로 enum 클래스를 받습니다.

```
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
<!-- #### Retrieving Input Via Dynamic Properties -->
#### Retrieving Input Via Dynamic Properties

<!-- You may also access user input using dynamic properties on the `Illuminate\Http\Request` instance. For example, if one of your application's forms contains a `name` field, you may access the value of the field like so: -->
`Illuminate\Http\Request` 인스턴스의 동적 프로퍼티를 이용해서도 입력값을 조회할 수 있습니다. 예를 들어, 애플리케이션 폼에 `name` 필드가 있다면 아래처럼 값을 조회할 수 있습니다.

```
$name = $request->name;
```

<!-- When using dynamic properties, Laravel will first look for the parameter's value in the request payload. If it is not present, Laravel will search for the field in the matched route's parameters. -->
동적 프로퍼티 사용 시, 먼저 요청 페이로드에서 프로퍼티명을 찾고, 없을 경우 매칭된 라우트의 파라미터에서 찾아 반환합니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
<!-- #### Retrieving A Portion Of The Input Data -->
#### Retrieving A Portion Of The Input Data

<!-- If you need to retrieve a subset of the input data, you may use the `only` and `except` methods. Both of these methods accept a single `array` or a dynamic list of arguments: -->
입력값 중 특정 값만 부분적으로 가져오려면 `only`와 `except` 메서드를 사용할 수 있습니다. 두 메서드 모두 하나의 `array`나 여러 개의 인자를 받을 수 있습니다.

```
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 실제로 존재하는 키/값만 반환합니다. 요청에 없는 키는 반환하지 않습니다.

<a name="determining-if-input-is-present"></a>
<!-- ### Determining If Input Is Present -->
### Determining If Input Is Present

<!-- You may use the `has` method to determine if a value is present on the request. The `has` method returns `true` if the value is present on the request: -->
입력값이 요청에 존재하는지 확인하려면 `has` 메서드를 사용하세요. 값이 있으면 `has` 메서드는 `true`를 반환합니다.

```
if ($request->has('name')) {
    //
}
```

<!-- When given an array, the `has` method will determine if all of the specified values are present: -->
배열로 여러 값을 전달하면 `has` 메서드가 모두 존재하는지 검사합니다.

```
if ($request->has(['name', 'email'])) {
    //
}
```

<!-- The `whenHas` method will execute the given closure if a value is present on the request: -->
`whenHas` 메서드를 사용하면, 입력값이 존재할 때만 지정한 클로저를 실행할 수 있습니다.

```
$request->whenHas('name', function ($input) {
    //
});
```

<!-- A second closure may be passed to the `whenHas` method that will be executed if the specified value is not present on the request: -->
`whenHas` 메서드에 두 번째 클로저를 전달하면, 지정한 값이 존재하지 않을 때 실행됩니다.

```
$request->whenHas('name', function ($input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```

<!-- The `hasAny` method returns `true` if any of the specified values are present: -->
`hasAny` 메서드는 지정한 값 중 하나라도 존재하면 `true`를 반환합니다.

```
if ($request->hasAny(['name', 'email'])) {
    //
}
```

<!-- If you would like to determine if a value is present on the request and is not an empty string, you may use the `filled` method: -->
요청에 값이 존재하고 빈 문자열이 아닌지도 확인할 수 있는데, 이때는 `filled` 메서드를 사용합니다.

```
if ($request->filled('name')) {
    //
}
```

<!-- The `whenFilled` method will execute the given closure if a value is present on the request and is not an empty string: -->
`whenFilled`는 값이 존재하고 비어있지 않을 때만 클로저가 실행됩니다.

```
$request->whenFilled('name', function ($input) {
    //
});
```

<!-- A second closure may be passed to the `whenFilled` method that will be executed if the specified value is not "filled": -->
`whenFilled` 메서드에 두 번째 클로저를 넘기면, 값이 비어있거나 없을 때 실행됩니다.

```
$request->whenFilled('name', function ($input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```

<!-- To determine if a given key is absent from the request, you may use the `missing` and `whenMissing` methods: -->
지정한 키가 요청에 존재하지 않는지 확인하려면 `missing`과 `whenMissing` 메서드를 사용할 수 있습니다.

```
if ($request->missing('name')) {
    //
}

$request->whenMissing('name', function ($input) {
    // The "name" value is missing...
}, function () {
    // The "name" value is present...
});
```

<a name="merging-additional-input"></a>
<!-- ### Merging Additional Input -->
### Merging Additional Input

<!-- Sometimes you may need to manually merge additional input into the request's existing input data. To accomplish this, you may use the `merge` method. If a given input key already exists on the request, it will be overwritten by the data provided to the `merge` method: -->
가끔은 기존 요청 입력값에 추가 데이터를 직접 합쳐야 할 수도 있습니다. 이럴 때는 `merge` 메서드를 사용하세요. 합치려는 키가 이미 있으면 `merge` 메서드에 전달한 값으로 덮어씁니다.

```
$request->merge(['votes' => 0]);
```

<!-- The `mergeIfMissing` method may be used to merge input into the request if the corresponding keys do not already exist within the request's input data: -->
키가 아직 요청 입력에 존재하지 않을 경우만 입력값을 병합하려면 `mergeIfMissing`를 사용할 수 있습니다.

```
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
<!-- ### Old Input -->
### Old Input

<!-- Laravel allows you to keep input from one request during the next request. This feature is particularly useful for re-populating forms after detecting validation errors. However, if you are using Laravel's included [validation features](/docs/9.x/validation), it is possible that you will not need to manually use these session input flashing methods directly, as some of Laravel's built-in validation facilities will call them automatically. -->
Laravel에서는 이전 요청의 입력값을 다음 요청에도 사용할 수 있습니다. 이 기능은 주로 입력값 유효성 검증 에러가 발생할 때 폼을 다시 채워줄 때 유용합니다. Laravel의 [validation features](/docs/9.x/validation)을 사용한다면, 세션 입력값 저장(플래싱) 메서드를 수동으로 쓸 필요 없이 자동으로 처리되는 경우가 많습니다.

<a name="flashing-input-to-the-session"></a>
<!-- #### Flashing Input To The Session -->
#### Flashing Input To The Session

<!-- The `flash` method on the `Illuminate\Http\Request` class will flash the current input to the [session](/docs/9.x/session) so that it is available during the user's next request to the application: -->
`Illuminate\Http\Request`의 `flash` 메서드를 호출하면, 현재 입력값을 [session](/docs/9.x/session)에 저장해 사용자의 다음 요청에서도 접근할 수 있습니다.

```
$request->flash();
```

<!-- You may also use the `flashOnly` and `flashExcept` methods to flash a subset of the request data to the session. These methods are useful for keeping sensitive information such as passwords out of the session: -->
`flashOnly`와 `flashExcept` 메서드를 사용해서 일부 값만 세션에 저장할 수 있습니다. 민감 정보(예: 비밀번호)는 세션 저장에서 제외할 때 유용합니다.

```
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
<!-- #### Flashing Input Then Redirecting -->
#### Flashing Input Then Redirecting

<!-- Since you often will want to flash input to the session and then redirect to the previous page, you may easily chain input flashing onto a redirect using the `withInput` method: -->
입력값을 세션에 저장하고 이전 페이지로 리다이렉트하는 경우가 많은데, 리다이렉트의 체이닝 메서드로 `withInput`을 사용하면 편리합니다.

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

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/9.x/session): -->
이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 사용하세요. `old` 메서드는 [session](/docs/9.x/session)에서 플래시된 값을 꺼내옵니다.

```
$username = $request->old('username');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/9.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
Laravel에서는 전역 `old` 헬퍼도 제공합니다. [Blade template](/docs/9.x/blade)에서 이전 입력값으로 폼을 다시 채워줄 때 `old` 헬퍼를 더 간편하게 사용할 수 있습니다. 해당 입력값이 없으면 `null`이 반환됩니다.

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
Laravel에서 생성된 모든 쿠키는 암호화되고 인증 코드로 서명되므로, 클라이언트가 값을 임의 변경할 경우 유효하지 않게 처리됩니다. 요청에서 쿠키 값을 조회하려면 `Illuminate\Http\Request`의 `cookie` 메서드를 사용하세요.

```
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
<!-- ## Input Trimming & Normalization -->
## Input Trimming & Normalization

<!-- By default, Laravel includes the `App\Http\Middleware\TrimStrings` and `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` middleware in your application's global middleware stack. These middleware are listed in the global middleware stack by the `App\Http\Kernel` class. These middleware will automatically trim all incoming string fields on the request, as well as convert any empty string fields to `null`. This allows you to not have to worry about these normalization concerns in your routes and controllers. -->
기본적으로 Laravel은 `App\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 전역 미들웨어 스택에 추가합니다(스택은 `App\Http\Kernel` 클래스에서 관리). 이 미들웨어들은 모든 들어오는 문자열 입력값을 자동으로 trim(양쪽 공백 제거)하고, 빈 문자열을 `null`로 변환해줍니다. 그래서 라우트나 컨트롤러에서 이런 정규화를 신경쓰지 않아도 됩니다.

<!-- #### Disabling Input Normalization -->
#### Disabling Input Normalization

<!-- If you would like to disable this behavior for all requests, you may remove the two middleware from your application's middleware stack by removing them from the `$middleware` property of your `App\Http\Kernel` class. -->
이 동작을 모든 요청에 적용하고 싶지 않다면, 애플리케이션의 미들웨어 스택에서 두 미들웨어를 `App\Http\Kernel` 클래스의 `$middleware` 속성에서 제거하면 됩니다.

<!-- If you would like to disable string trimming and empty string conversion for a subset of requests to your application, you may use the `skipWhen` method offered by both middleware. This method accepts a closure which should return `true` or `false` to indicate if input normalization should be skipped. Typically, the `skipWhen` method should be invoked in the `boot` method of your application's `AppServiceProvider`. -->
특정 요청에 한해서만 trim 또는 빈 문자열 변환을 적용하지 않으려면, 두 미들웨어가 제공하는 `skipWhen` 메서드를 사용할 수 있습니다. 이 메서드는 클로저를 받아 input 정규화를 건너뛸지 여부(`true`/`false`)를 반환합니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 `skipWhen`을 호출합니다.

```php
use App\Http\Middleware\TrimStrings;
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    TrimStrings::skipWhen(function ($request) {
        return $request->is('admin/*');
    });

    ConvertEmptyStringsToNull::skipWhen(function ($request) {
        // ...
    });
}
```

<a name="files"></a>
<!-- ## Files -->
## Files

<a name="retrieving-uploaded-files"></a>
<!-- ### Retrieving Uploaded Files -->
### Retrieving Uploaded Files

<!-- You may retrieve uploaded files from an `Illuminate\Http\Request` instance using the `file` method or using dynamic properties. The `file` method returns an instance of the `Illuminate\Http\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file: -->
업로드된 파일은 `Illuminate\Http\Request` 인스턴스에서 `file` 메서드를 사용하거나, 동적 프로퍼티로 조회할 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 이 클래스는 PHP의 `SplFileInfo`를 확장하여 다양한 파일 작업 메서드를 제공합니다.

```
$file = $request->file('photo');

$file = $request->photo;
```

<!-- You may determine if a file is present on the request using the `hasFile` method: -->
파일이 실제로 요청에 포함되어 있는지 확인하려면 `hasFile` 메서드를 사용할 수 있습니다.

```
if ($request->hasFile('photo')) {
    //
}
```

<a name="validating-successful-uploads"></a>
<!-- #### Validating Successful Uploads -->
#### Validating Successful Uploads

<!-- In addition to checking if the file is present, you may verify that there were no problems uploading the file via the `isValid` method: -->
파일이 존재하는지 체크하는 것에 더해, `isValid` 메서드를 사용하면 파일 업로드가 문제 없이 잘 되었는지도 확인할 수 있습니다.

```
if ($request->file('photo')->isValid()) {
    //
}
```

<a name="file-paths-extensions"></a>
<!-- #### File Paths & Extensions -->
#### File Paths & Extensions

<!-- The `UploadedFile` class also contains methods for accessing the file's fully-qualified path and its extension. The `extension` method will attempt to guess the file's extension based on its contents. This extension may be different from the extension that was supplied by the client: -->
`UploadedFile` 클래스는 파일의 전체 경로와 확장자를 가져오는 메서드도 제공합니다. `extension` 메서드는 실제 파일 내용을 바탕으로 확장자를 유추하며, 이는 클라이언트가 제출한 확장자와 다를 수 있습니다.

```
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
<!-- #### Other File Methods -->
#### Other File Methods

<!-- There are a variety of other methods available on `UploadedFile` instances. Check out the [API documentation for the class](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php) for more information regarding these methods. -->
`UploadedFile` 인스턴스에는 위에서 언급한 내용 외에도 다양한 메서드가 있습니다. 보다 자세한 내용은 [API documentation for the class](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하시기 바랍니다.

<a name="storing-uploaded-files"></a>
<!-- ### Storing Uploaded Files -->
### Storing Uploaded Files

<!-- To store an uploaded file, you will typically use one of your configured [filesystems](/docs/9.x/filesystem). The `UploadedFile` class has a `store` method that will move an uploaded file to one of your disks, which may be a location on your local filesystem or a cloud storage location like Amazon S3. -->
업로드된 파일을 저장하려면 보통 [filesystems](/docs/9.x/filesystem)을 구성하고, `UploadedFile` 클래스의 `store` 메서드를 사용합니다. 이때 파일은 로컬 파일시스템이나 Amazon S3 등 원하는 저장소에 저장할 수 있습니다.

<!-- The `store` method accepts the path where the file should be stored relative to the filesystem's configured root directory. This path should not contain a filename, since a unique ID will automatically be generated to serve as the filename. -->
`store` 메서드는 파일 저장 경로(파일시스템의 루트 기준 상대 경로)를 첫 번째 인자로 받습니다. 이때 파일명은 지정하지 않고, Laravel이 자동으로 고유한 파일명을 생성합니다.

<!-- The `store` method also accepts an optional second argument for the name of the disk that should be used to store the file. The method will return the path of the file relative to the disk's root: -->
`store` 메서드의 두 번째 인자로 사용할 저장소 디스크명을 지정할 수 있습니다. 반환값은 지정한 경로(디스크 루트 기준)입니다.

```
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

<!-- If you do not want a filename to be automatically generated, you may use the `storeAs` method, which accepts the path, filename, and disk name as its arguments: -->
파일명을 직접 지정하고 싶다면, `storeAs` 메서드를 사용합니다. 경로, 파일명, 디스크명을 차례로 입력합니다.

```
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> Laravel의 파일 저장에 대해 더 알고 싶다면 [file storage documentation](/docs/9.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
<!-- ## Configuring Trusted Proxies -->
## Configuring Trusted Proxies

<!-- When running your applications behind a load balancer that terminates TLS / SSL certificates, you may notice your application sometimes does not generate HTTPS links when using the `url` helper. Typically this is because your application is being forwarded traffic from your load balancer on port 80 and does not know it should generate secure links. -->
TLS/SSL 인증서를 종료시키는 로드 밸런서 뒤에서 애플리케이션을 실행할 경우, `url` 헬퍼 등을 사용할 때 가끔 HTTPS 링크가 아닌 일반 HTTP 링크가 생성되는 경우가 있습니다. 이는 대개 로드 밸런서가 80번 포트로 트래픽을 전달하므로, 애플리케이션 쪽에서 안전한 연결임을 인지하지 못하기 때문입니다.

<!-- To solve this, you may use the `App\Http\Middleware\TrustProxies` middleware that is included in your Laravel application, which allows you to quickly customize the load balancers or proxies that should be trusted by your application. Your trusted proxies should be listed as an array on the `$proxies` property of this middleware. In addition to configuring the trusted proxies, you may configure the proxy `$headers` that should be trusted: -->
이럴 때는, Laravel에 기본 포함된 `App\Http\Middleware\TrustProxies` 미들웨어를 이용해 신뢰할 수 있는 로드 밸런서 또는 프록시를 쉽게 커스터마이즈 할 수 있습니다. 신뢰할 프록시는 이 미들웨어의 `$proxies` 프로퍼티에 배열로 지정하면 됩니다. 아울러 사용할 프록시 `$headers`도 설정할 수 있습니다.

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

> [!NOTE]
> AWS Elastic Load Balancing을 사용할 경우, `$headers`는 `Request::HEADER_X_FORWARDED_AWS_ELB`로 지정해야 합니다. `$headers` 프로퍼티에 사용 가능한 상수 정보는 Symfony의 [trusting proxies](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
<!-- #### Trusting All Proxies -->
#### Trusting All Proxies

<!-- If you are using Amazon AWS or another "cloud" load balancer provider, you may not know the IP addresses of your actual balancers. In this case, you may use `*` to trust all proxies: -->
Amazon AWS 같은 클라우드 로드 밸런서 환경에서는 실제 밸런서의 IP를 알 수 없는 경우도 있습니다. 이럴 때는 `*`을 사용해서 모든 프록시를 신뢰할 수 있습니다.

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
Laravel은 기본적으로 HTTP 요청의 `Host` 헤더 내용과 상관없이 모든 요청에 응답합니다. 또한 웹 요청 중 애플리케이션의 절대 URL을 생성할 때도 `Host` 헤더의 값이 사용됩니다.

<!-- Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given host name. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain host names, you may do so by enabling the `App\Http\Middleware\TrustHosts` middleware for your application. -->
일반적으로는 Nginx 또는 Apache와 같은 웹 서버에서, 특정 호스트명과 일치하는 요청만 애플리케이션으로 전달하도록 설정하는 것이 바람직합니다. 직접 웹 서버를 설정할 수 없는 상황이라면, Laravel의 `App\Http\Middleware\TrustHosts` 미들웨어를 활성화해, Laravel에서 직접 응답할 호스트명을 제한할 수도 있습니다.

<!-- The `TrustHosts` middleware is already included in the `$middleware` stack of your application; however, you should uncomment it so that it becomes active. Within this middleware's `hosts` method, you may specify the host names that your application should respond to. Incoming requests with other `Host` value headers will be rejected: -->
`TrustHosts` 미들웨어는 애플리케이션의 `$middleware` 스택에 이미 포함되어 있으므로, 주석 처리를 해제하여 활성화할 수 있습니다. 미들웨어의 `hosts` 메서드에서, 애플리케이션에서 응답할 호스트명을 지정합니다. 이 외의 `Host` 값으로 들어오는 요청은 거부됩니다.

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
`allSubdomainsOfApplicationUrl` 헬퍼 메서드는 애플리케이션의 `app.url` 설정 값을 기준으로, 모든 서브도메인과 매칭되는 정규식을 반환합니다. 와일드카드 서브도메인을 허용하는 애플리케이션을 개발할 때 유용하게 활용할 수 있습니다.
