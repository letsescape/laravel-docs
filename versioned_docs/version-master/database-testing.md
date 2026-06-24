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
Laravel은 데이터베이스 기반 애플리케이션을 더 쉽게 테스트할 수 있도록 다양한 유용한 도구와 어서션을 제공합니다. 또한 Laravel 모델 팩토리와 시더를 사용하면 애플리케이션의 Eloquent 모델과 연관관계를 이용해 테스트용 데이터베이스 레코드를 손쉽게 만들 수 있습니다. 이어지는 문서에서는 이러한 강력한 기능들을 모두 살펴보겠습니다.

<a name="resetting-the-database-after-each-test"></a>
<!-- ### Resetting the Database After Each Test -->
### Resetting the Database After Each Test

<!-- Before proceeding much further, let's discuss how to reset your database after each of your tests so that data from a previous test does not interfere with subsequent tests. Laravel's included `Illuminate\Foundation\Testing\RefreshDatabase` trait will take care of this for you. Simply use the trait on your test class: -->
더 진행하기 전에, 이전 테스트의 데이터가 이후 테스트에 영향을 주지 않도록 각 테스트 후 데이터베이스를 재설정하는 방법을 살펴보겠습니다. Laravel에 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` trait가 이 작업을 처리해 줍니다. 테스트 클래스에서 이 trait를 사용하기만 하면 됩니다.

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
`Illuminate\Foundation\Testing\RefreshDatabase` trait는 스키마가 최신 상태라면 데이터베이스 마이그레이션을 실행하지 않습니다. 대신 테스트를 데이터베이스 트랜잭션 안에서만 실행합니다. 따라서 이 trait를 사용하지 않는 테스트 케이스가 데이터베이스에 추가한 레코드는 여전히 데이터베이스에 남아 있을 수 있습니다.

<!-- If you would like to totally reset the database, you may use the `Illuminate\Foundation\Testing\DatabaseMigrations` or `Illuminate\Foundation\Testing\DatabaseTruncation` traits instead. However, both of these options are significantly slower than the `RefreshDatabase` trait. -->
데이터베이스를 완전히 재설정하고 싶다면 대신 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` trait를 사용할 수 있습니다. 하지만 두 옵션 모두 `RefreshDatabase` trait보다 훨씬 느립니다.

<a name="model-factories"></a>
<!-- ## Model Factories -->
## Model Factories

<!-- When testing, you may need to insert a few records into your database before executing your test. Instead of manually specifying the value of each column when you create this test data, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/master/eloquent) using [model factories](/docs/master/eloquent-factories). -->
테스트를 실행하기 전에 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. 이러한 테스트 데이터를 만들 때 각 컬럼의 값을 직접 지정하는 대신, Laravel에서는 [Eloquent models](/docs/master/eloquent-factories)를 사용하여 각 [model factories](/docs/master/eloquent)에 대한 기본 속성 집합을 정의할 수 있습니다.

<!-- To learn more about creating and utilizing model factories to create models, please consult the complete [model factory documentation](/docs/master/eloquent-factories). Once you have defined a model factory, you may utilize the factory within your test to create models: -->
모델 팩토리를 만들고 이를 활용해 모델을 생성하는 방법을 더 자세히 알아보려면 전체 [model factory documentation](/docs/master/eloquent-factories)를 참고하시기 바랍니다. 모델 팩토리를 정의한 뒤에는 테스트 안에서 팩토리를 사용해 모델을 생성할 수 있습니다.

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

<!-- If you would like to use [database seeders](/docs/master/seeding) to populate your database during a feature test, you may invoke the `seed` method. By default, the `seed` method will execute the `DatabaseSeeder`, which should execute all of your other seeders. Alternatively, you pass a specific seeder class name to the `seed` method: -->
기능 테스트 중에 [database seeders](/docs/master/seeding)를 사용해 데이터베이스를 채우고 싶다면 `seed` 메서드를 호출할 수 있습니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하며, 이 시더는 다른 모든 시더를 실행해야 합니다. 또는 특정 시더 클래스명을 `seed` 메서드에 전달할 수 있습니다.

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

