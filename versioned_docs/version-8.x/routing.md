<!-- # Routing -->
# Routing

- [Basic Routing](#basic-routing)
    - [Redirect Routes](#redirect-routes)
    - [View Routes](#view-routes)
- [Route Parameters](#route-parameters)
    - [Required Parameters](#required-parameters)
    - [Optional Parameters](#parameters-optional-parameters)
    - [Regular Expression Constraints](#parameters-regular-expression-constraints)
- [Named Routes](#named-routes)
- [Route Groups](#route-groups)
    - [Middleware](#route-group-middleware)
    - [Controllers](#route-group-controllers)
    - [Subdomain Routing](#route-group-subdomain-routing)
    - [Route Prefixes](#route-group-prefixes)
    - [Route Name Prefixes](#route-group-name-prefixes)
- [Route Model Binding](#route-model-binding)
    - [Implicit Binding](#implicit-binding)
    - [Explicit Binding](#explicit-binding)
- [Fallback Routes](#fallback-routes)
- [Rate Limiting](#rate-limiting)
    - [Defining Rate Limiters](#defining-rate-limiters)
    - [Attaching Rate Limiters To Routes](#attaching-rate-limiters-to-routes)
- [Form Method Spoofing](#form-method-spoofing)
- [Accessing The Current Route](#accessing-the-current-route)
- [Cross-Origin Resource Sharing (CORS)](#cors)
- [Route Caching](#route-caching)

<a name="basic-routing"></a>
<!-- ## Basic Routing -->
## Basic Routing

<!-- The most basic Laravel routes accept a URI and a closure, providing a very simple and expressive method of defining routes and behavior without complicated routing configuration files: -->
Laravel에서 가장 기본적인 라우트는 URI와 클로저(익명 함수)를 받아, 복잡한 라우팅 설정 파일 없이도 매우 간단하고 직관적으로 라우트와 동작을 정의할 수 있도록 해줍니다.

```
use Illuminate\Support\Facades\Route;

Route::get('/greeting', function () {
    return 'Hello World';
});
```

<a name="the-default-route-files"></a>
<!-- #### The Default Route Files -->
#### The Default Route Files

<!-- All Laravel routes are defined in your route files, which are located in the `routes` directory. These files are automatically loaded by your application's `App\Providers\RouteServiceProvider`. The `routes/web.php` file defines routes that are for your web interface. These routes are assigned the `web` middleware group, which provides features like session state and CSRF protection. The routes in `routes/api.php` are stateless and are assigned the `api` middleware group. -->
모든 Laravel 라우트는 `routes` 디렉토리 내의 라우트 파일에 정의됩니다. 이 파일들은 애플리케이션의 `App\Providers\RouteServiceProvider`에 의해 자동으로 로드됩니다. `routes/web.php` 파일은 웹 인터페이스를 위한 라우트를 정의하며, 이 파일의 라우트는 세션 상태, CSRF 보호와 같은 기능을 제공하는 `web` 미들웨어 그룹이 할당됩니다. 반면, `routes/api.php`의 라우트는 상태를 보관하지 않으며, `api` 미들웨어 그룹이 할당됩니다.

<!-- For most applications, you will begin by defining routes in your `routes/web.php` file. The routes defined in `routes/web.php` may be accessed by entering the defined route's URL in your browser. For example, you may access the following route by navigating to `http://example.com/user` in your browser: -->
대부분의 애플리케이션에서는 `routes/web.php` 파일에 라우트 정의를 시작합니다. `routes/web.php`에 정의된 라우트는 브라우저에서 해당 URL로 접속하여 접근할 수 있습니다. 예를 들어, 아래 라우트는 브라우저에서 `http://example.com/user`로 접속하면 동작합니다.

```
use App\Http\Controllers\UserController;

Route::get('/user', [UserController::class, 'index']);
```

<!-- Routes defined in the `routes/api.php` file are nested within a route group by the `RouteServiceProvider`. Within this group, the `/api` URI prefix is automatically applied so you do not need to manually apply it to every route in the file. You may modify the prefix and other route group options by modifying your `RouteServiceProvider` class. -->
`routes/api.php` 파일에 정의된 라우트는 `RouteServiceProvider`에 의해 라우트 그룹 내부에 중첩됩니다. 이 그룹 내에서는 `/api` URI 프리픽스가 자동으로 적용되므로, 파일 내의 모든 라우트에 별도로 프리픽스를 붙일 필요가 없습니다. 프리픽스 및 기타 라우트 그룹 옵션은 `RouteServiceProvider` 클래스를 수정하여 변경할 수 있습니다.

<a name="available-router-methods"></a>
<!-- #### Available Router Methods -->
#### Available Router Methods

<!-- The router allows you to register routes that respond to any HTTP verb: -->
라우터에서는 모든 HTTP 메서드에 대응하는 라우트를 등록할 수 있습니다.

```
Route::get($uri, $callback);
Route::post($uri, $callback);
Route::put($uri, $callback);
Route::patch($uri, $callback);
Route::delete($uri, $callback);
Route::options($uri, $callback);
```

<!-- Sometimes you may need to register a route that responds to multiple HTTP verbs. You may do so using the `match` method. Or, you may even register a route that responds to all HTTP verbs using the `any` method: -->
여러 HTTP 메서드에 동시에 반응하는 라우트를 등록해야 할 때는 `match` 메서드를 사용할 수 있고, 모든 HTTP 메서드에 반응하도록 하려면 `any` 메서드를 사용할 수 있습니다.

```
Route::match(['get', 'post'], '/', function () {
    //
});

Route::any('/', function () {
    //
});
```

> [!TIP]
> 동일한 URI에 여러 라우트를 정의할 때, `get`, `post`, `put`, `patch`, `delete`, `options` 메서드를 사용하는 라우트를 `any`, `match`, `redirect` 메서드를 사용하는 라우트보다 먼저 정의해야 올바른 라우트에 요청이 매칭됩니다.

<a name="dependency-injection"></a>
<!-- #### Dependency Injection -->
#### Dependency Injection

<!-- You may type-hint any dependencies required by your route in your route's callback signature. The declared dependencies will automatically be resolved and injected into the callback by the Laravel [service container](/docs/8.x/container). For example, you may type-hint the `Illuminate\Http\Request` class to have the current HTTP request automatically injected into your route callback: -->
라우트의 콜백 시그니처에서 필요한 의존성(디펜던시)을 타입힌트로 지정하면, Laravel [service container](/docs/8.x/container)가 자동으로 해당 의존성을 해결하여 콜백에 주입합니다. 예를 들어, `Illuminate\Http\Request` 클래스를 타입힌트로 지정하면 현재 HTTP 요청 객체가 자동으로 라우트 콜백에 주입됩니다.

```
use Illuminate\Http\Request;

Route::get('/users', function (Request $request) {
    // ...
});
```

<a name="csrf-protection"></a>
<!-- #### CSRF Protection -->
#### CSRF Protection

<!-- Remember, any HTML forms pointing to `POST`, `PUT`, `PATCH`, or `DELETE` routes that are defined in the `web` routes file should include a CSRF token field. Otherwise, the request will be rejected. You can read more about CSRF protection in the [CSRF documentation](/docs/8.x/csrf): -->
`web` 라우트 파일에 정의된 `POST`, `PUT`, `PATCH`, `DELETE` 방식의 라우트로 동작하는 모든 HTML 양식에는 반드시 CSRF 토큰 필드를 포함해야 하며, 그렇지 않으면 요청이 거부됩니다. CSRF 보호에 대한 자세한 내용은 [CSRF documentation](/docs/8.x/csrf)에서 확인할 수 있습니다.

```
<form method="POST" action="/profile">
    @csrf
    ...
</form>
```

<a name="redirect-routes"></a>
<!-- ### Redirect Routes -->
### Redirect Routes

<!-- If you are defining a route that redirects to another URI, you may use the `Route::redirect` method. This method provides a convenient shortcut so that you do not have to define a full route or controller for performing a simple redirect: -->
다른 URI로 리디렉션하는 라우트를 정의하려면 `Route::redirect` 메서드를 사용할 수 있습니다. 이 메서드는 단순한 리디렉션을 위해 전체 라우트나 컨트롤러를 별도로 정의하지 않아도 되는 간편한 방법입니다.

```
Route::redirect('/here', '/there');
```

<!-- By default, `Route::redirect` returns a `302` status code. You may customize the status code using the optional third parameter: -->
`Route::redirect`는 기본적으로 `302` 상태 코드를 반환합니다. 세 번째 매개변수로 상태 코드를 직접 지정할 수도 있습니다.

```
Route::redirect('/here', '/there', 301);
```

<!-- Or, you may use the `Route::permanentRedirect` method to return a `301` status code: -->
또는, `Route::permanentRedirect` 메서드를 사용하면 항상 `301` 상태 코드를 반환하도록 할 수 있습니다.

```
Route::permanentRedirect('/here', '/there');
```

> [!NOTE]
> 리디렉션 라우트에서 라우트 파라미터를 사용할 때, `destination`과 `status`라는 파라미터 이름은 Laravel에서 예약되어 있어 사용할 수 없습니다.

<a name="view-routes"></a>
<!-- ### View Routes -->
### View Routes

<!-- If your route only needs to return a [view](/docs/8.x/views), you may use the `Route::view` method. Like the `redirect` method, this method provides a simple shortcut so that you do not have to define a full route or controller. The `view` method accepts a URI as its first argument and a view name as its second argument. In addition, you may provide an array of data to pass to the view as an optional third argument: -->
라우트에서 단순히 [view](/docs/8.x/views)를 반환하면 되는 경우, `Route::view` 메서드를 사용할 수 있습니다. `redirect` 메서드처럼 이 메서드는 전체 라우트나 컨트롤러를 정의하지 않고도 간단하게 뷰를 반환할 수 있도록 해줍니다. 첫 번째 인자는 URI, 두 번째 인자는 `view` 이름이며, 세 번째(선택) 인자로 뷰에 전달할 데이터를 배열로 넘길 수 있습니다.

```
Route::view('/welcome', 'welcome');

Route::view('/welcome', 'welcome', ['name' => 'Taylor']);
```

> [!NOTE]
> 뷰 라우트에서 파라미터를 사용할 경우, `view`, `data`, `status`, `headers`라는 파라미터 이름은 Laravel에서 예약되어 있어 사용할 수 없습니다.

<a name="route-parameters"></a>
<!-- ## Route Parameters -->
## Route Parameters

<a name="required-parameters"></a>
<!-- ### Required Parameters -->
### Required Parameters

<!-- Sometimes you will need to capture segments of the URI within your route. For example, you may need to capture a user's ID from the URL. You may do so by defining route parameters: -->
때로는 URI의 일부 세그먼트를 라우팅에서 받아와야 할 때가 있습니다. 예를 들어, URL에서 사용자의 ID를 받아와야 한다면 아래와 같이 라우트 파라미터를 정의할 수 있습니다.

```
Route::get('/user/{id}', function ($id) {
    return 'User '.$id;
});
```

<!-- You may define as many route parameters as required by your route: -->
라우트에서는 필요한 만큼 파라미터를 정의할 수 있습니다.

```
Route::get('/posts/{post}/comments/{comment}', function ($postId, $commentId) {
    //
});
```

<!-- Route parameters are always encased within `{}` braces and should consist of alphabetic characters. Underscores (`_`) are also acceptable within route parameter names. Route parameters are injected into route callbacks / controllers based on their order - the names of the route callback / controller arguments do not matter. -->
라우트 파라미터는 항상 `{}` 중괄호로 감싸며, 알파벳 문자로 구성하는 것이 좋습니다. 파라미터 이름에 밑줄(`_`)도 사용할 수 있습니다. 라우트 콜백/컨트롤러에 파라미터가 주입되는 순서는 정의된 라우트 파라미터의 순서에 따릅니다. 파라미터 변수명은 일치하지 않아도 순서대로 주입됩니다.

<a name="parameters-and-dependency-injection"></a>
<!-- #### Parameters & Dependency Injection -->
#### Parameters & Dependency Injection

<!-- If your route has dependencies that you would like the Laravel service container to automatically inject into your route's callback, you should list your route parameters after your dependencies: -->
라우트에서 서비스 컨테이너로 자동 의존성 주입이 필요한 경우, 라우트 파라미터는 의존성 뒤에 나열해야 합니다.

```
use Illuminate\Http\Request;

Route::get('/user/{id}', function (Request $request, $id) {
    return 'User '.$id;
});
```

<a name="parameters-optional-parameters"></a>
<!-- ### Optional Parameters -->
### Optional Parameters

<!-- Occasionally you may need to specify a route parameter that may not always be present in the URI. You may do so by placing a `?` mark after the parameter name. Make sure to give the route's corresponding variable a default value: -->
때로는 라우트 파라미터가 항상 URI에 존재하지 않도록 하고 싶을 수 있습니다. 이럴 때는 파라미터 이름 뒤에 `?`를 붙이면 됩니다. 또한, 해당 변수를 받는 인자에 기본값을 지정해야 합니다.

```
Route::get('/user/{name?}', function ($name = null) {
    return $name;
});

Route::get('/user/{name?}', function ($name = 'John') {
    return $name;
});
```

<a name="parameters-regular-expression-constraints"></a>
<!-- ### Regular Expression Constraints -->
### Regular Expression Constraints

<!-- You may constrain the format of your route parameters using the `where` method on a route instance. The `where` method accepts the name of the parameter and a regular expression defining how the parameter should be constrained: -->
라우트 인스턴스의 `where` 메서드를 이용해서 라우트 파라미터의 형식을 정규식으로 제한할 수 있습니다. 이 `where` 메서드는 파라미터 이름과, 파라미터를 제한할 정규식을 인자로 받습니다.

```
Route::get('/user/{name}', function ($name) {
    //
})->where('name', '[A-Za-z]+');

Route::get('/user/{id}', function ($id) {
    //
})->where('id', '[0-9]+');

Route::get('/user/{id}/{name}', function ($id, $name) {
    //
})->where(['id' => '[0-9]+', 'name' => '[a-z]+']);
```

<!-- For convenience, some commonly used regular expression patterns have helper methods that allow you to quickly add pattern constraints to your routes: -->
자주 쓰이는 정규식 패턴을 위해 라우트에는 여러 헬퍼 메서드가 제공되어, 패턴 제약을 쉽고 빠르게 추가할 수 있습니다.

```
Route::get('/user/{id}/{name}', function ($id, $name) {
    //
})->whereNumber('id')->whereAlpha('name');

Route::get('/user/{name}', function ($name) {
    //
})->whereAlphaNumeric('name');

Route::get('/user/{id}', function ($id) {
    //
})->whereUuid('id');
```

<!-- If the incoming request does not match the route pattern constraints, a 404 HTTP response will be returned. -->
요청이 라우트 패턴 제약조건에 일치하지 않는 경우, 404 HTTP 응답이 반환됩니다.

<a name="parameters-global-constraints"></a>
<!-- #### Global Constraints -->
#### Global Constraints

<!-- If you would like a route parameter to always be constrained by a given regular expression, you may use the `pattern` method. You should define these patterns in the `boot` method of your `App\Providers\RouteServiceProvider` class: -->
특정 라우트 파라미터에 항상 같은 정규식 제약조건을 적용하고 싶다면, `pattern` 메서드를 사용할 수 있습니다. 이 패턴은 `App\Providers\RouteServiceProvider` 클래스의 `boot` 메서드에서 정의해야 합니다.

```
/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::pattern('id', '[0-9]+');
}
```

<!-- Once the pattern has been defined, it is automatically applied to all routes using that parameter name: -->
이렇게 패턴을 지정하면, 해당 파라미터 이름이 사용되는 모든 라우트에 자동으로 적용됩니다.

```
Route::get('/user/{id}', function ($id) {
    // Only executed if {id} is numeric...
});
```

<a name="parameters-encoded-forward-slashes"></a>
<!-- #### Encoded Forward Slashes -->
#### Encoded Forward Slashes

<!-- The Laravel routing component allows all characters except `/` to be present within route parameter values. You must explicitly allow `/` to be part of your placeholder using a `where` condition regular expression: -->
Laravel 라우팅 컴포넌트는 라우트 파라미터 값으로 `/`를 제외한 모든 문자를 허용합니다. 만약 슬래시(`/`)도 파라미터 값에 포함하고 싶다면, `where` 정규식 조건에서 명시적으로 허용해줘야 합니다.

```
Route::get('/search/{search}', function ($search) {
    return $search;
})->where('search', '.*');
```

> [!NOTE]
> 인코딩된 슬래시는 오직 마지막 라우트 세그먼트에서만 지원됩니다.

<a name="named-routes"></a>
<!-- ## Named Routes -->
## Named Routes

<!-- Named routes allow the convenient generation of URLs or redirects for specific routes. You may specify a name for a route by chaining the `name` method onto the route definition: -->
네임드 라우트를 사용하면 특정 라우트에 대해 URL을 생성하거나 리디렉션하는 작업을 편리하게 할 수 있습니다. 라우트 정의에 `name` 메서드를 체이닝하여 라우트에 이름을 지정할 수 있습니다.

```
Route::get('/user/profile', function () {
    //
})->name('profile');
```

<!-- You may also specify route names for controller actions: -->
컨트롤러 액션에도 라우트 이름을 지정할 수 있습니다.

```
Route::get(
    '/user/profile',
    [UserProfileController::class, 'show']
)->name('profile');
```

> [!NOTE]
> 라우트 이름은 반드시 고유해야 합니다.

<a name="generating-urls-to-named-routes"></a>
<!-- #### Generating URLs To Named Routes -->
#### Generating URLs To Named Routes

<!-- Once you have assigned a name to a given route, you may use the route's name when generating URLs or redirects via Laravel's `route` and `redirect` helper functions: -->
특정 라우트에 이름을 지정한 뒤에는 `route` 및 `redirect` 헬퍼 함수를 통해 해당 라우트의 이름으로 URL 생성이나 리디렉션이 가능합니다.

```
// Generating URLs...
$url = route('profile');

// Generating Redirects...
return redirect()->route('profile');
```

<!-- If the named route defines parameters, you may pass the parameters as the second argument to the `route` function. The given parameters will automatically be inserted into the generated URL in their correct positions: -->
네임드 라우트에 파라미터가 있다면, `route` 함수의 두 번째 인자로 파라미터 배열을 넘기면 지정한 위치에 값이 자동으로 삽입되어 URL이 생성됩니다.

```
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1]);
```

<!-- If you pass additional parameters in the array, those key / value pairs will automatically be added to the generated URL's query string: -->
파라미터 배열에 추가로 더 많은 값을 전달하면, 이 값들은 자동으로 URL의 쿼리 스트링 형태로 추가됩니다.

```
Route::get('/user/{id}/profile', function ($id) {
    //
})->name('profile');

$url = route('profile', ['id' => 1, 'photos' => 'yes']);

// /user/1/profile?photos=yes
```

> [!TIP]
> 요청 전체에 대해 URL 파라미터의 기본값(예: 현재 로케일 등)을 지정하고 싶을 때는 [`URL::defaults` method](/docs/8.x/urls#default-values)를 사용할 수 있습니다.

<a name="inspecting-the-current-route"></a>
<!-- #### Inspecting The Current Route -->
#### Inspecting The Current Route

<!-- If you would like to determine if the current request was routed to a given named route, you may use the `named` method on a Route instance. For example, you may check the current route name from a route middleware: -->
현재 요청이 특정 네임드 라우트로 매칭됐는지 확인하려면, Route 인스턴스의 `named` 메서드를 사용할 수 있습니다. 예를 들어, 라우트 미들웨어 내에서 현재 라우트 이름을 체크할 수 있습니다.

```
/**
 * Handle an incoming request.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  \Closure  $next
 * @return mixed
 */
public function handle($request, Closure $next)
{
    if ($request->route()->named('profile')) {
        //
    }

    return $next($request);
}
```

<a name="route-groups"></a>
<!-- ## Route Groups -->
## Route Groups

<!-- Route groups allow you to share route attributes, such as middleware, across a large number of routes without needing to define those attributes on each individual route. -->
라우트 그룹을 사용하면 여러 라우트에 대해 미들웨어와 같은 라우트 속성을 개별적으로 반복해서 지정하지 않고, 그룹 단위로 한번에 공유할 수 있습니다.

<!-- Nested groups attempt to intelligently "merge" attributes with their parent group. Middleware and `where` conditions are merged while names and prefixes are appended. Namespace delimiters and slashes in URI prefixes are automatically added where appropriate. -->
중첩된 그룹은 상위 그룹의 속성을 자동으로 '병합'하여 적용합니다. 미들웨어 및 `where` 조건은 병합되고, 이름(name)과 프리픽스(prefix)는 덧붙여집니다. 네임스페이스 구분자와 URI 프리픽스의 슬래시는 적절하게 자동 추가됩니다.

<a name="route-group-middleware"></a>
<!-- ### Middleware -->
### Middleware

<!-- To assign [middleware](/docs/8.x/middleware) to all routes within a group, you may use the `middleware` method before defining the group. Middleware are executed in the order they are listed in the array: -->
라우트 그룹 내의 모든 라우트에 [middleware](/docs/8.x/middleware)를 적용하려면, 그룹 정의 전에 `middleware` 메서드를 사용하면 됩니다. 배열에 나열하는 순서대로 미들웨어가 실행됩니다.

```
Route::middleware(['first', 'second'])->group(function () {
    Route::get('/', function () {
        // Uses first & second middleware...
    });

    Route::get('/user/profile', function () {
        // Uses first & second middleware...
    });
});
```

<a name="route-group-controllers"></a>
<!-- ### Controllers -->
### Controllers

<!-- If a group of routes all utilize the same [controller](/docs/8.x/controllers), you may use the `controller` method to define the common controller for all of the routes within the group. Then, when defining the routes, you only need to provide the controller method that they invoke: -->
여러 라우트가 동일한 [controller](/docs/8.x/controllers)를 사용할 때는, `controller` 메서드를 사용하여 그룹 내 전체 라우트에 공통 컨트롤러를 지정할 수 있습니다. 이후 각각의 라우트 정의에서는 호출할 컨트롤러 메서드명만 적어주면 됩니다.

```
use App\Http\Controllers\OrderController;

Route::controller(OrderController::class)->group(function () {
    Route::get('/orders/{id}', 'show');
    Route::post('/orders', 'store');
});
```

<a name="route-group-subdomain-routing"></a>
<!-- ### Subdomain Routing -->
### Subdomain Routing

<!-- Route groups may also be used to handle subdomain routing. Subdomains may be assigned route parameters just like route URIs, allowing you to capture a portion of the subdomain for usage in your route or controller. The subdomain may be specified by calling the `domain` method before defining the group: -->
라우트 그룹은 서브도메인 라우팅에도 사용할 수 있습니다. 서브도메인에도 라우트 파라미터를 지정할 수 있어, 서브도메인의 일부를 라우트나 컨트롤러에서 사용할 수 있습니다. `domain` 메서드를 이용해 그룹 정의 전에 서브도메인을 설정합니다.

```
Route::domain('{account}.example.com')->group(function () {
    Route::get('user/{id}', function ($account, $id) {
        //
    });
});
```

> [!NOTE]
> 서브도메인 라우트가 올바르게 동작하려면, 반드시 루트 도메인 라우트보다 먼저 서브도메인 라우트를 등록해야 합니다. 그래야 루트 도메인 라우트가 같은 URI 경로를 가진 서브도메인 라우트를 덮어쓰지 않습니다.

<a name="route-group-prefixes"></a>
<!-- ### Route Prefixes -->
### Route Prefixes

<!-- The `prefix` method may be used to prefix each route in the group with a given URI. For example, you may want to prefix all route URIs within the group with `admin`: -->
`prefix` 메서드를 사용하면, 그룹 내의 모든 라우트 URI 앞에 특정 문자열 프리픽스를 붙일 수 있습니다. 예를 들어, 모든 그룹 내 라우트의 URI를 `admin`으로 시작하도록 할 수 있습니다.

```
Route::prefix('admin')->group(function () {
    Route::get('/users', function () {
        // Matches The "/admin/users" URL
    });
});
```

<a name="route-group-name-prefixes"></a>
<!-- ### Route Name Prefixes -->
### Route Name Prefixes

<!-- The `name` method may be used to prefix each route name in the group with a given string. For example, you may want to prefix all of the grouped route's names with `admin`. The given string is prefixed to the route name exactly as it is specified, so we will be sure to provide the trailing `.` character in the prefix: -->
`name` 메서드를 사용하면, 그룹 내 모든 라우트 이름에 지정한 문자열을 프리픽스로 붙일 수 있습니다. 예시에서는 그룹의 모든 라우트 이름에 `admin`을 붙입니다. 반드시 접미사로 `.`(점)을 붙여야 원하는 결과를 얻을 수 있습니다.

```
Route::name('admin.')->group(function () {
    Route::get('/users', function () {
        // Route assigned name "admin.users"...
    })->name('users');
});
```

<a name="route-model-binding"></a>
<!-- ## Route Model Binding -->
## Route Model Binding

<!-- When injecting a model ID to a route or controller action, you will often query the database to retrieve the model that corresponds to that ID. Laravel route model binding provides a convenient way to automatically inject the model instances directly into your routes. For example, instead of injecting a user's ID, you can inject the entire `User` model instance that matches the given ID. -->
모델 ID를 라우트나 컨트롤러 액션에 주입하는 경우, 일반적으로 해당 ID로 데이터베이스에서 모델을 조회해야 합니다. Laravel의 라우트 모델 바인딩을 사용하면, 모델 인스턴스를 자동으로 라우트에 주입할 수 있어 편리합니다. 예를 들어, 사용자의 ID를 주입하는 대신 해당 ID와 일치하는 전체 `User` 모델 인스턴스를 자동으로 받아올 수 있습니다.

<a name="implicit-binding"></a>
<!-- ### Implicit Binding -->
### Implicit Binding

<!-- Laravel automatically resolves Eloquent models defined in routes or controller actions whose type-hinted variable names match a route segment name. For example: -->
라우트나 컨트롤러 액션의 파라미터가 Eloquent 모델로 타입힌트되어 있고, 변수명과 라우트 세그먼트가 일치하면 Laravel이 자동으로 Eloquent 모델을 주입합니다. 예를 들어:

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
});
```

<!-- Since the `$user` variable is type-hinted as the `App\Models\User` Eloquent model and the variable name matches the `{user}` URI segment, Laravel will automatically inject the model instance that has an ID matching the corresponding value from the request URI. If a matching model instance is not found in the database, a 404 HTTP response will automatically be generated. -->
위와 같이 `$user` 변수가 `App\Models\User` 모델로 타입힌트되어 있고, 변수명과 `{user}` 세그먼트가 일치하면 Laravel은 해당 ID와 일치하는 모델 인스턴스를 자동으로 라우트에 주입합니다. 데이터베이스에서 일치하는 모델 인스턴스를 찾지 못하면 자동으로 404 HTTP 응답이 반환됩니다.

<!-- Of course, implicit binding is also possible when using controller methods. Again, note the `{user}` URI segment matches the `$user` variable in the controller which contains an `App\Models\User` type-hint: -->
암묵적 바인딩은 컨트롤러 메서드에서도 동일하게 동작합니다. 마찬가지로 `{user}` 세그먼트와 컨트롤러의 `$user` 파라미터가 일치하며, 이 파라미터에는 `App\Models\User` 타입힌트가 지정됩니다.

```
use App\Http\Controllers\UserController;
use App\Models\User;

// Route definition...
Route::get('/users/{user}', [UserController::class, 'show']);

// Controller method definition...
public function show(User $user)
{
    return view('user.profile', ['user' => $user]);
}
```

<a name="implicit-soft-deleted-models"></a>
<!-- #### Soft Deleted Models -->
#### Soft Deleted Models

<!-- Typically, implicit model binding will not retrieve models that have been [soft deleted](/docs/8.x/eloquent#soft-deleting). However, you may instruct the implicit binding to retrieve these models by chaining the `withTrashed` method onto your route's definition: -->
기본적으로 암묵적 모델 바인딩은 [soft deleted](/docs/8.x/eloquent#soft-deleting)된 모델을 조회하지 않습니다. 하지만 라우트 정의에 `withTrashed` 메서드를 체이닝하면 소프트 삭제된 모델도 함께 조회할 수 있습니다.

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    return $user->email;
})->withTrashed();
```

<a name="customizing-the-default-key-name"></a>
<!-- #### Customizing The Key -->
#### Customizing The Key

<!-- Sometimes you may wish to resolve Eloquent models using a column other than `id`. To do so, you may specify the column in the route parameter definition: -->
때로는 Eloquent 모델을 조회할 때 `id`가 아닌 다른 컬럼으로 조회하고 싶을 수 있습니다. 이럴 때, 라우트 파라미터 정의에 컬럼명을 명시할 수 있습니다.

```
use App\Models\Post;

Route::get('/posts/{post:slug}', function (Post $post) {
    return $post;
});
```

<!-- If you would like model binding to always use a database column other than `id` when retrieving a given model class, you may override the `getRouteKeyName` method on the Eloquent model: -->
특정 모델 클래스에 대해 항상 특정 컬럼을 바인딩 키로 사용하려면, Eloquent 모델에서 `getRouteKeyName` 메서드를 오버라이드하면 됩니다.

```
/**
 * Get the route key for the model.
 *
 * @return string
 */
public function getRouteKeyName()
{
    return 'slug';
}
```

<a name="implicit-model-binding-scoping"></a>
<!-- #### Custom Keys & Scoping -->
#### Custom Keys & Scoping

<!-- When implicitly binding multiple Eloquent models in a single route definition, you may wish to scope the second Eloquent model such that it must be a child of the previous Eloquent model. For example, consider this route definition that retrieves a blog post by slug for a specific user: -->
하나의 라우트에서 여러 Eloquent 모델을 암묵적으로 바인딩할 때, 두 번째 모델이 반드시 첫 번째 모델의 자식이어야 하는 상황이 있을 수 있습니다. 예를 들어, 특정 사용자의 게시글을 슬러그로 조회하는 아래의 라우트 정의를 보겠습니다.

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post:slug}', function (User $user, Post $post) {
    return $post;
});
```

<!-- When using a custom keyed implicit binding as a nested route parameter, Laravel will automatically scope the query to retrieve the nested model by its parent using conventions to guess the relationship name on the parent. In this case, it will be assumed that the `User` model has a relationship named `posts` (the plural form of the route parameter name) which can be used to retrieve the `Post` model. -->
이처럼 커스텀 키를 사용하는 중첩 바인딩의 경우, Laravel은 두 번째 모델을 자동으로 첫 번째(상위) 모델의 자식 관계로 스코프해 쿼리를 수행합니다. 이때 `User` 모델에 `posts`라는(라우트 파라미터 복수형) 관계가 정의되어 있고 이를 통해 `Post` 모델을 조회한다고 가정합니다.

<!-- If you wish, you may instruct Laravel to scope "child" bindings even when a custom key is not provided. To do so, you may invoke the `scopeBindings` method when defining your route: -->
커스텀 키가 없어도(기본 `id` 사용) 자식 모델 바인딩의 스코프 적용을 원한다면, 라우트 정의 시 `scopeBindings` 메서드를 체이닝하세요.

```
use App\Models\Post;
use App\Models\User;

Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
    return $post;
})->scopeBindings();
```

<!-- Or, you may instruct an entire group of route definitions to use scoped bindings: -->
여러 라우트를 그룹으로 묶어 모두 스코프 바인딩을 적용할 수도 있습니다.

```
Route::scopeBindings()->group(function () {
    Route::get('/users/{user}/posts/{post}', function (User $user, Post $post) {
        return $post;
    });
});
```

<a name="customizing-missing-model-behavior"></a>
<!-- #### Customizing Missing Model Behavior -->
#### Customizing Missing Model Behavior

<!-- Typically, a 404 HTTP response will be generated if an implicitly bound model is not found. However, you may customize this behavior by calling the `missing` method when defining your route. The `missing` method accepts a closure that will be invoked if an implicitly bound model can not be found: -->
기본적으로 암묵적 바인딩에서 모델을 찾지 못하면 404 HTTP 응답이 반환됩니다. 하지만 라우트 정의 시 `missing` 메서드를 통해 커스텀 동작을 지정할 수 있습니다. `missing` 메서드에는 콜백을 지정할 수 있고, 모델을 찾지 못했을 때 이 콜백이 실행됩니다.

```
use App\Http\Controllers\LocationsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::get('/locations/{location:slug}', [LocationsController::class, 'show'])
        ->name('locations.view')
        ->missing(function (Request $request) {
            return Redirect::route('locations.index');
        });
```

<a name="explicit-binding"></a>
<!-- ### Explicit Binding -->
### Explicit Binding

<!-- You are not required to use Laravel's implicit, convention based model resolution in order to use model binding. You can also explicitly define how route parameters correspond to models. To register an explicit binding, use the router's `model` method to specify the class for a given parameter. You should define your explicit model bindings at the beginning of the `boot` method of your `RouteServiceProvider` class: -->
암묵적(관례 기반) 모델 바인딩 대신, 어떻게 라우트 파라미터가 모델과 매핑될지 직접 명시할 수도 있습니다. 명시적 바인딩은 라우터의 `model` 메서드를 사용하며, 특정 파라미터에 대한 클래스를 지정합니다. 보통 `RouteServiceProvider`의 `boot` 메서드 시작 부분에 바인딩을 등록합니다.

```
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::model('user', User::class);

    // ...
}
```

<!-- Next, define a route that contains a `{user}` parameter: -->
이후 `{user}` 파라미터를 포함하는 라우트를 정의할 수 있습니다.

```
use App\Models\User;

Route::get('/users/{user}', function (User $user) {
    //
});
```

<!-- Since we have bound all `{user}` parameters to the `App\Models\User` model, an instance of that class will be injected into the route. So, for example, a request to `users/1` will inject the `User` instance from the database which has an ID of `1`. -->
모든 `{user}` 파라미터를 `App\Models\User` 모델에 바인딩했으므로, `users/1` 요청 시 데이터베이스에서 ID가 `1`인 `User` 인스턴스가 주입됩니다.

<!-- If a matching model instance is not found in the database, a 404 HTTP response will be automatically generated. -->
일치하는 모델을 찾지 못하면, 자동으로 404 응답이 반환됩니다.

<a name="customizing-the-resolution-logic"></a>
<!-- #### Customizing The Resolution Logic -->
#### Customizing The Resolution Logic

<!-- If you wish to define your own model binding resolution logic, you may use the `Route::bind` method. The closure you pass to the `bind` method will receive the value of the URI segment and should return the instance of the class that should be injected into the route. Again, this customization should take place in the `boot` method of your application's `RouteServiceProvider`: -->
직접 바인딩 인스턴스 조회 로직을 정의하고 싶다면, `Route::bind` 메서드를 사용할 수 있습니다. `bind` 메서드에 전달하는 클로저는 URI 세그먼트 값을 받아, 라우트에 주입할 인스턴스를 반환하면 됩니다. 역시 애플리케이션의 `RouteServiceProvider`의 `boot` 메서드에서 정의하세요.

```
use App\Models\User;
use Illuminate\Support\Facades\Route;

/**
 * Define your route model bindings, pattern filters, etc.
 *
 * @return void
 */
public function boot()
{
    Route::bind('user', function ($value) {
        return User::where('name', $value)->firstOrFail();
    });

    // ...
}
```

<!-- Alternatively, you may override the `resolveRouteBinding` method on your Eloquent model. This method will receive the value of the URI segment and should return the instance of the class that should be injected into the route: -->
또는, Eloquent 모델에 `resolveRouteBinding` 메서드를 오버라이드하여 모델 내에서 바인딩 인스턴스 조회 로직을 정의할 수도 있습니다.

```
/**
 * Retrieve the model for a bound value.
 *
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveRouteBinding($value, $field = null)
{
    return $this->where('name', $value)->firstOrFail();
}
```

<!-- If a route is utilizing [implicit binding scoping](#implicit-model-binding-scoping), the `resolveChildRouteBinding` method will be used to resolve the child binding of the parent model: -->
[implicit binding scoping](#implicit-model-binding-scoping)가 적용되는 라우트의 경우, `resolveChildRouteBinding` 메서드가 호출되어 자식 모델 바인딩이 처리됩니다.

```
/**
 * Retrieve the child model for a bound value.
 *
 * @param  string  $childType
 * @param  mixed  $value
 * @param  string|null  $field
 * @return \Illuminate\Database\Eloquent\Model|null
 */
public function resolveChildRouteBinding($childType, $value, $field)
{
    return parent::resolveChildRouteBinding($childType, $value, $field);
}
```

<a name="fallback-routes"></a>
<!-- ## Fallback Routes -->
## Fallback Routes

<!-- Using the `Route::fallback` method, you may define a route that will be executed when no other route matches the incoming request. Typically, unhandled requests will automatically render a "404" page via your application's exception handler. However, since you would typically define the `fallback` route within your `routes/web.php` file, all middleware in the `web` middleware group will apply to the route. You are free to add additional middleware to this route as needed: -->
`Route::fallback` 메서드를 사용하면, 다른 어떤 라우트와도 매칭되지 않을 때 실행되는 라우트를 정의할 수 있습니다. 처리되지 않은 요청은 기본적으로 예외 핸들러에 의해 "404" 페이지가 렌더링됩니다. 하지만 일반적으로 `routes/web.php`에 `fallback` 라우트를 정의하므로, 이 라우트에도 `web` 미들웨어 그룹의 모든 미들웨어가 적용됩니다. 필요한 경우 이 라우트에 추가 미들웨어도 자유롭게 지정할 수 있습니다.

```
Route::fallback(function () {
    //
});
```

> [!NOTE]
> 폴백 라우트는 반드시 애플리케이션의 마지막 라우트로 등록해야 합니다.

<a name="rate-limiting"></a>
<!-- ## Rate Limiting -->
## Rate Limiting

<a name="defining-rate-limiters"></a>
<!-- ### Defining Rate Limiters -->
### Defining Rate Limiters

<!-- Laravel includes powerful and customizable rate limiting services that you may utilize to restrict the amount of traffic for a given route or group of routes. To get started, you should define rate limiter configurations that meet your application's needs. Typically, this should be done within the `configureRateLimiting` method of your application's `App\Providers\RouteServiceProvider` class. -->
Laravel은 특정 라우트나 라우트 그룹에 대해 트래픽을 제한할 수 있는 강력하고 유연한 요청 제한 기능을 제공합니다. 먼저, 애플리케이션에 필요한 요청 제한자 설정을 정의해야 합니다. 주로 `App\Providers\RouteServiceProvider` 클래스의 `configureRateLimiting` 메서드 내에서 정의합니다.

<!-- Rate limiters are defined using the `RateLimiter` facade's `for` method. The `for` method accepts a rate limiter name and a closure that returns the limit configuration that should apply to routes that are assigned to the rate limiter. Limit configuration are instances of the `Illuminate\Cache\RateLimiting\Limit` class. This class contains helpful "builder" methods so that you can quickly define your limit. The rate limiter name may be any string you wish: -->
요청 제한자는 `RateLimiter` 파사드의 `for` 메서드를 사용하여 정의합니다. `for` 메서드는 제한자 이름과, 제한 설정을 반환하는 클로저를 인자로 받습니다. 제한 설정은 `Illuminate\Cache\RateLimiting\Limit` 클래스의 인스턴스여야 하며, 이 클래스에는 요청 제한을 빠르게 정의할 수 있는 다양한 빌더 메서드가 포함되어 있습니다. 제한자 이름은 원하는 아무 문자열이나 쓸 수 있습니다.

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Configure the rate limiters for the application.
 *
 * @return void
 */
protected function configureRateLimiting()
{
    RateLimiter::for('global', function (Request $request) {
        return Limit::perMinute(1000);
    });
}
```

<!-- If the incoming request exceeds the specified rate limit, a response with a 429 HTTP status code will automatically be returned by Laravel. If you would like to define your own response that should be returned by a rate limit, you may use the `response` method: -->
요청이 지정한 제한을 초과하면, Laravel은 자동으로 429 HTTP 상태 코드로 응답합니다. 요청 제한을 초과했을 때 반환되는 응답을 직접 정의하고 싶을 때는 `response` 메서드를 사용할 수 있습니다.

```
RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000)->response(function () {
        return response('Custom response...', 429);
    });
});
```

<!-- Since rate limiter callbacks receive the incoming HTTP request instance, you may build the appropriate rate limit dynamically based on the incoming request or authenticated user: -->
요청 제한자 클로저 안에서는 들어온 HTTP 요청 인스턴스를 받기 때문에, 요청이나 인증 사용자에 따라 동적으로 제한을 구성할 수도 있습니다.

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<a name="segmenting-rate-limits"></a>
<!-- #### Segmenting Rate Limits -->
#### Segmenting Rate Limits

<!-- Sometimes you may wish to segment rate limits by some arbitrary value. For example, you may wish to allow users to access a given route 100 times per minute per IP address. To accomplish this, you may use the `by` method when building your rate limit: -->
특정한 기준에 따라 요청 제한을 분리해서 적용하고 싶을 때가 있습니다. 예를 들어, 한 IP 주소당 1분에 100회씩 라우트에 접근하도록 제한하려면, 제한 빌더에서 `by` 메서드를 사용할 수 있습니다.

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

<!-- To illustrate this feature using another example, we can limit access to the route to 100 times per minute per authenticated user ID or 10 times per minute per IP address for guests: -->
또 다른 예시로, 인증된 사용자는 1분에 100회, 비회원(게스트)은 IP별로 1분에 10회만 접근하도록 제한할 수도 있습니다.

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()
                ? Limit::perMinute(100)->by($request->user()->id)
                : Limit::perMinute(10)->by($request->ip());
});
```

<a name="multiple-rate-limits"></a>
<!-- #### Multiple Rate Limits -->
#### Multiple Rate Limits

<!-- If needed, you may return an array of rate limits for a given rate limiter configuration. Each rate limit will be evaluated for the route based on the order they are placed within the array: -->
필요하다면, 하나의 제한자 설정에서 여러 개의 요청 제한을 배열로 반환할 수 있습니다. 배열에 나열된 순서대로 각 제한이 적용됩니다.

```
RateLimiter::for('login', function (Request $request) {
    return [
        Limit::perMinute(500),
        Limit::perMinute(3)->by($request->input('email')),
    ];
});
```

<a name="attaching-rate-limiters-to-routes"></a>
<!-- ### Attaching Rate Limiters To Routes -->
### Attaching Rate Limiters To Routes

<!-- Rate limiters may be attached to routes or route groups using the `throttle` [middleware](/docs/8.x/middleware). The throttle middleware accepts the name of the rate limiter you wish to assign to the route: -->
요청 제한자는 `throttle` [middleware](/docs/8.x/middleware)로 라우트 또는 라우트 그룹에 적용할 수 있습니다. 미들웨어에 제한자 이름을 지정하면 해당 제한이 적용됩니다.

```
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        //
    });

    Route::post('/video', function () {
        //
    });
});
```

<a name="throttling-with-redis"></a>
<!-- #### Throttling With Redis -->
#### Throttling With Redis

<!-- Typically, the `throttle` middleware is mapped to the `Illuminate\Routing\Middleware\ThrottleRequests` class. This mapping is defined in your application's HTTP kernel (`App\Http\Kernel`). However, if you are using Redis as your application's cache driver, you may wish to change this mapping to use the `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` class. This class is more efficient at managing rate limiting using Redis: -->
일반적으로 `throttle` 미들웨어는 `Illuminate\Routing\Middleware\ThrottleRequests` 클래스에 매핑되어 있습니다. 이 매핑은 애플리케이션의 HTTP 커널(`App\Http\Kernel`)에서 정의됩니다. 하지만 애플리케이션의 캐시 드라이버로 Redis를 사용한다면, 더 효율적인 제한 관리를 위해 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` 클래스로 매핑을 변경할 수 있습니다.

```
'throttle' => \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
```

<a name="form-method-spoofing"></a>
<!-- ## Form Method Spoofing -->
## Form Method Spoofing

<!-- HTML forms do not support `PUT`, `PATCH`, or `DELETE` actions. So, when defining `PUT`, `PATCH`, or `DELETE` routes that are called from an HTML form, you will need to add a hidden `_method` field to the form. The value sent with the `_method` field will be used as the HTTP request method: -->
HTML 폼은 `PUT`, `PATCH`, `DELETE` 메서드를 지원하지 않습니다. 따라서 폼에서 `PUT`, `PATCH`, `DELETE` 라우트로 요청하려면, 숨겨진 `_method` 필드를 추가해야 합니다. 이 `_method` 필드에 전달된 값이 HTTP 요청 메서드로 사용됩니다.

```
<form action="/example" method="POST">
    <input type="hidden" name="_method" value="PUT">
    <input type="hidden" name="_token" value="{{ csrf_token() }}">
</form>
```

<!-- For convenience, you may use the `@method` [Blade directive](/docs/8.x/blade) to generate the `_method` input field: -->
더 간편하게, [Blade directive](/docs/8.x/blade)인 `@method`를 이용해 `_method` 필드를 생성할 수 있습니다.

```
<form action="/example" method="POST">
    @method('PUT')
    @csrf
</form>
```

<a name="accessing-the-current-route"></a>
<!-- ## Accessing The Current Route -->
## Accessing The Current Route

<!-- You may use the `current`, `currentRouteName`, and `currentRouteAction` methods on the `Route` facade to access information about the route handling the incoming request: -->
`Route` 파사드의 `current`, `currentRouteName`, `currentRouteAction` 메서드를 사용하여 현재 요청을 처리하는 라우트 정보를 가져올 수 있습니다.

```
use Illuminate\Support\Facades\Route;

$route = Route::current(); // Illuminate\Routing\Route
$name = Route::currentRouteName(); // string
$action = Route::currentRouteAction(); // string
```

<!-- You may refer to the API documentation for both the [underlying class of the Route facade](https://laravel.com/api/8.x/Illuminate/Routing/Router.html) and [Route instance](https://laravel.com/api/8.x/Illuminate/Routing/Route.html) to review all of the methods that are available on the router and route classes. -->
라우터 및 라우트 클래스에서 사용할 수 있는 모든 메서드는 [underlying class of the Route facade](https://laravel.com/api/8.x/Illuminate/Routing/Router.html)와 [Route instance](https://laravel.com/api/8.x/Illuminate/Routing/Route.html)에서 참조할 수 있습니다.

<a name="cors"></a>
<!-- ## Cross-Origin Resource Sharing (CORS) -->
## Cross-Origin Resource Sharing (CORS)

<!-- Laravel can automatically respond to CORS `OPTIONS` HTTP requests with values that you configure. All CORS settings may be configured in your application's `config/cors.php` configuration file. The `OPTIONS` requests will automatically be handled by the `HandleCors` [middleware](/docs/8.x/middleware) that is included by default in your global middleware stack. Your global middleware stack is located in your application's HTTP kernel (`App\Http\Kernel`). -->
Laravel은 설정에 따라 CORS(교차 출처 리소스 공유) `OPTIONS` HTTP 요청에 자동으로 응답할 수 있습니다. 모든 CORS 설정은 애플리케이션의 `config/cors.php` 설정 파일에서 구성할 수 있습니다. `OPTIONS` 요청은 글로벌 미들웨어 스택(애플리케이션의 `App\Http\Kernel`)에 기본으로 포함된 `HandleCors` [middleware](/docs/8.x/middleware)에 의해 자동으로 처리됩니다.

> [!TIP]
> CORS와 CORS 헤더에 대해 더 알고 싶다면 [MDN web documentation on CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#The_HTTP_response_headers)를 참고하세요.

<a name="route-caching"></a>
<!-- ## Route Caching -->
## Route Caching

<!-- When deploying your application to production, you should take advantage of Laravel's route cache. Using the route cache will drastically decrease the amount of time it takes to register all of your application's routes. To generate a route cache, execute the `route:cache` Artisan command: -->
애플리케이션을 운영 환경에 배포할 때에는 Laravel의 라우트 캐시를 적극적으로 활용해야 합니다. 라우트 캐싱을 사용하면 전체 라우트 등록 시간(부트 타임)이 크게 단축됩니다. 라우트 캐시를 생성하려면 `route:cache` 아티즌 명령어를 실행하세요.

```
php artisan route:cache
```

<!-- After running this command, your cached routes file will be loaded on every request. Remember, if you add any new routes you will need to generate a fresh route cache. Because of this, you should only run the `route:cache` command during your project's deployment. -->
이 명령어 실행 후에는, 모든 요청에서 캐시된 라우트 파일이 사용됩니다. 새 라우트를 추가했다면 반드시 라우트 캐시를 재생성해야 합니다. 따라서, `route:cache`는 프로젝트 배포 시에만 실행하는 것이 좋습니다.

<!-- You may use the `route:clear` command to clear the route cache: -->
라우트 캐시는 `route:clear` 명령어로 삭제할 수 있습니다.

```
php artisan route:clear
```
