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
Laravel は、[Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/) を中心とした表現力豊かな最小限の API を提供し、他の Web アプリケーションと通信するための送信 HTTP リクエストを迅速に作成できるようにします。 Laravel の Guzzle のラッパーは、最も一般的なユースケースと素晴らしい開発者エクスペリエンスに重点を置いています。

<!-- Before getting started, you should ensure that you have installed the Guzzle package as a dependency of your application. By default, Laravel automatically includes this dependency. However, if you have previously removed the package, you may install it again via Composer: -->
開始する前に、アプリケーションの依存関係として Guzzle パッケージがインストールされていることを確認する必要があります。デフォルトでは、Laravel にはこの依存関係が自動的に組み込まれます。ただし、以前にパッケージを削除したことがある場合は、Composer 経由で再度インストールできます。

```
composer require guzzlehttp/guzzle
```

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make requests, you may use the `head`, `get`, `post`, `put`, `patch`, and `delete` methods provided by the `Http` facade. First, let's examine how to make a basic `GET` request to another URL: -->
リクエストを行うには、`Http` ファサードによって提供される `head`、`get`、`post`、`put`、`patch`、および `delete` メソッドを使用できます。まず、別の URL に対して基本的な `GET` リクエストを行う方法を調べてみましょう。

```
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

<!-- The `get` method returns an instance of `Illuminate\Http\Client\Response`, which provides a variety of methods that may be used to inspect the response: -->
`get` メソッドは、応答の検査に使用できるさまざまなメソッドを提供する `Illuminate\Http\Client\Response` のインスタンスを返します。

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
`Illuminate\Http\Client\Response` オブジェクトは PHP `ArrayAccess` インターフェイスも実装しているため、応答上で JSON 応答データに直接アクセスできます。

```
return Http::get('http://example.com/users/1')['name'];
```

<a name="dumping-requests"></a>
<!-- #### Dumping Requests -->
#### Dumping Requests

<!-- If you would like to dump the outgoing request instance before it is sent and terminate the script's execution, you may add the `dd` method to the beginning of your request definition: -->
発信リクエストのインスタンスが送信される前にダンプしてスクリプトの実行を終了したい場合は、リクエスト定義の先頭に `dd` メソッドを追加します。

```
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
<!-- ### Request Data -->
### Request Data

<!-- Of course, it is common when making `POST`, `PUT`, and `PATCH` requests to send additional data with your request, so these methods accept an array of data as their second argument. By default, data will be sent using the `application/json` content type: -->
もちろん、`POST`、`PUT`、および `PATCH` リクエストを作成するときは、リクエストとともに追加データを送信するのが一般的であるため、これらのメソッドは 2 番目の引数としてデータの配列を受け入れます。デフォルトでは、データは `application/json` コンテンツ タイプを使用して送信されます。

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
`GET` リクエストを行うときは、クエリ文字列を URL に直接追加するか、キーと値のペアの配列を 2 番目の引数として `get` メソッドに渡すことができます。

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
`application/x-www-form-urlencoded` コンテンツ タイプを使用してデータを送信したい場合は、リクエストを行う前に `asForm` メソッドを呼び出す必要があります。

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
リクエストを行うときに生のリクエスト本文を提供したい場合は、`withBody` メソッドを使用できます。コンテンツ タイプは、メソッドの 2 番目の引数を介して指定できます。

```
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
<!-- #### Multi-Part Requests -->
#### Multi-Part Requests

<!-- If you would like to send files as multi-part requests, you should call the `attach` method before making your request. This method accepts the name of the file and its contents. If needed, you may provide a third argument which will be considered the file's filename: -->
ファイルをマルチパートリクエストとして送信したい場合は、リクエストを行う前に `attach` メソッドを呼び出す必要があります。このメソッドは、ファイルの名前とその内容を受け入れます。必要に応じて、ファイルのファイル名とみなされる 3 番目の引数を指定できます。

```
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg'
)->post('http://example.com/attachments');
```

<!-- Instead of passing the raw contents of a file, you may pass a stream resource: -->
ファイルの生のコンテンツを渡す代わりに、ストリーム リソースを渡すこともできます。

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
ヘッダーは、`withHeaders` メソッドを使用してリクエストに追加できます。この `withHeaders` メソッドは、キーと値のペアの配列を受け入れます。

```
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<!-- You may use the `accept` method to specify the content type that your application is expecting in response to your request: -->
`accept` メソッドを使用して、アプリケーションがリクエストに応じて期待するコンテンツ タイプを指定できます。

```
$response = Http::accept('application/json')->get('http://example.com/users');
```

