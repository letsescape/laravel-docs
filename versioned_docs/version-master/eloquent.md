# Eloquent: 시작하기 (Eloquent: Getting Started)

- [소개](#introduction)
- [모델 클래스 생성](#generating-model-classes)
- [Eloquent 모델 관례](#eloquent-model-conventions)
    - [테이블 이름](#table-names)
    - [기본 키](#primary-keys)
    - [UUID 및 ULID 키](#uuid-and-ulid-keys)
    - [타임스탬프](#timestamps)
    - [데이터베이스 연결](#database-connections)
    - [기본 속성 값](#default-attribute-values)
    - [Eloquent 엄격성 설정](#configuring-eloquent-strictness)
- [모델 조회하기](#retrieving-models)
    - [컬렉션](#collections)
    - [결과 청크 처리](#chunking-results)
    - [Lazy 컬렉션으로 청크 처리](#chunking-using-lazy-collections)
    - [커서](#cursors)
    - [고급 서브쿼리](#advanced-subqueries)
- [단일 모델/집계 조회](#retrieving-single-models)
    - [모델 조회 또는 생성](#retrieving-or-creating-models)
    - [집계 조회](#retrieving-aggregates)
- [모델 삽입 및 업데이트](#inserting-and-updating-models)
    - [삽입](#inserts)
    - [업데이트](#updates)
    - [대량 할당](#mass-assignment)
    - [Upsert](#upserts)
- [모델 삭제](#deleting-models)
    - [소프트 삭제](#soft-deleting)
    - [소프트 삭제된 모델 조회](#querying-soft-deleted-models)
- [모델 정리](#pruning-models)
- [모델 복제](#replicating-models)
- [쿼리 스코프](#query-scopes)
    - [글로벌 스코프](#global-scopes)
    - [로컬 스코프](#local-scopes)
    - [대기 중 속성](#pending-attributes)
- [모델 비교](#comparing-models)
- [이벤트](#events)
    - [클로저 활용](#events-using-closures)
    - [옵저버](#observers)
    - [이벤트 음소거](#muting-events)

<a name="introduction"></a>
## 소개

Laravel에는 데이터베이스와의 상호작용을 즐겁게 만들어주는 객체 관계 매퍼(ORM)인 Eloquent가 포함되어 있습니다. Eloquent를 사용하면 데이터베이스의 각 테이블마다 그 테이블과 상호작용하는 "모델"이 존재하게 됩니다. Eloquent 모델을 통해 데이터베이스 테이블에서 레코드를 조회할 뿐만 아니라, 삽입, 업데이트, 삭제 작업도 가능합니다.

> [!NOTE]
> 시작 전에, 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 반드시 구성해야 합니다. 데이터베이스 설정에 대한 자세한 내용은 [데이터베이스 설정 문서](/docs/master/database#configuration)를 참고하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

먼저, Eloquent 모델을 생성해봅시다. 모델은 일반적으로 `app\Models` 디렉토리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. 새로운 모델을 생성하려면, `make:model` [Artisan 명령어](/docs/master/artisan)를 사용하면 됩니다.

```shell
php artisan make:model Flight
```

모델을 생성할 때 [데이터베이스 마이그레이션](/docs/master/migrations)도 함께 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다.

```shell
php artisan make:model Flight --migration
```

모델 생성 시, 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트 등 다양한 종류의 클래스를 동시에 생성할 수도 있습니다. 이 옵션들은 조합하여 여러 클래스를 한 번에 만들 수 있습니다.

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

# 모델, FlightController 리소스 클래스, 폼 리퀘스트 클래스 생성...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# 모델과 FlightPolicy 클래스 생성...
php artisan make:model Flight --policy

# 모델, 마이그레이션, 팩토리, 시더, 컨트롤러 생성...
php artisan make:model Flight -mfsc

# 모델, 마이그레이션, 팩토리, 시더, 정책, 컨트롤러, 폼 리퀘스트까지 한 번에 생성...
php artisan make:model Flight --all
php artisan make:model Flight -a

# 피벗 모델 생성...
php artisan make:model Member --pivot
php artisan make:model Member -p
```

<a name="inspecting-models"></a>
#### 모델 속성 및 관계 확인

모델의 모든 사용 가능한 속성과 연관관계를 코드만 훑어보아서는 파악하기 어려울 때가 있습니다. 이럴 때는, 모델의 모든 속성과 관계를 한눈에 확인할 수 있도록 `model:show` Artisan 명령어를 활용해보세요.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent 모델 관례

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉토리에 위치합니다. 아래는 기본적인 모델 클래스 예제이며, Eloquent의 주요 관례를 살펴보겠습니다.

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

위의 예제에서, Eloquent에게 `Flight` 모델이 어떤 데이터베이스 테이블과 연결되는지 별도로 알려주지 않아도 된다는 점을 알 수 있습니다. Eloquent는 기본적으로 클래스 이름을 "스네이크 케이스(snake case)"로 변환한 복수형을 테이블 이름으로 사용합니다. 즉, 위의 경우, `Flight` 모델은 `flights` 테이블과 연결된다고 간주합니다. 만약 `AirTrafficController` 모델이라면 `air_traffic_controllers` 테이블과 연결됩니다.

만약 모델이 연결될 데이터베이스 테이블이 이러한 관례를 따르지 않는다면, `Table` 속성을 이용해 테이블 이름을 명시적으로 지정할 수 있습니다.

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

Eloquent는 각 모델과 연결된 테이블에 `id`라는 기본 키 컬럼이 있다고 가정합니다. 필요하다면, `Table` 속성의 `key` 인수를 통해 모델의 기본 키 컬럼명을 변경할 수 있습니다.

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

또한 Eloquent는 기본 키가 자동 증가하는 정수형(integer)이라고 가정해서, 해당 키를 자동으로 정수형으로 변환합니다. 만약 자동 증가하지 않거나 숫자가 아닌 값(예: UUID 등)을 기본 키로 사용하고 싶다면, `Table` 속성의 `keyType`, `incrementing` 인수를 활용하세요.

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

<a name="composite-primary-keys"></a>
#### "복합" 기본 키

Eloquent의 모델은 적어도 하나의 고유 식별 가능한 "ID"를 기본 키로 가져야 합니다. Eloquent는 "복합(Composite)" 기본 키를 공식적으로 지원하지 않습니다. 그러나 테이블의 주요 기본 키 외에, 복수 컬럼에 대해 유니크 인덱스를 자유롭게 추가할 수는 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

일반적인 auto-increment 정수형 기본 키 대신, UUID를 Eloquent 모델의 기본 키로 사용할 수도 있습니다. UUID는 36자의 길이를 가진 유일성 보장 알파벳-숫자 조합 식별자입니다.

UUID 키를 사용하려면, 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 추가합니다. 또한, 해당 모델이 [UUID에 적합한 컬럼](/docs/master/migrations#column-method-uuid)을 기본 키로 사용하고 있는지 확인해야 합니다.

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

기본적으로 `HasUuids` 트레이트는 ["정렬 가능한(ordered)" UUID](/docs/master/strings#method-str-ordered-uuid)를 생성하는데, 이 UUID는 데이터베이스 인덱싱 시 더 효율적으로 사용됩니다(사전순 정렬 가능).

UUID 생성 방식을 오버라이드(재정의)하려면 모델에 `newUniqueId` 메서드를 정의하면 되고, 특정 컬럼만 UUID를 할당받게 하려면 `uniqueIds` 메서드를 정의할 수 있습니다.

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

원한다면, UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 유사하지만 길이가 26자이며, 마찬가지로 사전순 정렬이 가능해서 인덱스 작업에 효율적입니다. ULID 사용 시에는 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 모델에 사용하세요. 그리고 모델에 [ULID에 적합한 컬럼](/docs/master/migrations#column-method-ulid)이 존재하도록 설정해야 합니다.

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

Eloquent는 기본적으로 각 테이블에 `created_at`, `updated_at` 컬럼이 존재할 것으로 가정합니다. 모델이 생성되거나 업데이트될 때, 이 컬럼의 값이 자동으로 관리됩니다. 만약 이러한 컬럼들이 자동으로 관리되기를 원하지 않는다면, 모델의 `Table` 속성에서 `timestamps`를 `false`로 지정하세요.

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

타임스탬프의 저장 포맷을 변경하고 싶다면, `dateFormat` 인수를 활용하여 지정할 수 있습니다. 이 값은 데이터베이스에 저장될 때와 모델이 배열 또는 JSON으로 직렬화될 때의 포맷 형식에 영향을 줍니다.

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

타임스탬프 컬럼의 이름 역시 커스터마이즈할 수 있습니다. 모델에 `CREATED_AT`, `UPDATED_AT` 상수를 정의하면 됩니다.

```php
<?php

class Flight extends Model
{
    /**
     * 생성 시각 컬럼 이름.
     *
     * @var string|null
     */
    public const CREATED_AT = 'creation_date';

    /**
     * 수정 시각 컬럼 이름.
     *
     * @var string|null
     */
    public const UPDATED_AT = 'updated_date';
}
```

`updated_at` 타임스탬프가 변경되지 않게 모델 작업을 수행하려면, `withoutTimestamps` 메서드에 클로저를 전달하면 됩니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션에서 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델에 대해 다른 연결을 지정하려면, `Connection` 속성을 활용할 수 있습니다.

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

새로 인스턴스화된 모델에는 기본적으로 어떤 속성 값도 담겨 있지 않습니다. 일부 속성에 대한 기본 값을 지정하고 싶다면, 모델에 `$attributes` 프로퍼티를 정의하세요. `$attributes` 배열에 지정된 값은 데이터베이스에서 바로 읽은 원본, 즉 "저장 가능한(storable)" 포맷으로 작성되어야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * 모델 기본 속성 값.
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

Laravel은 다양한 상황에서 Eloquent의 동작과 "엄격성(strictness)"을 설정할 수 있는 여러 메서드를 제공합니다.

예를 들어 `preventLazyLoading` 메서드는 지연 로딩(lazy loading)을 막을지 여부를 지정하는 불리언 인수를 받습니다. 주로 비(非)프로덕션 환경에서만 지연 로딩을 금지하도록 설정하기도 합니다. 보통 이 메서드는 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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

또한, `preventSilentlyDiscardingAttributes` 메서드를 호출하면 Eloquent에 "일괄 할당 불가"한 속성을 채우려 할 때 예외를 던지도록 할 수 있습니다. 이는 모델의 `fillable` 배열에 미리 추가하지 않은 속성 할당 시, 예상치 못한 에러를 미연에 방지하는 데 도움이 됩니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## 모델 조회하기

모델과 [연관된 데이터베이스 테이블](/docs/master/migrations#generating-migrations)을 생성했다면, 이제 데이터베이스에서 데이터를 읽어올 수 있습니다. 각각의 Eloquent 모델은 강력한 [쿼리 빌더](/docs/master/queries)로써, 해당 모델이 연결된 데이터베이스 테이블을 유연하게 조회할 수 있습니다. 예를 들어, 모델의 `all` 메서드는 해당 테이블의 전체 레코드를 조회합니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### 쿼리 작성하기

Eloquent의 `all` 메서드는 테이블의 모든 결과를 반환합니다. 하지만 Eloquent 모델은 [쿼리 빌더](/docs/master/queries)로 동작하므로, 쿼리에 조건을 추가한 후 `get` 메서드로 결과를 조회할 수 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이기도 하므로, Laravel [쿼리 빌더](/docs/master/queries)가 제공하는 모든 메서드를 함께 사용할 수 있습니다. Eloquent 쿼리를 작성할 때 참고해 보세요.

<a name="refreshing-models"></a>
#### 모델 갱신(새로고침)

이미 데이터베이스에서 조회한 Eloquent 모델 인스턴스가 있다면, `fresh` 및 `refresh` 메서드로 모델을 새로고침할 수 있습니다. `fresh` 메서드는 모델을 데이터베이스에서 다시 읽어 새 인스턴스를 반환하며, 기존 인스턴스에는 영향을 주지 않습니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` 메서드는 현재 인스턴스 자체에 대해 데이터베이스에서 최신 데이터를 가져와 재할당합니다. 또한 이미 로드된 연관관계도 모두 갱신됩니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### 컬렉션

앞서 보았듯이, Eloquent의 `all` 및 `get` 메서드는 데이터베이스에서 여러 레코드를 가져옵니다. 그러나 이 메서드들은 일반 PHP 배열이 아닌, `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 확장하여, 데이터 컬렉션을 쉽게 조작할 수 있도록 [다양한 유틸리티 메서드](/docs/master/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드를 사용하여 클로저의 반환값에 따라 컬렉션에서 모델을 제거할 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

기본 컬렉션 클래스의 메서드 외에도, Eloquent 컬렉션에는 [Eloquent 모델 컬렉션 조작에 특화된 메서드](/docs/master/eloquent-collections#available-methods)도 포함되어 있습니다.

Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하므로, 일반 배열처럼 `foreach`문 등으로 순회할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### 결과 청크 처리

수만 건에 이르는 Eloquent 레코드를 `all`이나 `get` 메서드로 한 번에 메모리에 로딩하면 애플리케이션 메모리가 부족해질 수 있습니다. 이런 대량의 데이터를 효율적으로 처리하려면 `chunk` 메서드를 활용하세요.

`chunk`는 일정 개수만큼의 Eloquent 모델을 한 번에 가져오며, 각 청크(chunk)가 클로저에 전달되어 처리됩니다. 현재 청크에 해당하는 레코드만 메모리에 로드되기 때문에, 아주 많은 데이터를 다루더라도 메모리 사용을 크게 줄일 수 있습니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

`chunk` 메서드의 첫 번째 인수는 한 번에 가져올 레코드 개수입니다. 두 번째 인수의 클로저는, 데이터베이스에서 읽어온 각 청크마다 실행됩니다.

조회 결과를 기반으로, 동시에 특정 컬럼(예: `active`)을 업데이트해야 한다면 `chunk` 대신 `chunkById` 메서드를 사용하세요. `chunk`를 사용할 경우, 의도치 않은 결과나 이상한 동작이 발생할 수 있습니다. `chunkById`는 내부적으로 이전 청크의 마지막 모델보다 `id` 값이 큰 레코드만 새로 조회하는 방식을 사용합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById`, `lazyById` 메서드는 where 조건을 자체적으로 추가하므로, 직접 추가한 조건들끼리 [논리적 그룹](/docs/master/queries#logical-grouping)으로 묶어주는 것이 좋습니다.

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
### Lazy 컬렉션으로 청크 처리

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게, 내부적으로 쿼리를 청크 단위로 실행합니다. 하지만, 각각의 청크를 바로 콜백으로 전달하지 않고, Eloquent 모델들을 플랫(flat)한 [LazyCollection](/docs/master/collections#lazy-collections) 형태로 반환합니다. 따라서 하나의 스트림처럼 결과를 다룰 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

Lazy 컬렉션 처리 중, 동시에 컬럼을 업데이트해야 한다면 `lazyById` 메서드를 사용하세요. 이 메서드는 항상 이전 청크의 마지막 모델보다 `id` 값이 큰 레코드만 가져옵니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` 메서드를 이용하면, `id`의 내림차순으로 결과를 필터링할 수도 있습니다.

<a name="cursors"></a>
### 커서

`lazy` 메서드처럼, `cursor` 메서드도 수만 건의 Eloquent 모델을 반복 처리할 때 애플리케이션 메모리 사용량을 최소화할 수 있습니다.

`cursor` 메서드는 오직 한 번만 데이터베이스 쿼리를 실행합니다. 그러나 실제로 데이터가 순회(반복)될 때마다 Eloquent 모델이 하나씩 하이드레이트(hydrate) 되어, 항상 한 번에 하나의 모델만 메모리에 존재하게 됩니다.

> [!WARNING]
> `cursor` 메서드는 한 번에 한 모델만 메모리에 유지하기 때문에, 관계 미리 로딩(eager load)이 불가능합니다. 관계를 미리 로딩해야 한다면 [lazy 메서드](#chunking-using-lazy-collections)를 고려하세요.

내부적으로는 PHP [generator](https://www.php.net/manual/en/language.generators.overview.php)를 사용합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy 컬렉션](/docs/master/collections#lazy-collections)을 통해, 일반 Laravel 컬렉션에서 사용할 수 있는 많은 메서드를 단일 모델만 메모리에 올리면서 활용할 수 있습니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` 메서드는 일반 쿼리보다 메모리 사용량이 훨씬 적지만, 결국에는 [PHP의 PDO 드라이버가 내부적으로 모든 쿼리 결과를 버퍼에 캐싱하기 때문에](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php) 언젠가는 메모리가 소진될 수 있습니다. 아주 대량의 데이터를 처리한다면 [lazy 메서드](#chunking-using-lazy-collections)를 사용하세요.

<a name="advanced-subqueries"></a>
### 고급 서브쿼리

<a name="subquery-selects"></a>
#### 서브쿼리 Select

Eloquent는 고급 서브쿼리 기능을 제공하여, 단 한 번의 쿼리로 연관 테이블의 정보를 읽어올 수 있습니다. 예를 들어, `destinations` 테이블과 `flights` 테이블이 있고, `flights` 테이블은 항공편이 도착한 시각을 의미하는 `arrived_at` 컬럼을 가지고 있다고 가정해보겠습니다.

`select`, `addSelect` 메서드의 서브쿼리 기능을 활용하면, 각 `destinations`와 그 목적지에 가장 최근 도착한 항공편의 이름을 하나의 쿼리로 조회할 수 있습니다.

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

또한 쿼리 빌더의 `orderBy` 함수도 서브쿼리를 지원합니다. 예제처럼, 각 목적지에 마지막으로 도착한 항공편의 도착 시각 기준으로 `destinations`를 정렬할 수 있습니다.

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

주어진 쿼리와 일치하는 모든 레코드를 조회하는 것 외에도, `find`, `first`, `firstWhere` 같은 메서드를 이용해 단일 모델 인스턴스를 조회할 수도 있습니다.

```php
use App\Models\Flight;

// 기본 키로 모델 조회...
$flight = Flight::find(1);

// 쿼리 조건과 일치하는 첫 번째 모델 조회...
$flight = Flight::where('active', 1)->first();

// 쿼리 조건과 일치하는 첫 번째 모델(대안) 조회...
$flight = Flight::firstWhere('active', 1);
```

결과가 없는 경우 다른 작업을 하고 싶은 상황에는 `findOr`, `firstOr` 메서드를 활용할 수 있습니다. 이 메서드들은 결과가 없으면 지정한 클로저를 실행하고, 해당 반환값을 결과로 반환합니다.

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

모델이 조회되지 않았을 때 예외를 던지고 싶을 때도 있습니다. 이 동작은 주로 라우트 또는 컨트롤러에서 유용합니다. `findOrFail`, `firstOrFail` 메서드는 결과가 없을 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 던집니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException`이 포착되지 않으면 자동으로 404 HTTP 응답이 클라이언트에 전송됩니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### 모델 조회 또는 생성

`firstOrCreate` 메서드는 주어진 컬럼/값 쌍에 일치하는 데이터베이스 레코드를 찾으려 시도합니다. 해당 모델이 없으면, 첫 번째 배열(조건)과 두 번째 배열(기본 속성)을 병합하여 레코드를 삽입합니다.

`firstOrNew` 메서드는 `firstOrCreate`와 유사하지만, 모델을 찾지 못하면 새 모델 인스턴스만 반환하며 데이터베이스에는 아직 저장하지 않습니다. 직접 `save` 메서드를 호출해야 저장됩니다.

```php
use App\Models\Flight;

// 이름으로 항공편을 조회, 없으면 생성...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// 이름, 지연, 도착 시각 속성으로 생성...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// 이름으로 조회, 없으면 새 인스턴스 반환...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// 속성까지 포함하여 새 인스턴스 반환...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```

<a name="retrieving-aggregates"></a>
### 집계 조회

Eloquent를 사용할 때도, Laravel [쿼리 빌더](/docs/master/queries)가 제공하는 `count`, `sum`, `max` 등 [집계 메서드](/docs/master/queries#aggregates)를 그대로 사용할 수 있습니다. 이 메서드들은 Eloquent 모델 인스턴스 대신 스칼라 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 업데이트

<a name="inserts"></a>
### 삽입

Eloquent를 사용할 때는 데이터베이스로부터 모델을 조회하는 것뿐만 아니라, 새로운 레코드를 삽입해야 할 때도 있습니다. 이 작업은 매우 간단하게 처리할 수 있습니다. 데이터베이스에 새 레코드를 삽입하려면, 새로운 모델 인스턴스를 생성하고, 속성 값을 지정한 뒤 `save` 메서드를 호출하세요.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * 데이터베이스에 새 항공편을 저장
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

이 예제에서는, HTTP 요청 본문에서 전달된 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당했습니다. `save` 메서드를 호출하면 데이터베이스에 해당 레코드가 추가됩니다. `created_at` 및 `updated_at` 타임스탬프는 자동으로 설정되므로 수동으로 지정할 필요가 없습니다.

PHP 한 줄로 새 모델을 "저장"하려면 `create` 메서드를 사용할 수도 있습니다. `create` 메서드는 삽입된 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

단, `create` 메서드를 사용하려면 모델 클래스에 `Fillable` 또는 `Guarded` 속성을 반드시 지정해야 합니다. 이는 Eloquent 모델이 기본적으로 "대량 할당 취약점"을 방지하도록 보호되는 구조이기 때문입니다. 자세한 내용은 [대량 할당 문서](#mass-assignment)를 참고하세요.

<a name="updates"></a>
### 업데이트

`save` 메서드는 이미 데이터베이스에 존재하는 모델을 업데이트하는 데에도 사용됩니다. 업데이트하려면 모델을 조회 후, 원하는 속성 값을 새로 설정하고 `save` 메서드를 호출하세요. 이때도 `updated_at` 타임스탬프는 자동으로 갱신되니 별도로 신경 쓸 필요가 없습니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

경우에 따라, 기존 모델을 업데이트하거나 없는 경우 새로 생성해야 할 때도 있습니다. `firstOrCreate`와 유사한 방식으로, `updateOrCreate` 메서드는 해당 모델이 없으면 새로 생성, 있으면 업데이트한 뒤 항상 저장까지 완료해줍니다.

아래 예제에서는, `departure`가 `Oakland`이고 `destination`이 `San Diego`인 항공편이 이미 존재하면 `price`, `discounted` 컬럼을 업데이트합니다. 해당 레코드가 없다면 두 배열을 병합한 값으로 새 레코드를 만듭니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

이런 `firstOrCreate`, `updateOrCreate` 같은 메서드를 사용하면, 새 모델이 생성됐는지 아니면 기존 모델이 업데이트됐는지 구분하기 어려울 수 있습니다. 이럴 때는 `wasRecentlyCreated` 속성으로 판단할 수 있습니다.

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // 새 항공편 레코드가 삽입됨...
}
```

<a name="mass-updates"></a>
#### 대량 업데이트

쿼리와 일치하는 모든 모델에 대해 대량 업데이틀 할 수도 있습니다. 아래 예제에서는, `active`가 1이고 `destination`이 `San Diego`인 모든 항공편을 지연(delayed) 처리합니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` 메서드는 '컬럼-값' 쌍의 배열을 받아 해당 컬럼을 일괄 업데이트하며, 반환값으로 영향을 받은 행(row)의 수를 제공합니다.

> [!WARNING]
> Eloquent를 통한 대량 업데이트 시에는, `saving`, `saved`, `updating`, `updated` 모델 이벤트가 **발생하지 않습니다**. 이는 실제 모델 인스턴스를 조회하지 않고 직접 쿼리만 날리기 때문입니다.

<a name="examining-attribute-changes"></a>
#### 속성 변동점 확인

Eloquent는 모델의 내부 상태 변화를 확인할 수 있는 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

- `isDirty` : 모델이 조회된 이후로 속성 값이 변경됐는지 확인합니다. 특정 속성명을 인자로 넘기거나 배열로 여러 속성을 전달하면, 해당 속성이 하나라도 변경되었는지 검사합니다.
- `isClean` : 속성이 변하지 않았는지 확인합니다. 역시 속성명(또는 배열)을 받을 수 있습니다.

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

- `wasChanged` : 마지막으로 `save`한 이후 속성이 변경됐는지 여부를 반환합니다. 특정 속성명을 넘기면 해당 속성만 검사합니다.

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

- `getOriginal` : 모델이 처음 조회됐을 때의 원본 속성 배열을 반환합니다. 특정 속성명을 넘기면 해당 값만 원본에서 추출합니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // 원본 전체 배열...
```

- `getChanges` : 마지막 저장 시점에서 변경된 속성만 배열로 반환합니다.  
- `getPrevious` : 이전 저장 시점의 원본 값을 배열로 반환합니다.

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

`create` 메서드를 이용해 새로운 모델을 PHP 한 줄로 "저장"할 수 있습니다. 삽입된 모델 인스턴스가 반환됩니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

이때도 모델 클래스에 `Fillable` 또는 `Guarded` 속성(어트리뷰트)을 반드시 지정해야 합니다. Eloquent 모델은 기본적으로 "대량 할당 취약점"에 대비해 보호되어 있기 때문입니다.

대량 할당 취약점이란, 사용자가 예상하지 못한 HTTP 요청 필드를 전달해, 데이터베이스의 의도치 않은 컬럼이 변경되는 것을 의미합니다. 예를 들어, 악의적인 사용자가 `is_admin` 파라미터를 보내면, `create` 메서드로 인해 해당 계정이 관리자로 승격될 수 있습니다.

따라서, 모델에서 어떤 속성이 대량 할당될 수 있는지 명확히 지정해야 합니다. `Fillable` 속성을 통해, 예를 들어 `Flight` 모델의 `name` 속성만 대량 할당이 가능하도록 할 수 있습니다.

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

대량 할당 가능한 속성을 지정했다면, 이제 `create` 메서드로 데이터를 배열로 받아 데이터베이스에 쉽게 삽입할 수 있습니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

이미 모델 인스턴스가 있다면, `fill` 메서드를 사용해 값을 채울 수도 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 대량 할당과 JSON 컬럼

JSON 컬럼을 대량 할당하는 경우, 대량 할당 가능한 키(대부분 '->' 형태로 지정)는 모델의 `Fillable` 속성에 반드시 명시해야 합니다. 보안을 위해, `Guarded` 속성을 사용할 때는 JSON 내부의 중첩 키에 대한 대량 할당이 지원되지 않습니다.

```php
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['options->enabled'])]
class Flight extends Model
{
    // ...
}
```

<a name="allowing-mass-assignment"></a>
#### 대량 할당 전면 허용

모든 속성을 대량 할당 가능하게 하려면, `Unguarded` 속성을 모델에 부여할 수 있습니다. 단, 이 경우 `fill`, `create`, `update` 메서드에 전달되는 배열을 항상 수작업으로 신중하게 관리해야 합니다.

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

기본적으로 `Fillable` 속성에 포함되지 않은 컬럼은 대량 할당 시 조용히 무시됩니다. 프로덕션에서는 이 동작이 일반적이지만, 개발 중에는 모델 변경이 적용되지 않은 이유로 혼란스러울 수 있습니다.

원한다면, 대량 할당이 불가능한 속성을 채우려고 할 때 예외를 던지도록 하려면, `preventSilentlyDiscardingAttributes` 메서드를 호출하세요. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 호출합니다.

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
### Upsert

Eloquent의 `upsert` 메서드는 원자적(atomic)으로 레코드를 업데이트하거나 새로 생성할 수 있습니다. 첫 번째 인수에는 삽입 또는 업데이트할 값들(여러 배열의 배열), 두 번째 인수에는 해당 테이블에서 레코드를 고유하게 식별할 컬럼명 배열, 세 번째 인수에는 기존 레코드가 있다면 업데이트할 컬럼 배열을 지정합니다. `upsert` 메서드는 타임스탬프(`created_at`, `updated_at`)도 자동으로 설정합니다(모델에 타임스탬프 기능이 활성화된 경우).

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는, `upsert`의 두 번째 인수 컬럼(고유 조건)이 반드시 "primary" 또는 "unique" 인덱스로 명시되어 있어야 합니다. MariaDB, MySQL에서는 두 번째 인수를 무시하고 테이블의 전체 "primary/unique 인덱스"로 기존 레코드 존재 여부를 판단합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면, 해당 모델 인스턴스의 `delete` 메서드를 호출하면 됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제

위 예제처럼, 먼저 DB에서 모델을 조회한 후 삭제할 수도 있지만, 기본 키를 알고 있다면 `destroy` 메서드로 조회 없이 바로 삭제할 수 있습니다. `destroy` 메서드는 하나의 기본 키 외에도, 여러 개, 배열, [컬렉션](/docs/master/collections) 형식의 키도 받아들입니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[소프트 삭제 모델](#soft-deleting)을 사용할 경우, `forceDestroy` 메서드로 완전히 삭제할 수 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 개별적으로 모델을 조회한 뒤 `delete` 메서드를 호출합니다. 이는 각 모델에 대해 `deleting`, `deleted` 이벤트가 올바르게 발생할 수 있도록 하기 위함입니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리로 모델 삭제

물론, 쿼리 조건에 따라 일치하는 모든 모델을 한 번에 삭제할 수도 있습니다. 아래 예제는 `active`가 0인 모든 항공편을 삭제합니다. 대량 삭제와 마찬가지로, 이때는 삭제된 모델에 대한 이벤트가 발생하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

테이블의 모든 데이터(모델)를 삭제하려면 조건 없이 쿼리를 실행하세요.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent로 대량 삭제 명령을 실행하면, 해당 모델에 대해 `deleting`, `deleted` 모델 이벤트가 **발생하지 않습니다**. 이는 실제로 모델을 조회하지 않고 쿼리만 실행하기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

실제 데이터베이스에서 레코드를 완전히 삭제하는 것 대신, Eloquent는 "소프트 삭제" 기능을 제공합니다. 소프트 삭제 시, 데이터베이스에서 해당 레코드는 남아 있고, `deleted_at` 컬럼이 현재 시간으로 채워져 "삭제됨" 상태를 나타냅니다. 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하여 소프트 삭제 기능을 활성화할 수 있습니다.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` 또는 `Carbon` 인스턴스로 변환해줍니다.

데이터베이스 테이블에도 `deleted_at` 컬럼이 필요합니다. Laravel [스키마 빌더](/docs/master/migrations)의 헬퍼 메서드를 활용해 손쉽게 추가/삭제할 수 있습니다.

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

이제 `delete` 메서드를 호출하면, `deleted_at` 컬럼만 현재 날짜로 채워지고, 실제로는 데이터가 남아 있습니다. 소프트 삭제 모델을 조회할 때는 이 값이 적용되어 소프트 삭제된 데이터는 자동으로 쿼리 결과에서 제외됩니다.

특정 모델 인스턴스가 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용하세요.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제 모델 복구

가끔은 소프트 삭제된 모델을 "되살리기" 원할 수 있습니다. 이때는 모델 인스턴스의 `restore` 메서드를 사용하면 되고, 이는 `deleted_at` 값을 `null`로 돌려놓습니다.

```php
$flight->restore();
```

여러 데이터를 쿼리로 대량 복구하려면, `restore` 메서드를 쿼리에 직접 활용하세요. 이 경우 역시 "대량 작업"이므로 이벤트는 발생하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

[연관관계](/docs/master/eloquent-relationships) 쿼리에서도 `restore`를 사용할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### 모델 완전 제거

데이터베이스에서 모델을 아예 영구적으로 삭제해야 할 때는 `forceDelete` 메서드를 사용하면 됩니다.

```php
$flight->forceDelete();
```

이 메서드 역시 간접적으로 연관관계 쿼리에도 활용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 조회

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제 데이터 포함 조회

기본적으로 소프트 삭제된 모델은 쿼리 결과에서 제외되지만, `withTrashed` 메서드를 호출하여 쿼리 결과에 포함시킬 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

연관관계 쿼리에서도 활용 가능:

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 오직 소프트 삭제 데이터만 조회

`onlyTrashed` 메서드를 사용하면, 소프트 삭제된 모델만 조회됩니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## 모델 정리(Pruning)

불필요해진 모델을 주기적으로 삭제해야 할 때가 있습니다. 이때는 해당 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가한 다음, 더 이상 필요하지 않은 데이터를 선택하는 `prunable` 메서드를 구현하세요.

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
     * 정리 대상 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

모델을 Prunable로 지정하면, 모델이 삭제되기 전 추가적으로 리소스를 정리해야 할 때 `pruning` 메서드를 구현할 수 있습니다. (예: 연관 파일 삭제 등)

```php
/**
 * 정리 전에 호출되는 처리
 */
protected function pruning(): void
{
    // ...
}
```

Prunable 모델을 구성했다면, 애플리케이션의 `routes/console.php`에서 `model:prune` Artisan 명령을 스케줄링하세요. 실행 주기는 자유롭게 선택 가능합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

`model:prune` 명령은 자동으로 `app/Models` 디렉토리 내의 Prunable 모델을 감지합니다. 만약 다른 위치에 있다면, `--model` 옵션으로 직접 지정할 수도 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

특정 모델만 "정리 제외"하고 싶다면, `--except` 옵션을 사용하세요.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

정리 대상 쿼리를 실제 삭제 전 테스트하고 싶다면, `--pretend` 옵션으로 프리뷰 실행이 가능합니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제 모델이라도, 정리 대상 쿼리에 해당하면 영구 삭제(`forceDelete`)됩니다.

<a name="mass-pruning"></a>
#### 대량 정리(Mass Pruning)

`Illuminate\Database\Eloquent\MassPrunable` 트레이트가 붙은 모델은 대량 삭제 쿼리로 데이터를 삭제합니다. 이 경우 `pruning` 메서드나 각종 모델 이벤트(`deleting`, `deleted`)가 호출되지 않습니다. 조회 없이 바로 쿼리만 실행되므로 훨씬 빠릅니다.

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
     * 정리 대상 모델 쿼리 반환
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```

<a name="replicating-models"></a>
## 모델 복제

기존 모델 인스턴스의 "저장되지 않은" 복사본을 만들고 싶다면, `replicate` 메서드를 사용하세요. 이 방법은 여러 속성이 동일한 모델 인스턴스를 여러 개 만들어야 할 때 유용합니다.

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

복제 대상에서 일부 속성을 제외하려면, `replicate` 메서드에 배열로 제외할 속성명을 전달하세요.

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
## 쿼리 스코프

<a name="global-scopes"></a>
### 글로벌 스코프

글로벌 스코프는 특정 모델의 모든 쿼리에 자동으로 조건을 추가해줍니다. Laravel의 [소프트 삭제](#soft-deleting)도 글로벌 스코프를 활용해 삭제되지 않은 데이터만 조회하도록 합니다. 직접 글로벌 스코프를 작성하면, 반복적으로 사용되는 조건을 항상 쿼리에 적용할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 클래스 생성

글로벌 스코프 클래스를 새로 생성하려면 `make:scope` Artisan 명령을 사용하세요. 생성된 스코프는 `app/Models/Scopes` 디렉터리에 위치합니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### 글로벌 스코프 작성

글로벌 스코프는 매우 단순합니다. 먼저, `make:scope`로 생성한 클래스는 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현해야 하고, `apply` 메서드를 반드시 구현해야 합니다. 이 메서드에서 `where` 등 쿼리 조건을 자유롭게 추가할 수 있습니다.

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * 주어진 Eloquent 쿼리 빌더에 스코프를 적용
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```

> [!NOTE]
> 글로벌 스코프에서 쿼리의 select 절에 컬럼을 추가하려면, `select` 대신 `addSelect` 메서드를 사용하세요. 기존 select 절이 의도치 않게 대체되는 것을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
#### 글로벌 스코프 적용

글로벌 스코프를 모델에 적용하려면, 해당 모델에 `ScopedBy` 속성을 지정하면 됩니다.

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

또는, 모델의 `booted` 메서드를 오버라이드하여, `addGlobalScope` 메서드로 직접 스코프를 등록할 수 있습니다.

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 부트 메서드
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

위 예제에서 `App\Models\User` 모델에 스코프를 추가하면, `User::all()` 호출 시 아래와 같은 SQL이 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

Eloquent는 클래스 대신 클로저(익명 함수)로도 글로벌 스코프를 정의할 수 있습니다. 이 방법은 간단한 조건일 때 별도 클래스를 만들 필요가 없어서 편리합니다. 클로저 스코프를 등록할 때는, 문자열로 이름을 지정해 `addGlobalScope`의 첫 번째 인수로 전달하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 부트 메서드
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
#### 글로벌 스코프 해제

특정 쿼리에만 글로벌 스코프를 해제하고 싶다면, `withoutGlobalScope` 메서드를 사용하세요. 클래스명을 인수로 받습니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

클로저로 정의한 스코프는, 등록 시 지정한 문자열 이름을 전달해야 합니다.

```php
User::withoutGlobalScope('ancient')->get();
```

여러 개 또는 모든 글로벌 스코프를 해제하고 싶을 때는 `withoutGlobalScopes`, `withoutGlobalScopesExcept` 메서드를 사용할 수 있습니다.

```php
// 모든 글로벌 스코프 해제
User::withoutGlobalScopes()->get();

// 일부 글로벌 스코프만 해제
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// 지정한 스코프만 남기고 나머지 모두 해제
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```

<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프는 자주 사용되는 쿼리 조건 집합을 모델 메서드로 정의해, 애플리케이션에서 재사용할 수 있게 해줍니다. 예를 들어 '인기 있는 사용자'만 자주 조회한다면, 스코프로 정의하면 편리합니다. 스코프 정의 시 `Scope` 속성을 Eloquent 메서드에 추가하세요.

스코프 메서드는 항상 같은 쿼리 빌더 인스턴스(또는 void)를 반환해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 인기 사용자를 조회하는 쿼리 스코프
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * 활성 사용자를 조회하는 쿼리 스코프
     */
    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 활용

스코프를 정의하면, 쿼리 시 체이닝 방식으로 메서드처럼 쉽게 사용할 수 있습니다. 다양한 스코프 메서드를 연이어 사용할 수도 있습니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

여러 스코프를 `or` 연산자로 결합해야 한다면, [논리 그룹핑](/docs/master/queries#logical-grouping)을 위해 클로저가 필요할 수 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

하지만 이 방식이 번거로울 때, Laravel은 "상위 레벨(higher order)"의 `orWhere` 메서드로 더욱 간결하게 스코프를 연결할 수 있도록 지원합니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### 동적(Dynamic) 스코프

스코프에 파라미터(매개변수)를 받게 하고 싶다면, 스코프 메서드 시그니처에 파라미터를 추가하기만 하면 됩니다. 첫 번째 파라미터는 항상 `$query`여야 하고, 그 뒤에 필요한 매개변수를 추가하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 특정 타입만 조회하는 스코프
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```

이제 스코프 호출 시 파라미터를 직접 전달할 수 있습니다.

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 대기 중 속성(Pending Attributes)

스코프를 활용해, 스코프의 조건으로 사용된 속성을 자동으로 포함하는 모델을 생성하고 싶다면, 쿼리 작성 시 `withAttributes`를 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * 초안 상태만 쿼리하는 스코프
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

`withAttributes`는 지정한 속성으로 where 조건을 추가하고, 해당 속성을 스코프 쿼리로 새로 생성되는 모델에도 자동 할당합니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

조건 없이 속성만 생성용으로 활용하려면 `asConditions` 인수를 `false`로 지정하세요.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## 모델 비교

두 모델 인스턴스가 "동일"한지 비교해야 할 때도 있습니다. `is`, `isNot` 메서드를 사용하면, 두 인스턴스가 기본 키, 테이블, DB 연결 모두 동일한지 빠르게 확인할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

이 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [연관관계](/docs/master/eloquent-relationships)에서 활용할 수 있습니다. 예를 들어, 쿼리 없이 연관된 모델 자체를 비교하고자 할 때 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## 이벤트

> [!NOTE]
> Eloquent 이벤트를 클라이언트 애플리케이션에 실시간으로 브로드캐스트하고 싶다면, Laravel의 [모델 이벤트 브로드캐스팅](/docs/master/broadcasting#model-broadcasting)을 확인하세요.

Eloquent 모델은, 모델 생명주기(lifecycle)에서 여러 이벤트를 발생시킵니다. 예를 들어: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating` 등입니다.

- `retrieved`: 모델이 DB에서 조회될 때
- `creating`/`created`: 새 모델이 처음 저장될 때
- `updating`/`updated`: 기존 모델이 수정되어 `save`될 때
- `saving`/`saved`: 생성/수정으로 저장될 때 (속성 변동 여부와 무관)
- `-ing`: DB에 기록 전, `-ed`: 기록 후 이벤트

이벤트를 "청취(listen)"하려면, Eloquent 모델에서 `$dispatchesEvents` 설정을 사용하세요. 배열 형태로 생명주기 이벤트에 [이벤트 클래스](/docs/master/events)를 매핑할 수 있습니다. 각 이벤트 클래스는 생성자에서 영향받은 모델 인스턴스를 인자로 받습니다.

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

이벤트를 매핑했다면 [이벤트 리스너](/docs/master/events#defining-listeners)에서 이벤트를 처리하세요.

> [!WARNING]
> Eloquent에서 대량 업데이트/삭제 쿼리를 실행하면, 영향받은 모델에 대해 `saved`, `updated`, `deleting`, `deleted` 이벤트가 **발생하지 않습니다**. 이는 실제 모델 인스턴스를 조회하지 않고 쿼리만 실행하기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 활용

사용자 정의 이벤트 클래스 대신, 다양한 모델 이벤트가 발생할 때 실행될 클로저를 등록할 수도 있습니다. 이 클로저는 보통 모델의 `booted` 메서드에서 등록합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 모델 부트 메서드
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```

필요하다면, [큐 처리 가능한 익명 리스너](/docs/master/events#queuable-anonymous-event-listeners)도 사용할 수 있습니다. 이렇게 하면, 모델 이벤트 리스너가 [큐](/docs/master/queues) 작업으로 백그라운드에서 실행됩니다.

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

특정 모델의 여러 이벤트를 모두 청취해야 할 때, 옵저버를 사용하면 모든 리스너를 한 클래스에 묶어서 관리할 수 있습니다. 옵저버 클래스는 청취하려는 Eloquent 이벤트별로 메서드명을 정해 구현하며, 각 메서드는 영향받은 모델 인스턴스 하나를 인수로 받습니다. `make:observer` Artisan 명령어로 옵저버 클래스를 생성할 수 있습니다.

```shell
php artisan make:observer UserObserver --model=User
```

이 명령은 새 옵저버 클래스를 `app/Observers` 디렉토리에 생성합니다. 디렉토리가 없다면 Artisan이 자동으로 생성합니다. 기본 형태는 다음과 같습니다.

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * User "created" 이벤트 핸들러
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * User "updated" 이벤트 핸들러
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * User "deleted" 이벤트 핸들러
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * User "restored" 이벤트 핸들러
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * User "forceDeleted" 이벤트 핸들러
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```

옵저버를 등록하려면, 해당 모델에 `ObservedBy` 속성을 지정하면 됩니다.

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

또는, `observe` 메서드를 모델에서 직접 호출해 수동으로 등록할 수도 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드에서 옵저버를 등록합니다.

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * 애플리케이션 서비스 부트스트랩
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```

> [!NOTE]
> 옵저버가 청취할 수 있는 이벤트에는 `saving`, `retrieved` 등도 있습니다. 더 자세한 내용은 [이벤트](#events) 문서를 참고하세요.

<a name="observers-and-database-transactions"></a>
#### 옵저버와 데이터베이스 트랜잭션

모델이 데이터베이스 트랜잭션 내에서 생성될 때, 옵저버의 이벤트 핸들러들이 트랜잭션 커밋(commit) 이후에만 실행되게 하고 싶을 수 있습니다. 그럴 때는 옵저버에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하세요. 데이터베이스 트랜잭션이 없다면 즉시 핸들러가 실행됩니다.

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * User "created" 이벤트 핸들러
     */
    public function created(User $user): void
    {
        // ...
    }
}
```

<a name="muting-events"></a>
### 이벤트 음소거

가끔은 모델에서 발생하는 모든 이벤트를 임시로 "음소거(mute)"해야 할 필요가 있습니다. 이럴 때는 `withoutEvents` 메서드를 사용하면 됩니다. 이 메서드는 클로저 하나를 인수로 받고, 클로저 내부에서 실행된 모든 코드는 모델 이벤트를 발생시키지 않으며, 클로저 반환값이 그대로 반환됩니다.

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### 단일 모델을 이벤트 없이 저장하기

특정 모델을 저장할 때만 이벤트가 발생하지 않게 하려면, `saveQuietly` 메서드를 활용하세요.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

"update", "delete", "soft delete", "restore", "replicate" 등의 작업도 Quietly 메서드로 이벤트 없이 처리할 수 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
