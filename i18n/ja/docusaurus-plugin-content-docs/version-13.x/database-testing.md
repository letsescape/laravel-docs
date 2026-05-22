# データベースのテスト (Database Testing)

- [Introduction](#introduction)
    - [各テスト後のデータベースのリセット](#resetting-the-database-after-each-test)
- [モデルファクトリー](#model-factories)
- [シーダーの実行](#running-seeders)
- [利用可能なアサーション](#available-assertions)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、データベース駆動型アプリケーションのテストを容易にするさまざまな便利なツールとアサーションを提供します。さらに、Laravel モデル ファクトリとシーダーにより、アプリケーションの Eloquent モデルとリレーションシップを使用してテスト データベース レコードを簡単に作成できます。これらの強力な機能については、次のドキュメントで説明します。

<a name="resetting-the-database-after-each-test"></a>
### 各テスト後のデータベースのリセット

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

スキーマが最新の場合、`Illuminate\Foundation\Testing\RefreshDatabase` トレイトはデータベースを移行しません。代わりに、データベース トランザクション内でのみテストが実行されます。したがって、この特性を使用しないテスト ケースによってデータベースに追加されたレコードは、データベース内にまだ存在する可能性があります。

データベースを完全にリセットしたい場合は、代わりに `Illuminate\Foundation\Testing\DatabaseMigrations` または `Illuminate\Foundation\Testing\DatabaseTruncation` 特性を使用できます。ただし、これらのオプションは両方とも、`RefreshDatabase` 特性よりも大幅に遅くなります。

<a name="model-factories"></a>
## モデルファクトリー (Model Factories)

テストする場合、テストを実行する前にデータベースにいくつかのレコードを挿入する必要がある場合があります。このテストデータを作成するときに各列の値を手動で指定する代わりに、Laravel では、[モデル工場](/docs/{{version}}/eloquent) を使用して、[Eloquent モデル](/docs/{{version}}/eloquent-factories) ごとにデフォルト属性のセットを定義できます。

モデルを作成するためのモデル ファクトリの作成と利用の詳細については、完全な [モデルファクトリーのドキュメント](/docs/{{version}}/eloquent-factories) を参照してください。モデル ファクトリを定義したら、テスト内でそのファクトリを利用してモデルを作成できます。

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
## シーダーの実行 (Running Seeders)

機能テスト中に [データベースシーダー](/docs/{{version}}/seeding) を使用してデータベースにデータを入力する場合は、`seed` メソッドを呼び出すことができます。デフォルトでは、`seed` メソッドは `DatabaseSeeder` を実行し、これにより他のすべてのシーダーが実行されます。あるいは、特定のシーダー クラス名を `seed` メソッドに渡します。

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

あるいは、`RefreshDatabase` トレイトを使用する各テストの前にデータベースを自動的にシードするように Laravel に指示することもできます。これは、基本テスト クラスに `Seed` 属性を追加することで実現できます。

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\Attributes\Seed;
use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

#[Seed]
abstract class TestCase extends BaseTestCase
{
}
```

`Seed` 属性が存在する場合、テストは `RefreshDatabase` 特性を使用する各テストの前に `Database\Seeders\DatabaseSeeder` クラスを実行します。ただし、テスト クラスの `Seeder` 属性を使用して、実行する特定のシーダーを指定することもできます。

```php
<?php

namespace Tests\Feature;

use Database\Seeders\OrderStatusSeeder;
use Illuminate\Foundation\Testing\Attributes\Seeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

#[Seeder(OrderStatusSeeder::class)]
class OrderTest extends TestCase
{
    use RefreshDatabase;

    // ...
}
```

<a name="available-assertions"></a>
## 利用可能なアサーション (Available Assertions)

Laravel は、[Pest](https://pestphp.com) または [PHPUnit](https://phpunit.de) 機能テスト用にいくつかのデータベース アサーションを提供します。これらの各主張については、以下で説明します。

<a name="assert-database-count"></a>
#### アサートデータベース数

データベース内のテーブルに指定された数のレコードが含まれていることをアサートします。

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### アサートデータベース空

データベース内のテーブルにレコードが含まれていないことをアサートします。

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### データベースにアサートがある

データベース内のテーブルに、指定されたキー/値クエリ制約に一致するレコードが含まれていることをアサートします。

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### アサートデータベースが見つかりません

データベース内のテーブルに、指定されたキー/値クエリ制約に一致するレコードが含まれていないことをアサートします。

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### アサートソフト削除済み

`assertSoftDeleted` メソッドは、特定の Eloquent モデルが「論理的に削除された」ことをアサートするために使用できます。

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### アサートノットソフト削除済み

`assertNotSoftDeleted` メソッドは、特定の Eloquent モデルが「論理的に削除」されていないことをアサートするために使用できます。

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

指定されたモデルまたはモデルのコレクションがデータベースに存在することをアサートします。

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### アサートモデルが見つかりません

指定されたモデルまたはモデルのコレクションがデータベースに存在しないことをアサートします。

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### ExpectsDatabaseQueryCount

`expectsDatabaseQueryCount` メソッドは、テスト中に実行されることが予想されるデータベース クエリの総数を指定するために、テストの開始時に呼び出すことができます。実際に実行されたクエリの数がこの予想と正確に一致しない場合、テストは失敗します。

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```