<!-- Alternatively, you may instruct Laravel to automatically seed the database before each test that uses the `RefreshDatabase` trait. You may accomplish this by adding the `Seed` attribute to your base test class: -->
또는 `RefreshDatabase` trait를 사용하는 각 테스트 전에 Laravel이 데이터베이스를 자동으로 시딩하도록 지시할 수 있습니다. 기본 테스트 클래스에 `Seed` 속성을 추가하면 됩니다.

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

<!-- When the `Seed` attribute is present, the test will run the `Database\Seeders\DatabaseSeeder` class before each test that uses the `RefreshDatabase` trait. However, you may specify a specific seeder that should be executed by using the `Seeder` attribute on your test class: -->
`Seed` 속성이 있으면 테스트는 `RefreshDatabase` trait를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스를 실행합니다. 하지만 테스트 클래스에 `Seeder` 속성을 사용하여 실행할 특정 시더를 지정할 수도 있습니다.

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
<!-- ## Available Assertions -->
## Available Assertions

<!-- Laravel provides several database assertions for your [Pest](https://pestphp.com) or [PHPUnit](https://phpunit.de) feature tests. We'll discuss each of these assertions below. -->
Laravel은 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de) 기능 테스트를 위한 여러 데이터베이스 어서션을 제공합니다. 아래에서 각 어서션을 살펴보겠습니다.

<a name="assert-database-count"></a>
<!-- #### assertDatabaseCount -->
#### assertDatabaseCount

<!-- Assert that a table in the database contains the given number of records: -->
데이터베이스의 테이블에 지정한 수의 레코드가 포함되어 있는지 검증합니다.

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
<!-- #### assertDatabaseEmpty -->
#### assertDatabaseEmpty

<!-- Assert that a table in the database contains no records: -->
데이터베이스의 테이블에 레코드가 없는지 검증합니다.

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
<!-- #### assertDatabaseHas -->
#### assertDatabaseHas

<!-- Assert that a table in the database contains records matching the given key / value query constraints: -->
데이터베이스의 테이블에 주어진 키 / 값 쿼리 제약 조건과 일치하는 레코드가 포함되어 있는지 검증합니다.

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
<!-- #### assertDatabaseMissing -->
#### assertDatabaseMissing

<!-- Assert that a table in the database does not contain records matching the given key / value query constraints: -->
데이터베이스의 테이블에 주어진 키 / 값 쿼리 제약 조건과 일치하는 레코드가 포함되어 있지 않은지 검증합니다.

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
<!-- #### assertSoftDeleted -->
#### assertSoftDeleted

<!-- The `assertSoftDeleted` method may be used to assert a given Eloquent model has been "soft deleted": -->
`assertSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제"되었는지 검증하는 데 사용할 수 있습니다.

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
<!-- #### assertNotSoftDeleted -->
#### assertNotSoftDeleted

<!-- The `assertNotSoftDeleted` method may be used to assert a given Eloquent model hasn't been "soft deleted": -->
`assertNotSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제"되지 않았는지 검증하는 데 사용할 수 있습니다.

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
<!-- #### assertModelExists -->
#### assertModelExists

<!-- Assert that a given model or collection of models exist in the database: -->
주어진 모델 또는 모델 컬렉션이 데이터베이스에 존재하는지 검증합니다.

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
<!-- #### assertModelMissing -->
#### assertModelMissing

<!-- Assert that a given model or collection of models do not exist in the database: -->
주어진 모델 또는 모델 컬렉션이 데이터베이스에 존재하지 않는지 검증합니다.

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
`expectsDatabaseQueryCount` 메서드는 테스트 시작 부분에서 호출하여 테스트 중 실행될 것으로 예상하는 데이터베이스 쿼리의 총 개수를 지정할 수 있습니다. 실제 실행된 쿼리 수가 이 예상과 정확히 일치하지 않으면 테스트는 실패합니다.

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```
