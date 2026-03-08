# HTTP 클라이언트 (HTTP Client)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 데이터](#request-data)
    - [헤더](#headers)
    - [인증](#authentication)
    - [타임아웃](#timeout)
    - [재시도](#retries)
    - [에러 처리](#error-handling)
    - [Guzzle Middleware](#guzzle-middleware)
    - [Guzzle 옵션](#guzzle-options)
- [동시 요청](#concurrent-requests)
    - [요청 풀링](#request-pooling)
    - [요청 배치](#request-batching)
- [매크로](#macros)
- [테스트](#testing)
    - [응답 가짜 처리](#faking-responses)
    - [요청 검사](#inspecting-requests)
    - [의도치 않은 요청 방지](#preventing-stray-requests)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/) 위에 표현력이 뛰어나고 간결한 API를 제공하여, 다른 웹 애플리케이션과 통신하기 위한 HTTP 요청을 빠르게 보낼 수 있도록 합니다.  

Laravel의 Guzzle 래퍼(wrapper)는 가장 일반적인 사용 사례에 초점을 맞추고 있으며, 뛰어난 개발자 경험을 제공하도록 설계되었습니다.

<a name="making-requests"></a>
## 요청 보내기 (Making Requests)

HTTP 요청을 보내려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다.  

먼저 다른 URL에 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환합니다. 이 객체는 응답을 검사할 수 있는 다양한 메서드를 제공합니다.

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

`Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스도 구현하고 있으므로 JSON 응답 데이터를 배열처럼 직접 접근할 수 있습니다.

```php
return Http::get('http://example.com/users/1')['name'];
```

위에 나열된 메서드 외에도, 다음 메서드를 사용하여 응답이 특정 상태 코드인지 확인할 수 있습니다.

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

HTTP 클라이언트는 [URI template specification](https://www.rfc-editor.org/rfc/rfc6570)을 사용하여 요청 URL을 구성할 수도 있습니다.  

URI 템플릿에서 확장될 URL 파라미터를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다.

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### 요청 덤프 (Dumping Requests)

요청이 전송되기 전에 요청 인스턴스를 출력하고 스크립트 실행을 종료하려면 요청 정의의 시작 부분에 `dd` 메서드를 추가할 수 있습니다.

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### 요청 데이터 (Request Data)

일반적으로 `POST`, `PUT`, `PATCH` 요청을 보낼 때 추가 데이터를 함께 보내는 경우가 많습니다. 이러한 메서드는 두 번째 인수로 데이터 배열을 받을 수 있습니다.  

기본적으로 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 파라미터

`GET` 요청을 보낼 때 URL에 직접 쿼리 문자열을 추가하거나 `get` 메서드의 두 번째 인수로 key/value 배열을 전달할 수 있습니다.

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
#### Form URL Encoded 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내려면 요청 전에 `asForm` 메서드를 호출해야 합니다.

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### Raw 요청 본문 보내기

요청 시 raw body 데이터를 보내려면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 타입은 두 번째 인수로 지정할 수 있습니다.

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### Multi-Part 요청

파일을 multi-part 형식으로 보내려면 요청 전에 `attach` 메서드를 호출해야 합니다.  

이 메서드는 파일의 이름과 내용(contents)을 인수로 받습니다. 필요하다면 세 번째 인수로 파일 이름을 지정할 수 있으며, 네 번째 인수로 파일에 대한 헤더를 설정할 수 있습니다.

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

파일의 raw 내용을 전달하는 대신 stream 리소스를 전달할 수도 있습니다.

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### 헤더 (Headers)

`withHeaders` 메서드를 사용하여 요청에 헤더를 추가할 수 있습니다. 이 메서드는 key/value 쌍 배열을 인수로 받습니다.

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` 메서드를 사용하면 요청에 대한 응답으로 애플리케이션이 기대하는 콘텐츠 타입을 지정할 수 있습니다.

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

편의를 위해 `acceptJson` 메서드를 사용하면 응답 콘텐츠 타입이 `application/json`임을 빠르게 지정할 수 있습니다.

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

`withHeaders` 메서드는 기존 헤더에 새 헤더를 병합합니다. 모든 헤더를 완전히 교체하려면 `replaceHeaders` 메서드를 사용할 수 있습니다.

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

`withBasicAuth`와 `withDigestAuth` 메서드를 사용하여 각각 Basic 인증과 Digest 인증 자격 증명을 지정할 수 있습니다.

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

#### Bearer 토큰

요청의 `Authorization` 헤더에 Bearer 토큰을 빠르게 추가하려면 `withToken` 메서드를 사용할 수 있습니다.

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### 타임아웃 (Timeout)

`timeout` 메서드를 사용하여 응답을 기다리는 최대 시간을 초 단위로 지정할 수 있습니다. 기본값은 30초입니다.

```php
$response = Http::timeout(3)->get(/* ... */);
```

지정한 시간이 초과되면 `Illuminate\Http\Client\ConnectionException` 인스턴스가 발생합니다.

서버에 연결을 시도하는 동안 기다리는 최대 시간을 지정하려면 `connectTimeout` 메서드를 사용할 수 있습니다. 기본값은 10초입니다.

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 재시도 (Retries)

클라이언트 또는 서버 오류가 발생했을 때 자동으로 요청을 재시도하려면 `retry` 메서드를 사용할 수 있습니다.  

`retry` 메서드는 최대 시도 횟수와 각 시도 사이에 Laravel이 대기할 밀리초(ms)를 인수로 받습니다.

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

재시도 사이의 대기 시간을 직접 계산하려면 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

편의를 위해 첫 번째 인수로 배열을 전달할 수도 있습니다. 이 배열은 각 재시도 사이에 대기할 밀리초 값을 나타냅니다.

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

필요하다면 세 번째 인수로 콜러블(callable)을 전달하여 실제로 재시도를 수행할지 여부를 결정할 수 있습니다. 예를 들어 초기 요청에서 `ConnectionException`이 발생한 경우에만 재시도하도록 설정할 수 있습니다.

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

요청이 실패했을 때 다음 시도를 하기 전에 요청을 수정할 수도 있습니다. 이를 위해 `retry` 메서드의 콜러블에서 전달받은 `$request` 인수를 수정하면 됩니다.  

예를 들어 첫 번째 요청이 인증 오류를 반환했을 경우 새로운 토큰으로 재시도할 수 있습니다.

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

모든 요청이 실패하면 `Illuminate\Http\Client\RequestException` 인스턴스가 발생합니다.  

이 동작을 비활성화하려면 `throw` 인수를 `false`로 설정할 수 있습니다. 이 경우 모든 재시도가 끝난 뒤 마지막 응답이 반환됩니다.

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 모든 요청이 연결 문제로 실패한 경우 `throw` 인수를 `false`로 설정했더라도 `Illuminate\Http\Client\ConnectionException`이 여전히 발생합니다.

<a name="error-handling"></a>
### 에러 처리 (Error Handling)

Guzzle의 기본 동작과 달리 Laravel의 HTTP 클라이언트는 클라이언트 오류나 서버 오류(`400`, `500`대 응답)에 대해 자동으로 예외를 발생시키지 않습니다.  

다음 메서드를 사용하여 오류 여부를 확인할 수 있습니다.

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

#### 예외 발생시키기

응답 상태 코드가 클라이언트 오류나 서버 오류일 때 `Illuminate\Http\Client\RequestException`을 발생시키려면 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

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

`Illuminate\Http\Client\RequestException` 인스턴스에는 `$response`라는 public 속성이 있어 반환된 응답을 확인할 수 있습니다.

`throw` 메서드는 오류가 없을 경우 응답 인스턴스를 반환하므로 다른 메서드와 체이닝할 수 있습니다.

```php
return Http::post(/* ... */)->throw()->json();
```

예외가 발생하기 전에 추가 로직을 실행하려면 `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저 실행 후 예외는 자동으로 발생하므로 클로저 내부에서 다시 던질 필요는 없습니다.

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

기본적으로 `RequestException` 메시지는 로그나 리포트에 기록될 때 120자로 잘립니다. 이 동작을 변경하거나 비활성화하려면 `bootstrap/app.php` 파일에서 `truncateAt` 또는 `dontTruncate` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // Truncate request exception messages to 240 characters...
    RequestException::truncateAt(240);

    // Disable request exception message truncation...
    RequestException::dontTruncate();
})
```

요청별로 예외 메시지 길이를 설정하려면 `truncateExceptionsAt` 메서드를 사용할 수 있습니다.

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```