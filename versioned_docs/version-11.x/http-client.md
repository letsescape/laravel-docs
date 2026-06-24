<!-- # HTTP Client -->
# HTTP Client

- [Introduction](#introduction)
- [Making Requests](#making-requests)
    - [Request Data](#request-data)
    - [Headers](#headers)
    - [Authentication](#authentication)
    - [Timeout](#timeout)
    - [Retries](#retries)
    - [Error Handling](#error-handling)
    - [Guzzle Middleware](#guzzle-middleware)
    - [Guzzle Options](#guzzle-options)
- [Concurrent Requests](#concurrent-requests)
- [Macros](#macros)
- [Testing](#testing)
    - [Faking Responses](#faking-responses)
    - [Inspecting Requests](#inspecting-requests)
    - [Preventing Stray Requests](#preventing-stray-requests)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides an expressive, minimal API around the [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/), allowing you to quickly make outgoing HTTP requests to communicate with other web applications. Laravel's wrapper around Guzzle is focused on its most common use cases and a wonderful developer experience. -->
Laravel은 [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/)를 감싸는 간결하고 직관적인 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 쉽게 보낼 수 있습니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례에 집중되어 있으며, 쾌적한 개발자 경험을 제공합니다.

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make requests, you may use the `head`, `get`, `post`, `put`, `patch`, and `delete` methods provided by the `Http` facade. First, let's examine how to make a basic `GET` request to another URL: -->
요청을 보내기 위해서는 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

<!-- The `get` method returns an instance of `Illuminate\Http\Client\Response`, which provides a variety of methods that may be used to inspect the response: -->
`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 이를 통해 다양한 방식으로 응답을 확인할 수 있습니다.

```
$response->body() : string;
$response->json($key = null, $default = null) : mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->resource() : resource;
$response->status() : int;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

<!-- The `Illuminate\Http\Client\Response` object also implements the PHP `ArrayAccess` interface, allowing you to access JSON response data directly on the response: -->
`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있으므로, 아래와 같이 JSON 형식의 응답 데이터를 배열처럼 바로 접근할 수 있습니다.

```
return Http::get('http://example.com/users/1')['name'];
```

<!-- In addition to the response methods listed above, the following methods may be used to determine if the response has a given status code: -->
위에 소개된 응답 관련 메서드들 외에도, 응답이 특정 HTTP 상태코드를 가지는지 확인할 때 사용할 수 있는 메서드는 다음과 같습니다.

```
$response->ok() : bool;                  // 200 OK
$response->created() : bool;             // 201 Created
$response->accepted() : bool;            // 202 Accepted
$response->noContent() : bool;           // 204 No Content
$response->movedPermanently() : bool;    // 301 Moved Permanently
$response->found() : bool;               // 302 Found
$response->badRequest() : bool;          // 400 Bad Request
$response->unauthorized() : bool;        // 401 Unauthorized
$response->paymentRequired() : bool;     // 402 Payment Required
$response->forbidden() : bool;           // 403 Forbidden
$response->notFound() : bool;            // 404 Not Found
$response->requestTimeout() : bool;      // 408 Request Timeout
$response->conflict() : bool;            // 409 Conflict
$response->unprocessableEntity() : bool; // 422 Unprocessable Entity
$response->tooManyRequests() : bool;     // 429 Too Many Requests
$response->serverError() : bool;         // 500 Internal Server Error
```

<a name="uri-templates"></a>
<!-- #### URI Templates -->
#### URI Templates

<!-- The HTTP client also allows you to construct request URLs using the [URI template specification](https://www.rfc-editor.org/rfc/rfc6570). To define the URL parameters that can be expanded by your URI template, you may use the `withUrlParameters` method: -->
Laravel HTTP 클라이언트는 [URI template specification](https://www.rfc-editor.org/rfc/rfc6570)를 이용하여 요청 URL을 동적으로 구성할 수 있습니다. `withUrlParameters` 메서드를 사용하면 URI 템플릿에서 확장할 수 있는 URL 파라미터들을 지정할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '11.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
<!-- #### Dumping Requests -->
#### Dumping Requests

<!-- If you would like to dump the outgoing request instance before it is sent and terminate the script's execution, you may add the `dd` method to the beginning of your request definition: -->
보내기 전에 요청 인스턴스를 확인하고, 코드 실행을 즉시 종료하고 싶을 때는, 요청 정의의 앞부분에 `dd` 메서드를 추가하면 됩니다.

```
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
<!-- ### Request Data -->
### Request Data

<!-- Of course, it is common when making `POST`, `PUT`, and `PATCH` requests to send additional data with your request, so these methods accept an array of data as their second argument. By default, data will be sent using the `application/json` content type: -->
일반적으로 `POST`, `PUT`, `PATCH` 요청을 보낼 때는 추가 데이터를 함께 전송하게 됩니다. 이 메서드들은 두 번째 인자로 배열 형태의 데이터를 받을 수 있습니다. 기본적으로 이 데이터는 `application/json` Content-Type으로 전송됩니다.

```
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
<!-- #### GET Request Query Parameters -->
#### GET Request Query Parameters

<!-- When making `GET` requests, you may either append a query string to the URL directly or pass an array of key / value pairs as the second argument to the `get` method: -->
`GET` 요청 시에는 쿼리 스트링을 URL에 바로 붙이거나, `get` 메서드의 두 번째 인자로 키/값 쌍의 배열을 전달할 수 있습니다.

```
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

<!-- Alternatively, the `withQueryParameters` method may be used: -->
또한, `withQueryParameters` 메서드를 활용할 수도 있습니다.

```
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users')
```

<a name="sending-form-url-encoded-requests"></a>
<!-- #### Sending Form URL Encoded Requests -->
#### Sending Form URL Encoded Requests

<!-- If you would like to send data using the `application/x-www-form-urlencoded` content type, you should call the `asForm` method before making your request: -->
`application/x-www-form-urlencoded` Content-Type을 사용하여 데이터를 전송하고 싶다면, 요청 전에 `asForm` 메서드를 호출하십시오.

```
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
<!-- #### Sending a Raw Request Body -->
#### Sending a Raw Request Body

<!-- You may use the `withBody` method if you would like to provide a raw request body when making a request. The content type may be provided via the method's second argument: -->
요청 시에 raw 데이터를 직접 본문으로 보낼 경우에는 `withBody` 메서드를 사용할 수 있습니다. Content-Type은 두 번째 인자로 지정할 수 있습니다.

```
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
<!-- #### Multi-Part Requests -->
#### Multi-Part Requests

<!-- If you would like to send files as multi-part requests, you should call the `attach` method before making your request. This method accepts the name of the file and its contents. If needed, you may provide a third argument which will be considered the file's filename, while a fourth argument may be used to provide headers associated with the file: -->
파일을 멀티파트 형식으로 전송하려면, 요청 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일 이름과 파일의 내용을 인자로 받으며, 필요하다면 세 번째 인자로 파일 이름을, 네 번째 인자로 파일과 관련된 헤더를 지정할 수 있습니다.

```
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

<!-- Instead of passing the raw contents of a file, you may pass a stream resource: -->
파일의 raw 내용 대신 스트림 리소스를 전달할 수도 있습니다.

```
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
<!-- ### Headers -->
### Headers

<!-- Headers may be added to requests using the `withHeaders` method. This `withHeaders` method accepts an array of key / value pairs: -->
`withHeaders` 메서드를 사용하면 요청에 헤더를 추가할 수 있습니다. 이 `withHeaders` 메서드는 키/값 쌍의 배열을 받습니다.

```
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<!-- You may use the `accept` method to specify the content type that your application is expecting in response to your request: -->
`accept` 메서드를 사용하면, 요청에 대한 응답으로 애플리케이션이 기대하는 Content-Type을 명시할 수 있습니다.

```
$response = Http::accept('application/json')->get('http://example.com/users');
```

<!-- For convenience, you may use the `acceptJson` method to quickly specify that your application expects the `application/json` content type in response to your request: -->
편의를 위해, 응답에서 `application/json` Content-Type을 기대할 경우에는 `acceptJson` 메서드를 사용할 수 있습니다.

```
$response = Http::acceptJson()->get('http://example.com/users');
```

<!-- The `withHeaders` method merges new headers into the request's existing headers. If needed, you may replace all of the headers entirely using the `replaceHeaders` method: -->
`withHeaders` 메서드는 새 헤더를 기존 요청 헤더에 병합합니다. 모든 헤더를 완전히 교체하고 싶을 때는 `replaceHeaders` 메서드를 사용하면 됩니다.

```php
$response = Http::withHeaders([
    'X-Original' => 'foo',
])->replaceHeaders([
    'X-Replacement' => 'bar',
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<a name="authentication"></a>
<!-- ### Authentication -->
### Authentication

<!-- You may specify basic and digest authentication credentials using the `withBasicAuth` and `withDigestAuth` methods, respectively: -->
기본 인증과 다이제스트 인증 정보를 각각 `withBasicAuth`, `withDigestAuth` 메서드를 통해 지정할 수 있습니다.

```
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
<!-- #### Bearer Tokens -->
#### Bearer Tokens

<!-- If you would like to quickly add a bearer token to the request's `Authorization` header, you may use the `withToken` method: -->
요청의 `Authorization` 헤더에 bearer 토큰을 간단하게 추가하고 싶을 때는, `withToken` 메서드를 이용할 수 있습니다.

```
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
<!-- ### Timeout -->
### Timeout

<!-- The `timeout` method may be used to specify the maximum number of seconds to wait for a response. By default, the HTTP client will timeout after 30 seconds: -->
`timeout` 메서드는 응답을 기다리는 동안 허용할 최대 초(sec) 단위를 지정합니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃 처리합니다.

```
$response = Http::timeout(3)->get(/* ... */);
```

<!-- If the given timeout is exceeded, an instance of `Illuminate\Http\Client\ConnectionException` will  be thrown. -->
지정한 타임아웃보다 오래 걸리면, `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

<!-- You may specify the maximum number of seconds to wait while trying to connect to a server using the `connectTimeout` method: -->
서버에 연결되는 동안 대기할 최대 초 단위를 지정하고 싶을 때는 `connectTimeout` 메서드를 사용할 수 있습니다.

```
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
<!-- ### Retries -->
### Retries

<!-- If you would like the HTTP client to automatically retry the request if a client or server error occurs, you may use the `retry` method. The `retry` method accepts the maximum number of times the request should be attempted and the number of milliseconds that Laravel should wait in between attempts: -->
클라이언트 또는 서버 에러가 발생할 경우, HTTP 클라이언트가 자동으로 요청을 다시 시도하도록 하려면 `retry` 메서드를 사용하십시오. `retry` 메서드는 최대 요청 시도 횟수와, 각 시도 사이에 대기할 밀리초(ms) 단위를 인자로 받습니다.

```
$response = Http::retry(3, 100)->post(/* ... */);
```

<!-- If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the second argument to the `retry` method: -->
매 시도마다 대기할 밀리초(ms) 수를 직접 계산하고 싶을 때는, `retry` 메서드의 두 번째 인자로 클로저를 전달할 수 있습니다.

```
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

<!-- For convenience, you may also provide an array as the first argument to the `retry` method. This array will be used to determine how many milliseconds to sleep between subsequent attempts: -->
또한, `retry` 메서드의 첫 번째 인자로 배열을 전달해 각 재시도 사이 대기시간을 설정할 수도 있습니다.

```
$response = Http::retry([100, 200])->post(/* ... */);
```

<!-- If needed, you may pass a third argument to the `retry` method. The third argument should be a callable that determines if the retries should actually be attempted. For example, you may wish to only retry the request if the initial request encounters an `ConnectionException`: -->
필요하다면 `retry` 메서드에 세 번째 인자로 호출 가능한(callback) 값을 전달할 수 있습니다. 이 값은 실제로 재시도를 시도해야 하는지 여부를 결정합니다. 예를 들어, 최초 요청이 `ConnectionException`을 만났을 때만 재시도하도록 할 수 있습니다.

```
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

<!-- If a request attempt fails, you may wish to make a change to the request before a new attempt is made. You can achieve this by modifying the request argument provided to the callable you provided to the `retry` method. For example, you might want to retry the request with a new authorization token if the first attempt returned an authentication error: -->
요청 시도가 실패했을 때, 다음 시도 전에 요청을 변경하고 싶을 때는, `retry` 메서드에 전달한 콜러블에서 요청 객체를 수정하면 됩니다. 예를 들어, 첫 번째 시도에서 인증 에러가 반환된다면 새로운 인증 토큰을 사용해 재시도할 수 있습니다.

```
use Exception;
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\RequestException;

$response = Http::withToken($this->getToken())->retry(2, 0, function (Exception $exception, PendingRequest $request) {
    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
        return false;
    }

    $request->withToken($this->getNewToken());

    return true;
})->post(/* ... */);
```

<!-- If all of the requests fail, an instance of `Illuminate\Http\Client\RequestException` will be thrown. If you would like to disable this behavior, you may provide a `throw` argument with a value of `false`. When disabled, the last response received by the client will be returned after all retries have been attempted: -->
모든 요청이 실패한 경우에는 `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 비활성화하려면 `throw` 인자에 `false` 값을 전달하면 됩니다. 이때는 모든 재시도 후 마지막으로 받은 응답이 반환됩니다.

```
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 인해 실패한 경우, `throw` 인자 값이 `false`라도 `Illuminate\Http\Client\ConnectionException` 예외는 여전히 발생합니다.

<a name="error-handling"></a>
<!-- ### Error Handling -->
### Error Handling

<!-- Unlike Guzzle's default behavior, Laravel's HTTP client wrapper does not throw exceptions on client or server errors (`400` and `500` level responses from servers). You may determine if one of these errors was returned using the `successful`, `clientError`, or `serverError` methods: -->
Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 에러(`400` 또는 `500` 레벨 응답)가 발생해도 예외를 자동으로 발생시키지 않습니다. 대신, 이러한 에러가 반환되었는지 확인하려면 `successful`, `clientError`, `serverError` 메서드를 사용할 수 있습니다.

```
// Determine if the status code is >= 200 and < 300...
$response->successful();

// Determine if the status code is >= 400...
$response->failed();

// Determine if the response has a 400 level status code...
$response->clientError();

// Determine if the response has a 500 level status code...
$response->serverError();

// Immediately execute the given callback if there was a client or server error...
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
<!-- #### Throwing Exceptions -->
#### Throwing Exceptions

<!-- If you have a response instance and would like to throw an instance of `Illuminate\Http\Client\RequestException` if the response status code indicates a client or server error, you may use the `throw` or `throwIf` methods: -->
응답 인스턴스를 가지고 있고, 상태 코드가 클라이언트 또는 서버 에러를 의미할 때 `Illuminate\Http\Client\RequestException` 예외를 발생시키고 싶다면, `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// Throw an exception if a client or server error occurred...
$response->throw();

// Throw an exception if an error occurred and the given condition is true...
$response->throwIf($condition);

// Throw an exception if an error occurred and the given closure resolves to true...
$response->throwIf(fn (Response $response) => true);

// Throw an exception if an error occurred and the given condition is false...
$response->throwUnless($condition);

// Throw an exception if an error occurred and the given closure resolves to false...
$response->throwUnless(fn (Response $response) => false);

// Throw an exception if the response has a specific status code...
$response->throwIfStatus(403);

// Throw an exception unless the response has a specific status code...
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

<!-- The `Illuminate\Http\Client\RequestException` instance has a public `$response` property which will allow you to inspect the returned response. -->
`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 확인할 수 있도록 public `$response` 프로퍼티가 있습니다.

<!-- The `throw` method returns the response instance if no error occurred, allowing you to chain other operations onto the `throw` method: -->
`throw` 메서드는 에러가 없으면 응답 인스턴스를 그대로 반환하므로, `throw` 메서드에 이어서 다른 작업을 체이닝(연결)할 수 있습니다.

```
return Http::post(/* ... */)->throw()->json();
```

<!-- If you would like to perform some additional logic before the exception is thrown, you may pass a closure to the `throw` method. The exception will be thrown automatically after the closure is invoked, so you do not need to re-throw the exception from within the closure: -->
예외가 발생하기 전 추가 로직을 수행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 이 클로저가 실행된 후 예외는 자동으로 던져지므로, 클로저 안에서 예외를 다시 던질 필요는 없습니다.

```
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

<!-- By default, `RequestException` messages are truncated to 120 characters when logged or reported. To customize or disable this behavior, you may utilize the `truncateRequestExceptionsAt` and `dontTruncateRequestExceptions` methods when configuring your application's exception handling behavior in your `bootstrap/app.php` file: -->
기본적으로 `RequestException` 메시지는 120자까지만 기록되거나 보고됩니다. 이 동작을 커스터마이즈하거나 비활성화하고자 할 때는, 애플리케이션의 `bootstrap/app.php` 파일에서 `truncateRequestExceptionsAt` 과 `dontTruncateRequestExceptions` 메서드를 사용할 수 있습니다.

```
->withExceptions(function (Exceptions $exceptions) {
    // Truncate request exception messages to 240 characters...
    $exceptions->truncateRequestExceptionsAt(240);

    // Disable request exception message truncation...
    $exceptions->dontTruncateRequestExceptions();
})
```

<a name="guzzle-middleware"></a>
<!-- ### Guzzle Middleware -->
### Guzzle Middleware

<!-- Since Laravel's HTTP client is powered by Guzzle, you may take advantage of [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) to manipulate the outgoing request or inspect the incoming response. To manipulate the outgoing request, register a Guzzle middleware via the `withRequestMiddleware` method: -->
Laravel의 HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 통해 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 수정하려면, `withRequestMiddleware` 메서드를 사용해 Guzzle 미들웨어를 등록하십시오.

```
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

<!-- Likewise, you can inspect the incoming HTTP response by registering a middleware via the `withResponseMiddleware` method: -->
마찬가지로, 받는 HTTP 응답을 검사하려면 `withResponseMiddleware` 메서드에 미들웨어를 등록할 수 있습니다.

```
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\ResponseInterface;

$response = Http::withResponseMiddleware(
    function (ResponseInterface $response) {
        $header = $response->getHeader('X-Example');

        // ...

        return $response;
    }
)->get('http://example.com');
```

<a name="global-middleware"></a>
<!-- #### Global Middleware -->
#### Global Middleware

<!-- Sometimes, you may want to register a middleware that applies to every outgoing request and incoming response. To accomplish this, you may use the `globalRequestMiddleware` and `globalResponseMiddleware` methods. Typically, these methods should be invoked in the `boot` method of your application's `AppServiceProvider`: -->
모든 나가는 요청과 들어오는 응답에 대해 한 번에 적용되는 미들웨어를 등록하고 싶을 때는 `globalRequestMiddleware` 와 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 일반적으로 이러한 메서드는 애플리케이션의 `AppServiceProvider` 의 `boot` 메서드에서 호출해야 합니다.

```php
use Illuminate\Support\Facades\Http;

Http::globalRequestMiddleware(fn ($request) => $request->withHeader(
    'User-Agent', 'Example Application/1.0'
));

Http::globalResponseMiddleware(fn ($response) => $response->withHeader(
    'X-Finished-At', now()->toDateTimeString()
));
```

<a name="guzzle-options"></a>
<!-- ### Guzzle Options -->
### Guzzle Options

<!-- You may specify additional [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html) for an outgoing request using the `withOptions` method. The `withOptions` method accepts an array of key / value pairs: -->
나가는 요청에 대해 [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html) 을 지정하려면, `withOptions` 메서드를 사용할 수 있습니다. 이 `withOptions` 메서드는 키/값 쌍의 배열을 인자로 받습니다.

```
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
<!-- #### Global Options -->
#### Global Options

<!-- To configure default options for every outgoing request, you may utilize the `globalOptions` method. Typically, this method should be invoked from the `boot` method of your application's `AppServiceProvider`: -->
모든 나가는 요청의 기본 옵션을 설정하려면, `globalOptions` 메서드를 활용하세요. 이 메서드는 일반적으로 애플리케이션의 `AppServiceProvider` 의 `boot` 메서드에서 호출해야 합니다.

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::globalOptions([
        'allow_redirects' => false,
    ]);
}
```

<a name="concurrent-requests"></a>
<!-- ## Concurrent Requests -->
## Concurrent Requests

<!-- Sometimes, you may wish to make multiple HTTP requests concurrently. In other words, you want several requests to be dispatched at the same time instead of issuing the requests sequentially. This can lead to substantial performance improvements when interacting with slow HTTP APIs. -->
여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 여러 요청을 순차적으로 보내는 것이 아니라, 여러 요청을 한 번에 발송해 처리 속도를 크게 높이고자 할 때 사용할 수 있습니다. 천천히 동작하는 HTTP API를 사용할 때 성능이 크게 개선될 수 있습니다.

<!-- Thankfully, you may accomplish this using the `pool` method. The `pool` method accepts a closure which receives an `Illuminate\Http\Client\Pool` instance, allowing you to easily add requests to the request pool for dispatching: -->
이럴 때는 `pool` 메서드를 사용하면 됩니다. `pool` 메서드에는 `Illuminate\Http\Client\Pool` 인스턴스를 인자로 받는 클로저를 전달하여, 한 번에 여러 요청을 손쉽게 풀에 추가하고 발송할 수 있습니다.

```
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->get('http://localhost/first'),
    $pool->get('http://localhost/second'),
    $pool->get('http://localhost/third'),
]);

return $responses[0]->ok() &&
       $responses[1]->ok() &&
       $responses[2]->ok();
```

<!-- As you can see, each response instance can be accessed based on the order it was added to the pool. If you wish, you can name the requests using the `as` method, which allows you to access the corresponding responses by name: -->
보시다시피 각 응답 인스턴스는 풀에 추가된 순서대로 배열 인덱스로 접근할 수 있습니다. 필요하다면 `as` 메서드를 사용해 각 요청을 이름으로 지정할 수 있고, 응답도 해당 이름으로 접근할 수 있습니다.

```
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```

<a name="customizing-concurrent-requests"></a>
<!-- #### Customizing Concurrent Requests -->
#### Customizing Concurrent Requests

<!-- The `pool` method cannot be chained with other HTTP client methods such as the `withHeaders` or `middleware` methods. If you want to apply custom headers or middleware to pooled requests, you should configure those options on each request in the pool: -->
`pool` 메서드는 `withHeaders`나 `middleware`와 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 만약 풀에 추가하는 각 요청에 커스텀 헤더나 미들웨어를 적용하고 싶다면, 각 풀 요청에서 해당 옵션을 직접 지정해야 합니다.

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$headers = [
    'X-Example' => 'example',
];

$responses = Http::pool(fn (Pool $pool) => [
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
]);
```

<a name="macros"></a>
<!-- ## Macros -->
## Macros

<!-- The Laravel HTTP client allows you to define "macros", which can serve as a fluent, expressive mechanism to configure common request paths and headers when interacting with services throughout your application. To get started, you may define the macro within the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
Laravel HTTP 클라이언트는 "매크로" 기능을 제공합니다. 매크로를 통해 애플리케이션 전역에서 서비스별 공통 경로나 헤더를 간결하게 구성할 수 있으며, 직관적이고 유창한 방식으로 재사용할 수 있습니다. 먼저, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 매크로를 정의하세요.

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```

<!-- Once your macro has been configured, you may invoke it from anywhere in your application to create a pending request with the specified configuration: -->
매크로를 정의한 뒤에는, 애플리케이션 어디에서나 지정한 설정으로 미리 구성된 요청을 만들 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>

<!-- ## Testing -->
## Testing

<!-- Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's HTTP client is no exception. The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made. -->
Laravel의 다양한 서비스는 테스트 작성이 쉽고 직관적으로 이뤄질 수 있도록 다양한 기능을 제공합니다. Laravel의 HTTP 클라이언트 역시 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 요청이 발생할 때 더미(Stub) 또는 가짜(Dummy) 응답을 반환하도록 HTTP 클라이언트를 설정할 수 있습니다.

<a name="faking-responses"></a>
<!-- ### Faking Responses -->
### Faking Responses

<!-- For example, to instruct the HTTP client to return empty, `200` status code responses for every request, you may call the `fake` method with no arguments: -->
예를 들어, 모든 요청에 대해 비어 있는, 상태 코드가 `200`인 응답을 반환하도록 HTTP 클라이언트를 설정하려면 `fake` 메서드를 인수 없이 호출하면 됩니다.

```
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
<!-- #### Faking Specific URLs -->
#### Faking Specific URLs

<!-- Alternatively, you may pass an array to the `fake` method. The array's keys should represent URL patterns that you wish to fake and their associated responses. The `*` character may be used as a wildcard character. Any requests made to URLs that have not been faked will actually be executed. You may use the `Http` facade's `response` method to construct stub / fake responses for these endpoints: -->
또는, `fake` 메서드에 배열을 전달할 수도 있습니다. 이 배열의 키는 가짜 응답을 설정하고 싶은 URL 패턴을 나타내며, 값은 응답 객체입니다. `*` 문자는 와일드카드로 사용할 수 있습니다. 가짜 응답이 설정되지 않은 URL에 대한 요청은 실제로 전송됩니다. 이러한 엔드포인트에 대해 가짜 응답을 만들려면 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다.

```
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

<!-- If you would like to specify a fallback URL pattern that will stub all unmatched URLs, you may use a single `*` character: -->
모든 일치하지 않는 URL에도 가짜 응답을 적용하는 기본 패턴을 지정하고 싶다면, `*` 하나만 사용하면 됩니다.

```
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

<!-- For convenience, simple string, JSON, and empty responses may be generated by providing a string, array, or integer as the response: -->
편의상, 문자열, JSON, 빈 응답 등은 문자열, 배열, 정수를 응답값으로 제공해서도 생성할 수 있습니다.

```
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
<!-- #### Faking Connection Exceptions -->
#### Faking Connection Exceptions

<!-- Sometimes you may need to test your application's behavior if the HTTP client encounters an `Illuminate\Http\Client\ConnectionException` when attempting to make a request. You can instruct the HTTP client to throw a connection exception using the `failedConnection` method: -->
가끔 애플리케이션이 요청을 시도할 때 `Illuminate\Http\Client\ConnectionException`이 발생하는 경우를 테스트해야 할 수도 있습니다. 이때 `failedConnection` 메서드를 사용하여 HTTP 클라이언트가 연결 예외를 발생시키도록 설정할 수 있습니다.

```
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

<a name="faking-response-sequences"></a>
<!-- #### Faking Response Sequences -->
#### Faking Response Sequences

<!-- Sometimes you may need to specify that a single URL should return a series of fake responses in a specific order. You may accomplish this using the `Http::sequence` method to build the responses: -->
특정 URL이 여러 개의 가짜 응답을 순서대로 반환해야 하는 경우가 있습니다. 이럴 때 `Http::sequence` 메서드를 사용해 응답 시퀀스를 만들 수 있습니다.

```
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

<!-- When all the responses in a response sequence have been consumed, any further requests will cause the response sequence to throw an exception. If you would like to specify a default response that should be returned when a sequence is empty, you may use the `whenEmpty` method: -->
시퀀스에 포함된 모든 응답이 소진된 이후에 추가적인 요청이 오면 예외가 발생합니다. 만약 시퀀스가 비었을 때 반환할 기본 응답을 지정하고 싶다면 `whenEmpty` 메서드를 사용합니다.

```
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

<!-- If you would like to fake a sequence of responses but do not need to specify a specific URL pattern that should be faked, you may use the `Http::fakeSequence` method: -->
특정 URL 패턴을 지정하지 않고도 응답 시퀀스를 가짜 처리하고 싶다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
<!-- #### Fake Callback -->
#### Fake Callback

<!-- If you require more complicated logic to determine what responses to return for certain endpoints, you may pass a closure to the `fake` method. This closure will receive an instance of `Illuminate\Http\Client\Request` and should return a response instance. Within your closure, you may perform whatever logic is necessary to determine what type of response to return: -->
특정 엔드포인트에 대해 반환할 응답을 결정하는 더 복잡한 로직이 필요하다면, `fake` 메서드에 클로저(익명함수)를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 전달받으며, 응답 인스턴스를 반환해야 합니다. 클로저 내부에서 원하는 모든 판단 로직을 수행할 수 있습니다.

```
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
<!-- ### Preventing Stray Requests -->
### Preventing Stray Requests

<!-- If you would like to ensure that all requests sent via the HTTP client have been faked throughout your individual test or complete test suite, you can call the `preventStrayRequests` method. After calling this method, any requests that do not have a corresponding fake response will throw an exception rather than making the actual HTTP request: -->
테스트 단위나 전체 테스트 스위트에서, HTTP 클라이언트로 전송하는 모든 요청이 반드시 가짜 처리되었는지 보장하고 싶다면 `preventStrayRequests` 메서드를 호출할 수 있습니다. 이 메서드 호출 이후, 가짜 응답이 설정되지 않은 요청이 발생하면 실제 요청을 보내는 대신 예외가 발생합니다.

```
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// An "ok" response is returned...
Http::get('https://github.com/laravel/framework');

// An exception is thrown...
Http::get('https://laravel.com');
```

<a name="inspecting-requests"></a>
<!-- ### Inspecting Requests -->
### Inspecting Requests

<!-- When faking responses, you may occasionally wish to inspect the requests the client receives in order to make sure your application is sending the correct data or headers. You may accomplish this by calling the `Http::assertSent` method after calling `Http::fake`. -->
가짜 응답을 설정할 때, 실제로 애플리케이션이 올바른 데이터나 헤더 등을 포함하여 요청하는지 검사하고 싶을 수 있습니다. 이럴 때는 `Http::fake` 이후에 `Http::assertSent` 메서드를 호출하면 됩니다.

<!-- The `assertSent` method accepts a closure which will receive an `Illuminate\Http\Client\Request` instance and should return a boolean value indicating if the request matches your expectations. In order for the test to pass, at least one request must have been issued matching the given expectations: -->
`assertSent` 메서드는 클로저를 인수로 받으며, 클로저에는 `Illuminate\Http\Client\Request` 인스턴스가 전달됩니다. 그리고 클로저는 요청이 기대에 부합하는지 여부를 나타내는 불리언을 반환해야 합니다. 테스트가 통과하려면 하나 이상의 요청이 해당 조건을 만족해야 합니다.

```
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::withHeaders([
    'X-First' => 'foo',
])->post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertSent(function (Request $request) {
    return $request->hasHeader('X-First', 'foo') &&
           $request->url() == 'http://example.com/users' &&
           $request['name'] == 'Taylor' &&
           $request['role'] == 'Developer';
});
```

<!-- If needed, you may assert that a specific request was not sent using the `assertNotSent` method: -->
필요하다면 `assertNotSent` 메서드를 사용해서 특정 요청이 전송되지 않았음을 검증할 수도 있습니다.

```
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertNotSent(function (Request $request) {
    return $request->url() === 'http://example.com/posts';
});
```

<!-- You may use the `assertSentCount` method to assert how many requests were "sent" during the test: -->
`assertSentCount` 메서드를 사용하면 테스트 중 "전송된" 요청의 개수를 검증할 수 있습니다.

```
Http::fake();

Http::assertSentCount(5);
```

<!-- Or, you may use the `assertNothingSent` method to assert that no requests were sent during the test: -->
또는, 테스트 중 요청이 전혀 전송되지 않았음을 확인하려면 `assertNothingSent` 메서드를 사용할 수 있습니다.

```
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
<!-- #### Recording Requests / Responses -->
#### Recording Requests / Responses

<!-- You may use the `recorded` method to gather all requests and their corresponding responses. The `recorded` method returns a collection of arrays that contains instances of `Illuminate\Http\Client\Request` and `Illuminate\Http\Client\Response`: -->
`recorded` 메서드를 사용하면 모든 요청과 그에 대응하는 응답을 모아볼 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스로 구성된 배열 컬렉션을 반환합니다.

```php
Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded();

[$request, $response] = $recorded[0];
```

<!-- Additionally, the `recorded` method accepts a closure which will receive an instance of `Illuminate\Http\Client\Request` and `Illuminate\Http\Client\Response` and may be used to filter request / response pairs based on your expectations: -->
또한, `recorded` 메서드에 클로저를 전달하면, `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 인수로 받아서 원하는 조건으로 요청/응답 쌍을 필터링할 수 있습니다.

```php
use Illuminate\Http\Client\Request;
use Illuminate\Http\Client\Response;

Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded(function (Request $request, Response $response) {
    return $request->url() !== 'https://laravel.com' &&
           $response->successful();
});
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel fires three events during the process of sending HTTP requests. The `RequestSending` event is fired prior to a request being sent, while the `ResponseReceived` event is fired after a response is received for a given request. The `ConnectionFailed` event is fired if no response is received for a given request. -->
Laravel은 HTTP 요청을 전송하는 과정에서 세 가지 이벤트를 발생시킵니다. 요청을 전송하기 전에 `RequestSending` 이벤트가 발생하고, 요청에 대한 응답을 수신한 후에는 `ResponseReceived` 이벤트가 발생합니다. 주어진 요청에 응답이 없는 경우에는 `ConnectionFailed` 이벤트가 발생합니다.

<!-- The `RequestSending` and `ConnectionFailed` events both contain a public `$request` property that you may use to inspect the `Illuminate\Http\Client\Request` instance. Likewise, the `ResponseReceived` event contains a `$request` property as well as a `$response` property which may be used to inspect the `Illuminate\Http\Client\Response` instance. You may create [event listeners](/docs/11.x/events) for these events within your application: -->
`RequestSending` 및 `ConnectionFailed` 이벤트는 모두 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있는 공용 `$request` 속성을 포함하고 있습니다. 마찬가지로, `ResponseReceived` 이벤트는 `$request` 속성과 함께 `Illuminate\Http\Client\Response` 인스턴스를 검사할 수 있는 `$response` 속성을 포함합니다. 여러분의 애플리케이션 내에서 이 이벤트들에 [event listeners](/docs/11.x/events)를 등록하여 활용할 수 있습니다.

```
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * Handle the given event.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
