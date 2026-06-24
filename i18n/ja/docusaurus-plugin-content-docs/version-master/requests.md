<!-- # HTTP Requests -->
# HTTP Requests

- [Introduction](#introduction)
- [Interacting With The Request](#interacting-with-the-request)
    - [Accessing the Request](#accessing-the-request)
    - [Request Path, Host, and Method](#request-path-and-method)
    - [Request Headers](#request-headers)
    - [Request IP Address](#request-ip-address)
    - [Content Negotiation](#content-negotiation)
    - [PSR-7 Requests](#psr7-requests)
- [Input](#input)
    - [Retrieving Input](#retrieving-input)
    - [Input Presence](#input-presence)
    - [Merging Additional Input](#merging-additional-input)
    - [Old Input](#old-input)
    - [Cookies](#cookies)
    - [Input Trimming and Normalization](#input-trimming-and-normalization)
- [Files](#files)
    - [Retrieving Uploaded Files](#retrieving-uploaded-files)
    - [Storing Uploaded Files](#storing-uploaded-files)
- [Configuring Trusted Proxies](#configuring-trusted-proxies)
- [Configuring Trusted Hosts](#configuring-trusted-hosts)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's `Illuminate\Http\Request` class provides an object-oriented way to interact with the current HTTP request being handled by your application as well as retrieve the input, cookies, and files that were submitted with the request. -->
Laravel の `Illuminate\Http\Request` クラスは、アプリケーションによって処理されている現在の HTTP リクエストと対話し、リクエストとともに送信された入力、Cookie、およびファイルを取得するためのオブジェクト指向の方法を提供します。

<a name="interacting-with-the-request"></a>
<!-- ## Interacting With The Request -->
## Interacting With The Request

<a name="accessing-the-request"></a>
<!-- ### Accessing the Request -->
### Accessing the Request

<!-- To obtain an instance of the current HTTP request via dependency injection, you should type-hint the `Illuminate\Http\Request` class on your route closure or controller method. The incoming request instance will automatically be injected by the Laravel [service container](/docs/master/container): -->
依存注入を通じて現在の HTTP リクエストのインスタンスを取得するには、ルート クロージャーまたはコントローラ メソッドで `Illuminate\Http\Request` クラスをタイプヒントする必要があります。受信リクエストのインスタンスは、Laravel [service container](/docs/master/container) によって自動的に挿入されます。

```php
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
```

<!-- As mentioned, you may also type-hint the `Illuminate\Http\Request` class on a route closure. The service container will automatically inject the incoming request into the closure when it is executed: -->
前述したように、ルート クロージャで `Illuminate\Http\Request` クラスをタイプヒントで指定することもできます。サービスコンテナは、実行時に受信リクエストを自動的にクロージャに挿入します。

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
<!-- #### Dependency Injection and Route Parameters -->
#### Dependency Injection and Route Parameters

<!-- If your controller method is also expecting input from a route parameter you should list your route parameters after your other dependencies. For example, if your route is defined like so: -->
コントローラ メソッドがルート パラメーターからの入力も期待している場合は、他の依存関係の後にルート パラメーターをリストする必要があります。たとえば、ルートが次のように定義されているとします。

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

<!-- You may still type-hint the `Illuminate\Http\Request` and access your `id` route parameter by defining your controller method as follows: -->
次のようにコントローラ メソッドを定義することで、`Illuminate\Http\Request` をタイプヒントして `id` ルート パラメーターにアクセスすることもできます。

```php
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
```

<a name="request-path-and-method"></a>
<!-- ### Request Path, Host, and Method -->
### Request Path, Host, and Method

<!-- The `Illuminate\Http\Request` instance provides a variety of methods for examining the incoming HTTP request and extends the `Symfony\Component\HttpFoundation\Request` class. We will discuss a few of the most important methods below. -->
`Illuminate\Http\Request` インスタンスは、受信 HTTP リクエストを検査するためのさまざまなメソッドを提供し、`Symfony\Component\HttpFoundation\Request` クラスを拡張します。以下では、最も重要な方法のいくつかについて説明します。

<a name="retrieving-the-request-path"></a>
<!-- #### Retrieving the Request Path -->
#### Retrieving the Request Path

<!-- The `path` method returns the request's path information. So, if the incoming request is targeted at `http://example.com/foo/bar`, the `path` method will return `foo/bar`: -->
`path` メソッドは、リクエストのパス情報を返します。したがって、受信リクエストが `http://example.com/foo/bar` をターゲットにしている場合、`path` メソッドは `foo/bar` を返します。

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
<!-- #### Inspecting the Request Path / Route -->
#### Inspecting the Request Path / Route

<!-- The `is` method allows you to verify that the incoming request path matches a given pattern. You may use the `*` character as a wildcard when utilizing this method: -->
`is` メソッドを使用すると、受信リクエストのパスが指定されたパターンと一致することを確認できます。この方法を使用する場合は、`*` 文字をワイルドカードとして使用できます。

```php
if ($request->is('admin/*')) {
    // ...
}
```

<!-- Using the `routeIs` method, you may determine if the incoming request has matched a [named route](/docs/master/routing#named-routes): -->
`routeIs` メソッドを使用すると、受信リクエストが [named route](/docs/master/routing#named-routes) と一致したかどうかを判断できます。

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
<!-- #### Retrieving the Request URL -->
#### Retrieving the Request URL

<!-- To retrieve the full URL for the incoming request you may use the `url` or `fullUrl` methods. The `url` method will return the URL without the query string, while the `fullUrl` method includes the query string: -->
受信リクエストの完全な URL を取得するには、`url` メソッドまたは `fullUrl` メソッドを使用できます。 `url` メソッドはクエリ文字列なしで URL を返しますが、`fullUrl` メソッドにはクエリ文字列が含まれます。

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

<!-- If you would like to append query string data to the current URL, you may call the `fullUrlWithQuery` method. This method merges the given array of query string variables with the current query string: -->
現在の URL にクエリ文字列データを追加したい場合は、`fullUrlWithQuery` メソッドを呼び出すことができます。このメソッドは、指定されたクエリ文字列変数の配列を現在のクエリ文字列とマージします。

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

<!-- If you would like to get the current URL without a given query string parameter, you may utilize the `fullUrlWithoutQuery` method: -->
特定のクエリ文字列パラメータを指定せずに現在の URL を取得したい場合は、`fullUrlWithoutQuery` メソッドを利用できます。

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
<!-- #### Retrieving the Request Host -->
#### Retrieving the Request Host

<!-- You may retrieve the "host" of the incoming request via the `host`, `httpHost`, and `schemeAndHttpHost` methods: -->
受信リクエストの「ホスト」は、`host`、`httpHost`、および `schemeAndHttpHost` メソッドを介して取得できます。

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
<!-- #### Retrieving the Request Method -->
#### Retrieving the Request Method

<!-- The `method` method will return the HTTP verb for the request. You may use the `isMethod` method to verify that the HTTP verb matches a given string: -->
`method` メソッドは、リクエストの HTTP 動詞を返します。 `isMethod` メソッドを使用して、HTTP 動詞が指定された文字列と一致することを確認できます。

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
<!-- ### Request Headers -->
### Request Headers

<!-- You may retrieve a request header from the `Illuminate\Http\Request` instance using the `header` method. If the header is not present on the request, `null` will be returned. However, the `header` method accepts an optional second argument that will be returned if the header is not present on the request: -->
`header` メソッドを使用して、`Illuminate\Http\Request` インスタンスからリクエスト ヘッダーを取得できます。リクエストにヘッダーが存在しない場合は、`null` が返されます。ただし、`header` メソッドは、リクエストにヘッダーが存在しない場合に返されるオプションの 2 番目の引数を受け入れます。

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

<!-- The `hasHeader` method may be used to determine if the request contains a given header: -->
`hasHeader` メソッドを使用して、リクエストに特定のヘッダーが含まれているかどうかを判断できます。

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

<!-- For convenience, the `bearerToken` method may be used to retrieve a bearer token from the `Authorization` header. If no such header is present, an empty string will be returned: -->
便宜上、`bearerToken` メソッドを使用して、`Authorization` ヘッダーからベアラー トークンを取得できます。そのようなヘッダーが存在しない場合は、空の文字列が返されます。

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
<!-- ### Request IP Address -->
### Request IP Address

<!-- The `ip` method may be used to retrieve the IP address of the client that made the request to your application: -->
`ip` メソッドは、アプリケーションにリクエストを行ったクライアントの IP アドレスを取得するために使用できます。

```php
$ipAddress = $request->ip();
```

<!-- If you would like to retrieve an array of IP addresses, including all of the client IP addresses that were forwarded by proxies, you may use the `ips` method. The "original" client IP address will be at the end of the array: -->
プロキシによって転送されたすべてのクライアント IP アドレスを含む IP アドレスの配列を取得したい場合は、`ips` メソッドを使用できます。 「元の」クライアント IP アドレスは配列の最後にあります。

```php
$ipAddresses = $request->ips();
```

<!-- In general, IP addresses should be considered untrusted, user-controlled input and be used for informational purposes only. -->
一般に、IP アドレスは信頼できない、ユーザー制御の入力とみなされ、情報提供のみを目的として使用される必要があります。

<a name="content-negotiation"></a>
<!-- ### Content Negotiation -->
### Content Negotiation

<!-- Laravel provides several methods for inspecting the incoming request's requested content types via the `Accept` header. First, the `getAcceptableContentTypes` method will return an array containing all of the content types accepted by the request: -->
Laravel は、`Accept` ヘッダーを介して受信リクエストのリクエストされたコンテンツタイプを検査するためのメソッドをいくつか提供しています。まず、`getAcceptableContentTypes` メソッドは、リクエストによって受け入れられたすべてのコンテンツ タイプを含む配列を返します。

```php
$contentTypes = $request->getAcceptableContentTypes();
```

<!-- The `accepts` method accepts an array of content types and returns `true` if any of the content types are accepted by the request. Otherwise, `false` will be returned: -->
`accepts` メソッドはコンテンツ タイプの配列を受け入れ、いずれかのコンテンツ タイプがリクエストによって受け入れられた場合は `true` を返します。それ以外の場合は、`false` が返されます。

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

<!-- You may use the `prefers` method to determine which content type out of a given array of content types is most preferred by the request. If none of the provided content types are accepted by the request, `null` will be returned: -->
`prefers` メソッドを使用して、指定されたコンテンツ タイプの配列の中からどのコンテンツ タイプがリクエストで最も優先されるかを判断できます。指定されたコンテンツ タイプがリクエストで受け入れられない場合は、`null` が返されます。

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

<!-- Since many applications only serve HTML or JSON, you may use the `expectsJson` method to quickly determine if the incoming request expects a JSON response: -->
多くのアプリケーションは HTML または JSON のみを提供するため、`expectsJson` メソッドを使用して、受信リクエストが JSON 応答を予期しているかどうかをすばやく判断できます。

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
<!-- ### PSR-7 Requests -->
### PSR-7 Requests

<!-- The [PSR-7 standard](https://www.php-fig.org/psr/psr-7/) specifies interfaces for HTTP messages, including requests and responses. If you would like to obtain an instance of a PSR-7 request instead of a Laravel request, you will first need to install a few libraries. Laravel uses the *Symfony HTTP Message Bridge* component to convert typical Laravel requests and responses into PSR-7 compatible implementations: -->
[PSR-7 standard](https://www.php-fig.org/psr/psr-7/) は、リクエストとレスポンスを含む HTTP メッセージのインターフェイスを指定します。 Laravel リクエストではなく PSR-7 リクエストのインスタンスを取得したい場合は、まずいくつかのライブラリをインストールする必要があります。 Laravel は *Symfony HTTP Message Bridge* コンポーネントを使用して、典型的な Laravel リクエストとレスポンスを PSR-7 互換の実装に変換します。

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

<!-- Once you have installed these libraries, you may obtain a PSR-7 request by type-hinting the request interface on your route closure or controller method: -->
これらのライブラリをインストールしたら、ルート クロージャまたはコントローラ メソッドでリクエスト インターフェイスをタイプヒントすることで PSR-7 リクエストを取得できます。

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> ルートまたはコントローラから PSR-7 応答インスタンスを返すと、それは自動的に Laravel 応答インスタンスに変換され、フレームワークによって表示されます。

<a name="input"></a>
<!-- ## Input -->
## Input

<a name="retrieving-input"></a>
<!-- ### Retrieving Input -->
### Retrieving Input

<a name="retrieving-all-input-data"></a>
<!-- #### Retrieving All Input Data -->
#### Retrieving All Input Data

<!-- You may retrieve all of the incoming request's input data as an `array` using the `all` method. This method may be used regardless of whether the incoming request is from an HTML form or is an XHR request: -->
`all` メソッドを使用して、受信リクエストのすべての入力データを `array` として取得できます。このメソッドは、受信リクエストが HTML フォームからのものであるか、XHR リクエストであるかに関係なく使用できます。

```php
$input = $request->all();
```

<!-- Using the `collect` method, you may retrieve all of the incoming request's input data as a [collection](/docs/master/collections): -->
`collect` メソッドを使用すると、受信リクエストのすべての入力データを [collection](/docs/master/collections) として取得できます。

```php
$input = $request->collect();
```

<!-- The `collect` method also allows you to retrieve a subset of the incoming request's input as a collection: -->
`collect` メソッドを使用すると、受信リクエストの入力のサブセットをコレクションとして取得することもできます。

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
<!-- #### Retrieving an Input Value -->
#### Retrieving an Input Value

<!-- Using a few simple methods, you may access all of the user input from your `Illuminate\Http\Request` instance without worrying about which HTTP verb was used for the request. Regardless of the HTTP verb, the `input` method may be used to retrieve user input: -->
いくつかの簡単な方法を使用すると、リクエストにどの HTTP 動詞が使用されたかを気にすることなく、`Illuminate\Http\Request` インスタンスからすべてのユーザー入力にアクセスできます。 HTTP 動詞に関係なく、`input` メソッドを使用してユーザー入力を取得できます。

```php
$name = $request->input('name');
```

<!-- You may pass a default value as the second argument to the `input` method. This value will be returned if the requested input value is not present on the request: -->
`input` メソッドの 2 番目の引数としてデフォルト値を渡すことができます。要求された入力値がリクエストに存在しない場合、この値が返されます。

```php
$name = $request->input('name', 'Sally');
```

<!-- When working with forms that contain array inputs, use "dot" notation to access the arrays: -->
配列入力を含むフォームを操作する場合は、「ドット」表記を使用して配列にアクセスします。

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

<!-- You may call the `input` method without any arguments in order to retrieve all of the input values as an associative array: -->
すべての入力値を連想配列として取得するには、引数なしで `input` メソッドを呼び出すことができます。

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
<!-- #### Retrieving Input From the Query String -->
#### Retrieving Input From the Query String

<!-- While the `input` method retrieves values from the entire request payload (including the query string), the `query` method will only retrieve values from the query string: -->
`input` メソッドはリクエスト ペイロード全体 (クエリ文字列を含む) から値を取得しますが、`query` メソッドはクエリ文字列からのみ値を取得します。

```php
$name = $request->query('name');
```

<!-- If the requested query string value data is not present, the second argument to this method will be returned: -->
要求されたクエリ文字列値データが存在しない場合、このメソッドの 2 番目の引数が返されます。

```php
$name = $request->query('name', 'Helen');
```

<!-- You may call the `query` method without any arguments in order to retrieve all of the query string values as an associative array: -->
すべてのクエリ文字列値を連想配列として取得するには、引数なしで `query` メソッドを呼び出すことができます。

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
<!-- #### Retrieving JSON Input Values -->
#### Retrieving JSON Input Values

<!-- When sending JSON requests to your application, you may access the JSON data via the `input` method as long as the `Content-Type` header of the request is properly set to `application/json`. You may even use "dot" syntax to retrieve values that are nested within JSON arrays / objects: -->
JSON リクエストをアプリケーションに送信するとき、リクエストの `Content-Type` ヘッダーが `application/json` に適切に設定されている限り、`input` メソッド経由で JSON データにアクセスできます。 「ドット」構文を使用して、JSON 配列/オブジェクト内にネストされた値を取得することもできます。

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
<!-- #### Retrieving Stringable Input Values -->
#### Retrieving Stringable Input Values

<!-- Instead of retrieving the request's input data as a primitive `string`, you may use the `string` method to retrieve the request data as an instance of [Illuminate\Support\Stringable](/docs/master/strings): -->
リクエストの入力データをプリミティブ `string` として取得する代わりに、`string` メソッドを使用してリクエスト データを [Illuminate\Support\Stringable](/docs/master/strings) のインスタンスとして取得することもできます。

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
<!-- #### Retrieving Integer Input Values -->
#### Retrieving Integer Input Values

<!-- To retrieve input values as integers, you may use the `integer` method. This method will attempt to cast the input value to an integer. If the input is not present or the cast fails, it will return the default value you specify. This is particularly useful for pagination or other numeric inputs: -->
入力値を整数として取得するには、`integer` メソッドを使用できます。このメソッドは、入力値を整数にcastしようとします。入力が存在しない場合、またはcastが失敗した場合は、指定したデフォルト値が返されます。これは、ページネーションやその他の数値入力の場合に特に便利です。

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
<!-- #### Retrieving Boolean Input Values -->
#### Retrieving Boolean Input Values

<!-- When dealing with HTML elements like checkboxes, your application may receive "truthy" values that are actually strings. For example, "true" or "on". For convenience, you may use the `boolean` method to retrieve these values as booleans. The `boolean` method returns `true` for 1, "1", true, "true", "on", and "yes". All other values will return `false`: -->
チェックボックスなどの HTML 要素を処理する場合、アプリケーションは実際には文字列である「真実の」値を受け取ることがあります。たとえば、「true」または「on」です。便宜上、`boolean` メソッドを使用してこれらの値をブール値として取得できます。 `boolean` メソッドは、1、「1」、true、「true」、「on」、および「yes」の場合、`true` を返します。他のすべての値は `false` を返します。

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
<!-- #### Retrieving Array Input Values -->
#### Retrieving Array Input Values

<!-- Input values containing arrays may be retrieved using the `array` method. This method will always cast the input value to an array. If the request does not contain an input value with the given name, an empty array will be returned: -->
配列を含む入力値は、`array` メソッドを使用して取得できます。このメソッドは常に入力値を配列にcastします。リクエストに指定された名前の入力値が含まれていない場合は、空の配列が返されます。

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
<!-- #### Retrieving Date Input Values -->
#### Retrieving Date Input Values

<!-- For convenience, input values containing dates / times may be retrieved as Carbon instances using the `date` method. If the request does not contain an input value with the given name, `null` will be returned: -->
便宜上、日付/時刻を含む入力値は、`date` メソッドを使用して Carbon インスタンスとして取得できます。リクエストに指定された名前の入力値が含まれていない場合は、`null` が返されます。

```php
$birthday = $request->date('birthday');
```

<!-- The second and third arguments accepted by the `date` method may be used to specify the date's format and timezone, respectively: -->
`date` メソッドで受け入れられる 2 番目と 3 番目の引数は、それぞれ日付の形式とタイムゾーンを指定するために使用できます。

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

<!-- If the input value is present but has an invalid format, an `InvalidArgumentException` will be thrown; therefore, it is recommended that you validate the input before invoking the `date` method. -->
入力値が存在するものの形式が無効な場合は、`InvalidArgumentException` がスローされます。したがって、`date` メソッドを呼び出す前に入力を検証することをお勧めします。

<a name="retrieving-enum-input-values"></a>
<!-- #### Retrieving Enum Input Values -->
#### Retrieving Enum Input Values

<!-- Input values that correspond to [PHP enums](https://www.php.net/manual/en/language.types.enumerations.php) may also be retrieved from the request. If the request does not contain an input value with the given name or the enum does not have a backing value that matches the input value, `null` will be returned. The `enum` method accepts the name of the input value and the enum class as its first and second arguments: -->
[PHP enums](https://www.php.net/manual/en/language.types.enumerations.php) に対応する入力値もリクエストから取得できます。リクエストに指定された名前の入力値が含まれていない場合、または列挙型に入力値と一致するバッキング値がない場合は、`null` が返されます。 `enum` メソッドは、入力値の名前と enum クラスを最初と 2 番目の引数として受け入れます。

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

<!-- You may also provide a default value that will be returned if the value is missing or invalid: -->
値が欠落しているか無効な場合に返されるデフォルト値を指定することもできます。

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

<!-- If the input value is an array of values that correspond to a PHP enum, you may use the `enums` method to retrieve the array of values as enum instances: -->
入力値が PHP 列挙型に対応する値の配列である場合、`enums` メソッドを使用して値の配列を列挙型インスタンスとして取得できます。

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
<!-- #### Retrieving Input via Dynamic Properties -->
#### Retrieving Input via Dynamic Properties

<!-- You may also access user input using dynamic properties on the `Illuminate\Http\Request` instance. For example, if one of your application's forms contains a `name` field, you may access the value of the field like so: -->
`Illuminate\Http\Request` インスタンスの動的プロパティを使用してユーザー入力にアクセスすることもできます。たとえば、アプリケーションのフォームの 1 つに `name` フィールドが含まれている場合、次のようにフィールドの値にアクセスできます。

```php
$name = $request->name;
```

<!-- When using dynamic properties, Laravel will first look for the parameter's value in the request payload. If it is not present, Laravel will search for the field in the matched route's parameters. -->
動的プロパティを使用する場合、Laravel は最初にリクエストペイロード内のパラメーターの値を探します。存在しない場合、Laravel は一致したルートのパラメーター内のフィールドを検索します。

<a name="retrieving-a-portion-of-the-input-data"></a>
<!-- #### Retrieving a Portion of the Input Data -->
#### Retrieving a Portion of the Input Data

<!-- If you need to retrieve a subset of the input data, you may use the `only` and `except` methods. Both of these methods accept a single `array` or a dynamic list of arguments: -->
入力データのサブセットを取得する必要がある場合は、`only` メソッドと `except` メソッドを使用できます。これらのメソッドは両方とも、単一の `array` または引数の動的なリストを受け入れます。

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` メソッドは、要求したすべてのキーと値のペアを返します。ただし、リクエストに存在しないキーと値のペアは返されません。

<a name="input-presence"></a>
<!-- ### Input Presence -->
### Input Presence

<!-- You may use the `has` method to determine if a value is present on the request. The `has` method returns `true` if the value is present on the request: -->
`has` メソッドを使用して、リクエストに値が存在するかどうかを確認できます。値がリクエストに存在する場合、`has` メソッドは `true` を返します。

```php
if ($request->has('name')) {
    // ...
}
```

<!-- When given an array, the `has` method will determine if all of the specified values are present: -->
配列を指定すると、`has` メソッドは、指定された値がすべて存在するかどうかを判断します。

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

<!-- The `hasAny` method returns `true` if any of the specified values are present: -->
指定された値のいずれかが存在する場合、`hasAny` メソッドは `true` を返します。

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

<!-- The `whenHas` method will execute the given closure if a value is present on the request: -->
`whenHas` メソッドは、リクエストに値が存在する場合、指定されたクロージャを実行します。

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

<!-- A second closure may be passed to the `whenHas` method that will be executed if the specified value is not present on the request: -->
2 番目のクロージャーは、指定された値がリクエストに存在しない場合に実行される `whenHas` メソッドに渡すことができます。

```php
$request->whenHas('name', function (string $input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```

<!-- If you would like to determine if a value is present on the request and is not an empty string, you may use the `filled` method: -->
値がリクエストに存在し、空の文字列ではないかどうかを確認したい場合は、`filled` メソッドを使用できます。

```php
if ($request->filled('name')) {
    // ...
}
```

<!-- If you would like to determine if a value is missing from the request or is an empty string, you may use the `isNotFilled` method: -->
リクエストに値が欠落しているか空の文字列であるかを確認したい場合は、`isNotFilled` メソッドを使用できます。

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

<!-- When given an array, the `isNotFilled` method will determine if all of the specified values are missing or empty: -->
配列を指定すると、`isNotFilled` メソッドは、指定された値がすべて欠落しているか空であるかを判断します。

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

<!-- The `anyFilled` method returns `true` if any of the specified values is not an empty string: -->
指定された値のいずれかが空の文字列でない場合、`anyFilled` メソッドは `true` を返します。

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

<!-- The `whenFilled` method will execute the given closure if a value is present on the request and is not an empty string: -->
値がリクエストに存在し、空の文字列ではない場合、`whenFilled` メソッドは指定されたクロージャを実行します。

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

<!-- A second closure may be passed to the `whenFilled` method that will be executed if the specified value is not "filled": -->
2 番目のクロージャーは、指定された値が「満たされていない」場合に実行される `whenFilled` メソッドに渡すことができます。

```php
$request->whenFilled('name', function (string $input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```

<!-- To determine if a given key is absent from the request, you may use the `missing` and `whenMissing` methods: -->
指定されたキーがリクエストに存在しないかどうかを確認するには、`missing` メソッドと `whenMissing` メソッドを使用できます。

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // The "name" value is missing...
}, function () {
    // The "name" value is present...
});
```

<a name="merging-additional-input"></a>
<!-- ### Merging Additional Input -->
### Merging Additional Input

<!-- Sometimes you may need to manually merge additional input into the request's existing input data. To accomplish this, you may use the `merge` method. If a given input key already exists on the request, it will be overwritten by the data provided to the `merge` method: -->
場合によっては、追加の入力をリクエストの既存の入力データに手動でマージする必要がある場合があります。これを実現するには、`merge` メソッドを使用できます。指定された入力キーがリクエストにすでに存在する場合、`merge` メソッドに提供されたデータによって上書きされます。

```php
$request->merge(['votes' => 0]);
```

<!-- The `mergeIfMissing` method may be used to merge input into the request if the corresponding keys do not already exist within the request's input data: -->
対応するキーがリクエストの入力データ内に存在しない場合、`mergeIfMissing` メソッドを使用して入力をリクエストにマージできます。

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
<!-- ### Old Input -->
### Old Input

<!-- Laravel allows you to keep input from one request during the next request. This feature is particularly useful for re-populating forms after detecting validation errors. However, if you are using Laravel's included [validation features](/docs/master/validation), it is possible that you will not need to manually use these session input flashing methods directly, as some of Laravel's built-in validation facilities will call them automatically. -->
Laravel を使用すると、あるリクエストからの入力を次のリクエスト中に保持することができます。この機能は、検証エラーを検出した後にフォームを再入力する場合に特に役立ちます。ただし、Laravel に含まれる [validation features](/docs/master/validation) を使用している場合は、Laravel の組み込み検証機能の一部がそれらを自動的に呼び出すため、これらのセッション入力フラッシュ メソッドを手動で直接使用する必要がない可能性があります。

<a name="flashing-input-to-the-session"></a>
<!-- #### Flashing Input to the Session -->
#### Flashing Input to the Session

<!-- The `flash` method on the `Illuminate\Http\Request` class will flash the current input to the [session](/docs/master/session) so that it is available during the user's next request to the application: -->
`Illuminate\Http\Request` クラスの `flash` メソッドは、現在の入力を [session](/docs/master/session) にフラッシュして、アプリケーションに対するユーザーの次のリクエスト時に使用できるようにします。

```php
$request->flash();
```

<!-- You may also use the `flashOnly` and `flashExcept` methods to flash a subset of the request data to the session. These methods are useful for keeping sensitive information such as passwords out of the session: -->
`flashOnly` メソッドと `flashExcept` メソッドを使用して、リクエスト データのサブセットをセッションにフラッシュすることもできます。これらの方法は、パスワードなどの機密情報をセッションから遠ざけるのに役立ちます。

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
<!-- #### Flashing Input Then Redirecting -->
#### Flashing Input Then Redirecting

<!-- Since you often will want to flash input to the session and then redirect to the previous page, you may easily chain input flashing onto a redirect using the `withInput` method: -->
多くの場合、セッションへの入力をフラッシュしてから前のページにリダイレクトする必要があるため、`withInput` メソッドを使用して、入力のフラッシュをリダイレクトに簡単にチェーンできます。

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
<!-- #### Retrieving Old Input -->
#### Retrieving Old Input

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/master/session): -->
前のリクエストからフラッシュされた入力を取得するには、`Illuminate\Http\Request` のインスタンスで `old` メソッドを呼び出します。 `old` メソッドは、以前にフラッシュされた入力データを [session](/docs/master/session) から取得します。

```php
$username = $request->old('username');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/master/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
Laravel は、グローバル `old` ヘルパも提供します。 [Blade template](/docs/master/blade) 内で古い入力を表示している場合は、`old` ヘルパを使用してフォームに再入力する方が便利です。指定されたフィールドに古い入力が存在しない場合は、`null` が返されます。

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
<!-- ### Cookies -->
### Cookies

<a name="retrieving-cookies-from-requests"></a>
<!-- #### Retrieving Cookies From Requests -->
#### Retrieving Cookies From Requests

<!-- All cookies created by the Laravel framework are encrypted and signed with an authentication code, meaning they will be considered invalid if they have been changed by the client. To retrieve a cookie value from the request, use the `cookie` method on an `Illuminate\Http\Request` instance: -->
Laravel フレームワークによって作成されたすべての Cookie は暗号化され、認証コードで署名されます。つまり、クライアントによって変更された場合は無効とみなされます。リクエストから Cookie 値を取得するには、`Illuminate\Http\Request` インスタンスで `cookie` メソッドを使用します。

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
<!-- ## Input Trimming and Normalization -->
## Input Trimming and Normalization

<!-- By default, Laravel includes the `Illuminate\Foundation\Http\Middleware\TrimStrings` and `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` middleware in your application's global middleware stack. These middleware will automatically trim all incoming string fields on the request, as well as convert any empty string fields to `null`. This allows you to not have to worry about these normalization concerns in your routes and controllers. -->
デフォルトでは、Laravel にはアプリケーションのグローバルミドルウェアスタックに `Illuminate\Foundation\Http\Middleware\TrimStrings` および `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` ミドルウェアが含まれています。これらのミドルウェアは、リクエスト上のすべての受信文字列フィールドを自動的にトリミングし、空の文字列フィールドを `null` に変換します。これにより、ルートとコントローラにおけるこれらの正規化の問題を心配する必要がなくなります。

<!-- #### Disabling Input Normalization -->
#### Disabling Input Normalization

<!-- If you would like to disable this behavior for all requests, you may remove the two middleware from your application's middleware stack by invoking the `$middleware->remove` method in your application's `bootstrap/app.php` file: -->
すべてのリクエストに対してこの動作を無効にしたい場合は、アプリケーションの `bootstrap/app.php` ファイルで `$middleware->remove` メソッドを呼び出して、アプリケーションのミドルウェア スタックから 2 つのミドルウェアを削除できます。

```php
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```

<!-- If you would like to disable string trimming and empty string conversion for a subset of requests to your application, you may use the `trimStrings` and `convertEmptyStringsToNull` middleware methods within your application's `bootstrap/app.php` file. Both methods accept an array of closures, which should return `true` or `false` to indicate whether input normalization should be skipped: -->
アプリケーションへのリクエストのサブセットに対して文字列のトリミングと空の文字列の変換を無効にしたい場合は、アプリケーションの `bootstrap/app.php` ファイル内で `trimStrings` および `convertEmptyStringsToNull` ミドルウェア メソッドを使用できます。どちらのメソッドもクロージャの配列を受け入れます。これは、入力正規化をスキップするかどうかを示す `true` または `false` を返す必要があります。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->convertEmptyStringsToNull(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);

    $middleware->trimStrings(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);
})
```

<a name="files"></a>
<!-- ## Files -->
## Files

<a name="retrieving-uploaded-files"></a>
<!-- ### Retrieving Uploaded Files -->
### Retrieving Uploaded Files

<!-- You may retrieve uploaded files from an `Illuminate\Http\Request` instance using the `file` method or using dynamic properties. The `file` method returns an instance of the `Illuminate\Http\UploadedFile` class, which extends the PHP `SplFileInfo` class and provides a variety of methods for interacting with the file: -->
`file` メソッドまたは動的プロパティを使用して、`Illuminate\Http\Request` インスタンスからアップロードされたファイルを取得できます。 `file` メソッドは、PHP `SplFileInfo` クラスを拡張し、ファイルと対話するためのさまざまなメソッドを提供する `Illuminate\Http\UploadedFile` クラスのインスタンスを返します。

```php
$file = $request->file('photo');

$file = $request->photo;
```

<!-- You may determine if a file is present on the request using the `hasFile` method: -->
`hasFile` メソッドを使用して、リクエストにファイルが存在するかどうかを確認できます。

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
<!-- #### Validating Successful Uploads -->
#### Validating Successful Uploads

<!-- In addition to checking if the file is present, you may verify that there were no problems uploading the file via the `isValid` method: -->
ファイルが存在するかどうかを確認するだけでなく、`isValid` メソッドを使用してファイルのアップロードに問題がなかったことを確認することもできます。

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
<!-- #### File Paths and Extensions -->
#### File Paths and Extensions

<!-- The `UploadedFile` class also contains methods for accessing the file's fully-qualified path and its extension. The `extension` method will attempt to guess the file's extension based on its contents. This extension may be different from the extension that was supplied by the client: -->
`UploadedFile` クラスには、ファイルの完全修飾パスとその拡張子にアクセスするためのメソッドも含まれています。 `extension` メソッドは、ファイルの内容に基づいてファイルの拡張子を推測しようとします。この拡張子は、クライアントによって提供された拡張子とは異なる場合があります。

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
<!-- #### Other File Methods -->
#### Other File Methods

<!-- There are a variety of other methods available on `UploadedFile` instances. Check out the [API documentation for the class](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php) for more information regarding these methods. -->
`UploadedFile` インスタンスでは他にもさまざまなメソッドを使用できます。これらの方法の詳細については、[API documentation for the class](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php) を確認してください。

<a name="storing-uploaded-files"></a>
<!-- ### Storing Uploaded Files -->
### Storing Uploaded Files

<!-- To store an uploaded file, you will typically use one of your configured [filesystems](/docs/master/filesystem). The `UploadedFile` class has a `store` method that will move an uploaded file to one of your disks, which may be a location on your local filesystem or a cloud storage location like Amazon S3. -->
アップロードされたファイルを保存するには、通常、構成された [filesystems](/docs/master/filesystem) の 1 つを使用します。 `UploadedFile` クラスには、アップロードされたファイルをディスクの 1 つに移動する `store` メソッドがあります。ディスクは、ローカル ファイル システム上の場所または Amazon S3 などのクラウド ストレージの場所である可能性があります。

<!-- The `store` method accepts the path where the file should be stored relative to the filesystem's configured root directory. This path should not contain a filename, since a unique ID will automatically be generated to serve as the filename. -->
`store` メソッドは、ファイル システムの構成されたルート ディレクトリを基準にしてファイルを保存するパスを受け入れます。ファイル名として機能する一意の ID が自動的に生成されるため、このパスにはファイル名を含めないでください。

<!-- The `store` method also accepts an optional second argument for the name of the disk that should be used to store the file. The method will return the path of the file relative to the disk's root: -->
`store` メソッドは、ファイルの保存に使用するディスク名のオプションの 2 番目の引数も受け入れます。このメソッドは、ディスクのルートを基準としたファイルの相対パスを返します。

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

<!-- If you do not want a filename to be automatically generated, you may use the `storeAs` method, which accepts the path, filename, and disk name as its arguments: -->
ファイル名を自動的に生成したくない場合は、パス、ファイル名、およびディスク名を引数として受け入れる `storeAs` メソッドを使用できます。

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> Laravel のファイルストレージの詳細については、完全な [file storage documentation](/docs/master/filesystem) を確認してください。

<a name="configuring-trusted-proxies"></a>
<!-- ## Configuring Trusted Proxies -->
## Configuring Trusted Proxies

<!-- When running your applications behind a load balancer that terminates TLS / SSL certificates, you may notice your application sometimes does not generate HTTPS links when using the `url` helper. Typically this is because your application is being forwarded traffic from your load balancer on port 80 and does not know it should generate secure links. -->
TLS / SSL 証明書を終了するロード バランサーの背後でアプリケーションを実行する場合、`url` ヘルパの使用時にアプリケーションが HTTPS リンクを生成しないことがあります。通常、これは、アプリケーションがポート 80 上のロード バランサーからトラフィックを転送されており、安全なリンクを生成する必要があることを認識していないことが原因です。

<!-- To solve this, you may enable the `Illuminate\Http\Middleware\TrustProxies` middleware that is included in your Laravel application, which allows you to quickly customize the load balancers or proxies that should be trusted by your application. Your trusted proxies should be specified using the `trustProxies` middleware method in your application's `bootstrap/app.php` file: -->
これを解決するには、Laravel アプリケーションに含まれている `Illuminate\Http\Middleware\TrustProxies` ミドルウェアを有効にすることができます。これにより、アプリケーションが信頼する必要があるロード バランサーまたはプロキシを迅速にカスタマイズできます。信頼できるプロキシは、アプリケーションの `bootstrap/app.php` ファイルで `trustProxies` ミドルウェア メソッドを使用して指定する必要があります。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

<!-- In addition to configuring the trusted proxies, you may also configure the proxy headers that should be trusted: -->
信頼できるプロキシの構成に加えて、信頼すべきプロキシ ヘッダーも構成できます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
        Request::HEADER_X_FORWARDED_HOST |
        Request::HEADER_X_FORWARDED_PORT |
        Request::HEADER_X_FORWARDED_PROTO |
        Request::HEADER_X_FORWARDED_AWS_ELB
    );
})
```

> [!NOTE]
> AWS Elastic Load Balancing を使用している場合、`headers` 値は `Request::HEADER_X_FORWARDED_AWS_ELB` である必要があります。ロード バランサーが [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4) の標準 `Forwarded` ヘッダーを使用する場合、`headers` の値は `Request::HEADER_FORWARDED` である必要があります。 `headers` 値で使用できる定数の詳細については、[trusting proxies](https://symfony.com/doc/current/deployment/proxies.html) に関する Symfony のドキュメントを確認してください。

<a name="trusting-all-proxies"></a>
<!-- #### Trusting All Proxies -->
#### Trusting All Proxies

<!-- If you are using Amazon AWS or another "cloud" load balancer provider, you may not know the IP addresses of your actual balancers. In this case, you may use `*` to trust all proxies: -->
Amazon AWS または別の「クラウド」ロード バランサー プロバイダを使用している場合は、実際のバランサーの IP アドレスがわからない可能性があります。この場合、`*` を使用してすべてのプロキシを信頼できます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
<!-- ## Configuring Trusted Hosts -->
## Configuring Trusted Hosts

<!-- By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request. -->
デフォルトでは、Laravel は、HTTP リクエストの `Host` ヘッダーの内容に関係なく、受信したすべてのリクエストに応答します。さらに、`Host` ヘッダーの値は、Web リクエスト中にアプリケーションへの絶対 URL を生成するときに使用されます。

<!-- Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given hostname. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain hostnames, you may do so by enabling the `Illuminate\Http\Middleware\TrustHosts` middleware for your application. -->
通常、指定されたホスト名に一致するリクエストのみをアプリケーションに送信するように、Nginx や Apache などの Web サーバーを構成する必要があります。ただし、Web サーバーを直接カスタマイズする機能がなく、特定のホスト名にのみ応答するように Laravel に指示する必要がある場合は、アプリケーションの `Illuminate\Http\Middleware\TrustHosts` ミドルウェアを有効にすることでこれを行うことができます。

<!-- To enable the `TrustHosts` middleware, you should invoke the `trustHosts` middleware method in your application's `bootstrap/app.php` file. Using the `at` argument of this method, you may specify the hostnames that your application should respond to. The hostname string is treated as a regular expression. Incoming requests with other `Host` headers will be rejected: -->
`TrustHosts` ミドルウェアを有効にするには、アプリケーションの `bootstrap/app.php` ファイルで `trustHosts` ミドルウェア メソッドを呼び出す必要があります。このメソッドの `at` 引数を使用すると、アプリケーションが応答するホスト名を指定できます。ホスト名の文字列は正規表現として扱われます。他の `Host` ヘッダーを持つ受信リクエストは拒否されます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$']);
})
```

<!-- By default, requests coming from subdomains of the application's URL are also automatically trusted. If you would like to disable this behavior, you may use the `subdomains` argument: -->
デフォルトでは、アプリケーションの URL のサブドメインからのリクエストも自動的に信頼されます。この動作を無効にしたい場合は、`subdomains` 引数を使用できます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
})
```

<!-- If you need to access your application's configuration files or database to determine your trusted hosts, you may provide a closure to the `at` argument: -->
信頼できるホストを判断するためにアプリケーションの構成ファイルまたはデータベースにアクセスする必要がある場合は、`at` 引数にクロージャーを指定できます。

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```

