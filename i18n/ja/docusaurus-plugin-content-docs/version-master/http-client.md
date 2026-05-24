# HTTPクライアント (HTTP Client)

- [Introduction](#introduction)
- [リクエストの作成](#making-requests)
    - [データのリクエスト](#request-data)
    - [Headers](#headers)
    - [Authentication](#authentication)
    - [Timeout](#timeout)
    - [Retries](#retries)
    - [エラー処理](#error-handling)
    - [ガズルミドルウェア](#guzzle-middleware)
    - [ガズルオプション](#guzzle-options)
- [同時リクエスト](#concurrent-requests)
    - [リクエストプーリング](#request-pooling)
    - [リクエストのバッチ処理](#request-batching)
- [Macros](#macros)
- [Testing](#testing)
    - [偽装応答](#faking-responses)
    - [リクエストの検査](#inspecting-requests)
    - [迷走リクエストの防止](#preventing-stray-requests)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、[Guzzle HTTP クライアント](http://docs.guzzlephp.org/en/stable/) を中心とした表現力豊かな最小限の API を提供し、他の Web アプリケーションと通信するための送信 HTTP リクエストを迅速に作成できるようにします。 Laravel の Guzzle のラッパーは、最も一般的なユースケースと素晴らしい開発者エクスペリエンスに重点を置いています。

<a name="making-requests"></a>
## リクエストの作成 (Making Requests)

リクエストを行うには、`Http` ファサードによって提供される `head`、`get`、`post`、`put`、`patch`、および `delete` メソッドを使用できます。まず、別の URL に対して基本的な `GET` リクエストを行う方法を調べてみましょう。

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```

`get` メソッドは、応答の検査に使用できるさまざまなメソッドを提供する `Illuminate\Http\Client\Response` のインスタンスを返します。

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

`Illuminate\Http\Client\Response` オブジェクトは PHP `ArrayAccess` インターフェイスも実装しているため、応答上で JSON 応答データに直接アクセスできます。

```php
return Http::get('http://example.com/users/1')['name'];
```

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
#### URI テンプレート

HTTP クライアントでは、[URIテンプレートの仕様](https://www.rfc-editor.org/rfc/rfc6570) を使用してリクエスト URL を構築することもできます。 URI テンプレートによって展開できる URL パラメーターを定義するには、`withUrlParameters` メソッドを使用できます。

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '12.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```

<a name="dumping-requests"></a>
#### ダンピングリクエスト

発信リクエストのインスタンスが送信される前にダンプしてスクリプトの実行を終了したい場合は、リクエスト定義の先頭に `dd` メソッドを追加します。

```php
return Http::dd()->get('http://example.com');
```

<a name="request-data"></a>
### データのリクエスト

もちろん、`POST`、`PUT`、および `PATCH` リクエストを作成するときは、リクエストとともに追加データを送信するのが一般的であるため、これらのメソッドは 2 番目の引数としてデータの配列を受け入れます。デフォルトでは、データは `application/json` コンテンツ タイプを使用して送信されます。

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```

<a name="get-request-query-parameters"></a>
#### GETリクエストのクエリパラメータ

`GET` リクエストを行うときは、クエリ文字列を URL に直接追加するか、キーと値のペアの配列を 2 番目の引数として `get` メソッドに渡すことができます。

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```

あるいは、`withQueryParameters` メソッドを使用することもできます。

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```

<a name="sending-form-url-encoded-requests"></a>
#### フォーム URL エンコードされたリクエストの送信

`application/x-www-form-urlencoded` コンテンツ タイプを使用してデータを送信したい場合は、リクエストを行う前に `asForm` メソッドを呼び出す必要があります。

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```

<a name="sending-a-raw-request-body"></a>
#### 生のリクエスト本文の送信

リクエストを行うときに生のリクエスト本文を提供したい場合は、`withBody` メソッドを使用できます。コンテンツ タイプは、メソッドの 2 番目の引数を介して指定できます。

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```

<a name="multi-part-requests"></a>
#### マルチパートリクエスト

ファイルをマルチパートリクエストとして送信したい場合は、リクエストを行う前に `attach` メソッドを呼び出す必要があります。このメソッドは、ファイルの名前とその内容を受け入れます。必要に応じて、ファイルのファイル名とみなされる 3 番目の引数を指定できます。また、4 番目の引数は、ファイルに関連付けられたヘッダーを指定するために使用できます。

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```

ファイルの生のコンテンツを渡す代わりに、ストリーム リソースを渡すこともできます。

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```

<a name="headers"></a>
### ヘッダー

ヘッダーは、`withHeaders` メソッドを使用してリクエストに追加できます。この `withHeaders` メソッドは、キーと値のペアの配列を受け入れます。

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```

`accept` メソッドを使用して、アプリケーションがリクエストに応じて期待するコンテンツ タイプを指定できます。

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```

便宜上、`acceptJson` メソッドを使用して、アプリケーションがリクエストに応じて `application/json` コンテンツ タイプを予期していることをすばやく指定できます。

```php
$response = Http::acceptJson()->get('http://example.com/users');
```

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
### 認証

基本認証資格情報とダイジェスト認証資格情報は、それぞれ `withBasicAuth` メソッドと `withDigestAuth` メソッドを使用して指定できます。

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```

<a name="bearer-tokens"></a>
#### 無記名トークン

リクエストの `Authorization` ヘッダーにベアラー トークンをすぐに追加したい場合は、`withToken` メソッドを使用できます。

```php
$response = Http::withToken('token')->post(/* ... */);
```

<a name="timeout"></a>
### タイムアウト

`timeout` メソッドを使用して、応答を待機する最大秒数を指定できます。デフォルトでは、HTTP クライアントは 30 秒後にタイムアウトします。

```php
$response = Http::timeout(3)->get(/* ... */);
```

指定されたタイムアウトを超えると、`Illuminate\Http\Client\ConnectionException` のインスタンスがスローされます。

`connectTimeout` メソッドを使用して、サーバーへの接続を試行するときに待機する最大秒数を指定できます。デフォルトは 10 秒です。

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```

<a name="retries"></a>
### 再試行

クライアントまたはサーバーのエラーが発生した場合に HTTP クライアントがリクエストを自動的に再試行するようにしたい場合は、`retry` メソッドを使用できます。 `retry` メソッドは、リクエストを試行する最大回数と、Laravel が試行の間に待機するミリ秒数を受け入れます。

```php
$response = Http::retry(3, 100)->post(/* ... */);
```

試行間のスリープ時間を手動で計算したい場合は、`retry` メソッドの 2 番目の引数としてクロージャを渡すことができます。

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```

便宜上、`retry` メソッドの最初の引数として配列を指定することもできます。この配列は、次の試行の間にスリープする時間をミリ秒単位で決定するために使用されます。

```php
$response = Http::retry([100, 200])->post(/* ... */);
```

必要に応じて、`retry` メソッドに 3 番目の引数を渡すことができます。 3 番目の引数は、実際に再試行するかどうかを決定する呼び出し可能引数である必要があります。たとえば、最初のリクエストで `ConnectionException` が発生した場合にのみリクエストを再試行したい場合があります。

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```

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

すべてのリクエストが失敗した場合、`Illuminate\Http\Client\RequestException` のインスタンスがスローされます。この動作を無効にしたい場合は、`throw` 引数に値 `false` を指定できます。無効にすると、すべての再試行が試行された後に、クライアントが受信した最後の応答が返されます。

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```

> [!WARNING]
> 接続の問題によりすべてのリクエストが失敗した場合、`throw` 引数が `false` に設定されている場合でも、`Illuminate\Http\Client\ConnectionException` がスローされます。

<a name="error-handling"></a>
### エラー処理

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
#### 例外のスロー

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

return $response['user']['id'];
```

`Illuminate\Http\Client\RequestException` インスタンスには、返された応答を検査できるパブリック `$response` プロパティがあります。

`throw` メソッドは、エラーが発生しなかった場合に応答インスタンスを返し、他の操作を `throw` メソッドに連鎖させることができます。

```php
return Http::post(/* ... */)->throw()->json();
```

例外がスローされる前に追加のロジックを実行したい場合は、`throw` メソッドにクロージャを渡すことができます。例外はクロージャが呼び出された後に自動的にスローされるため、クロージャ内から例外を再スローする必要はありません。

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```

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

あるいは、`truncateExceptionsAt` メソッドを使用して、リクエストごとに例外切り捨て動作をカスタマイズすることもできます。

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```

<a name="guzzle-middleware"></a>
### ガズルミドルウェア

Laravel の HTTP クライアントは Guzzle を利用しているため、[ガズルミドルウェア](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html) を利用して送信リクエストを操作したり、受信レスポンスを検査したりできます。送信リクエストを操作するには、`withRequestMiddleware` メソッドを介して Guzzle ミドルウェアを登録します。

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```

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
#### グローバルミドルウェア

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
### ガズルオプション

`withOptions` メソッドを使用して、送信リクエストに追加の [Guzzle リクエストのオプション](http://docs.guzzlephp.org/en/stable/request-options.html) を指定できます。 `withOptions` メソッドは、キーと値のペアの配列を受け入れます。

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```

<a name="global-options"></a>
#### グローバルオプション

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
## 同時リクエスト (Concurrent Requests)

場合によっては、複数の HTTP リクエストを同時に実行したい場合があります。つまり、複数のリクエストを順番に発行するのではなく、同時にディスパッチする必要があります。これにより、遅い HTTP API を操作する際のパフォーマンスが大幅に向上する可能性があります。

<a name="request-pooling"></a>
### リクエストプーリング

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

リクエスト プールの最大同時実行数は、`concurrency` 引数を `pool` メソッドに指定することで制御できます。この値により、リクエスト プールの処理中に同時に実行できる HTTP リクエストの最大数が決まります。

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```

<a name="customizing-concurrent-requests"></a>
#### 同時リクエストのカスタマイズ

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
### リクエストのバッチ処理

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

`pool` メソッドと同様に、`as` メソッドを使用してリクエストに名前を付けることができます。

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```

`send` メソッドを呼び出して `batch` を開始した後は、それに新しいリクエストを追加することはできません。これを実行しようとすると、`Illuminate\Http\Client\BatchInProgressException` 例外がスローされます。

リクエスト バッチの最大同時実行数は、`concurrency` メソッドを介して制御できます。この値により、リクエスト バッチの処理中に同時に実行できる HTTP リクエストの最大数が決まります。

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```

<a name="inspecting-batches"></a>
#### バッチの検査

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
#### バッチの延期

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
## マクロ (Macros)

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

マクロを構成したら、アプリケーション内のどこからでもマクロを呼び出して、指定された構成で保留中のリクエストを作成できます。

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## テスト (Testing)

多くの Laravel サービスは、テストを簡単かつ表現力豊かに作成できるようにする機能を提供しており、Laravel の HTTP クライアントも例外ではありません。 `Http` ファサードの `fake` メソッドを使用すると、リクエストが行われたときにスタブ/ダミー応答を返すように HTTP クライアントに指示できます。

<a name="faking-responses"></a>
### 偽装応答

たとえば、すべてのリクエストに対して空の `200` ステータス コード応答を返すように HTTP クライアントに指示するには、引数なしで `fake` メソッドを呼び出すことができます。

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```

<a name="faking-specific-urls"></a>
#### 特定の URL を偽装する

あるいは、配列を `fake` メソッドに渡すこともできます。配列のキーは、偽装したい URL パターンとそれに関連する応答を表す必要があります。 `*` 文字はワイルドカード文字として使用できます。 `Http` ファサードの `response` メソッドを使用して、次のエンドポイントのスタブ/偽の応答を構築できます。

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```

偽装されていない URL に対して行われたリクエストはすべて実際に実行されます。一致しない URL をすべてスタブするフォールバック URL パターンを指定したい場合は、単一の `*` 文字を使用できます。

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```

便宜上、文字列、配列、または整数を応答として指定することで、単純な文字列、JSON、および空の応答を生成できます。

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```

<a name="faking-connection-exceptions"></a>
#### 例外の偽装

HTTP クライアントがリクエストを実行しようとしたときに `Illuminate\Http\Client\ConnectionException` を検出した場合、アプリケーションの動作をテストする必要がある場合があります。 `failedConnection` メソッドを使用して、HTTP クライアントに接続例外をスローするように指示できます。

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```

`Illuminate\Http\Client\RequestException` がスローされた場合のアプリケーションの動作をテストするには、`failedRequest` メソッドを使用できます。

```php
$this->mock(GithubService::class);
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```

<a name="faking-response-sequences"></a>
#### 応答シーケンスの偽装

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

一連の応答を偽装したいが、偽装する特定の URL パターンを指定する必要がない場合は、`Http::fakeSequence` メソッドを使用できます。

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```

<a name="fake-callback"></a>
#### 偽のコールバック

特定のエンドポイントに対してどのような応答を返すかを決定するために、より複雑なロジックが必要な場合は、`fake` メソッドにクロージャを渡すことができます。このクロージャは `Illuminate\Http\Client\Request` のインスタンスを受け取り、応答インスタンスを返す必要があります。クロージャ内では、返す応答の種類を決定するために必要なロジックを実行できます。

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```

<a name="inspecting-requests"></a>
### リクエストの検査

応答を偽装する場合、アプリケーションが正しいデータまたはヘッダーを送信していることを確認するために、クライアントが受信するリクエストを検査したい場合があります。これを行うには、`Http::fake` を呼び出した後に `Http::assertSent` メソッドを呼び出します。

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

`assertSentCount` メソッドを使用して、テスト中に「送信された」リクエストの数をアサートできます。

```php
Http::fake();

Http::assertSentCount(5);
```

または、`assertNothingSent` メソッドを使用して、テスト中にリクエストが送信されなかったことをアサートすることもできます。

```php
Http::fake();

Http::assertNothingSent();
```

<a name="recording-requests-and-responses"></a>
#### リクエスト/レスポンスの記録

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
### 迷走リクエストの防止

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
## イベント (Events)

Laravel は、HTTP リクエストの送信プロセス中に 3 つのイベントを発生させます。 `RequestSending` イベントはリクエストが送信される前に発生しますが、`ResponseReceived` イベントは特定のリクエストに対する応答を受信した後に発生します。 `ConnectionFailed` イベントは、指定されたリクエストに対する応答が受信されない場合に発生します。

`RequestSending` イベントと `ConnectionFailed` イベントには両方とも、`Illuminate\Http\Client\Request` インスタンスの検査に使用できるパブリック `$request` プロパティが含まれています。同様に、`ResponseReceived` イベントには、`$request` プロパティと、`Illuminate\Http\Client\Response` インスタンスの検査に使用できる `$response` プロパティが含まれています。アプリケーション内で次のイベントに対して [イベントリスナ](/docs/{{version}}/events) を作成できます。

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

