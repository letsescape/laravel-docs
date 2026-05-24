# HTTPリクエスト (HTTP Requests)

- [Introduction](#introduction)
- [リクエストの操作](#interacting-with-the-request)
    - [リクエストへのアクセス](#accessing-the-request)
    - [リクエストのパス、ホスト、およびメソッド](#request-path-and-method)
    - [リクエストヘッダー](#request-headers)
    - [リクエストIPアドレス](#request-ip-address)
    - [コンテンツのネゴシエーション](#content-negotiation)
    - [PSR-7 リクエスト](#psr7-requests)
- [Input](#input)
    - [入力の取得](#retrieving-input)
    - [入力の有無](#input-presence)
    - [追加入力のマージ](#merging-additional-input)
    - [古い入力](#old-input)
    - [Cookies](#cookies)
    - [入力トリミングと正規化](#input-trimming-and-normalization)
- [Files](#files)
    - [アップロードされたファイルの取得](#retrieving-uploaded-files)
    - [アップロードしたファイルの保存](#storing-uploaded-files)
- [信頼できるプロキシの構成](#configuring-trusted-proxies)
- [信頼できるホストの構成](#configuring-trusted-hosts)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel の `Illuminate\Http\Request` クラスは、アプリケーションによって処理されている現在の HTTP リクエストと対話し、リクエストとともに送信された入力、Cookie、およびファイルを取得するためのオブジェクト指向の方法を提供します。

<a name="interacting-with-the-request"></a>
## リクエストの操作 (Interacting With The Request)

<a name="accessing-the-request"></a>
### リクエストへのアクセス

依存注入を通じて現在の HTTP リクエストのインスタンスを取得するには、ルート クロージャーまたはコントローラ メソッドで `Illuminate\Http\Request` クラスをタイプヒントする必要があります。受信リクエストのインスタンスは、Laravel [サービスコンテナ](/docs/{{version}}/container) によって自動的に挿入されます。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * Store a new user.
         */
        public function store(Request $request): RedirectResponse
        {
            $name = $request->input('name');

            // Store the user...

            return redirect('/users');
        }
    }

前述したように、ルート クロージャで `Illuminate\Http\Request` クラスをタイプヒントで指定することもできます。サービスコンテナは、実行時に受信リクエストを自動的にクロージャに挿入します。

    use Illuminate\Http\Request;

    Route::get('/', function (Request $request) {
        // ...
    });

<a name="dependency-injection-route-parameters"></a>
#### 依存関係の注入とルート パラメーター

コントローラ メソッドがルート パラメーターからの入力も期待している場合は、他の依存関係の後にルート パラメーターをリストする必要があります。たとえば、ルートが次のように定義されているとします。

    use App\Http\Controllers\UserController;

    Route::put('/user/{id}', [UserController::class, 'update']);

次のようにコントローラ メソッドを定義することで、`Illuminate\Http\Request` をタイプヒントして `id` ルート パラメーターにアクセスすることもできます。

    <?php

    namespace App\Http\Controllers;

    use Illuminate\Http\RedirectResponse;
    use Illuminate\Http\Request;

    class UserController extends Controller
    {
        /**
         * Update the specified user.
         */
        public function update(Request $request, string $id): RedirectResponse
        {
            // Update the user...

            return redirect('/users');
        }
    }

<a name="request-path-and-method"></a>
### リクエストのパス、ホスト、およびメソッド

`Illuminate\Http\Request` インスタンスは、受信 HTTP リクエストを検査するためのさまざまなメソッドを提供し、`Symfony\Component\HttpFoundation\Request` クラスを拡張します。以下では、最も重要な方法のいくつかについて説明します。

<a name="retrieving-the-request-path"></a>
#### リクエストパスの取得

`path` メソッドは、リクエストのパス情報を返します。したがって、受信リクエストが `http://example.com/foo/bar` をターゲットにしている場合、`path` メソッドは `foo/bar` を返します。

    $uri = $request->path();

<a name="inspecting-the-request-path"></a>
#### リクエストのパス/ルートの検査

`is` メソッドを使用すると、受信リクエストのパスが指定されたパターンと一致することを確認できます。この方法を使用する場合は、`*` 文字をワイルドカードとして使用できます。

    if ($request->is('admin/*')) {
        // ...
    }

`routeIs` メソッドを使用すると、受信リクエストが [名前付きルート](/docs/{{version}}/routing#named-routes) と一致したかどうかを判断できます。

    if ($request->routeIs('admin.*')) {
        // ...
    }

<a name="retrieving-the-request-url"></a>
#### リクエストURLの取得

受信リクエストの完全な URL を取得するには、`url` メソッドまたは `fullUrl` メソッドを使用できます。 `url` メソッドはクエリ文字列なしで URL を返しますが、`fullUrl` メソッドにはクエリ文字列が含まれます。

    $url = $request->url();

    $urlWithQueryString = $request->fullUrl();

現在の URL にクエリ文字列データを追加したい場合は、`fullUrlWithQuery` メソッドを呼び出すことができます。このメソッドは、指定されたクエリ文字列変数の配列を現在のクエリ文字列とマージします。

    $request->fullUrlWithQuery(['type' => 'phone']);

特定のクエリ文字列パラメータを指定せずに現在の URL を取得したい場合は、`fullUrlWithoutQuery` メソッドを利用できます。

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### リクエストホストの取得

受信リクエストの「ホスト」は、`host`、`httpHost`、および `schemeAndHttpHost` メソッドを介して取得できます。

    $request->host();
    $request->httpHost();
    $request->schemeAndHttpHost();

<a name="retrieving-the-request-method"></a>
#### リクエストメソッドの取得

`method` メソッドは、リクエストの HTTP 動詞を返します。 `isMethod` メソッドを使用して、HTTP 動詞が指定された文字列と一致することを確認できます。

    $method = $request->method();

    if ($request->isMethod('post')) {
        // ...
    }

<a name="request-headers"></a>
### リクエストヘッダー

`header` メソッドを使用して、`Illuminate\Http\Request` インスタンスからリクエスト ヘッダーを取得できます。リクエストにヘッダーが存在しない場合は、`null` が返されます。ただし、`header` メソッドは、リクエストにヘッダーが存在しない場合に返されるオプションの 2 番目の引数を受け入れます。

    $value = $request->header('X-Header-Name');

    $value = $request->header('X-Header-Name', 'default');

`hasHeader` メソッドを使用して、リクエストに特定のヘッダーが含まれているかどうかを判断できます。

    if ($request->hasHeader('X-Header-Name')) {
        // ...
    }

便宜上、`bearerToken` メソッドを使用して、`Authorization` ヘッダーからベアラー トークンを取得できます。そのようなヘッダーが存在しない場合は、空の文字列が返されます。

    $token = $request->bearerToken();

<a name="request-ip-address"></a>
### リクエストIPアドレス

`ip` メソッドは、アプリケーションにリクエストを行ったクライアントの IP アドレスを取得するために使用できます。

    $ipAddress = $request->ip();

プロキシによって転送されたすべてのクライアント IP アドレスを含む IP アドレスの配列を取得したい場合は、`ips` メソッドを使用できます。 「元の」クライアント IP アドレスは配列の最後にあります。

    $ipAddresses = $request->ips();

一般に、IP アドレスは信頼できない、ユーザー制御の入力とみなされ、情報提供のみを目的として使用される必要があります。

<a name="content-negotiation"></a>
### コンテンツのネゴシエーション

Laravel は、`Accept` ヘッダーを介して受信リクエストのリクエストされたコンテンツタイプを検査するためのメソッドをいくつか提供しています。まず、`getAcceptableContentTypes` メソッドは、リクエストによって受け入れられたすべてのコンテンツ タイプを含む配列を返します。

    $contentTypes = $request->getAcceptableContentTypes();

`accepts` メソッドはコンテンツ タイプの配列を受け入れ、いずれかのコンテンツ タイプがリクエストによって受け入れられた場合は `true` を返します。それ以外の場合は、`false` が返されます。

    if ($request->accepts(['text/html', 'application/json'])) {
        // ...
    }

`prefers` メソッドを使用して、指定されたコンテンツ タイプの配列の中からどのコンテンツ タイプがリクエストで最も優先されるかを判断できます。指定されたコンテンツ タイプがリクエストで受け入れられない場合は、`null` が返されます。

    $preferred = $request->prefers(['text/html', 'application/json']);

多くのアプリケーションは HTML または JSON のみを提供するため、`expectsJson` メソッドを使用して、受信リクエストが JSON 応答を予期しているかどうかをすばやく判断できます。

    if ($request->expectsJson()) {
        // ...
    }

<a name="psr7-requests"></a>
### PSR-7 リクエスト

[PSR-7規格](https://www.php-fig.org/psr/psr-7/) は、リクエストとレスポンスを含む HTTP メッセージのインターフェイスを指定します。 Laravel リクエストではなく PSR-7 リクエストのインスタンスを取得したい場合は、まずいくつかのライブラリをインストールする必要があります。 Laravel は *Symfony HTTP Message Bridge* コンポーネントを使用して、典型的な Laravel リクエストとレスポンスを PSR-7 互換の実装に変換します。

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

これらのライブラリをインストールしたら、ルート クロージャまたはコントローラ メソッドでリクエスト インターフェイスをタイプヒントすることで PSR-7 リクエストを取得できます。

    use Psr\Http\Message\ServerRequestInterface;

    Route::get('/', function (ServerRequestInterface $request) {
        // ...
    });

> [!NOTE]  
> ルートまたはコントローラから PSR-7 応答インスタンスを返すと、それは自動的に Laravel 応答インスタンスに変換され、フレームワークによって表示されます。

<a name="input"></a>
## 入力 (Input)

<a name="retrieving-input"></a>
### 入力の取得

<a name="retrieving-all-input-data"></a>
#### すべての入力データの取得

`all` メソッドを使用して、受信リクエストのすべての入力データを `array` として取得できます。このメソッドは、受信リクエストが HTML フォームからのものであるか、XHR リクエストであるかに関係なく使用できます。

    $input = $request->all();

`collect` メソッドを使用すると、受信リクエストのすべての入力データを [collection](/docs/{{version}}/collections) として取得できます。

    $input = $request->collect();

`collect` メソッドを使用すると、受信リクエストの入力のサブセットをコレクションとして取得することもできます。

    $request->collect('users')->each(function (string $user) {
        // ...
    });

<a name="retrieving-an-input-value"></a>
#### 入力値の取得

いくつかの簡単な方法を使用すると、リクエストにどの HTTP 動詞が使用されたかを気にすることなく、`Illuminate\Http\Request` インスタンスからすべてのユーザー入力にアクセスできます。 HTTP 動詞に関係なく、`input` メソッドを使用してユーザー入力を取得できます。

    $name = $request->input('name');

`input` メソッドの 2 番目の引数としてデフォルト値を渡すことができます。要求された入力値がリクエストに存在しない場合、この値が返されます。

    $name = $request->input('name', 'Sally');

配列入力を含むフォームを操作する場合は、「ドット」表記を使用して配列にアクセスします。

    $name = $request->input('products.0.name');

    $names = $request->input('products.*.name');

すべての入力値を連想配列として取得するには、引数なしで `input` メソッドを呼び出すことができます。

    $input = $request->input();

<a name="retrieving-input-from-the-query-string"></a>
#### クエリ文字列からの入力の取得

`input` メソッドはリクエスト ペイロード全体 (クエリ文字列を含む) から値を取得しますが、`query` メソッドはクエリ文字列からのみ値を取得します。

    $name = $request->query('name');

要求されたクエリ文字列値データが存在しない場合、このメソッドの 2 番目の引数が返されます。

    $name = $request->query('name', 'Helen');

すべてのクエリ文字列値を連想配列として取得するには、引数なしで `query` メソッドを呼び出すことができます。

    $query = $request->query();

<a name="retrieving-json-input-values"></a>
#### JSON入力値の取得

JSON リクエストをアプリケーションに送信するとき、リクエストの `Content-Type` ヘッダーが `application/json` に適切に設定されている限り、`input` メソッド経由で JSON データにアクセスできます。 「ドット」構文を使用して、JSON 配列/オブジェクト内にネストされた値を取得することもできます。

    $name = $request->input('user.name');

<a name="retrieving-stringable-input-values"></a>
#### 文字列可能な入力値の取得

リクエストの入力データをプリミティブ `string` として取得する代わりに、`string` メソッドを使用してリクエスト データを [`Illuminate\Support\Stringable`](/docs/{{version}}/strings) のインスタンスとして取得することもできます。

    $name = $request->string('name')->trim();

<a name="retrieving-integer-input-values"></a>
#### 整数入力値の取得

入力値を整数として取得するには、`integer` メソッドを使用できます。このメソッドは、入力値を整数にキャストしようとします。入力が存在しない場合、またはキャストが失敗した場合は、指定したデフォルト値が返されます。これは、ページネーションやその他の数値入力の場合に特に便利です。

    $perPage = $request->integer('per_page');

<a name="retrieving-boolean-input-values"></a>
#### ブール入力値の取得

チェックボックスなどの HTML 要素を処理する場合、アプリケーションは実際には文字列である「真実の」値を受け取ることがあります。たとえば、「true」または「on」です。便宜上、`boolean` メソッドを使用してこれらの値をブール値として取得できます。 `boolean` メソッドは、1、「1」、true、「true」、「on」、および「yes」の場合、`true` を返します。他のすべての値は `false` を返します。

    $archived = $request->boolean('archived');

<a name="retrieving-date-input-values"></a>
#### 日付入力値の取得

便宜上、日付/時刻を含む入力値は、`date` メソッドを使用して Carbon インスタンスとして取得できます。リクエストに指定された名前の入力値が含まれていない場合は、`null` が返されます。

    $birthday = $request->date('birthday');

`date` メソッドで受け入れられる 2 番目と 3 番目の引数は、それぞれ日付の形式とタイムゾーンを指定するために使用できます。

    $elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');

入力値が存在するものの形式が無効な場合は、`InvalidArgumentException` がスローされます。したがって、`date` メソッドを呼び出す前に入力を検証することをお勧めします。

<a name="retrieving-enum-input-values"></a>
#### Enum 入力値の取得

[PHP 列挙型](https://www.php.net/manual/en/language.types.enumerations.php) に対応する入力値もリクエストから取得できます。リクエストに指定された名前の入力値が含まれていない場合、または列挙型に入力値と一致するバッキング値がない場合は、`null` が返されます。 `enum` メソッドは、入力値の名前と enum クラスを最初と 2 番目の引数として受け入れます。

    use App\Enums\Status;

    $status = $request->enum('status', Status::class);

入力値が PHP 列挙型に対応する値の配列である場合、`enums` メソッドを使用して値の配列を列挙型インスタンスとして取得できます。

    use App\Enums\Product;

    $products = $request->enums('products', Product::class);

<a name="retrieving-input-via-dynamic-properties"></a>
#### 動的プロパティによる入力の取得

`Illuminate\Http\Request` インスタンスの動的プロパティを使用してユーザー入力にアクセスすることもできます。たとえば、アプリケーションのフォームの 1 つに `name` フィールドが含まれている場合、次のようにフィールドの値にアクセスできます。

    $name = $request->name;

動的プロパティを使用する場合、Laravel は最初にリクエストペイロード内のパラメーターの値を探します。存在しない場合、Laravel は一致したルートのパラメーター内のフィールドを検索します。

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 入力データの一部の取得

入力データのサブセットを取得する必要がある場合は、`only` メソッドと `except` メソッドを使用できます。これらのメソッドは両方とも、単一の `array` または引数の動的なリストを受け入れます。

    $input = $request->only(['username', 'password']);

    $input = $request->only('username', 'password');

    $input = $request->except(['credit_card']);

    $input = $request->except('credit_card');

> [!WARNING]  
> `only` メソッドは、要求したすべてのキーと値のペアを返します。ただし、リクエストに存在しないキーと値のペアは返されません。

<a name="input-presence"></a>
### 入力の有無

`has` メソッドを使用して、リクエストに値が存在するかどうかを確認できます。値がリクエストに存在する場合、`has` メソッドは `true` を返します。

    if ($request->has('name')) {
        // ...
    }

配列を指定すると、`has` メソッドは、指定された値がすべて存在するかどうかを判断します。

    if ($request->has(['name', 'email'])) {
        // ...
    }

指定された値のいずれかが存在する場合、`hasAny` メソッドは `true` を返します。

    if ($request->hasAny(['name', 'email'])) {
        // ...
    }

`whenHas` メソッドは、リクエストに値が存在する場合、指定されたクロージャを実行します。

    $request->whenHas('name', function (string $input) {
        // ...
    });

2 番目のクロージャーは、指定された値がリクエストに存在しない場合に実行される `whenHas` メソッドに渡すことができます。

    $request->whenHas('name', function (string $input) {
        // The "name" value is present...
    }, function () {
        // The "name" value is not present...
    });

値がリクエストに存在し、空の文字列ではないかどうかを確認したい場合は、`filled` メソッドを使用できます。

    if ($request->filled('name')) {
        // ...
    }

リクエストに値が欠落しているか空の文字列であるかを確認したい場合は、`isNotFilled` メソッドを使用できます。

    if ($request->isNotFilled('name')) {
        // ...
    }

配列を指定すると、`isNotFilled` メソッドは、指定された値がすべて欠落しているか空であるかを判断します。

    if ($request->isNotFilled(['name', 'email'])) {
        // ...
    }

指定された値のいずれかが空の文字列でない場合、`anyFilled` メソッドは `true` を返します。

    if ($request->anyFilled(['name', 'email'])) {
        // ...
    }

値がリクエストに存在し、空の文字列ではない場合、`whenFilled` メソッドは指定されたクロージャを実行します。

    $request->whenFilled('name', function (string $input) {
        // ...
    });

2 番目のクロージャーは、指定された値が「満たされていない」場合に実行される `whenFilled` メソッドに渡すことができます。

    $request->whenFilled('name', function (string $input) {
        // The "name" value is filled...
    }, function () {
        // The "name" value is not filled...
    });

指定されたキーがリクエストに存在しないかどうかを確認するには、`missing` メソッドと `whenMissing` メソッドを使用できます。

    if ($request->missing('name')) {
        // ...
    }

    $request->whenMissing('name', function () {
        // The "name" value is missing...
    }, function () {
        // The "name" value is present...
    });

<a name="merging-additional-input"></a>
### 追加入力のマージ

場合によっては、追加の入力をリクエストの既存の入力データに手動でマージする必要がある場合があります。これを実現するには、`merge` メソッドを使用できます。指定された入力キーがリクエストにすでに存在する場合、`merge` メソッドに提供されたデータによって上書きされます。

    $request->merge(['votes' => 0]);

対応するキーがリクエストの入力データ内に存在しない場合、`mergeIfMissing` メソッドを使用して入力をリクエストにマージできます。

    $request->mergeIfMissing(['votes' => 0]);

<a name="old-input"></a>
### 古い入力

Laravel を使用すると、あるリクエストからの入力を次のリクエスト中に保持することができます。この機能は、検証エラーを検出した後にフォームを再入力する場合に特に役立ちます。ただし、Laravel に含まれる [検証機能](/docs/{{version}}/validation) を使用している場合は、Laravel の組み込み検証機能の一部がそれらを自動的に呼び出すため、これらのセッション入力フラッシュ メソッドを手動で直接使用する必要がない可能性があります。

<a name="flashing-input-to-the-session"></a>
#### セッションへの入力のフラッシュ

`Illuminate\Http\Request` クラスの `flash` メソッドは、現在の入力を [session](/docs/{{version}}/session) にフラッシュして、アプリケーションに対するユーザーの次のリクエスト時に使用できるようにします。

    $request->flash();

`flashOnly` メソッドと `flashExcept` メソッドを使用して、リクエスト データのサブセットをセッションにフラッシュすることもできます。これらの方法は、パスワードなどの機密情報をセッションから遠ざけるのに役立ちます。

    $request->flashOnly(['username', 'email']);

    $request->flashExcept('password');

<a name="flashing-input-then-redirecting"></a>
#### 入力を点滅させてからリダイレクトする

多くの場合、セッションへの入力をフラッシュしてから前のページにリダイレクトする必要があるため、`withInput` メソッドを使用して、入力のフラッシュをリダイレクトに簡単にチェーンできます。

    return redirect('/form')->withInput();

    return redirect()->route('user.create')->withInput();

    return redirect('/form')->withInput(
        $request->except('password')
    );

<a name="retrieving-old-input"></a>
#### 古い入力の取得

前のリクエストからフラッシュされた入力を取得するには、`Illuminate\Http\Request` のインスタンスで `old` メソッドを呼び出します。 `old` メソッドは、以前にフラッシュされた入力データを [session](/docs/{{version}}/session) から取得します。

    $username = $request->old('username');

Laravel は、グローバル `old` ヘルパも提供します。 [Blade テンプレート](/docs/{{version}}/blade) 内で古い入力を表示している場合は、`old` ヘルパを使用してフォームに再入力する方が便利です。指定されたフィールドに古い入力が存在しない場合は、`null` が返されます。

    <input type="text" name="username" value="{{ old('username') }}">

<a name="cookies"></a>
### クッキー

<a name="retrieving-cookies-from-requests"></a>
#### リクエストから Cookie を取得する

Laravel フレームワークによって作成されたすべての Cookie は暗号化され、認証コードで署名されます。つまり、クライアントによって変更された場合は無効とみなされます。リクエストから Cookie 値を取得するには、`Illuminate\Http\Request` インスタンスで `cookie` メソッドを使用します。

    $value = $request->cookie('name');

<a name="input-trimming-and-normalization"></a>
## 入力トリミングと正規化 (Input Trimming and Normalization)

デフォルトでは、Laravel にはアプリケーションのグローバルミドルウェアスタックに `Illuminate\Foundation\Http\Middleware\TrimStrings` および `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` ミドルウェアが含まれています。これらのミドルウェアは、リクエスト上のすべての受信文字列フィールドを自動的にトリミングし、空の文字列フィールドを `null` に変換します。これにより、ルートとコントローラにおけるこれらの正規化の問題を心配する必要がなくなります。

#### 入力正規化の無効化

すべてのリクエストに対してこの動作を無効にしたい場合は、アプリケーションの `bootstrap/app.php` ファイルで `$middleware->remove` メソッドを呼び出して、アプリケーションのミドルウェア スタックから 2 つのミドルウェアを削除できます。

    use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
    use Illuminate\Foundation\Http\Middleware\TrimStrings;

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->remove([
            ConvertEmptyStringsToNull::class,
            TrimStrings::class,
        ]);
    })

アプリケーションへのリクエストのサブセットに対して文字列のトリミングと空の文字列の変換を無効にしたい場合は、アプリケーションの `bootstrap/app.php` ファイル内で `trimStrings` および `convertEmptyStringsToNull` ミドルウェア メソッドを使用できます。どちらのメソッドもクロージャの配列を受け入れます。これは、入力正規化をスキップするかどうかを示す `true` または `false` を返す必要があります。

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->convertEmptyStringsToNull(except: [
            fn (Request $request) => $request->is('admin/*'),
        ]);

        $middleware->trimStrings(except: [
            fn (Request $request) => $request->is('admin/*'),
        ]);
    })

<a name="files"></a>
## ファイル (Files)

<a name="retrieving-uploaded-files"></a>
### アップロードされたファイルの取得

`file` メソッドまたは動的プロパティを使用して、`Illuminate\Http\Request` インスタンスからアップロードされたファイルを取得できます。 `file` メソッドは、PHP `SplFileInfo` クラスを拡張し、ファイルと対話するためのさまざまなメソッドを提供する `Illuminate\Http\UploadedFile` クラスのインスタンスを返します。

    $file = $request->file('photo');

    $file = $request->photo;

`hasFile` メソッドを使用して、リクエストにファイルが存在するかどうかを確認できます。

    if ($request->hasFile('photo')) {
        // ...
    }

<a name="validating-successful-uploads"></a>
#### 成功したアップロードの検証

ファイルが存在するかどうかを確認するだけでなく、`isValid` メソッドを使用してファイルのアップロードに問題がなかったことを確認することもできます。

    if ($request->file('photo')->isValid()) {
        // ...
    }

<a name="file-paths-extensions"></a>
#### ファイルのパスと拡張子

`UploadedFile` クラスには、ファイルの完全修飾パスとその拡張子にアクセスするためのメソッドも含まれています。 `extension` メソッドは、ファイルの内容に基づいてファイルの拡張子を推測しようとします。この拡張子は、クライアントによって提供された拡張子とは異なる場合があります。

    $path = $request->photo->path();

    $extension = $request->photo->extension();

<a name="other-file-methods"></a>
#### 他のファイル方法

`UploadedFile` インスタンスでは他にもさまざまなメソッドを使用できます。これらの方法の詳細については、[クラスの API ドキュメント](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php) を確認してください。

<a name="storing-uploaded-files"></a>
### アップロードしたファイルの保存

アップロードされたファイルを保存するには、通常、構成された [filesystems](/docs/{{version}}/filesystem) の 1 つを使用します。 `UploadedFile` クラスには、アップロードされたファイルをディスクの 1 つに移動する `store` メソッドがあります。ディスクは、ローカル ファイル システム上の場所または Amazon S3 などのクラウド ストレージの場所である可能性があります。

`store` メソッドは、ファイル システムの構成されたルート ディレクトリを基準にしてファイルを保存するパスを受け入れます。ファイル名として機能する一意の ID が自動的に生成されるため、このパスにはファイル名を含めないでください。

`store` メソッドは、ファイルの保存に使用するディスク名のオプションの 2 番目の引数も受け入れます。このメソッドは、ディスクのルートを基準としたファイルの相対パスを返します。

    $path = $request->photo->store('images');

    $path = $request->photo->store('images', 's3');

ファイル名を自動的に生成したくない場合は、パス、ファイル名、およびディスク名を引数として受け入れる `storeAs` メソッドを使用できます。

    $path = $request->photo->storeAs('images', 'filename.jpg');

    $path = $request->photo->storeAs('images', 'filename.jpg', 's3');

> [!NOTE]  
> Laravel のファイルストレージの詳細については、完全な [ファイルストレージのドキュメント](/docs/{{version}}/filesystem) を確認してください。

<a name="configuring-trusted-proxies"></a>
## 信頼できるプロキシの構成 (Configuring Trusted Proxies)

TLS / SSL 証明書を終了するロード バランサーの背後でアプリケーションを実行する場合、`url` ヘルパの使用時にアプリケーションが HTTPS リンクを生成しないことがあります。通常、これは、アプリケーションがポート 80 上のロード バランサーからトラフィックを転送されており、安全なリンクを生成する必要があることを認識していないことが原因です。

これを解決するには、Laravel アプリケーションに含まれている `Illuminate\Http\Middleware\TrustProxies` ミドルウェアを有効にすることができます。これにより、アプリケーションが信頼する必要があるロード バランサーまたはプロキシを迅速にカスタマイズできます。信頼できるプロキシは、アプリケーションの `bootstrap/app.php` ファイルで `trustProxies` ミドルウェア メソッドを使用して指定する必要があります。

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->trustProxies(at: [
            '192.168.1.1',
            '10.0.0.0/8',
        ]);
    })

信頼できるプロキシの構成に加えて、信頼すべきプロキシ ヘッダーも構成できます。

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
            Request::HEADER_X_FORWARDED_HOST |
            Request::HEADER_X_FORWARDED_PORT |
            Request::HEADER_X_FORWARDED_PROTO |
            Request::HEADER_X_FORWARDED_AWS_ELB
        );
    })

> [!NOTE]  
> AWS Elastic Load Balancing を使用している場合、`headers` 値は `Request::HEADER_X_FORWARDED_AWS_ELB` である必要があります。ロード バランサーが [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4) の標準 `Forwarded` ヘッダーを使用する場合、`headers` の値は `Request::HEADER_FORWARDED` である必要があります。 `headers` 値で使用できる定数の詳細については、[信頼できるプロキシ](https://symfony.com/doc/7.0/deployment/proxies.html) に関する Symfony のドキュメントを確認してください。

<a name="trusting-all-proxies"></a>
#### すべてのプロキシを信頼する

Amazon AWS または別の「クラウド」ロード バランサー プロバイダを使用している場合は、実際のバランサーの IP アドレスがわからない可能性があります。この場合、`*` を使用してすべてのプロキシを信頼できます。

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->trustProxies(at: '*');
    })

<a name="configuring-trusted-hosts"></a>
## 信頼できるホストの構成 (Configuring Trusted Hosts)

デフォルトでは、Laravel は、HTTP リクエストの `Host` ヘッダーの内容に関係なく、受信したすべてのリクエストに応答します。さらに、`Host` ヘッダーの値は、Web リクエスト中にアプリケーションへの絶対 URL を生成するときに使用されます。

通常、指定されたホスト名に一致するリクエストのみをアプリケーションに送信するように、Nginx や Apache などの Web サーバーを構成する必要があります。ただし、Web サーバーを直接カスタマイズする機能がなく、特定のホスト名にのみ応答するように Laravel に指示する必要がある場合は、アプリケーションの `Illuminate\Http\Middleware\TrustHosts` ミドルウェアを有効にすることでこれを行うことができます。

`TrustHosts` ミドルウェアを有効にするには、アプリケーションの `bootstrap/app.php` ファイルで `trustHosts` ミドルウェア メソッドを呼び出す必要があります。このメソッドの `at` 引数を使用すると、アプリケーションが応答するホスト名を指定できます。他の `Host` ヘッダーを持つ受信リクエストは拒否されます。

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->trustHosts(at: ['laravel.test']);
    })

デフォルトでは、アプリケーションの URL のサブドメインからのリクエストも自動的に信頼されます。この動作を無効にしたい場合は、`subdomains` 引数を使用できます。

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->trustHosts(at: ['laravel.test'], subdomains: false);
    })

信頼できるホストを判断するためにアプリケーションの構成ファイルまたはデータベースにアクセスする必要がある場合は、`at` 引数にクロージャーを指定できます。

    ->withMiddleware(function (Middleware $middleware) {
        $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
    })

