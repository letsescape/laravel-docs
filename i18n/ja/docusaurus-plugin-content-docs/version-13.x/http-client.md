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
Laravel は、[Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/) を中心とした表現力豊かな最小限の API を提供し、他の Web アプリケーションと通信するための送信 HTTP リクエストを迅速に作成できるようにします。 Laravel の Guzzle のラッパーは、最も一般的なユースケースと素晴らしい開発者エクスペリエンスに重点を置いています。

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make requests, you may use the `head`, `get`, `post`, `put`, `patch`, and `delete` methods provided by the `Http` facade. First, let's examine how to make a basic `GET` request to another URL: -->
リクエストを行うには、`Http` ファサードによって提供される `head`、`get`、`post`、`put`、`patch`、および `delete` メソッドを使用できます。まず、別の URL に対して基本的な `GET` リクエストを行う方法を調べてみましょう。

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

<!-- The `get` method returns an instance of `Illuminate\Http\Client\Response`, which provides a variety of methods that may be used to inspect the response: -->
`get` メソッドは、応答の検査に使用できるさまざまなメソッドを提供する `Illuminate\Http\Client\Response` のインスタンスを返します。

```php
$response->body() : string;
$response->json($key = null, $default = null, $flags = null) : mixed;
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
`Illuminate\Http\Client\Response` オブジェクトは PHP `ArrayAccess` インターフェイスも実装しているため、応答上で JSON 応答データに直接アクセスできます。

```php
return Http::get('http://example.com/users/1')['name'];
```

<!-- In addition to the response methods listed above, the following methods may be used to determine if the response has a specific status code: -->
上記の応答メソッドに加えて、次のメソッドを使用して、応答に特定のステータス コードがあるかどうかを判断できます。

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
HTTP クライアントでは、[URI template specification](https://www.rfc-editor.org/rfc/rfc6570) を使用してリクエスト URL を構築することもできます。 URI テンプレートによって展開できる URL パラメーターを定義するには、`withUrlParameters` メソッドを使用できます。

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '13.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
<!-- #### Dumping Requests -->
#### Dumping Requests

<!-- If you would like to dump the outgoing request instance before it is sent and terminate the script's execution, you may add the `dd` method to the beginning of your request definition: -->
発信リクエストのインスタンスが送信される前にダンプしてスクリプトの実行を終了したい場合は、リクエスト定義の先頭に `dd` メソッドを追加します。

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
<!-- ### Request Data -->
### Request Data

<!-- Of course, it is common when making `POST`, `PUT`, and `PATCH` requests to send additional data with your request, so these methods accept an array of data as their second argument. By default, data will be sent using the `application/json` content type: -->
もちろん、`POST`、`PUT`、および `PATCH` リクエストを作成するときは、リクエストとともに追加データを送信するのが一般的であるため、これらのメソッドは 2 番目の引数としてデータの配列を受け入れます。デフォルトでは、データは `application/json` コンテンツ タイプを使用して送信されます。

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
`GET` リクエストを行うときは、クエリ文字列を URL に直接追加するか、キーと値のペアの配列を 2 番目の引数として `get` メソッドに渡すことができます。

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

<!-- Alternatively, the `withQueryParameters` method may be used: -->
あるいは、`withQueryParameters` メソッドを使用することもできます。

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
`application/x-www-form-urlencoded` コンテンツ タイプを使用してデータを送信したい場合は、リクエストを行う前に `asForm` メソッドを呼び出す必要があります。

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
リクエストを行うときに生のリクエスト本文を提供したい場合は、`withBody` メソッドを使用できます。コンテンツ タイプは、メソッドの 2 番目の引数を介して指定できます。

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
<!-- #### Multi-Part Requests -->
#### Multi-Part Requests

<!-- If you would like to send files as multi-part requests, you should call the `attach` method before making your request. This method accepts the name of the file and its contents. If needed, you may provide a third argument which will be considered the file's filename, while a fourth argument may be used to provide headers associated with the file: -->
ファイルをマルチパートリクエストとして送信したい場合は、リクエストを行う前に `attach` メソッドを呼び出す必要があります。このメソッドは、ファイルの名前とその内容を受け入れます。必要に応じて、ファイルのファイル名とみなされる 3 番目の引数を指定できます。また、4 番目の引数は、ファイルに関連付けられたヘッダーを指定するために使用できます。

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

<!-- Instead of passing the raw contents of a file, you may pass a stream resource: -->
ファイルの生のコンテンツを渡す代わりに、ストリーム リソースを渡すこともできます。

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
ヘッダーは、`withHeaders` メソッドを使用してリクエストに追加できます。この `withHeaders` メソッドは、キーと値のペアの配列を受け入れます。

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

<!-- You may use the `accept` method to specify the content type that your application is expecting in response to your request: -->
`accept` メソッドを使用して、アプリケーションがリクエストに応じて期待するコンテンツ タイプを指定できます。

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

<!-- For convenience, you may use the `acceptJson` method to quickly specify that your application expects the `application/json` content type in response to your request: -->
便宜上、`acceptJson` メソッドを使用して、アプリケーションがリクエストに応じて `application/json` コンテンツ タイプを予期していることをすばやく指定できます。

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

<!-- The `withHeaders` method merges new headers into the request's existing headers. If needed, you may replace all of the headers entirely using the `replaceHeaders` method: -->
`withHeaders` メソッドは、新しいヘッダーをリクエストの既存のヘッダーにマージします。必要に応じて、`replaceHeaders` メソッドを使用してすべてのヘッダーを完全に置き換えることができます。

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
基本認証資格情報とダイジェスト認証資格情報は、それぞれ `withBasicAuth` メソッドと `withDigestAuth` メソッドを使用して指定できます。

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
リクエストの `Authorization` ヘッダーにベアラー トークンをすぐに追加したい場合は、`withToken` メソッドを使用できます。

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
<!-- ### Timeout -->
### Timeout

<!-- The `timeout` method may be used to specify the maximum number of seconds to wait for a response. By default, the HTTP client will timeout after 30 seconds: -->
`timeout` メソッドを使用して、応答を待機する最大秒数を指定できます。デフォルトでは、HTTP クライアントは 30 秒後にタイムアウトします。

```php
$response = Http::timeout(3)->get(/* ... */);
```

<!-- If the given timeout is exceeded, an instance of `Illuminate\Http\Client\ConnectionException` will be thrown. -->
指定されたタイムアウトを超えると、`Illuminate\Http\Client\ConnectionException` のインスタンスがスローされます。

<!-- You may specify the maximum number of seconds to wait while trying to connect to a server using the `connectTimeout` method. The default is 10 seconds: -->
`connectTimeout` メソッドを使用して、サーバーへの接続を試行するときに待機する最大秒数を指定できます。デフォルトは 10 秒です。

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
<!-- ### Retries -->
### Retries

<!-- If you would like the HTTP client to automatically retry the request if a client or server error occurs, you may use the `retry` method. The `retry` method accepts the maximum number of times the request should be attempted and the number of milliseconds that Laravel should wait in between attempts: -->
クライアントまたはサーバーのエラーが発生した場合に HTTP クライアントがリクエストを自動的に再試行するようにしたい場合は、`retry` メソッドを使用できます。 `retry` メソッドは、リクエストを試行する最大回数と、Laravel が試行の間に待機するミリ秒数を受け入れます。

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

<!-- If you would like to manually calculate the number of milliseconds to sleep between attempts, you may pass a closure as the second argument to the `retry` method: -->
試行間のスリープ時間を手動で計算したい場合は、`retry` メソッドの 2 番目の引数としてクロージャを渡すことができます。

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

<!-- For convenience, you may also provide an array as the first argument to the `retry` method. This array will be used to determine how many milliseconds to sleep between subsequent attempts: -->
便宜上、`retry` メソッドの最初の引数として配列を指定することもできます。この配列は、次の試行の間にスリープする時間をミリ秒単位で決定するために使用されます。

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

<!-- If needed, you may pass a third argument to the `retry` method. The third argument should be a callable that determines if the retries should actually be attempted. For example, you may wish to only retry the request if the initial request encounters an `ConnectionException`: -->
必要に応じて、`retry` メソッドに 3 番目の引数を渡すことができます。 3 番目の引数は、実際に再試行するかどうかを決定する呼び出し可能引数である必要があります。たとえば、最初のリクエストで `ConnectionException` が発生した場合にのみリクエストを再試行したい場合があります。

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

<!-- If a request attempt fails, you may wish to make a change to the request before a new attempt is made. You can achieve this by modifying the request argument provided to the callable you provided to the `retry` method. For example, you might want to retry the request with a new authorization token if the first attempt returned an authentication error: -->
リクエストの試行が失敗した場合は、新たな試行を行う前にリクエストを変更することができます。これを実現するには、`retry` メソッドに指定した呼び出し可能オブジェクトに指定したリクエスト引数を変更します。たとえば、最初の試行で認証エラーが返された場合は、新しい認可トークンを使用してリクエストを再試行することができます。

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
すべてのリクエストが失敗した場合、`Illuminate\Http\Client\RequestException` のインスタンスがスローされます。この動作を無効にしたい場合は、`throw` 引数に値 `false` を指定できます。無効にすると、すべての再試行が試行された後に、クライアントが受信した最後の応答が返されます。

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 接続の問題によりすべてのリクエストが失敗した場合、`throw` 引数が `false` に設定されている場合でも、`Illuminate\Http\Client\ConnectionException` がスローされます。

<a name="error-handling"></a>
<!-- ### Error Handling -->
### Error Handling

<!-- Unlike Guzzle's default behavior, Laravel's HTTP client wrapper does not throw exceptions on client or server errors (`400` and `500` level responses from servers). You may determine if one of these errors was returned using the `successful`, `clientError`, or `serverError` methods: -->
Guzzle のデフォルトの動作とは異なり、Laravel の HTTP クライアント ラッパーは、クライアントまたはサーバーのエラー (サーバーからの `400` および `500` レベルの応答) で例外をスローしません。 `successful`、`clientError`、または `serverError` メソッドを使用して、これらのエラーのいずれかが返されたかどうかを確認できます。

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
応答インスタンスがあり、応答ステータス コードがクライアント エラーまたはサーバー エラーを示している場合に `Illuminate\Http\Client\RequestException` のインスタンスをスローしたい場合は、`throw` メソッドまたは `throwIf` メソッドを使用できます。

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

// Throw an exception if a server error occurred (status >500)...
$response->throwIfServerError();

// Throw an exception if a client error occurred (status >400 and <500)...
$response->throwIfClientError();

return $response['user']['id'];
```

