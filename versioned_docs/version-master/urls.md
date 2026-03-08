# URL 생성 (URL Generation)

- [소개](#introduction)
- [기본 사용법](#the-basics)
    - [URL 생성하기](#generating-urls)
    - [현재 URL 가져오기](#accessing-the-current-url)
- [네임드 라우트의 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 액션의 URL](#urls-for-controller-actions)
- [플루언트 URI 객체](#fluent-uri-objects)
- [기본값 설정](#default-values)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 애플리케이션에서 URL을 생성하는 데 도움을 주는 여러 보조 함수를 제공합니다. 이러한 보조 함수는 주로 템플릿이나 API 응답에서 링크를 만들거나, 애플리케이션의 다른 부분으로 리다이렉트 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본 사용법 (The Basics)

<a name="generating-urls"></a>
### URL 생성하기 (Generating URLs)

`url` 보조 함수를 사용하면 애플리케이션용 임의의 URL을 생성할 수 있습니다. 생성된 URL은 애플리케이션이 처리 중인 현재 요청의 스킴(HTTP 또는 HTTPS)과 호스트를 자동으로 사용합니다:

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1
```

쿼리 스트링 파라미터가 포함된 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel
```

경로에 이미 존재하는 쿼리 파라미터에 값을 제공하면 해당 값을 덮어씁니다:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest
```

쿼리 파라미터로 값의 배열을 전달할 수도 있습니다. 이러한 값들은 생성된 URL에서 올바르게 키가 지정되고 인코딩됩니다:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body
```

<a name="accessing-the-current-url"></a>
### 현재 URL 가져오기 (Accessing the Current URL)

`url` 보조 함수에 경로를 제공하지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 정보를 확인할 수 있습니다:

```php
// 쿼리 스트링을 제외한 현재 URL 가져오기...
echo url()->current();

// 쿼리 스트링을 포함한 현재 URL 가져오기...
echo url()->full();
```

이러한 메서드는 [URL 파사드](/docs/master/facades)를 통해서도 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();
```

<a name="accessing-the-previous-url"></a>
#### 이전 URL 가져오기

사용자가 직전에 방문한 URL을 알아야 할 때가 있습니다. `url` 보조 함수의 `previous` 및 `previousPath` 메서드를 통해 이전 URL을 가져올 수 있습니다:

```php
// 이전 요청의 전체 URL 가져오기...
echo url()->previous();

// 이전 요청의 경로만 가져오기...
echo url()->previousPath();
```

또는, [세션](/docs/master/session)을 이용해 [플루언트 URI](#fluent-uri-objects) 인스턴스로 이전 URL에 접근할 수도 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/users', function (Request $request) {
    $previousUri = $request->session()->previousUri();

    // ...
});
```

또한, 세션을 통해 직전에 방문한 URL의 라우트 이름을 가져올 수도 있습니다:

```php
$previousRoute = $request->session()->previousRoute();
```

<a name="urls-for-named-routes"></a>
## 네임드 라우트의 URL (URLs for Named Routes)

`route` 보조 함수는 [네임드 라우트](/docs/master/routing#named-routes)의 URL을 생성하는 데 사용합니다. 네임드 라우트를 사용하면 실제 라우트에 정의된 URL에 의존하지 않고 URL을 생성할 수 있습니다. 따라서, 해당 라우트의 URL이 변경되어도 `route` 함수 호출 부분은 수정할 필요가 없습니다. 예를 들어, 아래와 같은 라우트가 있다고 가정합니다:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');
```

위 라우트의 URL을 생성하려면, 다음과 같이 `route` 보조 함수를 사용합니다:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1
```

물론, `route` 보조 함수는 여러 파라미터가 있는 라우트의 URL도 생성할 수 있습니다:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3
```

라우트 정의 파라미터에 해당하지 않는 배열 요소들은 URL의 쿼리 스트링으로 추가됩니다:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket
```

<a name="eloquent-models"></a>
#### Eloquent 모델 사용

[ Eloquent 모델 ](/docs/master/eloquent)의 라우트 키(일반적으로 기본 키)를 사용하여 URL을 생성하는 경우가 많습니다. 따라서, 파라미터로 Eloquent 모델 인스턴스를 직접 전달할 수 있습니다. 이때 `route` 보조 함수는 모델에서 라우트 키를 자동으로 추출합니다:

```php
echo route('post.show', ['post' => $post]);
```

<a name="signed-urls"></a>
### 서명된 URL (Signed URLs)

Laravel에서는 네임드 라우트에 대해 손쉽게 "서명된" URL을 생성할 수 있습니다. 이러한 URL에는 서명 해시가 쿼리 문자열에 추가되어, 생성 이후 URL이 수정되지 않았는지 Laravel이 검증할 수 있도록 해줍니다. 서명된 URL은 외부에 공개되어 있으면서도 URL 조작을 방지할 보호 계층이 필요한 라우트에 특히 유용합니다.

예를 들어, 공개 구독 해지(unsubscribe) 링크를 이메일로 발송할 때 서명된 URL을 사용할 수 있습니다. 네임드 라우트의 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);
```

서명된 URL 해시에 도메인을 제외하려면 `signedRoute` 메서드의 `absolute` 인수를 사용하세요:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);
```

정해진 시간 이후 만료되는 임시 서명 URL을 생성하려면 `temporarySignedRoute` 메서드를 사용합니다. Laravel이 임시 서명 URL을 검증할 때는, 해당 서명된 URL에 인코딩된 만료 타임스탬프가 지나지 않았는지 확인합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->plus(minutes: 30), ['user' => 1]
);
```

<a name="validating-signed-route-requests"></a>
#### 서명된 라우트 요청 검증

들어오는 요청이 유효한 서명을 가지고 있는지 확인하려면, 전달받은 `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출하세요:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');
```

애플리케이션의 프론트엔드에서 페이지네이션 등 서명된 URL에 데이터를 추가해야 할 필요가 있다면, 서명 URL 검증 시 무시할 쿼리 파라미터를 `hasValidSignatureWhileIgnoring` 메서드에 지정할 수 있습니다. 주의: 무시하는 파라미터는 누구나 해당 요청에서 변경할 수 있게 됩니다.

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}
```

요청 인스턴스에서 서명된 URL을 검증하는 대신, 해당 라우트에 `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [미들웨어](/docs/master/middleware)를 지정할 수도 있습니다. 요청이 유효한 서명을 포함하지 않을 경우, 미들웨어가 자동으로 `403` HTTP 응답을 반환합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');
```

서명된 URL 해시에 도메인이 포함되어 있지 않으면, 미들웨어에 `relative` 인수를 제공해야 합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');
```

<a name="responding-to-invalid-signed-routes"></a>
#### 유효하지 않은 서명 라우트 응답 커스터마이징

누군가 만료된 서명 URL에 접근하면, 기본적으로 `403` HTTP 상태 코드의 일반 오류 페이지가 표시됩니다. 그러나, 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대한 커스텀 "render" 클로저를 정의하여 이 동작을 변경할 수 있습니다:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})
```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션의 URL (URLs for Controller Actions)

`action` 함수는 지정한 컨트롤러 액션에 대한 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);
```

컨트롤러 메서드가 라우트 파라미터를 받는 경우, 두 번째 인자로 연관 배열 형태의 라우트 파라미터를 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);
```

<a name="fluent-uri-objects"></a>
## 플루언트 URI 객체 (Fluent URI Objects)

Laravel의 `Uri` 클래스는 객체 지향적으로 URI를 만들고 다룰 수 있는 편리하고 플루언트한 인터페이스를 제공합니다. 이 클래스는 기본적으로 League URI 패키지의 기능을 감싸면서, Laravel 라우팅 시스템과 원활하게 통합됩니다.

정적 메서드를 사용해 손쉽게 `Uri` 인스턴스를 만들 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// 주어진 문자열로부터 URI 인스턴스 생성...
$uri = Uri::of('https://example.com/path');

// 경로, 네임드 라우트, 컨트롤러 액션 등에 대한 URI 인스턴스 생성...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// 현재 요청의 URL로부터 URI 인스턴스 생성...
$uri = $request->uri();

// 이전 요청의 URL로부터 URI 인스턴스 생성...
$uri = $request->session()->previousUri();
```

URI 인스턴스를 받은 후에는 아래와 같이 플루언트하게 수정할 수 있습니다:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');
```

플루언트 URI 객체 다루기에 대한 더 자세한 내용은 [URI 문서](/docs/master/helpers#uri)를 참고하세요.

<a name="default-values"></a>
## 기본값 설정 (Default Values)

특정 URL 파라미터에 대해 요청 전체에 적용되는 기본값을 지정하고 싶을 때가 있습니다. 예를 들어, 많은 라우트에서 `{locale}` 파라미터를 사용하는 경우를 생각해봅니다:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');
```

`route` 보조 함수를 사용할 때마다 매번 `locale`을 전달하는 것은 번거롭기 때문에, `URL::defaults` 메서드를 사용하여 해당 파라미터의 기본값을 현재 요청에 항상 적용하도록 할 수 있습니다. 이 메서드는 [라우트 미들웨어](/docs/master/middleware#assigning-middleware-to-routes)에서 호출하면 현재 요청에 접근할 수 있습니다:

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

`locale` 파라미터에 대한 기본값을 지정하면, `route` 보조 함수로 URL을 생성할 때마다 값을 별도로 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 우선순위 (URL Defaults and Middleware Priority)

URL 기본값을 설정하는 것은 Laravel의 암묵적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 미들웨어는 Laravel 자체의 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 [미들웨어 우선순위](/docs/master/middleware#sorting-middleware)를 지정해야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 사용하여 할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})
```
