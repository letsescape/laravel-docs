<!-- # HTTP Responses -->
# HTTP Responses

- [Creating Responses](#creating-responses)
    - [Attaching Headers to Responses](#attaching-headers-to-responses)
    - [Attaching Cookies to Responses](#attaching-cookies-to-responses)
    - [Cookies and Encryption](#cookies-and-encryption)
- [Redirects](#redirects)
    - [Redirecting to Named Routes](#redirecting-named-routes)
    - [Redirecting to Controller Actions](#redirecting-controller-actions)
    - [Redirecting to External Domains](#redirecting-external-domains)
    - [Redirecting With Flashed Session Data](#redirecting-with-flashed-session-data)
- [Other Response Types](#other-response-types)
    - [View Responses](#view-responses)
    - [JSON Responses](#json-responses)
    - [File Downloads](#file-downloads)
    - [File Responses](#file-responses)
- [Streamed Responses](#streamed-responses)
    - [Consuming Streamed Responses](#consuming-streamed-responses)
    - [Streamed JSON Responses](#streamed-json-responses)
    - [Event Streams (SSE)](#event-streams)
    - [Streamed Downloads](#streamed-downloads)
- [Response Macros](#response-macros)

<a name="creating-responses"></a>
<!-- ## Creating Responses -->
## Creating Responses

<a name="strings-arrays"></a>
<!-- #### Strings and Arrays -->
#### Strings and Arrays

<!-- All routes and controllers should return a response to be sent back to the user's browser. Laravel provides several different ways to return responses. The most basic response is returning a string from a route or controller. The framework will automatically convert the string into a full HTTP response: -->
すべてのルートとコントローラは、ユーザーのブラウザーに送り返される応答を返す必要があります。 Laravel は、応答を返すためのいくつかの異なる方法を提供します。最も基本的な応答は、ルートまたはコントローラから文字列を返すことです。フレームワークは、文字列を完全な HTTP 応答に自動的に変換します。

```php
Route::get('/', function () {
    return 'Hello World';
});
```

<!-- In addition to returning strings from your routes and controllers, you may also return arrays. The framework will automatically convert the array into a JSON response: -->
ルートやコントローラから文字列を返すだけでなく、配列を返すこともできます。フレームワークは配列を JSON 応答に自動的に変換します。

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> ルートまたはコントローラから [Eloquent collections](/docs/master/eloquent-collections) を返すこともできることをご存知ですか?これらは自動的に JSON に変換されます。試してみてください!

<a name="response-objects"></a>
<!-- #### Response Objects -->
#### Response Objects

<!-- Typically, you won't just be returning simple strings or arrays from your route actions. Instead, you will be returning full `Illuminate\Http\Response` instances or [views](/docs/master/views). -->
通常、ルート アクションから単純な文字列や配列を返すだけではありません。代わりに、完全な `Illuminate\Http\Response` インスタンスまたは [views](/docs/master/views) を返します。

<!-- Returning a full `Response` instance allows you to customize the response's HTTP status code and headers. A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, which provides a variety of methods for building HTTP responses: -->
完全な `Response` インスタンスを返すと、応答の HTTP ステータス コードとヘッダーをカスタマイズできます。 `Response` インスタンスは、HTTP 応答を構築するためのさまざまなメソッドを提供する `Symfony\Component\HttpFoundation\Response` クラスを継承します。

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
<!-- #### Eloquent Models and Collections -->
#### Eloquent Models and Collections

<!-- You may also return [Eloquent ORM](/docs/master/eloquent) models and collections directly from your routes and controllers. When you do, Laravel will automatically convert the models and collections to JSON responses while respecting the model's [hidden attributes](/docs/master/eloquent-serialization#hiding-attributes-from-json): -->
[Eloquent ORM](/docs/master/eloquent) モデルとコレクションをルートとコントローラから直接返すこともできます。これを行うと、Laravel はモデルの [hidden attributes](/docs/master/eloquent-serialization#hiding-attributes-from-json) を尊重しながら、モデルとコレクションを JSON 応答に自動的に変換します。

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
<!-- ### Attaching Headers to Responses -->
### Attaching Headers to Responses

<!-- Keep in mind that most response methods are chainable, allowing for the fluent construction of response instances. For example, you may use the `header` method to add a series of headers to the response before sending it back to the user: -->
ほとんどの応答メソッドはチェーン可能であり、応答インスタンスをスムーズに構築できることに留意してください。たとえば、`header` メソッドを使用して、応答をユーザーに送り返す前に一連のヘッダーを応答に追加できます。

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

<!-- Or, you may use the `withHeaders` method to specify an array of headers to be added to the response: -->
または、`withHeaders` メソッドを使用して、応答に追加するヘッダーの配列を指定することもできます。

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

<!-- You can remove specific headers from an outgoing response using the `withoutHeader` method: -->
`withoutHeader` メソッドを使用して、送信応答から特定のヘッダーを削除できます。

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

<a name="cache-control-middleware"></a>
<!-- #### Cache Control Middleware -->
#### Cache Control Middleware

<!-- Laravel includes a `cache.headers` middleware, which may be used to quickly set the `Cache-Control` header for a group of routes. Directives should be provided using the "snake case" equivalent of the corresponding cache-control directive and should be separated by a semicolon. If `etag` is specified in the list of directives, an MD5 hash of the response content will automatically be set as the ETag identifier: -->
Laravel には `cache.headers` ミドルウェアが含まれており、ルートのグループに `Cache-Control` ヘッダーをすばやく設定するために使用できます。ディレクティブは、対応するキャッシュ制御ディレクティブと同等の「スネーク ケース」を使用して指定する必要があり、セミコロンで区切る必要があります。ディレクティブのリストで `etag` が指定されている場合、応答コンテンツの MD5 ハッシュが ETag 識別子として自動的に設定されます。

```php
Route::middleware('cache.headers:public;max_age=30;s_maxage=300;stale_while_revalidate=600;etag')->group(function () {
    Route::get('/privacy', function () {
        // ...
    });

    Route::get('/terms', function () {
        // ...
    });
});
```

<a name="attaching-cookies-to-responses"></a>
<!-- ### Attaching Cookies to Responses -->
### Attaching Cookies to Responses

<!-- You may attach a cookie to an outgoing `Illuminate\Http\Response` instance using the `cookie` method. You should pass the name, value, and the number of minutes the cookie should be considered valid to this method: -->
`cookie` メソッドを使用して、発信 `Illuminate\Http\Response` インスタンスに Cookie を添付できます。名前、値、Cookie が有効であるとみなされる分数をこのメソッドに渡す必要があります。

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

<!-- The `cookie` method also accepts a few more arguments which are used less frequently. Generally, these arguments have the same purpose and meaning as the arguments that would be given to PHP's native [setcookie](https://secure.php.net/manual/en/function.setcookie.php) method: -->
`cookie` メソッドは、使用頻度は低いですが、さらにいくつかの引数も受け入れます。一般に、これらの引数は、PHP のネイティブ [setcookie](https://secure.php.net/manual/en/function.setcookie.php) メソッドに与えられる引数と同じ目的と意味を持ちます。

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

<!-- If you would like to ensure that a cookie is sent with the outgoing response but you do not yet have an instance of that response, you can use the `Cookie` facade to "queue" cookies for attachment to the response when it is sent. The `queue` method accepts the arguments needed to create a cookie instance. These cookies will be attached to the outgoing response before it is sent to the browser: -->
発信応答とともに Cookie が送信されるようにしたいが、その応答のインスタンスがまだない場合は、`Cookie` ファサードを使用して、送信時に応答に添付する Cookie を「キュー」に入れることができます。 `queue` メソッドは、Cookie インスタンスの作成に必要な引数を受け取ります。これらの Cookie は、送信応答がブラウザーに送信される前に添付されます。

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
<!-- #### Generating Cookie Instances -->
#### Generating Cookie Instances

<!-- If you would like to generate a `Symfony\Component\HttpFoundation\Cookie` instance that can be attached to a response instance at a later time, you may use the global `cookie` helper. This cookie will not be sent back to the client unless it is attached to a response instance: -->
後で応答インスタンスにアタッチできる `Symfony\Component\HttpFoundation\Cookie` インスタンスを生成したい場合は、グローバル `cookie` ヘルパを使用できます。この Cookie は、応答インスタンスに添付されない限り、クライアントに送り返されません。

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
<!-- #### Expiring Cookies Early -->
#### Expiring Cookies Early

<!-- You may remove a cookie by expiring it via the `withoutCookie` method of an outgoing response: -->
発信応答の `withoutCookie` メソッドを使用して Cookie を期限切れにすることで、Cookie を削除できます。

```php
return response('Hello World')->withoutCookie('name');
```

<!-- If you do not yet have an instance of the outgoing response, you may use the `Cookie` facade's `expire` method to expire a cookie: -->
発信応答のインスタンスをまだ持っていない場合は、`Cookie` ファサードの `expire` メソッドを使用して Cookie を期限切れにすることができます。

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
<!-- ### Cookies and Encryption -->
### Cookies and Encryption

<!-- By default, thanks to the `Illuminate\Cookie\Middleware\EncryptCookies` middleware, all cookies generated by Laravel are encrypted and signed so that they can't be modified or read by the client. If you would like to disable encryption for a subset of cookies generated by your application, you may use the `encryptCookies` method in your application's `bootstrap/app.php` file: -->
デフォルトでは、`Illuminate\Cookie\Middleware\EncryptCookies` ミドルウェアのおかげで、Laravel によって生成されたすべての Cookie は暗号化および署名され、クライアントによる変更や読み取りができなくなります。アプリケーションによって生成された Cookie のサブセットの暗号化を無効にしたい場合は、アプリケーションの `bootstrap/app.php` ファイルで `encryptCookies` メソッドを使用できます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> 一般に、Cookie の暗号化を無効にしないでください。無効にすると、Cookie がクライアント側のデータ漏洩や改ざんにさらされる可能性があります。

<a name="redirects"></a>
<!-- ## Redirects -->
## Redirects

<!-- Redirect responses are instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL. There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the global `redirect` helper: -->
リダイレクト応答は `Illuminate\Http\RedirectResponse` クラスのインスタンスであり、ユーザーを別の URL にリダイレクトするために必要な適切なヘッダーが含まれています。 `RedirectResponse` インスタンスを生成するには、いくつかの方法があります。最も簡単な方法は、グローバル `redirect` ヘルパを使用することです。

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

<!-- Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/master/session), make sure the route calling the `back` function is using the `web` middleware group: -->
送信されたフォームが無効な場合など、ユーザーを以前の場所にリダイレクトしたい場合があります。これを行うには、グローバル `back` ヘルパ関数を使用します。この機能は [session](/docs/master/session) を利用するため、`back` 関数を呼び出すルートが `web` ミドルウェア グループを使用していることを確認してください。

```php
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
<!-- ### Redirecting to Named Routes -->
### Redirecting to Named Routes

<!-- When you call the `redirect` helper with no parameters, an instance of `Illuminate\Routing\Redirector` is returned, allowing you to call any method on the `Redirector` instance. For example, to generate a `RedirectResponse` to a named route, you may use the `route` method: -->
パラメーターを指定せずに `redirect` ヘルパを呼び出すと、`Illuminate\Routing\Redirector` のインスタンスが返され、`Redirector` インスタンスの任意のメソッドを呼び出すことができます。たとえば、名前付きルートに `RedirectResponse` を生成するには、`route` メソッドを使用できます。

```php
return redirect()->route('login');
```

<!-- If your route has parameters, you may pass them as the second argument to the `route` method: -->
ルートにパラメーターがある場合は、それらを `route` メソッドの 2 番目の引数として渡すことができます。

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
<!-- #### Populating Parameters via Eloquent Models -->
#### Populating Parameters via Eloquent Models

<!-- If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically: -->
Eloquent モデルから設定されている「ID」パラメータを持つルートにリダイレクトしている場合は、モデル自体を渡すことができます。 ID は自動的に抽出されます。

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

<!-- If you would like to customize the value that is placed in the route parameter, you can specify the column in the route parameter definition (`/profile/{id:slug}`) or you can override the `getRouteKey` method on your Eloquent model: -->
ルート パラメーターに配置される値をカスタマイズしたい場合は、ルート パラメーター定義 (`/profile/{id:slug}`) で列を指定するか、Eloquent モデルの `getRouteKey` メソッドをオーバーライドできます。

```php
/**
 * Get the value of the model's route key.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
<!-- ### Redirecting to Controller Actions -->
### Redirecting to Controller Actions

<!-- You may also generate redirects to [controller actions](/docs/master/controllers). To do so, pass the controller and action name to the `action` method: -->
[controller actions](/docs/master/controllers) へのリダイレクトを生成することもできます。これを行うには、コントローラとアクション名を `action` メソッドに渡します。

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

<!-- If your controller route requires parameters, you may pass them as the second argument to the `action` method: -->
コントローラ ルートにパラメーターが必要な場合は、それらを `action` メソッドの 2 番目の引数として渡すことができます。

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
<!-- ### Redirecting to External Domains -->
### Redirecting to External Domains

<!-- Sometimes you may need to redirect to a domain outside of your application. You may do so by calling the `away` method, which creates a `RedirectResponse` without any additional URL encoding, validation, or verification: -->
場合によっては、アプリケーションの外部のドメインにリダイレクトする必要があるかもしれません。これを行うには、`away` メソッドを呼び出して、追加の URL エンコード、検証、または検証を行わずに `RedirectResponse` を作成します。

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
<!-- ### Redirecting With Flashed Session Data -->
### Redirecting With Flashed Session Data

<!-- Redirecting to a new URL and [flashing data to the session](/docs/master/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain: -->
通常、新しい URL へのリダイレクトと [flashing data to the session](/docs/master/session#flash-data) は同時に行われます。通常、これはアクションが正常に実行された後で、成功メッセージをセッションにフラッシュするときに行われます。便宜上、`RedirectResponse` インスタンスを作成し、単一の滑らかなメソッド チェーンでセッションにデータをフラッシュすることができます。

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

<!-- After the user is redirected, you may display the flashed message from the [session](/docs/master/session). For example, using [Blade syntax](/docs/master/blade): -->
ユーザーがリダイレクトされた後、[session](/docs/master/session) からフラッシュされたメッセージを表示できます。たとえば、[Blade syntax](/docs/master/blade) を使用すると、次のようになります。

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
<!-- #### Redirecting With Input -->
#### Redirecting With Input

<!-- You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. This is typically done if the user has encountered a validation error. Once the input has been flashed to the session, you may easily [retrieve it](/docs/master/requests#retrieving-old-input) during the next request to repopulate the form: -->
`RedirectResponse` インスタンスによって提供される `withInput` メソッドを使用して、ユーザーを新しい場所にリダイレクトする前に、現在のリクエストの入力データをセッションにフラッシュできます。これは通常、ユーザーが検証エラーに遭遇した場合に行われます。入力がセッションにフラッシュされると、次のリクエスト中に [retrieve it](/docs/master/requests#retrieving-old-input) を実行してフォームに再入力することが簡単にできます。

```php
return back()->withInput();
```

<a name="other-response-types"></a>
<!-- ## Other Response Types -->
## Other Response Types

<!-- The `response` helper may be used to generate other types of response instances. When the `response` helper is called without arguments, an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/master/contracts) is returned. This contract provides several helpful methods for generating responses. -->
`response` ヘルパは、他のタイプの応答インスタンスを生成するために使用できます。 `response` ヘルパが引数なしで呼び出されると、`Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/master/contracts) の実装が返されます。この規約は、応答を生成するためのいくつかの便利な方法を提供します。

<a name="view-responses"></a>
<!-- ### View Responses -->
### View Responses

<!-- If you need control over the response's status and headers but also need to return a [view](/docs/master/views) as the response's content, you should use the `view` method: -->
応答のステータスとヘッダーを制御する必要があるが、応答のコンテンツとして [view](/docs/master/views) を返す必要がある場合は、`view` メソッドを使用する必要があります。

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

<!-- Of course, if you do not need to pass a custom HTTP status code or custom headers, you may use the global `view` helper function. -->
もちろん、カスタム HTTP ステータス コードやカスタム ヘッダーを渡す必要がない場合は、グローバル `view` ヘルパ関数を使用できます。

<a name="json-responses"></a>
<!-- ### JSON Responses -->
### JSON Responses

<!-- The `json` method will automatically set the `Content-Type` header to `application/json`, as well as convert the given array to JSON using the `json_encode` PHP function: -->
`json` メソッドは、`Content-Type` ヘッダーを `application/json` に自動的に設定し、`json_encode` PHP 関数を使用して指定された配列を JSON に変換します。

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

<!-- If you would like to create a JSONP response, you may use the `json` method in combination with the `withCallback` method: -->
JSONP 応答を作成したい場合は、`json` メソッドを `withCallback` メソッドと組み合わせて使用​​できます。

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
<!-- ### File Downloads -->
### File Downloads

<!-- The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method: -->
`download` メソッドは、ユーザーのブラウザに指定されたパスにファイルをダウンロードさせる応答を生成するために使用できます。 `download` メソッドは、メソッドの 2 番目の引数としてファイル名を受け入れます。これにより、ファイルをダウンロードするユーザーに表示されるファイル名が決まります。最後に、HTTP ヘッダーの配列を 3 番目の引数としてメソッドに渡すことができます。

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> ファイルのダウンロードを管理する Symfony HttpFoundation では、ダウンロードされるファイルに ASCII ファイル名が付いている必要があります。

<a name="file-responses"></a>
<!-- ### File Responses -->
### File Responses

<!-- The `file` method may be used to display a file, such as an image or PDF, directly in the user's browser instead of initiating a download. This method accepts the absolute path to the file as its first argument and an array of headers as its second argument: -->
`file` メソッドは、ダウンロードを開始する代わりに、画像や PDF などのファイルをユーザーのブラウザーに直接表示するために使用できます。このメソッドは、ファイルへの絶対パスを最初の引数として受け入れ、ヘッダーの配列を 2 番目の引数として受け入れます。

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
<!-- ## Streamed Responses -->
## Streamed Responses

<!-- By streaming data to the client as it is generated, you can significantly reduce memory usage and improve performance, especially for very large responses. Streamed responses allow the client to begin processing data before the server has finished sending it: -->
データの生成時にクライアントにデータをストリーミングすることで、特に非常に大規模な応答の場合、メモリ使用量を大幅に削減し、パフォーマンスを向上させることができます。ストリーミング応答を使用すると、サーバーがデータの送信を完了する前に、クライアントがデータの処理を開始できます。

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // Simulate delay between chunks...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```

<!-- For convenience, if the closure you provide to the `stream` method returns a [Generator](https://www.php.net/manual/en/language.generators.overview.php), Laravel will automatically flush the output buffer between strings returned by the generator, as well as disable Nginx output buffering: -->
便宜上、`stream` メソッドに指定したクロージャが [Generator](https://www.php.net/manual/en/language.generators.overview.php) を返す場合、Laravel はジェネレーターによって返された文字列間の出力バッファを自動的にフラッシュし、Nginx の出力バッファリングを無効にします。

```php
Route::post('/chat', function () {
    return response()->stream(function (): Generator {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

<a name="consuming-streamed-responses"></a>
<!-- ### Consuming Streamed Responses -->
### Consuming Streamed Responses

<!-- Streamed responses may be consumed using Laravel's `stream` npm package, which provides a convenient API for interacting with Laravel response and event streams. To get started, install the `@laravel/stream-react` or `@laravel/stream-vue` package: -->
ストリーミングされた応答は、Laravel の `stream` npm パッケージを使用して消費できます。これは、Laravel 応答およびイベント ストリームと対話するための便利な API を提供します。まず、`@laravel/stream-react` または `@laravel/stream-vue` パッケージをインストールします。

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

<!-- Then, `useStream` may be used to consume the event stream. After providing your stream URL, the hook will automatically update the `data` with the concatenated response as content is returned from your Laravel application: -->
次に、`useStream` を使用してイベント ストリームを消費できます。ストリーム URL を指定すると、Laravel アプリケーションからコンテンツが返されると、フックは連結された応答で `data` を自動的に更新します。

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, isFetching, isStreaming, send } = useStream("chat");

    const sendMessage = () => {
        send({
            message: `Current timestamp: ${Date.now()}`,
        });
    };

    return (
        <div>
            <div>{data}</div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
            <button onClick={sendMessage}>Send Message</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, isFetching, isStreaming, send } = useStream("chat");

const sendMessage = () => {
    send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
        <button @click="sendMessage">Send Message</button>
    </div>
</template>
```

<!-- When sending data back to the stream via `send`, the active connection to the stream is canceled before sending the new data. All requests are sent as JSON `POST` requests. -->
`send` 経由でデータをストリームに送り返すと、新しいデータを送信する前にストリームへのアクティブな接続がキャンセルされます。すべてのリクエストは JSON `POST` リクエストとして送信されます。

> [!WARNING]
> `useStream` フックはアプリケーションに対して `POST` リクエストを行うため、有効な CSRF トークンが必要です。 CSRF トークンを提供する最も簡単な方法は、[include it via a meta tag in your application layout's head](/docs/master/csrf#csrf-x-csrf-token) です。

<!-- The second argument given to `useStream` is an options object that you may use to customize the stream consumption behavior. The default values for this object are shown below: -->
`useStream` に指定される 2 番目の引数は、ストリーム消費動作をカスタマイズするために使用できるオプション オブジェクトです。このオブジェクトのデフォルト値を以下に示します。

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        id: undefined,
        initialInput: undefined,
        headers: undefined,
        csrfToken: undefined,
        onResponse: (response: Response) => void,
        onData: (data: string) => void,
        onCancel: () => void,
        onFinish: () => void,
        onError: (error: Error) => void,
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response: Response) => void,
    onData: (data: string) => void,
    onCancel: () => void,
    onFinish: () => void,
    onError: (error: Error) => void,
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

<!-- `onResponse` is triggered after a successful initial response from the stream and the raw [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) is passed to the callback. `onData` is called as each chunk is received - the current chunk is passed to the callback. `onFinish` is called when a stream has finished and when an error is thrown during the fetch / read cycle. -->
`onResponse` は、ストリームからの初期応答が成功した後にトリガーされ、生の [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) がコールバックに渡されます。各チャンクが受信されると、`onData` が呼び出され、現在のチャンクがコールバックに渡されます。 `onFinish` は、ストリームが終了したとき、およびフェッチ/読み取りサイクル中にエラーがスローされたときに呼び出されます。

<!-- By default, a request is not made to the stream on initialization. You may pass an initial payload to the stream by using the `initialInput` option: -->
デフォルトでは、初期化時にストリームに対してリクエストは行われません。 `initialInput` オプションを使用して、初期ペイロードをストリームに渡すことができます。

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        initialInput: {
            message: "Introduce yourself.",
        },
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

<!-- To cancel a stream manually, you may use the `cancel` method returned from the hook: -->
ストリームを手動でキャンセルするには、フックから返された `cancel` メソッドを使用できます。

```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, cancel } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <button onClick={cancel}>Cancel</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, cancel } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <button @click="cancel">Cancel</button>
    </div>
</template>
```

<!-- Each time the `useStream` hook is used, a random `id` is generated to identify the stream. This is sent back to the server with each request in the `X-STREAM-ID` header. When consuming the same stream from multiple components, you can read and write to the stream by providing your own `id`: -->
`useStream` フックが使用されるたびに、ストリームを識別するためにランダムな `id` が生成されます。これは、`X-STREAM-ID` ヘッダー内の各リクエストとともにサーバーに返送されます。複数のコンポーネントから同じストリームを使用する場合、独自の `id` を提供することで、ストリームの読み取りと書き込みを行うことができます。

```tsx tab=React
// App.tsx
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, id } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <StreamStatus id={id} />
        </div>
    );
}

// StreamStatus.tsx
import { useStream } from "@laravel/stream-react";

function StreamStatus({ id }) {
    const { isFetching, isStreaming } = useStream("chat", { id });

    return (
        <div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
        </div>
    );
}
```

```vue tab=Vue
<!-- App.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";
import StreamStatus from "./StreamStatus.vue";

const { data, id } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <StreamStatus :id="id" />
    </div>
</template>

<!-- StreamStatus.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const props = defineProps<{
    id: string;
}>();

const { isFetching, isStreaming } = useStream("chat", { id: props.id });
</script>

<template>
    <div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
    </div>
</template>
```

<a name="streamed-json-responses"></a>
<!-- ### Streamed JSON Responses -->
### Streamed JSON Responses

<!-- If you need to stream JSON data incrementally, you may utilize the `streamJson` method. This method is especially useful for large datasets that need to be sent progressively to the browser in a format that can be easily parsed by JavaScript: -->
JSON データを段階的にストリーミングする必要がある場合は、`streamJson` メソッドを利用できます。この方法は、JavaScript で簡単に解析できる形式でブラウザに段階的に送信する必要がある大規模なデータセットに特に役立ちます。

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

<!-- The `useJsonStream` hook is identical to the [useStream hook](#consuming-streamed-responses) except that it will attempt to parse the data as JSON once it has finished streaming: -->
`useJsonStream` フックは、ストリーミング終了後にデータを JSON として解析しようとする点を除いて、[useStream hook](#consuming-streamed-responses) と同じです。

```tsx tab=React
import { useJsonStream } from "@laravel/stream-react";

type User = {
    id: number;
    name: string;
    email: string;
};

function App() {
    const { data, send } = useJsonStream<{ users: User[] }>("users");

    const loadUsers = () => {
        send({
            query: "taylor",
        });
    };

    return (
        <div>
            <ul>
                {data?.users.map((user) => (
                    <li>
                        {user.id}: {user.name}
                    </li>
                ))}
            </ul>
            <button onClick={loadUsers}>Load Users</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useJsonStream } from "@laravel/stream-vue";

type User = {
    id: number;
    name: string;
    email: string;
};

const { data, send } = useJsonStream<{ users: User[] }>("users");

const loadUsers = () => {
    send({
        query: "taylor",
    });
};
</script>

<template>
    <div>
        <ul>
            <li v-for="user in data?.users" :key="user.id">
                {{ user.id }}: {{ user.name }}
            </li>
        </ul>
        <button @click="loadUsers">Load Users</button>
    </div>
</template>
```

<a name="event-streams"></a>
<!-- ### Event Streams (SSE) -->
### Event Streams (SSE)

<!-- The `eventStream` method may be used to return a server-sent events (SSE) streamed response using the `text/event-stream` content type. The `eventStream` method accepts a closure which should [yield](https://www.php.net/manual/en/language.generators.overview.php) responses to the stream as the responses become available: -->
`eventStream` メソッドは、`text/event-stream` コンテンツ タイプを使用してサーバー送信イベント (SSE) ストリーミング応答を返すために使用できます。 `eventStream` メソッドは、応答が利用可能になったときに [yield](https://www.php.net/manual/en/language.generators.overview.php) がストリームに応答する必要があるクロージャを受け入れます。

```php
Route::get('/chat', function () {
    return response()->eventStream(function () {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```

<!-- If you would like to customize the name of the event, you may yield an instance of the `StreamedEvent` class: -->
イベントの名前をカスタマイズしたい場合は、`StreamedEvent` クラスのインスタンスを生成します。

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
<!-- #### Consuming Event Streams -->
#### Consuming Event Streams

<!-- Event streams may be consumed using Laravel's `stream` npm package, which provides a convenient API for interacting with Laravel event streams. To get started, install the `@laravel/stream-react` or `@laravel/stream-vue` package: -->
イベントストリームは、Laravelの`stream` npmパッケージを使用して消費できます。これは、Laravelイベントストリームと対話するための便利なAPIを提供します。まず、`@laravel/stream-react` または `@laravel/stream-vue` パッケージをインストールします。

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

<!-- Then, `useEventStream` may be used to consume the event stream. After providing your stream URL, the hook will automatically update the `message` with the concatenated response as messages are returned from your Laravel application: -->
次に、`useEventStream` を使用してイベント ストリームを消費できます。ストリーム URL を指定すると、Laravel アプリケーションからメッセージが返されると、フックは連結された応答で `message` を自動的に更新します。

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/chat");

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat");
</script>

<template>
  <div>{{ message }}</div>
</template>
```

<!-- The second argument given to `useEventStream` is an options object that you may use to customize the stream consumption behavior. The default values for this object are shown below: -->
`useEventStream` に指定される 2 番目の引数は、ストリーム消費動作をカスタマイズするために使用できるオプション オブジェクトです。このオブジェクトのデフォルト値を以下に示します。

```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/stream", {
    eventName: "update",
    onMessage: (message) => {
      //
    },
    onError: (error) => {
      //
    },
    onComplete: () => {
      //
    },
    endSignal: "</stream>",
    glue: " ",
  });

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat", {
  eventName: "update",
  onMessage: (message) => {
    // ...
  },
  onError: (error) => {
    // ...
  },
  onComplete: () => {
    // ...
  },
  endSignal: "</stream>",
  glue: " ",
});
</script>
```

<!-- Event streams may also be manually consumed via an [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) object by your application's frontend. The `eventStream` method will automatically send a `</stream>` update to the event stream when the stream is complete: -->
イベント ストリームは、アプリケーションのフロントエンドによって [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) オブジェクトを介して手動で使用することもできます。 `eventStream` メソッドは、ストリームが完了すると、イベント ストリームに `</stream>` 更新を自動的に送信します。

```js
const source = new EventSource('/chat');

source.addEventListener('update', (event) => {
    if (event.data === '</stream>') {
        source.close();

        return;
    }

    console.log(event.data);
});
```

<!-- To customize the final event that is sent to the event stream, you may provide a `StreamedEvent` instance to the `eventStream` method's `endStreamWith` argument: -->
イベント ストリームに送信される最終イベントをカスタマイズするには、`StreamedEvent` インスタンスを `eventStream` メソッドの `endStreamWith` 引数に指定します。

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
<!-- ### Streamed Downloads -->
### Streamed Downloads

<!-- Sometimes you may wish to turn the string response of a given operation into a downloadable response without having to write the contents of the operation to disk. You may use the `streamDownload` method in this scenario. This method accepts a callback, filename, and an optional array of headers as its arguments: -->
場合によっては、操作の内容をディスクに書き込むことなく、特定の操作の文字列応答をダウンロード可能な応答に変換したい場合があります。このシナリオでは、`streamDownload` メソッドを使用できます。このメソッドは、コールバック、ファイル名、およびオプションのヘッダー配列を引数として受け取ります。

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="response-macros"></a>
<!-- ## Response Macros -->
## Response Macros

<!-- If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on the `Response` facade. Typically, you should call this method from the `boot` method of one of your application's [service providers](/docs/master/providers), such as the `App\Providers\AppServiceProvider` service provider: -->
さまざまなルートやコントローラで再利用できるカスタム応答を定義したい場合は、`Response` ファサードで `macro` メソッドを使用できます。通常、このメソッドは、アプリケーションの [service providers](/docs/master/providers) の 1 つ (`App\Providers\AppServiceProvider` サービスプロバイダなど) の `boot` メソッドから呼び出す必要があります。

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

<!-- The `macro` function accepts a name as its first argument and a closure as its second argument. The macro's closure will be executed when calling the macro name from a `ResponseFactory` implementation or the `response` helper: -->
`macro` 関数は、最初の引数として名前を受け入れ、2 番目の引数としてクロージャーを受け入れます。マクロのクロージャーは、`ResponseFactory` 実装または `response` ヘルパからマクロ名を呼び出すときに実行されます。

```php
return response()->caps('foo');
```

