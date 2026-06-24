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
Laravel은 [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/)를 감싸서, 간단하고 직관적인 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 신속하게 HTTP 요청을 주고받을 수 있습니다. Laravel의 Guzzle 래퍼는 가장 자주 사용되는 사례에 초점을 맞췄으며, 개발자 경험을 극대화했습니다.

<!-- Before getting started, you should ensure that you have installed the Guzzle package as a dependency of your application. By default, Laravel automatically includes this dependency. However, if you have previously removed the package, you may install it again via Composer: -->
시작하기 전에, 애플리케이션의 의존성으로 Guzzle 패키지를 설치했는지 확인해야 합니다. 기본적으로 Laravel에서는 이 의존성을 자동으로 포함합니다. 만약 Guzzle 패키지를 삭제했다면, 아래 Composer 명령어로 다시 설치할 수 있습니다:

```shell
composer require guzzlehttp/guzzle
```

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make requests, you may use the `head`, `get`, `post`, `put`, `patch`, and `delete` methods provided by the `Http` facade. First, let's examine how to make a basic `GET` request to another URL: -->
`Http` 파사드가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 통해 HTTP 요청을 보낼 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다:

```
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

<!-- The `get` method returns an instance of `Illuminate\Http\Client\Response`, which provides a variety of methods that may be used to inspect the response: -->
`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환합니다. 이 객체는 다양한 메서드를 제공하여 응답을 쉽게 확인할 수 있도록 돕습니다:

```
$response->body() : string;
$response->json($key = null, $default = null) : array|mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->status() : int;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

<!-- The `Illuminate\Http\Client\Response` object also implements the PHP `ArrayAccess` interface, allowing you to access JSON response data directly on the response: -->
`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있어서, 응답으로 반환된 JSON 데이터를 배열처럼 바로 접근할 수 있습니다:

```
return Http::get('http://example.com/users/1')['name'];
```

