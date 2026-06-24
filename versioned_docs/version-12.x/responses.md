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
모든 라우트와 컨트롤러는 사용자의 브라우저로 다시 전송할 응답을 반환해야 합니다. Laravel은 응답을 반환하는 여러 가지 방법을 제공합니다. 가장 기본적인 응답은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. 프레임워크는 이 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

```php
Route::get('/', function () {
    return 'Hello World';
});
```

<!-- In addition to returning strings from your routes and controllers, you may also return arrays. The framework will automatically convert the array into a JSON response: -->
라우트와 컨트롤러에서 문자열을 반환하는 것 외에도 배열을 반환할 수도 있습니다. 프레임워크는 배열을 자동으로 JSON 응답으로 변환합니다.

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent collections](/docs/12.x/eloquent-collections)도 반환할 수 있다는 사실을 알고 계셨나요? 이 컬렉션은 자동으로 JSON으로 변환됩니다. 한번 시도해 보세요!

<a name="response-objects"></a>
<!-- #### Response Objects -->
#### Response Objects

<!-- Typically, you won't just be returning simple strings or arrays from your route actions. Instead, you will be returning full `Illuminate\Http\Response` instances or [views](/docs/12.x/views). -->
일반적으로 라우트 액션에서 단순한 문자열이나 배열만 반환하지는 않습니다. 대신 전체 `Illuminate\Http\Response` 인스턴스나 [views](/docs/12.x/views)를 반환하게 됩니다.

<!-- Returning a full `Response` instance allows you to customize the response's HTTP status code and headers. A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, which provides a variety of methods for building HTTP responses: -->
전체 `Response` 인스턴스를 반환하면 응답의 HTTP 상태 코드와 헤더를 사용자 지정할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하며, 이 클래스는 HTTP 응답을 만드는 다양한 메서드를 제공합니다.

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
<!-- #### Eloquent Models and Collections -->
#### Eloquent Models and Collections

