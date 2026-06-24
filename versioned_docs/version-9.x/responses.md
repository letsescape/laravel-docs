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
모든 라우트와 컨트롤러는 최종적으로 사용자 브라우저로 보낼 응답을 반환해야 합니다. Laravel에서는 다양한 방식으로 응답을 반환할 수 있습니다. 가장 기본적인 방법은 라우트나 컨트롤러에서 문자열을 반환하는 것인데, 프레임워크가 이 문자열을 자동으로 완전한 HTTP 응답으로 만들어 줍니다.

```
Route::get('/', function () {
    return 'Hello World';
});
```

<!-- In addition to returning strings from your routes and controllers, you may also return arrays. The framework will automatically convert the array into a JSON response: -->
라우트나 컨트롤러에서 문자열뿐만 아니라 배열도 반환할 수 있습니다. 배열을 반환하면 프레임워크가 이를 자동으로 JSON 응답으로 변환합니다.

```
Route::get('/', function () {
    return [1, 2, 3];
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent collections](/docs/9.x/eloquent-collections)도 반환할 수 있다는 것을 알고 계셨나요? 자동으로 JSON으로 변환되어 응답됩니다. 한번 시도해 보세요!

<a name="response-objects"></a>
<!-- #### Response Objects -->
#### Response Objects

<!-- Typically, you won't just be returning simple strings or arrays from your route actions. Instead, you will be returning full `Illuminate\Http\Response` instances or [views](/docs/9.x/views). -->
실무에서는 단순한 문자열이나 배열만 반환하는 경우는 드뭅니다. 일반적으로는 `Illuminate\Http\Response` 인스턴스나 [views](/docs/9.x/views) 를 반환하게 됩니다.

<!-- Returning a full `Response` instance allows you to customize the response's HTTP status code and headers. A `Response` instance inherits from the `Symfony\Component\HttpFoundation\Response` class, which provides a variety of methods for building HTTP responses: -->
`Response` 인스턴스를 반환하면 HTTP 상태 코드나 헤더 값을 자유롭게 지정할 수 있습니다. `Response` 클래스는 `Symfony\Component\HttpFoundation\Response`를 상속하고 있으므로, HTTP 응답을 만들기 위한 다양한 메서드를 제공합니다.

```
Route::get('/home', function () {
    return response('Hello World', 200)
                  ->header('Content-Type', 'text/plain');
});
```

<a name="eloquent-models-and-collections"></a>
<!-- #### Eloquent Models & Collections -->
#### Eloquent Models & Collections

<!-- You may also return [Eloquent ORM](/docs/9.x/eloquent) models and collections directly from your routes and controllers. When you do, Laravel will automatically convert the models and collections to JSON responses while respecting the model's [hidden attributes](/docs/9.x/eloquent-serialization#hiding-attributes-from-json): -->
[Eloquent ORM](/docs/9.x/eloquent)의 모델이나 컬렉션도 라우트나 컨트롤러에서 직접 반환할 수 있습니다. 이 경우 Laravel이 해당 모델이나 컬렉션을 자동으로 JSON 응답으로 변환하며, 모델의 [hidden attributes](/docs/9.x/eloquent-serialization#hiding-attributes-from-json) 역시 존중하여 처리합니다.

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
대부분의 응답 메서드는 메서드 체이닝을 지원하므로, 여러 개의 헤더를 연속적으로 지정하여 응답 객체를 손쉽게 생성할 수 있습니다. 예를 들어, `header` 메서드를 여러 번 호출해 다양한 헤더를 응답에 추가할 수 있습니다.

```
return response($content)
            ->header('Content-Type', $type)
            ->header('X-Header-One', 'Header Value')
            ->header('X-Header-Two', 'Header Value');