<!-- In addition to the response methods listed above, the following methods may be used to determine if the response has a given status code: -->
위의 다양한 응답 메서드 외에도, 특정 상태 코드를 반환했는지 확인할 수 있는 메서드들도 사용할 수 있습니다:

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
HTTP 클라이언트는 [URI template specification](https://www.rfc-editor.org/rfc/rfc6570)를 활용하여 요청 URL을 동적으로 구성할 수 있도록 지원합니다. URI 템플릿에서 변수로 사용될 URL 파라미터는 `withUrlParameters` 메서드를 이용해 정의합니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '9.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
<!-- #### Dumping Requests -->
#### Dumping Requests

<!-- If you would like to dump the outgoing request instance before it is sent and terminate the script's execution, you may add the `dd` method to the beginning of your request definition: -->
요청이 실제로 전송되기 전에 해당 요청 인스턴스를 덤프하고(즉시 출력) 스크립트 실행을 중단하고 싶을 때는 `dd` 메서드를 요청 정의의 시작 부분에 추가하면 됩니다:

```
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
<!-- ### Request Data -->
### Request Data

<!-- Of course, it is common when making `POST`, `PUT`, and `PATCH` requests to send additional data with your request, so these methods accept an array of data as their second argument. By default, data will be sent using the `application/json` content type: -->
`POST`, `PUT`, `PATCH` 요청을 보내면서 추가적인 데이터 전송이 필요한 경우가 많습니다. 이러한 메서드들은 두 번째 인수로 데이터 배열을 받을 수 있습니다. 기본적으로 데이터는 `application/json` content-type으로 전송됩니다:

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
`GET` 요청을 보낼 때는, 쿼리 스트링을 URL에 직접 추가하거나, `get` 메서드의 두 번째 인수로 key / value 쌍 배열을 전달할 수 있습니다:

```
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

<!-- Alternatively, the `withQueryParameters` method may be used: -->
또는, `withQueryParameters` 메서드를 사용할 수도 있습니다:

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
`application/x-www-form-urlencoded` content-type으로 데이터를 전송하려면, 요청 전송 전에 `asForm` 메서드를 호출해야 합니다:

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
요청 시, 원시(raw) 데이터 본문을 직접 지정하고 싶을 때는 `withBody` 메서드를 사용할 수 있습니다. 두 번째 인수로 content-type을 지정할 수 있습니다:

```
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
<!-- #### Multi-Part Requests -->
#### Multi-Part Requests

<!-- If you would like to send files as multi-part requests, you should call the `attach` method before making your request. This method accepts the name of the file and its contents. If needed, you may provide a third argument which will be considered the file's filename, while a fourth argument may be used to provide headers associated with the file: -->
파일을 멀티파트로 전송하려면, 요청 전에 `attach` 메서드를 사용해야 합니다. 이 메서드는 파일 이름과 파일 내용을 인수로 받으며, 필요하다면 세 번째 인수로 파일 이름, 네 번째 인수로 파일과 관련된 헤더를 추가할 수 있습니다:

```
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

<!-- Instead of passing the raw contents of a file, you may pass a stream resource: -->
파일의 원시 데이터를 전달하는 대신, 스트림 리소스를 사용할 수도 있습니다:

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
요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용합니다. 이 `withHeaders` 메서드는 key / value 쌍 배열을 인수로 받습니다:

```
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<!-- You may use the `accept` method to specify the content type that your application is expecting in response to your request: -->
요청에 대해 응답으로 기대하는 content-type을 지정하고 싶다면 `accept` 메서드를 사용할 수 있습니다:

```
$response = Http::accept('application/json')->get('http://example.com/users');
```

<!-- For convenience, you may use the `acceptJson` method to quickly specify that your application expects the `application/json` content type in response to your request: -->
자주 사용하는 경우, `acceptJson` 메서드를 사용해 `application/json` content-type을 간편하게 지정할 수 있습니다:

```
$response = Http::acceptJson()->get('http://example.com/users');
```

<!-- The `withHeaders` method merges new headers into the request's existing headers. If needed, you may replace all of the headers entirely using the `replaceHeaders` method: -->
`withHeaders` 메서드는 새로운 헤더를 기존 요청 헤더에 병합합니다. 만약 모든 헤더를 완전히 교체하고 싶다면 `replaceHeaders` 메서드를 사용할 수 있습니다:

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
베이직 인증과 다이제스트 인증(Basic, Digest)은 각각 `withBasicAuth`, `withDigestAuth` 메서드로 지정할 수 있습니다:

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
요청의 `Authorization` 헤더에 Bearer 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용합니다:

```
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
<!-- ### Timeout -->
### Timeout

<!-- The `timeout` method may be used to specify the maximum number of seconds to wait for a response. By default, the HTTP client will timeout after 30 seconds: -->
응답을 기다리는 최대 초(second) 수를 지정하려면 `timeout` 메서드를 사용하면 됩니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃됩니다:

```
$response = Http::timeout(3)->get(/* ... */);
```

<!-- If the given timeout is exceeded, an instance of `Illuminate\Http\Client\ConnectionException` will  be thrown. -->
지정한 타임아웃을 초과하는 경우 `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

<!-- You may specify the maximum number of seconds to wait while trying to connect to a server using the `connectTimeout` method: -->
서버 연결 시도에 대해 별도의 최대 대기 초를 지정하고 싶다면, `connectTimeout` 메서드를 사용할 수 있습니다:

```
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
<!-- ### Retries -->
### Retries

<!-- If you would like the HTTP client to automatically retry the request if a client or server error occurs, you may use the `retry` method. The `retry` method accepts the maximum number of times the request should be attempted and the number of milliseconds that Laravel should wait in between attempts: -->
클라이언트 오류 또는 서버 오류가 발생하면 HTTP 클라이언트가 자동으로 요청을 재시도하도록 `retry` 메서드를 사용할 수 있습니다. 이 `retry` 메서드는 요청을 최대 몇 번 재시도할지와, 각 시도 사이 대기 시간을 밀리초(ms) 단위로 받습니다:

```
$response = Http::retry(3, 100)->post(/* ... */);
```

<!-- If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the second argument to the `retry` method: -->
재시도 사이 대기 밀리초를 직접 계산하고 싶다면, `retry` 메서드의 두 번째 인수로 클로저를 전달하면 됩니다:

```
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

<!-- For convenience, you may also provide an array as the first argument to the `retry` method. This array will be used to determine how many milliseconds to sleep between subsequent attempts: -->
편리하게, `retry` 메서드의 첫 번째 인수에 배열을 전달할 수도 있습니다. 이 배열은 각 시도 사이에 대기할 밀리초를 결정하는데 사용됩니다:

```
$response = Http::retry([100, 200])->post(/* ... */);
```

<!-- If needed, you may pass a third argument to the `retry` method. The third argument should be a callable that determines if the retries should actually be attempted. For example, you may wish to only retry the request if the initial request encounters an `ConnectionException`: -->
필요하다면, `retry` 메서드의 세 번째 인수로 실제로 재시도를 해야 하는지 판단하는 콜러블을 전달할 수 있습니다. 예를 들어, 처음 요청에서 `ConnectionException`만 발생할 때만 재시도하고 싶을 때 사용할 수 있습니다:

```
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

<!-- If a request attempt fails, you may wish to make a change to the request before a new attempt is made. You can achieve this by modifying the request argument provided to the callable you provided to the `retry` method. For example, you might want to retry the request with a new authorization token if the first attempt returned an authentication error: -->
요청이 실패할 경우, 다음 시도 전에 요청 객체를 변경하고 싶을 때도 있습니다. `retry` 메서드에 전달한 콜러블에 제공되는 요청 인수를 수정하면 됩니다. 예를 들어, 첫 번째 요청이 인증 오류(401)였다면 새로운 토큰을 받아서 재시도할 수도 있습니다:

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
모든 요청이 실패할 경우, `Illuminate\Http\Client\RequestException` 예외가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수를 `false`로 지정하세요. 이 경우 모든 재시도 후 마지막 응답 객체가 반환됩니다:

```
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 네트워크 연결 문제로 실패하면, `throw` 인수를 `false`로 설정해도 `Illuminate\Http\Client\ConnectionException` 예외는 여전히 발생합니다.

<a name="error-handling"></a>
<!-- ### Error Handling -->
### Error Handling

<!-- Unlike Guzzle's default behavior, Laravel's HTTP client wrapper does not throw exceptions on client or server errors (`400` and `500` level responses from servers). You may determine if one of these errors was returned using the `successful`, `clientError`, or `serverError` methods: -->
Guzzle의 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트/서버 에러(`400`·`500` 상태) 발생 시 예외를 자동으로 던지지 않습니다. 이러한 오류가 반환됐는지 확인하려면 `successful`, `clientError`, `serverError` 등의 메서드를 사용할 수 있습니다:

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
응답 인스턴스가 있고, 상태 코드가 클라이언트 또는 서버 에러를 나타낸다면 직접 `Illuminate\Http\Client\RequestException` 예외를 던질 수 있습니다. 이때 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

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
`Illuminate\Http\Client\RequestException` 인스턴스에는 공개 `$response` 속성이 있어 반환된 응답을 확인할 수 있습니다.

<!-- The `throw` method returns the response instance if no error occurred, allowing you to chain other operations onto the `throw` method: -->
`throw` 메서드는 에러가 없으면 해당 응답 인스턴스를 그대로 반환하므로, `throw` 메서드에 추가적인 연산을 체이닝할 수도 있습니다:

```
return Http::post(/* ... */)->throw()->json();
```

<!-- If you would like to perform some additional logic before the exception is thrown, you may pass a closure to the `throw` method. The exception will be thrown automatically after the closure is invoked, so you do not need to re-throw the exception from within the closure: -->
예외가 발생하기 전 추가 로직이 필요하다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 이 때 예외는 클로저 실행 후 자동으로 던져지므로 내부에서 예외를 명시적으로 다시 던질 필요는 없습니다:

```
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

<a name="guzzle-middleware"></a>
<!-- ### Guzzle Middleware -->
### Guzzle Middleware

<!-- Since Laravel's HTTP client is powered by Guzzle, you may take advantage of [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) to manipulate the outgoing request or inspect the incoming response. To manipulate the outgoing request, register a Guzzle middleware via the `withRequestMiddleware` method: -->
Laravel의 HTTP 클라이언트는 Guzzle을 기반으로 동작하므로, [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용하여 아웃바운드 요청을 조작하거나 인바운드 응답을 검사할 수 있습니다. 아웃바운드 요청을 조작하고 싶을 경우 `withRequestMiddleware` 메서드로 미들웨어를 등록합니다:

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
마찬가지로, 들어오는 HTTP 응답을 검사하고 싶을 때는 `withResponseMiddleware` 메서드로 미들웨어를 등록할 수 있습니다:

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
모든 아웃바운드 요청과 인바운드 응답에 항상 적용할 미들웨어를 등록하고 싶을 때는 `globalRequestMiddleware`, `globalResponseMiddleware` 메서드를 사용합니다. 보통 이들은 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다:

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

<!-- You may specify additional [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html) using the `withOptions` method. The `withOptions` method accepts an array of key / value pairs: -->
`withOptions` 메서드를 사용하면 추가 [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. 이 `withOptions` 메서드는 key / value 쌍 배열을 인수로 받습니다:

```
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="concurrent-requests"></a>
<!-- ## Concurrent Requests -->
## Concurrent Requests

<!-- Sometimes, you may wish to make multiple HTTP requests concurrently. In other words, you want several requests to be dispatched at the same time instead of issuing the requests sequentially. This can lead to substantial performance improvements when interacting with slow HTTP APIs. -->
여러 HTTP 요청을 동시에 보낼 필요가 있을 때가 있습니다. 즉, 여러 요청을 순차적으로 처리하지 않고 한 번에 병렬로 전송하고자 하는 경우이며, 이는 느린 HTTP API와 상호작용할 때 큰 성능 향상으로 이어질 수 있습니다.

<!-- Thankfully, you may accomplish this using the `pool` method. The `pool` method accepts a closure which receives an `Illuminate\Http\Client\Pool` instance, allowing you to easily add requests to the request pool for dispatching: -->
이러한 경우 `pool` 메서드를 사용하면 됩니다. `pool` 메서드는 클로저를 인수로 받아 `Illuminate\Http\Client\Pool` 인스턴스를 제공하고, 여기에 요청을 추가할 수 있습니다:

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
각 응답 인스턴스에 pool에 추가된 순서대로 접근할 수 있습니다. 만약 요청에 이름을 붙이고 싶다면 `as` 메서드를 사용할 수 있고, 그러면 이름으로 결과에 접근할 수 있습니다:

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
`pool` 메서드는 `withHeaders`나 `middleware` 같은 다른 HTTP 클라이언트 메서드와 체이닝이 불가능합니다. pool에 추가한 각 요청에 직접 옵션을 지정해주어야 합니다:

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
Laravel HTTP 클라이언트를 사용하면 "매크로"를 정의할 수 있습니다. 매크로는 특정 서비스에 대해 자주 사용하는 주소, 헤더 등 공통 설정을 간결하게 묶어서 사용할 수 있게 도와줍니다. 매크로는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 정의합니다:

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
이렇게 매크로를 구성하면, 애플리케이션 어디서든 지정한 구성을 가진 pending request를 사용할 수 있습니다:

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's HTTP client is no exception. The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made. -->
Laravel의 여러 서비스는 테스트를 쉽게 할 수 있도록 다양한 기능을 제공합니다. HTTP 클라이언트도 예외는 아니며, `Http` 파사드의 `fake` 메서드를 이용하면 요청 시 미리 지정한 더미(dummpy) 응답을 반환하도록 가짜처리(stubbing/faking)할 수 있습니다.

<a name="faking-responses"></a>
<!-- ### Faking Responses -->
### Faking Responses

<!-- For example, to instruct the HTTP client to return empty, `200` status code responses for every request, you may call the `fake` method with no arguments: -->
예를 들어, 모든 요청에 대해 비어있는(내용 없음) `200` 상태 코드 응답을 반환하도록 하려면, `fake` 메서드를 인수 없이 호출하면 됩니다:

```
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
<!-- #### Faking Specific URLs -->
#### Faking Specific URLs

<!-- Alternatively, you may pass an array to the `fake` method. The array's keys should represent URL patterns that you wish to fake and their associated responses. The `*` character may be used as a wildcard character. Any requests made to URLs that have not been faked will actually be executed. You may use the `Http` facade's `response` method to construct stub / fake responses for these endpoints: -->
또는, `fake` 메서드에 배열을 전달할 수 있습니다. 이 때 배열의 키는 가짜로 만들고자 하는 URL 패턴, 값은 각 엔드포인트별로 반환할 응답 객체입니다. `*`(별표)는 와일드카드로 사용 가능합니다. 배열에 없는 URL로 요청하면 실제로 HTTP 요청이 전송됩니다. 각 엔드포인트에 대한 스텁 응답은 `Http` 파사드의 `response` 메서드로 생성합니다:

```
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

<!-- If you would like to specify a fallback URL pattern that will stub all unmatched URLs, you may use a single `*` character: -->
패턴에 매칭되지 않는 모든 URL을 포괄(fallback)해서 스텁 응답을 반환하고 싶다면, `*` 하나만 키로 사용하면 됩니다:

```
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

<a name="faking-response-sequences"></a>
<!-- #### Faking Response Sequences -->
#### Faking Response Sequences

<!-- Sometimes you may need to specify that a single URL should return a series of fake responses in a specific order. You may accomplish this using the `Http::sequence` method to build the responses: -->
특정 URL에 대해 여러 개의 응답을 순서대로 반환해야 할 상황도 있습니다. 이때는 `Http::sequence` 메서드로 응답 시퀀스를 구성할 수 있습니다:

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
응답 시퀀스의 모든 응답이 소진되면, 이후 요청에서는 예외가 발생합니다. 시퀀스가 모두 비었을 때 대신 반환할 기본 응답이 필요하다면, `whenEmpty` 메서드를 사용할 수 있습니다:

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
특정 URL 패턴 없이 모든 요청에 대해 응답 시퀀스를 가짜로 만들 때는 `Http::fakeSequence` 메서드를 사용할 수 있습니다:

```
Http::fakeSequence()
        ->push('Hello World', 200)
        ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
<!-- #### Fake Callback -->
#### Fake Callback

<!-- If you require more complicated logic to determine what responses to return for certain endpoints, you may pass a closure to the `fake` method. This closure will receive an instance of `Illuminate\Http\Client\Request` as well as an array of options. The closure should return a response instance. Within your closure, you may perform whatever logic is necessary to determine what type of response to return: -->
특정 엔드포인트에 대해 더 복잡한 논리로 어떤 응답을 반환할지 결정해야 할 때는, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스와 옵션 배열을 인수로 받으며, 반드시 응답 인스턴스를 반환해야 합니다. 이 안에서 필요한 모든 복잡한 로직을 구현할 수 있습니다:

```
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request, array $options) {
    return Http::response('Hello World', 200);
});
```

<a name="preventing-stray-requests"></a>
<!-- ### Preventing Stray Requests -->
### Preventing Stray Requests

<!-- If you would like to ensure that all requests sent via the HTTP client have been faked throughout your individual test or complete test suite, you can call the `preventStrayRequests` method. After calling this method, any requests that do not have a corresponding fake response will throw an exception rather than making the actual HTTP request: -->
테스트 중에 HTTP 클라이언트로 전송된 모든 요청이 반드시 fake이어야 한다는 것을 보장하고 싶을 때는, `preventStrayRequests` 메서드를 호출합니다. 이후 fake되지 않은 요청이 발생하면 실제 HTTP 요청 대신 예외가 발생합니다:

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
응답을 fake하는 경우, 클라이언트가 올바른 데이터나 헤더로 요청을 전송했는지 확인하고 싶은 경우가 있습니다. 이때 `Http::fake`를 호출한 후 `Http::assertSent` 메서드를 호출하면 됩니다.

<!-- The `assertSent` method accepts a closure which will receive an `Illuminate\Http\Client\Request` instance and should return a boolean value indicating if the request matches your expectations. In order for the test to pass, at least one request must have been issued matching the given expectations: -->
`assertSent` 메서드는 `Illuminate\Http\Client\Request` 인스턴스를 전달받는 클로저를 인수로 받으며, 이 클로저는 요청이 기대에 부합하는지를 나타내는 불리언 값을 반환해야 합니다. 테스트를 통과하려면 주어진 기대에 부합하는 요청이 최소 한 번은 전송되었어야 합니다:

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
특정 요청이 전송되지 않았음(assertNotSent)을 확인하려면 `assertNotSent` 메서드를 사용할 수 있습니다:

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
`assertSentCount` 메서드로 테스트 중 전송된 요청 수를 검증할 수 있습니다:

```
Http::fake();

Http::assertSentCount(5);
```

<!-- Or, you may use the `assertNothingSent` method to assert that no requests were sent during the test: -->
또는, `assertNothingSent` 메서드로 아무런 요청도 보내지 않았음을 검증할 수 있습니다:

```
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
<!-- #### Recording Requests / Responses -->
#### Recording Requests / Responses

<!-- You may use the `recorded` method to gather all requests and their corresponding responses. The `recorded` method returns a collection of arrays that contains instances of `Illuminate\Http\Client\Request` and `Illuminate\Http\Client\Response`: -->
`recorded` 메서드를 사용하면 모든 요청과 그에 대한 응답 목록을 조회할 수 있습니다. 이 `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스 쌍으로 구성된 컬렉션을 반환합니다:

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
또한, `recorded` 메서드에 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 전달받는 클로저를 전달하여 특정 조건에 맞는 요청/응답 쌍만 필터링할 수도 있습니다:

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
Laravel은 HTTP 요청 처리 과정에서 총 3개의 이벤트를 발생시킵니다. 요청이 전송되기 직전에 `RequestSending` 이벤트가, 요청에 대해 응답이 도착한 후에는 `ResponseReceived` 이벤트가 발생합니다. 서버로부터 응답을 받지 못한 경우에는 `ConnectionFailed` 이벤트가 발생합니다.

<!-- The `RequestSending` and `ConnectionFailed` events both contain a public `$request` property that you may use to inspect the `Illuminate\Http\Client\Request` instance. Likewise, the `ResponseReceived` event contains a `$request` property as well as a `$response` property which may be used to inspect the `Illuminate\Http\Client\Response` instance. You may register event listeners for this event in your `App\Providers\EventServiceProvider` service provider: -->
`RequestSending`과 `ConnectionFailed` 이벤트에는 `Illuminate\Http\Client\Request` 인스턴스를 확인할 수 있는 공개 `$request` 속성이 있습니다. 마찬가지로 `ResponseReceived` 이벤트에는 `$request`와 함께, `Illuminate\Http\Client\Response` 인스턴스를 확인할 수 있는 `$response` 속성도 있습니다. 이러한 이벤트에 리스너를 등록하려면, `App\Providers\EventServiceProvider`의 이벤트 매핑에 아래와 같이 추가하세요:

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Http\Client\Events\RequestSending' => [
        'App\Listeners\LogRequestSending',
    ],
    'Illuminate\Http\Client\Events\ResponseReceived' => [
        'App\Listeners\LogResponseReceived',
    ],
    'Illuminate\Http\Client\Events\ConnectionFailed' => [
        'App\Listeners\LogConnectionFailed',
    ],
];
```
