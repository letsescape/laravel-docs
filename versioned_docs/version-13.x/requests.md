# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청에 접근하기](#accessing-the-request)
    - [요청 경로, 호스트 및 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력](#input)
    - [입력값 조회하기](#retrieving-input)
    - [입력값 존재 여부](#input-presence)
    - [추가 입력값 병합하기](#merging-additional-input)
    - [이전 입력값](#old-input)
    - [쿠키](#cookies)
    - [입력값 공백 제거 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 조회하기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 구성하기](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 구성하기](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션에서 현재 처리 중인 HTTP 요청과 상호작용하고, 요청과 함께 제출된 입력값, 쿠키, 파일을 가져올 수 있는 객체 지향 방식을 제공합니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기 (Interacting With The Request)

<a name="accessing-the-request"></a>
### 요청에 접근하기

의존성 주입을 통해 현재 HTTP 요청 인스턴스를 얻으려면 라우트 클로저나 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스 타입을 지정해야 합니다. 들어오는 요청 인스턴스는 Laravel [서비스 컨테이너](/docs/13.x/container)에 의해 자동으로 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // Store the user...

        return redirect('/users');
    }
}
```

앞서 언급했듯이 라우트 클로저에서도 `Illuminate\Http\Request` 클래스 타입을 지정할 수 있습니다. 서비스 컨테이너는 클로저가 실행될 때 들어오는 요청을 클로저에 자동으로 주입합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메서드가 라우트 파라미터의 입력도 기대한다면, 다른 의존성 뒤에 라우트 파라미터를 나열해야 합니다. 예를 들어 라우트가 다음과 같이 정의되어 있다고 가정해 보겠습니다.

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

다음처럼 컨트롤러 메서드를 정의하면 여전히 `Illuminate\Http\Request` 타입을 지정하면서 `id` 라우트 파라미터에도 접근할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the specified user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트 및 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 살펴볼 수 있는 다양한 메서드를 제공하며, `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 아래에서는 가장 중요한 메서드 몇 가지를 살펴보겠습니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 조회하기

`path` 메서드는 요청의 경로 정보를 반환합니다. 따라서 들어오는 요청이 `http://example.com/foo/bar`를 대상으로 한다면 `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로 / 라우트 검사하기

`is` 메서드를 사용하면 들어오는 요청 경로가 주어진 패턴과 일치하는지 확인할 수 있습니다. 이 메서드를 사용할 때 `*` 문자를 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면 들어오는 요청이 [이름이 지정된 라우트](/docs/13.x/routing#named-routes)와 일치했는지 확인할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 조회하기

들어오는 요청의 전체 URL을 조회하려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리 문자열을 제외한 URL을 반환하고, `fullUrl` 메서드는 쿼리 문자열을 포함합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 문자열 데이터를 추가하고 싶다면 `fullUrlWithQuery` 메서드를 호출할 수 있습니다. 이 메서드는 주어진 쿼리 문자열 변수 배열을 현재 쿼리 문자열과 병합합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

주어진 쿼리 문자열 파라미터를 제외한 현재 URL을 가져오고 싶다면 `fullUrlWithoutQuery` 메서드를 사용할 수 있습니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 조회하기

`host`, `httpHost`, `schemeAndHttpHost` 메서드를 통해 들어오는 요청의 "host"를 조회할 수 있습니다.

```php
// http://localhost:8000
$request->host(); // localhost
$request->httpHost(); // localhost:8000
$request->schemeAndHttpHost(); // http://localhost:8000
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 조회하기

`method` 메서드는 요청의 HTTP 동사를 반환합니다. `isMethod` 메서드를 사용하면 HTTP 동사가 주어진 문자열과 일치하는지 확인할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더

`header` 메서드를 사용하여 `Illuminate\Http\Request` 인스턴스에서 요청 헤더를 조회할 수 있습니다. 요청에 해당 헤더가 없으면 `null`이 반환됩니다. 하지만 `header` 메서드는 선택적인 두 번째 인수를 받으며, 요청에 해당 헤더가 없을 때 이 값이 반환됩니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드를 사용하면 요청에 주어진 헤더가 포함되어 있는지 확인할 수 있습니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의를 위해 `bearerToken` 메서드를 사용하여 `Authorization` 헤더에서 Bearer 토큰을 조회할 수 있습니다. 해당 헤더가 없으면 빈 문자열이 반환됩니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 메서드를 사용하면 애플리케이션에 요청을 보낸 클라이언트의 IP 주소를 조회할 수 있습니다.

```php
$ipAddress = $request->ip();
```

프록시를 통해 전달된 모든 클라이언트 IP 주소를 포함하여 IP 주소 배열을 조회하고 싶다면 `ips` 메서드를 사용할 수 있습니다. "원래" 클라이언트 IP 주소는 배열의 끝에 위치합니다.

```php
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는 사용자 제어 입력값으로 간주해야 하며, 정보 제공 목적으로만 사용해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 `Accept` 헤더를 통해 들어오는 요청이 요구하는 콘텐츠 타입을 검사할 수 있는 여러 메서드를 제공합니다. 먼저 `getAcceptableContentTypes` 메서드는 요청이 허용하는 모든 콘텐츠 타입을 담은 배열을 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 콘텐츠 타입 배열을 받고, 그중 하나라도 요청에서 허용되면 `true`를 반환합니다. 그렇지 않으면 `false`가 반환됩니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드를 사용하면 주어진 콘텐츠 타입 배열 중 요청이 가장 선호하는 콘텐츠 타입을 확인할 수 있습니다. 제공된 콘텐츠 타입 중 요청에서 허용하는 것이 없다면 `null`이 반환됩니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML 또는 JSON만 제공하므로, `expectsJson` 메서드를 사용하면 들어오는 요청이 JSON 응답을 기대하는지 빠르게 확인할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

AI 에이전트나 Markdown 응답을 소비하는 다른 클라이언트에 응답을 제공하는 경우처럼, 요청이 특별히 Markdown을 선호하는지 또는 다른 콘텐츠 타입과 함께 Markdown을 허용하는지 확인해야 한다면 `wantsMarkdown` 및 `acceptsMarkdown` 메서드를 사용할 수 있습니다.

```php
if ($request->wantsMarkdown()) {
    // The client's most preferred content type is text/markdown...
}

if ($request->acceptsMarkdown()) {
    // The client accepts Markdown responses...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 요청과 응답을 포함한 HTTP 메시지 인터페이스를 정의합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻고 싶다면 먼저 몇 가지 라이브러리를 설치해야 합니다. Laravel은 일반적인 Laravel 요청과 응답을 PSR-7 호환 구현으로 변환하기 위해 *Symfony HTTP Message Bridge* 컴포넌트를 사용합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이 라이브러리들을 설치한 뒤에는 라우트 클로저나 컨트롤러 메서드에서 요청 인터페이스 타입을 지정하여 PSR-7 요청을 얻을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 이를 자동으로 Laravel 응답 인스턴스로 다시 변환하여 표시합니다.

<a name="input"></a>
## 입력 (Input)

<a name="retrieving-input"></a>
### 입력값 조회하기

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 조회하기

`all` 메서드를 사용하면 들어오는 요청의 모든 입력 데이터를 `array`로 조회할 수 있습니다. 이 메서드는 들어오는 요청이 HTML 폼에서 온 것인지 XHR 요청인지와 관계없이 사용할 수 있습니다.

```php
$input = $request->all();
```

`collect` 메서드를 사용하면 들어오는 요청의 모든 입력 데이터를 [컬렉션](/docs/13.x/collections)으로 조회할 수 있습니다.

```php
$input = $request->collect();
```

`collect` 메서드를 사용하면 들어오는 요청 입력값의 일부만 컬렉션으로 조회할 수도 있습니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 입력값 조회하기

몇 가지 간단한 메서드를 사용하면 요청에 어떤 HTTP 동사가 사용되었는지 신경 쓰지 않고 `Illuminate\Http\Request` 인스턴스에서 모든 사용자 입력값에 접근할 수 있습니다. HTTP 동사와 관계없이 `input` 메서드를 사용하여 사용자 입력값을 조회할 수 있습니다.

```php
$name = $request->input('name');
```

`input` 메서드의 두 번째 인수로 기본값을 전달할 수 있습니다. 요청에 조회하려는 입력값이 없으면 이 값이 반환됩니다.

```php
$name = $request->input('name', 'Sally');
```

배열 입력을 포함하는 폼을 다룰 때는 "dot" 표기법을 사용하여 배열에 접근합니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

모든 입력값을 연관 배열로 조회하려면 아무 인수 없이 `input` 메서드를 호출할 수 있습니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 문자열에서 입력값 조회하기

`input` 메서드는 전체 요청 페이로드(쿼리 문자열 포함)에서 값을 조회하지만, `query` 메서드는 쿼리 문자열에서만 값을 조회합니다.

```php
$name = $request->query('name');
```

요청한 쿼리 문자열 값 데이터가 없으면 이 메서드의 두 번째 인수가 반환됩니다.

```php
$name = $request->query('name', 'Helen');
```

모든 쿼리 문자열 값을 연관 배열로 조회하려면 아무 인수 없이 `query` 메서드를 호출할 수 있습니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 조회하기

애플리케이션에 JSON 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 설정되어 있다면 `input` 메서드를 통해 JSON 데이터에 접근할 수 있습니다. "dot" 문법을 사용하여 JSON 배열 / 객체 안에 중첩된 값을 조회할 수도 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 조회하기

요청의 입력 데이터를 원시 `string`으로 조회하는 대신, `string` 메서드를 사용하여 요청 데이터를 [Illuminate\Support\Stringable](/docs/13.x/strings) 인스턴스로 조회할 수 있습니다.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수 입력값 조회하기

입력값을 정수로 조회하려면 `integer` 메서드를 사용할 수 있습니다. 이 메서드는 입력값을 정수로 캐스팅하려고 시도합니다. 입력값이 없거나 캐스팅에 실패하면 지정한 기본값을 반환합니다. 이 메서드는 특히 페이지네이션이나 기타 숫자 입력값에 유용합니다.

```php
$perPage = $request->integer('per_page');
```
<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력 값 조회

체크박스와 같은 HTML 요소를 다룰 때 애플리케이션은 실제로는 문자열인 `truthy`(참으로 평가되는) 값을 받을 수 있습니다. 예를 들어 "true" 또는 "on" 같은 값입니다. 편의를 위해 `boolean` 메서드를 사용하여 이러한 값을 불리언으로 조회할 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes"에 대해 `true`를 반환합니다. 그 외의 모든 값은 `false`를 반환합니다:

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
#### 배열 입력 값 조회

배열을 포함하는 입력 값은 `array` 메서드를 사용하여 조회할 수 있습니다. 이 메서드는 항상 입력 값을 배열로 형 변환합니다. 요청에 주어진 이름의 입력 값이 포함되어 있지 않으면 빈 배열이 반환됩니다:

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력 값 조회

편의를 위해 날짜 / 시간을 포함하는 입력 값은 `date` 메서드를 사용하여 Carbon 인스턴스로 조회할 수 있습니다. 요청에 주어진 이름의 입력 값이 포함되어 있지 않으면 `null`이 반환됩니다:

```php
$birthday = $request->date('birthday');
```

`date` 메서드가 받는 두 번째와 세 번째 인수는 각각 날짜의 형식과 시간대를 지정하는 데 사용할 수 있습니다:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력 값이 존재하지만 형식이 유효하지 않으면 `InvalidArgumentException`이 발생합니다. 따라서 `date` 메서드를 호출하기 전에 입력 값을 유효성 검증하는 것이 좋습니다.

<a name="retrieving-interval-input-values"></a>
#### 간격 입력 값 조회

기간을 포함하는 입력 값은 `interval` 메서드를 사용하여 `CarbonInterval` 인스턴스로 조회할 수 있습니다. 요청에 주어진 이름의 입력 값이 포함되어 있지 않으면 `null`이 반환됩니다:

```php
$duration = $request->interval('duration');
```

입력 값이 숫자인 경우 두 번째 인수로 단위를 제공할 수 있습니다. 단위는 `second`, `minute`, `day` 같은 문자열이거나 `Carbon\Unit` enum 인스턴스일 수 있습니다:

```php
use Carbon\Unit;

$timeout = $request->interval('timeout', 'second');

$delay = $request->interval('delay', Unit::Minute);
```

입력 값이 존재하지만 형식이 유효하지 않으면 `InvalidArgumentException`이 발생합니다. 따라서 `interval` 메서드를 호출하기 전에 입력 값을 유효성 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력 값 조회

[PHP enums](https://www.php.net/manual/en/language.types.enumerations.php)에 해당하는 입력 값도 요청에서 조회할 수 있습니다. 요청에 주어진 이름의 입력 값이 포함되어 있지 않거나, enum에 입력 값과 일치하는 backing value(백킹 값)가 없으면 `null`이 반환됩니다. `enum` 메서드는 첫 번째 인수로 입력 값의 이름을, 두 번째 인수로 enum 클래스를 받습니다:

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

값이 없거나 유효하지 않을 때 반환할 기본값을 제공할 수도 있습니다:

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

입력 값이 PHP enum에 해당하는 값들의 배열이라면, `enums` 메서드를 사용하여 값 배열을 enum 인스턴스 배열로 조회할 수 있습니다:

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 속성을 통한 입력 조회

`Illuminate\Http\Request` 인스턴스의 동적 속성을 사용하여 사용자 입력에 접근할 수도 있습니다. 예를 들어 애플리케이션의 폼 중 하나에 `name` 필드가 있다면, 다음과 같이 해당 필드의 값에 접근할 수 있습니다:

```php
$name = $request->name;
```

동적 속성을 사용할 때 Laravel은 먼저 요청 페이로드에서 해당 파라미터 값을 찾습니다. 값이 없으면 Laravel은 일치한 라우트의 파라미터에서 해당 필드를 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력 데이터의 일부 조회

입력 데이터의 하위 집합을 조회해야 한다면 `only`와 `except` 메서드를 사용할 수 있습니다. 두 메서드 모두 단일 `array` 또는 동적인 인수 목록을 받습니다:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청한 모든 키 / 값 쌍을 반환합니다. 다만 요청에 존재하지 않는 키 / 값 쌍은 반환하지 않습니다.

<a name="input-presence"></a>
### 입력 존재 여부

요청에 값이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 요청에 값이 존재하면 `true`를 반환합니다:

```php
if ($request->has('name')) {
    // ...
}
```

배열이 주어지면 `has` 메서드는 지정된 값이 모두 존재하는지 확인합니다:

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메서드는 지정된 값 중 하나라도 존재하면 `true`를 반환합니다:

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 요청에 값이 존재하면 주어진 클로저를 실행합니다:

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

지정된 값이 요청에 존재하지 않을 때 실행할 두 번째 클로저를 `whenHas` 메서드에 전달할 수도 있습니다:

```php
$request->whenHas('name', function (string $input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```

요청에 값이 존재하고 빈 문자열이 아닌지 확인하려면 `filled` 메서드를 사용할 수 있습니다:

```php
if ($request->filled('name')) {
    // ...
}
```

요청에서 값이 누락되었거나 빈 문자열인지 확인하려면 `isNotFilled` 메서드를 사용할 수 있습니다:

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열이 주어지면 `isNotFilled` 메서드는 지정된 값이 모두 누락되었거나 비어 있는지 확인합니다:

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled` 메서드는 지정된 값 중 하나라도 빈 문자열이 아니면 `true`를 반환합니다:

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 요청에 값이 존재하고 빈 문자열이 아니면 주어진 클로저를 실행합니다:

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

지정된 값이 "filled" 상태가 아닐 때 실행할 두 번째 클로저를 `whenFilled` 메서드에 전달할 수도 있습니다:

```php
$request->whenFilled('name', function (string $input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```

주어진 키가 요청에 없는지 확인하려면 `missing`과 `whenMissing` 메서드를 사용할 수 있습니다:

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // The "name" value is missing...
}, function () {
    // The "name" value is present...
});
```

<a name="merging-additional-input"></a>
### 추가 입력 병합

때로는 요청의 기존 입력 데이터에 추가 입력을 수동으로 병합해야 할 수 있습니다. 이를 위해 `merge` 메서드를 사용할 수 있습니다. 주어진 입력 키가 요청에 이미 존재하면 `merge` 메서드에 제공된 데이터로 덮어씁니다:

```php
$request->merge(['votes' => 0]);
```

해당 키가 요청의 입력 데이터에 아직 존재하지 않을 때만 입력을 병합하려면 `mergeIfMissing` 메서드를 사용할 수 있습니다:

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력

Laravel은 한 요청의 입력을 다음 요청 동안 유지할 수 있게 해 줍니다. 이 기능은 유효성 검증 오류를 감지한 후 폼을 다시 채울 때 특히 유용합니다. 하지만 Laravel에 포함된 [유효성 검증 기능](/docs/13.x/validation)을 사용하고 있다면, Laravel의 일부 내장 유효성 검증 기능이 이러한 세션 입력 플래시 메서드를 자동으로 호출하므로 직접 사용할 필요가 없을 수 있습니다.

<a name="flashing-input-to-the-session"></a>
#### 세션에 입력 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력을 [session](/docs/13.x/session)에 플래시하여, 사용자의 다음 애플리케이션 요청 중에 사용할 수 있게 합니다:

```php
$request->flash();
```

`flashOnly`와 `flashExcept` 메서드를 사용하여 요청 데이터의 하위 집합만 세션에 플래시할 수도 있습니다. 이 메서드는 비밀번호 같은 민감한 정보를 세션에 저장하지 않도록 할 때 유용합니다:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력을 플래시한 다음 리다이렉트하기

입력을 세션에 플래시한 다음 이전 페이지로 리다이렉트하고 싶은 경우가 많으므로, `withInput` 메서드를 사용하여 리다이렉트에 입력 플래시를 쉽게 체이닝할 수 있습니다:

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력 조회

이전 요청에서 플래시된 입력을 조회하려면 `Illuminate\Http\Request` 인스턴스에서 `old` 메서드를 호출합니다. `old` 메서드는 이전에 플래시된 입력 데이터를 [session](/docs/13.x/session)에서 가져옵니다:

```php
$username = $request->old('username');
```

Laravel은 전역 `old` 헬퍼도 제공합니다. [Blade template](/docs/13.x/blade) 안에서 이전 입력을 표시하는 경우, 폼을 다시 채우기 위해 `old` 헬퍼를 사용하는 것이 더 편리합니다. 주어진 필드에 대한 이전 입력이 없으면 `null`이 반환됩니다:

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 조회

Laravel 프레임워크가 생성한 모든 쿠키는 암호화되고 인증 코드로 서명됩니다. 따라서 클라이언트가 쿠키를 변경했다면 유효하지 않은 것으로 간주됩니다. 요청에서 쿠키 값을 조회하려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용합니다:

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력 트리밍과 정규화 (Input Trimming and Normalization)

기본적으로 Laravel은 애플리케이션의 전역 미들웨어 스택에 `Illuminate\Foundation\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 미들웨어는 요청으로 들어오는 모든 문자열 필드를 자동으로 트리밍하고, 빈 문자열 필드를 `null`로 변환합니다. 덕분에 라우트와 컨트롤러에서 이러한 정규화 문제를 신경 쓰지 않아도 됩니다.

#### 입력 정규화 비활성화

모든 요청에 대해 이 동작을 비활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드를 호출하여 두 미들웨어를 애플리케이션의 미들웨어 스택에서 제거할 수 있습니다:

```php
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```

애플리케이션으로 들어오는 요청 중 일부에 대해서만 문자열 트리밍과 빈 문자열 변환을 비활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `trimStrings`와 `convertEmptyStringsToNull` 미들웨어 메서드를 사용할 수 있습니다. 두 메서드 모두 클로저 배열을 받으며, 각 클로저는 입력 정규화를 건너뛸지 여부를 나타내기 위해 `true` 또는 `false`를 반환해야 합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->convertEmptyStringsToNull(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);

    $middleware->trimStrings(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);
})
```

<a name="files"></a>
## 파일 (Files)

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 조회

`file` 메서드나 동적 속성을 사용하여 `Illuminate\Http\Request` 인스턴스에서 업로드된 파일을 조회할 수 있습니다. `file` 메서드는 `Illuminate\Http\UploadedFile` 클래스의 인스턴스를 반환합니다. 이 클래스는 PHP `SplFileInfo` 클래스를 확장하며, 파일과 상호작용하기 위한 다양한 메서드를 제공합니다:

```php
$file = $request->file('photo');

$file = $request->photo;
```

요청에 파일이 존재하는지 확인하려면 `hasFile` 메서드를 사용할 수 있습니다:

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 성공적인 업로드 검증

파일이 존재하는지 확인하는 것 외에도, `isValid` 메서드를 통해 파일 업로드 중 문제가 없었는지 확인할 수 있습니다:

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로와 확장자

`UploadedFile` 클래스에는 파일의 정규화된 전체 경로와 확장자에 접근하는 메서드도 포함되어 있습니다. `extension` 메서드는 파일의 내용을 기반으로 파일 확장자를 추측하려고 시도합니다. 이 확장자는 클라이언트가 제공한 확장자와 다를 수 있습니다:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에서 사용할 수 있는 다양한 다른 메서드가 있습니다. 이러한 메서드에 대한 자세한 내용은 [클래스의 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 확인하십시오.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장

업로드된 파일을 저장하려면 일반적으로 설정된 [filesystems](/docs/13.x/filesystem) 중 하나를 사용합니다. `UploadedFile` 클래스에는 업로드된 파일을 디스크 중 하나로 이동하는 `store` 메서드가 있습니다. 이 디스크는 로컬 파일 시스템의 위치일 수도 있고 Amazon S3 같은 클라우드 스토리지 위치일 수도 있습니다.

`store` 메서드는 파일 시스템에 설정된 루트 디렉터리를 기준으로 파일을 저장할 경로를 받습니다. 이 경로에는 파일명이 포함되어서는 안 됩니다. 파일명으로 사용할 고유 ID가 자동으로 생성되기 때문입니다.

`store` 메서드는 파일을 저장하는 데 사용할 디스크 이름을 선택적인 두 번째 인수로 받을 수도 있습니다. 이 메서드는 디스크의 루트를 기준으로 한 파일 경로를 반환합니다:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명이 자동으로 생성되지 않게 하려면 `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로, 파일명, 디스크 이름을 인수로 받습니다:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```
> [!NOTE]
> Laravel의 파일 저장소에 대한 자세한 내용은 전체 [파일 저장소 문서](/docs/13.x/filesystem)를 확인하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정 (Configuring Trusted Proxies)

TLS / SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼를 사용하면 애플리케이션이 가끔 HTTPS 링크를 생성하지 않는 것을 볼 수 있습니다. 일반적으로 이는 애플리케이션이 로드 밸런서로부터 포트 80을 통해 트래픽을 전달받고 있어, 보안 링크를 생성해야 한다는 사실을 알지 못하기 때문입니다.

이 문제를 해결하려면 Laravel 애플리케이션에 포함된 `Illuminate\Http\Middleware\TrustProxies` Middleware를 활성화할 수 있습니다. 이를 통해 애플리케이션이 신뢰해야 하는 로드 밸런서나 프록시를 빠르게 사용자 정의할 수 있습니다. 신뢰할 수 있는 프록시는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` Middleware 메서드를 사용하여 지정해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰할 수 있는 프록시를 설정하는 것 외에도, 신뢰해야 하는 프록시 헤더를 설정할 수도 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
        Request::HEADER_X_FORWARDED_HOST |
        Request::HEADER_X_FORWARDED_PORT |
        Request::HEADER_X_FORWARDED_PROTO |
        Request::HEADER_X_FORWARDED_AWS_ELB
    );
})
```

> [!NOTE]
> AWS Elastic Load Balancing을 사용하고 있다면 `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`이어야 합니다. 로드 밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)의 표준 `Forwarded` 헤더를 사용한다면 `headers` 값은 `Request::HEADER_FORWARDED`이어야 합니다. `headers` 값에 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [프록시 신뢰](https://symfony.com/doc/current/deployment/proxies.html) 문서를 확인하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰

Amazon AWS 또는 다른 "클라우드" 로드 밸런서 제공자를 사용하고 있다면 실제 로드 밸런서의 IP 주소를 알 수 없을 수 있습니다. 이 경우 `*`를 사용하여 모든 프록시를 신뢰할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정 (Configuring Trusted Hosts)

기본적으로 Laravel은 HTTP 요청의 `Host` 헤더 내용과 관계없이 수신한 모든 요청에 응답합니다. 또한 웹 요청 중 애플리케이션에 대한 절대 URL을 생성할 때 `Host` 헤더의 값이 사용됩니다.

일반적으로 Nginx나 Apache 같은 웹 서버를 설정하여 지정된 호스트명과 일치하는 요청만 애플리케이션으로 보내도록 해야 합니다. 하지만 웹 서버를 직접 사용자 정의할 수 없고, Laravel이 특정 호스트명에만 응답하도록 지시해야 한다면 애플리케이션에서 `Illuminate\Http\Middleware\TrustHosts` Middleware를 활성화하여 처리할 수 있습니다.

`TrustHosts` Middleware를 활성화하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` Middleware 메서드를 호출해야 합니다. 이 메서드의 `at` 인수를 사용하여 애플리케이션이 응답해야 하는 호스트명을 지정할 수 있습니다. 호스트명 문자열은 정규 표현식으로 처리됩니다. 다른 `Host` 헤더를 가진 들어오는 요청은 거부됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$']);
})
```

기본적으로 애플리케이션 URL의 서브도메인에서 오는 요청도 자동으로 신뢰됩니다. 이 동작을 비활성화하려면 `subdomains` 인수를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
})
```

신뢰할 수 있는 호스트를 결정하기 위해 애플리케이션의 설정 파일이나 데이터베이스에 접근해야 한다면 `at` 인수에 클로저를 제공할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```
