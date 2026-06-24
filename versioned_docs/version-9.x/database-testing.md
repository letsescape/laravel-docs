<!-- # Database Testing -->
# Database Testing

- [Introduction](#introduction)
    - [Resetting The Database After Each Test](#resetting-the-database-after-each-test)
- [Model Factories](#model-factories)
- [Running Seeders](#running-seeders)
- [Available Assertions](#available-assertions)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides a variety of helpful tools and assertions to make it easier to test your database driven applications. In addition, Laravel model factories and seeders make it painless to create test database records using your application's Eloquent models and relationships. We'll discuss all of these powerful features in the following documentation. -->
Laravel은 데이터베이스 기반 애플리케이션의 테스트를 더 쉽게 만들어주는 다양한 유용한 도구와 assertion(어설션, 검증 메서드)을 제공합니다. 또한 Laravel의 모델 팩토리와 시더 기능을 활용하면, 여러분의 애플리케이션에서 Eloquent 모델과 연관관계를 사용하여 테스트용 데이터베이스 레코드를 쉽게 만들 수 있습니다. 이 문서에서는 이러한 강력한 기능들을 모두 다룹니다.

<a name="resetting-the-database-after-each-test"></a>
<!-- ### Resetting The Database After Each Test -->
### Resetting The Database After Each Test

<!-- Before proceeding much further, let's discuss how to reset your database after each of your tests so that data from a previous test does not interfere with subsequent tests. Laravel's included `Illuminate\Foundation\Testing\RefreshDatabase` trait will take care of this for you. Simply use the trait on your test class: -->
자세한 내용으로 들어가기 전에, 각 테스트가 끝날 때마다 데이터베이스를 초기화하여 이전 테스트의 데이터가 이후 테스트에 영향을 주지 않도록 처리하는 방법을 먼저 설명합니다. Laravel에 포함된 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트를 사용하면 이 과정을 간단하게 처리할 수 있습니다. 테스트 클래스에서 아래와 같이 해당 트레이트를 사용하세요:

```
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A basic functional test example.
     *
     * @return void
     */
    public function test_basic_example()
    {
        $response = $this->get('/');

        // ...
    }
}
```

<!-- The `Illuminate\Foundation\Testing\RefreshDatabase` trait does not migrate your database if your schema is up to date. Instead, it will only execute the test within a database transaction. Therefore, any records added to the database by test cases that do not use this trait may still exist in the database. -->
`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스의 스키마가 최신 상태라면 마이그레이션을 다시 수행하지 않습니다. 대신 데이터베이스 트랜잭션 내에서 테스트를 실행합니다. 즉, 이 트레이트를 사용하지 않는 테스트 케이스에서 추가된 레코드는 데이터베이스에 남아있을 수 있습니다.

<!-- If you would like to totally reset the database, you may use the `Illuminate\Foundation\Testing\DatabaseMigrations` or `Illuminate\Foundation\Testing\DatabaseTruncation` traits instead. However, both of these options are significantly slower than the `RefreshDatabase` trait. -->
만약 데이터베이스를 완전히 초기 상태로 되돌리고 싶다면, `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 그러나 두 방법 모두 `RefreshDatabase` 트레이트보다는 처리 속도가 훨씬 느립니다.

<a name="model-factories"></a>
<!-- ## Model Factories -->
## Model Factories

<!-- When testing, you may need to insert a few records into your database before executing your test. Instead of manually specifying the value of each column when you create this test data, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/9.x/eloquent) using [model factories](/docs/9.x/eloquent-factories). -->
테스트를 진행할 때 테스트 실행 전에 데이터베이스에 몇 개의 레코드를 삽입해야 할 때가 있습니다. 이때 일일이 각 컬럼의 값을 지정해서 테스트 데이터를 만들 필요 없이, Laravel의 [Eloquent models](/docs/9.x/eloquent-factories)를 이용하면 각 [model factories](/docs/9.x/eloquent)에 대해 기본 속성(attribute) 세트를 미리 정의하여 손쉽게 테스트 데이터를 생성할 수 있습니다.

<!-- To learn more about creating and utilizing model factories to create models, please consult the complete [model factory documentation](/docs/9.x/eloquent-factories). Once you have defined a model factory, you may utilize the factory within your test to create models: -->
모델 팩토리의 생성 및 활용 방법은 [model factory documentation](/docs/9.x/eloquent-factories)를 참고해 주세요. 팩토리를 정의해두었다면, 테스트 내에서 다음과 같이 팩토리를 활용해 모델을 생성할 수 있습니다:

```
use App\Models\User;

public function test_models_can_be_instantiated()
{
    $user = User::factory()->create();

    // ...
}
```

<a name="running-seeders"></a>
<!-- ## Running Seeders -->
## Running Seeders

<!-- If you would like to use [database seeders](/docs/9.x/seeding) to populate your database during a feature test, you may invoke the `seed` method. By default, the `seed` method will execute the `DatabaseSeeder`, which should execute all of your other seeders. Alternatively, you pass a specific seeder class name to the `seed` method: -->
기능 테스트(Feature Test) 도중에 [database seeders](/docs/9.x/seeding)를 사용하여 데이터베이스를 채우고 싶다면, `seed` 메서드를 호출하면 됩니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하며, 이를 통해 여러분이 정의한 모든 시더가 실행됩니다. 원한다면, 특정 시더 클래스명을 `seed` 메서드에 파라미터로 전달하여 일부 시더만 실행할 수도 있습니다:

```
<?php

namespace Tests\Feature;

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithoutMiddleware;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    use RefreshDatabase;

    /**
     * Test creating a new order.
     *
     * @return void
     */
    public function test_orders_can_be_created()
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
또한, `RefreshDatabase` 트레이트를 사용하는 각 테스트 시작 전마다 Laravel이 자동으로 시더를 실행하도록 할 수도 있습니다. 이 기능은 기본 테스트 클래스에 `$seed` 속성을 정의하여 활성화할 수 있습니다:

```
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication;

    /**
     * Indicates whether the default seeder should run before each test.
     *
     * @var bool
     */
    protected $seed = true;
}
```

<!-- When the `$seed` property is `true`, the test will run the `Database\Seeders\DatabaseSeeder` class before each test that uses the `RefreshDatabase` trait. However, you may specify a specific seeder that should be executed by defining a `$seeder` property on your test class: -->
`$seed` 속성이 `true`일 경우, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 만약 매번 실행할 특정 시더를 지정하고 싶다면, 테스트 클래스에서 `$seeder` 속성을 정의하면 됩니다:

```
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

<!-- Laravel provides several database assertions for your [PHPUnit](https://phpunit.de/) feature tests. We'll discuss each of these assertions below. -->
Laravel은 [PHPUnit](https://phpunit.de/) 기능 테스트에서 사용할 수 있는 다양한 데이터베이스 assertion(검증 메서드)을 제공합니다. 아래에서 각각의 assertion에 대해 설명합니다.

<a name="assert-database-count"></a>
<!-- #### assertDatabaseCount -->
#### assertDatabaseCount

<!-- Assert that a table in the database contains the given number of records: -->
데이터베이스의 특정 테이블에 지정한 개수만큼의 레코드가 존재하는지 검증합니다:

```
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-has"></a>
<!-- #### assertDatabaseHas -->
#### assertDatabaseHas

<!-- Assert that a table in the database contains records matching the given key / value query constraints: -->
데이터베이스의 특정 테이블에서 주어진 키/값 조건과 일치하는 레코드가 존재하는지 검증합니다:

```
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
<!-- #### assertDatabaseMissing -->
#### assertDatabaseMissing

<!-- Assert that a table in the database does not contain records matching the given key / value query constraints: -->
데이터베이스의 특정 테이블에 주어진 키/값 조건과 일치하는 레코드가 존재하지 않는지 검증합니다:

```
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
<!-- #### assertSoftDeleted -->
#### assertSoftDeleted

<!-- The `assertSoftDeleted` method may be used to assert a given Eloquent model has been "soft deleted": -->
`assertSoftDeleted` 메서드는 지정한 Eloquent 모델이 '소프트 삭제' 상태임을 확인할 때 사용합니다:

```
$this->assertSoftDeleted($user);
```
<a name="assert-not-deleted"></a>
<!-- #### assertNotSoftDeleted -->
#### assertNotSoftDeleted

<!-- The `assertNotSoftDeleted` method may be used to assert a given Eloquent model hasn't been "soft deleted": -->
`assertNotSoftDeleted` 메서드는 지정한 Eloquent 모델이 '소프트 삭제' 상태가 아님을 확인할 때 사용합니다:

```
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
<!-- #### assertModelExists -->
#### assertModelExists

<!-- Assert that a given model exists in the database: -->
지정한 모델 인스턴스가 데이터베이스에 존재하는지 검증합니다:

```
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
<!-- #### assertModelMissing -->
#### assertModelMissing

<!-- Assert that a given model does not exist in the database: -->
지정한 모델 인스턴스가 데이터베이스에 존재하지 않는지 검증합니다:

```
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
<!-- #### expectsDatabaseQueryCount -->
#### expectsDatabaseQueryCount

<!-- The `expectsDatabaseQueryCount` method may be invoked at the beginning of your test to specify the total number of database queries that you expect to be run during the test. If the actual number of executed queries does not exactly match this expectation, the test will fail: -->
`expectsDatabaseQueryCount` 메서드는 테스트가 시작할 때, 해당 테스트 내에서 실행될 데이터베이스 쿼리의 총 개수를 미리 기대값으로 지정할 수 있습니다. 실제 쿼리 실행 횟수가 기대값과 정확히 일치하지 않으면 테스트가 실패합니다:

```
$this->expectsDatabaseQueryCount(5);

// Test...
```
