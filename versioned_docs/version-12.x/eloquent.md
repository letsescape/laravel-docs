<!-- # Eloquent: Getting Started -->
# Eloquent: Getting Started

- [Introduction](#introduction)
- [Generating Model Classes](#generating-model-classes)
- [Eloquent Model Conventions](#eloquent-model-conventions)
    - [Table Names](#table-names)
    - [Primary Keys](#primary-keys)
    - [UUID and ULID Keys](#uuid-and-ulid-keys)
    - [Timestamps](#timestamps)
    - [Database Connections](#database-connections)
    - [Default Attribute Values](#default-attribute-values)
    - [Configuring Eloquent Strictness](#configuring-eloquent-strictness)
- [Retrieving Models](#retrieving-models)
    - [Collections](#collections)
    - [Chunking Results](#chunking-results)
    - [Chunk Using Lazy Collections](#chunking-using-lazy-collections)
    - [Cursors](#cursors)
    - [Advanced Subqueries](#advanced-subqueries)
- [Retrieving Single Models / Aggregates](#retrieving-single-models)
    - [Retrieving or Creating Models](#retrieving-or-creating-models)
    - [Retrieving Aggregates](#retrieving-aggregates)
- [Inserting and Updating Models](#inserting-and-updating-models)
    - [Inserts](#inserts)
    - [Updates](#updates)
    - [Mass Assignment](#mass-assignment)
    - [Upserts](#upserts)
- [Deleting Models](#deleting-models)
    - [Soft Deleting](#soft-deleting)
    - [Querying Soft Deleted Models](#querying-soft-deleted-models)
- [Pruning Models](#pruning-models)
- [Replicating Models](#replicating-models)
- [Query Scopes](#query-scopes)
    - [Global Scopes](#global-scopes)
    - [Local Scopes](#local-scopes)
    - [Pending Attributes](#pending-attributes)
- [Comparing Models](#comparing-models)
- [Events](#events)
    - [Using Closures](#events-using-closures)
    - [Observers](#observers)
    - [Muting Events](#muting-events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel includes Eloquent, an object-relational mapper (ORM) that makes it enjoyable to interact with your database. When using Eloquent, each database table has a corresponding "Model" that is used to interact with that table. In addition to retrieving records from the database table, Eloquent models allow you to insert, update, and delete records from the table as well. -->
Laravel에는 데이터베이스와 즐겁게 상호작용할 수 있도록 도와주는 객체 관계 매퍼(ORM)인 Eloquent가 포함되어 있습니다. Eloquent를 사용할 때 각 데이터베이스 테이블에는 해당 테이블과 상호작용하는 데 사용되는 "Model"이 대응됩니다. Eloquent 모델은 데이터베이스 테이블에서 레코드를 조회하는 것뿐만 아니라, 테이블에 레코드를 삽입하고 업데이트하며 삭제할 수도 있게 해줍니다.

> [!NOTE]
> 시작하기 전에 애플리케이션의 `config/database.php` 설정 파일에서 데이터베이스 연결을 설정해야 합니다. 데이터베이스 설정에 대한 자세한 내용은 [the database configuration documentation](/docs/12.x/database#configuration)를 확인하십시오.

<a name="generating-model-classes"></a>
<!-- ## Generating Model Classes -->
## Generating Model Classes

<!-- To get started, let's create an Eloquent model. Models typically live in the `app\Models` directory and extend the `Illuminate\Database\Eloquent\Model` class. You may use the `make:model` [Artisan command](/docs/12.x/artisan) to generate a new model: -->
시작하려면 Eloquent 모델을 생성해 보겠습니다. 모델은 일반적으로 `app\Models` 디렉터리에 위치하며 `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. 새 모델을 생성하려면 `make:model` [Artisan command](/docs/12.x/artisan)를 사용할 수 있습니다.

```shell
php artisan make:model Flight
```

<!-- If you would like to generate a [database migration](/docs/12.x/migrations) when you generate the model, you may use the `--migration` or `-m` option: -->
모델을 생성할 때 [database migration](/docs/12.x/migrations)도 함께 생성하려면 `--migration` 또는 `-m` 옵션을 사용할 수 있습니다.

```shell
php artisan make:model Flight --migration
```

<!-- You may generate various other types of classes when generating a model, such as factories, seeders, policies, controllers, and form requests. In addition, these options may be combined to create multiple classes at once: -->
모델을 생성할 때 팩토리, 시더, 정책, 컨트롤러, 폼 요청 등 다양한 종류의 클래스도 함께 생성할 수 있습니다. 또한 이러한 옵션을 조합하여 여러 클래스를 한 번에 생성할 수도 있습니다.

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
<!-- #### Inspecting Models -->
#### Inspecting Models

<!-- Sometimes it can be difficult to determine all of a model's available attributes and relationships just by skimming its code. Instead, try the `model:show` Artisan command, which provides a convenient overview of all the model's attributes and relations: -->
때로는 모델 코드를 훑어보는 것만으로는 모델에서 사용할 수 있는 모든 속성과 연관관계를 파악하기 어려울 수 있습니다. 이럴 때는 모델의 모든 속성과 연관관계를 편리하게 요약해 주는 `model:show` Artisan 명령어를 사용해 보십시오.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
<!-- ## Eloquent Model Conventions -->
## Eloquent Model Conventions

<!-- Models generated by the `make:model` command will be placed in the `app/Models` directory. Let's examine a basic model class and discuss some of Eloquent's key conventions: -->
`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 배치됩니다. 기본 모델 클래스를 살펴보고 Eloquent의 핵심 규칙 몇 가지를 알아보겠습니다.

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
<!-- ### Table Names -->
### Table Names

<!-- After glancing at the example above, you may have noticed that we did not tell Eloquent which database table corresponds to our `Flight` model. By convention, the "snake case", plural name of the class will be used as the table name unless another name is explicitly specified. So, in this case, Eloquent will assume the `Flight` model stores records in the `flights` table, while an `AirTrafficController` model would store records in an `air_traffic_controllers` table. -->
위 예제를 보면, `Flight` 모델이 어떤 데이터베이스 테이블에 대응되는지 Eloquent에 알려주지 않았다는 점을 눈치챘을 수 있습니다. 관례에 따라 다른 이름을 명시적으로 지정하지 않으면 클래스명의 "snake case" 복수형 이름이 테이블 이름으로 사용됩니다. 따라서 이 경우 Eloquent는 `Flight` 모델이 `flights` 테이블에 레코드를 저장한다고 가정하며, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 레코드를 저장한다고 가정합니다.

<!-- If your model's corresponding database table does not fit this convention, you may manually specify the model's table name by defining a `table` property on the model: -->
모델에 대응되는 데이터베이스 테이블이 이 관례에 맞지 않는 경우, 모델에 `table` 속성을 정의하여 모델의 테이블 이름을 직접 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'my_flights';
}
```

<a name="primary-keys"></a>
<!-- ### Primary Keys -->
### Primary Keys

<!-- Eloquent will also assume that each model's corresponding database table has a primary key column named `id`. If necessary, you may define a protected `$primaryKey` property on your model to specify a different column that serves as your model's primary key: -->
Eloquent는 각 모델에 대응되는 데이터베이스 테이블에 `id`라는 이름의 기본 키 컬럼이 있다고 가정합니다. 필요한 경우 모델에 protected `$primaryKey` 속성을 정의하여 모델의 기본 키로 사용할 다른 컬럼을 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The primary key associated with the table.
     *
     * @var string
     */
    protected $primaryKey = 'flight_id';
}
```

<!-- In addition, Eloquent assumes that the primary key is an incrementing integer value, which means that Eloquent will automatically cast the primary key to an integer. If you wish to use a non-incrementing or a non-numeric primary key you must define a public `$incrementing` property on your model that is set to `false`: -->
또한 Eloquent는 기본 키가 증가하는 정수 값이라고 가정합니다. 따라서 Eloquent는 기본 키를 자동으로 정수로 casting합니다. 증가하지 않거나 숫자가 아닌 기본 키를 사용하려면 모델에 public `$incrementing` 속성을 정의하고 값을 `false`로 설정해야 합니다.

```php
<?php

class Flight extends Model
{
    /**
     * Indicates if the model's ID is auto-incrementing.
     *
     * @var bool
     */
    public $incrementing = false;
}
```

<!-- If your model's primary key is not an integer, you should define a protected `$keyType` property on your model. This property should have a value of `string`: -->
모델의 기본 키가 정수가 아니라면 모델에 protected `$keyType` 속성을 정의해야 합니다. 이 속성의 값은 `string`이어야 합니다.

```php
<?php

class Flight extends Model
{
    /**
     * The data type of the primary key ID.
     *
     * @var string
     */
    protected $keyType = 'string';
}
```

<a name="composite-primary-keys"></a>
<!-- #### "Composite" Primary Keys -->
#### "Composite" Primary Keys

<!-- Eloquent requires each model to have at least one uniquely identifying "ID" that can serve as its primary key. "Composite" primary keys are not supported by Eloquent models. However, you are free to add additional multi-column, unique indexes to your database tables in addition to the table's uniquely identifying primary key. -->
Eloquent는 각 모델에 기본 키로 사용할 수 있는, 최소 하나의 고유하게 식별되는 "ID"가 있어야 한다고 요구합니다. "복합" 기본 키는 Eloquent 모델에서 지원되지 않습니다. 하지만 테이블을 고유하게 식별하는 기본 키와 별도로, 데이터베이스 테이블에 여러 컬럼으로 구성된 추가 고유 인덱스를 자유롭게 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
<!-- ### UUID and ULID Keys -->
### UUID and ULID Keys

<!-- Instead of using auto-incrementing integers as your Eloquent model's primary keys, you may choose to use UUIDs instead. UUIDs are universally unique alpha-numeric identifiers that are 36 characters long. -->
Eloquent 모델의 기본 키로 자동 증가 정수를 사용하는 대신 UUID를 사용할 수도 있습니다. UUID는 전 세계적으로 고유한 36자 길이의 영숫자 식별자입니다.

<!-- If you would like a model to use a UUID key instead of an auto-incrementing integer key, you may use the `Illuminate\Database\Eloquent\Concerns\HasUuids` trait on the model. Of course, you should ensure that the model has a [UUID equivalent primary key column](/docs/12.x/migrations#column-method-uuid): -->
모델에서 자동 증가 정수 키 대신 UUID 키를 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용할 수 있습니다. 물론 모델에 [UUID equivalent primary key column](/docs/12.x/migrations#column-method-uuid)이 있는지도 확인해야 합니다.

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

<!-- By default, the `HasUuids` trait will generate [UUIDv7](/docs/12.x/strings#method-str-uuid7) identifiers for your models. These UUIDs are more efficient for indexed database storage because they can be sorted lexicographically. -->
기본적으로 `HasUuids` 트레이트는 모델에 대해 [UUIDv7](/docs/12.x/strings#method-str-uuid7) 식별자를 생성합니다. 이러한 UUID는 사전식으로 정렬할 수 있기 때문에 인덱싱된 데이터베이스 저장소에서 더 효율적입니다.

<!-- You can override the UUID generation process for a given model by defining a `newUniqueId` method on the model. In addition, you may specify which columns should receive UUIDs by defining a `uniqueIds` method on the model: -->
특정 모델의 UUID 생성 과정을 재정의하려면 모델에 `newUniqueId` 메서드를 정의하면 됩니다. 또한 어떤 컬럼이 UUID를 받아야 하는지 지정하려면 모델에 `uniqueIds` 메서드를 정의할 수 있습니다.

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

<!-- If you wish, you may choose to utilize "ULIDs" instead of UUIDs. ULIDs are similar to UUIDs; however, they are only 26 characters in length. Like ordered UUIDs, ULIDs are lexicographically sortable for efficient database indexing. To utilize ULIDs, you should use the `Illuminate\Database\Eloquent\Concerns\HasUlids` trait on your model. You should also ensure that the model has a [ULID equivalent primary key column](/docs/12.x/migrations#column-method-ulid): -->
원한다면 UUID 대신 "ULID"를 사용할 수도 있습니다. ULID는 UUID와 비슷하지만 길이가 26자뿐입니다. 정렬 가능한 UUID처럼 ULID도 사전식으로 정렬할 수 있어 데이터베이스 인덱싱에 효율적입니다. ULID를 사용하려면 모델에 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레이트를 사용해야 합니다. 또한 모델에 [ULID equivalent primary key column](/docs/12.x/migrations#column-method-ulid)이 있는지도 확인해야 합니다.

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
<!-- ### Timestamps -->
### Timestamps

<!-- By default, Eloquent expects `created_at` and `updated_at` columns to exist on your model's corresponding database table. Eloquent will automatically set these column's values when models are created or updated. If you do not want these columns to be automatically managed by Eloquent, you should define a `$timestamps` property on your model with a value of `false`: -->
기본적으로 Eloquent는 모델에 대응되는 데이터베이스 테이블에 `created_at` 및 `updated_at` 컬럼이 존재한다고 가정합니다. Eloquent는 모델이 생성되거나 업데이트될 때 이 컬럼들의 값을 자동으로 설정합니다. 이러한 컬럼을 Eloquent가 자동으로 관리하지 않도록 하려면 모델에 `$timestamps` 속성을 정의하고 값을 `false`로 설정해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * Indicates if the model should be timestamped.
     *
     * @var bool
     */
    public $timestamps = false;
}
```

<!-- If you need to customize the format of your model's timestamps, set the `$dateFormat` property on your model. This property determines how date attributes are stored in the database as well as their format when the model is serialized to an array or JSON: -->
모델의 타임스탬프 형식을 사용자 지정해야 한다면 모델에 `$dateFormat` 속성을 설정하십시오. 이 속성은 날짜 속성이 데이터베이스에 저장되는 방식뿐만 아니라, 모델이 배열이나 JSON으로 직렬화될 때의 형식도 결정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The storage format of the model's date columns.
     *
     * @var string
     */
    protected $dateFormat = 'U';
}
```

<!-- If you need to customize the names of the columns used to store the timestamps, you may define `CREATED_AT` and `UPDATED_AT` constants on your model: -->
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

<!-- If you would like to perform model operations without the model having its `updated_at` timestamp modified, you may operate on the model within a closure given to the `withoutTimestamps` method: -->
모델의 `updated_at` 타임스탬프를 변경하지 않고 모델 작업을 수행하려면 `withoutTimestamps` 메서드에 전달한 클로저 안에서 모델을 조작하면 됩니다.

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
<!-- ### Database Connections -->
### Database Connections

<!-- By default, all Eloquent models will use the default database connection that is configured for your application. If you would like to specify a different connection that should be used when interacting with a particular model, you should define a `$connection` property on the model: -->
기본적으로 모든 Eloquent 모델은 애플리케이션에 설정된 기본 데이터베이스 연결을 사용합니다. 특정 모델과 상호작용할 때 사용할 다른 연결을 지정하려면 모델에 `$connection` 속성을 정의해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The database connection that should be used by the model.
     *
     * @var string
     */
    protected $connection = 'mysql';
}
```

<a name="default-attribute-values"></a>
<!-- ### Default Attribute Values -->
### Default Attribute Values

<!-- By default, a newly instantiated model instance will not contain any attribute values. If you would like to define the default values for some of your model's attributes, you may define an `$attributes` property on your model. Attribute values placed in the `$attributes` array should be in their raw, "storable" format as if they were just read from the database: -->
기본적으로 새로 인스턴스화된 모델 인스턴스에는 어떤 속성값도 포함되어 있지 않습니다. 모델 속성 중 일부에 기본값을 정의하려면 모델에 `$attributes` 속성을 정의할 수 있습니다. `$attributes` 배열에 넣는 속성값은 데이터베이스에서 방금 읽어 온 것처럼 원시의 "저장 가능한" 형식이어야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The model's default values for attributes.
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
<!-- ### Configuring Eloquent Strictness -->
### Configuring Eloquent Strictness
<!-- Laravel offers several methods that allow you to configure Eloquent's behavior and "strictness" in a variety of situations. -->
Laravel은 다양한 상황에서 Eloquent의 동작과 "엄격성"을 설정할 수 있는 여러 메서드를 제공합니다.

<!-- First, the `preventLazyLoading` method accepts an optional boolean argument that indicates if lazy loading should be prevented. For example, you may wish to only disable lazy loading in non-production environments so that your production environment will continue to function normally even if a lazy loaded relationship is accidentally present in production code. Typically, this method should be invoked in the `boot` method of your application's `AppServiceProvider`: -->
먼저, `preventLazyLoading` 메서드는 지연 로딩을 방지할지 여부를 나타내는 선택적 boolean 인수를 받습니다. 예를 들어, 프로덕션 환경에서 실수로 지연 로딩된 연관관계가 코드에 포함되더라도 프로덕션 환경은 정상적으로 계속 동작하도록, 프로덕션이 아닌 환경에서만 지연 로딩을 비활성화하고 싶을 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드에서 호출해야 합니다.

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

<!-- Also, you may instruct Laravel to throw an exception when attempting to fill an unfillable attribute by invoking the `preventSilentlyDiscardingAttributes` method. This can help prevent unexpected errors during local development when attempting to set an attribute that has not been added to the model's `fillable` array: -->
또한 `preventSilentlyDiscardingAttributes` 메서드를 호출하여 채울 수 없는 속성을 채우려고 할 때 Laravel이 예외를 던지도록 지시할 수 있습니다. 이는 모델의 `fillable` 배열에 추가되지 않은 속성을 설정하려고 할 때 로컬 개발 중 예상치 못한 오류를 방지하는 데 도움이 됩니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
<!-- ## Retrieving Models -->
## Retrieving Models

<!-- Once you have created a model and [its associated database table](/docs/12.x/migrations#generating-migrations), you are ready to start retrieving data from your database. You can think of each Eloquent model as a powerful [query builder](/docs/12.x/queries) allowing you to fluently query the database table associated with the model. The model's `all` method will retrieve all of the records from the model's associated database table: -->
모델과 [its associated database table](/docs/12.x/migrations#generating-migrations)을 만들었다면, 이제 데이터베이스에서 데이터를 조회할 준비가 되었습니다. 각 Eloquent 모델은 모델에 연결된 데이터베이스 테이블을 유창하게 조회할 수 있게 해주는 강력한 [query builder](/docs/12.x/queries)라고 생각할 수 있습니다. 모델의 `all` 메서드는 모델에 연결된 데이터베이스 테이블의 모든 레코드를 조회합니다.

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
<!-- #### Building Queries -->
#### Building Queries

<!-- The Eloquent `all` method will return all of the results in the model's table. However, since each Eloquent model serves as a [query builder](/docs/12.x/queries), you may add additional constraints to queries and then invoke the `get` method to retrieve the results: -->
Eloquent의 `all` 메서드는 모델 테이블의 모든 결과를 반환합니다. 하지만 각 Eloquent 모델은 [query builder](/docs/12.x/queries) 역할도 하므로, 쿼리에 추가 제약 조건을 더한 다음 `get` 메서드를 호출하여 결과를 조회할 수 있습니다.

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [query builder](/docs/12.x/queries)가 제공하는 모든 메서드를 살펴보는 것이 좋습니다. Eloquent 쿼리를 작성할 때 이러한 메서드를 모두 사용할 수 있습니다.

<a name="refreshing-models"></a>
<!-- #### Refreshing Models -->
#### Refreshing Models

<!-- If you already have an instance of an Eloquent model that was retrieved from the database, you can "refresh" the model using the `fresh` and `refresh` methods. The `fresh` method will re-retrieve the model from the database. The existing model instance will not be affected: -->
데이터베이스에서 조회한 Eloquent 모델 인스턴스가 이미 있다면, `fresh`와 `refresh` 메서드를 사용하여 모델을 "새로 고칠" 수 있습니다. `fresh` 메서드는 데이터베이스에서 모델을 다시 조회합니다. 기존 모델 인스턴스는 영향을 받지 않습니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

<!-- The `refresh` method will re-hydrate the existing model using fresh data from the database. In addition, all of its loaded relationships will be refreshed as well: -->
`refresh` 메서드는 데이터베이스의 최신 데이터를 사용하여 기존 모델을 다시 하이드레이트합니다. 또한 로드된 모든 연관관계도 함께 새로 고쳐집니다.

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
<!-- ### Collections -->
### Collections

<!-- As we have seen, Eloquent methods like `all` and `get` retrieve multiple records from the database. However, these methods don't return a plain PHP array. Instead, an instance of `Illuminate\Database\Eloquent\Collection` is returned. -->
앞서 보았듯이, `all`과 `get` 같은 Eloquent 메서드는 데이터베이스에서 여러 레코드를 조회합니다. 하지만 이 메서드들은 일반 PHP 배열을 반환하지 않습니다. 대신 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

<!-- The Eloquent `Collection` class extends Laravel's base `Illuminate\Support\Collection` class, which provides a [variety of helpful methods](/docs/12.x/collections#available-methods) for interacting with data collections. For example, the `reject` method may be used to remove models from a collection based on the results of an invoked closure: -->
Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 확장합니다. 이 기본 컬렉션 클래스는 데이터 컬렉션을 다루기 위한 [variety of helpful methods](/docs/12.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드는 호출된 클로저의 결과를 기준으로 컬렉션에서 모델을 제거하는 데 사용할 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

<!-- In addition to the methods provided by Laravel's base collection class, the Eloquent collection class provides [a few extra methods](/docs/12.x/eloquent-collections#available-methods) that are specifically intended for interacting with collections of Eloquent models. -->
Laravel의 기본 컬렉션 클래스가 제공하는 메서드 외에도, Eloquent 컬렉션 클래스는 Eloquent 모델 컬렉션을 다루기 위해 특별히 마련된 [a few extra methods](/docs/12.x/eloquent-collections#available-methods)를 제공합니다.

<!-- Since all of Laravel's collections implement PHP's iterable interfaces, you may loop over collections as if they were an array: -->
Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하므로, 배열처럼 컬렉션을 반복할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
<!-- ### Chunking Results -->
### Chunking Results

<!-- Your application may run out of memory if you attempt to load tens of thousands of Eloquent records via the `all` or `get` methods. Instead of using these methods, the `chunk` method may be used to process large numbers of models more efficiently. -->
`all` 또는 `get` 메서드로 수만 개의 Eloquent 레코드를 로드하려고 하면 애플리케이션의 메모리가 부족해질 수 있습니다. 이런 메서드 대신 `chunk` 메서드를 사용하면 많은 수의 모델을 더 효율적으로 처리할 수 있습니다.

<!-- The `chunk` method will retrieve a subset of Eloquent models, passing them to a closure for processing. Since only the current chunk of Eloquent models is retrieved at a time, the `chunk` method will provide significantly reduced memory usage when working with a large number of models: -->
`chunk` 메서드는 Eloquent 모델의 일부 집합을 조회한 뒤, 처리를 위해 클로저로 전달합니다. 한 번에 현재 청크에 해당하는 Eloquent 모델만 조회하므로, 많은 수의 모델을 다룰 때 `chunk` 메서드는 메모리 사용량을 크게 줄여 줍니다.

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```

<!-- The first argument passed to the `chunk` method is the number of records you wish to receive per "chunk". The closure passed as the second argument will be invoked for each chunk that is retrieved from the database. A database query will be executed to retrieve each chunk of records passed to the closure. -->
`chunk` 메서드에 전달하는 첫 번째 인수는 각 "청크"마다 받고 싶은 레코드 수입니다. 두 번째 인수로 전달한 클로저는 데이터베이스에서 조회된 각 청크마다 호출됩니다. 클로저에 전달될 각 레코드 청크를 조회하기 위해 데이터베이스 쿼리가 실행됩니다.

<!-- If you are filtering the results of the `chunk` method based on a column that you will also be updating while iterating over the results, you should use the `chunkById` method. Using the `chunk` method in these scenarios could lead to unexpected and inconsistent results. Internally, the `chunkById` method will always retrieve models with an `id` column greater than the last model in the previous chunk: -->
`chunk` 메서드의 결과를 필터링하는 데 사용하는 컬럼을 결과를 반복하는 동안 함께 업데이트할 예정이라면, `chunkById` 메서드를 사용해야 합니다. 이러한 상황에서 `chunk` 메서드를 사용하면 예상치 못한 일관성 없는 결과가 발생할 수 있습니다. 내부적으로 `chunkById` 메서드는 항상 이전 청크의 마지막 모델보다 큰 `id` 컬럼 값을 가진 모델을 조회합니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

<!-- Since the `chunkById` and `lazyById` methods add their own "where" conditions to the query being executed, you should typically [logically group](/docs/12.x/queries#logical-grouping) your own conditions within a closure: -->
`chunkById`와 `lazyById` 메서드는 실행되는 쿼리에 자체적인 "where" 조건을 추가하므로, 일반적으로 직접 작성한 조건은 클로저 안에서 [logically group](/docs/12.x/queries#logical-grouping)해야 합니다.

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
<!-- ### Chunking Using Lazy Collections -->
### Chunking Using Lazy Collections

<!-- The `lazy` method works similarly to [the `chunk` method](#chunking-results) in the sense that, behind the scenes, it executes the query in chunks. However, instead of passing each chunk directly into a callback as is, the `lazy` method returns a flattened [LazyCollection](/docs/12.x/collections#lazy-collections) of Eloquent models, which lets you interact with the results as a single stream: -->
`lazy` 메서드는 내부적으로 쿼리를 청크 단위로 실행한다는 점에서 [the `chunk` method](#chunking-results)와 비슷하게 동작합니다. 하지만 각 청크를 콜백에 그대로 직접 전달하는 대신, `lazy` 메서드는 Eloquent 모델로 이루어진 평탄화된 [LazyCollection](/docs/12.x/collections#lazy-collections)을 반환합니다. 이를 통해 결과를 하나의 스트림처럼 다룰 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

<!-- If you are filtering the results of the `lazy` method based on a column that you will also be updating while iterating over the results, you should use the `lazyById` method. Internally, the `lazyById` method will always retrieve models with an `id` column greater than the last model in the previous chunk: -->
`lazy` 메서드의 결과를 필터링하는 데 사용하는 컬럼을 결과를 반복하는 동안 함께 업데이트할 예정이라면, `lazyById` 메서드를 사용해야 합니다. 내부적으로 `lazyById` 메서드는 항상 이전 청크의 마지막 모델보다 큰 `id` 컬럼 값을 가진 모델을 조회합니다.

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

<!-- You may filter the results based on the descending order of the `id` using the `lazyByIdDesc` method. -->
`lazyByIdDesc` 메서드를 사용하면 `id`의 내림차순을 기준으로 결과를 필터링할 수 있습니다.

<a name="cursors"></a>
<!-- ### Cursors -->
### Cursors

<!-- Similar to the `lazy` method, the `cursor` method may be used to significantly reduce your application's memory consumption when iterating through tens of thousands of Eloquent model records. -->
`lazy` 메서드와 비슷하게, `cursor` 메서드는 수만 개의 Eloquent 모델 레코드를 반복할 때 애플리케이션의 메모리 사용량을 크게 줄이는 데 사용할 수 있습니다.

<!-- The `cursor` method will only execute a single database query; however, the individual Eloquent models will not be hydrated until they are actually iterated over. Therefore, only one Eloquent model is kept in memory at any given time while iterating over the cursor. -->
`cursor` 메서드는 데이터베이스 쿼리를 한 번만 실행합니다. 하지만 개별 Eloquent 모델은 실제로 반복되는 시점까지 하이드레이트되지 않습니다. 따라서 커서를 반복하는 동안에는 항상 하나의 Eloquent 모델만 메모리에 유지됩니다.

> [!WARNING]
> `cursor` 메서드는 한 번에 하나의 Eloquent 모델만 메모리에 보관하므로 연관관계를 즉시 로딩할 수 없습니다. 연관관계를 즉시 로딩해야 한다면 대신 [the `lazy` method](#chunking-using-lazy-collections)를 사용하는 것을 고려하세요.

<!-- Internally, the `cursor` method uses PHP [generators](https://www.php.net/manual/en/language.generators.overview.php) to implement this functionality: -->
내부적으로 `cursor` 메서드는 이 기능을 구현하기 위해 PHP [generators](https://www.php.net/manual/en/language.generators.overview.php)를 사용합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

<!-- The `cursor` returns an `Illuminate\Support\LazyCollection` instance. [Lazy collections](/docs/12.x/collections#lazy-collections) allow you to use many of the collection methods available on typical Laravel collections while only loading a single model into memory at a time: -->
`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy collections](/docs/12.x/collections#lazy-collections)을 사용하면 한 번에 하나의 모델만 메모리에 로드하면서도 일반적인 Laravel 컬렉션에서 사용할 수 있는 많은 컬렉션 메서드를 사용할 수 있습니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

<!-- Although the `cursor` method uses far less memory than a regular query (by only holding a single Eloquent model in memory at a time), it will still eventually run out of memory. This is [due to PHP's PDO driver internally caching all raw query results in its buffer](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php). If you're dealing with a very large number of Eloquent records, consider using [the `lazy` method](#chunking-using-lazy-collections) instead. -->
`cursor` 메서드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만(한 번에 하나의 Eloquent 모델만 메모리에 보관하기 때문입니다), 결국에는 여전히 메모리가 부족해질 수 있습니다. 이는 [due to PHP's PDO driver internally caching all raw query results in its buffer](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php). 매우 많은 수의 Eloquent 레코드를 다루고 있다면 대신 [the `lazy` method](#chunking-using-lazy-collections)를 사용하는 것을 고려하세요.

<a name="advanced-subqueries"></a>
<!-- ### Advanced Subqueries -->
### Advanced Subqueries

<a name="subquery-selects"></a>
<!-- #### Subquery Selects -->
#### Subquery Selects

<!-- Eloquent also offers advanced subquery support, which allows you to pull information from related tables in a single query. For example, let's imagine that we have a table of flight `destinations` and a table of `flights` to destinations. The `flights` table contains an `arrived_at` column which indicates when the flight arrived at the destination. -->
Eloquent는 고급 서브쿼리 지원도 제공하므로, 하나의 쿼리로 관련 테이블의 정보를 가져올 수 있습니다. 예를 들어, 비행 `destinations` 테이블과 목적지로 향하는 `flights` 테이블이 있다고 가정해 보겠습니다. `flights` 테이블에는 항공편이 목적지에 도착한 시간을 나타내는 `arrived_at` 컬럼이 포함되어 있습니다.

<!-- Using the subquery functionality available to the query builder's `select` and `addSelect` methods, we can select all of the `destinations` and the name of the flight that most recently arrived at that destination using a single query: -->
쿼리 빌더의 `select`와 `addSelect` 메서드에서 제공하는 서브쿼리 기능을 사용하면, 하나의 쿼리로 모든 `destinations`와 각 목적지에 가장 최근에 도착한 항공편의 이름을 선택할 수 있습니다.

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
<!-- #### Subquery Ordering -->
#### Subquery Ordering

<!-- In addition, the query builder's `orderBy` function supports subqueries. Continuing to use our flight example, we may use this functionality to sort all destinations based on when the last flight arrived at that destination. Again, this may be done while executing a single database query: -->
또한 쿼리 빌더의 `orderBy` 함수는 서브쿼리를 지원합니다. 앞의 항공편 예제를 계속 사용하면, 이 기능을 사용해 마지막 항공편이 해당 목적지에 도착한 시간을 기준으로 모든 목적지를 정렬할 수 있습니다. 이 역시 하나의 데이터베이스 쿼리만 실행하면서 처리할 수 있습니다.

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```

<a name="retrieving-single-models"></a>
<!-- ## Retrieving Single Models / Aggregates -->
## Retrieving Single Models / Aggregates

<!-- In addition to retrieving all of the records matching a given query, you may also retrieve single records using the `find`, `first`, or `firstWhere` methods. Instead of returning a collection of models, these methods return a single model instance: -->
주어진 쿼리와 일치하는 모든 레코드를 조회하는 것 외에도, `find`, `first`, `firstWhere` 메서드를 사용하여 단일 레코드를 조회할 수 있습니다. 이 메서드들은 모델 컬렉션을 반환하는 대신 단일 모델 인스턴스를 반환합니다.

```php
use App\Models\Flight;

// Retrieve a model by its primary key...
$flight = Flight::find(1);

// Retrieve the first model matching the query constraints...
$flight = Flight::where('active', 1)->first();

// Alternative to retrieving the first model matching the query constraints...
$flight = Flight::firstWhere('active', 1);
```

<!-- Sometimes you may wish to perform some other action if no results are found. The `findOr` and `firstOr` methods will return a single model instance or, if no results are found, execute the given closure. The value returned by the closure will be considered the result of the method: -->
때로는 결과를 찾지 못했을 때 다른 작업을 수행하고 싶을 수 있습니다. `findOr`와 `firstOr` 메서드는 단일 모델 인스턴스를 반환하거나, 결과를 찾지 못한 경우 주어진 클로저를 실행합니다. 클로저가 반환한 값이 해당 메서드의 결과로 간주됩니다.

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```

<a name="not-found-exceptions"></a>
<!-- #### Not Found Exceptions -->
#### Not Found Exceptions

<!-- Sometimes you may wish to throw an exception if a model is not found. This is particularly useful in routes or controllers. The `findOrFail` and `firstOrFail` methods will retrieve the first result of the query; however, if no result is found, an `Illuminate\Database\Eloquent\ModelNotFoundException` will be thrown: -->
때로는 모델을 찾지 못했을 때 예외를 던지고 싶을 수 있습니다. 이는 특히 라우트나 컨트롤러에서 유용합니다. `findOrFail`과 `firstOrFail` 메서드는 쿼리의 첫 번째 결과를 조회합니다. 하지만 결과를 찾지 못하면 `Illuminate\Database\Eloquent\ModelNotFoundException`이 발생합니다.

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

<!-- If the `ModelNotFoundException` is not caught, a 404 HTTP response is automatically sent back to the client: -->
`ModelNotFoundException`이 잡히지 않으면, 404 HTTP 응답이 자동으로 클라이언트에 반환됩니다.

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
<!-- ### Retrieving or Creating Models -->
### Retrieving or Creating Models

<!-- The `firstOrCreate` method will attempt to locate a database record using the given column / value pairs. If the model cannot be found in the database, a record will be inserted with the attributes resulting from merging the first array argument with the optional second array argument. -->
`firstOrCreate` 메서드는 주어진 컬럼 / 값 쌍을 사용하여 데이터베이스 레코드를 찾으려고 시도합니다. 데이터베이스에서 모델을 찾을 수 없으면, 첫 번째 배열 인수와 선택적인 두 번째 배열 인수를 병합한 속성으로 레코드가 삽입됩니다.

<!-- The `firstOrNew` method, like `firstOrCreate`, will attempt to locate a record in the database matching the given attributes. However, if a model is not found, a new model instance will be returned. Note that the model returned by `firstOrNew` has not yet been persisted to the database. You will need to manually call the `save` method to persist it: -->
`firstOrNew` 메서드도 `firstOrCreate`처럼 주어진 속성과 일치하는 레코드를 데이터베이스에서 찾으려고 시도합니다. 하지만 모델을 찾지 못하면 새 모델 인스턴스가 반환됩니다. `firstOrNew`가 반환한 모델은 아직 데이터베이스에 저장되지 않았다는 점에 유의하세요. 저장하려면 `save` 메서드를 직접 호출해야 합니다.

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
<!-- ### Retrieving Aggregates -->
### Retrieving Aggregates

<!-- When interacting with Eloquent models, you may also use the `count`, `sum`, `max`, and other [aggregate methods](/docs/12.x/queries#aggregates) provided by the Laravel [query builder](/docs/12.x/queries). As you might expect, these methods return a scalar value instead of an Eloquent model instance: -->
Eloquent 모델을 다룰 때 `count`, `sum`, `max` 및 기타 [aggregate methods](/docs/12.x/queries#aggregates)도 사용할 수 있으며, 이는 Laravel [query builder](/docs/12.x/queries)가 제공합니다. 예상할 수 있듯이, 이 메서드들은 Eloquent 모델 인스턴스가 아니라 스칼라 값을 반환합니다.

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
<!-- ## Inserting and Updating Models -->
## Inserting and Updating Models

<a name="inserts"></a>
<!-- ### Inserts -->
### Inserts

<!-- Of course, when using Eloquent, we don't only need to retrieve models from the database. We also need to insert new records. Thankfully, Eloquent makes it simple. To insert a new record into the database, you should instantiate a new model instance and set attributes on the model. Then, call the `save` method on the model instance: -->
물론 Eloquent를 사용할 때 데이터베이스에서 모델을 조회하기만 하는 것은 아닙니다. 새 레코드도 삽입해야 합니다. 다행히 Eloquent는 이 작업을 간단하게 만들어 줍니다. 데이터베이스에 새 레코드를 삽입하려면 새 모델 인스턴스를 만들고 모델에 속성을 설정해야 합니다. 그런 다음 모델 인스턴스에서 `save` 메서드를 호출합니다.

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

<!-- In this example, we assign the `name` field from the incoming HTTP request to the `name` attribute of the `App\Models\Flight` model instance. When we call the `save` method, a record will be inserted into the database. The model's `created_at` and `updated_at` timestamps will automatically be set when the `save` method is called, so there is no need to set them manually. -->
이 예제에서는 들어오는 HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당합니다. `save` 메서드를 호출하면 데이터베이스에 레코드가 삽입됩니다. `save` 메서드가 호출될 때 모델의 `created_at`과 `updated_at` 타임스탬프가 자동으로 설정되므로, 직접 설정할 필요가 없습니다.

<!-- Alternatively, you may use the `create` method to "save" a new model using a single PHP statement. The inserted model instance will be returned to you by the `create` method: -->
또는 `create` 메서드를 사용해 하나의 PHP 문장으로 새 모델을 "저장"할 수도 있습니다. 삽입된 모델 인스턴스는 `create` 메서드에서 반환됩니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

<!-- However, before using the `create` method, you will need to specify either a `fillable` or `guarded` property on your model class. These properties are required because all Eloquent models are protected against mass assignment vulnerabilities by default. To learn more about mass assignment, please consult the [mass assignment documentation](#mass-assignment). -->
하지만 `create` 메서드를 사용하기 전에 모델 클래스에 `fillable` 또는 `guarded` 속성을 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 대량 할당 취약점으로부터 보호되기 때문에 이 속성들이 필요합니다. 대량 할당에 대해 더 알아보려면 [mass assignment documentation](#mass-assignment)를 참고하세요.

<a name="updates"></a>
<!-- ### Updates -->
### Updates

<!-- The `save` method may also be used to update models that already exist in the database. To update a model, you should retrieve it and set any attributes you wish to update. Then, you should call the model's `save` method. Again, the `updated_at` timestamp will automatically be updated, so there is no need to manually set its value: -->
`save` 메서드는 데이터베이스에 이미 존재하는 모델을 수정하는 데에도 사용할 수 있습니다. 모델을 수정하려면 먼저 모델을 조회한 뒤, 수정하려는 속성을 설정해야 합니다. 그런 다음 모델의 `save` 메서드를 호출합니다. 이 경우에도 `updated_at` 타임스탬프는 자동으로 업데이트되므로, 값을 직접 설정할 필요가 없습니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

<!-- Occasionally, you may need to update an existing model or create a new model if no matching model exists. Like the `firstOrCreate` method, the `updateOrCreate` method persists the model, so there's no need to manually call the `save` method. -->
때로는 기존 모델을 수정하거나, 일치하는 모델이 없으면 새 모델을 생성해야 할 수 있습니다. `firstOrCreate` 메서드와 마찬가지로 `updateOrCreate` 메서드는 모델을 저장하므로, `save` 메서드를 직접 호출할 필요가 없습니다.

<!-- In the example below, if a flight exists with a `departure` location of `Oakland` and a `destination` location of `San Diego`, its `price` and `discounted` columns will be updated. If no such flight exists, a new flight will be created which has the attributes resulting from merging the first argument array with the second argument array: -->
아래 예제에서 `departure` 위치가 `Oakland`이고 `destination` 위치가 `San Diego`인 항공편이 존재하면, 해당 항공편의 `price`와 `discounted` 컬럼이 업데이트됩니다. 그런 항공편이 없으면 첫 번째 인수 배열과 두 번째 인수 배열을 병합한 속성을 가진 새 항공편이 생성됩니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```
<!-- When using methods such as `firstOrCreate` or `updateOrCreate`, you may not know whether a new model has been created or an existing one has been updated. The `wasRecentlyCreated` property indicates if the model was created during its current lifecycle: -->
`firstOrCreate` 또는 `updateOrCreate` 같은 메서드를 사용할 때는 새 모델이 생성되었는지, 기존 모델이 업데이트되었는지 알기 어려울 수 있습니다. `wasRecentlyCreated` 속성은 현재 생명주기 동안 모델이 생성되었는지를 나타냅니다.

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // New flight record was inserted...
}
```

<a name="mass-updates"></a>
<!-- #### Mass Updates -->
#### Mass Updates

<!-- Updates can also be performed against models that match a given query. In this example, all flights that are `active` and have a `destination` of `San Diego` will be marked as delayed: -->
특정 쿼리와 일치하는 모델에 대해서도 업데이트를 수행할 수 있습니다. 이 예시에서는 `active` 상태이고 `destination`이 `San Diego`인 모든 항공편을 지연 상태로 표시합니다.

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

<!-- The `update` method expects an array of column and value pairs representing the columns that should be updated. The `update` method returns the number of affected rows. -->
`update` 메서드는 업데이트할 컬럼과 값의 쌍을 담은 배열을 기대합니다. `update` 메서드는 영향을 받은 행의 수를 반환합니다.

> [!WARNING]
> Eloquent를 통해 대량 업데이트를 실행할 때는 업데이트된 모델에 대해 `saving`, `saved`, `updating`, `updated` 모델 이벤트가 발생하지 않습니다. 대량 업데이트를 실행할 때 모델이 실제로 조회되지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
<!-- #### Examining Attribute Changes -->
#### Examining Attribute Changes

<!-- Eloquent provides the `isDirty`, `isClean`, and `wasChanged` methods to examine the internal state of your model and determine how its attributes have changed from when the model was originally retrieved. -->
Eloquent는 모델의 내부 상태를 검사하고, 모델을 처음 조회한 시점과 비교해 속성이 어떻게 변경되었는지 확인할 수 있도록 `isDirty`, `isClean`, `wasChanged` 메서드를 제공합니다.

<!-- The `isDirty` method determines if any of the model's attributes have been changed since the model was retrieved. You may pass a specific attribute name or an array of attributes to the `isDirty` method to determine if any of the attributes are "dirty". The `isClean` method will determine if an attribute has remained unchanged since the model was retrieved. This method also accepts an optional attribute argument: -->
`isDirty` 메서드는 모델을 조회한 이후 모델의 속성이 변경되었는지 확인합니다. 특정 속성 이름이나 속성 배열을 `isDirty` 메서드에 전달하여 해당 속성 중 하나라도 "더티(dirty)", 즉 변경된 상태인지 확인할 수 있습니다. `isClean` 메서드는 모델을 조회한 이후 속성이 변경되지 않은 상태로 유지되었는지 확인합니다. 이 메서드도 선택적으로 속성 인수를 받을 수 있습니다.

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

<!-- The `wasChanged` method determines if any attributes were changed when the model was last saved within the current request cycle. If needed, you may pass an attribute name to see if a particular attribute was changed: -->
`wasChanged` 메서드는 현재 요청 주기 안에서 모델이 마지막으로 저장될 때 어떤 속성이 변경되었는지 확인합니다. 필요한 경우 속성 이름을 전달하여 특정 속성이 변경되었는지 확인할 수 있습니다.

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

<!-- The `getOriginal` method returns an array containing the original attributes of the model regardless of any changes to the model since it was retrieved. If needed, you may pass a specific attribute name to get the original value of a particular attribute: -->
`getOriginal` 메서드는 모델을 조회한 이후 어떤 변경이 있었는지와 관계없이 모델의 원래 속성을 담은 배열을 반환합니다. 필요한 경우 특정 속성 이름을 전달하여 해당 속성의 원래 값을 가져올 수 있습니다.

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // Array of original attributes...
```

<!-- The `getChanges` method returns an array containing the attributes that changed when the model was last saved, while the `getPrevious` method returns an array containing the original attribute values before the model was last saved: -->
`getChanges` 메서드는 모델이 마지막으로 저장될 때 변경된 속성을 담은 배열을 반환하며, `getPrevious` 메서드는 모델이 마지막으로 저장되기 전의 원래 속성값을 담은 배열을 반환합니다.

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
<!-- ### Mass Assignment -->
### Mass Assignment

<!-- You may use the `create` method to "save" a new model using a single PHP statement. The inserted model instance will be returned to you by the method: -->
`create` 메서드를 사용하면 하나의 PHP 문장으로 새 모델을 "저장"할 수 있습니다. 삽입된 모델 인스턴스가 이 메서드에서 반환됩니다.

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

<!-- However, before using the `create` method, you will need to specify either a `fillable` or `guarded` property on your model class. These properties are required because all Eloquent models are protected against mass assignment vulnerabilities by default. -->
하지만 `create` 메서드를 사용하기 전에 모델 클래스에 `fillable` 또는 `guarded` 속성 중 하나를 지정해야 합니다. 모든 Eloquent 모델은 기본적으로 대량 할당 취약점으로부터 보호되므로 이러한 속성이 필요합니다.

<!-- A mass assignment vulnerability occurs when a user passes an unexpected HTTP request field and that field changes a column in your database that you did not expect. For example, a malicious user might send an `is_admin` parameter through an HTTP request, which is then passed to your model's `create` method, allowing the user to escalate themselves to an administrator. -->
대량 할당 취약점은 사용자가 예상하지 못한 HTTP 요청 필드를 전달하고, 그 필드가 개발자가 의도하지 않은 데이터베이스 컬럼을 변경할 때 발생합니다. 예를 들어 악의적인 사용자가 HTTP 요청을 통해 `is_admin` 파라미터를 보내고, 이 값이 모델의 `create` 메서드에 전달되면 사용자가 자신을 관리자로 승격시킬 수 있습니다.

<!-- So, to get started, you should define which model attributes you want to make mass assignable. You may do this using the `$fillable` property on the model. For example, let's make the `name` attribute of our `Flight` model mass assignable: -->
따라서 먼저 어떤 모델 속성을 대량 할당 가능하게 만들지 정의해야 합니다. 모델의 `$fillable` 속성을 사용하여 이를 설정할 수 있습니다. 예를 들어 `Flight` 모델의 `name` 속성을 대량 할당 가능하게 만들어 보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = ['name'];
}
```

<!-- Once you have specified which attributes are mass assignable, you may use the `create` method to insert a new record in the database. The `create` method returns the newly created model instance: -->
어떤 속성을 대량 할당 가능하게 할지 지정한 뒤에는 `create` 메서드를 사용하여 데이터베이스에 새 레코드를 삽입할 수 있습니다. `create` 메서드는 새로 생성된 모델 인스턴스를 반환합니다.

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

<!-- If you already have a model instance, you may use the `fill` method to populate it with an array of attributes: -->
이미 모델 인스턴스가 있다면 `fill` 메서드를 사용하여 속성 배열로 모델을 채울 수 있습니다.

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
<!-- #### Mass Assignment and JSON Columns -->
#### Mass Assignment and JSON Columns

<!-- When assigning JSON columns, each column's mass assignable key must be specified in your model's `$fillable` array. For security, Laravel does not support updating nested JSON attributes when using the `guarded` property: -->
JSON 컬럼을 할당할 때는 각 컬럼의 대량 할당 가능 키를 모델의 `$fillable` 배열에 지정해야 합니다. 보안을 위해 Laravel은 `guarded` 속성을 사용할 때 중첩된 JSON 속성 업데이트를 지원하지 않습니다.

```php
/**
 * The attributes that are mass assignable.
 *
 * @var array<int, string>
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
<!-- #### Allowing Mass Assignment -->
#### Allowing Mass Assignment

<!-- If you would like to make all of your attributes mass assignable, you may define your model's `$guarded` property as an empty array. If you choose to unguard your model, you should take special care to always hand-craft the arrays passed to Eloquent's `fill`, `create`, and `update` methods: -->
모든 속성을 대량 할당 가능하게 만들고 싶다면 모델의 `$guarded` 속성을 빈 배열로 정의할 수 있습니다. 모델의 보호를 해제하기로 했다면 Eloquent의 `fill`, `create`, `update` 메서드에 전달하는 배열을 항상 직접 신중하게 구성해야 합니다.

```php
/**
 * The attributes that aren't mass assignable.
 *
 * @var array<string>
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
<!-- #### Mass Assignment Exceptions -->
#### Mass Assignment Exceptions

<!-- By default, attributes that are not included in the `$fillable` array are silently discarded when performing mass-assignment operations. In production, this is expected behavior; however, during local development it can lead to confusion as to why model changes are not taking effect. -->
기본적으로 `$fillable` 배열에 포함되지 않은 속성은 대량 할당 작업을 수행할 때 조용히 버려집니다. 프로덕션 환경에서는 기대되는 동작입니다. 하지만 로컬 개발 중에는 모델 변경 사항이 왜 적용되지 않는지 혼란스러울 수 있습니다.

<!-- If you wish, you may instruct Laravel to throw an exception when attempting to fill an unfillable attribute by invoking the `preventSilentlyDiscardingAttributes` method. Typically, this method should be invoked in the `boot` method of your application's `AppServiceProvider` class: -->
원한다면 채울 수 없는 속성을 채우려고 할 때 Laravel이 예외를 발생시키도록 지시할 수 있습니다. 이를 위해 `preventSilentlyDiscardingAttributes` 메서드를 호출하면 됩니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스에 있는 `boot` 메서드에서 호출해야 합니다.

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
<!-- ### Upserts -->
### Upserts

<!-- Eloquent's `upsert` method may be used to update or create records in a single, atomic operation. The method's first argument consists of the values to insert or update, while the second argument lists the column(s) that uniquely identify records within the associated table. The method's third and final argument is an array of the columns that should be updated if a matching record already exists in the database. The `upsert` method will automatically set the `created_at` and `updated_at` timestamps if timestamps are enabled on the model: -->
Eloquent의 `upsert` 메서드는 하나의 원자적 작업으로 레코드를 업데이트하거나 생성하는 데 사용할 수 있습니다. 이 메서드의 첫 번째 인수는 삽입하거나 업데이트할 값으로 구성되며, 두 번째 인수는 관련 테이블에서 레코드를 고유하게 식별하는 컬럼을 나열합니다. 세 번째이자 마지막 인수는 데이터베이스에 일치하는 레코드가 이미 존재할 경우 업데이트할 컬럼 배열입니다. 모델에서 타임스탬프가 활성화되어 있다면 `upsert` 메서드는 `created_at` 및 `updated_at` 타임스탬프를 자동으로 설정합니다.

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인수에 지정한 컬럼에 "primary" 또는 "unique" 인덱스가 있어야 합니다. 또한 MariaDB와 MySQL 데이터베이스 드라이버는 `upsert` 메서드의 두 번째 인수를 무시하고, 항상 테이블의 "primary" 및 "unique" 인덱스를 사용해 기존 레코드를 감지합니다.

<a name="deleting-models"></a>
<!-- ## Deleting Models -->
## Deleting Models

<!-- To delete a model, you may call the `delete` method on the model instance: -->
모델을 삭제하려면 모델 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
<!-- #### Deleting an Existing Model by its Primary Key -->
#### Deleting an Existing Model by its Primary Key

<!-- In the example above, we are retrieving the model from the database before calling the `delete` method. However, if you know the primary key of the model, you may delete the model without explicitly retrieving it by calling the `destroy` method. In addition to accepting the single primary key, the `destroy` method will accept multiple primary keys, an array of primary keys, or a [collection](/docs/12.x/collections) of primary keys: -->
위 예시에서는 `delete` 메서드를 호출하기 전에 데이터베이스에서 모델을 조회했습니다. 하지만 모델의 기본 키를 알고 있다면 `destroy` 메서드를 호출하여 모델을 명시적으로 조회하지 않고 삭제할 수 있습니다. `destroy` 메서드는 단일 기본 키뿐 아니라 여러 기본 키, 기본 키 배열, 또는 기본 키의 [collection](/docs/12.x/collections)도 받을 수 있습니다.

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

<!-- If you are utilizing [soft deleting models](#soft-deleting), you may permanently delete models via the `forceDestroy` method: -->
[soft deleting models](#soft-deleting)을 사용하고 있다면 `forceDestroy` 메서드를 통해 모델을 영구적으로 삭제할 수 있습니다.

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 로드한 뒤 `delete` 메서드를 호출합니다. 따라서 각 모델에 대해 `deleting` 및 `deleted` 이벤트가 올바르게 디스패치됩니다.

<a name="deleting-models-using-queries"></a>
<!-- #### Deleting Models Using Queries -->
#### Deleting Models Using Queries

<!-- Of course, you may build an Eloquent query to delete all models matching your query's criteria. In this example, we will delete all flights that are marked as inactive. Like mass updates, mass deletes will not dispatch model events for the models that are deleted: -->
물론 Eloquent 쿼리를 구성하여 쿼리 조건과 일치하는 모든 모델을 삭제할 수도 있습니다. 이 예시에서는 비활성 상태로 표시된 모든 항공편을 삭제합니다. 대량 업데이트와 마찬가지로, 대량 삭제는 삭제되는 모델에 대해 모델 이벤트를 디스패치하지 않습니다.

```php
$deleted = Flight::where('active', 0)->delete();
```

<!-- To delete all models in a table, you should execute a query without adding any conditions: -->
테이블의 모든 모델을 삭제하려면 조건을 추가하지 않고 쿼리를 실행해야 합니다.

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent를 통해 대량 삭제 문을 실행할 때는 삭제된 모델에 대해 `deleting` 및 `deleted` 모델 이벤트가 디스패치되지 않습니다. 삭제 문을 실행할 때 모델이 실제로 조회되지 않기 때문입니다.

<a name="soft-deleting"></a>
<!-- ### Soft Deleting -->
### Soft Deleting

<!-- In addition to actually removing records from your database, Eloquent can also "soft delete" models. When models are soft deleted, they are not actually removed from your database. Instead, a `deleted_at` attribute is set on the model indicating the date and time at which the model was "deleted". To enable soft deletes for a model, add the `Illuminate\Database\Eloquent\SoftDeletes` trait to the model: -->
Eloquent는 데이터베이스에서 레코드를 실제로 제거하는 것뿐만 아니라 모델을 "소프트 삭제"할 수도 있습니다. 모델이 소프트 삭제되면 데이터베이스에서 실제로 제거되지 않습니다. 대신 모델에 `deleted_at` 속성이 설정되어 해당 모델이 "삭제"된 날짜와 시간을 나타냅니다. 모델에서 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가합니다.

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
> `SoftDeletes` 트레이트는 `deleted_at` 속성을 자동으로 `DateTime` / `Carbon` 인스턴스로 casting합니다.

<!-- You should also add the `deleted_at` column to your database table. The Laravel [schema builder](/docs/12.x/migrations) contains a helper method to create this column: -->
데이터베이스 테이블에도 `deleted_at` 컬럼을 추가해야 합니다. Laravel [schema builder](/docs/12.x/migrations)는 이 컬럼을 생성하는 헬퍼 메서드를 제공합니다.

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

<!-- Now, when you call the `delete` method on the model, the `deleted_at` column will be set to the current date and time. However, the model's database record will be left in the table. When querying a model that uses soft deletes, the soft deleted models will automatically be excluded from all query results. -->
이제 모델에서 `delete` 메서드를 호출하면 `deleted_at` 컬럼이 현재 날짜와 시간으로 설정됩니다. 하지만 모델의 데이터베이스 레코드는 테이블에 그대로 남습니다. 소프트 삭제를 사용하는 모델을 쿼리할 때는 소프트 삭제된 모델이 모든 쿼리 결과에서 자동으로 제외됩니다.

<!-- To determine if a given model instance has been soft deleted, you may use the `trashed` method: -->
주어진 모델 인스턴스가 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용할 수 있습니다.

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
<!-- #### Restoring Soft Deleted Models -->
#### Restoring Soft Deleted Models

<!-- Sometimes you may wish to "un-delete" a soft deleted model. To restore a soft deleted model, you may call the `restore` method on a model instance. The `restore` method will set the model's `deleted_at` column to `null`: -->
때로는 소프트 삭제된 모델의 "삭제를 취소"하고 싶을 수 있습니다. 소프트 삭제된 모델을 복원하려면 모델 인스턴스에서 `restore` 메서드를 호출하면 됩니다. `restore` 메서드는 모델의 `deleted_at` 컬럼을 `null`로 설정합니다.

```php
$flight->restore();
```

<!-- You may also use the `restore` method in a query to restore multiple models. Again, like other "mass" operations, this will not dispatch any model events for the models that are restored: -->
쿼리에서 `restore` 메서드를 사용하여 여러 모델을 복원할 수도 있습니다. 다시 말하지만, 다른 "대량" 작업과 마찬가지로 복원되는 모델에 대해 어떤 모델 이벤트도 디스패치하지 않습니다.

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

<!-- The `restore` method may also be used when building [relationship](/docs/12.x/eloquent-relationships) queries: -->
`restore` 메서드는 [relationship](/docs/12.x/eloquent-relationships) 쿼리를 구성할 때도 사용할 수 있습니다.

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
<!-- #### Permanently Deleting Models -->
#### Permanently Deleting Models

<!-- Sometimes you may need to truly remove a model from your database. You may use the `forceDelete` method to permanently remove a soft deleted model from the database table: -->
때로는 데이터베이스에서 모델을 완전히 제거해야 할 수 있습니다. `forceDelete` 메서드를 사용하여 소프트 삭제된 모델을 데이터베이스 테이블에서 영구적으로 제거할 수 있습니다.

```php
$flight->forceDelete();
```

<!-- You may also use the `forceDelete` method when building Eloquent relationship queries: -->
Eloquent 연관관계 쿼리를 구성할 때도 `forceDelete` 메서드를 사용할 수 있습니다.

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
<!-- ### Querying Soft Deleted Models -->
### Querying Soft Deleted Models

<a name="including-soft-deleted-models"></a>
<!-- #### Including Soft Deleted Models -->
#### Including Soft Deleted Models

<!-- As noted above, soft deleted models will automatically be excluded from query results. However, you may force soft deleted models to be included in a query's results by calling the `withTrashed` method on the query: -->
위에서 설명한 것처럼 소프트 삭제된 모델은 쿼리 결과에서 자동으로 제외됩니다. 하지만 쿼리에서 `withTrashed` 메서드를 호출하면 소프트 삭제된 모델이 쿼리 결과에 포함되도록 강제할 수 있습니다.

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

<!-- The `withTrashed` method may also be called when building a [relationship](/docs/12.x/eloquent-relationships) query: -->
`withTrashed` 메서드는 [relationship](/docs/12.x/eloquent-relationships) 쿼리를 구성할 때도 호출할 수 있습니다.
```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
<!-- #### Retrieving Only Soft Deleted Models -->
#### Retrieving Only Soft Deleted Models

<!-- The `onlyTrashed` method will retrieve **only** soft deleted models: -->
`onlyTrashed` 메서드는 **소프트 삭제된** 모델만 조회합니다.

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
<!-- ## Pruning Models -->
## Pruning Models

<!-- Sometimes you may want to periodically delete models that are no longer needed. To accomplish this, you may add the `Illuminate\Database\Eloquent\Prunable` or `Illuminate\Database\Eloquent\MassPrunable` trait to the models you would like to periodically prune. After adding one of the traits to the model, implement a `prunable` method which returns an Eloquent query builder that resolves the models that are no longer needed: -->
때로는 더 이상 필요하지 않은 모델을 주기적으로 삭제하고 싶을 수 있습니다. 이를 위해 주기적으로 가지치기하려는 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` trait을 추가할 수 있습니다. 모델에 이 trait 중 하나를 추가한 뒤에는, 더 이상 필요하지 않은 모델을 결정하는 Eloquent 쿼리 빌더를 반환하는 `prunable` 메서드를 구현합니다.

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

<!-- When marking models as `Prunable`, you may also define a `pruning` method on the model. This method will be called before the model is deleted. This method can be useful for deleting any additional resources associated with the model, such as stored files, before the model is permanently removed from the database: -->
모델을 `Prunable`로 표시할 때, 모델에 `pruning` 메서드를 정의할 수도 있습니다. 이 메서드는 모델이 삭제되기 전에 호출됩니다. 이 메서드는 모델이 데이터베이스에서 영구적으로 제거되기 전에, 저장된 파일처럼 모델과 연결된 추가 리소스를 삭제할 때 유용합니다.

```php
/**
 * Prepare the model for pruning.
 */
protected function pruning(): void
{
    // ...
}
```

<!-- After configuring your prunable model, you should schedule the `model:prune` Artisan command in your application's `routes/console.php` file. You are free to choose the appropriate interval at which this command should be run: -->
가지치기 가능한 모델 설정을 마친 뒤에는 애플리케이션의 `routes/console.php` 파일에서 `model:prune` Artisan 명령어를 스케줄링해야 합니다. 이 명령어가 실행될 적절한 주기는 자유롭게 선택할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

<!-- Behind the scenes, the `model:prune` command will automatically detect "Prunable" models within your application's `app/Models` directory. If your models are in a different location, you may use the `--model` option to specify the model class names: -->
내부적으로 `model:prune` 명령어는 애플리케이션의 `app/Models` 디렉터리 안에 있는 "Prunable" 모델을 자동으로 감지합니다. 모델이 다른 위치에 있다면 `--model` 옵션을 사용하여 모델 클래스명을 지정할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

<!-- If you wish to exclude certain models from being pruned while pruning all other detected models, you may use the `--except` option: -->
감지된 다른 모든 모델은 가지치기하되 특정 모델만 제외하고 싶다면 `--except` 옵션을 사용할 수 있습니다.

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

<!-- You may test your `prunable` query by executing the `model:prune` command with the `--pretend` option. When pretending, the `model:prune` command will simply report how many records would be pruned if the command were to actually run: -->
`--pretend` 옵션과 함께 `model:prune` 명령어를 실행하여 `prunable` 쿼리를 테스트할 수 있습니다. pretend 모드에서는 `model:prune` 명령어가 실제로 실행될 경우 몇 개의 레코드가 가지치기될지만 보고합니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제된 모델이 prunable 쿼리와 일치하면 영구적으로 삭제됩니다(`forceDelete`).

<a name="mass-pruning"></a>
<!-- #### Mass Pruning -->
#### Mass Pruning

<!-- When models are marked with the `Illuminate\Database\Eloquent\MassPrunable` trait, models are deleted from the database using mass-deletion queries. Therefore, the `pruning` method will not be invoked, nor will the `deleting` and `deleted` model events be dispatched. This is because the models are never actually retrieved before deletion, thus making the pruning process much more efficient: -->
모델에 `Illuminate\Database\Eloquent\MassPrunable` trait이 표시되어 있으면, 모델은 대량 삭제 쿼리를 사용하여 데이터베이스에서 삭제됩니다. 따라서 `pruning` 메서드는 호출되지 않으며, `deleting` 및 `deleted` 모델 이벤트도 디스패치되지 않습니다. 이는 삭제 전에 모델을 실제로 조회하지 않기 때문이며, 그 결과 가지치기 과정이 훨씬 더 효율적입니다.

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
<!-- ## Replicating Models -->
## Replicating Models

<!-- You may create an unsaved copy of an existing model instance using the `replicate` method. This method is particularly useful when you have model instances that share many of the same attributes: -->
`replicate` 메서드를 사용하여 기존 모델 인스턴스의 저장되지 않은 복사본을 만들 수 있습니다. 이 메서드는 같은 속성을 많이 공유하는 모델 인스턴스가 있을 때 특히 유용합니다.

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

<!-- To exclude one or more attributes from being replicated to the new model, you may pass an array to the `replicate` method: -->
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
<!-- ## Query Scopes -->
## Query Scopes

<a name="global-scopes"></a>
<!-- ### Global Scopes -->
### Global Scopes

<!-- Global scopes allow you to add constraints to all queries for a given model. Laravel's own [soft delete](#soft-deleting) functionality utilizes global scopes to only retrieve "non-deleted" models from the database. Writing your own global scopes can provide a convenient, easy way to make sure every query for a given model receives certain constraints. -->
전역 스코프를 사용하면 특정 모델의 모든 쿼리에 제약 조건을 추가할 수 있습니다. Laravel 자체의 [soft delete](#soft-deleting) 기능은 전역 스코프를 활용하여 데이터베이스에서 "삭제되지 않은" 모델만 조회합니다. 직접 전역 스코프를 작성하면 특정 모델의 모든 쿼리에 특정 제약 조건이 적용되도록 편리하고 쉽게 보장할 수 있습니다.

<a name="generating-scopes"></a>
<!-- #### Generating Scopes -->
#### Generating Scopes

<!-- To generate a new global scope, you may invoke the `make:scope` Artisan command, which will place the generated scope in your application's `app/Models/Scopes` directory: -->
새 전역 스코프를 생성하려면 `make:scope` Artisan 명령어를 호출할 수 있습니다. 생성된 스코프는 애플리케이션의 `app/Models/Scopes` 디렉터리에 배치됩니다.

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
<!-- #### Writing Global Scopes -->
#### Writing Global Scopes

<!-- Writing a global scope is simple. First, use the `make:scope` command to generate a class that implements the `Illuminate\Database\Eloquent\Scope` interface. The `Scope` interface requires you to implement one method: `apply`. The `apply` method may add `where` constraints or other types of clauses to the query as needed: -->
전역 스코프를 작성하는 일은 간단합니다. 먼저 `make:scope` 명령어를 사용하여 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스를 생성합니다. `Scope` 인터페이스는 하나의 메서드, 즉 `apply`를 구현하도록 요구합니다. `apply` 메서드는 필요에 따라 쿼리에 `where` 제약 조건이나 다른 종류의 절을 추가할 수 있습니다.

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
> 전역 스코프가 쿼리의 select 절에 컬럼을 추가하는 경우, `select` 대신 `addSelect` 메서드를 사용해야 합니다. 이렇게 하면 쿼리의 기존 select 절이 의도치 않게 대체되는 일을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
<!-- #### Applying Global Scopes -->
#### Applying Global Scopes

<!-- To assign a global scope to a model, you may simply place the `ScopedBy` attribute on the model: -->
모델에 전역 스코프를 지정하려면 모델에 `ScopedBy` 속성을 배치하면 됩니다.

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

<!-- Or, you may manually register the global scope by overriding the model's `booted` method and invoke the model's `addGlobalScope` method. The `addGlobalScope` method accepts an instance of your scope as its only argument: -->
또는 모델의 `booted` 메서드를 오버라이드하고 모델의 `addGlobalScope` 메서드를 호출하여 전역 스코프를 직접 등록할 수 있습니다. `addGlobalScope` 메서드는 유일한 인수로 스코프 인스턴스를 받습니다.

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

<!-- After adding the scope in the example above to the `App\Models\User` model, a call to the `User::all()` method will execute the following SQL query: -->
위 예시의 스코프를 `App\Models\User` 모델에 추가한 후 `User::all()` 메서드를 호출하면 다음 SQL 쿼리가 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
<!-- #### Anonymous Global Scopes -->
#### Anonymous Global Scopes

<!-- Eloquent also allows you to define global scopes using closures, which is particularly useful for simple scopes that do not warrant a separate class of their own. When defining a global scope using a closure, you should provide a scope name of your own choosing as the first argument to the `addGlobalScope` method: -->
Eloquent에서는 클로저를 사용하여 전역 스코프를 정의할 수도 있습니다. 이는 별도의 클래스를 만들 필요가 없는 단순한 스코프에 특히 유용합니다. 클로저로 전역 스코프를 정의할 때는 `addGlobalScope` 메서드의 첫 번째 인수로 원하는 스코프 이름을 제공해야 합니다.

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
<!-- #### Removing Global Scopes -->
#### Removing Global Scopes

<!-- If you would like to remove a global scope for a given query, you may use the `withoutGlobalScope` method. This method accepts the class name of the global scope as its only argument: -->
특정 쿼리에서 전역 스코프를 제거하려면 `withoutGlobalScope` 메서드를 사용할 수 있습니다. 이 메서드는 유일한 인수로 전역 스코프의 클래스명을 받습니다.

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

<!-- Or, if you defined the global scope using a closure, you should pass the string name that you assigned to the global scope: -->
또는 클로저를 사용하여 전역 스코프를 정의했다면, 전역 스코프에 지정한 문자열 이름을 전달해야 합니다.

```php
User::withoutGlobalScope('ancient')->get();
```

<!-- If you would like to remove several or even all of the query's global scopes, you may use the `withoutGlobalScopes` and `withoutGlobalScopesExcept` methods: -->
쿼리의 여러 전역 스코프 또는 모든 전역 스코프를 제거하고 싶다면 `withoutGlobalScopes` 및 `withoutGlobalScopesExcept` 메서드를 사용할 수 있습니다.

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
<!-- ### Local Scopes -->
### Local Scopes

<!-- Local scopes allow you to define common sets of query constraints that you may easily re-use throughout your application. For example, you may need to frequently retrieve all users that are considered "popular". To define a scope, add the `Scope` attribute to an Eloquent method. -->
로컬 스코프를 사용하면 애플리케이션 전반에서 쉽게 재사용할 수 있는 공통 쿼리 제약 조건 집합을 정의할 수 있습니다. 예를 들어 "인기 있는" 사용자로 간주되는 모든 사용자를 자주 조회해야 할 수 있습니다. 스코프를 정의하려면 Eloquent 메서드에 `Scope` 속성을 추가합니다.

<!-- Scopes should always return the same query builder instance or `void`: -->
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
<!-- #### Utilizing a Local Scope -->
#### Utilizing a Local Scope

<!-- Once the scope has been defined, you may call the scope methods when querying the model. You can even chain calls to various scopes: -->
스코프가 정의되면 모델을 쿼리할 때 스코프 메서드를 호출할 수 있습니다. 여러 스코프 호출을 체인으로 연결할 수도 있습니다.

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

<!-- Combining multiple Eloquent model scopes via an `or` query operator may require the use of closures to achieve the correct [logical grouping](/docs/12.x/queries#logical-grouping): -->
`or` 쿼리 연산자를 통해 여러 Eloquent 모델 스코프를 결합할 때는 올바른 [logical grouping](/docs/12.x/queries#logical-grouping)를 위해 클로저를 사용해야 할 수 있습니다.

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

<!-- However, since this can be cumbersome, Laravel provides a "higher order" `orWhere` method that allows you to fluently chain scopes together without the use of closures: -->
하지만 이 방식은 번거로울 수 있으므로, Laravel은 클로저를 사용하지 않고도 스코프를 유창하게 체인으로 연결할 수 있는 "고차" `orWhere` 메서드를 제공합니다.

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
<!-- #### Dynamic Scopes -->
#### Dynamic Scopes

<!-- Sometimes you may wish to define a scope that accepts parameters. To get started, just add your additional parameters to your scope method's signature. Scope parameters should be defined after the `$query` parameter: -->
때로는 매개변수를 받는 스코프를 정의하고 싶을 수 있습니다. 시작하려면 스코프 메서드의 시그니처에 추가 매개변수를 넣으면 됩니다. 스코프 매개변수는 `$query` 매개변수 뒤에 정의해야 합니다.

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

<!-- Once the expected arguments have been added to your scope method's signature, you may pass the arguments when calling the scope: -->
예상되는 인수를 스코프 메서드의 시그니처에 추가했다면, 스코프를 호출할 때 해당 인수를 전달할 수 있습니다.
```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
<!-- ### Pending Attributes -->
### Pending Attributes

<!-- If you would like to use scopes to create models that have the same attributes as those used to constrain the scope, you may use the `withAttributes` method when building the scope query: -->
스코프를 제한하는 데 사용한 속성과 동일한 속성을 가진 모델을 스코프로 생성하고 싶다면, 스코프 쿼리를 구성할 때 `withAttributes` 메서드를 사용할 수 있습니다.

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

<!-- The `withAttributes` method will add `where` conditions to the query using the given attributes, and it will also add the given attributes to any models created via the scope: -->
`withAttributes` 메서드는 주어진 속성을 사용해 쿼리에 `where` 조건을 추가하며, 해당 스코프를 통해 생성되는 모든 모델에도 주어진 속성을 추가합니다.

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

<!-- To instruct the `withAttributes` method to not add `where` conditions to the query, you may set the `asConditions` argument to `false`: -->
`withAttributes` 메서드가 쿼리에 `where` 조건을 추가하지 않도록 하려면, `asConditions` 인수를 `false`로 설정하면 됩니다.

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
<!-- ## Comparing Models -->
## Comparing Models

<!-- Sometimes you may need to determine if two models are the "same" or not. The `is` and `isNot` methods may be used to quickly verify two models have the same primary key, table, and database connection or not: -->
때로는 두 모델이 "같은" 모델인지 확인해야 할 수 있습니다. `is`와 `isNot` 메서드를 사용하면 두 모델이 같은 기본 키, 테이블, 데이터베이스 연결을 가지고 있는지 빠르게 확인할 수 있습니다.

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

<!-- The `is` and `isNot` methods are also available when using the `belongsTo`, `hasOne`, `morphTo`, and `morphOne` [relationships](/docs/12.x/eloquent-relationships). This method is particularly helpful when you would like to compare a related model without issuing a query to retrieve that model: -->
`is`와 `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne` [relationships](/docs/12.x/eloquent-relationships)를 사용할 때도 사용할 수 있습니다. 이 메서드는 관련 모델을 가져오기 위해 쿼리를 실행하지 않고도 해당 모델을 비교하고 싶을 때 특히 유용합니다.

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
<!-- ## Events -->
## Events

> [!NOTE]
> Eloquent 이벤트를 클라이언트 측 애플리케이션으로 직접 broadcast하고 싶으신가요? Laravel의 [model event broadcasting](/docs/12.x/broadcasting#model-broadcasting)을 확인해 보세요.

<!-- Eloquent models dispatch several events, allowing you to hook into the following moments in a model's lifecycle: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, and `replicating`. -->
Eloquent 모델은 여러 이벤트를 발생시켜, 모델 생명주기의 다음 시점에 원하는 로직을 연결할 수 있게 해줍니다. `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

<!-- The `retrieved` event will dispatch when an existing model is retrieved from the database. When a new model is saved for the first time, the `creating` and `created` events will dispatch. The `updating` / `updated` events will dispatch when an existing model is modified and the `save` method is called. The `saving` / `saved` events will dispatch when a model is created or updated - even if the model's attributes have not been changed. Event names ending with `-ing` are dispatched before any changes to the model are persisted, while events ending with `-ed` are dispatched after the changes to the model are persisted. -->
`retrieved` 이벤트는 기존 모델이 데이터베이스에서 조회될 때 발생합니다. 새 모델이 처음 저장될 때는 `creating`과 `created` 이벤트가 발생합니다. 기존 모델이 수정되고 `save` 메서드가 호출되면 `updating` / `updated` 이벤트가 발생합니다. 모델이 생성되거나 업데이트될 때는 모델의 속성이 변경되지 않았더라도 `saving` / `saved` 이벤트가 발생합니다. 이름이 `-ing`으로 끝나는 이벤트는 모델의 변경 사항이 저장되기 전에 발생하고, `-ed`로 끝나는 이벤트는 모델의 변경 사항이 저장된 후에 발생합니다.

<!-- To start listening to model events, define a `$dispatchesEvents` property on your Eloquent model. This property maps various points of the Eloquent model's lifecycle to your own [event classes](/docs/12.x/events). Each model event class should expect to receive an instance of the affected model via its constructor: -->
모델 이벤트 수신을 시작하려면 Eloquent 모델에 `$dispatchesEvents` 속성을 정의하세요. 이 속성은 Eloquent 모델 생명주기의 여러 지점을 직접 만든 [event classes](/docs/12.x/events)에 매핑합니다. 각 모델 이벤트 클래스는 생성자를 통해 영향을 받은 모델 인스턴스를 받을 수 있어야 합니다.

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

<!-- After defining and mapping your Eloquent events, you may use [event listeners](/docs/12.x/events#defining-listeners) to handle the events. -->
Eloquent 이벤트를 정의하고 매핑한 후에는 [event listeners](/docs/12.x/events#defining-listeners)를 사용해 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent를 통해 대량 업데이트 또는 삭제 쿼리를 실행하면, 영향을 받은 모델에 대해 `saved`, `updated`, `deleting`, `deleted` 모델 이벤트가 발생하지 않습니다. 대량 업데이트나 삭제를 수행할 때는 모델이 실제로 조회되지 않기 때문입니다.

<a name="events-using-closures"></a>
<!-- ### Using Closures -->
### Using Closures

<!-- Instead of using custom event classes, you may register closures that execute when various model events are dispatched. Typically, you should register these closures in the `booted` method of your model: -->
커스텀 이벤트 클래스를 사용하는 대신, 다양한 모델 이벤트가 발생할 때 실행될 클로저를 등록할 수 있습니다. 일반적으로 이러한 클로저는 모델의 `booted` 메서드 안에 등록해야 합니다.

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

<!-- If needed, you may utilize [queueable anonymous event listeners](/docs/12.x/events#queuable-anonymous-event-listeners) when registering model events. This will instruct Laravel to execute the model event listener in the background using your application's [queue](/docs/12.x/queues): -->
필요하다면 모델 이벤트를 등록할 때 [queueable anonymous event listeners](/docs/12.x/events#queuable-anonymous-event-listeners)를 사용할 수 있습니다. 이렇게 하면 Laravel이 애플리케이션의 [queue](/docs/12.x/queues)를 사용해 모델 이벤트 리스너를 백그라운드에서 실행합니다.

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
<!-- ### Observers -->
### Observers

<a name="defining-observers"></a>
<!-- #### Defining Observers -->
#### Defining Observers

<!-- If you are listening for many events on a given model, you may use observers to group all of your listeners into a single class. Observer classes have method names which reflect the Eloquent events you wish to listen for. Each of these methods receives the affected model as their only argument. The `make:observer` Artisan command is the easiest way to create a new observer class: -->
특정 모델의 여러 이벤트를 수신하고 있다면, 옵저버를 사용해 모든 리스너를 하나의 클래스로 묶을 수 있습니다. 옵저버 클래스에는 수신하려는 Eloquent 이벤트를 반영한 메서드 이름이 있습니다. 각 메서드는 영향을 받은 모델을 유일한 인수로 받습니다. 새 옵저버 클래스를 만드는 가장 쉬운 방법은 `make:observer` Artisan 명령어를 사용하는 것입니다.

```shell
php artisan make:observer UserObserver --model=User
```

<!-- This command will place the new observer in your `app/Observers` directory. If this directory does not exist, Artisan will create it for you. Your fresh observer will look like the following: -->
이 명령어는 새 옵저버를 `app/Observers` 디렉터리에 배치합니다. 이 디렉터리가 없다면 Artisan이 자동으로 생성합니다. 새로 생성된 옵저버는 다음과 같습니다.

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

<!-- To register an observer, you may place the `ObservedBy` attribute on the corresponding model: -->
옵저버를 등록하려면 해당 모델에 `ObservedBy` 속성을 배치하면 됩니다.

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```

<!-- Or, you may manually register an observer by invoking the `observe` method on the model you wish to observe. You may register observers in the `boot` method of your application's `AppServiceProvider` class: -->
또는 관찰하려는 모델에서 `observe` 메서드를 호출해 옵저버를 직접 등록할 수도 있습니다. 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 옵저버를 등록할 수 있습니다.

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
> 옵저버가 수신할 수 있는 추가 이벤트로는 `saving`, `retrieved` 등이 있습니다. 이러한 이벤트는 [events](#events) 문서에 설명되어 있습니다.

<a name="observers-and-database-transactions"></a>
<!-- #### Observers and Database Transactions -->
#### Observers and Database Transactions

<!-- When models are being created within a database transaction, you may want to instruct an observer to only execute its event handlers after the database transaction is committed. You may accomplish this by implementing the `ShouldHandleEventsAfterCommit` interface on your observer. If a database transaction is not in progress, the event handlers will execute immediately: -->
데이터베이스 트랜잭션 안에서 모델이 생성되는 경우, 데이터베이스 트랜잭션이 커밋된 후에만 옵저버의 이벤트 핸들러가 실행되도록 하고 싶을 수 있습니다. 옵저버에 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하면 이를 처리할 수 있습니다. 진행 중인 데이터베이스 트랜잭션이 없다면 이벤트 핸들러는 즉시 실행됩니다.

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
<!-- ### Muting Events -->
### Muting Events

<!-- You may occasionally need to temporarily "mute" all events fired by a model. You may achieve this using the `withoutEvents` method. The `withoutEvents` method accepts a closure as its only argument. Any code executed within this closure will not dispatch model events, and any value returned by the closure will be returned by the `withoutEvents` method: -->
가끔 모델에서 발생하는 모든 이벤트를 일시적으로 "비활성화"해야 할 수 있습니다. `withoutEvents` 메서드를 사용하면 이를 처리할 수 있습니다. `withoutEvents` 메서드는 클로저를 유일한 인수로 받습니다. 이 클로저 안에서 실행되는 모든 코드는 모델 이벤트를 발생시키지 않으며, 클로저가 반환하는 값은 `withoutEvents` 메서드의 반환값이 됩니다.

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
<!-- #### Saving a Single Model Without Events -->
#### Saving a Single Model Without Events

<!-- Sometimes you may wish to "save" a given model without dispatching any events. You may accomplish this using the `saveQuietly` method: -->
때로는 어떤 이벤트도 발생시키지 않고 특정 모델을 "저장"하고 싶을 수 있습니다. `saveQuietly` 메서드를 사용하면 이를 처리할 수 있습니다.

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

<!-- You may also "update", "delete", "soft delete", "restore", and "replicate" a given model without dispatching any events: -->
특정 모델을 이벤트 없이 "업데이트", "삭제", "소프트 삭제", "복원", "복제"할 수도 있습니다.

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
