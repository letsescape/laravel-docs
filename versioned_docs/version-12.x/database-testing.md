# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행](#running-seeders)
- [사용 가능한 어설션](#available-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스를 사용하는 애플리케이션을 보다 쉽게 테스트할 수 있도록 다양한 유용한 도구와 어설션(assertion)을 제공합니다. 또한, Laravel의 모델 팩토리와 시더(seeder)를 이용하면 애플리케이션의 Eloquent 모델과 연관관계를 활용해 테스트용 데이터베이스 레코드를 손쉽게 생성할 수 있습니다. 이 문서에서는 이러한 강력한 기능에 대해 자세히 알아봅니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화 (Resetting the Database After Each Test)

본격적으로 진행하기 전에, 각 테스트가 끝난 후 이전 테스트 데이터가 다음 테스트에 영향을 주지 않도록 데이터베이스를 초기화하는 방법에 대해 살펴보겠습니다. Laravel에서 제공하는 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트가 이 작업을 자동으로 처리합니다. 테스트 클래스에 해당 트레이트를 적용하여 사용하면 됩니다:

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

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태라면 데이터베이스 마이그레이션을 수행하지 않습니다. 대신, 테스트를 데이터베이스 트랜잭션 내에서 실행합니다. 따라서 이 트레이트를 사용하지 않는 테스트 케이스에서 추가된 레코드는 데이터베이스에 그대로 남아 있을 수 있습니다.

데이터베이스를 완전히 초기화하고 싶다면 `Illuminate\Foundation\Testing\DatabaseMigrations`나 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 하지만 이 두 방법은 `RefreshDatabase` 트레이트에 비해 실행 속도가 상당히 느립니다.

<a name="model-factories"></a>
## 모델 팩토리 (Model Factories)

테스트를 작성할 때, 테스트 실행 전 데이터베이스에 몇 개의 레코드를 삽입할 필요가 있을 수 있습니다. 모든 컬럼 값을 일일이 지정하는 대신, Laravel은 각 [Eloquent 모델](/docs/12.x/eloquent)별로 [모델 팩토리](/docs/12.x/eloquent-factories)를 통해 기본 속성(attribute) 셋을 정의할 수 있게 해줍니다.

모델 팩토리를 생성하고 활용하는 방법에 대해 더 자세히 알고 싶다면 [모델 팩토리 공식 문서](/docs/12.x/eloquent-factories)를 참고하시기 바랍니다. 팩토리를 정의했다면, 다음과 같이 테스트 내에서 팩토리를 활용해 모델 인스턴스를 생성할 수 있습니다:

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
## 시더 실행 (Running Seeders)

[데이터베이스 시더](/docs/12.x/seeding)를 활용해 기능 테스트 시 데이터베이스를 채우고 싶다면, `seed` 메서드를 호출하면 됩니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하며, 이 시더가 다른 모든 시더들을 실행해야 합니다. 특정한 시더 클래스만 실행하고 싶다면 해당 클래스명을 `seed` 메서드에 전달할 수 있습니다:

```php tab=Pest
<?php

use Database\Seeders\OrderStatusSeeder;
use Database\Seeders\TransactionStatusSeeder;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('orders can be created', function () {
    // DatabaseSeeder 실행...
    $this->seed();

    // 특정 시더 실행...
    $this->seed(OrderStatusSeeder::class);

    // ...

    // 여러 시더 배열 실행...
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
        // DatabaseSeeder 실행...
        $this->seed();

        // 특정 시더 실행...
        $this->seed(OrderStatusSeeder::class);

        // ...

        // 여러 시더 배열 실행...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

또는, `RefreshDatabase` 트레이트를 사용하는 모든 테스트에서 테스트마다 자동으로 데이터베이스 시더가 실행되도록 지정할 수도 있습니다. 이를 위해, 기본 테스트 클래스에 `$seed` 속성을 정의해주면 됩니다:

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

`$seed` 속성이 `true`일 경우, `RefreshDatabase` 트레이트를 사용하는 각 테스트 전에 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 만약 특정한 시더만 실행하고 싶다면 테스트 클래스에 `$seeder` 속성을 지정할 수 있습니다:

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
## 사용 가능한 어설션 (Available Assertions)

Laravel에서는 [Pest](https://pestphp.com) 혹은 [PHPUnit](https://phpunit.de) 기반의 기능 테스트에서 사용할 수 있는 다양한 데이터베이스 어설션을 제공합니다. 아래에서 각각의 어설션에 대해 자세히 알아봅니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 지정한 테이블에 일정 개수의 레코드가 존재하는지 검증합니다:

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

데이터베이스의 지정한 테이블에 레코드가 하나도 없는지 검증합니다:

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

데이터베이스의 지정한 테이블에 전달한 key/value 조건과 일치하는 레코드가 존재하는지 검증합니다:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

데이터베이스의 지정한 테이블에 전달한 key/value 조건과 일치하는 레코드가 존재하지 않는지 검증합니다:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 전달한 Eloquent 모델이 "소프트 삭제" 되었는지 검증합니다:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 전달한 Eloquent 모델이 "소프트 삭제" 되지 않았는지 검증합니다:

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

전달한 모델 인스턴스 또는 모델 컬렉션이 데이터베이스에 실제로 존재하는지 검증합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

전달한 모델 인스턴스 또는 모델 컬렉션이 데이터베이스에 존재하지 않는지 검증합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트 시작 시 호출하여, 해당 테스트에서 실행될 데이터베이스 쿼리의 예상 총 개수를 지정할 수 있습니다. 만약 실제로 실행된 쿼리 개수가 지정한 값과 정확히 일치하지 않으면 테스트가 실패합니다:

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```
