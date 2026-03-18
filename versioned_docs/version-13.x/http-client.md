# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청하기](#making-requests)
    - [데이터 요청](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [시간 초과](#timeout)
    - [재시도](#retries)
    - [오류 처리](#error-handling)
    - [Guzzle 미들웨어](#guzzle-middleware)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
    - [풀링 요청](#request-pooling)
    - [배치 요청](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [가짜 응답](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [예기치 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel는 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/) 주변에 표현력이 뛰어나고 최소한의 API를 제공하므로 다른 웹 애플리케이션과 통신하기 위해 나가는 HTTP 요청을 빠르게 만들 수 있습니다. Guzzle를 둘러싼 Laravel 래퍼는 가장 일반적인 사용 사례와 훌륭한 개발자 경험에 중점을 두고 있습니다.

<a name="making-requests"></a>
## 요청하기 (Making Requests)

요청을 하려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저 다른 URL에 기본 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 응답을 검사하는 데 사용할 수 있는 다양한 메서드를 제공하는 `Illuminate\Http\Client\Response`의 인스턴스를 반환합니다.

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

`Illuminate\Http\Client\Response` 객체는 또한 PHP `ArrayAccess` 인터페이스를 구현하여 응답에서 직접 JSON 응답 데이터에 액세스할 수 있도록 합니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 응답 방법 외에도 다음 방법을 사용하여 응답에 특정 상태 코드가 있는지 확인할 수 있습니다.

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

HTTP 클라이언트를 사용하면 [URI 템플릿 사양](https://www.rfc-editor.org/rfc/rfc6570)을 사용하여 요청 URL을 구성할 수도 있습니다. URI 템플릿으로 확장할 수 있는 URL 매개변수를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 덤핑 요청

나가는 요청 인스턴스가 전송되기 전에 덤프하고 스크립트 실행을 종료하려면 요청 정의 시작 부분에 `dd` 메서드를 추가하면 됩니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 데이터 요청

물론 `POST`, `PUT` 및 `PATCH` 요청을 할 때 요청과 함께 추가 데이터를 보내는 것이 일반적이므로 이러한 메서드는 데이터 배열을 두 번째 인수로 허용합니다. 기본적으로 데이터는 `application/json` 콘텐츠 유형을 사용하여 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 매개변수

`GET` 요청을 할 때 쿼리 문자열을 URL에 직접 추가하거나 키/값 쌍의 배열을 `get` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는 `withQueryParameters` 방법을 사용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### 양식 URL 인코딩된 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 유형을 사용하여 데이터를 전송하려면 요청하기 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문 보내기

요청할 때 원시 요청 본문을 제공하려는 경우 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 유형은 메서드의 두 번째 인수를 통해 제공될 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 다중 부분 요청

다중 부분 요청으로 파일을 보내려면 요청하기 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일 이름과 내용을 승인합니다. 필요한 경우 파일의 파일 이름으로 간주되는 세 번째 인수를 제공할 수 있으며, 네 번째 인수는 파일과 관련된 헤더를 제공하는 데 사용될 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원시 내용을 전달하는 대신 스트림 리소스를 전달할 수 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더

`withHeaders` 메서드를 사용하여 요청에 헤더를 추가할 수 있습니다. 이 `withHeaders` 메서드는 키/값 쌍의 배열을 허용합니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용하여 요청에 대한 응답으로 애플리케이션이 기대하는 콘텐츠 유형을 지정할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

편의를 위해 `acceptJson` 메서드를 사용하여 애플리케이션이 요청에 대한 응답으로 `application/json` 콘텐츠 유형을 기대하도록 신속하게 지정할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 새 헤더를 요청의 기존 헤더에 병합합니다. 필요한 경우 `replaceHeaders` 방법을 사용하여 모든 헤더를 완전히 바꿀 수 있습니다.

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

`withBasicAuth` 및 `withDigestAuth` 메서드를 사용하여 기본 인증 및 다이제스트 인증 자격 증명을 각각 지정할 수 있습니다.

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 베어러 토큰

요청의 `Authorization` 헤더에 베어러 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용할 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 시간 초과

`timeout` 메서드는 응답을 기다리는 최대 시간(초)을 지정하는 데 사용될 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후에 시간 초과됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정된 시간 초과가 초과되면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

`connectTimeout` 메서드를 사용하여 서버에 연결을 시도하는 동안 대기할 최대 시간(초)을 지정할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류가 발생하는 경우 HTTP 클라이언트가 자동으로 요청을 재시도하도록 하려면 `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 요청이 시도되어야 하는 최대 횟수와 시도 사이에 Laravel가 대기해야 하는 밀리초 수를 허용합니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

시도 사이에 대기할 시간(밀리초)을 수동으로 계산하려면 `retry` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해 배열을 `retry` 메서드의 첫 번째 인수로 제공할 수도 있습니다. 이 배열은 후속 시도 사이에 대기할 시간(밀리초)을 결정하는 데 사용됩니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요한 경우 `retry` 메서드에 세 번째 인수를 전달할 수 있습니다. 세 번째 인수는 실제로 재시도를 시도해야 하는지 여부를 결정하는 호출 가능 항목이어야 합니다. 예를 들어 초기 요청에서 `ConnectionException`가 발생한 경우에만 요청을 재시도할 수 있습니다.

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청 시도가 실패하면 새로운 시도가 이루어지기 전에 요청을 변경할 수 있습니다. `retry` 메서드에 제공한 콜러블에 제공된 요청 인수를 수정하여 이를 달성할 수 있습니다. 예를 들어 첫 번째 시도에서 인증 오류가 반환된 경우 새 인증 토큰을 사용하여 요청을 재시도할 수 있습니다.

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하려면 `false` 값으로 `throw` 인수를 제공할 수 있습니다. 비활성화되면 모든 재시도가 시도된 후 클라이언트가 받은 마지막 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 연결 문제로 인해 모든 요청이 실패하면 `throw` 인수가 `false`로 설정된 경우에도 `Illuminate\Http\Client\ConnectionException`가 계속 발생합니다.

<a name="error-handling"></a>
### 오류 처리

Guzzle의 기본 동작과 달리 Laravel의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버의 `400` 및 `500` 수준 응답)에 예외를 발생시키지 않습니다. `successful`, `clientError` 또는 `serverError` 메서드를 사용하여 이러한 오류 중 하나가 반환되었는지 확인할 수 있습니다.

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
#### 예외 던지기

응답 인스턴스가 있고 응답 상태 코드가 클라이언트 또는 서버 오류를 나타내는 경우 `Illuminate\Http\Client\RequestException` 인스턴스를 발생시키려는 경우 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

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

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있는 공개 `$response` 속성이 있습니다.

`throw` 메서드는 오류가 발생하지 않은 경우 응답 인스턴스를 반환하므로 `throw` 메서드에 다른 작업을 연결할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 몇 가지 추가 논리를 수행하려면 `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저가 호출된 후 예외가 자동으로 발생하므로 클로저 내에서 예외를 다시 발생시킬 필요가 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 기록되거나 보고될 때 120자로 잘립니다. 이 동작을 사용자 지정하거나 비활성화하려면 `bootstrap/app.php` 파일에서 애플리케이션의 등록된 동작을 구성할 때 `truncateAt` 및 `dontTruncate` 메서드를 활용할 수 있습니다.

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // Truncate request exception messages to 240 characters...
    RequestException::truncateAt(240);

    // Disable request exception message truncation...
    RequestException::dontTruncate();
})
```

또는 `truncateExceptionsAt` 메서드를 사용하여 요청별로 예외 잘림 동작을 사용자 지정할 수 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel의 HTTP 클라이언트는 Guzzle에 의해 구동되므로 [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용하여 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면 `withRequestMiddleware` 메서드를 통해 Guzzle 미들웨어를 등록하세요.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로 `withResponseMiddleware` 메서드를 통해 미들웨어를 등록하여 수신 HTTP 응답을 검사할 수 있습니다.

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
#### 글로벌 미들웨어

때로는 모든 나가는 요청과 들어오는 응답에 적용되는 미들웨어를 등록하고 싶을 수도 있습니다. 이를 수행하려면 `globalRequestMiddleware` 및 `globalResponseMiddleware` 방법을 사용할 수 있습니다. 일반적으로 이러한 메서드는 애플리케이션 `AppServiceProvider`의 `boot` 메서드에서 호출되어야 합니다.

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

`withOptions` 메서드를 사용하여 나가는 요청에 대해 추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. `withOptions` 메서드는 키/값 쌍의 배열을 허용합니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 글로벌 옵션

나가는 모든 요청에 대해 기본 옵션을 구성하려면 `globalOptions` 메서드를 활용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션 `AppServiceProvider`의 `boot` 메서드에서 호출되어야 합니다.

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

때로는 여러 HTTP 요청을 동시에 만들고 싶을 수도 있습니다. 즉, 요청을 순차적으로 발행하는 대신 여러 요청이 동시에 디스패치가 되기를 원합니다. 이는 느린 HTTP API와 상호작용할 때 상당한 성능 향상으로 이어질 수 있습니다.

<a name="request-pooling"></a>
### 풀링 요청

다행히도 `pool` 메서드를 사용하여 이 작업을 수행할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 수신하는 클로저를 허용하므로 디스패치에 대한 요청 풀에 요청을 쉽게 추가할 수 있습니다.

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

보시다시피 각 응답 인스턴스는 풀에 추가된 순서에 따라 액세스할 수 있습니다. 원하는 경우 `as` 메서드를 사용하여 요청에 이름을 지정할 수 있습니다. 이를 통해 이름으로 해당 응답에 액세스할 수 있습니다.

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

요청 풀의 최대 동시성은 `pool` 메서드에 `concurrency` 인수를 제공하여 제어할 수 있습니다. 이 값은 요청 풀을 처리하는 동안 동시에 진행될 수 있는 HTTP 요청의 최대 수를 결정합니다.

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 사용자 지정

`pool` 메서드는 `withHeaders` 또는 `middleware` 메서드와 같은 다른 HTTP 클라이언트 메서드와 연결할 수 없습니다. 풀링된 요청에 사용자 지정 헤더 또는 미들웨어를 적용하려면 풀의 각 요청에 대해 해당 옵션을 구성해야 합니다.

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
### 배치 요청

Laravel에서 동시 요청을 처리하는 또 다른 방법은 `batch` 메서드를 사용하는 것입니다. `pool` 메서드와 마찬가지로 `Illuminate\Http\Client\Batch` 인스턴스를 수신하는 클로저를 허용하므로 디스패치에 대한 요청 풀에 요청을 쉽게 추가할 수 있지만 완료 콜백을 정의할 수도 있습니다.

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

`pool` 메서드와 마찬가지로 `as` 메서드를 사용하여 요청 이름을 지정할 수 있습니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`batch`가 `send` 메서드를 호출하여 시작된 후에는 새 요청을 추가할 수 없습니다. 그렇게 하면 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생하게 됩니다.

배치 요청의 최대 동시성은 `concurrency` 메서드를 통해 제어될 수 있습니다. 이 값은 배치 요청을 처리하는 동안 동시에 진행 중인 HTTP 요청의 최대 수를 결정합니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### 배치 검사

배치 완료 콜백에 제공되는 `Illuminate\Http\Client\Batch` 인스턴스에는 지정된 배치 요청과 상호작용하고 검사하는 데 도움이 되는 다양한 속성과 메서드가 있습니다.

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
#### 배치 연기

`defer` 메서드가 호출되면 요청의 배치가 즉시 실행되지 않습니다. 대신, Laravel는 현재 애플리케이션 요청의 HTTP 응답이 사용자에게 전송된 후 배치를 실행하여 애플리케이션의 속도와 반응성을 유지합니다.

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

Laravel HTTP 클라이언트를 사용하면 애플리케이션 전체에서 서비스와 상호 작용할 때 공통 요청 경로 및 헤더를 구성하는 유창하고 표현력 있는 메커니즘 역할을 할 수 있는 "매크로"를 정의할 수 있습니다. 시작하려면 애플리케이션 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 매크로를 정의할 수 있습니다.

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

매크로가 구성되면 애플리케이션의 어느 곳에서나 매크로를 호출하여 지정된 구성으로 보류 중인 요청을 생성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

많은 Laravel 서비스는 테스트를 쉽고 표현력 있게 작성하는 데 도움이 되는 기능을 제공하며, Laravel의 HTTP 클라이언트도 예외는 아닙니다. `Http` 파사드의 `fake` 메서드를 사용하면 요청이 있을 때 HTTP 클라이언트가 스텁/더미 응답을 반환하도록 지시할 수 있습니다.

<a name="faking-responses"></a>
### 가짜 응답

예를 들어, HTTP 클라이언트가 모든 요청에 ​​대해 빈 `200` 상태 코드 응답을 반환하도록 지시하려면 인수 없이 `fake` 메서드를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL 위조

또는 `fake` 메서드에 배열을 전달할 수도 있습니다. 배열의 키는 위조하려는 URL 패턴과 관련 응답을 나타내야 합니다. `*` 문자는 와일드카드 문자로 사용될 수 있습니다. `Http` 파사드의 `response` 메서드를 사용하여 다음 엔드포인트에 대한 스텁/가짜 응답을 생성할 수 있습니다:

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

위조되지 않은 URL에 대한 요청은 실제로 실행됩니다. 일치하지 않는 모든 URL을 스텁하는 대체 URL 패턴을 지정하려면 단일 `*` 문자를 사용할 수 있습니다.

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

편의를 위해 문자열, 배열 또는 정수를 응답으로 제공하여 간단한 문자열, JSON 및 빈 응답을 생성할 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 가짜 예외

때때로 HTTP 클라이언트가 요청을 시도할 때 `Illuminate\Http\Client\ConnectionException`를 발견하는 경우 애플리케이션의 동작을 테스트해야 할 수도 있습니다. `failedConnection` 메서드를 사용하여 연결 예외를 발생시키도록 HTTP 클라이언트에 지시할 수 있습니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException`가 발생한 경우 애플리케이션의 동작을 테스트하려면 `failedRequest` 메서드를 사용할 수 있습니다.

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
#### 가짜 응답 시퀀스

때로는 단일 URL가 특정 순서로 일련의 가짜 응답을 반환하도록 지정해야 할 수도 있습니다. 응답을 작성하기 위해 `Http::sequence` 메서드를 사용하여 이를 수행할 수 있습니다.

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

응답 시퀀스의 모든 응답이 사용되면 추가 요청으로 인해 응답 시퀀스에서 예외가 발생합니다. 시퀀스가 비어 있을 때 반환되어야 하는 기본 응답을 지정하려면 `whenEmpty` 메서드를 사용할 수 있습니다.

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

일련의 응답을 위조하고 싶지만 위조해야 하는 특정 URL 패턴을 지정할 필요가 없는 경우 `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 가짜 콜백

특정 끝점에 대해 반환할 응답을 결정하기 위해 더 복잡한 논리가 필요한 경우 `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 수신하고 응답 인스턴스를 반환해야 합니다. 클로저 내에서 반환할 응답 유형을 결정하는 데 필요한 모든 논리를 수행할 수 있습니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 검사

응답을 속일 때 애플리케이션이 올바른 데이터나 헤더를 보내고 있는지 확인하기 위해 때때로 클라이언트가 받는 요청을 검사하고 싶을 수도 있습니다. `Http::fake`를 호출한 후 `Http::assertSent` 메서드를 호출하여 이를 수행할 수 있습니다.

`assertSent` 메서드는 `Illuminate\Http\Client\Request` 인스턴스를 수신하는 클로저를 승인하고 요청이 기대와 일치하는지 나타내는 부울 값을 반환해야 합니다. 테스트를 통과하려면 주어진 기대와 일치하는 요청이 하나 이상 발행되어야 합니다.

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

필요한 경우 `assertNotSent` 메서드를 사용하여 특정 요청이 전송되지 않았다고 주장할 수 있습니다.

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

`assertSentCount` 메서드를 사용하여 테스트에 "전송된" 요청 수를 확인할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또는 `assertNothingSent` 메서드를 사용하여 테스트에 요청이 전송되지 않았음을 확인할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록

`recorded` 메서드를 사용하여 모든 요청과 해당 응답을 수집할 수 있습니다. `recorded` 메서드는 `Illuminate\Http\Client\Request` 및 `Illuminate\Http\Client\Response`의 인스턴스를 포함하는 배열 컬렉션을 반환합니다.

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

추가적으로, `recorded` 메서드는 `Illuminate\Http\Client\Request` 및 `Illuminate\Http\Client\Response`의 인스턴스를 수신하고 기대에 따라 요청/응답 쌍을 필터링하는 데 사용될 수 있는 클로저를 허용합니다.

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
### 예기치 않은 요청 방지

HTTP 클라이언트를 통해 전송된 모든 요청이 개별 테스트 또는 전체 테스트 모음에서 위조되었는지 확인하려면 `preventStrayRequests` 메서드를 호출하면 됩니다. 이 메서드를 호출한 후 해당 가짜 응답이 없는 요청은 실제 HTTP 요청을 수행하는 대신 예외를 발생시킵니다.

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

때로는 특정 요청의 실행을 허용하면서 대부분의 예기치 않은 요청을 방지하고 싶을 수도 있습니다. 이를 수행하려면 URL 패턴 배열을 `allowStrayRequests` 메서드에 전달할 수 있습니다. 지정된 패턴 중 하나와 일치하는 요청은 허용되지만 다른 모든 요청은 계속해서 예외가 발생합니다.

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

Laravel는 HTTP 요청을 보내는 과정에서 3개의 이벤트를 실행합니다. `RequestSending` 이벤트는 요청이 전송되기 전에 실행되는 반면, `ResponseReceived` 이벤트는 주어진 요청에 대한 응답이 수신된 후에 실행됩니다. 주어진 요청에 대해 응답이 수신되지 않으면 `ConnectionFailed` 이벤트가 실행됩니다.

`RequestSending` 및 `ConnectionFailed` 이벤트에는 모두 `Illuminate\Http\Client\Request` 인스턴스를 검사하는 데 사용할 수 있는 공개 `$request` 속성이 포함되어 있습니다. 마찬가지로, `ResponseReceived` 이벤트에는 `$request` 속성과 `Illuminate\Http\Client\Response` 인스턴스를 검사하는 데 사용할 수 있는 `$response` 속성이 포함되어 있습니다. 애플리케이션 내에서 다음 이벤트에 대해 [이벤트 리스너](/docs/13.x/events)를 생성할 수 있습니다.

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
