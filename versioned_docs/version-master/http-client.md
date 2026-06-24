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
    - [Request Pooling](#request-pooling)
    - [Request Batching](#request-batching)
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
Laravel은 [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/)를 감싸는 표현력 있고 간결한 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위한 외부 HTTP 요청을 빠르게 보낼 수 있습니다. Laravel의 Guzzle 래퍼는 가장 자주 사용되는 사례와 뛰어난 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make requests, you may use the `head`, `get`, `post`, `put`, `patch`, and `delete` methods provided by the `Http` facade. First, let's examine how to make a basic `GET` request to another URL: -->
요청을 보내려면 `Http` facade가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

<!-- The `get` method returns an instance of `Illuminate\Http\Client\Response`, which provides a variety of methods that may be used to inspect the response: -->
`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환합니다. 이 인스턴스는 응답을 검사하는 데 사용할 수 있는 다양한 메서드를 제공합니다.

```php
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
`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하므로, 응답에서 JSON 응답 데이터에 직접 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

<!-- In addition to the response methods listed above, the following methods may be used to determine if the response has a specific status code: -->
위에 나열된 응답 메서드 외에도, 응답이 특정 상태 코드를 가지고 있는지 확인하기 위해 다음 메서드를 사용할 수 있습니다.

```php
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
HTTP 클라이언트는 [URI template specification](https://www.rfc-editor.org/rfc/rfc6570)를 사용하여 요청 URL을 구성할 수도 있습니다. URI 템플릿에서 확장될 수 있는 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
<!-- #### Dumping Requests -->
#### Dumping Requests

<!-- If you would like to dump the outgoing request instance before it is sent and terminate the script's execution, you may add the `dd` method to the beginning of your request definition: -->
전송되기 전에 외부로 나가는 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가할 수 있습니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
<!-- ### Request Data -->
### Request Data

<!-- Of course, it is common when making `POST`, `PUT`, and `PATCH` requests to send additional data with your request, so these methods accept an array of data as their second argument. By default, data will be sent using the `application/json` content type: -->
물론 `POST`, `PUT`, `PATCH` 요청을 보낼 때 요청과 함께 추가 데이터를 보내는 일은 흔합니다. 따라서 이 메서드들은 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

```php
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
`GET` 요청을 보낼 때는 URL에 쿼리 문자열을 직접 붙이거나, `get` 메서드의 두 번째 인수로 키 / 값 쌍의 배열을 전달할 수 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

<!-- Alternatively, the `withQueryParameters` method may be used: -->
또는 `withQueryParameters` 메서드를 사용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
<!-- #### Sending Form URL Encoded Requests -->
#### Sending Form URL Encoded Requests

<!-- If you would like to send data using the `application/x-www-form-urlencoded` content type, you should call the `asForm` method before making your request: -->
`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶다면, 요청을 보내기 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
<!-- #### Sending a Raw Request Body -->
#### Sending a Raw Request Body

<!-- You may use the `withBody` method if you would like to provide a raw request body when making a request. The content type may be provided via the method's second argument: -->
요청을 보낼 때 원시 요청 본문을 제공하고 싶다면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 이 메서드의 두 번째 인수로 제공할 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
<!-- #### Multi-Part Requests -->
#### Multi-Part Requests

<!-- If you would like to send files as multi-part requests, you should call the `attach` method before making your request. This method accepts the name of the file and its contents. If needed, you may provide a third argument which will be considered the file's filename, while a fourth argument may be used to provide headers associated with the file: -->
파일을 멀티파트 요청으로 보내고 싶다면, 요청을 보내기 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일의 이름과 내용을 받습니다. 필요하다면 세 번째 인수로 파일명을 제공할 수 있으며, 네 번째 인수는 파일과 관련된 헤더를 제공하는 데 사용할 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

<!-- Instead of passing the raw contents of a file, you may pass a stream resource: -->
파일의 원시 내용을 전달하는 대신 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
<!-- ### Headers -->
### Headers

<!-- Headers may be added to requests using the `withHeaders` method. This `withHeaders` method accepts an array of key / value pairs: -->
`withHeaders` 메서드를 사용하여 요청에 헤더를 추가할 수 있습니다. 이 `withHeaders` 메서드는 키 / 값 쌍의 배열을 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<!-- You may use the `accept` method to specify the content type that your application is expecting in response to your request: -->
`accept` 메서드를 사용하여 애플리케이션이 요청에 대한 응답으로 기대하는 콘텐츠 타입을 지정할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

<!-- For convenience, you may use the `acceptJson` method to quickly specify that your application expects the `application/json` content type in response to your request: -->
편의를 위해 `acceptJson` 메서드를 사용하면, 애플리케이션이 요청에 대한 응답으로 `application/json` 콘텐츠 타입을 기대한다고 빠르게 지정할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

<!-- The `withHeaders` method merges new headers into the request's existing headers. If needed, you may replace all of the headers entirely using the `replaceHeaders` method: -->
`withHeaders` 메서드는 새 헤더를 요청의 기존 헤더에 병합합니다. 필요하다면 `replaceHeaders` 메서드를 사용하여 모든 헤더를 완전히 교체할 수 있습니다.

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
`withBasicAuth` 및 `withDigestAuth` 메서드를 사용하여 각각 기본 인증과 다이제스트 인증 자격 증명을 지정할 수 있습니다.

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
<!-- #### Bearer Tokens -->
#### Bearer Tokens

<!-- If you would like to quickly add a bearer token to the request's `Authorization` header, you may use the `withToken` method: -->
요청의 `Authorization` 헤더에 Bearer 토큰을 빠르게 추가하고 싶다면 `withToken` 메서드를 사용할 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
<!-- ### Timeout -->
### Timeout

<!-- The `timeout` method may be used to specify the maximum number of seconds to wait for a response. By default, the HTTP client will timeout after 30 seconds: -->
`timeout` 메서드는 응답을 기다릴 최대 초 수를 지정하는 데 사용할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

<!-- If the given timeout is exceeded, an instance of `Illuminate\Http\Client\ConnectionException` will  be thrown. -->
지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

<!-- You may specify the maximum number of seconds to wait while trying to connect to a server using the `connectTimeout` method. The default is 10 seconds: -->
서버에 연결을 시도하는 동안 기다릴 최대 초 수는 `connectTimeout` 메서드를 사용하여 지정할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
<!-- ### Retries -->
### Retries

<!-- If you would like the HTTP client to automatically retry the request if a client or server error occurs, you may use the `retry` method. The `retry` method accepts the maximum number of times the request should be attempted and the number of milliseconds that Laravel should wait in between attempts: -->
클라이언트 또는 서버 오류가 발생했을 때 HTTP 클라이언트가 요청을 자동으로 재시도하도록 하려면 `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 요청을 시도할 최대 횟수와 Laravel이 각 시도 사이에 기다릴 밀리초 수를 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

<!-- If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the second argument to the `retry` method: -->
각 시도 사이에 대기할 밀리초 수를 직접 계산하고 싶다면, `retry` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

<!-- For convenience, you may also provide an array as the first argument to the `retry` method. This array will be used to determine how many milliseconds to sleep between subsequent attempts: -->
편의를 위해 `retry` 메서드의 첫 번째 인수로 배열을 제공할 수도 있습니다. 이 배열은 이어지는 시도 사이에 몇 밀리초 동안 대기할지 결정하는 데 사용됩니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

<!-- If needed, you may pass a third argument to the `retry` method. The third argument should be a callable that determines if the retries should actually be attempted. For example, you may wish to only retry the request if the initial request encounters an `ConnectionException`: -->
필요하다면 `retry` 메서드에 세 번째 인수를 전달할 수 있습니다. 세 번째 인수는 실제로 재시도를 시도할지 결정하는 callable이어야 합니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생한 경우에만 요청을 재시도하고 싶을 수 있습니다.

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

<!-- If a request attempt fails, you may wish to make a change to the request before a new attempt is made. You can achieve this by modifying the request argument provided to the callable you provided to the `retry` method. For example, you might want to retry the request with a new authorization token if the first attempt returned an authentication error: -->
요청 시도가 실패하면, 새 시도를 하기 전에 요청을 변경하고 싶을 수 있습니다. 이를 위해 `retry` 메서드에 제공한 callable에 전달되는 요청 인수를 수정할 수 있습니다. 예를 들어, 첫 번째 시도에서 인증 오류가 반환된 경우 새 인증 토큰으로 요청을 재시도하고 싶을 수 있습니다.

```php
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\RequestException;
use Throwable;

$response = Http::withToken($this->getToken())->retry(2, 0, function (Throwable $exception, PendingRequest $request) {
    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
        return false;
    }

    $request->withToken($this->getNewToken());

    return true;
})->post(/* ... */);
```

<!-- If all of the requests fail, an instance of `Illuminate\Http\Client\RequestException` will be thrown. If you would like to disable this behavior, you may provide a `throw` argument with a value of `false`. When disabled, the last response received by the client will be returned after all retries have been attempted: -->
모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하고 싶다면 `throw` 인수에 `false` 값을 제공할 수 있습니다. 비활성화하면 모든 재시도가 시도된 후 클라이언트가 마지막으로 받은 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 인해 실패한 경우에는 `throw` 인수가 `false`로 설정되어 있어도 `Illuminate\Http\Client\ConnectionException`이 계속 발생합니다.

<a name="error-handling"></a>
<!-- ### Error Handling -->
### Error Handling

<!-- Unlike Guzzle's default behavior, Laravel's HTTP client wrapper does not throw exceptions on client or server errors (`400` and `500` level responses from servers). You may determine if one of these errors was returned using the `successful`, `clientError`, or `serverError` methods: -->
Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버의 `400` 및 `500` 수준 응답)에서 예외를 발생시키지 않습니다. 이러한 오류 중 하나가 반환되었는지는 `successful`, `clientError`, `serverError` 메서드를 사용하여 확인할 수 있습니다.

```php
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
응답 인스턴스가 있고, 응답 상태 코드가 클라이언트 또는 서버 오류를 나타내는 경우 `Illuminate\Http\Client\RequestException` 인스턴스를 발생시키고 싶다면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```php
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
`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있도록 public `$response` 속성이 있습니다.

<!-- The `throw` method returns the response instance if no error occurred, allowing you to chain other operations onto the `throw` method: -->
오류가 발생하지 않았다면 `throw` 메서드는 응답 인스턴스를 반환하므로, `throw` 메서드 뒤에 다른 작업을 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

<!-- If you would like to perform some additional logic before the exception is thrown, you may pass a closure to the `throw` method. The exception will be thrown automatically after the closure is invoked, so you do not need to re-throw the exception from within the closure: -->
예외가 발생하기 전에 추가 로직을 수행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저가 호출된 후 예외는 자동으로 발생하므로, 클로저 안에서 예외를 다시 던질 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

<!-- By default, `RequestException` messages are truncated to 120 characters when logged or reported. To customize or disable this behavior, you may utilize the `truncateAt` and `dontTruncate` methods when configuring your application's registered behavior in your `bootstrap/app.php` file: -->
기본적으로 `RequestException` 메시지는 로그에 기록되거나 보고될 때 120자로 잘립니다. 이 동작을 사용자 지정하거나 비활성화하려면, `bootstrap/app.php` 파일에서 애플리케이션에 등록된 동작을 설정할 때 `truncateAt` 및 `dontTruncate` 메서드를 사용할 수 있습니다:
```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // Truncate request exception messages to 240 characters...
    RequestException::truncateAt(240);

    // Disable request exception message truncation...
    RequestException::dontTruncate();
})
```

<!-- Alternatively, you may customize the exception truncation behavior per request using the `truncateExceptionsAt` method: -->
또는 `truncateExceptionsAt` 메서드를 사용하여 요청별로 예외 메시지 자르기 동작을 사용자 정의할 수 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
<!-- ### Guzzle Middleware -->
### Guzzle Middleware

<!-- Since Laravel's HTTP client is powered by Guzzle, you may take advantage of [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) to manipulate the outgoing request or inspect the incoming response. To manipulate the outgoing request, register a Guzzle middleware via the `withRequestMiddleware` method: -->
Laravel의 HTTP 클라이언트는 Guzzle을 기반으로 하므로, [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용하여 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면 `withRequestMiddleware` 메서드로 Guzzle Middleware를 등록합니다.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

<!-- Likewise, you can inspect the incoming HTTP response by registering a middleware via the `withResponseMiddleware` method: -->
마찬가지로, `withResponseMiddleware` 메서드로 Middleware를 등록하여 들어오는 HTTP 응답을 검사할 수 있습니다.

```php
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
때로는 모든 나가는 요청과 들어오는 응답에 적용되는 Middleware를 등록하고 싶을 수 있습니다. 이를 위해 `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드들은 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드에서 호출해야 합니다.

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
`withOptions` 메서드를 사용하여 나가는 요청에 추가 [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. `withOptions` 메서드는 키 / 값 쌍의 배열을 인수로 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
<!-- #### Global Options -->
#### Global Options

<!-- To configure default options for every outgoing request, you may utilize the `globalOptions` method. Typically, this method should be invoked from the `boot` method of your application's `AppServiceProvider`: -->
모든 나가는 요청에 대한 기본 옵션을 설정하려면 `globalOptions` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드에서 호출해야 합니다.

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
때로는 여러 HTTP 요청을 동시에 보내고 싶을 수 있습니다. 즉, 요청을 순차적으로 실행하는 대신 여러 요청을 같은 시점에 디스패치하려는 것입니다. 느린 HTTP API와 통신할 때 이는 상당한 성능 향상으로 이어질 수 있습니다.

<a name="request-pooling"></a>
<!-- ### Request Pooling -->
### Request Pooling

<!-- Thankfully, you may accomplish this using the `pool` method. The `pool` method accepts a closure which receives an `Illuminate\Http\Client\Pool` instance, allowing you to easily add requests to the request pool for dispatching: -->
다행히 `pool` 메서드를 사용하면 이를 쉽게 처리할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인수로 받으며, 이 인스턴스를 통해 디스패치할 요청을 요청 풀에 손쉽게 추가할 수 있습니다.

```php
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
보시다시피, 각 응답 인스턴스는 풀에 추가된 순서에 따라 접근할 수 있습니다. 원한다면 `as` 메서드를 사용하여 요청에 이름을 붙일 수 있으며, 이렇게 하면 해당 응답을 이름으로 접근할 수 있습니다.

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```

<!-- The maximum concurrency of the request pool may be controlled by providing the `concurrency` argument to the `pool` method. This value determines the maximum number of HTTP requests that may be concurrently in-flight while processing the request pool: -->
요청 풀의 최대 동시성은 `pool` 메서드에 `concurrency` 인수를 전달하여 제어할 수 있습니다. 이 값은 요청 풀을 처리하는 동안 동시에 진행 중일 수 있는 HTTP 요청의 최대 개수를 결정합니다.

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
<!-- #### Customizing Concurrent Requests -->
#### Customizing Concurrent Requests

<!-- The `pool` method cannot be chained with other HTTP client methods such as the `withHeaders` or `middleware` methods. If you want to apply custom headers or middleware to pooled requests, you should configure those options on each request in the pool: -->
`pool` 메서드는 `withHeaders` 또는 `middleware` 메서드와 같은 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀링된 요청에 사용자 정의 헤더나 Middleware를 적용하려면 풀 안의 각 요청에 해당 옵션을 설정해야 합니다.

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

<a name="request-batching"></a>
<!-- ### Request Batching -->
### Request Batching

<!-- Another way of working with concurrent requests in Laravel is to use the `batch` method. Like the `pool` method, it accepts a closure which receives an `Illuminate\Http\Client\Batch` instance, allowing you to easily add requests to the request pool for dispatching, but it also allows you to define completion callbacks: -->
Laravel에서 동시 요청을 처리하는 또 다른 방법은 `batch` 메서드를 사용하는 것입니다. `pool` 메서드와 마찬가지로 `Illuminate\Http\Client\Batch` 인스턴스를 받는 클로저를 인수로 받으며, 디스패치할 요청을 요청 풀에 손쉽게 추가할 수 있습니다. 여기에 더해 완료 콜백도 정의할 수 있습니다.

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->before(function (Batch $batch) {
    // The batch has been created but no requests have been initialized...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // An individual request has completed successfully...
})->then(function (Batch $batch, array $results) {
    // All requests completed successfully...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // Batch request failure detected...
})->finally(function (Batch $batch, array $results) {
    // The batch has finished executing...
})->send();
```

<!-- Like the `pool` method, you can use the `as` method to name your requests: -->
`pool` 메서드와 마찬가지로 `as` 메서드를 사용하여 요청에 이름을 붙일 수 있습니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

<!-- After a `batch` is started by calling the `send` method, you can't add new requests to it. Trying to do so will result in a `Illuminate\Http\Client\BatchInProgressException` exception being thrown. -->
`send` 메서드를 호출하여 `batch`가 시작된 뒤에는 새 요청을 추가할 수 없습니다. 이를 시도하면 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

<!-- The maximum concurrency of the request batch may be controlled via the `concurrency` method. This value determines the maximum number of HTTP requests that may be concurrently in-flight while processing the request batch: -->
요청 배치의 최대 동시성은 `concurrency` 메서드로 제어할 수 있습니다. 이 값은 요청 배치를 처리하는 동안 동시에 진행 중일 수 있는 HTTP 요청의 최대 개수를 결정합니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
<!-- #### Inspecting Batches -->
#### Inspecting Batches

<!-- The `Illuminate\Http\Client\Batch` instance that is provided to batch completion callbacks has a variety of properties and methods to assist you in interacting with and inspecting a given batch of requests: -->
배치 완료 콜백에 전달되는 `Illuminate\Http\Client\Batch` 인스턴스에는 주어진 요청 배치와 상호작용하고 이를 검사하는 데 도움이 되는 다양한 속성과 메서드가 있습니다.

```php
// The number of requests assigned to the batch...
$batch->totalRequests;

// The number of requests that have not been processed yet...
$batch->pendingRequests;

// The number of requests that have failed...
$batch->failedRequests;

// The number of requests that have been processed thus far...
$batch->processedRequests();

// Indicates if the batch has finished executing...
$batch->finished();

// Indicates if the batch has request failures...
$batch->hasFailures();
```
<a name="deferring-batches"></a>
<!-- #### Deferring Batches -->
#### Deferring Batches

<!-- When the `defer` method is invoked, the batch of requests is not executed immediately. Instead, Laravel will execute the batch after the current application request's HTTP response has been sent to the user, keeping your application feeling fast and responsive: -->
`defer` 메서드가 호출되면 요청 배치는 즉시 실행되지 않습니다. 대신 Laravel은 현재 애플리케이션 요청의 HTTP 응답이 사용자에게 전송된 뒤에 배치를 실행하여, 애플리케이션이 빠르고 반응성 있게 느껴지도록 유지합니다.

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // All requests completed successfully...
})->defer();
```

<a name="macros"></a>
<!-- ## Macros -->
## Macros

<!-- The Laravel HTTP client allows you to define "macros", which can serve as a fluent, expressive mechanism to configure common request paths and headers when interacting with services throughout your application. To get started, you may define the macro within the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있게 해줍니다. 매크로는 애플리케이션 전반에서 여러 서비스와 통신할 때 자주 사용하는 요청 경로와 헤더를 유창하고 표현력 있는 방식으로 설정하는 메커니즘으로 사용할 수 있습니다. 시작하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드 안에서 매크로를 정의하면 됩니다.

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
매크로 설정이 완료되면 애플리케이션 어디에서나 이를 호출하여 지정된 설정을 가진 보류 중인 요청을 생성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's HTTP client is no exception. The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made. -->
많은 Laravel 서비스는 테스트를 쉽고 표현력 있게 작성할 수 있도록 돕는 기능을 제공하며, Laravel의 HTTP 클라이언트도 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 요청이 이루어질 때 HTTP 클라이언트가 스텁 / 더미 응답을 반환하도록 지시할 수 있습니다.

<a name="faking-responses"></a>
<!-- ### Faking Responses -->
### Faking Responses

<!-- For example, to instruct the HTTP client to return empty, `200` status code responses for every request, you may call the `fake` method with no arguments: -->
예를 들어 모든 요청에 대해 빈 `200` 상태 코드 응답을 반환하도록 HTTP 클라이언트에 지시하려면, 인수 없이 `fake` 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
<!-- #### Faking Specific URLs -->
#### Faking Specific URLs

<!-- Alternatively, you may pass an array to the `fake` method. The array's keys should represent URL patterns that you wish to fake and their associated responses. The `*` character may be used as a wildcard character. You may use the `Http` facade's `response` method to construct stub / fake responses for these endpoints: -->
또는 `fake` 메서드에 배열을 전달할 수 있습니다. 배열의 키는 페이크하려는 URL 패턴을 나타내고, 값은 그에 연결된 응답을 나타내야 합니다. `*` 문자는 와일드카드 문자로 사용할 수 있습니다. 이러한 엔드포인트에 대한 스텁 / 페이크 응답을 구성하려면 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

<!-- Any requests made to URLs that have not been faked will actually be executed. If you would like to specify a fallback URL pattern that will stub all unmatched URLs, you may use a single `*` character: -->
페이크되지 않은 URL로 이루어지는 모든 요청은 실제로 실행됩니다. 매칭되지 않는 모든 URL을 스텁 처리할 fallback URL 패턴을 지정하고 싶다면 단일 `*` 문자를 사용할 수 있습니다.

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

<!-- For convenience, simple string, JSON, and empty responses may be generated by providing a string, array, or integer as the response: -->
편의를 위해 문자열, 배열, 정수를 응답으로 제공하여 간단한 문자열, JSON, 빈 응답을 생성할 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
<!-- #### Faking Exceptions -->
#### Faking Exceptions

<!-- Sometimes you may need to test your application's behavior if the HTTP client encounters an `Illuminate\Http\Client\ConnectionException` when attempting to make a request. You can instruct the HTTP client to throw a connection exception using the `failedConnection` method: -->
때로는 HTTP 클라이언트가 요청을 시도하는 중 `Illuminate\Http\Client\ConnectionException`을 만났을 때 애플리케이션이 어떻게 동작하는지 테스트해야 할 수 있습니다. `failedConnection` 메서드를 사용하면 HTTP 클라이언트가 연결 예외를 발생시키도록 지시할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

<!-- To test your application's behavior if a `Illuminate\Http\Client\RequestException` is thrown, you may use the `failedRequest` method: -->
`Illuminate\Http\Client\RequestException`이 발생했을 때 애플리케이션의 동작을 테스트하려면 `failedRequest` 메서드를 사용할 수 있습니다.

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
<!-- #### Faking Response Sequences -->
#### Faking Response Sequences

<!-- Sometimes you may need to specify that a single URL should return a series of fake responses in a specific order. You may accomplish this using the `Http::sequence` method to build the responses: -->
때로는 하나의 URL이 특정 순서로 일련의 페이크 응답을 반환하도록 지정해야 할 수 있습니다. `Http::sequence` 메서드를 사용하여 응답을 구성하면 이를 처리할 수 있습니다.

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

<!-- When all the responses in a response sequence have been consumed, any further requests will cause the response sequence to throw an exception. If you would like to specify a default response that should be returned when a sequence is empty, you may use the `whenEmpty` method: -->
응답 시퀀스의 모든 응답이 소비되면 이후 요청은 응답 시퀀스가 예외를 발생시키게 됩니다. 시퀀스가 비어 있을 때 반환할 기본 응답을 지정하고 싶다면 `whenEmpty` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

<!-- If you would like to fake a sequence of responses but do not need to specify a specific URL pattern that should be faked, you may use the `Http::fakeSequence` method: -->
응답 시퀀스를 페이크하고 싶지만 페이크할 특정 URL 패턴을 지정할 필요가 없다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
<!-- #### Fake Callback -->
#### Fake Callback

<!-- If you require more complicated logic to determine what responses to return for certain endpoints, you may pass a closure to the `fake` method. This closure will receive an instance of `Illuminate\Http\Client\Request` and should return a response instance. Within your closure, you may perform whatever logic is necessary to determine what type of response to return: -->
특정 엔드포인트에 대해 어떤 응답을 반환할지 결정하는 더 복잡한 로직이 필요하다면 `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받으며 응답 인스턴스를 반환해야 합니다. 클로저 안에서는 어떤 유형의 응답을 반환할지 결정하는 데 필요한 모든 로직을 수행할 수 있습니다.
```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
<!-- ### Inspecting Requests -->
### Inspecting Requests

<!-- When faking responses, you may occasionally wish to inspect the requests the client receives in order to make sure your application is sending the correct data or headers. You may accomplish this by calling the `Http::assertSent` method after calling `Http::fake`. -->
응답을 fake 처리할 때, 애플리케이션이 올바른 데이터나 헤더를 전송하는지 확인하기 위해 클라이언트가 받은 요청을 검사하고 싶을 때가 있습니다. 이는 `Http::fake`를 호출한 뒤 `Http::assertSent` 메서드를 호출하여 수행할 수 있습니다.

<!-- The `assertSent` method accepts a closure which will receive an `Illuminate\Http\Client\Request` instance and should return a boolean value indicating if the request matches your expectations. In order for the test to pass, at least one request must have been issued matching the given expectations: -->
`assertSent` 메서드는 `Illuminate\Http\Client\Request` 인스턴스를 전달받는 클로저를 인수로 받으며, 해당 요청이 기대한 조건과 일치하는지를 나타내는 boolean 값을 반환해야 합니다. 테스트가 통과하려면, 주어진 기대 조건과 일치하는 요청이 하나 이상 발생해야 합니다.

```php
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
필요하다면 `assertNotSent` 메서드를 사용하여 특정 요청이 전송되지 않았는지 검증할 수 있습니다.

```php
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
`assertSentCount` 메서드를 사용하여 테스트 중에 몇 개의 요청이 "전송"되었는지 검증할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

<!-- Or, you may use the `assertNothingSent` method to assert that no requests were sent during the test: -->
또는 `assertNothingSent` 메서드를 사용하여 테스트 중에 아무 요청도 전송되지 않았는지 검증할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
<!-- #### Recording Requests / Responses -->
#### Recording Requests / Responses

<!-- You may use the `recorded` method to gather all requests and their corresponding responses. The `recorded` method returns a collection of arrays that contains instances of `Illuminate\Http\Client\Request` and `Illuminate\Http\Client\Response`: -->
`recorded` 메서드를 사용하여 모든 요청과 그에 대응하는 응답을 수집할 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 포함하는 배열 컬렉션을 반환합니다.

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
또한 `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 전달받는 클로저를 인수로 받을 수 있으며, 이를 사용해 기대 조건에 따라 요청 / 응답 쌍을 필터링할 수 있습니다.

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

<a name="preventing-stray-requests"></a>
<!-- ### Preventing Stray Requests -->
### Preventing Stray Requests

<!-- If you would like to ensure that all requests sent via the HTTP client have been faked throughout your individual test or complete test suite, you can call the `preventStrayRequests` method. After calling this method, any requests that do not have a corresponding fake response will throw an exception rather than making the actual HTTP request: -->
개별 테스트 또는 전체 테스트 스위트에서 HTTP 클라이언트를 통해 전송되는 모든 요청이 fake 처리되었는지 보장하고 싶다면 `preventStrayRequests` 메서드를 호출할 수 있습니다. 이 메서드를 호출한 뒤에는, 대응되는 fake 응답이 없는 모든 요청이 실제 HTTP 요청을 보내는 대신 예외를 발생시킵니다.

```php
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

<!-- Sometimes, you may wish to prevent most stray requests while still allowing specific requests to execute. To accomplish this, you may pass an array of URL patterns to the `allowStrayRequests` method. Any request matching one of the given patterns will be allowed, while all other requests will continue to throw an exception: -->
때로는 대부분의 예상 밖 요청은 방지하면서도 특정 요청은 실행되도록 허용하고 싶을 수 있습니다. 이를 위해 `allowStrayRequests` 메서드에 URL 패턴 배열을 전달할 수 있습니다. 주어진 패턴 중 하나와 일치하는 요청은 허용되며, 그 밖의 모든 요청은 계속해서 예외를 발생시킵니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// This request is executed...
Http::get('http://127.0.0.1:5000/generate');

// An exception is thrown...
Http::get('https://laravel.com');
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel fires three events during the process of sending HTTP requests. The `RequestSending` event is fired prior to a request being sent, while the `ResponseReceived` event is fired after a response is received for a given request. The `ConnectionFailed` event is fired if no response is received for a given request. -->
Laravel은 HTTP 요청을 전송하는 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에 발생하고, `ResponseReceived` 이벤트는 특정 요청에 대한 응답을 받은 뒤에 발생합니다. `ConnectionFailed` 이벤트는 특정 요청에 대한 응답을 받지 못한 경우 발생합니다.

<!-- The `RequestSending` and `ConnectionFailed` events both contain a public `$request` property that you may use to inspect the `Illuminate\Http\Client\Request` instance. Likewise, the `ResponseReceived` event contains a `$request` property as well as a `$response` property which may be used to inspect the `Illuminate\Http\Client\Response` instance. You may create [event listeners](/docs/master/events) for these events within your application: -->
`RequestSending` 이벤트와 `ConnectionFailed` 이벤트는 모두 공개 `$request` 속성을 포함하며, 이를 사용해 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있습니다. 마찬가지로 `ResponseReceived` 이벤트는 `$request` 속성과 함께 `$response` 속성을 포함하며, 이를 사용해 `Illuminate\Http\Client\Response` 인스턴스를 검사할 수 있습니다. 애플리케이션 안에서 이러한 이벤트에 대한 [event listeners](/docs/master/events)를 만들 수 있습니다.

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * Handle the event.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
