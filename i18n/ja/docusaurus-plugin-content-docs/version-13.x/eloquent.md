# Eloquent: はじめに (Eloquent: Getting Started)

- [Introduction](#introduction)
- [モデルクラスの生成](#generating-model-classes)
- [Eloquent モデルの規約](#eloquent-model-conventions)
    - [テーブル名](#table-names)
    - [主キー](#primary-keys)
    - [UUID キーと ULID キー](#uuid-and-ulid-keys)
    - [Timestamps](#timestamps)
    - [データベース接続](#database-connections)
    - [デフォルトの属性値](#default-attribute-values)
    - [Eloquent 厳密性の構成](#configuring-eloquent-strictness)
- [モデルの取得](#retrieving-models)
    - [Collections](#collections)
    - [チャンク化の結果](#chunking-results)
    - [遅延コレクションを使用したチャンク](#chunking-using-lazy-collections)
    - [Cursors](#cursors)
    - [高度なサブクエリ](#advanced-subqueries)
- [単一モデル/集約の取得](#retrieving-single-models)
    - [モデルの取得または作成](#retrieving-or-creating-models)
    - [集計の取得](#retrieving-aggregates)
- [モデルの挿入と更新](#inserting-and-updating-models)
    - [Inserts](#inserts)
    - [Updates](#updates)
    - [一括割り当て](#mass-assignment)
    - [Upserts](#upserts)
- [モデルの削除](#deleting-models)
    - [ソフト削除](#soft-deleting)
    - [論理的に削除されたモデルのクエリ](#querying-soft-deleted-models)
- [モデルの枝刈り](#pruning-models)
- [モデルの複製](#replicating-models)
- [クエリのスコープ](#query-scopes)
    - [グローバルスコープ](#global-scopes)
    - [ローカルスコープ](#local-scopes)
    - [保留中の属性](#pending-attributes)
- [モデルの比較](#comparing-models)
- [Events](#events)
    - [クロージャの使用](#events-using-closures)
    - [Observers](#observers)
    - [イベントのミュート](#muting-events)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel には、データベースとの対話を楽しくするオブジェクト リレーショナル マッパー (ORM) である Eloquent が含まれています。 Eloquent を使用する場合、各データベース テーブルには、そのテーブルと対話するために使用される対応する「モデル」があります。 Eloquent モデルでは、データベース テーブルからレコードを取得するだけでなく、テーブルからレコードを挿入、更新、削除することもできます。

> [!NOTE]
> 開始する前に、必ずアプリケーションの `config/database.php` 構成ファイルでデータベース接続を構成してください。データベースの構成の詳細については、[データベース構成ドキュメント](/docs/{{version}}/database#configuration) を確認してください。

<a name="generating-model-classes"></a>
## モデルクラスの生成 (Generating Model Classes)

まず、Eloquent モデルを作成しましょう。モデルは通常、`app\Models` ディレクトリに存在し、`Illuminate\Database\Eloquent\Model` クラスを拡張します。 `make:model` [Artisan コマンド](/docs/{{version}}/artisan) を使用して新しいモデルを生成できます。

```shell
php artisan make:model Flight
```

モデルの生成時に [データベースの移行](/docs/{{version}}/migrations) を生成したい場合は、`--migration` または `-m` オプションを使用できます。

```shell
php artisan make:model Flight --migration
```

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
#### モデルの検査

コードをざっと読んだだけでは、モデルで使用可能な属性と関係をすべて判断するのが難しい場合があります。代わりに、`model:show` Artisan コマンドを試してください。このコマンドは、すべてのモデルの属性と関係の便利な概要を提供します。

```shell
php artisan model:show Flight
```

<a name="eloquent-model-conventions"></a>
## Eloquent モデルの規約 (Eloquent Model Conventions)

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
### テーブル名

上記の例を見た後、どのデータベース テーブルが `Flight` モデルに対応するかを Eloquent に伝えていないことに気付いたかもしれません。慣例により、別の名前が明示的に指定されない限り、「スネークケース」クラスの複数名がテーブル名として使用されます。したがって、この場合、Eloquent は、`Flight` モデルが `flights` テーブルにレコードを保存するのに対し、`AirTrafficController` モデルは `air_traffic_controllers` テーブルにレコードを保存すると想定します。

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
### 主キー

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

さらに、Eloquent は主キーが増加する整数値であると想定します。これは、Eloquent が主キーを自動的に整数にキャストすることを意味します。非インクリメントまたは非数値の主キーを使用したい場合は、`Table` 属性で `keyType` および `incrementing` 引数を指定する必要があります。

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

自動インクリメント ID のみを無効にする必要がある場合は、`WithoutIncrementing` 属性を使用できます。

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
#### 「複合」主キー

Eloquent では、各モデルに主キーとして機能する一意に識別できる「ID」を少なくとも 1 つ持つ必要があります。 「複合」主キーは Eloquent モデルではサポートされていません。ただし、テーブルを一意に識別する主キーに加えて、複数列の一意のインデックスをデータベース テーブルに自由に追加できます。

<a name="uuid-and-ulid-keys"></a>
### UUID キーと ULID キー

Eloquent モデルの主キーとして自動インクリメント整数を使用する代わりに、UUID を使用することを選択することもできます。 UUID は、36 文字の長さの普遍的に一意の英数字の識別子です。

モデルで自動インクリメント整数キーの代わりに UUID キーを使用したい場合は、モデルで `Illuminate\Database\Eloquent\Concerns\HasUuids` トレイトを使用できます。もちろん、モデルに [UUID に相当する主キー列](/docs/{{version}}/migrations#column-method-uuid) があることを確認する必要があります。

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

デフォルトでは、`HasUuids` 特性によりモデルの [UUIDv7](/docs/{{version}}/strings#method-str-uuid7) 識別子が生成されます。これらの UUID は辞書順に並べ替えることができるため、インデックス付きデータベース ストレージにとってより効率的です。

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

必要に応じて、UUID の代わりに「ULID」を使用することを選択できます。 ULID は UUID に似ています。ただし、長さはわずか 26 文字です。順序付けされた UUID と同様に、ULID は辞書編集的にソート可能であり、効率的なデータベースのインデックス作成が可能です。 ULID を利用するには、モデルで `Illuminate\Database\Eloquent\Concerns\HasUlids` トレイトを使用する必要があります。モデルに [ULID に相当する主キー列](/docs/{{version}}/migrations#column-method-ulid) があることも確認する必要があります。

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
### タイムスタンプ

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

タイムスタンプを無効にする必要があるだけの場合は、`WithoutTimestamps` 属性を使用できます。

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

日付形式を定義するだけの場合は、`DateFormat` 属性を使用できます。

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

モデルの `updated_at` タイムスタンプを変更せずにモデル操作を実行したい場合は、`withoutTimestamps` メソッドに指定されたクロージャ内でモデルを操作できます。

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```

<a name="database-connections"></a>
### データベース接続

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
### デフォルトの属性値

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
     * @var array<string, mixed>
     */
    protected $attributes = [
        'options' => '[]',
        'delayed' => false,
    ];
}
```

<a name="configuring-eloquent-strictness"></a>
### Eloquent 厳密性の構成

Laravel は、さまざまな状況で Eloquent の動作と「厳密さ」を設定できるいくつかのメソッドを提供します。

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

また、`preventSilentlyDiscardingAttributes` メソッドを呼び出して、入力できない属性を入力しようとしたときに例外をスローするように Laravel に指示することもできます。これは、ローカル開発中にモデルの `fillable` 配列に追加されていない属性を設定しようとしたときの予期しないエラーを防ぐのに役立ちます。

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```

<a name="retrieving-models"></a>
## モデルの取得 (Retrieving Models)

モデルと [関連するデータベーステーブル](/docs/{{version}}/migrations#generating-migrations) を作成したら、データベースからのデータの取得を開始する準備が整います。各 Eloquent モデルは、モデルに関連付けられたデータベース テーブルにスムーズにクエリを実行できる強力な [クエリビルダ](/docs/{{version}}/queries) と考えることができます。モデルの `all` メソッドは、モデルに関連付けられたデータベース テーブルからすべてのレコードを取得します。

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```

<a name="building-queries"></a>
#### クエリの構築

Eloquent `all` メソッドは、モデルのテーブル内のすべての結果を返します。ただし、各 Eloquent モデルは [クエリビルダ](/docs/{{version}}/queries) として機能するため、クエリに追加の制約を追加してから、`get` メソッドを呼び出して結果を取得することができます。

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```

> [!NOTE]
> Eloquent モデルはクエリビルダであるため、Laravel の [クエリビルダ](/docs/{{version}}/queries) によって提供されるすべてのメソッドを確認する必要があります。 Eloquent クエリを作成するときは、これらのメソッドのいずれかを使用できます。

<a name="refreshing-models"></a>
#### モデルの更新

データベースから取得した Eloquent モデルのインスタンスがすでにある場合は、`fresh` メソッドと `refresh` メソッドを使用してモデルを「更新」できます。 `fresh` メソッドはデータベースからモデルを再取得します。既存のモデル インスタンスは影響を受けません。

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```

`refresh` メソッドは、データベースからの新しいデータを使用して既存のモデルを再ハイドレートします。さらに、読み込まれた関係もすべて更新されます。

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```

<a name="collections"></a>
### コレクション

これまで見てきたように、`all` や `get` などの Eloquent メソッドはデータベースから複数のレコードを取得します。ただし、これらのメソッドはプレーンな PHP 配列を返しません。代わりに、`Illuminate\Database\Eloquent\Collection` のインスタンスが返されます。

Eloquent `Collection` クラスは、Laravel の基本 `Illuminate\Support\Collection` クラスを拡張し、データ コレクションと対話するための [さまざまな役立つ方法](/docs/{{version}}/collections#available-methods) を提供します。たとえば、`reject` メソッドは、呼び出されたクロージャの結果に基づいてコレクションからモデルを削除するために使用できます。

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```

Laravel の基本コレクション クラスによって提供されるメソッドに加えて、Eloquent コレクション クラスは、特に Eloquent モデルのコレクションと対話することを目的とした [いくつかの追加のメソッド](/docs/{{version}}/eloquent-collections#available-methods) を提供します。

Laravel のコレクションはすべて PHP の反復可能なインターフェイスを実装しているため、コレクションを配列であるかのようにループできます。

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```

<a name="chunking-results"></a>
### チャンク化の結果

`all` メソッドまたは `get` メソッドを介して数万の Eloquent レコードをロードしようとすると、アプリケーションがメモリ不足になる可能性があります。これらのメソッドを使用する代わりに、`chunk` メソッドを使用して、多数のモデルをより効率的に処理できます。

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

`chunk` メソッドに渡される最初の引数は、「チャンク」ごとに受信するレコードの数です。 2 番目の引数として渡されたクロージャは、データベースから取得されるチャンクごとに呼び出されます。データベース クエリが実行され、クロージャに渡されたレコードの各チャンクが取得されます。

結果の反復処理中に更新も行う列に基づいて `chunk` メソッドの結果をフィルター処理する場合は、`chunkById` メソッドを使用する必要があります。これらのシナリオで `chunk` メソッドを使用すると、予期しない一貫性のない結果が生じる可能性があります。内部的には、`chunkById` メソッドは常に、前のチャンクの最後のモデルより大きい `id` 列を持つモデルを取得します。

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```

`chunkById` メソッドと `lazyById` メソッドは、実行されるクエリに独自の「where」条件を追加するため、通常はクロージャ内で独自の条件を [論理的にグループ化する](/docs/{{version}}/queries#logical-grouping) する必要があります。

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
### 遅延コレクションを使用したチャンク化

`lazy` メソッドは、バックグラウンドでクエリをチャンク単位で実行するという意味で、[`chunk` メソッド](#chunking-results) と同様に機能します。ただし、各チャンクをそのままコールバックに直接渡す代わりに、`lazy` メソッドは Eloquent モデルのフラット化された [LazyCollection](/docs/{{version}}/collections#lazy-collections) を返します。これにより、結果を単一のストリームとして操作できます。

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```

結果の反復処理中に更新も行う列に基づいて `lazy` メソッドの結果をフィルター処理する場合は、`lazyById` メソッドを使用する必要があります。内部的には、`lazyById` メソッドは常に、前のチャンクの最後のモデルより大きい `id` 列を持つモデルを取得します。

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```

`lazyByIdDesc` メソッドを使用して、`id` の降順に基づいて結果をフィルタリングできます。

<a name="cursors"></a>
### カーソル

`lazy` メソッドと同様に、`cursor` メソッドを使用すると、数万の Eloquent モデル レコードを反復処理するときにアプリケーションのメモリ消費を大幅に削減できます。

`cursor` メソッドは、単一のデータベース クエリのみを実行します。ただし、個々の Eloquent モデルは、実際に反復されるまでハイドレートされません。したがって、カーソル上で反復している間、常に 1 つの Eloquent モデルだけがメモリに保持されます。

> [!WARNING]
> `cursor` メソッドは、メモリ内に一度に 1 つの Eloquent モデルしか保持しないため、関係を一括ロードすることはできません。関係を一括ロードする必要がある場合は、代わりに [`lazy` メソッド](#chunking-using-lazy-collections) の使用を検討してください。

内部的には、`cursor` メソッドは PHP [generators](https://www.php.net/manual/en/language.generators.overview.php) を使用してこの機能を実装します。

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```

`cursor` は、`Illuminate\Support\LazyCollection` インスタンスを返します。 [レイジーコレクション](/docs/{{version}}/collections#lazy-collections) を使用すると、一度に 1 つのモデルのみをメモリにロードしながら、一般的な Laravel コレクションで利用可能な多くのコレクション メソッドを使用できます。

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```

`cursor` メソッドは、通常のクエリよりもはるかに少ないメモリを使用しますが (一度に 1 つの Eloquent モデルのみをメモリに保持するため)、それでも最終的にはメモリが不足します。 [PHP の PDO ドライバが内部ですべての生のクエリ結果をバッファーにキャッシュしているためです。](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php)です。非常に多くの Eloquent レコードを扱っている場合は、代わりに [`lazy` メソッド](#chunking-using-lazy-collections) の使用を検討してください。

<a name="advanced-subqueries"></a>
### 高度なサブクエリ

<a name="subquery-selects"></a>
#### サブクエリ選択

Eloquent は、高度なサブクエリ サポートも提供しており、これにより、単一のクエリで関連テーブルから情報を取得できます。たとえば、目的地へのフライト `destinations` のテーブルと `flights` のテーブルがあると想像してみましょう。 `flights` テーブルには、フライトが目的地にいつ到着したかを示す `arrived_at` 列が含まれています。

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
#### サブクエリの順序付け

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
## 単一モデル/集約の取得 (Retrieving Single Models / Aggregates)

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
#### 例外が見つかりませんでした

モデルが見つからない場合に例外をスローしたい場合があります。これは、ルートまたはコントローラで特に便利です。 `findOrFail` メソッドと `firstOrFail` メソッドは、クエリの最初の結果を取得します。ただし、結果が見つからない場合は、`Illuminate\Database\Eloquent\ModelNotFoundException` がスローされます。

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```

`ModelNotFoundException` が捕捉されない場合、404 HTTP 応答が自動的にクライアントに返されます。

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```

<a name="retrieving-or-creating-models"></a>
### モデルの取得または作成

`firstOrCreate` メソッドは、指定された列と値のペアを使用してデータベース レコードの検索を試みます。データベース内でモデルが見つからない場合は、最初の配列引数とオプションの 2 番目の配列引数をマージした結果の属性を持つレコードが挿入されます。

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
### 集計の取得

Eloquent モデルを操作するときは、Laravel [クエリビルダ](/docs/{{version}}/queries#aggregates) によって提供される `count`、`sum`、`max`、およびその他の [集約メソッド](/docs/{{version}}/queries) を使用することもできます。ご想像のとおり、これらのメソッドは Eloquent モデル インスタンスの代わりにスカラー値を返します。

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```

<a name="inserting-and-updating-models"></a>
## モデルの挿入と更新 (Inserting and Updating Models)

<a name="inserts"></a>
### インサート

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

この例では、受信 HTTP リクエストの `name` フィールドを、`App\Models\Flight` モデル インスタンスの `name` 属性に割り当てます。 `save` メソッドを呼び出すと、レコードがデータベースに挿入されます。モデルの `created_at` および `updated_at` タイムスタンプは、`save` メソッドが呼び出されるときに自動的に設定されるため、手動で設定する必要はありません。

データベース トランザクション内でモデルを保存したい場合は、`saveOrFail` メソッドを使用できます。保存中に例外がスローされた場合、トランザクションは自動的にロールバックされます。

```php
$flight->saveOrFail();
```

あるいは、`create` メソッドを使用して、単一の PHP ステートメントを使用して新しいモデルを「保存」することもできます。挿入されたモデル インスタンスは、`create` メソッドによって返されます。

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

ただし、`create` メソッドを使用する前に、モデル クラスで `Fillable` または `Guarded` 属性を指定する必要があります。すべての Eloquent モデルはデフォルトで一括割り当ての脆弱性から保護されているため、これらの属性が必要です。一括割り当ての詳細については、[一括割り当てのドキュメント](#mass-assignment) を参照してください。

<a name="updates"></a>
### アップデート

`save` メソッドは、データベースにすでに存在するモデルを更新するために使用することもできます。モデルを更新するには、モデルを取得し、更新する属性を設定する必要があります。次に、モデルの `save` メソッドを呼び出す必要があります。繰り返しますが、`updated_at` タイムスタンプは自動的に更新されるため、その値を手動で設定する必要はありません。

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```

データベース トランザクション内でモデルを更新したい場合は、`updateOrFail` メソッドを使用できます。更新中に例外がスローされた場合、トランザクションは自動的にロールバックされます。

```php
$flight->updateOrFail(['name' => 'Paris to London']);
```

場合によっては、既存のモデルを更新するか、一致するモデルが存在しない場合は新しいモデルを作成することが必要になることがあります。 `firstOrCreate` メソッドと同様、`updateOrCreate` メソッドはモデルを保持するため、`save` メソッドを手動で呼び出す必要はありません。

以下の例では、`Oakland` の `departure` 位置と `San Diego` の `destination` 位置を持つフライトが存在する場合、その `price` 列と `discounted` 列が更新されます。そのようなフライトが存在しない場合は、最初の引数の配列と 2 番目の引数の配列をマージした結果の属性を持つ新しいフライトが作成されます。

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```

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
#### 一括アップデート

特定のクエリに一致するモデルに対して更新を実行することもできます。この例では、`active` で、`destination` が `San Diego` であるすべてのフライトが遅延としてマークされます。

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```

`update` メソッドは、更新する必要がある列を表す列と値のペアの配列を予期します。 `update` メソッドは、影響を受ける行の数を返します。

> [!WARNING]
> Eloquent 経由で一括更新を発行する場合、更新されたモデルに対して `saving`、`saved`、`updating`、および `updated` モデル イベントは起動されません。これは、一括更新を発行するときにモデルが実際には取得されないためです。

<a name="examining-attribute-changes"></a>
#### 属性変更の検査

Eloquent は、モデルの内部状態を検査し、モデルが最初に取得されたときからその属性がどのように変化したかを判断するための、`isDirty`、`isClean`、および `wasChanged` メソッドを提供します。

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
### 一括割り当て

`create` メソッドを使用すると、単一の PHP ステートメントを使用して新しいモデルを「保存」できます。挿入されたモデル インスタンスは、次のメソッドによって返されます。

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```

ただし、`create` メソッドを使用する前に、モデル クラスで `Fillable` または `Guarded` 属性を指定する必要があります。すべての Eloquent モデルはデフォルトで一括割り当ての脆弱性から保護されているため、これらの属性が必要です。

一括割り当ての脆弱性は、ユーザーが予期しない HTTP リクエスト フィールドを渡し、そのフィールドがデータベース内の予期しない列を変更した場合に発生します。たとえば、悪意のあるユーザーが HTTP リクエストを通じて `is_admin` パラメーターを送信し、それがモデルの `create` メソッドに渡されることで、ユーザーが管理者にエスカレーションできるようになります。

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

どの属性を一括割り当て可能にするかを指定したら、`create` メソッドを使用してデータベースに新しいレコードを挿入できます。 `create` メソッドは、新しく作成されたモデル インスタンスを返します。

```php
$flight = Flight::create(['name' => 'London to Paris']);
```

すでにモデル インスタンスがある場合は、`fill` メソッドを使用して属性の配列を設定できます。

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```

<a name="mass-assignment-json-columns"></a>
#### 一括割り当てと JSON 列

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
#### 一括割り当ての許可

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
#### 一括割り当ての例外

デフォルトでは、`Fillable` 属性に含まれていない属性は、一括割り当て操作を実行するときに暗黙的に破棄されます。運用環境では、これは予期される動作です。ただし、ローカル開発中に、モデルの変更が反映されない理由について混乱が生じる可能性があります。

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
### アップサート

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
## モデルの削除 (Deleting Models)

モデルを削除するには、モデル インスタンスで `delete` メソッドを呼び出します。

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```

データベース トランザクション内でモデルを削除したい場合は、`deleteOrFail` メソッドを使用できます。削除中に例外がスローされた場合、トランザクションは自動的にロールバックされます。

```php
$flight->deleteOrFail();
```

<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 主キーによる既存のモデルの削除

上の例では、`delete` メソッドを呼び出す前にデータベースからモデルを取得しています。ただし、モデルの主キーがわかっている場合は、`destroy` メソッドを呼び出して明示的に取得しなくても、モデルを削除できます。 `destroy` メソッドは、単一の主キーを受け入れることに加えて、複数の主キー、主キーの配列、または主キーの [collection](/docs/{{version}}/collections) を受け入れます。

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```

[ソフト削除モデル](#soft-deleting) を利用している場合は、`forceDestroy` メソッドを使用してモデルを完全に削除できます。

```php
Flight::forceDestroy(1);
```

> [!WARNING]
> `destroy` メソッドは、各モデルを個別にロードし、`delete` メソッドを呼び出して、`deleting` および `deleted` イベントがモデルごとに適切にディスパッチされるようにします。

<a name="deleting-models-using-queries"></a>
#### クエリを使用したモデルの削除

もちろん、Eloquent クエリを作成して、クエリの条件に一致するすべてのモデルを削除することもできます。この例では、非アクティブとしてマークされているすべてのフライトを削除します。一括更新と同様に、一括削除では、削除されたモデルのモデル イベントは送出されません。

```php
$deleted = Flight::where('active', 0)->delete();
```

テーブル内のすべてのモデルを削除するには、条件を追加せずにクエリを実行する必要があります。

```php
$deleted = Flight::query()->delete();
```

> [!WARNING]
> Eloquent 経由で一括削除ステートメントを実行する場合、削除されたモデルに対して `deleting` および `deleted` モデル イベントはディスパッチされません。これは、delete ステートメントの実行時にモデルが実際に取得されないためです。

<a name="soft-deleting"></a>
### ソフト削除

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
> `SoftDeletes` トレイトは、`deleted_at` 属性を `DateTime` / `Carbon` インスタンスに自動的にキャストします。

`deleted_at` 列もデータベース テーブルに追加する必要があります。 Laravel [スキーマビルダ](/docs/{{version}}/migrations) には、この列を作成するためのヘルパ メソッドが含まれています。

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

ここで、モデルで `delete` メソッドを呼び出すと、`deleted_at` 列が現在の日付と時刻に設定されます。ただし、モデルのデータベース レコードはテーブルに残ります。論理的な削除を使用するモデルをクエリすると、論理的に削除されたモデルはすべてのクエリ結果から自動的に除外されます。

特定のモデル インスタンスが論理的に削除されたかどうかを確認するには、`trashed` メソッドを使用できます。

```php
if ($flight->trashed()) {
    // ...
}
```

<a name="restoring-soft-deleted-models"></a>
#### 論理的に削除されたモデルの復元

場合によっては、論理的に削除されたモデルの「削除を取り消し」たい場合があります。論理的に削除されたモデルを復元するには、モデル インスタンスで `restore` メソッドを呼び出すことができます。 `restore` メソッドは、モデルの `deleted_at` 列を `null` に設定します。

```php
$flight->restore();
```

クエリで `restore` メソッドを使用して、複数のモデルを復元することもできます。繰り返しますが、他の「一括」操作と同様に、これは復元されるモデルのモデル イベントをディスパッチしません。

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```

`restore` メソッドは、[relationship](/docs/{{version}}/eloquent-relationships) クエリを構築するときにも使用できます。

```php
$flight->history()->restore();
```

<a name="permanently-deleting-models"></a>
#### モデルを完全に削除する

場合によっては、データベースからモデルを完全に削除する必要がある場合があります。 `forceDelete` メソッドを使用して、論理的に削除されたモデルをデータベース テーブルから完全に削除できます。

```php
$flight->forceDelete();
```

Eloquent リレーションシップ クエリを構築するときに、`forceDelete` メソッドを使用することもできます。

```php
$flight->history()->forceDelete();
```

<a name="querying-soft-deleted-models"></a>
### 論理的に削除されたモデルのクエリ

<a name="including-soft-deleted-models"></a>
#### ソフト削除されたモデルを含む

上で述べたように、論理的に削除されたモデルはクエリ結果から自動的に除外されます。ただし、クエリで `withTrashed` メソッドを呼び出すことで、論理的に削除されたモデルをクエリの結果に強制的に含めることができます。

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```

`withTrashed` メソッドは、[relationship](/docs/{{version}}/eloquent-relationships) クエリを構築するときに呼び出すこともできます。

```php
$flight->history()->withTrashed()->get();
```

<a name="retrieving-only-soft-deleted-models"></a>
#### 論理的に削除されたモデルのみを取得する

`onlyTrashed` メソッドは、**のみ** 論理的に削除されたモデルを取得します。

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```

<a name="pruning-models"></a>
## モデルの枝刈り (Pruning Models)

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

プルーナブル モデルを構成した後、アプリケーションの `routes/console.php` ファイルで `model:prune` Artisan コマンドをスケジュールする必要があります。このコマンドを実行する適切な間隔を自由に選択できます。

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```

バックグラウンドで、`model:prune` コマンドは、アプリケーションの `app/Models` ディレクトリ内の「Prunable」モデルを自動的に検出します。モデルが別の場所にある場合は、`--model` オプションを使用してモデル クラス名を指定できます。

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```

検出された他のすべてのモデルをプルーニングする一方で、特定のモデルをプルーニングから除外したい場合は、`--except` オプションを使用できます。

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```

`--pretend` オプションを指定して `model:prune` コマンドを実行することで、`prunable` クエリをテストできます。ふりをするとき、`model:prune` コマンドは、コマンドが実際に実行された場合にプルーニングされるレコードの数を単純に報告します。

```shell
php artisan model:prune --pretend
```

> [!WARNING]
> 論理的な削除モデルは、プルーナブル クエリに一致する場合、完全に削除されます (`forceDelete`)。

<a name="mass-pruning"></a>
#### 大量剪定

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
## モデルの複製 (Replicating Models)

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
## クエリのスコープ (Query Scopes)

<a name="global-scopes"></a>
### グローバルスコープ

グローバル スコープを使用すると、特定のモデルのすべてのクエリに制約を追加できます。 Laravel 独自の [ソフトデリート](#soft-deleting) 機能は、グローバル スコープを利用して、データベースから「削除されていない」モデルのみを取得します。独自のグローバル スコープを作成すると、特定のモデルに対するすべてのクエリが特定の制約を受けるようにする便利で簡単な方法が提供されます。

<a name="generating-scopes"></a>
#### スコープの生成

新しいグローバル スコープを生成するには、`make:scope` Artisan コマンドを呼び出します。これにより、生成されたスコープがアプリケーションの `app/Models/Scopes` ディレクトリに配置されます。

```shell
php artisan make:scope AncientScope
```

<a name="writing-global-scopes"></a>
#### グローバル スコープの作成

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
#### グローバル スコープの適用

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

上の例のスコープを `App\Models\User` モデルに追加した後、`User::all()` メソッドの呼び出しによって次の SQL クエリが実行されます。

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```

<a name="anonymous-global-scopes"></a>
#### 匿名グローバルスコープ

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
#### グローバル スコープの削除

特定のクエリのグローバル スコープを削除したい場合は、`withoutGlobalScope` メソッドを使用できます。このメソッドは、グローバル スコープのクラス名を唯一の引数として受け入れます。

```php
User::withoutGlobalScope(AncientScope::class)->get();
```

または、クロージャを使用してグローバル スコープを定義した場合は、グローバル スコープに割り当てた文字列名を渡す必要があります。

```php
User::withoutGlobalScope('ancient')->get();
```

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
### ローカルスコープ

ローカル スコープを使用すると、アプリケーション全体で簡単に再利用できるクエリ制約の共通セットを定義できます。たとえば、「人気がある」と考えられるすべてのユーザーを頻繁に取得する必要がある場合があります。スコープを定義するには、`Scope` 属性を Eloquent メソッドに追加します。

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
#### ローカルスコープの利用

スコープを定義したら、モデルをクエリするときにスコープ メソッドを呼び出すことができます。呼び出しをさまざまなスコープにチェーンすることもできます。

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```

`or` クエリ演算子を介して複数の Eloquent モデル スコープを結合するには、正しい [論理グループ化](/docs/{{version}}/queries#logical-grouping) を実現するためにクロージャーの使用が必要になる場合があります。

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```

ただし、これは面倒になる可能性があるため、Laravel では、クロージャを使用せずにスコープをスムーズにチェーンできる「高次」の `orWhere` メソッドを提供しています。

```php
$users = User::popular()->orWhere->active()->get();
```

<a name="dynamic-scopes"></a>
#### ダイナミックスコープ

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

期待される引数がスコープ メソッドのシグネチャに追加されたら、スコープを呼び出すときに引数を渡すことができます。

```php
$users = User::ofType('admin')->get();
```

<a name="pending-attributes"></a>
### 保留中の属性

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

`withAttributes` メソッドは、指定された属性を使用して `where` 条件をクエリに追加し、スコープを介して作成されたモデルにも指定された属性を追加します。

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```

`withAttributes` メソッドに `where` 条件をクエリに追加しないように指示するには、`asConditions` 引数を `false` に設定します。

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```

<a name="comparing-models"></a>
## モデルの比較 (Comparing Models)

場合によっては、2 つのモデルが「同じ」かどうかを判断する必要がある場合があります。 `is` メソッドと `isNot` メソッドを使用すると、2 つのモデルに同じ主キー、テーブル、データベース接続があるかどうかを迅速に検証できます。

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```

`is` および `isNot` メソッドは、`belongsTo`、`hasOne`、`morphTo`、および `morphOne` [relationships](/docs/{{version}}/eloquent-relationships) を使用する場合にも使用できます。この方法は、モデルを取得するためのクエリを発行せずに関連モデルを比較したい場合に特に役立ちます。

```php
if ($post->author()->is($user)) {
    // ...
}
```

<a name="events"></a>
## イベント (Events)

> [!NOTE]
> Eloquent イベントをクライアント側アプリケーションに直接ブロードキャストしたいですか? Laravel の [モデルイベント放送](/docs/{{version}}/broadcasting#model-broadcasting) をチェックしてください。

Eloquent モデルはいくつかのイベントをディスパッチし、モデルのライフサイクルの次の瞬間にフックできるようにします: `retrieved`、`creating`、`created`、`updating`、`updated`、`saving`、`saved`、`deleting`、 `deleted`、`trashed`、`forceDeleting`、`forceDeleted`、`restoring`、`restored`、および `replicating`。

`retrieved` イベントは、既存のモデルがデータベースから取得されるときに送出されます。新しいモデルが初めて保存されると、`creating` および `created` イベントが送出されます。 `updating` / `updated` イベントは、既存のモデルが変更され、`save` メソッドが呼び出されたときに送出されます。 `saving` / `saved` イベントは、モデルの属性が変更されていない場合でも、モデルが作成または更新されるときに送出されます。 `-ing` で終わるイベント名はモデルへの変更が永続化される前に送出されますが、`-ed` で終わるイベントはモデルへの変更が永続化された後に送出されます。

モデル イベントのリスニングを開始するには、Eloquent モデルで `$dispatchesEvents` プロパティを定義します。このプロパティは、Eloquent モデルのライフサイクルのさまざまなポイントを独自の [イベントクラス](/docs/{{version}}/events) にマップします。各モデル イベント クラスは、コンストラクターを介して影響を受けるモデルのインスタンスを受け取ることを期待する必要があります。

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

Eloquent イベントを定義してマッピングした後、[イベントリスナ](/docs/{{version}}/events#defining-listeners) を使用してイベントを処理できます。

> [!WARNING]
> Eloquent 経由で一括更新または削除クエリを発行すると、影響を受けるモデルに対して `saved`、`updated`、`deleting`、および `deleted` モデル イベントは送出されません。これは、一括更新または削除を実行するときにモデルが実際には取得されないためです。

<a name="events-using-closures"></a>
### クロージャの使用

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

必要に応じて、モデル イベントを登録するときに [キュー可能な匿名イベント リスナ](/docs/{{version}}/events#queueable-anonymous-event-listeners) を利用できます。これにより、アプリケーションの [queue](/docs/{{version}}/queues) を使用してバックグラウンドでモデル イベント リスナを実行するように Laravel に指示されます。

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```

<a name="observers"></a>
### オブザーバ

<a name="defining-observers"></a>
#### オブザーバの定義

特定のモデルで多くのイベントをリッスンしている場合は、オブザーバを使用してすべてのリスナを 1 つのクラスにグループ化できます。 Observer クラスには、リッスンしたい Eloquent イベントを反映するメソッド名が付いています。これらの各メソッドは、影響を受けるモデルを唯一の引数として受け取ります。 `make:observer` Artisan コマンドは、新しいオブザーバ クラスを作成する最も簡単な方法です。

```shell
php artisan make:observer UserObserver --model=User
```

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
#### オブザーバとデータベーストランザクション

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
### イベントのミュート

場合によっては、モデルによって起動されるすべてのイベントを一時的に「ミュート」する必要がある場合があります。これは、`withoutEvents` メソッドを使用して実現できます。 `withoutEvents` メソッドは、唯一の引数としてクロージャを受け入れます。このクロージャ内で実行されるコードはモデル イベントをディスパッチせず、クロージャによって返される値は `withoutEvents` メソッドによって返されます。

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```

<a name="saving-a-single-model-without-events"></a>
#### イベントなしの単一モデルの保存

場合によっては、イベントを送出せずに特定のモデルを「保存」したい場合があります。これは、`saveQuietly` メソッドを使用して実行できます。

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```

イベントを送出せずに、特定のモデルを「更新」、「削除」、「論理的な削除」、「復元」、「複製」することもできます。

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```