<!-- The `Illuminate\Http\Client\RequestException` instance has a public `$response` property which will allow you to inspect the returned response. -->
`Illuminate\Http\Client\RequestException` インスタンスには、返された応答を検査できるパブリック `$response` プロパティがあります。

<!-- The `throw` method returns the response instance if no error occurred, allowing you to chain other operations onto the `throw` method: -->
`throw` メソッドは、エラーが発生しなかった場合に応答インスタンスを返し、他の操作を `throw` メソッドに連鎖させることができます。

```php
return Http::post(/* ... */)->throw()->json();
```

<!-- If you would like to perform some additional logic before the exception is thrown, you may pass a closure to the `throw` method. The exception will be thrown automatically after the closure is invoked, so you do not need to re-throw the exception from within the closure: -->
例外がスローされる前に追加のロジックを実行したい場合は、`throw` メソッドにクロージャを渡すことができます。例外はクロージャが呼び出された後に自動的にスローされるため、クロージャ内から例外を再スローする必要はありません。

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

<!-- By default, `RequestException` messages are truncated to 120 characters when logged or reported. To customize or disable this behavior, you may utilize the `truncateAt` and `dontTruncate` methods when configuring your application's registered behavior in your `bootstrap/app.php` file: -->
デフォルトでは、`RequestException` メッセージはログに記録またはレポートされるときに 120 文字に切り詰められます。この動作をカスタマイズまたは無効にするには、`bootstrap/app.php` ファイルでアプリケーションの登録された動作を構成するときに、`truncateAt` メソッドと `dontTruncate` メソッドを利用できます。

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
あるいは、`truncateExceptionsAt` メソッドを使用して、リクエストごとに例外切り捨て動作をカスタマイズすることもできます。

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
<!-- ### Guzzle Middleware -->
### Guzzle Middleware

