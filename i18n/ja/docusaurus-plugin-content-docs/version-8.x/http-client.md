# HTTPクライアント (HTTP Client)

- [Introduction](#introduction)
- [リクエストの作成](#making-requests)
    - [データのリクエスト](#request-data)
    - [Headers](#headers)
    - [Authentication](#authentication)
    - [Timeout](#timeout)
    - [Retries](#retries)
    - [エラー処理](#error-handling)
    - [ガズルオプション](#guzzle-options)
- [同時リクエスト](#concurrent-requests)
- [Macros](#macros)
- [Testing](#testing)
    - [偽装応答](#faking-responses)
    - [リクエストの検査](#inspecting-requests)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、[Guzzle HTTP クライアント](http://docs.guzzlephp.org/en/stable/) を中心とした表現力豊かな最小限の API を提供し、他の Web アプリケーションと通信するための送信 HTTP リクエストを迅速に作成できるようにします。 Laravel の Guzzle のラッパーは、最も一般的なユースケースと素晴らしい開発者エクスペリエンスに重点を置いています。

開始する前に、アプリケーションの依存関係として Guzzle パッケージがインストールされていることを確認する必要があります。デフォルトでは、Laravel にはこの依存関係が自動的に組み込まれます。ただし、以前にパッケージを削除したことがある場合は、Composer 経由で再度インストールできます。

    composer require guzzlehttp/guzzle

<a name="making-requests"></a>
## リクエストの作成 (Making Requests)

リクエストを行うには、`Http` ファサードによって提供される `head`、`get`、`post`、`put`、`patch`、および `delete` メソッドを使用できます。まず、別の URL に対して基本的な `GET` リクエストを行う方法を調べてみましょう。

    use Illuminate\Support\Facades\Http;

    $response = Http::get('http://example.com');

`get` メソッドは、応答の検査に使用できるさまざまなメソッドを提供する `Illuminate\Http\Client\Response` のインスタンスを返します。

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

`Illuminate\Http\Client\Response` オブジェクトは PHP `ArrayAccess` インターフェイスも実装しているため、応答上で JSON 応答データに直接アクセスできます。

    return Http::get('http://example.com/users/1')['name'];

<a name="dumping-requests"></a>
#### ダンピングリクエスト

発信リクエストのインスタンスが送信される前にダンプしてスクリプトの実行を終了したい場合は、リクエスト定義の先頭に `dd` メソッドを追加します。

    return Http::dd()->get('http://example.com');

<a name="request-data"></a>
### データのリクエスト

もちろん、`POST`、`PUT`、および `PATCH` リクエストを作成するときは、リクエストとともに追加データを送信するのが一般的であるため、これらのメソッドは 2 番目の引数としてデータの配列を受け入れます。デフォルトでは、データは `application/json` コンテンツ タイプを使用して送信されます。

    use Illuminate\Support\Facades\Http;

    $response = Http::post('http://example.com/users', [
        'name' => 'Steve',
        'role' => 'Network Administrator',
    ]);

<a name="get-request-query-parameters"></a>
#### GETリクエストのクエリパラメータ

`GET` リクエストを行うときは、クエリ文字列を URL に直接追加するか、キーと値のペアの配列を 2 番目の引数として `get` メソッドに渡すことができます。

    $response = Http::get('http://example.com/users', [
        'name' => 'Taylor',
        'page' => 1,
    ]);

<a name="sending-form-url-encoded-requests"></a>
#### フォーム URL エンコードされたリクエストの送信

`application/x-www-form-urlencoded` コンテンツ タイプを使用してデータを送信したい場合は、リクエストを行う前に `asForm` メソッドを呼び出す必要があります。

    $response = Http::asForm()->post('http://example.com/users', [
        'name' => 'Sara',
        'role' => 'Privacy Consultant',
    ]);

<a name="sending-a-raw-request-body"></a>
#### 生のリクエスト本文の送信

リクエストを行うときに生のリクエスト本文を提供したい場合は、`withBody` メソッドを使用できます。コンテンツ タイプは、メソッドの 2 番目の引数を介して指定できます。

    $response = Http::withBody(
        base64_encode($photo), 'image/jpeg'
    )->post('http://example.com/photo');

<a name="multi-part-requests"></a>
#### マルチパートリクエスト

ファイルをマルチパートリクエストとして送信したい場合は、リクエストを行う前に `attach` メソッドを呼び出す必要があります。このメソッドは、ファイルの名前とその内容を受け入れます。必要に応じて、ファイルのファイル名とみなされる 3 番目の引数を指定できます。

    $response = Http::attach(
        'attachment', file_get_contents('photo.jpg'), 'photo.jpg'
    )->post('http://example.com/attachments');

ファイルの生のコンテンツを渡す代わりに、ストリーム リソースを渡すこともできます。

    $photo = fopen('photo.jpg', 'r');

    $response = Http::attach(
        'attachment', $photo, 'photo.jpg'
    )->post('http://example.com/attachments');

<a name="headers"></a>
### ヘッダー

ヘッダーは、`withHeaders` メソッドを使用してリクエストに追加できます。この `withHeaders` メソッドは、キーと値のペアの配列を受け入れます。

    $response = Http::withHeaders([
        'X-First' => 'foo',
        'X-Second' => 'bar'
    ])->post('http://example.com/users', [
        'name' => 'Taylor',
    ]);

`accept` メソッドを使用して、アプリケーションがリクエストに応じて期待するコンテンツ タイプを指定できます。

    $response = Http::accept('application/json')->get('http://example.com/users');

便宜上、`acceptJson` メソッドを使用して、アプリケーションがリクエストに応じて `application/json` コンテンツ タイプを予期していることをすばやく指定できます。

    $response = Http::acceptJson()->get('http://example.com/users');

<a name="authentication"></a>
### 認証

基本認証資格情報とダイジェスト認証資格情報は、それぞれ `withBasicAuth` メソッドと `withDigestAuth` メソッドを使用して指定できます。

    // Basic authentication...
    $response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(...);

    // Digest authentication...
    $response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(...);

<a name="bearer-tokens"></a>
#### 無記名トークン

リクエストの `Authorization` ヘッダーにベアラー トークンをすぐに追加したい場合は、`withToken` メソッドを使用できます。

    $response = Http::withToken('token')->post(...);

<a name="timeout"></a>
### タイムアウト

`timeout` メソッドを使用して、応答を待機する最大秒数を指定できます。

    $response = Http::timeout(3)->get(...);

指定されたタイムアウトを超えると、`Illuminate\Http\Client\ConnectionException` のインスタンスがスローされます。

<a name="retries"></a>
### 再試行

クライアントまたはサーバーのエラーが発生した場合に HTTP クライアントがリクエストを自動的に再試行するようにしたい場合は、`retry` メソッドを使用できます。 `retry` メソッドは、リクエストを試行する最大回数と、Laravel が試行の間に待機するミリ秒数を受け入れます。

    $response = Http::retry(3, 100)->post(...);

必要に応じて、`retry` メソッドに 3 番目の引数を渡すことができます。 3 番目の引数は、実際に再試行するかどうかを決定する呼び出し可能引数である必要があります。たとえば、最初のリクエストで `ConnectionException` が発生した場合にのみリクエストを再試行したい場合があります。

    $response = Http::retry(3, 100, function ($exception) {
        return $exception instanceof ConnectionException;
    })->post(...);

すべてのリクエストが失敗した場合、`Illuminate\Http\Client\RequestException` のインスタンスがスローされます。

<a name="error-handling"></a>
### エラー処理

Guzzle のデフォルトの動作とは異なり、Laravel の HTTP クライアント ラッパーは、クライアントまたはサーバーのエラー (サーバーからの `400` および `500` レベルの応答) で例外をスローしません。 `successful`、`clientError`、または `serverError` メソッドを使用して、これらのエラーのいずれかが返されたかどうかを確認できます。

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

<a name="throwing-exceptions"></a>
#### 例外のスロー

応答インスタンスがあり、応答ステータス コードがクライアント エラーまたはサーバー エラーを示している場合に `Illuminate\Http\Client\RequestException` のインスタンスをスローしたい場合は、`throw` メソッドまたは `throwIf` メソッドを使用できます。

    $response = Http::post(...);

    // Throw an exception if a client or server error occurred...
    $response->throw();

    // Throw an exception if an error occurred and the given condition is true...
    $response->throwIf($condition);

    return $response['user']['id'];

`Illuminate\Http\Client\RequestException` インスタンスには、返された応答を検査できるパブリック `$response` プロパティがあります。

`throw` メソッドは、エラーが発生しなかった場合に応答インスタンスを返し、他の操作を `throw` メソッドに連鎖させることができます。

    return Http::post(...)->throw()->json();

例外がスローされる前に追加のロジックを実行したい場合は、`throw` メソッドにクロージャを渡すことができます。例外はクロージャが呼び出された後に自動的にスローされるため、クロージャ内から例外を再スローする必要はありません。

    return Http::post(...)->throw(function ($response, $e) {
        //
    })->json();

<a name="guzzle-options"></a>
### ガズルオプション

`withOptions` メソッドを使用して、追加の [Guzzle リクエストのオプション](http://docs.guzzlephp.org/en/stable/request-options.html) を指定できます。 `withOptions` メソッドは、キーと値のペアの配列を受け入れます。

    $response = Http::withOptions([
        'debug' => true,
    ])->get('http://example.com/users');

<a name="concurrent-requests"></a>
## 同時リクエスト (Concurrent Requests)

場合によっては、複数の HTTP リクエストを同時に実行したい場合があります。つまり、複数のリクエストを順番に発行するのではなく、同時にディスパッチする必要があります。これにより、遅い HTTP API を操作する際のパフォーマンスが大幅に向上する可能性があります。

ありがたいことに、`pool` メソッドを使用してこれを実現できます。 `pool` メソッドは、`Illuminate\Http\Client\Pool` インスタンスを受け取るクロージャーを受け入れるため、ディスパッチするリクエストをリクエスト プールに簡単に追加できます。

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

ご覧のとおり、各応答インスタンスは、プールに追加された順序に基づいてアクセスできます。必要に応じて、`as` メソッドを使用してリクエストに名前を付けることができます。これにより、対応するレスポンスに名前でアクセスできるようになります。

    use Illuminate\Http\Client\Pool;
    use Illuminate\Support\Facades\Http;

    $responses = Http::pool(fn (Pool $pool) => [
        $pool->as('first')->get('http://localhost/first'),
        $pool->as('second')->get('http://localhost/second'),
        $pool->as('third')->get('http://localhost/third'),
    ]);

    return $responses['first']->ok();

<a name="macros"></a>
## マクロ (Macros)

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

マクロを構成したら、アプリケーション内のどこからでもマクロを呼び出して、指定された構成で保留中のリクエストを作成できます。

```php
$response = Http::github()->get('/');
```

<a name="testing"></a>
## テスト (Testing)

多くの Laravel サービスは、テストを簡単かつ表現力豊かに作成できるようにする機能を提供しており、Laravel の HTTP ラッパーも例外ではありません。 `Http` ファサードの `fake` メソッドを使用すると、リクエストが行われたときにスタブ/ダミー応答を返すように HTTP クライアントに指示できます。

<a name="faking-responses"></a>
### 偽装応答

たとえば、すべてのリクエストに対して空の `200` ステータス コード応答を返すように HTTP クライアントに指示するには、引数なしで `fake` メソッドを呼び出すことができます。

    use Illuminate\Support\Facades\Http;

    Http::fake();

    $response = Http::post(...);

> {note} リクエストを偽装する場合、HTTP クライアント ミドルウェアは実行されません。これらのミドルウェアが正しく実行されているかのように、偽の応答に対する期待値を定義する必要があります。

<a name="faking-specific-urls"></a>
#### 特定の URL を偽装する

あるいは、配列を `fake` メソッドに渡すこともできます。配列のキーは、偽装したい URL パターンとそれに関連する応答を表す必要があります。 `*` 文字はワイルドカード文字として使用できます。偽装されていない URL に対して行われたリクエストはすべて実際に実行されます。 `Http` ファサードの `response` メソッドを使用して、次のエンドポイントのスタブ/偽の応答を構築できます。

    Http::fake([
        // Stub a JSON response for GitHub endpoints...
        'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

        // Stub a string response for Google endpoints...
        'google.com/*' => Http::response('Hello World', 200, $headers),
    ]);

一致しない URL をすべてスタブするフォールバック URL パターンを指定したい場合は、単一の `*` 文字を使用できます。

    Http::fake([
        // Stub a JSON response for GitHub endpoints...
        'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

        // Stub a string response for all other endpoints...
        '*' => Http::response('Hello World', 200, ['Headers']),
    ]);

<a name="faking-response-sequences"></a>
#### 応答シーケンスの偽装

場合によっては、単一の URL が特定の順序で一連の偽の応答を返すように指定する必要がある場合があります。これは、`Http::sequence` メソッドを使用して応答を構築することで実現できます。

    Http::fake([
        // Stub a series of responses for GitHub endpoints...
        'github.com/*' => Http::sequence()
                                ->push('Hello World', 200)
                                ->push(['foo' => 'bar'], 200)
                                ->pushStatus(404),
    ]);

応答シーケンス内のすべての応答が消費されると、それ以上の要求によって応答シーケンスが例外をスローします。シーケンスが空の場合に返されるデフォルトの応答を指定したい場合は、`whenEmpty` メソッドを使用できます。

    Http::fake([
        // Stub a series of responses for GitHub endpoints...
        'github.com/*' => Http::sequence()
                                ->push('Hello World', 200)
                                ->push(['foo' => 'bar'], 200)
                                ->whenEmpty(Http::response()),
    ]);

一連の応答を偽装したいが、偽装する特定の URL パターンを指定する必要がない場合は、`Http::fakeSequence` メソッドを使用できます。

    Http::fakeSequence()
            ->push('Hello World', 200)
            ->whenEmpty(Http::response());

<a name="fake-callback"></a>
#### 偽のコールバック

特定のエンドポイントに対してどのような応答を返すかを決定するために、より複雑なロジックが必要な場合は、`fake` メソッドにクロージャを渡すことができます。このクロージャは `Illuminate\Http\Client\Request` のインスタンスを受け取り、応答インスタンスを返す必要があります。クロージャ内では、返す応答の種類を決定するために必要なロジックを実行できます。

    Http::fake(function ($request) {
        return Http::response('Hello World', 200);
    });

<a name="inspecting-requests"></a>
### リクエストの検査

応答を偽装する場合、アプリケーションが正しいデータまたはヘッダーを送信していることを確認するために、クライアントが受信するリクエストを検査したい場合があります。これを行うには、`Http::fake` を呼び出した後に `Http::assertSent` メソッドを呼び出します。

`assertSent` メソッドは、`Illuminate\Http\Client\Request` インスタンスを受け取るクロージャーを受け入れ、リクエストが期待と一致するかどうかを示すブール値を返す必要があります。テストに合格するには、指定された期待に一致するリクエストが少なくとも 1 つ発行されている必要があります。

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

必要に応じて、`assertNotSent` メソッドを使用して、特定のリクエストが送信されなかったことをアサートできます。

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

`assertSentCount` メソッドを使用して、テスト中に「送信された」リクエストの数をアサートできます。

    Http::fake();

    Http::assertSentCount(5);

または、`assertNothingSent` メソッドを使用して、テスト中にリクエストが送信されなかったことをアサートすることもできます。

    Http::fake();

    Http::assertNothingSent();

<a name="events"></a>
## イベント (Events)

Laravel は、HTTP リクエストの送信プロセス中に 3 つのイベントを発生させます。 `RequestSending` イベントはリクエストが送信される前に発生しますが、`ResponseReceived` イベントは特定のリクエストに対する応答を受信した後に発生します。 `ConnectionFailed` イベントは、指定されたリクエストに対する応答が受信されない場合に発生します。

`RequestSending` イベントと `ConnectionFailed` イベントには両方とも、`Illuminate\Http\Client\Request` インスタンスの検査に使用できるパブリック `$request` プロパティが含まれています。同様に、`ResponseReceived` イベントには、`$request` プロパティと、`Illuminate\Http\Client\Response` インスタンスの検査に使用できる `$response` プロパティが含まれています。 `App\Providers\EventServiceProvider` サービスプロバイダでこのイベントのイベント リスナを登録できます。

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

