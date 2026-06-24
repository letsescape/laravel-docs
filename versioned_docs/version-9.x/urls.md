<!-- # URL Generation -->
# URL Generation

- [Introduction](#introduction)
- [The Basics](#the-basics)
    - [Generating URLs](#generating-urls)
    - [Accessing The Current URL](#accessing-the-current-url)
- [URLs For Named Routes](#urls-for-named-routes)
    - [Signed URLs](#signed-urls)
- [URLs For Controller Actions](#urls-for-controller-actions)
- [Default Values](#default-values)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides several helpers to assist you in generating URLs for your application. These helpers are primarily helpful when building links in your templates and API responses, or when generating redirect responses to another part of your application. -->
Laravel은 애플리케이션에서 URL을 생성할 때 편리하게 사용할 수 있는 여러 헬퍼 함수를 제공합니다. 이 헬퍼들은 주로 템플릿과 API 응답에서의 링크 생성이나, 애플리케이션 내 다른 위치로 리디렉션을 할 때 유용하게 사용됩니다.

<a name="the-basics"></a>
<!-- ## The Basics -->
## The Basics

<a name="generating-urls"></a>
<!-- ### Generating URLs -->
### Generating URLs

<!-- The `url` helper may be used to generate arbitrary URLs for your application. The generated URL will automatically use the scheme (HTTP or HTTPS) and host from the current request being handled by the application: -->
`url` 헬퍼 함수를 사용하여 애플리케이션의 임의의 URL을 생성할 수 있습니다. 이 때 생성되는 URL은 처리 중인 현재 요청의 스킴(HTTP 또는 HTTPS)과 호스트 정보를 자동으로 반영합니다.

```
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

<a name="accessing-the-current-url"></a>
<!-- ### Accessing The Current URL -->
### Accessing The Current URL

<!-- If no path is provided to the `url` helper, an `Illuminate\Routing\UrlGenerator` instance is returned, allowing you to access information about the current URL: -->
`url` 헬퍼에 경로를 전달하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어, 현재 URL에 관한 정보를 조회할 수 있습니다.

```
// Get the current URL without the query string...
echo url()->current();

// Get the current URL including the query string...
echo url()->full();

// Get the full URL for the previous request...
echo url()->previous();
```

<!-- Each of these methods may also be accessed via the `URL` [facade](/docs/9.x/facades): -->
이러한 메서드들은 [facade](/docs/9.x/facades)인 `URL`을 통해서도 사용할 수 있습니다.

```
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
<!-- ## URLs For Named Routes -->
## URLs For Named Routes

<!-- The `route` helper may be used to generate URLs to [named routes](/docs/9.x/routing#named-routes). Named routes allow you to generate URLs without being coupled to the actual URL defined on the route. Therefore, if the route's URL changes, no changes need to be made to your calls to the `route` function. For example, imagine your application contains a route defined like the following: -->
`route` 헬퍼는 [named routes](/docs/9.x/routing#named-routes)로 이동하는 URL을 생성할 때 사용합니다. 이름이 지정된 라우트를 사용하면 실제 라우트의 URL에 직접 의존하지 않아도 되어, 라우트 URL이 변경되더라도 `route` 함수 호출 코드를 수정할 필요가 없습니다. 예를 들어, 아래와 같은 라우트가 있다고 가정해보겠습니다.

```
Route::get('/post/{post}', function (Post $post) {
    //
})->name('post.show');
```

<!-- To generate a URL to this route, you may use the `route` helper like so: -->
이 라우트로 이동하는 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용하면 됩니다.

```
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

<!-- Of course, the `route` helper may also be used to generate URLs for routes with multiple parameters: -->
물론, `route` 헬퍼는 여러 개의 파라미터를 가지는 라우트에 대해서도 URL을 생성할 수 있습니다.

```
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    //
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

<!-- Any additional array elements that do not correspond to the route's definition parameters will be added to the URL's query string: -->
라우트 정의에 없는 추가 배열 요소들은 URL의 쿼리 문자열로 자동으로 추가됩니다.

```
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
<!-- #### Eloquent Models -->
#### Eloquent Models

<!-- You will often be generating URLs using the route key (typically the primary key) of [Eloquent models](/docs/9.x/eloquent). For this reason, you may pass Eloquent models as parameter values. The `route` helper will automatically extract the model's route key: -->
[Eloquent models](/docs/9.x/eloquent)의 라우트 키(보통 기본 키 값)를 이용해 URL을 생성하는 경우가 많습니다. 이런 경우, 파라미터 값으로 Eloquent 모델을 직접 전달할 수 있으며, `route` 헬퍼가 모델의 라우트 키를 자동으로 추출하여 사용합니다.

```
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
<!-- ### Signed URLs -->
### Signed URLs

<!-- Laravel allows you to easily create "signed" URLs to named routes. These URLs have a "signature" hash appended to the query string which allows Laravel to verify that the URL has not been modified since it was created. Signed URLs are especially useful for routes that are publicly accessible yet need a layer of protection against URL manipulation. -->
Laravel은 이름이 지정된 라우트에 대해 "서명된" URL을 손쉽게 만들 수 있도록 지원합니다. 서명된 URL은 쿼리 문자열에 "서명(signature)" 해시값이 추가되어, 생성 이후 URL이 변경되지 않았음을 Laravel이 검증할 수 있도록 해줍니다. 서명된 URL은 외부에 공개되지만 URL 변조로부터 보호해야 하는 라우트에서 특히 유용합니다.

<!-- For example, you might use signed URLs to implement a public "unsubscribe" link that is emailed to your customers. To create a signed URL to a named route, use the `signedRoute` method of the `URL` facade: -->
예를 들어, 이메일로 전송하는 공개 "구독 해지" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 이름이 지정된 라우트의 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요.

```
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

<!-- If you would like to generate a temporary signed route URL that expires after a specified amount of time, you may use the `temporarySignedRoute` method. When Laravel validates a temporary signed route URL, it will ensure that the expiration timestamp that is encoded into the signed URL has not elapsed: -->
지정한 시간 후 만료되는 임시 서명 URL을 만들고 싶다면 `temporarySignedRoute` 메서드를 사용할 수 있습니다. 이 경우 Laravel은 서명된 URL 안에 암호화된 만료 타임스탬프가 아직 유효한지 확인합니다.

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
들어오는 요청이 유효한 서명을 가지고 있는지 확인하려면, 요청 객체(`Illuminate\Http\Request`)에서 `hasValidSignature` 메서드를 호출해야 합니다.

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
때로는, 프론트엔드에서 페이지네이션 등으로 URL에 데이터를 추가해야 할 수도 있습니다. 이럴 경우, 인증에서 무시해야 할 쿼리 파라미터를 `hasValidSignatureWhileIgnoring` 메서드에 지정할 수 있습니다. 단, 무시된 파라미터는 누구나 자유롭게 수정할 수 있다는 점을 주의하세요.

```
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

<!-- Instead of validating signed URLs using the incoming request instance, you may assign the `Illuminate\Routing\Middleware\ValidateSignature` [middleware](/docs/9.x/middleware) to the route. If it is not already present, you should assign this middleware a key in your HTTP kernel's `routeMiddleware` array: -->
서명된 URL을 직접 검증하는 대신, 라우트에 `Illuminate\Routing\Middleware\ValidateSignature` [middleware](/docs/9.x/middleware)를 부여할 수도 있습니다. 만약 이 미들웨어가 등록되어 있지 않다면 HTTP 커널의 `routeMiddleware` 배열에 키를 할당해 추가합니다.

```
/**
 * The application's route middleware.
 *
 * These middleware may be assigned to groups or used individually.
 *
 * @var array
 */
protected $routeMiddleware = [
    'signed' => \Illuminate\Routing\Middleware\ValidateSignature::class,
];
```

<!-- Once you have registered the middleware in your kernel, you may attach it to a route. If the incoming request does not have a valid signature, the middleware will automatically return a `403` HTTP response: -->
미들웨어 등록을 마쳤다면, 라우트에 해당 미들웨어를 적용할 수 있습니다. 요청이 유효한 서명을 포함하지 않은 경우 미들웨어는 자동으로 `403` HTTP 응답을 반환합니다.

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

<a name="responding-to-invalid-signed-routes"></a>
<!-- #### Responding To Invalid Signed Routes -->
#### Responding To Invalid Signed Routes

<!-- When someone visits a signed URL that has expired, they will receive a generic error page for the `403` HTTP status code. However, you can customize this behavior by defining a custom "renderable" closure for the `InvalidSignatureException` exception in your exception handler. This closure should return an HTTP response: -->
사용자가 만료된 서명 URL에 접근하면, 기본적으로 `403` HTTP 상태 코드에 해당하는 일반적인 에러 페이지가 표시됩니다. 하지만 예외 처리기에서 `InvalidSignatureException` 예외에 대한 커스텀 "renderable" 클로저를 정의하여 이 동작을 원하는 대로 맞춤 설정할 수 있습니다. 이 클로저는 HTTP 응답을 반환해야 합니다.

```
use Illuminate\Routing\Exceptions\InvalidSignatureException;

/**
 * Register the exception handling callbacks for the application.
 *
 * @return void
 */
public function register()
{
    $this->renderable(function (InvalidSignatureException $e) {
        return response()->view('error.link-expired', [], 403);
    });
}
```

<a name="urls-for-controller-actions"></a>
<!-- ## URLs For Controller Actions -->
## URLs For Controller Actions

<!-- The `action` function generates a URL for the given controller action: -->
`action` 함수는 지정한 컨트롤러 액션에 해당하는 URL을 생성합니다.

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

<!-- If the controller method accepts route parameters, you may pass an associative array of route parameters as the second argument to the function: -->
만약 컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인수로 연관 배열 형태의 파라미터를 전달할 수 있습니다.

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
<!-- ## Default Values -->
## Default Values

<!-- For some applications, you may wish to specify request-wide default values for certain URL parameters. For example, imagine many of your routes define a `{locale}` parameter: -->
일부 애플리케이션에서는 특정 URL 파라미터에 대해 요청마다 기본값을 지정하고 싶을 수도 있습니다. 예를 들어, 여러 라우트에서 `{locale}` 파라미터를 사용하는 경우를 가정해보세요.

```
Route::get('/{locale}/posts', function () {
    //
})->name('post.index');
```

<!-- It is cumbersome to always pass the `locale` every time you call the `route` helper. So, you may use the `URL::defaults` method to define a default value for this parameter that will always be applied during the current request. You may wish to call this method from a [route middleware](/docs/9.x/middleware#assigning-middleware-to-routes) so that you have access to the current request: -->
매번 `route` 헬퍼를 호출할 때마다 `locale` 값을 일일이 전달하는 것은 번거로운 일입니다. 이때는 `URL::defaults` 메서드를 이용해 해당 파라미터의 기본값을 설정할 수 있습니다. 이렇게 하면 현재 요청에 한해 항상 이 기본값이 자동으로 적용됩니다. 보통 [route middleware](/docs/9.x/middleware#assigning-middleware-to-routes) 내에서 현재 요청 정보를 활용하여 호출하는 것이 좋습니다.

```
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\URL;

class SetDefaultLocaleForUrls
{
    /**
     * Handle the incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return \Illuminate\Http\Response
     */
    public function handle($request, Closure $next)
    {
        URL::defaults(['locale' => $request->user()->locale]);

        return $next($request);
    }
}
```

<!-- Once the default value for the `locale` parameter has been set, you are no longer required to pass its value when generating URLs via the `route` helper. -->
`locale` 파라미터의 기본값을 설정한 후에는, 이후 `route` 헬퍼를 사용할 때 더 이상 별도로 값을 전달하지 않아도 됩니다.

<a name="url-defaults-middleware-priority"></a>
<!-- #### URL Defaults & Middleware Priority -->
#### URL Defaults & Middleware Priority

<!-- Setting URL default values can interfere with Laravel's handling of implicit model bindings. Therefore, you should [prioritize your middleware](/docs/9.x/middleware#sorting-middleware) that set URL defaults to be executed before Laravel's own `SubstituteBindings` middleware. You can accomplish this by making sure your middleware occurs before the `SubstituteBindings` middleware within the `$middlewarePriority` property of your application's HTTP kernel. -->
URL 기본값을 지정하면 Laravel의 암묵적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어가 Laravel의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [prioritize your middleware](/docs/9.x/middleware#sorting-middleware)를 반드시 조정해야 합니다. 이를 위해서는 애플리케이션 HTTP 커널의 `$middlewarePriority` 프로퍼티에서, 해당 미들웨어가 `SubstituteBindings` 미들웨어보다 앞서 위치하도록 설정하면 됩니다.

<!-- The `$middlewarePriority` property is defined in the base `Illuminate\Foundation\Http\Kernel` class. You may copy its definition from that class and overwrite it in your application's HTTP kernel in order to modify it: -->
`$middlewarePriority` 프로퍼티는 기본적으로 `Illuminate\Foundation\Http\Kernel` 클래스에 정의되어 있습니다. 정의를 복사하여 애플리케이션의 HTTP 커널에 덮어쓰고, 필요한 순서로 수정하면 됩니다.

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