<!-- You may also return [Eloquent ORM](/docs/12.x/eloquent) models and collections directly from your routes and controllers. When you do, Laravel will automatically convert the models and collections to JSON responses while respecting the model's [hidden attributes](/docs/12.x/eloquent-serialization#hiding-attributes-from-json): -->
라우트와 컨트롤러에서 [Eloquent ORM](/docs/12.x/eloquent) 모델과 컬렉션을 직접 반환할 수도 있습니다. 그렇게 하면 Laravel은 모델의 [hidden attributes](/docs/12.x/eloquent-serialization#hiding-attributes-from-json)을 존중하면서 모델과 컬렉션을 자동으로 JSON 응답으로 변환합니다.

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
대부분의 응답 메서드는 체이닝할 수 있으므로, 응답 인스턴스를 유연하게 구성할 수 있다는 점을 기억하세요. 예를 들어 `header` 메서드를 사용하여 응답을 사용자에게 다시 보내기 전에 여러 헤더를 추가할 수 있습니다.

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```

<!-- Or, you may use the `withHeaders` method to specify an array of headers to be added to the response: -->
또는 `withHeaders` 메서드를 사용하여 응답에 추가할 헤더 배열을 지정할 수 있습니다.

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```

<!-- You can remove specific headers from an outgoing response using the `withoutHeader` method: -->
`withoutHeader` 메서드를 사용하여 나가는 응답에서 특정 헤더를 제거할 수 있습니다.

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```

<a name="cache-control-middleware"></a>
<!-- #### Cache Control Middleware -->
#### Cache Control Middleware

<!-- Laravel includes a `cache.headers` middleware, which may be used to quickly set the `Cache-Control` header for a group of routes. Directives should be provided using the "snake case" equivalent of the corresponding cache-control directive and should be separated by a semicolon. If `etag` is specified in the list of directives, an MD5 hash of the response content will automatically be set as the ETag identifier: -->
Laravel에는 라우트 그룹에 대해 `Cache-Control` 헤더를 빠르게 설정하는 데 사용할 수 있는 `cache.headers` Middleware가 포함되어 있습니다. 디렉티브는 해당 cache-control 디렉티브에 대응하는 "snake case" 형식으로 제공해야 하며, 세미콜론으로 구분해야 합니다. 디렉티브 목록에 `etag`가 지정되어 있으면 응답 콘텐츠의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다.

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
`cookie` 메서드를 사용하여 나가는 `Illuminate\Http\Response` 인스턴스에 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 그리고 쿠키가 유효하다고 간주될 분 단위 시간을 전달해야 합니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

<!-- The `cookie` method also accepts a few more arguments which are used less frequently. Generally, these arguments have the same purpose and meaning as the arguments that would be given to PHP's native [setcookie](https://secure.php.net/manual/en/function.setcookie.php) method: -->
`cookie` 메서드는 덜 자주 사용되는 몇 가지 추가 인수도 받습니다. 일반적으로 이러한 인수는 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 메서드에 전달되는 인수와 같은 목적과 의미를 가집니다.

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

<!-- If you would like to ensure that a cookie is sent with the outgoing response but you do not yet have an instance of that response, you can use the `Cookie` facade to "queue" cookies for attachment to the response when it is sent. The `queue` method accepts the arguments needed to create a cookie instance. These cookies will be attached to the outgoing response before it is sent to the browser: -->
나가는 응답과 함께 쿠키가 전송되도록 보장하고 싶지만 아직 해당 응답 인스턴스를 가지고 있지 않다면, `Cookie` facade를 사용하여 응답이 전송될 때 쿠키가 첨부되도록 "대기열에 추가"할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 만드는 데 필요한 인수를 받습니다. 이러한 쿠키는 브라우저로 전송되기 전에 나가는 응답에 첨부됩니다.

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
<!-- #### Generating Cookie Instances -->
#### Generating Cookie Instances

<!-- If you would like to generate a `Symfony\Component\HttpFoundation\Cookie` instance that can be attached to a response instance at a later time, you may use the global `cookie` helper. This cookie will not be sent back to the client unless it is attached to a response instance: -->
나중에 응답 인스턴스에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하고 싶다면 전역 `cookie` 헬퍼를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 첨부되지 않는 한 클라이언트로 다시 전송되지 않습니다.

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
<!-- #### Expiring Cookies Early -->
#### Expiring Cookies Early

<!-- You may remove a cookie by expiring it via the `withoutCookie` method of an outgoing response: -->
나가는 응답의 `withoutCookie` 메서드를 통해 쿠키를 만료시켜 제거할 수 있습니다.

```php
return response('Hello World')->withoutCookie('name');
```

<!-- If you do not yet have an instance of the outgoing response, you may use the `Cookie` facade's `expire` method to expire a cookie: -->
아직 나가는 응답 인스턴스를 가지고 있지 않다면 `Cookie` facade의 `expire` 메서드를 사용하여 쿠키를 만료시킬 수 있습니다.

```php
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
<!-- ### Cookies and Encryption -->
### Cookies and Encryption

<!-- By default, thanks to the `Illuminate\Cookie\Middleware\EncryptCookies` middleware, all cookies generated by Laravel are encrypted and signed so that they can't be modified or read by the client. If you would like to disable encryption for a subset of cookies generated by your application, you may use the `encryptCookies` method in your application's `bootstrap/app.php` file: -->
기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` Middleware 덕분에 Laravel에서 생성하는 모든 쿠키는 암호화되고 서명됩니다. 따라서 클라이언트가 쿠키를 수정하거나 읽을 수 없습니다. 애플리케이션에서 생성하는 일부 쿠키에 대해 암호화를 비활성화하고 싶다면 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```

> [!NOTE]
> 일반적으로 쿠키 암호화는 절대 비활성화해서는 안 됩니다. 쿠키가 클라이언트 측 데이터 노출과 변조 위험에 놓이기 때문입니다.

<a name="redirects"></a>
<!-- ## Redirects -->
## Redirects

<!-- Redirect responses are instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL. There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the global `redirect` helper: -->
리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지입니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

<!-- Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/12.x/session), make sure the route calling the `back` function is using the `web` middleware group: -->
제출된 폼이 유효하지 않은 경우처럼, 사용자를 이전 위치로 리다이렉트하고 싶을 때가 있습니다. 이 경우 전역 `back` 헬퍼 함수를 사용하면 됩니다. 이 기능은 [session](/docs/12.x/session)을 사용하므로, `back` 함수를 호출하는 라우트가 `web` Middleware 그룹을 사용하고 있는지 확인하세요.

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
인수 없이 `redirect` 헬퍼를 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되며, 이를 통해 `Redirector` 인스턴스의 모든 메서드를 호출할 수 있습니다. 예를 들어 이름이 지정된 라우트로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용할 수 있습니다.