<!-- For convenience, you may use the `acceptJson` method to quickly specify that your application expects the `application/json` content type in response to your request: -->
便宜上、`acceptJson` メソッドを使用して、アプリケーションがリクエストに応じて `application/json` コンテンツ タイプを予期していることをすばやく指定できます。

```
$response = Http::acceptJson()->get('http://example.com/users');
```

<a name="authentication"></a>
<!-- ### Authentication -->
### Authentication

<!-- You may specify basic and digest authentication credentials using the `withBasicAuth` and `withDigestAuth` methods, respectively: -->
基本認証資格情報とダイジェスト認証資格情報は、それぞれ `withBasicAuth` メソッドと `withDigestAuth` メソッドを使用して指定できます。

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
リクエストの `Authorization` ヘッダーにベアラー トークンをすぐに追加したい場合は、`withToken` メソッドを使用できます。

```
$response = Http::withToken('token')->post(...);
```

<a name="timeout"></a>
<!-- ### Timeout -->
### Timeout

<!-- The `timeout` method may be used to specify the maximum number of seconds to wait for a response: -->
`timeout` メソッドを使用して、応答を待機する最大秒数を指定できます。

```
$response = Http::timeout(3)->get(...);
```

<!-- If the given timeout is exceeded, an instance of `Illuminate\Http\Client\ConnectionException` will  be thrown. -->
指定されたタイムアウトを超えると、`Illuminate\Http\Client\ConnectionException` のインスタンスがスローされます。

<a name="retries"></a>
<!-- ### Retries -->
### Retries

<!-- If you would like HTTP client to automatically retry the request if a client or server error occurs, you may use the `retry` method. The `retry` method accepts the maximum number of times the request should be attempted and the number of milliseconds that Laravel should wait in between attempts: -->
クライアントまたはサーバーのエラーが発生した場合に HTTP クライアントがリクエストを自動的に再試行するようにしたい場合は、`retry` メソッドを使用できます。 `retry` メソッドは、リクエストを試行する最大回数と、Laravel が試行の間に待機するミリ秒数を受け入れます。

```
$response = Http::retry(3, 100)->post(...);
```

<!-- If needed, you may pass a third argument to the `retry` method. The third argument should be a callable that determines if the retries should actually be attempted. For example, you may wish to only retry the request if the initial request encounters an `ConnectionException`: -->
必要に応じて、`retry` メソッドに 3 番目の引数を渡すことができます。 3 番目の引数は、実際に再試行するかどうかを決定する呼び出し可能引数である必要があります。たとえば、最初のリクエストで `ConnectionException` が発生した場合にのみリクエストを再試行したい場合があります。

```
$response = Http::retry(3, 100, function ($exception) {
    return $exception instanceof ConnectionException;
})->post(...);
```

<!-- If all of the requests fail, an instance of `Illuminate\Http\Client\RequestException` will be thrown. -->
すべてのリクエストが失敗した場合、`Illuminate\Http\Client\RequestException` のインスタンスがスローされます。

<a name="error-handling"></a>
<!-- ### Error Handling -->
### Error Handling

<!-- Unlike Guzzle's default behavior, Laravel's HTTP client wrapper does not throw exceptions on client or server errors (`400` and `500` level responses from servers). You may determine if one of these errors was returned using the `successful`, `clientError`, or `serverError` methods: -->
Guzzle のデフォルトの動作とは異なり、Laravel の HTTP クライアント ラッパーは、クライアントまたはサーバーのエラー (サーバーからの `400` および `500` レベルの応答) で例外をスローしません。 `successful`、`clientError`、または `serverError` メソッドを使用して、これらのエラーのいずれかが返されたかどうかを確認できます。

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
応答インスタンスがあり、応答ステータス コードがクライアント エラーまたはサーバー エラーを示している場合に `Illuminate\Http\Client\RequestException` のインスタンスをスローしたい場合は、`throw` メソッドまたは `throwIf` メソッドを使用できます。

```
$response = Http::post(...);

// Throw an exception if a client or server error occurred...
$response->throw();

// Throw an exception if an error occurred and the given condition is true...
$response->throwIf($condition);

return $response['user']['id'];
```

<!-- The `Illuminate\Http\Client\RequestException` instance has a public `$response` property which will allow you to inspect the returned response. -->
`Illuminate\Http\Client\RequestException` インスタンスには、返された応答を検査できるパブリック `$response` プロパティがあります。

<!-- The `throw` method returns the response instance if no error occurred, allowing you to chain other operations onto the `throw` method: -->
`throw` メソッドは、エラーが発生しなかった場合に応答インスタンスを返し、他の操作を `throw` メソッドに連鎖させることができます。

```
return Http::post(...)->throw()->json();
```