```

<!-- Or, you may use the `withHeaders` method to specify an array of headers to be added to the response: -->
또는, `withHeaders` 메서드를 사용해 헤더들을 배열 형태로 한 번에 추가할 수도 있습니다.

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
Laravel에는 `cache.headers` 미들웨어가 포함되어 있어, 여러 라우트에 대해 `Cache-Control` 헤더를 손쉽게 설정할 수 있습니다. 각 디렉티브는 해당 cache-control 옵션의 snake case 형태로, 세미콜론(;)으로 구분하여 지정합니다. 만약 `etag`를 포함시키면, 응답 컨텐츠의 MD5 해시값이 자동으로 ETag로 설정됩니다.

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
`Illuminate\Http\Response` 인스턴스의 `cookie` 메서드를 통해 응답에 쿠키를 추가할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 유효기간(분 단위)을 전달하면 됩니다.

```
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```

<!-- The `cookie` method also accepts a few more arguments which are used less frequently. Generally, these arguments have the same purpose and meaning as the arguments that would be given to PHP's native [setcookie](https://secure.php.net/manual/en/function.setcookie.php) method: -->
`cookie` 메서드는 종종 잘 사용되지 않는 몇 가지 추가 인수도 받을 수 있습니다. 이 인수들은 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 함수에 전달하는 인수와 동일하게 동작합니다.

```
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```

<!-- If you would like to ensure that a cookie is sent with the outgoing response but you do not yet have an instance of that response, you can use the `Cookie` facade to "queue" cookies for attachment to the response when it is sent. The `queue` method accepts the arguments needed to create a cookie instance. These cookies will be attached to the outgoing response before it is sent to the browser: -->
아직 응답 인스턴스가 없는 상황에서도, `Cookie` 파사드를 이용하여 쿠키를 "큐"에 등록하고, 실제 응답이 생성될 때 쿠키를 붙일 수도 있습니다. `queue` 메서드는 쿠키 인스턴스를 만들 때 필요한 인수들을 받으며, 등록된 쿠키들은 실제 응답이 브라우저로 전송될 때 자동으로 추가됩니다.

```
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```

<a name="generating-cookie-instances"></a>
<!-- #### Generating Cookie Instances -->
#### Generating Cookie Instances

<!-- If you would like to generate a `Symfony\Component\HttpFoundation\Cookie` instance that can be attached to a response instance at a later time, you may use the global `cookie` helper. This cookie will not be sent back to the client unless it is attached to a response instance: -->
나중에 응답 인스턴스에 붙이기 위해, `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 미리 생성해 둘 수도 있습니다. 이 때는 전역 `cookie` 헬퍼 함수를 사용하면 됩니다. 이렇게 생성한 쿠키는 반드시 응답 인스턴스에 추가해야만 브라우저로 전달됩니다.

```
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```

<a name="expiring-cookies-early"></a>
<!-- #### Expiring Cookies Early -->
#### Expiring Cookies Early

<!-- You may remove a cookie by expiring it via the `withoutCookie` method of an outgoing response: -->
응답에서 `withoutCookie` 메서드를 사용하면 특정 쿠키를 미리 만료시켜 제거할 수 있습니다.

```
return response('Hello World')->withoutCookie('name');
```

<!-- If you do not yet have an instance of the outgoing response, you may use the `Cookie` facade's `expire` method to expire a cookie: -->
아직 응답 인스턴스가 없는 경우라면, `Cookie` 파사드의 `expire` 메서드를 사용해도 쿠키를 만료시킬 수 있습니다.

```
Cookie::expire('name');
```

<a name="cookies-and-encryption"></a>
<!-- ### Cookies & Encryption -->
### Cookies & Encryption

<!-- By default, all cookies generated by Laravel are encrypted and signed so that they can't be modified or read by the client. If you would like to disable encryption for a subset of cookies generated by your application, you may use the `$except` property of the `App\Http\Middleware\EncryptCookies` middleware, which is located in the `app/Http/Middleware` directory: -->
기본적으로 Laravel에서 발급되는 모든 쿠키는 암호화되고 서명되어, 클라이언트가 내용을 읽거나 변조할 수 없습니다. 만약 특정 쿠키에 한해 암호화를 사용하지 않으려면, `app/Http/Middleware` 디렉터리에 있는 `App\Http\Middleware\EncryptCookies` 미들웨어의 `$except` 속성에 해당 쿠키의 이름을 추가하면 됩니다.

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
리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스로, 사용자를 다른 URL로 이동할 때 필요한 적절한 헤더를 포함합니다. 다양한 방식으로 `RedirectResponse` 인스턴스를 생성할 수 있지만, 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

```
Route::get('/dashboard', function () {
    return redirect('home/dashboard');
});
```

<!-- Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/9.x/session), make sure the route calling the `back` function is using the `web` middleware group: -->
종종 사용자가 이전 페이지로 돌아가게 하고 싶을 때가 있습니다. 예를 들어, 입력 폼이 올바르지 않을 때 이전 위치로 돌려보낼 수 있는데, 이럴 때는 전역 `back` 헬퍼 함수를 사용하세요. 이 기능은 [session](/docs/9.x/session)을 활용하므로, 반드시 `back` 함수를 호출하는 라우트가 `web` 미들웨어 그룹을 사용하는지 확인해야 합니다.

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
`redirect` 헬퍼를 아무 인수 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 리턴되고, `Redirector` 인스턴스에서 다양한 메서드를 사용할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용할 수 있습니다.

