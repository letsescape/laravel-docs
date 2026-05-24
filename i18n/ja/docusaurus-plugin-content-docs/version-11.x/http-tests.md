# HTTP テスト (HTTP Tests)

- [Introduction](#introduction)
- [リクエストの作成](#making-requests)
    - [リクエストヘッダーのカスタマイズ](#customizing-request-headers)
    - [Cookies](#cookies)
    - [セッション/認証](#session-and-authentication)
    - [デバッグ応答](#debugging-responses)
    - [例外処理](#exception-handling)
- [JSON APIのテスト](#testing-json-apis)
    - [流暢な JSON テスト](#fluent-json-testing)
- [ファイルのアップロードのテスト](#testing-file-uploads)
- [ビューのテスト](#testing-views)
    - [レンダリングBladeとコンポーネント](#rendering-blade-and-components)
- [利用可能なアサーション](#available-assertions)
    - [応答アサーション](#response-assertions)
    - [認証アサーション](#authentication-assertions)
    - [検証アサーション](#validation-assertions)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、アプリケーションに HTTP リクエストを送信し、その応答を調べるための非常に流暢な API を提供します。たとえば、以下に定義されている機能テストを見てください。

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

`get` メソッドは、アプリケーションに `GET` リクエストを送信します。一方、`assertStatus` メソッドは、返される応答には指定された HTTP ステータス コードが含まれる必要があることをアサートします。この単純なアサーションに加えて、Laravel には、応答ヘッダー、コンテンツ、JSON 構造などを検査するためのさまざまなアサーションも含まれています。

<a name="making-requests"></a>
## リクエストの作成 (Making Requests)

アプリケーションにリクエストを行うには、テスト内で `get`、`post`、`put`、`patch`、または `delete` メソッドを呼び出すことができます。これらのメソッドは、実際にはアプリケーションに「実際の」HTTP リクエストを発行しません。代わりに、ネットワーク要求全体が内部的にシミュレートされます。

テスト リクエスト メソッドは、`Illuminate\Http\Response` インスタンスを返す代わりに、`Illuminate\Testing\TestResponse` のインスタンスを返します。これにより、アプリケーションの応答を検査できる [さまざまな役立つ主張](#available-assertions) が提供されます。

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

一般に、各テストはアプリケーションに対して 1 つのリクエストのみを行う必要があります。単一のテスト メソッド内で複数のリクエストが実行されると、予期しない動作が発生する可能性があります。

> [!NOTE]  
> 便宜上、CSRF ミドルウェアはテストの実行時に自動的に無効になります。

<a name="customizing-request-headers"></a>
### リクエストヘッダーのカスタマイズ

`withHeaders` メソッドを使用して、アプリケーションに送信される前にリクエストのヘッダーをカスタマイズできます。このメソッドを使用すると、リクエストに必要なカスタム ヘッダーを追加できます。

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
### クッキー

リクエストを行う前に、`withCookie` メソッドまたは `withCookies` メソッドを使用して Cookie 値を設定できます。 `withCookie` メソッドは 2 つの引数として Cookie 名と値を受け入れますが、`withCookies` メソッドは名前と値のペアの配列を受け入れます。

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
### セッション/認証

Laravel は、HTTP テスト中にセッションと対話するためのいくつかのヘルパを提供します。まず、`withSession` メソッドを使用して、セッション データを特定の配列に設定します。これは、アプリケーションにリクエストを発行する前にセッションにデータをロードする場合に便利です。

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

Laravel のセッションは通常、現在認証されているユーザーの状態を維持するために使用されます。したがって、`actingAs` ヘルパ メソッドは、特定のユーザーを現在のユーザーとして認証する簡単な方法を提供します。たとえば、[モデルファクトリー](/docs/{{version}}/eloquent-factories) を使用してユーザーを生成および認証できます。

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

`actingAs` メソッドの 2 番目の引数としてガード名を渡すことで、特定のユーザーの認証にどのガードを使用するかを指定することもできます。 `actingAs` メソッドに提供されるガードも、テスト中のデフォルトのガードになります。

    $this->actingAs($user, 'web')

<a name="debugging-responses"></a>
### デバッグ応答

アプリケーションにテスト要求を行った後、`dump`、`dumpHeaders`、および `dumpSession` メソッドを使用して、応答の内容を調べてデバッグできます。

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dumpHeaders();

    $response->dumpSession();

    $response->dump();
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

        $response->dumpHeaders();

        $response->dumpSession();

        $response->dump();
    }
}
```

あるいは、`dd`、`ddHeaders`、`ddSession`、および `ddJson` メソッドを使用して、応答に関する情報をダンプしてから実行を停止することもできます。

```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->ddHeaders();
    $response->ddSession();
    $response->ddJson();
    $response->dd();
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

        $response->ddHeaders();

        $response->ddSession();

        $response->dd();
    }
}
```

<a name="exception-handling"></a>
### 例外処理

場合によっては、アプリケーションが特定の例外をスローしているかどうかをテストする必要があるかもしれません。これを実現するには、`Exceptions` ファサードを介して例外ハンドラーを「偽装」できます。例外ハンドラーが偽装されると、`assertReported` メソッドと `assertNotReported` メソッドを利用して、リクエスト中にスローされた例外に対するアサーションを行うことができます。

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

`assertNotReported` メソッドと `assertNothingReported` メソッドは、リクエスト中に特定の例外がスローされなかったこと、または例外がスローされなかったことをアサートするために使用できます。

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```

リクエストを行う前に `withoutExceptionHandling` メソッドを呼び出すことで、特定のリクエストの例外処理を完全に無効にすることができます。

    $response = $this->withoutExceptionHandling()->get('/');

さらに、アプリケーションが PHP 言語またはアプリケーションが使用しているライブラリによって非推奨になった機能を利用していないことを確認したい場合は、リクエストを行う前に `withoutDeprecationHandling` メソッドを呼び出すことができます。非推奨の処理が無効になっていると、非推奨の警告が例外に変換されるため、テストが失敗します。

    $response = $this->withoutDeprecationHandling()->get('/');

`assertThrows` メソッドは、指定されたクロージャ内のコードが指定されたタイプの例外をスローすることをアサートするために使用できます。

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```

スローされた例外を検査してアサーションを行いたい場合は、`assertThrows` メソッドの 2 番目の引数としてクロージャを指定できます。

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123;
);
```

<a name="testing-json-apis"></a>
## JSON APIのテスト (Testing JSON APIs)

Laravel は、JSON API とその応答をテストするためのいくつかのヘルパも提供します。たとえば、`json`、`getJson`、`postJson`、`putJson`、`patchJson`、`deleteJson`、および `optionsJson` メソッドを使用して、さまざまな HTTP 動詞を含む JSON リクエストを発行できます。これらのメソッドにデータとヘッダーを簡単に渡すこともできます。まず、`POST` リクエストを `/api/user` に送信し、予期した JSON データが返されたことをアサートするテストを作成しましょう。

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

さらに、JSON 応答データは応答の配列変数としてアクセスできるため、JSON 応答内で返される個々の値を検査するのが便利になります。

```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```

> [!NOTE]  
> `assertJson` メソッドは、応答を配列に変換して、アプリケーションから返された JSON 応答内に指定された配列が存在することを確認します。したがって、JSON 応答に他のプロパティがある場合でも、指定されたフラグメントが存在する限り、このテストは合格します。

<a name="verifying-exact-match"></a>
#### JSON の完全一致のアサート

前述したように、`assertJson` メソッドを使用して、JSON 応答内に JSON のフラグメントが存在することを確認できます。指定された配列がアプリケーションから返された JSON と**完全に一致**していることを確認したい場合は、`assertExactJson` メソッドを使用する必要があります。

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
#### JSON パスでのアサート

JSON 応答に指定されたパスの指定されたデータが含まれていることを確認したい場合は、`assertJsonPath` メソッドを使用する必要があります。

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

`assertJsonPath` メソッドはクロージャーも受け入れます。これは、アサーションを渡す必要があるかどうかを動的に決定するために使用できます。

    $response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);

<a name="fluent-json-testing"></a>
### 流暢な JSON テスト

Laravel は、アプリケーションの JSON 応答をスムーズにテストするための美しい方法も提供します。まず、クロージャを `assertJson` メソッドに渡します。このクロージャは、アプリケーションから返された JSON に対してアサーションを行うために使用できる `Illuminate\Testing\Fluent\AssertableJson` のインスタンスで呼び出されます。 `where` メソッドは、JSON の特定の属性に対するアサーションを行うために使用できますが、`missing` メソッドは、特定の属性が JSON に欠落していることをアサートするために使用できます。

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

#### `etc` メソッドについて

上の例では、アサーション チェーンの最後で `etc` メソッドを呼び出していることに気づいたかもしれません。このメソッドは、JSON オブジェクトに他の属性が存在する可能性があることを Laravel に通知します。 `etc` メソッドが使用されていない場合、アサーションを行っていない他の属性が JSON オブジェクトに存在するとテストは失敗します。

この動作の背後にある目的は、属性に対して明示的にアサーションを行うか、`etc` メソッドを介して追加の属性を明示的に許可することを強制することで、JSON 応答内の機密情報が意図せず公開されるのを防ぐことです。

ただし、アサーション チェーンに `etc` メソッドを含めないと、JSON オブジェクト内でネストされている配列に追加の属性が追加されなくなるわけではないことに注意してください。 `etc` メソッドは、`etc` メソッドが呼び出される入れ子レベルに追加の属性が存在しないことのみを保証します。

<a name="asserting-json-attribute-presence-and-absence"></a>
#### 属性の有無のアサート

属性が存在するか存在しないかをアサートするには、`has` メソッドと `missing` メソッドを使用できます。

    $response->assertJson(fn (AssertableJson $json) =>
        $json->has('data')
            ->missing('message')
    );

さらに、`hasAll` メソッドと `missingAll` メソッドを使用すると、複数の属性の有無を同時にアサートできます。

    $response->assertJson(fn (AssertableJson $json) =>
        $json->hasAll(['status', 'data'])
            ->missingAll(['message', 'code'])
    );

`hasAny` メソッドを使用して、指定された属性リストの少なくとも 1 つが存在するかどうかを確認できます。

    $response->assertJson(fn (AssertableJson $json) =>
        $json->has('status')
            ->hasAny('data', 'message', 'code')
    );

<a name="asserting-against-json-collections"></a>
#### JSON コレクションに対するアサート

多くの場合、ルートは複数の項目 (複数のユーザーなど) を含む JSON 応答を返します。

    Route::get('/users', function () {
        return User::all();
    });

このような状況では、Fluent JSON オブジェクトの `has` メソッドを使用して、応答に含まれるユーザーに対してアサーションを行うことができます。たとえば、JSON 応答に 3 人のユーザーが含まれていると仮定します。次に、`first` メソッドを使用して、コレクション内の最初のユーザーに関するいくつかのアサーションを作成します。 `first` メソッドは、JSON コレクションの最初のオブジェクトについてアサーションを行うために使用できる別のアサート可能な JSON 文字列を受け取るクロージャを受け入れます。

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

<a name="scoping-json-collection-assertions"></a>
#### JSON コレクション アサーションのスコープ設定

場合によっては、アプリケーションのルートが名前付きキーが割り当てられた JSON コレクションを返すことがあります。

    Route::get('/users', function () {
        return [
            'meta' => [...],
            'users' => User::all(),
        ];
    })

これらのルートをテストするときは、`has` メソッドを使用して、コレクション内の項目の数に対してアサートできます。さらに、`has` メソッドを使用して、一連のアサーションの範囲を指定することもできます。

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

ただし、`users` コレクションに対してアサートするために `has` メソッドを 2 回別々に呼び出す代わりに、3 番目のパラメーターとしてクロージャを提供する 1 回の呼び出しを行うことができます。これを行うと、クロージャーが自動的に呼び出され、コレクション内の最初の項目にスコープが設定されます。

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

<a name="asserting-json-types"></a>
#### JSON タイプのアサート

JSON 応答内のプロパティが特定のタイプであることをアサートしたいだけかもしれません。 `Illuminate\Testing\Fluent\AssertableJson` クラスは、まさにそれを行うための `whereType` メソッドと `whereAllType` メソッドを提供します。

    $response->assertJson(fn (AssertableJson $json) =>
        $json->whereType('id', 'integer')
            ->whereAllType([
                'users.0.name' => 'string',
                'meta' => 'array'
            ])
    );

`|` 文字を使用するか、タイプの配列を 2 番目のパラメータとして `whereType` メソッドに渡すことで、複数のタイプを指定できます。応答値がリストされているタイプのいずれかである場合、アサーションは成功します。

    $response->assertJson(fn (AssertableJson $json) =>
        $json->whereType('name', 'string|null')
            ->whereType('id', ['string', 'integer'])
    );

`whereType` メソッドと `whereAllType` メソッドは、`string`、`integer`、`double`、`boolean`、`array`、および `null` のタイプを認識します。

<a name="testing-file-uploads"></a>
## ファイルのアップロードのテスト (Testing File Uploads)

`Illuminate\Http\UploadedFile` クラスは、テスト用のダミー ファイルまたはイメージを生成するために使用できる `fake` メソッドを提供します。これを `Storage` ファサードの `fake` メソッドと組み合わせると、ファイル アップロードのテストが大幅に簡素化されます。たとえば、次の 2 つの機能を組み合わせて、アバター アップロード フォームを簡単にテストできます。

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

特定のファイルが存在しないことを主張したい場合は、`Storage` ファサードによって提供される `assertMissing` メソッドを使用できます。

    Storage::fake('avatars');

    // ...

    Storage::disk('avatars')->assertMissing('missing.jpg');

<a name="fake-file-customization"></a>
#### 偽ファイルのカスタマイズ

`UploadedFile` クラスによって提供される `fake` メソッドを使用してファイルを作成する場合、アプリケーションの検証ルールをより適切にテストするために、画像の幅、高さ、サイズ (キロバイト単位) を指定できます。

    UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);

イメージの作成に加えて、`create` メソッドを使用して他のタイプのファイルを作成することもできます。

    UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);

必要に応じて、`$mimeType` 引数をメソッドに渡して、ファイルによって返される MIME タイプを明示的に定義できます。

    UploadedFile::fake()->create(
        'document.pdf', $sizeInKilobytes, 'application/pdf'
    );

<a name="testing-views"></a>
## ビューのテスト (Testing Views)

Laravel では、アプリケーションに対してシミュレートされた HTTP リクエストを行わずにビューをレンダリングすることもできます。これを実現するには、テスト内で `view` メソッドを呼び出すことができます。 `view` メソッドは、ビュー名とオプションのデータ配列を受け入れます。このメソッドは `Illuminate\Testing\TestView` のインスタンスを返します。これは、ビューのコンテンツについて簡単にアサーションを行うためのいくつかのメソッドを提供します。

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

`TestView` クラスは、`assertSee`、`assertSeeInOrder`、`assertSeeText`、`assertSeeTextInOrder`、`assertDontSee`、および `assertDontSeeText` のアサーション メソッドを提供します。

必要に応じて、`TestView` インスタンスを文字列にキャストすることで、生のレンダリングされたビューのコンテンツを取得できます。

    $contents = (string) $this->view('welcome');

<a name="sharing-errors"></a>
#### 共有エラー

一部のビューは、[Laravelが提供するグローバルエラーバッグ](/docs/{{version}}/validation#quick-displaying-the-validation-errors) で共有されたエラーに依存する場合があります。エラー バッグにエラー メッセージを追加するには、`withViewErrors` メソッドを使用します。

    $view = $this->withViewErrors([
        'name' => ['Please provide a valid name.']
    ])->view('form');

    $view->assertSee('Please provide a valid name.');

<a name="rendering-blade-and-components"></a>
### レンダリングBladeとコンポーネント

必要に応じて、`blade` メソッドを使用して、生の [Blade](/docs/{{version}}/blade) 文字列を評価およびレンダリングできます。 `view` メソッドと同様に、`blade` メソッドは `Illuminate\Testing\TestView` のインスタンスを返します。

    $view = $this->blade(
        '<x-component :name="$name" />',
        ['name' => 'Taylor']
    );

    $view->assertSee('Taylor');

`component` メソッドを使用して、[Blade コンポーネント](/docs/{{version}}/blade#components) を評価およびレンダリングできます。 `component` メソッドは、`Illuminate\Testing\TestComponent` のインスタンスを返します。

    $view = $this->component(Profile::class, ['name' => 'Taylor']);

    $view->assertSee('Taylor');

<a name="available-assertions"></a>
## 利用可能なアサーション (Available Assertions)

<a name="response-assertions"></a>
### 応答アサーション

Laravel の `Illuminate\Testing\TestResponse` クラスは、アプリケーションのテスト時に利用できるさまざまなカスタム アサーション メソッドを提供します。これらのアサーションは、`json`、`get`、`post`、`put`、および `delete` テスト メソッドによって返される応答でアクセスできます。

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

[assertAccepted](#assert-accepted)
[assertBadRequest](#assert-bad-request)
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
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertRequestTimeout](#assert-request-timeout)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertServerError](#assert-server-error)
[assertServiceUnavailable](#assert-server-unavailable)
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

</div>

<a name="assert-bad-request"></a>
#### アサート悪いリクエスト

応答に不正なリクエスト (400) HTTP ステータス コードがあることをアサートします。

    $response->assertBadRequest();

<a name="assert-accepted"></a>
#### アサート受け入れ済み

応答に承認済み (202) HTTP ステータス コードがあることをアサートします。

    $response->assertAccepted();

<a name="assert-conflict"></a>
#### アサート競合

応答に競合 (409) HTTP ステータス コードがあることをアサートします。

    $response->assertConflict();

<a name="assert-cookie"></a>
#### アサートクッキー

応答に指定された Cookie が含まれていることをアサートします。

    $response->assertCookie($cookieName, $value = null);

<a name="assert-cookie-expired"></a>
#### アサートCookie期限切れ

応答に指定された Cookie が含まれており、有効期限が切れていることをアサートします。

    $response->assertCookieExpired($cookieName);

<a name="assert-cookie-not-expired"></a>
#### アサートCookieNotExpired

応答に指定された Cookie が含まれており、有効期限が切れていないことをアサートします。

    $response->assertCookieNotExpired($cookieName);

<a name="assert-cookie-missing"></a>
#### アサートクッキーがありません

応答に指定された Cookie が含まれていないことをアサートします。

    $response->assertCookieMissing($cookieName);

<a name="assert-created"></a>
#### アサート作成されました

応答に 201 HTTP ステータス コードがあることをアサートします。

    $response->assertCreated();

<a name="assert-dont-see"></a>
#### 主張しないでください

指定された文字列がアプリケーションから返された応答に含まれていないことをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。

    $response->assertDontSee($value, $escaped = true);

<a name="assert-dont-see-text"></a>
#### アサートDontSeeText

指定された文字列が応答テキストに含まれていないことをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。このメソッドは、アサーションを行う前に、応答コンテンツを `strip_tags` PHP 関数に渡します。

    $response->assertDontSeeText($value, $escaped = true);

<a name="assert-download"></a>
#### アサートダウンロード

応答が「ダウンロード」であることをアサートします。通常、これは、応答を返した呼び出されたルートが `Response::download` 応答、`BinaryFileResponse`、または `Storage::download` 応答を返したことを意味します。

    $response->assertDownload();

必要に応じて、ダウンロード可能なファイルに特定のファイル名が割り当てられていることを主張できます。

    $response->assertDownload('image.jpg');

<a name="assert-exact-json"></a>
#### アサートExactJson

応答に指定された JSON データと完全に一致するものが含まれていることをアサートします。

    $response->assertExactJson(array $data);

<a name="assert-exact-json-structure"></a>
#### アサート正確なJson構造

指定された JSON 構造と完全に一致するものが応答に含まれていることをアサートします。

    $response->assertExactJsonStructure(array $data);

このメソッドは、[assertJsonStructure](#assert-json-structure) のより厳密な変形です。 `assertJsonStructure` とは対照的に、このメソッドは、予期される JSON 構造に明示的に含まれていないキーが応答に含まれている場合に失敗します。

<a name="assert-forbidden"></a>
#### アサート禁止

応答に禁止された (403) HTTP ステータス コードがあることをアサートします。

    $response->assertForbidden();

<a name="assert-found"></a>
#### アサート見つかりました

応答に見つかった (302) HTTP ステータス コードがあることをアサートします。

    $response->assertFound();

<a name="assert-gone"></a>
#### アサートゴーン

応答に、Gone (410) HTTP ステータス コードがあることをアサートします。

    $response->assertGone();

<a name="assert-header"></a>
#### アサートヘッダー

指定されたヘッダーと値が応答に存在することをアサートします。

    $response->assertHeader($headerName, $value = null);

<a name="assert-header-missing"></a>
#### アサートヘッダーがありません

指定されたヘッダーが応答に存在しないことをアサートします。

    $response->assertHeaderMissing($headerName);

<a name="assert-internal-server-error"></a>
#### アサート内部サーバーエラー

応答に「内部サーバー エラー」(500) HTTP ステータス コードがあることをアサートします。

    $response->assertInternalServerError();

<a name="assert-json"></a>
#### アサートJson

応答に指定された JSON データが含まれていることをアサートします。

    $response->assertJson(array $data, $strict = false);

`assertJson` メソッドは、応答を配列に変換して、アプリケーションから返された JSON 応答内に指定された配列が存在することを確認します。したがって、JSON 応答に他のプロパティがある場合でも、指定されたフラグメントが存在する限り、このテストは合格します。

<a name="assert-json-count"></a>
#### アサートJsonCount

応答 JSON に、指定されたキーで予想される数の項目を含む配列があることをアサートします。

    $response->assertJsonCount($count, $key = null);

<a name="assert-json-fragment"></a>
#### アサートJsonFragment

応答の任意の場所に指定された JSON データが含まれていることをアサートします。

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

<a name="assert-json-is-array"></a>
#### アサートJsonIsArray

応答 JSON が配列であることをアサートします。

    $response->assertJsonIsArray();

<a name="assert-json-is-object"></a>
#### assertJsonIsObject

応答 JSON がオブジェクトであることをアサートします。

    $response->assertJsonIsObject();

<a name="assert-json-missing"></a>
#### アサートJsonMissing

応答に指定された JSON データが含まれていないことをアサートします。

    $response->assertJsonMissing(array $data);

<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

応答に正確な JSON データが含まれていないことをアサートします。

    $response->assertJsonMissingExact(array $data);

<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

指定されたキーに対する応答に JSON 検証エラーがないことをアサートします。

    $response->assertJsonMissingValidationErrors($keys);

> [!NOTE]  
> より汎用的な [assertValid](#assert-valid) メソッドを使用すると、応答に JSON として返された検証エラーがないこと、**およびセッション ストレージにフラッシュされたエラーがないこと**を主張できます。

<a name="assert-json-path"></a>
#### アサートJsonPath

応答に指定されたパスにある指定されたデータが含まれていることをアサートします。

    $response->assertJsonPath($path, $expectedValue);

たとえば、アプリケーションから次の JSON 応答が返されたとします。

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

次のように、`user` オブジェクトの `name` プロパティが指定された値と一致すると主張できます。

    $response->assertJsonPath('user.name', 'Steve Schoger');

<a name="assert-json-missing-path"></a>
#### アサートJsonMissingPath

応答に指定されたパスが含まれていないことをアサートします。

    $response->assertJsonMissingPath($path);

たとえば、アプリケーションから次の JSON 応答が返されたとします。

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

`user` オブジェクトの `email` プロパティが含まれていないと主張することもできます。

    $response->assertJsonMissingPath('user.email');

<a name="assert-json-structure"></a>
#### アサートJson構造

応答が指定された JSON 構造を持つことをアサートします。

    $response->assertJsonStructure(array $structure);

たとえば、アプリケーションから返された JSON 応答に次のデータが含まれているとします。

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```

次のように、JSON 構造が期待どおりであると主張できます。

    $response->assertJsonStructure([
        'user' => [
            'name',
        ]
    ]);

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

この状況では、`*` 文字を使用して、配列内のすべてのオブジェクトの構造に対してアサートできます。

    $response->assertJsonStructure([
        'user' => [
            '*' => [
                 'name',
                 'age',
                 'location'
            ]
        ]
    ]);

<a name="assert-json-validation-errors"></a>
#### アサートJsonValidationErrors

応答に指定されたキーに対して指定された JSON 検証エラーがあることをアサートします。このメソッドは、検証エラーがセッションにフラッシュされるのではなく JSON 構造として返される応答に対してアサートするときに使用する必要があります。

    $response->assertJsonValidationErrors(array $data, $responseKey = 'errors');

> [!NOTE]  
> より汎用的な [assertInvalid](#assert-invalid) メソッドを使用すると、応答に検証エラーが JSON として返されたことを主張する ** または ** エラーがセッション ストレージにフラッシュされたことを主張できます。

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

応答に指定されたキーの JSON 検証エラーがあることをアサートします。

    $response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');

<a name="assert-method-not-allowed"></a>
#### アサートメソッドが許可されていません

応答に許可されていないメソッド (405) HTTP ステータス コードがあることをアサートします。

    $response->assertMethodNotAllowed();

<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

応答に完全に移動された (301) HTTP ステータス コードがあることをアサートします。

    $response->assertMovedPermanently();

<a name="assert-location"></a>
#### アサート場所

応答の `Location` ヘッダーに指定された URI 値があることをアサートします。

    $response->assertLocation($uri);

<a name="assert-content"></a>
#### アサートコンテンツ

指定された文字列が応答の内容と一致することをアサートします。

    $response->assertContent($value);

<a name="assert-no-content"></a>
#### アサートNoContent

応答に指定された HTTP ステータス コードがあり、内容が含まれていないことをアサートします。

    $response->assertNoContent($status = 204);

<a name="assert-streamed"></a>
#### アサートストリーミング

応答がストリーミング応答であることをアサートします。

    $response->assertStreamed();

<a name="assert-streamed-content"></a>
#### アサートストリームコンテンツ

指定された文字列がストリーミングされた応答コンテンツと一致することをアサートします。

    $response->assertStreamedContent($value);

<a name="assert-not-found"></a>
#### アサートが見つかりませんでした

応答に not found (404) HTTP ステータス コードがあることをアサートします。

    $response->assertNotFound();

<a name="assert-ok"></a>
#### アサートOK

応答に 200 HTTP ステータス コードがあることをアサートします。

    $response->assertOk();

<a name="assert-payment-required"></a>
#### アサート支払い必須

応答に支払いが必要な (402) HTTP ステータス コードがあることをアサートします。

    $response->assertPaymentRequired();

<a name="assert-plain-cookie"></a>
#### アサートプレーンクッキー

応答に指定された暗号化されていない Cookie が含まれていることをアサートします。

    $response->assertPlainCookie($cookieName, $value = null);

<a name="assert-redirect"></a>
#### アサートリダイレクト

応答が指定された URI へのリダイレクトであることをアサートします。

    $response->assertRedirect($uri = null);

<a name="assert-redirect-contains"></a>
#### assertRedirectContains

応答が指定された文字列を含む URI にリダイレクトされているかどうかを確認します。

    $response->assertRedirectContains($string);

<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

応答が指定された [名前付きルート](/docs/{{version}}/routing#named-routes) へのリダイレクトであることをアサートします。

    $response->assertRedirectToRoute($name, $parameters = []);

<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

応答が指定された [署名されたルート](/docs/{{version}}/urls#signed-urls) へのリダイレクトであることをアサートします。

    $response->assertRedirectToSignedRoute($name = null, $parameters = []);

<a name="assert-request-timeout"></a>
#### アサートリクエストタイムアウト

応答にリクエスト タイムアウト (408) HTTP ステータス コードがあることをアサートします。

    $response->assertRequestTimeout();

<a name="assert-see"></a>
#### アサートを参照

指定された文字列が応答内に含まれていることをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。

    $response->assertSee($value, $escaped = true);

<a name="assert-see-in-order"></a>
#### アサートSeeInOrder

指定された文字列が応答内に順番に含まれていることをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。

    $response->assertSeeInOrder(array $values, $escaped = true);

<a name="assert-see-text"></a>
#### アサート参照テキスト

指定された文字列が応答テキストに含まれていることをアサートします。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。応答コンテンツは、アサーションが行われる前に `strip_tags` PHP 関数に渡されます。

    $response->assertSeeText($value, $escaped = true);

<a name="assert-see-text-in-order"></a>
#### アサートSeeTextInOrder

指定された文字列が応答テキスト内に順番に含まれていることを確認します。このアサーションは、`false` の 2 番目の引数を渡さない限り、指定された文字列を自動的にエスケープします。応答コンテンツは、アサーションが行われる前に `strip_tags` PHP 関数に渡されます。

    $response->assertSeeTextInOrder(array $values, $escaped = true);

<a name="assert-server-error"></a>
#### アサートサーバーエラー

応答にサーバー エラー (>= 500 、< 600) HTTP ステータス コードがあることをアサートします。

    $response->assertServerError();

<a name="assert-server-unavailable"></a>
#### アサートサービスが利用できません

応答に「Service Unavailable」(503) HTTP ステータス コードがあることをアサートします。

    $response->assertServiceUnavailable();

<a name="assert-session-has"></a>
#### アサートセッションが持っています

セッションに指定されたデータが含まれていることをアサートします。

    $response->assertSessionHas($key, $value = null);

必要に応じて、`assertSessionHas` メソッドの 2 番目の引数としてクロージャーを提供できます。クロージャが `true` を返す場合、アサーションは合格します。

    $response->assertSessionHas($key, function (User $value) {
        return $value->name === 'Taylor Otwell';
    });

<a name="assert-session-has-input"></a>
#### assertSessionHasInput

セッションの [フラッシュ入力アレイ](/docs/{{version}}/responses#redirecting-with-flashed-session-data) に指定された値があることをアサートします。

    $response->assertSessionHasInput($key, $value = null);

必要に応じて、`assertSessionHasInput` メソッドの 2 番目の引数としてクロージャーを提供できます。クロージャが `true` を返す場合、アサーションは合格します。

    use Illuminate\Support\Facades\Crypt;

    $response->assertSessionHasInput($key, function (string $value) {
        return Crypt::decryptString($value) === 'secret';
    });

<a name="assert-session-has-all"></a>
#### assertSessionHasAll

セッションにキーと値のペアの指定された配列が含まれていることをアサートします。

    $response->assertSessionHasAll(array $data);

たとえば、アプリケーションのセッションに `name` キーと `status` キーが含まれている場合、次のように両方が存在し、指定された値を持つことをアサートできます。

    $response->assertSessionHasAll([
        'name' => 'Taylor Otwell',
        'status' => 'active',
    ]);

<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

セッションに指定された `$keys` のエラーが含まれていることをアサートします。 `$keys` が連想配列の場合、セッションに各フィールド (キー) に特定のエラー メッセージ (値) が含まれていることをアサートします。このメソッドは、検証エラーを JSON 構造として返すのではなく、セッションにフラッシュするルートをテストするときに使用する必要があります。

    $response->assertSessionHasErrors(
        array $keys = [], $format = null, $errorBag = 'default'
    );

たとえば、`name` フィールドと `email` フィールドにセッションにフラッシュされた検証エラー メッセージがあることを主張するには、次のように `assertSessionHasErrors` メソッドを呼び出すことができます。

    $response->assertSessionHasErrors(['name', 'email']);

または、特定のフィールドに特定の検証エラー メッセージがあると主張することもできます。

    $response->assertSessionHasErrors([
        'name' => 'The given name was invalid.'
    ]);

> [!NOTE]  
> より汎用的な [assertInvalid](#assert-invalid) メソッドを使用すると、応答に検証エラーが JSON として返されたことを主張する ** または ** エラーがセッション ストレージにフラッシュされたことを主張できます。

<a name="assert-session-has-errors-in"></a>
#### アサートセッションにエラーが発生しました

セッションに特定の [エラーバッグ](/docs/{{version}}/validation#named-error-bags) 内の指定された `$keys` のエラーが含まれていることをアサートします。 `$keys` が連想配列の場合、セッションのエラー バッグ内に各フィールド (キー) に特定のエラー メッセージ (値) が含まれていることをアサートします。

    $response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);

<a name="assert-session-has-no-errors"></a>
#### assertSessionHasNoErrors

セッションに検証エラーがないことをアサートします。

    $response->assertSessionHasNoErrors();

<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

セッションに指定されたキーの検証エラーがないことをアサートします。

    $response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');

> [!NOTE]  
> より汎用的な [assertValid](#assert-valid) メソッドを使用すると、応答に JSON として返された検証エラーがないこと、**およびセッション ストレージにフラッシュされたエラーがないこと**を主張できます。

<a name="assert-session-missing"></a>
#### アサートセッションが見つかりません

セッションに指定されたキーが含まれていないことをアサートします。

    $response->assertSessionMissing($key);

<a name="assert-status"></a>
#### アサートステータス

応答に指定された HTTP ステータス コードがあることをアサートします。

    $response->assertStatus($code);

<a name="assert-successful"></a>
#### アサート成功

応答に成功 (>= 200 および < 300) HTTP ステータス コードがあることをアサートします。

    $response->assertSuccessful();

<a name="assert-too-many-requests"></a>
#### アサートが多すぎるリクエスト

応答に多すぎるリクエスト (429) HTTP ステータス コードがあることをアサートします。

    $response->assertTooManyRequests();

<a name="assert-unauthorized"></a>
#### アサート未承認

応答に未承認 (401) HTTP ステータス コードがあることをアサートします。

    $response->assertUnauthorized();

<a name="assert-unprocessable"></a>
#### アサート処理不能

応答に処理できないエンティティ (422) HTTP ステータス コードがあることをアサートします。

    $response->assertUnprocessable();

<a name="assert-unsupported-media-type"></a>
#### アサートUnsupportedMediaType

応答にサポートされていないメディア タイプ (415) HTTP ステータス コードがあることをアサートします。

    $response->assertUnsupportedMediaType();

<a name="assert-valid"></a>
#### アサート有効

応答に指定されたキーの検証エラーがないことをアサートします。このメソッドは、検証エラーが JSON 構造として返される場合、または検証エラーがセッションにフラッシュされた場合の応答に対するアサートに使用できます。

    // Assert that no validation errors are present...
    $response->assertValid();

    // Assert that the given keys do not have validation errors...
    $response->assertValid(['name', 'email']);

<a name="assert-invalid"></a>
#### アサート無効

応答に指定されたキーの検証エラーがあることをアサートします。このメソッドは、検証エラーが JSON 構造として返される場合、または検証エラーがセッションにフラッシュされた場合の応答に対するアサートに使用できます。

    $response->assertInvalid(['name', 'email']);

特定のキーに特定の検証エラー メッセージがあると主張することもできます。その際、メッセージ全体を提供することも、メッセージの一部だけを提供することもできます。

    $response->assertInvalid([
        'name' => 'The name field is required.',
        'email' => 'valid email address',
    ]);

<a name="assert-view-has"></a>
#### アサートビューがあります

応答ビューに指定されたデータが含まれていることをアサートします。

    $response->assertViewHas($key, $value = null);

`assertViewHas` メソッドの 2 番目の引数としてクロージャを渡すと、ビュー データの特定の部分を検査してアサーションを行うことができます。

    $response->assertViewHas('user', function (User $user) {
        return $user->name === 'Taylor';
    });

さらに、ビュー データは応答の配列変数としてアクセスできるため、簡単に検査できます。

```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```

<a name="assert-view-has-all"></a>
#### アサートビューにはすべてがあります

応答ビューに指定されたデータのリストがあることをアサートします。

    $response->assertViewHasAll(array $data);

このメソッドは、ビューに単に指定されたキーに一致するデータが含まれていることをアサートするために使用できます。

    $response->assertViewHasAll([
        'name',
        'email',
    ]);

または、ビュー データが存在し、特定の値を持っていると主張することもできます。

    $response->assertViewHasAll([
        'name' => 'Taylor Otwell',
        'email' => 'taylor@example.com,',
    ]);

<a name="assert-view-is"></a>
#### アサートビューIs

指定されたビューがルートによって返されたことをアサートします。

    $response->assertViewIs($value);

<a name="assert-view-missing"></a>
#### アサートビューがありません

指定されたデータ キーがアプリケーションの応答で返されたビューで使用可能になっていないことをアサートします。

    $response->assertViewMissing($key);

<a name="authentication-assertions"></a>
### 認証アサーション

Laravel は、アプリケーションの機能テスト内で利用できるさまざまな認証関連のアサーションも提供します。これらのメソッドは、`get` や `post` などのメソッドによって返される `Illuminate\Testing\TestResponse` インスタンスではなく、テスト クラス自体で呼び出されることに注意してください。

<a name="assert-authenticated"></a>
#### 認証済み

ユーザーが認証されていることをアサートします。

    $this->assertAuthenticated($guard = null);

<a name="assert-guest"></a>
#### アサートゲスト

ユーザーが認証されていないことをアサートします。

    $this->assertGuest($guard = null);

<a name="assert-authenticated-as"></a>
#### 認証済みとしてアサート

特定のユーザーが認証されていることをアサートします。

    $this->assertAuthenticatedAs($user, $guard = null);

<a name="validation-assertions"></a>
## 検証アサーション (Validation Assertions)

Laravel は、リクエストで提供されたデータが有効か無効かを確認するために使用できる 2 つの主要な検証関連アサーションを提供します。

<a name="validation-assert-valid"></a>
#### アサート有効

応答に指定されたキーの検証エラーがないことをアサートします。このメソッドは、検証エラーが JSON 構造として返される場合、または検証エラーがセッションにフラッシュされた場合の応答に対するアサートに使用できます。

    // Assert that no validation errors are present...
    $response->assertValid();

    // Assert that the given keys do not have validation errors...
    $response->assertValid(['name', 'email']);

<a name="validation-assert-invalid"></a>
#### アサート無効

応答に指定されたキーの検証エラーがあることをアサートします。このメソッドは、検証エラーが JSON 構造として返される場合、または検証エラーがセッションにフラッシュされた場合の応答に対するアサートに使用できます。

    $response->assertInvalid(['name', 'email']);

特定のキーに特定の検証エラー メッセージがあると主張することもできます。その際、メッセージ全体を提供することも、メッセージの一部だけを提供することもできます。

    $response->assertInvalid([
        'name' => 'The name field is required.',
        'email' => 'valid email address',
    ]);

