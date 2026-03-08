# 데이터베이스 테스트 (Database Testing)

- [소개](#introduction)
    - [각 테스트 후 데이터베이스 초기화](#resetting-the-database-after-each-test)
- [모델 팩토리](#model-factories)
- [시더 실행](#running-seeders)
- [사용 가능한 어서션](#available-assertions)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 데이터베이스 기반 애플리케이션의 테스트를 쉽게 만들어 주는 다양한 유용한 도구와 어서션(assertion)을 제공합니다. 또한, 모델 팩토리와 시더를 활용하면 Eloquent 모델과 연관관계를 이용해 간편하게 테스트용 데이터베이스 레코드를 생성할 수 있습니다. 아래 문서에서는 이와 같은 강력한 기능들을 자세히 설명합니다.

<a name="resetting-the-database-after-each-test"></a>
### 각 테스트 후 데이터베이스 초기화

진행하기에 앞서, 이전 테스트에서 생성된 데이터가 이후 테스트에 영향을 주지 않도록 테스트가 끝날 때마다 데이터베이스를 리셋하는 방법부터 살펴보겠습니다. Laravel에서 기본 제공하는 `Illuminate\Foundation\Testing\RefreshDatabase` 트레이트(trait)를 사용하면 이 과정을 자동으로 처리할 수 있습니다. 테스트 클래스에서 해당 트레이트를 사용하면 됩니다:

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

`Illuminate\Foundation\Testing\RefreshDatabase` 트레이트는 데이터베이스 스키마가 최신 상태일 경우 마이그레이션을 실행하지 않습니다. 대신, 테스트를 데이터베이스 트랜잭션 내에서만 실행합니다. 따라서 이 트레이트를 사용하지 않는 다른 테스트 케이스에서 추가된 레코드는 데이터베이스에 남아있을 수 있습니다.

데이터베이스를 완전히 초기화하고 싶다면 `Illuminate\Foundation\Testing\DatabaseMigrations` 또는 `Illuminate\Foundation\Testing\DatabaseTruncation` 트레이트를 사용할 수 있습니다. 하지만 이 두 옵션은 `RefreshDatabase` 트레이트보다 상당히 느릴 수 있습니다.

<a name="model-factories"></a>
## 모델 팩토리 (Model Factories)

테스트를 진행할 때, 테스트를 실행하기 전에 데이터베이스에 몇 개의 레코드를 미리 삽입해야 할 수도 있습니다. 이때, 각 컬럼 값을 일일이 입력하는 대신 Laravel에서는 [모델 팩토리](/docs/master/eloquent-factories)를 통해 [Eloquent 모델](/docs/master/eloquent) 별로 기본 속성 집합을 정의할 수 있습니다.

모델 팩토리를 만드는 방법과 사용하는 법에 대한 자세한 내용은 [모델 팩토리 공식 문서](/docs/master/eloquent-factories)를 참고하시기 바랍니다. 모델 팩토리를 정의한 후에는 테스트 내에서 다음과 같이 모델을 생성할 수 있습니다:

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

[데이터베이스 시더](/docs/master/seeding)를 사용하여 기능 테스트 중에 데이터베이스를 채우고 싶을 때는 `seed` 메서드를 호출하면 됩니다. 기본적으로 `seed` 메서드는 `DatabaseSeeder`를 실행하여 나머지 시더들을 모두 호출합니다. 또는, 특정 시더 클래스 이름을 `seed` 메서드에 전달해 지정한 시더만 실행할 수도 있습니다:

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

    // 여러 시더 배열로 실행...
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

        // 여러 시더 배열로 실행...
        $this->seed([
            OrderStatusSeeder::class,
            TransactionStatusSeeder::class,
            // ...
        ]);
    }
}
```

또 다른 방법으로, `RefreshDatabase` 트레이트를 사용하는 각 테스트마다 자동으로 데이터베이스 시딩이 이뤄지도록 Laravel에 지시할 수 있습니다. 기본 테스트 클래스에 `Seed` 속성(attribute)을 추가하면 됩니다:

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

`Seed` 속성이 있으면, `RefreshDatabase` 트레이트가 적용된 각 테스트마다 `Database\Seeders\DatabaseSeeder` 클래스가 실행됩니다. 특정 시더만 실행하도록 하고 싶으면 테스트 클래스에 `Seeder` 속성을 다음과 같이 추가할 수 있습니다:

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
## 사용 가능한 어서션 (Available Assertions)

Laravel은 [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de) 기반 기능 테스트에서 사용할 수 있는 여러 데이터베이스 어서션을 제공합니다. 각 어서션에 대해 아래에서 설명합니다.

<a name="assert-database-count"></a>
#### assertDatabaseCount

데이터베이스의 테이블에 특정 개수의 레코드가 존재하는지 확인합니다:

```php
$this->assertDatabaseCount('users', 5);
```

<a name="assert-database-empty"></a>
#### assertDatabaseEmpty

데이터베이스의 테이블이 비어 있는지(레코드가 없는지) 확인합니다:

```php
$this->assertDatabaseEmpty('users');
```

<a name="assert-database-has"></a>
#### assertDatabaseHas

지정한 키/값 쿼리 조건에 일치하는 레코드가 데이터베이스의 테이블에 존재하는지 확인합니다:

```php
$this->assertDatabaseHas('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-database-missing"></a>
#### assertDatabaseMissing

지정한 키/값 쿼리 조건에 일치하는 레코드가 데이터베이스의 테이블에 존재하지 않는지 확인합니다:

```php
$this->assertDatabaseMissing('users', [
    'email' => 'sally@example.com',
]);
```

<a name="assert-deleted"></a>
#### assertSoftDeleted

`assertSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제"되었는지 확인할 때 사용할 수 있습니다:

```php
$this->assertSoftDeleted($user);
```

<a name="assert-not-deleted"></a>
#### assertNotSoftDeleted

`assertNotSoftDeleted` 메서드는 주어진 Eloquent 모델이 "소프트 삭제"되지 않았는지 확인할 때 사용할 수 있습니다:

```php
$this->assertNotSoftDeleted($user);
```

<a name="assert-model-exists"></a>
#### assertModelExists

지정한 모델이나 모델 컬렉션이 데이터베이스에 존재하는지 확인합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$this->assertModelExists($user);
```

<a name="assert-model-missing"></a>
#### assertModelMissing

지정한 모델이나 모델 컬렉션이 데이터베이스에 존재하지 않는지 확인합니다:

```php
use App\Models\User;

$user = User::factory()->create();

$user->delete();

$this->assertModelMissing($user);
```

<a name="expects-database-query-count"></a>
#### expectsDatabaseQueryCount

`expectsDatabaseQueryCount` 메서드는 테스트가 실행되는 동안 예상되는 전체 데이터베이스 쿼리 횟수를 테스트 시작 시 지정할 수 있습니다. 실제 쿼리 실행 횟수가 예상과 정확히 일치하지 않으면 해당 테스트는 실패하게 됩니다:

```php
$this->expectsDatabaseQueryCount(5);

// Test...
```
