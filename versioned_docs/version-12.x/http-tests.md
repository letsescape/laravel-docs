# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청 보내기](#making-requests)
    - [요청 헤더 커스터마이징](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [Fluent JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [라우트 캐싱](#caching-routes)
- [사용 가능한 Assertions](#available-assertions)
    - [응답 Assertions](#response-assertions)
    - [인증 Assertions](#authentication-assertions)
    - [유효성 검증 Assertions](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 그 응답을 검사할 수 있도록 매우 직관적인(Fluent) API를 제공합니다. 예를 들어 아래의 기능 테스트(feature test)를 살펴보겠습니다.

```php tab=Pest
<?php

test('the application returns a successful response', function () {
    $response = $this->get('/');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

`get` 메서드는 애플리케이션에 `GET` 요청을 보내며, `assertStatus` 메서드는 반환된 응답이 지정한 HTTP 상태 코드를 가지고 있는지 검증(assert)합니다.  
이러한 기본적인 검증 외에도 Laravel은 응답 헤더, 콘텐츠, JSON 구조 등을 검사할 수 있는 다양한 assertion을 제공합니다.

<a name="making-requests"></a>
## 요청 보내기

애플리케이션에 요청을 보내기 위해 테스트 코드에서 `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 이러한 메서드는 실제 네트워크 HTTP 요청을 보내는 것이 아니라, 내부적으로 전체 네트워크 요청을 **시뮬레이션**합니다.

테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하는 대신 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 객체는 애플리케이션 응답을 검사할 수 있도록 [다양한 assertion](#available-assertions)을 제공합니다.

```php tab=Pest
<?php

test('basic request', function () {
    $response = $this->get('/');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_a_basic_request(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

일반적으로 하나의 테스트에서는 **한 번의 요청만 수행하는 것이 좋습니다.**  
하나의 테스트 메서드에서 여러 요청을 실행하면 예상하지 못한 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해 테스트 실행 시 CSRF Middleware는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 커스터마이징

`withHeaders` 메서드를 사용하면 애플리케이션으로 요청을 보내기 전에 요청 헤더를 커스터마이징할 수 있습니다. 이 메서드를 통해 원하는 사용자 정의 헤더를 추가할 수 있습니다.

```php tab=Pest
<?php

test('interacting with headers', function () {
    $response = $this->withHeaders([
        'X-Header' => 'Value',
    ])->post('/user', ['name' => 'Sally']);

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_interacting_with_headers(): void
    {
        $response = $this->withHeaders([
            'X-Header' => 'Value',
        ])->post('/user', ['name' => 'Sally']);

        $response->assertStatus(201);
    }
}
```

<a name="cookies"></a>
### 쿠키

`withCookie` 또는 `withCookies` 메서드를 사용하여 요청을 보내기 전에 쿠키 값을 설정할 수 있습니다.

- `withCookie`는 쿠키 이름과 값을 인수로 받습니다.
- `withCookies`는 이름 / 값 쌍의 배열을 받습니다.

```php tab=Pest
<?php

test('interacting with cookies', function () {
    $response = $this->withCookie('color', 'blue')->get('/');

    $response = $this->withCookies([
        'color' => 'blue',
        'name' => 'Taylor',
    ])->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_cookies(): void
    {
        $response = $this->withCookie('color', 'blue')->get('/');

        $response = $this->withCookies([
            'color' => 'blue',
            'name' => 'Taylor',
        ])->get('/');

        //
    }
}
```

<a name="session-and-authentication"></a>
### 세션 / 인증

Laravel은 HTTP 테스트 중 세션(session)을 다룰 수 있는 여러 헬퍼(helper)를 제공합니다.

먼저 `withSession` 메서드를 사용하여 세션 데이터를 배열 형태로 설정할 수 있습니다. 이는 애플리케이션에 요청을 보내기 전에 세션에 데이터를 미리 로드할 때 유용합니다.

```php tab=Pest
<?php

test('interacting with the session', function () {
    $response = $this->withSession(['banned' => false])->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_the_session(): void
    {
        $response = $this->withSession(['banned' => false])->get('/');

        //
    }
}
```

Laravel의 세션은 일반적으로 **현재 인증된 사용자 상태를 유지**하는 데 사용됩니다.  
따라서 `actingAs` 헬퍼 메서드를 사용하면 특정 사용자를 현재 사용자로 쉽게 인증할 수 있습니다.

예를 들어 [모델 팩토리](/docs/12.x/eloquent-factories)를 사용하여 사용자를 생성하고 인증할 수 있습니다.

```php tab=Pest
<?php

use App\Models\User;

test('an action that requires authentication', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->withSession(['banned' => false])
        ->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_an_action_that_requires_authentication(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
            ->withSession(['banned' => false])
            ->get('/');

        //
    }
}
```

`actingAs` 메서드의 두 번째 인수로 guard 이름을 전달하여 어떤 guard를 사용할지 지정할 수도 있습니다.  
이렇게 지정된 guard는 테스트 실행 동안 기본 guard로 설정됩니다.

```php
$this->actingAs($user, 'web');
```

요청이 **인증되지 않은 상태임을 보장**하려면 `actingAsGuest` 메서드를 사용할 수 있습니다.

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
### 응답 디버깅

테스트 요청을 보낸 후 `dump`, `dumpHeaders`, `dumpSession` 메서드를 사용하여 응답 내용을 확인하고 디버깅할 수 있습니다.

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dump();
    $response->dumpHeaders();
    $response->dumpSession();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->dump();
        $response->dumpHeaders();
        $response->dumpSession();
    }
}
```

또는 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용하면 응답 정보를 출력한 뒤 실행을 중단할 수 있습니다.

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dd();
    $response->ddHeaders();
    $response->ddBody();
    $response->ddJson();
    $response->ddSession();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->dd();
        $response->ddHeaders();
        $response->ddBody();
        $response->ddJson();
        $response->ddSession();
    }
}
```

<a name="exception-handling"></a>
### 예외 처리

때때로 애플리케이션이 특정 예외를 발생시키는지 테스트해야 할 수 있습니다. 이를 위해 `Exceptions` facade를 사용하여 예외 핸들러를 **fake** 처리할 수 있습니다.

예외 핸들러를 fake 처리한 뒤 `assertReported` 및 `assertNotReported` 메서드를 사용하여 요청 중 발생한 예외를 검증할 수 있습니다.

```php tab=Pest
<?php

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;

test('exception is thrown', function () {
    Exceptions::fake();

    $response = $this->get('/order/1');

    // Assert an exception was thrown...
    Exceptions::assertReported(InvalidOrderException::class);

    // Assert against the exception...
    Exceptions::assertReported(function (InvalidOrderException $e) {
        return $e->getMessage() === 'The order was invalid.';
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_exception_is_thrown(): void
    {
        Exceptions::fake();

        $response = $this->get('/');

        // Assert an exception was thrown...
        Exceptions::assertReported(InvalidOrderException::class);

        // Assert against the exception...
        Exceptions::assertReported(function (InvalidOrderException $e) {
            return $e->getMessage() === 'The order was invalid.';
        });
    }
}
```

요청 중 특정 예외가 발생하지 않았음을 검증하려면 `assertNotReported` 또는 `assertNothingReported` 메서드를 사용할 수 있습니다.

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

특정 요청에서 예외 처리를 완전히 비활성화하려면 요청을 보내기 전에 `withoutExceptionHandling` 메서드를 호출하면 됩니다.

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한 PHP 언어나 애플리케이션이 사용하는 라이브러리에서 **deprecated(더 이상 사용 권장되지 않는 기능)**이 사용되지 않는지 확인하려면 `withoutDeprecationHandling` 메서드를 사용할 수 있습니다.  

이 기능을 사용하면 deprecated 경고가 예외로 변환되어 테스트가 실패하게 됩니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메서드는 특정 클로저 내부의 코드가 지정된 타입의 예외를 발생시키는지 검증하는 데 사용됩니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

발생한 예외를 직접 검사하려면 두 번째 인수로 클로저를 전달할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow` 메서드는 클로저 내부 코드가 **어떠한 예외도 발생시키지 않는지** 검증할 때 사용합니다.

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API와 그 응답을 테스트하기 위한 여러 헬퍼를 제공합니다.

예를 들어 `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 사용하여 다양한 HTTP 메서드로 JSON 요청을 보낼 수 있습니다.

데이터와 헤더도 쉽게 전달할 수 있습니다. 아래 예제에서는 `/api/user` 엔드포인트로 `POST` 요청을 보내고 예상되는 JSON 응답을 검증합니다.

```php tab=Pest
<?php

test('making an api request', function () {
    $response = $this->postJson('/api/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertJson([
            'created' => true,
        ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_making_an_api_request(): void
    {
        $response = $this->postJson('/api/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJson([
                'created' => true,
            ]);
    }
}
```

또한 JSON 응답 데이터는 응답 객체에서 **배열처럼 접근**할 수 있습니다. 이를 통해 JSON 응답 내부의 개별 값을 쉽게 검사할 수 있습니다.

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여 지정한 배열이 JSON 응답 내부에 존재하는지 확인합니다.  
> 따라서 JSON 응답에 다른 속성이 추가로 존재하더라도, 지정한 조각(fragment)이 포함되어 있으면 테스트는 통과합니다.