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
Laravel は、アプリケーションに HTTP リクエストを送信し、その応答を調べるための非常に流暢な API を提供します。たとえば、以下に定義されている機能テストを見てください。

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
`get` メソッドは、アプリケーションに `GET` リクエストを送信します。一方、`assertStatus` メソッドは、返される応答には指定された HTTP ステータス コードが含まれる必要があることをアサートします。この単純なアサーションに加えて、Laravel には、応答ヘッダー、コンテンツ、JSON 構造などを検査するためのさまざまなアサーションも含まれています。

<a name="making-requests"></a>
<!-- ## Making Requests -->
## Making Requests

<!-- To make a request to your application, you may invoke the `get`, `post`, `put`, `patch`, or `delete` methods within your test. These methods do not actually issue a "real" HTTP request to your application. Instead, the entire network request is simulated internally. -->
アプリケーションにリクエストを行うには、テスト内で `get`、`post`、`put`、`patch`、または `delete` メソッドを呼び出すことができます。これらのメソッドは、実際にはアプリケーションに「実際の」HTTP リクエストを発行しません。代わりに、ネットワーク要求全体が内部的にシミュレートされます。

<!-- Instead of returning an `Illuminate\Http\Response` instance, test request methods return an instance of `Illuminate\Testing\TestResponse`, which provides a [variety of helpful assertions](#available-assertions) that allow you to inspect your application's responses: -->
テスト リクエスト メソッドは、`Illuminate\Http\Response` インスタンスを返す代わりに、`Illuminate\Testing\TestResponse` のインスタンスを返します。これにより、アプリケーションの応答を検査できる [variety of helpful assertions](#available-assertions) が提供されます。

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
一般に、各テストはアプリケーションに対して 1 つのリクエストのみを行う必要があります。単一のテスト メソッド内で複数のリクエストが実行されると、予期しない動作が発生する可能性があります。

> [!NOTE]
> 便宜上、CSRF ミドルウェアはテストの実行時に自動的に無効になります。

<a name="customizing-request-headers"></a>
<!-- ### Customizing Request Headers -->
### Customizing Request Headers

<!-- You may use the `withHeaders` method to customize the request's headers before it is sent to the application. This method allows you to add any custom headers you would like to the request: -->
`withHeaders` メソッドを使用して、アプリケーションに送信される前にリクエストのヘッダーをカスタマイズできます。このメソッドを使用すると、リクエストに必要なカスタム ヘッダーを追加できます。

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
リクエストを行う前に、`withCookie` メソッドまたは `withCookies` メソッドを使用して Cookie 値を設定できます。 `withCookie` メソッドは 2 つの引数として Cookie 名と値を受け入れますが、`withCookies` メソッドは名前と値のペアの配列を受け入れます。

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
Laravel は、HTTP テスト中にセッションと対話するためのいくつかのヘルパを提供します。まず、`withSession` メソッドを使用して、セッション データを特定の配列に設定します。これは、アプリケーションにリクエストを発行する前にセッションにデータをロードする場合に便利です。

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
Laravel のセッションは通常、現在認証されているユーザーの状態を維持するために使用されます。したがって、`actingAs` ヘルパ メソッドは、特定のユーザーを現在のユーザーとして認証する簡単な方法を提供します。たとえば、[model factory](/docs/9.x/eloquent-factories) を使用してユーザーを生成および認証できます。

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
`actingAs` メソッドの 2 番目の引数としてガード名を渡すことで、特定のユーザーの認証にどのガードを使用するかを指定することもできます。 `actingAs` メソッドに提供されるガードも、テスト中のデフォルトのガードになります。

```
$this->actingAs($user, 'web')
```

<a name="debugging-responses"></a>
<!-- ### Debugging Responses -->
### Debugging Responses

<!-- After making a test request to your application, the `dump`, `dumpHeaders`, and `dumpSession` methods may be used to examine and debug the response contents: -->
アプリケーションにテスト要求を行った後、`dump`、`dumpHeaders`、および `dumpSession` メソッドを使用して、応答の内容を調べてデバッグできます。

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
あるいは、`dd`、`ddHeaders`、および `ddSession` メソッドを使用して、応答に関する情報をダンプしてから実行を停止することもできます。

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
場合によっては、アプリケーションが特定の例外をスローしているかどうかをテストしたい場合があります。例外が Laravel の例外ハンドラーによって捕捉され、HTTP 応答として返されないようにするには、リクエストを行う前に `withoutExceptionHandling` メソッドを呼び出すことができます。

```
$response = $this->withoutExceptionHandling()->get('/');
```

<!-- In addition, if you would like to ensure that your application is not utilizing features that have been deprecated by the PHP language or the libraries your application is using, you may invoke the `withoutDeprecationHandling` method before making your request. When deprecation handling is disabled, deprecation warnings will be converted to exceptions, thus causing your test to fail: -->
さらに、アプリケーションが PHP 言語またはアプリケーションが使用しているライブラリによって非推奨になった機能を利用していないことを確認したい場合は、リクエストを行う前に `withoutDeprecationHandling` メソッドを呼び出すことができます。非推奨の処理が無効になっていると、非推奨の警告が例外に変換されるため、テストが失敗します。

```
$response = $this->withoutDeprecationHandling()->get('/');
```

<a name="testing-json-apis"></a>
<!-- ## Testing JSON APIs -->
## Testing JSON APIs

<!-- Laravel also provides several helpers for testing JSON APIs and their responses. For example, the `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, and `optionsJson` methods may be used to issue JSON requests with various HTTP verbs. You may also easily pass data and headers to these methods. To get started, let's write a test to make a `POST` request to `/api/user` and assert that the expected JSON data was returned: -->
Laravel は、JSON API とその応答をテストするためのいくつかのヘルパも提供します。たとえば、`json`、`getJson`、`postJson`、`putJson`、`patchJson`、`deleteJson`、および `optionsJson` メソッドを使用して、さまざまな HTTP 動詞を含む JSON リクエストを発行できます。これらのメソッドにデータとヘッダーを簡単に渡すこともできます。まず、`POST` リクエストを `/api/user` に送信し、予期した JSON データが返されたことをアサートするテストを作成しましょう。

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
さらに、JSON 応答データは応答の配列変数としてアクセスできるため、JSON 応答内で返される個々の値を検査するのが便利になります。

```
$this->assertTrue($response['created']);
```

> [!NOTE]
> `assertJson` メソッドは、応答を配列に変換し、`PHPUnit::assertArraySubset` を利用して、アプリケーションから返された JSON 応答内に指定された配列が存在することを確認します。したがって、JSON 応答に他のプロパティがある場合でも、指定されたフラグメントが存在する限り、このテストは合格します。

<a name="verifying-exact-match"></a>
<!-- #### Asserting Exact JSON Matches -->
#### Asserting Exact JSON Matches

<!-- As previously mentioned, the `assertJson` method may be used to assert that a fragment of JSON exists within the JSON response. If you would like to verify that a given array **exactly matches** the JSON returned by your application, you should use the `assertExactJson` method: -->
前述したように、`assertJson` メソッドを使用して、JSON 応答内に JSON のフラグメントが存在することを確認できます。指定された配列がアプリケーションから返された JSON と**完全に一致**していることを確認したい場合は、`assertExactJson` メソッドを使用する必要があります。

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
JSON 応答に指定されたパスの指定されたデータが含まれていることを確認したい場合は、`assertJsonPath` メソッドを使用する必要があります。

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
`assertJsonPath` メソッドはクロージャーも受け入れます。これは、アサーションを渡す必要があるかどうかを動的に決定するために使用できます。

```
$response->assertJsonPath('team.owner.name', fn ($name) => strlen($name) >= 3);
```

<a name="fluent-json-testing"></a>
<!-- ### Fluent JSON Testing -->
### Fluent JSON Testing

<!-- Laravel also offers a beautiful way to fluently test your application's JSON responses. To get started, pass a closure to the `assertJson` method. This closure will be invoked with an instance of `Illuminate\Testing\Fluent\AssertableJson` which can be used to make assertions against the JSON that was returned by your application. The `where` method may be used to make assertions against a particular attribute of the JSON, while the `missing` method may be used to assert that a particular attribute is missing from the JSON: -->
Laravel は、アプリケーションの JSON 応答をスムーズにテストするための美しい方法も提供します。まず、クロージャを `assertJson` メソッドに渡します。このクロージャは、アプリケーションから返された JSON に対してアサーションを行うために使用できる `Illuminate\Testing\Fluent\AssertableJson` のインスタンスで呼び出されます。 `where` メソッドは、JSON の特定の属性に対するアサーションを行うために使用できますが、`missing` メソッドは、特定の属性が JSON に欠落していることをアサートするために使用できます。

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
上の例では、アサーション チェーンの最後で `etc` メソッドを呼び出していることに気づいたかもしれません。このメソッドは、JSON オブジェクトに他の属性が存在する可能性があることを Laravel に通知します。 `etc` メソッドが使用されていない場合、アサーションを行っていない他の属性が JSON オブジェクトに存在するとテストは失敗します。

<!-- The intention behind this behavior is to protect you from unintentionally exposing sensitive information in your JSON responses by forcing you to either explicitly make an assertion against the attribute or explicitly allow additional attributes via the `etc` method. -->
この動作の背後にある目的は、属性に対して明示的にアサーションを行うか、`etc` メソッドを介して追加の属性を明示的に許可することを強制することで、JSON 応答内の機密情報が意図せず公開されるのを防ぐことです。

<!-- However, you should be aware that not including the `etc` method in your assertion chain does not ensure that additional attributes are not being added to arrays that are nested within your JSON object. The `etc` method only ensures that no additional attributes exist at the nesting level in which the `etc` method is invoked. -->
ただし、アサーション チェーンに `etc` メソッドを含めないと、JSON オブジェクト内でネストされている配列に追加の属性が追加されなくなるわけではないことに注意してください。 `etc` メソッドは、`etc` メソッドが呼び出される入れ子レベルに追加の属性が存在しないことのみを保証します。

<a name="asserting-json-attribute-presence-and-absence"></a>
<!-- #### Asserting Attribute Presence / Absence -->
#### Asserting Attribute Presence / Absence

<!-- To assert that an attribute is present or absent, you may use the `has` and `missing` methods: -->
属性が存在するか存在しないかをアサートするには、`has` メソッドと `missing` メソッドを使用できます。

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
         ->missing('message')
);
```

<!-- In addition, the `hasAll` and `missingAll` methods allow asserting the presence or absence of multiple attributes simultaneously: -->
さらに、`hasAll` メソッドと `missingAll` メソッドを使用すると、複数の属性の有無を同時にアサートできます。

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
         ->missingAll(['message', 'code'])
);
```

<!-- You may use the `hasAny` method to determine if at least one of a given list of attributes is present: -->
`hasAny` メソッドを使用して、指定された属性リストの少なくとも 1 つが存在するかどうかを確認できます。

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
多くの場合、ルートは複数の項目 (複数のユーザーなど) を含む JSON 応答を返します。

```
Route::get('/users', function () {
    return User::all();
});
```

<!-- In these situations, we may use the fluent JSON object's `has` method to make assertions against the users included in the response. For example, let's assert that the JSON response contains three users. Next, we'll make some assertions about the first user in the collection using the `first` method. The `first` method accepts a closure which receives another assertable JSON string that we can use to make assertions about the first object in the JSON collection: -->
このような状況では、Fluent JSON オブジェクトの `has` メソッドを使用して、応答に含まれるユーザーに対してアサーションを行うことができます。たとえば、JSON 応答に 3 人のユーザーが含まれていると仮定します。次に、`first` メソッドを使用して、コレクション内の最初のユーザーに関するいくつかのアサーションを作成します。 `first` メソッドは、JSON コレクションの最初のオブジェクトについてアサーションを行うために使用できる別のアサート可能な JSON 文字列を受け取るクロージャを受け入れます。

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
場合によっては、アプリケーションのルートが名前付きキーが割り当てられた JSON コレクションを返すことがあります。

```
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```

<!-- When testing these routes, you may use the `has` method to assert against the number of items in the collection. In addition, you may use the `has` method to scope a chain of assertions: -->
これらのルートをテストするときは、`has` メソッドを使用して、コレクション内の項目の数に対してアサートできます。さらに、`has` メソッドを使用して、一連のアサーションの範囲を指定することもできます。

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
ただし、`users` コレクションに対してアサートするために `has` メソッドを 2 回別々に呼び出す代わりに、3 番目のパラメーターとしてクロージャを提供する 1 回の呼び出しを行うことができます。これを行うと、クロージャーが自動的に呼び出され、コレクション内の最初の項目にスコープが設定されます。

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
JSON 応答内のプロパティが特定のタイプであることをアサートしたいだけかもしれません。 `Illuminate\Testing\Fluent\AssertableJson` クラスは、まさにそれを行うための `whereType` メソッドと `whereAllType` メソッドを提供します。

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
`|` 文字を使用するか、タイプの配列を 2 番目のパラメータとして `whereType` メソッドに渡すことで、複数のタイプを指定できます。応答値がリストされているタイプのいずれかである場合、アサーションは成功します。

```
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
         ->whereType('id', ['string', 'integer'])
);
```

<!-- The `whereType` and `whereAllType` methods recognize the following types: `string`, `integer`, `double`, `boolean`, `array`, and `null`. -->
`whereType` メソッドと `whereAllType` メソッドは、`string`、`integer`、`double`、`boolean`、`array`、および `null` のタイプを認識します。

<a name="testing-file-uploads"></a>
<!-- ## Testing File Uploads -->
## Testing File Uploads

<!-- The `Illuminate\Http\UploadedFile` class provides a `fake` method which may be used to generate dummy files or images for testing. This, combined with the `Storage` facade's `fake` method, greatly simplifies the testing of file uploads. For example, you may combine these two features to easily test an avatar upload form: -->
`Illuminate\Http\UploadedFile` クラスは、テスト用のダミー ファイルまたはイメージを生成するために使用できる `fake` メソッドを提供します。これを `Storage` ファサードの `fake` メソッドと組み合わせると、ファイル アップロードのテストが大幅に簡素化されます。たとえば、次の 2 つの機能を組み合わせて、アバター アップロード フォームを簡単にテストできます。

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
特定のファイルが存在しないことを主張したい場合は、`Storage` ファサードによって提供される `assertMissing` メソッドを使用できます。

```
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```

<a name="fake-file-customization"></a>
<!-- #### Fake File Customization -->
#### Fake File Customization

<!-- When creating files using the `fake` method provided by the `UploadedFile` class, you may specify the width, height, and size of the image (in kilobytes) in order to better test your application's validation rules: -->
`UploadedFile` クラスによって提供される `fake` メソッドを使用してファイルを作成する場合、アプリケーションの検証ルールをより適切にテストするために、画像の幅、高さ、サイズ (キロバイト単位) を指定できます。

```
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```

<!-- In addition to creating images, you may create files of any other type using the `create` method: -->
イメージの作成に加えて、`create` メソッドを使用して他のタイプのファイルを作成することもできます。

```
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```

<!-- If needed, you may pass a `$mimeType` argument to the method to explicitly define the MIME type that should be returned by the file: -->
必要に応じて、`$mimeType` 引数をメソッドに渡して、ファイルによって返される MIME タイプを明示的に定義できます。

```
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```

<a name="testing-views"></a>
<!-- ## Testing Views -->
## Testing Views

<!-- Laravel also allows you to render a view without making a simulated HTTP request to the application. To accomplish this, you may call the `view` method within your test. The `view` method accepts the view name and an optional array of data. The method returns an instance of `Illuminate\Testing\TestView`, which offers several methods to conveniently make assertions about the view's contents: -->
Laravel では、アプリケーションに対してシミュレートされた HTTP リクエストを行わずにビューをレンダリングすることもできます。これを実現するには、テスト内で `view` メソッドを呼び出すことができます。 `view` メソッドは、ビュー名とオプションのデータ配列を受け入れます。このメソッドは `Illuminate\Testing\TestView` のインスタンスを返します。これは、ビューのコンテンツについて簡単にアサーションを行うためのいくつかのメソッドを提供します。

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
`TestView` クラスは、`assertSee`、`assertSeeInOrder`、`assertSeeText`、`assertSeeTextInOrder`、`assertDontSee`、および `assertDontSeeText` のアサーション メソッドを提供します。

<!-- If needed, you may get the raw, rendered view contents by casting the `TestView` instance to a string: -->
必要に応じて、`TestView` インスタンスを文字列にcastすることで、生のレンダリングされたビューのコンテンツを取得できます。

```
$contents = (string) $this->view('welcome');
```

<a name="sharing-errors"></a>
<!-- #### Sharing Errors -->
#### Sharing Errors

<!-- Some views may depend on errors shared in the [global error bag provided by Laravel](/docs/9.x/validation#quick-displaying-the-validation-errors). To hydrate the error bag with error messages, you may use the `withViewErrors` method: -->
一部のビューは、[global error bag provided by Laravel](/docs/9.x/validation#quick-displaying-the-validation-errors) で共有されたエラーに依存する場合があります。エラー バッグにエラー メッセージを追加するには、`withViewErrors` メソッドを使用します。

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
必要に応じて、`blade` メソッドを使用して、生の [Blade](/docs/9.x/blade) 文字列を評価およびレンダリングできます。 `view` メソッドと同様に、`blade` メソッドは `Illuminate\Testing\TestView` のインスタンスを返します。

```
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```

<!-- You may use the `component` method to evaluate and render a [Blade component](/docs/9.x/blade#components). The `component` method returns an instance of `Illuminate\Testing\TestComponent`: -->
`component` メソッドを使用して、[Blade component](/docs/9.x/blade#components) を評価およびレンダリングできます。 `component` メソッドは、`Illuminate\Testing\TestComponent` のインスタンスを返します。

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
Laravel の `Illuminate\Testing\TestResponse` クラスは、アプリケーションのテスト時に利用できるさまざまなカスタム アサーション メソッドを提供します。これらのアサーションは、`json`、`get`、`post`、`put`、および `delete` テスト メソッドによって返される応答でアクセスできます。

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
応答に指定された Cookie が含まれていることをアサートします。

```
$response->assertCookie($cookieName, $value = null);
```

<a name="assert-cookie-expired"></a>
<!-- #### assertCookieExpired -->
#### assertCookieExpired

<!-- Assert that the response contains the given cookie and it is expired: -->
応答に指定された Cookie が含まれており、有効期限が切れていることをアサートします。

```
$response->assertCookieExpired($cookieName);
```

<a name="assert-cookie-not-expired"></a>
<!-- #### assertCookieNotExpired -->
#### assertCookieNotExpired

<!-- Assert that the response contains the given cookie and it is not expired: -->
応答に指定された Cookie が含まれており、有効期限が切れていないことをアサートします。

```
$response->assertCookieNotExpired($cookieName);
```

<a name="assert-cookie-missing"></a>
<!-- #### assertCookieMissing -->
#### assertCookieMissing

<!-- Assert that the response does not contain the given cookie: -->
応答に指定された Cookie が含まれていないことをアサートします。

```
$response->assertCookieMissing($cookieName);
```

<a name="assert-created"></a>
<!-- #### assertCreated -->
#### assertCreated

<!-- Assert that the response has a 201 HTTP status code: -->
応答に 201 HTTP ステータス コードがあることをアサートします。

```
$response->assertCreated();
```

<a name="assert-dont-see"></a>
<!-- #### assertDontSee -->
#### assertDontSee

<!-- Assert that the given string is not contained within the response returned by the application. This assertion will automatically escape the given string unless you pass a second argument of `false`: -->
指定された文字列がアプリケーションから返された応答に含まれていないことをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。

```
$response->assertDontSee($value, $escaped = true);
```

<a name="assert-dont-see-text"></a>
<!-- #### assertDontSeeText -->
#### assertDontSeeText

<!-- Assert that the given string is not contained within the response text. This assertion will automatically escape the given string unless you pass a second argument of `false`. This method will pass the response content to the `strip_tags` PHP function before making the assertion: -->
指定された文字列が応答テキストに含まれていないことをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。このメソッドは、アサーションを行う前に、応答コンテンツを `strip_tags` PHP 関数に渡します。

```
$response->assertDontSeeText($value, $escaped = true);
```

<a name="assert-download"></a>
<!-- #### assertDownload -->
#### assertDownload

<!-- Assert that the response is a "download". Typically, this means the invoked route that returned the response returned a `Response::download` response, `BinaryFileResponse`, or `Storage::download` response: -->
応答が「ダウンロード」であることをアサートします。通常、これは、応答を返した呼び出されたルートが `Response::download` 応答、`BinaryFileResponse`、または `Storage::download` 応答を返したことを意味します。

```
$response->assertDownload();
```

<!-- If you wish, you may assert that the downloadable file was assigned a given file name: -->
必要に応じて、ダウンロード可能なファイルに特定のファイル名が割り当てられていることを主張できます。

```
$response->assertDownload('image.jpg');
```

<a name="assert-exact-json"></a>
<!-- #### assertExactJson -->
#### assertExactJson

<!-- Assert that the response contains an exact match of the given JSON data: -->
応答に指定された JSON データと完全に一致するものが含まれていることをアサートします。

```
$response->assertExactJson(array $data);
```

<a name="assert-forbidden"></a>
<!-- #### assertForbidden -->
#### assertForbidden

<!-- Assert that the response has a forbidden (403) HTTP status code: -->
応答に禁止された (403) HTTP ステータス コードがあることをアサートします。

```
$response->assertForbidden();
```

<a name="assert-header"></a>
<!-- #### assertHeader -->
#### assertHeader

<!-- Assert that the given header and value is present on the response: -->
指定されたヘッダーと値が応答に存在することをアサートします。

```
$response->assertHeader($headerName, $value = null);
```

<a name="assert-header-missing"></a>
<!-- #### assertHeaderMissing -->
#### assertHeaderMissing

<!-- Assert that the given header is not present on the response: -->
指定されたヘッダーが応答に存在しないことをアサートします。

```
$response->assertHeaderMissing($headerName);
```

<a name="assert-json"></a>
<!-- #### assertJson -->
#### assertJson

<!-- Assert that the response contains the given JSON data: -->
応答に指定された JSON データが含まれていることをアサートします。

```
$response->assertJson(array $data, $strict = false);
```

<!-- The `assertJson` method converts the response to an array and utilizes `PHPUnit::assertArraySubset` to verify that the given array exists within the JSON response returned by the application. So, if there are other properties in the JSON response, this test will still pass as long as the given fragment is present. -->
`assertJson` メソッドは、応答を配列に変換し、`PHPUnit::assertArraySubset` を利用して、アプリケーションから返された JSON 応答内に指定された配列が存在することを確認します。したがって、JSON 応答に他のプロパティがある場合でも、指定されたフラグメントが存在する限り、このテストは合格します。

<a name="assert-json-count"></a>
<!-- #### assertJsonCount -->
#### assertJsonCount

<!-- Assert that the response JSON has an array with the expected number of items at the given key: -->
応答 JSON に、指定されたキーで予想される数の項目を含む配列があることをアサートします。

```
$response->assertJsonCount($count, $key = null);
```

<a name="assert-json-fragment"></a>
<!-- #### assertJsonFragment -->
#### assertJsonFragment

<!-- Assert that the response contains the given JSON data anywhere in the response: -->
応答の任意の場所に指定された JSON データが含まれていることをアサートします。

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
応答 JSON が配列であることをアサートします。

```
$response->assertJsonIsArray();
```

<a name="assert-json-is-object"></a>
<!-- #### assertJsonIsObject -->
#### assertJsonIsObject

<!-- Assert that the response JSON is an object: -->
応答 JSON がオブジェクトであることをアサートします。

```
$response->assertJsonIsObject();
```

<a name="assert-json-missing"></a>
<!-- #### assertJsonMissing -->
#### assertJsonMissing

<!-- Assert that the response does not contain the given JSON data: -->
応答に指定された JSON データが含まれていないことをアサートします。

```
$response->assertJsonMissing(array $data);
```

<a name="assert-json-missing-exact"></a>
<!-- #### assertJsonMissingExact -->
#### assertJsonMissingExact

<!-- Assert that the response does not contain the exact JSON data: -->
応答に正確な JSON データが含まれていないことをアサートします。

```
$response->assertJsonMissingExact(array $data);
```

<a name="assert-json-missing-validation-errors"></a>
<!-- #### assertJsonMissingValidationErrors -->
#### assertJsonMissingValidationErrors

<!-- Assert that the response has no JSON validation errors for the given keys: -->
指定されたキーに対する応答に JSON 検証エラーがないことをアサートします。

```
$response->assertJsonMissingValidationErrors($keys);
```

> [!NOTE]
> より汎用的な [assertValid](#assert-valid) メソッドを使用すると、応答に JSON として返された検証エラーがないこと、**およびセッション ストレージにフラッシュされたエラーがないこと**を主張できます。

<a name="assert-json-path"></a>
<!-- #### assertJsonPath -->
#### assertJsonPath

<!-- Assert that the response contains the given data at the specified path: -->
応答に指定されたパスにある指定されたデータが含まれていることをアサートします。

```
$response->assertJsonPath($path, $expectedValue);
```

<!-- For example, if the following JSON response is returned by your application: -->
たとえば、アプリケーションから次の JSON 応答が返されたとします。

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that the `name` property of the `user` object matches a given value like so: -->
次のように、`user` オブジェクトの `name` プロパティが指定された値と一致すると主張できます。

```
$response->assertJsonPath('user.name', 'Steve Schoger');
```

<a name="assert-json-missing-path"></a>
<!-- #### assertJsonMissingPath -->
#### assertJsonMissingPath

<!-- Assert that the response does not contain the given path: -->
応答に指定されたパスが含まれていないことをアサートします。

```
$response->assertJsonMissingPath($path);
```

<!-- For example, if the following JSON response is returned by your application: -->
たとえば、アプリケーションから次の JSON 応答が返されたとします。

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that it does not contain the `email` property of the `user` object: -->
`user` オブジェクトの `email` プロパティが含まれていないと主張することもできます。

```
$response->assertJsonMissingPath('user.email');
```

<a name="assert-json-structure"></a>
<!-- #### assertJsonStructure -->
#### assertJsonStructure

<!-- Assert that the response has a given JSON structure: -->
応答が指定された JSON 構造を持つことをアサートします。

```
$response->assertJsonStructure(array $structure);
```

<!-- For example, if the JSON response returned by your application contains the following data: -->
たとえば、アプリケーションから返された JSON 応答に次のデータが含まれているとします。

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

<!-- You may assert that the JSON structure matches your expectations like so: -->
次のように、JSON 構造が期待どおりであると主張できます。

```
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```

<!-- Sometimes, JSON responses returned by your application may contain arrays of objects: -->
場合によっては、アプリケーションから返される JSON 応答にオブジェクトの配列が含まれる場合があります。

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
この状況では、`*` 文字を使用して、配列内のすべてのオブジェクトの構造に対してアサートできます。

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
応答に指定されたキーに対して指定された JSON 検証エラーがあることをアサートします。このメソッドは、検証エラーがセッションにフラッシュされるのではなく JSON 構造として返される応答に対してアサートするときに使用する必要があります。

```
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```

> [!NOTE]
> より汎用的な [assertInvalid](#assert-invalid) メソッドを使用すると、応答に検証エラーが JSON として返されたことを主張する ** または ** エラーがセッション ストレージにフラッシュされたことを主張できます。

<a name="assert-json-validation-error-for"></a>
<!-- #### assertJsonValidationErrorFor -->
#### assertJsonValidationErrorFor

<!-- Assert the response has any JSON validation errors for the given key: -->
応答に指定されたキーの JSON 検証エラーがあることをアサートします。

```
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```

<a name="assert-location"></a>
<!-- #### assertLocation -->
#### assertLocation

<!-- Assert that the response has the given URI value in the `Location` header: -->
応答の `Location` ヘッダーに指定された URI 値があることをアサートします。

```
$response->assertLocation($uri);
```
<a name="assert-content"></a>
<!-- #### assertContent -->
#### assertContent

<!-- Assert that the given string matches the response content: -->
指定された文字列が応答の内容と一致することをアサートします。

```
$response->assertContent($value);
```

<a name="assert-no-content"></a>
<!-- #### assertNoContent -->
#### assertNoContent

<!-- Assert that the response has the given HTTP status code and no content: -->
応答に指定された HTTP ステータス コードがあり、内容が含まれていないことをアサートします。

```
$response->assertNoContent($status = 204);
```

<a name="assert-streamed-content"></a>
<!-- #### assertStreamedContent -->
#### assertStreamedContent

<!-- Assert that the given string matches the streamed response content: -->
指定された文字列がストリーミングされた応答コンテンツと一致することをアサートします。

```
$response->assertStreamedContent($value);
```

<a name="assert-not-found"></a>
<!-- #### assertNotFound -->
#### assertNotFound

<!-- Assert that the response has a not found (404) HTTP status code: -->
応答に not found (404) HTTP ステータス コードがあることをアサートします。

```
$response->assertNotFound();
```

<a name="assert-ok"></a>
<!-- #### assertOk -->
#### assertOk

<!-- Assert that the response has a 200 HTTP status code: -->
応答に 200 HTTP ステータス コードがあることをアサートします。

```
$response->assertOk();
```

<a name="assert-plain-cookie"></a>
<!-- #### assertPlainCookie -->
#### assertPlainCookie

<!-- Assert that the response contains the given unencrypted cookie: -->
応答に指定された暗号化されていない Cookie が含まれていることをアサートします。

```
$response->assertPlainCookie($cookieName, $value = null);
```

<a name="assert-redirect"></a>
<!-- #### assertRedirect -->
#### assertRedirect

<!-- Assert that the response is a redirect to the given URI: -->
応答が指定された URI へのリダイレクトであることをアサートします。

```
$response->assertRedirect($uri);
```

<a name="assert-redirect-contains"></a>
<!-- #### assertRedirectContains -->
#### assertRedirectContains

<!-- Assert whether the response is redirecting to a URI that contains the given string: -->
応答が指定された文字列を含む URI にリダイレクトされているかどうかを確認します。

```
$response->assertRedirectContains($string);
```

<a name="assert-redirect-to-route"></a>
<!-- #### assertRedirectToRoute -->
#### assertRedirectToRoute

<!-- Assert that the response is a redirect to the given [named route](/docs/9.x/routing#named-routes): -->
応答が指定された [named route](/docs/9.x/routing#named-routes) へのリダイレクトであることをアサートします。

```
$response->assertRedirectToRoute($name = null, $parameters = []);
```

<a name="assert-redirect-to-signed-route"></a>
<!-- #### assertRedirectToSignedRoute -->
#### assertRedirectToSignedRoute

<!-- Assert that the response is a redirect to the given [signed route](/docs/9.x/urls#signed-urls): -->
応答が指定された [signed route](/docs/9.x/urls#signed-urls) へのリダイレクトであることをアサートします。

```
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```

<a name="assert-see"></a>
<!-- #### assertSee -->
#### assertSee

<!-- Assert that the given string is contained within the response. This assertion will automatically escape the given string unless you pass a second argument of `false`: -->
指定された文字列が応答内に含まれていることをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。

```
$response->assertSee($value, $escaped = true);
```

<a name="assert-see-in-order"></a>
<!-- #### assertSeeInOrder -->
#### assertSeeInOrder

<!-- Assert that the given strings are contained in order within the response. This assertion will automatically escape the given strings unless you pass a second argument of `false`: -->
指定された文字列が応答内に順番に含まれていることをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。

```
$response->assertSeeInOrder(array $values, $escaped = true);
```

<a name="assert-see-text"></a>
<!-- #### assertSeeText -->
#### assertSeeText

<!-- Assert that the given string is contained within the response text. This assertion will automatically escape the given string unless you pass a second argument of `false`. The response content will be passed to the `strip_tags` PHP function before the assertion is made: -->
指定された文字列が応答テキストに含まれていることをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。応答コンテンツは、アサーションが行われる前に `strip_tags` PHP 関数に渡されます。

```
$response->assertSeeText($value, $escaped = true);
```

<a name="assert-see-text-in-order"></a>
<!-- #### assertSeeTextInOrder -->
#### assertSeeTextInOrder

<!-- Assert that the given strings are contained in order within the response text. This assertion will automatically escape the given strings unless you pass a second argument of `false`. The response content will be passed to the `strip_tags` PHP function before the assertion is made: -->
指定された文字列が応答テキスト内に順番に含まれていることを確認します。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。応答コンテンツは、アサーションが行われる前に `strip_tags` PHP 関数に渡されます。

```
$response->assertSeeTextInOrder(array $values, $escaped = true);
```

<a name="assert-session-has"></a>
<!-- #### assertSessionHas -->
#### assertSessionHas

<!-- Assert that the session contains the given piece of data: -->
セッションに指定されたデータが含まれていることをアサートします。

```
$response->assertSessionHas($key, $value = null);
```

<!-- If needed, a closure can be provided as the second argument to the `assertSessionHas` method. The assertion will pass if the closure returns `true`: -->
必要に応じて、`assertSessionHas` メソッドの 2 番目の引数としてクロージャーを提供できます。クロージャが `true` を返す場合、アサーションは合格します。

```
$response->assertSessionHas($key, function ($value) {
    return $value->name === 'Taylor Otwell';
});
```

<a name="assert-session-has-input"></a>
<!-- #### assertSessionHasInput -->
#### assertSessionHasInput

<!-- Assert that the session has a given value in the [flashed input array](/docs/9.x/responses#redirecting-with-flashed-session-data): -->
セッションの [flashed input array](/docs/9.x/responses#redirecting-with-flashed-session-data) に指定された値があることをアサートします。

```
$response->assertSessionHasInput($key, $value = null);
```

<!-- If needed, a closure can be provided as the second argument to the `assertSessionHasInput` method. The assertion will pass if the closure returns `true`: -->
必要に応じて、`assertSessionHasInput` メソッドの 2 番目の引数としてクロージャーを提供できます。クロージャが `true` を返す場合、アサーションは合格します。

```
$response->assertSessionHasInput($key, function ($value) {
    return Crypt::decryptString($value) === 'secret';
});
```

<a name="assert-session-has-all"></a>
<!-- #### assertSessionHasAll -->
#### assertSessionHasAll

<!-- Assert that the session contains a given array of key / value pairs: -->
セッションにキーと値のペアの指定された配列が含まれていることをアサートします。

```
$response->assertSessionHasAll(array $data);
```

<!-- For example, if your application's session contains `name` and `status` keys, you may assert that both exist and have the specified values like so: -->
たとえば、アプリケーションのセッションに `name` キーと `status` キーが含まれている場合、次のように両方が存在し、指定された値を持つことをアサートできます。

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
セッションに指定された `$keys` のエラーが含まれていることをアサートします。 `$keys` が連想配列の場合、セッションに各フィールド (キー) に特定のエラー メッセージ (値) が含まれていることをアサートします。このメソッドは、検証エラーを JSON 構造として返すのではなく、セッションにフラッシュするルートをテストするときに使用する必要があります。

```
$response->assertSessionHasErrors(
    array $keys, $format = null, $errorBag = 'default'
);
```

<!-- For example, to assert that the `name` and `email` fields have validation error messages that were flashed to the session, you may invoke the `assertSessionHasErrors` method like so: -->
たとえば、`name` フィールドと `email` フィールドにセッションにフラッシュされた検証エラー メッセージがあることを主張するには、次のように `assertSessionHasErrors` メソッドを呼び出すことができます。

```
$response->assertSessionHasErrors(['name', 'email']);
```

<!-- Or, you may assert that a given field has a particular validation error message: -->
または、特定のフィールドに特定の検証エラー メッセージがあると主張することもできます。

```
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```

> [!NOTE]
> より汎用的な [assertInvalid](#assert-invalid) メソッドを使用すると、応答に検証エラーが JSON として返されたことを主張する ** または ** エラーがセッション ストレージにフラッシュされたことを主張できます。

<a name="assert-session-has-errors-in"></a>
<!-- #### assertSessionHasErrorsIn -->
#### assertSessionHasErrorsIn

<!-- Assert that the session contains an error for the given `$keys` within a specific [error bag](/docs/9.x/validation#named-error-bags). If `$keys` is an associative array, assert that the session contains a specific error message (value) for each field (key), within the error bag: -->
セッションに特定の [error bag](/docs/9.x/validation#named-error-bags) 内の指定された `$keys` のエラーが含まれていることをアサートします。 `$keys` が連想配列の場合、セッションのエラー バッグ内に各フィールド (キー) に特定のエラー メッセージ (値) が含まれていることをアサートします。

```
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```

<a name="assert-session-has-no-errors"></a>
<!-- #### assertSessionHasNoErrors -->
#### assertSessionHasNoErrors

<!-- Assert that the session has no validation errors: -->
セッションに検証エラーがないことをアサートします。

```
$response->assertSessionHasNoErrors();
```

<a name="assert-session-doesnt-have-errors"></a>
<!-- #### assertSessionDoesntHaveErrors -->
#### assertSessionDoesntHaveErrors

<!-- Assert that the session has no validation errors for the given keys: -->
セッションに指定されたキーの検証エラーがないことをアサートします。

```
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```

> [!NOTE]
> より汎用的な [assertValid](#assert-valid) メソッドを使用すると、応答に JSON として返された検証エラーがないこと、**およびセッション ストレージにフラッシュされたエラーがないこと**を主張できます。

<a name="assert-session-missing"></a>
<!-- #### assertSessionMissing -->
#### assertSessionMissing

<!-- Assert that the session does not contain the given key: -->
セッションに指定されたキーが含まれていないことをアサートします。

```
$response->assertSessionMissing($key);
```

<a name="assert-status"></a>
<!-- #### assertStatus -->
#### assertStatus

<!-- Assert that the response has a given HTTP status code: -->
応答に指定された HTTP ステータス コードがあることをアサートします。

```
$response->assertStatus($code);
```

<a name="assert-successful"></a>
<!-- #### assertSuccessful -->
#### assertSuccessful

<!-- Assert that the response has a successful (>= 200 and < 300) HTTP status code: -->
応答に成功 (>= 200 および < 300) HTTP ステータス コードがあることをアサートします。

```
$response->assertSuccessful();
```

<a name="assert-unauthorized"></a>
<!-- #### assertUnauthorized -->
#### assertUnauthorized

<!-- Assert that the response has an unauthorized (401) HTTP status code: -->
応答に未承認 (401) HTTP ステータス コードがあることをアサートします。

```
$response->assertUnauthorized();
```

<a name="assert-unprocessable"></a>
<!-- #### assertUnprocessable -->
#### assertUnprocessable

<!-- Assert that the response has an unprocessable entity (422) HTTP status code: -->
応答に処理できないエンティティ (422) HTTP ステータス コードがあることをアサートします。

```
$response->assertUnprocessable();
```

<a name="assert-valid"></a>
<!-- #### assertValid -->
#### assertValid

<!-- Assert that the response has no validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
応答に指定されたキーの検証エラーがないことをアサートします。このメソッドは、検証エラーが JSON 構造として返される場合、または検証エラーがセッションにフラッシュされた場合の応答に対するアサートに使用できます。

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
応答に指定されたキーの検証エラーがあることをアサートします。このメソッドは、検証エラーが JSON 構造として返される場合、または検証エラーがセッションにフラッシュされた場合の応答に対するアサートに使用できます。

```
$response->assertInvalid(['name', 'email']);
```

<!-- You may also assert that a given key has a particular validation error message. When doing so, you may provide the entire message or only a small portion of the message: -->
特定のキーに特定の検証エラー メッセージがあると主張することもできます。その際、メッセージ全体を提供することも、メッセージの一部だけを提供することもできます。

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
応答ビューに指定されたデータが含まれていることをアサートします。

```
$response->assertViewHas($key, $value = null);
```

<!-- Passing a closure as the second argument to the `assertViewHas` method will allow you to inspect and make assertions against a particular piece of view data: -->
`assertViewHas` メソッドの 2 番目の引数としてクロージャを渡すと、ビュー データの特定の部分を検査してアサーションを行うことができます。

```
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```

<!-- In addition, view data may be accessed as array variables on the response, allowing you to conveniently inspect it: -->
さらに、ビュー データは応答の配列変数としてアクセスできるため、簡単に検査できます。

```
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
<!-- #### assertViewHasAll -->
#### assertViewHasAll

