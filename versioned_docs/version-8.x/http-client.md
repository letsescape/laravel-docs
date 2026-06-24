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
    - [Guzzle Options](#guzzle-options)
- [Concurrent Requests](#concurrent-requests)
- [Macros](#macros)
- [Testing](#testing)
    - [Faking Responses](#faking-responses)
    - [Inspecting Requests](#inspecting-requests)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides an expressive, minimal API around the [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/), allowing you to quickly make outgoing HTTP requests to communicate with other web applications. Laravel's wrapper around Guzzle is focused on its most common use cases and a wonderful developer experience. -->
Laravel은 [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/) 위에 표현적이며 최소한의 API를 제공합니다. 이를 통해 다른 웹 애플리케이션과 통신할 때 빠르게 외부 HTTP 요청을 보낼 수 있습니다. Laravel의 Guzzle 래퍼는 가장 흔히 사용하는 기능들에 중점을 두고, 개발자 경험이 탁월하도록 설계되어 있습니다.

<!-- Before getting started, you should ensure that you have installed the Guzzle package as a dependency of your application. By default, Laravel automatically includes this dependency. However, if you have previously removed the package, you may install it again via Composer: -->
시작하기 전에, Guzzle 패키지가 애플리케이션의 의존성으로 설치되어 있는지 확인해야 합니다. 기본적으로 Laravel에는 이 의존성이 자동으로 포함되어 있습니다. 하지만 만약 이전에 이 패키지를 제거한 적이 있다면, 다음과 같이 Composer를 통해 다시 설치할 수 있습니다.

```
composer require guzzlehttp/guzzle
```

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make requests, you may use the `head`, `get`, `post`, `put`, `patch`, and `delete` methods provided by the `Http` facade. First, let's examine how to make a basic `GET` request to another URL: -->
요청을 보내려면 `Http` 파사드에서 제공하는 `head`, `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 먼저, 다른 URL에 기본적인 `GET` 요청을 보내는 방법을 살펴보겠습니다.

```
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

<!-- The `get` method returns an instance of `Illuminate\Http\Client\Response`, which provides a variety of methods that may be used to inspect the response: -->
`get` 메서드는 `Illuminate\Http\Client\Response` 인스턴스를 반환하며, 다음과 같은 다양한 메서드를 이용해 응답을 검사할 수 있습니다.

```
$response->body() : string;
$response->json($key = null) : array|mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->status() : int;
$response->ok() : bool;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->serverError() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```

<!-- The `Illuminate\Http\Client\Response` object also implements the PHP `ArrayAccess` interface, allowing you to access JSON response data directly on the response: -->
또한 `Illuminate\Http\Client\Response` 객체는 PHP의 `ArrayAccess` 인터페이스를 구현하므로, JSON 응답 데이터를 배열처럼 바로 접근할 수 있습니다.

```
return Http::get('http://example.com/users/1')['name'];
```

<a name="dumping-requests"></a>
<!-- #### Dumping Requests -->
#### Dumping Requests

<!-- If you would like to dump the outgoing request instance before it is sent and terminate the script's execution, you may add the `dd` method to the beginning of your request definition: -->
요청이 전송되기 전에 해당 요청 인스턴스를 덤프하고 스크립트 실행을 즉시 종료하고 싶다면, 요청 정의의 처음에 `dd` 메서드를 추가하면 됩니다.

```
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
<!-- ### Request Data -->
### Request Data

<!-- Of course, it is common when making `POST`, `PUT`, and `PATCH` requests to send additional data with your request, so these methods accept an array of data as their second argument. By default, data will be sent using the `application/json` content type: -->
`POST`, `PUT`, `PATCH` 요청 시에는 추가 데이터를 함께 보내는 경우가 많습니다. 이런 메서드들은 두 번째 인수로 데이터 배열을 받을 수 있습니다. 기본적으로, 데이터는 `application/json` 콘텐츠 타입으로 전송됩니다.

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
`GET` 요청을 할 때, 쿼리 문자열을 URL에 직접 추가하거나, `get` 메서드의 두 번째 인수로 키/값 쌍 배열을 전달할 수 있습니다.

```
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

<a name="sending-form-url-encoded-requests"></a>
<!-- #### Sending Form URL Encoded Requests -->
#### Sending Form URL Encoded Requests

<!-- If you would like to send data using the `application/x-www-form-urlencoded` content type, you should call the `asForm` method before making your request: -->
만약 `application/x-www-form-urlencoded` 콘텐츠 타입으로 데이터를 보내고 싶다면, 요청 전에 `asForm` 메서드를 호출해야 합니다.

```
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
<!-- #### Sending A Raw Request Body -->
#### Sending A Raw Request Body

<!-- You may use the `withBody` method if you would like to provide a raw request body when making a request. The content type may be provided via the method's second argument: -->
요청을 보낼 때 raw 데이터를 직접 주고 싶다면, `withBody` 메서드를 사용할 수 있습니다. 두 번째 인수로 콘텐츠 타입을 지정할 수 있습니다.

```
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
<!-- #### Multi-Part Requests -->
#### Multi-Part Requests

<!-- If you would like to send files as multi-part requests, you should call the `attach` method before making your request. This method accepts the name of the file and its contents. If needed, you may provide a third argument which will be considered the file's filename: -->
파일을 다중 파트 요청으로 보내야 할 경우, `attach` 메서드를 사용해야 합니다. 이 메서드는 파일의 이름과 내용을 받으며, 필요하다면 파일명을 세 번째 인수로 지정할 수 있습니다.

```
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg'
)->post('http://example.com/attachments');
```

<!-- Instead of passing the raw contents of a file, you may pass a stream resource: -->
파일의 raw 데이터를 전달하는 대신, 스트림 리소스를 전달하는 것도 가능합니다.

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
요청에 헤더를 추가하려면 `withHeaders` 메서드를 사용합니다. 이 `withHeaders` 메서드는 키/값 쌍의 배열을 받습니다.

```
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<!-- You may use the `accept` method to specify the content type that your application is expecting in response to your request: -->
응답에서 어떤 콘텐츠 타입을 기대할 것인지 지정하려면 `accept` 메서드를 사용할 수 있습니다.

```
$response = Http::accept('application/json')->get('http://example.com/users');
```

<!-- For convenience, you may use the `acceptJson` method to quickly specify that your application expects the `application/json` content type in response to your request: -->
간편하게 `application/json` 콘텐츠 타입을 기대한다고 지정하려면, `acceptJson` 메서드를 사용할 수 있습니다.

```
$response = Http::acceptJson()->get('http://example.com/users');
```

<a name="authentication"></a>
<!-- ### Authentication -->
### Authentication

<!-- You may specify basic and digest authentication credentials using the `withBasicAuth` and `withDigestAuth` methods, respectively: -->
Basic 인증과 Digest 인증을 각각 `withBasicAuth`, `withDigestAuth` 메서드를 사용해 지정할 수 있습니다.

```
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(...);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(...);
```

<a name="bearer-tokens"></a>
<!-- #### Bearer Tokens -->
#### Bearer Tokens

<!-- If you would like to quickly add a bearer token to the request's `Authorization` header, you may use the `withToken` method: -->
요청의 `Authorization` 헤더에 Bearer 토큰을 빠르게 추가하고 싶다면, `withToken` 메서드를 사용합니다.

```
$response = Http::withToken('token')->post(...);
```

<a name="timeout"></a>
<!-- ### Timeout -->
### Timeout

<!-- The `timeout` method may be used to specify the maximum number of seconds to wait for a response: -->
`timeout` 메서드를 통해 응답을 기다리는 최대 초(sec)를 지정할 수 있습니다.

```
$response = Http::timeout(3)->get(...);
```

<!-- If the given timeout is exceeded, an instance of `Illuminate\Http\Client\ConnectionException` will  be thrown. -->
만약 지정한 시간 내에 응답을 받지 못하면, `Illuminate\Http\Client\ConnectionException` 예외가 발생합니다.

<a name="retries"></a>
<!-- ### Retries -->
### Retries

<!-- If you would like HTTP client to automatically retry the request if a client or server error occurs, you may use the `retry` method. The `retry` method accepts the maximum number of times the request should be attempted and the number of milliseconds that Laravel should wait in between attempts: -->
클라이언트 오류나 서버 오류가 발생했을 때 HTTP 클라이언트가 자동으로 요청을 재시도하게 하려면, `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 요청을 시도할 최대 횟수와 요청 사이에 Laravel이 대기할 시간(밀리초 단위)을 각각 받습니다.

```
$response = Http::retry(3, 100)->post(...);
```

<!-- If needed, you may pass a third argument to the `retry` method. The third argument should be a callable that determines if the retries should actually be attempted. For example, you may wish to only retry the request if the initial request encounters an `ConnectionException`: -->
필요하다면, `retry` 메서드에 세 번째 인수로 콜러블을 전달할 수 있습니다. 세 번째 인수는 실제로 재시도를 할지 결정하는 콜백입니다. 예를 들어, 최초 요청에서 `ConnectionException`이 발생할 때만 재시도하도록 할 수 있습니다.

```
$response = Http::retry(3, 100, function ($exception) {
    return $exception instanceof ConnectionException;
})->post(...);
```

<!-- If all of the requests fail, an instance of `Illuminate\Http\Client\RequestException` will be thrown. -->
모든 시도가 실패한다면, `Illuminate\Http\Client\RequestException` 예외가 발생합니다.

<a name="error-handling"></a>
<!-- ### Error Handling -->
### Error Handling

<!-- Unlike Guzzle's default behavior, Laravel's HTTP client wrapper does not throw exceptions on client or server errors (`400` and `500` level responses from servers). You may determine if one of these errors was returned using the `successful`, `clientError`, or `serverError` methods: -->
Guzzle의 기본 동작과 달리, Laravel HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(서버에서 `400`, `500`번대 응답)에서 예외를 발생시키지 않습니다. `successful`, `clientError`, `serverError` 메서드를 사용해 이러한 오류가 발생했는지 확인할 수 있습니다.

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
응답 인스턴스가 있고, 상태 코드가 클라이언트 또는 서버 오류임을 나타낸다면 `Illuminate\Http\Client\RequestException` 예외를 발생시키도록 `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다.

```
$response = Http::post(...);

// Throw an exception if a client or server error occurred...
$response->throw();

// Throw an exception if an error occurred and the given condition is true...
$response->throwIf($condition);

return $response['user']['id'];
```

<!-- The `Illuminate\Http\Client\RequestException` instance has a public `$response` property which will allow you to inspect the returned response. -->
`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있도록 public `$response` 속성이 있습니다.

<!-- The `throw` method returns the response instance if no error occurred, allowing you to chain other operations onto the `throw` method: -->
`throw` 메서드는 오류가 없으면 응답 인스턴스를 반환하므로, `throw` 이후에 다른 메서드를 체이닝할 수 있습니다.

```
return Http::post(...)->throw()->json();
```

<!-- If you would like to perform some additional logic before the exception is thrown, you may pass a closure to the `throw` method. The exception will be thrown automatically after the closure is invoked, so you do not need to re-throw the exception from within the closure: -->
예외가 발생하기 전에 추가적인 로직을 실행하고 싶다면, 클로저를 `throw` 메서드에 전달할 수 있습니다. 이 경우, 클로저 실행 후 예외가 자동으로 발생하기 때문에 직접 예외를 다시 던질 필요는 없습니다.

```
return Http::post(...)->throw(function ($response, $e) {
    //
})->json();
```

<a name="guzzle-options"></a>
<!-- ### Guzzle Options -->
### Guzzle Options

<!-- You may specify additional [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html) using the `withOptions` method. The `withOptions` method accepts an array of key / value pairs: -->
추가적인 [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html)이 필요할 경우, `withOptions` 메서드를 사용하면 됩니다. 이 `withOptions` 메서드는 키/값 쌍의 배열을 받습니다.

```
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="concurrent-requests"></a>
<!-- ## Concurrent Requests -->
## Concurrent Requests

<!-- Sometimes, you may wish to make multiple HTTP requests concurrently. In other words, you want several requests to be dispatched at the same time instead of issuing the requests sequentially. This can lead to substantial performance improvements when interacting with slow HTTP APIs. -->
여러 개의 HTTP 요청을 동시에 보내야 할 때가 있습니다. 즉, 여러 요청을 순차적으로 처리하는 대신 한 번에 동시에 보냅니다. 이를 통해 반응이 느린 HTTP API와 통신할 때 성능이 크게 개선될 수 있습니다.

<!-- Thankfully, you may accomplish this using the `pool` method. The `pool` method accepts a closure which receives an `Illuminate\Http\Client\Pool` instance, allowing you to easily add requests to the request pool for dispatching: -->
이럴 때는 `pool` 메서드를 사용하면 됩니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 인수로 받으며, 여기에 요청들을 추가해 한 번에 보낼 수 있습니다.

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
각 응답 인스턴스는 풀에 추가된 순서대로 접근할 수 있습니다. 또한 `as` 메서드를 사용해 요청에 이름을 붙이고, 그 이름으로 응답을 조회할 수도 있습니다.

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

<a name="macros"></a>
<!-- ## Macros -->
## Macros

<!-- The Laravel HTTP client allows you to define "macros", which can serve as a fluent, expressive mechanism to configure common request paths and headers when interacting with services throughout your application. To get started, you may define the macro within the `boot` method of your application's `App\Providers\AppServiceProvider` class: -->
Laravel HTTP 클라이언트는 "매크로"를 정의할 수 있게 하여, 서비스와 상호작용할 때 자주 사용하는 요청 경로와 헤더를 손쉽게 구성할 수 있도록 지원합니다. 먼저, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에 매크로를 정의하세요.

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```

<!-- Once your macro has been configured, you may invoke it from anywhere in your application to create a pending request with the specified configuration: -->
매크로 설정을 완료했다면, 애플리케이션 어디에서든 지정한 설정으로 대기 중인(pending) 요청을 다음과 같이 만들 수 있습니다.

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's HTTP wrapper is no exception. The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made. -->
Laravel의 다양한 서비스들은 테스트 작성을 보다 쉽고 표현적으로 할 수 있게 도와주는 기능을 제공합니다. HTTP 래퍼 역시 예외는 아닙니다. `Http` 파사드의 `fake` 메서드를 이용하면, 요청 시 미리 준비된(stub) 또는 더미(dummmy) 응답을 반환하도록 지정할 수 있습니다.

<a name="faking-responses"></a>
<!-- ### Faking Responses -->
### Faking Responses

<!-- For example, to instruct the HTTP client to return empty, `200` status code responses for every request, you may call the `fake` method with no arguments: -->
예를 들어, HTTP 클라이언트가 모든 요청마다 비어 있는 `200` 상태 코드 응답을 반환하도록 하려면, `fake` 메서드에 인수를 주지 않고 호출하면 됩니다.

```
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(...);
```

> [!NOTE]
> 요청을 가짜로 만들면, HTTP 클라이언트의 미들웨어는 실행되지 않습니다. 가짜 응답에 대한 기대값을 정의할 때 이 미들웨어들이 정상적으로 동작했다고 가정하여 테스트를 작성해야 합니다.

<a name="faking-specific-urls"></a>
<!-- #### Faking Specific URLs -->
#### Faking Specific URLs

<!-- Alternatively, you may pass an array to the `fake` method. The array's keys should represent URL patterns that you wish to fake and their associated responses. The `*` character may be used as a wildcard character. Any requests made to URLs that have not been faked will actually be executed. You may use the `Http` facade's `response` method to construct stub / fake responses for these endpoints: -->
또는, `fake` 메서드에 배열을 전달할 수도 있습니다. 이 배열의 키는 가짜로 만들고자 하는 URL 패턴이고, 값은 해당 응답입니다. `*` 문자를 와일드카드로 사용할 수 있습니다. 가짜로 지정되지 않은 URL로의 요청은 실제로 실행됩니다. 이런 엔드포인트용 가짜 응답을 만들려면, `Http` 파사드의 `response` 메서드를 사용할 수 있습니다.

```
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

<!-- If you would like to specify a fallback URL pattern that will stub all unmatched URLs, you may use a single `*` character: -->
모든 매칭되지 않은 URL을 위한 fallback URL 패턴을 지정하고 싶다면, 단일 `*` 문자를 사용할 수 있습니다.

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
특정 URL에서 여러 개의 가짜 응답을 순서대로 반환해야 할 때가 있습니다. 이럴 때는 `Http::sequence` 메서드로 응답 시퀀스를 만들 수 있습니다.

```
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
                            ->push('Hello World', 200)
                            ->push(['foo' => 'bar'], 200)
                            ->pushStatus(404),
]);
```

<!-- When all of the responses in a response sequence have been consumed, any further requests will cause the response sequence to throw an exception. If you would like to specify a default response that should be returned when a sequence is empty, you may use the `whenEmpty` method: -->
시퀀스의 모든 응답이 소진되면, 그 이후의 요청은 예외를 발생시킵니다. 시퀀스가 비었을 때 반환할 기본 응답을 지정하고 싶다면, `whenEmpty` 메서드를 사용할 수 있습니다.

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
만약 특정 URL 패턴이 필요 없고, 단순히 응답 시퀀스만 가짜로 만들고 싶다면, `Http::fakeSequence` 메서드를 사용할 수 있습니다.

```
Http::fakeSequence()
        ->push('Hello World', 200)
        ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
<!-- #### Fake Callback -->
#### Fake Callback

<!-- If you require more complicated logic to determine what responses to return for certain endpoints, you may pass a closure to the `fake` method. This closure will receive an instance of `Illuminate\Http\Client\Request` and should return a response instance. Within your closure, you may perform whatever logic is necessary to determine what type of response to return: -->
특정 엔드포인트에 대해 반환할 응답을 동적으로 결정해야 하는 더 복잡한 로직이 필요하다면, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인수로 받고, 응답 인스턴스를 반환해야 합니다. 클로저 내부에서 원하는 모든 로직을 실행할 수 있습니다.

```
Http::fake(function ($request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
<!-- ### Inspecting Requests -->
### Inspecting Requests

<!-- When faking responses, you may occasionally wish to inspect the requests the client receives in order to make sure your application is sending the correct data or headers. You may accomplish this by calling the `Http::assertSent` method after calling `Http::fake`. -->
가짜 응답을 만드는 도중, 클라이언트가 받은 요청을 검사해 애플리케이션이 올바른 데이터 또는 헤더를 보내는지 확인하고 싶을 수 있습니다. 이를 위해 `Http::fake` 호출 이후 `Http::assertSent` 메서드를 사용할 수 있습니다.

<!-- The `assertSent` method accepts a closure which will receive an `Illuminate\Http\Client\Request` instance and should return a boolean value indicating if the request matches your expectations. In order for the test to pass, at least one request must have been issued matching the given expectations: -->
`assertSent` 메서드는 클로저를 받으며, 이 클로저는 `Illuminate\Http\Client\Request` 인스턴스를 인수로 받고, 요청이 기대에 부합하면 true를 반환하면 됩니다. 적어도 하나의 요청이 기대에 맞으면 테스트가 통과합니다.

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
특정 요청이 전송되지 않았음을 확인하려면 `assertNotSent` 메서드를 사용할 수 있습니다.

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
테스트 도중 "전송된" 요청 횟수를 검증하려면, `assertSentCount` 메서드를 사용할 수 있습니다.

```
Http::fake();

Http::assertSentCount(5);
```

<!-- Or, you may use the `assertNothingSent` method to assert that no requests were sent during the test: -->
혹은, 테스트 중 단 하나의 요청도 전송되지 않았는지 확인하려면, `assertNothingSent` 메서드를 사용합니다.

```
Http::fake();

Http::assertNothingSent();
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel fires three events during the process of sending HTTP requests. The `RequestSending` event is fired prior to a request being sent, while the `ResponseReceived` event is fired after a response is received for a given request. The `ConnectionFailed` event is fired if no response is received for a given request. -->
Laravel은 HTTP 요청 전송 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에 발생하고, `ResponseReceived` 이벤트는 주어진 요청에 대한 응답을 받은 후 발생합니다. 요청에 응답을 받지 못할 경우에는 `ConnectionFailed` 이벤트가 발생합니다.

<!-- The `RequestSending` and `ConnectionFailed` events both contain a public `$request` property that you may use to inspect the `Illuminate\Http\Client\Request` instance. Likewise, the `ResponseReceived` event contains a `$request` property as well as a `$response` property which may be used to inspect the `Illuminate\Http\Client\Response` instance. You may register event listeners for this event in your `App\Providers\EventServiceProvider` service provider: -->
`RequestSending`과 `ConnectionFailed` 이벤트 모두 `Illuminate\Http\Client\Request` 인스턴스를 검사할 수 있도록 public `$request` 속성을 포함합니다. `ResponseReceived` 이벤트는 `$request`뿐만 아니라 `$response` 속성도 포함하여, `Illuminate\Http\Client\Response` 인스턴스를 검사할 수 있습니다. 이 이벤트에 대한 리스터는 애플리케이션의 `App\Providers\EventServiceProvider` 서비스 프로바이더에서 등록할 수 있습니다.

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
