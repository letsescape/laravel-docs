# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 규칙](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청크 처리](#chunking-results)
    - [Lazy 컬렉션을 사용한 청크 처리](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델 / 집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 수정](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [수정](#updates)
    - [대량 할당](#mass-assignment)
    - [업서트](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 쿼리](#querying-soft-deleted-models)
- [모델 가지치기](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [전역 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [대기 중인 속성](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 사용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 비활성화](#muting-events)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel에는 데이터베이스와 즐겁게 상호작용할 수 있게 해주는 객체 관계 매퍼(ORM)인 Eloquent가 포함되어 있습니다. Eloquent를 사용할 때 각 데이터베이스 테이블에는 해당 테이블과 상호작용하는 데 사용되는 "모델"이 대응됩니다. Eloquent 모델은 데이터베이스 테이블에서 레코드를 조회하는 것뿐만 아니라, 테이블에 레코드를 삽입, 수정, 삭제할 수도 있게 해줍니다.

> [!NOTE]
> 시작하기 전에 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 설정하세요. 데이터베이스 설정에 대한 자세한 내용은 [데이터베이스 설정 문서](/docs/13.x/database#configuration)를 확인하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성 (Generating Model Classes)

시작하려면 Eloquent 모델을 만들어 보겠습니다. 모델은 일반적으로 `app\Models` 디렉터리에 위치하며 `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. 새 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/13.x/artisan)를 사용할 수 있습니다.

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/13.x/migrations)도 함께 생성하고 싶다면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다.

```shell
php artisan make:model Flight --migration
```

모델을 생성할 때 팩토리, 시더, 정책, 컨트롤러, 폼 요청 같은 여러 종류의 클래스도 함께 생성할 수 있습니다. 또한 이러한 옵션을 조합하여 여러 클래스를 한 번에 만들 수도 있습니다.

```shell
# Generate a model and a FlightFactory class...
php artisan make:model Flight --factory
php artisan make:model Flight -f

# Generate a model and a FlightSeeder class...
php artisan make:model Flight --seed
php artisan make:model Flight -s

# Generate a model and a FlightController class...
php artisan make:model Flight --controller
php artisan make:model Flight -c

# Generate a model, FlightController resource class, and form request classes...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# Generate a model and a FlightPolicy class...
php artisan make:model Flight --policy

# Generate a model and a migration, factory, seeder, and controller...
php artisan make:model Flight -mfsc

# Shortcut to generate a model, migration, factory, seeder, policy, controller, and form requests...
php artisan make:model Flight --all
php artisan make:model Flight -a

# Generate a pivot model...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 살펴보기

때로는 모델의 코드를 대략 훑어보는 것만으로 해당 모델에서 사용할 수 있는 모든 속성과 연관관계를 파악하기 어려울 수 있습니다. 이럴 때는 `model:show` Artisan 명령어를 사용해 보세요. 이 명령어는 모델의 모든 속성과 연관관계를 편리하게 한눈에 볼 수 있도록 보여줍니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 규칙 (Eloquent Model Conventions)

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 배치됩니다. 기본적인 모델 클래스를 살펴보면서 Eloquent의 핵심 규칙 몇 가지를 알아보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    // ...
}
```

<a name="table-names"></a>
### 테이블 이름

위 예제를 보면, `Flight` 모델이 어떤 데이터베이스 테이블에 대응되는지 Eloquent에 따로 알려주지 않았다는 것을 알 수 있습니다. 규칙상 다른 이름을 명시적으로 지정하지 않으면 클래스명의 "스네이크 케이스", 복수형 이름이 테이블 이름으로 사용됩니다. 따라서 이 경우 Eloquent는 `Flight` 모델이 `flights` 테이블에 레코드를 저장한다고 가정하고, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 레코드를 저장한다고 가정합니다.

모델에 대응되는 데이터베이스 테이블이 이 규칙에 맞지 않는다면, `Table` 속성을 사용하여 모델의 테이블 이름을 직접 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table('my_flights')]
class Flight extends Model
{
    // ...
}
```


<a name="primary-keys"></a>
### 기본 키

Eloquent는 각 모델에 대응되는 데이터베이스 테이블에 `id`라는 이름의 기본 키 컬럼이 있다고 가정합니다. 필요한 경우 `Table` 속성의 `key` 인수를 사용하여 모델의 기본 키로 사용할 다른 컬럼을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(key: 'flight_id')]
class Flight extends Model
{
    // ...
}
```

또한 Eloquent는 기본 키가 증가하는 정수 값이라고 가정합니다. 즉, Eloquent는 기본 키를 자동으로 정수로 캐스팅합니다. 증가하지 않는 기본 키나 숫자가 아닌 기본 키를 사용하려면 `Table` 속성에 `keyType` 및 `incrementing` 인수를 지정해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(key: 'uuid', keyType: 'string', incrementing: false)]
class Flight extends Model
{
    // ...
}
```

자동 증가 ID만 비활성화하면 된다면 `WithoutIncrementing` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\WithoutIncrementing;
use Illuminate\Database\Eloquent\Model;

#[WithoutIncrementing]
class Flight extends Model
{
    // ...
}
```

<a name="composite-primary-keys"></a>
#### "복합" 기본 키

Eloquent는 각 모델에 기본 키 역할을 할 수 있는, 고유하게 식별 가능한 "ID"가 최소 하나 있어야 한다고 요구합니다. "복합" 기본 키는 Eloquent 모델에서 지원되지 않습니다. 하지만 테이블을 고유하게 식별하는 기본 키와 별개로, 데이터베이스 테이블에 여러 컬럼으로 구성된 고유 인덱스를 추가하는 것은 자유롭게 할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본 키로 자동 증가 정수 대신 UUID를 사용할 수 있습니다. UUID는 전 세계적으로 고유한 영숫자 식별자이며 길이는 36자입니다.

모델이 자동 증가 정수 키 대신 UUID 키를 사용하게 하려면 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용할 수 있습니다. 물론 해당 모델에 [UUID에 해당하는 기본 키 컬럼](/docs/13.x/migrations#column-method-uuid)이 있는지도 확인해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUuids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Europe']);

$article->id; // "018f2b5c-6a7f-7b12-9d6f-2f8a4e0c9c11"
```

기본적으로 `HasUuids` 트레이트는 모델에 대해 [UUIDv7](/docs/13.x/strings#method-str-uuid7) 식별자를 생성합니다. 이러한 UUID는 사전식으로 정렬할 수 있기 때문에 인덱스가 적용된 데이터베이스 저장소에서 더 효율적입니다.

특정 모델에서 UUID 생성 과정을 재정의하려면 모델에 `newUniqueId` 메서드를 정의하면 됩니다. 또한 UUID가 부여될 컬럼을 지정하려면 모델에 `uniqueIds` 메서드를 정의할 수 있습니다.

```php
use Ramsey\Uuid\Uuid;

/**
 * Generate a new UUID for the model.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * Get the columns that should receive a unique identifier.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 비슷하지만 길이가 26자에 불과합니다. 정렬 가능한 UUID와 마찬가지로, ULID도 사전식으로 정렬할 수 있어 효율적인 데이터베이스 인덱싱에 적합합니다. ULID를 사용하려면 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 사용해야 합니다. 또한 해당 모델에 [ULID에 해당하는 기본 키 컬럼](/docs/13.x/migrations#column-method-ulid)이 있는지도 확인해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUlids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Asia']);

$article->id; // "01gd4d3tgrrfqeda94gdbtdk5c"
```

<a name="timestamps"></a>
### 타임스탬프

기본적으로 Eloquent는 모델에 대응되는 데이터베이스 테이블에 `created_at` 및 `updated_at` 컬럼이 있다고 기대합니다. Eloquent는 모델이 생성되거나 수정될 때 이 컬럼들의 값을 자동으로 설정합니다. 이 컬럼들이 Eloquent에 의해 자동으로 관리되지 않게 하려면 모델의 `Table` 속성에서 `timestamps`를 `false`로 설정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(timestamps: false)]
class Flight extends Model
{
    // ...
}
```

타임스탬프만 비활성화하면 된다면 `WithoutTimestamps` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\WithoutTimestamps;
use Illuminate\Database\Eloquent\Model;

#[WithoutTimestamps]
class Flight extends Model
{
    // ...
}
```

모델의 타임스탬프 형식을 사용자 지정해야 한다면 `Table` 속성의 `dateFormat` 인수를 사용할 수 있습니다. 이 설정은 날짜 속성이 데이터베이스에 저장되는 방식과 모델이 배열 또는 JSON으로 직렬화될 때의 형식을 결정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(dateFormat: 'U')]
class Flight extends Model
{
    // ...
}
```

날짜 형식만 정의하면 된다면 `DateFormat` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\DateFormat;
use Illuminate\Database\Eloquent\Model;

#[DateFormat('U')]
class Flight extends Model
{
    // ...
}
```

타임스탬프를 저장하는 데 사용되는 컬럼 이름을 사용자 지정해야 한다면 모델에 `CREATED_AT` 및 `UPDATED_AT` 상수를 정의할 수 있습니다.

```php
<?php

class Flight extends Model
{
    /**
     * The name of the "created at" column.
     *
     * @var string|null
     */
    public const CREATED_AT = 'creation_date';

    /**
     * The name of the "updated at" column.
     *
     * @var string|null
     */
    public const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 타임스탬프가 변경되지 않은 상태로 모델 작업을 수행하고 싶다면, `withoutTimestamps` 메서드에 전달한 클로저 안에서 모델을 조작할 수 있습니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션에 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델과 상호작용할 때 다른 연결을 사용하도록 지정하고 싶다면 `Connection` 속성을 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Connection;
use Illuminate\Database\Eloquent\Model;

#[Connection('mysql')]
class Flight extends Model
{
    // ...
}
```

<a name="default-attribute-values"></a>
### 기본 속성 값

기본적으로 새로 인스턴스화된 모델 인스턴스에는 어떤 속성 값도 포함되어 있지 않습니다. 모델 속성 중 일부에 기본값을 정의하고 싶다면 모델에 `$attributes` 속성을 정의할 수 있습니다. `$attributes` 배열에 넣는 속성 값은 데이터베이스에서 막 읽어 온 것처럼 원시(raw) 형식, 즉 "저장 가능한" 형식이어야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The model's default values for attributes.
     *
     * @var array<string, mixed>
     */
    protected $attributes = [
        'options' => '[]',
        'delayed' => false,
    ];
}
```
<a name="configuring-eloquent-strictness"></a>
### Eloquent 엄격성 설정

Laravel은 다양한 상황에서 Eloquent의 동작과 "엄격성"을 설정할 수 있는 여러 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 지연 로딩을 막을지 여부를 나타내는 선택적 boolean 인수를 받습니다. 예를 들어 프로덕션 환경에서는 코드에 지연 로딩된 연관관계가 실수로 포함되어 있더라도 정상적으로 동작하도록 두고, 프로덕션이 아닌 환경에서만 지연 로딩을 비활성화하고 싶을 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드에서 호출해야 합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또한 `preventSilentlyDiscardingAttributes` 메서드를 호출하여 채울 수 없는 속성을 채우려고 할 때 Laravel이 예외를 던지도록 지시할 수 있습니다. 이렇게 하면 모델의 `fillable` 배열에 추가되지 않은 속성을 설정하려고 할 때 로컬 개발 중 예상치 못한 오류를 방지하는 데 도움이 됩니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기 (Retrieving Models)

모델과 [해당 모델에 연결된 데이터베이스 테이블](/docs/13.x/migrations#generating-migrations)을 만들었다면, 이제 데이터베이스에서 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델은 모델과 연결된 데이터베이스 테이블을 유연하게 쿼리할 수 있게 해주는 강력한 [쿼리 빌더](/docs/13.x/queries)라고 생각할 수 있습니다. 모델의 `all` 메서드는 모델과 연결된 데이터베이스 테이블의 모든 레코드를 조회합니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성하기

Eloquent의 `all` 메서드는 모델 테이블의 모든 결과를 반환합니다. 하지만 각 Eloquent 모델은 [쿼리 빌더](/docs/13.x/queries) 역할을 하므로, 쿼리에 추가 제약 조건을 붙인 뒤 `get` 메서드를 호출하여 결과를 조회할 수 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [쿼리 빌더](/docs/13.x/queries)가 제공하는 모든 메서드를 살펴보는 것이 좋습니다. Eloquent 쿼리를 작성할 때 이러한 메서드를 모두 사용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 새로고침하기

이미 데이터베이스에서 조회한 Eloquent 모델 인스턴스가 있다면, `fresh`와 `refresh` 메서드를 사용해 모델을 "새로고침"할 수 있습니다. `fresh` 메서드는 데이터베이스에서 모델을 다시 조회합니다. 기존 모델 인스턴스는 영향을 받지 않습니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 데이터베이스의 최신 데이터를 사용해 기존 모델을 다시 하이드레이션합니다. 또한 이미 로드된 모든 연관관계도 함께 새로고침됩니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

앞에서 살펴본 것처럼 `all`과 `get` 같은 Eloquent 메서드는 데이터베이스에서 여러 레코드를 조회합니다. 하지만 이 메서드들은 일반 PHP 배열을 반환하지 않습니다. 대신 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 확장합니다. 이 기본 컬렉션 클래스는 데이터 컬렉션을 다룰 때 유용한 [다양한 메서드](/docs/13.x/collections#available-methods)를 제공합니다. 예를 들어 `reject` 메서드를 사용하면 호출된 클로저의 결과에 따라 컬렉션에서 모델을 제거할 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Laravel의 기본 컬렉션 클래스가 제공하는 메서드 외에도, Eloquent 컬렉션 클래스는 Eloquent 모델 컬렉션과 상호작용하기 위해 특별히 마련된 [몇 가지 추가 메서드](/docs/13.x/eloquent-collections#available-methods)를 제공합니다.

Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하므로, 배열처럼 컬렉션을 반복할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리

`all` 또는 `get` 메서드로 수만 개의 Eloquent 레코드를 로드하려고 하면 애플리케이션의 메모리가 부족해질 수 있습니다. 이러한 메서드 대신 `chunk` 메서드를 사용하면 많은 수의 모델을 더 효율적으로 처리할 수 있습니다.

`chunk` 메서드는 Eloquent 모델의 일부 집합을 조회한 뒤, 처리할 수 있도록 클로저에 전달합니다. 한 번에 현재 청크에 해당하는 Eloquent 모델만 조회하므로, 많은 수의 모델을 다룰 때 `chunk` 메서드는 메모리 사용량을 크게 줄여줍니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드에 전달하는 첫 번째 인수는 각 "청크"마다 받을 레코드 수입니다. 두 번째 인수로 전달한 클로저는 데이터베이스에서 조회된 각 청크마다 호출됩니다. 클로저에 전달할 각 레코드 청크를 조회하기 위해 데이터베이스 쿼리가 실행됩니다.

`chunk` 메서드의 결과를 특정 컬럼 기준으로 필터링하면서, 결과를 반복하는 동안 같은 컬럼도 함께 업데이트한다면 `chunkById` 메서드를 사용해야 합니다. 이러한 상황에서 `chunk` 메서드를 사용하면 예상치 못한 일관성 없는 결과가 발생할 수 있습니다. 내부적으로 `chunkById` 메서드는 항상 이전 청크의 마지막 모델보다 큰 `id` 컬럼 값을 가진 모델을 조회합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`와 `lazyById` 메서드는 실행되는 쿼리에 자체적인 "where" 조건을 추가하므로, 일반적으로 여러분의 조건은 클로저 안에서 [논리적으로 그룹화](/docs/13.x/queries#logical-grouping)해야 합니다.

```php
Flight::where(function ($query) {
    $query->where('delayed', true)->orWhere('cancelled', true);
})->chunkById(200, function (Collection $flights) {
    $flights->each->update([
        'departed' => false,
        'cancelled' => true
    ]);
}, column: 'id');
```

<a name="chunking-using-lazy-collections"></a>
### 지연 컬렉션으로 청크 처리하기

`lazy` 메서드는 내부적으로 쿼리를 청크 단위로 실행한다는 점에서 [`chunk` 메서드](#chunking-results)와 비슷하게 동작합니다. 하지만 각 청크를 그대로 콜백에 직접 전달하는 대신, `lazy` 메서드는 Eloquent 모델의 평탄화된 [LazyCollection](/docs/13.x/collections#lazy-collections)을 반환합니다. 따라서 결과를 하나의 스트림처럼 다룰 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

`lazy` 메서드의 결과를 특정 컬럼 기준으로 필터링하면서, 결과를 반복하는 동안 같은 컬럼도 함께 업데이트한다면 `lazyById` 메서드를 사용해야 합니다. 내부적으로 `lazyById` 메서드는 항상 이전 청크의 마지막 모델보다 큰 `id` 컬럼 값을 가진 모델을 조회합니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 사용하면 `id`의 내림차순을 기준으로 결과를 필터링할 수 있습니다.

<a name="cursors"></a>
### 커서

`lazy` 메서드와 비슷하게, `cursor` 메서드는 수만 개의 Eloquent 모델 레코드를 반복 처리할 때 애플리케이션의 메모리 사용량을 크게 줄이는 데 사용할 수 있습니다.

`cursor` 메서드는 데이터베이스 쿼리를 한 번만 실행합니다. 다만 개별 Eloquent 모델은 실제로 반복될 때까지 하이드레이션되지 않습니다. 따라서 커서를 반복하는 동안 메모리에는 항상 Eloquent 모델 하나만 유지됩니다.

> [!WARNING]
> `cursor` 메서드는 한 번에 Eloquent 모델 하나만 메모리에 보관하므로, 연관관계를 즉시 로딩할 수 없습니다. 연관관계를 즉시 로딩해야 한다면 대신 [`lazy` 메서드](#chunking-using-lazy-collections)를 사용하는 것을 고려하세요.

내부적으로 `cursor` 메서드는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 사용해 이 기능을 구현합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [지연 컬렉션](/docs/13.x/collections#lazy-collections)을 사용하면 한 번에 모델 하나만 메모리에 로드하면서도 일반적인 Laravel 컬렉션에서 사용할 수 있는 많은 컬렉션 메서드를 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만(한 번에 Eloquent 모델 하나만 메모리에 보관하기 때문입니다), 결국에는 여전히 메모리가 부족해질 수 있습니다. 이는 [PHP의 PDO 드라이버가 내부적으로 모든 원시 쿼리 결과를 버퍼에 캐시하기 때문](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)입니다. 매우 많은 수의 Eloquent 레코드를 다룬다면 대신 [`lazy` 메서드](#chunking-using-lazy-collections)를 사용하는 것을 고려하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 Select

Eloquent는 고급 서브쿼리 기능도 제공합니다. 이 기능을 사용하면 단일 쿼리에서 관련 테이블의 정보를 가져올 수 있습니다. 예를 들어 항공편 `destinations` 테이블과 목적지로 향하는 `flights` 테이블이 있다고 가정해 보겠습니다. `flights` 테이블에는 항공편이 목적지에 도착한 시간을 나타내는 `arrived_at` 컬럼이 있습니다.

쿼리 빌더의 `select`와 `addSelect` 메서드에서 사용할 수 있는 서브쿼리 기능을 사용하면, 단일 쿼리로 모든 `destinations`와 각 목적지에 가장 최근 도착한 항공편의 이름을 선택할 수 있습니다.

```php
use App\Models\Destination;
use App\Models\Flight;

return Destination::addSelect(['last_flight' => Flight::select('name')
    ->whereColumn('destination_id', 'destinations.id')
    ->orderByDesc('arrived_at')
    ->limit(1)
])->get();
```

<a name="subquery-ordering"></a>
#### 서브쿼리 정렬

또한 쿼리 빌더의 `orderBy` 함수는 서브쿼리를 지원합니다. 항공편 예제를 계속 사용하면, 이 기능을 사용해 각 목적지에 마지막 항공편이 도착한 시간을 기준으로 모든 목적지를 정렬할 수 있습니다. 이 작업 역시 단일 데이터베이스 쿼리를 실행하면서 처리할 수 있습니다.

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델 / 집계 조회하기 (Retrieving Single Models / Aggregates)

주어진 쿼리와 일치하는 모든 레코드를 조회하는 것 외에도, `find`, `first`, `firstWhere` 메서드를 사용해 단일 레코드를 조회할 수 있습니다. 이 메서드들은 모델 컬렉션을 반환하는 대신 단일 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

// Retrieve a model by its primary key...
$flight = Flight::find(1);

// Retrieve the first model matching the query constraints...
$flight = Flight::where('active', 1)->first();

// Alternative to retrieving the first model matching the query constraints...
$flight = Flight::firstWhere('active', 1);
```

때로는 결과를 찾지 못했을 때 다른 작업을 수행하고 싶을 수 있습니다. `findOr`와 `firstOr` 메서드는 단일 모델 인스턴스를 반환하거나, 결과를 찾지 못한 경우 주어진 클로저를 실행합니다. 클로저가 반환하는 값이 해당 메서드의 결과로 간주됩니다.

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### 찾을 수 없음 예외

때로는 모델을 찾지 못했을 때 예외를 던지고 싶을 수 있습니다. 이는 라우트나 컨트롤러에서 특히 유용합니다. `findOrFail`과 `firstOrFail` 메서드는 쿼리의 첫 번째 결과를 조회합니다. 하지만 결과를 찾지 못하면 `Illuminate\Database\Eloquent\ModelNotFoundException`이 던져집니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`이 처리되지 않으면, 404 HTTP 응답이 자동으로 클라이언트에 반환됩니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성하기

`firstOrCreate` 메서드는 주어진 컬럼 / 값 쌍을 사용해 데이터베이스 레코드를 찾으려고 시도합니다. 데이터베이스에서 모델을 찾을 수 없다면, 첫 번째 배열 인수와 선택적인 두 번째 배열 인수를 병합한 결과 속성으로 레코드를 삽입합니다.

`firstOrNew` 메서드는 `firstOrCreate`와 마찬가지로 주어진 속성과 일치하는 레코드를 데이터베이스에서 찾으려고 시도합니다. 하지만 모델을 찾지 못하면 새 모델 인스턴스를 반환합니다. `firstOrNew`가 반환한 모델은 아직 데이터베이스에 저장되지 않았다는 점에 유의하세요. 저장하려면 `save` 메서드를 직접 호출해야 합니다.

```php
use App\Models\Flight;

// Retrieve flight by name or create it if it doesn't exist...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// Retrieve flight by name or create it with the name, delayed, and arrival_time attributes...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// Retrieve flight by name or instantiate a new Flight instance...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// Retrieve flight by name or instantiate with the name, delayed, and arrival_time attributes...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회하기

Eloquent 모델을 다룰 때 Laravel [쿼리 빌더](/docs/13.x/queries)가 제공하는 `count`, `sum`, `max` 및 기타 [집계 메서드](/docs/13.x/queries#aggregates)도 사용할 수 있습니다. 예상할 수 있듯이, 이 메서드들은 Eloquent 모델 인스턴스 대신 스칼라 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 업데이트하기 (Inserting and Updating Models)

<a name="inserts"></a>
### 삽입

물론 Eloquent를 사용할 때 데이터베이스에서 모델을 조회하기만 하는 것은 아닙니다. 새 레코드도 삽입해야 합니다. 다행히 Eloquent는 이 작업을 간단하게 만들어 줍니다. 데이터베이스에 새 레코드를 삽입하려면 새 모델 인스턴스를 만들고 모델의 속성을 설정해야 합니다. 그런 다음 모델 인스턴스에서 `save` 메서드를 호출합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Store a new flight in the database.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate the request...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

이 예제에서는 들어오는 HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당합니다. `save` 메서드를 호출하면 데이터베이스에 레코드가 삽입됩니다. 모델의 `created_at`과 `updated_at` 타임스탬프는 `save` 메서드가 호출될 때 자동으로 설정되므로, 직접 설정할 필요가 없습니다.

데이터베이스 트랜잭션 안에서 모델을 저장하고 싶다면 `saveOrFail` 메서드를 사용할 수 있습니다. 저장 중 예외가 발생하면 트랜잭션은 자동으로 롤백됩니다.

```php
$flight->saveOrFail();
```

또는 `create` 메서드를 사용해 하나의 PHP 문장으로 새 모델을 "저장"할 수 있습니다. 삽입된 모델 인스턴스는 `create` 메서드에 의해 반환됩니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create` 메서드를 사용하기 전에 모델 클래스에 `Fillable` 또는 `Guarded` 속성을 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 대량 할당 취약점으로부터 보호되기 때문에 이러한 속성이 필요합니다. 대량 할당에 대해 더 알아보려면 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 업데이트

`save` 메서드는 데이터베이스에 이미 존재하는 모델을 업데이트하는 데도 사용할 수 있습니다. 모델을 업데이트하려면 먼저 모델을 조회한 뒤 업데이트하려는 속성을 설정해야 합니다. 그런 다음 모델의 `save` 메서드를 호출합니다. 이 경우에도 `updated_at` 타임스탬프는 자동으로 업데이트되므로, 값을 직접 설정할 필요가 없습니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```
데이터베이스 트랜잭션 안에서 모델을 업데이트하려면 `updateOrFail` 메서드를 사용할 수 있습니다. 업데이트 중 예외가 발생하면 트랜잭션은 자동으로 롤백됩니다.

```php
$flight->updateOrFail(['name' => 'Paris to London']);
```

때로는 기존 모델을 업데이트하거나, 일치하는 모델이 없으면 새 모델을 생성해야 할 수 있습니다. `firstOrCreate` 메서드와 마찬가지로, `updateOrCreate` 메서드는 모델을 영속화하므로 `save` 메서드를 직접 호출할 필요가 없습니다.

아래 예시에서는 `departure` 위치가 `Oakland`이고 `destination` 위치가 `San Diego`인 항공편이 존재하면, 해당 항공편의 `price`와 `discounted` 컬럼이 업데이트됩니다. 그런 항공편이 없으면 첫 번째 인수 배열과 두 번째 인수 배열을 병합한 결과 속성을 가진 새 항공편이 생성됩니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

`firstOrCreate` 또는 `updateOrCreate` 같은 메서드를 사용할 때는 새 모델이 생성되었는지, 기존 모델이 업데이트되었는지 알 수 없을 수 있습니다. `wasRecentlyCreated` 속성은 현재 라이프사이클 동안 해당 모델이 생성되었는지를 나타냅니다.

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // New flight record was inserted...
}
```

<a name="mass-updates"></a>
#### 대량 업데이트

주어진 쿼리와 일치하는 모델에 대해서도 업데이트를 수행할 수 있습니다. 이 예시에서는 `active` 상태이고 `destination`이 `San Diego`인 모든 항공편을 지연 상태로 표시합니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 업데이트할 컬럼을 나타내는 컬럼과 값 쌍의 배열을 기대합니다. `update` 메서드는 영향받은 행 수를 반환합니다.

> [!WARNING]
> Eloquent를 통해 대량 업데이트를 실행하면 업데이트된 모델에 대해 `saving`, `saved`, `updating`, `updated` 모델 이벤트가 실행되지 않습니다. 대량 업데이트를 실행할 때 모델을 실제로 조회하지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 검사

Eloquent는 모델의 내부 상태를 검사하고, 모델이 처음 조회된 이후 속성이 어떻게 변경되었는지 확인할 수 있도록 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

`isDirty` 메서드는 모델이 조회된 이후 모델의 속성이 변경되었는지 확인합니다. 특정 속성명이나 속성 배열을 `isDirty` 메서드에 전달하여 해당 속성 중 하나라도 "dirty" 상태인지 확인할 수 있습니다. `isClean` 메서드는 모델이 조회된 이후 속성이 변경되지 않았는지 확인합니다. 이 메서드도 선택적으로 속성 인수를 받을 수 있습니다.

```php
use App\Models\User;

$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->isDirty(); // true
$user->isDirty('title'); // true
$user->isDirty('first_name'); // false
$user->isDirty(['first_name', 'title']); // true

$user->isClean(); // false
$user->isClean('title'); // false
$user->isClean('first_name'); // true
$user->isClean(['first_name', 'title']); // false

$user->save();

$user->isDirty(); // false
$user->isClean(); // true
```

`wasChanged` 메서드는 현재 요청 사이클 안에서 모델이 마지막으로 저장될 때 속성이 변경되었는지 확인합니다. 필요한 경우 속성명을 전달하여 특정 속성이 변경되었는지 확인할 수 있습니다.

```php
$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->save();

$user->wasChanged(); // true
$user->wasChanged('title'); // true
$user->wasChanged(['title', 'slug']); // true
$user->wasChanged('first_name'); // false
$user->wasChanged(['first_name', 'title']); // true
```

`getOriginal` 메서드는 모델이 조회된 이후 변경된 내용과 관계없이 모델의 원래 속성을 담은 배열을 반환합니다. 필요한 경우 특정 속성명을 전달하여 해당 속성의 원래 값을 가져올 수 있습니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // Array of original attributes...
```

`getChanges` 메서드는 모델이 마지막으로 저장될 때 변경된 속성을 담은 배열을 반환하며, `getPrevious` 메서드는 모델이 마지막으로 저장되기 전의 원래 속성 값을 담은 배열을 반환합니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->update([
    'name' => 'Jack',
    'email' => 'jack@example.com',
]);

$user->getChanges();

/*
    [
        'name' => 'Jack',
        'email' => 'jack@example.com',
    ]
*/

$user->getPrevious();

/*
    [
        'name' => 'John',
        'email' => 'john@example.com',
    ]
*/
```

<a name="mass-assignment"></a>
### 대량 할당

`create` 메서드를 사용하면 하나의 PHP 문장으로 새 모델을 "저장"할 수 있습니다. 삽입된 모델 인스턴스가 이 메서드를 통해 반환됩니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

하지만 `create` 메서드를 사용하기 전에 모델 클래스에 `Fillable` 또는 `Guarded` 속성을 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 대량 할당 취약점으로부터 보호되기 때문에 이러한 속성이 필요합니다.

대량 할당 취약점은 사용자가 예상치 못한 HTTP 요청 필드를 전달하고, 그 필드가 의도하지 않은 데이터베이스 컬럼을 변경할 때 발생합니다. 예를 들어 악의적인 사용자가 HTTP 요청을 통해 `is_admin` 파라미터를 보낼 수 있고, 이 값이 모델의 `create` 메서드에 전달되면 사용자가 자신을 관리자로 승격시킬 수 있습니다.

따라서 먼저 어떤 모델 속성을 대량 할당 가능하게 만들지 정의해야 합니다. 모델의 `Fillable` 속성을 사용하면 됩니다. 예를 들어 `Flight` 모델의 `name` 속성을 대량 할당 가능하게 만들어 보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['name'])]
class Flight extends Model
{
    // ...
}
```

대량 할당 가능한 속성을 지정한 후에는 `create` 메서드를 사용하여 데이터베이스에 새 레코드를 삽입할 수 있습니다. `create` 메서드는 새로 생성된 모델 인스턴스를 반환합니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면 `fill` 메서드를 사용하여 속성 배열로 값을 채울 수 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼을 할당할 때는 각 컬럼의 대량 할당 가능한 키를 모델의 `Fillable` 속성에 지정해야 합니다. 보안을 위해 Laravel은 `Guarded` 속성을 사용할 때 중첩된 JSON 속성 업데이트를 지원하지 않습니다.

```php
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['options->enabled'])]
class Flight extends Model
{
    // ...
}
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 허용

모든 속성을 대량 할당 가능하게 만들고 싶다면 모델에 `Unguarded` 속성을 사용할 수 있습니다. 모델의 보호를 해제하기로 했다면, Eloquent의 `fill`, `create`, `update` 메서드에 전달하는 배열은 항상 직접 신중하게 구성해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Unguarded;
use Illuminate\Database\Eloquent\Model;

#[Unguarded]
class Flight extends Model
{
    // ...
}
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외

기본적으로 대량 할당 작업을 수행할 때 `Fillable` 속성에 포함되지 않은 속성은 조용히 버려집니다. 프로덕션 환경에서는 이것이 기대되는 동작입니다. 하지만 로컬 개발 중에는 모델 변경 사항이 왜 적용되지 않는지 혼란을 줄 수 있습니다.

원한다면 채울 수 없는 속성을 채우려고 할 때 Laravel이 예외를 던지도록 지시할 수 있습니다. 이를 위해 `preventSilentlyDiscardingAttributes` 메서드를 호출하면 됩니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### 업서트

Eloquent의 `upsert` 메서드는 하나의 원자적 작업으로 레코드를 업데이트하거나 생성하는 데 사용할 수 있습니다. 이 메서드의 첫 번째 인수는 삽입하거나 업데이트할 값으로 구성되며, 두 번째 인수는 관련 테이블 안에서 레코드를 고유하게 식별하는 컬럼을 나열합니다. 세 번째이자 마지막 인수는 데이터베이스에 일치하는 레코드가 이미 존재할 경우 업데이트할 컬럼 배열입니다. 모델에서 타임스탬프가 활성화되어 있으면 `upsert` 메서드는 `created_at`과 `updated_at` 타임스탬프를 자동으로 설정합니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 메서드의 두 번째 인수에 포함된 컬럼에 "primary" 또는 "unique" 인덱스가 있어야 합니다. 또한 MariaDB와 MySQL 데이터베이스 드라이버는 `upsert` 메서드의 두 번째 인수를 무시하고, 항상 테이블의 "primary" 및 "unique" 인덱스를 사용하여 기존 레코드를 감지합니다.

<a name="deleting-models"></a>
## 모델 삭제 (Deleting Models)

모델을 삭제하려면 모델 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

데이터베이스 트랜잭션 안에서 모델을 삭제하려면 `deleteOrFail` 메서드를 사용할 수 있습니다. 삭제 중 예외가 발생하면 트랜잭션은 자동으로 롤백됩니다.

```php
$flight->deleteOrFail();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제

위 예시에서는 `delete` 메서드를 호출하기 전에 데이터베이스에서 모델을 조회하고 있습니다. 하지만 모델의 기본 키를 알고 있다면 `destroy` 메서드를 호출하여 모델을 명시적으로 조회하지 않고 삭제할 수 있습니다. `destroy` 메서드는 단일 기본 키뿐만 아니라 여러 기본 키, 기본 키 배열, 또는 기본 키의 [컬렉션](/docs/13.x/collections)도 받을 수 있습니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)을 사용하고 있다면 `forceDestroy` 메서드를 통해 모델을 영구적으로 삭제할 수 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델에 대해 `deleting` 및 `deleted` 이벤트가 올바르게 디스패치되도록 각 모델을 개별적으로 로드한 뒤 `delete` 메서드를 호출합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 사용한 모델 삭제

물론 Eloquent 쿼리를 만들어 쿼리 조건과 일치하는 모든 모델을 삭제할 수 있습니다. 이 예시에서는 비활성 상태로 표시된 모든 항공편을 삭제합니다. 대량 업데이트와 마찬가지로, 대량 삭제는 삭제되는 모델에 대해 모델 이벤트를 디스패치하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블의 모든 모델을 삭제하려면 조건을 추가하지 않고 쿼리를 실행해야 합니다.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent를 통해 대량 삭제 문을 실행하면 삭제된 모델에 대해 `deleting` 및 `deleted` 모델 이벤트가 디스패치되지 않습니다. 삭제 문을 실행할 때 모델을 실제로 조회하지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

Eloquent는 데이터베이스에서 레코드를 실제로 제거하는 것 외에도 모델을 "소프트 삭제"할 수 있습니다. 모델이 소프트 삭제되면 데이터베이스에서 실제로 제거되지 않습니다. 대신 모델에 `deleted_at` 속성이 설정되어 모델이 "삭제"된 날짜와 시간을 나타냅니다. 모델에서 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` trait를 추가하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Flight extends Model
{
    use SoftDeletes;
}
```

> [!NOTE]
> `SoftDeletes` trait는 `deleted_at` 속성을 자동으로 `DateTime` / `Carbon` 인스턴스로 캐스팅합니다.

데이터베이스 테이블에도 `deleted_at` 컬럼을 추가해야 합니다. Laravel [스키마 빌더](/docs/13.x/migrations)에는 이 컬럼을 생성하는 헬퍼 메서드가 포함되어 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('flights', function (Blueprint $table) {
    $table->softDeletes();
});

Schema::table('flights', function (Blueprint $table) {
    $table->dropSoftDeletes();
});
```

이제 모델에서 `delete` 메서드를 호출하면 `deleted_at` 컬럼이 현재 날짜와 시간으로 설정됩니다. 하지만 모델의 데이터베이스 레코드는 테이블에 남아 있습니다. 소프트 삭제를 사용하는 모델을 쿼리할 때는 소프트 삭제된 모델이 모든 쿼리 결과에서 자동으로 제외됩니다.

주어진 모델 인스턴스가 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제된 모델 복원

때로는 소프트 삭제된 모델을 "삭제 취소"하고 싶을 수 있습니다. 소프트 삭제된 모델을 복원하려면 모델 인스턴스에서 `restore` 메서드를 호출하면 됩니다. `restore` 메서드는 모델의 `deleted_at` 컬럼을 `null`로 설정합니다.

```php
$flight->restore();
```

쿼리에서 `restore` 메서드를 사용하여 여러 모델을 복원할 수도 있습니다. 다시 말해, 다른 "대량" 작업과 마찬가지로 복원되는 모델에 대해 어떤 모델 이벤트도 디스패치하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

`restore` 메서드는 [연관관계](/docs/13.x/eloquent-relationships) 쿼리를 만들 때도 사용할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 모델 영구 삭제

때로는 데이터베이스에서 모델을 실제로 제거해야 할 수 있습니다. `forceDelete` 메서드를 사용하면 데이터베이스 테이블에서 소프트 삭제된 모델을 영구적으로 제거할 수 있습니다.

```php
$flight->forceDelete();
```
Eloquent 연관관계 쿼리를 구성할 때도 `forceDelete` 메서드를 사용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 쿼리하기

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제된 모델 포함하기

앞서 언급했듯이, 소프트 삭제된 모델은 쿼리 결과에서 자동으로 제외됩니다. 하지만 쿼리에서 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델도 쿼리 결과에 포함되도록 강제할 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

`withTrashed` 메서드는 [연관관계](/docs/13.x/eloquent-relationships) 쿼리를 구성할 때도 호출할 수 있습니다.

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 조회하기

`onlyTrashed` 메서드는 소프트 삭제된 모델만 조회합니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 정리하기 (Pruning Models)

때로는 더 이상 필요하지 않은 모델을 주기적으로 삭제하고 싶을 수 있습니다. 이를 위해 주기적으로 정리하려는 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가할 수 있습니다. 트레이트 중 하나를 모델에 추가한 뒤, 더 이상 필요하지 않은 모델을 찾는 Eloquent 쿼리 빌더를 반환하는 `prunable` 메서드를 구현합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

모델을 `Prunable`로 표시할 때, 모델에 `pruning` 메서드를 정의할 수도 있습니다. 이 메서드는 모델이 삭제되기 전에 호출됩니다. 이 메서드는 모델이 데이터베이스에서 영구적으로 제거되기 전에 저장된 파일처럼 모델과 연결된 추가 리소스를 삭제하는 데 유용합니다.

```php
/**
 * Prepare the model for pruning.
 */
protected function pruning(): void
{
    // ...
}
```

정리 가능한 모델을 설정한 후에는 애플리케이션의 `routes/console.php` 파일에서 `model:prune` Artisan 명령어를 예약해야 합니다. 이 명령어를 어떤 주기로 실행할지는 자유롭게 선택할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

내부적으로 `model:prune` 명령어는 애플리케이션의 `app/Models` 디렉터리 안에서 "Prunable" 모델을 자동으로 감지합니다. 모델이 다른 위치에 있다면 `--model` 옵션을 사용하여 모델 클래스 이름을 지정할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

감지된 다른 모든 모델은 정리하되 특정 모델만 정리 대상에서 제외하고 싶다면 `--except` 옵션을 사용할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션과 함께 `model:prune` 명령어를 실행하여 `prunable` 쿼리를 테스트할 수 있습니다. 가상 실행 모드에서는 `model:prune` 명령어가 실제로 실행되었을 때 몇 개의 레코드가 정리될지만 보고합니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제된 모델이 정리 대상 쿼리와 일치하면 영구 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 정리

모델에 `Illuminate\Database\Eloquent\MassPrunable` 트레이트가 표시되어 있으면, 모델은 대량 삭제 쿼리를 사용하여 데이터베이스에서 삭제됩니다. 따라서 `pruning` 메서드는 호출되지 않으며, `deleting` 및 `deleted` 모델 이벤트도 디스패치되지 않습니다. 이는 삭제 전에 모델을 실제로 조회하지 않기 때문이며, 그 결과 정리 과정이 훨씬 더 효율적입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

<a name="replicating-models"></a>
## 모델 복제하기 (Replicating Models)

`replicate` 메서드를 사용하여 기존 모델 인스턴스의 저장되지 않은 복사본을 만들 수 있습니다. 이 메서드는 동일한 속성을 많이 공유하는 모델 인스턴스가 있을 때 특히 유용합니다.

```php
use App\Models\Address;

$shipping = Address::create([
    'type' => 'shipping',
    'line_1' => '123 Example Street',
    'city' => 'Victorville',
    'state' => 'CA',
    'postcode' => '90001',
]);

$billing = $shipping->replicate()->fill([
    'type' => 'billing'
]);

$billing->save();
```

새 모델로 복제하지 않을 속성이 하나 이상 있다면 `replicate` 메서드에 배열을 전달할 수 있습니다.

```php
$flight = Flight::create([
    'destination' => 'LAX',
    'origin' => 'LHR',
    'last_flown' => '2020-03-04 11:00:00',
    'last_pilot_id' => 747,
]);

$flight = $flight->replicate([
    'last_flown',
    'last_pilot_id'
]);
```

<a name="query-scopes"></a>
## 쿼리 스코프 (Query Scopes)

<a name="global-scopes"></a>
### 전역 스코프

전역 스코프를 사용하면 특정 모델의 모든 쿼리에 제약 조건을 추가할 수 있습니다. Laravel의 [소프트 삭제](#soft-deleting) 기능도 전역 스코프를 활용하여 데이터베이스에서 "삭제되지 않은" 모델만 조회합니다. 직접 전역 스코프를 작성하면 특정 모델의 모든 쿼리에 일정한 제약 조건이 적용되도록 간편하게 보장할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성하기

새 전역 스코프를 생성하려면 `make:scope` Artisan 명령어를 실행할 수 있습니다. 생성된 스코프는 애플리케이션의 `app/Models/Scopes` 디렉터리에 배치됩니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 전역 스코프 작성하기

전역 스코프 작성은 간단합니다. 먼저 `make:scope` 명령어를 사용하여 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스를 생성합니다. `Scope` 인터페이스는 하나의 메서드인 `apply`를 구현하도록 요구합니다. `apply` 메서드는 필요에 따라 쿼리에 `where` 제약 조건이나 다른 종류의 절을 추가할 수 있습니다.

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Apply the scope to a given Eloquent query builder.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```

> [!NOTE]
> 전역 스코프가 쿼리의 select 절에 컬럼을 추가한다면 `select` 대신 `addSelect` 메서드를 사용해야 합니다. 이렇게 하면 쿼리에 이미 존재하는 select 절이 의도치 않게 대체되는 것을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
#### 전역 스코프 적용하기

모델에 전역 스코프를 지정하려면 모델에 `ScopedBy` 속성을 배치하기만 하면 됩니다.

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Attributes\ScopedBy;

#[ScopedBy([AncientScope::class])]
class User extends Model
{
    //
}
```

또는 모델의 `booted` 메서드를 오버라이드하고 모델의 `addGlobalScope` 메서드를 호출하여 전역 스코프를 수동으로 등록할 수 있습니다. `addGlobalScope` 메서드는 스코프 인스턴스 하나만 인수로 받습니다.

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 예제의 스코프를 `App\Models\User` 모델에 추가한 후 `User::all()` 메서드를 호출하면 다음 SQL 쿼리가 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 전역 스코프

Eloquent는 클로저를 사용하여 전역 스코프를 정의하는 것도 허용합니다. 이는 별도의 클래스를 만들 만큼 크지 않은 간단한 스코프에 특히 유용합니다. 클로저로 전역 스코프를 정의할 때는 `addGlobalScope` 메서드의 첫 번째 인수로 직접 선택한 스코프 이름을 제공해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope('ancient', function (Builder $builder) {
            $builder->where('created_at', '<', now()->minus(years: 2000));
        });
    }
}
```

<a name="removing-global-scopes"></a>
#### 전역 스코프 제거하기

특정 쿼리에서 전역 스코프를 제거하고 싶다면 `withoutGlobalScope` 메서드를 사용할 수 있습니다. 이 메서드는 전역 스코프의 클래스 이름 하나만 인수로 받습니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

또는 클로저를 사용하여 전역 스코프를 정의했다면, 전역 스코프에 지정한 문자열 이름을 전달해야 합니다.

```php
User::withoutGlobalScope('ancient')->get();
```

쿼리의 전역 스코프 여러 개 또는 전체를 제거하고 싶다면 `withoutGlobalScopes` 및 `withoutGlobalScopesExcept` 메서드를 사용할 수 있습니다.

```php
// Remove all of the global scopes...
User::withoutGlobalScopes()->get();

// Remove some of the global scopes...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// Remove all global scopes except the given ones...
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프를 사용하면 애플리케이션 전체에서 쉽게 재사용할 수 있는 공통 쿼리 제약 조건 묶음을 정의할 수 있습니다. 예를 들어 "인기 있는" 사용자로 간주되는 모든 사용자를 자주 조회해야 할 수 있습니다. 스코프를 정의하려면 Eloquent 메서드에 `Scope` 속성을 추가합니다.

스코프는 항상 동일한 쿼리 빌더 인스턴스 또는 `void`를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include popular users.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * Scope a query to only include active users.
     */
    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 사용하기

스코프가 정의되면 모델을 쿼리할 때 스코프 메서드를 호출할 수 있습니다. 여러 스코프 호출을 체이닝할 수도 있습니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` 쿼리 연산자를 통해 여러 Eloquent 모델 스코프를 결합하려면 올바른 [논리 그룹화](/docs/13.x/queries#logical-grouping)를 위해 클로저를 사용해야 할 수 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

하지만 이 방식은 번거로울 수 있으므로, Laravel은 클로저를 사용하지 않고도 스코프를 유창하게 체이닝할 수 있는 "고차" `orWhere` 메서드를 제공합니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프

때로는 매개변수를 받는 스코프를 정의하고 싶을 수 있습니다. 시작하려면 스코프 메서드의 시그니처에 추가 매개변수를 넣기만 하면 됩니다. 스코프 매개변수는 `$query` 매개변수 뒤에 정의해야 합니다.
```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include users of a given type.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

필요한 인수를 스코프 메서드의 시그니처에 추가한 뒤에는, 스코프를 호출할 때 해당 인수를 전달할 수 있습니다:

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 보류 중인 속성

스코프를 제한하는 데 사용한 속성과 동일한 속성을 가진 모델을 스코프로 생성하고 싶다면, 스코프 쿼리를 구성할 때 `withAttributes` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Scope the query to only include drafts.
     */
    #[Scope]
    protected function draft(Builder $query): void
    {
        $query->withAttributes([
            'hidden' => true,
        ]);
    }
}
```

`withAttributes` 메서드는 주어진 속성을 사용해 쿼리에 `where` 조건을 추가하며, 스코프를 통해 생성되는 모든 모델에도 해당 속성을 추가합니다:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes` 메서드가 쿼리에 `where` 조건을 추가하지 않도록 하려면, `asConditions` 인수를 `false`로 설정할 수 있습니다:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교 (Comparing Models)

두 모델이 "같은" 모델인지 확인해야 할 때가 있습니다. `is` 및 `isNot` 메서드를 사용하면 두 모델이 동일한 기본 키, 테이블, 데이터베이스 연결을 가지고 있는지 빠르게 확인할 수 있습니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is` 및 `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [연관관계](/docs/13.x/eloquent-relationships)를 사용할 때도 사용할 수 있습니다. 이 메서드는 관련 모델을 조회하기 위한 쿼리를 실행하지 않고도 해당 모델을 비교하고 싶을 때 특히 유용합니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트 (Events)

> [!NOTE]
> Eloquent 이벤트를 클라이언트 측 애플리케이션으로 직접 브로드캐스트하고 싶으신가요? Laravel의 [모델 이벤트 브로드캐스팅](/docs/13.x/broadcasting#model-broadcasting)을 확인해 보세요.

Eloquent 모델은 여러 이벤트를 디스패치하므로, 모델 생명주기의 다음 시점에 코드를 연결할 수 있습니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

`retrieved` 이벤트는 기존 모델이 데이터베이스에서 조회될 때 디스패치됩니다. 새 모델이 처음 저장될 때는 `creating` 및 `created` 이벤트가 디스패치됩니다. 기존 모델이 수정되고 `save` 메서드가 호출될 때는 `updating` / `updated` 이벤트가 디스패치됩니다. 모델이 생성되거나 업데이트될 때는, 모델의 속성이 변경되지 않았더라도 `saving` / `saved` 이벤트가 디스패치됩니다. `-ing`으로 끝나는 이벤트 이름은 모델의 변경 사항이 저장되기 전에 디스패치되고, `-ed`로 끝나는 이벤트는 변경 사항이 저장된 후에 디스패치됩니다.

모델 이벤트를 수신하려면 Eloquent 모델에 `$dispatchesEvents` 속성을 정의하세요. 이 속성은 Eloquent 모델 생명주기의 여러 지점을 직접 만든 [이벤트 클래스](/docs/13.x/events)에 매핑합니다. 각 모델 이벤트 클래스는 생성자를 통해 영향을 받은 모델 인스턴스를 받을 수 있어야 합니다:

```php
<?php

namespace App\Models;

use App\Events\UserDeleted;
use App\Events\UserSaved;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The event map for the model.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

Eloquent 이벤트를 정의하고 매핑한 후에는 [이벤트 리스너](/docs/13.x/events#defining-listeners)를 사용해 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent를 통해 대량 업데이트 또는 삭제 쿼리를 실행할 때는 영향을 받는 모델에 대해 `saved`, `updated`, `deleting`, `deleted` 모델 이벤트가 디스패치되지 않습니다. 대량 업데이트나 삭제를 수행할 때는 모델이 실제로 조회되지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 사용

커스텀 이벤트 클래스를 사용하는 대신, 다양한 모델 이벤트가 디스패치될 때 실행되는 클로저를 등록할 수 있습니다. 일반적으로 이러한 클로저는 모델의 `booted` 메서드에 등록해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면 모델 이벤트를 등록할 때 [큐에 넣을 수 있는 익명 이벤트 리스너](/docs/13.x/events#queueable-anonymous-event-listeners)를 활용할 수 있습니다. 이렇게 하면 Laravel이 애플리케이션의 [큐](/docs/13.x/queues)를 사용해 모델 이벤트 리스너를 백그라운드에서 실행합니다:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵저버

<a name="defining-observers"></a>
#### 옵저버 정의

특정 모델의 여러 이벤트를 수신하고 있다면, 옵저버를 사용해 모든 리스너를 하나의 클래스로 묶을 수 있습니다. 옵저버 클래스는 수신하려는 Eloquent 이벤트를 반영한 메서드 이름을 가집니다. 각 메서드는 영향을 받은 모델을 유일한 인수로 받습니다. 새 옵저버 클래스를 만드는 가장 쉬운 방법은 `make:observer` Artisan 명령어를 사용하는 것입니다:

```shell
php artisan make:observer UserObserver --model=User
```

이 명령어는 새 옵저버를 `app/Observers` 디렉터리에 배치합니다. 이 디렉터리가 없다면 Artisan이 자동으로 생성합니다. 새로 생성된 옵저버는 다음과 같습니다:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "updated" event.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "deleted" event.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "restored" event.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "forceDeleted" event.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버를 등록하려면 해당 모델에 `ObservedBy` 속성을 지정할 수 있습니다:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는 관찰하려는 모델에서 `observe` 메서드를 호출해 옵저버를 수동으로 등록할 수도 있습니다. 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 옵저버를 등록할 수 있습니다:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버가 수신할 수 있는 추가 이벤트도 있습니다. 예를 들어 `saving` 및 `retrieved` 같은 이벤트가 있습니다. 이러한 이벤트는 [이벤트](#events) 문서에서 설명합니다.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

데이터베이스 트랜잭션 안에서 모델이 생성되는 경우, 데이터베이스 트랜잭션이 커밋된 후에만 옵저버의 이벤트 핸들러가 실행되도록 하고 싶을 수 있습니다. 옵저버에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 이를 수행할 수 있습니다. 진행 중인 데이터베이스 트랜잭션이 없다면 이벤트 핸들러는 즉시 실행됩니다:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 음소거

모델에서 발생하는 모든 이벤트를 일시적으로 "음소거"해야 할 때가 있습니다. 이 작업은 `withoutEvents` 메서드를 사용해 수행할 수 있습니다. `withoutEvents` 메서드는 클로저를 유일한 인수로 받습니다. 이 클로저 안에서 실행되는 모든 코드는 모델 이벤트를 디스패치하지 않으며, 클로저가 반환하는 값은 `withoutEvents` 메서드가 그대로 반환합니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 이벤트 없이 단일 모델 저장

때로는 이벤트를 디스패치하지 않고 특정 모델을 "저장"하고 싶을 수 있습니다. 이 작업은 `saveQuietly` 메서드를 사용해 수행할 수 있습니다:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

이벤트를 디스패치하지 않고 특정 모델을 "업데이트", "삭제", "소프트 삭제", "복원", "복제"할 수도 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
