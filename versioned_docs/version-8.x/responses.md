<!-- # HTTP Responses -->
# HTTP Responses

- [Creating Responses](#creating-responses)
    - [Attaching Headers To Responses](#attaching-headers-to-responses)
    - [Attaching Cookies To Responses](#attaching-cookies-to-responses)
    - [Cookies & Encryption](#cookies-and-encryption)
- [Redirects](#redirects)
    - [Redirecting To Named Routes](#redirecting-named-routes)
    - [Redirecting To Controller Actions](#redirecting-controller-actions)
    - [Redirecting To External Domains](#redirecting-external-domains)
    - [Redirecting With Flashed Session Data](#redirecting-with-flashed-session-data)
- [Other Response Types](#other-response-types)
    - [View Responses](#view-responses)
    - [JSON Responses](#json-responses)
    - [File Downloads](#file-downloads)
    - [File Responses](#file-responses)
- [Response Macros](#response-macros)

<a name="creating-responses"></a>
<!-- ## Creating Responses -->
## Creating Responses

<a name="strings-arrays"></a>
<!-- #### Strings & Arrays -->
#### Strings & Arrays

<!-- All routes and controllers should return a response to be sent back to the user's browser. Laravel provides several different ways to return responses. The most basic response is returning a string from a route or controller. The framework will automatically convert the string into a full HTTP response: -->
모든 라우트와 컨트롤러는 사용자 브라우저로 반환할 응답을 리턴해야 합니다. Laravel은 다양한 방식으로 응답을 반환할 수 있습니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것입니다. Laravel은 문자열을 자동으로 완전한 HTTP 응답으로 변환합니다.

```
Route::get('/', function () {
    return 'Hello World';
});
```

<!-- In addition to returning strings from your routes and controllers, you may also return arrays. The framework will automatically convert the array into a JSON response: -->
라우트나 컨트롤러에서 문자열뿐 아니라 배열도 반환할 수 있습니다. 배열을 반환하면 Laravel이 해당 배열을 자동으로 JSON 응답으로 변환합니다.

```
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!TIP]
> [Eloquent collections](/docs/8.x/eloquent-collections)도 라우트나 컨트롤러에서 반환할 수 있다는 사실, 알고 계셨나요? 컬렉션도 자동으로 JSON으로 변환됩니다. 한번 시도해 보세요!

<a name="response-objects"></a>
<!-- #### Response Objects -->
#### Response Objects

<!-- Typically, you won't just be returning simple strings or arrays from your route actions. Instead, you will be returning full `Illuminate\Http\Response` instances or [views](/docs/8.x/views). -->
실제 개발에서는 단순히 문자열이나 배열만 반환하는 경우는 드물며, 주로 `Illuminate\Http\Response` 인스턴스나 [views](/docs/8.x/views)를 반환하게 됩니다.

<!-- Returning a full `Response` instance allows you to customize the response's HTTP status code and headers. A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, which provides a variety of methods for building HTTP responses: -->
`Response` 인스턴스를 반환하면, HTTP 상태 코드와 헤더를 자유롭게 지정할 수 있습니다. `Response` 클래스는 `Symfony\Component\HttpFoundation\Response` 클래스를 상속하고 있기 때문에, HTTP 응답을 구성하기 위한 다양한 메서드를 사용할 수 있습니다.

```
Route::get('/home', function () {
    return response('Hello World', 200)
                  ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
<!-- #### Eloquent Models & Collections -->
#### Eloquent Models & Collections

<!-- You may also return [Eloquent ORM](/docs/8.x/eloquent) models and collections directly from your routes and controllers. When you do, Laravel will automatically convert the models and collections to JSON responses while respecting the model's [hidden attributes](/docs/8.x/eloquent-serialization#hiding-attributes-from-json): -->
[Eloquent ORM](/docs/8.x/eloquent) 모델이나 컬렉션을 라우트 또는 컨트롤러에서 바로 반환하는 것도 가능합니다. 이렇게 반환하면, Laravel이 모델과 컬렉션을 자동으로 JSON 응답으로 변환해줍니다. 이때 모델의 [hidden attributes](/docs/8.x/eloquent-serialization#hiding-attributes-from-json)도 자동으로 반영됩니다.

```
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```

<a name="attaching-headers-to-responses"></a>
<!-- ### Attaching Headers To Responses -->
### Attaching Headers To Responses

<!-- Keep in mind that most response methods are chainable, allowing for the fluent construction of response instances. For example, you may use the `header` method to add a series of headers to the response before sending it back to the user: -->
대부분의 응답 관련 메서드는 체이닝이 가능하므로, 다양한 헤더를 메서드 체이닝 방식으로 손쉽게 추가할 수 있습니다. 예를 들어, `header` 메서드를 사용해서 응답에 여러 헤더를 추가할 수 있습니다.

```
return response($content)
            ->header('Content-Type', $type)
            ->header('X-Header-One', 'Header Value')
            ->header('X-Header-Two', 'Header Value');
```

<!-- Or, you may use the `withHeaders` method to specify an array of headers to be added to the response: -->
또는 `withHeaders` 메서드를 사용해 한 번에 여러 헤더를 배열 형태로 지정할 수도 있습니다.

```
return response($content)
            ->withHeaders([
                'Content-Type' => $type,
                'X-Header-One' => 'Header Value',
                'X-Header-Two' => 'Header Value',
            ]);
```

<a name="cache-control-middleware"></a>
<!-- #### Cache Control Middleware -->
#### Cache Control Middleware

<!-- Laravel includes a `cache.headers` middleware, which may be used to quickly set the `Cache-Control` header for a group of routes. Directives should be provided using the "snake case" equivalent of the corresponding cache-control directive and should be separated by a semicolon. If `etag` is specified in the list of directives, an MD5 hash of the response content will automatically be set as the ETag identifier: -->
Laravel에는 `cache.headers` 미들웨어가 내장되어 있어, 여러 라우트에서 `Cache-Control` 헤더를 간편하게 지정할 수 있습니다. 각 디렉티브는 해당 캐시 컨트롤 디렉티브의 스네이크 케이스 형식으로 작성하며, 세미콜론으로 구분합니다. 만약 `etag` 디렉티브를 명시하면, 응답 내용의 MD5 해시값이 ETag 식별자로 자동 설정됩니다.

```
Route::middleware('cache.headers:public;max_age=2628000;etag')->group(function () {
    Route::get('/privacy', function () {
        // ...
    });

    Route::get('/terms', function () {
        // ...
    });
});
```

<a name="attaching-cookies-to-responses"></a>
<!-- ### Attaching Cookies To Responses -->
### Attaching Cookies To Responses

<!-- You may attach a cookie to an outgoing `Illuminate\Http\Response` instance using the `cookie` method. You should pass the name, value, and the number of minutes the cookie should be considered valid to this method: -->
`Illuminate\Http\Response` 인스턴스의 `cookie` 메서드를 사용해서, 응답에 쿠키를 붙일 수 있습니다. 쿠키명, 값, 그리고 쿠키가 유효한 시간(분)을 인수로 전달합니다.

```
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

<!-- The `cookie` method also accepts a few more arguments which are used less frequently. Generally, these arguments have the same purpose and meaning as the arguments that would be given to PHP's native [setcookie](https://secure.php.net/manual/en/function.setcookie.php) method: -->
`cookie` 메서드는 추가로 몇 가지 인수를 더 받을 수 있습니다. 이 인수들은 PHP의 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수와 거의 동일한 역할을 합니다.

```
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

<!-- If you would like to ensure that a cookie is sent with the outgoing response but you do not yet have an instance of that response, you can use the `Cookie` facade to "queue" cookies for attachment to the response when it is sent. The `queue` method accepts the arguments needed to create a cookie instance. These cookies will be attached to the outgoing response before it is sent to the browser: -->
아직 응답 인스턴스가 없는 상황에서, 특정 쿠키가 응답에 꼭 포함되길 원한다면 `Cookie` 파사드를 이용해서 쿠키를 "큐"에 등록할 수 있습니다. `queue` 메서드는 쿠키를 생성하는 데 필요한 인수들을 받아, 응답이 전송되기 전에 쿠키를 자동으로 붙여줍니다.

```
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
<!-- #### Generating Cookie Instances -->
#### Generating Cookie Instances

<!-- If you would like to generate a `Symfony\Component\HttpFoundation\Cookie` instance that can be attached to a response instance at a later time, you may use the global `cookie` helper. This cookie will not be sent back to the client unless it is attached to a response instance: -->
나중에 응답 인스턴스에 붙이기 위해 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하고 싶다면, 전역 `cookie` 헬퍼를 사용하면 됩니다. 이렇게 생성한 쿠키는 반드시 응답에 추가해야만 실제로 클라이언트에 전달됩니다.

```
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
<!-- #### Expiring Cookies Early -->
#### Expiring Cookies Early

<!-- You may remove a cookie by expiring it via the `withoutCookie` method of an outgoing response: -->
응답의 `withoutCookie` 메서드를 이용해, 특정 쿠키를 만료시켜 삭제할 수 있습니다.

```
return response('Hello World')->withoutCookie('name');
```

<!-- If you do not yet have an instance of the outgoing response, you may use the `Cookie` facade's `expire` method to expire a cookie: -->
아직 응답 인스턴스가 없다면, `Cookie` 파사드의 `expire` 메서드를 사용해 쿠키를 만료시킬 수 있습니다.

```
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
<!-- ### Cookies & Encryption -->
### Cookies & Encryption

<!-- By default, all cookies generated by Laravel are encrypted and signed so that they can't be modified or read by the client. If you would like to disable encryption for a subset of cookies generated by your application, you may use the `$except` property of the `App\Http\Middleware\EncryptCookies` middleware, which is located in the `app/Http/Middleware` directory: -->
Laravel이 기본적으로 만들어내는 모든 쿠키는 클라이언트에서 수정하거나 읽을 수 없도록 암호화 및 서명 처리가 되어 있습니다. 만약 애플리케이션에서 생성되는 일부 쿠키만 암호화를 비활성화하고 싶다면, `app/Http/Middleware` 디렉터리의 `App\Http\Middleware\EncryptCookies` 미들웨어 클래스 내 `$except` 속성에 쿠키명을 지정하면 됩니다.

```
/**
 * The names of the cookies that should not be encrypted.
 *
 * @var array
 */
protected $except = [
    'cookie_name',
];
```

<a name="redirects"></a>
<!-- ## Redirects -->
## Redirects

<!-- Redirect responses are instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL. There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the global `redirect` helper: -->
리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 안내하기 위한 적절한 헤더를 포함합니다. 여러 가지 방식으로 `RedirectResponse` 인스턴스를 만들 수 있는데, 가장 단순한 방법은 전역 `redirect` 헬퍼를 이용하는 것입니다.

```
Route::get('/dashboard', function () {
    return redirect('home/dashboard');
});
```

<!-- Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/8.x/session), make sure the route calling the `back` function is using the `web` middleware group: -->
때로는 사용자를 이전 위치로 리다이렉트해야 할 때가 있습니다. 예를 들어, 폼 제출이 유효하지 않은 경우, `back` 헬퍼 함수를 사용하면 이전 위치로 쉽게 리다이렉트할 수 있습니다. 이 기능은 [session](/docs/8.x/session)을 이용하므로, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹에 속해야 합니다.

```
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
<!-- ### Redirecting To Named Routes -->
### Redirecting To Named Routes

<!-- When you call the `redirect` helper with no parameters, an instance of `Illuminate\Routing\Redirector` is returned, allowing you to call any method on the `Redirector` instance. For example, to generate a `RedirectResponse` to a named route, you may use the `route` method: -->
`redirect` 헬퍼를 인수 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 `Redirector` 인스턴스의 다양한 메서드를 호출할 수 있습니다. 예를 들어, 네임드 라우트로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용합니다.

```
return redirect()->route('login');
```

<!-- If your route has parameters, you may pass them as the second argument to the `route` method: -->
라우트에 파라미터가 필요한 경우, 파라미터는 `route` 메서드의 두 번째 인수로 전달합니다.

```
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
<!-- #### Populating Parameters Via Eloquent Models -->
#### Populating Parameters Via Eloquent Models

<!-- If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically: -->
Eloquent 모델에서 "ID" 파라미터를 추출해 라우트로 리다이렉트하려면, 모델 인스턴스를 직접 전달해도 됩니다. Laravel이 ID를 자동으로 추출합니다.

```
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

<!-- If you would like to customize the value that is placed in the route parameter, you can specify the column in the route parameter definition (`/profile/{id:slug}`) or you can override the `getRouteKey` method on your Eloquent model: -->
라우트 파라미터에 원하는 값을 직접 지정하고 싶다면, 라우트 파라미터 정의에서 컬럼명을 지정할 수 있고(`/profile/{id:slug}`), 또는 Eloquent 모델의 `getRouteKey` 메서드를 오버라이드할 수도 있습니다.

```
/**
 * Get the value of the model's route key.
 *
 * @return mixed
 */
public function getRouteKey()
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
<!-- ### Redirecting To Controller Actions -->
### Redirecting To Controller Actions

<!-- You may also generate redirects to [controller actions](/docs/8.x/controllers). To do so, pass the controller and action name to the `action` method: -->
[controller actions](/docs/8.x/controllers)으로 리다이렉트해야 할 때는, `action` 메서드에 컨트롤러와 액션명을 지정해주면 됩니다.

```
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

<!-- If your controller route requires parameters, you may pass them as the second argument to the `action` method: -->
컨트롤러 라우트에 파라미터가 필요하다면, `action` 메서드의 두 번째 인수로 전달하면 됩니다.

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
<!-- ### Redirecting To External Domains -->
### Redirecting To External Domains

<!-- Sometimes you may need to redirect to a domain outside of your application. You may do so by calling the `away` method, which creates a `RedirectResponse` without any additional URL encoding, validation, or verification: -->
가끔 애플리케이션 외부의 도메인으로 리다이렉트해야 할 때가 있습니다. 이럴 때는 `away` 메서드를 사용하면 URL 추가 인코딩, 검증, 확인 없이 바로 `RedirectResponse`를 생성할 수 있습니다.

```
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
<!-- ### Redirecting With Flashed Session Data -->
### Redirecting With Flashed Session Data

<!-- Redirecting to a new URL and [flashing data to the session](/docs/8.x/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain: -->
새로운 URL로 리다이렉트하면서, 동시에 [flashing data to the session](/docs/8.x/session#flash-data)하는 경우가 많습니다. 보통 어떤 작업이 성공했을 때, 성공 메시지를 세션에 저장하고 리다이렉트하는 식입니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성한 뒤 메서드 체이닝으로 한 번에 세션에 데이터를 플래시할 수 있습니다.

```
Route::post('/user/profile', function () {
    // ...

    return redirect('dashboard')->with('status', 'Profile updated!');
});
```

<!-- After the user is redirected, you may display the flashed message from the [session](/docs/8.x/session). For example, using [Blade syntax](/docs/8.x/blade): -->
사용자가 리다이렉트된 후에는, [session](/docs/8.x/session)에서 플래시된 메시지를 꺼내서 표시할 수 있습니다. 예를 들어, [Blade syntax](/docs/8.x/blade)을 사용할 수 있습니다.

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

<a name="redirecting-with-input"></a>
<!-- #### Redirecting With Input -->
#### Redirecting With Input

<!-- You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. This is typically done if the user has encountered a validation error. Once the input has been flashed to the session, you may easily [retrieve it](/docs/8.x/requests#retrieving-old-input) during the next request to repopulate the form: -->
`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면, 현재 요청의 입력 데이터를 세션에 저장하여, 사용자가 새로운 위치로 리다이렉트된 후에도 해당 입력 데이터를 쉽게 불러올 수 있습니다. 주로 유효성 검사에 실패했을 때 많이 활용합니다. 입력값이 세션에 플래시된 후에는, [retrieve it](/docs/8.x/requests#retrieving-old-input)해서 폼을 다시 채워 넣을 수 있습니다.

```
return back()->withInput();
```

<a name="other-response-types"></a>
<!-- ## Other Response Types -->
## Other Response Types

<!-- The `response` helper may be used to generate other types of response instances. When the `response` helper is called without arguments, an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/8.x/contracts) is returned. This contract provides several helpful methods for generating responses. -->
`response` 헬퍼는 다른 타입의 응답 인스턴스를 생성하는 데에도 사용할 수 있습니다. `response` 헬퍼를 인수 없이 호출하면, `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/8.x/contracts)을 구현한 인스턴스가 반환됩니다. 이 계약에서는 여러 가지 유용한 응답 생성 메서드를 제공합니다.

<a name="view-responses"></a>
<!-- ### View Responses -->
### View Responses

<!-- If you need control over the response's status and headers but also need to return a [view](/docs/8.x/views) as the response's content, you should use the `view` method: -->
응답의 상태 코드와 헤더를 직접 지정하면서도, [view](/docs/8.x/views)를 응답 본문으로 사용해야 한다면 `view` 메서드를 사용하면 됩니다.

```
return response()
            ->view('hello', $data, 200)
            ->header('Content-Type', $type);
```

<!-- Of course, if you do not need to pass a custom HTTP status code or custom headers, you may use the global `view` helper function. -->
단, HTTP 상태 코드나 헤더 값을 지정할 필요가 없다면, 전역 `view` 헬퍼 함수를 그대로 사용해도 됩니다.

<a name="json-responses"></a>
<!-- ### JSON Responses -->
### JSON Responses

<!-- The `json` method will automatically set the `Content-Type` header to `application/json`, as well as convert the given array to JSON using the `json_encode` PHP function: -->
`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 지정하고, 전달받은 배열을 PHP의 `json_encode` 함수를 사용해 JSON으로 변환해줍니다.

```
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

<!-- If you would like to create a JSONP response, you may use the `json` method in combination with the `withCallback` method: -->
만약 JSONP 응답을 만들고 싶다면, `json` 메서드와 `withCallback` 메서드를 조합해서 사용할 수 있습니다.

```
return response()
            ->json(['name' => 'Abigail', 'state' => 'CA'])
            ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
<!-- ### File Downloads -->
### File Downloads

<!-- The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method: -->
`download` 메서드는 지정한 경로의 파일을 사용자 브라우저가 강제로 다운로드 하게 하는 응답을 생성합니다. `download` 메서드는 다운로드되는 파일명을 두 번째 인수로 받으며, 세 번째 인수로 HTTP 헤더 배열을 넘길 수 있습니다.

```
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!NOTE]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은, 다운로드할 파일명이 반드시 ASCII 문자여야 합니다.

<a name="streamed-downloads"></a>
<!-- #### Streamed Downloads -->
#### Streamed Downloads

<!-- Sometimes you may wish to turn the string response of a given operation into a downloadable response without having to write the contents of the operation to disk. You may use the `streamDownload` method in this scenario. This method accepts a callback, filename, and an optional array of headers as its arguments: -->
특정 작업의 결과로 나온 문자열을 파일처럼 바로 다운로드시키고 싶을 때, 임시 파일을 따로 만들지 않고도 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고 (선택적으로) 헤더 배열을 인수로 받습니다.

```
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
                ->contents()
                ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```

<a name="file-responses"></a>
<!-- ### File Responses -->
### File Responses

<!-- The `file` method may be used to display a file, such as an image or PDF, directly in the user's browser instead of initiating a download. This method accepts the path to the file as its first argument and an array of headers as its second argument: -->
`file` 메서드를 사용하면, 이미지나 PDF와 같이 파일을 다운로드하지 않고 브라우저 화면에 바로 표시할 수 있습니다. 첫 번째 인수로 파일 경로를, 두 번째 인수로 헤더 배열을 넘깁니다.

```
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="response-macros"></a>
<!-- ## Response Macros -->
## Response Macros

<!-- If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on the `Response` facade. Typically, you should call this method from the `boot` method of one of your application's [service providers](/docs/8.x/providers), such as the `App\Providers\AppServiceProvider` service provider: -->
여러 라우트나 컨트롤러에서 재사용할 수 있는 커스텀 응답을 만들고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 보통 이 메서드는 애플리케이션의 [service providers](/docs/8.x/providers), 예를 들어 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 호출합니다.

```
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     *
     * @return void
     */
    public function boot()
    {
        Response::macro('caps', function ($value) {
            return Response::make(strtoupper($value));
        });
    }
}
```

<!-- The `macro` function accepts a name as its first argument and a closure as its second argument. The macro's closure will be executed when calling the macro name from a `ResponseFactory` implementation or the `response` helper: -->
`macro` 함수는 첫 번째 인수에 매크로 이름을, 두 번째 인수에 클로저를 받습니다. 매크로로 등록된 클로저는 `ResponseFactory` 구현이나 `response` 헬퍼에서 매크로 이름으로 호출할 때 실행됩니다.

```
return response()->caps('foo');
```
