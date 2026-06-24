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
Laravel은 애플리케이션의 URL을 생성할 때 도움을 주는 다양한 헬퍼 함수를 제공합니다. 이러한 헬퍼들은 주로 템플릿이나 API 응답에서 링크를 만들거나, 애플리케이션의 다른 부분으로 리다이렉트 응답을 생성할 때 유용하게 사용할 수 있습니다.

<a name="the-basics"></a>
<!-- ## The Basics -->
## The Basics

<a name="generating-urls"></a>
<!-- ### Generating URLs -->
### Generating URLs

<!-- The `url` helper may be used to generate arbitrary URLs for your application. The generated URL will automatically use the scheme (HTTP or HTTPS) and host from the current request being handled by the application: -->
`url` 헬퍼를 사용하면 애플리케이션에서 임의의 URL을 생성할 수 있습니다. 이 헬퍼가 반환하는 URL은 현재 애플리케이션이 처리 중인 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 자동으로 사용합니다.

```
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

<a name="accessing-the-current-url"></a>
<!-- ### Accessing the Current URL -->
### Accessing the Current URL

<!-- If no path is provided to the `url` helper, an `Illuminate\Routing\UrlGenerator` instance is returned, allowing you to access information about the current URL: -->
`url` 헬퍼에 경로를 전달하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 다양한 정보를 얻을 수 있습니다.

```
// Get the current URL without the query string...
echo url()->current();

// Get the current URL including the query string...
echo url()->full();

// Get the full URL for the previous request...
echo url()->previous();
```

<!-- Each of these methods may also be accessed via the `URL` [facade](/docs/10.x/facades): -->
이러한 메서드들은 `URL` [facade](/docs/10.x/facades)를 통해서도 사용할 수 있습니다.

```
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
<!-- ## URLs for Named Routes -->
## URLs for Named Routes

