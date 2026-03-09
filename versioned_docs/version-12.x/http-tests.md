# HTTP 테스트 (HTTP Tests)

- [소개](#introduction)
- [요청하기](#making-requests)
    - [요청 헤더 사용자 지정](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션/인증](#session-and-authentication)
    - [디버깅 응답](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유창한 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [Blade 및 구성요소 렌더링](#rendering-blade-and-components)
- [라우트 캐싱](#caching-routes)
- [사용 가능한 어설션](#available-assertions)
    - [응답 주장](#response-assertions)
    - [인증 어설션](#authentication-assertions)
    - [검증 주장](#validation-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel는 애플리케이션에 HTTP 요청을 보내고 응답을 검사하기 위해 매우 유창한 API를 제공합니다. 예를 들어 아래에 정의된 기능 테스트를 살펴보세요.

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

`get` 메서드는 애플리케이션에 `GET` 요청을 보내는 반면, `assertStatus` 메서드는 반환된 응답에 지정된 HTTP 상태 코드가 있어야 한다고 어설션합니다. 이 간단한 어설션 외에도 Laravel에는 응답 헤더, 콘텐츠, JSON 구조 등을 검사하기 위한 다양한 어설션도 포함되어 있습니다.

<a name="making-requests"></a>
## 요청하기 (Making Requests)

애플리케이션에 요청하려면 테스트 내에서 `get`, `post`, `put`, `patch` 또는 `delete` 메서드를 호출할 수 있습니다. 이러한 메서드는 실제로 애플리케이션에 "실제" HTTP 요청을 발행하지 않습니다. 대신 전체 네트워크 요청이 내부적으로 시뮬레이션됩니다.

`Illuminate\Http\Response` 인스턴스를 반환하는 대신 테스트 요청 메서드는 애플리케이션의 응답을 검사할 수 있는 [다양한 유용한 어설션](#available-assertions)을 제공하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다.

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

일반적으로 각 테스트는 애플리케이션에 대해 하나의 요청만 수행해야 합니다. 단일 테스트 메서드 내에서 여러 요청이 실행되면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해 테스트를 실행할 때 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 사용자 지정

요청이 애플리케이션으로 전송되기 전에 `withHeaders` 메소드를 사용하여 요청 헤더를 사용자 지정할 수 있습니다. 이 방법을 사용하면 요청에 원하는 사용자 지정 헤더를 추가할 수 있습니다.

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

요청하기 전에 `withCookie` 또는 `withCookies` 메소드를 사용하여 쿠키 값을 설정할 수 있습니다. `withCookie` 메서드는 쿠키 이름과 값을 두 개의 인수로 받아들이는 반면, `withCookies` 메서드는 이름/값 쌍의 배열을 받아들입니다.

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
### 세션/인증

Laravel는 HTTP 테스트에 세션과 상호 작용하기 위한 여러 도우미를 제공합니다. 먼저, `withSession` 메소드를 사용하여 세션 데이터를 주어진 배열로 설정할 수 있습니다. 이는 애플리케이션에 요청을 보내기 전에 세션에 데이터를 로드하는 데 유용합니다.

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

Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서 `actingAs` 도우미 메서드는 지정된 사용자를 현재 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, [모델 팩토리](/docs/12.x/eloquent-factories)를 사용하여 사용자를 생성하고 인증할 수 있습니다.

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

가드 이름을 `actingAs` 메소드의 두 번째 인수로 전달하여 특정 사용자를 인증하는 데 어떤 가드를 사용해야 하는지 지정할 수도 있습니다. `actingAs` 메서드에 제공되는 가드도 테스트 기간 동안 기본 가드가 됩니다.

```php
$this->actingAs($user, 'web');
```

요청이 인증되지 않았는지 확인하려면 `actingAsGuest` 메소드를 사용할 수 있습니다.

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
### 디버깅 응답

애플리케이션에 테스트 요청을 한 후 `dump`, `dumpHeaders` 및 `dumpSession` 메서드를 사용하여 응답 내용을 검사하고 디버그할 수 있습니다.

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

또는 `dd`, `ddHeaders`, `ddBody`, `ddJson` 및 `ddSession` 메서드를 사용하여 응답에 대한 정보를 덤프한 다음 실행을 중지할 수 있습니다.

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

때로는 애플리케이션이 특정 예외를 발생시키고 있는지 테스트해야 할 수도 있습니다. 이를 달성하려면 `Exceptions` 파사드를 통해 예외 처리기를 "가짜"로 만들 수 있습니다. 예외 처리기가 위조되면 `assertReported` 및 `assertNotReported` 메서드를 활용하여 요청 중에 발생한 예외에 대해 어설션을 만들 수 있습니다.

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

`assertNotReported` 및 `assertNothingReported` 메소드는 요청 중에 주어진 예외가 발생하지 않았거나 예외가 발생하지 않았음을 주장하는 데 사용될 수 있습니다.

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

요청하기 전에 `withoutExceptionHandling` 메소드를 호출하여 특정 요청에 대한 예외 처리를 완전히 비활성화할 수 있습니다.

```php
$response = $this->withoutExceptionHandling()->get('/');
```

또한 애플리케이션이 PHP 언어 또는 애플리케이션에서 사용하는 라이브러리에서 더 이상 사용되지 않는 기능을 활용하지 않는지 확인하려면 요청하기 전에 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 지원 중단 처리가 비활성화되면 지원 중단 경고가 예외로 변환되어 테스트가 실패하게 됩니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

`assertThrows` 메소드는 주어진 클로저 내의 코드가 지정된 유형의 예외를 발생시키는 것을 주장하는 데 사용될 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

발생한 예외를 검사하고 어설션하려면 `assertThrows` 메서드의 두 번째 인수로 클로저를 제공할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

`assertDoesntThrow` 메소드는 주어진 클로저 내의 코드가 예외를 발생시키지 않는다는 것을 주장하는 데 사용될 수 있습니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
## JSON API 테스트 (Testing JSON APIs)

Laravel는 또한 JSON API 및 해당 응답을 테스트하기 위한 여러 도우미를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson` 및 `optionsJson` 메서드를 사용하여 다양한 HTTP 동사로 JSON 요청을 실행할 수 있습니다. 데이터와 헤더를 이러한 메소드에 쉽게 전달할 수도 있습니다. 시작하려면 `/api/user`에 `POST` 요청을 보내고 예상된 JSON 데이터가 반환되었는지 확인하는 테스트를 작성해 보겠습니다.

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

또한 JSON 응답 데이터는 응답의 배열 변수로 액세스할 수 있으므로 JSON 응답 내에서 반환된 개별 값을 검사하는 것이 편리합니다.

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메소드는 응답을 배열로 변환하여 지정된 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 있는 경우 지정된 조각이 존재하는 한 이 테스트는 계속 통과됩니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 확인

앞서 언급한 바와 같이, `assertJson` 메소드는 JSON의 단편이 JSON 응답 내에 존재함을 주장하는 데 사용될 수 있습니다. 주어진 배열이 애플리케이션에서 반환된 JSON와 **정확히 일치**하는지 확인하려면 `assertExactJson` 메서드를 사용해야 합니다.

```php tab=Pest
<?php

test('asserting an exact json match', function () {
    $response = $this->postJson('/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertExactJson([
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
    public function test_asserting_an_exact_json_match(): void
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertExactJson([
                'created' => true,
            ]);
    }
}
```

<a name="verifying-json-paths"></a>
#### JSON 경로에 대한 어설션

JSON 응답에 지정된 경로에 지정된 데이터가 포함되어 있는지 확인하려면 `assertJsonPath` 메서드를 사용해야 합니다.

```php tab=Pest
<?php

test('asserting a json path value', function () {
    $response = $this->postJson('/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertJsonPath('team.owner.name', 'Darian');
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
    public function test_asserting_a_json_paths_value(): void
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJsonPath('team.owner.name', 'Darian');
    }
}
```

`assertJsonPath` 메소드는 또한 어설션이 통과되어야 하는지를 동적으로 결정하는 데 사용할 수 있는 클로저를 허용합니다.

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
### 유창한 JSON 테스트

Laravel는 또한 애플리케이션의 JSON 응답을 유창하게 테스트할 수 있는 아름다운 방법을 제공합니다. 시작하려면 `assertJson` 메서드에 클로저를 전달하세요. 이 클로저는 애플리케이션에서 반환된 JSON에 대해 어설션을 만드는 데 사용할 수 있는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스로 호출됩니다. `where` 메소드는 JSON의 특정 속성에 대해 주장을 하는 데 사용될 수 있는 반면, `missing` 메소드는 JSON에서 특정 속성이 누락되었음을 주장하는 데 사용될 수 있습니다.

```php tab=Pest
use Illuminate\Testing\Fluent\AssertableJson;

test('fluent json', function () {
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                ->where('name', 'Victoria Faith')
                ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                ->whereNot('status', 'pending')
                ->missing('password')
                ->etc()
        );
});
```

```php tab=PHPUnit
use Illuminate\Testing\Fluent\AssertableJson;

/**
 * A basic functional test example.
 */
public function test_fluent_json(): void
{
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                ->where('name', 'Victoria Faith')
                ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                ->whereNot('status', 'pending')
                ->missing('password')
                ->etc()
        );
}
```

#### `etc` 방법 이해

위의 예에서 어설션 체인의 끝에서 `etc` 메서드를 호출했음을 알 수 있습니다. 이 메소드는 JSON 객체에 다른 속성이 있을 수 있음을 Laravel에 알립니다. `etc` 메서드를 사용하지 않는 경우 어설션을 수행하지 않은 다른 속성이 JSON 개체에 있으면 테스트가 실패합니다.

이 동작의 의도는 사용자가 속성에 대해 명시적으로 어설션을 수행하거나 `etc` 메서드를 통해 추가 속성을 명시적으로 허용하도록 하여 JSON 응답에 민감한 정보가 의도치 않게 노출되지 않도록 보호하는 것입니다.

그러나 어설션 체인에 `etc` 메서드를 포함하지 않는다고 해서 JSON 개체 내에 중첩된 배열에 추가 특성이 추가되지 않는 것은 아닙니다. `etc` 방법은 `etc` 방법이 호출되는 중첩 수준에 추가 속성이 존재하지 않도록 보장합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 속성 존재/부재 확인

속성의 존재 여부를 확인하려면 `has` 및 `missing` 메소드를 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

또한 `hasAll` 및 `missingAll` 메서드를 사용하면 여러 속성의 존재 여부를 동시에 확인할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

`hasAny` 메소드를 사용하여 주어진 속성 목록 중 하나 이상이 존재하는지 확인할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션에 대한 주장

종종 라우트는 여러 사용자와 같은 여러 항목이 포함된 JSON 응답을 반환합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

이러한 상황에서는 유연한 JSON 개체의 `has` 메서드를 사용하여 응답에 포함된 사용자에 대해 어설션을 만들 수 있습니다. 예를 들어 JSON 응답에 세 명의 사용자가 포함되어 있다고 가정해 보겠습니다. 다음으로 `first` 메서드를 사용하여 컬렉션의 첫 번째 사용자에 대한 몇 가지 어설션을 만듭니다. `first` 메소드는 JSON 컬렉션의 첫 번째 개체에 대한 주장을 만드는 데 사용할 수 있는 또 다른 주장 가능한 JSON 문자열을 수신하는 클로저를 허용합니다.

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has(3)
            ->first(fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```

JSON 컬렉션의 모든 항목에 대해 동일한 어설션을 만들고 싶다면 `each` 메서드를 사용할 수 있습니다.

```php
$response
  ->assertJson(fn (AssertableJson $json) =>
      $json->has(3)
          ->each(fn (AssertableJson $json) =>
              $json->whereType('id', 'integer')
                  ->whereType('name', 'string')
                  ->whereType('email', 'string')
                  ->missing('password')
                  ->etc()
          )
  );
```

<a name="scoping-json-collection-assertions"></a>
#### JSON 컬렉션 어설션 범위 지정

때때로 애플리케이션의 라우트는 명명된 키가 할당된 JSON 컬렉션을 반환합니다.

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

이러한 라우트를 테스트할 때 `has` 메서드를 사용하여 컬렉션의 항목 수에 대해 어설션할 수 있습니다. 또한 `has` 메서드를 사용하여 주장 체인의 범위를 지정할 수 있습니다.

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
            ->has('users', 3)
            ->has('users.0', fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```

그러나 `users` 컬렉션에 대해 어설션하기 위해 `has` 메서드를 두 번 개별적으로 호출하는 대신 세 번째 매개 변수로 클로저를 제공하는 단일 호출을 수행할 수 있습니다. 그렇게 하면 클로저가 자동으로 호출되고 컬렉션의 첫 번째 항목으로 범위가 지정됩니다.

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
            ->has('users', 3, fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```

<a name="asserting-json-types"></a>
#### JSON 유형 어설션

JSON 응답의 속성이 특정 유형인지 확인하고 싶을 수도 있습니다. `Illuminate\Testing\Fluent\AssertableJson` 클래스는 이를 수행하기 위해 `whereType` 및 `whereAllType` 메서드를 제공합니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

`|` 문자를 사용하거나 유형 배열을 `whereType` 메소드에 두 번째 매개변수로 전달하여 여러 유형을 지정할 수 있습니다. 응답 값이 나열된 유형 중 하나이면 어설션이 성공합니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

`whereType` 및 `whereAllType` 방법은 `string`, `integer`, `double`, `boolean`, `array` 및 `null` 유형을 인식합니다.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트 (Testing File Uploads)

`Illuminate\Http\UploadedFile` 클래스는 테스트용 더미 파일이나 이미지를 생성하는 데 사용할 수 있는 `fake` 메서드를 제공합니다. 이는 `Storage` 파사드의 `fake` 방법과 결합되어 파일 업로드 테스트를 크게 단순화합니다. 예를 들어 다음 두 기능을 결합하여 아바타 업로드 양식을 쉽게 테스트할 수 있습니다.

```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('avatars can be uploaded', function () {
    Storage::fake('avatars');

    $file = UploadedFile::fake()->image('avatar.jpg');

    $response = $this->post('/avatar', [
        'avatar' => $file,
    ]);

    Storage::disk('avatars')->assertExists($file->hashName());
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_avatars_can_be_uploaded(): void
    {
        Storage::fake('avatars');

        $file = UploadedFile::fake()->image('avatar.jpg');

        $response = $this->post('/avatar', [
            'avatar' => $file,
        ]);

        Storage::disk('avatars')->assertExists($file->hashName());
    }
}
```

주어진 파일이 존재하지 않는다고 주장하고 싶다면, `Storage` 파사드에서 제공하는 `assertMissing` 메소드를 사용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
#### 가짜 파일 사용자 지정

`UploadedFile` 클래스에서 제공하는 `fake` 메서드를 사용하여 파일을 생성할 때 애플리케이션의 유효성 검사 규칙을 더 잘 테스트하기 위해 이미지의 너비, 높이 및 크기(KB)를 지정할 수 있습니다.

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

이미지 생성 외에도 `create` 메소드를 사용하여 다른 유형의 파일을 생성할 수 있습니다.

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

필요한 경우 `$mimeType` 인수를 메서드에 전달하여 파일에서 반환해야 하는 MIME 유형을 명시적으로 정의할 수 있습니다.

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
## 뷰 테스트 (Testing Views)

또한 Laravel을 사용하면 애플리케이션에 시뮬레이션된 HTTP 요청을 하지 않고도 뷰를 렌더링할 수 있습니다. 이를 수행하려면 테스트 내에서 `view` 메서드를 호출하면 됩니다. `view` 메서드는 뷰 이름과 선택적 데이터 배열을 허용합니다. 이 메서드는 뷰의 내용에 대해 편리하게 주장할 수 있는 여러 메서드를 제공하는 `Illuminate\Testing\TestView`의 인스턴스를 반환합니다.

```php tab=Pest
<?php

test('a welcome view can be rendered', function () {
    $view = $this->view('welcome', ['name' => 'Taylor']);

    $view->assertSee('Taylor');
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_a_welcome_view_can_be_rendered(): void
    {
        $view = $this->view('welcome', ['name' => 'Taylor']);

        $view->assertSee('Taylor');
    }
}
```

`TestView` 클래스는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee` 및 `assertDontSeeText` 어설션 메서드를 제공합니다.

필요한 경우 `TestView` 인스턴스를 문자열로 캐스팅하여 원시 렌더링된 뷰 콘텐츠를 얻을 수 있습니다.

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
#### 공유 오류

일부 뷰는 [Laravel에서 제공하는 전역 오류 백](/docs/12.x/validation#quick-displaying-the-validation-errors)에 공유된 오류에 따라 달라질 수 있습니다. 오류 메시지와 함께 오류 백을 수화하려면 `withViewErrors` 메소드를 사용할 수 있습니다.

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
### Blade 및 컴포넌트 렌더링

필요한 경우 `blade` 메서드를 사용하여 원시 [Blade](/docs/12.x/blade) 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로 `blade` 메서드는 `Illuminate\Testing\TestView`의 인스턴스를 반환합니다.

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

`component` 메서드를 사용하여 [Blade 컴포넌트](/docs/12.x/blade#components)를 평가하고 렌더링할 수 있습니다. `component` 메소드는 `Illuminate\Testing\TestComponent`의 인스턴스를 반환합니다.

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="caching-routes"></a>
## 라우트 캐싱 (Caching Routes)

테스트가 실행되기 전에 Laravel는 정의된 모든 라우트 수집을 포함하여 애플리케이션의 새로운 인스턴스를 부팅합니다. 애플리케이션에 라우트 파일이 많으면 테스트 케이스에 `Illuminate\Foundation\Testing\WithCachedRoutes` 특성을 추가할 수 있습니다. 이 특성을 사용하는 테스트에서 라우트는 한 번 빌드되어 메모리에 저장됩니다. 즉, 라우트 수집 프로세스는 제품군의 모든 테스트에 대해 한 번만 실행됩니다.

```php tab=Pest
<?php

use App\Http\Controllers\UserController;
use Illuminate\Foundation\Testing\WithCachedRoutes;

pest()->use(WithCachedRoutes::class);

test('basic example', function () {
    $this->get(action([UserController::class, 'index']));

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Http\Controllers\UserController;
use Illuminate\Foundation\Testing\WithCachedRoutes;
use Tests\TestCase;

class BasicTest extends TestCase
{
    use WithCachedRoutes;

    /**
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        $response = $this->get(action([UserController::class, 'index']));

        // ...
    }
}
```

<a name="available-assertions"></a>
## 사용 가능한 어설션 (Available Assertions)

<a name="response-assertions"></a>
### 응답 주장

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션을 테스트할 때 활용할 수 있는 다양한 사용자 지정 어설션 방법을 제공합니다. 이러한 어설션은 `json`, `get`, `post`, `put` 및 `delete` 테스트 메서드에서 반환된 응답에서 액세스할 수 있습니다.

<style>
    .collection-method-list > p {
        columns: 14.4em 2; -moz-columns: 14.4em 2; -webkit-columns: 14.4em 2;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<div class="collection-method-list" markdown="1">

[수락됨](#assert-accepted)
[잘못된 요청 주장](#assert-bad-request)
[클라이언트 오류 주장](#assert-client-error)
[충돌 주장](#assert-conflict)
[쿠키 주장](#assert-cookie)
[쿠키 만료됨 주장](#assert-cookie-expired)
[쿠키가 만료되지 않았다고 주장](#assert-cookie-not-expired)
[쿠키누락 주장](#assert-cookie-missing)
[생성됨](#assert-created)
[참조하지 말라고 주장](#assert-dont-see)
[텍스트를 보지 말라고 주장](#assert-dont-see-text)
[다운로드 주장](#assert-download)
[정확한Json 주장](#assert-exact-json)
[정확한Json구조 주장](#assert-exact-json-structure)
[금지됨 주장](#assert-forbidden)
[발견 주장](#assert-found)
[사라졌다 주장](#assert-gone)
[어설션헤더](#assert-header)
[assertHeaderContains](#assert-header-contains)
[assertHeader누락](#assert-header-missing)
[내부 서버 오류 주장](#assert-internal-server-error)
[어설션Json](#assert-json)
[JsonCount 주장](#assert-json-count)
[assertJsonFragment](#assert-json-fragment)
[JsonIsArray 주장](#assert-json-is-array)
[assertJsonIsObject](#assert-json-is-object)
[JsonMissing](#assert-json-missing)
[JsonMissingExact 주장](#assert-json-missing-exact)
[JsonMissingValidationErrors 주장](#assert-json-missing-validation-errors)
[JsonPath 주장](#assert-json-path)
[JsonMissingPath 주장](#assert-json-missing-path)
[Json구조 주장](#assert-json-structure)
[JsonValidationErrors 주장](#assert-json-validation-errors)
[JsonValidationErrorFor 주장](#assert-json-validation-error-for)
[위치 주장](#assert-location)
[메소드가 허용되지 않음 주장](#assert-method-not-allowed)
[영구적으로 이동되었다고 주장](#assert-moved-permanently)
[내용 주장](#assert-content)
[콘텐츠 없음 주장](#assert-no-content)
[assertStreamed](#assert-streamed)
[스트리밍된 콘텐츠 주장](#assert-streamed-content)
[발견되지 않음 주장](#assert-not-found)
[확인](#assert-ok)
[결제 필수 주장](#assert-payment-required)
[PlainCookie 주장](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectBack](#assert-redirect-back)
[RedirectBackWithErrors 주장](#assert-redirect-back-with-errors)
[오류 없이 RedirectBack 주장](#assert-redirect-back-without-errors)
[assertRedirectContains](#assert-redirect-contains)
[RedirectToRoute 주장](#assert-redirect-to-route)
[SignedRoute로 리디렉션 주장](#assert-redirect-to-signed-route)
[assertRequestTimeout](#assert-request-timeout)
[주장참조](#assert-see)
[AsertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[서버 오류 주장](#assert-server-error)
[assertServiceUnavailable](#assert-service-unavailable)
[세션이 있다고 주장](#assert-session-has)
[assertSessionHasInput](#assert-session-has-input)
[assertSessionHasAll](#assert-session-has-all)
[assertSessionHasErrors](#assert-session-has-errors)
[assertSessionHasErrorsIn](#assert-session-has-errors-in)
[assertSessionHasNoErrors](#assert-session-has-no-errors)
[assertSessionDoesntHaveErrors](#assert-session-doesnt-have-errors)
[세션 누락됨](#assert-session-missing)
[상태 주장](#assert-status)
[성공적 주장](#assert-successful)
[요청이 너무 많다고 주장](#assert-too-many-requests)
[무단 주장](#assert-unauthorized)
[처리할 수 없음](#assert-unprocessable)
[지원되지 않는 미디어 유형 주장](#assert-unsupported-media-type)
[유효함 주장](#assert-valid)
[잘못된 주장](#assert-invalid)
[ViewHas 주장](#assert-view-has)
[ViewHasAll 주장](#assert-view-has-all)
[ViewIs 주장](#assert-view-is)
[어설션뷰 누락](#assert-view-missing)

</div>

<a name="assert-accepted"></a>
#### 주장수락됨

응답에 승인된(202) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
#### 잘못된 요청 주장

응답에 잘못된 요청(400) HTTP 상태 코드가 있는지 확인:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
#### 주장클라이언트 오류

응답에 클라이언트 오류(>= 400, < 500) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
#### 주장충돌

응답에 충돌(409) HTTP 상태 코드가 있는지 확인:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
#### 주장쿠키

응답에 주어진 쿠키가 포함되어 있는지 확인:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
#### Assert쿠키가 만료되었습니다.

응답에 주어진 쿠키가 포함되어 있고 만료되었는지 확인:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
#### AssertCookieNotExpired

응답에 주어진 쿠키가 포함되어 있고 만료되지 않았는지 확인:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
#### 어설션쿠키누락

응답에 주어진 쿠키가 포함되어 있지 않은지 확인:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
#### 주장생성됨

응답에 201 HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
#### 주장하지 마세요.

주어진 문자열이 애플리케이션이 반환한 응답에 포함되어 있지 않은지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다.

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
#### 주장하지 마세요텍스트를 참조하세요

주어진 문자열이 응답 텍스트에 포함되어 있지 않은지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다. 이 메소드는 어설션을 수행하기 전에 응답 내용을 `strip_tags` PHP 함수에 전달합니다.

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
#### 주장다운로드

응답이 "다운로드"인지 확인합니다. 일반적으로 이는 응답을 반환한 호출된 라우트가 `Response::download` 응답, `BinaryFileResponse` 또는 `Storage::download` 응답을 반환했음을 의미합니다.

```php
$response->assertDownload();
```

원하는 경우 다운로드 가능한 파일에 특정 파일 이름이 할당되었다고 주장할 수 있습니다.

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
#### AssertExactJson

응답에 주어진 JSON 데이터와 정확히 일치하는 항목이 포함되어 있는지 확인:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
#### AssertExactJson구조

응답에 주어진 JSON 구조와 정확히 일치하는 항목이 포함되어 있는지 확인:

```php
$response->assertExactJsonStructure(array $data);
```

이 방법은 [assertJsonStructure](#assert-json-structure)의 보다 엄격한 변형입니다. `assertJsonStructure`와 달리 이 메서드는 응답에 예상 JSON 구조에 명시적으로 포함되지 않은 키가 포함된 경우 실패합니다.

<a name="assert-forbidden"></a>
#### 주장금지됨

응답에 금지된(403) HTTP 상태 코드가 있는지 확인:

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
#### 주장발견됨

응답에 발견된(302) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertFound();
```

<a name="assert-gone"></a>
#### 주장사라짐

응답에 사라짐(410) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertGone();
```

<a name="assert-header"></a>
#### 주장헤더

주어진 헤더와 값이 응답에 존재하는지 확인:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-contains"></a>
#### 주장헤더가 포함되어 있습니다.

주어진 헤더에 주어진 하위 문자열 값이 포함되어 있는지 확인:

```php
$response->assertHeaderContains($headerName, $value);
```

<a name="assert-header-missing"></a>
#### 주장헤더가 누락되었습니다.

주어진 헤더가 응답에 존재하지 않는지 확인:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
#### 내부 서버 오류 주장

응답에 "내부 서버 오류"(500) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
#### 주장Json

응답에 주어진 JSON 데이터가 포함되어 있는지 확인:

```php
$response->assertJson(array $data, $strict = false);
```

`assertJson` 메소드는 응답을 배열로 변환하여 지정된 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 있는 경우 지정된 조각이 존재하는 한 이 테스트는 계속 통과됩니다.

<a name="assert-json-count"></a>
#### 주장JsonCount

응답 JSON에 주어진 키에 예상되는 항목 수의 배열이 있는지 확인:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
#### 주장JsonFragment

응답의 어느 위치에나 주어진 JSON 데이터가 응답에 포함되어 있는지 확인합니다.

```php
Route::get('/users', function () {
    return [
        'users' => [
            [
                'name' => 'Taylor Otwell',
            ],
        ],
    ];
});

$response->assertJsonFragment(['name' => 'Taylor Otwell']);
```

<a name="assert-json-is-array"></a>
#### 주장JsonIsArray

JSON 응답이 배열인지 확인합니다.

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
#### 주장JsonIsObject

JSON 응답이 객체인지 확인합니다:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
#### AssertJsonMissing

응답에 주어진 JSON 데이터가 포함되어 있지 않은지 확인:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
#### AssertJsonMissingExact

응답에 정확한 JSON 데이터가 포함되어 있지 않은지 확인:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
#### AssertJsonMissingValidationErrors

응답에 주어진 키에 대한 JSON 유효성 검사 오류가 없는지 확인:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드를 사용하여 응답에 JSON로 반환된 유효성 검사 오류가 없고 **오류가 세션 저장소에 플래시되지 않았음을 주장할 수 있습니다.

<a name="assert-json-path"></a>
#### 주장JsonPath

응답에 지정된 경로에 지정된 데이터가 포함되어 있는지 확인:

```php
$response->assertJsonPath($path, $expectedValue);
```

예를 들어 애플리케이션에서 다음 JSON 응답을 반환하는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 `user` 개체의 `name` 속성이 지정된 값과 일치한다고 주장할 수 있습니다.

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
#### AssertJsonMissingPath

응답에 주어진 경로가 포함되어 있지 않은지 확인:

```php
$response->assertJsonMissingPath($path);
```

예를 들어 애플리케이션에서 다음 JSON 응답을 반환하는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` 객체의 `email` 속성이 포함되어 있지 않다고 주장할 수 있습니다.

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
#### 주장Json구조

응답에 주어진 JSON 구조가 있는지 확인:

```php
$response->assertJsonStructure(array $structure);
```

예를 들어, 애플리케이션에서 반환된 JSON 응답에 다음 데이터가 포함되어 있는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

다음과 같이 JSON 구조가 기대와 일치한다고 주장할 수 있습니다.

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

때로는 애플리케이션에서 반환된 JSON 응답에 객체 배열이 포함될 수 있습니다.

```json
{
    "user": [
        {
            "name": "Steve Schoger",
            "age": 55,
            "location": "Earth"
        },
        {
            "name": "Mary Schoger",
            "age": 60,
            "location": "Earth"
        }
    ]
}
```

이 상황에서는 `*` 문자를 사용하여 배열에 있는 모든 객체의 구조에 대해 주장할 수 있습니다.

```php
$response->assertJsonStructure([
    'user' => [
        '*' => [
             'name',
             'age',
             'location'
        ]
    ]
]);
```

<a name="assert-json-validation-errors"></a>
#### 주장JsonValidationErrors

응답에 주어진 키에 대해 주어진 JSON 유효성 검사 오류가 있는지 확인합니다. 유효성 검사 오류가 세션에 플래시되는 대신 JSON 구조로 반환되는 응답에 대해 어설션할 때 이 메서드를 사용해야 합니다.

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드를 사용하면 응답에 JSON로 반환된 유효성 검사 오류가 있거나** 오류가 세션 저장소에 플래시되었음을 주장하는 데 사용할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### AssertJsonValidationErrorFor

응답에 지정된 키에 대한 JSON 유효성 검사 오류가 있는지 확인합니다.

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
#### AssertMethodNotAllowed

응답에 허용되지 않는 메서드(405) HTTP 상태 코드가 있는지 확인:

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
#### AssertMovedPermanently

응답이 영구적으로 이동했는지(301) HTTP 상태 코드를 확인합니다.

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
#### 주장 위치

응답의 `Location` 헤더에 지정된 URI 값이 있는지 확인합니다.

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
#### 내용 주장

주어진 문자열이 응답 내용과 일치하는지 확인합니다:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
#### 내용 없음 주장

응답에 주어진 HTTP 상태 코드가 있고 내용이 없는지 확인:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
#### AssertStreamed

응답이 스트리밍된 응답인지 확인합니다.

$응답->assertStreamed();

<a name="assert-streamed-content"></a>
#### AssertStreamedContent

주어진 문자열이 스트리밍된 응답 콘텐츠와 일치하는지 확인합니다.

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
#### AssertNotFound

응답에 찾을 수 없음(404) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
#### 주장좋아요

응답에 200 HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
#### 주장지불필수

응답에 결제 필요(402) HTTP 상태 코드가 있는지 확인:

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
#### 주장일반쿠키

응답에 암호화되지 않은 주어진 쿠키가 포함되어 있는지 확인:

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
#### 방향전환 주장

응답이 주어진 URI로의 리디렉션인지 확인:

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
#### AssertRedirectBack

응답이 이전 페이지로 다시 리디렉션되는지 확인합니다.

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
#### AssertRedirectBackWithErrors

응답이 이전 페이지로 다시 리디렉션되고 [세션에 지정된 오류가 있음](#assert-session-has-errors)인지 확인합니다.

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<a name="assert-redirect-back-without-errors"></a>
#### AssertRedirectBackWithoutErrors

응답이 이전 페이지로 다시 리디렉션되고 세션에 오류 메시지가 없는지 확인합니다.

```php
$response->assertRedirectBackWithoutErrors();
```

<a name="assert-redirect-contains"></a>
#### AssertRedirectContains

응답이 주어진 문자열을 포함하는 URI로 리디렉션되는지 확인합니다.

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
#### AssertRedirectToRoute

응답이 주어진 [라우트](/docs/12.x/routing#named-routes)에 대한 리디렉션인지 확인합니다.

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
#### AssertRedirectToSignedRoute

응답이 주어진 [서명된 라우트](/docs/12.x/urls#signed-urls)에 대한 리디렉션인지 확인합니다.

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
#### 주장요청 시간 초과

응답에 요청 시간 초과(408) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
#### 주장참조

주어진 문자열이 응답 내에 포함되어 있는지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다.

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
#### 주장보기순서

주어진 문자열이 응답 내에 순서대로 포함되어 있는지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다.

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
#### 주장텍스트 보기

주어진 문자열이 응답 텍스트 내에 포함되어 있는지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다. 어설션이 이루어지기 전에 응답 콘텐츠가 `strip_tags` PHP 함수에 전달됩니다.

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
#### AssertSeeTextInOrder

주어진 문자열이 응답 텍스트 내에 순서대로 포함되어 있는지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다. 어설션이 이루어지기 전에 응답 콘텐츠가 `strip_tags` PHP 함수에 전달됩니다.

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
#### 주장서버 오류

응답에 서버 오류(>= 500, < 600) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
#### AssertService를 사용할 수 없음

응답에 "Service Unavailable"(503) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
#### AssertSessionHas

세션에 주어진 데이터가 포함되어 있는지 확인:

```php
$response->assertSessionHas($key, $value = null);
```

필요한 경우 클로저를 `assertSessionHas` 메서드의 두 번째 인수로 제공할 수 있습니다. 클로저가 `true`를 반환하면 어설션이 통과됩니다.

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
#### AssertSessionHasInput

세션이 [플래시된 입력 배열](/docs/12.x/responses#redirecting-with-flashed-session-data)에 지정된 값을 가지고 있는지 확인합니다.

```php
$response->assertSessionHasInput($key, $value = null);
```

필요한 경우 클로저를 `assertSessionHasInput` 메서드의 두 번째 인수로 제공할 수 있습니다. 클로저가 `true`를 반환하면 어설션이 통과됩니다.

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
#### AssertSessionHasAll

세션에 주어진 키/값 쌍 배열이 포함되어 있는지 확인:

```php
$response->assertSessionHasAll(array $data);
```

예를 들어, 애플리케이션의 세션에 `name` 및 `status` 키가 포함된 경우 두 키가 모두 존재하고 다음과 같이 지정된 값을 갖는다고 주장할 수 있습니다.

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
#### AssertSessionHasErrors

세션에 주어진 `$keys`에 대한 오류가 포함되어 있는지 확인합니다. `$keys`가 연관 배열인 경우 세션에 각 필드(키)에 대한 특정 오류 메시지(값)가 포함되어 있음을 어설션합니다. 이 방법은 유효성 검사 오류를 JSON 구조로 반환하는 대신 세션에 플래시하는 라우트를 테스트할 때 사용해야 합니다.

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

예를 들어, `name` 및 `email` 필드에 세션에 플래시된 유효성 검사 오류 메시지가 있음을 확인하려면 다음과 같이 `assertSessionHasErrors` 메서드를 호출할 수 있습니다.

```php
$response->assertSessionHasErrors(['name', 'email']);
```

또는 특정 필드에 특정 유효성 검사 오류 메시지가 있다고 주장할 수도 있습니다.

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드를 사용하면 응답에 JSON로 반환된 유효성 검사 오류가 있거나** 오류가 세션 저장소에 플래시되었음을 주장하는 데 사용할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### AssertSessionHasErrorsIn

세션이 특정 [오류 백](/docs/12.x/validation#named-error-bags) 내에서 주어진 `$keys`에 대한 오류를 포함하고 있는지 확인합니다. `$keys`가 연관 배열인 경우 세션에 오류 백 내에서 각 필드(키)에 대한 특정 오류 메시지(값)가 포함되어 있음을 어설션합니다.

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
#### AssertSessionHasNoErrors

세션에 유효성 검사 오류가 없는지 확인합니다.

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
#### AssertSessionDoesntHaveErrors

세션에 주어진 키에 대한 유효성 검사 오류가 없는지 확인:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드를 사용하여 응답에 JSON로 반환된 유효성 검사 오류가 없고 **오류가 세션 저장소에 플래시되지 않았음을 주장할 수 있습니다.

<a name="assert-session-missing"></a>
#### AssertSession누락

세션에 주어진 키가 포함되어 있지 않은지 확인:

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
#### 주장상태

응답에 주어진 HTTP 상태 코드가 있는지 확인:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
#### 주장성공

응답에 성공(>= 200 및 < 300) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
#### 너무 많은 요청을 주장함

응답에 너무 많은 요청(429)이 있는지 확인합니다. HTTP 상태 코드:

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
#### 주장권한이 없음

응답에 승인되지 않은(401) HTTP 상태 코드가 있는지 확인:

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
#### 주장처리할 수 없음

응답에 처리할 수 없는 엔터티(422) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
#### 지원되지 않는 미디어 유형 주장

응답에 지원되지 않는 미디어 유형(415) HTTP 상태 코드가 있는지 확인:

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
#### 유효한 주장

응답에 주어진 키에 대한 유효성 검사 오류가 없는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 유효성 검사 오류가 세션에 플래시된 응답에 대해 어설션하는 데 사용될 수 있습니다.

```php
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
#### 잘못된 주장

응답에 주어진 키에 대한 유효성 검사 오류가 있는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 유효성 검사 오류가 세션에 플래시된 응답에 대해 어설션하는 데 사용될 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

또한 특정 키에 특정 유효성 검사 오류 메시지가 있다고 주장할 수도 있습니다. 그렇게 할 때 전체 메시지를 제공하거나 메시지의 일부만 제공할 수 있습니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

주어진 필드가 유효성 검사 오류가 있는 유일한 필드라고 주장하려면 `assertOnlyInvalid` 메서드를 사용할 수 있습니다.

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
#### AssertViewHas

뷰 응답에 주어진 데이터가 포함되어 있는지 확인:

```php
$response->assertViewHas($key, $value = null);
```

클로저를 `assertViewHas` 메소드의 두 번째 인수로 전달하면 뷰 데이터의 특정 부분을 검사하고 이에 대한 어설션을 만들 수 있습니다.

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

또한 뷰 데이터는 응답에서 배열 변수로 액세스할 수 있으므로 편리하게 검사할 수 있습니다.

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### AssertViewHasAll

뷰 응답에 주어진 데이터 목록이 있는지 확인:

```php
$response->assertViewHasAll(array $data);
```

이 메소드는 뷰가 단순히 주어진 키와 일치하는 데이터를 포함하고 있음을 주장하는 데 사용될 수 있습니다.

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

또는 뷰 데이터가 존재하고 특정 값을 가지고 있다고 주장할 수 있습니다.

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
#### AssertViewIs

주어진 뷰가 라우트에 의해 반환되었는지 확인:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
#### AssertViewMissing

주어진 데이터 키가 애플리케이션의 응답으로 반환된 뷰에 사용 가능하지 않은지 확인:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
### 인증 어설션

Laravel는 또한 애플리케이션의 기능 테스트 내에서 활용할 수 있는 다양한 인증 관련 어설션을 제공합니다. 이러한 메서드는 `get` 및 `post`와 같은 메서드에서 반환된 `Illuminate\Testing\TestResponse` 인스턴스가 아니라 테스트 클래스 자체에서 호출됩니다.

<a name="assert-authenticated"></a>
#### 주장인증됨

사용자가 인증되었는지 확인:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
#### 주장게스트

사용자가 인증되지 않았는지 확인:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
#### AssertAuthenticatedAs

특정 사용자가 인증되었는지 확인:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
## 검증 주장 (Validation Assertions)

Laravel는 요청에 제공된 데이터가 유효한지 또는 유효하지 않은지 확인하는 데 사용할 수 있는 두 가지 기본 검증 관련 어설션을 제공합니다.

<a name="validation-assert-valid"></a>
#### 유효한 주장

응답에 주어진 키에 대한 유효성 검사 오류가 없는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 유효성 검사 오류가 세션에 플래시된 응답에 대해 어설션하는 데 사용될 수 있습니다.

```php
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
#### 잘못된 주장

응답에 주어진 키에 대한 유효성 검사 오류가 있는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 유효성 검사 오류가 세션에 플래시된 응답에 대해 어설션하는 데 사용될 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

또한 특정 키에 특정 유효성 검사 오류 메시지가 있다고 주장할 수도 있습니다. 그렇게 할 때 전체 메시지를 제공하거나 메시지의 일부만 제공할 수 있습니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
