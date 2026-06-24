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
    - [Rendering Blade & Components](#rendering-blade-and-components)
- [Available Assertions](#available-assertions)
    - [Response Assertions](#response-assertions)
    - [Authentication Assertions](#authentication-assertions)
    - [Validation Assertions](#validation-assertions)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a very fluent API for making HTTP requests to your application and examining the responses. For example, take a look at the feature test defined below: -->
Laravel은 애플리케이션에 HTTP 요청을 보내고, 그 응답을 검사할 수 있는 매우 유창한(Fluent) API를 제공합니다. 예를 들어, 아래에 정의된 기능 테스트를 살펴보십시오.

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_a_basic_request()
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

<!-- The `get` method makes a `GET` request into the application, while the `assertStatus` method asserts that the returned response should have the given HTTP status code. In addition to this simple assertion, Laravel also contains a variety of assertions for inspecting the response headers, content, JSON structure, and more. -->
`get` 메서드는 애플리케이션 내에서 `GET` 요청을 수행하며, `assertStatus` 메서드는 반환된 응답의 HTTP 상태 코드가 지정한 값과 일치하는지 확인합니다. 이 외에도 Laravel은 응답 헤더, 내용, JSON 구조 등을 검사할 수 있는 다양한 assertion 메서드를 제공합니다.

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make a request to your application, you may invoke the `get`, `post`, `put`, `patch`, or `delete` methods within your test. These methods do not actually issue a "real" HTTP request to your application. Instead, the entire network request is simulated internally. -->
테스트 내에서 애플리케이션에 요청하려면 `get`, `post`, `put`, `patch`, `delete` 메서드를 사용할 수 있습니다. 이 메서드들은 실제 "HTTP" 요청을 발생시키는 것이 아니라, 내부적으로 네트워크 요청을 시뮬레이션합니다.

<!-- Instead of returning an `Illuminate\Http\Response` instance, test request methods return an instance of `Illuminate\Testing\TestResponse`, which provides a [variety of helpful assertions](#available-assertions) that allow you to inspect your application's responses: -->
이러한 테스트 요청 메서드는 `Illuminate\Http\Response` 인스턴스를 반환하지 않고, 대신 `Illuminate\Testing\TestResponse` 인스턴스를 반환합니다. 이 객체는 애플리케이션의 응답을 검사할 수 있는 [variety of helpful assertions](#available-assertions) 기능을 제공합니다.

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_a_basic_request()
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```

<!-- In general, each of your tests should only make one request to your application. Unexpected behavior may occur if multiple requests are executed within a single test method. -->
일반적으로, 각 테스트는 애플리케이션에 한 번의 요청만을 보내는 것이 좋습니다. 하나의 테스트 메서드에서 여러 요청을 실행하면 예기치 않은 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해, 테스트를 실행할 때 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
<!-- ### Customizing Request Headers -->
### Customizing Request Headers

<!-- You may use the `withHeaders` method to customize the request's headers before it is sent to the application. This method allows you to add any custom headers you would like to the request: -->
요청을 애플리케이션에 보내기 전에 `withHeaders` 메서드를 사용해서 요청의 헤더를 커스터마이즈할 수 있습니다. 이 메서드를 이용해 원하는 어떤 커스텀 헤더도 쉽게 추가할 수 있습니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_interacting_with_headers()
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
요청을 보내기 전에 쿠키 값을 설정하려면 `withCookie` 또는 `withCookies` 메서드를 사용할 수 있습니다. `withCookie`는 쿠키의 이름과 값을 인수로 받아 하나의 쿠키를 추가하고, `withCookies`는 이름/값 쌍의 배열을 받아 여러 개의 쿠키를 한 번에 추가할 수 있습니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_cookies()
    {
        $response = $this->withCookie('color', 'blue')->get('/');

        $response = $this->withCookies([
            'color' => 'blue',
            'name' => 'Taylor',
        ])->get('/');
    }
}
```

<a name="session-and-authentication"></a>
<!-- ### Session / Authentication -->
### Session / Authentication

<!-- Laravel provides several helpers for interacting with the session during HTTP testing. First, you may set the session data to a given array using the `withSession` method. This is useful for loading the session with data before issuing a request to your application: -->
HTTP 테스트를 진행할 때 세션을 다루기 위한 여러 가지 헬퍼가 제공됩니다. 먼저, `withSession` 메서드를 사용하면 세션에 특정 데이터를 미리 저장할 수 있습니다. 이 방법은 요청 전에 세션에 데이터를 로드할 때 유용합니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_the_session()
    {
        $response = $this->withSession(['banned' => false])->get('/');
    }
}
```

<!-- Laravel's session is typically used to maintain state for the currently authenticated user. Therefore, the `actingAs` helper method provides a simple way to authenticate a given user as the current user. For example, we may use a [model factory](/docs/9.x/eloquent-factories) to generate and authenticate a user: -->
Laravel의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 이에 따라, `actingAs` 헬퍼 메서드를 사용하면 지정한 사용자를 현재 사용자로 쉽게 인증할 수 있습니다. 예를 들어, [model factory](/docs/9.x/eloquent-factories)를 사용하여 사용자를 생성하고 인증할 수 있습니다.

```
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_an_action_that_requires_authentication()
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
                         ->withSession(['banned' => false])
                         ->get('/');
    }
}
```

<!-- You may also specify which guard should be used to authenticate the given user by passing the guard name as the second argument to the `actingAs` method. The guard that is provided to the `actingAs` method will also become the default guard for the duration of the test: -->
또한, 두 번째 인수로 guard 이름을 `actingAs` 메서드에 전달하여 사용할 guard를 지정할 수 있습니다. `actingAs` 메서드에 지정한 guard는 테스트가 진행되는 동안 기본 guard로도 사용됩니다.

```
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
<!-- ### Debugging Responses -->
### Debugging Responses

<!-- After making a test request to your application, the `dump`, `dumpHeaders`, and `dumpSession` methods may be used to examine and debug the response contents: -->
테스트 요청을 보낸 후, `dump`, `dumpHeaders`, `dumpSession` 메서드를 이용해 응답 내용을 확인하고 디버깅할 수 있습니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_basic_test()
    {
        $response = $this->get('/');

        $response->dumpHeaders();

        $response->dumpSession();

        $response->dump();
    }
}
```

<!-- Alternatively, you may use the `dd`, `ddHeaders`, and `ddSession` methods to dump information about the response and then stop execution: -->
또는, `dd`, `ddHeaders`, `ddSession` 메서드를 사용하면 응답 정보를 출력하고 바로 실행을 중단할 수 있습니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     *
     * @return void
     */
    public function test_basic_test()
    {
        $response = $this->get('/');

        $response->ddHeaders();

        $response->ddSession();

        $response->dd();
    }
}
```

<a name="exception-handling"></a>
<!-- ### Exception Handling -->
### Exception Handling

<!-- Sometimes you may want to test that your application is throwing a specific exception. To ensure that the exception does not get caught by Laravel's exception handler and returned as an HTTP response, you may invoke the `withoutExceptionHandling` method before making your request: -->
때로는 애플리케이션이 특정 예외를 던지는지 테스트하고 싶을 수 있습니다. Laravel의 예외 핸들러에서 예외가 잡혀서 HTTP 응답으로 반환되는 것을 막으려면, 요청 전에 `withoutExceptionHandling` 메서드를 호출할 수 있습니다.

```
$response = $this->withoutExceptionHandling()->get('/');
```

<!-- In addition, if you would like to ensure that your application is not utilizing features that have been deprecated by the PHP language or the libraries your application is using, you may invoke the `withoutDeprecationHandling` method before making your request. When deprecation handling is disabled, deprecation warnings will be converted to exceptions, thus causing your test to fail: -->
또한, PHP 언어나 애플리케이션에서 사용하는 라이브러리에서 더 이상 권장되지 않는(deprecated) 기능이 사용되는지 테스트하고 싶다면, 요청 전에 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 이렇게 하면 deprecated 경고가 예외로 전환되어, 테스트가 실패하게 됩니다.

```
$response = $this->withoutDeprecationHandling()->get('/');
```

<a name="testing-json-apis"></a>
<!-- ## Testing JSON APIs -->
## Testing JSON APIs

<!-- Laravel also provides several helpers for testing JSON APIs and their responses. For example, the `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, and `optionsJson` methods may be used to issue JSON requests with various HTTP verbs. You may also easily pass data and headers to these methods. To get started, let's write a test to make a `POST` request to `/api/user` and assert that the expected JSON data was returned: -->
Laravel은 JSON API 및 그 응답을 테스트할 수 있는 여러 헬퍼를 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메서드를 통해 다양한 HTTP 메서드로 JSON 요청을 손쉽게 보낼 수 있습니다. 또한 데이터와 헤더도 간편하게 전달할 수 있습니다. 간단하게, `/api/user`로 `POST` 요청을 보내고 예상한 JSON 데이터가 반환되는지 확인하는 테스트 코드를 작성해보겠습니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_making_an_api_request()
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
또한, JSON 응답 데이터는 배열 변수처럼 접근할 수 있으므로, 각 값이 맞게 반환되었는지 쉽게 검사할 수 있습니다.

```
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환한 뒤 `PHPUnit::assertArraySubset`을 활용하여 지정한 배열이 응답 JSON에 포함되어 있는지 확인합니다. 즉, 응답 JSON에 다른 프로퍼티가 존재해도 지정한 부분이 포함되어 있으면 이 테스트는 통과합니다.

<a name="verifying-exact-match"></a>
<!-- #### Asserting Exact JSON Matches -->
#### Asserting Exact JSON Matches

<!-- As previously mentioned, the `assertJson` method may be used to assert that a fragment of JSON exists within the JSON response. If you would like to verify that a given array **exactly matches** the JSON returned by your application, you should use the `assertExactJson` method: -->
앞서 설명했듯이, `assertJson` 메서드는 JSON 응답에 일부만 포함되어 있는지 검사합니다. 응답 JSON과 지정한 배열이 **정확히 일치하는지** 확인하고 싶다면 `assertExactJson` 메서드를 사용해야 합니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_asserting_an_exact_json_match()
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
<!-- #### Asserting On JSON Paths -->
#### Asserting On JSON Paths

<!-- If you would like to verify that the JSON response contains the given data at a specified path, you should use the `assertJsonPath` method: -->
JSON 응답에서 특정 경로의 데이터가 올바른지 확인하고 싶다면, `assertJsonPath` 메서드를 사용할 수 있습니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_asserting_a_json_paths_value()
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJsonPath('team.owner.name', 'Darian');
    }
}
```

<!-- The `assertJsonPath` method also accepts a closure, which may be used to dynamically determine if the assertion should pass: -->
`assertJsonPath` 메서드는 클로저도 받을 수 있으므로, 동적으로 assertion이 통과해야 할 조건을 지정할 수 있습니다.

```
$response->assertJsonPath('team.owner.name', fn ($name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
<!-- ### Fluent JSON Testing -->
### Fluent JSON Testing

<!-- Laravel also offers a beautiful way to fluently test your application's JSON responses. To get started, pass a closure to the `assertJson` method. This closure will be invoked with an instance of `Illuminate\Testing\Fluent\AssertableJson` which can be used to make assertions against the JSON that was returned by your application. The `where` method may be used to make assertions against a particular attribute of the JSON, while the `missing` method may be used to assert that a particular attribute is missing from the JSON: -->
Laravel은 애플리케이션의 JSON 응답을 유창하게 테스트할 수 있는 기능도 제공합니다. 먼저, `assertJson` 메서드에 클로저를 전달합니다. 이 클로저는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스를 받아, 반환된 JSON에 대해 assertion을 할 수 있습니다. `where` 메서드는 JSON의 특정 속성에 대한 assertion을, `missing` 메서드는 특정 속성이 JSON에서 누락되었는지 확인합니다.

```
use Illuminate\Testing\Fluent\AssertableJson;

/**
 * A basic functional test example.
 *
 * @return void
 */
public function test_fluent_json()
{
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                 ->where('name', 'Victoria Faith')
                 ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                 ->whereNot('status', 'pending')
                 ->missing('password')
                 ->etc()
        );
}
```

<!-- #### Understanding The `etc` Method -->
#### Understanding The `etc` Method

<!-- In the example above, you may have noticed we invoked the `etc` method at the end of our assertion chain. This method informs Laravel that there may be other attributes present on the JSON object. If the `etc` method is not used, the test will fail if other attributes that you did not make assertions against exist on the JSON object. -->
위 예제에서 assertion 메서드 체인의 마지막에 `etc` 메서드를 사용한 것을 볼 수 있습니다. 이 메서드는 해당 JSON 객체에 다른 속성이 추가적으로 존재할 수 있음을 Laravel에 알리는 역할을 합니다. 만약 `etc` 메서드를 사용하지 않으면, assertion을 하지 않은 속성이 JSON 객체에 존재하면 테스트가 실패하게 됩니다.

<!-- The intention behind this behavior is to protect you from unintentionally exposing sensitive information in your JSON responses by forcing you to either explicitly make an assertion against the attribute or explicitly allow additional attributes via the `etc` method. -->
이러한 동작의 의도는, JSON 응답에 민감한 정보가 실수로 노출되는 것을 막기 위해, 해당 속성에 대해 명시적으로 assertion을 하거나 `etc`를 통해 추가 속성을 허용하도록 강제하기 위함입니다.

<!-- However, you should be aware that not including the `etc` method in your assertion chain does not ensure that additional attributes are not being added to arrays that are nested within your JSON object. The `etc` method only ensures that no additional attributes exist at the nesting level in which the `etc` method is invoked. -->
단, assertion 체인에 `etc` 메서드를 포함하지 않는다고 해서, JSON 객체 내부에 중첩된 배열에 추가 속성이 추가되지 않았다는 의미는 아닙니다. `etc` 메서드는 `etc` 메서드가 호출된 nesting 레벨에만 추가 속성이 존재하지 않음을 보장합니다.

<a name="asserting-json-attribute-presence-and-absence"></a>
<!-- #### Asserting Attribute Presence / Absence -->
#### Asserting Attribute Presence / Absence

<!-- To assert that an attribute is present or absent, you may use the `has` and `missing` methods: -->
속성이 존재하는지/존재하지 않는지 검증하려면, `has`와 `missing` 메서드를 사용할 수 있습니다.

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
         ->missing('message')
);
```

<!-- In addition, the `hasAll` and `missingAll` methods allow asserting the presence or absence of multiple attributes simultaneously: -->
또한, `hasAll`과 `missingAll` 메서드를 통해 여러 속성의 존재 유무를 한 번에 검증할 수 있습니다.

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
         ->missingAll(['message', 'code'])
);
```

<!-- You may use the `hasAny` method to determine if at least one of a given list of attributes is present: -->
`hasAny` 메서드를 이용하면, 지정한 속성 목록 중 하나라도 존재하는지 확인할 수 있습니다.

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
         ->hasAny('data', 'message', 'code')
);
```

<a name="asserting-against-json-collections"></a>
<!-- #### Asserting Against JSON Collections -->
#### Asserting Against JSON Collections

<!-- Often, your route will return a JSON response that contains multiple items, such as multiple users: -->
종종, 라우트가 여러 항목이 포함된 JSON 응답(예: 여러 사용자)을 반환할 수 있습니다.

```
Route::get('/users', function () {
    return User::all();
});
```

<!-- In these situations, we may use the fluent JSON object's `has` method to make assertions against the users included in the response. For example, let's assert that the JSON response contains three users. Next, we'll make some assertions about the first user in the collection using the `first` method. The `first` method accepts a closure which receives another assertable JSON string that we can use to make assertions about the first object in the JSON collection: -->
이 경우, 유창한 JSON 객체의 `has` 메서드를 사용해 응답에 포함된 사용자 수를 assertion 할 수 있습니다. 예를 들어, JSON 응답에 3명의 사용자가 포함되었는지 assertion 하고, 이어 `first` 메서드를 사용해 컬렉션의 첫 번째 사용자에 대해 추가 검증을 할 수 있습니다. `first` 메서드는 클로저를 받아, 해당 JSON 컬렉션의 첫 번째 객체에 대한 assertion을 할 수 있습니다.

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has(3)
             ->first(fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="scoping-json-collection-assertions"></a>
<!-- #### Scoping JSON Collection Assertions -->
#### Scoping JSON Collection Assertions

<!-- Sometimes, your application's routes will return JSON collections that are assigned named keys: -->
때때로, 여러분의 애플리케이션 라우트는 키가 지정된(named) JSON 컬렉션을 반환할 수 있습니다.

```
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

<!-- When testing these routes, you may use the `has` method to assert against the number of items in the collection. In addition, you may use the `has` method to scope a chain of assertions: -->
이러한 라우트를 테스트할 때에는, `has` 메서드로 컬렉션의 항목 개수를 assertion 할 수 있습니다. 또한, `has` 메서드를 통해 assertion의 범위를 지정해서 체이닝할 수 있습니다.

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3)
             ->has('users.0', fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<!-- However, instead of making two separate calls to the `has` method to assert against the `users` collection, you may make a single call which provides a closure as its third parameter. When doing so, the closure will automatically be invoked and scoped to the first item in the collection: -->
하지만, `users` 컬렉션에 대한 assertion을 위해 `has` 메서드를 두 번 호출하는 대신, 세 번째 인수에 클로저를 전달하여 한 번에 처리할 수 있습니다. 이 경우, 클로저는 컬렉션의 첫 번째 항목에 자동으로 적용됩니다.

```
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
             ->has('users', 3, fn ($json) =>
                $json->where('id', 1)
                     ->where('name', 'Victoria Faith')
                     ->where('email', fn ($email) => str($email)->is('victoria@gmail.com'))
                     ->missing('password')
                     ->etc()
             )
    );
```

<a name="asserting-json-types"></a>
<!-- #### Asserting JSON Types -->
#### Asserting JSON Types

<!-- You may only want to assert that the properties in the JSON response are of a certain type. The `Illuminate\Testing\Fluent\AssertableJson` class provides the `whereType` and `whereAllType` methods for doing just that: -->
JSON 응답의 속성이 특정 타입인지 assertion 하고 싶을 때가 있습니다. `Illuminate\Testing\Fluent\AssertableJson` 클래스는 이를 위해 `whereType`, `whereAllType` 메서드를 제공합니다.

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
         ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```

<!-- You may specify multiple types using the `|` character, or passing an array of types as the second parameter to the `whereType` method. The assertion will be successful if the response value is any of the listed types: -->
`|` 문자를 사용하거나, `whereType` 메서드의 두 번째 인수로 타입 배열을 전달하여 여러 타입을 지정할 수도 있습니다. 응답 값이 지정한 타입 중 하나라도 일치하면 assertion은 통과합니다.

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
         ->whereType('id', ['string', 'integer'])
);
```

<!-- The `whereType` and `whereAllType` methods recognize the following types: `string`, `integer`, `double`, `boolean`, `array`, and `null`. -->
`whereType` 및 `whereAllType` 메서드는 다음 타입을 인식합니다: `string`, `integer`, `double`, `boolean`, `array`, `null`.

<a name="testing-file-uploads"></a>
<!-- ## Testing File Uploads -->
## Testing File Uploads

<!-- The `Illuminate\Http\UploadedFile` class provides a `fake` method which may be used to generate dummy files or images for testing. This, combined with the `Storage` facade's `fake` method, greatly simplifies the testing of file uploads. For example, you may combine these two features to easily test an avatar upload form: -->
`Illuminate\Http\UploadedFile` 클래스의 `fake` 메서드를 사용하면 테스트용 더미 파일이나 이미지를 쉽게 만들 수 있습니다. 이를 `Storage` 파사드의 `fake` 메서드와 함께 사용하면 파일 업로드 테스트가 매우 간단해집니다. 예를 들어, 이 두 기능을 조합하여 아바타 업로드 폼에 대한 테스트를 쉽게 작성할 수 있습니다.

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_avatars_can_be_uploaded()
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
특정 파일이 존재하지 않는지 assertion 하고 싶을 때는 `Storage` 파사드가 제공하는 `assertMissing` 메서드를 사용할 수 있습니다.

```
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>

<!-- #### Fake File Customization -->
#### Fake File Customization

<!-- When creating files using the `fake` method provided by the `UploadedFile` class, you may specify the width, height, and size of the image (in kilobytes) in order to better test your application's validation rules: -->
`UploadedFile` 클래스에서 제공하는 `fake` 메서드를 사용하여 파일을 생성할 때, 이미지의 너비, 높이, 그리고 용량(킬로바이트 단위)을 지정하여 애플리케이션의 유효성 검증 규칙을 더 효과적으로 테스트할 수 있습니다.

```
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

<!-- In addition to creating images, you may create files of any other type using the `create` method: -->
이미지 생성뿐 아니라, `create` 메서드를 사용하면 다른 모든 종류의 파일도 생성할 수 있습니다.

```
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

<!-- If needed, you may pass a `$mimeType` argument to the method to explicitly define the MIME type that should be returned by the file: -->
필요하다면, 메서드에 `$mimeType` 인수를 추가로 전달해 파일의 MIME 타입을 명시적으로 지정할 수 있습니다.

```
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
<!-- ## Testing Views -->
## Testing Views

<!-- Laravel also allows you to render a view without making a simulated HTTP request to the application. To accomplish this, you may call the `view` method within your test. The `view` method accepts the view name and an optional array of data. The method returns an instance of `Illuminate\Testing\TestView`, which offers several methods to conveniently make assertions about the view's contents: -->
Laravel에서는 애플리케이션에 대한 실제 HTTP 요청을 시뮬레이션하지 않고도 뷰를 렌더링할 수 있습니다. 이를 위해 테스트 내에서 `view` 메서드를 호출하면 됩니다. `view` 메서드는 뷰의 이름과 선택적으로 데이터를 담은 배열을 받습니다. 이 메서드는 `Illuminate\Testing\TestView` 인스턴스를 반환하는데, 이 인스턴스는 뷰 내용에 대해 편리하게 assertion(확인)을 할 수 있는 여러 메서드를 제공합니다.

```
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_a_welcome_view_can_be_rendered()
    {
        $view = $this->view('welcome', ['name' => 'Taylor']);

        $view->assertSee('Taylor');
    }
}
```

<!-- The `TestView` class provides the following assertion methods: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, and `assertDontSeeText`. -->
`TestView` 클래스는 다음과 같은 assertion 메서드들을 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, `assertDontSeeText`.

<!-- If needed, you may get the raw, rendered view contents by casting the `TestView` instance to a string: -->
필요하다면, `TestView` 인스턴스를 문자열로 casting하여 실제 렌더링된 뷰의 원본 내용을 가져올 수 있습니다.

```
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
<!-- #### Sharing Errors -->
#### Sharing Errors

<!-- Some views may depend on errors shared in the [global error bag provided by Laravel](/docs/9.x/validation#quick-displaying-the-validation-errors). To hydrate the error bag with error messages, you may use the `withViewErrors` method: -->
일부 뷰는 [global error bag provided by Laravel](/docs/9.x/validation#quick-displaying-the-validation-errors)에 공유된 오류에 의존할 수 있습니다. 에러 메시지로 에러 백을 채우려면 `withViewErrors` 메서드를 사용할 수 있습니다.

```
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```

<a name="rendering-blade-and-components"></a>
<!-- ### Rendering Blade & Components -->
### Rendering Blade & Components

<!-- If necessary, you may use the `blade` method to evaluate and render a raw [Blade](/docs/9.x/blade) string. Like the `view` method, the `blade` method returns an instance of `Illuminate\Testing\TestView`: -->
필요하다면, `blade` 메서드를 사용해 [Blade](/docs/9.x/blade) 원본 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로, `blade` 메서드는 `Illuminate\Testing\TestView` 인스턴스를 반환합니다.

```
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

<!-- You may use the `component` method to evaluate and render a [Blade component](/docs/9.x/blade#components). The `component` method returns an instance of `Illuminate\Testing\TestComponent`: -->
[Blade component](/docs/9.x/blade#components)를 평가해 렌더링하려면 `component` 메서드를 사용할 수 있습니다. `component` 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다.

```
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```

<a name="available-assertions"></a>
<!-- ## Available Assertions -->
## Available Assertions

<a name="response-assertions"></a>
<!-- ### Response Assertions -->
### Response Assertions

<!-- Laravel's `Illuminate\Testing\TestResponse` class provides a variety of custom assertion methods that you may utilize when testing your application. These assertions may be accessed on the response that is returned by the `json`, `get`, `post`, `put`, and `delete` test methods: -->
Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션을 테스트할 때 활용할 수 있는 다양한 커스텀 assertion(검증) 메서드를 제공합니다. 이 assertion들은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드로 반환된 응답에서 사용할 수 있습니다.



<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[assertCookie](#assert-cookie)
[assertCookieExpired](#assert-cookie-expired)
[assertCookieNotExpired](#assert-cookie-not-expired)
[assertCookieMissing](#assert-cookie-missing)
[assertCreated](#assert-created)
[assertDontSee](#assert-dont-see)
[assertDontSeeText](#assert-dont-see-text)
[assertDownload](#assert-download)
[assertExactJson](#assert-exact-json)
[assertForbidden](#assert-forbidden)
[assertHeader](#assert-header)
[assertHeaderMissing](#assert-header-missing)
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
[assertContent](#assert-content)
[assertNoContent](#assert-no-content)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
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
[assertUnauthorized](#assert-unauthorized)
[assertUnprocessable](#assert-unprocessable)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)
-->
[assertCookie](#assert-cookie)
[assertCookieExpired](#assert-cookie-expired)
[assertCookieNotExpired](#assert-cookie-not-expired)
[assertCookieMissing](#assert-cookie-missing)
[assertCreated](#assert-created)
[assertDontSee](#assert-dont-see)
[assertDontSeeText](#assert-dont-see-text)
[assertDownload](#assert-download)
[assertExactJson](#assert-exact-json)
[assertForbidden](#assert-forbidden)
[assertHeader](#assert-header)
[assertHeaderMissing](#assert-header-missing)
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
[assertContent](#assert-content)
[assertNoContent](#assert-no-content)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
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
[assertUnauthorized](#assert-unauthorized)
[assertUnprocessable](#assert-unprocessable)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)

<!-- </div> -->
</div>

<a name="assert-cookie"></a>
<!-- #### assertCookie -->
#### assertCookie

<!-- Assert that the response contains the given cookie: -->
응답에 지정한 쿠키가 포함되어 있는지 확인합니다.

```
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
<!-- #### assertCookieExpired -->
#### assertCookieExpired

<!-- Assert that the response contains the given cookie and it is expired: -->
응답에 지정한 쿠키가 포함되어 있으며, 해당 쿠키가 만료된 상태인지 확인합니다.

```
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
<!-- #### assertCookieNotExpired -->
#### assertCookieNotExpired

<!-- Assert that the response contains the given cookie and it is not expired: -->
응답에 지정한 쿠키가 포함되어 있고, 해당 쿠키가 만료되지 않은 상태인지 확인합니다.

```
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
<!-- #### assertCookieMissing -->
#### assertCookieMissing

<!-- Assert that the response does not contain the given cookie: -->
응답에 지정한 쿠키가 포함되어 있지 않은지 확인합니다.

```
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
<!-- #### assertCreated -->
#### assertCreated

<!-- Assert that the response has a 201 HTTP status code: -->
응답이 201 HTTP 상태 코드를 가지는지 확인합니다.

```
$response->assertCreated();
```

<a name="assert-dont-see"></a>
<!-- #### assertDontSee -->
#### assertDontSee

<!-- Assert that the given string is not contained within the response returned by the application. This assertion will automatically escape the given string unless you pass a second argument of `false`: -->
애플리케이션이 반환한 응답 내용에 지정한 문자열이 포함되어 있지 않은지 확인합니다. 두 번째 인자에 `false`를 전달하지 않는 한, 기본적으로 지정한 문자열이 자동으로 이스케이프 처리됩니다.

```
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
<!-- #### assertDontSeeText -->
#### assertDontSeeText

<!-- Assert that the given string is not contained within the response text. This assertion will automatically escape the given string unless you pass a second argument of `false`. This method will pass the response content to the `strip_tags` PHP function before making the assertion: -->
응답 텍스트에 지정한 문자열이 포함되어 있지 않은지 확인합니다. 두 번째 인자에 `false`를 전달하지 않는 한, 기본적으로 지정한 문자열이 자동으로 이스케이프 처리됩니다. 이 메서드는 assert 시 PHP의 `strip_tags` 함수로 응답 내용을 처리한 후 비교를 수행합니다.

```
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
<!-- #### assertDownload -->
#### assertDownload

<!-- Assert that the response is a "download". Typically, this means the invoked route that returned the response returned a `Response::download` response, `BinaryFileResponse`, or `Storage::download` response: -->
응답이 "다운로드" 타입인지를 확인합니다. 일반적으로 라우트가 반환한 응답이 `Response::download`, `BinaryFileResponse`, 혹은 `Storage::download` 형태인 경우입니다.

```
$response->assertDownload();
```

<!-- If you wish, you may assert that the downloadable file was assigned a given file name: -->
원한다면, 다운로드 파일에 지정한 파일명이 할당되었는지도 함께 확인할 수 있습니다.

```
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
<!-- #### assertExactJson -->
#### assertExactJson

<!-- Assert that the response contains an exact match of the given JSON data: -->
응답이 지정한 JSON 데이터와 정확히 일치하는지 확인합니다.

```
$response->assertExactJson(array $data);
```

<a name="assert-forbidden"></a>
<!-- #### assertForbidden -->
#### assertForbidden

<!-- Assert that the response has a forbidden (403) HTTP status code: -->
응답이 금지(403) HTTP 상태 코드를 가지는지 확인합니다.

```
$response->assertForbidden();
```

<a name="assert-header"></a>
<!-- #### assertHeader -->
#### assertHeader

<!-- Assert that the given header and value is present on the response: -->
응답에 지정한 헤더와 값이 포함되어 있는지 확인합니다.

```
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
<!-- #### assertHeaderMissing -->
#### assertHeaderMissing

<!-- Assert that the given header is not present on the response: -->
응답에 지정한 헤더가 포함되어 있지 않은지 확인합니다.

```
$response->assertHeaderMissing($headerName);
```

<a name="assert-json"></a>
<!-- #### assertJson -->
#### assertJson

<!-- Assert that the response contains the given JSON data: -->
응답에 지정한 JSON 데이터가 포함되어 있는지 확인합니다.

```
$response->assertJson(array $data, $strict = false);
```

<!-- The `assertJson` method converts the response to an array and utilizes `PHPUnit::assertArraySubset` to verify that the given array exists within the JSON response returned by the application. So, if there are other properties in the JSON response, this test will still pass as long as the given fragment is present. -->
`assertJson` 메서드는 응답을 배열로 변환한 뒤, `PHPUnit::assertArraySubset`을 활용해 지정한 배열이 응답 JSON 내에 존재하는지 검증합니다. 즉, JSON 응답에 다른 속성이 있더라도, 지정한 데이터 일부만 존재한다면 이 테스트는 통과합니다.

<a name="assert-json-count"></a>
<!-- #### assertJsonCount -->
#### assertJsonCount

<!-- Assert that the response JSON has an array with the expected number of items at the given key: -->
지정한 key에 해당하는 응답 JSON 배열의 요소 개수가 기대한 값과 일치하는지 확인합니다.

```
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
<!-- #### assertJsonFragment -->
#### assertJsonFragment

<!-- Assert that the response contains the given JSON data anywhere in the response: -->
응답 전체에서 지정한 JSON 데이터가 어느 곳에든 포함되어 있는지 확인합니다.

```
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
응답의 JSON이 배열인지 확인합니다.

```
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
<!-- #### assertJsonIsObject -->
#### assertJsonIsObject

<!-- Assert that the response JSON is an object: -->
응답의 JSON이 객체인지 확인합니다.

```
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
<!-- #### assertJsonMissing -->
#### assertJsonMissing

<!-- Assert that the response does not contain the given JSON data: -->
응답에 지정한 JSON 데이터가 포함되어 있지 않은지 확인합니다.

```
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
<!-- #### assertJsonMissingExact -->
#### assertJsonMissingExact

<!-- Assert that the response does not contain the exact JSON data: -->
응답에 지정한 JSON 데이터가 정확하게 일치하여 포함되어 있지 않은지 확인합니다.

```
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
<!-- #### assertJsonMissingValidationErrors -->
#### assertJsonMissingValidationErrors

<!-- Assert that the response has no JSON validation errors for the given keys: -->
응답에서 지정한 key들에 대한 JSON 유효성 검증 오류가 없는지 확인합니다.

```
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드를 사용하면, 응답에 JSON 형태로 반환된 검증 오류가 없고 **세션 저장소에도 오류가 플래시되지 않았는지** 함께 확인할 수 있습니다.

<a name="assert-json-path"></a>
<!-- #### assertJsonPath -->
#### assertJsonPath

<!-- Assert that the response contains the given data at the specified path: -->
지정한 경로(path)에 해당하는 응답 데이터가 기대한 값과 일치하는지 확인합니다.

```
$response->assertJsonPath($path, $expectedValue);
```

<!-- For example, if the following JSON response is returned by your application: -->
예를 들어, 애플리케이션에서 다음과 같은 JSON 응답이 반환된다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that the `name` property of the `user` object matches a given value like so: -->
`user` 객체의 `name` 속성이 특정 값과 일치하는지 다음과 같이 검증할 수 있습니다.

```
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
<!-- #### assertJsonMissingPath -->
#### assertJsonMissingPath

<!-- Assert that the response does not contain the given path: -->
응답에 지정한 경로(path)가 존재하지 않는지 확인합니다.

```
$response->assertJsonMissingPath($path);
```

<!-- For example, if the following JSON response is returned by your application: -->
예를 들어, 애플리케이션에서 다음과 같은 JSON 응답이 반환된다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that it does not contain the `email` property of the `user` object: -->
`user` 객체의 `email` 속성이 없는지 다음과 같이 확인할 수 있습니다.

```
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
<!-- #### assertJsonStructure -->
#### assertJsonStructure

<!-- Assert that the response has a given JSON structure: -->
응답이 기대하는 구조의 JSON을 가지고 있는지 확인합니다.

```
$response->assertJsonStructure(array $structure);
```

<!-- For example, if the JSON response returned by your application contains the following data: -->
예를 들어, 애플리케이션이 반환하는 JSON 응답이 다음 데이터를 담고 있다면:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that the JSON structure matches your expectations like so: -->
아래와 같이 JSON 구조가 기대에 부합하는지 검증할 수 있습니다.

```
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

<!-- Sometimes, JSON responses returned by your application may contain arrays of objects: -->
때로는 애플리케이션에서 반환되는 JSON 응답에 여러 객체로 이루어진 배열이 포함될 수 있습니다.

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
이런 경우에는 `*` 문자를 사용해 배열 내 모든 객체의 구조를 검증할 수 있습니다.

```
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
응답에서 지정한 key들에 대해 JSON 기반의 유효성 검증 오류가 존재하는지 확인합니다. 이 메서드는 유효성 검증 오류가 세션에 플래시되는 대신 JSON 구조로 반환되는 응답을 대상으로 합니다.

```
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는, 오류가 JSON으로 반환되든 세션 저장소로 플래시되든 검증 오류가 존재하는지를 확인할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
<!-- #### assertJsonValidationErrorFor -->
#### assertJsonValidationErrorFor

<!-- Assert the response has any JSON validation errors for the given key: -->
응답에서 지정한 key에 대해 어떠한 JSON 검증 오류가 존재하는지 확인합니다.

```
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-location"></a>
<!-- #### assertLocation -->
#### assertLocation

<!-- Assert that the response has the given URI value in the `Location` header: -->
응답의 `Location` 헤더에 기대하는 URI 값이 있는지 확인합니다.

```
$response->assertLocation($uri);
```
<a name="assert-content"></a>
<!-- #### assertContent -->
#### assertContent

<!-- Assert that the given string matches the response content: -->
응답 내용이 지정한 문자열과 정확히 일치하는지 확인합니다.

```
$response->assertContent($value);
```

<a name="assert-no-content"></a>
<!-- #### assertNoContent -->
#### assertNoContent

<!-- Assert that the response has the given HTTP status code and no content: -->
응답이 지정한 HTTP 상태 코드와 함께 콘텐츠가 없는지 확인합니다.

```
$response->assertNoContent($status = 204);
```

<a name="assert-streamed-content"></a>
<!-- #### assertStreamedContent -->
#### assertStreamedContent

<!-- Assert that the given string matches the streamed response content: -->
스트림 형식의 응답 내용이 지정한 문자열과 일치하는지 확인합니다.

```
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
<!-- #### assertNotFound -->
#### assertNotFound

<!-- Assert that the response has a not found (404) HTTP status code: -->
응답이 찾을 수 없음(404) HTTP 상태 코드를 가지는지 확인합니다.

```
$response->assertNotFound();
```

<a name="assert-ok"></a>
<!-- #### assertOk -->
#### assertOk

<!-- Assert that the response has a 200 HTTP status code: -->
응답이 200 HTTP 상태 코드를 가지는지 확인합니다.

```
$response->assertOk();
```

<a name="assert-plain-cookie"></a>
<!-- #### assertPlainCookie -->
#### assertPlainCookie

<!-- Assert that the response contains the given unencrypted cookie: -->
응답에 지정한 암호화되지 않은 쿠키가 포함되어 있는지 확인합니다.

```
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
<!-- #### assertRedirect -->
#### assertRedirect

<!-- Assert that the response is a redirect to the given URI: -->
응답이 지정한 URI로 리다이렉트되는지 확인합니다.

```
$response->assertRedirect($uri);
```

<a name="assert-redirect-contains"></a>

<!-- #### assertRedirectContains -->
#### assertRedirectContains

<!-- Assert whether the response is redirecting to a URI that contains the given string: -->
응답이 지정한 문자열을 포함하는 URI로 리디렉션되는지 확인합니다.

```
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
<!-- #### assertRedirectToRoute -->
#### assertRedirectToRoute

<!-- Assert that the response is a redirect to the given [named route](/docs/9.x/routing#named-routes): -->
응답이 [named route](/docs/9.x/routing#named-routes)로 리디렉션되는지 확인합니다.

```
$response->assertRedirectToRoute($name = null, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
<!-- #### assertRedirectToSignedRoute -->
#### assertRedirectToSignedRoute

<!-- Assert that the response is a redirect to the given [signed route](/docs/9.x/urls#signed-urls): -->
응답이 [signed route](/docs/9.x/urls#signed-urls)로 리디렉션되는지 확인합니다.

```
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-see"></a>
<!-- #### assertSee -->
#### assertSee

<!-- Assert that the given string is contained within the response. This assertion will automatically escape the given string unless you pass a second argument of `false`: -->
응답에 지정한 문자열이 포함되어 있는지 확인합니다. 이 assert는 두 번째 인자로 `false`를 전달하지 않는 한, 지정한 문자열을 자동으로 이스케이프합니다.

```
$response->assertSee($value, $escaped = true);
```

<a name="assert-see-in-order"></a>
<!-- #### assertSeeInOrder -->
#### assertSeeInOrder

<!-- Assert that the given strings are contained in order within the response. This assertion will automatically escape the given strings unless you pass a second argument of `false`: -->
응답에 여러 문자열이 순서대로 포함되어 있는지 확인합니다. 이 assert는 두 번째 인자로 `false`를 전달하지 않는 한, 지정한 문자열을 자동으로 이스케이프합니다.

```
$response->assertSeeInOrder(array $values, $escaped = true);
```

<a name="assert-see-text"></a>
<!-- #### assertSeeText -->
#### assertSeeText

<!-- Assert that the given string is contained within the response text. This assertion will automatically escape the given string unless you pass a second argument of `false`. The response content will be passed to the `strip_tags` PHP function before the assertion is made: -->
응답 텍스트에 지정한 문자열이 포함되어 있는지 확인합니다. 이 assert는 두 번째 인자로 `false`를 전달하지 않는 한, 지정한 문자열을 자동으로 이스케이프합니다. assert를 수행하기 전, 응답 본문은 `strip_tags` PHP 함수로 HTML 태그가 제거됩니다.

```
$response->assertSeeText($value, $escaped = true);
```

<a name="assert-see-text-in-order"></a>
<!-- #### assertSeeTextInOrder -->
#### assertSeeTextInOrder

<!-- Assert that the given strings are contained in order within the response text. This assertion will automatically escape the given strings unless you pass a second argument of `false`. The response content will be passed to the `strip_tags` PHP function before the assertion is made: -->
응답 텍스트에 여러 문자열이 순서대로 포함되어 있는지 확인합니다. 이 assert는 두 번째 인자로 `false`를 전달하지 않는 한, 지정한 문자열을 자동으로 이스케이프합니다. 응답 본문은 assert 전에 `strip_tags` PHP 함수로 HTML 태그가 제거됩니다.

```
$response->assertSeeTextInOrder(array $values, $escaped = true);
```

<a name="assert-session-has"></a>
<!-- #### assertSessionHas -->
#### assertSessionHas

<!-- Assert that the session contains the given piece of data: -->
세션에 지정한 데이터를 가지고 있는지 확인합니다.

```
$response->assertSessionHas($key, $value = null);
```

<!-- If needed, a closure can be provided as the second argument to the `assertSessionHas` method. The assertion will pass if the closure returns `true`: -->
필요하다면, `assertSessionHas` 메서드의 두 번째 인자로 클로저를 전달할 수도 있습니다. 클로저가 `true`를 반환하면 assertion이 통과합니다.

```
$response->assertSessionHas($key, function ($value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
<!-- #### assertSessionHasInput -->
#### assertSessionHasInput

<!-- Assert that the session has a given value in the [flashed input array](/docs/9.x/responses#redirecting-with-flashed-session-data): -->
세션의 [flashed input array](/docs/9.x/responses#redirecting-with-flashed-session-data)에 특정 값이 포함되어 있는지 확인합니다.

```
$response->assertSessionHasInput($key, $value = null);
```

<!-- If needed, a closure can be provided as the second argument to the `assertSessionHasInput` method. The assertion will pass if the closure returns `true`: -->
필요하다면, `assertSessionHasInput` 메서드의 두 번째 인자로 클로저를 전달할 수 있습니다. 클로저가 `true`를 반환하면 assertion이 통과합니다.

```
$response->assertSessionHasInput($key, function ($value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
<!-- #### assertSessionHasAll -->
#### assertSessionHasAll

<!-- Assert that the session contains a given array of key / value pairs: -->
세션에 지정한 키/값 쌍 배열을 모두 가지고 있는지 확인합니다.

```
$response->assertSessionHasAll(array $data);
```

<!-- For example, if your application's session contains `name` and `status` keys, you may assert that both exist and have the specified values like so: -->
예를 들어, 애플리케이션의 세션에 `name`과 `status` 키가 들어 있다면, 아래와 같이 두 값이 모두 존재하고 각각의 값을 가지고 있는지 assert할 수 있습니다.

```
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```

<a name="assert-session-has-errors"></a>
<!-- #### assertSessionHasErrors -->
#### assertSessionHasErrors

<!-- Assert that the session contains an error for the given `$keys`. If `$keys` is an associative array, assert that the session contains a specific error message (value) for each field (key). This method should be used when testing routes that flash validation errors to the session instead of returning them as a JSON structure: -->
세션에 지정한 `$keys`에 대한 에러가 있는지 확인합니다. `$keys`가 연관 배열(associative array)이면, 각 필드(키)에 대해 각각의 에러 메시지(값)가 포함되어 있는지 확인합니다. 이 메서드는 유효성 검증 오류가 JSON이 아닌, 세션에 플래시 데이터로 저장되는 라우트를 테스트할 때 사용하면 좋습니다.

```
$response->assertSessionHasErrors(
    array $keys, $format = null, $errorBag = 'default'
);
```

<!-- For example, to assert that the `name` and `email` fields have validation error messages that were flashed to the session, you may invoke the `assertSessionHasErrors` method like so: -->
예를 들어, `name`과 `email` 필드에 세션에 플래시된 유효성 검사 오류 메시지가 있는지 확인하려면 다음과 같이 `assertSessionHasErrors` 메서드를 호출할 수 있습니다.

```
$response->assertSessionHasErrors(['name', 'email']);
```

<!-- Or, you may assert that a given field has a particular validation error message: -->
또는, 특정 필드에 특정 에러 메시지가 포함되어 있는지 검증할 수도 있습니다.

```
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> 더 범용적으로 사용할 수 있는 [assertInvalid](#assert-invalid) 메서드는 유효성 검증 오류가 JSON 형태로 반환되거나 세션에 플래시된 경우 모두를 검증할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
<!-- #### assertSessionHasErrorsIn -->
#### assertSessionHasErrorsIn

<!-- Assert that the session contains an error for the given `$keys` within a specific [error bag](/docs/9.x/validation#named-error-bags). If `$keys` is an associative array, assert that the session contains a specific error message (value) for each field (key), within the error bag: -->
지정한 [error bag](/docs/9.x/validation#named-error-bags) 내부에 `$keys`에 대한 에러가 있는지 확인합니다. `$keys`가 연관 배열일 경우, 각 필드(키)에 대해 해당 에러 메시지(값)가 에러 백에 포함되어 있는지 검증합니다.

```
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
<!-- #### assertSessionHasNoErrors -->
#### assertSessionHasNoErrors

<!-- Assert that the session has no validation errors: -->
세션에 유효성 검사 오류가 전혀 없는지 확인합니다.

```
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
<!-- #### assertSessionDoesntHaveErrors -->
#### assertSessionDoesntHaveErrors

<!-- Assert that the session has no validation errors for the given keys: -->
세션에 지정한 키들에 대한 유효성 검증 오류가 없는지 확인합니다.

```
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> 더 범용적으로 사용할 수 있는 [assertValid](#assert-valid) 메서드는 유효성 검사 오류가 JSON 형태로 반환되거나, 세션에 플래시된 경우 모두 해당 키에 대한 에러가 없는지 검증할 수 있습니다.

<a name="assert-session-missing"></a>
<!-- #### assertSessionMissing -->
#### assertSessionMissing

<!-- Assert that the session does not contain the given key: -->
세션에 지정한 키가 없는지 확인합니다.

```
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
<!-- #### assertStatus -->
#### assertStatus

<!-- Assert that the response has a given HTTP status code: -->
응답의 HTTP 상태 코드가 지정한 값과 일치하는지 확인합니다.

```
$response->assertStatus($code);
```

<a name="assert-successful"></a>
<!-- #### assertSuccessful -->
#### assertSuccessful

<!-- Assert that the response has a successful (>= 200 and < 300) HTTP status code: -->
응답이 성공 상태(HTTP 코드 200 이상, 300 미만)인지 확인합니다.

```
$response->assertSuccessful();
```

<a name="assert-unauthorized"></a>
<!-- #### assertUnauthorized -->
#### assertUnauthorized

<!-- Assert that the response has an unauthorized (401) HTTP status code: -->
응답의 HTTP 상태 코드가 인증되지 않음(401) 코드인지 확인합니다.

```
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
<!-- #### assertUnprocessable -->
#### assertUnprocessable

<!-- Assert that the response has an unprocessable entity (422) HTTP status code: -->
응답의 HTTP 상태 코드가 처리할 수 없음(422) 코드인지 확인합니다.

```
$response->assertUnprocessable();
```

<a name="assert-valid"></a>
<!-- #### assertValid -->
#### assertValid

<!-- Assert that the response has no validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
응답에서 지정한 키에 대해 유효성 검사 오류가 전혀 없는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되었거나 세션에 플래시된 경우 모두에 사용할 수 있습니다.

```
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```

<a name="assert-invalid"></a>
<!-- #### assertInvalid -->
#### assertInvalid

<!-- Assert that the response has validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
응답에서 지정한 키에 대해 유효성 검사 오류가 있는지 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되었거나 세션에 플래시된 경우 모두에 사용할 수 있습니다.

```
$response->assertInvalid(['name', 'email']);
```

<!-- You may also assert that a given key has a particular validation error message. When doing so, you may provide the entire message or only a small portion of the message: -->
특정 키가 특정 유효성 검사 에러 메시지를 가지고 있는지 assert할 수도 있습니다. 이때 전체 에러 메시지를 입력하거나, 메시지의 일부만 입력할 수도 있습니다.

```
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

<a name="assert-view-has"></a>
<!-- #### assertViewHas -->
#### assertViewHas

<!-- Assert that the response view contains given a piece of data: -->
응답의 뷰에 특정 데이터가 포함되어 있는지 확인합니다.

```
$response->assertViewHas($key, $value = null);
```

<!-- Passing a closure as the second argument to the `assertViewHas` method will allow you to inspect and make assertions against a particular piece of view data: -->
`assertViewHas` 메서드의 두 번째 인자로 클로저를 전달하면, 뷰 데이터의 특정 값을 확인하고 그에 대한 assertion을 수행할 수 있습니다.

```
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

<!-- In addition, view data may be accessed as array variables on the response, allowing you to conveniently inspect it: -->
또한, 응답의 뷰 데이터를 배열 변수처럼 바로 접근하여 확인할 수도 있습니다.

```
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
<!-- #### assertViewHasAll -->
#### assertViewHasAll

<!-- Assert that the response view has a given list of data: -->
응답의 뷰에 여러 데이터를 동시에 가지고 있는지 확인합니다.

```
$response->assertViewHasAll(array $data);
```

<!-- This method may be used to assert that the view simply contains data matching the given keys: -->
다음과 같이 뷰가 지정한 키들을 가지고 있는지 확인하거나,

```
$response->assertViewHasAll([
    'name',
    'email',
]);
```

<!-- Or, you may assert that the view data is present and has specific values: -->
데이터가 존재할 뿐 아니라 특정 값을 가지고 있는지도 assert할 수 있습니다.

```
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```

<a name="assert-view-is"></a>
<!-- #### assertViewIs -->
#### assertViewIs

<!-- Assert that the given view was returned by the route: -->
지정한 뷰가 해당 라우트에서 반환되었는지 확인합니다.

```
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
<!-- #### assertViewMissing -->
#### assertViewMissing

<!-- Assert that the given data key was not made available to the view returned in the application's response: -->
애플리케이션 응답의 뷰에 특정 데이터 키가 포함되지 않았는지 확인합니다.

```
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
<!-- ### Authentication Assertions -->
### Authentication Assertions

<!-- Laravel also provides a variety of authentication related assertions that you may utilize within your application's feature tests. Note that these methods are invoked on the test class itself and not the `Illuminate\Testing\TestResponse` instance returned by methods such as `get` and `post`. -->
Laravel은 애플리케이션의 기능 테스트 내에서 사용할 수 있는 다양한 인증 관련 assertion 메서드도 제공합니다. 이 메서드들은 `get`이나 `post`로 반환되는 `Illuminate\Testing\TestResponse` 인스턴스가 아니라, 테스트 클래스 자체에서 호출해야 합니다.

<a name="assert-authenticated"></a>
<!-- #### assertAuthenticated -->
#### assertAuthenticated

<!-- Assert that a user is authenticated: -->
사용자가 인증되었는지 확인합니다.

```
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
<!-- #### assertGuest -->
#### assertGuest

<!-- Assert that a user is not authenticated: -->
사용자가 인증되지 않은 상태(게스트)인지 확인합니다.

```
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
<!-- #### assertAuthenticatedAs -->
#### assertAuthenticatedAs

<!-- Assert that a specific user is authenticated: -->
특정 사용자가 인증되었는지 확인합니다.

```
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
<!-- ## Validation Assertions -->
## Validation Assertions

<!-- Laravel provides two primary validation related assertions that you may use to ensure the data provided in your request was either valid or invalid. -->
Laravel에서는 요청에 제공된 데이터가 유효 또는 무효인지 확인할 수 있는 두 가지 주요 유효성 검증 assertion을 제공합니다.

<a name="validation-assert-valid"></a>
<!-- #### assertValid -->
#### assertValid

<!-- Assert that the response has no validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
응답에서 지정한 키에 대해 유효성 검증 오류가 없는지 확인합니다. 이 메서드는 유효성 오류가 JSON 구조로 반환되었거나 세션에 플래시된 경우 모두 사용할 수 있습니다.

```
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```

<a name="validation-assert-invalid"></a>
<!-- #### assertInvalid -->
#### assertInvalid

<!-- Assert that the response has validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
응답에서 지정한 키에 대해 유효성 검사 오류가 있는지 확인합니다. 이 메서드는 유효성 오류가 JSON 구조로 반환되었거나 세션에 플래시된 경우 모두 사용할 수 있습니다.

```
$response->assertInvalid(['name', 'email']);
```

<!-- You may also assert that a given key has a particular validation error message. When doing so, you may provide the entire message or only a small portion of the message: -->
또한, 특정 키가 특정 유효성 오류 메시지를 가지고 있는지, 전체 메시지나 일부 메시지를 기준으로 검증할 수도 있습니다.

```
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