```
return redirect()->route('login');
```

<!-- If your route has parameters, you may pass them as the second argument to the `route` method: -->
라우트에 파라미터가 필요한 경우, `route` 메서드의 두 번째 인수로 파라미터 배열을 전달합니다.

```
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
<!-- #### Populating Parameters Via Eloquent Models -->
#### Populating Parameters Via Eloquent Models

<!-- If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically: -->
라우트 파라미터(ID 등)가 Eloquent 모델에서 채워지는 경우, 모델 인스턴스 자체를 전달할 수도 있습니다. 그러면 ID가 자동으로 추출되어 적용됩니다.

```
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```

<!-- If you would like to customize the value that is placed in the route parameter, you can specify the column in the route parameter definition (`/profile/{id:slug}`) or you can override the `getRouteKey` method on your Eloquent model: -->
특정 컬럼 값을 라우트 파라미터로 사용하고 싶다면, 라우트 파라미터 정의에서 해당 컬럼을 지정하거나(`/profile/{id:slug}`) Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드할 수 있습니다.

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

<!-- You may also generate redirects to [controller actions](/docs/9.x/controllers). To do so, pass the controller and action name to the `action` method: -->
[controller actions](/docs/9.x/controllers)으로도 리다이렉트할 수 있습니다. 이때는 `action` 메서드에 컨트롤러 이름과 액션 메서드명을 전달하면 됩니다.

```
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```

<!-- If your controller route requires parameters, you may pass them as the second argument to the `action` method: -->
컨트롤러 라우트에 파라미터가 필요하다면 `action` 메서드의 두 번째 인수로 파라미터 배열을 전달하세요.

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-external-domains"></a>
<!-- ### Redirecting To External Domains -->
### Redirecting To External Domains

<!-- Sometimes you may need to redirect to a domain outside of your application. You may do so by calling the `away` method, which creates a `RedirectResponse` without any additional URL encoding, validation, or verification: -->
가끔 애플리케이션 외부의 도메인으로 리다이렉트할 필요가 있을 때, `away` 메서드를 사용하면 추가적인 URL 인코딩, 검증, 확인 없이 `RedirectResponse`를 생성할 수 있습니다.

```
return redirect()->away('https://www.google.com');
```

<a name="redirecting-with-flashed-session-data"></a>
<!-- ### Redirecting With Flashed Session Data -->
### Redirecting With Flashed Session Data

<!-- Redirecting to a new URL and [flashing data to the session](/docs/9.x/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain: -->
새 URL로 리다이렉트하면서 [flashing data to the session](/docs/9.x/session#flash-data)하는 경우가 자주 있습니다. 주로 특정 작업이 성공적으로 처리된 뒤에, 성공 메시지를 세션에 저장해 전달할 때 사용됩니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성한 뒤 한 번의 메서드 체이닝으로 세션에 데이터를 플래시할 수 있습니다.

```
Route::post('/user/profile', function () {
    // ...

    return redirect('dashboard')->with('status', 'Profile updated!');
});
```

<!-- After the user is redirected, you may display the flashed message from the [session](/docs/9.x/session). For example, using [Blade syntax](/docs/9.x/blade): -->
사용자가 리다이렉트된 이후에는 [session](/docs/9.x/session)에 저장된 메시지를 화면에 표시할 수 있습니다. 예를 들어 [Blade syntax](/docs/9.x/blade)에서는 아래와 같이 할 수 있습니다.

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

<!-- You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. This is typically done if the user has encountered a validation error. Once the input has been flashed to the session, you may easily [retrieve it](/docs/9.x/requests#retrieving-old-input) during the next request to repopulate the form: -->
`RedirectResponse` 인스턴스에서 제공하는 `withInput` 메서드를 활용하면, 현재 요청의 입력값을 세션에 플래시하고 사용자를 새로운 위치로 리다이렉트할 수 있습니다. 주로 유효성 검사에 실패한 경우에 활용하며, 플래시된 입력값은 다음 요청에서 손쉽게 [retrieve it](/docs/9.x/requests#retrieving-old-input)하여 폼을 다시 채울 수 있습니다.

```
return back()->withInput();
```

<a name="other-response-types"></a>
<!-- ## Other Response Types -->
## Other Response Types

<!-- The `response` helper may be used to generate other types of response instances. When the `response` helper is called without arguments, an implementation of the `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/9.x/contracts) is returned. This contract provides several helpful methods for generating responses. -->
`response` 헬퍼는 다양한 유형의 응답 인스턴스를 쉽게 생성할 때 사용할 수 있습니다. 인수 없이 `response` 헬퍼를 호출하면 `Illuminate\Contracts\Routing\ResponseFactory` [contract](/docs/9.x/contracts)의 구현 인스턴스가 반환됩니다. 이 컨트랙트에는 여러 유용한 응답 생성 메서드가 포함되어 있습니다.