```php
return redirect()->route('login');
```

<!-- If your route has parameters, you may pass them as the second argument to the `route` method: -->
라우트에 매개변수가 있다면 `route` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
<!-- #### Populating Parameters via Eloquent Models -->
#### Populating Parameters via Eloquent Models

<!-- If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically: -->
Eloquent 모델에서 채워지는 "ID" 매개변수가 있는 라우트로 리다이렉트하는 경우, 모델 자체를 전달할 수 있습니다. ID는 자동으로 추출됩니다.

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

<!-- If you would like to customize the value that is placed in the route parameter, you can specify the column in the route parameter definition (`/profile/{id:slug}`) or you can override the `getRouteKey` method on your Eloquent model: -->
라우트 매개변수에 들어갈 값을 사용자 지정하고 싶다면 라우트 매개변수 정의에서 컬럼을 지정하거나(`/profile/{id:slug}`), Eloquent 모델에서 `getRouteKey` 메서드를 재정의할 수 있습니다.

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

<!-- You may also generate redirects to [controller actions](/docs/12.x/controllers). To do so, pass the controller and action name to the `action` method: -->
[controller actions](/docs/12.x/controllers)으로 리다이렉트를 생성할 수도 있습니다. 이를 위해 컨트롤러와 액션 이름을 `action` 메서드에 전달하세요.

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

<!-- If your controller route requires parameters, you may pass them as the second argument to the `action` method: -->
컨트롤러 라우트에 매개변수가 필요하다면 `action` 메서드의 두 번째 인수로 전달할 수 있습니다.

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
<!-- ### Redirecting to External Domains -->
### Redirecting to External Domains

<!-- Sometimes you may need to redirect to a domain outside of your application. You may do so by calling the `away` method, which creates a `RedirectResponse` without any additional URL encoding, validation, or verification: -->
때로는 애플리케이션 외부의 도메인으로 리다이렉트해야 할 수 있습니다. 이 경우 `away` 메서드를 호출하면 됩니다. 이 메서드는 추가 URL 인코딩, 유효성 검증, 검증 절차 없이 `RedirectResponse`를 생성합니다.

```php
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
<!-- ### Redirecting With Flashed Session Data -->
### Redirecting With Flashed Session Data

<!-- Redirecting to a new URL and [flashing data to the session](/docs/12.x/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain: -->
새 URL로 리다이렉트하면서 [flashing data to the session](/docs/12.x/session#flash-data)하는 작업은 보통 동시에 이루어집니다. 일반적으로 액션을 성공적으로 수행한 뒤 성공 메시지를 세션에 플래시할 때 사용합니다. 편의를 위해 하나의 유연한 메서드 체인에서 `RedirectResponse` 인스턴스를 만들고 데이터를 세션에 플래시할 수 있습니다.

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

<!-- After the user is redirected, you may display the flashed message from the [session](/docs/12.x/session). For example, using [Blade syntax](/docs/12.x/blade): -->
사용자가 리다이렉트된 뒤에는 [session](/docs/12.x/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어 [Blade syntax](/docs/12.x/blade)을 사용하면 다음과 같습니다.

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

<!-- You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. This is typically done if the user has encountered a validation error. Once the input has been flashed to the session, you may easily [retrieve it](/docs/12.x/requests#retrieving-old-input) during the next request to repopulate the form: -->
`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면 사용자를 새 위치로 리다이렉트하기 전에 현재 요청의 입력 데이터를 세션에 플래시할 수 있습니다. 이는 일반적으로 사용자가 유효성 검증 오류를 만났을 때 수행됩니다. 입력값이 세션에 플래시되면 다음 요청에서 폼을 다시 채우기 위해 이를 쉽게 [retrieve it](/docs/12.x/requests#retrieving-old-input).

```php
return back()->withInput();
```

<a name="other-response-types"></a>
<!-- ## Other Response Types -->
## Other Response Types

<!-- The `response` helper may be used to generate other types of response instances. When the `response` helper is called without arguments, an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/12.x/contracts) is returned. This contract provides several helpful methods for generating responses. -->
`response` 헬퍼는 다른 종류의 응답 인스턴스를 생성하는 데 사용할 수 있습니다. `response` 헬퍼를 인수 없이 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/12.x/contracts)의 구현체가 반환됩니다. 이 계약은 응답을 생성하는 데 유용한 여러 메서드를 제공합니다.