<!-- If you would like to perform some additional logic before the exception is thrown, you may pass a closure to the `throw` method. The exception will be thrown automatically after the closure is invoked, so you do not need to re-throw the exception from within the closure: -->
例外がスローされる前に追加のロジックを実行したい場合は、`throw` メソッドにクロージャを渡すことができます。例外はクロージャが呼び出された後に自動的にスローされるため、クロージャ内から例外を再スローする必要はありません。

```
return Http::post(...)->throw(function ($response, $e) {
    //
})->json();
```

<a name="guzzle-options"></a>
<!-- ### Guzzle Options -->
### Guzzle Options

<!-- You may specify additional [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html) using the `withOptions` method. The `withOptions` method accepts an array of key / value pairs: -->
`withOptions` メソッドを使用して、追加の [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html) を指定できます。 `withOptions` メソッドは、キーと値のペアの配列を受け入れます。

```
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="concurrent-requests"></a>
<!-- ## Concurrent Requests -->
## Concurrent Requests

<!-- Sometimes, you may wish to make multiple HTTP requests concurrently. In other words, you want several requests to be dispatched at the same time instead of issuing the requests sequentially. This can lead to substantial performance improvements when interacting with slow HTTP APIs. -->
場合によっては、複数の HTTP リクエストを同時に実行したい場合があります。つまり、複数のリクエストを順番に発行するのではなく、同時にディスパッチする必要があります。これにより、遅い HTTP API を操作する際のパフォーマンスが大幅に向上する可能性があります。

<!-- Thankfully, you may accomplish this using the `pool` method. The `pool` method accepts a closure which receives an `Illuminate\Http\Client\Pool` instance, allowing you to easily add requests to the request pool for dispatching: -->
ありがたいことに、`pool` メソッドを使用してこれを実現できます。 `pool` メソッドは、`Illuminate\Http\Client\Pool` インスタンスを受け取るクロージャーを受け入れるため、ディスパッチするリクエストをリクエスト プールに簡単に追加できます。

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
ご覧のとおり、各応答インスタンスは、プールに追加された順序に基づいてアクセスできます。必要に応じて、`as` メソッドを使用してリクエストに名前を付けることができます。これにより、対応するレスポンスに名前でアクセスできるようになります。

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
Laravel HTTP クライアントを使用すると、アプリケーション全体でサービスと対話するときに共通のリクエスト パスとヘッダーを構成するための流暢で表現力豊かなメカニズムとして機能する「マクロ」を定義できます。まず、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッド内でマクロを定義します。

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
マクロを構成したら、アプリケーション内のどこからでもマクロを呼び出して、指定された構成で保留中のリクエストを作成できます。

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's HTTP wrapper is no exception. The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made. -->
多くの Laravel サービスは、テストを簡単かつ表現力豊かに作成できるようにする機能を提供しており、Laravel の HTTP ラッパーも例外ではありません。 `Http` ファサードの `fake` メソッドを使用すると、リクエストが行われたときにスタブ/ダミー応答を返すように HTTP クライアントに指示できます。

<a name="faking-responses"></a>
<!-- ### Faking Responses -->
### Faking Responses

<!-- For example, to instruct the HTTP client to return empty, `200` status code responses for every request, you may call the `fake` method with no arguments: -->
たとえば、すべてのリクエストに対して空の `200` ステータス コード応答を返すように HTTP クライアントに指示するには、引数なしで `fake` メソッドを呼び出すことができます。

```
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(...);
```

> [!NOTE]
> リクエストを偽装する場合、HTTP クライアント ミドルウェアは実行されません。これらのミドルウェアが正しく実行されているかのように、偽の応答に対する期待値を定義する必要があります。

<a name="faking-specific-urls"></a>
<!-- #### Faking Specific URLs -->
#### Faking Specific URLs

<!-- Alternatively, you may pass an array to the `fake` method. The array's keys should represent URL patterns that you wish to fake and their associated responses. The `*` character may be used as a wildcard character. Any requests made to URLs that have not been faked will actually be executed. You may use the `Http` facade's `response` method to construct stub / fake responses for these endpoints: -->
あるいは、配列を `fake` メソッドに渡すこともできます。配列のキーは、偽装したい URL パターンとそれに関連する応答を表す必要があります。 `*` 文字はワイルドカード文字として使用できます。偽装されていない URL に対して行われたリクエストはすべて実際に実行されます。 `Http` ファサードの `response` メソッドを使用して、次のエンドポイントのスタブ/偽の応答を構築できます。

```
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

