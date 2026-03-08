# HTTP 요청 (HTTP Requests)

- [소개](#introduction)
- [요청과 상호작용하기](#interacting-with-the-request)
    - [요청 접근하기](#accessing-the-request)
    - [요청 경로, 호스트, 메서드](#request-path-and-method)
    - [요청 헤더](#request-headers)
    - [요청 IP 주소](#request-ip-address)
    - [콘텐츠 협상](#content-negotiation)
    - [PSR-7 요청](#psr7-requests)
- [입력값(Input)](#input)
    - [입력값 조회](#retrieving-input)
    - [입력값 존재 여부 확인](#input-presence)
    - [추가 입력값 병합](#merging-additional-input)
    - [이전 입력값(Old Input)](#old-input)
    - [쿠키](#cookies)
    - [입력값 트리밍 및 정규화](#input-trimming-and-normalization)
- [파일](#files)
    - [업로드된 파일 조회](#retrieving-uploaded-files)
    - [업로드된 파일 저장](#storing-uploaded-files)
- [신뢰할 수 있는 프록시 설정](#configuring-trusted-proxies)
- [신뢰할 수 있는 호스트 설정](#configuring-trusted-hosts)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel의 `Illuminate\Http\Request` 클래스는 현재 애플리케이션에서 처리 중인 HTTP 요청 객체와 상호작용할 수 있는 객체지향적인 방법을 제공합니다. 이를 통해 요청에 동봉된 입력값, 쿠키, 파일 등도 쉽게 조회할 수 있습니다.

<a name="interacting-with-the-request"></a>
## 요청과 상호작용하기 (Interacting With The Request)

<a name="accessing-the-request"></a>
### 요청 접근하기 (Accessing the Request)

현재 HTTP 요청 인스턴스를 의존성 주입(dependency injection)을 통해 얻으려면, 라우트 클로저나 컨트롤러 메서드에서 `Illuminate\Http\Request` 클래스를 타입힌트(type-hint) 하십시오. 라라벨 [서비스 컨테이너](/docs/master/container) 덕분에 자동으로 해당 인스턴스가 주입됩니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 새로운 사용자를 저장합니다.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // 사용자 저장...

        return redirect('/users');
    }
}
```

앞서 설명한 것처럼, 라우트 클로저에서도 `Illuminate\Http\Request` 클래스를 타입힌트하여 사용할 수 있습니다. 클로저가 실행될 때 서비스 컨테이너가 해당 요청 인스턴스를 주입합니다.

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```

<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입과 라우트 파라미터

컨트롤러 메서드에서 라우트 파라미터로부터 입력값을 받아야 하는 경우에는, 다른 의존성 항목들 뒤에 라우트 파라미터를 나열하면 됩니다. 예를 들어, 다음처럼 라우트를 정의했다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```

컨트롤러 메서드에서는 아래와 같이 `Illuminate\Http\Request`를 타입힌트하고, `id` 라우트 파라미터를 그대로 사용할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * 지정된 사용자를 업데이트합니다.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // 사용자 업데이트...

        return redirect('/users');
    }
}
```

<a name="request-path-and-method"></a>
### 요청 경로, 호스트, 메서드 (Request Path, Host, and Method)

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사할 수 있는 다양한 메서드를 제공합니다. 이 클래스는 또한 `Symfony\Component\HttpFoundation\Request` 클래스를 확장하고 있습니다. 아래에서 주요 메서드 몇 가지를 살펴보겠습니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로(path) 조회

`path` 메서드는 요청의 경로 정보를 반환합니다. 예를 들어, 요청이 `http://example.com/foo/bar`에 왔다면, `path` 메서드는 `foo/bar`를 반환합니다.

```php
$uri = $request->path();
```

<a name="inspecting-the-request-path"></a>
#### 요청 경로/라우트 검사

`is` 메서드를 사용하면, 요청 경로가 지정한 패턴과 일치하는지 확인할 수 있습니다. 이 메서드에서 `*` 문자를 와일드카드로 사용할 수 있습니다.

```php
if ($request->is('admin/*')) {
    // ...
}
```

`routeIs` 메서드를 사용하면, 현재 요청이 [이름이 지정된 라우트](/docs/master/routing#named-routes)와 일치하는지 확인할 수 있습니다.

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```

<a name="retrieving-the-request-url"></a>
#### 요청 URL 조회

들어오는 요청의 전체 URL을 조회하려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리 스트링을 제외한 URL을, `fullUrl`은 쿼리 스트링까지 포함한 URL을 반환합니다.

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```

현재 URL에 쿼리 스트링 데이터를 추가하려면 `fullUrlWithQuery` 메서드를 사용할 수 있습니다. 이 메서드는 현재 쿼리 스트링에 주어진 배열을 병합합니다.

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```

특정 쿼리 스트링 파라미터를 제외한 현재 URL을 얻고 싶다면 `fullUrlWithoutQuery` 메서드를 사용할 수 있습니다.

```php
$request->fullUrlWithoutQuery(['type']);
```

<a name="retrieving-the-request-host"></a>
#### 요청 호스트(host) 조회

요청의 "호스트" 값을 얻으려면 `host`, `httpHost`, `schemeAndHttpHost` 메서드를 사용할 수 있습니다.

```php
$request->host();
$request->httpHost();
$request->schemeAndHttpHost();
```

<a name="retrieving-the-request-method"></a>
#### 요청 메서드(method) 조회

`method` 메서드는 요청의 HTTP 메서드(verb)를 반환합니다. 또한, `isMethod` 메서드를 사용하여 요청의 HTTP 메서드가 특정 값과 일치하는지 확인할 수 있습니다.

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```

<a name="request-headers"></a>
### 요청 헤더 (Request Headers)

`Illuminate\Http\Request` 인스턴스의 `header` 메서드를 사용하여 요청 헤더를 조회할 수 있습니다. 해당 헤더가 요청에 없으면 `null`이 반환됩니다. 그러나 이 메서드는 두 번째 인수로 기본값을 받을 수 있으니, 헤더가 없을 경우 기본값이 반환됩니다.

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```

`hasHeader` 메서드를 사용하면 요청에 특정 헤더가 포함되어 있는지 확인할 수 있습니다.

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```

편의를 위해, `bearerToken` 메서드를 사용하면 `Authorization` 헤더에서 bearer 토큰을 조회할 수 있습니다. 만약 해당 헤더가 없으면 빈 문자열이 반환됩니다.

```php
$token = $request->bearerToken();
```

<a name="request-ip-address"></a>
### 요청 IP 주소 (Request IP Address)

`ip` 메서드를 사용하면 요청을 보낸 클라이언트의 IP 주소를 조회할 수 있습니다.

```php
$ipAddress = $request->ip();
```

프록시 서버에 의해 전달된 모든 클라이언트 IP 주소 배열이 필요하다면 `ips` 메서드를 사용하세요. 배열의 마지막 요소가 "원본" 클라이언트 IP가 됩니다.

```php
$ipAddresses = $request->ips();
```

일반적으로 IP 주소는 신뢰할 수 없는, 사용자가 제어 가능한 입력값이므로 참고용으로만 사용하는 것이 좋습니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상 (Content Negotiation)

Laravel에서는 요청의 `Accept` 헤더를 통해 요청된 콘텐츠 타입을 검사할 수 있는 여러 메서드를 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청이 수용 가능한 모든 콘텐츠 타입을 배열로 반환합니다.

```php
$contentTypes = $request->getAcceptableContentTypes();
```

`accepts` 메서드는 콘텐츠 타입 배열을 받아, 그 중 하나라도 요청에서 수용 가능한 타입이면 `true`를 반환하고, 그렇지 않으면 `false`를 반환합니다.

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```

`prefers` 메서드를 사용하면, 주어진 배열 중에서 요청에서 가장 우선순위가 높은 콘텐츠 타입을 확인할 수 있습니다. 만약 전달된 타입 중 아무것도 요청에서 허용되지 않으면 `null`이 반환됩니다.

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```

많은 애플리케이션이 HTML이나 JSON만 제공하는 경우, `expectsJson` 메서드를 통해 현재 요청이 JSON 응답을 기대하는지 빠르게 확인할 수 있습니다.

```php
if ($request->expectsJson()) {
    // ...
}
```

<a name="psr7-requests"></a>
### PSR-7 요청 (PSR-7 Requests)

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 HTTP 메시지(요청 및 응답)에 대한 인터페이스를 명시합니다. 만약 Laravel 요청 대신 PSR-7 요청 인스턴스를 얻고 싶다면, 몇 가지 라이브러리를 먼저 설치해야 합니다. Laravel은 *Symfony HTTP Message Bridge* 컴포넌트를 이용해 일반 Laravel 요청/응답을 PSR-7 호환 구현체로 변환합니다.

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```

이러한 라이브러리 설치 후에는 요청 인터페이스를 라우트 클로저나 컨트롤러 메서드에서 타입힌트하여 PSR-7 요청을 사용할 수 있습니다.

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```

> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 프레임워크가 이를 자동으로 Laravel 응답 인스턴스로 변환하여 출력합니다.

<a name="input"></a>
## 입력값(Input) (Input)

<a name="retrieving-input"></a>
### 입력값 조회 (Retrieving Input)

<a name="retrieving-all-input-data"></a>
#### 모든 입력값 데이터 조회

입력값 전체를 `array`로 가져오려면 `all` 메서드를 사용하세요. 이 메서드는 들어오는 요청이 HTML 폼이든 XHR 요청이든 상관없이 사용할 수 있습니다.

```php
$input = $request->all();
```

`collect` 메서드를 사용하면, 모든 입력값을 [컬렉션](/docs/master/collections)으로도 가져올 수 있습니다.

```php
$input = $request->collect();
```

또한, 특정 입력값 배열만 컬렉션으로 가져올 수도 있습니다.

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```

<a name="retrieving-an-input-value"></a>
#### 단일 입력값 조회

몇 가지 간단한 메서드를 통해 `Illuminate\Http\Request` 인스턴스에서 HTTP 메서드 종류와 상관없이 사용자 입력을 조회할 수 있습니다. `input` 메서드는 어떤 HTTP 메서드이든 입력값을 가져올 수 있습니다.

```php
$name = $request->input('name');
```

두 번째 인수로 기본값을 전달할 수 있습니다. 요청에 해당 입력값이 없으면 이 값을 반환받습니다.

```php
$name = $request->input('name', 'Sally');
```

입력폼에 배열 데이터가 있다면, "dot" 표기법으로 배열 내 값을 조회할 수 있습니다.

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```

인수를 전달하지 않고 `input` 메서드를 호출하면 입력값 전체를 연관 배열로 반환받습니다.

```php
$input = $request->input();
```

<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 스트링에서 입력값 조회

`input` 메서드는 전체 요청 페이로드(쿼리 스트링 포함)에서 값을 조회하지만, 쿼리 스트링에서만 값을 얻으려면 `query` 메서드를 사용합니다.

```php
$name = $request->query('name');
```

요청에 해당 쿼리 스트링 값이 없을 경우 두 번째 인수로 기본값을 받을 수 있습니다.

```php
$name = $request->query('name', 'Helen');
```

인수 없이 `query` 메서드를 사용하면 모든 쿼리 스트링 값을 연관 배열로 반환합니다.

```php
$query = $request->query();
```

<a name="retrieving-json-input-values"></a>
#### JSON 입력값 조회

애플리케이션에 JSON 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`으로 올바르게 설정되어 있다면, `input` 메서드를 통해 JSON 데이터에 접근할 수 있습니다. JSON 배열/객체 내부의 값도 "dot" 표기법으로 조회할 수 있습니다.

```php
$name = $request->input('user.name');
```

<a name="retrieving-stringable-input-values"></a>
#### Stringable 입력값 조회

입력 데이터를 기본 `string` 타입 대신 [Illuminate\Support\Stringable](/docs/master/strings) 인스턴스로 받아오려면 `string` 메서드를 사용할 수 있습니다.

```php
$name = $request->string('name')->trim();
```

<a name="retrieving-integer-input-values"></a>
#### 정수(integer) 입력값 조회

입력값을 정수형으로 받고 싶으면 `integer` 메서드를 활용할 수 있습니다. 이 메서드는 입력값을 정수로 변환하려 시도하며, 값이 없거나 변환에 실패하면 지정한 기본값을 반환합니다. 주로 페이지네이션이나 수치 입력에 유용합니다.

```php
$perPage = $request->integer('per_page');
```

<a name="retrieving-boolean-input-values"></a>
#### 불리언(boolean) 입력값 조회

HTML의 체크박스처럼, 실제로는 문자열이지만 "truthy"한 값을 받는 경우가 많습니다(예: "true", "on" 등). `boolean` 메서드는 이런 값을 실제 불리언으로 변환합니다. 이 메서드는 1, "1", true, "true", "on", "yes"에 대해 `true`를 반환하며, 그 외에는 모두 `false`를 반환합니다.

```php
$archived = $request->boolean('archived');
```

<a name="retrieving-array-input-values"></a>
#### 배열 입력값 조회

배열 형태의 입력값은 `array` 메서드로 조회할 수 있습니다. 이 메서드는 해당 입력값의 존재 여부와 상관없이 항상 배열로 변환해 반환합니다. 값이 없으면 빈 배열이 반환됩니다.

```php
$versions = $request->array('versions');
```

<a name="retrieving-date-input-values"></a>
#### 날짜 입력값 조회

날짜/시간 데이터는 편리하게 `date` 메서드로 [Carbon](https://carbon.nesbot.com/) 인스턴스로 변환해 받을 수 있습니다. 값이 없으면 `null`을 반환합니다.

```php
$birthday = $request->date('birthday');
```

`date` 메서드는 두 번째 및 세 번째 인수로, 각각 날짜 형식과 타임존을 지정할 수 있습니다.

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```

입력값이 존재하지만 형식이 잘못된 경우, `InvalidArgumentException` 예외가 발생하므로 메서드 호출 전 입력값을 유효성 검증하는 것이 좋습니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력값 조회

[PHP enum](https://www.php.net/manual/en/language.types.enumerations.php)에 해당하는 입력값도 조회할 수 있습니다. 지정한 이름의 입력값이 없거나 enum의 백킹값과 일치하지 않으면 `null`이 반환됩니다. `enum` 메서드는 첫 번째 인수로 입력값 이름, 두 번째 인수로 enum 클래스를 받습니다.

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```

값이 없거나 잘못된 경우 반환할 기본값을 세 번째 인수로 지정할 수도 있습니다.

```php
$status = $request->enum('status', Status::class, Status::Pending);
```

입력값이 enum의 배열일 경우에는 `enums` 메서드로 enum 인스턴스의 배열을 얻을 수 있습니다.

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```

<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 속성(Dynamic Property)으로 입력값 조회

`Illuminate\Http\Request` 인스턴스에서는 동적 속성을 사용해서도 입력값에 접근할 수 있습니다. 예를 들어, 폼 필드에 `name`이 있다면 아래처럼 해당 값을 조회할 수 있습니다.

```php
$name = $request->name;
```

동적 속성을 사용할 때 Laravel은 먼저 요청 페이로드에서 값을 찾고, 없으면 매칭된 라우트 파라미터에서 값을 찾습니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력값 일부만 조회

입력값 중 일부만 추출하려면 `only` 및 `except` 메서드를 사용할 수 있습니다. 이들 메서드는 배열 또는 동적으로 구분되는 인수를 받을 수 있습니다.

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```

> [!WARNING]
> `only` 메서드는 요청에 실제 존재하는 key/value 쌍만 반환하며, 요청에 없는 key는 절대로 반환하지 않습니다.

<a name="input-presence"></a>
### 입력값 존재 여부 확인 (Input Presence)

`has` 메서드는 요청에 특정 값이 존재하는지 확인합니다. 값이 존재하면 `true`를 반환합니다.

```php
if ($request->has('name')) {
    // ...
}
```

배열을 전달하면, 모든 값이 존재하는지 검사합니다.

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```

`hasAny` 메서드는 지정한 값 중 하나라도 존재하면 `true`를 반환합니다.

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```

`whenHas` 메서드는 값이 존재할 때만 전달한 클로저를 실행합니다.

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 넘기면, 값이 없을 때 해당 클로저가 실행됩니다.

```php
$request->whenHas('name', function (string $input) {
    // "name" 값이 존재...
}, function () {
    // "name" 값이 없음...
});
```

요청에 값이 존재하면서 비어 있지 않은 경우를 확인하려면 `filled` 메서드를 사용하세요.

```php
if ($request->filled('name')) {
    // ...
}
```

값이 존재하지 않거나 빈 문자열일 때는 `isNotFilled` 메서드로 확인할 수 있습니다.

```php
if ($request->isNotFilled('name')) {
    // ...
}
```

배열을 전달하면, 배열의 모든 값이 존재하지 않거나 비어 있는지 검사합니다.

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```

`anyFilled` 메서드는 전달한 값들 중 하나라도 비어 있지 않으면 `true`를 반환합니다.

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```

`whenFilled` 메서드는 값이 존재하며 비어 있지 않을 때만 클로저를 실행합니다.

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```

두 번째 클로저를 전달하면, 값이 "filled"되지 않았을 경우에도 처리할 수 있습니다.

```php
$request->whenFilled('name', function (string $input) {
    // "name" 값이 채워져 있음...
}, function () {
    // "name" 값이 없음 또는 비어 있음...
});
```

특정 key가 요청에 없을 경우에는 `missing`, `whenMissing` 메서드를 사용할 수 있습니다.

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // "name" 값이 없음...
}, function () {
    // "name" 값이 존재...
});
```

<a name="merging-additional-input"></a>
### 추가 입력값 병합 (Merging Additional Input)

입력값에 추가 데이터를 수동으로 병합할 필요가 있을 때는 `merge` 메서드를 사용할 수 있습니다. 이미 요청에 존재하는 입력값이 있으면, `merge` 메서드에 전달한 값으로 덮어씌워집니다.

```php
$request->merge(['votes' => 0]);
```

`mergeIfMissing` 메서드는 요청의 입력 데이터에 해당 key가 없을 때만 데이터를 병합합니다.

```php
$request->mergeIfMissing(['votes' => 0]);
```

<a name="old-input"></a>
### 이전 입력값(Old Input)

Laravel은 요청 간에 입력값을 유지할 수 있도록 지원합니다. 이 기능은 주로 유효성 검증 에러 발생 시 폼을 다시 채우는 데 유용합니다. 참고로, Laravel이 제공하는 [유효성 검증 기능](/docs/master/validation)을 사용할 때는 세션 입력 플래시 메서드를 직접 호출할 필요가 없으며 내장 유효성 검증 시 자동 호출됩니다.

<a name="flashing-input-to-the-session"></a>
#### 입력값을 세션에 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 요청의 입력값을 [세션](/docs/master/session)에 플래시(저장)해서 다음 요청 시 사용할 수 있게 합니다.

```php
$request->flash();
```

`flashOnly`와 `flashExcept` 메서드를 통해 입력값의 일부만 세션에 플래시할 수도 있습니다. 비밀번호처럼 민감한 정보는 세션에 남기지 않기 위해 해당 API를 활용하세요.

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```

<a name="flashing-input-then-redirecting"></a>
#### 입력값 플래시 후 리다이렉트

입력값을 세션에 플래시하고 바로 이전 페이지로 리다이렉트하는 경우가 많으므로, `withInput` 메서드를 통해 간단하게 체이닝할 수 있습니다.

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```

<a name="retrieving-old-input"></a>
#### 이전 입력값(old input) 조회

이전 요청에서 플래시된 입력값을 얻으려면, `Illuminate\Http\Request` 인스턴스의 `old` 메서드를 호출하면 됩니다. 이 메서드는 [세션](/docs/master/session)에서 이전 입력 데이터를 꺼냅니다.

```php
$username = $request->old('username');
```

또한, 글로벌 `old` 헬퍼가 제공되므로, [Blade 템플릿](/docs/master/blade)에서 이전 입력값으로 폼을 다시 채울 때 더욱 간편하게 사용할 수 있습니다. 해당 필드에 이전 입력값이 없다면 `null`이 반환됩니다.

```blade
<input type="text" name="username" value="{{ old('username') }}">
```

<a name="cookies"></a>
### 쿠키 (Cookies)

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 조회

Laravel 프레임워크에서 생성된 모든 쿠키는 암호화되어 있으며, 인증 코드로 서명되어 있습니다. 이 덕분에 사용자가 쿠키 값을 변경했을 경우 쿠키는 무효화됩니다. 쿠키 값을 요청에서 얻으려면 `Illuminate\Http\Request` 인스턴스의 `cookie` 메서드를 사용하세요.

```php
$value = $request->cookie('name');
```

<a name="input-trimming-and-normalization"></a>
## 입력값 트리밍 및 정규화 (Input Trimming and Normalization)

Laravel은 기본적으로 `Illuminate\Foundation\Http\Middleware\TrimStrings` 및 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 애플리케이션의 전역 미들웨어 스택에 포함하고 있습니다. 이 미들웨어들은 들어오는 모든 문자열 필드를 자동으로 트리밍하며, 빈 문자열 필드는 `null`로 변환합니다. 덕분에 컨트롤러나 라우트에서 직접 그런 처리를 따로 해줄 필요가 없습니다.

#### 입력 정규화 비활성화

이 처리를 모든 요청에 대해 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드로 두 미들웨어를 제거하면 됩니다.

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

특정 요청에 대해서만 문자열 트리밍이나 빈 문자열 변환을 건너뛰고 싶다면, `bootstrap/app.php` 파일 내에서 `trimStrings` 및 `convertEmptyStringsToNull` 미들웨어 메서드를 사용할 수 있습니다. 각각은 클로저 배열을 받아, `true` 또는 `false`를 반환해 정규화 건너뛰기를 제어합니다.

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
### 업로드된 파일 조회 (Retrieving Uploaded Files)

`Illuminate\Http\Request` 인스턴스에서 `file` 메서드 또는 동적 속성을 통해 업로드된 파일을 조회할 수 있습니다. `file` 메서드는 PHP의 `SplFileInfo`를 확장한 `Illuminate\Http\UploadedFile` 인스턴스를 반환하며, 파일 조작에 다양한 메서드를 제공합니다.

```php
$file = $request->file('photo');

$file = $request->photo;
```

요청에 해당 파일이 포함되어 있는지 확인하려면 `hasFile` 메서드를 사용할 수 있습니다.

```php
if ($request->hasFile('photo')) {
    // ...
}
```

<a name="validating-successful-uploads"></a>
#### 업로드 성공 여부 검증

파일 존재 여부 뿐만 아니라, 업로드 과정에서 문제가 없었는지도 `isValid` 메서드로 확인 가능합니다.

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```

<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스에는 파일의 전체 경로나 확장자를 확인할 수 있는 메서드도 있습니다. `extension` 메서드는 파일 내용을 바탕으로 확장자를 추정하며, 이 확장자는 클라이언트가 지정한 확장자와 다를 수 있습니다.

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```

<a name="other-file-methods"></a>
#### 기타 파일 메서드

`UploadedFile` 인스턴스에는 그 외에도 다양한 메서드가 있습니다. 해당 클래스에 대한 더 자세한 내용은 [API 문서](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php)를 참고하세요.

<a name="storing-uploaded-files"></a>
### 업로드된 파일 저장 (Storing Uploaded Files)

업로드된 파일을 저장하려면, 일반적으로 [파일시스템(filesystems)](/docs/master/filesystem)에 설정된 디스크 중 하나를 사용합니다. `UploadedFile` 클래스의 `store` 메서드는 업로드된 파일을 원하는 위치(디스크의 루트로부터 상대 경로)로 이동시킵니다. 이 경로에는 파일명을 포함하지 않으며, 고유한 식별자가 자동으로 파일명으로 지정됩니다.

`store` 메서드는 파일을 저장할 경로(루트에서 상대 경로)를 첫 번째 인수로, 사용할 디스크명을 두 번째 인수로 받을 수 있습니다. 반환값은 디스크 루트로부터의 파일 경로입니다.

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```

파일명을 직접 지정해서 저장하려면 `storeAs` 메서드를 사용하세요. 경로, 파일명, 디스크명을 인수로 받습니다.

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```

> [!NOTE]
> Laravel의 파일 저장에 관한 더 많은 정보는 [파일 저장소 문서](/docs/master/filesystem)를 참고하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 설정 (Configuring Trusted Proxies)

로드밸런서가 TLS/SSL 인증서를 종료(Offload)한 뒤 애플리케이션을 구동할 경우, `url` 헬퍼를 사용할 때 HTTPS 링크가 생성되지 않을 수 있습니다. 이는 종종 로드밸런서가 80번 포트로 트래픽을 전달하면서 애플리케이션이 보안 연결 상태임을 인지하지 못할 때 발생합니다.

이 문제를 해결하려면, 라라벨 애플리케이션에 포함된 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화하세요. 이를 통해 신뢰할 수 있는 로드밸런서/프록시를 설정할 수 있습니다. 신뢰할 프록시는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 통해 지정합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```

신뢰할 수 있는 프록시 설정 외에도, 어떤 프록시 헤더를 신뢰할지 추가로 지정할 수 있습니다.

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
> AWS Elastic Load Balancing을 사용하는 경우 `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`여야 합니다. 로드밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)에 명시된 표준 `Forwarded` 헤더를 사용할 경우, `headers` 값은 `Request::HEADER_FORWARDED`여야 합니다. `headers`에 사용할 수 있는 상수에 대한 더 자세한 정보는 Symfony의 [신뢰할 수 있는 프록시 문서](https://symfony.com/doc/current/deployment/proxies.html)를 참고하세요.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기

Amazon AWS 등 클라우드 로드밸런서 공급자는 실제 밸런서의 IP를 알 수 없는 경우가 많으므로, 이럴 땐 `*`로 모든 프록시를 신뢰하도록 설정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```

<a name="configuring-trusted-hosts"></a>
## 신뢰할 수 있는 호스트 설정 (Configuring Trusted Hosts)

Laravel은 기본적으로 들어오는 HTTP 요청의 `Host` 헤더 값에 상관없이 모든 요청에 응답합니다. 뿐만 아니라, 절대 URL을 생성할 때도 `Host` 헤더의 값을 사용합니다.

일반적으로는 Nginx나 Apache 같은 웹 서버에서 허용할 호스트명을 명시하여 요청을 제한해야 하지만, 웹 서버를 직접 구성할 수 없을 때 Laravel에게만 특정 호스트에 응답하도록 제한할 수 있습니다. 이를 위해서는 `Illuminate\Http\Middleware\TrustHosts` 미들웨어를 활성화해야 합니다.

`TrustHosts` 미들웨어는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 메서드를 호출하여 활성화할 수 있습니다. 이 메서드의 `at` 인수에, 애플리케이션이 응답해야 할 호스트명을 정규 표현식으로 지정할 수 있습니다. 다른 `Host` 헤더의 요청은 거절됩니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$']);
})
```

기본적으로 애플리케이션 URL의 서브도메인에서 오는 요청도 자동으로 허용됩니다. 이 동작을 끄고 싶다면 `subdomains` 인수를 사용할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
})
```

신뢰할 호스트를 결정하기 위해 애플리케이션의 설정 파일이나 데이터베이스를 조회해야 하는 경우, `at` 인수에 클로저를 전달할 수도 있습니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```