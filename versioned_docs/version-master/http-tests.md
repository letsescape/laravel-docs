<!-- # HTTP Tests -->
# HTTP Tests

- [Introduction](#introduction)
- [Making Requests](#making-requests)
    - [Customizing Request Headers](#customizing-request-headers)
    - [Cookies](#cookies)
    - [Session / Authentication](#session-and-authentication)
    - [Debugging Responses](#debugging-responses)
    - [Exception Handling](#exception-handling)
- [Testing JSON APIs](#testing-json-apis)
    - [Fluent JSON Testing](#fluent-json-testing)
- [Testing File Uploads](#testing-file-uploads)
- [Testing Views](#testing-views)
    - [Rendering Blade and Components](#rendering-blade-and-components)
- [Caching Routes](#caching-routes)
- [Available Assertions](#available-assertions)
    - [Response Assertions](#response-assertions)
    - [Authentication Assertions](#authentication-assertions)
    - [Validation Assertions](#validation-assertions)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a very fluent API for making HTTP requests to your application and examining the responses. For example, take a look at the feature test defined below: -->
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

<!-- The `get` method makes a `GET` request into the application, while the `assertStatus` method asserts that the returned response should have the given HTTP status code. In addition to this simple assertion, Laravel also contains a variety of assertions for inspecting the response headers, content, JSON structure, and more. -->
`get` 메서드는 애플리케이션에 `GET` 요청을 보내는 반면, `assertStatus` 메서드는 반환된 응답에 지정된 HTTP 상태 코드가 있어야 한다고 어설션합니다. 이 간단한 어설션 외에도 Laravel에는 응답 헤더, 콘텐츠, JSON 구조 등을 검사하기 위한 다양한 어설션도 포함되어 있습니다.

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make a request to your application, you may invoke the `get`, `post`, `put`, `patch`, or `delete` methods within your test. These methods do not actually issue a "real" HTTP request to your application. Instead, the entire network request is simulated internally. -->
애플리케이션에 요청하려면 테스트 내에서 `get`, `post`, `put`, `patch` 또는 `delete` 메서드를 호출할 수 있습니다. 이러한 메서드는 실제로 애플리케이션에 "실제" HTTP 요청을 발행하지 않습니다. 대신 전체 네트워크 요청이 내부적으로 시뮬레이션됩니다.

<!-- Instead of returning an `Illuminate\Http\Response` instance, test request methods return an instance of `Illuminate\Testing\TestResponse`, which provides a [variety of helpful assertions](#available-assertions) that allow you to inspect your application's responses: -->
`Illuminate\Http\Response` 인스턴스를 반환하는 대신 테스트 요청 메서드는 애플리케이션의 응답을 검사할 수 있는 [variety of helpful assertions](#available-assertions)을 제공하는 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다.

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

<!-- In general, each of your tests should only make one request to your application. Unexpected behavior may occur if multiple requests are executed within a single test method. -->
일반적으로 각 테스트는 애플리케이션에 대해 하나의 요청만 수행해야 합니다. 단일 테스트 메서드 내에서 여러 요청이 실행되면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해 테스트를 실행할 때 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
<!-- ### Customizing Request Headers -->
### Customizing Request Headers

<!-- You may use the `withHeaders` method to customize the request's headers before it is sent to the application. This method allows you to add any custom headers you would like to the request: -->
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
<!-- ### Cookies -->
### Cookies

<!-- You may use the `withCookie` or `withCookies` methods to set cookie values before making a request. The `withCookie` method accepts a cookie name and value as its two arguments, while the `withCookies` method accepts an array of name / value pairs: -->
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
<!-- ### Session / Authentication -->
### Session / Authentication

<!-- Laravel provides several helpers for interacting with the session during HTTP testing. First, you may set the session data to a given array using the `withSession` method. This is useful for loading the session with data before issuing a request to your application: -->
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

<!-- Laravel's session is typically used to maintain state for the currently authenticated user. Therefore, the `actingAs` helper method provides a simple way to authenticate a given user as the current user. For example, we may use a [model factory](/docs/master/eloquent-factories) to generate and authenticate a user: -->
Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서 `actingAs` 도우미 메서드는 지정된 사용자를 현재 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, [model factory](/docs/master/eloquent-factories)를 사용하여 사용자를 생성하고 인증할 수 있습니다.

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

<!-- You may also specify which guard should be used to authenticate the given user by passing the guard name as the second argument to the `actingAs` method. The guard that is provided to the `actingAs` method will also become the default guard for the duration of the test: -->
가드 이름을 `actingAs` 메소드의 두 번째 인수로 전달하여 특정 사용자를 인증하는 데 어떤 가드를 사용해야 하는지 지정할 수도 있습니다. `actingAs` 메서드에 제공되는 가드도 테스트 기간 동안 기본 가드가 됩니다.

```php
$this->actingAs($user, 'web');
```

<!-- If you would like to ensure the request is unauthenticated, you may use the `actingAsGuest` method: -->
요청이 인증되지 않았는지 확인하려면 `actingAsGuest` 메소드를 사용할 수 있습니다.

```php
$this->actingAsGuest();
```

<a name="debugging-responses"></a>
<!-- ### Debugging Responses -->
### Debugging Responses

<!-- After making a test request to your application, the `dump`, `dumpHeaders`, and `dumpSession` methods may be used to examine and debug the response contents: -->
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

<!-- Alternatively, you may use the `dd`, `ddHeaders`, `ddBody`, `ddJson`, and `ddSession` methods to dump information about the response and then stop execution: -->
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
<!-- ### Exception Handling -->
### Exception Handling

<!-- Sometimes you may need to test that your application is throwing a specific exception. To accomplish this, you may "fake" the exception handler via the `Exceptions` facade. Once the exception handler has been faked, you may utilize the `assertReported` and `assertNotReported` methods to make assertions against exceptions that were thrown during the request: -->
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

<!-- The `assertNotReported` and `assertNothingReported` methods may be used to assert that a given exception was not thrown during the request or that no exceptions were thrown: -->
`assertNotReported` 및 `assertNothingReported` 메소드는 요청 중에 주어진 예외가 발생하지 않았거나 예외가 발생하지 않았음을 주장하는 데 사용될 수 있습니다.

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

<!-- You may totally disable exception handling for a given request by invoking the `withoutExceptionHandling` method before making your request: -->
요청하기 전에 `withoutExceptionHandling` 메소드를 호출하여 특정 요청에 대한 예외 처리를 완전히 비활성화할 수 있습니다.

```php
$response = $this->withoutExceptionHandling()->get('/');
```

<!-- In addition, if you would like to ensure that your application is not utilizing features that have been deprecated by the PHP language or the libraries your application is using, you may invoke the `withoutDeprecationHandling` method before making your request. When deprecation handling is disabled, deprecation warnings will be converted to exceptions, thus causing your test to fail: -->
또한 애플리케이션이 PHP 언어 또는 애플리케이션에서 사용하는 라이브러리에서 더 이상 사용되지 않는 기능을 활용하지 않는지 확인하려면 요청하기 전에 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 지원 중단 처리가 비활성화되면 지원 중단 경고가 예외로 변환되어 테스트가 실패하게 됩니다.

```php
$response = $this->withoutDeprecationHandling()->get('/');
```

<!-- The `assertThrows` method may be used to assert that code within a given closure throws an exception of the specified type: -->
`assertThrows` 메소드는 주어진 클로저 내의 코드가 지정된 유형의 예외를 발생시키는 것을 주장하는 데 사용될 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

<!-- If you would like to inspect and make assertions against the exception that is thrown, you may provide a closure as the second argument to the `assertThrows` method: -->
발생한 예외를 검사하고 어설션하려면 `assertThrows` 메서드의 두 번째 인수로 클로저를 제공할 수 있습니다.

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

<!-- The `assertDoesntThrow` method may be used to assert that the code within a given closure does not throw any exceptions: -->
`assertDoesntThrow` 메소드는 주어진 클로저 내의 코드가 예외를 발생시키지 않는다는 것을 주장하는 데 사용될 수 있습니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```

<a name="testing-json-apis"></a>
<!-- ## Testing JSON APIs -->
## Testing JSON APIs

<!-- Laravel also provides several helpers for testing JSON APIs and their responses. For example, the `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, and `optionsJson` methods may be used to issue JSON requests with various HTTP verbs. You may also easily pass data and headers to these methods. To get started, let's write a test to make a `POST` request to `/api/user` and assert that the expected JSON data was returned: -->
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

<!-- In addition, JSON response data may be accessed as array variables on the response, making it convenient for you to inspect the individual values returned within a JSON response: -->
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
<!-- #### Asserting Exact JSON Matches -->
#### Asserting Exact JSON Matches

<!-- As previously mentioned, the `assertJson` method may be used to assert that a fragment of JSON exists within the JSON response. If you would like to verify that a given array **exactly matches** the JSON returned by your application, you should use the `assertExactJson` method: -->
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
<!-- #### Asserting on JSON Paths -->
#### Asserting on JSON Paths

<!-- If you would like to verify that the JSON response contains the given data at a specified path, you should use the `assertJsonPath` method: -->
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

<!-- The `assertJsonPath` method also accepts a closure, which may be used to dynamically determine if the assertion should pass: -->
`assertJsonPath` 메소드는 또한 어설션이 통과되어야 하는지를 동적으로 결정하는 데 사용할 수 있는 클로저를 허용합니다.

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
<!-- ### Fluent JSON Testing -->
### Fluent JSON Testing

<!-- Laravel also offers a beautiful way to fluently test your application's JSON responses. To get started, pass a closure to the `assertJson` method. This closure will be invoked with an instance of `Illuminate\Testing\Fluent\AssertableJson` which can be used to make assertions against the JSON that was returned by your application. The `where` method may be used to make assertions against a particular attribute of the JSON, while the `missing` method may be used to assert that a particular attribute is missing from the JSON: -->
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

<!-- #### Understanding the `etc` Method -->
#### Understanding the `etc` Method

<!-- In the example above, you may have noticed we invoked the `etc` method at the end of our assertion chain. This method informs Laravel that there may be other attributes present on the JSON object. If the `etc` method is not used, the test will fail if other attributes that you did not make assertions against exist on the JSON object. -->
위의 예에서 어설션 체인의 끝에서 `etc` 메서드를 호출했음을 알 수 있습니다. 이 메소드는 JSON 객체에 다른 속성이 있을 수 있음을 Laravel에 알립니다. `etc` 메서드를 사용하지 않는 경우 어설션을 수행하지 않은 다른 속성이 JSON 개체에 있으면 테스트가 실패합니다.

<!-- The intention behind this behavior is to protect you from unintentionally exposing sensitive information in your JSON responses by forcing you to either explicitly make an assertion against the attribute or explicitly allow additional attributes via the `etc` method. -->
이 동작의 의도는 사용자가 속성에 대해 명시적으로 어설션을 수행하거나 `etc` 메서드를 통해 추가 속성을 명시적으로 허용하도록 하여 JSON 응답에 민감한 정보가 의도치 않게 노출되지 않도록 보호하는 것입니다.

<!-- However, you should be aware that not including the `etc` method in your assertion chain does not ensure that additional attributes are not being added to arrays that are nested within your JSON object. The `etc` method only ensures that no additional attributes exist at the nesting level in which the `etc` method is invoked. -->
그러나 어설션 체인에 `etc` 메서드를 포함하지 않는다고 해서 JSON 개체 내에 중첩된 배열에 추가 특성이 추가되지 않는 것은 아닙니다. `etc` 방법은 `etc` 방법이 호출되는 중첩 수준에 추가 속성이 존재하지 않도록 보장합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
<!-- #### Asserting Attribute Presence / Absence -->
#### Asserting Attribute Presence / Absence

<!-- To assert that an attribute is present or absent, you may use the `has` and `missing` methods: -->
속성의 존재 여부를 확인하려면 `has` 및 `missing` 메소드를 사용할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```

<!-- In addition, the `hasAll` and `missingAll` methods allow asserting the presence or absence of multiple attributes simultaneously: -->
또한 `hasAll` 및 `missingAll` 메서드를 사용하면 여러 속성의 존재 여부를 동시에 확인할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```

<!-- You may use the `hasAny` method to determine if at least one of a given list of attributes is present: -->
`hasAny` 메소드를 사용하여 주어진 속성 목록 중 하나 이상이 존재하는지 확인할 수 있습니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
<!-- #### Asserting Against JSON Collections -->
#### Asserting Against JSON Collections

<!-- Often, your route will return a JSON response that contains multiple items, such as multiple users: -->
종종 라우트는 여러 사용자와 같은 여러 항목이 포함된 JSON 응답을 반환합니다.

```php
Route::get('/users', function () {
    return User::all();
});
```

<!-- In these situations, we may use the fluent JSON object's `has` method to make assertions against the users included in the response. For example, let's assert that the JSON response contains three users. Next, we'll make some assertions about the first user in the collection using the `first` method. The `first` method accepts a closure which receives another assertable JSON string that we can use to make assertions about the first object in the JSON collection: -->
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

<!-- If you would like to make the same assertions against every item in a JSON collection, you may use the `each` method: -->
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
<!-- #### Scoping JSON Collection Assertions -->
#### Scoping JSON Collection Assertions

<!-- Sometimes, your application's routes will return JSON collections that are assigned named keys: -->
때때로 애플리케이션의 라우트는 명명된 키가 할당된 JSON 컬렉션을 반환합니다.

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

<!-- When testing these routes, you may use the `has` method to assert against the number of items in the collection. In addition, you may use the `has` method to scope a chain of assertions: -->
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

<!-- However, instead of making two separate calls to the `has` method to assert against the `users` collection, you may make a single call which provides a closure as its third parameter. When doing so, the closure will automatically be invoked and scoped to the first item in the collection: -->
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
<!-- #### Asserting JSON Types -->
#### Asserting JSON Types

<!-- You may only want to assert that the properties in the JSON response are of a certain type. The `Illuminate\Testing\Fluent\AssertableJson` class provides the `whereType` and `whereAllType` methods for doing just that: -->
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

<!-- You may specify multiple types using the `|` character, or passing an array of types as the second parameter to the `whereType` method. The assertion will be successful if the response value is any of the listed types: -->
`|` 문자를 사용하거나 유형 배열을 `whereType` 메소드에 두 번째 매개변수로 전달하여 여러 유형을 지정할 수 있습니다. 응답 값이 나열된 유형 중 하나이면 어설션이 성공합니다.

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```

<!-- The `whereType` and `whereAllType` methods recognize the following types: `string`, `integer`, `double`, `boolean`, `array`, and `null`. -->
`whereType` 및 `whereAllType` 방법은 `string`, `integer`, `double`, `boolean`, `array` 및 `null` 유형을 인식합니다.

<a name="testing-file-uploads"></a>
<!-- ## Testing File Uploads -->
## Testing File Uploads

<!-- The `Illuminate\Http\UploadedFile` class provides a `fake` method which may be used to generate dummy files or images for testing. This, combined with the `Storage` facade's `fake` method, greatly simplifies the testing of file uploads. For example, you may combine these two features to easily test an avatar upload form: -->
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

<!-- If you would like to assert that a given file does not exist, you may use the `assertMissing` method provided by the `Storage` facade: -->
주어진 파일이 존재하지 않는다고 주장하고 싶다면, `Storage` 파사드에서 제공하는 `assertMissing` 메소드를 사용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
<!-- #### Fake File Customization -->
#### Fake File Customization

<!-- When creating files using the `fake` method provided by the `UploadedFile` class, you may specify the width, height, and size of the image (in kilobytes) in order to better test your application's validation rules: -->
`UploadedFile` 클래스에서 제공하는 `fake` 메서드를 사용하여 파일을 생성할 때 애플리케이션의 유효성 검사 규칙을 더 잘 테스트하기 위해 이미지의 너비, 높이 및 크기(KB)를 지정할 수 있습니다.

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

<!-- In addition to creating images, you may create files of any other type using the `create` method: -->
이미지 생성 외에도 `create` 메소드를 사용하여 다른 유형의 파일을 생성할 수 있습니다.

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

<!-- If needed, you may pass a `$mimeType` argument to the method to explicitly define the MIME type that should be returned by the file: -->
필요한 경우 `$mimeType` 인수를 메서드에 전달하여 파일에서 반환해야 하는 MIME 유형을 명시적으로 정의할 수 있습니다.

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
<!-- ## Testing Views -->
## Testing Views

<!-- Laravel also allows you to render a view without making a simulated HTTP request to the application. To accomplish this, you may call the `view` method within your test. The `view` method accepts the view name and an optional array of data. The method returns an instance of `Illuminate\Testing\TestView`, which offers several methods to conveniently make assertions about the view's contents: -->
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

<!-- The `TestView` class provides the following assertion methods: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, and `assertDontSeeText`. -->
`TestView` 클래스는 `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee` 및 `assertDontSeeText` 어설션 메서드를 제공합니다.

<!-- If needed, you may get the raw, rendered view contents by casting the `TestView` instance to a string: -->
필요한 경우 `TestView` 인스턴스를 문자열로 casting하여 원시 렌더링된 뷰 콘텐츠를 얻을 수 있습니다.

```php
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
<!-- #### Sharing Errors -->
#### Sharing Errors

<!-- Some views may depend on errors shared in the [global error bag provided by Laravel](/docs/master/validation#quick-displaying-the-validation-errors). To hydrate the error bag with error messages, you may use the `withViewErrors` method: -->
일부 뷰는 [global error bag provided by Laravel](/docs/master/validation#quick-displaying-the-validation-errors)에 공유된 오류에 따라 달라질 수 있습니다. 오류 메시지와 함께 오류 백을 수화하려면 `withViewErrors` 메소드를 사용할 수 있습니다.

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
<!-- ### Rendering Blade and Components -->
### Rendering Blade and Components

<!-- If necessary, you may use the `blade` method to evaluate and render a raw [Blade](/docs/master/blade) string. Like the `view` method, the `blade` method returns an instance of `Illuminate\Testing\TestView`: -->
필요한 경우 `blade` 메서드를 사용하여 원시 [Blade](/docs/master/blade) 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로 `blade` 메서드는 `Illuminate\Testing\TestView`의 인스턴스를 반환합니다.

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

<!-- You may use the `component` method to evaluate and render a [Blade component](/docs/master/blade#components). The `component` method returns an instance of `Illuminate\Testing\TestComponent`: -->
`component` 메서드를 사용하여 [Blade component](/docs/master/blade#components)를 평가하고 렌더링할 수 있습니다. `component` 메소드는 `Illuminate\Testing\TestComponent`의 인스턴스를 반환합니다.

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="caching-routes"></a>
<!-- ## Caching Routes -->
## Caching Routes

<!-- Before a test runs, Laravel boots a fresh instance of the application, including collecting all defined routes. If your applications have many route files, you may wish to add the `Illuminate\Foundation\Testing\WithCachedRoutes` trait to your test cases. On tests which use this trait, routes are built once and stored in memory, meaning the route collection process is only run once for all tests in your suite: -->
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
<!-- ## Available Assertions -->
## Available Assertions

<a name="response-assertions"></a>
<!-- ### Response Assertions -->
### Response Assertions

<!-- Laravel's `Illuminate\Testing\TestResponse` class provides a variety of custom assertion methods that you may utilize when testing your application. These assertions may be accessed on the response that is returned by the `json`, `get`, `post`, `put`, and `delete` test methods: -->
Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션을 테스트할 때 활용할 수 있는 다양한 사용자 지정 어설션 방법을 제공합니다. 이러한 어설션은 `json`, `get`, `post`, `put` 및 `delete` 테스트 메서드에서 반환된 응답에서 액세스할 수 있습니다.

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[assertAccepted](#assert-accepted)
[assertBadRequest](#assert-bad-request)
[assertClientError](#assert-client-error)
[assertConflict](#assert-conflict)
[assertCookie](#assert-cookie)
[assertCookieExpired](#assert-cookie-expired)
[assertCookieNotExpired](#assert-cookie-not-expired)
[assertCookieMissing](#assert-cookie-missing)
[assertCreated](#assert-created)
[assertDontSee](#assert-dont-see)
[assertDontSeeText](#assert-dont-see-text)
[assertDownload](#assert-download)
[assertExactJson](#assert-exact-json)
[assertExactJsonStructure](#assert-exact-json-structure)
[assertForbidden](#assert-forbidden)
[assertFound](#assert-found)
[assertGone](#assert-gone)
[assertHeader](#assert-header)
[assertHeaderContains](#assert-header-contains)
[assertHeaderMissing](#assert-header-missing)
[assertInternalServerError](#assert-internal-server-error)
[assertJson](#assert-json)
[assertJsonCount](#assert-json-count)
[assertJsonFragment](#assert-json-fragment)
[assertJsonIsArray](#assert-json-is-array)
[assertJsonIsObject](#assert-json-is-object)
[assertJsonMissing](#assert-json-missing)
[assertJsonMissingExact](#assert-json-missing-exact)
[assertJsonMissingValidationErrors](#assert-json-missing-validation-errors)
[assertJsonPath](#assert-json-path)
[assertJsonMissingPath](#assert-json-missing-path)
[assertJsonStructure](#assert-json-structure)
[assertJsonValidationErrors](#assert-json-validation-errors)
[assertJsonValidationErrorFor](#assert-json-validation-error-for)
[assertLocation](#assert-location)
[assertMethodNotAllowed](#assert-method-not-allowed)
[assertMovedPermanently](#assert-moved-permanently)
[assertContent](#assert-content)
[assertNoContent](#assert-no-content)
[assertStreamed](#assert-streamed)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPaymentRequired](#assert-payment-required)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectBack](#assert-redirect-back)
[assertRedirectBackWithErrors](#assert-redirect-back-with-errors)
[assertRedirectBackWithoutErrors](#assert-redirect-back-without-errors)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertRequestTimeout](#assert-request-timeout)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertServerError](#assert-server-error)
[assertServiceUnavailable](#assert-service-unavailable)
[assertSessionHas](#assert-session-has)
[assertSessionHasInput](#assert-session-has-input)
[assertSessionHasAll](#assert-session-has-all)
[assertSessionHasErrors](#assert-session-has-errors)
[assertSessionHasErrorsIn](#assert-session-has-errors-in)
[assertSessionHasNoErrors](#assert-session-has-no-errors)
[assertSessionDoesntHaveErrors](#assert-session-doesnt-have-errors)
[assertSessionMissing](#assert-session-missing)
[assertStatus](#assert-status)
[assertSuccessful](#assert-successful)
[assertTooManyRequests](#assert-too-many-requests)
[assertUnauthorized](#assert-unauthorized)
[assertUnprocessable](#assert-unprocessable)
[assertUnsupportedMediaType](#assert-unsupported-media-type)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)
-->
[assertAccepted](#assert-accepted)
[assertBadRequest](#assert-bad-request)
[assertClientError](#assert-client-error)
[assertConflict](#assert-conflict)
[assertCookie](#assert-cookie)
[assertCookieExpired](#assert-cookie-expired)
[assertCookieNotExpired](#assert-cookie-not-expired)
[assertCookieMissing](#assert-cookie-missing)
[assertCreated](#assert-created)
[assertDontSee](#assert-dont-see)
[assertDontSeeText](#assert-dont-see-text)
[assertDownload](#assert-download)
[assertExactJson](#assert-exact-json)
[assertExactJsonStructure](#assert-exact-json-structure)
[assertForbidden](#assert-forbidden)
[assertFound](#assert-found)
[assertGone](#assert-gone)
[assertHeader](#assert-header)
[assertHeaderContains](#assert-header-contains)
[assertHeaderMissing](#assert-header-missing)
[assertInternalServerError](#assert-internal-server-error)
[assertJson](#assert-json)
[assertJsonCount](#assert-json-count)
[assertJsonFragment](#assert-json-fragment)
[assertJsonIsArray](#assert-json-is-array)
[assertJsonIsObject](#assert-json-is-object)
[assertJsonMissing](#assert-json-missing)
[assertJsonMissingExact](#assert-json-missing-exact)
[assertJsonMissingValidationErrors](#assert-json-missing-validation-errors)
[assertJsonPath](#assert-json-path)
[assertJsonMissingPath](#assert-json-missing-path)
[assertJsonStructure](#assert-json-structure)
[assertJsonValidationErrors](#assert-json-validation-errors)
[assertJsonValidationErrorFor](#assert-json-validation-error-for)
[assertLocation](#assert-location)
[assertMethodNotAllowed](#assert-method-not-allowed)
[assertMovedPermanently](#assert-moved-permanently)
[assertContent](#assert-content)
[assertNoContent](#assert-no-content)
[assertStreamed](#assert-streamed)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPaymentRequired](#assert-payment-required)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectBack](#assert-redirect-back)
[assertRedirectBackWithErrors](#assert-redirect-back-with-errors)
[assertRedirectBackWithoutErrors](#assert-redirect-back-without-errors)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertRequestTimeout](#assert-request-timeout)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertServerError](#assert-server-error)
[assertServiceUnavailable](#assert-service-unavailable)
[assertSessionHas](#assert-session-has)
[assertSessionHasInput](#assert-session-has-input)
[assertSessionHasAll](#assert-session-has-all)
[assertSessionHasErrors](#assert-session-has-errors)
[assertSessionHasErrorsIn](#assert-session-has-errors-in)
[assertSessionHasNoErrors](#assert-session-has-no-errors)
[assertSessionDoesntHaveErrors](#assert-session-doesnt-have-errors)
[assertSessionMissing](#assert-session-missing)
[assertStatus](#assert-status)
[assertSuccessful](#assert-successful)
[assertTooManyRequests](#assert-too-many-requests)
[assertUnauthorized](#assert-unauthorized)
[assertUnprocessable](#assert-unprocessable)
[assertUnsupportedMediaType](#assert-unsupported-media-type)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)

<!-- </div> -->
</div>

<a name="assert-accepted"></a>
<!-- #### assertAccepted -->
#### assertAccepted

<!-- Assert that the response has an accepted (202) HTTP status code: -->
응답에 승인된(202) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertAccepted();
```

<a name="assert-bad-request"></a>
<!-- #### assertBadRequest -->
#### assertBadRequest

<!-- Assert that the response has a bad request (400) HTTP status code: -->
응답에 잘못된 요청(400) HTTP 상태 코드가 있는지 확인:

```php
$response->assertBadRequest();
```

<a name="assert-client-error"></a>
<!-- #### assertClientError -->
#### assertClientError

<!-- Assert that the response has a client error (>= 400, < 500) HTTP status code: -->
응답에 클라이언트 오류(>= 400, < 500) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertClientError();
```

<a name="assert-conflict"></a>
<!-- #### assertConflict -->
#### assertConflict

<!-- Assert that the response has a conflict (409) HTTP status code: -->
응답에 충돌(409) HTTP 상태 코드가 있는지 확인:

```php
$response->assertConflict();
```

<a name="assert-cookie"></a>
<!-- #### assertCookie -->
#### assertCookie

<!-- Assert that the response contains the given cookie: -->
응답에 주어진 쿠키가 포함되어 있는지 확인:

```php
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
<!-- #### assertCookieExpired -->
#### assertCookieExpired

<!-- Assert that the response contains the given cookie and it is expired: -->
응답에 주어진 쿠키가 포함되어 있고 만료되었는지 확인:

```php
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
<!-- #### assertCookieNotExpired -->
#### assertCookieNotExpired

<!-- Assert that the response contains the given cookie and it is not expired: -->
응답에 주어진 쿠키가 포함되어 있고 만료되지 않았는지 확인:

```php
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
<!-- #### assertCookieMissing -->
#### assertCookieMissing

<!-- Assert that the response does not contain the given cookie: -->
응답에 주어진 쿠키가 포함되어 있지 않은지 확인:

```php
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
<!-- #### assertCreated -->
#### assertCreated

<!-- Assert that the response has a 201 HTTP status code: -->
응답에 201 HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertCreated();
```

<a name="assert-dont-see"></a>
<!-- #### assertDontSee -->
#### assertDontSee

<!-- Assert that the given string is not contained within the response returned by the application. This assertion will automatically escape the given string unless you pass a second argument of `false`: -->
주어진 문자열이 애플리케이션이 반환한 응답에 포함되어 있지 않은지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다.

```php
$response->assertDontSee($value, $escape = true);
```

<a name="assert-dont-see-text"></a>
<!-- #### assertDontSeeText -->
#### assertDontSeeText

<!-- Assert that the given string is not contained within the response text. This assertion will automatically escape the given string unless you pass a second argument of `false`. This method will pass the response content to the `strip_tags` PHP function before making the assertion: -->
주어진 문자열이 응답 텍스트에 포함되어 있지 않은지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다. 이 메소드는 어설션을 수행하기 전에 응답 내용을 `strip_tags` PHP 함수에 전달합니다.

```php
$response->assertDontSeeText($value, $escape = true);
```

<a name="assert-download"></a>
<!-- #### assertDownload -->
#### assertDownload

<!-- Assert that the response is a "download". Typically, this means the invoked route that returned the response returned a `Response::download` response, `BinaryFileResponse`, or `Storage::download` response: -->
응답이 "다운로드"인지 확인합니다. 일반적으로 이는 응답을 반환한 호출된 라우트가 `Response::download` 응답, `BinaryFileResponse` 또는 `Storage::download` 응답을 반환했음을 의미합니다.

```php
$response->assertDownload();
```

<!-- If you wish, you may assert that the downloadable file was assigned a given file name: -->
원하는 경우 다운로드 가능한 파일에 특정 파일 이름이 할당되었다고 주장할 수 있습니다.

```php
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
<!-- #### assertExactJson -->
#### assertExactJson

<!-- Assert that the response contains an exact match of the given JSON data: -->
응답에 주어진 JSON 데이터와 정확히 일치하는 항목이 포함되어 있는지 확인:

```php
$response->assertExactJson(array $data);
```

<a name="assert-exact-json-structure"></a>
<!-- #### assertExactJsonStructure -->
#### assertExactJsonStructure

<!-- Assert that the response contains an exact match of the given JSON structure: -->
응답에 주어진 JSON 구조와 정확히 일치하는 항목이 포함되어 있는지 확인:

```php
$response->assertExactJsonStructure(array $data);
```

<!-- This method is a more strict variant of [assertJsonStructure](#assert-json-structure). In contrast with `assertJsonStructure`, this method will fail if the response contains any keys that aren't explicitly included in the expected JSON structure. -->
이 방법은 [assertJsonStructure](#assert-json-structure)의 보다 엄격한 변형입니다. `assertJsonStructure`와 달리 이 메서드는 응답에 예상 JSON 구조에 명시적으로 포함되지 않은 키가 포함된 경우 실패합니다.

<a name="assert-forbidden"></a>
<!-- #### assertForbidden -->
#### assertForbidden

<!-- Assert that the response has a forbidden (403) HTTP status code: -->
응답에 금지된(403) HTTP 상태 코드가 있는지 확인:

```php
$response->assertForbidden();
```

<a name="assert-found"></a>
<!-- #### assertFound -->
#### assertFound

<!-- Assert that the response has a found (302) HTTP status code: -->
응답에 발견된(302) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertFound();
```

<a name="assert-gone"></a>
<!-- #### assertGone -->
#### assertGone

<!-- Assert that the response has a gone (410) HTTP status code: -->
응답에 사라짐(410) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertGone();
```

<a name="assert-header"></a>
<!-- #### assertHeader -->
#### assertHeader

<!-- Assert that the given header and value is present on the response: -->
주어진 헤더와 값이 응답에 존재하는지 확인:

```php
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-contains"></a>
<!-- #### assertHeaderContains -->
#### assertHeaderContains

<!-- Assert that the given header contains a given substring value: -->
주어진 헤더에 주어진 하위 문자열 값이 포함되어 있는지 확인:

```php
$response->assertHeaderContains($headerName, $value);
```

<a name="assert-header-missing"></a>
<!-- #### assertHeaderMissing -->
#### assertHeaderMissing

<!-- Assert that the given header is not present on the response: -->
주어진 헤더가 응답에 존재하지 않는지 확인:

```php
$response->assertHeaderMissing($headerName);
```

<a name="assert-internal-server-error"></a>
<!-- #### assertInternalServerError -->
#### assertInternalServerError

<!-- Assert that the response has an "Internal Server Error" (500) HTTP status code: -->
응답에 "내부 서버 오류"(500) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertInternalServerError();
```

<a name="assert-json"></a>
<!-- #### assertJson -->
#### assertJson

<!-- Assert that the response contains the given JSON data: -->
응답에 주어진 JSON 데이터가 포함되어 있는지 확인:

```php
$response->assertJson(array $data, $strict = false);
```

<!-- The `assertJson` method converts the response to an array to verify that the given array exists within the JSON response returned by the application. So, if there are other properties in the JSON response, this test will still pass as long as the given fragment is present. -->
`assertJson` 메소드는 응답을 배열로 변환하여 지정된 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 있는 경우 지정된 조각이 존재하는 한 이 테스트는 계속 통과됩니다.

<a name="assert-json-count"></a>
<!-- #### assertJsonCount -->
#### assertJsonCount

<!-- Assert that the response JSON has an array with the expected number of items at the given key: -->
응답 JSON에 주어진 키에 예상되는 항목 수의 배열이 있는지 확인:

```php
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
<!-- #### assertJsonFragment -->
#### assertJsonFragment

<!-- Assert that the response contains the given JSON data anywhere in the response: -->
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
<!-- #### assertJsonIsArray -->
#### assertJsonIsArray

<!-- Assert that the response JSON is an array: -->
JSON 응답이 배열인지 확인합니다.

```php
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
<!-- #### assertJsonIsObject -->
#### assertJsonIsObject

<!-- Assert that the response JSON is an object: -->
JSON 응답이 객체인지 확인합니다:

```php
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
<!-- #### assertJsonMissing -->
#### assertJsonMissing

<!-- Assert that the response does not contain the given JSON data: -->
응답에 주어진 JSON 데이터가 포함되어 있지 않은지 확인:

```php
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
<!-- #### assertJsonMissingExact -->
#### assertJsonMissingExact

<!-- Assert that the response does not contain the exact JSON data: -->
응답에 정확한 JSON 데이터가 포함되어 있지 않은지 확인:

```php
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
<!-- #### assertJsonMissingValidationErrors -->
#### assertJsonMissingValidationErrors

<!-- Assert that the response has no JSON validation errors for the given keys: -->
응답에 주어진 키에 대한 JSON 유효성 검사 오류가 없는지 확인:

```php
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드를 사용하여 응답에 JSON로 반환된 유효성 검사 오류가 없고 **오류가 세션 저장소에 플래시되지 않았음**을 주장할 수 있습니다.

<a name="assert-json-path"></a>
<!-- #### assertJsonPath -->
#### assertJsonPath

<!-- Assert that the response contains the given data at the specified path: -->
응답에 지정된 경로에 지정된 데이터가 포함되어 있는지 확인:

```php
$response->assertJsonPath($path, $expectedValue);
```

<!-- For example, if the following JSON response is returned by your application: -->
예를 들어 애플리케이션에서 다음 JSON 응답을 반환하는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that the `name` property of the `user` object matches a given value like so: -->
다음과 같이 `user` 개체의 `name` 속성이 지정된 값과 일치한다고 주장할 수 있습니다.

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
<!-- #### assertJsonMissingPath -->
#### assertJsonMissingPath

<!-- Assert that the response does not contain the given path: -->
응답에 주어진 경로가 포함되어 있지 않은지 확인:

```php
$response->assertJsonMissingPath($path);
```

<!-- For example, if the following JSON response is returned by your application: -->
예를 들어 애플리케이션에서 다음 JSON 응답을 반환하는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that it does not contain the `email` property of the `user` object: -->
`user` 객체의 `email` 속성이 포함되어 있지 않다고 주장할 수 있습니다.

```php
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
<!-- #### assertJsonStructure -->
#### assertJsonStructure

<!-- Assert that the response has a given JSON structure: -->
응답에 주어진 JSON 구조가 있는지 확인:

```php
$response->assertJsonStructure(array $structure);
```

<!-- For example, if the JSON response returned by your application contains the following data: -->
예를 들어, 애플리케이션에서 반환된 JSON 응답에 다음 데이터가 포함되어 있는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that the JSON structure matches your expectations like so: -->
다음과 같이 JSON 구조가 기대와 일치한다고 주장할 수 있습니다.

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

<!-- Sometimes, JSON responses returned by your application may contain arrays of objects: -->
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

<!-- In this situation, you may use the `*` character to assert against the structure of all of the objects in the array: -->
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
<!-- #### assertJsonValidationErrors -->
#### assertJsonValidationErrors

<!-- Assert that the response has the given JSON validation errors for the given keys. This method should be used when asserting against responses where the validation errors are returned as a JSON structure instead of being flashed to the session: -->
응답에 주어진 키에 대해 주어진 JSON 유효성 검사 오류가 있는지 확인합니다. 유효성 검사 오류가 세션에 플래시되는 대신 JSON 구조로 반환되는 응답에 대해 어설션할 때 이 메서드를 사용해야 합니다.

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드를 사용하면 응답에 JSON로 반환된 유효성 검사 오류가 있거나 **오류가 세션 저장소에 플래시되었음**을 주장하는 데 사용할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
<!-- #### assertJsonValidationErrorFor -->
#### assertJsonValidationErrorFor

<!-- Assert the response has any JSON validation errors for the given key: -->
응답에 지정된 키에 대한 JSON 유효성 검사 오류가 있는지 확인합니다.

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-method-not-allowed"></a>
<!-- #### assertMethodNotAllowed -->
#### assertMethodNotAllowed

<!-- Assert that the response has a method not allowed (405) HTTP status code: -->
응답에 허용되지 않는 메서드(405) HTTP 상태 코드가 있는지 확인:

```php
$response->assertMethodNotAllowed();
```

<a name="assert-moved-permanently"></a>
<!-- #### assertMovedPermanently -->
#### assertMovedPermanently

<!-- Assert that the response has a moved permanently (301) HTTP status code: -->
응답이 영구적으로 이동했는지(301) HTTP 상태 코드를 확인합니다.

```php
$response->assertMovedPermanently();
```

<a name="assert-location"></a>
<!-- #### assertLocation -->
#### assertLocation

<!-- Assert that the response has the given URI value in the `Location` header: -->
응답의 `Location` 헤더에 지정된 URI 값이 있는지 확인합니다.

```php
$response->assertLocation($uri);
```

<a name="assert-content"></a>
<!-- #### assertContent -->
#### assertContent

<!-- Assert that the given string matches the response content: -->
주어진 문자열이 응답 내용과 일치하는지 확인합니다:

```php
$response->assertContent($value);
```

<a name="assert-no-content"></a>
<!-- #### assertNoContent -->
#### assertNoContent

<!-- Assert that the response has the given HTTP status code and no content: -->
응답에 주어진 HTTP 상태 코드가 있고 내용이 없는지 확인:

```php
$response->assertNoContent($status = 204);
```

<a name="assert-streamed"></a>
<!-- #### assertStreamed -->
#### assertStreamed

<!-- Assert that the response was a streamed response: -->
응답이 스트리밍된 응답인지 확인합니다.

```
$response->assertStreamed();
```

<a name="assert-streamed-content"></a>
<!-- #### assertStreamedContent -->
#### assertStreamedContent

<!-- Assert that the given string matches the streamed response content: -->
주어진 문자열이 스트리밍된 응답 콘텐츠와 일치하는지 확인합니다.

```php
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
<!-- #### assertNotFound -->
#### assertNotFound

<!-- Assert that the response has a not found (404) HTTP status code: -->
응답에 찾을 수 없음(404) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertNotFound();
```

<a name="assert-ok"></a>
<!-- #### assertOk -->
#### assertOk

<!-- Assert that the response has a 200 HTTP status code: -->
응답에 200 HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertOk();
```

<a name="assert-payment-required"></a>
<!-- #### assertPaymentRequired -->
#### assertPaymentRequired

<!-- Assert that the response has a payment required (402) HTTP status code: -->
응답에 결제 필요(402) HTTP 상태 코드가 있는지 확인:

```php
$response->assertPaymentRequired();
```

<a name="assert-plain-cookie"></a>
<!-- #### assertPlainCookie -->
#### assertPlainCookie

<!-- Assert that the response contains the given unencrypted cookie: -->
응답에 암호화되지 않은 주어진 쿠키가 포함되어 있는지 확인:

```php
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
<!-- #### assertRedirect -->
#### assertRedirect

<!-- Assert that the response is a redirect to the given URI: -->
응답이 주어진 URI로의 리디렉션인지 확인:

```php
$response->assertRedirect($uri = null);
```

<a name="assert-redirect-back"></a>
<!-- #### assertRedirectBack -->
#### assertRedirectBack

<!-- Assert whether the response is redirecting back to the previous page: -->
응답이 이전 페이지로 다시 리디렉션되는지 확인합니다.

```php
$response->assertRedirectBack();
```

<a name="assert-redirect-back-with-errors"></a>
<!-- #### assertRedirectBackWithErrors -->
#### assertRedirectBackWithErrors

<!-- Assert whether the response is redirecting back to the previous page and the [session has the given errors](#assert-session-has-errors): -->
응답이 이전 페이지로 다시 리디렉션되고 [session has the given errors](#assert-session-has-errors)인지 확인합니다.

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<a name="assert-redirect-back-without-errors"></a>
<!-- #### assertRedirectBackWithoutErrors -->
#### assertRedirectBackWithoutErrors

<!-- Assert whether the response is redirecting back to the previous page and the session does not contain any error messages: -->
응답이 이전 페이지로 다시 리디렉션되고 세션에 오류 메시지가 없는지 확인합니다.

```php
$response->assertRedirectBackWithoutErrors();
```

<a name="assert-redirect-contains"></a>
<!-- #### assertRedirectContains -->
#### assertRedirectContains

<!-- Assert whether the response is redirecting to a URI that contains the given string: -->
응답이 주어진 문자열을 포함하는 URI로 리디렉션되는지 확인합니다.

```php
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
<!-- #### assertRedirectToRoute -->
#### assertRedirectToRoute

<!-- Assert that the response is a redirect to the given [named route](/docs/master/routing#named-routes): -->
응답이 주어진 [named route](/docs/master/routing#named-routes)에 대한 리디렉션인지 확인합니다.

```php
$response->assertRedirectToRoute($name, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
<!-- #### assertRedirectToSignedRoute -->
#### assertRedirectToSignedRoute

<!-- Assert that the response is a redirect to the given [signed route](/docs/master/urls#signed-urls): -->
응답이 주어진 [signed route](/docs/master/urls#signed-urls)에 대한 리디렉션인지 확인합니다.

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-request-timeout"></a>
<!-- #### assertRequestTimeout -->
#### assertRequestTimeout

<!-- Assert that the response has a request timeout (408) HTTP status code: -->
응답에 요청 시간 초과(408) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertRequestTimeout();
```

<a name="assert-see"></a>
<!-- #### assertSee -->
#### assertSee

<!-- Assert that the given string is contained within the response. This assertion will automatically escape the given string unless you pass a second argument of `false`: -->
주어진 문자열이 응답 내에 포함되어 있는지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다.

```php
$response->assertSee($value, $escape = true);
```

<a name="assert-see-in-order"></a>
<!-- #### assertSeeInOrder -->
#### assertSeeInOrder

<!-- Assert that the given strings are contained in order within the response. This assertion will automatically escape the given strings unless you pass a second argument of `false`: -->
주어진 문자열이 응답 내에 순서대로 포함되어 있는지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다.

```php
$response->assertSeeInOrder(array $values, $escape = true);
```

<a name="assert-see-text"></a>
<!-- #### assertSeeText -->
#### assertSeeText

<!-- Assert that the given string is contained within the response text. This assertion will automatically escape the given string unless you pass a second argument of `false`. The response content will be passed to the `strip_tags` PHP function before the assertion is made: -->
주어진 문자열이 응답 텍스트 내에 포함되어 있는지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다. 어설션이 이루어지기 전에 응답 콘텐츠가 `strip_tags` PHP 함수에 전달됩니다.

```php
$response->assertSeeText($value, $escape = true);
```

<a name="assert-see-text-in-order"></a>
<!-- #### assertSeeTextInOrder -->
#### assertSeeTextInOrder

<!-- Assert that the given strings are contained in order within the response text. This assertion will automatically escape the given strings unless you pass a second argument of `false`. The response content will be passed to the `strip_tags` PHP function before the assertion is made: -->
주어진 문자열이 응답 텍스트 내에 순서대로 포함되어 있는지 확인합니다. 이 어설션은 `false`의 두 번째 인수를 전달하지 않는 한 자동으로 주어진 문자열을 이스케이프합니다. 어설션이 이루어지기 전에 응답 콘텐츠가 `strip_tags` PHP 함수에 전달됩니다.

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```

<a name="assert-server-error"></a>
<!-- #### assertServerError -->
#### assertServerError

<!-- Assert that the response has a server error (>= 500 , < 600) HTTP status code: -->
응답에 서버 오류(>= 500, < 600) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertServerError();
```

<a name="assert-service-unavailable"></a>
<!-- #### assertServiceUnavailable -->
#### assertServiceUnavailable

<!-- Assert that the response has a "Service Unavailable" (503) HTTP status code: -->
응답에 "Service Unavailable"(503) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertServiceUnavailable();
```

<a name="assert-session-has"></a>
<!-- #### assertSessionHas -->
#### assertSessionHas

<!-- Assert that the session contains the given piece of data: -->
세션에 주어진 데이터가 포함되어 있는지 확인:

```php
$response->assertSessionHas($key, $value = null);
```

<!-- If needed, a closure can be provided as the second argument to the `assertSessionHas` method. The assertion will pass if the closure returns `true`: -->
필요한 경우 클로저를 `assertSessionHas` 메서드의 두 번째 인수로 제공할 수 있습니다. 클로저가 `true`를 반환하면 어설션이 통과됩니다.

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
<!-- #### assertSessionHasInput -->
#### assertSessionHasInput

<!-- Assert that the session has a given value in the [flashed input array](/docs/master/responses#redirecting-with-flashed-session-data): -->
세션이 [flashed input array](/docs/master/responses#redirecting-with-flashed-session-data)에 지정된 값을 가지고 있는지 확인합니다.

```php
$response->assertSessionHasInput($key, $value = null);
```

<!-- If needed, a closure can be provided as the second argument to the `assertSessionHasInput` method. The assertion will pass if the closure returns `true`: -->
필요한 경우 클로저를 `assertSessionHasInput` 메서드의 두 번째 인수로 제공할 수 있습니다. 클로저가 `true`를 반환하면 어설션이 통과됩니다.

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
<!-- #### assertSessionHasAll -->
#### assertSessionHasAll

<!-- Assert that the session contains a given array of key / value pairs: -->
세션에 주어진 키/값 쌍 배열이 포함되어 있는지 확인:

```php
$response->assertSessionHasAll(array $data);
```

<!-- For example, if your application's session contains `name` and `status` keys, you may assert that both exist and have the specified values like so: -->
예를 들어, 애플리케이션의 세션에 `name` 및 `status` 키가 포함된 경우 두 키가 모두 존재하고 다음과 같이 지정된 값을 갖는다고 주장할 수 있습니다.

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
<!-- #### assertSessionHasErrors -->
#### assertSessionHasErrors

<!-- Assert that the session contains an error for the given `$keys`. If `$keys` is an associative array, assert that the session contains a specific error message (value) for each field (key). This method should be used when testing routes that flash validation errors to the session instead of returning them as a JSON structure: -->
세션에 주어진 `$keys`에 대한 오류가 포함되어 있는지 확인합니다. `$keys`가 연관 배열인 경우 세션에 각 필드(키)에 대한 특정 오류 메시지(값)가 포함되어 있음을 어설션합니다. 이 방법은 유효성 검사 오류를 JSON 구조로 반환하는 대신 세션에 플래시하는 라우트를 테스트할 때 사용해야 합니다.

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```

<!-- For example, to assert that the `name` and `email` fields have validation error messages that were flashed to the session, you may invoke the `assertSessionHasErrors` method like so: -->
예를 들어, `name` 및 `email` 필드에 세션에 플래시된 유효성 검사 오류 메시지가 있음을 확인하려면 다음과 같이 `assertSessionHasErrors` 메서드를 호출할 수 있습니다.

```php
$response->assertSessionHasErrors(['name', 'email']);
```

<!-- Or, you may assert that a given field has a particular validation error message: -->
또는 특정 필드에 특정 유효성 검사 오류 메시지가 있다고 주장할 수도 있습니다.

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드를 사용하면 응답에 JSON로 반환된 유효성 검사 오류가 있거나 **오류가 세션 저장소에 플래시되었음**을 주장하는 데 사용할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
<!-- #### assertSessionHasErrorsIn -->
#### assertSessionHasErrorsIn

<!-- Assert that the session contains an error for the given `$keys` within a specific [error bag](/docs/master/validation#named-error-bags). If `$keys` is an associative array, assert that the session contains a specific error message (value) for each field (key), within the error bag: -->
세션이 특정 [error bag](/docs/master/validation#named-error-bags) 내에서 주어진 `$keys`에 대한 오류를 포함하고 있는지 확인합니다. `$keys`가 연관 배열인 경우 세션에 오류 백 내에서 각 필드(키)에 대한 특정 오류 메시지(값)가 포함되어 있음을 어설션합니다.

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
<!-- #### assertSessionHasNoErrors -->
#### assertSessionHasNoErrors

<!-- Assert that the session has no validation errors: -->
세션에 유효성 검사 오류가 없는지 확인합니다.

```php
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
<!-- #### assertSessionDoesntHaveErrors -->
#### assertSessionDoesntHaveErrors

<!-- Assert that the session has no validation errors for the given keys: -->
세션에 주어진 키에 대한 유효성 검사 오류가 없는지 확인:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드를 사용하여 응답에 JSON로 반환된 유효성 검사 오류가 없고 **오류가 세션 저장소에 플래시되지 않았음**을 주장할 수 있습니다.

<a name="assert-session-missing"></a>
<!-- #### assertSessionMissing -->
#### assertSessionMissing

<!-- Assert that the session does not contain the given key: -->
세션에 주어진 키가 포함되어 있지 않은지 확인:

```php
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
<!-- #### assertStatus -->
#### assertStatus

<!-- Assert that the response has a given HTTP status code: -->
응답에 주어진 HTTP 상태 코드가 있는지 확인:

```php
$response->assertStatus($code);
```

<a name="assert-successful"></a>
<!-- #### assertSuccessful -->
#### assertSuccessful

<!-- Assert that the response has a successful (>= 200 and < 300) HTTP status code: -->
응답에 성공(>= 200 및 < 300) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertSuccessful();
```

<a name="assert-too-many-requests"></a>
<!-- #### assertTooManyRequests -->
#### assertTooManyRequests

<!-- Assert that the response has a too many requests (429) HTTP status code: -->
응답에 너무 많은 요청(429)이 있는지 확인합니다. HTTP 상태 코드:

```php
$response->assertTooManyRequests();
```

<a name="assert-unauthorized"></a>
<!-- #### assertUnauthorized -->
#### assertUnauthorized

<!-- Assert that the response has an unauthorized (401) HTTP status code: -->
응답에 승인되지 않은(401) HTTP 상태 코드가 있는지 확인:

```php
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
<!-- #### assertUnprocessable -->
#### assertUnprocessable

<!-- Assert that the response has an unprocessable entity (422) HTTP status code: -->
응답에 처리할 수 없는 엔터티(422) HTTP 상태 코드가 있는지 확인합니다.

```php
$response->assertUnprocessable();
```

<a name="assert-unsupported-media-type"></a>
<!-- #### assertUnsupportedMediaType -->
#### assertUnsupportedMediaType

<!-- Assert that the response has an unsupported media type (415) HTTP status code: -->
응답에 지원되지 않는 미디어 유형(415) HTTP 상태 코드가 있는지 확인:

```php
$response->assertUnsupportedMediaType();
```

<a name="assert-valid"></a>
<!-- #### assertValid -->
#### assertValid

<!-- Assert that the response has no validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
응답에 주어진 키에 대한 유효성 검사 오류가 없는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 유효성 검사 오류가 세션에 플래시된 응답에 대해 어설션하는 데 사용될 수 있습니다.

```php
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
<!-- #### assertInvalid -->
#### assertInvalid

<!-- Assert that the response has validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
응답에 주어진 키에 대한 유효성 검사 오류가 있는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 유효성 검사 오류가 세션에 플래시된 응답에 대해 어설션하는 데 사용될 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

<!-- You may also assert that a given key has a particular validation error message. When doing so, you may provide the entire message or only a small portion of the message: -->
또한 특정 키에 특정 유효성 검사 오류 메시지가 있다고 주장할 수도 있습니다. 그렇게 할 때 전체 메시지를 제공하거나 메시지의 일부만 제공할 수 있습니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

<!-- If you would like to assert that the given fields are the only fields with validation errors, you may use the `assertOnlyInvalid` method: -->
주어진 필드가 유효성 검사 오류가 있는 유일한 필드라고 주장하려면 `assertOnlyInvalid` 메서드를 사용할 수 있습니다.

```php
$response->assertOnlyInvalid(['name', 'email']);
```

<a name="assert-view-has"></a>
<!-- #### assertViewHas -->
#### assertViewHas

<!-- Assert that the response view contains a given piece of data: -->
뷰 응답에 주어진 데이터가 포함되어 있는지 확인:

```php
$response->assertViewHas($key, $value = null);
```

<!-- Passing a closure as the second argument to the `assertViewHas` method will allow you to inspect and make assertions against a particular piece of view data: -->
클로저를 `assertViewHas` 메소드의 두 번째 인수로 전달하면 뷰 데이터의 특정 부분을 검사하고 이에 대한 어설션을 만들 수 있습니다.

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

<!-- In addition, view data may be accessed as array variables on the response, allowing you to conveniently inspect it: -->
또한 뷰 데이터는 응답에서 배열 변수로 액세스할 수 있으므로 편리하게 검사할 수 있습니다.

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
<!-- #### assertViewHasAll -->
#### assertViewHasAll

<!-- Assert that the response view has a given list of data: -->
뷰 응답에 주어진 데이터 목록이 있는지 확인:

```php
$response->assertViewHasAll(array $data);
```

<!-- This method may be used to assert that the view simply contains data matching the given keys: -->
이 메소드는 뷰가 단순히 주어진 키와 일치하는 데이터를 포함하고 있음을 주장하는 데 사용될 수 있습니다.

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```

<!-- Or, you may assert that the view data is present and has specific values: -->
또는 뷰 데이터가 존재하고 특정 값을 가지고 있다고 주장할 수 있습니다.

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
<!-- #### assertViewIs -->
#### assertViewIs

<!-- Assert that the given view was returned by the route: -->
주어진 뷰가 라우트에 의해 반환되었는지 확인:

```php
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
<!-- #### assertViewMissing -->
#### assertViewMissing

<!-- Assert that the given data key was not made available to the view returned in the application's response: -->
주어진 데이터 키가 애플리케이션의 응답으로 반환된 뷰에 사용 가능하지 않은지 확인:

```php
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
<!-- ### Authentication Assertions -->
### Authentication Assertions

<!-- Laravel also provides a variety of authentication related assertions that you may utilize within your application's feature tests. Note that these methods are invoked on the test class itself and not the `Illuminate\Testing\TestResponse` instance returned by methods such as `get` and `post`. -->
Laravel는 또한 애플리케이션의 기능 테스트 내에서 활용할 수 있는 다양한 인증 관련 어설션을 제공합니다. 이러한 메서드는 `get` 및 `post`와 같은 메서드에서 반환된 `Illuminate\Testing\TestResponse` 인스턴스가 아니라 테스트 클래스 자체에서 호출됩니다.

<a name="assert-authenticated"></a>
<!-- #### assertAuthenticated -->
#### assertAuthenticated

<!-- Assert that a user is authenticated: -->
사용자가 인증되었는지 확인:

```php
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
<!-- #### assertGuest -->
#### assertGuest

<!-- Assert that a user is not authenticated: -->
사용자가 인증되지 않았는지 확인:

```php
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
<!-- #### assertAuthenticatedAs -->
#### assertAuthenticatedAs

<!-- Assert that a specific user is authenticated: -->
특정 사용자가 인증되었는지 확인:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
<!-- ## Validation Assertions -->
## Validation Assertions

<!-- Laravel provides two primary validation related assertions that you may use to ensure the data provided in your request was either valid or invalid. -->
Laravel는 요청에 제공된 데이터가 유효한지 또는 유효하지 않은지 확인하는 데 사용할 수 있는 두 가지 기본 검증 관련 어설션을 제공합니다.

<a name="validation-assert-valid"></a>
<!-- #### assertValid -->
#### assertValid

<!-- Assert that the response has no validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
응답에 주어진 키에 대한 유효성 검사 오류가 없는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 유효성 검사 오류가 세션에 플래시된 응답에 대해 어설션하는 데 사용될 수 있습니다.

```php
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
<!-- #### assertInvalid -->
#### assertInvalid

<!-- Assert that the response has validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
응답에 주어진 키에 대한 유효성 검사 오류가 있는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 유효성 검사 오류가 세션에 플래시된 응답에 대해 어설션하는 데 사용될 수 있습니다.

```php
$response->assertInvalid(['name', 'email']);
```

<!-- You may also assert that a given key has a particular validation error message. When doing so, you may provide the entire message or only a small portion of the message: -->
또한 특정 키에 특정 유효성 검사 오류 메시지가 있다고 주장할 수도 있습니다. 그렇게 할 때 전체 메시지를 제공하거나 메시지의 일부만 제공할 수 있습니다.

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
