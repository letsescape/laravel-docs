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
Laravel은 애플리케이션에서 URL을 생성할 수 있도록 도와주는 다양한 헬퍼를 제공합니다. 이 헬퍼들은 주로 템플릿에서 링크를 만들거나, API 응답에 링크를 포함시키거나, 애플리케이션의 다른 위치로 리디렉션 응답을 보낼 때 유용하게 사용할 수 있습니다.

<a name="the-basics"></a>
<!-- ## The Basics -->
## The Basics

<a name="generating-urls"></a>
<!-- ### Generating URLs -->
### Generating URLs

<!-- The `url` helper may be used to generate arbitrary URLs for your application. The generated URL will automatically use the scheme (HTTP or HTTPS) and host from the current request being handled by the application: -->
`url` 헬퍼를 사용하면 애플리케이션에서 임의의 URL을 쉽게 생성할 수 있습니다. 생성되는 URL은 현재 요청의 스킴(HTTP 또는 HTTPS)과 호스트 정보를 자동으로 사용합니다.

```
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

<!-- To generate a URL with query string parameters, you may use the `query` method: -->
쿼리 문자열 파라미터와 함께 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다.

```
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

<!-- Providing query string parameters that already exist in the path will overwrite their existing value: -->
쿼리 문자열 파라미터 중 이미 경로에 존재하는 값이 있다면, 전달한 값으로 기존 파라미터가 덮어씌워집니다.

```
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

<!-- Arrays of values may also be passed as query parameters. These values will be properly keyed and encoded in the generated URL: -->
쿼리 파라미터로 값의 배열도 전달할 수 있습니다. 배열로 전달된 값은 키가 제대로 지정되고 인코딩되어 URL에 포함됩니다.

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
`url` 헬퍼에 인수를 전달하지 않으면 `Illuminate\Routing\UrlGenerator` 인스턴스를 반환하므로, 이를 통해 현재 URL에 대한 다양한 정보를 얻을 수 있습니다.

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
이러한 메서드들은 [facade](/docs/11.x/facades)인 `URL`을 통해서도 접근할 수 있습니다.

```
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="urls-for-named-routes"></a>
<!-- ## URLs for Named Routes -->
## URLs for Named Routes

