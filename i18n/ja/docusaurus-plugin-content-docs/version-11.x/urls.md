<!-- # URL Generation -->
# URL Generation

- [Introduction](#introduction)
- [The Basics](#the-basics)
    - [Generating URLs](#generating-urls)
    - [Accessing the Current URL](#accessing-the-current-url)
- [URLs for Named Routes](#urls-for-named-routes)
    - [Signed URLs](#signed-urls)
- [URLs for Controller Actions](#urls-for-controller-actions)
- [Default Values](#default-values)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides several helpers to assist you in generating URLs for your application. These helpers are primarily helpful when building links in your templates and API responses, or when generating redirect responses to another part of your application. -->
Laravel には、アプリケーションの URL の生成を支援するいくつかのヘルパが用意されています。これらのヘルパは主に、テンプレートや API 応答にリンクを構築するとき、またはアプリケーションの別の部分へのリダイレクト応答を生成するときに役立ちます。

<a name="the-basics"></a>
<!-- ## The Basics -->
## The Basics

<a name="generating-urls"></a>
<!-- ### Generating URLs -->
### Generating URLs

<!-- The `url` helper may be used to generate arbitrary URLs for your application. The generated URL will automatically use the scheme (HTTP or HTTPS) and host from the current request being handled by the application: -->
`url` ヘルパは、アプリケーションの任意の URL を生成するために使用できます。生成された URL は、アプリケーションによって処理されている現在のリクエストのスキーム (HTTP または HTTPS) とホストを自動的に使用します。

```
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

<!-- To generate a URL with query string parameters, you may use the `query` method: -->
クエリ文字列パラメーターを含む URL を生成するには、`query` メソッドを使用できます。

```
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

<!-- Providing query string parameters that already exist in the path will overwrite their existing value: -->
パス内にすでに存在するクエリ文字列パラメーターを指定すると、既存の値が上書きされます。

```
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

<!-- Arrays of values may also be passed as query parameters. These values will be properly keyed and encoded in the generated URL: -->
値の配列をクエリ パラメーターとして渡すこともできます。これらの値は、生成された URL 内で適切にキー設定され、エンコードされます。

```
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
<!-- ### Accessing the Current URL -->
### Accessing the Current URL

<!-- If no path is provided to the `url` helper, an `Illuminate\Routing\UrlGenerator` instance is returned, allowing you to access information about the current URL: -->
`url` ヘルパにパスが指定されていない場合は、`Illuminate\Routing\UrlGenerator` インスタンスが返され、現在の URL に関する情報にアクセスできるようになります。

```
// Get the current URL without the query string...
echo url()->current();

// Get the current URL including the query string...
echo url()->full();

// Get the full URL for the previous request...
echo url()->previous();

// Get the path for the previous request...
echo url()->previousPath();
```

<!-- Each of these methods may also be accessed via the `URL` [facade](/docs/11.x/facades): -->
これらの各メソッドには、`URL` [facade](/docs/11.x/facades) 経由でもアクセスできます。

```
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
<!-- ## URLs for Named Routes -->
## URLs for Named Routes

<!-- The `route` helper may be used to generate URLs to [named routes](/docs/11.x/routing#named-routes). Named routes allow you to generate URLs without being coupled to the actual URL defined on the route. Therefore, if the route's URL changes, no changes need to be made to your calls to the `route` function. For example, imagine your application contains a route defined like the following: -->
`route` ヘルパを使用して、[named routes](/docs/11.x/routing#named-routes) への URL を生成できます。名前付きルートを使用すると、ルート上で定義された実際の URL に結合せずに URL を生成できます。したがって、ルートの URL が変更された場合、`route` 関数の呼び出しを変更する必要はありません。たとえば、アプリケーションに次のように定義されたルートが含まれていると想像してください。

```
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

<!-- To generate a URL to this route, you may use the `route` helper like so: -->
このルートへの URL を生成するには、次のように `route` ヘルパを使用します。

```
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

<!-- Of course, the `route` helper may also be used to generate URLs for routes with multiple parameters: -->
もちろん、`route` ヘルパを使用して、複数のパラメータを持つルートの URL を生成することもできます。

```
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

<!-- Any additional array elements that do not correspond to the route's definition parameters will be added to the URL's query string: -->
ルートの定義パラメーターに対応しない追加の配列要素は、URL のクエリ文字列に追加されます。

```
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
<!-- #### Eloquent Models -->
#### Eloquent Models

<!-- You will often be generating URLs using the route key (typically the primary key) of [Eloquent models](/docs/11.x/eloquent). For this reason, you may pass Eloquent models as parameter values. The `route` helper will automatically extract the model's route key: -->
多くの場合、[Eloquent models](/docs/11.x/eloquent) のルート キー (通常は主キー) を使用して URL を生成します。このため、Eloquent モデルをパラメーター値として渡すことができます。 `route` ヘルパは、モデルのルート キーを自動的に抽出します。

```
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
<!-- ### Signed URLs -->
### Signed URLs

<!-- Laravel allows you to easily create "signed" URLs to named routes. These URLs have a "signature" hash appended to the query string which allows Laravel to verify that the URL has not been modified since it was created. Signed URLs are especially useful for routes that are publicly accessible yet need a layer of protection against URL manipulation. -->
Laravel を使用すると、名前付きルートへの「署名付き」URL を簡単に作成できます。これらの URL にはクエリ文字列に「署名」ハッシュが追加されており、これにより Laravel は URL が作成されてから変更されていないことを確認できます。署名付き URL は、公的にアクセス可能でありながら、URL 操作に対する保護層が必要なルートに特に役立ちます。

<!-- For example, you might use signed URLs to implement a public "unsubscribe" link that is emailed to your customers. To create a signed URL to a named route, use the `signedRoute` method of the `URL` facade: -->
たとえば、署名付き URL を使用して、顧客に電子メールで送信される公開「購読解除」リンクを実装できます。名前付きルートへの署名付き URL を作成するには、`URL` ファサードの `signedRoute` メソッドを使用します。

```
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

<!-- You may exclude the domain from the signed URL hash by providing the `absolute` argument to the `signedRoute` method: -->
`absolute` 引数を `signedRoute` メソッドに指定することで、署名付き URL ハッシュからドメインを除外できます。

```
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

<!-- If you would like to generate a temporary signed route URL that expires after a specified amount of time, you may use the `temporarySignedRoute` method. When Laravel validates a temporary signed route URL, it will ensure that the expiration timestamp that is encoded into the signed URL has not elapsed: -->
指定した時間が経過すると期限切れになる一時的な署名付きルート URL を生成したい場合は、`temporarySignedRoute` メソッドを使用できます。 Laravel は、一時的な署名付きルート URL を検証するときに、署名付き URL にエンコードされている有効期限タイムスタンプが経過していないことを確認します。

```
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->addMinutes(30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
<!-- #### Validating Signed Route Requests -->
#### Validating Signed Route Requests

<!-- To verify that an incoming request has a valid signature, you should call the `hasValidSignature` method on the incoming `Illuminate\Http\Request` instance: -->
受信リクエストに有効な署名があることを確認するには、受信 `Illuminate\Http\Request` インスタンスで `hasValidSignature` メソッドを呼び出す必要があります。

```
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

<!-- Sometimes, you may need to allow your application's frontend to append data to a signed URL, such as when performing client-side pagination. Therefore, you can specify request query parameters that should be ignored when validating a signed URL using the `hasValidSignatureWhileIgnoring` method. Remember, ignoring parameters allows anyone to modify those parameters on the request: -->
場合によっては、クライアント側でページネーションを実行する場合など、アプリケーションのフロントエンドが署名付き URL にデータを追加できるようにする必要があります。したがって、`hasValidSignatureWhileIgnoring` メソッドを使用して署名付き URL を検証するときに無視する必要があるリクエスト クエリ パラメーターを指定できます。パラメーターを無視すると、誰でもリクエストでそれらのパラメーターを変更できるようになることに注意してください。

```
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

<!-- Instead of validating signed URLs using the incoming request instance, you may assign the `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [middleware](/docs/11.x/middleware) to the route. If the incoming request does not have a valid signature, the middleware will automatically return a `403` HTTP response: -->
受信リクエスト インスタンスを使用して署名付き URL を検証する代わりに、`signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [middleware](/docs/11.x/middleware) をルートに割り当てることができます。受信リクエストに有効な署名がない場合、ミドルウェアは自動的に `403` HTTP レスポンスを返します。

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

<!-- If your signed URLs do not include the domain in the URL hash, you should provide the `relative` argument to the middleware: -->
署名付き URL の URL ハッシュにドメインが含まれていない場合は、`relative` 引数をミドルウェアに提供する必要があります。

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
<!-- #### Responding to Invalid Signed Routes -->
#### Responding to Invalid Signed Routes

<!-- When someone visits a signed URL that has expired, they will receive a generic error page for the `403` HTTP status code. However, you can customize this behavior by defining a custom "render" closure for the `InvalidSignatureException` exception in your application's `bootstrap/app.php` file: -->
有効期限が切れた署名付き URL にアクセスすると、`403` HTTP ステータス コードの一般的なエラー ページが表示されます。ただし、アプリケーションの `bootstrap/app.php` ファイルで `InvalidSignatureException` 例外のカスタム "render" クロージャを定義することで、この動作をカスタマイズできます。

```
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions) {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
<!-- ## URLs for Controller Actions -->
## URLs for Controller Actions

<!-- The `action` function generates a URL for the given controller action: -->
`action` 関数は、指定されたコントローラ アクションの URL を生成します。

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

<!-- If the controller method accepts route parameters, you may pass an associative array of route parameters as the second argument to the function: -->
コントローラ メソッドがルート パラメーターを受け入れる場合、ルート パラメーターの連想配列を 2 番目の引数として関数に渡すことができます。

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
<!-- ## Default Values -->
## Default Values

<!-- For some applications, you may wish to specify request-wide default values for certain URL parameters. For example, imagine many of your routes define a `{locale}` parameter: -->
一部のアプリケーションでは、特定の URL パラメータに対してリクエスト全体のデフォルト値を指定することが必要な場合があります。たとえば、多くのルートで `{locale}` パラメータが定義されていると想像してください。

```
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

<!-- It is cumbersome to always pass the `locale` every time you call the `route` helper. So, you may use the `URL::defaults` method to define a default value for this parameter that will always be applied during the current request. You may wish to call this method from a [route middleware](/docs/11.x/middleware#assigning-middleware-to-routes) so that you have access to the current request: -->
`route` ヘルパを呼び出すたびに、常に `locale` を渡すのは面倒です。したがって、`URL::defaults` メソッドを使用して、現在のリクエスト中に常に適用されるこのパラメータのデフォルト値を定義できます。現在のリクエストにアクセスできるように、[route middleware](/docs/11.x/middleware#assigning-middleware-to-routes) からこのメソッドを呼び出すこともできます。

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\URL;
use Symfony\Component\HttpFoundation\Response;

class SetDefaultLocaleForUrls
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        URL::defaults(['locale' => $request->user()->locale]);

        return $next($request);
    }
}
```

<!-- Once the default value for the `locale` parameter has been set, you are no longer required to pass its value when generating URLs via the `route` helper. -->
`locale` パラメータのデフォルト値を設定すると、`route` ヘルパを介して URL を生成するときにその値を渡す必要はなくなります。

<a name="url-defaults-middleware-priority"></a>
<!-- #### URL Defaults and Middleware Priority -->
#### URL Defaults and Middleware Priority

<!-- Setting URL default values can interfere with Laravel's handling of implicit model bindings. Therefore, you should [prioritize your middleware](/docs/11.x/middleware#sorting-middleware) that set URL defaults to be executed before Laravel's own `SubstituteBindings` middleware. You can accomplish this using the `priority` middleware method in your application's `bootstrap/app.php` file: -->
URL のデフォルト値を設定すると、Laravel による暗黙的なモデルバインディングの処理が妨げられる可能性があります。したがって、URL のデフォルトを設定する [prioritize your middleware](/docs/11.x/middleware#sorting-middleware) は、Laravel 独自の `SubstituteBindings` ミドルウェアよりも前に実行する必要があります。これは、アプリケーションの `bootstrap/app.php` ファイルで `priority` ミドルウェア メソッドを使用して実現できます。

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```