<!-- The `route` helper may be used to generate URLs to [named routes](/docs/10.x/routing#named-routes). Named routes allow you to generate URLs without being coupled to the actual URL defined on the route. Therefore, if the route's URL changes, no changes need to be made to your calls to the `route` function. For example, imagine your application contains a route defined like the following: -->
`route` 헬퍼를 사용하면 [named routes](/docs/10.x/routing#named-routes)의 URL을 생성할 수 있습니다. 이름이 지정된 라우트(named route)를 사용하면 실제 라우트의 URL에 직접 의존하지 않고도 URL을 생성할 수 있습니다. 따라서 라우트의 URL이 변경되어도 `route` 함수 호출 자체는 수정할 필요가 없습니다. 예를 들어, 다음과 같이 라우트가 정의되어 있다고 가정해보겠습니다.

```
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

<!-- To generate a URL to this route, you may use the `route` helper like so: -->
이 라우트에 대한 URL을 생성하려면 아래와 같이 `route` 헬퍼를 사용합니다.

```
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

<!-- Of course, the `route` helper may also be used to generate URLs for routes with multiple parameters: -->
물론, `route` 헬퍼는 여러 개의 파라미터를 가진 라우트의 URL도 생성할 수 있습니다.

```
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

<!-- Any additional array elements that do not correspond to the route's definition parameters will be added to the URL's query string: -->
라우트에 정의되지 않은 추가 배열 요소들은 자동으로 URL의 쿼리 스트링에 추가됩니다.

```
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
<!-- #### Eloquent Models -->
#### Eloquent Models

<!-- You will often be generating URLs using the route key (typically the primary key) of [Eloquent models](/docs/10.x/eloquent). For this reason, you may pass Eloquent models as parameter values. The `route` helper will automatically extract the model's route key: -->
URL을 생성할 때 대부분의 경우 [Eloquent models](/docs/10.x/eloquent)의 라우트 키(보통은 기본 키)를 사용하게 됩니다. 이를 위해, Eloquent 모델 인스턴스를 파라미터 값으로 바로 전달할 수 있습니다. `route` 헬퍼가 모델의 라우트 키를 자동으로 추출해 사용합니다.

```
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
<!-- ### Signed URLs -->
### Signed URLs

<!-- Laravel allows you to easily create "signed" URLs to named routes. These URLs have a "signature" hash appended to the query string which allows Laravel to verify that the URL has not been modified since it was created. Signed URLs are especially useful for routes that are publicly accessible yet need a layer of protection against URL manipulation. -->
Laravel에서는 이름이 지정된 라우트에 대해 "서명된" URL을 손쉽게 생성할 수 있습니다. 이러한 URL에는 쿼리 스트링에 "시그니처" 해시가 추가되어 Laravel이 URL이 생성된 이후로 변경되지 않았음을 검증할 수 있습니다. 서명된 URL은 누구나 접근할 수 있는 공개 라우트이면서도, URL 조작에 대한 보호가 필요한 경우에 특히 유용합니다.

<!-- For example, you might use signed URLs to implement a public "unsubscribe" link that is emailed to your customers. To create a signed URL to a named route, use the `signedRoute` method of the `URL` facade: -->
예를 들어, 고객에게 이메일로 발송하는 공개 "구독 취소" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트에 대한 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하면 됩니다.

```
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

<!-- You may exclude the domain from the signed URL hash by providing the `absolute` argument to the `signedRoute` method: -->
서명된 URL의 해시에서 도메인을 제외하고 싶다면 `signedRoute` 메서드에 `absolute` 인수를 제공하면 됩니다.

```
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

<!-- If you would like to generate a temporary signed route URL that expires after a specified amount of time, you may use the `temporarySignedRoute` method. When Laravel validates a temporary signed route URL, it will ensure that the expiration timestamp that is encoded into the signed URL has not elapsed: -->
특정 시간 후에 만료되도록 임시 서명 URL을 만들고 싶다면 `temporarySignedRoute` 메서드를 사용할 수 있습니다. Laravel이 임시 서명 URL을 검증할 때, 서명된 URL에 인코딩된 만료 시간이 아직 지나지 않았는지 확인합니다.

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
들어온 요청이 유효한 서명을 가지고 있는지 확인하려면, 전달받은 `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출하면 됩니다.

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
애플리케이션의 프론트엔드에서 클라이언트 측 페이지네이션 등으로 서명된 URL에 추가 데이터를 붙여 보내야 할 때도 있습니다. 이런 경우, `hasValidSignatureWhileIgnoring` 메서드를 사용하여 서명 검증시 무시할 쿼리 파라미터 목록을 지정할 수 있습니다. 단, 무시 목록에 포함된 파라미터는 누구나 요청에서 값을 변경할 수 있으니 주의해야 합니다.

```
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

<!-- Instead of validating signed URLs using the incoming request instance, you may assign the `Illuminate\Routing\Middleware\ValidateSignature` [middleware](/docs/10.x/middleware) to the route. If it is not already present, you may assign this middleware an alias in your HTTP kernel's `$middlewareAliases` array: -->
요청 인스턴스를 직접 사용하지 않고, 라우트에 `Illuminate\Routing\Middleware\ValidateSignature` [middleware](/docs/10.x/middleware)를 할당하여 서명 URL을 검증할 수도 있습니다. 만약 이 미들웨어가 등록되어 있지 않다면, HTTP 커널의 `$middlewareAliases` 배열에 별칭을 추가하세요.

```
/**
 * The application's middleware aliases.
 *
 * Aliases may be used to conveniently assign middleware to routes and groups.
 *
 * @var array<string, class-string|string>
 */
protected $middlewareAliases = [
    'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
];
```

<!-- Once you have registered the middleware in your kernel, you may attach it to a route. If the incoming request does not have a valid signature, the middleware will automatically return a `403` HTTP response: -->
커널에 미들웨어가 등록되었다면, 해당 미들웨어를 라우트에 붙일 수 있습니다. 요청의 시그니처가 유효하지 않을 경우, 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다.

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

<!-- If your signed URLs do not include the domain in the URL hash, you should provide the `relative` argument to the middleware: -->
만약 서명된 URL의 해시에 도메인이 포함되어 있지 않다면, 미들웨어에 `relative` 인수를 전달합니다.

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
<!-- #### Responding to Invalid Signed Routes -->
#### Responding to Invalid Signed Routes

<!-- When someone visits a signed URL that has expired, they will receive a generic error page for the `403` HTTP status code. However, you can customize this behavior by defining a custom "renderable" closure for the `InvalidSignatureException` exception in your exception handler. This closure should return an HTTP response: -->
누군가 만료된 서명 URL로 접근하면, 일반적으로 `403` HTTP 상태 코드의 에러 페이지가 표시됩니다. 이 동작은 예외 핸들러에서 `InvalidSignatureException` 예외에 대해 커스텀 "렌더러블(renderable)" 클로저를 정의함으로써 직접 제어할 수 있습니다. 이 클로저는 HTTP 응답을 반환해야 합니다.

```
use Illuminate\Routing\Exceptions\InvalidSignatureException;

/**
 * Register the exception handling callbacks for the application.
 */
public function register(): void
{
    $this->renderable(function (InvalidSignatureException $e) {
        return response()->view('error.link-expired', [], 403);
    });
}
```

<a name="urls-for-controller-actions"></a>
<!-- ## URLs for Controller Actions -->
## URLs for Controller Actions

<!-- The `action` function generates a URL for the given controller action: -->
`action` 함수를 사용하면 지정한 컨트롤러 액션에 대한 URL을 생성할 수 있습니다.

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

<!-- If the controller method accepts route parameters, you may pass an associative array of route parameters as the second argument to the function: -->
컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 연관 배열 형태의 파라미터를 전달할 수 있습니다.

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
<!-- ## Default Values -->
## Default Values

<!-- For some applications, you may wish to specify request-wide default values for certain URL parameters. For example, imagine many of your routes define a `{locale}` parameter: -->
어떤 애플리케이션에서는 특정 URL 파라미터에 대해 요청 전체에 적용되는 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 여러 라우트에서 `{locale}` 파라미터를 사용하는 경우를 생각해봅시다.

```
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

<!-- It is cumbersome to always pass the `locale` every time you call the `route` helper. So, you may use the `URL::defaults` method to define a default value for this parameter that will always be applied during the current request. You may wish to call this method from a [route middleware](/docs/10.x/middleware#assigning-middleware-to-routes) so that you have access to the current request: -->
`route` 헬퍼를 호출할 때마다 매번 `locale`을 전달하는 것은 불편할 수 있습니다. 이런 경우 `URL::defaults` 메서드를 사용하면, 현재 요청에서 항상 적용되는 기본값을 지정할 수 있습니다. 이 메서드는 [route middleware](/docs/10.x/middleware#assigning-middleware-to-routes)에서 호출하여 현재 요청 정보에 접근하도록 하는 것이 일반적입니다.

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
`locale` 파라미터의 기본값이 설정되면, `route` 헬퍼로 URL을 생성할 때 값을 별도로 전달하지 않아도 됩니다.

<a name="url-defaults-middleware-priority"></a>
<!-- #### URL Defaults and Middleware Priority -->
#### URL Defaults and Middleware Priority

<!-- Setting URL default values can interfere with Laravel's handling of implicit model bindings. Therefore, you should [prioritize your middleware](/docs/10.x/middleware#sorting-middleware) that set URL defaults to be executed before Laravel's own `SubstituteBindings` middleware. You can accomplish this by making sure your middleware occurs before the `SubstituteBindings` middleware within the `$middlewarePriority` property of your application's HTTP kernel. -->
URL 기본값을 설정하는 미들웨어는 Laravel의 암시적 모델 바인딩 처리와 충돌할 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어는 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [prioritize your middleware](/docs/10.x/middleware#sorting-middleware)를 지정해야 합니다. 이를 위해 애플리케이션 HTTP 커널의 `$middlewarePriority` 속성에서 해당 미들웨어를 `SubstituteBindings`보다 앞에 위치시키세요.

<!-- The `$middlewarePriority` property is defined in the base `Illuminate\Foundation\Http\Kernel` class. You may copy its definition from that class and overwrite it in your application's HTTP kernel in order to modify it: -->
`$middlewarePriority` 속성은 기본적으로 `Illuminate\Foundation\Http\Kernel` 클래스에 정의되어 있습니다. 이 속성을 애플리케이션의 HTTP 커널로 복사해서 순서를 수정할 수 있습니다.

```
/**
 * The priority-sorted list of middleware.
 *
 * This forces non-global middleware to always be in the given order.
 *
 * @var array
 */
protected $middlewarePriority = [
    // ...
     \App\Http\Middleware\SetDefaultLocaleForUrls::class,
     \Illuminate\Routing\Middleware\SubstituteBindings::class,
     // ...
];
```