<!-- Since Laravel's HTTP client is powered by Guzzle, you may take advantage of [Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) to manipulate the outgoing request or inspect the incoming response. To manipulate the outgoing request, register a Guzzle middleware via the `withRequestMiddleware` method: -->
Laravel の HTTP クライアントは Guzzle を利用しているため、[Guzzle Middleware](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) を利用して送信リクエストを操作したり、受信レスポンスを検査したりできます。送信リクエストを操作するには、`withRequestMiddleware` メソッドを介して Guzzle ミドルウェアを登録します。

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
同様に、`withResponseMiddleware` メソッドを介してミドルウェアを登録することで、受信 HTTP 応答を検査できます。

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
場合によっては、すべての送信リクエストと受信応答に適用されるミドルウェアを登録したい場合があります。これを実現するには、`globalRequestMiddleware` メソッドと `globalResponseMiddleware` メソッドを使用できます。通常、これらのメソッドは、アプリケーションの `AppServiceProvider` の `boot` メソッドで呼び出す必要があります。

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
`withOptions` メソッドを使用して、送信リクエストに追加の [Guzzle request options](http://docs.guzzlephp.org/en/stable/request-options.html) を指定できます。 `withOptions` メソッドは、キーと値のペアの配列を受け入れます。

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
<!-- #### Global Options -->
#### Global Options

<!-- To configure default options for every outgoing request, you may utilize the `globalOptions` method. Typically, this method should be invoked from the `boot` method of your application's `AppServiceProvider`: -->
すべての発信リクエストのデフォルト オプションを設定するには、`globalOptions` メソッドを利用できます。通常、このメソッドは、アプリケーションの `AppServiceProvider` の `boot` メソッドから呼び出す必要があります。

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
場合によっては、複数の HTTP リクエストを同時に実行したい場合があります。つまり、複数のリクエストを順番に発行するのではなく、同時にディスパッチする必要があります。これにより、遅い HTTP API を操作する際のパフォーマンスが大幅に向上する可能性があります。

<a name="request-pooling"></a>
<!-- ### Request Pooling -->
### Request Pooling

<!-- Thankfully, you may accomplish this using the `pool` method. The `pool` method accepts a closure which receives an `Illuminate\Http\Client\Pool` instance, allowing you to easily add requests to the request pool for dispatching: -->
ありがたいことに、`pool` メソッドを使用してこれを実現できます。 `pool` メソッドは、`Illuminate\Http\Client\Pool` インスタンスを受け取るクロージャーを受け入れるため、ディスパッチするリクエストをリクエスト プールに簡単に追加できます。

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
ご覧のとおり、各応答インスタンスは、プールに追加された順序に基づいてアクセスできます。必要に応じて、`as` メソッドを使用してリクエストに名前を付けることができます。これにより、対応するレスポンスに名前でアクセスできるようになります。

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
リクエスト プールの最大同時実行数は、`concurrency` 引数を `pool` メソッドに指定することで制御できます。この値により、リクエスト プールの処理中に同時に実行できる HTTP リクエストの最大数が決まります。

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<!-- If a pooled request fails at the connection level (for example, a timeout or DNS failure), the corresponding entry in the `$responses` array will be an `Illuminate\Http\Client\ConnectionException` instance instead of a `Response` instance: -->
プールされたリクエストが接続レベルで失敗した場合（たとえば、タイムアウトや DNS エラーが発生した場合）、`$responses` 配列の対応する要素は `Response` インスタンスではなく、`Illuminate\Http\Client\ConnectionException` インスタンスになります。

```php
foreach ($responses as $response) {
    if ($response instanceof Throwable) {
        // The request failed to connect...
    } elseif ($response->failed()) {
        // The request connected but received an error response...
    }
}
```

<a name="customizing-concurrent-requests"></a>
<!-- #### Customizing Concurrent Requests -->
#### Customizing Concurrent Requests

<!-- The `pool` method cannot be chained with other HTTP client methods such as the `withHeaders` or `middleware` methods. If you want to apply custom headers or middleware to pooled requests, you should configure those options on each request in the pool: -->
`pool` メソッドは、`withHeaders` メソッドや `middleware` メソッドなどの他の HTTP クライアント メソッドとチェーンすることはできません。プールされたリクエストにカスタム ヘッダーまたはミドルウェアを適用する場合は、プール内の各リクエストでこれらのオプションを構成する必要があります。

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
Laravel で同時リクエストを処理するもう 1 つの方法は、`batch` メソッドを使用することです。 `pool` メソッドと同様に、`Illuminate\Http\Client\Batch` インスタンスを受け取るクロージャを受け入れるため、ディスパッチするリクエスト プールにリクエストを簡単に追加できますが、完了コールバックを定義することもできます。

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
`pool` メソッドと同様に、`as` メソッドを使用してリクエストに名前を付けることができます。

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

<!-- After a `batch` is started by calling the `send` method, you can't add new requests to it. Trying to do so will result in a `Illuminate\Http\Client\BatchInProgressException` exception being thrown. -->
`send` メソッドを呼び出して `batch` を開始した後は、それに新しいリクエストを追加することはできません。これを実行しようとすると、`Illuminate\Http\Client\BatchInProgressException` 例外がスローされます。

<!-- The maximum concurrency of the request batch may be controlled via the `concurrency` method. This value determines the maximum number of HTTP requests that may be concurrently in-flight while processing the request batch: -->
リクエスト バッチの最大同時実行数は、`concurrency` メソッドを介して制御できます。この値により、リクエスト バッチの処理中に同時に実行できる HTTP リクエストの最大数が決まります。

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
<!-- #### Inspecting Batches -->
#### Inspecting Batches

<!-- The `Illuminate\Http\Client\Batch` instance that is provided to batch completion callbacks has a variety of properties and methods to assist you in interacting with and inspecting a given batch of requests: -->
バッチ完了コールバックに提供される `Illuminate\Http\Client\Batch` インスタンスには、特定のリクエストのバッチの操作と検査を支援するさまざまなプロパティとメソッドがあります。

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
`defer` メソッドが呼び出されたとき、リクエストのバッチはすぐには実行されません。代わりに、Laravel は、現在のアプリケーションリクエストの HTTP 応答がユーザーに送信された後にバッチを実行し、アプリケーションの高速性と応答性を維持します。

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
Laravel HTTP クライアントを使用すると、アプリケーション全体でサービスと対話するときに共通のリクエスト パスとヘッダーを構成するための流暢で表現力豊かなメカニズムとして機能する「マクロ」を定義できます。まず、アプリケーションの `App\Providers\AppServiceProvider` クラスの `boot` メソッド内でマクロを定義します。

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
マクロを構成したら、アプリケーション内のどこからでもマクロを呼び出して、指定された構成で保留中のリクエストを作成できます。

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
<!-- ## Testing -->
## Testing

<!-- Many Laravel services provide functionality to help you easily and expressively write tests, and Laravel's HTTP client is no exception. The `Http` facade's `fake` method allows you to instruct the HTTP client to return stubbed / dummy responses when requests are made. -->
多くの Laravel サービスは、テストを簡単かつ表現力豊かに作成できるようにする機能を提供しており、Laravel の HTTP クライアントも例外ではありません。 `Http` ファサードの `fake` メソッドを使用すると、リクエストが行われたときにスタブ/ダミー応答を返すように HTTP クライアントに指示できます。

<a name="faking-responses"></a>
<!-- ### Faking Responses -->
### Faking Responses

<!-- For example, to instruct the HTTP client to return empty, `200` status code responses for every request, you may call the `fake` method with no arguments: -->
たとえば、すべてのリクエストに対して空の `200` ステータス コード応答を返すように HTTP クライアントに指示するには、引数なしで `fake` メソッドを呼び出すことができます。

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
<!-- #### Faking Specific URLs -->
#### Faking Specific URLs

<!-- Alternatively, you may pass an array to the `fake` method. The array's keys should represent URL patterns that you wish to fake and their associated responses. The `*` character may be used as a wildcard character. You may use the `Http` facade's `response` method to construct stub / fake responses for these endpoints: -->
あるいは、配列を `fake` メソッドに渡すこともできます。配列のキーは、偽装したい URL パターンとそれに関連する応答を表す必要があります。 `*` 文字はワイルドカード文字として使用できます。 `Http` ファサードの `response` メソッドを使用して、次のエンドポイントのスタブ/偽の応答を構築できます。

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

<!-- Any requests made to URLs that have not been faked will actually be executed. If you would like to specify a fallback URL pattern that will stub all unmatched URLs, you may use a single `*` character: -->
偽装されていない URL に対して行われたリクエストはすべて実際に実行されます。一致しない URL をすべてスタブするフォールバック URL パターンを指定したい場合は、単一の `*` 文字を使用できます。

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

<!-- For convenience, simple string, JSON, and empty responses may be generated by providing a string, array, or integer as the response: -->
便宜上、文字列、配列、または整数を応答として指定することで、単純な文字列、JSON、および空の応答を生成できます。

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
HTTP クライアントがリクエストを実行しようとしたときに `Illuminate\Http\Client\ConnectionException` を検出した場合、アプリケーションの動作をテストする必要がある場合があります。 `failedConnection` メソッドを使用して、HTTP クライアントに接続例外をスローするように指示できます。

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

<!-- To test your application's behavior if a `Illuminate\Http\Client\RequestException` is thrown, you may use the `failedRequest` method: -->
`Illuminate\Http\Client\RequestException` がスローされた場合のアプリケーションの動作をテストするには、`failedRequest` メソッドを使用できます。

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
場合によっては、単一の URL が特定の順序で一連の偽の応答を返すように指定する必要がある場合があります。これは、`Http::sequence` メソッドを使用して応答を構築することで実現できます。

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
応答シーケンス内のすべての応答が消費されると、それ以上の要求によって応答シーケンスは例外をスローします。シーケンスが空の場合に返されるデフォルトの応答を指定したい場合は、`whenEmpty` メソッドを使用できます。

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
一連の応答を偽装したいが、偽装する特定の URL パターンを指定する必要がない場合は、`Http::fakeSequence` メソッドを使用できます。

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
<!-- #### Fake Callback -->
#### Fake Callback

<!-- If you require more complicated logic to determine what responses to return for certain endpoints, you may pass a closure to the `fake` method. This closure will receive an instance of `Illuminate\Http\Client\Request` and should return a response instance. Within your closure, you may perform whatever logic is necessary to determine what type of response to return: -->
特定のエンドポイントに対してどのような応答を返すかを決定するために、より複雑なロジックが必要な場合は、`fake` メソッドにクロージャを渡すことができます。このクロージャは `Illuminate\Http\Client\Request` のインスタンスを受け取り、応答インスタンスを返す必要があります。クロージャ内では、返す応答の種類を決定するために必要なロジックを実行できます。

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
応答を偽装する場合、アプリケーションが正しいデータまたはヘッダーを送信していることを確認するために、クライアントが受信するリクエストを検査したい場合があります。これを行うには、`Http::fake` を呼び出した後に `Http::assertSent` メソッドを呼び出します。

<!-- The `assertSent` method accepts a closure which will receive an `Illuminate\Http\Client\Request` instance and should return a boolean value indicating if the request matches your expectations. In order for the test to pass, at least one request must have been issued matching the given expectations: -->
`assertSent` メソッドは、`Illuminate\Http\Client\Request` インスタンスを受け取るクロージャーを受け入れ、リクエストが期待と一致するかどうかを示すブール値を返す必要があります。テストに合格するには、指定された期待に一致するリクエストが少なくとも 1 つ発行されている必要があります。

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
必要に応じて、`assertNotSent` メソッドを使用して、特定のリクエストが送信されなかったことをアサートできます。

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
`assertSentCount` メソッドを使用して、テスト中に「送信された」リクエストの数をアサートできます。

```php
Http::fake();

Http::assertSentCount(5);
```

<!-- Or, you may use the `assertNothingSent` method to assert that no requests were sent during the test: -->
または、`assertNothingSent` メソッドを使用して、テスト中にリクエストが送信されなかったことをアサートすることもできます。

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
<!-- #### Recording Requests / Responses -->
#### Recording Requests / Responses

<!-- You may use the `recorded` method to gather all requests and their corresponding responses. The `recorded` method returns a collection of arrays that contains instances of `Illuminate\Http\Client\Request` and `Illuminate\Http\Client\Response`: -->
`recorded` メソッドを使用して、すべてのリクエストとそれに対応するレスポンスを収集できます。 `recorded` メソッドは、`Illuminate\Http\Client\Request` および `Illuminate\Http\Client\Response` のインスタンスを含む配列のコレクションを返します。

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
さらに、`recorded` メソッドは、`Illuminate\Http\Client\Request` および `Illuminate\Http\Client\Response` のインスタンスを受け取るクロージャを受け入れ、期待に基づいてリクエスト/レスポンスのペアをフィルタリングするために使用できます。

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
HTTP クライアント経由で送信されたすべてのリクエストが個別のテストまたはテスト スイート全体にわたって偽装されていることを確認したい場合は、`preventStrayRequests` メソッドを呼び出すことができます。このメソッドを呼び出した後、対応する偽の応答がないリクエストは、実際の HTTP リクエストを作成するのではなく、例外をスローします。

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
場合によっては、特定のリクエストの実行を許可しながら、ほとんどの迷走リクエストを阻止したい場合があります。これを実現するには、URL パターンの配列を `allowStrayRequests` メソッドに渡すことができます。指定されたパターンのいずれかに一致するリクエストは許可されますが、他のすべてのリクエストは例外をスローし続けます。

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
Laravel は、HTTP リクエストの送信プロセス中に 3 つのイベントを発生させます。 `RequestSending` イベントはリクエストが送信される前に発生しますが、`ResponseReceived` イベントは特定のリクエストに対する応答を受信した後に発生します。 `ConnectionFailed` イベントは、指定されたリクエストに対する応答が受信されない場合に発生します。

<!-- The `RequestSending` and `ConnectionFailed` events both contain a public `$request` property that you may use to inspect the `Illuminate\Http\Client\Request` instance. Likewise, the `ResponseReceived` event contains a `$request` property as well as a `$response` property which may be used to inspect the `Illuminate\Http\Client\Response` instance. You may create [event listeners](/docs/13.x/events) for these events within your application: -->
`RequestSending` イベントと `ConnectionFailed` イベントには両方とも、`Illuminate\Http\Client\Request` インスタンスの検査に使用できるパブリック `$request` プロパティが含まれています。同様に、`ResponseReceived` イベントには、`$request` プロパティと、`Illuminate\Http\Client\Response` インスタンスの検査に使用できる `$response` プロパティが含まれています。アプリケーション内で次のイベントに対して [event listeners](/docs/13.x/events) を作成できます。

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