<!-- Assert that the response view has a given list of data: -->
応答ビューに指定されたデータのリストがあることをアサートします。

```
$response->assertViewHasAll(array $data);
```

<!-- This method may be used to assert that the view simply contains data matching the given keys: -->
このメソッドは、ビューに単に指定されたキーに一致するデータが含まれていることをアサートするために使用できます。

```
$response->assertViewHasAll([
    'name',
    'email',
]);
```

<!-- Or, you may assert that the view data is present and has specific values: -->
または、ビュー データが存在し、特定の値を持っていると主張することもできます。

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
指定されたビューがルートによって返されたことをアサートします。

```
$response->assertViewIs($value);
```

<a name="assert-view-missing"></a>
<!-- #### assertViewMissing -->
#### assertViewMissing

<!-- Assert that the given data key was not made available to the view returned in the application's response: -->
指定されたデータ キーがアプリケーションの応答で返されたビューで使用可能になっていないことをアサートします。

```
$response->assertViewMissing($key);
```

<a name="authentication-assertions"></a>
<!-- ### Authentication Assertions -->
### Authentication Assertions

<!-- Laravel also provides a variety of authentication related assertions that you may utilize within your application's feature tests. Note that these methods are invoked on the test class itself and not the `Illuminate\Testing\TestResponse` instance returned by methods such as `get` and `post`. -->
Laravel は、アプリケーションの機能テスト内で利用できるさまざまな認証関連のアサーションも提供します。これらのメソッドは、`get` や `post` などのメソッドによって返される `Illuminate\Testing\TestResponse` インスタンスではなく、テスト クラス自体で呼び出されることに注意してください。

