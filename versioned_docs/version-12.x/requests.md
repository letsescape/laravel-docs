# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값](#input)
    - [입력값 조회](#retrieving-input)
    - [입력값 존재 여부](#input-presence)
    - [추가 입력값 병합](#merging-additional-input)
    - [이전 입력값](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 가져오기](#retrieving-uploaded-files)
    - [업로드된 파일 저장하기](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정하기](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정하기](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Illuminate\Http\Request` 클래스는 애플리케이션에서 현재 처리 중인 HTTP 요청과 상호작용하고, 요청과 함께 전달된 입력값, 쿠키, 파일 등 다양한 데이터를 객체 지향적으로 읽어올 수 있게 해줍니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기 (Interacting With The Request)

<a name="accessing-the-request"></a>
### 요청 접근하기 (Accessing the Request)

현재 HTTP 요청 인스턴스를 의존성 주입(dependency injection)을 통해 얻으려면, 라우트 클로저 또는 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입힌트로 지정하면 됩니다. 라라벨의 [서비스 컨테이너](/docs/12.x/container)는 자동으로 요청 인스턴스를 주입합니다.

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

위와 같이 컨트롤러 뿐만 아니라, 라우트 클로저에서도 요청 인스턴스를 타입힌트로 지정할 수 있습니다. 클로저가 실행될 때, 서비스 컨테이너가 자동으로 요청을 주입합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메서드에서 라우트 파라미터와 의존성 주입을 같이 쓰는 경우, 라우트 파라미터는 다른 의존성 뒤에 나열해야 합니다. 예를 들어, 다음과 같이 라우트를 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드에서 `Illuminate\Http\Request`를 타입힌트로 받고, 이후에 `id` 라우트 파라미터를 사용하면 됩니다.

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
### 요청 경로, 호스트, 메서드 (Request Path, Host, and Method)

`Illuminate\Http\Request` 인스턴스는 다양한 메서드를 제공하여 들어온 HTTP 요청을 살펴볼 수 있으며, 이는 `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 아래에서 주요 메서드 몇 가지를 살펴봅니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 조회

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어, 들어온 요청이 `http://example.com/foo/bar`라면, `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로/라우트 검사

`is` 메서드를 사용하면, 들어온 요청의 경로가 특정 패턴과 일치하는지 확인할 수 있습니다. 이때 `*` 문자를 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면 들어온 요청이 [네임드 라우트](/docs/12.x/routing#named-routes)와 일치하는지 확인할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 조회

요청의 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url`은 쿼리 스트링 없는 URL을, `fullUrl`은 쿼리 스트링을 포함한 전체 URL을 반환합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 문자열 데이터를 추가하려면 `fullUrlWithQuery` 메서드를 사용할 수 있습니다. 이 메서드는 지정한 쿼리 변수와 현재 쿼리 문자열을 합칩니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 문자열 파라미터를 제거한 현재 URL이 필요하다면, `fullUrlWithoutQuery` 메서드를 사용할 수 있습니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트 조회

요청의 "호스트" 값은 `host`, `httpHost`, `schemeAndHttpHost` 메서드를 통해 각각 가져올 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드 조회

`method` 메서드는 요청의 HTTP 메서드(HTTP verb)를 반환합니다. 또한, `isMethod` 메서드는 메서드가 특정 문자열과 일치하는지 확인합니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더 (Request Headers)

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드를 사용해 요청 헤더를 조회할 수 있습니다. 해당 헤더가 요청에 없다면 `null`을 반환하며, 두 번째 인수로 기본값을 지정할 수도 있습니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드는 요청에 특정 헤더가 포함되어 있는지 여부를 확인합니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의를 위해, `bearerToken` 메서드를 사용하면 `Authorization` 헤더에서 bearer 토큰을 쉽게 가져올 수 있습니다. 해당 헤더가 없다면 빈 문자열을 반환합니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소 (Request IP Address)

`ip` 메서드는 요청을 보낸 클라이언트의 IP 주소를 반환합니다.

```php
$ipAddress = $request->ip();
```

프록시를 통해 전달된 모든 클라이언트 IP 주소 배열이 필요하다면 `ips` 메서드를 사용하세요. 배열의 마지막 값이 "실제" 클라이언트의 IP 주소입니다.

```php
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는, 사용자 제어 입력으로 간주해야 하며 참고용으로만 사용하는 것이 좋습니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상 (Content Negotiation)

Laravel은 요청의 `Accept` 헤더를 기반으로, 요청이 요구하는 콘텐츠 타입을 확인하는 여러 메서드를 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청이 허용하는 모든 콘텐츠 타입의 배열을 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 여러 콘텐츠 타입이 배열로 주어질 때, 그 중 하나라도 요청에 허용되는 타입이 있다면 `true`를, 없으면 `false`를 반환합니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드는 배열로 전달한 콘텐츠 타입 중 요청이 제일 선호하는 타입을 반환합니다. 어떠한 타입도 허용되지 않으면 `null`을 반환합니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML이나 JSON만을 제공하는 경우 `expectsJson` 메서드를 사용하여 요청이 JSON 응답을 기대하는지 빠르게 확인할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청 (PSR-7 Requests)

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청 및 응답)를 위한 인터페이스를 정의합니다. 만약 Laravel의 Request 대신 PSR-7 요청 인스턴스를 사용하고 싶다면, 몇 가지 라이브러리가 필요합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 사용해 기존 Request/Response를 PSR-7 방식으로 변환합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

라이브러리를 설치한 후, 라우트 클로저나 컨트롤러 메서드에서 PSR-7 요청 인터페이스를 타입힌트로 지정하면 자동으로 주입받을 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 자동으로 Laravel의 응답 인스턴스로 변환하여 출력합니다.

<a name="input"></a>
## 입력값 (Input)

<a name="retrieving-input"></a>
### 입력값 조회 (Retrieving Input)

<a name="retrieving-all-input-data"></a>
#### 전체 입력값 가져오기

`all` 메서드를 사용하면 들어온 요청의 모든 입력값을 `array` 형태로 얻을 수 있습니다. 이 메서드는 요청이 HTML 폼이든 XHR 요청이든 관계없이 모두 사용할 수 있습니다.

```php
$input = $request->all();
```

`collect` 메서드를 사용해 입력값을 [컬렉션](/docs/12.x/collections)으로 받을 수도 있습니다.

```php
$input = $request->collect();
```

또한, `collect`에 키를 전달하여 특정 입력만 부분적으로 컬렉션으로 가져올 수 있습니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 특정 입력값 가져오기

`Illuminate\Http\Request` 인스턴스에서 간단한 메서드로 모든 사용자 입력을 가져올 수 있습니다. HTTP 메서드가 무엇이든 `input` 메서드를 사용하면 값을 받을 수 있습니다.

```php
$name = $request->input('name');
```

값이 없을 때 반환할 기본값은 두 번째 인수로 지정할 수 있습니다.

```php
$name = $request->input('name', 'Sally');
```

폼에서 배열 형태의 입력값을 다룰 때는 "점 표기법"을 쓸 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인수를 생략하고 `input`을 호출하면 모든 입력값을 연관 배열 형태로 가져옵니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링에서 입력값 가져오기

`input` 메서드는 요청 전체 페이로드(쿼리 스트링 포함)에서 값을 조회하지만, 오직 쿼리 스트링만에서 값을 얻고 싶다면 `query` 메서드를 쓰세요.

```php
$name = $request->query('name');
```

값이 없을 때 반환할 기본값도 두 번째 인수로 지정할 수 있습니다.

```php
$name = $request->query('name', 'Helen');
```

인수 없이 호출하면 모든 쿼리 스트링 값을 연관 배열 형태로 반환합니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 가져오기

JSON 요청이 전달된 경우, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 지정되어 있다면 `input` 메서드로 JSON 데이터를 접근할 수 있습니다. 점 표기법으로 내부에 중첩된 값도 읽을 수 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 가져오기

입력값을 원시 `string`이 아닌 [Illuminate\Support\Stringable](/docs/12.x/strings) 인스턴스로 받고 싶다면, `string` 메서드를 사용하세요.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수형 입력값 가져오기

입력값을 정수형으로 받고 싶을 때는 `integer` 메서드를 사용하면 됩니다. 입력값이 없거나 형 변환이 실패할 경우 지정한 기본값을 반환합니다. 페이징이나 숫자 입력에 유용합니다.

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력값 가져오기

체크박스 같은 HTML 요소는 실제로는 문자열 형태의 "truthy" 값을 보낼 수 있습니다. 예를 들어, "true" 또는 "on"이 그런 값입니다. `boolean` 메서드는 `"1"`, `1`, `true`, `"true"`, `"on"`, `"yes"`를 모두 `true`로 변환합니다. 다른 값은 모두 `false`입니다.

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
#### 배열 입력값 가져오기

배열 형태의 입력값은 `array` 메서드로 받을 수 있습니다. 무조건 배열 타입으로 변환되어 반환되며, 입력값이 없으면 빈 배열이 반환됩니다.

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 가져오기

날짜나 시간을 입력값으로 받을 때는 `date` 메서드를 사용해 [Carbon] 인스턴스로 반환받을 수 있습니다. 값이 없으면 `null`을 반환합니다.

```php
$birthday = $request->date('birthday');
```

두 번째, 세 번째 인수로 날짜 형식과 타임존을 명시적으로 지정할 수 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값 존재는 하지만 형식이 올바르지 않으면 `InvalidArgumentException`이 발생하니, `date` 메서드를 사용하기 전에 반드시 유효성 검증을 선행하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### 열거형(enum) 입력값 가져오기

[PHP 열거형(enum)](https://www.php.net/manual/en/language.types.enumerations.php)과 대응되는 입력값도 요청에서 가져올 수 있습니다. 해당 이름의 입력값이 없거나, enum의 백킹 값과 일치하지 않으면 `null`을 반환합니다. `enum` 메서드는 입력값의 이름과 enum 클래스를 첫 번째, 두 번째 인수로 받습니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

값이 없거나 올바르지 않을 때 사용할 기본값도 세 번째 인수로 지정할 수 있습니다.

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

만약 입력값이 여러 개의 enum 배열이라면, `enums` 메서드를 사용해 배열 전체를 enum 인스턴스 배열로 받을 수 있습니다.

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 프로퍼티를 통한 입력값 접근

`Illuminate\Http\Request` 인스턴스에서 동적 프로퍼티로도 사용자 입력값에 접근할 수 있습니다. 예를 들어, 폼에 `name` 필드가 있다면 아래와 같이 값을 가져올 수 있습니다.

```php
$name = $request->name;
```

이 방식으로 값을 조회하면, Laravel은 먼저 요청 페이로드에서 값을 찾아보고, 없으면 일치하는 라우트 파라미터에서도 값을 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력값 일부만 가져오기

입력값 일부만 필요할 때는 `only`와 `except` 메서드를 사용할 수 있습니다. 두 메서드는 배열 또는 가변 인수로 키 목록을 받습니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 실제로 존재하는 key/value 쌍만 반환합니다. 요청에 없는 key는 반환하지 않습니다.

<a name="input-presence"></a>
### 입력값 존재 여부 (Input Presence)

`has` 메서드를 사용해 특정 값이 요청에 존재하는지 확인할 수 있습니다. 값이 있으면 `true`를, 없으면 `false`를 반환합니다.

```php
if ($request->has('name')) {
    // ...
}
```

배열을 인수로 넘기면, 지정한 모든 값이 요청에 존재해야 `true`를 반환합니다.

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny`는 지정한 값 중 하나라도 존재하면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas`는 값이 있을 때만 지정한 클로저를 실행합니다.

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

값이 없을 때 실행할 두 번째 클로저도 전달할 수 있습니다.

```php
$request->whenHas('name', function (string $input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```

값이 존재하며, 빈 문자열이 아닌지 확인하려면 `filled` 메서드를 사용합니다.

```php
if ($request->filled('name')) {
    // ...
}
```

요청에 값이 없거나 빈 문자열인지 확인하려면 `isNotFilled` 메서드를 사용할 수 있습니다.

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열로 전달할 수도 있습니다.

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled`는 지정한 값 중 한 개라도 빈 문자열이 아닌 경우 `true`를 반환합니다.

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled`는 값이 존재하고, 빈 문자열이 아닌 상태에서만 클로저를 실행합니다.

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

값이 비어있을 때 실행할 두 번째 클로저도 지정할 수 있습니다.

```php
$request->whenFilled('name', function (string $input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```

주어진 key가 요청에 아예 없을 때는 `missing` 및 `whenMissing` 메서드를 사용할 수 있습니다.

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
### 추가 입력값 병합 (Merging Additional Input)

기존 요청 입력값에 추가 데이터를 직접 병합하고 싶을 때는 `merge` 메서드를 사용합니다. 이미 입력값에 같은 키가 있다면 새로운 값이 덮어써집니다.

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing`은 해당 키가 없을 때만 값을 병합합니다.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값 (Old Input)

라라벨에서는 한 번의 요청에서 제출한 입력값을 다음 요청까지 유지할 수 있습니다. 이 기능은 유효성 검증에서 에러가 발생한 후, 폼을 다시 채워주는 데 유용합니다. 라라벨의 [유효성 검증 기능](/docs/12.x/validation)을 사용할 때는 해당 메서드를 직접 사용할 일이 줄어들 수 있습니다. 일부 내장 기능에서 자동으로 입력값을 세션에 플래시(flashing)하기 때문입니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드는, 현재의 입력값을 [세션](/docs/12.x/session)에 플래시하여 다음 요청 때 사용 가능하게 해줍니다.

```php
$request->flash();
```

`flashOnly`와 `flashExcept`는 입력값 일부만 세션에 플래시할 때 유용합니다. 비밀번호 등 민감한 정보를 세션에 남기지 않기 위해 사용할 수 있습니다.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리다이렉트

입력값을 세션에 플래시하고, 이전 페이지로 리다이렉트하고 싶다면 `withInput` 메서드를 리다이렉트와 함께 체이닝할 수 있습니다.

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값 가져오기

이전 요청에서 플래시된 입력값을 가져오려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출합니다. 이 값들은 [세션](/docs/12.x/session)에서 꺼내옵니다.

```php
$username = $request->old('username');
```

라라벨은 전역 `old` 헬퍼도 제공합니다. [Blade 템플릿](/docs/12.x/blade)에서 폼을 다시 채워줄 때는 이 헬퍼를 사용하는 것이 더욱 편리합니다. 만약 해당 입력값이 없다면 `null`을 반환합니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키 (Cookies)

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 값 가져오기

라라벨 프레임워크가 생성한 모든 쿠키는 암호화되어 있고, 인증 코드로 서명되어 있기 때문에 클라이언트에서 변경된 쿠키는 무효로 처리됩니다. 쿠키 값을 얻으려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화 (Input Trimming and Normalization)

기본적으로 Laravel은 `Illuminate\Foundation\Http\Middleware\TrimStrings`와 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 글로벌 미들웨어 스택에 포함하고 있습니다. 이 미들웨어들은 들어오는 모든 문자열 입력값을 자동으로 트리밍(trim)하며, 빈 문자열은 자동으로 `null`로 변환합니다. 덕분에 라우트나 컨트롤러에서 이러한 정규화를 따로 신경 쓰지 않아도 됩니다.

#### 입력값 정규화 비활성화

모든 요청에 대해 이 동작을 비활성화하고 싶으면, 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드를 호출해 두 미들웨어를 미들웨어 스택에서 제거하면 됩니다.

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

특정 요청에서만 문자열 트리밍/빈 문자열 변환을 비활성화하려면 `bootstrap/app.php` 파일에서 각각 `trimStrings`, `convertEmptyStringsToNull` 메서드를 사용하면 됩니다. 두 메서드 모두 클로저 배열을 인수로 받으며, 해당 클로저가 `true`를 반환하면 정규화 과정이 건너뜁니다.

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
### 업로드된 파일 가져오기 (Retrieving Uploaded Files)

업로드된 파일은 `Illuminate\Http\Request` 인스턴스에서 `file` 메서드나 동적 프로퍼티를 통해 가져올 수 있습니다. 반환되는 값은 PHP의 `SplFileInfo` 클래스를 확장한 `Illuminate\Http\UploadedFile`입니다. 여러 메서드를 통해 파일과 상호작용할 수 있습니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

파일이 요청에 존재하는지 확인하려면 `hasFile` 메서드를 사용하세요.

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 검증

파일이 존재하는지 외에도, `isValid` 메서드를 통해 업로드에 문제가 없었는지 검증할 수 있습니다.

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스에는 파일의 전체 경로나 확장자를 확인할 수 있는 여러 메서드가 있습니다. `extension` 메서드는 파일의 실제 내용을 기반으로 확장자를 추측하며, 클라이언트가 제공한 확장자와 다를 수 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에는 다양한 추가 메서드가 있습니다. 더 자세한 내용은 [클래스 API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장하기 (Storing Uploaded Files)

업로드된 파일을 저장하려면 보통 미리 설정된 [파일 시스템](/docs/12.x/filesystem) 중 하나를 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드 파일을 로컬/클라우드 저장소(예: Amazon S3)의 디스크로 이동시킵니다.

`store` 메서드는 파일이 저장될 경로를 파일 시스템의 루트 디렉터리 기준으로 지정하며, 파일 이름은 별도로 지정하지 않아도 자동으로 고유한 이름이 생성됩니다.

옵션으로 두 번째 인수에 사용할 디스크 이름을 넘길 수도 있습니다. 반환 값은 해당 디스크 루트에 대한 경로입니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 자동 생성하지 않고 직접 지정하고 싶으면, `storeAs` 메서드를 사용할 수 있습니다. 이 메서드는 경로, 파일명, 디스크명을 인수로 받습니다.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> 라라벨 파일 저장소에 대한 자세한 정보는 [파일 저장 문서](/docs/12.x/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정하기 (Configuring Trusted Proxies)

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행하는 경우, `url` 헬퍼로 HTTPS 링크가 생성되지 않는 현상을 볼 수 있습니다. 이는 로드 밸런서가 80번 포트로 트래픽을 포워딩하고, 애플리케이션이 해당 요청이 HTTPS 기반인지 알지 못하기 때문입니다.

이 문제를 해결하려면, 라라벨에 포함된 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화해, 신뢰할 수 있는 프록시 또는 로드 밸런서를 지정할 수 있습니다. 신뢰하는 프록시는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 이용해 설정해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰하는 프록시뿐 아니라, 신뢰할 수 있는 프록시 헤더도 설정할 수 있습니다.

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
> AWS Elastic Load Balancing을 사용하는 경우, `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`여야 합니다. 표준 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)의 `Forwarded` 헤더를 사용하는 로드 밸런서라면 `Request::HEADER_FORWARDED`를 사용해야 합니다. 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [프록시 신뢰 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기

Amazon AWS 등의 "클라우드" 로드 밸런서를 사용할 경우 실제 밸런서의 IP 주소를 알 수 없을 수 있습니다. 이럴 때는 `*`를 사용해 모든 프록시를 신뢰할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정하기 (Configuring Trusted Hosts)

기본적으로 라라벨은 HTTP 요청의 `Host` 헤더 내용과 상관없이 들어오는 모든 요청을 처리하고, 절대 URL을 자동 생성할 때 `Host` 값을 사용합니다.

일반적으로 Nginx, Apache와 같은 웹서버에서 요청을 특정 호스트네임에만 전달하도록 설정해야 합니다. 하지만 웹서버 설정 변경이 불가능하거나, 라라벨에서 지정된 호스트에만 응답하도록 제한하고 싶을 때는, `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화해야 합니다.

이 미들웨어를 사용하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 호출하세요. `at` 인수에 호스트네임(정규식)을 지정합니다. 일치하지 않는 요청은 거부됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$']);
})
```

기본적으로, 애플리케이션 URL의 서브도메인에서 오는 요청도 자동으로 신뢰합니다. 이 동작을 비활성화하려면 `subdomains` 인수를 사용하세요.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
})
```

신뢰할 호스트를 애플리케이션 설정 파일이나 DB에서 가져와야 할 경우, `at` 인수에 클로저를 지정할 수도 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```