<a name="view-responses"></a>
<!-- ### View Responses -->
### View Responses

<!-- If you need control over the response's status and headers but also need to return a [view](/docs/12.x/views) as the response's content, you should use the `view` method: -->
응답의 상태 코드와 헤더를 제어해야 하면서도 응답의 콘텐츠로 [view](/docs/12.x/views)를 반환해야 한다면 `view` 메서드를 사용해야 합니다.

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```

<!-- Of course, if you do not need to pass a custom HTTP status code or custom headers, you may use the global `view` helper function. -->
물론 사용자 지정 HTTP 상태 코드나 사용자 지정 헤더를 전달할 필요가 없다면 전역 `view` 헬퍼 함수를 사용할 수 있습니다.

<a name="json-responses"></a>
<!-- ### JSON Responses -->
### JSON Responses

<!-- The `json` method will automatically set the `Content-Type` header to `application/json`, as well as convert the given array to JSON using the `json_encode` PHP function: -->
`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 설정하고, 주어진 배열을 PHP의 `json_encode` 함수를 사용하여 JSON으로 변환합니다.

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

<!-- If you would like to create a JSONP response, you may use the `json` method in combination with the `withCallback` method: -->
JSONP 응답을 만들고 싶다면 `json` 메서드와 `withCallback` 메서드를 함께 사용할 수 있습니다.

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
<!-- ### File Downloads -->
### File Downloads

<!-- The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method: -->
`download` 메서드는 지정된 경로의 파일을 사용자의 브라우저가 다운로드하도록 강제하는 응답을 생성하는 데 사용할 수 있습니다. `download` 메서드는 두 번째 인수로 파일명을 받으며, 이 파일명은 파일을 다운로드하는 사용자에게 표시될 파일명을 결정합니다. 마지막으로 세 번째 인수로 HTTP 헤더 배열을 전달할 수 있습니다.

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드되는 파일이 ASCII 파일명을 가져야 한다고 요구합니다.

<a name="file-responses"></a>
<!-- ### File Responses -->
### File Responses

<!-- The `file` method may be used to display a file, such as an image or PDF, directly in the user's browser instead of initiating a download. This method accepts the absolute path to the file as its first argument and an array of headers as its second argument: -->
`file` 메서드는 다운로드를 시작하는 대신 이미지나 PDF 같은 파일을 사용자의 브라우저에 직접 표시하는 데 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 파일의 절대 경로를 받고, 두 번째 인수로 헤더 배열을 받습니다.

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="streamed-responses"></a>
<!-- ## Streamed Responses -->
## Streamed Responses

<!-- By streaming data to the client as it is generated, you can significantly reduce memory usage and improve performance, especially for very large responses. Streamed responses allow the client to begin processing data before the server has finished sending it: -->
데이터가 생성되는 즉시 클라이언트로 스트리밍하면 메모리 사용량을 크게 줄이고 성능을 향상시킬 수 있으며, 특히 매우 큰 응답에서 효과적입니다. 스트리밍 응답을 사용하면 서버가 데이터를 모두 보내기 전에 클라이언트가 데이터 처리를 시작할 수 있습니다.

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
편의를 위해 `stream` 메서드에 제공한 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel은 generator가 반환하는 문자열 사이에서 출력 버퍼를 자동으로 flush하고 Nginx 출력 버퍼링도 비활성화합니다.

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

