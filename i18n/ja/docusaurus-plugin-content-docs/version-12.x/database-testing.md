<!-- # Database Testing -->
# Database Testing

- [Introduction](#introduction)
    - [Resetting the Database After Each Test](#resetting-the-database-after-each-test)
- [Model Factories](#model-factories)
- [Running Seeders](#running-seeders)
- [Available Assertions](#available-assertions)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a variety of helpful tools and assertions to make it easier to test your database driven applications. In addition, Laravel model factories and seeders make it painless to create test database records using your application's Eloquent models and relationships. We'll discuss all of these powerful features in the following documentation. -->
Laravel は、データベース駆動型アプリケーションのテストを容易にするさまざまな便利なツールとアサーションを提供します。さらに、Laravel モデル ファクトリとシーダーにより、アプリケーションの Eloquent モデルとリレーションシップを使用してテスト データベース レコードを簡単に作成できます。これらの強力な機能については、次のドキュメントで説明します。

<a name="resetting-the-database-after-each-test"></a>
<!-- ### Resetting the Database After Each Test -->
### Resetting the Database After Each Test

<!-- Before proceeding much further, let's discuss how to reset your database after each of your tests so that data from a previous test does not interfere with subsequent tests. Laravel's included `Illuminate\Foundation\Testing\RefreshDatabase` trait will take care of this for you. Simply use the trait on your test class: -->
さらに先に進む前に、前のテストのデータが後続のテストに干渉しないように、各テストの後にデータベースをリセットする方法について説明します。 Laravel に含まれる `Illuminate\Foundation\Testing\RefreshDatabase` トレイトがこれを処理します。テストクラスでトレイトを使用するだけです。

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('basic example', function () {
    $response = $this->get('/');

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        $response = $this->get('/');

        // ...
    }
}
```

<!-- The `Illuminate\Foundation\Testing\RefreshDatabase` trait does not migrate your database if your schema is up to date. Instead, it will only execute the test within a database transaction. Therefore, any records added to the database by test cases that do not use this trait may still exist in the database. -->
スキーマが最新の場合、`Illuminate\Foundation\Testing\RefreshDatabase` トレイトはデータベースを移行しません。代わりに、データベース トランザクション内でのみテストが実行されます。したがって、この特性を使用しないテスト ケースによってデータベースに追加されたレコードは、データベース内にまだ存在する可能性があります。

<!-- If you would like to totally reset the database, you may use the `Illuminate\Foundation\Testing\DatabaseMigrations` or `Illuminate\Foundation\Testing\DatabaseTruncation` traits instead. However, both of these options are significantly slower than the `RefreshDatabase` trait. -->
データベースを完全にリセットしたい場合は、代わりに `Illuminate\Foundation\Testing\DatabaseMigrations` または `Illuminate\Foundation\Testing\DatabaseTruncation` 特性を使用できます。ただし、これらのオプションは両方とも、`RefreshDatabase` 特性よりも大幅に遅くなります。

<a name="model-factories"></a>
<!-- ## Model Factories -->
## Model Factories

<!-- When testing, you may need to insert a few records into your database before executing your test. Instead of manually specifying the value of each column when you create this test data, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/12.x/eloquent) using [model factories](/docs/12.x/eloquent-factories). -->
テストする場合、テストを実行する前にデータベースにいくつかのレコードを挿入する必要がある場合があります。このテストデータを作成するときに各列の値を手動で指定する代わりに、Laravel では、[Eloquent models](/docs/12.x/eloquent-factories) を使用して、[model factories](/docs/12.x/eloquent) ごとにデフォルト属性のセットを定義できます。

<!-- To learn more about creating and utilizing model factories to create models, please consult the complete [model factory documentation](/docs/12.x/eloquent-factories). Once you have defined a model factory, you may utilize the factory within your test to create models: -->
モデルを作成するためのモデル ファクトリの作成と利用の詳細については、完全な [model factory documentation](/docs/12.x/eloquent-factories) を参照してください。モデル ファクトリを定義したら、テスト内でそのファクトリを利用してモデルを作成できます。

```php tab=Pest
use App\Models\User;

test('models can be instantiated', function () {
    $user = User::factory()->create();

    // ...
});
```

```php tab=PHPUnit
use App\Models\User;

public function test_models_can_be_instantiated(): void
{
    $user = User::factory()->create();

    // ...
}
```

<a name="running-seeders"></a>
<!-- ## Running Seeders -->
## Running Seeders

<!-- If you would like to use [database seeders](/docs/12.x/seeding) to populate your database during a feature test, you may invoke the `seed` method. By default, the `seed` method will execute the `DatabaseSeeder`, which should execute all of your other seeders. Alternatively, you pass a specific seeder class name to the `seed` method: -->
機能テスト中に [database seeders](/docs/12.x/seeding) を使用してデータベースにデータを入力する場合は、`seed` メソッドを呼び出すことができます。デフォルトでは、`seed` メソッドは `DatabaseSeeder` を実行し、これにより他のすべてのシーダーが実行されます。あるいは、特定のシーダー クラス名を `seed` メソッドに渡します。

```php tab=Pest
<?php

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('orders can be created', function () {
    // Run the DatabaseSeeder...
    $this->seed();

    // Run a specific seeder...
    $this->seed(OrderStatusSeeder::class);

    // ...

    // Run an array of specific seeders...
    $this->seed([
        OrderStatusSeeder::class,
        TransactionStatusSeeder::class,
        // ...
    ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * Test creating a new order.
     */
    public function test_orders_can_be_created(): void
    {
        // Run the DatabaseSeeder...
        $this->seed();

        // Run a specific seeder...
        $this->seed(OrderStatusSeeder::class);

        // ...

        // Run an array of specific seeders...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

<!-- Alternatively, you may instruct Laravel to automatically seed the database before each test that uses the `RefreshDatabase` trait. You may accomplish this by defining a `$seed` property on your base test class: -->
あるいは、`RefreshDatabase` トレイトを使用する各テストの前にデータベースを自動的にシードするように Laravel に指示することもできます。これを行うには、基本テスト クラスで `$seed` プロパティを定義します。

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    /**
     * Indicates whether the default seeder should run before each test.
     *
     * @var bool
     */
    protected $seed = true;
}
```

<!-- When the `$seed` property is `true`, the test will run the `Database\Seeders\DatabaseSeeder` class before each test that uses the `RefreshDatabase` trait. However, you may specify a specific seeder that should be executed by defining a `$seeder` property on your test class: -->
`$seed` プロパティが `true` の場合、テストは `RefreshDatabase` トレイトを使用する各テストの前に `Database\Seeders\DatabaseSeeder` クラスを実行します。ただし、テスト クラスで `$seeder` プロパティを定義することで、実行する特定のシーダーを指定できます。

```php
use Database\Seeders\OrderStatusSeeder;

/**
 * Run a specific seeder before each test.
 *
 * @var string
 */
protected $seeder = OrderStatusSeeder::class;
```

<a name="available-assertions"></a>
<!-- ## Available Assertions -->
## Available Assertions

<!-- Laravel provides several database assertions for your [Pest](https://pestphp.com) or [PHPUnit](https://phpunit.de) feature tests. We'll discuss each of these assertions below. -->
Laravel は、[Pest](https://pestphp.com) または [PHPUnit](https://phpunit.de) 機能テスト用にいくつかのデータベース アサーションを提供します。これらの各主張については、以下で説明します。

<a name="assert-database-count"></a>
<!-- #### assertDatabaseCount -->
#### assertDatabaseCount

<!-- Assert that a table in the database contains the given number of records: -->
データベース内のテーブルに指定された数のレコードが含まれていることをアサートします。

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
<!-- #### assertDatabaseEmpty -->
#### assertDatabaseEmpty

<!-- Assert that a table in the database contains no records: -->
データベース内のテーブルにレコードが含まれていないことをアサートします。

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
<!-- #### assertDatabaseHas -->
#### assertDatabaseHas

<!-- Assert that a table in the database contains records matching the given key / value query constraints: -->
データベース内のテーブルに、指定されたキー/値クエリ制約に一致するレコードが含まれていることをアサートします。

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
<!-- #### assertDatabaseMissing -->
#### assertDatabaseMissing

<!-- Assert that a table in the database does not contain records matching the given key / value query constraints: -->
データベース内のテーブルに、指定されたキー/値クエリ制約に一致するレコードが含まれていないことをアサートします。

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
<!-- #### assertSoftDeleted -->
#### assertSoftDeleted

<!-- The `assertSoftDeleted` method may be used to assert a given Eloquent model has been "soft deleted": -->
`assertSoftDeleted` メソッドは、特定の Eloquent モデルが「論理的に削除された」ことをアサートするために使用できます。

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
<!-- #### assertNotSoftDeleted -->
#### assertNotSoftDeleted

<!-- The `assertNotSoftDeleted` method may be used to assert a given Eloquent model hasn't been "soft deleted": -->
`assertNotSoftDeleted` メソッドは、特定の Eloquent モデルが「論理的に削除」されていないことをアサートするために使用できます。

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
<!-- #### assertModelExists -->
#### assertModelExists

<!-- Assert that a given model or collection of models exist in the database: -->
指定されたモデルまたはモデルのコレクションがデータベースに存在することをアサートします。

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
<!-- #### assertModelMissing -->
#### assertModelMissing

<!-- Assert that a given model or collection of models do not exist in the database: -->
指定されたモデルまたはモデルのコレクションがデータベースに存在しないことをアサートします。

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
<!-- #### expectsDatabaseQueryCount -->
#### expectsDatabaseQueryCount

<!-- The `expectsDatabaseQueryCount` method may be invoked at the beginning of your test to specify the total number of database queries that you expect to be run during the test. If the actual number of executed queries does not exactly match this expectation, the test will fail: -->
`expectsDatabaseQueryCount` メソッドは、テスト中に実行されることが予想されるデータベース クエリの総数を指定するために、テストの開始時に呼び出すことができます。実際に実行されたクエリの数がこの予想と正確に一致しない場合、テストは失敗します。

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```

