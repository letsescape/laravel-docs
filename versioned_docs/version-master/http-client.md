# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더 설정](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [에러 처리](#error-handling)
    - [Guzzle 미들웨어](#guzzle-middleware)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
    - [요청 풀링](#request-pooling)
    - [요청 배치](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 페이크](#faking-responses)
    - [요청 확인](#inspecting-requests)
    - [임의의 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP 클라이언트](http://docs.guzzlephp.org/en/stable/)를 기반으로 직관적이면서도 최소한의 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신하기 위한 외부 HTTP 요청을 매우 빠르게 구현할 수 있습니다. Laravel의 Guzzle 래퍼는 가장 일반적인 사용 사례 및 개발자 경험에 초점을 맞추고 있습니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

HTTP 요청을 보내기 위해 `Http` 파사드(Facade)가 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL로 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 반환된 객체를 통해 다양한 방식으로 응답을 확인할 수 있습니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP `ArrayAccess` 인터페이스도 구현하고 있어서, JSON 응답 데이터를 배열 형태로 바로 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에서 언급한 응답 메서드 외에도, 특정 상태 코드(status code)를 확인할 수 있는 추가 메서드들이 제공됩니다.

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

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용하여 요청 URL을 구성할 수 있습니다. `withUrlParameters` 메서드를 활용하면, URI 템플릿에서 확장될 URL 파라미터를 정의할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 내용 디버깅 (Dumping Requests)

요청이 실제로 전송되기 전에 해당 요청 인스턴스를 출력하고 스크립트 실행을 중단하고 싶다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가하면 됩니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

`POST`, `PUT`, `PATCH` 요청과 같이 서버에 추가 데이터를 전송해야 할 경우, 해당 메서드의 두 번째 인수로 데이터를 배열 형태로 전달할 수 있습니다. 기본적으로 `application/json` 컨텐트 타입으로 데이터가 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청에서 쿼리 문자열을 URL에 바로 붙일 수도 있고, 두 번째 인수로 키-값 쌍의 배열을 넘길 수도 있습니다.

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

또는, `withQueryParameters` 메서드를 사용할 수도 있습니다.

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### Form URL 인코딩 데이터 전송

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 전송하고 싶다면, 요청 전에 `asForm` 메서드를 호출하면 됩니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 원시 바디 데이터 전송

원시(raw) 데이터로 요청 바디를 지정해야 할 경우, `withBody` 메서드를 사용할 수 있습니다. 컨텐츠 타입은 두 번째 인수로 지정합니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### 멀티파트(Multi-Part) 요청

파일을 멀티파트 요청으로 전송하려면, 요청 전에 `attach` 메서드를 사용해 파일명을 지정하고, 파일의 실제 내용을 전달해야 합니다. '파일명', '파일 내용', '파일의 파일명(선택)', '파일 관련 헤더(선택)' 순으로 인수를 받을 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 원시 내용 대신 스트림 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 설정 (Headers)

요청에 헤더를 추가하려면, `withHeaders` 메서드를 사용하면 됩니다. 이 메서드는 키-값 쌍의 배열을 인수로 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용해 응답으로 기대하는 컨텐츠 타입을 지정할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

응답으로 `application/json` 타입을 기대할 때는 `acceptJson`을 이용해 더 간단히 지정할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders`는 기존 헤더에 새로운 헤더를 병합합니다. 모든 헤더를 완전히 교체하고 싶다면, `replaceHeaders` 메서드를 사용하세요.

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
### 인증 (Authentication)

기본 인증(베이직 인증)과 다이제스트 인증을 각각 `withBasicAuth`, `withDigestAuth` 메서드를 사용하여 지정할 수 있습니다.

```php
// Basic 인증...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest 인증...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### Bearer 토큰

요청의 `Authorization` 헤더에 bearer 토큰을 빠르게 추가하려면, `withToken` 메서드를 사용할 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드를 사용해 응답을 기다리는 최대 초(second) 단위를 지정할 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후 타임아웃 됩니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 타임아웃이 초과되면, `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

서버에 연결을 시도할 때 기다리는 최대 시간을 `connectTimeout` 메서드로 지정할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 오류가 발생했을 때, HTTP 클라이언트가 자동으로 요청을 재시도하도록 하려면, `retry` 메서드를 사용할 수 있습니다. 이 메서드는 최대 시도 횟수와 각 시도 사이에 기다릴 밀리초(ms) 단위를 인수로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

각 시도 사이에 대기할 밀리초를 직접 계산하고 싶다면, 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

첫 번째 인수로 배열을 전달하면, 배열의 각 값만큼 순차적으로 대기하게 됩니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

세 번째 인수로는 실제로 재시도를 할지 여부를 결정하는 콜러블을 지정할 수 있습니다. 예를 들어, 처음 요청에서 `ConnectionException`이 발생한 경우에만 재시도하고 싶을 때 사용할 수 있습니다.

```php
use Exception;
use Illuminate\Http\Client\PendingRequest;

$response = Http::retry(3, 100, function (Exception $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

만약 요청이 실패하면, 다음 시도 전에 요청을 수정할 수도 있습니다. 예를 들어, 첫 번째 시도에서 인증 오류가 발생하면 새 인증 토큰으로 재시도할 수 있습니다.

```php
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

모든 요청이 실패한 경우, `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다. 이 동작을 비활성화하려면, `throw` 파라미터를 `false`로 지정할 수 있습니다. 이 설정을 하면, 모든 재시도 후 마지막 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패하면, `throw` 파라미터를 `false`로 해도 `Illuminate\Http\Client\ConnectionException` 예외는 계속 발생합니다.

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

Guzzle의 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버에서 `400`, `500`대 응답)에 대해 예외를 자동으로 발생시키지 않습니다. 이러한 오류가 발생했는지 여부는 `successful`, `clientError`, `serverError` 메서드로 확인할 수 있습니다.

```php
// 상태 코드가 200 이상 300 미만인지 확인
$response->successful();

// 상태 코드가 400 이상인지 확인
$response->failed();

// 400번대 상태 코드(클라이언트 오류)인지 확인
$response->clientError();

// 500번대 상태 코드(서버 오류)인지 확인
$response->serverError();

// 클라이언트/서버 오류시 즉시 콜백 실행
$response->onError(callable $callback);
```

<a name="throwing-exceptions"></a>
#### 예외 발생 (Throwing Exceptions)

응답 인스턴스가 있고, 상태 코드가 클라이언트 또는 서버 오류라면 `Illuminate\Http\Client\RequestException` 예외를 발생시키고 싶을 때 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// 클라이언트나 서버 오류 시 예외 발생
$response->throw();

// 오류가 발생했고, 특정 조건이 true라면 예외 발생
$response->throwIf($condition);

// 오류가 발생했고, 클로저 반환값이 true라면 예외 발생
$response->throwIf(fn (Response $response) => true);

// 오류가 발생했고, 특정 조건이 false라면 예외 발생
$response->throwUnless($condition);

// 오류가 발생했고, 클로저 반환값이 false라면 예외 발생
$response->throwUnless(fn (Response $response) => false);

// 응답이 특정 상태 코드일 때 예외 발생
$response->throwIfStatus(403);

// 응답이 특정 상태 코드가 아닐 때 예외 발생
$response->throwUnlessStatus(200);

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 확인할 수 있도록 public `$response` 속성이 있습니다.

`throw` 메서드는 오류가 없을 때 응답 인스턴스를 그대로 반환하므로, 체이닝으로 추가 작업을 이어갈 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 실제로 발생되기 전에 추가적인 로직을 수행하려면, `throw` 메서드에 클로저를 넘길 수 있습니다. 클로저 실행 이후 예외는 자동으로 발생하니, 클로저 내에서 직접 throw 할 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그 또는 리포트 시 120자로 잘립니다. 이 동작을 변경하거나 비활성화하려면, `bootstrap/app.php`에서 `truncateAt`, `dontTruncate`를 활용할 수 있습니다.

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // 예외 메시지를 240자로 잘라서 기록
    RequestException::truncateAt(240);

    // 메시지 자르기 비활성화
    RequestException::dontTruncate();
})
```

또는, 요청마다 예외 메시지 자르기 동작을 `truncateExceptionsAt`을 통해 지정할 수도 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### Guzzle 미들웨어 (Guzzle Middleware)

Laravel HTTP 클라이언트는 Guzzle 기반이기 때문에, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 활용해 요청 전/후로 데이터를 조작하거나 검사할 수 있습니다. 요청을 조작하려면 `withRequestMiddleware`로 미들웨어를 등록합니다.

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

마찬가지로, 응답을 검사하고 싶다면 `withResponseMiddleware`에 미들웨어를 등록합니다.

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
#### 전역 미들웨어 (Global Middleware)

모든 요청 및 응답에 적용되는 미들웨어를 등록하고 싶다면, `globalRequestMiddleware`, `globalResponseMiddleware`를 사용할 수 있습니다. 일반적으로, 이 메서드들은 `AppServiceProvider`의 `boot` 메서드 내에서 호출합니다.

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
### Guzzle 옵션 (Guzzle Options)

요청을 보낼 때 추가적인 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)이 필요하면, `withOptions` 메서드를 사용하세요. 이 메서드는 키-값 쌍의 배열을 받습니다.

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### 전역 옵션 (Global Options)

모든 요청에 기본 옵션을 적용하려면, `globalOptions` 메서드를 사용할 수 있습니다. 이 메서드는 일반적으로 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 즉, 각각의 요청을 연속적으로(순차적으로) 보내는 대신, 동시에 여러 요청을 발송하여 느린 HTTP API와 통신할 때 성능을 크게 개선할 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀링 (Request Pooling)

Laravel에서는 `pool` 메서드로 위 기능을 손쉽게 사용할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인수로 받으며, 이를 통해 요청 풀에 여러 요청을 추가할 수 있습니다.

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

각 응답 인스턴스는 풀에 추가한 순서대로 접근할 수 있습니다. `as` 메서드를 사용하면 요청마다 이름을 붙여, 응답도 이름으로 접근할 수 있습니다.

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

동시 처리되는 요청의 최대 개수는 `pool` 메서드의 `concurrency` 인수로 조절할 수 있습니다.

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 동시 요청 커스터마이즈

`pool` 메서드는 `withHeaders`, `middleware` 등 다른 HTTP 클라이언트 메서드와 체이닝할 수 없습니다. 풀에 포함된 각 요청마다 개별적으로 옵션을 지정해야 합니다.

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
### 요청 배치 (Request Batching)

동시 요청을 다루는 또 다른 방법으로 `batch` 메서드를 사용할 수 있습니다. `batch` 메서드는 `pool`과 마찬가지로 요청을 추가할 수 있을 뿐만 아니라, 요청 완료 시점마다 다양한 콜백을 정의할 수 있습니다.

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
    // 배치가 생성되었지만 아직 요청이 초기화되지 않은 상태
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // 개별 요청이 성공적으로 완료됨
})->then(function (Batch $batch, array $results) {
    // 모든 요청이 성공적으로 완료됨
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // 배치 요청 중 실패가 발생함
})->finally(function (Batch $batch, array $results) {
    // 모든 배치 작업이 끝남
})->send();
```

`pool` 메서드처럼 `as` 메서드를 사용해 각 요청에 이름을 부여할 수도 있습니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` 메서드를 호출해 배치가 시작되면, 더 이상 요청을 추가할 수 없습니다. 이후에 요청을 추가하면 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

배치의 최대 동시성은 `concurrency` 메서드로 지정할 수 있습니다. 이 값이 허용하는 만큼 배치가 동시에 처리됩니다.

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### 배치 정보 확인

Batch 완료 콜백에서 제공되는 `Illuminate\Http\Client\Batch` 인스턴스는 여러 프로퍼티와 메서드를 통해 배치 요청 상황을 확인할 수 있습니다.

```php
// 배치에 할당된 총 요청 수
$batch->totalRequests;
 
// 아직 처리되지 않은 요청 수
$batch->pendingRequests;
 
// 실패한 요청 수
$batch->failedRequests;

// 지금까지 처리된 요청 수
$batch->processedRequests();

// 배치 실행이 끝났는지 여부
$batch->finished();

// 배치 내에 실패가 있는지 여부
$batch->hasFailures();
```

<a name="deferring-batches"></a>
#### 배치 요청 지연 실행 (Deferring Batches)

`defer` 메서드를 호출하면, 요청 배치가 즉시 실행되지 않고, 현재 애플리케이션 HTTP 응답이 사용자에게 전송된 뒤에 실행됩니다. 이를 통해 애플리케이션의 반응속도를 빠르게 유지할 수 있습니다.

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // 모든 요청이 완료됨
})->defer();
```

<a name="macros"></a>
## 매크로 (Macros)

Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있습니다. 매크로는 특정 서비스와의 상호작용에서 자주 사용하는 요청 경로와 헤더를 일관적이고 직관적으로 설정하는 데 유용합니다. 매크로를 정의하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 작성하면 됩니다.

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

매크로를 설정한 뒤에는, 애플리케이션 어디서든 지정한 구성을 가진 pending 요청 객체를 생성할 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel의 많은 서비스들과 마찬가지로, HTTP 클라이언트도 쉽고 직관적인 테스트 작성을 지원합니다. `Http` 파사드의 `fake` 메서드를 사용하면, 모든 요청에 대해 예상되는(dummy) 응답을 돌려주도록 설정할 수 있습니다.

<a name="faking-responses"></a>
### 응답 페이크 (Faking Responses)

예를 들어, 모든 요청에 대해 비어있는 200 상태 응답을 반환하고 싶다면, 인수 없이 `fake`를 호출하면 됩니다.

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 특정 URL에 대한 페이크

`fake` 메서드에 배열을 전달할 수도 있는데, 배열의 키가 페이크할 URL 패턴이고, 값이 응답입니다. `*`는 와일드카드로 동작합니다. 페이크 응답을 만들 때는 `Http` 파사드의 `response` 메서드를 이용하세요.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 페이크 응답
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Google 엔드포인트에 대한 문자열 응답
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

지정된 URL로 지정되지 않은 요청은 실제 요청이 전송됩니다. 모든 미지정 URL에 대해 특정 값을 반환하고 싶다면, `*` 를 단일 패턴으로 사용합니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 JSON 페이크 응답
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // 기타 모든 엔드포인트에는 문자열 응답
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

문자열, 배열, 정수 등 간단한 형태로도 페이크 응답을 만들 수 있습니다.

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 예외 응답 페이크

HTTP 클라이언트가 요청을 보내다 `Illuminate\Http\Client\ConnectionException` 예외를 만나야 하는 경우, `failedConnection` 메서드를 이용해 예외를 발생시키는 테스트가 가능합니다.

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` 을 던져야 하는 경우, `failedRequest` 메서드를 사용할 수 있습니다.

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
#### 응답 시퀀스 페이크

하나의 URL이 순차적으로 여러 응답을 반환해야 하는 경우, `Http::sequence` 메서드를 사용해 응답들을 차례로 반환하도록 만들 수 있습니다.

```php
Http::fake([
    // GitHub 엔드포인트에 대해 일련의 응답 생성
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```

시퀀스의 모든 응답이 소진되면, 추가 요청시 예외가 발생합니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하려면, `whenEmpty` 메서드를 사용하세요.

```php
Http::fake([
    // GitHub 엔드포인트에 대한 응답 시퀀스
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```

특정 URL에 대한 패턴 없이 응답 시퀀스를 만들고 싶다면, `Http::fakeSequence`를 사용할 수 있습니다.

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### Fake 콜백

특정 엔드포인트에 대해 복잡한 조건으로 페이크 응답을 반환해야 한다면, `fake` 메서드에 클로저를 넘길 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 받아, 적절한 응답을 반환해야 합니다.

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### 요청 확인 (Inspecting Requests)

응답을 페이크하는 상황에서는, 실제 클라이언트가 올바른 데이터/헤더로 요청을 보냈는지 확인하고 싶을 때가 있습니다. 이는 `Http::fake` 호출 뒤 `Http::assertSent` 메서드로 확인할 수 있습니다.

`assertSent`는 클로저를 받아, 이 클로저에 전달되는 `Illuminate\Http\Client\Request` 인스턴스를 통해 기대하는 조건이 맞는지 검사할 수 있습니다. 하나 이상의 요청이 해당 조건에 부합하면 테스트는 통과합니다.

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

특정 요청이 보내지지 않았음을 확인할 때는 `assertNotSent` 메서드를 사용할 수 있습니다.

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

`assertSentCount`를 사용하면 테스트 동안 "보낸" 요청의 개수를 단언할 수 있습니다.

```php
Http::fake();

Http::assertSentCount(5);
```

또는, `assertNothingSent`로 어떤 요청도 보내지 않았음을 단언할 수 있습니다.

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### 요청/응답 기록 (Recording Requests / Responses)

`recorded` 메서드는 모든 요청과 그에 대응하는 응답을 수집합니다. 이 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response` 인스턴스를 담은 배열의 컬렉션을 반환합니다.

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

또한, `recorded` 메서드에 클로저를 넘겨 요청/응답 쌍을 원하는 조건에 따라 필터링할 수 있습니다.

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
### 임의의 요청 방지 (Preventing Stray Requests)

테스트나 전체 테스트 스위트 동안 HTTP 클라이언트를 통한 모든 요청이 페이크되었는지 보장하고 싶다면, `preventStrayRequests` 메서드를 사용할 수 있습니다. 이 메서드 호출 이후, 페이크 응답이 없는 요청은 실제 HTTP 요청을 보내지 않고 예외를 발생시킵니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// "ok" 응답이 반환됨
Http::get('https://github.com/laravel/framework');

// 예외 발생!
Http::get('https://laravel.com');
```

대부분의 임의 요청을 방지하면서, 특정 요청만 허용하고 싶다면 `allowStrayRequests`에 URL 패턴 배열을 넘길 수 있습니다. 지정된 패턴에 부합하는 요청은 가능하며, 그 외 요청은 예외가 발생합니다.

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// 이 요청은 실행됨
Http::get('http://127.0.0.1:5000/generate');

// 예외 발생!
Http::get('https://laravel.com');
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 HTTP 요청 전송 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에 발생하고, `ResponseReceived` 이벤트는 특정 요청에 대한 응답이 수신된 후에 발생합니다. 응답을 받지 못한 경우에는 `ConnectionFailed` 이벤트가 발생합니다.

`RequestSending`, `ConnectionFailed` 이벤트는 모두 요청 객체(`Illuminate\Http\Client\Request`)를 확인할 수 있는 public `$request` 속성이 있습니다. `ResponseReceived` 이벤트도 `$request` 속성 외에 응답 객체(`$response`)를 함께 제공합니다. 이 이벤트들에 대한 [이벤트 리스너](/docs/master/events)를 만들어 사용할 수 있습니다.

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * 이벤트를 처리합니다.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