<!-- The `route` helper may be used to generate URLs to [named routes](/docs/11.x/routing#named-routes). Named routes allow you to generate URLs without being coupled to the actual URL defined on the route. Therefore, if the route's URL changes, no changes need to be made to your calls to the `route` function. For example, imagine your application contains a route defined like the following: -->
`route` 헬퍼를 사용하면 [named routes](/docs/11.x/routing#named-routes)의 URL을 만들 수 있습니다. 이름이 지정된 라우트는 실제 URL에 의존하지 않고도 URL을 생성할 수 있게 해주므로, 라우트의 URL이 변경되더라도 `route` 함수 호출부를 수정할 필요가 없습니다. 예를 들어, 아래와 같이 라우트를 정의했다고 가정해보겠습니다.

```
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

<!-- To generate a URL to this route, you may use the `route` helper like so: -->
이 라우트에 대한 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용할 수 있습니다.

```
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

<!-- Of course, the `route` helper may also be used to generate URLs for routes with multiple parameters: -->
물론, `route` 헬퍼는 여러 파라미터가 필요한 라우트의 URL도 생성할 수 있습니다.

```
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

<!-- Any additional array elements that do not correspond to the route's definition parameters will be added to the URL's query string: -->
라우트 정의에 없는 추가 배열 요소들은 URL의 쿼리 문자열로 포함됩니다.

```
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
<!-- #### Eloquent Models -->
#### Eloquent Models

<!-- You will often be generating URLs using the route key (typically the primary key) of [Eloquent models](/docs/11.x/eloquent). For this reason, you may pass Eloquent models as parameter values. The `route` helper will automatically extract the model's route key: -->
주로 [Eloquent models](/docs/11.x/eloquent)의 라우트 키(일반적으로 기본 키)를 사용해 URL을 생성하는 경우가 많습니다. 이러한 경우, Eloquent 모델 인스턴스를 파라미터로 그대로 전달할 수 있습니다. 그러면 `route` 헬퍼가 모델의 라우트 키 값을 자동으로 추출해 사용합니다.

```
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
<!-- ### Signed URLs -->
### Signed URLs

<!-- Laravel allows you to easily create "signed" URLs to named routes. These URLs have a "signature" hash appended to the query string which allows Laravel to verify that the URL has not been modified since it was created. Signed URLs are especially useful for routes that are publicly accessible yet need a layer of protection against URL manipulation. -->
Laravel에서는 라우트 이름에 대해 "서명된" URL을 손쉽게 생성할 수 있습니다. 이 URL에는 시그니처(해시값)가 쿼리 문자열에 추가되어, 생성된 이후로 내용이 변경되지 않았는지 Laravel이 검증할 수 있습니다. 서명된 URL은 공개적으로 접근 가능하지만 URL 변조로부터 보호가 필요한 라우트에 특히 유용합니다.

<!-- For example, you might use signed URLs to implement a public "unsubscribe" link that is emailed to your customers. To create a signed URL to a named route, use the `signedRoute` method of the `URL` facade: -->
예를 들어, 고객에게 이메일로 발송하는 "구독 해지"와 같은 공개 링크를 구현할 때 서명된 URL을 활용할 수 있습니다. 라우트 이름에 대한 서명된 URL을 만들려면 `URL` 파사드의 `signedRoute` 메서드를 사용합니다.

```
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

<!-- You may exclude the domain from the signed URL hash by providing the `absolute` argument to the `signedRoute` method: -->
서명된 URL 해시에 도메인을 포함하지 않으려면, `signedRoute` 메서드에 `absolute` 인자를 제공하면 됩니다.

```
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

<!-- If you would like to generate a temporary signed route URL that expires after a specified amount of time, you may use the `temporarySignedRoute` method. When Laravel validates a temporary signed route URL, it will ensure that the expiration timestamp that is encoded into the signed URL has not elapsed: -->
지정한 시간 이후 만료되는 임시 서명 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용할 수 있습니다. Laravel은 임시 서명 URL을 검증할 때 URL에 인코딩된 만료 타임스탬프가 아직 유효한지도 확인합니다.

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
들어오는 요청이 올바른 서명을 가지고 있는지 확인하려면, `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출하면 됩니다.

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
때때로, 프론트엔드에서 클라이언트 측 페이지네이션처럼 서명 URL에 데이터를 추가로 붙여야 할 수도 있습니다. 이럴 경우, `hasValidSignatureWhileIgnoring` 메서드를 사용해 서명 검증 시 무시할 쿼리 파라미터를 지정할 수 있습니다. 단, 무시한 파라미터는 누구나 요청에서 변경할 수 있음을 꼭 명심해야 합니다.

```
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

<!-- Instead of validating signed URLs using the incoming request instance, you may assign the `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [middleware](/docs/11.x/middleware) to the route. If the incoming request does not have a valid signature, the middleware will automatically return a `403` HTTP response: -->
들어오는 요청 인스턴스로 직접 서명된 URL을 검증하는 대신, 해당 라우트에 `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [middleware](/docs/11.x/middleware)를 지정할 수 있습니다. 이 경우, 요청이 올바른 서명을 가지고 있지 않으면 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다.

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

<!-- If your signed URLs do not include the domain in the URL hash, you should provide the `relative` argument to the middleware: -->
서명된 URL이 해시에서 도메인을 제외한 경우, 미들웨어에 `relative` 인자를 추가해야 합니다.

```
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
<!-- #### Responding to Invalid Signed Routes -->
#### Responding to Invalid Signed Routes

<!-- When someone visits a signed URL that has expired, they will receive a generic error page for the `403` HTTP status code. However, you can customize this behavior by defining a custom "render" closure for the `InvalidSignatureException` exception in your application's `bootstrap/app.php` file: -->
서명된 URL에 만료 기간이 지난 후 접근하면 `403` HTTP 코드에 대한 일반 오류 페이지를 보게 됩니다. 이러한 동작을 커스터마이즈하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대해 직접 "render" 클로저를 정의할 수 있습니다.

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
`action` 함수는 지정된 컨트롤러 액션에 대한 URL을 생성합니다.

```
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

<!-- If the controller method accepts route parameters, you may pass an associative array of route parameters as the second argument to the function: -->
컨트롤러 메서드가 라우트 파라미터를 받는다면, 해당 파라미터들로 구성된 연관 배열을 두 번째 인자로 전달할 수 있습니다.

```
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="default-values"></a>
<!-- ## Default Values -->
## Default Values

<!-- For some applications, you may wish to specify request-wide default values for certain URL parameters. For example, imagine many of your routes define a `{locale}` parameter: -->
일부 애플리케이션에서는 특정 URL 파라미터에 대해 전체 요청에 적용되는 기본값을 지정하고 싶을 수 있습니다. 예를 들어, 많은 라우트에서 `{locale}` 파라미터를 정의하는 구조라면 아래와 같습니다.

```
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

<!-- It is cumbersome to always pass the `locale` every time you call the `route` helper. So, you may use the `URL::defaults` method to define a default value for this parameter that will always be applied during the current request. You may wish to call this method from a [route middleware](/docs/11.x/middleware#assigning-middleware-to-routes) so that you have access to the current request: -->
매번 `route` 헬퍼를 쓸 때마다 `locale` 값을 일일이 전달하는 것은 번거로울 수 있습니다. 이때, `URL::defaults` 메서드를 사용해 파라미터별 기본값을 설정해두면, 현재 요청 처리 내내 자동으로 적용됩니다. 이 메서드는 [route middleware](/docs/11.x/middleware#assigning-middleware-to-routes)에서 호출하는 것이 일반적이며, 이렇게 하면 현재 요청정보에도 접근할 수 있습니다.

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
`locale` 파라미터의 기본값이 설정되면, 이제부터 URL을 생성할 때 `route` 헬퍼에 별도로 값을 전달하지 않아도 됩니다.

<a name="url-defaults-middleware-priority"></a>
<!-- #### URL Defaults and Middleware Priority -->
#### URL Defaults and Middleware Priority

<!-- Setting URL default values can interfere with Laravel's handling of implicit model bindings. Therefore, you should [prioritize your middleware](/docs/11.x/middleware#sorting-middleware) that set URL defaults to be executed before Laravel's own `SubstituteBindings` middleware. You can accomplish this using the `priority` middleware method in your application's `bootstrap/app.php` file: -->
URL 기본값 설정은 Laravel의 암시적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어가 Laravel 기본 미들웨어인 `SubstituteBindings`보다 먼저 실행되도록 [prioritize your middleware](/docs/11.x/middleware#sorting-middleware)를 조정해야 합니다. 이를 위해 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 사용하여 순서를 지정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```
