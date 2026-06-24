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
Laravel には、データベースとの対話を楽しくするオブジェクト リレーショナル マッパー (ORM) である Eloquent が含まれています。 Eloquent を使用する場合、各データベース テーブルには、そのテーブルと対話するために使用される対応する「モデル」があります。 Eloquent モデルでは、データベース テーブルからレコードを取得するだけでなく、テーブルからレコードを挿入、更新、削除することもできます。

> [!NOTE]
> 開始する前に、必ずアプリケーションの `config/database.php` 構成ファイルでデータベース接続を構成してください。データベースの構成の詳細については、[the database configuration documentation](/docs/master/database#configuration) を確認してください。

<a name="generating-model-classes"></a>
<!-- ## Generating Model Classes -->
## Generating Model Classes

<!-- To get started, let's create an Eloquent model. Models typically live in the `app\Models` directory and extend the `Illuminate\Database\Eloquent\Model` class. You may use the `make:model` [Artisan command](/docs/master/artisan) to generate a new model: -->
まず、Eloquent モデルを作成しましょう。モデルは通常、`app\Models` ディレクトリに存在し、`Illuminate\Database\Eloquent\Model` クラスを拡張します。 `make:model` [Artisan command](/docs/master/artisan) を使用して新しいモデルを生成できます。

```shell
php artisan make:model Flight
```

<!-- If you would like to generate a [database migration](/docs/master/migrations) when you generate the model, you may use the `--migration` or `-m` option: -->
モデルの生成時に [database migration](/docs/master/migrations) を生成したい場合は、`--migration` または `-m` オプションを使用できます。

```shell
php artisan make:model Flight --migration
```

<!-- You may generate various other types of classes when generating a model, such as factories, seeders, policies, controllers, and form requests. In addition, these options may be combined to create multiple classes at once: -->
モデルを生成するときに、ファクトリ、シーダー、ポリシー、コントローラ、フォーム リクエストなど、他のさまざまなタイプのクラスを生成できます。さらに、これらのオプションを組み合わせて複数のクラスを一度に作成することもできます。

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
コードをざっと読んだだけでは、モデルで使用可能な属性と関係をすべて判断するのが難しい場合があります。代わりに、`model:show` Artisan コマンドを試してください。このコマンドは、すべてのモデルの属性と関係の便利な概要を提供します。

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
<!-- ## Eloquent Model Conventions -->
## Eloquent Model Conventions

<!-- Models generated by the `make:model` command will be placed in the `app/Models` directory. Let's examine a basic model class and discuss some of Eloquent's key conventions: -->
`make:model` コマンドによって生成されたモデルは、`app/Models` ディレクトリに配置されます。基本的なモデル クラスを調べて、Eloquent の主要な規則のいくつかについて説明しましょう。

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
上記の例を見た後、どのデータベース テーブルが `Flight` モデルに対応するかを Eloquent に伝えていないことに気付いたかもしれません。慣例により、別の名前が明示的に指定されない限り、「スネークケース」クラスの複数名がテーブル名として使用されます。したがって、この場合、Eloquent は、`Flight` モデルが `flights` テーブルにレコードを保存するのに対し、`AirTrafficController` モデルは `air_traffic_controllers` テーブルにレコードを保存すると想定します。

<!-- If your model's corresponding database table does not fit this convention, you may manually specify the model's table name using the `Table` attribute: -->
モデルの対応するデータベース テーブルがこの規則に適合しない場合は、`Table` 属性を使用してモデルのテーブル名を手動で指定できます。

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
<!-- ### Primary Keys -->
### Primary Keys

<!-- Eloquent will also assume that each model's corresponding database table has a primary key column named `id`. If necessary, you may specify a different column that serves as your model's primary key using the `key` argument on the `Table` attribute: -->
また、Eloquent は、各モデルの対応するデータベース テーブルに `id` という名前の主キー列があると想定します。必要に応じて、`Table` 属性の `key` 引数を使用して、モデルの主キーとして機能する別の列を指定できます。

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

<!-- In addition, Eloquent assumes that the primary key is an incrementing integer value, which means that Eloquent will automatically cast the primary key to an integer. If you wish to use a non-incrementing or a non-numeric primary key, you should specify the `keyType` and `incrementing` arguments on the `Table` attribute: -->
さらに、Eloquent は主キーが増加する整数値であると想定します。これは、Eloquent が主キーを自動的に整数にcastすることを意味します。非インクリメントまたは非数値の主キーを使用したい場合は、`Table` 属性で `keyType` および `incrementing` 引数を指定する必要があります。

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
<!-- #### "Composite" Primary Keys -->
#### "Composite" Primary Keys

<!-- Eloquent requires each model to have at least one uniquely identifying "ID" that can serve as its primary key. "Composite" primary keys are not supported by Eloquent models. However, you are free to add additional multi-column, unique indexes to your database tables in addition to the table's uniquely identifying primary key. -->
Eloquent では、各モデルに主キーとして機能する一意に識別できる「ID」を少なくとも 1 つ持つ必要があります。 「複合」主キーは Eloquent モデルではサポートされていません。ただし、テーブルを一意に識別する主キーに加えて、複数列の一意のインデックスをデータベース テーブルに自由に追加できます。

<a name="uuid-and-ulid-keys"></a>
<!-- ### UUID and ULID Keys -->
### UUID and ULID Keys

<!-- Instead of using auto-incrementing integers as your Eloquent model's primary keys, you may choose to use UUIDs instead. UUIDs are universally unique alpha-numeric identifiers that are 36 characters long. -->
Eloquent モデルの主キーとして自動インクリメント整数を使用する代わりに、UUID を使用することを選択することもできます。 UUID は、36 文字の長さの普遍的に一意の英数字の識別子です。

<!-- If you would like a model to use a UUID key instead of an auto-incrementing integer key, you may use the `Illuminate\Database\Eloquent\Concerns\HasUuids` trait on the model. Of course, you should ensure that the model has a [UUID equivalent primary key column](/docs/master/migrations#column-method-uuid): -->
モデルで自動インクリメント整数キーの代わりに UUID キーを使用したい場合は、モデルで `Illuminate\Database\Eloquent\Concerns\HasUuids` トレイトを使用できます。もちろん、モデルに [UUID equivalent primary key column](/docs/master/migrations#column-method-uuid) があることを確認する必要があります。

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

<!-- By default, The `HasUuids` trait will generate ["ordered" UUIDs](/docs/master/strings#method-str-ordered-uuid) for your models. These UUIDs are more efficient for indexed database storage because they can be sorted lexicographically. -->
デフォルトでは、`HasUuids` トレイトはモデルに ["ordered" UUIDs](/docs/master/strings#method-str-ordered-uuid) を生成します。これらの UUID は辞書順に並べ替えることができるため、インデックス付きデータベース ストレージにとってより効率的です。

<!-- You can override the UUID generation process for a given model by defining a `newUniqueId` method on the model. In addition, you may specify which columns should receive UUIDs by defining a `uniqueIds` method on the model: -->
モデルで `newUniqueId` メソッドを定義することで、特定のモデルの UUID 生成プロセスをオーバーライドできます。さらに、モデルで `uniqueIds` メソッドを定義することで、どの列が UUID を受け取るかを指定できます。

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

<!-- If you wish, you may choose to utilize "ULIDs" instead of UUIDs. ULIDs are similar to UUIDs; however, they are only 26 characters in length. Like ordered UUIDs, ULIDs are lexicographically sortable for efficient database indexing. To utilize ULIDs, you should use the `Illuminate\Database\Eloquent\Concerns\HasUlids` trait on your model. You should also ensure that the model has a [ULID equivalent primary key column](/docs/master/migrations#column-method-ulid): -->
必要に応じて、UUID の代わりに「ULID」を使用することを選択できます。 ULID は UUID に似ています。ただし、長さはわずか 26 文字です。順序付けされた UUID と同様に、ULID は辞書編集的にソート可能であり、効率的なデータベースのインデックス作成が可能です。 ULID を利用するには、モデルで `Illuminate\Database\Eloquent\Concerns\HasUlids` トレイトを使用する必要があります。モデルに [ULID equivalent primary key column](/docs/master/migrations#column-method-ulid) があることも確認する必要があります。

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

<!-- By default, Eloquent expects `created_at` and `updated_at` columns to exist on your model's corresponding database table. Eloquent will automatically set these column's values when models are created or updated. If you do not want these columns to be automatically managed by Eloquent, you may set `timestamps` to `false` on your model's `Table` attribute: -->
デフォルトでは、Eloquent は、モデルの対応するデータベース テーブルに `created_at` 列と `updated_at` 列が存在することを期待します。 Eloquent は、モデルの作成または更新時にこれらの列の値を自動的に設定します。これらの列を Eloquent によって自動的に管理したくない場合は、モデルの `Table` 属性で `timestamps` を `false` に設定できます。

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

<!-- If you need to customize the format of your model's timestamps, you may use the `dateFormat` argument on the `Table` attribute. This determines how date attributes are stored in the database as well as their format when the model is serialized to an array or JSON: -->
モデルのタイムスタンプの形式をカスタマイズする必要がある場合は、`Table` 属性で `dateFormat` 引数を使用できます。これにより、モデルが配列または JSON にシリアル化されるときの日付属性のデータベースへの保存方法とその形式が決まります。

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

<!-- If you need to customize the names of the columns used to store the timestamps, you may define `CREATED_AT` and `UPDATED_AT` constants on your model: -->
タイムスタンプの保存に使用される列の名前をカスタマイズする必要がある場合は、モデルで `CREATED_AT` および `UPDATED_AT` 定数を定義できます。

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
モデルの `updated_at` タイムスタンプを変更せずにモデル操作を実行したい場合は、`withoutTimestamps` メソッドに指定されたクロージャ内でモデルを操作できます。

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
<!-- ### Database Connections -->
### Database Connections

<!-- By default, all Eloquent models will use the default database connection that is configured for your application. If you would like to specify a different connection that should be used when interacting with a particular model, you may use the `Connection` attribute: -->
デフォルトでは、すべての Eloquent モデルは、アプリケーション用に設定されたデフォルトのデータベース接続を使用します。特定のモデルと対話するときに使用する別の接続を指定したい場合は、`Connection` 属性を使用できます。

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
<!-- ### Default Attribute Values -->
### Default Attribute Values

<!-- By default, a newly instantiated model instance will not contain any attribute values. If you would like to define the default values for some of your model's attributes, you may define an `$attributes` property on your model. Attribute values placed in the `$attributes` array should be in their raw, "storable" format as if they were just read from the database: -->
デフォルトでは、新しくインスタンス化されたモデル インスタンスには属性値が含まれません。モデルの一部の属性のデフォルト値を定義したい場合は、モデルで `$attributes` プロパティを定義できます。 `$attributes` 配列に配置される属性値は、データベースから読み取られたばかりのような生の「保存可能な」形式である必要があります。

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
Laravel は、さまざまな状況で Eloquent の動作と「厳密さ」を設定できるいくつかのメソッドを提供します。

<!-- First, the `preventLazyLoading` method accepts an optional boolean argument that indicates if lazy loading should be prevented. For example, you may wish to only disable lazy loading in non-production environments so that your production environment will continue to function normally even if a lazy loaded relationship is accidentally present in production code. Typically, this method should be invoked in the `boot` method of your application's `AppServiceProvider`: -->
まず、`preventLazyLoading` メソッドは、遅延読み込みを防止する必要があるかどうかを示すオプションのブール引数を受け入れます。たとえば、非実稼働環境でのみ遅延ロードを無効にし、実稼働コードに遅延ロード関係が誤って存在した場合でも実稼働環境が正常に機能し続けるようにすることができます。通常、このメソッドはアプリケーションの `AppServiceProvider` の `boot` メソッドで呼び出す必要があります。

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
また、`preventSilentlyDiscardingAttributes` メソッドを呼び出して、入力できない属性を入力しようとしたときに例外をスローするように Laravel に指示することもできます。これは、ローカル開発中にモデルの `fillable` 配列に追加されていない属性を設定しようとしたときの予期しないエラーを防ぐのに役立ちます。

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
<!-- ## Retrieving Models -->
## Retrieving Models

<!-- Once you have created a model and [its associated database table](/docs/master/migrations#generating-migrations), you are ready to start retrieving data from your database. You can think of each Eloquent model as a powerful [query builder](/docs/master/queries) allowing you to fluently query the database table associated with the model. The model's `all` method will retrieve all of the records from the model's associated database table: -->
モデルと [its associated database table](/docs/master/migrations#generating-migrations) を作成したら、データベースからのデータの取得を開始する準備が整います。各 Eloquent モデルは、モデルに関連付けられたデータベース テーブルにスムーズにクエリを実行できる強力な [query builder](/docs/master/queries) と考えることができます。モデルの `all` メソッドは、モデルに関連付けられたデータベース テーブルからすべてのレコードを取得します。

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
<!-- #### Building Queries -->
#### Building Queries

<!-- The Eloquent `all` method will return all of the results in the model's table. However, since each Eloquent model serves as a [query builder](/docs/master/queries), you may add additional constraints to queries and then invoke the `get` method to retrieve the results: -->
Eloquent `all` メソッドは、モデルのテーブル内のすべての結果を返します。ただし、各 Eloquent モデルは [query builder](/docs/master/queries) として機能するため、クエリに追加の制約を追加してから、`get` メソッドを呼び出して結果を取得することができます。

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent モデルはクエリビルダであるため、Laravel の [query builder](/docs/master/queries) によって提供されるすべてのメソッドを確認する必要があります。 Eloquent クエリを作成するときは、これらのメソッドのいずれかを使用できます。

<a name="refreshing-models"></a>
<!-- #### Refreshing Models -->
#### Refreshing Models

<!-- If you already have an instance of an Eloquent model that was retrieved from the database, you can "refresh" the model using the `fresh` and `refresh` methods. The `fresh` method will re-retrieve the model from the database. The existing model instance will not be affected: -->
データベースから取得した Eloquent モデルのインスタンスがすでにある場合は、`fresh` メソッドと `refresh` メソッドを使用してモデルを「更新」できます。 `fresh` メソッドはデータベースからモデルを再取得します。既存のモデル インスタンスは影響を受けません。

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

<!-- The `refresh` method will re-hydrate the existing model using fresh data from the database. In addition, all of its loaded relationships will be refreshed as well: -->
`refresh` メソッドは、データベースからの新しいデータを使用して既存のモデルを再ハイドレートします。さらに、読み込まれた関係もすべて更新されます。

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
これまで見てきたように、`all` や `get` などの Eloquent メソッドはデータベースから複数のレコードを取得します。ただし、これらのメソッドはプレーンな PHP 配列を返しません。代わりに、`Illuminate\Database\Eloquent\Collection` のインスタンスが返されます。

<!-- The Eloquent `Collection` class extends Laravel's base `Illuminate\Support\Collection` class, which provides a [variety of helpful methods](/docs/master/collections#available-methods) for interacting with data collections. For example, the `reject` method may be used to remove models from a collection based on the results of an invoked closure: -->
Eloquent `Collection` クラスは、Laravel の基本 `Illuminate\Support\Collection` クラスを拡張し、データ コレクションと対話するための [variety of helpful methods](/docs/master/collections#available-methods) を提供します。たとえば、`reject` メソッドは、呼び出されたクロージャの結果に基づいてコレクションからモデルを削除するために使用できます。

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

<!-- In addition to the methods provided by Laravel's base collection class, the Eloquent collection class provides [a few extra methods](/docs/master/eloquent-collections#available-methods) that are specifically intended for interacting with collections of Eloquent models. -->
Laravel の基本コレクション クラスによって提供されるメソッドに加えて、Eloquent コレクション クラスは、特に Eloquent モデルのコレクションと対話することを目的とした [a few extra methods](/docs/master/eloquent-collections#available-methods) を提供します。

<!-- Since all of Laravel's collections implement PHP's iterable interfaces, you may loop over collections as if they were an array: -->
Laravel のコレクションはすべて PHP の反復可能なインターフェイスを実装しているため、コレクションを配列であるかのようにループできます。

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
<!-- ### Chunking Results -->
### Chunking Results

<!-- Your application may run out of memory if you attempt to load tens of thousands of Eloquent records via the `all` or `get` methods. Instead of using these methods, the `chunk` method may be used to process large numbers of models more efficiently. -->
`all` メソッドまたは `get` メソッドを介して数万の Eloquent レコードをロードしようとすると、アプリケーションがメモリ不足になる可能性があります。これらのメソッドを使用する代わりに、`chunk` メソッドを使用して、多数のモデルをより効率的に処理できます。

<!-- The `chunk` method will retrieve a subset of Eloquent models, passing them to a closure for processing. Since only the current chunk of Eloquent models is retrieved at a time, the `chunk` method will provide significantly reduced memory usage when working with a large number of models: -->
`chunk` メソッドは Eloquent モデルのサブセットを取得し、処理のためにクロージャに渡します。一度に取得されるのは Eloquent モデルの現在のチャンクのみであるため、`chunk` メソッドを使用すると、多数のモデルを操作する場合にメモリ使用量が大幅に削減されます。

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
`chunk` メソッドに渡される最初の引数は、「チャンク」ごとに受信するレコードの数です。 2 番目の引数として渡されたクロージャは、データベースから取得されるチャンクごとに呼び出されます。データベース クエリが実行され、クロージャに渡されたレコードの各チャンクが取得されます。

<!-- If you are filtering the results of the `chunk` method based on a column that you will also be updating while iterating over the results, you should use the `chunkById` method. Using the `chunk` method in these scenarios could lead to unexpected and inconsistent results. Internally, the `chunkById` method will always retrieve models with an `id` column greater than the last model in the previous chunk: -->
結果の反復処理中に更新も行う列に基づいて `chunk` メソッドの結果をフィルター処理する場合は、`chunkById` メソッドを使用する必要があります。これらのシナリオで `chunk` メソッドを使用すると、予期しない一貫性のない結果が生じる可能性があります。内部的には、`chunkById` メソッドは常に、前のチャンクの最後のモデルより大きい `id` 列を持つモデルを取得します。

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

<!-- Since the `chunkById` and `lazyById` methods add their own "where" conditions to the query being executed, you should typically [logically group](/docs/master/queries#logical-grouping) your own conditions within a closure: -->
`chunkById` メソッドと `lazyById` メソッドは、実行されるクエリに独自の「where」条件を追加するため、通常はクロージャ内で独自の条件を [logically group](/docs/master/queries#logical-grouping) する必要があります。

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

<!-- The `lazy` method works similarly to [the `chunk` method](#chunking-results) in the sense that, behind the scenes, it executes the query in chunks. However, instead of passing each chunk directly into a callback as is, the `lazy` method returns a flattened [LazyCollection](/docs/master/collections#lazy-collections) of Eloquent models, which lets you interact with the results as a single stream: -->
`lazy` メソッドは、バックグラウンドでクエリをチャンク単位で実行するという意味で、[the `chunk` method](#chunking-results) と同様に機能します。ただし、各チャンクをそのままコールバックに直接渡す代わりに、`lazy` メソッドは Eloquent モデルのフラット化された [LazyCollection](/docs/master/collections#lazy-collections) を返します。これにより、結果を単一のストリームとして操作できます。

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

<!-- If you are filtering the results of the `lazy` method based on a column that you will also be updating while iterating over the results, you should use the `lazyById` method. Internally, the `lazyById` method will always retrieve models with an `id` column greater than the last model in the previous chunk: -->
結果の反復処理中に更新も行う列に基づいて `lazy` メソッドの結果をフィルター処理する場合は、`lazyById` メソッドを使用する必要があります。内部的には、`lazyById` メソッドは常に、前のチャンクの最後のモデルより大きい `id` 列を持つモデルを取得します。

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

<!-- You may filter the results based on the descending order of the `id` using the `lazyByIdDesc` method. -->
`lazyByIdDesc` メソッドを使用して、`id` の降順に基づいて結果をフィルタリングできます。

<a name="cursors"></a>
<!-- ### Cursors -->
### Cursors

<!-- Similar to the `lazy` method, the `cursor` method may be used to significantly reduce your application's memory consumption when iterating through tens of thousands of Eloquent model records. -->
`lazy` メソッドと同様に、`cursor` メソッドを使用すると、数万の Eloquent モデル レコードを反復処理するときにアプリケーションのメモリ消費を大幅に削減できます。

<!-- The `cursor` method will only execute a single database query; however, the individual Eloquent models will not be hydrated until they are actually iterated over. Therefore, only one Eloquent model is kept in memory at any given time while iterating over the cursor. -->
`cursor` メソッドは、単一のデータベース クエリのみを実行します。ただし、個々の Eloquent モデルは、実際に反復されるまでハイドレートされません。したがって、カーソル上で反復している間、常に 1 つの Eloquent モデルだけがメモリに保持されます。

> [!WARNING]
> `cursor` メソッドは、メモリ内に一度に 1 つの Eloquent モデルしか保持しないため、関係を一括ロードすることはできません。関係を一括ロードする必要がある場合は、代わりに [the `lazy` method](#chunking-using-lazy-collections) の使用を検討してください。

<!-- Internally, the `cursor` method uses PHP [generators](https://www.php.net/manual/en/language.generators.overview.php) to implement this functionality: -->
内部的には、`cursor` メソッドは PHP [generators](https://www.php.net/manual/en/language.generators.overview.php) を使用してこの機能を実装します。

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

<!-- The `cursor` returns an `Illuminate\Support\LazyCollection` instance. [Lazy collections](/docs/master/collections#lazy-collections) allow you to use many of the collection methods available on typical Laravel collections while only loading a single model into memory at a time: -->
`cursor` は、`Illuminate\Support\LazyCollection` インスタンスを返します。 [Lazy collections](/docs/master/collections#lazy-collections) を使用すると、一度に 1 つのモデルのみをメモリにロードしながら、一般的な Laravel コレクションで利用可能な多くのコレクション メソッドを使用できます。

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
`cursor` メソッドは、通常のクエリよりもはるかに少ないメモリを使用しますが (一度に 1 つの Eloquent モデルのみをメモリに保持するため)、それでも最終的にはメモリが不足します。 [due to PHP's PDO driver internally caching all raw query results in its buffer](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)です。非常に多くの Eloquent レコードを扱っている場合は、代わりに [the `lazy` method](#chunking-using-lazy-collections) の使用を検討してください。

<a name="advanced-subqueries"></a>
<!-- ### Advanced Subqueries -->
### Advanced Subqueries

<a name="subquery-selects"></a>
<!-- #### Subquery Selects -->
#### Subquery Selects

<!-- Eloquent also offers advanced subquery support, which allows you to pull information from related tables in a single query. For example, let's imagine that we have a table of flight `destinations` and a table of `flights` to destinations. The `flights` table contains an `arrived_at` column which indicates when the flight arrived at the destination. -->
Eloquent は、高度なサブクエリ サポートも提供しており、これにより、単一のクエリで関連テーブルから情報を取得できます。たとえば、目的地へのフライト `destinations` のテーブルと `flights` のテーブルがあると想像してみましょう。 `flights` テーブルには、フライトが目的地にいつ到着したかを示す `arrived_at` 列が含まれています。

<!-- Using the subquery functionality available to the query builder's `select` and `addSelect` methods, we can select all of the `destinations` and the name of the flight that most recently arrived at that destination using a single query: -->
クエリビルダの `select` メソッドと `addSelect` メソッドで利用できるサブクエリ機能を使用すると、単一のクエリを使用して、すべての `destinations` とその目的地に最後に到着したフライトの名前を選択できます。

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
さらに、クエリビルダの `orderBy` 関数はサブクエリをサポートします。引き続きフライトの例を使用します。この機能を使用して、最後のフライトが目的地に到着した時間に基づいてすべての目的地を並べ替えることができます。繰り返しますが、これは単一のデータベース クエリの実行中に行うことができます。

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
特定のクエリに一致するすべてのレコードを取得するだけでなく、`find`、`first`、または `firstWhere` メソッドを使用して単一のレコードを取得することもできます。これらのメソッドは、モデルのコレクションを返す代わりに、単一のモデル インスタンスを返します。

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
結果が見つからない場合は、他のアクションを実行したい場合があります。 `findOr` メソッドと `firstOr` メソッドは、単一のモデル インスタンスを返すか、結果が見つからない場合は、指定されたクロージャを実行します。クロージャによって返される値は、メソッドの結果とみなされます。

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
モデルが見つからない場合に例外をスローしたい場合があります。これは、ルートまたはコントローラで特に便利です。 `findOrFail` メソッドと `firstOrFail` メソッドは、クエリの最初の結果を取得します。ただし、結果が見つからない場合は、`Illuminate\Database\Eloquent\ModelNotFoundException` がスローされます。

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

<!-- If the `ModelNotFoundException` is not caught, a 404 HTTP response is automatically sent back to the client: -->
`ModelNotFoundException` が捕捉されない場合、404 HTTP 応答が自動的にクライアントに返されます。

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
`firstOrCreate` メソッドは、指定された列と値のペアを使用してデータベース レコードの検索を試みます。データベース内でモデルが見つからない場合は、最初の配列引数とオプションの 2 番目の配列引数をマージした結果の属性を持つレコードが挿入されます。

<!-- The `firstOrNew` method, like `firstOrCreate`, will attempt to locate a record in the database matching the given attributes. However, if a model is not found, a new model instance will be returned. Note that the model returned by `firstOrNew` has not yet been persisted to the database. You will need to manually call the `save` method to persist it: -->
`firstOrNew` メソッドは、`firstOrCreate` と同様に、指定された属性に一致するデータベース内のレコードを検索しようとします。ただし、モデルが見つからない場合は、新しいモデル インスタンスが返されます。 `firstOrNew` によって返されたモデルはまだデータベースに永続化されていないことに注意してください。 `save` メソッドを手動で呼び出して永続化する必要があります。

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

<!-- When interacting with Eloquent models, you may also use the `count`, `sum`, `max`, and other [aggregate methods](/docs/master/queries#aggregates) provided by the Laravel [query builder](/docs/master/queries). As you might expect, these methods return a scalar value instead of an Eloquent model instance: -->
Eloquent モデルを操作するときは、Laravel [aggregate methods](/docs/master/queries#aggregates) によって提供される `count`、`sum`、`max`、およびその他の [query builder](/docs/master/queries) を使用することもできます。ご想像のとおり、これらのメソッドは Eloquent モデル インスタンスの代わりにスカラー値を返します。

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
もちろん、Eloquent を使用する場合、データベースからモデルを取得するだけではありません。新しいレコードを挿入する必要もあります。ありがたいことに、Eloquent を使用するとそれが簡単になります。新しいレコードをデータベースに挿入するには、新しいモデル インスタンスをインスタンス化し、モデルに属性を設定する必要があります。次に、モデル インスタンスで `save` メソッドを呼び出します。

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
この例では、受信 HTTP リクエストの `name` フィールドを、`App\Models\Flight` モデル インスタンスの `name` 属性に割り当てます。 `save` メソッドを呼び出すと、レコードがデータベースに挿入されます。モデルの `created_at` および `updated_at` タイムスタンプは、`save` メソッドが呼び出されるときに自動的に設定されるため、手動で設定する必要はありません。

<!-- Alternatively, you may use the `create` method to "save" a new model using a single PHP statement. The inserted model instance will be returned to you by the `create` method: -->
あるいは、`create` メソッドを使用して、単一の PHP ステートメントを使用して新しいモデルを「保存」することもできます。挿入されたモデル インスタンスは、`create` メソッドによって返されます。

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

<!-- However, before using the `create` method, you will need to specify either a `Fillable` or `Guarded` attribute on your model class. These attributes are required because all Eloquent models are protected against mass assignment vulnerabilities by default. To learn more about mass assignment, please consult the [mass assignment documentation](#mass-assignment). -->
ただし、`create` メソッドを使用する前に、モデル クラスで `Fillable` または `Guarded` 属性を指定する必要があります。すべての Eloquent モデルはデフォルトで一括割り当ての脆弱性から保護されているため、これらの属性が必要です。一括割り当ての詳細については、[mass assignment documentation](#mass-assignment) を参照してください。

<a name="updates"></a>
<!-- ### Updates -->
### Updates

<!-- The `save` method may also be used to update models that already exist in the database. To update a model, you should retrieve it and set any attributes you wish to update. Then, you should call the model's `save` method. Again, the `updated_at` timestamp will automatically be updated, so there is no need to manually set its value: -->
`save` メソッドは、データベースにすでに存在するモデルを更新するために使用することもできます。モデルを更新するには、モデルを取得し、更新する属性を設定する必要があります。次に、モデルの `save` メソッドを呼び出す必要があります。繰り返しますが、`updated_at` タイムスタンプは自動的に更新されるため、その値を手動で設定する必要はありません。

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

<!-- Occasionally, you may need to update an existing model or create a new model if no matching model exists. Like the `firstOrCreate` method, the `updateOrCreate` method persists the model, so there's no need to manually call the `save` method. -->
場合によっては、既存のモデルを更新するか、一致するモデルが存在しない場合は新しいモデルを作成することが必要になることがあります。 `firstOrCreate` メソッドと同様、`updateOrCreate` メソッドはモデルを保持するため、`save` メソッドを手動で呼び出す必要はありません。

<!-- In the example below, if a flight exists with a `departure` location of `Oakland` and a `destination` location of `San Diego`, its `price` and `discounted` columns will be updated. If no such flight exists, a new flight will be created which has the attributes resulting from merging the first argument array with the second argument array: -->
以下の例では、`Oakland` の `departure` 位置と `San Diego` の `destination` 位置を持つフライトが存在する場合、その `price` 列と `discounted` 列が更新されます。そのようなフライトが存在しない場合は、最初の引数の配列と 2 番目の引数の配列をマージした結果の属性を持つ新しいフライトが作成されます。

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

<!-- When using methods such as `firstOrCreate` or `updateOrCreate`, you may not know whether a new model has been created or an existing one has been updated. The `wasRecentlyCreated` property indicates if the model was created during its current lifecycle: -->
`firstOrCreate` や `updateOrCreate` などのメソッドを使用する場合、新しいモデルが作成されたのか、既存のモデルが更新されたのかがわからない場合があります。 `wasRecentlyCreated` プロパティは、モデルが現在のライフサイクル中に作成されたかどうかを示します。

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
特定のクエリに一致するモデルに対して更新を実行することもできます。この例では、`active` で、`destination` が `San Diego` であるすべてのフライトが遅延としてマークされます。

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

<!-- The `update` method expects an array of column and value pairs representing the columns that should be updated. The `update` method returns the number of affected rows. -->
`update` メソッドは、更新する必要がある列を表す列と値のペアの配列を予期します。 `update` メソッドは、影響を受ける行の数を返します。

> [!WARNING]
> Eloquent 経由で一括更新を発行する場合、更新されたモデルに対して `saving`、`saved`、`updating`、および `updated` モデル イベントは起動されません。これは、一括更新を発行するときにモデルが実際には取得されないためです。

<a name="examining-attribute-changes"></a>
<!-- #### Examining Attribute Changes -->
#### Examining Attribute Changes

<!-- Eloquent provides the `isDirty`, `isClean`, and `wasChanged` methods to examine the internal state of your model and determine how its attributes have changed from when the model was originally retrieved. -->
Eloquent は、モデルの内部状態を検査し、モデルが最初に取得されたときからその属性がどのように変化したかを判断するための、`isDirty`、`isClean`、および `wasChanged` メソッドを提供します。

<!-- The `isDirty` method determines if any of the model's attributes have been changed since the model was retrieved. You may pass a specific attribute name or an array of attributes to the `isDirty` method to determine if any of the attributes are "dirty". The `isClean` method will determine if an attribute has remained unchanged since the model was retrieved. This method also accepts an optional attribute argument: -->
`isDirty` メソッドは、モデルの取得後にモデルの属性のいずれかが変更されたかどうかを判断します。特定の属性名または属性の配列を `isDirty` メソッドに渡して、属性のいずれかが「ダーティ」であるかどうかを判断できます。 `isClean` メソッドは、モデルが取得されてから属性が変更されていないかを判断します。このメソッドはオプションの属性引数も受け入れます。

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
`wasChanged` メソッドは、現在のリクエスト サイクル内でモデルが最後に保存されたときに属性が変更されたかどうかを判断します。必要に応じて、属性名を渡して、特定の属性が変更されたかどうかを確認できます。

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
`getOriginal` メソッドは、取得後のモデルへの変更に関係なく、モデルの元の属性を含む配列を返します。必要に応じて、特定の属性名を渡して、特定の属性の元の値を取得できます。

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
`getChanges` メソッドは、モデルが最後に保存されたときに変更された属性を含む配列を返しますが、`getPrevious` メソッドは、モデルが最後に保存される前の元の属性値を含む配列を返します。

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
`create` メソッドを使用すると、単一の PHP ステートメントを使用して新しいモデルを「保存」できます。挿入されたモデル インスタンスは、次のメソッドによって返されます。

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

<!-- However, before using the `create` method, you will need to specify either a `Fillable` or `Guarded` attribute on your model class. These attributes are required because all Eloquent models are protected against mass assignment vulnerabilities by default. -->
ただし、`create` メソッドを使用する前に、モデル クラスで `Fillable` または `Guarded` 属性を指定する必要があります。すべての Eloquent モデルはデフォルトで一括割り当ての脆弱性から保護されているため、これらの属性が必要です。

<!-- A mass assignment vulnerability occurs when a user passes an unexpected HTTP request field and that field changes a column in your database that you did not expect. For example, a malicious user might send an `is_admin` parameter through an HTTP request, which is then passed to your model's `create` method, allowing the user to escalate themselves to an administrator. -->
一括割り当ての脆弱性は、ユーザーが予期しない HTTP リクエスト フィールドを渡し、そのフィールドがデータベース内の予期しない列を変更した場合に発生します。たとえば、悪意のあるユーザーが HTTP リクエストを通じて `is_admin` パラメーターを送信し、それがモデルの `create` メソッドに渡されることで、ユーザーが管理者にエスカレーションできるようになります。

<!-- So, to get started, you should define which model attributes you want to make mass assignable. You may do this using the `Fillable` attribute on the model. For example, let's make the `name` attribute of our `Flight` model mass assignable: -->
したがって、まず、どのモデル属性を一括割り当て可能にするかを定義する必要があります。これは、モデルの `Fillable` 属性を使用して行うことができます。たとえば、`Flight` モデルの `name` 属性を一括割り当て可能にしてみましょう。

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

<!-- Once you have specified which attributes are mass assignable, you may use the `create` method to insert a new record in the database. The `create` method returns the newly created model instance: -->
どの属性を一括割り当て可能にするかを指定したら、`create` メソッドを使用してデータベースに新しいレコードを挿入できます。 `create` メソッドは、新しく作成されたモデル インスタンスを返します。

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

<!-- If you already have a model instance, you may use the `fill` method to populate it with an array of attributes: -->
すでにモデル インスタンスがある場合は、`fill` メソッドを使用して属性の配列を設定できます。

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
<!-- #### Mass Assignment and JSON Columns -->
#### Mass Assignment and JSON Columns

<!-- When assigning JSON columns, each column's mass assignable key must be specified in your model's `Fillable` attribute. For security, Laravel does not support updating nested JSON attributes when using the `Guarded` attribute: -->
JSON 列を割り当てるときは、各列の一括割り当て可能キーをモデルの `Fillable` 属性で指定する必要があります。セキュリティのため、Laravel は、`Guarded` 属性を使用する場合のネストされた JSON 属性の更新をサポートしません。

```php
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['options->enabled'])]
class Flight extends Model
{
    // ...
}
```

<a name="allowing-mass-assignment"></a>
<!-- #### Allowing Mass Assignment -->
#### Allowing Mass Assignment

<!-- If you would like to make all of your attributes mass assignable, you may use the `Unguarded` attribute on your model. If you choose to unguard your model, you should take special care to always hand-craft the arrays passed to Eloquent's `fill`, `create`, and `update` methods: -->
すべての属性を一括割り当て可能にしたい場合は、モデルで `Unguarded` 属性を使用できます。モデルの保護を解除することを選択した場合は、Eloquent の `fill`、`create`、および `update` メソッドに渡される配列を常に手動で作成するように特別な注意を払う必要があります。

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
<!-- #### Mass Assignment Exceptions -->
#### Mass Assignment Exceptions

<!-- By default, attributes that are not included in the `Fillable` attribute are silently discarded when performing mass-assignment operations. In production, this is expected behavior; however, during local development it can lead to confusion as to why model changes are not taking effect. -->
デフォルトでは、`Fillable` 属性に含まれていない属性は、一括割り当て操作を実行するときに暗黙的に破棄されます。運用環境では、これは予期される動作です。ただし、ローカル開発中に、モデルの変更が反映されない理由について混乱が生じる可能性があります。

<!-- If you wish, you may instruct Laravel to throw an exception when attempting to fill an unfillable attribute by invoking the `preventSilentlyDiscardingAttributes` method. Typically, this method should be invoked in the `boot` method of your application's `AppServiceProvider` class: -->
必要に応じて、`preventSilentlyDiscardingAttributes` メソッドを呼び出して入力できない属性を入力しようとしたときに例外をスローするように Laravel に指示することもできます。通常、このメソッドは、アプリケーションの `AppServiceProvider` クラスの `boot` メソッドで呼び出す必要があります。

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
Eloquent の `upsert` メソッドを使用すると、単一のアトミック操作でレコードを更新または作成できます。メソッドの最初の引数は挿入または更新する値で構成され、2 番目の引数は関連するテーブル内のレコードを一意に識別する列をリストします。このメソッドの 3 番目と最後の引数は、一致するレコードがデータベースにすでに存在する場合に更新する必要がある列の配列です。モデルでタイムスタンプが有効になっている場合、`upsert` メソッドは、`created_at` および `updated_at` タイムスタンプを自動的に設定します。

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```

> [!WARNING]
> SQL Server を除くすべてのデータベースでは、`upsert` メソッドの 2 番目の引数の列に「プライマリ」または「一意」インデックスが必要です。さらに、MariaDB および MySQL データベース ドライバは、`upsert` メソッドの 2 番目の引数を無視し、常にテーブルの「プライマリ」インデックスと「一意」インデックスを使用して既存のレコードを検出します。

<a name="deleting-models"></a>
<!-- ## Deleting Models -->
## Deleting Models

<!-- To delete a model, you may call the `delete` method on the model instance: -->
モデルを削除するには、モデル インスタンスで `delete` メソッドを呼び出します。

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
<!-- #### Deleting an Existing Model by its Primary Key -->
#### Deleting an Existing Model by its Primary Key

<!-- In the example above, we are retrieving the model from the database before calling the `delete` method. However, if you know the primary key of the model, you may delete the model without explicitly retrieving it by calling the `destroy` method. In addition to accepting the single primary key, the `destroy` method will accept multiple primary keys, an array of primary keys, or a [collection](/docs/master/collections) of primary keys: -->
上の例では、`delete` メソッドを呼び出す前にデータベースからモデルを取得しています。ただし、モデルの主キーがわかっている場合は、`destroy` メソッドを呼び出して明示的に取得しなくても、モデルを削除できます。 `destroy` メソッドは、単一の主キーを受け入れることに加えて、複数の主キー、主キーの配列、または主キーの [collection](/docs/master/collections) を受け入れます。

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

<!-- If you are utilizing [soft deleting models](#soft-deleting), you may permanently delete models via the `forceDestroy` method: -->
[soft deleting models](#soft-deleting) を利用している場合は、`forceDestroy` メソッドを使用してモデルを完全に削除できます。

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` メソッドは、各モデルを個別にロードし、`delete` メソッドを呼び出して、`deleting` および `deleted` イベントがモデルごとに適切にディスパッチされるようにします。

<a name="deleting-models-using-queries"></a>
<!-- #### Deleting Models Using Queries -->
#### Deleting Models Using Queries

<!-- Of course, you may build an Eloquent query to delete all models matching your query's criteria. In this example, we will delete all flights that are marked as inactive. Like mass updates, mass deletes will not dispatch model events for the models that are deleted: -->
もちろん、Eloquent クエリを作成して、クエリの条件に一致するすべてのモデルを削除することもできます。この例では、非アクティブとしてマークされているすべてのフライトを削除します。一括更新と同様に、一括削除では、削除されたモデルのモデル イベントは送出されません。

```php
$deleted = Flight::where('active', 0)->delete();
```

<!-- To delete all models in a table, you should execute a query without adding any conditions: -->
テーブル内のすべてのモデルを削除するには、条件を追加せずにクエリを実行する必要があります。

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent 経由で一括削除ステートメントを実行する場合、削除されたモデルに対して `deleting` および `deleted` モデル イベントはディスパッチされません。これは、delete ステートメントの実行時にモデルが実際に取得されないためです。

<a name="soft-deleting"></a>
<!-- ### Soft Deleting -->
### Soft Deleting

<!-- In addition to actually removing records from your database, Eloquent can also "soft delete" models. When models are soft deleted, they are not actually removed from your database. Instead, a `deleted_at` attribute is set on the model indicating the date and time at which the model was "deleted". To enable soft deletes for a model, add the `Illuminate\Database\Eloquent\SoftDeletes` trait to the model: -->
実際にデータベースからレコードを削除するだけでなく、Eloquent はモデルを「論理的に削除」することもできます。モデルが論理的に削除されても、実際にはデータベースから削除されません。代わりに、モデルが「削除」された日時を示す `deleted_at` 属性がモデルに設定されます。モデルの論理的な削除を有効にするには、`Illuminate\Database\Eloquent\SoftDeletes` 特性をモデルに追加します。

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
> `SoftDeletes` トレイトは、`deleted_at` 属性を `DateTime` / `Carbon` インスタンスに自動的にcastします。

<!-- You should also add the `deleted_at` column to your database table. The Laravel [schema builder](/docs/master/migrations) contains a helper method to create this column: -->
`deleted_at` 列もデータベース テーブルに追加する必要があります。 Laravel [schema builder](/docs/master/migrations) には、この列を作成するためのヘルパ メソッドが含まれています。

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
ここで、モデルで `delete` メソッドを呼び出すと、`deleted_at` 列が現在の日付と時刻に設定されます。ただし、モデルのデータベース レコードはテーブルに残ります。論理的な削除を使用するモデルをクエリすると、論理的に削除されたモデルはすべてのクエリ結果から自動的に除外されます。

<!-- To determine if a given model instance has been soft deleted, you may use the `trashed` method: -->
特定のモデル インスタンスが論理的に削除されたかどうかを確認するには、`trashed` メソッドを使用できます。

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
<!-- #### Restoring Soft Deleted Models -->
#### Restoring Soft Deleted Models

<!-- Sometimes you may wish to "un-delete" a soft deleted model. To restore a soft deleted model, you may call the `restore` method on a model instance. The `restore` method will set the model's `deleted_at` column to `null`: -->
場合によっては、論理的に削除されたモデルの「削除を取り消し」たい場合があります。論理的に削除されたモデルを復元するには、モデル インスタンスで `restore` メソッドを呼び出すことができます。 `restore` メソッドは、モデルの `deleted_at` 列を `null` に設定します。

```php
$flight->restore();
```

<!-- You may also use the `restore` method in a query to restore multiple models. Again, like other "mass" operations, this will not dispatch any model events for the models that are restored: -->
クエリで `restore` メソッドを使用して、複数のモデルを復元することもできます。繰り返しますが、他の「一括」操作と同様に、これは復元されるモデルのモデル イベントをディスパッチしません。

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

<!-- The `restore` method may also be used when building [relationship](/docs/master/eloquent-relationships) queries: -->
`restore` メソッドは、[relationship](/docs/master/eloquent-relationships) クエリを構築するときにも使用できます。

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
<!-- #### Permanently Deleting Models -->
#### Permanently Deleting Models

<!-- Sometimes you may need to truly remove a model from your database. You may use the `forceDelete` method to permanently remove a soft deleted model from the database table: -->
場合によっては、データベースからモデルを完全に削除する必要がある場合があります。 `forceDelete` メソッドを使用して、論理的に削除されたモデルをデータベース テーブルから完全に削除できます。

```php
$flight->forceDelete();
```

<!-- You may also use the `forceDelete` method when building Eloquent relationship queries: -->
Eloquent リレーションシップ クエリを構築するときに、`forceDelete` メソッドを使用することもできます。

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
上で述べたように、論理的に削除されたモデルはクエリ結果から自動的に除外されます。ただし、クエリで `withTrashed` メソッドを呼び出すことで、論理的に削除されたモデルをクエリの結果に強制的に含めることができます。

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

<!-- The `withTrashed` method may also be called when building a [relationship](/docs/master/eloquent-relationships) query: -->
`withTrashed` メソッドは、[relationship](/docs/master/eloquent-relationships) クエリを構築するときに呼び出すこともできます。

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
<!-- #### Retrieving Only Soft Deleted Models -->
#### Retrieving Only Soft Deleted Models

<!-- The `onlyTrashed` method will retrieve **only** soft deleted models: -->
`onlyTrashed` メソッドは、**のみ** 論理的に削除されたモデルを取得します。

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
<!-- ## Pruning Models -->
## Pruning Models

<!-- Sometimes you may want to periodically delete models that are no longer needed. To accomplish this, you may add the `Illuminate\Database\Eloquent\Prunable` or `Illuminate\Database\Eloquent\MassPrunable` trait to the models you would like to periodically prune. After adding one of the traits to the model, implement a `prunable` method which returns an Eloquent query builder that resolves the models that are no longer needed: -->
不要になったモデルを定期的に削除したい場合があります。これを実現するには、定期的にプルーニングしたいモデルに `Illuminate\Database\Eloquent\Prunable` または `Illuminate\Database\Eloquent\MassPrunable` 特性を追加します。特性の 1 つをモデルに追加した後、不要になったモデルを解決する Eloquent クエリビルダを返す `prunable` メソッドを実装します。

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
モデルを `Prunable` としてマークする場合、モデルに `pruning` メソッドを定義することもできます。このメソッドは、モデルが削除される前に呼び出されます。このメソッドは、モデルがデータベースから完全に削除される前に、保存されたファイルなど、モデルに関連付けられた追加のリソースを削除する場合に役立ちます。

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
プルーナブル モデルを構成した後、アプリケーションの `routes/console.php` ファイルで `model:prune` Artisan コマンドをスケジュールする必要があります。このコマンドを実行する適切な間隔を自由に選択できます。

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

<!-- Behind the scenes, the `model:prune` command will automatically detect "Prunable" models within your application's `app/Models` directory. If your models are in a different location, you may use the `--model` option to specify the model class names: -->
バックグラウンドで、`model:prune` コマンドは、アプリケーションの `app/Models` ディレクトリ内の「Prunable」モデルを自動的に検出します。モデルが別の場所にある場合は、`--model` オプションを使用してモデル クラス名を指定できます。

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

<!-- If you wish to exclude certain models from being pruned while pruning all other detected models, you may use the `--except` option: -->
検出された他のすべてのモデルをプルーニングする一方で、特定のモデルをプルーニングから除外したい場合は、`--except` オプションを使用できます。

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

<!-- You may test your `prunable` query by executing the `model:prune` command with the `--pretend` option. When pretending, the `model:prune` command will simply report how many records would be pruned if the command were to actually run: -->
`--pretend` オプションを指定して `model:prune` コマンドを実行することで、`prunable` クエリをテストできます。このオプションを指定すると、`model:prune` コマンドは、コマンドが実際に実行された場合にプルーニングされるレコードの数を単純に報告します。

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 論理的な削除モデルは、プルーナブル クエリに一致する場合、完全に削除されます (`forceDelete`)。

<a name="mass-pruning"></a>
<!-- #### Mass Pruning -->
#### Mass Pruning

<!-- When models are marked with the `Illuminate\Database\Eloquent\MassPrunable` trait, models are deleted from the database using mass-deletion queries. Therefore, the `pruning` method will not be invoked, nor will the `deleting` and `deleted` model events be dispatched. This is because the models are never actually retrieved before deletion, thus making the pruning process much more efficient: -->
モデルが `Illuminate\Database\Eloquent\MassPrunable` 特性でマークされている場合、モデルは一括削除クエリを使用してデータベースから削除されます。したがって、`pruning` メソッドは呼び出されず、`deleting` および `deleted` モデル イベントも送出されません。これは、削除前にモデルが実際に取得されることがないため、プルーニング プロセスがはるかに効率的になるためです。

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
`replicate` メソッドを使用して、既存のモデル インスタンスの保存されていないコピーを作成できます。この方法は、同じ属性を多く共有するモデル インスタンスがある場合に特に便利です。

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
新しいモデルへのレプリケートから 1 つ以上の属性を除外するには、配列を `replicate` メソッドに渡すことができます。

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
グローバル スコープを使用すると、特定のモデルのすべてのクエリに制約を追加できます。 Laravel 独自の [soft delete](#soft-deleting) 機能は、グローバル スコープを利用して、データベースから「削除されていない」モデルのみを取得します。独自のグローバル スコープを作成すると、特定のモデルに対するすべてのクエリが特定の制約を受けるようにする便利で簡単な方法が提供されます。

<a name="generating-scopes"></a>
<!-- #### Generating Scopes -->
#### Generating Scopes

<!-- To generate a new global scope, you may invoke the `make:scope` Artisan command, which will place the generated scope in your application's `app/Models/Scopes` directory: -->
新しいグローバル スコープを生成するには、`make:scope` Artisan コマンドを呼び出します。これにより、生成されたスコープがアプリケーションの `app/Models/Scopes` ディレクトリに配置されます。

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
<!-- #### Writing Global Scopes -->
#### Writing Global Scopes

<!-- Writing a global scope is simple. First, use the `make:scope` command to generate a class that implements the `Illuminate\Database\Eloquent\Scope` interface. The `Scope` interface requires you to implement one method: `apply`. The `apply` method may add `where` constraints or other types of clauses to the query as needed: -->
グローバル スコープの記述は簡単です。まず、`make:scope` コマンドを使用して、`Illuminate\Database\Eloquent\Scope` インターフェイスを実装するクラスを生成します。 `Scope` インターフェイスでは、`apply` という 1 つのメソッドを実装する必要があります。 `apply` メソッドは、必要に応じて、`where` 制約または他のタイプの句をクエリに追加できます。

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
> グローバル スコープがクエリの select 句に列を追加している場合は、`select` の代わりに `addSelect` メソッドを使用する必要があります。これにより、クエリの既存の select 句が意図せず置換されるのを防ぎます。

<a name="applying-global-scopes"></a>
<!-- #### Applying Global Scopes -->
#### Applying Global Scopes

<!-- To assign a global scope to a model, you may simply place the `ScopedBy` attribute on the model: -->
モデルにグローバル スコープを割り当てるには、モデルに `ScopedBy` 属性を配置するだけです。

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
または、モデルの `booted` メソッドをオーバーライドしてグローバル スコープを手動で登録し、モデルの `addGlobalScope` メソッドを呼び出すこともできます。 `addGlobalScope` メソッドは、スコープのインスタンスを唯一の引数として受け入れます。

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
上の例のスコープを `App\Models\User` モデルに追加した後、`User::all()` メソッドの呼び出しによって次の SQL クエリが実行されます。

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
<!-- #### Anonymous Global Scopes -->
#### Anonymous Global Scopes

<!-- Eloquent also allows you to define global scopes using closures, which is particularly useful for simple scopes that do not warrant a separate class of their own. When defining a global scope using a closure, you should provide a scope name of your own choosing as the first argument to the `addGlobalScope` method: -->
Eloquent では、クロージャを使用してグローバル スコープを定義することもできます。これは、独自の別のクラスを保証しない単純なスコープに特に役立ちます。クロージャを使用してグローバル スコープを定義する場合は、`addGlobalScope` メソッドの最初の引数として独自に選択したスコープ名を指定する必要があります。

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
特定のクエリのグローバル スコープを削除したい場合は、`withoutGlobalScope` メソッドを使用できます。このメソッドは、グローバル スコープのクラス名を唯一の引数として受け入れます。

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

<!-- Or, if you defined the global scope using a closure, you should pass the string name that you assigned to the global scope: -->
または、クロージャを使用してグローバル スコープを定義した場合は、グローバル スコープに割り当てた文字列名を渡す必要があります。

```php
User::withoutGlobalScope('ancient')->get();
```

<!-- If you would like to remove several or even all of the query's global scopes, you may use the `withoutGlobalScopes` and `withoutGlobalScopesExcept` methods: -->
クエリのグローバル スコープの一部またはすべてを削除したい場合は、`withoutGlobalScopes` メソッドと `withoutGlobalScopesExcept` メソッドを使用できます。

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
ローカル スコープを使用すると、アプリケーション全体で簡単に再利用できるクエリ制約の共通セットを定義できます。たとえば、「人気がある」と考えられるすべてのユーザーを頻繁に取得する必要がある場合があります。スコープを定義するには、`Scope` 属性を Eloquent メソッドに追加します。

<!-- Scopes should always return the same query builder instance or `void`: -->
スコープは常に同じクエリビルダ インスタンスまたは `void` を返す必要があります。

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
スコープを定義したら、モデルをクエリするときにスコープ メソッドを呼び出すことができます。呼び出しをさまざまなスコープにチェーンすることもできます。

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

<!-- Combining multiple Eloquent model scopes via an `or` query operator may require the use of closures to achieve the correct [logical grouping](/docs/master/queries#logical-grouping): -->
`or` クエリ演算子を介して複数の Eloquent モデル スコープを結合するには、正しい [logical grouping](/docs/master/queries#logical-grouping) を実現するためにクロージャーの使用が必要になる場合があります。

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

<!-- However, since this can be cumbersome, Laravel provides a "higher order" `orWhere` method that allows you to fluently chain scopes together without the use of closures: -->
ただし、これは面倒になる可能性があるため、Laravel では、クロージャを使用せずにスコープをスムーズにチェーンできる「高次」の `orWhere` メソッドを提供しています。

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
<!-- #### Dynamic Scopes -->
#### Dynamic Scopes

<!-- Sometimes you may wish to define a scope that accepts parameters. To get started, just add your additional parameters to your scope method's signature. Scope parameters should be defined after the `$query` parameter: -->
パラメータを受け入れるスコープを定義したい場合があります。まず、追加のパラメーターをスコープ メソッドのシグネチャに追加するだけです。スコープ パラメーターは、`$query` パラメーターの後に定義する必要があります。

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
期待される引数がスコープ メソッドのシグネチャに追加されたら、スコープを呼び出すときに引数を渡すことができます。

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
<!-- ### Pending Attributes -->
### Pending Attributes

<!-- If you would like to use scopes to create models that have the same attributes as those used to constrain the scope, you may use the `withAttributes` method when building the scope query: -->
スコープを使用して、スコープの制約に使用したものと同じ属性を持つモデルを作成したい場合は、スコープ クエリを構築するときに `withAttributes` メソッドを使用できます。

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
`withAttributes` メソッドは、指定された属性を使用して `where` 条件をクエリに追加し、スコープを介して作成されたモデルにも指定された属性を追加します。

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

<!-- To instruct the `withAttributes` method to not add `where` conditions to the query, you may set the `asConditions` argument to `false`: -->
`withAttributes` メソッドに `where` 条件をクエリに追加しないように指示するには、`asConditions` 引数を `false` に設定します。

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
<!-- ## Comparing Models -->
## Comparing Models

<!-- Sometimes you may need to determine if two models are the "same" or not. The `is` and `isNot` methods may be used to quickly verify two models have the same primary key, table, and database connection or not: -->
場合によっては、2 つのモデルが「同じ」かどうかを判断する必要がある場合があります。 `is` メソッドと `isNot` メソッドを使用すると、2 つのモデルに同じ主キー、テーブル、データベース接続があるかどうかを迅速に検証できます。

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

<!-- The `is` and `isNot` methods are also available when using the `belongsTo`, `hasOne`, `morphTo`, and `morphOne` [relationships](/docs/master/eloquent-relationships). This method is particularly helpful when you would like to compare a related model without issuing a query to retrieve that model: -->
`is` および `isNot` メソッドは、`belongsTo`、`hasOne`、`morphTo`、および `morphOne` [relationships](/docs/master/eloquent-relationships) を使用する場合にも使用できます。この方法は、モデルを取得するためのクエリを発行せずに関連モデルを比較したい場合に特に役立ちます。

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
<!-- ## Events -->
## Events

> [!NOTE]
> Eloquent イベントをクライアント側アプリケーションに直接broadcastしたいですか? Laravel の [model event broadcasting](/docs/master/broadcasting#model-broadcasting) をチェックしてください。

<!-- Eloquent models dispatch several events, allowing you to hook into the following moments in a model's lifecycle: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, and `replicating`. -->
Eloquent モデルはいくつかのイベントをディスパッチし、モデルのライフサイクルの次の瞬間にフックできるようにします: `retrieved`、`creating`、`created`、`updating`、`updated`、`saving`、`saved`、`deleting`、 `deleted`、`trashed`、`forceDeleting`、`forceDeleted`、`restoring`、`restored`、および `replicating`。

<!-- The `retrieved` event will dispatch when an existing model is retrieved from the database. When a new model is saved for the first time, the `creating` and `created` events will dispatch. The `updating` / `updated` events will dispatch when an existing model is modified and the `save` method is called. The `saving` / `saved` events will dispatch when a model is created or updated - even if the model's attributes have not been changed. Event names ending with `-ing` are dispatched before any changes to the model are persisted, while events ending with `-ed` are dispatched after the changes to the model are persisted. -->
`retrieved` イベントは、既存のモデルがデータベースから取得されるときに送出されます。新しいモデルが初めて保存されると、`creating` および `created` イベントが送出されます。 `updating` / `updated` イベントは、既存のモデルが変更され、`save` メソッドが呼び出されたときに送出されます。 `saving` / `saved` イベントは、モデルの属性が変更されていない場合でも、モデルが作成または更新されるときに送出されます。 `-ing` で終わるイベント名はモデルへの変更が永続化される前に送出されますが、`-ed` で終わるイベントはモデルへの変更が永続化された後に送出されます。

<!-- To start listening to model events, define a `$dispatchesEvents` property on your Eloquent model. This property maps various points of the Eloquent model's lifecycle to your own [event classes](/docs/master/events). Each model event class should expect to receive an instance of the affected model via its constructor: -->
モデル イベントのリスニングを開始するには、Eloquent モデルで `$dispatchesEvents` プロパティを定義します。このプロパティは、Eloquent モデルのライフサイクルのさまざまなポイントを独自の [event classes](/docs/master/events) にマップします。各モデル イベント クラスは、コンストラクターを介して影響を受けるモデルのインスタンスを受け取ることを期待する必要があります。

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

<!-- After defining and mapping your Eloquent events, you may use [event listeners](/docs/master/events#defining-listeners) to handle the events. -->
Eloquent イベントを定義してマッピングした後、[event listeners](/docs/master/events#defining-listeners) を使用してイベントを処理できます。

> [!WARNING]
> Eloquent 経由で一括更新または削除クエリを発行すると、影響を受けるモデルに対して `saved`、`updated`、`deleting`、および `deleted` モデル イベントは送出されません。これは、一括更新または削除を実行するときにモデルが実際には取得されないためです。

<a name="events-using-closures"></a>
<!-- ### Using Closures -->
### Using Closures

<!-- Instead of using custom event classes, you may register closures that execute when various model events are dispatched. Typically, you should register these closures in the `booted` method of your model: -->
カスタム イベント クラスを使用する代わりに、さまざまなモデル イベントがディスパッチされたときに実行されるクロージャを登録できます。通常、これらのクロージャはモデルの `booted` メソッドに登録する必要があります。

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

<!-- If needed, you may utilize [queueable anonymous event listeners](/docs/master/events#queuable-anonymous-event-listeners) when registering model events. This will instruct Laravel to execute the model event listener in the background using your application's [queue](/docs/master/queues): -->
必要に応じて、モデル イベントを登録するときに [queueable anonymous event listeners](/docs/master/events#queuable-anonymous-event-listeners) を利用できます。これにより、アプリケーションの [queue](/docs/master/queues) を使用してバックグラウンドでモデル イベント リスナを実行するように Laravel に指示されます。

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
特定のモデルで多くのイベントをリッスンしている場合は、オブザーバを使用してすべてのリスナを 1 つのクラスにグループ化できます。 Observer クラスには、リッスンしたい Eloquent イベントを反映するメソッド名が付いています。これらの各メソッドは、影響を受けるモデルを唯一の引数として受け取ります。 `make:observer` Artisan コマンドは、新しいオブザーバ クラスを作成する最も簡単な方法です。

```shell
php artisan make:observer UserObserver --model=User
```

<!-- This command will place the new observer in your `app/Observers` directory. If this directory does not exist, Artisan will create it for you. Your fresh observer will look like the following: -->
このコマンドは、新しいオブザーバを `app/Observers` ディレクトリに配置します。このディレクトリが存在しない場合は、Artisan が作成します。新しいオブザーバは次のようになります。

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
オブザーバを登録するには、対応するモデルに `ObservedBy` 属性を配置します。

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
または、観察したいモデルで `observe` メソッドを呼び出して、オブザーバを手動で登録することもできます。アプリケーションの `AppServiceProvider` クラスの `boot` メソッドでオブザーバを登録できます。

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
> `saving` や `retrieved` など、オブザーバがリッスンできる追加のイベントがあります。これらのイベントについては、[events](#events) ドキュメント内で説明されています。

<a name="observers-and-database-transactions"></a>
<!-- #### Observers and Database Transactions -->
#### Observers and Database Transactions

<!-- When models are being created within a database transaction, you may want to instruct an observer to only execute its event handlers after the database transaction is committed. You may accomplish this by implementing the `ShouldHandleEventsAfterCommit` interface on your observer. If a database transaction is not in progress, the event handlers will execute immediately: -->
データベース トランザクション内でモデルが作成されている場合、データベース トランザクションがコミットされた後にのみイベント ハンドラーを実行するようにオブザーバに指示することができます。これは、オブザーバに `ShouldHandleEventsAfterCommit` インターフェイスを実装することで実現できます。データベース トランザクションが進行中でない場合、イベント ハンドラーはすぐに実行されます。

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
場合によっては、モデルによって起動されるすべてのイベントを一時的に「ミュート」する必要がある場合があります。これは、`withoutEvents` メソッドを使用して実現できます。 `withoutEvents` メソッドは、唯一の引数としてクロージャを受け入れます。このクロージャ内で実行されるコードはモデル イベントをディスパッチせず、クロージャによって返される値は `withoutEvents` メソッドによって返されます。

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
場合によっては、イベントを送出せずに特定のモデルを「保存」したい場合があります。これは、`saveQuietly` メソッドを使用して実行できます。

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

<!-- You may also "update", "delete", "soft delete", "restore", and "replicate" a given model without dispatching any events: -->
イベントを送出せずに、特定のモデルを「更新」、「削除」、「論理的な削除」、「復元」、「複製」することもできます。

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```