<!-- If you would like to specify a fallback URL pattern that will stub all unmatched URLs, you may use a single `*` character: -->
一致しない URL をすべてスタブするフォールバック URL パターンを指定したい場合は、単一の `*` 文字を使用できます。

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
場合によっては、単一の URL が特定の順序で一連の偽の応答を返すように指定する必要がある場合があります。これは、`Http::sequence` メソッドを使用して応答を構築することで実現できます。

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
応答シーケンス内のすべての応答が消費されると、それ以上の要求によって応答シーケンスが例外をスローします。シーケンスが空の場合に返されるデフォルトの応答を指定したい場合は、`whenEmpty` メソッドを使用できます。

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
一連の応答を偽装したいが、偽装する特定の URL パターンを指定する必要がない場合は、`Http::fakeSequence` メソッドを使用できます。

```
Http::fakeSequence()
        ->push('Hello World', 200)
        ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
<!-- #### Fake Callback -->
#### Fake Callback

<!-- If you require more complicated logic to determine what responses to return for certain endpoints, you may pass a closure to the `fake` method. This closure will receive an instance of `Illuminate\Http\Client\Request` and should return a response instance. Within your closure, you may perform whatever logic is necessary to determine what type of response to return: -->
特定のエンドポイントに対してどのような応答を返すかを決定するために、より複雑なロジックが必要な場合は、`fake` メソッドにクロージャを渡すことができます。このクロージャは `Illuminate\Http\Client\Request` のインスタンスを受け取り、応答インスタンスを返す必要があります。クロージャ内では、返す応答の種類を決定するために必要なロジックを実行できます。

```
Http::fake(function ($request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
<!-- ### Inspecting Requests -->
### Inspecting Requests

<!-- When faking responses, you may occasionally wish to inspect the requests the client receives in order to make sure your application is sending the correct data or headers. You may accomplish this by calling the `Http::assertSent` method after calling `Http::fake`. -->
応答を偽装する場合、アプリケーションが正しいデータまたはヘッダーを送信していることを確認するために、クライアントが受信するリクエストを検査したい場合があります。これを行うには、`Http::fake` を呼び出した後に `Http::assertSent` メソッドを呼び出します。

<!-- The `assertSent` method accepts a closure which will receive an `Illuminate\Http\Client\Request` instance and should return a boolean value indicating if the request matches your expectations. In order for the test to pass, at least one request must have been issued matching the given expectations: -->
`assertSent` メソッドは、`Illuminate\Http\Client\Request` インスタンスを受け取るクロージャーを受け入れ、リクエストが期待と一致するかどうかを示すブール値を返す必要があります。テストに合格するには、指定された期待に一致するリクエストが少なくとも 1 つ発行されている必要があります。

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
必要に応じて、`assertNotSent` メソッドを使用して、特定のリクエストが送信されなかったことをアサートできます。

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
`assertSentCount` メソッドを使用して、テスト中に「送信された」リクエストの数をアサートできます。

```
Http::fake();

Http::assertSentCount(5);
```

<!-- Or, you may use the `assertNothingSent` method to assert that no requests were sent during the test: -->
または、`assertNothingSent` メソッドを使用して、テスト中にリクエストが送信されなかったことをアサートすることもできます。

```
Http::fake();

Http::assertNothingSent();
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Laravel fires three events during the process of sending HTTP requests. The `RequestSending` event is fired prior to a request being sent, while the `ResponseReceived` event is fired after a response is received for a given request. The `ConnectionFailed` event is fired if no response is received for a given request. -->
Laravel は、HTTP リクエストの送信プロセス中に 3 つのイベントを発生させます。 `RequestSending` イベントはリクエストが送信される前に発生しますが、`ResponseReceived` イベントは特定のリクエストに対する応答を受信した後に発生します。 `ConnectionFailed` イベントは、指定されたリクエストに対する応答が受信されない場合に発生します。

<!-- The `RequestSending` and `ConnectionFailed` events both contain a public `$request` property that you may use to inspect the `Illuminate\Http\Client\Request` instance. Likewise, the `ResponseReceived` event contains a `$request` property as well as a `$response` property which may be used to inspect the `Illuminate\Http\Client\Response` instance. You may register event listeners for this event in your `App\Providers\EventServiceProvider` service provider: -->
`RequestSending` イベントと `ConnectionFailed` イベントには両方とも、`Illuminate\Http\Client\Request` インスタンスの検査に使用できるパブリック `$request` プロパティが含まれています。同様に、`ResponseReceived` イベントには、`$request` プロパティと、`Illuminate\Http\Client\Response` インスタンスの検査に使用できる `$response` プロパティが含まれています。 `App\Providers\EventServiceProvider` サービスプロバイダでこのイベントのイベント リスナを登録できます。

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

