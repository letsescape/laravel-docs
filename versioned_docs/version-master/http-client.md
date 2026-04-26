# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [오류 처리](#error-handling)
    - [Guzzle Middleware](#guzzle-middleware)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
    - [요청 풀링](#request-pooling)
    - [요청 배치 처리](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 가짜 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [의도하지 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 감싸는 표현력 있고 간결한 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위한 외부 HTTP 요청을 빠르게 보낼 수 있습니다. Laravel의 Guzzle 래퍼는 가장 자주 사용되는 사례와 뛰어난 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

요청을 보내려면 `Http` facade가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하므로, 응답에서 JSON 응답 데이터에 직접 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

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
#### URI 템플릿

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용하여 요청 URL을 구성할 수도 있습니다. URI 템플릿에서 확장될 수 있는 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프하기

전송되기 전에 외부로 나가는 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가할 수 있습니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터

물론 `POST`, `PUT`, `PATCH` 요청을 보낼 때 요청과 함께 추가 데이터를 보내는 일은 흔합니다. 따라서 이 메서드들은 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때는 URL에 쿼리 문자열을 직접 붙이거나, `get` 메서드의 두 번째 인수로 키 / 값 쌍의 배열을 전달할 수 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 메서드를 사용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶다면, 요청을 보내기 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문 보내기

요청을 보낼 때 원시 요청 본문을 제공하고 싶다면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 이 메서드의 두 번째 인수로 제공할 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트 요청

파일을 멀티파트 요청으로 보내고 싶다면, 요청을 보내기 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일의 이름과 내용을 받습니다. 필요하다면 세 번째 인수로 파일명을 제공할 수 있으며, 네 번째 인수는 파일과 관련된 헤더를 제공하는 데 사용할 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원시 내용을 전달하는 대신 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

`withHeaders` 메서드를 사용하여 요청에 헤더를 추가할 수 있습니다. 이 `withHeaders` 메서드는 키 / 값 쌍의 배열을 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용하여 애플리케이션이 요청에 대한 응답으로 기대하는 콘텐츠 타입을 지정할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

편의를 위해 `acceptJson` 메서드를 사용하면, 애플리케이션이 요청에 대한 응답으로 `application/json` 콘텐츠 타입을 기대한다고 빠르게 지정할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

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
### 인증

`withBasicAuth` 및 `withDigestAuth` 메서드를 사용하여 각각 기본 인증과 다이제스트 인증 자격 증명을 지정할 수 있습니다.

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

요청의 `Authorization` 헤더에 Bearer 토큰을 빠르게 추가하고 싶다면 `withToken` 메서드를 사용할 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃

`timeout` 메서드는 응답을 기다릴 최대 초 수를 지정하는 데 사용할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

서버에 연결을 시도하는 동안 기다릴 최대 초 수는 `connectTimeout` 메서드를 사용하여 지정할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류가 발생했을 때 HTTP 클라이언트가 요청을 자동으로 재시도하도록 하려면 `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 요청을 시도할 최대 횟수와 Laravel이 각 시도 사이에 기다릴 밀리초 수를 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

각 시도 사이에 대기할 밀리초 수를 직접 계산하고 싶다면, `retry` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해 `retry` 메서드의 첫 번째 인수로 배열을 제공할 수도 있습니다. 이 배열은 이어지는 시도 사이에 몇 밀리초 동안 대기할지 결정하는 데 사용됩니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 `retry` 메서드에 세 번째 인수를 전달할 수 있습니다. 세 번째 인수는 실제로 재시도를 시도할지 결정하는 callable이어야 합니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생한 경우에만 요청을 재시도하고 싶을 수 있습니다.

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하고 싶다면 `throw` 인수에 `false` 값을 제공할 수 있습니다. 비활성화하면 모든 재시도가 시도된 후 클라이언트가 마지막으로 받은 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 인해 실패한 경우에는 `throw` 인수가 `false`로 설정되어 있어도 `Illuminate\Http\Client\ConnectionException`이 계속 발생합니다.

<a name="error-handling"></a>
### 오류 처리

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
#### 예외 발생시키기

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

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있도록 public `$response` 속성이 있습니다.

오류가 발생하지 않았다면 `throw` 메서드는 응답 인스턴스를 반환하므로, `throw` 메서드 뒤에 다른 작업을 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 로직을 수행하고 싶다면, `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저가 호출된 후 예외는 자동으로 발생하므로, 클로저 안에서 예외를 다시 던질 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

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

또는 `truncateExceptionsAt` 메서드를 사용하여 요청별로 예외 메시지 자르기 동작을 사용자 정의할 수 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle Middleware

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
#### 전역 Middleware

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
### Guzzle 옵션

`withOptions` 메서드를 사용하여 나가는 요청에 추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. `withOptions` 메서드는 키 / 값 쌍의 배열을 인수로 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션

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
## 동시 요청 (Concurrent Requests)

때로는 여러 HTTP 요청을 동시에 보내고 싶을 수 있습니다. 즉, 요청을 순차적으로 실행하는 대신 여러 요청을 같은 시점에 디스패치하려는 것입니다. 느린 HTTP API와 통신할 때 이는 상당한 성능 향상으로 이어질 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀링

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

요청 풀의 최대 동시성은 `pool` 메서드에 `concurrency` 인수를 전달하여 제어할 수 있습니다. 이 값은 요청 풀을 처리하는 동안 동시에 진행 중일 수 있는 HTTP 요청의 최대 개수를 결정합니다.

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 사용자 정의

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
### 요청 배치 처리

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

`pool` 메서드와 마찬가지로 `as` 메서드를 사용하여 요청에 이름을 붙일 수 있습니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` 메서드를 호출하여 `batch`가 시작된 뒤에는 새 요청을 추가할 수 없습니다. 이를 시도하면 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

요청 배치의 최대 동시성은 `concurrency` 메서드로 제어할 수 있습니다. 이 값은 요청 배치를 처리하는 동안 동시에 진행 중일 수 있는 HTTP 요청의 최대 개수를 결정합니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### 배치 검사

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
#### 배치 지연 실행

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
## 매크로 (Macros)

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

매크로 설정이 완료되면 애플리케이션 어디에서나 이를 호출하여 지정된 설정을 가진 보류 중인 요청을 생성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스는 테스트를 쉽고 표현력 있게 작성할 수 있도록 돕는 기능을 제공하며, Laravel의 HTTP 클라이언트도 예외가 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 요청이 이루어질 때 HTTP 클라이언트가 스텁 / 더미 응답을 반환하도록 지시할 수 있습니다.

<a name="faking-responses"></a>
### 응답 페이크

예를 들어 모든 요청에 대해 빈 `200` 상태 코드 응답을 반환하도록 HTTP 클라이언트에 지시하려면, 인수 없이 `fake` 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 페이크

또는 `fake` 메서드에 배열을 전달할 수 있습니다. 배열의 키는 페이크하려는 URL 패턴을 나타내고, 값은 그에 연결된 응답을 나타내야 합니다. `*` 문자는 와일드카드 문자로 사용할 수 있습니다. 이러한 엔드포인트에 대한 스텁 / 페이크 응답을 구성하려면 `Http` 파사드의 `response` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

페이크되지 않은 URL로 이루어지는 모든 요청은 실제로 실행됩니다. 매칭되지 않는 모든 URL을 스텁 처리할 fallback URL 패턴을 지정하고 싶다면 단일 `*` 문자를 사용할 수 있습니다.

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편의를 위해 문자열, 배열, 정수를 응답으로 제공하여 간단한 문자열, JSON, 빈 응답을 생성할 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 페이크

때로는 HTTP 클라이언트가 요청을 시도하는 중 `Illuminate\Http\Client\ConnectionException`을 만났을 때 애플리케이션이 어떻게 동작하는지 테스트해야 할 수 있습니다. `failedConnection` 메서드를 사용하면 HTTP 클라이언트가 연결 예외를 발생시키도록 지시할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException`이 발생했을 때 애플리케이션의 동작을 테스트하려면 `failedRequest` 메서드를 사용할 수 있습니다.

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 페이크

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

응답 시퀀스를 페이크하고 싶지만 페이크할 특정 URL 패턴을 지정할 필요가 없다면 `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 페이크 콜백

특정 엔드포인트에 대해 어떤 응답을 반환할지 결정하는 더 복잡한 로직이 필요하다면 `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받으며 응답 인스턴스를 반환해야 합니다. 클로저 안에서는 어떤 유형의 응답을 반환할지 결정하는 데 필요한 모든 로직을 수행할 수 있습니다.
```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사

응답을 fake 처리할 때, 애플리케이션이 올바른 데이터나 헤더를 전송하는지 확인하기 위해 클라이언트가 받은 요청을 검사하고 싶을 때가 있습니다. 이는 `Http::fake`를 호출한 뒤 `Http::assertSent` 메서드를 호출하여 수행할 수 있습니다.

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

`assertSentCount` 메서드를 사용하여 테스트 중에 몇 개의 요청이 "전송"되었는지 검증할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또는 `assertNothingSent` 메서드를 사용하여 테스트 중에 아무 요청도 전송되지 않았는지 검증할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청 / 응답 기록

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
### 예상 밖 요청 방지

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
## 이벤트 (Events)

Laravel은 HTTP 요청을 전송하는 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에 발생하고, `ResponseReceived` 이벤트는 특정 요청에 대한 응답을 받은 뒤에 발생합니다. `ConnectionFailed` 이벤트는 특정 요청에 대한 응답을 받지 못한 경우 발생합니다.

`RequestSending` 이벤트와 `ConnectionFailed` 이벤트는 모두 공개 `$request` 속성을 포함하며, 이를 사용해 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있습니다. 마찬가지로 `ResponseReceived` 이벤트는 `$request` 속성과 함께 `$response` 속성을 포함하며, 이 `$response` 속성을 사용해 `Illuminate\Http\Client\Response` 인스턴스를 검사할 수 있습니다. 애플리케이션 안에서 이러한 이벤트에 대한 [이벤트 리스너](/docs/master/events)를 만들 수 있습니다.

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
