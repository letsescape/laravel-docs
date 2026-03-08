# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성하기](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블명](#table-names)
    - [기본키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결 설정](#database-connections)
    - [속성 기본값 지정](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회하기](#retrieving-models)
    - [컬렉션](#collections)
    - [결과를 청크로 분할해서 처리하기](#chunking-results)
    - [Lazy 컬렉션으로 청크 처리하기](#chunking-using-lazy-collections)
    - [커서(cursor) 사용하기](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계값 조회](#retrieving-aggregates)
- [모델 삽입 및 수정](#inserting-and-updating-models)
    - [데이터 삽입](#inserts)
    - [데이터 수정](#updates)
    - [대량 할당(Mass Assignment)](#mass-assignment)
    - [업서트(Upserts)](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제 모델 쿼리](#querying-soft-deleted-models)
- [모델 정리(Pruning)](#pruning-models)
- [모델 복제(Replicating)](#replicating-models)
- [쿼리 스코프(Scopes)](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [보류 중인 속성(Pending Attributes)](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저(Closure) 사용](#events-using-closures)
    - [옵저버(Observer)](#observers)
    - [이벤트 비활성화(muting)](#muting-events)

<a name="introduction"></a>
## 소개

Laravel은 Eloquent라는 객체-관계 매퍼(ORM)를 기본 제공하여, 데이터베이스와 쉽고 즐겁게 상호작용할 수 있도록 지원합니다. Eloquent를 사용할 때 데이터베이스의 각 테이블은 해당 테이블과 연결된 "모델"이 있으며, 이 모델을 통해 테이블에 접근합니다. Eloquent 모델을 사용하면 데이터베이스에서 레코드를 조회하는 것뿐만 아니라, 테이블에 레코드를 삽입, 수정, 삭제할 수 있습니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성해야 합니다. 데이터베이스 설정에 관한 더 자세한 내용은 [데이터베이스 구성 문서](/docs/12.x/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성하기

먼저, Eloquent 모델을 생성해보겠습니다. 모델은 보통 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. 새로운 모델을 생성하려면 `make:model` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다.

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/12.x/migrations)도 함께 생성하고 싶다면, `--migration` 또는 `-m` 옵션을 사용하세요.

```shell
php artisan make:model Flight --migration
```

모델과 함께 팩토리, 시더, 폴리시, 컨트롤러, 폼 요청과 같은 다양한 클래스들을 동시에 생성할 수도 있습니다. 필요하다면 여러 옵션을 결합해 다양한 클래스를 한꺼번에 만들 수 있습니다.

```shell
# 모델과 FlightFactory 클래스 생성...
php artisan make:model Flight --factory
php artisan make:model Flight -f

# 모델과 FlightSeeder 클래스 생성...
php artisan make:model Flight --seed
php artisan make:model Flight -s

# 모델과 FlightController 클래스 생성...
php artisan make:model Flight --controller
php artisan make:model Flight -c

# 모델, FlightController 리소스 클래스, 폼 요청 클래스를 함께 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러를 모두 생성...
php artisan make:model Flight -mfsc

# 모든 부속 클래스를 단축어로 생성(모델, 마이그레이션, 팩토리, 시더, 폴리시, 컨트롤러, 폼 요청)...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗(pivot) 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 속성 및 관계 확인

모델의 코드만 훑어봐서는 해당 모델이 갖고 있는 모든 속성과 관계를 한눈에 파악하기 어려울 때가 있습니다. 이럴 때, Artisan의 `model:show` 명령어를 이용하면 모델의 속성과 연관관계를 종합적으로 확인할 수 있습니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치하게 됩니다. 기본적인 모델 클래스를 살펴보며 Eloquent의 주요 관례를 알아봅시다.

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
### 테이블명

위 예제에서 우리는 `Flight` 모델이 어느 데이터베이스 테이블과 연결되는지 별도로 명시하지 않았습니다. Eloquent는 기본적으로 클래스명을 "스네이크 케이스(snake case)"로 변환하고, 복수형을 사용해 테이블명을 지정합니다. 즉, `Flight` 모델은 자동으로 `flights` 테이블에, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 연결된다고 간주합니다.

만약 모델에 해당하는 데이터베이스 테이블명이 이 관례와 다르다면, 모델에서 직접 `table` 속성을 정의해 테이블명을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델과 연관된 테이블명
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
### 기본키

Eloquent는 기본적으로 각 모델의 테이블이 `id`라는 이름의 기본키 컬럼을 가진다고 가정합니다. 만약 다른 컬럼을 기본키로 사용하고 싶다면, 모델에 `protected $primaryKey` 속성을 정의하여 원하는 컬럼명을 지정하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델과 연관된 기본키
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

또한 Eloquent는 기본키가 자동 증가하는 정수값이라고 가정해서, 기본키를 자동으로 정수형으로 변환합니다. 만약 자동 증가하지 않거나 숫자가 아닌 기본키를 사용하고 싶다면, `public $incrementing` 속성을 `false`로 지정해야 합니다.

```php
<?php

class Flight extends Model
{
    /**
     * 기본키가 자동 증가하는지 여부
     *
     * @var bool
     */
    public $incrementing = false;
}
```

기본키가 정수형이 아니면, `protected $keyType` 속성에 `'string'`을 지정해야 합니다.

```php
<?php

class Flight extends Model
{
    /**
     * 기본키 타입
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
#### 복합 기본키(Composite Primary Keys)

Eloquent 모델은 적어도 하나의 고유한 "ID" 값을 기본키로 갖는 것을 전제로 합니다. 복합 기본키(여러 컬럼을 조합한 기본키)는 Eloquent 모델에서는 지원하지 않습니다. 단, 복수 컬럼을 가진 고유 인덱스는 테이블에 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본키로 자동 증가 정수 대신 UUID(범용 고유 식별자)를 사용할 수도 있습니다. UUID는 36자리의 영숫자 문자열입니다.

만약 자동 증가 정수 대신 UUID를 기본키로 사용하고 싶다면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 추가하세요. 물론, 모델의 테이블에 [UUID 타입의 기본키 컬럼](/docs/12.x/migrations#column-method-uuid)이 있어야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUuids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Europe']);

$article->id; // "8f8e8478-9035-4d23-b9a7-62f4d2612ce5"
```

기본적으로 `HasUuids` 트레이트는 ["순서가 보장되는(ordered)" UUID](/docs/12.x/strings#method-str-ordered-uuid)를 생성합니다. 순서가 보장되는 UUID는 인덱싱된 데이터베이스에서 정렬이 효율적입니다.

UUID 생성 과정을 사용자 정의하려면, 모델에 `newUniqueId` 메서드를 정의하면 됩니다. 또한, 어떤 컬럼에 UUID를 적용할지 지정하고 싶다면, 모델에 `uniqueIds` 메서드를 정의할 수 있습니다.

```php
use Ramsey\Uuid\Uuid;

/**
 * 모델의 새 UUID 생성
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * UUID를 적용할 컬럼명을 반환
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```

원한다면 UUID 대신 ULID(26자리 영숫자 식별자) 사용도 가능합니다. ULID 역시 정렬이 용이하여 인덱싱에 효율적입니다. ULID를 적용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 사용하고, 테이블에 [ULID 타입의 기본키 컬럼](/docs/12.x/migrations#column-method-ulid)이 있어야 합니다.

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

Eloquent는 기본적으로 모델의 테이블에 `created_at`과 `updated_at` 컬럼이 있다고 가정합니다. 모델이 생성되거나 수정될 때 이 컬럼 값은 자동으로 관리됩니다. Eloquent가 해당 컬럼을 자동으로 관리하지 않도록 하려면, 모델에서 `$timestamps` 속성을 `false`로 지정하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 타임스탬프를 사용할지 여부
     *
     * @var bool
     */
    public $timestamps = false;
}
```

타임스탬프의 데이터 저장 형식을 지정하고 싶다면 `$dateFormat` 속성을 사용하세요. 이 속성은 데이터베이스에 날짜 컬럼을 저장하는 포맷뿐 아니라, 모델이 배열이나 JSON으로 직렬화될 때의 포맷에도 영향을 줍니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 날짜 컬럼 저장 포맷
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

타임스탬프 컬럼명을 커스터마이징하려면, 모델에 `CREATED_AT` 및 `UPDATED_AT` 상수를 정의하세요.

```php
<?php

class Flight extends Model
{
    /**
     * 생성 시각 컬럼명
     *
     * @var string|null
     */
    public const CREATED_AT = 'creation_date';

    /**
     * 수정 시각 컬럼명
     *
     * @var string|null
     */
    public const UPDATED_AT = 'updated_date';
}
```

모델의 `updated_at` 타임스탬프 변경 없이 작업을 수행하고 싶다면, `withoutTimestamps` 메서드에 클로저를 전달해 해당 코드 블록 내에서 타임스탬프 변경 없이 모델 작업을 실행할 수 있습니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결 설정

기본적으로 모든 Eloquent 모델은 애플리케이션에서 지정된 기본 데이터베이스 연결을 사용합니다. 특정 모델에 대해 별도의 데이터베이스 연결을 지정하려면, 모델의 `$connection` 속성에 연결명을 지정하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델이 사용할 데이터베이스 연결명
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
### 속성 기본값 지정

모델 인스턴스를 새로 만들 때, 기본적으로 어떤 속성값도 포함하지 않습니다. 특정 속성에 기본값을 지정하고 싶다면 모델의 `$attributes` 속성에 배열로 지정할 수 있습니다. 이 배열의 값은 데이터베이스에 저장된 형태와 동일해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 속성의 기본값 지정
     *
     * @var array
     */
    protected $attributes = [
        'options' => '[]',
        'delayed' => false,
    ];
}
```

<a name="configuring-eloquent-strictness"></a>
### Eloquent 엄격성 설정

Laravel은 Eloquent의 동작 및 "엄격성(strictness)"을 상황에 따라 설정할 수 있는 다양한 메서드를 제공합니다.

먼저, `preventLazyLoading` 메서드는 지연 로딩(lazy loading)을 허용할지 여부를 결정합니다. 예를 들어, 운영 환경에서는 실수로 지연 로딩된 연관관계가 코드에 섞여 있더라도 정상 동작을 유지하고 싶을 수 있습니다. 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 주로 호출합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

또한 `preventSilentlyDiscardingAttributes` 메서드를 통해, 모델의 `fillable` 배열에 없는 속성을 할당하려 할 때 예외를 발생시키도록 할 수 있습니다. 이는 로컬 개발 환경에서 원하지 않는 속성이 조용히 무시되어 버그가 생기는 것을 방지할 수 있습니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기

모델과 [연관된 데이터베이스 테이블](/docs/12.x/migrations#generating-migrations)이 준비되면, 데이터베이스에서 데이터를 조회할 수 있습니다. 각각의 Eloquent 모델은 강력한 [쿼리 빌더](/docs/12.x/queries)처럼 동작하여 해당 모델이 연결된 테이블을 유연하게 쿼리할 수 있습니다. 예를 들어, 모델의 `all` 메서드는 연관된 테이블의 모든 레코드를 조회합니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성하기

Eloquent의 `all` 메서드는 해당 테이블의 모든 결과를 반환합니다. 하지만 Eloquent 모델은 [쿼리 빌더](/docs/12.x/queries) 역할도 하므로, 조건을 추가하여 원하는 레코드만 조회할 수 있습니다. 조건을 추가한 후에는 `get` 메서드를 호출하여 결과를 가져옵니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델이 쿼리 빌더 역할을 하므로, Laravel의 [쿼리 빌더](/docs/12.x/queries)가 제공하는 모든 메서드를 활용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 새로고침

데이터베이스에서 조회한 Eloquent 모델 인스턴스를 보유한 경우, `fresh` 및 `refresh` 메서드를 이용해 모델 정보를 갱신할 수 있습니다. `fresh` 메서드는 데이터베이스에서 새로 모델을 조회하여 반환하나, 기존 인스턴스는 변경하지 않습니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 기존 인스턴스 자체를 데이터베이스의 최신 값으로 재적용(re-hydrate) 하며, 이미 로드된 모든 연관관계도 함께 갱신합니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

앞서 본 것처럼, Eloquent의 `all` 혹은 `get` 메서드는 여러 레코드를 반환하지만, 이 값이 일반적인 PHP 배열이 아니라 `Illuminate\Database\Eloquent\Collection` 인스턴스가 됩니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 컬렉션 클래스인 `Illuminate\Support\Collection`을 확장하며, 데이터를 다룰 때 유용한 [다양한 메서드](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드를 이용해 클로저의 조건에 맞는 모델을 컬렉션에서 제외할 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Laravel의 기본 컬렉션 메서드 외에도, Eloquent 컬렉션만을 위한 [추가 메서드](/docs/12.x/eloquent-collections#available-methods)들이 있습니다.

모든 Laravel 컬렉션은 PHP의 반복자 인터페이스(iterable)를 구현하므로, 배열처럼 순회할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과를 청크로 분할해서 처리하기

`all` 또는 `get` 메서드로 수만~수십만개의 Eloquent 레코드를 한 번에 불러오면, 애플리케이션의 메모리가 부족해질 수 있습니다. 이런 경우, `chunk` 메서드를 사용하면, 모델을 일정 단위(청크, chunk)로 나눠서 효율적으로 처리할 수 있습니다.

`chunk` 메서드는 일부 모델들만 불러와서, 클로저로 전달합니다. 즉, 한번에 전체 데이터를 메모리에 올리지 않으므로 메모리 사용량이 크게 감소합니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

첫 번째 인자는 청크당 가져올 레코드 개수이며, 두 번째 인자로 넘기는 클로저가 청크별로 실행됩니다. 각각의 청크마다 데이터베이스 쿼리가 실행되며, 각 레코드를 클로저 내부에서 처리할 수 있습니다.

만약 청크 처리 중, 기준이 되는 컬럼을 업데이트하면서 쿼리를 필터링한다면, 일반 `chunk` 대신 `chunkById` 메서드를 사용해야 예기치 못한 결과를 막을 수 있습니다. `chunkById`는 내부적으로 `id` 컬럼이 이전 청크의 마지막 모델보다 큰 레코드만 조회하도록 쿼리를 구성합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`나 `lazyById` 메서드는 쿼리에 자체적으로 "where" 조건을 추가하므로, 직접 추가하는 조건은 클로저로 [논리 그룹화](/docs/12.x/queries#logical-grouping)해야 합니다.

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
### Lazy 컬렉션으로 청크 처리하기

`lazy` 메서드는 내부적으로 [chunk 메서드](#chunking-results)와 비슷하게 쿼리를 청크 단위로 실행합니다. 그러나, 각각의 청크를 콜백으로 바로 넘기지 않고, 평탄화(flatten)된 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환하여, 결과를 하나의 스트림 처럼 다룰 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

역시 청크 중 필터 기준 컬럼을 변경할 경우, `lazyById`를 사용하세요.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 이용하면 `id` 컬럼 내림차순 기반으로 결과를 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서(cursor) 사용하기

`lazy` 메서드처럼, `cursor` 메서드를 사용해 수만~수십만 건의 Eloquent 모델을 반복처리할 때 메모리 점유를 최소화할 수 있습니다.

`cursor` 메서드는 데이터베이스 쿼리를 한 번만 실행하지만, 실제로 값을 순회할 때마다 한 개씩 모델을 "하이드레이트(hydrate)"하여 하나씩만 메모리에 보관합니다.

> [!WARNING]
> `cursor` 메서드는 오직 한 개의 Eloquent 모델만 메모리에 유지하기 때문에, 관계(eager loading)는 불가능합니다. 관계를 미리 로드하려면 [lazy 메서드](#chunking-using-lazy-collections)를 이용하세요.

내부적으로 `cursor` 메서드는 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 활용합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor` 메서드는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/12.x/collections#lazy-collections)을 활용하면, 각 모델을 한 번에 하나씩만 메모리에 올리면서 일반 컬렉션 메서드 활용이 가능합니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 단일 모델만 메모리에 잡으므로 메모리 사용량이 매우 적지만, [PHP의 PDO 드라이버가 쿼리의 원본 결과를 내부 버퍼에 계속 저장하기 때문에](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php) 데이터가 굉장히 많아지면 결국 메모리 부족이 발생할 수 있습니다. 이런 상황에서는 [lazy 메서드](#chunking-using-lazy-collections) 사용을 고려하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 Select

Eloquent는 고급 서브쿼리 지원도 제공합니다. 이를 통해 관련 테이블의 정보를 한 번의 쿼리로 가져올 수 있습니다. 예를 들어, `destinations`(목적지) 테이블과 해당 목적지로 향하는 `flights` 테이블이 있다고 가정해 봅니다. `flights` 테이블에는 목적지 도착 시간을 나타내는 `arrived_at` 컬럼이 있습니다.

`select` 및 `addSelect` 메서드에 서브쿼리 기능을 활용해, 각 목적지의 가장 최근에 온 항공편의 이름을 불러올 수 있습니다.

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

쿼리 빌더의 `orderBy` 역시 서브쿼리를 지원합니다. 위 예제를 이어서, 각 목적지에 마지막으로 도착한 비행 시간 순으로 목적지를 정렬할 수도 있습니다. 역시 한 번의 쿼리로 처리됩니다.

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
## 단일 모델/집계 조회

주어진 조건에 맞는 여러 레코드 전체가 아닌, 단일 레코드만 반환받고 싶을 때는 `find`, `first`, `firstWhere` 메서드를 사용할 수 있습니다. 이들은 컬렉션 대신 한 개의 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

// 기본키로 모델 조회...
$flight = Flight::find(1);

// 조건에 맞는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 조건식 기반 첫 번째 모델 조회(대체 방법)...
$flight = Flight::firstWhere('active', 1);
```

조회 결과가 없을 때 다른 작업을 수행하고 싶다면, `findOr`, `firstOr` 메서드를 사용하면 됩니다. 이들은 결과가 있으면 단일 모델 인스턴스를, 없으면 주어진 클로저를 실행합니다. 클로저의 반환값이 메서드의 반환값이 됩니다.

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
#### Not Found 예외

경로(route)나 컨트롤러에서 모델이 없을 때 자동으로 예외를 발생시키고 싶다면, `findOrFail`, `firstOrFail` 메서드를 사용할 수 있습니다. 조회 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외가 발생합니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`이 별도로 처리되지 않으면, 클라이언트에 404 HTTP 응답이 자동으로 반환됩니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값 쌍으로 데이터베이스 레코드를 찾으려 시도합니다. 만약 해당 레코드가 존재하지 않으면, 첫 번째 배열(조건)과 두 번째 배열(추가 속성값)을 병합해서 새로운 레코드를 생성·저장합니다.

그리고 `firstOrNew` 메서드는 `firstOrCreate`처럼 조건에 맞는 레코드를 찾으려 하나, 없을 경우 새 모델 인스턴스만 반환합니다(데이터베이스에는 저장하지 않음). 따라서 `firstOrNew`로 반환된 모델을 저장하려면 `save` 메서드를 직접 호출해야 합니다.

```php
use App\Models\Flight;

// 이름으로 조회, 없으면 새로 생성...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 이름·지연여부·도착시간으로 생성...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 그냥 새 Flight 인스턴스 반환...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 이름으로 조회, 없으면 추가 속성값으로 인스턴스 반환...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계값 조회

Eloquent 모델과 상호작용할 때, Laravel [쿼리 빌더](/docs/12.x/queries)가 제공하는 `count`, `sum`, `max` 등 [집계 메서드](/docs/12.x/queries#aggregates)도 그대로 사용할 수 있습니다. 이 메서드들은 Eloquent 모델 인스턴스 대신 보통의 스칼라 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 수정

<a name="inserts"></a>
### 데이터 삽입

Eloquent를 통해 데이터베이스에서 모델을 조회하는 것뿐 아니라, 새로운 레코드를 삽입할 수 있습니다. 새로운 레코드를 추가하려면 모델 인스턴스를 생성하고, 필요한 속성을 채운 뒤 `save` 메서드를 호출하세요.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 새로운 항공편 데이터 저장
     */
    public function store(Request $request): RedirectResponse
    {
        // 요청 유효성 검증...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```

위 예제에서 HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당합니다. 그리고 `save`를 호출하면 레코드가 삽입됩니다. 이 때, `created_at`, `updated_at` 타임스탬프는 자동으로 기록되어 별도 설정이 필요 없습니다.

또한 `create` 메서드를 이용하면 한 줄의 PHP 코드로 모델을 "저장"할 수 있습니다. 이 때 새로 저장된 모델 인스턴스가 반환됩니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 사용 전 모델에 `fillable`이나 `guarded` 속성을 정의해야 합니다. 이는 Eloquent 모델이 기본적으로 대량 할당 보안 취약점을 막기 위해 필요합니다. 대량 할당에 관한 자세한 내용은 [mass assignment 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 데이터 수정

`save` 메서드는 이미 존재하는 모델을 수정(업데이트)할 때도 사용할 수 있습니다. 수정하려는 모델을 먼저 조회하고, 원하는 속성을 변경한 후, 모델의 `save`를 호출하세요. 마찬가지로 `updated_at` 타임스탬프는 자동으로 업데이트됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

기존 모델이 있다면 수정하고, 없으면 새로 생성해야 하는 경우도 있습니다. 이때는 `firstOrCreate`처럼, `updateOrCreate` 메서드를 사용할 수 있습니다. 이 메서드는 저장까지 수행하므로, 추가적으로 `save`를 호출할 필요가 없습니다.

아래 예에서는 출발지가 `Oakland`이고 목적지가 `San Diego`인 항공편이 있다면 그 모델의 `price`와 `discounted` 컬럼이 수정됩니다. 만약 해당하는 항공편이 없으면 두 배열 인자를 병합한 값으로 새로 생성됩니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

`firstOrCreate`나 `updateOrCreate`처럼, 모델이 새로 만들어졌는지 수정되었는지 구분할 필요가 있다면, `wasRecentlyCreated` 속성을 확인할 수 있습니다.

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // 새 항공편 레코드가 삽입됨...
}
```

<a name="mass-updates"></a>
#### 대량 수정(Mass Updates)

특정 조건을 만족하는 여러 모델을 한 번에 수정할 수도 있습니다. 예를 들어, `active`이고 `destination`이 `San Diego`인 모든 항공편을 지연 처리하려면 다음과 같이 합니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 수정할 컬럼과 값 쌍의 배열을 받습니다. 반환값은 수정된 행(row)의 개수입니다.

> [!WARNING]
> Eloquent로 대량 수정 시, 해당 모델들에 대해 `saving`, `saved`, `updating`, `updated` 이벤트가 발생하지 않습니다. 이는 실제로 모델이 조회되지 않고 바로 쿼리만 실행되기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변경 탐지

Eloquent는 모델의 내부 상태를 파악할 수 있도록 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다. 이를 이용해 모델이 언제, 어떤 속성이 변경됐는지 확인할 수 있습니다.

`isDirty` 메서드는 모델이 데이터베이스에서 조회된 이후 어떤 속성이 변경되었는지 확인합니다. 특정 속성명을 넘기면 해당 속성만 검사할 수 있습니다. `isClean`은 지정한 속성이 변경되지 않았는지 검사합니다.

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

`wasChanged` 메서드는 최근에 저장(save)된 후 변경된 속성이 있는지 확인합니다. 필요하면 특정 속성명을 인자로 전달해서 그 속성만 검사할 수 있습니다.

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

`getOriginal` 메서드는 모델이 조회된 직후의 원본 속성값 배열을 반환합니다. 특정 속성명을 넘기면 해당 속성의 원래 값을 반환합니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 속성 전체 배열 반환...
```

`getChanges` 메서드는 마지막 저장 시점에 변경된 모든 속성을 배열로 반환합니다. `getPrevious`는 직전 저장 전에 가지고 있었던 속성값을 반환합니다.

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
### 대량 할당(Mass Assignment)

`create` 메서드를 사용하면 한 줄의 PHP 코드로 모델을 저장할 수 있습니다. 이때 반환값은 새로 만들어진 모델 인스턴스입니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 사용 전 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 이는 기본적으로 모든 Eloquent 모델이 대량 할당 취약점으로부터 보호되기 때문입니다.

대량 할당 취약점은 사용자가 예기치 않은 HTTP 필드를 전달해서, 의도하지 않은 데이터베이스 컬럼이 변경되는 상황을 의미합니다. 예를 들어, 악의적인 사용자가 `is_admin`이라는 파라미터를 요청에 전달해, 모델의 `create` 메서드에 주입시켜 자신을 관리자 권한으로 바꿀 수 있습니다.

따라서, 어떤 모델 속성을 대량 할당 허용할지 `$fillable` 속성으로 지정해야 합니다. 예를 들어, `Flight` 모델의 `name` 속성만 대량 할당 허용하려면 다음과 같이 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 대량 할당이 허용된 속성
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

허용된 속성만 지정했다면 다음과 같이 간단하게 레코드를 생성할 수 있습니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있을 때는 `fill` 메서드를 사용해 속성값을 채울 수 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼에 값을 대량 할당할 때는 해당 컬럼의 키를 `$fillable` 배열에 명확히 지정해야 합니다. 보안을 이유로, Laravel은 `guarded`를 사용할 경우 중첩된 JSON 속성 대량 업데이트는 지원하지 않습니다.

```php
/**
 * 대량 할당이 허용된 속성
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
#### 모든 속성 대량 할당 허용

모든 속성을 대량 할당 허용하고 싶다면, 모델의 `$guarded` 속성을 빈 배열로 지정할 수 있습니다. 다만, 이렇게 설정하면 반드시 `fill`, `create`, `update`에 전달하는 데이터를 항상 신중하게 직접 구성해야 합니다.

```php
/**
 * 대량 할당이 금지된 속성
 *
 * @var array<string>|bool
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외

기본적으로 `$fillable` 배열에 없는 속성은 대량 할당 시 조용히 무시됩니다. 운영 환경에서는 이 동작이 주로 기대되지만, 개발 환경에서는 모델이 왜 변경되지 않는지 혼란을 줄 수 있습니다.

원한다면, `preventSilentlyDiscardingAttributes` 메서드를 호출해 허용되지 않은 속성을 할당하려 할 때 에러가 나도록 할 수 있습니다. 보통은 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
### 업서트(Upserts)

Eloquent의 `upsert` 메서드를 사용하여 레코드를 한 번의 원자적(atomic) 연산으로 "업데이트 또는 삽입"할 수 있습니다. 첫 번째 인자는 삽입하거나 업데이트할 값이며, 두 번째 인자는 테이블에서 레코드를 고유하게 식별할 컬럼입니다. 세 번째 인자는 일치하는 레코드가 있을 때 업데이트할 컬럼 목록입니다. 타임스탬프가 활성화된 모델이라면 자동으로 `created_at`, `updated_at`이 갱신됩니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 메서드의 두 번째 인자(고유 컬럼)에 "기본키"나 "유니크" 인덱스가 있어야 합니다. MariaDB와 MySQL의 경우 두 번째 인자를 무시하고 항상 테이블의 "기본키"와 "유니크" 인덱스를 기준으로 기존 레코드 여부를 판단합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면, 인스턴스에서 `delete` 메서드를 호출하세요.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본키로 기존 모델 삭제

위 예제에서는 먼저 모델을 조회한 후 `delete`를 호출하지만, 기본키를 알고 있다면 `destroy` 메서드로 별도의 조회 없이 바로 삭제가 가능합니다. 이 메서드는 기본키 하나, 여러 개, 배열, 또는 [컬렉션](/docs/12.x/collections)도 인자로 받을 수 있습니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)을 사용할 경우, 모델을 완전히 삭제하려면 `forceDestroy` 메서드를 사용할 수 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 내부적으로 각 모델을 별도 조회한 후 `delete`를 호출하여, 모델별 `deleting` 및 `deleted` 이벤트가 정상 발생하도록 처리합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

쿼리를 작성하여 조건에 맞는 모든 모델을 한꺼번에 삭제할 수도 있습니다. 예를 들어, 비활성(`active=0`) 항공편을 모두 삭제하려면 다음과 같이 할 수 있습니다. 대량 삭제 역시 모델 이벤트는 발생하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블의 모든 레코드를 삭제하려면 조건 없이 `query()` 사용 후 `delete`를 호출하세요.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent의 대량 삭제 실행 시, 삭제되는 모델에 대해 `deleting` 및 `deleted` 이벤트가 발생하지 않습니다. 이는 삭제 쿼리에 실제로 모델이 조회되지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

실제로 데이터를 데이터베이스에서 완전히 삭제하는 대신, Eloquent는 "소프트 삭제"도 지원합니다. 소프트 삭제된 모델은 삭제된 것이 아니라, `deleted_at` 속성에 삭제 시각만 기록하고 테이블에 그대로 남아 있게 됩니다. 소프트 삭제를 활성화하려면, 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하세요.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime`/`Carbon` 객체로 변환해줍니다.

데이터베이스 테이블에도 `deleted_at` 컬럼이 필요합니다. Laravel [스키마 빌더](/docs/12.x/migrations)의 헬퍼 메서드를 이용해 손쉽게 추가할 수 있습니다.

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

이제 모델에서 `delete`를 호출하면, 해당 레코드의 `deleted_at` 컬럼에 현재 시각이 기록됩니다. 하지만 데이터는 테이블에 남아 있습니다. 이 상태에서 해당 모델을 조회하면, 자동으로 소프트 삭제된 데이터는 결과에서 제외됩니다.

모델 인스턴스가 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복원

가끔 소프트 삭제된 모델을 "살려내고" 싶을 때가 있습니다. 모델 인스턴스에서 `restore` 메서드를 호출하면 `deleted_at` 컬럼이 `null`로 설정되어 복원이 이뤄집니다.

```php
$flight->restore();
```

여러 모델을 한꺼번에 복원하고 싶다면 쿼리로도 가능합니다. 역시 대량 복원 작업에는 모델 이벤트가 발생하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[연관관계](/docs/12.x/eloquent-relationships) 쿼리에도 `restore`를 사용할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 모델 완전 삭제(영구 삭제)

진짜로 데이터베이스에서 모델을 완전히 삭제해야 할 때는 `forceDelete` 메서드를 사용합니다. 소프트 삭제 모델의 경우 실제 데이터까지 영구적으로 삭제합니다.

```php
$flight->forceDelete();
```

Eloquent 연관관계 쿼리에서도 `forceDelete`를 사용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제 모델 쿼리

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 데이터 포함하여 조회

기본적으로 소프트 삭제된 모델은 쿼리 결과에서 자동으로 제외됩니다. 하지만, 쿼리에서 `withTrashed` 메서드를 호출하면 소프트 삭제 데이터도 결과에 포함할 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

[연관관계](/docs/12.x/eloquent-relationships) 쿼리에서도 사용 가능합니다.

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제 데이터만 조회

`onlyTrashed` 메서드를 사용하면, **소프트 삭제된 모델만** 조회할 수 있습니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 정리(Pruning)

더 이상 필요하지 않은 모델을 주기적으로 삭제하고 싶을 때가 있습니다. 이를 위해, 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가하고, 더 이상 필요 없는 레코드를 선택하는 `prunable` 메서드를 구현하면 됩니다.

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
     * 정리가 필요한 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

모델에 `Prunable` 트레이트를 적용했다면, 필요한 경우 `pruning` 메서드를 정의해 삭제 전에 파일 등 부가 리소스를 정리할 수도 있습니다.

```php
/**
 * 정리(Pruning) 전 모델 준비
 */
protected function pruning(): void
{
    // ...
}
```

정리 대상 모델을 준비했다면, `routes/console.php`에 `model:prune` Artisan 명령어를 일정 주기로 스케줄링하세요.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령어는 자동으로 `app/Models` 디렉터리 내의 "Prunable" 모델을 검색합니다. 다른 위치에 있는 경우 `--model` 옵션을 이용해 클래스명을 직접 지정할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 제외하고 나머지만 정리하고 싶으면 `--except` 옵션을 사용합니다.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` 옵션을 사용하면 실제 삭제 없이, 삭제될 레코드 개수만 출력되어 쿼리를 테스트할 수 있습니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델도, 정리(Pruning) 쿼리에 포함되면 완전히 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 정리(Mass Pruning)

`Illuminate\Database\Eloquent\MassPrunable` 트레이트를 사용하는 경우, 정리는 "대량 삭제" 쿼리 방식으로 처리되어 성능이 더 탁월합니다. 이 방식에선 `pruning` 메서드는 호출되지 않고, `deleting` 및 `deleted` 모델 이벤트도 발생하지 않습니다. 실제로 삭제 전에 모델을 조회하지 않기 때문입니다.

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
     * 정리가 필요한 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

<a name="replicating-models"></a>
## 모델 복제(Replicating)

기존 모델과 대부분 속성이 동일한 새로운 모델을 만들고 싶다면, `replicate` 메서드를 이용해 저장되지 않은 새로운 복제본을 쉽게 만들 수 있습니다.

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

특정 속성만 제외한 채 복제하려면, 제외할 속성명 배열을 `replicate` 메서드에 전달하면 됩니다.

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
## 쿼리 스코프(Scopes)

<a name="global-scopes"></a>
### 글로벌 스코프

글로벌 스코프는 특정 모델에 대해 항상 쿼리 조건을 추가할 수 있도록 돕는 기능입니다. Laravel의 [소프트 삭제](#soft-deleting) 역시 글로벌 스코프를 활용해, 자동으로 "삭제되지 않은" 데이터만 조회하도록 구성합니다. 직접 글로벌 스코프를 작성해 모델 쿼리에 공통 조건을 쉽게 적용할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성하기

새 글로벌 스코프를 생성하려면, `make:scope` Artisan 명령어를 이용해 `app/Models/Scopes` 폴더에 스코프 클래스를 생성하세요.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 구현하기

글로벌 스코프를 구현하는 방법은 간단합니다. `make:scope` 명령으로 생성한 클래스는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하며, 반드시 `apply` 메서드를 작성해야 합니다. `apply` 메서드에서는 필요에 따라 `where` 또는 다양한 쿼리 절을 추가할 수 있습니다.

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Eloquent 쿼리 빌더에 스코프 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프에서 쿼리의 select 절에 컬럼을 추가할 때는 `select` 대신 `addSelect` 메서드를 사용하세요. 기존 select 절이 의도치 않게 덮어써지는 것을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용하기

글로벌 스코프를 모델에 적용하려면, 모델 클래스에 `ScopedBy` 속성(attribute)을 붙이세요.

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

또는, 모델의 `booted` 메서드를 오버라이드하여 `addGlobalScope`를 직접 호출해 등록할 수도 있습니다.

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

이처럼 스코프를 `App\Models\User` 모델에 적용하면, `User::all()` 호출 시 아래와 같은 SQL 쿼리가 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명(Anonymous) 글로벌 스코프

Eloquent는 별도 클래스를 만들 필요 없이 간단한 글로벌 스코프는 클로저(closure)로도 정의할 수 있습니다. 이때 `addGlobalScope` 메서드의 첫 번째 인자로 고유한 스코프 이름을 문자열로 지정해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
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
#### 글로벌 스코프 제거

특정 쿼리에서 글로벌 스코프를 제거하고 싶다면 `withoutGlobalScope` 메서드를 사용하세요. 이때 인자로는 글로벌 스코프의 클래스명을 넘깁니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저로 정의했다면, 등록한 스코프 이름을 문자열로 넘기면 됩니다.

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개의 글로벌 스코프를 한꺼번에(혹은 모두) 제거하고 싶을 때는 `withoutGlobalScopes` 또는 `withoutGlobalScopesExcept` 메서드를 사용하세요.

```php
// 모든 글로벌 스코프 제거
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 제거
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// 특정 글로벌 스코프만 유지하고 나머지 제거
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 애플리케이션 내에서 자주 사용하는 쿼리 조건 집합을 메서드로 만들어, 반복적으로 사용할 수 있도록 하는 기능입니다. 예를 들어 "인기있는 사용자"를 자주 조회한다면, Eloquent 메서드에 `Scope` 속성을 붙여 별도의 스코프를 만들어 재사용할 수 있습니다.

스코프는 항상 같은 쿼리 빌더 인스턴스나 `void`를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기있는 사용자만 쿼리
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자만 쿼리
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

스코프를 정의했다면, 쿼리 시 스코프 메서드를 그대로 체이닝하여 호출할 수 있습니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 스코프를 `or`(또는) 조건으로 결합할 때는 [논리 그룹화](/docs/12.x/queries#logical-grouping)를 위해 클로저를 써야 할 수도 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

이러한 방식이 번거롭다면, Laravel의 "고차원(higher order)" `orWhere` 문법을 사용해 좀 더 간결하게 스코프를 연속해서 쓸 수 있습니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적 스코프(Dynamic Scopes)

매개변수를 받아서 동적으로 작동하는 스코프도 만들 수 있습니다. `$query` 인자 다음에 추가 매개변수를 선언하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 주어진 타입의 사용자만 쿼리
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

스코프 메서드가 인자를 받게 만들었다면, 쿼리 시 해당 값만 넘겨주면 됩니다.

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 보류 중인 속성(Pending Attributes)

스코프를 활용해, 쿼리에 썼던 조건을 모델 생성 시 기본 속성으로도 지정하고 싶다면 `withAttributes` 메서드를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 임시글(초안)만 쿼리
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

`withAttributes` 메서드는, 지정한 속성으로 쿼리에 자동으로 `where` 조건을 추가하고, 해당 스코프로 생성된 모델에도 동일한 속성값을 할당합니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes` 메서드가 쿼리에 `where` 조건을 추가하지 않게 하려면 `asConditions` 인자를 `false`로 설정하세요.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교

두 모델이 "동일한" 모델인지 비교해야 하는 경우가 있습니다. `is` 및 `isNot` 메서드를 사용해 두 모델이 동일한 기본키, 테이블, 데이터베이스 연결을 갖는 모델인지 쉽게 판별할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is` 및 `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [연관관계](/docs/12.x/eloquent-relationships)에서도 사용이 가능합니다. 쿼리를 추가로 발행하지 않고도 연관모델을 비교하고 싶을 때 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 애플리케이션에 직접 브로드캐스팅하고 싶으신가요? Laravel의 [모델 이벤트 브로드캐스팅](/docs/12.x/broadcasting#model-broadcasting)을 참고하세요.

Eloquent 모델은 여러 이벤트를 발행하여 모델의 라이프사이클에서 다양한 시점에 후킹할 수 있도록 해줍니다. 지원하는 이벤트로는 `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating` 등이 있습니다.

* `retrieved`: 기존 모델이 데이터베이스에서 조회될 때 발생
* `creating`/`created`: 새 모델이 처음 저장될 때 이벤트 발생
* `updating`/`updated`: 기존 모델이 수정되고 save 메서드가 호출될 때 발생
* `saving`/`saved`: 모델이 생성 또는 수정(저장)될 때, 속성이 변경되지 않아도 발생
* 이벤트 이름이 `-ing`로 끝나면 변경 전, `-ed`로 끝나면 변경 후에 이벤트가 발생합니다.

모델 이벤트에 반응하려면, 모델의 `$dispatchesEvents` 속성에 이벤트 매핑을 지정하세요. 각 이벤트 클래스는 생성자를 통해 변경된 모델 인스턴스를 전달 받을 수 있습니다.

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
     * 모델 이벤트 매핑
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

Eloquent 이벤트를 정의해 매핑했다면, [이벤트 리스너](/docs/12.x/events#defining-listeners)를 작성해 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent에서 대량 수정/삭제 쿼리를 실행할 경우, 해당 모델의 `saved`, `updated`, `deleting`, `deleted` 이벤트는 발생하지 않습니다. 실제로 쿼리만 실행되고 모델이 조회되지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저(Closure) 사용

별도의 이벤트 클래스 대신, 다양한 모델 이벤트 발생 시 실행되는 클로저를 등록할 수도 있습니다. 주로 모델의 `booted` 메서드 안에서 이런 클로저를 등록합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델의 "booted" 메서드
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면 [큐잉 가능한 익명 이벤트 리스너](/docs/12.x/events#queuable-anonymous-event-listeners)를 활용해, 모델 이벤트 리스너가 애플리케이션의 [큐](/docs/12.x/queues)에서 백그라운드로 실행되도록 할 수도 있습니다.

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### 옵저버(Observer)

<a name="defining-observers"></a>
#### 옵저버 정의하기

특정 모델에 대해 여러 이벤트를 처리해야 한다면, 옵저버 클래스로 리스너들을 모아둘 수 있습니다. 옵저버 클래스는 처리하고자 하는 Eloquent 이벤트명과 일치하는 메서드를 구현하며, 각 메서드는 영향을 받는 모델을 인자로 받습니다. 새 옵저버 클래스 생성은 `make:observer` Artisan 명령어로 손쉽게 할 수 있습니다.

```shell
php artisan make:observer UserObserver --model=User
```

명령어를 실행하면 `app/Observers` 디렉터리에 옵저버가 생성됩니다. 디렉터리가 없다면 자동으로 생성됩니다. 예시는 아래와 같습니다.

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User "created" 이벤트 처리
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User "updated" 이벤트 처리
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User "deleted" 이벤트 처리
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User "restored" 이벤트 처리
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User "forceDeleted" 이벤트 처리
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버를 등록하려면, 모델에 `ObservedBy` 속성을 추가하면 됩니다.

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는, 원하는 경우 `observe` 메서드를 호출해 직접 옵저버를 등록할 수 있습니다. 이 방식은 `AppServiceProvider`의 `boot` 메서드에서 사용됩니다.

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 서비스 부트스트랩.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버에서 감지 가능한 추가 이벤트(예: `saving`, `retrieved`)가 있으며, 자세한 내용은 [이벤트 문서](#events)를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델 생성 등이 데이터베이스 트랜잭션 내에서 일어난다면, 트랜잭션 커밋 이후에만 옵저버의 이벤트 핸들러를 실행하도록 설정할 수 있습니다. 옵저버 클래스에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 됩니다. 트랜잭션이 없으면 이벤트는 즉시 실행됩니다.

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트 처리
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 비활성화(muting)

특정 코드 블록에서 임시로 모델 이벤트를 "비활성화"하고 싶을 수 있습니다. 이때는 `withoutEvents` 메서드에 클로저를 전달해, 내부 코드에서 발생하는 모델 이벤트가 무시되도록 할 수 있습니다(클로저의 반환값이 그대로 반환됨).

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델 이벤트 없이 저장

특정 모델을 이벤트 발생 없이 저장하고 싶을 때는 `saveQuietly` 메서드를 사용하세요.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

마찬가지로, "update", "delete", "soft delete", "restore", "replicate"에도 `Quietly` 접미사가 붙은 메서드를 사용할 수 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
