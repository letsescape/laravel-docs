<!-- # URL Generation -->
# URL Generation

- [Introduction](#introduction)
- [The Basics](#the-basics)
    - [Generating URLs](#generating-urls)
    - [Accessing the Current URL](#accessing-the-current-url)
- [URLs for Named Routes](#urls-for-named-routes)
    - [Signed URLs](#signed-urls)
- [URLs for Controller Actions](#urls-for-controller-actions)
- [Fluent URI Objects](#fluent-uri-objects)
- [Default Values](#default-values)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides several helpers to assist you in generating URLs for your application. These helpers are primarily helpful when building links in your templates and API responses, or when generating redirect responses to another part of your application. -->
Laravel은 애플리케이션의 URL을 생성할 때 사용할 수 있는 여러 헬퍼를 제공합니다. 이러한 헬퍼는 주로 템플릿이나 API 응답에서 링크를 생성하거나, 애플리케이션 내 다른 위치로 리다이렉트 응답을 보낼 때 유용합니다.

<a name="the-basics"></a>
<!-- ## The Basics -->
## The Basics

<a name="generating-urls"></a>
<!-- ### Generating URLs -->
### Generating URLs

<!-- The `url` helper may be used to generate arbitrary URLs for your application. The generated URL will automatically use the scheme (HTTP or HTTPS) and host from the current request being handled by the application: -->
`url` 헬퍼를 사용하면 애플리케이션에서 원하는 임의의 URL을 생성할 수 있습니다. 생성되는 URL은 현재 애플리케이션이 처리 중인 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 자동으로 사용합니다:

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

<!-- To generate a URL with query string parameters, you may use the `query` method: -->
쿼리 문자열 파라미터가 포함된 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

<!-- Providing query string parameters that already exist in the path will overwrite their existing value: -->
이미 경로(path)에 존재하는 쿼리 문자열 파라미터에 대해 새로운 값을 제공하면 해당 값이 덮어써집니다:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

<!-- Arrays of values may also be passed as query parameters. These values will be properly keyed and encoded in the generated URL: -->
배열 형태의 값을 쿼리 파라미터로 전달하는 것도 가능합니다. 이 값들은 자동으로 올바르게 키-값 형태로 인코딩되어 URL에 추가됩니다:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
<!-- ### Accessing the Current URL -->
### Accessing the Current URL

<!-- If no path is provided to the `url` helper, an `Illuminate\Routing\UrlGenerator` instance is returned, allowing you to access information about the current URL: -->
`url` 헬퍼에 경로를 전달하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스를 반환하여 현재 URL에 대한 정보를 얻을 수 있습니다:

```php
// Get the current URL without the query string...
echo url()->current();

// Get the current URL including the query string...
echo url()->full();
```

<!-- Each of these methods may also be accessed via the `URL` [facade](/docs/13.x/facades): -->
이 메서드들은 `URL` [facade](/docs/13.x/facades)를 통해서도 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="accessing-the-previous-url"></a>
<!-- #### Accessing the Previous URL -->
#### Accessing the Previous URL

<!-- Sometimes it is helpful to know the previous URL that the user is visiting from. You can access the previous URL via the `url` helper's `previous` and `previousPath` methods: -->
사용자가 직전에 방문한 URL을 알아야 할 때가 있을 수 있습니다. 이때 `url` 헬퍼의 `previous` 및 `previousPath` 메서드로 이전 URL을 확인할 수 있습니다:

```php
// Get the full URL for the previous request...
echo url()->previous();

// Get the path for the previous request...
echo url()->previousPath();
```

<!-- Or, via the [session](/docs/13.x/session), you may access the previous URL as a [fluent URI](#fluent-uri-objects) instance: -->
또는 [session](/docs/13.x/session)을 이용해서 [fluent URI](#fluent-uri-objects) 형태로 이전 URL을 가져올 수도 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/users', function (Request $request) {
    $previousUri = $request->session()->previousUri();

    // ...
});
```

<!-- It is also possible to retrieve the route name for the previously visited URL via the session: -->
또한 세션을 통해서 이전에 방문했던 라우트의 이름을 가져오는 것도 가능합니다:

```php
$previousRoute = $request->session()->previousRoute();
```

<a name="urls-for-named-routes"></a>
<!-- ## URLs for Named Routes -->
## URLs for Named Routes

<!-- The `route` helper may be used to generate URLs to [named routes](/docs/13.x/routing#named-routes). Named routes allow you to generate URLs without being coupled to the actual URL defined on the route. Therefore, if the route's URL changes, no changes need to be made to your calls to the `route` function. For example, imagine your application contains a route defined like the following: -->
`route` 헬퍼를 사용하면 [named routes](/docs/13.x/routing#named-routes)에 대한 URL을 생성할 수 있습니다. 네임드 라우트를 사용하면 라우트에 지정된 실제 URL에 의존하지 않고도 원하는 URL을 생성할 수 있으므로, 라우트의 URL이 변경되어도 `route` 함수 호출을 수정할 필요가 없습니다. 예를 들어, 애플리케이션에 아래와 같은 라우트가 있다고 가정해봅니다:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

<!-- To generate a URL to this route, you may use the `route` helper like so: -->
이 라우트에 대한 URL을 생성하려면 아래처럼 `route` 헬퍼를 사용합니다:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

<!-- Of course, the `route` helper may also be used to generate URLs for routes with multiple parameters: -->
물론, `route` 헬퍼로 여러 개의 파라미터를 가진 라우트의 URL도 생성할 수 있습니다:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

<!-- Any additional array elements that do not correspond to the route's definition parameters will be added to the URL's query string: -->
라우트 정의에 없는 배열 요소들은 URL의 쿼리 문자열로 추가됩니다:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
<!-- #### Eloquent Models -->
#### Eloquent Models

<!-- You will often be generating URLs using the route key (typically the primary key) of [Eloquent models](/docs/13.x/eloquent). For this reason, you may pass Eloquent models as parameter values. The `route` helper will automatically extract the model's route key: -->
[Eloquent models](/docs/13.x/eloquent)의 라우트 키(주로 기본키)를 사용해 URL을 생성하는 일이 자주 있습니다. 이 경우 파라미터 값으로 Eloquent 모델을 전달하면, `route` 헬퍼가 자동으로 모델의 라우트 키를 추출하여 사용합니다:

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
<!-- ### Signed URLs -->
### Signed URLs

<!-- Laravel allows you to easily create "signed" URLs to named routes. These URLs have a "signature" hash appended to the query string which allows Laravel to verify that the URL has not been modified since it was created. Signed URLs are especially useful for routes that are publicly accessible yet need a layer of protection against URL manipulation. -->
Laravel에서는 네임드 라우트에 대해 "서명된" URL을 쉽게 생성할 수 있습니다. 이러한 URL에는 쿼리 문자열에 "signature" 해시가 추가되어, URL 생성 이후에 변경되지 않았는지 Laravel이 검증할 수 있도록 해줍니다. 서명된 URL은 공개 접근이 가능한 라우트이지만 URL 자체의 변조를 방지해야 하는 경우에 특히 유용합니다.

<!-- For example, you might use signed URLs to implement a public "unsubscribe" link that is emailed to your customers. To create a signed URL to a named route, use the `signedRoute` method of the `URL` facade: -->
예를 들어, 고객에게 이메일로 발송하는 공개 "구독 해지" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 네임드 라우트에 대한 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

<!-- You may exclude the domain from the signed URL hash by providing the `absolute` argument to the `signedRoute` method: -->
`signedRoute` 메서드의 `absolute` 인수를 사용하면 서명된 URL 해시에서 도메인을 제외할 수 있습니다:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

<!-- If you would like to generate a temporary signed route URL that expires after a specified amount of time, you may use the `temporarySignedRoute` method. When Laravel validates a temporary signed route URL, it will ensure that the expiration timestamp that is encoded into the signed URL has not elapsed: -->
지정한 시간 이후 만료되는 임시 서명 라우트 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용합니다. 이때 Laravel은 서명된 URL에서 인코딩된 만료 타임스탬프가 경과하지 않았는지 검사합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->plus(minutes: 30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
<!-- #### Validating Signed Route Requests -->
#### Validating Signed Route Requests

<!-- To verify that an incoming request has a valid signature, you should call the `hasValidSignature` method on the incoming `Illuminate\Http\Request` instance: -->
들어오는 요청이 유효한 서명을 가지고 있는지 확인하려면 요청 객체(`Illuminate\Http\Request`)에서 `hasValidSignature` 메서드를 호출하면 됩니다:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

<!-- Sometimes, you may need to allow your application's frontend to append data to a signed URL, such as when performing client-side pagination. Therefore, you can specify request query parameters that should be ignored when validating a signed URL using the `hasValidSignatureWhileIgnoring` method. Remember, ignoring parameters allows anyone to modify those parameters on the request: -->
때때로, 프론트엔드에서 클라이언트 측 페이지네이션 등으로 인해 서명된 URL에 추가 데이터를 덧붙여야 할 수 있습니다. 이 경우, `hasValidSignatureWhileIgnoring` 메서드를 사용하여 검증에서 무시할 쿼리 파라미터를 지정할 수 있습니다. 참고로, 무시 처리된 파라미터는 누구나 자유롭게 수정할 수 있습니다:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

<!-- Instead of validating signed URLs using the incoming request instance, you may assign the `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [middleware](/docs/13.x/middleware) to the route. If the incoming request does not have a valid signature, the middleware will automatically return a `403` HTTP response: -->
요청 객체 대신 [middleware](/docs/13.x/middleware)를 사용하여 서명된 URL을 검증할 수도 있습니다. 해당 라우트에 `signed`(`Illuminate\Routing\Middleware\ValidateSignature`) 미들웨어를 할당하면, 요청이 유효한 서명을 가지지 않은 경우 자동으로 `403` HTTP 응답을 반환합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

<!-- If your signed URLs do not include the domain in the URL hash, you should provide the `relative` argument to the middleware: -->
만약 서명된 URL 해시에 도메인이 포함되어 있지 않다면, 미들웨어에 `relative` 인수를 전달해야 합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
<!-- #### Responding to Invalid Signed Routes -->
#### Responding to Invalid Signed Routes

<!-- When someone visits a signed URL that has expired, they will receive a generic error page for the `403` HTTP status code. However, you can customize this behavior by defining a custom "render" closure for the `InvalidSignatureException` exception in your application's `bootstrap/app.php` file: -->
누군가 만료된 서명 URL에 방문하면, 기본적으로 `403` HTTP 상태 코드의 일반 오류 페이지가 표시됩니다. 하지만, 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대해 커스텀 "렌더" 클로저를 정의하여 이 동작을 변경할 수 있습니다:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
<!-- ## URLs for Controller Actions -->
## URLs for Controller Actions

<!-- The `action` function generates a URL for the given controller action: -->
`action` 함수를 사용하면 지정한 컨트롤러 액션에 대한 URL을 생성할 수 있습니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

<!-- If the controller method accepts route parameters, you may pass an associative array of route parameters as the second argument to the function: -->
컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 키-값 형태의 연관 배열을 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="fluent-uri-objects"></a>
<!-- ## Fluent URI Objects -->
## Fluent URI Objects

<!-- Laravel's `Uri` class provides a convenient and fluent interface for creating and manipulating URIs via objects. This class wraps the functionality provided by the underlying League URI package and integrates seamlessly with Laravel's routing system. -->
Laravel의 `Uri` 클래스는 객체를 통해 URI를 쉽게 생성·조작할 수 있는 플루언트 인터페이스를 제공합니다. 이 클래스는 내부적으로 League URI 패키지의 기능을 감싸면서, Laravel의 라우팅 시스템과 자연스럽게 연동됩니다.

<!-- You can create a `Uri` instance easily using static methods: -->
정적 메서드를 이용해 간단히 `Uri` 인스턴스를 만들 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// Generate a URI instance from the given string...
$uri = Uri::of('https://example.com/path');

// Generate URI instances to paths, named routes, or controller actions...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// Generate a URI instance from the current request URL...
$uri = $request->uri();

// Generate a URI instance from the previous request URL...
$uri = $request->session()->previousUri();
```

<!-- Once you have a URI instance, you can fluently modify it: -->
URI 인스턴스를 이용하면 다음과 같이 플루언트하게 URI를 수정할 수 있습니다:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

<!-- For more information on working with fluent URI objects, consult the [URI documentation](/docs/13.x/helpers#uri). -->
플루언트 URI 객체 활용에 대한 자세한 내용은 [URI documentation](/docs/13.x/helpers#uri)를 참고하시기 바랍니다.

<a name="default-values"></a>
<!-- ## Default Values -->
## Default Values

<!-- For some applications, you may wish to specify request-wide default values for certain URL parameters. For example, imagine many of your routes define a `{locale}` parameter: -->
일부 애플리케이션에서는 특정 URL 파라미터에 대해 전체 요청 범위에서 사용할 기본값을 설정하고자 할 수 있습니다. 예를 들어, 많은 라우트에 `{locale}` 파라미터가 포함되어 있다면:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

<!-- It is cumbersome to always pass the `locale` every time you call the `route` helper. So, you may use the `URL::defaults` method to define a default value for this parameter that will always be applied during the current request. You may wish to call this method from a [route middleware](/docs/13.x/middleware#assigning-middleware-to-routes) so that you have access to the current request: -->
매번 `route` 헬퍼를 호출할 때마다 `locale` 값을 직접 전달하는 것은 번거로울 수 있습니다. 이를 위해 `URL::defaults` 메서드를 사용하여 해당 파라미터의 기본값을 현재 요청 동안 항상 적용되도록 지정할 수 있습니다. 이 메서드는 [route middleware](/docs/13.x/middleware#assigning-middleware-to-routes)에서 호출하면 현재 요청에 접근할 수 있어 유용합니다:

```php
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
`locale` 파라미터에 대한 기본값을 세팅하면, `route` 헬퍼로 URL을 생성할 때 해당 값을 더 이상 전달하지 않아도 됩니다.

<a name="url-defaults-middleware-priority"></a>
<!-- #### URL Defaults and Middleware Priority -->
#### URL Defaults and Middleware Priority

<!-- Setting URL default values can interfere with Laravel's handling of implicit model bindings. Therefore, you should [prioritize your middleware](/docs/13.x/middleware#sorting-middleware) that set URL defaults to be executed before Laravel's own `SubstituteBindings` middleware. You can accomplish this using the `priority` middleware method in your application's `bootstrap/app.php` file: -->
URL 기본값을 설정하면 Laravel의 암묵적 모델 바인딩 처리에 영향을 미칠 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어가 Laravel 자체의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [prioritize your middleware](/docs/13.x/middleware#sorting-middleware)를 지정해야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 사용해 설정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```