<a name="assert-authenticated"></a>
<!-- #### assertAuthenticated -->
#### assertAuthenticated

<!-- Assert that a user is authenticated: -->
ユーザーが認証されていることをアサートします。

```
$this->assertAuthenticated($guard = null);
```

<a name="assert-guest"></a>
<!-- #### assertGuest -->
#### assertGuest

<!-- Assert that a user is not authenticated: -->
ユーザーが認証されていないことをアサートします。

```
$this->assertGuest($guard = null);
```

<a name="assert-authenticated-as"></a>
<!-- #### assertAuthenticatedAs -->
#### assertAuthenticatedAs

<!-- Assert that a specific user is authenticated: -->
特定のユーザーが認証されていることをアサートします。

```
$this->assertAuthenticatedAs($user, $guard = null);
```

<a name="validation-assertions"></a>
<!-- ## Validation Assertions -->
## Validation Assertions

<!-- Laravel provides two primary validation related assertions that you may use to ensure the data provided in your request was either valid or invalid. -->
Laravel は、リクエストで提供されたデータが有効か無効かを確認するために使用できる 2 つの主要な検証関連アサーションを提供します。

<a name="validation-assert-valid"></a>
<!-- #### assertValid -->
#### assertValid

<!-- Assert that the response has no validation errors for the given keys. This method may be used for asserting against responses where the validation errors are returned as a JSON structure or where the validation errors have been flashed to the session: -->
応答に指定されたキーの検証エラーがないことをアサートします。このメソッドは、検証エラーが JSON 構造として返される場合、または検証エラーがセッションにフラッシュされた場合の応答に対するアサートに使用できます。

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
応答に指定されたキーの検証エラーがあることをアサートします。このメソッドは、検証エラーが JSON 構造として返される場合、または検証エラーがセッションにフラッシュされた場合の応答に対するアサートに使用できます。

```
$response->assertInvalid(['name', 'email']);
```

<!-- You may also assert that a given key has a particular validation error message. When doing so, you may provide the entire message or only a small portion of the message: -->
特定のキーに特定の検証エラー メッセージがあると主張することもできます。その際、メッセージ全体を提供することも、メッセージの一部だけを提供することもできます。

```
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```