<!-- Streamed responses may be consumed using Laravel's `stream` npm package, which provides a convenient API for interacting with Laravel response and event streams. To get started, install the `@laravel/stream-react`, `@laravel/stream-vue`, or `@laravel/stream-svelte` package: -->
스트림 응답은 Laravel 응답 및 이벤트 스트림과 상호작용하기 위한 편리한 API를 제공하는 Laravel의 `stream` npm 패키지를 사용하여 소비할 수 있습니다. 시작하려면 `@laravel/stream-react`, `@laravel/stream-vue`, 또는 `@laravel/stream-svelte` 패키지를 설치합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```

<!-- Then, `useStream` may be used to consume the event stream. After providing your stream URL, the hook will automatically update the `data` with the concatenated response as content is returned from your Laravel application: -->
그런 다음 `useStream`을 사용하여 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 제공하면, Laravel 애플리케이션에서 콘텐츠가 반환될 때 훅이 이어 붙인 응답으로 `data`를 자동 업데이트합니다.

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

<!-- When sending data back to the stream via `send`, the active connection to the stream is canceled before sending the new data. All requests are sent as JSON `POST` requests. -->
`send`를 통해 데이터를 스트림으로 다시 보낼 때는 새 데이터를 보내기 전에 스트림에 대한 활성 연결이 취소됩니다. 모든 요청은 JSON `POST` 요청으로 전송됩니다.

> [!WARNING]
> `useStream` 훅은 애플리케이션에 `POST` 요청을 보내므로, 유효한 CSRF 토큰이 필요합니다. CSRF 토큰을 제공하는 가장 쉬운 방법은 [include it via a meta tag in your application layout's head](/docs/12.x/csrf#csrf-x-csrf-token)입니다.

<!-- The second argument given to `useStream` is an options object that you may use to customize the stream consumption behavior. The default values for this object are shown below: -->
`useStream`에 전달되는 두 번째 인수는 스트림 소비 동작을 사용자화하는 데 사용할 수 있는 옵션 객체입니다. 이 객체의 기본값은 아래와 같습니다.

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

<!-- `onResponse` is triggered after a successful initial response from the stream and the raw [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response) is passed to the callback. `onData` is called as each chunk is received - the current chunk is passed to the callback. `onFinish` is called when a stream has finished and when an error is thrown during the fetch / read cycle. -->
`onResponse`는 스트림에서 성공적인 초기 응답을 받은 뒤 트리거되며, 원본 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response)가 콜백에 전달됩니다. `onData`는 각 청크가 수신될 때마다 호출되며, 현재 청크가 콜백에 전달됩니다. `onFinish`는 스트림이 완료되었을 때와 fetch / read 주기 중 오류가 발생했을 때 호출됩니다.

<!-- By default, a request is not made to the stream on initialization. You may pass an initial payload to the stream by using the `initialInput` option: -->
기본적으로 초기화 시점에는 스트림에 요청을 보내지 않습니다. `initialInput` 옵션을 사용하여 스트림에 초기 페이로드를 전달할 수 있습니다.

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

<!-- To cancel a stream manually, you may use the `cancel` method returned from the hook: -->
스트림을 수동으로 취소하려면 훅에서 반환되는 `cancel` 메서드를 사용할 수 있습니다.

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

<!-- Each time the `useStream` hook is used, a random `id` is generated to identify the stream. This is sent back to the server with each request in the `X-STREAM-ID` header. When consuming the same stream from multiple components, you can read and write to the stream by providing your own `id`: -->
`useStream` 훅을 사용할 때마다 스트림을 식별하기 위한 임의의 `id`가 생성됩니다. 이 값은 각 요청마다 `X-STREAM-ID` 헤더에 담겨 서버로 다시 전송됩니다. 여러 컴포넌트에서 같은 스트림을 소비할 때는 직접 `id`를 제공하여 스트림을 읽고 쓸 수 있습니다.

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
<!-- ### Streamed JSON Responses -->
### Streamed JSON Responses

<!-- If you need to stream JSON data incrementally, you may utilize the `streamJson` method. This method is especially useful for large datasets that need to be sent progressively to the browser in a format that can be easily parsed by JavaScript: -->
JSON 데이터를 점진적으로 스트리밍해야 하는 경우 `streamJson` 메서드를 활용할 수 있습니다. 이 메서드는 JavaScript에서 쉽게 파싱할 수 있는 형식으로 대용량 데이터셋을 브라우저에 점진적으로 보내야 할 때 특히 유용합니다.

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```

