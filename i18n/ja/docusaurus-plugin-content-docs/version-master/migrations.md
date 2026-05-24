# データベース: 移行 (Database: Migrations)

- [Introduction](#introduction)
- [移行の生成](#generating-migrations)
    - [移行を潰す](#squashing-migrations)
- [移行構造](#migration-structure)
- [移行の実行](#running-migrations)
    - [移行のロールバック](#rolling-back-migrations)
- [Tables](#tables)
    - [テーブルの作成](#creating-tables)
    - [テーブルの更新](#updating-tables)
    - [テーブルの名前変更/削除](#renaming-and-dropping-tables)
- [Columns](#columns)
    - [列の作成](#creating-columns)
    - [利用可能な列のタイプ](#available-column-types)
    - [列修飾子](#column-modifiers)
    - [列の変更](#modifying-columns)
    - [列名の変更](#renaming-columns)
    - [列の削除](#dropping-columns)
- [Indexes](#indexes)
    - [インデックスの作成](#creating-indexes)
    - [インデックスの名前変更](#renaming-indexes)
    - [インデックスの削除](#dropping-indexes)
    - [外部キー制約](#foreign-key-constraints)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

移行はデータベースのバージョン管理のようなもので、チームがアプリケーションのデータベース スキーマ定義を定義して共有できるようにします。ソース管理から変更を取り込んだ後、ローカル データベース スキーマに列を手動で追加するようにチームメイトに指示しなければならなかった場合は、データベースの移行によって解決される問題に直面したことがあるでしょう。

Laravel `Schema` [facade](/docs/{{version}}/facades) は、Laravel でサポートされているすべてのデータベース システムにわたってテーブルを作成および操作するためのデータベースに依存しないサポートを提供します。通常、移行ではこのファサードを使用してデータベースのテーブルと列を作成および変更します。

<a name="generating-migrations"></a>
## 移行の生成 (Generating Migrations)

`make:migration` [Artisan コマンド](/docs/{{version}}/artisan) を使用してデータベース移行を生成できます。新しい移行は、`database/migrations` ディレクトリに配置されます。各移行ファイル名には、Laravel が移行の順序を決定できるようにするタイムスタンプが含まれています。

```shell
php artisan make:migration create_flights_table
```

Laravel は移行の名前を使用して、テーブルの名前と、移行によって新しいテーブルが作成されるかどうかを推測しようとします。 Laravel が移行名からテーブル名を決定できる場合、Laravel は生成された移行ファイルに指定されたテーブルを事前に入力します。それ以外の場合は、移行ファイルにテーブルを手動で指定するだけです。

生成された移行のカスタム パスを指定したい場合は、`make:migration` コマンドを実行するときに `--path` オプションを使用できます。指定されたパスは、アプリケーションのベース パスに対する相対パスである必要があります。

> [!NOTE]
> 移行スタブは、[スタブ発行](/docs/{{version}}/artisan#stub-customization) を使用してカスタマイズできます。

<a name="squashing-migrations"></a>
### 移行を潰す

アプリケーションを構築すると、時間の経過とともにさらに多くの移行が蓄積される可能性があります。これにより、数百もの移行が行われる可能性があり、`database/migrations` ディレクトリが肥大化する可能性があります。必要に応じて、移行を単一の SQL ファイルに「圧縮」することもできます。まず、`schema:dump` コマンドを実行します。

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

このコマンドを実行すると、Laravel はアプリケーションの `database/schema` ディレクトリに「スキーマ」ファイルを書き込みます。スキーマ ファイルの名前はデータベース接続に対応します。ここで、他の移行が実行されていないときにデータベースを移行しようとすると、Laravel はまず、使用しているデータベース接続のスキーマ ファイル内の SQL ステートメントを実行します。スキーマファイルのSQLステートメントを実行した後、Laravelはスキーマダンプの一部ではなかった残りの移行を実行します。

アプリケーションのテストでローカル開発中に通常使用するデータベース接続とは異なるデータベース接続を使用する場合は、テストでデータベースを構築できるように、そのデータベース接続を使用してスキーマ ファイルをダンプしていることを確認する必要があります。ローカル開発中に通常使用するデータベース接続をダンプした後でこれを実行するとよいでしょう。

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

チームの他の新しい開発者がアプリケーションの初期データベース構造を迅速に作成できるように、データベース スキーマ ファイルをソース管理にコミットする必要があります。

> [!WARNING]
> 移行スカッシングは、MariaDB、MySQL、PostgreSQL、および SQLite データベースでのみ利用可能であり、データベースのコマンドライン クライアントを利用します。

<a name="migration-structure"></a>
## 移行構造 (Migration Structure)

移行クラスには、`up` と `down` の 2 つのメソッドが含まれています。 `up` メソッドは、新しいテーブル、列、またはインデックスをデータベースに追加するために使用されますが、`down` メソッドは、`up` メソッドによって実行された操作を元に戻す必要があります。

これらの両方のメソッド内で、Laravel スキーマ ビルダを使用して、テーブルを表現的に作成および変更できます。 `Schema` ビルダ、[ドキュメントを確認してください](#creating-tables) で使用できるすべてのメソッドについて学習するには。たとえば、次の移行では `flights` テーブルが作成されます。

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('flights', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('airline');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::drop('flights');
    }
};
```

<a name="setting-the-migration-connection"></a>
#### 移行接続の設定

移行がアプリケーションのデフォルトのデータベース接続以外のデータベース接続と対話する場合は、移行の `$connection` プロパティを設定する必要があります。

```php
/**
 * The database connection that should be used by the migration.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * Run the migrations.
 */
public function up(): void
{
    // ...
}
```

<a name="skipping-migrations"></a>
#### 移行のスキップ

場合によっては、移行は、まだアクティブではなく、まだ実行したくない機能をサポートすることを目的としている場合があります。この場合、移行時に `shouldRun` メソッドを定義できます。 `shouldRun` メソッドが `false` を返した場合、移行はスキップされます。

```php
use App\Models\Flight;
use Laravel\Pennant\Feature;

/**
 * Determine if this migration should run.
 */
public function shouldRun(): bool
{
    return Feature::active(Flight::class);
}
```

<a name="running-migrations"></a>
## 移行の実行 (Running Migrations)

未処理の移行をすべて実行するには、`migrate` Artisan コマンドを実行します。

```shell
php artisan migrate
```

どの移行がすでに実行され、どの移行がまだ保留中であるかを確認したい場合は、`migrate:status` Artisan コマンドを使用できます。

```shell
php artisan migrate:status
```

`migrate` コマンドに `--step` オプションを指定すると、コマンドは各移行を独自のバッチとして実行し、後から `migrate:rollback` コマンドを使用して個々の移行をロールバックできます。

```shell
php artisan migrate --step
```

移行によって実行される SQL ステートメントを実際に実行せずに確認したい場合は、`--pretend` フラグを `migrate` コマンドに指定できます。

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
#### 移行実行の分離

アプリケーションを複数のサーバーにデプロイし、デプロイメント プロセスの一環として移行を実行している場合、2 つのサーバーが同時にデータベースを移行しようとすることは望ましくありません。これを回避するには、`migrate` コマンドを呼び出すときに `isolated` オプションを使用できます。

`isolated` オプションが指定されている場合、Laravel は移行の実行を試行する前に、アプリケーションのキャッシュドライバを使用してアトミックロックを取得します。ロックが保持されている間に `migrate` コマンドを実行しようとする他の試みはすべて実行されません。ただし、コマンドは引き続き正常終了ステータス コードで終了します。

```shell
php artisan migrate --isolated
```

> [!WARNING]
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<a name="forcing-migrations-to-run-in-production"></a>
#### 本番環境での強制的な移行の実行

一部の移行操作は破壊的なものであり、データが失われる可能性があります。運用データベースに対してこれらのコマンドを実行しないようにするために、コマンドを実行する前に確認を求めるメッセージが表示されます。プロンプトを表示せずにコマンドを強制的に実行するには、`--force` フラグを使用します。

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 移行のロールバック

最新の移行操作をロールバックするには、`rollback` Artisan コマンドを使用できます。このコマンドは、移行の最後の「バッチ」をロールバックします。これには複数の移行ファイルが含まれる場合があります。

```shell
php artisan migrate:rollback
```

`step` オプションを `rollback` コマンドに指定すると、限られた数の移行をロールバックできます。たとえば、次のコマンドは最後の 5 つの移行をロールバックします。

```shell
php artisan migrate:rollback --step=5
```

`rollback` コマンドに `batch` オプションを指定すると、移行の特定の「バッチ」をロールバックできます。`batch` オプションは、アプリケーションの `migrations` データベース テーブル内のバッチ値に対応します。たとえば、次のコマンドはバッチ 3 のすべての移行をロールバックします。

```shell
php artisan migrate:rollback --batch=3
```

移行によって実行される SQL ステートメントを実際に実行せずに確認したい場合は、`--pretend` フラグを `migrate:rollback` コマンドに指定できます。

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` コマンドは、アプリケーションのすべての移行をロールバックします。

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 単一のコマンドを使用したロールバックと移行

`migrate:refresh` コマンドは、すべての移行をロールバックしてから、`migrate` コマンドを実行します。このコマンドはデータベース全体を効果的に再作成します。

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

`refresh` コマンドに `step` オプションを指定すると、限られた数の移行をロールバックして再移行できます。たとえば、次のコマンドは、最後の 5 つの移行をロールバックして再移行します。

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### すべてのテーブルを削除して移行する

`migrate:fresh` コマンドは、データベースからすべてのテーブルを削除してから、`migrate` コマンドを実行します。

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

デフォルトでは、`migrate:fresh` コマンドはデフォルトのデータベース接続からテーブルのみを削除します。ただし、`--database` オプションを使用して、移行するデータベース接続を指定できます。データベース接続名は、アプリケーションの `database` [設定ファイル](/docs/{{version}}/configuration) で定義された接続に対応する必要があります。

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` コマンドは、プレフィックスに関係なく、すべてのデータベース テーブルを削除します。他のアプリケーションと共有されるデータベース上で開発する場合、このコマンドは注意して使用する必要があります。

<a name="tables"></a>
## テーブル (Tables)

<a name="creating-tables"></a>
### テーブルの作成

新しいデータベース テーブルを作成するには、`Schema` ファサードで `create` メソッドを使用します。 `create` メソッドは 2 つの引数を受け入れます。1 つ目はテーブルの名前で、2 つ目は新しいテーブルの定義に使用できる `Blueprint` オブジェクトを受け取るクロージャです。

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email');
    $table->timestamps();
});
```

テーブルを作成するときは、スキーマ ビルダの [列メソッド](#creating-columns) のいずれかを使用してテーブルの列を定義できます。

<a name="determining-table-column-existence"></a>
#### テーブル/カラムの存在の確認

`hasTable`、`hasColumn`、および `hasIndex` メソッドを使用して、テーブル、列、またはインデックスの存在を確認できます。

```php
if (Schema::hasTable('users')) {
    // The "users" table exists...
}

if (Schema::hasColumn('users', 'email')) {
    // The "users" table exists and has an "email" column...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // The "users" table exists and has a unique index on the "email" column...
}
```

<a name="database-connection-table-options"></a>
#### データベース接続とテーブルのオプション

アプリケーションのデフォルト接続ではないデータベース接続でスキーマ操作を実行する場合は、`connection` メソッドを使用します。

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

さらに、他のいくつかのプロパティとメソッドを使用して、テーブル作成の他の側面を定義することもできます。 MariaDB または MySQL を使用する場合、`engine` プロパティを使用してテーブルのストレージ エンジンを指定できます。

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

MariaDB または MySQL を使用する場合、`charset` プロパティと `collation` プロパティを使用して、作成されたテーブルの文字セットと照合順序を指定できます。

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

`temporary` メソッドを使用して、テーブルを「一時的」にする必要があることを示すことができます。一時テーブルは現在の接続のデータベース セッションにのみ表示され、接続が閉じられると自動的に削除されます。

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

データベース テーブルに「コメント」を追加したい場合は、テーブル インスタンスで `comment` メソッドを呼び出します。テーブル コメントは現在、MariaDB、MySQL、および PostgreSQL でのみサポートされています。

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### テーブルの更新

`Schema` ファサードの `table` メソッドを使用して、既存のテーブルを更新できます。 `create` メソッドと同様に、`table` メソッドは 2 つの引数を受け入れます。テーブルの名前と、テーブルに列またはインデックスを追加するために使用できる `Blueprint` インスタンスを受け取るクロージャです。

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### テーブルの名前変更/削除

既存のデータベーステーブルの名前を変更するには、`rename` メソッドを使用します。

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

既存のテーブルを削除するには、`drop` メソッドまたは `dropIfExists` メソッドを使用できます。

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 外部キーを使用したテーブルの名前変更

テーブルの名前を変更する前に、Laravel に規則に基づいた名前を割り当てるのではなく、テーブルの外部キー制約に明示的な名前が移行ファイルに含まれていることを確認する必要があります。それ以外の場合、外部キー制約名は古いテーブル名を参照します。

<a name="columns"></a>
## コラム (Columns)

<a name="creating-columns"></a>
### 列の作成

`Schema` ファサードの `table` メソッドを使用して、既存のテーブルを更新できます。 `create` メソッドと同様に、`table` メソッドは 2 つの引数を受け入れます。テーブルの名前と、テーブルに列を追加するために使用できる `Illuminate\Database\Schema\Blueprint` インスタンスを受け取るクロージャです。

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 利用可能な列のタイプ

スキーマ ビルダ ブループリントは、データベース テーブルに追加できるさまざまな種類の列に対応するさまざまなメソッドを提供します。使用可能な各メソッドを次の表に示します。

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

    .collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .collection-method code {
        font-size: 14px;
    }

    .collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a name="booleans-method-list"></a>
#### ブール型

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

<a name="strings-and-texts-method-list"></a>
#### 文字列とテキスト型

<div class="collection-method-list" markdown="1">

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

<a name="numbers--method-list"></a>
#### 数値型

<div class="collection-method-list" markdown="1">

[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[decimal](#column-method-decimal)
[double](#column-method-double)
[float](#column-method-float)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)

</div>

<a name="dates-and-times-method-list"></a>
#### 日付と時刻のタイプ

<div class="collection-method-list" markdown="1">

[dateTime](#column-method-dateTime)
[dateTimeTz](#column-method-dateTimeTz)
[date](#column-method-date)
[time](#column-method-time)
[timeTz](#column-method-timeTz)
[timestamp](#column-method-timestamp)
[timestamps](#column-method-timestamps)
[timestampsTz](#column-method-timestampsTz)
[softDeletes](#column-method-softDeletes)
[softDeletesTz](#column-method-softDeletesTz)
[year](#column-method-year)

</div>

<a name="binaries-method-list"></a>
#### バイナリ型

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

<a name="object-and-jsons-method-list"></a>
#### オブジェクトと Json タイプ

<div class="collection-method-list" markdown="1">

[json](#column-method-json)
[jsonb](#column-method-jsonb)

</div>

<a name="uuids-and-ulids-method-list"></a>
#### UUID と ULID のタイプ

<div class="collection-method-list" markdown="1">

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

<a name="spatials-method-list"></a>
#### 空間タイプ

<div class="collection-method-list" markdown="1">

[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

<a name="relationship-method-list"></a>
#### 関係の種類

<div class="collection-method-list" markdown="1">

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

<a name="spacifics-method-list"></a>
#### 専門分野の種類

<div class="collection-method-list" markdown="1">

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()` {.collection-method .first-collection-method}

`bigIncrements` メソッドは、自動インクリメントする `UNSIGNED BIGINT` (主キー) と同等の列を作成します。

```php
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
#### `bigInteger()` {.collection-method}

`bigInteger` メソッドは、`BIGINT` と同等の列を作成します。

```php
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
#### `binary()` {.collection-method}

`binary` メソッドは、`BLOB` と同等の列を作成します。

```php
$table->binary('photo');
```

MySQL、MariaDB、または SQL Server を利用する場合、`length` および `fixed` 引数を渡して、`VARBINARY` または `BINARY` と同等の列を作成できます。

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```

<a name="column-method-boolean"></a>
#### `boolean()` {.collection-method}

`boolean` メソッドは、`BOOLEAN` と同等の列を作成します。

```php
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
#### `char()` {.collection-method}

`char` メソッドは、指定された長さの `CHAR` と同等の列を作成します。

```php
$table->char('name', length: 100);
```

<a name="column-method-dateTimeTz"></a>
#### `dateTimeTz()` {.collection-method}

`dateTimeTz` メソッドは、オプションの小数秒精度を持つ `DATETIME` (タイムゾーン付き) と同等の列を作成します。

```php
$table->dateTimeTz('created_at', precision: 0);
```

<a name="column-method-dateTime"></a>
#### `dateTime()` {.collection-method}

`dateTime` メソッドは、オプションの小数秒精度を使用して、`DATETIME` と同等の列を作成します。

```php
$table->dateTime('created_at', precision: 0);
```

<a name="column-method-date"></a>
#### `date()` {.collection-method}

`date` メソッドは、`DATE` と同等の列を作成します。

```php
$table->date('created_at');
```

<a name="column-method-decimal"></a>
#### `decimal()` {.collection-method}

`decimal` メソッドは、指定された精度 (合計桁数) と位取り (10 進数の桁数) を持つ `DECIMAL` と同等の列を作成します。

```php
$table->decimal('amount', total: 8, places: 2);
```

<a name="column-method-double"></a>
#### `double()` {.collection-method}

`double` メソッドは、`DOUBLE` と同等の列を作成します。

```php
$table->double('amount');
```

<a name="column-method-enum"></a>
#### `enum()` {.collection-method}

`enum` メソッドは、指定された有効な値を使用して `ENUM` と同等の列を作成します。

```php
$table->enum('difficulty', ['easy', 'hard']);
```

もちろん、許可される値の配列を手動で定義する代わりに、`Enum::cases()` メソッドを使用することもできます。

```php
use App\Enums\Difficulty;

$table->enum('difficulty', Difficulty::cases());
```

<a name="column-method-float"></a>
#### `float()` {.collection-method}

`float` メソッドは、指定された精度で `FLOAT` と同等の列を作成します。

```php
$table->float('amount', precision: 53);
```

<a name="column-method-foreignId"></a>
#### `foreignId()` {.collection-method}

`foreignId` メソッドは、`UNSIGNED BIGINT` と同等の列を作成します。

```php
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
#### `foreignIdFor()` {.collection-method}

`foreignIdFor` メソッドは、指定されたモデル クラスに `{column}_id` と同等の列を追加します。列のタイプは、モデルのキーのタイプに応じて、`UNSIGNED BIGINT`、`CHAR(36)`、または `CHAR(26)` になります。

```php
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
#### `foreignUlid()` {.collection-method}

`foreignUlid` メソッドは、`ULID` と同等の列を作成します。

```php
$table->foreignUlid('user_id');
```

<a name="column-method-foreignUuid"></a>
#### `foreignUuid()` {.collection-method}

`foreignUuid` メソッドは、`UUID` と同等の列を作成します。

```php
$table->foreignUuid('user_id');
```

<a name="column-method-geography"></a>
#### `geography()` {.collection-method}

`geography` メソッドは、指定された空間タイプと SRID (空間参照システム識別子) を使用して、`GEOGRAPHY` と同等の列を作成します。

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]
> 空間タイプのサポートは、データベース ドライバによって異なります。データベースのドキュメントを参照してください。アプリケーションが PostgreSQL データベースを利用している場合は、`geography` メソッドを使用する前に、[PostGIS](https://postgis.net) 拡張機能をインストールする必要があります。

<a name="column-method-geometry"></a>
#### `geometry()` {.collection-method}

`geometry` メソッドは、指定された空間タイプと SRID (空間参照システム識別子) を使用して、`GEOMETRY` と同等の列を作成します。

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]
> 空間タイプのサポートは、データベース ドライバによって異なります。データベースのドキュメントを参照してください。アプリケーションが PostgreSQL データベースを利用している場合は、`geometry` メソッドを使用する前に、[PostGIS](https://postgis.net) 拡張機能をインストールする必要があります。

<a name="column-method-id"></a>
#### `id()` {.collection-method}

`id` メソッドは、`bigIncrements` メソッドのエイリアスです。デフォルトでは、このメソッドは `id` 列を作成します。ただし、列に別の名前を割り当てたい場合は、列名を渡すことができます。

```php
$table->id();
```

<a name="column-method-increments"></a>
#### `increments()` {.collection-method}

`increments` メソッドは、自動インクリメントする `UNSIGNED INTEGER` と同等の列を主キーとして作成します。

```php
$table->increments('id');
```

<a name="column-method-integer"></a>
#### `integer()` {.collection-method}

`integer` メソッドは、`INTEGER` と同等の列を作成します。

```php
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
#### `ipAddress()` {.collection-method}

`ipAddress` メソッドは、`VARCHAR` と同等の列を作成します。

```php
$table->ipAddress('visitor');
```

PostgreSQLを使用する場合、`INET`列が作成されます。

<a name="column-method-json"></a>
#### `json()` {.collection-method}

`json` メソッドは、`JSON` と同等の列を作成します。

```php
$table->json('options');
```

SQLiteを使用する場合、`TEXT`列が作成されます。

<a name="column-method-jsonb"></a>
#### `jsonb()` {.collection-method}

`jsonb` メソッドは、`JSONB` と同等の列を作成します。

```php
$table->jsonb('options');
```

SQLiteを使用する場合、`TEXT`列が作成されます。

<a name="column-method-longText"></a>
#### `longText()` {.collection-method}

`longText` メソッドは、`LONGTEXT` と同等の列を作成します。

```php
$table->longText('description');
```

MySQL または MariaDB を利用する場合、`LONGBLOB` と同等の列を作成するために、`binary` 文字セットを列に適用できます。

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```

<a name="column-method-macAddress"></a>
#### `macAddress()` {.collection-method}

`macAddress` メソッドは、MAC アドレスを保持するための列を作成します。 PostgreSQL などの一部のデータベース システムには、このタイプのデータ専用の列タイプがあります。他のデータベース システムでは、文字列と同等の列が使用されます。

```php
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()` {.collection-method}

`mediumIncrements` メソッドは、自動インクリメントする `UNSIGNED MEDIUMINT` と同等の列を主キーとして作成します。

```php
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
#### `mediumInteger()` {.collection-method}

`mediumInteger` メソッドは、`MEDIUMINT` と同等の列を作成します。

```php
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
#### `mediumText()` {.collection-method}

`mediumText` メソッドは、`MEDIUMTEXT` と同等の列を作成します。

```php
$table->mediumText('description');
```

MySQL または MariaDB を利用する場合、`MEDIUMBLOB` と同等の列を作成するために、`binary` 文字セットを列に適用できます。

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a name="column-method-morphs"></a>
#### `morphs()` {.collection-method}

`morphs` メソッドは、`{column}_id` に相当する列と `{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。 `{column}_id` の列タイプは、モデルのキー タイプに応じて、`UNSIGNED BIGINT`、`CHAR(36)`、または `CHAR(26)` になります。

このメソッドは、多態性 [Eloquent リレーション](/docs/{{version}}/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

```php
$table->morphs('taggable');
```

<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()` {.collection-method}

このメソッドは [morphs](#column-method-morphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

```php
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()` {.collection-method}

このメソッドは [ulidMorphs](#column-method-ulidMorphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

```php
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()` {.collection-method}

このメソッドは [uuidMorphs](#column-method-uuidMorphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

```php
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-rememberToken"></a>
#### `rememberToken()` {.collection-method}

`rememberToken` メソッドは、現在の「remember me」 [認証トークン](/docs/{{version}}/authentication#remembering-users) を格納するための、null 許容の `VARCHAR(100)` と同等の列を作成します。

```php
$table->rememberToken();
```

<a name="column-method-set"></a>
#### `set()` {.collection-method}

`set` メソッドは、指定された有効な値のリストを使用して、`SET` と同等の列を作成します。

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
#### `smallIncrements()` {.collection-method}

`smallIncrements` メソッドは、自動インクリメントする `UNSIGNED SMALLINT` と同等の列を主キーとして作成します。

```php
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
#### `smallInteger()` {.collection-method}

`smallInteger` メソッドは、`SMALLINT` と同等の列を作成します。

```php
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
#### `softDeletesTz()` {.collection-method}

`softDeletesTz` メソッドは、オプションの小数秒精度を持つ、NULL 許容の `deleted_at` `TIMESTAMP` (タイムゾーンあり) と同等の列を追加します。この列は、Eloquent の「論理的な削除」機能に必要な `deleted_at` タイムスタンプを保存することを目的としています。

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

<a name="column-method-softDeletes"></a>
#### `softDeletes()` {.collection-method}

`softDeletes` メソッドは、オプションの小数秒精度を持つ、NULL 許容の `deleted_at` `TIMESTAMP` 同等の列を追加します。この列は、Eloquent の「論理的な削除」機能に必要な `deleted_at` タイムスタンプを保存することを目的としています。

```php
$table->softDeletes('deleted_at', precision: 0);
```

<a name="column-method-string"></a>
#### `string()` {.collection-method}

`string` メソッドは、指定された長さの `VARCHAR` と同等の列を作成します。

```php
$table->string('name', length: 100);
```

<a name="column-method-text"></a>
#### `text()` {.collection-method}

`text` メソッドは、`TEXT` と同等の列を作成します。

```php
$table->text('description');
```

MySQL または MariaDB を利用する場合、`BLOB` と同等の列を作成するために、`binary` 文字セットを列に適用できます。

```php
$table->text('data')->charset('binary'); // BLOB
```

<a name="column-method-timeTz"></a>
#### `timeTz()` {.collection-method}

`timeTz` メソッドは、オプションの小数秒精度を持つ `TIME` (タイムゾーン付き) と同等の列を作成します。

```php
$table->timeTz('sunrise', precision: 0);
```

<a name="column-method-time"></a>
#### `time()` {.collection-method}

`time` メソッドは、オプションの小数秒精度を使用して、`TIME` と同等の列を作成します。

```php
$table->time('sunrise', precision: 0);
```

<a name="column-method-timestampTz"></a>
#### `timestampTz()` {.collection-method}

`timestampTz` メソッドは、オプションの小数秒精度を持つ `TIMESTAMP` (タイムゾーン付き) と同等の列を作成します。

```php
$table->timestampTz('added_at', precision: 0);
```

<a name="column-method-timestamp"></a>
#### `timestamp()` {.collection-method}

`timestamp` メソッドは、オプションの小数秒精度を使用して、`TIMESTAMP` と同等の列を作成します。

```php
$table->timestamp('added_at', precision: 0);
```

<a name="column-method-timestampsTz"></a>
#### `timestampsTz()` {.collection-method}

`timestampsTz` メソッドは、オプションの小数秒精度を使用して、`created_at` および `updated_at` `TIMESTAMP` (タイムゾーン付き) と同等の列を作成します。

```php
$table->timestampsTz(precision: 0);
```

<a name="column-method-timestamps"></a>
#### `timestamps()` {.collection-method}

`timestamps` メソッドは、オプションの小数秒精度を使用して、`created_at` および `updated_at` `TIMESTAMP` と同等の列を作成します。

```php
$table->timestamps(precision: 0);
```

<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()` {.collection-method}

`tinyIncrements` メソッドは、自動インクリメントする `UNSIGNED TINYINT` と同等の列を主キーとして作成します。

```php
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
#### `tinyInteger()` {.collection-method}

`tinyInteger` メソッドは、`TINYINT` と同等の列を作成します。

```php
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
#### `tinyText()` {.collection-method}

`tinyText` メソッドは、`TINYTEXT` と同等の列を作成します。

```php
$table->tinyText('notes');
```

MySQL または MariaDB を利用する場合、`TINYBLOB` と同等の列を作成するために、`binary` 文字セットを列に適用できます。

```php
$table->tinyText('data')->charset('binary'); // TINYBLOB
```

<a name="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()` {.collection-method}

`unsignedBigInteger` メソッドは、`UNSIGNED BIGINT` と同等の列を作成します。

```php
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedInteger"></a>
#### `unsignedInteger()` {.collection-method}

`unsignedInteger` メソッドは、`UNSIGNED INTEGER` と同等の列を作成します。

```php
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()` {.collection-method}

`unsignedMediumInteger` メソッドは、`UNSIGNED MEDIUMINT` と同等の列を作成します。

```php
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()` {.collection-method}

`unsignedSmallInteger` メソッドは、`UNSIGNED SMALLINT` と同等の列を作成します。

```php
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()` {.collection-method}

`unsignedTinyInteger` メソッドは、`UNSIGNED TINYINT` と同等の列を作成します。

```php
$table->unsignedTinyInteger('votes');
```

<a name="column-method-ulidMorphs"></a>
#### `ulidMorphs()` {.collection-method}

`ulidMorphs` メソッドは、`{column}_id` `CHAR(26)` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

このメソッドは、ULID 識別子を使用する多態性 [Eloquent リレーション](/docs/{{version}}/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

```php
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()` {.collection-method}

`uuidMorphs` メソッドは、`{column}_id` `CHAR(36)` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

このメソッドは、UUID 識別子を使用する [多様なEloquent リレーション](/docs/{{version}}/eloquent-relationships#polymorphic-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

```php
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
#### `ulid()` {.collection-method}

`ulid` メソッドは、`ULID` と同等の列を作成します。

```php
$table->ulid('id');
```

<a name="column-method-uuid"></a>
#### `uuid()` {.collection-method}

`uuid` メソッドは、`UUID` と同等の列を作成します。

```php
$table->uuid('id');
```

<a name="column-method-vector"></a>
#### `vector()` {.collection-method}

`vector` メソッドは、`vector` と同等の列を作成します。

```php
$table->vector('embedding', dimensions: 100);
```

PostgreSQL を利用する場合、`vector` 列を作成する前に、`pgvector` 拡張機能をロードする必要があります。

```php
Schema::ensureVectorExtensionExists();
```

<a name="column-method-year"></a>
#### `year()` {.collection-method}

`year` メソッドは、`YEAR` と同等の列を作成します。

```php
$table->year('birth_year');
```

<a name="column-modifiers"></a>
### 列修飾子

上記の列タイプに加えて、データベース テーブルに列を追加するときに使用できる列「修飾子」がいくつかあります。たとえば、列を「NULL 可能」にするには、`nullable` メソッドを使用します。

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

次の表には、使用可能な列修飾子がすべて含まれています。このリストには、[インデックス修飾子](#creating-indexes) は含まれていません。

<div class="overflow-auto">

| 修飾子                            | 説明                                                                                    |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- |
| `->after('column')`                 | 列を別の列 (MariaDB / MySQL) の「後」に配置します。                                     |
| `->autoIncrement()`                 | `INTEGER` 列を自動インクリメント (主キー) として設定します。                                      |
| `->charset('utf8mb4')`              | カラム（MariaDB / MySQL）の文字セットを指定します。                                      |
| `->collation('utf8mb4_unicode_ci')` | 列の照合順序を指定します。                                                            |
| `->comment('my comment')`           | 列にコメントを追加します (MariaDB / MySQL / PostgreSQL)。                                      |
| `->default($value)`                 | 列の「デフォルト」値を指定します。                                                      |
| `->first()`                         | テーブル (MariaDB / MySQL) の「最初」に列を配置します。                                       |
| `->from($integer)`                  | 自動インクリメントフィールドの開始値を設定します (MariaDB / MySQL / PostgreSQL)。           |
| `->instant()`                       | インスタント操作 (MySQL) を使用して列を追加または変更します。                                   |
| `->invisible()`                     | 列を `SELECT *` クエリに対して「非表示」にします (MariaDB / MySQL)。                           |
| `->lock($mode)`                     | カラム操作のロックモードを指定します(MySQL)。                                          |
| `->nullable($value = true)`         | `NULL` 値を列に挿入できるようにします。                                            |
| `->storedAs($expression)`           | 格納された生成列 (MariaDB / MySQL / PostgreSQL / SQLite) を作成します。                      |
| `->unsigned()`                      | `INTEGER` 列を `UNSIGNED` (MariaDB / MySQL) として設定します。                                         |
| `->useCurrent()`                    | `TIMESTAMP` 列をデフォルト値として `CURRENT_TIMESTAMP` を使用するように設定します。                           |
| `->useCurrentOnUpdate()`            | レコードの更新時に `CURRENT_TIMESTAMP` を使用するように `TIMESTAMP` 列を設定します (MariaDB / MySQL)。 |
| `->virtualAs($expression)`          | 仮想生成列 (MariaDB / MySQL / SQLite) を作成します。                                  |
| `->generatedAs($expression)`        | シーケンス オプションを指定して ID 列を作成します (PostgreSQL)。                        |
| `->always()`                        | ID 列の入力に対するシーケンス値の優先順位を定義します (PostgreSQL)。      |

</div>

<a name="default-expressions"></a>
#### デフォルトの式

`default` 修飾子は、値または `Illuminate\Database\Query\Expression` インスタンスを受け入れます。 `Expression` インスタンスを使用すると、Laravel が値を引用符で囲むことがなくなり、データベース固有の関数を使用できるようになります。これが特に役立つ状況の 1 つは、JSON 列にデフォルト値を割り当てる必要がある場合です。

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('flights', function (Blueprint $table) {
            $table->id();
            $table->json('movies')->default(new Expression('(JSON_ARRAY())'));
            $table->timestamps();
        });
    }
};
```

> [!WARNING]
> デフォルトの式のサポートは、データベース ドライバ、データベース バージョン、およびフィールド タイプによって異なります。データベースのドキュメントを参照してください。

<a name="column-order"></a>
#### 列の順序

MariaDB または MySQL データベースを使用する場合、`after` メソッドを使用して、スキーマ内の既存の列の後に列を追加できます。

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="instant-column-operations"></a>
#### インスタント列操作

MySQL を使用する場合、`instant` 修飾子を列定義に連結して、MySQL の「インスタント」アルゴリズムを使用して列を追加または変更する必要があることを示すことができます。このアルゴリズムにより、テーブル全体を再構築せずに特定のスキーマ変更を実行できるため、テーブル サイズに関係なく、ほぼ瞬時に変更が行われます。

```php
$table->string('name')->nullable()->instant();
```

インスタント列追加ではテーブルの末尾にのみ列を追加できるため、`instant` 修飾子を `after` または `first` 修飾子と組み合わせることはできません。さらに、このアルゴリズムはすべての列の種類や操作をサポートしているわけではありません。要求された操作に互換性がない場合、MySQL はエラーを発生させます。

どの操作が列の即時変更と互換性があるかを判断するには、[MySQL のドキュメント](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html) を参照してください。

<a name="ddl-locking"></a>
#### DDL ロック

MySQL を使用する場合、`lock` 修飾子を列、インデックス、または外部キー定義に連鎖させて、スキーマ操作中のテーブルのロックを制御できます。 MySQL はいくつかのロック モードをサポートしています。 `none` は同時読み取りと書き込みを許可します。 `shared` は同時読み取りを許可しますが書き込みをブロックします。 `exclusive` はすべての同時アクセスをブロックします。 `default` は MySQL に最適なモードを選択させます。

```php
$table->string('name')->lock('none');

$table->index('email')->lock('shared');
```

要求されたロック モードが操作と互換性がない場合、MySQL はエラーを生成します。 `lock` 修飾子を `instant` 修飾子と組み合わせて、スキーマ変更をさらに最適化することができます。

```php
$table->string('name')->instant()->lock('none');
```

<a name="modifying-columns"></a>
### 列の変更

`change` メソッドを使用すると、既存の列のタイプと属性を変更できます。たとえば、`string` 列のサイズを増やしたい場合があります。 `change` メソッドの動作を確認するには、`name` 列のサイズを 25 から 50 に増やしてみましょう。これを実現するには、単に列の新しい状態を定義してから、`change` メソッドを呼び出します。

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

列を変更するときは、列定義に保持したいすべての修飾子を明示的に含める必要があります。欠落している属性は削除されます。たとえば、`unsigned`、`default`、および `comment` 属性を保持するには、列を変更するときに各修飾子を明示的に呼び出す必要があります。

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

`change` メソッドは列のインデックスを変更しません。したがって、列を変更するときにインデックス修飾子を使用してインデックスを明示的に追加または削除できます。

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="renaming-columns"></a>
### 列名の変更

列の名前を変更するには、スキーマ ビルダが提供する `renameColumn` メソッドを使用できます。

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
### 列の削除

列を削除するには、スキーマ ビルダで `dropColumn` メソッドを使用できます。

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

列名の配列を `dropColumn` メソッドに渡すことで、テーブルから複数の列を削除できます。

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
#### 使用可能なコマンドエイリアス

Laravel は、一般的なタイプの列の削除に関連する便利なメソッドをいくつか提供しています。これらの各方法については、次の表で説明します。

<div class="overflow-auto">

| 指示                             | 説明                                           |
| ----------------------------------- | ----------------------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_id` 列と `morphable_type` 列を削除します。 |
| `$table->dropRememberToken();`      | `remember_token` 列を削除します。                     |
| `$table->dropSoftDeletes();`        | `deleted_at` 列を削除します。                         |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()` メソッドの別名。                  |
| `$table->dropTimestamps();`         | `created_at` 列と `updated_at` 列を削除します。       |
| `$table->dropTimestampsTz();`       | `dropTimestamps()` メソッドの別名。                   |

</div>

<a name="indexes"></a>
## インデックス (Indexes)

<a name="creating-indexes"></a>
### インデックスの作成

Laravel スキーマ ビルダは、いくつかの種類のインデックスをサポートしています。次の例では、新しい `email` 列を作成し、その値が一意である必要があることを指定します。インデックスを作成するには、`unique` メソッドを列定義に連鎖させます。

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

あるいは、列を定義した後にインデックスを作成することもできます。これを行うには、スキーマ ビルダ ブループリントで `unique` メソッドを呼び出す必要があります。このメソッドは、一意のインデックスを受け取る列の名前を受け入れます。

```php
$table->unique('email');
```

列の配列をインデックス メソッドに渡して、複合 (または複合) インデックスを作成することもできます。

```php
$table->index(['account_id', 'created_at']);
```

インデックスを作成するとき、Laravel はテーブル、列名、インデックスの種類に基づいてインデックス名を自動的に生成しますが、メソッドに 2 番目の引数を渡してインデックス名を自分で指定することもできます。

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
#### 利用可能なインデックスの種類

Laravel のスキーマ ビルダ ブループリント クラスは、Laravel でサポートされる各タイプのインデックスを作成するためのメソッドを提供します。各インデックス メソッドは、オプションの 2 番目の引数を受け入れてインデックスの名前を指定します。省略した場合、名前はインデックスに使用されるテーブルと列の名前、およびインデックス タイプから派生します。使用可能な各インデックス方法については、次の表で説明します。

<div class="overflow-auto">

| 指示                                          | 説明                                                    |
| ------------------------------------------------ | -------------------------------------------------------------- |
| `$table->primary('id');`                         | 主キーを追加します。                                            |
| `$table->primary(['id', 'parent_id']);`          | 複合キーを追加します。                                           |
| `$table->unique('email');`                       | 一意のインデックスを追加します。                                           |
| `$table->index('state');`                        | インデックスを追加します。                                                 |
| `$table->fullText('body');`                      | 全文インデックスを追加します (MariaDB / MySQL / PostgreSQL)。         |
| `$table->fullText('body')->language('english');` | 指定した言語 (PostgreSQL) の全文インデックスを追加します。 |
| `$table->spatialIndex('location');`              | 空間インデックスを追加します (SQLite を除く)。                          |

</div>

<a name="online-index-creation"></a>
#### オンラインインデックス作成

デフォルトでは、大きなテーブルにインデックスを作成するとテーブルがロックされ、インデックスの構築中に読み取りまたは書き込みがブロックされることがあります。 PostgreSQL または SQL Server を使用する場合、`online` メソッドをインデックス定義にチェーンして、テーブルをロックせずにインデックスを作成すると、インデックス作成中にアプリケーションがデータの読み取りと書き込みを継続できるようになります。

```php
$table->string('email')->unique()->online();
```

PostgreSQL を使用する場合、これにより、インデックス作成ステートメントに `CONCURRENTLY` オプションが追加されます。 SQL Server を使用する場合、これにより `WITH (online = on)` オプションが追加されます。

<a name="renaming-indexes"></a>
### インデックスの名前変更

インデックスの名前を変更するには、スキーマ ビルダ ブループリントによって提供される `renameIndex` メソッドを使用できます。このメソッドは、現在のインデックス名を最初の引数として受け入れ、目的の名前を 2 番目の引数として受け入れます。

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
### インデックスの削除

インデックスを削除するには、インデックスの名前を指定する必要があります。デフォルトでは、Laravel はテーブル名、インデックス付き列の名前、インデックスタイプに基づいてインデックス名を自動的に割り当てます。以下にいくつかの例を示します。

<div class="overflow-auto">

| 指示                                                  | 説明                                                 |
| -------------------------------------------------------- | ----------------------------------------------------------- |
| `$table->dropPrimary('users_id_primary');`               | 「users」テーブルから主キーを削除します。                  |
| `$table->dropUnique('users_email_unique');`              | 「users」テーブルから一意のインデックスを削除します。                 |
| `$table->dropIndex('geo_state_index');`                  | 「geo」テーブルから基本インデックスを削除します。                    |
| `$table->dropFullText('posts_body_fulltext');`           | 「posts」テーブルから全文インデックスを削除します。              |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | 「geo」テーブルから空間インデックスを削除します (SQLite を除く)。 |

</div>

インデックスを削除するメソッドに列の配列を渡すと、テーブル名、列、インデックス タイプに基づいて従来のインデックス名が生成されます。

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a name="foreign-key-constraints"></a>
### 外部キー制約

Laravel は、データベース レベルで参照整合性を強制するために使用される外部キー制約の作成のサポートも提供します。たとえば、`users` テーブルの `id` 列を参照する `posts` テーブルの `user_id` 列を定義してみましょう。

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

この構文はかなり冗長であるため、Laravel では、より良い開発者エクスペリエンスを提供するために、規則を使用する追加の簡潔なメソッドが提供されています。 `foreignId` メソッドを使用して列を作成する場合、上記の例は次のように書き換えることができます。

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

`foreignId` メソッドは `UNSIGNED BIGINT` と同等の列を作成しますが、`constrained` メソッドは規則を使用して参照されるテーブルと列を決定します。テーブル名が Laravel の規則と一致しない場合は、それを `constrained` メソッドに手動で指定できます。さらに、生成されたインデックスに割り当てる名前も指定できます。

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

制約の「削除時」プロパティと「更新時」プロパティに必要なアクションを指定することもできます。

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

これらのアクションには、代替の表現力豊かな構文も提供されています。

<div class="overflow-auto">

| 方法                        | 説明                                       |
| ----------------------------- | ------------------------------------------------- |
| `$table->cascadeOnUpdate();`  | 更新はカスケードする必要があります。                           |
| `$table->restrictOnUpdate();` | 更新は制限されるべきです。                     |
| `$table->nullOnUpdate();`     | 更新では外部キー値を null に設定する必要があります。 |
| `$table->noActionOnUpdate();` | 更新に対するアクションはありません。                             |
| `$table->cascadeOnDelete();`  | 削除はカスケードする必要があります。                           |
| `$table->restrictOnDelete();` | 削除は制限する必要があります。                     |
| `$table->nullOnDelete();`     | 削除では、外部キーの値を null に設定する必要があります。 |
| `$table->noActionOnDelete();` | 子レコードが存在する場合は削除を防止します。          |

</div>

追加の [列修飾子](#column-modifiers) は、`constrained` メソッドの前に呼び出す必要があります。

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
#### 外部キーの削除

外部キーを削除するには、`dropForeign` メソッドを使用して、削除する外部キー制約の名前を引数として渡します。外部キー制約では、インデックスと同じ命名規則が使用されます。つまり、外部キー制約名は、制約内のテーブル名と列名に基づいて、その後に「\_foreign」サフィックスが付加されます。

```php
$table->dropForeign('posts_user_id_foreign');
```

あるいは、外部キーを保持する列名を含む配列を `dropForeign` メソッドに渡すこともできます。配列は、Laravel の制約命名規則を使用して外部キー制約名に変換されます。

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
#### 外部キー制約の切り替え

次の方法を使用して、移行内で外部キー制約を有効または無効にすることができます。

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> [!WARNING]
> SQLite はデフォルトで外部キー制約を無効にします。 SQLite を使用する場合は、移行で SQLite を作成する前に、データベース構成で [外部キーのサポートを有効にする](/docs/{{version}}/database#configuration) を実行してください。

<a name="events"></a>
## イベント (Events)

便宜上、各移行操作では [event](/docs/{{version}}/events) がディスパッチされます。次のイベントはすべて、基本 `Illuminate\Database\Events\MigrationEvent` クラスを拡張します。

<div class="overflow-auto">

| クラス                                            | 説明                                      |
| ------------------------------------------------ | ------------------------------------------------ |
| `Illuminate\Database\Events\MigrationsStarted`   | 移行のバッチが実行されようとしています。   |
| `Illuminate\Database\Events\MigrationsEnded`     | 移行のバッチの実行が終了しました。    |
| `Illuminate\Database\Events\MigrationStarted`    | 単一の移行が実行されようとしています。      |
| `Illuminate\Database\Events\MigrationEnded`      | 1 つの移行の実行が終了しました。       |
| `Illuminate\Database\Events\NoPendingMigrations` | 移行コマンドで保留中の移行が見つかりませんでした。 |
| `Illuminate\Database\Events\SchemaDumped`        | データベース スキーマ ダンプが完了しました。            |
| `Illuminate\Database\Events\SchemaLoaded`        | 既存のデータベース スキーマ ダンプがロードされました。     |

</div>

