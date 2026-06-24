<!-- # Eloquent: Getting Started -->
# Eloquent: Getting Started

- [Introduction](#introduction)
- [Generating Model Classes](#generating-model-classes)
- [Eloquent Model Conventions](#eloquent-model-conventions)
    - [Table Names](#table-names)
    - [Primary Keys](#primary-keys)
    - [UUID & ULID Keys](#uuid-and-ulid-keys)
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
    - [Retrieving Or Creating Models](#retrieving-or-creating-models)
    - [Retrieving Aggregates](#retrieving-aggregates)
- [Inserting & Updating Models](#inserting-and-updating-models)
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
- [Comparing Models](#comparing-models)
- [Events](#events)
    - [Using Closures](#events-using-closures)
    - [Observers](#observers)
    - [Muting Events](#muting-events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel includes Eloquent, an object-relational mapper (ORM) that makes it enjoyable to interact with your database. When using Eloquent, each database table has a corresponding "Model" that is used to interact with that table. In addition to retrieving records from the database table, Eloquent models allow you to insert, update, and delete records from the table as well. -->
Laravel은 데이터베이스와 즐겁게 상호작용할 수 있도록 해주는 객체 관계 매퍼(ORM)인 Eloquent를 포함하고 있습니다. Eloquent를 사용할 때, 각 데이터베이스 테이블은 그 테이블과 상호작용하는 "모델(Model)" 클래스를 갖게 됩니다. Eloquent 모델을 사용하면 데이터베이스 테이블에서 레코드를 조회할 뿐만 아니라, 레코드를 삽입, 수정, 삭제하는 작업도 수행할 수 있습니다.

> [!NOTE]
> 시작하기 전에, 애플리케이션의 `config/database.php` 구성 파일에서 데이터베이스 커넥션을 반드시 설정해야 합니다. 데이터베이스 설정에 대한 자세한 내용은 [the database configuration documentation](/docs/9.x/database#configuration)를 참고하세요.

<!-- #### Laravel Bootcamp -->
#### Laravel Bootcamp

<!-- If you're new to Laravel, feel free to jump into the [Laravel Bootcamp](https://bootcamp.laravel.com). The Laravel Bootcamp will walk you through building your first Laravel application using Eloquent. It's a great way to get a tour of everything the Laravel and Eloquent have to offer. -->
Laravel을 처음 접한다면 [Laravel Bootcamp](https://bootcamp.laravel.com)에서 바로 시작해보셔도 좋습니다. Laravel Bootcamp는 Eloquent를 사용하여 첫 번째 Laravel 애플리케이션을 만드는 과정을 단계별로 안내합니다. Laravel과 Eloquent의 다양한 기능을 빠르게 체험해보기 좋은 방법입니다.

<a name="generating-model-classes"></a>
<!-- ## Generating Model Classes -->
## Generating Model Classes

<!-- To get started, let's create an Eloquent model. Models typically live in the `app\Models` directory and extend the `Illuminate\Database\Eloquent\Model` class. You may use the `make:model` [Artisan command](/docs/9.x/artisan) to generate a new model: -->
이제 Eloquent 모델을 한번 만들어보겠습니다. 모델 클래스는 일반적으로 `app\Models` 디렉터리에 위치하며, `Illuminate\Database\Eloquent\Model` 클래스를 확장합니다. [Artisan command](/docs/9.x/artisan)인 `make:model`을 사용하여 새 모델을 생성할 수 있습니다.

```shell
php artisan make:model Flight
```

<!-- If you would like to generate a [database migration](/docs/9.x/migrations) when you generate the model, you may use the `--migration` or `-m` option: -->
모델을 생성할 때 [database migration](/docs/9.x/migrations)도 함께 생성하고 싶다면, `--migration` 또는 `-m` 옵션을 사용할 수 있습니다.

```shell
php artisan make:model Flight --migration
```

<!-- You may generate various other types of classes when generating a model, such as factories, seeders, policies, controllers, and form requests. In addition, these options may be combined to create multiple classes at once: -->
모델 생성 시 팩토리, 시더, 폴리시, 컨트롤러, 폼 요청 등 다양한 유형의 클래스도 함께 생성할 수 있습니다. 이러한 옵션들을 조합하여 여러 클래스를 한 번에 생성하는 것도 가능합니다.

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

# Generate a pivot model...
php artisan make:model Member --pivot
```

<a name="inspecting-models"></a>
<!-- #### Inspecting Models -->
#### Inspecting Models

<!-- Sometimes it can be difficult to determine all of a model's available attributes and relationships just by skimming its code. Instead, try the `model:show` Artisan command, which provides a convenient overview of all the model's attributes and relations: -->
모델 코드만 훑어봐서는 어느 속성(attribute)과 연관관계(relation)가 정의되어 있는지 파악하기 어려운 경우가 있습니다. 이럴 땐 `model:show` Artisan 명령어를 사용해 모델의 속성과 관계를 한눈에 확인할 수 있습니다.

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
<!-- ## Eloquent Model Conventions -->
## Eloquent Model Conventions

<!-- Models generated by the `make:model` command will be placed in the `app/Models` directory. Let's examine a basic model class and discuss some of Eloquent's key conventions: -->
`make:model` 명령어로 생성된 모델은 `app/Models` 디렉터리에 위치하게 됩니다. 기본적인 모델 클래스를 살펴보며, Eloquent의 주요 관례 몇 가지를 알아보겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    //
}
```

<a name="table-names"></a>
<!-- ### Table Names -->
### Table Names

<!-- After glancing at the example above, you may have noticed that we did not tell Eloquent which database table corresponds to our `Flight` model. By convention, the "snake case", plural name of the class will be used as the table name unless another name is explicitly specified. So, in this case, Eloquent will assume the `Flight` model stores records in the `flights` table, while an `AirTrafficController` model would store records in an `air_traffic_controllers` table. -->
위 예시에서 보듯이, 우리는 `Flight` 모델이 어떤 데이터베이스 테이블과 연결되는지 별도로 지정하지 않았습니다. Eloquent는 관례적으로 "스네이크 케이스" 복수형(class명)을 테이블명으로 사용합니다. 예를 들어, 위의 경우 `Flight` 모델은 `flights` 테이블에 레코드를 저장한다고 간주하고, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블을 사용한다고 판단합니다.

<!-- If your model's corresponding database table does not fit this convention, you may manually specify the model's table name by defining a `table` property on the model: -->
만약 모델과 연결할 데이터베이스 테이블이 이 관례를 따르지 않는다면, 모델의 `table` 속성을 통해 테이블명을 직접 지정할 수 있습니다.

```
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
Eloquent는 각 모델이 연결된 데이터베이스 테이블에 기본 키 컬럼명이 `id`일 것이라 가정합니다. 만약 기본 키로 사용할 컬럼명이 다르다면, 모델에 protected `$primaryKey` 속성을 정의하여 사용할 기본 키 컬럼명을 지정할 수 있습니다.

```
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
기본적으로 Eloquent는 기본 키가 자동 증가하는 정수(integer) 값이라고 가정하며, 기본 키 값을 자동으로 정수로 casting합니다. 만약 숫자가 아니거나 자동 증가하지 않는 기본 키를 사용하려면, 모델에 `false`로 설정된 public `$incrementing` 속성을 정의해야 합니다.

```
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
기본 키 컬럼이 정수가 아닌 경우에는 모델에 protected `$keyType` 속성을 정의해야 합니다. 이 속성은 `string` 값을 가져야 합니다.

```
<?php

class Flight extends Model
{
    /**
     * The data type of the auto-incrementing ID.
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
Eloquent는 각 모델에 최소 하나의 고유 "ID"가 존재하여 기본 키로 사용될 수 있어야 한다고 요구합니다. 여러 컬럼을 조합한 "복합 기본 키"는 Eloquent 모델에서 지원하지 않습니다. 대신, 데이터베이스 테이블에는 단일 기본 키 외에 여러 컬럼을 조합한 unique 인덱스를 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
<!-- ### UUID & ULID Keys -->
### UUID & ULID Keys

<!-- Instead of using auto-incrementing integers as your Eloquent model's primary keys, you may choose to use UUIDs instead. UUIDs are universally unique alpha-numeric identifiers that are 36 characters long. -->
기본적으로 Eloquent 모델의 기본 키로는 자동 증가하는 정수 값을 사용하지만, UUID도 사용할 수 있습니다. UUID는 36자 길이의 전역적으로 고유한 영숫자 식별자입니다.

<!-- If you would like a model to use a UUID key instead of an auto-incrementing integer key, you may use the `Illuminate\Database\Eloquent\Concerns\HasUuids` trait on the model. Of course, you should ensure that the model has a [UUID equivalent primary key column](/docs/9.x/migrations#column-method-uuid): -->
모델에서 자동 증가 정수 대신 UUID를 기본 키로 사용하고 싶다면 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레잇(trait)을 모델에 적용하세요. 이 때, 모델에 [UUID equivalent primary key column](/docs/9.x/migrations#column-method-uuid)이 반드시 있어야 합니다.

```
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

<!-- By default, The `HasUuids` trait will generate ["ordered" UUIDs](/docs/9.x/helpers#method-str-ordered-uuid) for your models. These UUIDs are more efficient for indexed database storage because they can be sorted lexicographically. -->
기본적으로 `HasUuids` 트레잇은 ["ordered" UUIDs](/docs/9.x/helpers#method-str-ordered-uuid)를 생성합니다. 이러한 UUID는 사전식(lexicographical)으로 정렬할 수 있으므로, 데이터베이스 인덱싱에 더 효율적입니다.

<!-- You can override the UUID generation process for a given model by defining a `newUniqueId` method on the model. In addition, you may specify which columns should receive UUIDs by defining a `uniqueIds` method on the model: -->
모델에 `newUniqueId` 메서드를 정의하면 UUID 생성 방식을 오버라이드(재정의)할 수 있습니다. 또한 `uniqueIds` 메서드를 정의하여 어떤 컬럼에 UUID를 할당할지 지정할 수도 있습니다.

```
use Ramsey\Uuid\Uuid;

/**
 * Generate a new UUID for the model.
 *
 * @return string
 */
public function newUniqueId()
{
    return (string) Uuid::uuid4();
}

/**
 * Get the columns that should receive a unique identifier.
 *
 * @return array
 */
public function uniqueIds()
{
    return ['id', 'discount_code'];
}
```

<!-- If you wish, you may choose to utilize "ULIDs" instead of UUIDs. ULIDs are similar to UUIDs; however, they are only 26 characters in length. Like ordered UUIDs, ULIDs are lexicographically sortable for efficient database indexing. To utilize ULIDs, you should use the `Illuminate\Database\Eloquent\Concerns\HasUlids` trait on your model. You should also ensure that the model has a [ULID equivalent primary key column](/docs/9.x/migrations#column-method-ulid): -->
원한다면 UUID 대신 "ULID"도 사용할 수 있습니다. ULID는 UUID와 유사하지만, 26자리만 사용합니다. 정렬 가능한 UUID처럼 ULID도 사전식(lexicographical)으로 정렬이 가능하여 인덱싱 효율이 높습니다. ULID를 사용하려면 `Illuminate\Database\Eloquent\Concerns\HasUlids` 트레잇을 모델에 적용하고, [ULID equivalent primary key column](/docs/9.x/migrations#column-method-ulid)이 정의되어 있는지 확인하세요.

```
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

<!-- By default, Eloquent expects `created_at` and `updated_at` columns to exist on your model's corresponding database table.  Eloquent will automatically set these column's values when models are created or updated. If you do not want these columns to be automatically managed by Eloquent, you should define a `$timestamps` property on your model with a value of `false`: -->
기본적으로 Eloquent는 `created_at`, `updated_at` 컬럼이 모델과 연결된 테이블에 존재하리라 기대합니다. Eloquent는 모델이 생성되거나 수정될 때 이 컬럼들의 값을 자동으로 설정합니다. 만약 Eloquent가 이러한 컬럼을 자동으로 관리하지 않길 원한다면, 모델에서 `$timestamps` 속성을 `false`로 지정하면 됩니다.

```
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
타임스탬프의 저장 포맷을 맞춤 설정하려면, 모델의 `$dateFormat` 속성을 설정하세요. 이 속성은 데이터베이스에 날짜 속성을 저장하는 포맷과, 모델이 배열이나 JSON으로 직렬화될 때의 포맷 모두에 적용됩니다.

```
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
타임스탬프로 사용할 컬럼명을 커스터마이즈하려면, 모델에 `CREATED_AT` 및 `UPDATED_AT` 상수를 정의해주면 됩니다.

```
<?php

class Flight extends Model
{
    const CREATED_AT = 'creation_date';
    const UPDATED_AT = 'updated_date';
}
```

<!-- If you would like to perform model operations without the model having its `updated_at` timestamp modified, you may operate on the model within a closure given to the `withoutTimestamps` method: -->
모델의 `updated_at` 값이 변경되지 않도록 하면서 모델을 조작하려면, `withoutTimestamps` 메서드의 클로저 내부에서 관련 작업을 수행하면 됩니다.

```
Model::withoutTimestamps(fn () => $post->increment(['reads']));
```

<a name="database-connections"></a>
<!-- ### Database Connections -->
### Database Connections

<!-- By default, all Eloquent models will use the default database connection that is configured for your application. If you would like to specify a different connection that should be used when interacting with a particular model, you should define a `$connection` property on the model: -->
기본적으로 모든 Eloquent 모델은 애플리케이션에 설정된 기본 데이터베이스 커넥션을 사용합니다. 특정 모델에 대해 다른 데이터베이스 커넥션을 사용하려면, 모델에 `$connection` 속성을 지정해주면 됩니다.

```
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
    protected $connection = 'sqlite';
}
```

<a name="default-attribute-values"></a>
<!-- ### Default Attribute Values -->
### Default Attribute Values

<!-- By default, a newly instantiated model instance will not contain any attribute values. If you would like to define the default values for some of your model's attributes, you may define an `$attributes` property on your model. Attribute values placed in the `$attributes` array should be in their raw, "storable" format as if they were just read from the database: -->
새로 생성한 모델 인스턴스는 기본적으로 어떤 속성(attribute) 값도 갖고 있지 않습니다. 어떤 속성에 대해 기본값을 지정하고 싶을 때는, 모델에 `$attributes` 속성을 배열로 선언해서 사용할 수 있습니다. `$attributes` 배열에 지정한 값은, 데이터베이스에서 막 읽어온 것처럼 "저장 가능한" 원시(raw) 형태여야 합니다.

```
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
Laravel은 Eloquent의 동작 방식과 "엄격성(strictness)"을 다양한 상황에 맞게 조정할 수 있는 여러 메서드를 제공합니다.

<!-- First, the `preventLazyLoading` method accepts an optional boolean argument that indicates if lazy loading should be prevented. For example, you may wish to only disable lazy loading in non-production environments so that your production environment will continue to function normally even if a lazy loaded relationship is accidentally present in production code. Typically, this method should be invoked in the `boot` method of your application's `AppServiceProvider`: -->
먼저, `preventLazyLoading` 메서드는 lazy loading(지연 로딩)을 방지할지 여부를 나타내는 불리언 값을 인수로 받습니다. 예를 들어, 프로덕션 환경에서는 lazy loading이 우연히 실행되어도 애플리케이션이 정상 동작할 수 있게 하기 위해, 비프로덕션 환경에서만 lazy loading을 막을 수 있습니다. 이 메서드는 보통 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 호출합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

<!-- Also, you may instruct Laravel to throw an exception when attempting to fill an unfillable attribute by invoking the `preventSilentlyDiscardingAttributes` method. This can help prevent unexpected errors during local development when attempting to set an attribute that has not been added to the model's `fillable` array: -->
또한, `preventSilentlyDiscardingAttributes` 메서드를 사용하면, 모델의 `fillable` 배열에 포함되지 않은 속성 값을 할당하려고 할 때 예외를 발생시킬 수 있습니다. 이를 통해 로컬 개발 중 실수로 fillable 속성에 추가되지 않은 속성을 지정했을 때, 예기치 않은 에러를 예방할 수 있습니다.

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<!-- Finally, you may instruct Eloquent to throw an exception if you attempt to access an attribute on a model when that attribute was not actually retrieved from the database or when the attribute does not exist. For example, this may occur when you forget to add an attribute to the `select` clause of an Eloquent query: -->
마지막으로, 데이터베이스에서 실제로 조회되지 않았거나 존재하지 않는 속성에 접근하려고 시도했을 때 Eloquent가 예외를 던지도록 지시할 수 있습니다. 예를 들어, Eloquent 쿼리의 `select` 절에 해당 속성을 빼먹고 추가하지 않은 경우 이런 일이 발생할 수 있습니다.

```php
Model::preventAccessingMissingAttributes(! $this->app->isProduction());
```

<a name="enabling-eloquent-strict-mode"></a>
<!-- #### Enabling Eloquent "Strict Mode" -->
#### Enabling Eloquent "Strict Mode"

<!-- For convenience, you may enable all three of the methods discussed above by simply invoking the `shouldBeStrict` method: -->
위에서 설명한 세 가지 메서드를 모두 한 번에 활성화하려면, `shouldBeStrict` 메서드를 호출하면 간편합니다.

```php
Model::shouldBeStrict(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
<!-- ## Retrieving Models -->
## Retrieving Models

<!-- Once you have created a model and [its associated database table](/docs/9.x/migrations#writing-migrations), you are ready to start retrieving data from your database. You can think of each Eloquent model as a powerful [query builder](/docs/9.x/queries) allowing you to fluently query the database table associated with the model. The model's `all` method will retrieve all of the records from the model's associated database table: -->
모델과 [its associated database table](/docs/9.x/migrations#writing-migrations)을 만들었다면, 이제 데이터베이스에서 데이터를 조회할 준비가 된 것입니다. 각 Eloquent 모델은 [query builder](/docs/9.x/queries)로서, 모델과 연결된 테이블에 대해 유연하게 쿼리를 작성할 수 있습니다. 모델의 `all` 메서드는 해당 테이블에 있는 모든 레코드를 조회합니다.

```
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
<!-- #### Building Queries -->
#### Building Queries

<!-- The Eloquent `all` method will return all of the results in the model's table. However, since each Eloquent model serves as a [query builder](/docs/9.x/queries), you may add additional constraints to queries and then invoke the `get` method to retrieve the results: -->
Eloquent의 `all` 메서드는 테이블의 모든 결과를 반환합니다. 하지만, 각각의 Eloquent 모델은 자체적으로 [query builder](/docs/9.x/queries)로 동작하기 때문에 쿼리에 제약 조건을 추가한 뒤, `get` 메서드를 호출하여 원하는 결과만 조회할 수 있습니다.

```
$flights = Flight::where('active', 1)
               ->orderBy('name')
               ->take(10)
               ->get();
```

> [!NOTE]
> Eloquent 모델은 쿼리 빌더 역할도 하므로, Laravel [query builder](/docs/9.x/queries)에서 제공하는 모든 메서드를 사용할 수 있습니다. Eloquent 쿼리 작성 시 이 메서드들을 활용해보세요.

<a name="refreshing-models"></a>
<!-- #### Refreshing Models -->
#### Refreshing Models

<!-- If you already have an instance of an Eloquent model that was retrieved from the database, you can "refresh" the model using the `fresh` and `refresh` methods. The `fresh` method will re-retrieve the model from the database. The existing model instance will not be affected: -->
이미 데이터베이스에서 조회한 Eloquent 모델 인스턴스가 있다면, `fresh`나 `refresh` 메서드를 사용해 모델을 "새로 고침"할 수 있습니다. `fresh` 메서드는 데이터베이스에서 해당 모델을 다시 조회하지만, 기존 인스턴스에는 영향을 미치지 않습니다.

```
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

<!-- The `refresh` method will re-hydrate the existing model using fresh data from the database. In addition, all of its loaded relationships will be refreshed as well: -->
`refresh` 메서드는 현재 모델 인스턴스를 데이터베이스의 최신 데이터로 다시 "하이드레이션"합니다. 또한, 모델과 함께 로드된 모든 연관관계도 최신화됩니다.

```
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
<!-- ### Collections -->
### Collections

<!-- As we have seen, Eloquent methods like `all` and `get` retrieve multiple records from the database. However, these methods don't return a plain PHP array. Instead, an instance of `Illuminate\Database\Eloquent\Collection` is returned. -->
앞서 살펴본 것처럼, Eloquent의 `all`이나 `get` 같은 메서드는 데이터베이스에서 여러 건의 레코드를 조회합니다. 이때 Eloquent는 단순한 PHP 배열을 반환하지 않고, `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환합니다.

<!-- The Eloquent `Collection` class extends Laravel's base `Illuminate\Support\Collection` class, which provides a [variety of helpful methods](/docs/9.x/collections#available-methods) for interacting with data collections. For example, the `reject` method may be used to remove models from a collection based on the results of an invoked closure: -->
Eloquent의 `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection`을 확장하며, 데이터 컬렉션을 쉽게 다룰 수 있는 [variety of helpful methods](/docs/9.x/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드는 클로저를 이용해 컬렉션에서 특정 모델을 제외시킬 수 있습니다.

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function ($flight) {
    return $flight->cancelled;
});
```

<!-- In addition to the methods provided by Laravel's base collection class, the Eloquent collection class provides [a few extra methods](/docs/9.x/eloquent-collections#available-methods) that are specifically intended for interacting with collections of Eloquent models. -->
기본 컬렉션 클래스에서 제공하는 메서드 외에도, Eloquent 컬렉션만의 [a few extra methods](/docs/9.x/eloquent-collections#available-methods)이 있어서, Eloquent 모델 컬렉션을 좀 더 유연하게 다룰 수 있습니다.

<!-- Since all of Laravel's collections implement PHP's iterable interfaces, you may loop over collections as if they were an array: -->
Laravel의 모든 컬렉션은 PHP의 iterable 인터페이스를 구현하고 있으므로, 배열처럼 반복문으로 순회할 수 있습니다.

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
<!-- ### Chunking Results -->
### Chunking Results

<!-- Your application may run out of memory if you attempt to load tens of thousands of Eloquent records via the `all` or `get` methods. Instead of using these methods, the `chunk` method may be used to process large numbers of models more efficiently. -->
`all`이나 `get` 같은 메서드로 수만 건의 Eloquent 레코드를 한 번에 로드하면 애플리케이션이 메모리 부족에 빠질 수 있습니다. 이런 경우 `chunk` 메서드를 사용하면, 대량의 모델을 좀 더 효율적으로 처리할 수 있습니다.

<!-- The `chunk` method will retrieve a subset of Eloquent models, passing them to a closure for processing. Since only the current chunk of Eloquent models is retrieved at a time, the `chunk` method will provide significantly reduced memory usage when working with a large number of models: -->
`chunk` 메서드는 Eloquent 모델의 일부분(subset)만 조회하여, 이를 클로저에 전달해 처리합니다. 한 번에 현재 청크의 Eloquent 모델만 조회하므로, `chunk` 메서드는 많은 수의 모델을 다룰 때 메모리 사용량을 크게 줄여줍니다.

```php
use App\Models\Flight;

Flight::chunk(200, function ($flights) {
    foreach ($flights as $flight) {
        //
    }
});
```

<!-- The first argument passed to the `chunk` method is the number of records you wish to receive per "chunk". The closure passed as the second argument will be invoked for each chunk that is retrieved from the database. A database query will be executed to retrieve each chunk of records passed to the closure. -->
`chunk` 메서드의 첫 번째 인자는 한 번에 조회할 레코드 수(청크 크기)입니다. 두 번째 인자로는 각 청크가 조회될 때마다 호출되는 클로저를 전달합니다. 데이터베이스 쿼리가 매번 실행되어 각 청크마다 결과를 가져옵니다.

<!-- If you are filtering the results of the `chunk` method based on a column that you will also be updating while iterating over the results, you should use the `chunkById` method. Using the `chunk` method in these scenarios could lead to unexpected and inconsistent results. Internally, the `chunkById` method will always retrieve models with an `id` column greater than the last model in the previous chunk: -->
반복 처리 중에 동시에 업데이트할 컬럼을 기준으로 `chunk` 메서드의 결과를 필터링하는 경우에는 `chunkById` 메서드를 사용해야 합니다. 이런 상황에서 `chunk` 메서드를 사용하면 예기치 못한 비일관적인 결과가 나올 수 있습니다. `chunkById` 메서드는 내부적으로 매 청크마다 이전 청크의 마지막 모델보다 큰 `id` 값을 가진 레코드만 조회하기 때문입니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function ($flights) {
        $flights->each->update(['departed' => false]);
    }, $column = 'id');
```

<a name="chunking-using-lazy-collections"></a>
<!-- ### Chunking Using Lazy Collections -->
### Chunking Using Lazy Collections

<!-- The `lazy` method works similarly to [the `chunk` method](#chunking-results) in the sense that, behind the scenes, it executes the query in chunks. However, instead of passing each chunk directly into a callback as is, the `lazy` method returns a flattened [`LazyCollection`](/docs/9.x/collections#lazy-collections) of Eloquent models, which lets you interact with the results as a single stream: -->
`lazy` 메서드는 [the `chunk` method](#chunking-results)와 유사하게, 내부적으로 쿼리를 청크 단위로 실행합니다. 하지만 각 청크 결과를 클로저로 전달하는 대신, `lazy`는 Eloquent 모델들의 평면화(flattened)된 [`LazyCollection`](/docs/9.x/collections#lazy-collections)을 반환합니다. 이를 통해 결과를 하나의 스트림처럼 처리할 수 있습니다.

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    //
}
```

<!-- If you are filtering the results of the `lazy` method based on a column that you will also be updating while iterating over the results, you should use the `lazyById` method. Internally, the `lazyById` method will always retrieve models with an `id` column greater than the last model in the previous chunk: -->
`lazy` 메서드를 사용할 때, 순회하면서 업데이트할 컬럼이 쿼리 필터 조건에 포함되어 있다면, `lazyById` 메서드를 사용하는 것이 안전합니다. `lazyById`는 매번 이전 청크의 마지막 모델보다 큰 `id` 값을 가진 레코드만 조회합니다.

```php
Flight::where('departed', true)
    ->lazyById(200, $column = 'id')
    ->each->update(['departed' => false]);
```

<!-- You may filter the results based on the descending order of the `id` using the `lazyByIdDesc` method. -->
내림차순으로 `id`를 기준 삼아 결과를 필터링하려면, `lazyByIdDesc` 메서드를 사용할 수 있습니다.

<a name="cursors"></a>

<!-- ### Cursors -->
### Cursors

<!-- Similar to the `lazy` method, the `cursor` method may be used to significantly reduce your application's memory consumption when iterating through tens of thousands of Eloquent model records. -->
`lazy` 메서드와 유사하게, `cursor` 메서드를 사용하면 수만 건이 넘는 Eloquent 모델 레코드를 반복(iterate)할 때 애플리케이션의 메모리 사용량을 획기적으로 줄일 수 있습니다.

<!-- The `cursor` method will only execute a single database query; however, the individual Eloquent models will not be hydrated until they are actually iterated over. Therefore, only one Eloquent model is kept in memory at any given time while iterating over the cursor. -->
`cursor` 메서드는 단 한 번의 데이터베이스 쿼리만을 실행하지만, 실제로 각 Eloquent 모델이 반복 처리될 때까지 메모리에 로드(하이드레이트)하지 않습니다. 따라서 반복이 진행되는 동안 한 시점에 한 개의 Eloquent 모델만 메모리에 유지됩니다.

> [!WARNING]
> `cursor` 메서드는 항상 한 번에 한 개의 Eloquent 모델만 메모리에 보관하기 때문에, 연관관계(eager loading)를 사용할 수 없습니다. 연관관계를 함께 로드해야 하는 경우 [the `lazy` method](#chunking-using-lazy-collections)를 대신 사용하는 것이 좋습니다.

<!-- Internally, the `cursor` method uses PHP [generators](https://www.php.net/manual/en/language.generators.overview.php) to implement this functionality: -->
내부적으로 `cursor` 메서드는 PHP의 [generators](https://www.php.net/manual/en/language.generators.overview.php)를 사용하여 이 기능을 제공합니다.

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    //
}
```

<!-- The `cursor` returns an `Illuminate\Support\LazyCollection` instance. [Lazy collections](/docs/9.x/collections#lazy-collections) allow you to use many of the collection methods available on typical Laravel collections while only loading a single model into memory at a time: -->
`cursor` 메서드는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [Lazy collections](/docs/9.x/collections#lazy-collections)은 Laravel 컬렉션에서 사용할 수 있는 다양한 메서드를 지원하면서도, 한 번에 오직 하나의 모델만 메모리에 로드합니다.

```php
use App\Models\User;

$users = User::cursor()->filter(function ($user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

<!-- Although the `cursor` method uses far less memory than a regular query (by only holding a single Eloquent model in memory at a time), it will still eventually run out of memory. This is [due to PHP's PDO driver internally caching all raw query results in its buffer](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php). If you're dealing with a very large number of Eloquent records, consider using [the `lazy` method](#chunking-using-lazy-collections) instead. -->
`cursor` 메서드는 일반 쿼리보다 훨씬 적은 메모리를 사용하지만(한 번에 하나의 모델만 메모리에 저장), 결국에는 메모리가 모두 사용될 수도 있습니다. 이는 [due to PHP's PDO driver internally caching all raw query results in its buffer](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)입니다. 매우 많은 수의 Eloquent 레코드를 다뤄야 한다면, [the `lazy` method](#chunking-using-lazy-collections)를 사용하는 것을 고려하세요.

<a name="advanced-subqueries"></a>
<!-- ### Advanced Subqueries -->
### Advanced Subqueries

<a name="subquery-selects"></a>
<!-- #### Subquery Selects -->
#### Subquery Selects

<!-- Eloquent also offers advanced subquery support, which allows you to pull information from related tables in a single query. For example, let's imagine that we have a table of flight `destinations` and a table of `flights` to destinations. The `flights` table contains an `arrived_at` column which indicates when the flight arrived at the destination. -->
Eloquent는 고급 서브쿼리 기능을 제공하여, 연관된 테이블에서 정보를 한 번의 쿼리로 가져올 수 있도록 지원합니다. 예를 들어, flight `destinations`(목적지) 테이블과 목적지로 가는 `flights`(비행편) 테이블이 있다고 가정해봅니다. `flights` 테이블에는 해당 비행기가 목적지에 도착한 시각을 나타내는 `arrived_at` 컬럼이 있습니다.

<!-- Using the subquery functionality available to the query builder's `select` and `addSelect` methods, we can select all of the `destinations` and the name of the flight that most recently arrived at that destination using a single query: -->
쿼리 빌더의 `select` 및 `addSelect` 메서드에서 제공하는 서브쿼리 기능을 활용하면, 모든 `destinations`와 각 목적지에 가장 최근에 도착한 비행편의 이름을 한 번의 쿼리로 조회할 수 있습니다.

```
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
또한 쿼리 빌더의 `orderBy` 기능에서도 서브쿼리를 사용할 수 있습니다. 앞서 예시로 든 flight 테이블을 기준으로, 각 목적지에 가장 최근에 도착한 비행편의 도착 시각을 기준으로 목적지 목록을 정렬할 수 있습니다. 이 역시 한 번의 쿼리로 처리됩니다.

```
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
주어진 쿼리 조건에 해당하는 모든 레코드를 조회하는 것 외에도, `find`, `first`, `firstWhere` 메서드를 이용해 단일 레코드만 조회할 수 있습니다. 이 메서드들은 모델 컬렉션 대신 단일 모델 인스턴스를 반환합니다.

```
use App\Models\Flight;

// Retrieve a model by its primary key...
$flight = Flight::find(1);

// Retrieve the first model matching the query constraints...
$flight = Flight::where('active', 1)->first();

// Alternative to retrieving the first model matching the query constraints...
$flight = Flight::firstWhere('active', 1);
```

<!-- Sometimes you may wish to perform some other action if no results are found. The `findOr` and `firstOr` methods will return a single model instance or, if no results are found, execute the given closure. The value returned by the closure will be considered the result of the method: -->
때때로 결과가 존재하지 않을 때 다른 동작을 하고 싶을 수도 있습니다. `findOr`와 `firstOr` 메서드는 조건에 맞는 모델 인스턴스를 반환하거나, 결과가 없을 경우 주어진 클로저를 실행합니다. 클로저가 반환한 값이 메서드의 반환 값으로 사용됩니다.

```
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
모델을 찾지 못했을 때 예외를 발생시키고 싶은 상황이 있을 수 있습니다. 라우트나 컨트롤러에서 특히 유용합니다. `findOrFail`과 `firstOrFail` 메서드는 쿼리 조건에 맞는 첫 결과를 반환하거나, 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다.

```
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

<!-- If the `ModelNotFoundException` is not caught, a 404 HTTP response is automatically sent back to the client: -->
`ModelNotFoundException` 예외를 따로 처리하지 않으면, Laravel이 자동으로 404 HTTP 응답을 클라이언트로 반환합니다.

```
use App\Models\Flight;

Route::get('/api/flights/{id}', function ($id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
<!-- ### Retrieving Or Creating Models -->
### Retrieving Or Creating Models

<!-- The `firstOrCreate` method will attempt to locate a database record using the given column / value pairs. If the model can not be found in the database, a record will be inserted with the attributes resulting from merging the first array argument with the optional second array argument: -->
`firstOrCreate` 메서드는 주어진 컬럼/값 쌍(column/value pairs)으로 데이터베이스 레코드를 찾으려 시도합니다. 만약 해당 모델이 데이터베이스에 없다면, 첫 번째 배열 인자와 (선택적으로) 두 번째 배열 인자를 합쳐서 새로운 레코드가 삽입됩니다.

<!-- The `firstOrNew` method, like `firstOrCreate`, will attempt to locate a record in the database matching the given attributes. However, if a model is not found, a new model instance will be returned. Note that the model returned by `firstOrNew` has not yet been persisted to the database. You will need to manually call the `save` method to persist it: -->
`firstOrNew` 메서드도 `firstOrCreate`와 비슷하게 주어진 속성에 일치하는 레코드를 데이터베이스에서 조회합니다. 다만 모델을 찾지 못하면 새 모델 인스턴스를 반환합니다. 이때 `firstOrNew`가 반환한 모델은 아직 데이터베이스에 저장되지 않은 상태라는 점에 유의하세요. 저장하려면 직접 `save` 메서드를 호출해야 합니다.

```
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

<!-- When interacting with Eloquent models, you may also use the `count`, `sum`, `max`, and other [aggregate methods](/docs/9.x/queries#aggregates) provided by the Laravel [query builder](/docs/9.x/queries). As you might expect, these methods return a scalar value instead of an Eloquent model instance: -->
Eloquent 모델을 사용할 때도, Laravel [aggregate methods](/docs/9.x/queries)에서 제공하는 `count`, `sum`, `max` 등 [query builder](/docs/9.x/queries#aggregates)를 사용할 수 있습니다. 이 메서드들은 Eloquent 모델 인스턴스가 아닌 스칼라 값을 반환합니다.

```
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
<!-- ## Inserting & Updating Models -->
## Inserting & Updating Models

<a name="inserts"></a>
<!-- ### Inserts -->
### Inserts

<!-- Of course, when using Eloquent, we don't only need to retrieve models from the database. We also need to insert new records. Thankfully, Eloquent makes it simple. To insert a new record into the database, you should instantiate a new model instance and set attributes on the model. Then, call the `save` method on the model instance: -->
Eloquent를 사용할 때는 데이터베이스에서 모델을 조회하는 것 외에도 새로운 레코드를 추가할 수 있습니다. 다행히도 Eloquent에서는 이 과정이 매우 간단합니다. 새 레코드를 데이터베이스에 삽입하려면 모델 인스턴스를 생성해 속성 값을 지정하고, 해당 인스턴스에서 `save` 메서드를 호출하면 됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Flight;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Store a new flight in the database.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        // Validate the request...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();
    }
}
```

<!-- In this example, we assign the `name` field from the incoming HTTP request to the `name` attribute of the `App\Models\Flight` model instance. When we call the `save` method, a record will be inserted into the database. The model's `created_at` and `updated_at` timestamps will automatically be set when the `save` method is called, so there is no need to set them manually. -->
위 예시에서는 HTTP 요청에서 넘어온 `name` 값을 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당합니다. `save` 메서드를 호출하면 레코드가 데이터베이스에 삽입됩니다. 모델의 `created_at` 및 `updated_at` 타임스탬프는 `save` 메서드가 호출될 때 자동으로 설정되므로, 별도로 지정할 필요가 없습니다.

<!-- Alternatively, you may use the `create` method to "save" a new model using a single PHP statement. The inserted model instance will be returned to you by the `create` method: -->
또한, `create` 메서드를 이용하면 한 줄의 PHP 코드로 새 모델을 "저장"할 수 있습니다. 삽입된 모델 인스턴스는 `create` 메서드가 반환합니다.

```
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

<!-- However, before using the `create` method, you will need to specify either a `fillable` or `guarded` property on your model class. These properties are required because all Eloquent models are protected against mass assignment vulnerabilities by default. To learn more about mass assignment, please consult the [mass assignment documentation](#mass-assignment). -->
단, `create` 메서드를 사용하려면 모델 클래스에 `fillable` 또는 `guarded` 속성(property)이 반드시 지정되어 있어야 합니다. 이는 모든 Eloquent 모델이 기본적으로 대량 할당 취약점(mass assignment vulnerability)으로부터 보호되기 때문입니다. 대량 할당에 대한 자세한 내용은 [mass assignment documentation](#mass-assignment)를 참고하세요.

<a name="updates"></a>
<!-- ### Updates -->
### Updates

<!-- The `save` method may also be used to update models that already exist in the database. To update a model, you should retrieve it and set any attributes you wish to update. Then, you should call the model's `save` method. Again, the `updated_at` timestamp will automatically be updated, so there is no need to manually set its value: -->
이미 데이터베이스에 존재하는 모델을 수정할 때도 `save` 메서드를 사용할 수 있습니다. 먼저 수정할 모델을 조회한 뒤, 변경할 속성 값을 지정하고, 모델의 `save` 메서드를 호출하면 됩니다. 이때도 `updated_at` 타임스탬프가 자동으로 갱신되므로, 따로 지정할 필요가 없습니다.

```
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

<a name="mass-updates"></a>
<!-- #### Mass Updates -->
#### Mass Updates

<!-- Updates can also be performed against models that match a given query. In this example, all flights that are `active` and have a `destination` of `San Diego` will be marked as delayed: -->
주어진 쿼리와 일치하는 여러 모델을 한꺼번에 업데이트할 수도 있습니다. 아래 예시에서는, `active` 상태이면서 `destination`이 `San Diego`인 모든 flight를 지연(delayed)된 것으로 표시합니다.

```
Flight::where('active', 1)
      ->where('destination', 'San Diego')
      ->update(['delayed' => 1]);
```

<!-- The `update` method expects an array of column and value pairs representing the columns that should be updated. The `update` method returns the number of affected rows. -->
`update` 메서드는 업데이트될 컬럼과 값을 나타내는 배열을 인자로 받습니다. `update` 메서드는 영향을 받은(수정된) 행의 개수를 반환합니다.

> [!WARNING]
> Eloquent에서 대량 업데이트를 실행하면, 해당 모델에 대한 `saving`, `saved`, `updating`, `updated` 모델 이벤트가 발생하지 않습니다. 이는 대량 업데이트 시 모델이 실제로 조회되지 않기 때문입니다.

<a name="examining-attribute-changes"></a>
<!-- #### Examining Attribute Changes -->
#### Examining Attribute Changes

<!-- Eloquent provides the `isDirty`, `isClean`, and `wasChanged` methods to examine the internal state of your model and determine how its attributes have changed from when the model was originally retrieved. -->
Eloquent에서는 모델의 내부 상태를 파악하고, 속성이 조회 당시와 비교해 어떻게 변경되었는지 확인할 수 있도록 `isDirty`, `isClean`, `wasChanged` 등의 메서드를 제공합니다.

<!-- The `isDirty` method determines if any of the model's attributes have been changed since the model was retrieved. You may pass a specific attribute name or an array of attributes to the `isDirty` method to determine if any of the attributes are "dirty". The `isClean` method will determine if an attribute has remained unchanged since the model was retrieved. This method also accepts an optional attribute argument: -->
`isDirty` 메서드는 모델 조회 이후 모델의 속성 중 하나라도 변경되었는지를 판단합니다. 특정 속성(또는 속성 배열)을 `isDirty` 메서드에 인자로 넘겨, 해당 속성이 변경(더티) 상태인지 판별할 수도 있습니다. `isClean` 메서드는 지정한 속성이 조회된 이후 변경되지 않았는지 확인합니다. 이 메서드 역시 옵션으로 속성명을 지정할 수 있습니다.

```
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
`wasChanged` 메서드는 모델 인스턴스가 마지막으로 저장(save)됐을 때 속성이 변경되었는지를 확인합니다. 필요하다면 구체적인 속성명을 전달해 특정 속성이 변경되었는지 확인할 수도 있습니다.

```
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
`getOriginal` 메서드는, 모델 인스턴스를 조회한 이후 현재까지의 변경 사항과 상관없이, 모델의 원래 속성값을 배열로 반환합니다. 특정 속성값만 필요하다면, 속성명을 인자로 넘길 수 있습니다.

```
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = "Jack";
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // Array of original attributes...
```

<a name="mass-assignment"></a>
<!-- ### Mass Assignment -->
### Mass Assignment

<!-- You may use the `create` method to "save" a new model using a single PHP statement. The inserted model instance will be returned to you by the method: -->
`create` 메서드를 활용하면 한 줄의 PHP 코드로 새 모델을 "저장"할 수 있습니다. 이때 생성된 모델 인스턴스가 반환됩니다.

```
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

<!-- However, before using the `create` method, you will need to specify either a `fillable` or `guarded` property on your model class. These properties are required because all Eloquent models are protected against mass assignment vulnerabilities by default. -->
하지만 `create` 메서드를 사용하기 전, 반드시 모델 클래스에 `fillable` 또는 `guarded` 속성이 지정되어 있어야 합니다. 이는 모든 Eloquent 모델이 기본적으로 대량 할당 취약점(mass assignment vulnerability)에 대비해 보호되기 때문입니다.

<!-- A mass assignment vulnerability occurs when a user passes an unexpected HTTP request field and that field changes a column in your database that you did not expect. For example, a malicious user might send an `is_admin` parameter through an HTTP request, which is then passed to your model's `create` method, allowing the user to escalate themselves to an administrator. -->
대량 할당 취약점(mass assignment vulnerability)은 사용자가 예상치 못한 HTTP 요청 필드를 전달했고, 그 필드가 데이터베이스의 원하는 컬럼을 변경하는 경우 발생합니다. 예를 들어, 악의적인 사용자가 HTTP 요청을 통해 `is_admin` 파라미터를 전달하면, 해당 값이 모델의 `create` 메서드에 전달되어 사용자가 스스로 관리자로 권한을 올릴 수도 있습니다.

<!-- So, to get started, you should define which model attributes you want to make mass assignable. You may do this using the `$fillable` property on the model. For example, let's make the `name` attribute of our `Flight` model mass assignable: -->
따라서 우선, 어떤 모델 속성을 대량 할당이 가능하도록 허용할지 지정해야 합니다. 모델의 `$fillable` 속성에 허용할 속성을 배열로 정의하면 됩니다. 예시로, `Flight` 모델의 `name` 속성을 대량 할당 가능하도록 만들겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = ['name'];
}
```

<!-- Once you have specified which attributes are mass assignable, you may use the `create` method to insert a new record in the database. The `create` method returns the newly created model instance: -->
대량 할당 허용 속성을 지정한 뒤에는, `create` 메서드를 사용해 데이터베이스에 새 레코드를 삽입할 수 있습니다. `create` 메서드는 새로 생성된 모델 인스턴스를 반환합니다.

```
$flight = Flight::create(['name' => 'London to Paris']);
```

<!-- If you already have a model instance, you may use the `fill` method to populate it with an array of attributes: -->
이미 모델 인스턴스가 존재한다면, `fill` 메서드로 한꺼번에 속성을 할당할 수 있습니다.

```
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
<!-- #### Mass Assignment & JSON Columns -->
#### Mass Assignment & JSON Columns

<!-- When assigning JSON columns, each column's mass assignable key must be specified in your model's `$fillable` array. For security, Laravel does not support updating nested JSON attributes when using the `guarded` property: -->
JSON 컬럼에 값을 할당할 때는, 각 컬럼의 대량 할당 키를 반드시 모델의 `$fillable` 배열에 명시해야 합니다. 보안상의 이유로, Laravel은 `guarded` 속성을 사용할 때 중첩된(nested) JSON 속성값의 업데이트를 지원하지 않습니다.

```
/**
 * The attributes that are mass assignable.
 *
 * @var array
 */
protected $fillable = [
    'options->enabled',
];
```

<a name="allowing-mass-assignment"></a>
<!-- #### Allowing Mass Assignment -->
#### Allowing Mass Assignment

<!-- If you would like to make all of your attributes mass assignable, you may define your model's `$guarded` property as an empty array. If you choose to unguard your model, you should take special care to always hand-craft the arrays passed to Eloquent's `fill`, `create`, and `update` methods: -->
모델의 모든 속성을 대량 할당 가능하게 만들고 싶다면, 모델의 `$guarded` 속성을 빈 배열로 지정하면 됩니다. 모델을 보호 해제(unguard)할 경우, Eloquent의 `fill`, `create`, `update` 메서드에 전달하는 배열을 항상 신중하게 직접 작성해야 합니다.

```
/**
 * The attributes that aren't mass assignable.
 *
 * @var array
 */
protected $guarded = [];
```

<a name="mass-assignment-exceptions"></a>
<!-- #### Mass Assignment Exceptions -->
#### Mass Assignment Exceptions

<!-- By default, attributes that are not included in the `$fillable` array are silently discarded when performing mass-assignment operations. In production, this is expected behavior; however, during local development it can lead to confusion as to why model changes are not taking effect. -->
기본적으로, `$fillable` 배열에 포함되지 않은 속성은 대량 할당 시 조용히 무시됩니다. 실제 운영 환경에서는 이것이 기대되는 동작이지만, 개발 환경에서는 종종 모델 변화가 반영되지 않는 이유를 모르고 혼란스럽게 느낄 수 있습니다.

<!-- If you wish, you may instruct Laravel to throw an exception when attempting to fill an unfillable attribute by invoking the `preventSilentlyDiscardingAttributes` method. Typically, this method should be invoked within the `boot` method of one of your application's service providers: -->
필요하다면, `preventSilentlyDiscardingAttributes` 메서드를 호출해, 허용되지 않은 속성이 할당될 때 예외를 발생시키도록 Laravel에 지시할 수 있습니다. 보통 이 메서드는 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 호출하면 됩니다.

```
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```

<a name="upserts"></a>
<!-- ### Upserts -->
### Upserts

<!-- Occasionally, you may need to update an existing model or create a new model if no matching model exists. Like the `firstOrCreate` method, the `updateOrCreate` method persists the model, so there's no need to manually call the `save` method. -->
기존 모델을 업데이트해야 할 수도 있고, 일치하는 모델이 없으면 새로 생성해야 할 수도 있습니다. `firstOrCreate`와 유사하게, `updateOrCreate` 메서드는 모델을 데이터베이스에 저장(persist)하기 때문에 수동으로 `save`를 호출할 필요가 없습니다.

<!-- In the example below, if a flight exists with a `departure` location of `Oakland` and a `destination` location of `San Diego`, its `price` and `discounted` columns will be updated. If no such flight exists, a new flight will be created which has the attributes resulting from merging the first argument array with the second argument array: -->
아래 예시처럼, `departure`가 `Oakland`, `destination`이 `San Diego`인 flight가 이미 있으면 `price`와 `discounted` 컬럼만 업데이트하고, 해당 조건이 없으면 두 인자 배열을 병합해 새 flight가 생성됩니다.

```
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<!-- If you would like to perform multiple "upserts" in a single query, then you should use the `upsert` method instead. The method's first argument consists of the values to insert or update, while the second argument lists the column(s) that uniquely identify records within the associated table. The method's third and final argument is an array of the columns that should be updated if a matching record already exists in the database. The `upsert` method will automatically set the `created_at` and `updated_at` timestamps if timestamps are enabled on the model: -->
여러 개의 "업서트"를 단일 쿼리로 처리하려면 `upsert` 메서드를 사용할 수 있습니다. 첫 번째 인자는 삽입 또는 업데이트할 값 배열, 두 번째 인자는 테이블 내 레코드를 고유하게 식별하는 컬럼(들) 목록, 세 번째는 이미 존재하는 레코드일 경우 업데이트할 컬럼 목록입니다. `upsert` 메서드는 모델에 타임스탬프가 활성화된 경우, `created_at` 및 `updated_at` 필드를 자동으로 지정합니다.

```
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], ['departure', 'destination'], ['price']);
```
> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스에서는 `upsert` 메서드의 두 번째 인자 컬럼이 반드시 "primary" 또는 "unique" 인덱스를 가져야 합니다. 또한, MariaDB 및 MySQL 드라이버는 `upsert` 메서드의 두 번째 인자를 무시하고, 해당 테이블의 "primary" 및 "unique" 인덱스를 자동으로 사용해 기존 레코드 판별에 활용합니다.

<a name="deleting-models"></a>
<!-- ## Deleting Models -->
## Deleting Models

<!-- To delete a model, you may call the `delete` method on the model instance: -->
모델을 삭제하려면, 해당 모델 인스턴스에서 `delete` 메서드를 호출하면 됩니다.

```
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<!-- You may call the `truncate` method to delete all of the model's associated database records. The `truncate` operation will also reset any auto-incrementing IDs on the model's associated table: -->
모델과 연관된 모든 데이터베이스 레코드를 삭제하려면 `truncate` 메서드를 사용할 수 있습니다. `truncate` 작업은 모델의 테이블에서 자동 증가 식별자(auto-incrementing id) 역시 초기화(reset)합니다.

```
Flight::truncate();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
<!-- #### Deleting An Existing Model By Its Primary Key -->
#### Deleting An Existing Model By Its Primary Key

<!-- In the example above, we are retrieving the model from the database before calling the `delete` method. However, if you know the primary key of the model, you may delete the model without explicitly retrieving it by calling the `destroy` method.  In addition to accepting the single primary key, the `destroy` method will accept multiple primary keys, an array of primary keys, or a [collection](/docs/9.x/collections) of primary keys: -->
위 예시에서는 `delete` 메서드를 호출하기 전에 데이터베이스에서 모델을 먼저 조회했지만, 모델의 프라이머리 키(primary key)를 알고 있다면, 모델을 명시적으로 조회하지 않고 `destroy` 메서드를 호출해 바로 삭제할 수 있습니다. `destroy` 메서드는 단일 프라이머리 키뿐 아니라, 여러 개의 프라이머리 키, 프라이머리 키의 배열, 또는 [collection](/docs/9.x/collections)도 인자로 받을 수 있습니다.

```
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 로드(load)한 뒤 `delete` 메서드를 호출하므로, 해당 모델의 `deleting` 및 `deleted` 이벤트가 제대로 발생(dispatch)합니다.

<a name="deleting-models-using-queries"></a>
<!-- #### Deleting Models Using Queries -->
#### Deleting Models Using Queries

<!-- Of course, you may build an Eloquent query to delete all models matching your query's criteria. In this example, we will delete all flights that are marked as inactive. Like mass updates, mass deletes will not dispatch model events for the models that are deleted: -->
물론, Eloquent 쿼리를 작성해 쿼리 조건에 일치하는 모델을 한꺼번에 삭제할 수도 있습니다. 아래 예시에서는, 비활성(inactive)으로 표시된 모든 flight를 삭제합니다. 대량 업데이트와 마찬가지로, 대량 삭제 역시 모델 이벤트가 발생하지 않습니다.

```
$deleted = Flight::where('active', 0)->delete();
```

> [!WARNING]
> Eloquent에서 대량 삭제(mass delete) 명령을 실행하면, 삭제된 모델에 대해 `deleting`, `deleted` 이벤트가 발생하지 않습니다. 이는 삭제 명령이 실행될 때 모델을 실제로 조회하지 않기 때문입니다.

<a name="soft-deleting"></a>
<!-- ### Soft Deleting -->
### Soft Deleting

<!-- In addition to actually removing records from your database, Eloquent can also "soft delete" models. When models are soft deleted, they are not actually removed from your database. Instead, a `deleted_at` attribute is set on the model indicating the date and time at which the model was "deleted". To enable soft deletes for a model, add the `Illuminate\Database\Eloquent\SoftDeletes` trait to the model: -->
데이터베이스에서 레코드를 실제로 삭제하지 않고, Eloquent를 통해 "소프트 삭제"를 할 수도 있습니다. 소프트 삭제된 모델은 데이터베이스에서 실제로 삭제되지 않으며, 대신 모델에 `deleted_at` 속성(attribute)이 설정되어 "삭제된" 시점을 나타냅니다. 소프트 삭제를 사용하려면, 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레잇을 추가하면 됩니다.

```
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
> `SoftDeletes` 트레잇은 `deleted_at` 속성을 자동으로 `DateTime` 또는 `Carbon` 인스턴스로 변환(cast)해줍니다.

<!-- You should also add the `deleted_at` column to your database table. The Laravel [schema builder](/docs/9.x/migrations) contains a helper method to create this column: -->
데이터베이스 테이블에도 `deleted_at` 컬럼을 추가해야 합니다. Laravel [schema builder](/docs/9.x/migrations)를 사용하면 이 컬럼을 쉽게 추가할 수 있습니다.

```
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
이제 모델에서 `delete` 메서드를 호출하면 `deleted_at` 컬럼이 현재 시각으로 지정되고, 실제로는 테이블에서 레코드가 남아 있습니다. 소프트 삭제 기능이 적용된 모델을 조회할 때는 자동으로 소프트 삭제된 레코드가 질의 결과에서 제외됩니다.

<!-- To determine if a given model instance has been soft deleted, you may use the `trashed` method: -->
모델 인스턴스가 소프트 삭제된 상태인지 확인하려면, `trashed` 메서드를 사용할 수 있습니다.

```
if ($flight->trashed()) {
    //
}
```

<a name="restoring-soft-deleted-models"></a>
<!-- #### Restoring Soft Deleted Models -->
#### Restoring Soft Deleted Models

<!-- Sometimes you may wish to "un-delete" a soft deleted model. To restore a soft deleted model, you may call the `restore` method on a model instance. The `restore` method will set the model's `deleted_at` column to `null`: -->
때때로 소프트 삭제된 모델을 "삭제 취소"(복원)하고 싶을 때가 있습니다. 이럴 때는 모델 인스턴스에서 `restore` 메서드를 호출하면 됩니다. `restore` 메서드는 모델의 `deleted_at` 컬럼 값을 `null`로 재설정합니다.

```
$flight->restore();
```

<!-- You may also use the `restore` method in a query to restore multiple models. Again, like other "mass" operations, this will not dispatch any model events for the models that are restored: -->
쿼리 빌더에서 `restore` 메서드를 이용해 여러 모델을 한꺼번에 복원할 수도 있습니다. 마찬가지로, 대량 복원 역시 해당 모델들의 이벤트는 발생하지 않습니다.

```
Flight::withTrashed()
        ->where('airline_id', 1)
        ->restore();
```

<!-- The `restore` method may also be used when building [relationship](/docs/9.x/eloquent-relationships) queries: -->
[relationship](/docs/9.x/eloquent-relationships) 쿼리를 작성할 때도 `restore` 메서드를 사용할 수 있습니다.

```
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>

<!-- #### Permanently Deleting Models -->
#### Permanently Deleting Models

<!-- Sometimes you may need to truly remove a model from your database. You may use the `forceDelete` method to permanently remove a soft deleted model from the database table: -->
때때로, 모델을 데이터베이스에서 완전히 제거해야 할 때가 있습니다. 소프트 삭제된 모델을 데이터베이스 테이블에서 영구적으로 삭제하려면 `forceDelete` 메서드를 사용할 수 있습니다.

```
$flight->forceDelete();
```

<!-- You may also use the `forceDelete` method when building Eloquent relationship queries: -->
또한, Eloquent의 연관관계 쿼리를 작성할 때도 `forceDelete` 메서드를 사용할 수 있습니다.

```
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
<!-- ### Querying Soft Deleted Models -->
### Querying Soft Deleted Models

<a name="including-soft-deleted-models"></a>
<!-- #### Including Soft Deleted Models -->
#### Including Soft Deleted Models

<!-- As noted above, soft deleted models will automatically be excluded from query results. However, you may force soft deleted models to be included in a query's results by calling the `withTrashed` method on the query: -->
앞서 설명했듯이, 소프트 삭제된 모델은 기본적으로 쿼리 결과에서 자동으로 제외됩니다. 그러나, 쿼리에서 소프트 삭제된 모델도 결과에 포함하려면 `withTrashed` 메서드를 쿼리에 호출하면 됩니다.

```
use App\Models\Flight;

$flights = Flight::withTrashed()
                ->where('account_id', 1)
                ->get();
```

<!-- The `withTrashed` method may also be called when building a [relationship](/docs/9.x/eloquent-relationships) query: -->
`withTrashed` 메서드는 [relationship](/docs/9.x/eloquent-relationships) 쿼리를 작성할 때도 사용할 수 있습니다.

```
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
<!-- #### Retrieving Only Soft Deleted Models -->
#### Retrieving Only Soft Deleted Models

<!-- The `onlyTrashed` method will retrieve **only** soft deleted models: -->
`onlyTrashed` 메서드는 소프트 삭제된 모델 **만을** 조회합니다.

```
$flights = Flight::onlyTrashed()
                ->where('airline_id', 1)
                ->get();
```

<a name="pruning-models"></a>
<!-- ## Pruning Models -->
## Pruning Models

<!-- Sometimes you may want to periodically delete models that are no longer needed. To accomplish this, you may add the `Illuminate\Database\Eloquent\Prunable` or `Illuminate\Database\Eloquent\MassPrunable` trait to the models you would like to periodically prune. After adding one of the traits to the model, implement a `prunable` method which returns an Eloquent query builder that resolves the models that are no longer needed: -->
더 이상 필요하지 않은 모델을 주기적으로 삭제하고 싶은 경우가 있습니다. 이를 위해 삭제가 필요한 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레잇을 추가할 수 있습니다. 트레잇을 모델에 추가한 다음, 필요 없는 모델을 조회하는 Eloquent 쿼리 빌더를 반환하는 `prunable` 메서드를 구현해 주세요.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * Get the prunable model query.
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function prunable()
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<!-- When marking models as `Prunable`, you may also define a `pruning` method on the model. This method will be called before the model is deleted. This method can be useful for deleting any additional resources associated with the model, such as stored files, before the model is permanently removed from the database: -->
`Prunable`로 지정한 모델에는 `pruning` 메서드를 추가로 정의할 수도 있습니다. 이 메서드는 모델이 삭제되기 **전**에 호출되며, 저장된 파일 등 모델과 연관된 추가 리소스를 데이터베이스에서 영구 삭제되기 전에 정리하는 데 유용합니다.

```
/**
 * Prepare the model for pruning.
 *
 * @return void
 */
protected function pruning()
{
    //
}
```

<!-- After configuring your prunable model, you should schedule the `model:prune` Artisan command in your application's `App\Console\Kernel` class. You are free to choose the appropriate interval at which this command should be run: -->
가지치기가 필요한 모델을 설정한 뒤에는, 애플리케이션의 `App\Console\Kernel` 클래스에서 `model:prune` Artisan 명령어가 일정 주기로 실행되도록 스케줄링해야 합니다. 이 스케줄 주기는 자유롭게 선택할 수 있습니다.

```
/**
 * Define the application's command schedule.
 *
 * @param  \Illuminate\Console\Scheduling\Schedule  $schedule
 * @return void
 */
protected function schedule(Schedule $schedule)
{
    $schedule->command('model:prune')->daily();
}
```

<!-- Behind the scenes, the `model:prune` command will automatically detect "Prunable" models within your application's `app/Models` directory. If your models are in a different location, you may use the `--model` option to specify the model class names: -->
내부적으로 `model:prune` 명령어는 애플리케이션의 `app/Models` 디렉토리 내에서 "Prunable" 모델을 자동으로 감지합니다. 만약 모델이 다른 위치에 있다면, `--model` 옵션을 사용하여 모델 클래스명을 직접 지정할 수 있습니다.

```
$schedule->command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

<!-- If you wish to exclude certain models from being pruned while pruning all other detected models, you may use the `--except` option: -->
반대로, 감지된 모든 모델을 가지치기(Prune)하면서 특정 모델만 제외하고 싶다면, `--except` 옵션을 사용할 수 있습니다.

```
$schedule->command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

<!-- You may test your `prunable` query by executing the `model:prune` command with the `--pretend` option. When pretending, the `model:prune` command will simply report how many records would be pruned if the command were to actually run: -->
`prunable` 쿼리가 제대로 동작하는지 테스트하려면, `--pretend` 옵션과 함께 `model:prune` 명령어를 실행하면 됩니다. pretend로 실행하면 `model:prune` 명령어는 실제로 명령어가 실행될 경우 얼마만큼의 레코드가 가지치기될지 보고만 해줍니다.

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 소프트 삭제된 모델이라도 prunable 쿼리에 일치할 경우, `forceDelete`로 **영구 삭제**됩니다.

<a name="mass-pruning"></a>
<!-- #### Mass Pruning -->
#### Mass Pruning

<!-- When models are marked with the `Illuminate\Database\Eloquent\MassPrunable` trait, models are deleted from the database using mass-deletion queries. Therefore, the `pruning` method will not be invoked, nor will the `deleting` and `deleted` model events be dispatched. This is because the models are never actually retrieved before deletion, thus making the pruning process much more efficient: -->
모델에 `Illuminate\Database\Eloquent\MassPrunable` 트레잇이 적용되어 있으면, 대량 삭제 쿼리를 통해 모델을 데이터베이스에서 삭제합니다. 이 경우 `pruning` 메서드는 호출되지 않고, `deleting` 및 `deleted`와 같은 모델 이벤트도 발생하지 않습니다. 이는 실제로 삭제 전에 모델이 조회되지 않기 때문에 가지치기 과정이 훨씬 더 효율적으로 동작합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * Get the prunable model query.
     *
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function prunable()
    {
        return static::where('created_at', '<=', now()->subMonth());
    }
}
```

<a name="replicating-models"></a>
<!-- ## Replicating Models -->
## Replicating Models

<!-- You may create an unsaved copy of an existing model instance using the `replicate` method. This method is particularly useful when you have model instances that share many of the same attributes: -->
이미 존재하는 모델 인스턴스의 저장되지 않은 복사본을 생성하려면 `replicate` 메서드를 사용할 수 있습니다. 이 메서드는 여러 속성(attribute)이 동일한 모델 인스턴스를 관리할 때 특히 유용합니다.

```
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
복제 시 새로운 모델에 복사하지 않을 속성(attribute)이 있다면, 배열에 속성명을 담아 `replicate` 메서드의 인수로 전달하면 됩니다.

```
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
전역 스코프를 사용하면 특정 모델에 대해 모든 쿼리에 제약 조건을 추가할 수 있습니다. Laravel의 [soft delete](#soft-deleting) 기능도 전역 스코프를 이용해 "삭제되지 않은" 모델만 데이터베이스에서 조회합니다. 직접 전역 스코프를 작성하면, 특정 모델의 모든 쿼리가 반드시 특정 제약 조건을 받도록 손쉽게 만들 수 있습니다.

<a name="writing-global-scopes"></a>
<!-- #### Writing Global Scopes -->
#### Writing Global Scopes

<!-- Writing a global scope is simple. First, define a class that implements the `Illuminate\Database\Eloquent\Scope` interface. Laravel does not have a conventional location where you should place scope classes, so you are free to place this class in any directory that you wish. -->
전역 스코프 작성은 간단합니다. 먼저, `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스를 정의하세요. Laravel에서는 스코프 클래스를 넣어야 할 위치가 정해져 있지 않으므로, 원하는 디렉터리에 클래스를 자유롭게 생성할 수 있습니다.

<!-- The `Scope` interface requires you to implement one method: `apply`. The `apply` method may add `where` constraints or other types of clauses to the query as needed: -->
`Scope` 인터페이스는 반드시 하나의 메서드: `apply`를 구현해야 합니다. `apply` 메서드에서는 쿼리에 필요한 `where` 조건이나 기타 절을 추가할 수 있습니다.

```
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Apply the scope to a given Eloquent query builder.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $builder
     * @param  \Illuminate\Database\Eloquent\Model  $model
     * @return void
     */
    public function apply(Builder $builder, Model $model)
    {
        $builder->where('created_at', '<', now()->subYears(2000));
    }
}
```

> [!NOTE]
> 전역 스코프에서 쿼리의 select 절에 컬럼을 추가하려면, 기존의 `select` 대신 `addSelect` 메서드를 사용하는 것이 좋습니다. 이렇게 하면 쿼리의 기존 select 절이 의도치 않게 덮어써지는 것을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
<!-- #### Applying Global Scopes -->
#### Applying Global Scopes

<!-- To assign a global scope to a model, you should override the model's `booted` method and invoke the model's `addGlobalScope` method. The `addGlobalScope` method accepts an instance of your scope as its only argument: -->
모델에 전역 스코프를 할당하려면, 모델의 `booted` 메서드를 오버라이드하여 내부에서 `addGlobalScope` 메서드를 호출해야 합니다. `addGlobalScope` 메서드에는 앞서 정의한 스코프의 인스턴스를 유일한 인수로 전달합니다.

```
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     *
     * @return void
     */
    protected static function booted()
    {
        static::addGlobalScope(new AncientScope);
    }
}
```

<!-- After adding the scope in the example above to the `App\Models\User` model, a call to the `User::all()` method will execute the following SQL query: -->
위 예제처럼 `App\Models\User` 모델에 스코프를 추가하면, `User::all()` 호출 시 아래와 같은 SQL 쿼리가 실행됩니다.

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
<!-- #### Anonymous Global Scopes -->
#### Anonymous Global Scopes

<!-- Eloquent also allows you to define global scopes using closures, which is particularly useful for simple scopes that do not warrant a separate class of their own. When defining a global scope using a closure, you should provide a scope name of your own choosing as the first argument to the `addGlobalScope` method: -->
Eloquent에서는 전역 스코프를 클로저(익명 함수)로도 정의할 수 있습니다. 간단한 스코프의 경우 별도의 클래스를 만들지 않아도 되어 편리합니다. 이때는 `addGlobalScope` 메서드에 첫 번째 인수로 스코프 이름 문자열을 전달하고, 두 번째 인수에 클로저를 전달합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     *
     * @return void
     */
    protected static function booted()
    {
        static::addGlobalScope('ancient', function (Builder $builder) {
            $builder->where('created_at', '<', now()->subYears(2000));
        });
    }
}
```

<a name="removing-global-scopes"></a>
<!-- #### Removing Global Scopes -->
#### Removing Global Scopes

<!-- If you would like to remove a global scope for a given query, you may use the `withoutGlobalScope` method. This method accepts the class name of the global scope as its only argument: -->
특정 쿼리에 대해 전역 스코프를 제거하려면, `withoutGlobalScope` 메서드를 사용하면 됩니다. 이 메서드에는 전역 스코프 클래스명을 유일한 인수로 전달합니다.

```
User::withoutGlobalScope(AncientScope::class)->get();
```

<!-- Or, if you defined the global scope using a closure, you should pass the string name that you assigned to the global scope: -->
만약 전역 스코프를 클로저로 정의했다면, 스코프를 추가할 때 지정한 문자열 이름을 전달해야 합니다.

```
User::withoutGlobalScope('ancient')->get();
```

<!-- If you would like to remove several or even all of the query's global scopes, you may use the `withoutGlobalScopes` method: -->
여러 개 또는 모든 전역 스코프를 한 번에 제거하고 싶다면, `withoutGlobalScopes` 메서드를 사용할 수 있습니다.

```
// Remove all of the global scopes...
User::withoutGlobalScopes()->get();

// Remove some of the global scopes...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();
```

<a name="local-scopes"></a>
<!-- ### Local Scopes -->
### Local Scopes

<!-- Local scopes allow you to define common sets of query constraints that you may easily re-use throughout your application. For example, you may need to frequently retrieve all users that are considered "popular". To define a scope, prefix an Eloquent model method with `scope`. -->
로컬 스코프를 사용하면 애플리케이션 전반에서 손쉽게 재사용할 수 있는 공통 쿼리 조건 집합을 정의할 수 있습니다. 예를 들어, 자주 "인기 있는" 사용자를 모두 조회해야 하는 상황이 있을 수 있습니다. 스코프를 정의하려면 Eloquent 모델의 메서드명 앞에 `scope`를 붙이면 됩니다.

<!-- Scopes should always return the same query builder instance or `void`: -->
스코프는 항상 동일한 쿼리 빌더 인스턴스 또는 `void`를 반환해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include popular users.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $query
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function scopePopular($query)
    {
        return $query->where('votes', '>', 100);
    }

    /**
     * Scope a query to only include active users.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $query
     * @return void
     */
    public function scopeActive($query)
    {
        $query->where('active', 1);
    }
}
```

<a name="utilizing-a-local-scope"></a>
<!-- #### Utilizing A Local Scope -->
#### Utilizing A Local Scope

<!-- Once the scope has been defined, you may call the scope methods when querying the model. However, you should not include the `scope` prefix when calling the method. You can even chain calls to various scopes: -->
스코프가 정의되었다면, 모델을 쿼리할 때 해당 스코프 메서드를 호출할 수 있습니다. 이때 메서드를 호출할 때에는 `scope` 접두사는 생략해야 합니다. 여러 스코프를 체이닝해서 사용할 수도 있습니다.

```
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

<!-- Combining multiple Eloquent model scopes via an `or` query operator may require the use of closures to achieve the correct [logical grouping](/docs/9.x/queries#logical-grouping): -->
여러 개의 Eloquent 모델 스코프를 `or` 쿼리 연산자로 조합하려면, [logical grouping](/docs/9.x/queries#logical-grouping)를 위해 클로저를 사용해야 할 수도 있습니다.

```
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

<!-- However, since this can be cumbersome, Laravel provides a "higher order" `orWhere` method that allows you to fluently chain scopes together without the use of closures: -->
하지만 이런 방식은 번거로울 수 있으므로, Laravel은 "고차원" `orWhere` 메서드를 제공해 클로저 없이도 스코프들을 유연하게 체이닝할 수 있게 해줍니다.

```
$users = App\Models\User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
<!-- #### Dynamic Scopes -->
#### Dynamic Scopes

<!-- Sometimes you may wish to define a scope that accepts parameters. To get started, just add your additional parameters to your scope method's signature. Scope parameters should be defined after the `$query` parameter: -->
스코프에 파라미터(인수)를 전달하고 싶을 때도 있습니다. 이 경우, 스코프 메서드의 시그니처에 추가 인수를 작성하면 됩니다. 스코프의 인수는 항상 `$query` 인수 뒤에 정의해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include users of a given type.
     *
     * @param  \Illuminate\Database\Eloquent\Builder  $query
     * @param  mixed  $type
     * @return \Illuminate\Database\Eloquent\Builder
     */
    public function scopeOfType($query, $type)
    {
        return $query->where('type', $type);
    }
}
```

<!-- Once the expected arguments have been added to your scope method's signature, you may pass the arguments when calling the scope: -->
필요한 인수가 스코프 메서드에 추가되었다면, 스코프를 호출할 때 인수를 전달할 수 있습니다.

```
$users = User::ofType('admin')->get();
```

<a name="comparing-models"></a>
<!-- ## Comparing Models -->
## Comparing Models

<!-- Sometimes you may need to determine if two models are the "same" or not. The `is` and `isNot` methods may be used to quickly verify two models have the same primary key, table, and database connection or not: -->
가끔 두 모델이 "같은" 모델인지 판별해야 할 때가 있습니다. `is` 및 `isNot` 메서드를 이용하면 두 모델의 기본키, 테이블, 데이터베이스 커넥션이 같은지 빠르게 확인할 수 있습니다.

```
if ($post->is($anotherPost)) {
    //
}

if ($post->isNot($anotherPost)) {
    //
}
```

<!-- The `is` and `isNot` methods are also available when using the `belongsTo`, `hasOne`, `morphTo`, and `morphOne` [relationships](/docs/9.x/eloquent-relationships). This method is particularly helpful when you would like to compare a related model without issuing a query to retrieve that model: -->
`is`와 `isNot` 메서드는 `belongsTo`, `hasOne`, `morphTo`, `morphOne`과 같은 [relationships](/docs/9.x/eloquent-relationships)에서도 사용할 수 있습니다. 이 기능은 관련된 모델을 쿼리로 조회하지 않고도 비교할 수 있다는 점에서 유용합니다.

```
if ($post->author()->is($user)) {
    //
}
```

<a name="events"></a>
<!-- ## Events -->
## Events

> [!NOTE]
> Eloquent 이벤트를 클라이언트 사이드 애플리케이션으로 직접 broadcasting하고 싶으신가요? Laravel의 [model event broadcasting](/docs/9.x/broadcasting#model-broadcasting)을 참고하세요.

<!-- Eloquent models dispatch several events, allowing you to hook into the following moments in a model's lifecycle: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, and `replicating`. -->
Eloquent 모델은 여러 이벤트를 발생시키며, 이를 통해 모델 생명주기에서 다음과 같은 시점에 후킹(hook)이 가능합니다: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, `replicating`.

<!-- The `retrieved` event will dispatch when an existing model is retrieved from the database. When a new model is saved for the first time, the `creating` and `created` events will dispatch. The `updating` / `updated` events will dispatch when an existing model is modified and the `save` method is called. The `saving` / `saved` events will dispatch when a model is created or updated - even if the model's attributes have not been changed. Event names ending with `-ing` are dispatched before any changes to the model are persisted, while events ending with `-ed` are dispatched after the changes to the model are persisted. -->
`retrieved` 이벤트는 데이터베이스에서 기존 모델을 조회할 때 발생합니다. 새 모델을 처음 저장할 때는 `creating`과 `created` 이벤트가 발생합니다. `updating` / `updated` 이벤트는 기존 모델이 수정되고 `save` 메서드가 호출될 때 발생합니다. `saving` / `saved` 이벤트는 모델이 생성되거나 수정될 때, 모델의 속성이 실제로 변경되지 않았더라도 발생합니다. 이벤트 이름이 `-ing`로 끝나면 모델의 변경 사항이 데이터베이스에 반영되기 전에 발생하고, `-ed`로 끝나면 변경 사항이 반영된 후에 발생합니다.

<!-- To start listening to model events, define a `$dispatchesEvents` property on your Eloquent model. This property maps various points of the Eloquent model's lifecycle to your own [event classes](/docs/9.x/events). Each model event class should expect to receive an instance of the affected model via its constructor: -->
모델 이벤트를 수신하려면, Eloquent 모델에 `$dispatchesEvents` 속성을 정의해야 합니다. 이 속성은 Eloquent 모델의 생명주기의 여러 지점과 여러분이 작성한 [event classes](/docs/9.x/events)를 연결해줍니다. 각 모델 이벤트 클래스는 영향을 받는 모델 인스턴스를 생성자에서 받을 것으로 예상합니다.

```
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
     * @var array
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```

<!-- After defining and mapping your Eloquent events, you may use [event listeners](/docs/9.x/events#defining-listeners) to handle the events. -->
Eloquent 이벤트의 정의와 매핑을 마치면, [event listeners](/docs/9.x/events#defining-listeners)를 사용해 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent를 통한 대량 업데이트나 삭제 쿼리를 실행하면, 해당 모델에 대해 `saved`, `updated`, `deleting`, `deleted` 이벤트가 **발생하지 않습니다**. 이는 실제로 대량 업데이트/삭제 시 모델을 조회하지 않기 때문에 그렇습니다.

<a name="events-using-closures"></a>
<!-- ### Using Closures -->
### Using Closures

<!-- Instead of using custom event classes, you may register closures that execute when various model events are dispatched. Typically, you should register these closures in the `booted` method of your model: -->
커스텀 이벤트 클래스 대신, 다양한 모델 이벤트가 발생할 때 실행할 클로저를 등록할 수도 있습니다. 일반적으로 이런 클로저들은 모델의 `booted` 메서드 내에 등록하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     *
     * @return void
     */
    protected static function booted()
    {
        static::created(function ($user) {
            //
        });
    }
}
```

<!-- If needed, you may utilize [queueable anonymous event listeners](/docs/9.x/events#queuable-anonymous-event-listeners) when registering model events. This will instruct Laravel to execute the model event listener in the background using your application's [queue](/docs/9.x/queues): -->
필요하다면, [queueable anonymous event listeners](/docs/9.x/events#queuable-anonymous-event-listeners)도 사용할 수 있습니다. 이를 사용하면, 이벤트 리스너가 애플리케이션의 [queue](/docs/9.x/queues)를 통해 백그라운드에서 실행되도록 Laravel에 지정할 수 있습니다.

```
use function Illuminate\Events\queueable;

static::created(queueable(function ($user) {
    //
}));
```

<a name="observers"></a>
<!-- ### Observers -->
### Observers

<a name="defining-observers"></a>
<!-- #### Defining Observers -->
#### Defining Observers

<!-- If you are listening for many events on a given model, you may use observers to group all of your listeners into a single class. Observer classes have method names which reflect the Eloquent events you wish to listen for. Each of these methods receives the affected model as their only argument. The `make:observer` Artisan command is the easiest way to create a new observer class: -->
하나의 모델에서 여러 이벤트를 동시에 관찰(listen)하고 싶을 경우, 여러 리스너를 하나의 클래스에 그룹화할 수 있는 옵저버를 사용할 수 있습니다. 옵저버 클래스는 감지하고자 하는 Eloquent 이벤트와 이름이 동일한 메서드를 가집니다. 각 메서드는 영향을 받는 모델을 유일한 인수로 받습니다. 새로운 옵저버 클래스를 생성하는 가장 쉬운 방법은 `make:observer` Artisan 명령어를 사용하는 것입니다.

```shell
php artisan make:observer UserObserver --model=User
```

<!-- This command will place the new observer in your `app/Observers` directory. If this directory does not exist, Artisan will create it for you. Your fresh observer will look like the following: -->
이 명령어는 새로운 옵저버 파일을 `app/Observers` 디렉토리에 생성합니다. 해당 디렉토리가 없다면 Artisan이 자동으로 만들어줍니다. 생성된 옵저버 클래스의 기본 구조는 아래와 같습니다.

```
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * Handle the User "created" event.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function created(User $user)
    {
        //
    }

    /**
     * Handle the User "updated" event.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function updated(User $user)
    {
        //
    }

    /**
     * Handle the User "deleted" event.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function deleted(User $user)
    {
        //
    }

    /**
     * Handle the User "restored" event.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function restored(User $user)
    {
        //
    }

    /**
     * Handle the User "forceDeleted" event.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function forceDeleted(User $user)
    {
        //
    }
}
```

<!-- To register an observer, you need to call the `observe` method on the model you wish to observe. You may register observers in the `boot` method of your application's `App\Providers\EventServiceProvider` service provider: -->
옵저버를 등록하려면, 관찰하고자 하는 모델에서 `observe` 메서드를 호출하면 됩니다. 대개는 애플리케이션의 `App\Providers\EventServiceProvider` 서비스 프로바이더의 `boot` 메서드에서 옵저버를 등록합니다.

```
use App\Models\User;
use App\Observers\UserObserver;

/**
 * Register any events for your application.
 *
 * @return void
 */
public function boot()
{
    User::observe(UserObserver::class);
}
```

<!-- Alternatively, you may list your observers within an `$observers` property of your applications' `App\Providers\EventServiceProvider` class: -->
또는, 애플리케이션의 `App\Providers\EventServiceProvider` 클래스의 `$observers` 속성에 옵저버를 나열해 둘 수도 있습니다.

```
use App\Models\User;
use App\Observers\UserObserver;

/**
 * The model observers for your application.
 *
 * @var array
 */
protected $observers = [
    User::class => [UserObserver::class],
];
```

> [!NOTE]
> 옵저버에서 감지할 수 있는 이벤트는 `saving`, `retrieved` 등 더 다양하게 있습니다. 자세한 내용은 [events](#events) 문서에서 확인할 수 있습니다.

<a name="observers-and-database-transactions"></a>

<!-- #### Observers & Database Transactions -->
#### Observers & Database Transactions

<!-- When models are being created within a database transaction, you may want to instruct an observer to only execute its event handlers after the database transaction is committed. You may accomplish this by defining an `$afterCommit` property on the observer. If a database transaction is not in progress, the event handlers will execute immediately: -->
모델이 데이터베이스 트랜잭션 내에서 생성될 때, 옵저버의 이벤트 핸들러가 트랜잭션이 커밋된 이후에만 실행되도록 지정하고 싶을 때가 있습니다. 이럴 때는 옵저버 클래스에 `$afterCommit` 속성을 정의하면 됩니다. 만약 데이터베이스 트랜잭션이 진행 중이 아니라면, 이벤트 핸들러는 즉시 실행됩니다.

```
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * Handle events after all transactions are committed.
     *
     * @var bool
     */
    public $afterCommit = true;

    /**
     * Handle the User "created" event.
     *
     * @param  \App\Models\User  $user
     * @return void
     */
    public function created(User $user)
    {
        //
    }
}
```

<a name="muting-events"></a>
<!-- ### Muting Events -->
### Muting Events

<!-- You may occasionally need to temporarily "mute" all events fired by a model. You may achieve this using the `withoutEvents` method. The `withoutEvents` method accepts a closure as its only argument. Any code executed within this closure will not dispatch model events, and any value returned by the closure will be returned by the `withoutEvents` method: -->
가끔 모델에서 발생하는 모든 이벤트를 일시적으로 "무시"하고 싶을 때가 있습니다. 이 경우에는 `withoutEvents` 메서드를 사용하면 됩니다. `withoutEvents` 메서드는 하나의 클로저를 인수로 받으며, 해당 클로저 내에서 실행되는 모든 코드는 모델 이벤트를 발생시키지 않습니다. 또한, 클로저가 반환한 값이 곧 `withoutEvents` 메서드의 반환값이 됩니다.

```
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
<!-- #### Saving A Single Model Without Events -->
#### Saving A Single Model Without Events

<!-- Sometimes you may wish to "save" a given model without dispatching any events. You may accomplish this using the `saveQuietly` method: -->
특정 모델을 저장하면서 이벤트를 발생시키고 싶지 않을 때도 있습니다. 이럴 때는 `saveQuietly` 메서드를 사용하면 이벤트가 실행되지 않습니다.

```
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

<!-- You may also "update", "delete", "soft delete", "restore", and "replicate" a given model without dispatching any events: -->
또한, 주어진 모델에 대해 이벤트를 발생시키지 않고 "update", "delete", "soft delete", "restore", "replicate" 등도 실행할 수 있습니다.

```
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
