# HTTP 応答 (HTTP Responses)

- [応答の作成](#creating-responses)
    - [応答にヘッダーを添付する](#attaching-headers-to-responses)
    - [応答に Cookie を添付する](#attaching-cookies-to-responses)
    - [Cookie と暗号化](#cookies-and-encryption)
- [Redirects](#redirects)
    - [名前付きルートへのリダイレクト](#redirecting-named-routes)
    - [コントローラアクションへのリダイレクト](#redirecting-controller-actions)
    - [外部ドメインへのリダイレクト](#redirecting-external-domains)
    - [フラッシュされたセッション データによるリダイレクト](#redirecting-with-flashed-session-data)
- [他の応答タイプ](#other-response-types)
    - [回答を見る](#view-responses)
    - [JSON 応答](#json-responses)
    - [ファイルのダウンロード](#file-downloads)
    - [ファイル応答](#file-responses)
- [ストリーミングされた応答](#streamed-responses)
    - [ストリーミングされた応答の消費](#consuming-streamed-responses)
    - [ストリーミングされた JSON 応答](#streamed-json-responses)
    - [イベントストリーム (SSE)](#event-streams)
    - [ストリーミングダウンロード](#streamed-downloads)
- [応答マクロ](#response-macros)

<a name="creating-responses"></a>
## 応答の作成 (Creating Responses)

<a name="strings-arrays"></a>
#### 文字列と配列

すべてのルートとコントローラは、ユーザーのブラウザーに送り返される応答を返す必要があります。 Laravel は、応答を返すためのいくつかの異なる方法を提供します。最も基本的な応答は、ルートまたはコントローラから文字列を返すことです。フレームワークは、文字列を完全な HTTP 応答に自動的に変換します。

```php
Route::get('/', function () {
    return 'Hello World';
});
```

ルートやコントローラから文字列を返すだけでなく、配列を返すこともできます。フレームワークは配列を JSON 応答に自動的に変換します。

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> ルートまたはコントローラから [Eloquent コレクション](/docs/{{version}}/eloquent-collections) を返すこともできることをご存知ですか?これらは自動的に JSON に変換されます。試してみてください!

<a name="response-objects"></a>
#### 応答オブジェクト

通常、ルート アクションから単純な文字列や配列を返すだけではありません。代わりに、完全な `Illuminate\Http\Response` インスタンスまたは [views](/docs/{{version}}/views) を返します。

完全な `Response` インスタンスを返すと、応答の HTTP ステータス コードとヘッダーをカスタマイズできます。 `Response` インスタンスは、HTTP 応答を構築するためのさまざまなメソッドを提供する `Symfony\Component\HttpFoundation\Response` クラスを継承します。

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
#### Eloquent モデルとコレクション

[Eloquent ORM](/docs/{{version}}/eloquent) モデルとコレクションをルートとコントローラから直接返すこともできます。これを行うと、Laravel はモデルの [隠し属性](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) を尊重しながら、モデルとコレクションを JSON 応答に自動的に変換します。

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
### 応答にヘッダーを添付する

ほとんどの応答メソッドはチェーン可能であり、応答インスタンスをスムーズに構築できることに留意してください。たとえば、`header` メソッドを使用して、応答をユーザーに送り返す前に一連のヘッダーを応答に追加できます。

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

または、`withHeaders` メソッドを使用して、応答に追加するヘッダーの配列を指定することもできます。

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

`withoutHeader` メソッドを使用して、送信応答から特定のヘッダーを削除できます。

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

<a name="cache-control-middleware"></a>
#### キャッシュ制御ミドルウェア

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
### 応答に Cookie を添付する

`cookie` メソッドを使用して、発信 `Illuminate\Http\Response` インスタンスに Cookie を添付できます。名前、値、Cookie が有効であるとみなされる分数をこのメソッドに渡す必要があります。

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

`cookie` メソッドは、使用頻度は低いですが、さらにいくつかの引数も受け入れます。一般に、これらの引数は、PHP のネイティブ [setcookie](https://secure.php.net/manual/en/function.setcookie.php) メソッドに与えられる引数と同じ目的と意味を持ちます。

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

発信応答とともに Cookie が送信されるようにしたいが、その応答のインスタンスがまだない場合は、`Cookie` ファサードを使用して、送信時に応答に添付する Cookie を「キュー」に入れることができます。 `queue` メソッドは、Cookie インスタンスの作成に必要な引数を受け取ります。これらの Cookie は、送信応答がブラウザーに送信される前に添付されます。

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
#### Cookie インスタンスの生成

後で応答インスタンスにアタッチできる `Symfony\Component\HttpFoundation\Cookie` インスタンスを生成したい場合は、グローバル `cookie` ヘルパを使用できます。この Cookie は、応答インスタンスに添付されない限り、クライアントに送り返されません。

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
#### Cookie の期限切れを早める

発信応答の `withoutCookie` メソッドを使用して Cookie を期限切れにすることで、Cookie を削除できます。

```php
return response('Hello World')->withoutCookie('name');
```

発信応答のインスタンスをまだ持っていない場合は、`Cookie` ファサードの `expire` メソッドを使用して Cookie を期限切れにすることができます。

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
### Cookie と暗号化

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
## リダイレクト (Redirects)

リダイレクト応答は `Illuminate\Http\RedirectResponse` クラスのインスタンスであり、ユーザーを別の URL にリダイレクトするために必要な適切なヘッダーが含まれています。 `RedirectResponse` インスタンスを生成するには、いくつかの方法があります。最も簡単な方法は、グローバル `redirect` ヘルパを使用することです。

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

送信されたフォームが無効な場合など、ユーザーを以前の場所にリダイレクトしたい場合があります。これを行うには、グローバル `back` ヘルパ関数を使用します。この機能は [session](/docs/{{version}}/session) を利用するため、`back` 関数を呼び出すルートが `web` ミドルウェア グループを使用していることを確認してください。

```php
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
### 名前付きルートへのリダイレクト

パラメーターを指定せずに `redirect` ヘルパを呼び出すと、`Illuminate\Routing\Redirector` のインスタンスが返され、`Redirector` インスタンスの任意のメソッドを呼び出すことができます。たとえば、名前付きルートに `RedirectResponse` を生成するには、`route` メソッドを使用できます。

```php
return redirect()->route('login');
```

ルートにパラメーターがある場合は、それらを `route` メソッドの 2 番目の引数として渡すことができます。

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent モデルを介したパラメーターの入力

Eloquent モデルから設定されている「ID」パラメータを持つルートにリダイレクトしている場合は、モデル自体を渡すことができます。 ID は自動的に抽出されます。

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

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
### コントローラアクションへのリダイレクト

[コントローラのアクション](/docs/{{version}}/controllers) へのリダイレクトを生成することもできます。これを行うには、コントローラとアクション名を `action` メソッドに渡します。

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

コントローラ ルートにパラメーターが必要な場合は、それらを `action` メソッドの 2 番目の引数として渡すことができます。

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
### 外部ドメインへのリダイレクト

場合によっては、アプリケーションの外部のドメインにリダイレクトする必要があるかもしれません。これを行うには、`away` メソッドを呼び出して、追加の URL エンコード、検証、または検証を行わずに `RedirectResponse` を作成します。

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
### フラッシュされたセッション データによるリダイレクト

通常、新しい URL へのリダイレクトと [セッションにデータをフラッシュする](/docs/{{version}}/session#flash-data) は同時に行われます。通常、これはアクションが正常に実行された後で、成功メッセージをセッションにフラッシュするときに行われます。便宜上、`RedirectResponse` インスタンスを作成し、単一の滑らかなメソッド チェーンでセッションにデータをフラッシュすることができます。

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

ユーザーがリダイレクトされた後、[session](/docs/{{version}}/session) からフラッシュされたメッセージを表示できます。たとえば、[Blade 構文](/docs/{{version}}/blade) を使用すると、次のようになります。

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
#### 入力によるリダイレクト

`RedirectResponse` インスタンスによって提供される `withInput` メソッドを使用して、ユーザーを新しい場所にリダイレクトする前に、現在のリクエストの入力データをセッションにフラッシュできます。これは通常、ユーザーが検証エラーに遭遇した場合に行われます。入力がセッションにフラッシュされると、次のリクエスト中に [それを取得します](/docs/{{version}}/requests#retrieving-old-input) を実行してフォームに再入力することが簡単にできます。

```php
return back()->withInput();
```

<a name="other-response-types"></a>
## 他の応答タイプ (Other Response Types)

`response` ヘルパは、他のタイプの応答インスタンスを生成するために使用できます。 `response` ヘルパが引数なしで呼び出されると、`Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/{{version}}/contracts) の実装が返されます。この規約は、応答を生成するためのいくつかの便利な方法を提供します。

<a name="view-responses"></a>
### 回答を見る

応答のステータスとヘッダーを制御する必要があるが、応答のコンテンツとして [view](/docs/{{version}}/views) を返す必要がある場合は、`view` メソッドを使用する必要があります。

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

もちろん、カスタム HTTP ステータス コードやカスタム ヘッダーを渡す必要がない場合は、グローバル `view` ヘルパ関数を使用できます。

<a name="json-responses"></a>
### JSON 応答

`json` メソッドは、`Content-Type` ヘッダーを `application/json` に自動的に設定し、`json_encode` PHP 関数を使用して指定された配列を JSON に変換します。

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

JSONP 応答を作成したい場合は、`json` メソッドを `withCallback` メソッドと組み合わせて使用​​できます。

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
### ファイルのダウンロード

`download` メソッドは、ユーザーのブラウザに指定されたパスにファイルをダウンロードさせる応答を生成するために使用できます。 `download` メソッドは、メソッドの 2 番目の引数としてファイル名を受け入れます。これにより、ファイルをダウンロードするユーザーに表示されるファイル名が決まります。最後に、HTTP ヘッダーの配列を 3 番目の引数としてメソッドに渡すことができます。

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> ファイルのダウンロードを管理する Symfony HttpFoundation では、ダウンロードされるファイルに ASCII ファイル名が付いている必要があります。

<a name="file-responses"></a>
### ファイル応答

`file` メソッドは、ダウンロードを開始する代わりに、画像や PDF などのファイルをユーザーのブラウザーに直接表示するために使用できます。このメソッドは、ファイルへの絶対パスを最初の引数として受け入れ、ヘッダーの配列を 2 番目の引数として受け入れます。

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
## ストリーミングされた応答 (Streamed Responses)

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
### ストリーミングされた応答の消費

ストリーミングされた応答は、Laravel の `stream` npm パッケージを使用して消費できます。これは、Laravel 応答およびイベント ストリームと対話するための便利な API を提供します。まず、`@laravel/stream-react`、`@laravel/stream-vue`、または `@laravel/stream-svelte` パッケージをインストールします。

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```

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

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");

const sendMessage = () => {
    stream.send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<div>
    <div>{$stream.data}</div>
    {#if $stream.isFetching}
        <div>Connecting...</div>
    {/if}
    {#if $stream.isStreaming}
        <div>Generating...</div>
    {/if}
    <button onclick={sendMessage}>Send Message</button>
</div>
```

`send` 経由でデータをストリームに送り返すと、新しいデータを送信する前にストリームへのアクティブな接続がキャンセルされます。すべてのリクエストは JSON `POST` リクエストとして送信されます。

> [!WARNING]
> `useStream` フックはアプリケーションに対して `POST` リクエストを行うため、有効な CSRF トークンが必要です。 CSRF トークンを提供する最も簡単な方法は、[アプリケーションレイアウトのヘッドにメタタグを介して含めます](/docs/{{version}}/csrf#csrf-x-csrf-token) です。

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

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response) => {},
    onData: (data) => {},
    onCancel: () => {},
    onFinish: () => {},
    onError: (error) => {},
});
</script>

<div>{$stream.data}</div>
```

`onResponse` は、ストリームからの初期応答が成功した後にトリガーされ、生の [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) がコールバックに渡されます。各チャンクが受信されると、`onData` が呼び出され、現在のチャンクがコールバックに渡されます。 `onFinish` は、ストリームが終了したとき、およびフェッチ/読み取りサイクル中にエラーがスローされたときに呼び出されます。

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

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<div>{$stream.data}</div>
```

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

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");
</script>

<div>
    <div>{$stream.data}</div>
    <button onclick={() => stream.cancel()}>Cancel</button>
</div>
```

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

```svelte tab=Svelte
<!-- App.svelte -->
<script>
import { useStream } from "@laravel/stream-svelte";
import StreamStatus from "./StreamStatus.svelte";

const stream = useStream("chat");
</script>

<div>
    <div>{$stream.data}</div>
    <StreamStatus id={stream.id} />
</div>

<!-- StreamStatus.svelte -->
<script>
import { useStream } from "@laravel/stream-svelte";

let { id } = $props();

const stream = useStream("chat", { id });
</script>

<div>
    {#if $stream.isFetching}
        <div>Connecting...</div>
    {/if}
    {#if $stream.isStreaming}
        <div>Generating...</div>
    {/if}
</div>
```

<a name="streamed-json-responses"></a>
### ストリーミングされた JSON 応答

JSON データを段階的にストリーミングする必要がある場合は、`streamJson` メソッドを利用できます。この方法は、JavaScript で簡単に解析できる形式でブラウザに段階的に送信する必要がある大規模なデータセットに特に役立ちます。

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

`useJsonStream` フックは、ストリーミング終了後にデータを JSON として解析しようとする点を除いて、[useStreamフック](#consuming-streamed-responses) と同じです。

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

```svelte tab=Svelte
<script>
import { useJsonStream } from "@laravel/stream-svelte";

const stream = useJsonStream("users");

const loadUsers = () => {
    stream.send({
        query: "taylor",
    });
};
</script>

<div>
    <ul>
        {#if $stream.data?.users}
            {#each $stream.data.users as user (user.id)}
                <li>{user.id}: {user.name}</li>
            {/each}
        {/if}
    </ul>
    <button onclick={loadUsers}>Load Users</button>
</div>
```

<a name="event-streams"></a>
### イベントストリーム (SSE)

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

イベントの名前をカスタマイズしたい場合は、`StreamedEvent` クラスのインスタンスを生成します。

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```

<a name="consuming-event-streams"></a>
#### イベントストリームの消費

イベントストリームは、Laravelの`stream` npmパッケージを使用して消費できます。これは、Laravelイベントストリームと対話するための便利なAPIを提供します。まず、`@laravel/stream-react`、`@laravel/stream-vue`、または `@laravel/stream-svelte` パッケージをインストールします。

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```

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

```svelte tab=Svelte
<script>
import { useEventStream } from "@laravel/stream-svelte";

const eventStream = useEventStream("/chat");
</script>

<div>{$eventStream.message}</div>
```

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

```svelte tab=Svelte
<script>
import { useEventStream } from "@laravel/stream-svelte";

const eventStream = useEventStream("/chat", {
    eventName: "update",
    onMessage: (event) => {
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
    replace: false,
});
</script>
```

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

イベント ストリームに送信される最終イベントをカスタマイズするには、`StreamedEvent` インスタンスを `eventStream` メソッドの `endStreamWith` 引数に指定します。

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
### ストリーミングダウンロード

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
## 応答マクロ (Response Macros)

さまざまなルートやコントローラで再利用できるカスタム応答を定義したい場合は、`Response` ファサードで `macro` メソッドを使用できます。通常、このメソッドは、アプリケーションの [サービスプロバイダ](/docs/{{version}}/providers) の 1 つ (`App\Providers\AppServiceProvider` サービスプロバイダなど) の `boot` メソッドから呼び出す必要があります。

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

`macro` 関数は、最初の引数として名前を受け入れ、2 番目の引数としてクロージャーを受け入れます。マクロのクロージャーは、`ResponseFactory` 実装または `response` ヘルパからマクロ名を呼び出すときに実行されます。

```php
return response()->caps('foo');
```