<a name="view-responses"></a>
<!-- ### View Responses -->
### View Responses

<!-- If you need control over the response's status and headers but also need to return a [view](/docs/9.x/views) as the response's content, you should use the `view` method: -->
응답의 상태 코드와 헤더 값을 직접 지정할 필요가 있으면서도, [view](/docs/9.x/views) 콘텐츠로 응답을 반환하고 싶다면 `view` 메서드를 사용하세요.

```
return response()
            ->view('hello', $data, 200)
            ->header('Content-Type', $type);
```

<!-- Of course, if you do not need to pass a custom HTTP status code or custom headers, you may use the global `view` helper function. -->
별도의 HTTP 상태 코드나 헤더를 지정할 필요가 없다면 전역 `view` 헬퍼 함수를 그대로 사용할 수도 있습니다.

<a name="json-responses"></a>
<!-- ### JSON Responses -->
### JSON Responses

<!-- The `json` method will automatically set the `Content-Type` header to `application/json`, as well as convert the given array to JSON using the `json_encode` PHP function: -->
`json` 메서드는 `Content-Type` 헤더를 자동으로 `application/json`으로 지정하고, 전달된 배열을 PHP의 `json_encode` 함수를 이용해 JSON 문자열로 변환합니다.

```
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```

<!-- If you would like to create a JSONP response, you may use the `json` method in combination with the `withCallback` method: -->
JSONP 응답을 만들려면 `json` 메서드와 함께 `withCallback` 메서드도 사용할 수 있습니다.

```
return response()
            ->json(['name' => 'Abigail', 'state' => 'CA'])
            ->withCallback($request->input('callback'));
```

<a name="file-downloads"></a>
<!-- ### File Downloads -->
### File Downloads

<!-- The `download` method may be used to generate a response that forces the user's browser to download the file at the given path. The `download` method accepts a filename as the second argument to the method, which will determine the filename that is seen by the user downloading the file. Finally, you may pass an array of HTTP headers as the third argument to the method: -->
`download` 메서드는 특정 경로의 파일을 사용자의 브라우저가 다운로드하도록 유도하는 응답을 생성합니다. `download` 메서드는 두 번째 인수로 다운로드 시 사용자에게 보여질 파일명을 받으며, 세 번째 인수로는 추가적인 HTTP 헤더의 배열을 전달할 수 있습니다.

```
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```

> [!WARNING]
> 파일 다운로드를 담당하는 Symfony HttpFoundation은 다운로드 파일의 이름이 반드시 ASCII 문자여야 합니다.

<a name="streamed-downloads"></a>
<!-- #### Streamed Downloads -->
#### Streamed Downloads

<!-- Sometimes you may wish to turn the string response of a given operation into a downloadable response without having to write the contents of the operation to disk. You may use the `streamDownload` method in this scenario. This method accepts a callback, filename, and an optional array of headers as its arguments: -->
작업 결과 문자열을 파일로 먼저 저장하지 않고 바로 다운로드 형태로 제공하고 싶을 때는 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일명, 그리고 선택적으로 헤더 배열을 인수로 받습니다.

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
`file` 메서드는 이미지나 PDF 같은 파일을 다운로드가 아닌, 브라우저 내에서 바로 보여주는 용도로 사용할 수 있습니다. 첫 번째 인수로 파일 경로를, 두 번째 인수로 헤더 배열을 전달합니다.

```
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```

<a name="response-macros"></a>
<!-- ## Response Macros -->
## Response Macros

<!-- If you would like to define a custom response that you can re-use in a variety of your routes and controllers, you may use the `macro` method on the `Response` facade. Typically, you should call this method from the `boot` method of one of your application's [service providers](/docs/9.x/providers), such as the `App\Providers\AppServiceProvider` service provider: -->
여러 라우트와 컨트롤러에서 반복적으로 사용할 맞춤 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용해 매크로를 등록할 수 있습니다. 보통 이 작업은 애플리케이션의 [service providers](/docs/9.x/providers), 예를 들면 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 수행합니다.

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
`macro` 함수는 첫 번째 인수로 매크로명을, 두 번째 인수로 클로저(익명 함수)를 받습니다. 이렇게 등록한 매크로는 `ResponseFactory` 구현체나 `response` 헬퍼에서 매크로 이름을 호출하는 것으로 실행할 수 있습니다.

```
return response()->caps('foo');
```