<!-- The `useJsonStream` hook is identical to the [useStream hook](#consuming-streamed-responses) except that it will attempt to parse the data as JSON once it has finished streaming: -->
`useJsonStream` 훅은 스트리밍이 완료된 뒤 데이터를 JSON으로 파싱하려고 시도한다는 점을 제외하면 [useStream hook](#consuming-streamed-responses)과 동일합니다.

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
<!-- ### Event Streams (SSE) -->
### Event Streams (SSE)

<!-- The `eventStream` method may be used to return a server-sent events (SSE) streamed response using the `text/event-stream` content type. The `eventStream` method accepts a closure which should [yield](https://www.php.net/manual/en/language.generators.overview.php) responses to the stream as the responses become available: -->
`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하여 서버 전송 이벤트(server-sent events, SSE) 스트리밍 응답을 반환하는 데 사용할 수 있습니다. `eventStream` 메서드는 클로저를 인수로 받으며, 이 클로저는 응답이 준비되는 대로 스트림에 응답을 [yield](https://www.php.net/manual/en/language.generators.overview.php)해야 합니다.

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
이벤트 이름을 사용자 지정하려면 `StreamedEvent` 클래스의 인스턴스를 yield 하면 됩니다.

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

<!-- Event streams may be consumed using Laravel's `stream` npm package, which provides a convenient API for interacting with Laravel event streams. To get started, install the `@laravel/stream-react`, `@laravel/stream-vue`, or `@laravel/stream-svelte` package: -->
이벤트 스트림은 Laravel의 `stream` npm 패키지를 사용하여 사용할 수 있습니다. 이 패키지는 Laravel 이벤트 스트림과 상호 작용하기 위한 편리한 API를 제공합니다. 시작하려면 `@laravel/stream-react`, `@laravel/stream-vue`, 또는 `@laravel/stream-svelte` 패키지를 설치합니다.

```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```

<!-- Then, `useEventStream` may be used to consume the event stream. After providing your stream URL, the hook will automatically update the `message` with the concatenated response as messages are returned from your Laravel application: -->
그런 다음 `useEventStream`을 사용하여 이벤트 스트림을 사용할 수 있습니다. 스트림 URL을 제공하면, Laravel 애플리케이션에서 메시지가 반환될 때마다 hook이 연결된 응답으로 `message`를 자동으로 업데이트합니다.

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

<!-- The second argument given to `useEventStream` is an options object that you may use to customize the stream consumption behavior. The default values for this object are shown below: -->
`useEventStream`에 전달되는 두 번째 인수는 스트림 사용 동작을 사용자 지정하는 데 사용할 수 있는 옵션 객체입니다. 이 객체의 기본값은 아래와 같습니다.

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

<!-- Event streams may also be manually consumed via an [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) object by your application's frontend. The `eventStream` method will automatically send a `</stream>` update to the event stream when the stream is complete: -->
이벤트 스트림은 애플리케이션의 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 통해 직접 사용할 수도 있습니다. `eventStream` 메서드는 스트림이 완료되면 이벤트 스트림에 `</stream>` 업데이트를 자동으로 보냅니다.

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
이벤트 스트림으로 전송되는 마지막 이벤트를 사용자 지정하려면 `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 제공하면 됩니다.

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```

<a name="streamed-downloads"></a>
<!-- ### Streamed Downloads -->
### Streamed Downloads

<!-- Sometimes you may wish to turn the string response of a given operation into a downloadable response without having to write the contents of the operation to disk. You may use the `streamDownload` method in this scenario. This method accepts a callback, filename, and an optional array of headers as its arguments: -->
때로는 어떤 작업의 문자열 응답을 디스크에 기록하지 않고도 다운로드 가능한 응답으로 바꾸고 싶을 수 있습니다. 이런 경우 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고 선택적인 헤더 배열을 인수로 받습니다.

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

<!-- If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on the `Response` facade. Typically, you should call this method from the `boot` method of one of your application's [service providers](/docs/12.x/providers), such as the `App\Providers\AppServiceProvider` service provider: -->
여러 라우트와 컨트롤러에서 재사용할 수 있는 사용자 지정 응답을 정의하고 싶다면 `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 [service providers](/docs/12.x/providers) 중 하나의 `boot` 메서드에서 호출해야 합니다. 예를 들어 `App\Providers\AppServiceProvider` 서비스 프로바이더에서 호출할 수 있습니다.

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
`macro` 함수는 첫 번째 인수로 이름을, 두 번째 인수로 클로저를 받습니다. 매크로의 클로저는 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름을 호출할 때 실행됩니다.

```php
return response()->caps('foo');
```
