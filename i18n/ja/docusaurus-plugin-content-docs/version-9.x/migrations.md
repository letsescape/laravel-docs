<!-- # Database: Migrations -->
# Database: Migrations

- [Introduction](#introduction)
- [Generating Migrations](#generating-migrations)
    - [Squashing Migrations](#squashing-migrations)
- [Migration Structure](#migration-structure)
- [Running Migrations](#running-migrations)
    - [Rolling Back Migrations](#rolling-back-migrations)
- [Tables](#tables)
    - [Creating Tables](#creating-tables)
    - [Updating Tables](#updating-tables)
    - [Renaming / Dropping Tables](#renaming-and-dropping-tables)
- [Columns](#columns)
    - [Creating Columns](#creating-columns)
    - [Available Column Types](#available-column-types)
    - [Column Modifiers](#column-modifiers)
    - [Modifying Columns](#modifying-columns)
    - [Renaming Columns](#renaming-columns)
    - [Dropping Columns](#dropping-columns)
- [Indexes](#indexes)
    - [Creating Indexes](#creating-indexes)
    - [Renaming Indexes](#renaming-indexes)
    - [Dropping Indexes](#dropping-indexes)
    - [Foreign Key Constraints](#foreign-key-constraints)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Migrations are like version control for your database, allowing your team to define and share the application's database schema definition. If you have ever had to tell a teammate to manually add a column to their local database schema after pulling in your changes from source control, you've faced the problem that database migrations solve. -->
移行はデータベースのバージョン管理のようなもので、チームがアプリケーションのデータベース スキーマ定義を定義して共有できるようにします。ソース管理から変更を取り込んだ後、ローカル データベース スキーマに列を手動で追加するようにチームメイトに指示しなければならなかった場合は、データベースの移行によって解決される問題に直面したことがあるでしょう。

<!-- The Laravel `Schema` [facade](/docs/9.x/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns. -->
Laravel `Schema` [facade](/docs/9.x/facades) は、Laravel でサポートされているすべてのデータベース システムにわたってテーブルを作成および操作するためのデータベースに依存しないサポートを提供します。通常、移行ではこのファサードを使用してデータベースのテーブルと列を作成および変更します。

<a name="generating-migrations"></a>
<!-- ## Generating Migrations -->
## Generating Migrations

<!-- You may use the `make:migration` [Artisan command](/docs/9.x/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations: -->
`make:migration` [Artisan command](/docs/9.x/artisan) を使用してデータベース移行を生成できます。新しい移行は、`database/migrations` ディレクトリに配置されます。各移行ファイル名には、Laravel が移行の順序を決定できるようにするタイムスタンプが含まれています。

```shell
php artisan make:migration create_flights_table
```

<!-- Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually. -->
Laravel は移行の名前を使用して、テーブルの名前と、移行によって新しいテーブルが作成されるかどうかを推測しようとします。 Laravel が移行名からテーブル名を決定できる場合、Laravel は生成された移行ファイルに指定されたテーブルを事前に入力します。それ以外の場合は、移行ファイルにテーブルを手動で指定するだけです。

<!-- If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path. -->
生成された移行のカスタム パスを指定したい場合は、`make:migration` コマンドを実行するときに `--path` オプションを使用できます。指定されたパスは、アプリケーションのベース パスに対する相対パスである必要があります。

> [!NOTE]
> 移行スタブは、[stub publishing](/docs/9.x/artisan#stub-customization) を使用してカスタマイズできます。

<a name="squashing-migrations"></a>
<!-- ### Squashing Migrations -->
### Squashing Migrations

<!-- As you build your application, you may accumulate more and more migrations over time. This can lead to your `database/migrations` directory becoming bloated with potentially hundreds of migrations. If you would like, you may "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command: -->
アプリケーションを構築すると、時間の経過とともにさらに多くの移行が蓄積される可能性があります。これにより、数百もの移行が行われる可能性があり、`database/migrations` ディレクトリが肥大化する可能性があります。必要に応じて、移行を単一の SQL ファイルに「圧縮」することもできます。まず、`schema:dump` コマンドを実行します。

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

<!-- When you execute this command, Laravel will write a "schema" file to your application's `database/schema` directory. The schema file's name will correspond to the database connection. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will execute first the SQL statements of the schema file of the database connection you are using. After executing the schema file's statements, Laravel will execute any remaining migrations that were not part of the schema dump. -->
このコマンドを実行すると、Laravel はアプリケーションの `database/schema` ディレクトリに「スキーマ」ファイルを書き込みます。スキーマ ファイルの名前はデータベース接続に対応します。ここで、他の移行が実行されていないときにデータベースを移行しようとすると、Laravel は、使用しているデータベース接続のスキーマ ファイルの SQL ステートメントを最初に実行します。スキーマファイルのステートメントを実行した後、Laravel はスキーマダンプの一部ではなかった残りの移行を実行します。

<!-- If your application's tests use a different database connection than the one you typically use during local development, you should ensure you have dumped a schema file using that database connection so that your tests are able to build your database. You may wish to do this after dumping the database connection you typically use during local development: -->
アプリケーションのテストでローカル開発中に通常使用するデータベース接続とは異なるデータベース接続を使用する場合は、テストでデータベースを構築できるように、そのデータベース接続を使用してスキーマ ファイルをダンプしていることを確認する必要があります。ローカル開発中に通常使用するデータベース接続をダンプした後でこれを実行するとよいでしょう。

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

<!-- You should commit your database schema file to source control so that other new developers on your team may quickly create your application's initial database structure. -->
チームの他の新しい開発者がアプリケーションの初期データベース構造を迅速に作成できるように、データベース スキーマ ファイルをソース管理にコミットする必要があります。

> [!WARNING]
> 移行スカッシングは、MySQL、PostgreSQL、および SQLite データベースでのみ利用可能であり、データベースのコマンドライン クライアントを利用します。スキーマ ダンプはインメモリ SQLite データベースに復元できない場合があります。

<a name="migration-structure"></a>
<!-- ## Migration Structure -->
## Migration Structure

<!-- A migration class contains two methods: `up` and `down`. The `up` method is used to add new tables, columns, or indexes to your database, while the `down` method should reverse the operations performed by the `up` method. -->
移行クラスには、`up` と `down` の 2 つのメソッドが含まれています。 `up` メソッドは、新しいテーブル、列、またはインデックスをデータベースに追加するために使用されますが、`down` メソッドは、`up` メソッドによって実行された操作を元に戻す必要があります。

<!-- Within both of these methods, you may use the Laravel schema builder to expressively create and modify tables. To learn about all of the methods available on the `Schema` builder, [check out its documentation](#creating-tables). For example, the following migration creates a `flights` table: -->
これらの両方のメソッド内で、Laravel スキーマ ビルダを使用して、テーブルを表現的に作成および変更できます。 `Schema` ビルダ、[check out its documentation](#creating-tables) で使用できるすべてのメソッドについて学習するには。たとえば、次の移行では `flights` テーブルが作成されます。

```
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
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
     *
     * @return void
     */
    public function down()
    {
        Schema::drop('flights');
    }
};
```

<a name="setting-the-migration-connection"></a>
<!-- #### Setting The Migration Connection -->
#### Setting The Migration Connection

<!-- If your migration will be interacting with a database connection other than your application's default database connection, you should set the `$connection` property of your migration: -->
移行がアプリケーションのデフォルトのデータベース接続以外のデータベース接続と対話する場合は、移行の `$connection` プロパティを設定する必要があります。

```
/**
 * The database connection that should be used by the migration.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * Run the migrations.
 *
 * @return void
 */
public function up()
{
    //
}
```

<a name="running-migrations"></a>
<!-- ## Running Migrations -->
## Running Migrations

<!-- To run all of your outstanding migrations, execute the `migrate` Artisan command: -->
未処理の移行をすべて実行するには、`migrate` Artisan コマンドを実行します。

```shell
php artisan migrate
```

<!-- If you would like to see which migrations have run thus far, you may use the `migrate:status` Artisan command: -->
これまでにどの移行が実行されたかを確認したい場合は、`migrate:status` Artisan コマンドを使用できます。

```shell
php artisan migrate:status
```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate` command: -->
移行によって実行される SQL ステートメントを実際に実行せずに確認したい場合は、`--pretend` フラグを `migrate` コマンドに指定できます。

```shell
php artisan migrate --pretend
```

<!-- #### Isolating Migration Execution -->
#### Isolating Migration Execution

<!-- If you are deploying your application across multiple servers and running migrations as part of your deployment process, you likely do not want two servers attempting to migrate the database at the same time. To avoid this, you may use the `isolated` option when invoking the `migrate` command. -->
アプリケーションを複数のサーバーにデプロイし、デプロイメント プロセスの一環として移行を実行している場合、2 つのサーバーが同時にデータベースを移行しようとすることは望ましくありません。これを回避するには、`migrate` コマンドを呼び出すときに `isolated` オプションを使用できます。

<!-- When the `isolated` option is provided, Laravel will acquire an atomic lock using your application's cache driver before attempting to run your migrations. All other attempts to run the `migrate` command while that lock is held will not execute; however, the command will still exit with a successful exit status code: -->
`isolated` オプションが指定されている場合、Laravel は移行の実行を試行する前に、アプリケーションのキャッシュドライバを使用してアトミックロックを取得します。ロックが保持されている間に `migrate` コマンドを実行しようとする他の試みはすべて実行されません。ただし、コマンドは引き続き正常終了ステータス コードで終了します。

```shell
php artisan migrate --isolated
```

> [!WARNING]
> この機能を利用するには、アプリケーションが `memcached`、`redis`、`dynamodb`、`database`、`file`、または `array` キャッシュ ドライバをアプリケーションのデフォルト キャッシュ ドライバとして使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

<a name="forcing-migrations-to-run-in-production"></a>
<!-- #### Forcing Migrations To Run In Production -->
#### Forcing Migrations To Run In Production

<!-- Some migration operations are destructive, which means they may cause you to lose data. In order to protect you from running these commands against your production database, you will be prompted for confirmation before the commands are executed. To force the commands to run without a prompt, use the `--force` flag: -->
一部の移行操作は破壊的なものであり、データが失われる可能性があります。運用データベースに対してこれらのコマンドを実行しないようにするために、コマンドを実行する前に確認を求めるメッセージが表示されます。プロンプトを表示せずにコマンドを強制的に実行するには、`--force` フラグを使用します。

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
<!-- ### Rolling Back Migrations -->
### Rolling Back Migrations

<!-- To roll back the latest migration operation, you may use the `rollback` Artisan command. This command rolls back the last "batch" of migrations, which may include multiple migration files: -->
最新の移行操作をロールバックするには、`rollback` Artisan コマンドを使用できます。このコマンドは、移行の最後の「バッチ」をロールバックします。これには複数の移行ファイルが含まれる場合があります。

```shell
php artisan migrate:rollback
```

<!-- You may roll back a limited number of migrations by providing the `step` option to the `rollback` command. For example, the following command will roll back the last five migrations: -->
`step` オプションを `rollback` コマンドに指定すると、限られた数の移行をロールバックできます。たとえば、次のコマンドは最後の 5 つの移行をロールバックします。

```shell
php artisan migrate:rollback --step=5
```

<!-- The `migrate:reset` command will roll back all of your application's migrations: -->
`migrate:reset` コマンドは、アプリケーションのすべての移行をロールバックします。

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
<!-- #### Roll Back & Migrate Using A Single Command -->
#### Roll Back & Migrate Using A Single Command

<!-- The `migrate:refresh` command will roll back all of your migrations and then execute the `migrate` command. This command effectively re-creates your entire database: -->
`migrate:refresh` コマンドは、すべての移行をロールバックしてから、`migrate` コマンドを実行します。このコマンドはデータベース全体を効果的に再作成します。

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

<!-- You may roll back and re-migrate a limited number of migrations by providing the `step` option to the `refresh` command. For example, the following command will roll back and re-migrate the last five migrations: -->
`refresh` コマンドに `step` オプションを指定すると、限られた数の移行をロールバックして再移行できます。たとえば、次のコマンドは、最後の 5 つの移行をロールバックして再移行します。

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
<!-- #### Drop All Tables & Migrate -->
#### Drop All Tables & Migrate

<!-- The `migrate:fresh` command will drop all tables from the database and then execute the `migrate` command: -->
`migrate:fresh` コマンドは、データベースからすべてのテーブルを削除してから、`migrate` コマンドを実行します。

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

> [!WARNING]
> `migrate:fresh` コマンドは、プレフィックスに関係なく、すべてのデータベース テーブルを削除します。他のアプリケーションと共有されるデータベース上で開発する場合、このコマンドは注意して使用する必要があります。

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<a name="creating-tables"></a>
<!-- ### Creating Tables -->
### Creating Tables

<!-- To create a new database table, use the `create` method on the `Schema` facade. The `create` method accepts two arguments: the first is the name of the table, while the second is a closure which receives a `Blueprint` object that may be used to define the new table: -->
新しいデータベース テーブルを作成するには、`Schema` ファサードで `create` メソッドを使用します。 `create` メソッドは 2 つの引数を受け入れます。1 つ目はテーブルの名前で、2 つ目は新しいテーブルの定義に使用できる `Blueprint` オブジェクトを受け取るクロージャです。

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email');
    $table->timestamps();
});
```

<!-- When creating the table, you may use any of the schema builder's [column methods](#creating-columns) to define the table's columns. -->
テーブルを作成するときは、スキーマ ビルダの [column methods](#creating-columns) のいずれかを使用してテーブルの列を定義できます。

<a name="checking-for-table-column-existence"></a>
<!-- #### Checking For Table / Column Existence -->
#### Checking For Table / Column Existence

<!-- You may check for the existence of a table or column using the `hasTable` and `hasColumn` methods: -->
`hasTable` および `hasColumn` メソッドを使用して、テーブルまたは列の存在を確認できます。

```
if (Schema::hasTable('users')) {
    // The "users" table exists...
}

if (Schema::hasColumn('users', 'email')) {
    // The "users" table exists and has an "email" column...
}
```

<a name="database-connection-table-options"></a>
<!-- #### Database Connection & Table Options -->
#### Database Connection & Table Options

<!-- If you want to perform a schema operation on a database connection that is not your application's default connection, use the `connection` method: -->
アプリケーションのデフォルト接続ではないデータベース接続でスキーマ操作を実行する場合は、`connection` メソッドを使用します。

```
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

<!-- In addition, a few other properties and methods may be used to define other aspects of the table's creation. The `engine` property may be used to specify the table's storage engine when using MySQL: -->
さらに、他のいくつかのプロパティとメソッドを使用して、テーブル作成の他の側面を定義することもできます。 `engine` プロパティは、MySQL の使用時にテーブルのストレージ エンジンを指定するために使用できます。

```
Schema::create('users', function (Blueprint $table) {
    $table->engine = 'InnoDB';

    // ...
});
```

<!-- The `charset` and `collation` properties may be used to specify the character set and collation for the created table when using MySQL: -->
`charset` プロパティと `collation` プロパティは、MySQL の使用時に作成されるテーブルの文字セットと照合順序を指定するために使用できます。

```
Schema::create('users', function (Blueprint $table) {
    $table->charset = 'utf8mb4';
    $table->collation = 'utf8mb4_unicode_ci';

    // ...
});
```

<!-- The `temporary` method may be used to indicate that the table should be "temporary". Temporary tables are only visible to the current connection's database session and are dropped automatically when the connection is closed: -->
`temporary` メソッドを使用して、テーブルを「一時的」にする必要があることを示すことができます。一時テーブルは現在の接続のデータベース セッションにのみ表示され、接続が閉じられると自動的に削除されます。

```
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

<!-- If you would like to add a "comment" to a database table, you may invoke the `comment` method on the table instance. Table comments are currently only supported by MySQL and Postgres: -->
データベース テーブルに「コメント」を追加したい場合は、テーブル インスタンスで `comment` メソッドを呼び出します。テーブル コメントは現在、MySQL と Postgres でのみサポートされています。

```
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
<!-- ### Updating Tables -->
### Updating Tables

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives a `Blueprint` instance you may use to add columns or indexes to the table: -->
`Schema` ファサードの `table` メソッドを使用して、既存のテーブルを更新できます。 `create` メソッドと同様に、`table` メソッドは 2 つの引数を受け入れます。テーブルの名前と、テーブルに列またはインデックスを追加するために使用できる `Blueprint` インスタンスを受け取るクロージャです。

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
<!-- ### Renaming / Dropping Tables -->
### Renaming / Dropping Tables

<!-- To rename an existing database table, use the `rename` method: -->
既存のデータベーステーブルの名前を変更するには、`rename` メソッドを使用します。

```
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

<!-- To drop an existing table, you may use the `drop` or `dropIfExists` methods: -->
既存のテーブルを削除するには、`drop` メソッドまたは `dropIfExists` メソッドを使用できます。

```
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
<!-- #### Renaming Tables With Foreign Keys -->
#### Renaming Tables With Foreign Keys

<!-- Before renaming a table, you should verify that any foreign key constraints on the table have an explicit name in your migration files instead of letting Laravel assign a convention based name. Otherwise, the foreign key constraint name will refer to the old table name. -->
テーブルの名前を変更する前に、Laravel に規則に基づいた名前を割り当てるのではなく、テーブルの外部キー制約に明示的な名前が移行ファイルに含まれていることを確認する必要があります。それ以外の場合、外部キー制約名は古いテーブル名を参照します。

<a name="columns"></a>
<!-- ## Columns -->
## Columns

<a name="creating-columns"></a>
<!-- ### Creating Columns -->
### Creating Columns

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives an `Illuminate\Database\Schema\Blueprint` instance you may use to add columns to the table: -->
`Schema` ファサードの `table` メソッドを使用して、既存のテーブルを更新できます。 `create` メソッドと同様に、`table` メソッドは 2 つの引数を受け入れます。テーブルの名前と、テーブルに列を追加するために使用できる `Illuminate\Database\Schema\Blueprint` インスタンスを受け取るクロージャです。

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
<!-- ### Available Column Types -->
### Available Column Types

<!-- The schema builder blueprint offers a variety of methods that correspond to the different types of columns you can add to your database tables. Each of the available methods are listed in the table below: -->
スキーマ ビルダ ブループリントは、データベース テーブルに追加できるさまざまな種類の列に対応するさまざまなメソッドを提供します。使用可能な各メソッドを次の表に示します。

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[binary](#column-method-binary)
[boolean](#column-method-boolean)
[char](#column-method-char)
[dateTimeTz](#column-method-dateTimeTz)
[dateTime](#column-method-dateTime)
[date](#column-method-date)
[decimal](#column-method-decimal)
[double](#column-method-double)
[enum](#column-method-enum)
[float](#column-method-float)
[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[geometryCollection](#column-method-geometryCollection)
[geometry](#column-method-geometry)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[ipAddress](#column-method-ipAddress)
[json](#column-method-json)
[jsonb](#column-method-jsonb)
[lineString](#column-method-lineString)
[longText](#column-method-longText)
[macAddress](#column-method-macAddress)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[mediumText](#column-method-mediumText)
[morphs](#column-method-morphs)
[multiLineString](#column-method-multiLineString)
[multiPoint](#column-method-multiPoint)
[multiPolygon](#column-method-multiPolygon)
[nullableMorphs](#column-method-nullableMorphs)
[nullableTimestamps](#column-method-nullableTimestamps)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)
[point](#column-method-point)
[polygon](#column-method-polygon)
[rememberToken](#column-method-rememberToken)
[set](#column-method-set)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[softDeletesTz](#column-method-softDeletesTz)
[softDeletes](#column-method-softDeletes)
[string](#column-method-string)
[text](#column-method-text)
[timeTz](#column-method-timeTz)
[time](#column-method-time)
[timestampTz](#column-method-timestampTz)
[timestamp](#column-method-timestamp)
[timestampsTz](#column-method-timestampsTz)
[timestamps](#column-method-timestamps)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[tinyText](#column-method-tinyText)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedDecimal](#column-method-unsignedDecimal)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)
[ulidMorphs](#column-method-ulidMorphs)
[uuidMorphs](#column-method-uuidMorphs)
[ulid](#column-method-ulid)
[uuid](#column-method-uuid)
[year](#column-method-year)
-->
[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[binary](#column-method-binary)
[boolean](#column-method-boolean)
[char](#column-method-char)
[dateTimeTz](#column-method-dateTimeTz)
[dateTime](#column-method-dateTime)
[date](#column-method-date)
[decimal](#column-method-decimal)
[double](#column-method-double)
[enum](#column-method-enum)
[float](#column-method-float)
[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[geometryCollection](#column-method-geometryCollection)
[geometry](#column-method-geometry)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[ipAddress](#column-method-ipAddress)
[json](#column-method-json)
[jsonb](#column-method-jsonb)
[lineString](#column-method-lineString)
[longText](#column-method-longText)
[macAddress](#column-method-macAddress)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[mediumText](#column-method-mediumText)
[morphs](#column-method-morphs)
[multiLineString](#column-method-multiLineString)
[multiPoint](#column-method-multiPoint)
[multiPolygon](#column-method-multiPolygon)
[nullableMorphs](#column-method-nullableMorphs)
[nullableTimestamps](#column-method-nullableTimestamps)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)
[point](#column-method-point)
[polygon](#column-method-polygon)
[rememberToken](#column-method-rememberToken)
[set](#column-method-set)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[softDeletesTz](#column-method-softDeletesTz)
[softDeletes](#column-method-softDeletes)
[string](#column-method-string)
[text](#column-method-text)
[timeTz](#column-method-timeTz)
[time](#column-method-time)
[timestampTz](#column-method-timestampTz)
[timestamp](#column-method-timestamp)
[timestampsTz](#column-method-timestampsTz)
[timestamps](#column-method-timestamps)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[tinyText](#column-method-tinyText)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedDecimal](#column-method-unsignedDecimal)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)
[ulidMorphs](#column-method-ulidMorphs)
[uuidMorphs](#column-method-uuidMorphs)
[ulid](#column-method-ulid)
[uuid](#column-method-uuid)
[year](#column-method-year)

<!-- </div> -->
</div>

<a name="column-method-bigIncrements"></a>
<!-- #### `bigIncrements()` -->
#### `bigIncrements()`
<!-- The `bigIncrements` method creates an auto-incrementing `UNSIGNED BIGINT` (primary key) equivalent column: -->
`bigIncrements` メソッドは、自動インクリメントする `UNSIGNED BIGINT` (主キー) と同等の列を作成します。

```
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
<!-- #### `bigInteger()` -->
#### `bigInteger()`
<!-- The `bigInteger` method creates a `BIGINT` equivalent column: -->
`bigInteger` メソッドは、`BIGINT` と同等の列を作成します。

```
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
<!-- #### `binary()` -->
#### `binary()`
<!-- The `binary` method creates a `BLOB` equivalent column: -->
`binary` メソッドは、`BLOB` と同等の列を作成します。

```
$table->binary('photo');
```

<a name="column-method-boolean"></a>
<!-- #### `boolean()` -->
#### `boolean()`
<!-- The `boolean` method creates a `BOOLEAN` equivalent column: -->
`boolean` メソッドは、`BOOLEAN` と同等の列を作成します。

```
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
<!-- #### `char()` -->
#### `char()`
<!-- The `char` method creates a `CHAR` equivalent column with of a given length: -->
`char` メソッドは、指定された長さの `CHAR` と同等の列を作成します。

```
$table->char('name', 100);
```

<a name="column-method-dateTimeTz"></a>
<!-- #### `dateTimeTz()` -->
#### `dateTimeTz()`
<!-- The `dateTimeTz` method creates a `DATETIME` (with timezone) equivalent column with an optional precision (total digits): -->
`dateTimeTz` メソッドは、オプションの精度 (合計桁数) を使用して、`DATETIME` (タイムゾーンあり) と同等の列を作成します。

```
$table->dateTimeTz('created_at', $precision = 0);
```

<a name="column-method-dateTime"></a>
<!-- #### `dateTime()` -->
#### `dateTime()`
<!-- The `dateTime` method creates a `DATETIME` equivalent column with an optional precision (total digits): -->
`dateTime` メソッドは、オプションの精度 (合計桁数) を使用して、`DATETIME` と同等の列を作成します。

```
$table->dateTime('created_at', $precision = 0);
```

<a name="column-method-date"></a>
<!-- #### `date()` -->
#### `date()`
<!-- The `date` method creates a `DATE` equivalent column: -->
`date` メソッドは、`DATE` と同等の列を作成します。

```
$table->date('created_at');
```

<a name="column-method-decimal"></a>
<!-- #### `decimal()` -->
#### `decimal()`
<!-- The `decimal` method creates a `DECIMAL` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`decimal` メソッドは、指定された精度 (合計桁数) と位取り (10 進数の桁数) を持つ `DECIMAL` と同等の列を作成します。

```
$table->decimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-double"></a>
<!-- #### `double()` -->
#### `double()`
<!-- The `double` method creates a `DOUBLE` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`double` メソッドは、指定された精度 (合計桁数) と位取り (10 進数の桁数) を持つ `DOUBLE` と同等の列を作成します。

```
$table->double('amount', 8, 2);
```

<a name="column-method-enum"></a>
<!-- #### `enum()` -->
#### `enum()`
<!-- The `enum` method creates a `ENUM` equivalent column with the given valid values: -->
`enum` メソッドは、指定された有効な値を使用して `ENUM` と同等の列を作成します。

```
$table->enum('difficulty', ['easy', 'hard']);
```

<a name="column-method-float"></a>
<!-- #### `float()` -->
#### `float()`
<!-- The `float` method creates a `FLOAT` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`float` メソッドは、指定された精度 (合計桁数) と位取り (10 進数の桁数) を持つ `FLOAT` と同等の列を作成します。

```
$table->float('amount', 8, 2);
```

<a name="column-method-foreignId"></a>
<!-- #### `foreignId()` -->
#### `foreignId()`
<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column: -->
`foreignId` メソッドは、`UNSIGNED BIGINT` と同等の列を作成します。

```
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
<!-- #### `foreignIdFor()` -->
#### `foreignIdFor()`
<!-- The `foreignIdFor` method adds a `{column}_id UNSIGNED BIGINT` equivalent column for a given model class: -->
`foreignIdFor` メソッドは、指定されたモデル クラスに `{column}_id UNSIGNED BIGINT` と同等の列を追加します。

```
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
<!-- #### `foreignUlid()` -->
#### `foreignUlid()`
<!-- The `foreignUlid` method creates a `ULID` equivalent column: -->
`foreignUlid` メソッドは、`ULID` と同等の列を作成します。

```
$table->foreignUlid('user_id');
```

<a name="column-method-foreignUuid"></a>
<!-- #### `foreignUuid()` -->
#### `foreignUuid()`
<!-- The `foreignUuid` method creates a `UUID` equivalent column: -->
`foreignUuid` メソッドは、`UUID` と同等の列を作成します。

```
$table->foreignUuid('user_id');
```

<a name="column-method-geometryCollection"></a>
<!-- #### `geometryCollection()` -->
#### `geometryCollection()`
<!-- The `geometryCollection` method creates a `GEOMETRYCOLLECTION` equivalent column: -->
`geometryCollection` メソッドは、`GEOMETRYCOLLECTION` と同等の列を作成します。

```
$table->geometryCollection('positions');
```

<a name="column-method-geometry"></a>
<!-- #### `geometry()` -->
#### `geometry()`
<!-- The `geometry` method creates a `GEOMETRY` equivalent column: -->
`geometry` メソッドは、`GEOMETRY` と同等の列を作成します。

```
$table->geometry('positions');
```

<a name="column-method-id"></a>
<!-- #### `id()` -->
#### `id()`
<!-- The `id` method is an alias of the `bigIncrements` method. By default, the method will create an `id` column; however, you may pass a column name if you would like to assign a different name to the column: -->
`id` メソッドは、`bigIncrements` メソッドのエイリアスです。デフォルトでは、このメソッドは `id` 列を作成します。ただし、列に別の名前を割り当てたい場合は、列名を渡すことができます。

```
$table->id();
```

<a name="column-method-increments"></a>
<!-- #### `increments()` -->
#### `increments()`
<!-- The `increments` method creates an auto-incrementing `UNSIGNED INTEGER` equivalent column as a primary key: -->
`increments` メソッドは、自動インクリメントする `UNSIGNED INTEGER` と同等の列を主キーとして作成します。

```
$table->increments('id');
```

<a name="column-method-integer"></a>
<!-- #### `integer()` -->
#### `integer()`
<!-- The `integer` method creates an `INTEGER` equivalent column: -->
`integer` メソッドは、`INTEGER` と同等の列を作成します。

```
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
<!-- #### `ipAddress()` -->
#### `ipAddress()`
<!-- The `ipAddress` method creates a `VARCHAR` equivalent column: -->
`ipAddress` メソッドは、`VARCHAR` と同等の列を作成します。

```
$table->ipAddress('visitor');
```

<a name="column-method-json"></a>
<!-- #### `json()` -->
#### `json()`
<!-- The `json` method creates a `JSON` equivalent column: -->
`json` メソッドは、`JSON` と同等の列を作成します。

```
$table->json('options');
```

<a name="column-method-jsonb"></a>
<!-- #### `jsonb()` -->
#### `jsonb()`
<!-- The `jsonb` method creates a `JSONB` equivalent column: -->
`jsonb` メソッドは、`JSONB` と同等の列を作成します。

```
$table->jsonb('options');
```

<a name="column-method-lineString"></a>
<!-- #### `lineString()` -->
#### `lineString()`
<!-- The `lineString` method creates a `LINESTRING` equivalent column: -->
`lineString` メソッドは、`LINESTRING` と同等の列を作成します。

```
$table->lineString('positions');
```

<a name="column-method-longText"></a>
<!-- #### `longText()` -->
#### `longText()`
<!-- The `longText` method creates a `LONGTEXT` equivalent column: -->
`longText` メソッドは、`LONGTEXT` と同等の列を作成します。

```
$table->longText('description');
```

<a name="column-method-macAddress"></a>
<!-- #### `macAddress()` -->
#### `macAddress()`
<!-- The `macAddress` method creates a column that is intended to hold a MAC address. Some database systems, such as PostgreSQL, have a dedicated column type for this type of data. Other database systems will use a string equivalent column: -->
`macAddress` メソッドは、MAC アドレスを保持するための列を作成します。 PostgreSQL などの一部のデータベース システムには、このタイプのデータ専用の列タイプがあります。他のデータベース システムでは、文字列と同等の列が使用されます。

```
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
<!-- #### `mediumIncrements()` -->
#### `mediumIncrements()`
<!-- The `mediumIncrements` method creates an auto-incrementing `UNSIGNED MEDIUMINT` equivalent column as a primary key: -->
`mediumIncrements` メソッドは、自動インクリメントする `UNSIGNED MEDIUMINT` と同等の列を主キーとして作成します。

```
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
<!-- #### `mediumInteger()` -->
#### `mediumInteger()`
<!-- The `mediumInteger` method creates a `MEDIUMINT` equivalent column: -->
`mediumInteger` メソッドは、`MEDIUMINT` と同等の列を作成します。

```
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
<!-- #### `mediumText()` -->
#### `mediumText()`
<!-- The `mediumText` method creates a `MEDIUMTEXT` equivalent column: -->
`mediumText` メソッドは、`MEDIUMTEXT` と同等の列を作成します。

```
$table->mediumText('description');
```

<a name="column-method-morphs"></a>
<!-- #### `morphs()` -->
#### `morphs()`
<!-- The `morphs` method is a convenience method that adds a `{column}_id` `UNSIGNED BIGINT` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`morphs` メソッドは、`{column}_id` `UNSIGNED BIGINT` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/9.x/eloquent-relationships). In the following example, `taggable_id` and `taggable_type` columns would be created: -->
このメソッドは、多態性 [Eloquent relationship](/docs/9.x/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

```
$table->morphs('taggable');
```

<a name="column-method-multiLineString"></a>
<!-- #### `multiLineString()` -->
#### `multiLineString()`
<!-- The `multiLineString` method creates a `MULTILINESTRING` equivalent column: -->
`multiLineString` メソッドは、`MULTILINESTRING` と同等の列を作成します。

```
$table->multiLineString('positions');
```

<a name="column-method-multiPoint"></a>
<!-- #### `multiPoint()` -->
#### `multiPoint()`
<!-- The `multiPoint` method creates a `MULTIPOINT` equivalent column: -->
`multiPoint` メソッドは、`MULTIPOINT` と同等の列を作成します。

```
$table->multiPoint('positions');
```

<a name="column-method-multiPolygon"></a>
<!-- #### `multiPolygon()` -->
#### `multiPolygon()`
<!-- The `multiPolygon` method creates a `MULTIPOLYGON` equivalent column: -->
`multiPolygon` メソッドは、`MULTIPOLYGON` と同等の列を作成します。

```
$table->multiPolygon('positions');
```

<a name="column-method-nullableTimestamps"></a>
<!-- #### `nullableTimestamps()` -->
#### `nullableTimestamps()`
<!-- The `nullableTimestamps` method is an alias of the [timestamps](#column-method-timestamps) method: -->
`nullableTimestamps` メソッドは、[timestamps](#column-method-timestamps) メソッドのエイリアスです。

```
$table->nullableTimestamps(0);
```

<a name="column-method-nullableMorphs"></a>
<!-- #### `nullableMorphs()` -->
#### `nullableMorphs()`
<!-- The method is similar to the [morphs](#column-method-morphs) method; however, the columns that are created will be "nullable": -->
このメソッドは [morphs](#column-method-morphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

```
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
<!-- #### `nullableUlidMorphs()` -->
#### `nullableUlidMorphs()`
<!-- The method is similar to the [ulidMorphs](#column-method-ulidMorphs) method; however, the columns that are created will be "nullable": -->
このメソッドは [ulidMorphs](#column-method-ulidMorphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

```
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
<!-- #### `nullableUuidMorphs()` -->
#### `nullableUuidMorphs()`
<!-- The method is similar to the [uuidMorphs](#column-method-uuidMorphs) method; however, the columns that are created will be "nullable": -->
このメソッドは [uuidMorphs](#column-method-uuidMorphs) メソッドに似ています。ただし、作成される列は「NULL 可能」になります。

```
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-point"></a>
<!-- #### `point()` -->
#### `point()`
<!-- The `point` method creates a `POINT` equivalent column: -->
`point` メソッドは、`POINT` と同等の列を作成します。

```
$table->point('position');
```

<a name="column-method-polygon"></a>
<!-- #### `polygon()` -->
#### `polygon()`
<!-- The `polygon` method creates a `POLYGON` equivalent column: -->
`polygon` メソッドは、`POLYGON` と同等の列を作成します。

```
$table->polygon('position');
```

<a name="column-method-rememberToken"></a>
<!-- #### `rememberToken()` -->
#### `rememberToken()`
<!-- The `rememberToken` method creates a nullable, `VARCHAR(100)` equivalent column that is intended to store the current "remember me" [authentication token](/docs/9.x/authentication#remembering-users): -->
`rememberToken` メソッドは、現在の「remember me」 [authentication token](/docs/9.x/authentication#remembering-users) を格納するための、null 許容の `VARCHAR(100)` と同等の列を作成します。

```
$table->rememberToken();
```

<a name="column-method-set"></a>
<!-- #### `set()` -->
#### `set()`
<!-- The `set` method creates a `SET` equivalent column with the given list of valid values: -->
`set` メソッドは、指定された有効な値のリストを使用して、`SET` と同等の列を作成します。

```
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
<!-- #### `smallIncrements()` -->
#### `smallIncrements()`
<!-- The `smallIncrements` method creates an auto-incrementing `UNSIGNED SMALLINT` equivalent column as a primary key: -->
`smallIncrements` メソッドは、自動インクリメントする `UNSIGNED SMALLINT` と同等の列を主キーとして作成します。

```
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
<!-- #### `smallInteger()` -->
#### `smallInteger()`
<!-- The `smallInteger` method creates a `SMALLINT` equivalent column: -->
`smallInteger` メソッドは、`SMALLINT` と同等の列を作成します。

```
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
<!-- #### `softDeletesTz()` -->
#### `softDeletesTz()`
<!-- The `softDeletesTz` method adds a nullable `deleted_at` `TIMESTAMP` (with timezone) equivalent column with an optional precision (total digits). This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletesTz` メソッドは、オプションの精度 (合計桁数) を持つ、NULL 許容の `deleted_at` `TIMESTAMP` (タイムゾーンあり) と同等の列を追加します。この列は、Eloquent の「論理的な削除」機能に必要な `deleted_at` タイムスタンプを保存することを目的としています。

```
$table->softDeletesTz($column = 'deleted_at', $precision = 0);
```

<a name="column-method-softDeletes"></a>
<!-- #### `softDeletes()` -->
#### `softDeletes()`
<!-- The `softDeletes` method adds a nullable `deleted_at` `TIMESTAMP` equivalent column with an optional precision (total digits). This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletes` メソッドは、オプションの精度 (合計桁数) を持つ NULL 許容の `deleted_at` `TIMESTAMP` 同等の列を追加します。この列は、Eloquent の「論理的な削除」機能に必要な `deleted_at` タイムスタンプを保存することを目的としています。

```
$table->softDeletes($column = 'deleted_at', $precision = 0);
```

<a name="column-method-string"></a>
<!-- #### `string()` -->
#### `string()`
<!-- The `string` method creates a `VARCHAR` equivalent column of the given length: -->
`string` メソッドは、指定された長さの `VARCHAR` と同等の列を作成します。

```
$table->string('name', 100);
```

<a name="column-method-text"></a>
<!-- #### `text()` -->
#### `text()`
<!-- The `text` method creates a `TEXT` equivalent column: -->
`text` メソッドは、`TEXT` と同等の列を作成します。

```
$table->text('description');
```

<a name="column-method-timeTz"></a>
<!-- #### `timeTz()` -->
#### `timeTz()`
<!-- The `timeTz` method creates a `TIME` (with timezone) equivalent column with an optional precision (total digits): -->
`timeTz` メソッドは、オプションの精度 (合計桁数) を使用して、`TIME` (タイムゾーンあり) と同等の列を作成します。

```
$table->timeTz('sunrise', $precision = 0);
```

<a name="column-method-time"></a>
<!-- #### `time()` -->
#### `time()`
<!-- The `time` method creates a `TIME` equivalent column with an optional precision (total digits): -->
`time` メソッドは、オプションの精度 (合計桁数) を使用して、`TIME` と同等の列を作成します。

```
$table->time('sunrise', $precision = 0);
```

<a name="column-method-timestampTz"></a>
<!-- #### `timestampTz()` -->
#### `timestampTz()`
<!-- The `timestampTz` method creates a `TIMESTAMP` (with timezone) equivalent column with an optional precision (total digits): -->
`timestampTz` メソッドは、オプションの精度 (合計桁数) を使用して、`TIMESTAMP` (タイムゾーンあり) と同等の列を作成します。

```
$table->timestampTz('added_at', $precision = 0);
```

<a name="column-method-timestamp"></a>
<!-- #### `timestamp()` -->
#### `timestamp()`
<!-- The `timestamp` method creates a `TIMESTAMP` equivalent column with an optional precision (total digits): -->
`timestamp` メソッドは、オプションの精度 (合計桁数) を使用して、`TIMESTAMP` と同等の列を作成します。

```
$table->timestamp('added_at', $precision = 0);
```

<a name="column-method-timestampsTz"></a>
<!-- #### `timestampsTz()` -->
#### `timestampsTz()`
<!-- The `timestampsTz` method creates `created_at` and `updated_at` `TIMESTAMP` (with timezone) equivalent columns with an optional precision (total digits): -->
`timestampsTz` メソッドは、オプションの精度 (合計桁数) を使用して、`created_at` および `updated_at` `TIMESTAMP` (タイムゾーン付き) と同等の列を作成します。

```
$table->timestampsTz($precision = 0);
```

<a name="column-method-timestamps"></a>
<!-- #### `timestamps()` -->
#### `timestamps()`
<!-- The `timestamps` method creates `created_at` and `updated_at` `TIMESTAMP` equivalent columns with an optional precision (total digits): -->
`timestamps` メソッドは、オプションの精度 (合計桁数) で、`created_at` および `updated_at` `TIMESTAMP` と同等の列を作成します。

```
$table->timestamps($precision = 0);
```

<a name="column-method-tinyIncrements"></a>
<!-- #### `tinyIncrements()` -->
#### `tinyIncrements()`
<!-- The `tinyIncrements` method creates an auto-incrementing `UNSIGNED TINYINT` equivalent column as a primary key: -->
`tinyIncrements` メソッドは、自動インクリメントする `UNSIGNED TINYINT` と同等の列を主キーとして作成します。

```
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
<!-- #### `tinyInteger()` -->
#### `tinyInteger()`
<!-- The `tinyInteger` method creates a `TINYINT` equivalent column: -->
`tinyInteger` メソッドは、`TINYINT` と同等の列を作成します。

```
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
<!-- #### `tinyText()` -->
#### `tinyText()`
<!-- The `tinyText` method creates a `TINYTEXT` equivalent column: -->
`tinyText` メソッドは、`TINYTEXT` と同等の列を作成します。

```
$table->tinyText('notes');
```

<a name="column-method-unsignedBigInteger"></a>
<!-- #### `unsignedBigInteger()` -->
#### `unsignedBigInteger()`
<!-- The `unsignedBigInteger` method creates an `UNSIGNED BIGINT` equivalent column: -->
`unsignedBigInteger` メソッドは、`UNSIGNED BIGINT` と同等の列を作成します。

```
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedDecimal"></a>
<!-- #### `unsignedDecimal()` -->
#### `unsignedDecimal()`
<!-- The `unsignedDecimal` method creates an `UNSIGNED DECIMAL` equivalent column with an optional precision (total digits) and scale (decimal digits): -->
`unsignedDecimal` メソッドは、オプションの精度 (合計桁数) とスケール (10 進数の桁数) を使用して、`UNSIGNED DECIMAL` と同等の列を作成します。

```
$table->unsignedDecimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-unsignedInteger"></a>
<!-- #### `unsignedInteger()` -->
#### `unsignedInteger()`
<!-- The `unsignedInteger` method creates an `UNSIGNED INTEGER` equivalent column: -->
`unsignedInteger` メソッドは、`UNSIGNED INTEGER` と同等の列を作成します。

```
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
<!-- #### `unsignedMediumInteger()` -->
#### `unsignedMediumInteger()`
<!-- The `unsignedMediumInteger` method creates an `UNSIGNED MEDIUMINT` equivalent column: -->
`unsignedMediumInteger` メソッドは、`UNSIGNED MEDIUMINT` と同等の列を作成します。

```
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
<!-- #### `unsignedSmallInteger()` -->
#### `unsignedSmallInteger()`
<!-- The `unsignedSmallInteger` method creates an `UNSIGNED SMALLINT` equivalent column: -->
`unsignedSmallInteger` メソッドは、`UNSIGNED SMALLINT` と同等の列を作成します。

```
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
<!-- #### `unsignedTinyInteger()` -->
#### `unsignedTinyInteger()`
<!-- The `unsignedTinyInteger` method creates an `UNSIGNED TINYINT` equivalent column: -->
`unsignedTinyInteger` メソッドは、`UNSIGNED TINYINT` と同等の列を作成します。

```
$table->unsignedTinyInteger('votes');
```

<a name="column-method-ulidMorphs"></a>
<!-- #### `ulidMorphs()` -->
#### `ulidMorphs()`
<!-- The `ulidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(26)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`ulidMorphs` メソッドは、`{column}_id` `CHAR(26)` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/9.x/eloquent-relationships) that use ULID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
このメソッドは、ULID 識別子を使用する多態性 [Eloquent relationship](/docs/9.x/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

```
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
<!-- #### `uuidMorphs()` -->
#### `uuidMorphs()`
<!-- The `uuidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(36)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`uuidMorphs` メソッドは、`{column}_id` `CHAR(36)` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/9.x/eloquent-relationships) that use UUID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
このメソッドは、UUID 識別子を使用する多態性 [Eloquent relationship](/docs/9.x/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

```
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
<!-- #### `ulid()` -->
#### `ulid()`
<!-- The `ulid` method creates a `ULID` equivalent column: -->
`ulid` メソッドは、`ULID` と同等の列を作成します。

```
$table->ulid('id');
```

<a name="column-method-uuid"></a>
<!-- #### `uuid()` -->
#### `uuid()`
<!-- The `uuid` method creates a `UUID` equivalent column: -->
`uuid` メソッドは、`UUID` と同等の列を作成します。

```
$table->uuid('id');
```

<a name="column-method-year"></a>
<!-- #### `year()` -->
#### `year()`
<!-- The `year` method creates a `YEAR` equivalent column: -->
`year` メソッドは、`YEAR` と同等の列を作成します。

```
$table->year('birth_year');
```

<a name="column-modifiers"></a>
<!-- ### Column Modifiers -->
### Column Modifiers

<!-- In addition to the column types listed above, there are several column "modifiers" you may use when adding a column to a database table. For example, to make the column "nullable", you may use the `nullable` method: -->
上記の列タイプに加えて、データベース テーブルに列を追加するときに使用できる列「修飾子」がいくつかあります。たとえば、列を「NULL 可能」にするには、`nullable` メソッドを使用します。

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

<!-- The following table contains all of the available column modifiers. This list does not include [index modifiers](#creating-indexes): -->
次の表には、使用可能な列修飾子がすべて含まれています。このリストには、[index modifiers](#creating-indexes) は含まれていません。

<!--
Modifier  |  Description
--------  |  -----------
`->after('column')`  |  Place the column "after" another column (MySQL).
`->autoIncrement()`  |  Set INTEGER columns as auto-incrementing (primary key).
`->charset('utf8mb4')`  |  Specify a character set for the column (MySQL).
`->collation('utf8mb4_unicode_ci')`  |  Specify a collation for the column (MySQL/PostgreSQL/SQL Server).
`->comment('my comment')`  |  Add a comment to a column (MySQL/PostgreSQL).
`->default($value)`  |  Specify a "default" value for the column.
`->first()`  |  Place the column "first" in the table (MySQL).
`->from($integer)`  |  Set the starting value of an auto-incrementing field (MySQL / PostgreSQL).
`->invisible()`  |  Make the column "invisible" to `SELECT *` queries (MySQL).
`->nullable($value = true)`  |  Allow NULL values to be inserted into the column.
`->storedAs($expression)`  |  Create a stored generated column (MySQL / PostgreSQL).
`->unsigned()`  |  Set INTEGER columns as UNSIGNED (MySQL).
`->useCurrent()`  |  Set TIMESTAMP columns to use CURRENT_TIMESTAMP as default value.
`->useCurrentOnUpdate()`  |  Set TIMESTAMP columns to use CURRENT_TIMESTAMP when a record is updated.
`->virtualAs($expression)`  |  Create a virtual generated column (MySQL / PostgreSQL / SQLite).
`->generatedAs($expression)`  |  Create an identity column with specified sequence options (PostgreSQL).
`->always()`  |  Defines the precedence of sequence values over input for an identity column (PostgreSQL).
`->isGeometry()`  |  Set spatial column type to `geometry` - the default type is `geography` (PostgreSQL).
-->
修飾子 |  説明
--------  |  -----------
`->after('column')` |  列を別の列の「後」に配置します (MySQL)。
`->autoIncrement()` |  INTEGER 列を自動インクリメント (主キー) として設定します。
`->charset('utf8mb4')` |  カラムの文字セットを指定します (MySQL)。
`->collation('utf8mb4_unicode_ci')` |  列の照合順序を指定します (MySQL/PostgreSQL/SQL Server)。
`->comment('my comment')` |  列にコメントを追加します (MySQL/PostgreSQL)。
`->default($value)` |  列の「デフォルト」値を指定します。
`->first()` |  テーブル (MySQL) の「最初」に列を配置します。
`->from($integer)` |  自動インクリメントフィールドの開始値を設定します (MySQL / PostgreSQL)。
`->invisible()` |  列を `SELECT *` クエリに対して「非表示」にします (MySQL)。
`->nullable($value = true)` |  NULL 値を列に挿入できるようにします。
`->storedAs($expression)` |  格納された生成列を作成します (MySQL / PostgreSQL)。
`->unsigned()` |  INTEGER 列を UNSIGNED として設定します (MySQL)。
`->useCurrent()` |  デフォルト値として CURRENT_TIMESTAMP を使用するように TIMESTAMP 列を設定します。
`->useCurrentOnUpdate()` |  レコードの更新時に CURRENT_TIMESTAMP を使用するように TIMESTAMP 列を設定します。
`->virtualAs($expression)` |  仮想生成列 (MySQL / PostgreSQL / SQLite) を作成します。
`->generatedAs($expression)` |  シーケンス オプションを指定して ID 列を作成します (PostgreSQL)。
`->always()` |  ID 列の入力に対するシーケンス値の優先順位を定義します (PostgreSQL)。
`->isGeometry()` |  空間列タイプを `geometry` に設定します。デフォルトのタイプは `geography` (PostgreSQL) です。

<a name="default-expressions"></a>
<!-- #### Default Expressions -->
#### Default Expressions

<!-- The `default` modifier accepts a value or an `Illuminate\Database\Query\Expression` instance. Using an `Expression` instance will prevent Laravel from wrapping the value in quotes and allow you to use database specific functions. One situation where this is particularly useful is when you need to assign default values to JSON columns: -->
`default` 修飾子は、値または `Illuminate\Database\Query\Expression` インスタンスを受け入れます。 `Expression` インスタンスを使用すると、Laravel が値を引用符で囲むことがなくなり、データベース固有の関数を使用できるようになります。これが特に役立つ状況の 1 つは、JSON 列にデフォルト値を割り当てる必要がある場合です。

```
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
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
> デフォルトの式のサポートは、データベース ドライバ、データベース バージョン、およびフィールド タイプによって異なります。データベースのドキュメントを参照してください。さらに、生の `default` 式 (`DB::raw` を使用) と、`change` メソッドによる列の変更を組み合わせることはできません。

<a name="column-order"></a>
<!-- #### Column Order -->
#### Column Order

<!-- When using the MySQL database, the `after` method may be used to add columns after an existing column in the schema: -->
MySQL データベースを使用する場合、`after` メソッドを使用して、スキーマ内の既存の列の後に列を追加できます。

```
$table->after('password', function ($table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
<!-- ### Modifying Columns -->
### Modifying Columns

<a name="prerequisites"></a>
<!-- #### Prerequisites -->
#### Prerequisites

<!-- Before modifying a column, you must install the `doctrine/dbal` package using the Composer package manager. The Doctrine DBAL library is used to determine the current state of the column and to create the SQL queries needed to make the requested changes to your column: -->
列を変更する前に、Composer パッケージ マネージャーを使用して `doctrine/dbal` パッケージをインストールする必要があります。 Doctrine DBAL ライブラリは、列の現在の状態を判断し、要求された変更を列に加えるために必要な SQL クエリを作成するために使用されます。

```
composer require doctrine/dbal
```

<!-- If you plan to modify columns created using the `timestamp` method, you must also add the following configuration to your application's `config/database.php` configuration file: -->
`timestamp` メソッドを使用して作成された列を変更する場合は、アプリケーションの `config/database.php` 構成ファイルに次の構成も追加する必要があります。

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> [!WARNING]
> アプリケーションが Microsoft SQL Server を使用している場合は、必ず `doctrine/dbal:^3.0` をインストールしてください。

<a name="updating-column-attributes"></a>
<!-- #### Updating Column Attributes -->
#### Updating Column Attributes

<!-- The `change` method allows you to modify the type and attributes of existing columns. For example, you may wish to increase the size of a `string` column. To see the `change` method in action, let's increase the size of the `name` column from 25 to 50. To accomplish this, we simply define the new state of the column and then call the `change` method: -->
`change` メソッドを使用すると、既存の列のタイプと属性を変更できます。たとえば、`string` 列のサイズを増やしたい場合があります。 `change` メソッドの動作を確認するには、`name` 列のサイズを 25 から 50 に増やしてみましょう。これを実現するには、単に列の新しい状態を定義してから、`change` メソッドを呼び出します。

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

<!-- We could also modify a column to be nullable: -->
列を NULL 可能に変更することもできます。

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->nullable()->change();
});
```

> [!WARNING]
> 次の列タイプを変更できます: `bigInteger`、`binary`、`boolean`、`char`、`date`、`dateTime`、`dateTimeTz`、`decimal`、`double`、 `integer`、`json`、`longText`、`mediumText`、`smallInteger`、`string`、`text`、`time`、`tinyText`、 `unsignedBigInteger`、`unsignedInteger`、`unsignedSmallInteger`、および `uuid`。  `timestamp` 列を変更するには、「[Doctrine type must be registered](#prerequisites)」と入力します。

<a name="renaming-columns"></a>
<!-- ### Renaming Columns -->
### Renaming Columns

<!-- To rename a column, you may use the `renameColumn` method provided by the schema builder: -->
列の名前を変更するには、スキーマ ビルダが提供する `renameColumn` メソッドを使用できます。

```
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="renaming-columns-on-legacy-databases"></a>
<!-- #### Renaming Columns On Legacy Databases -->
#### Renaming Columns On Legacy Databases

<!-- If you are running a database installation older than one of the following releases, you should ensure that you have installed the `doctrine/dbal` library via the Composer package manager before renaming a column: -->
次のリリースのいずれかよりも古いデータベース インストールを実行している場合は、列の名前を変更する前に、Composer パッケージ マネージャーを介して `doctrine/dbal` ライブラリがインストールされていることを確認する必要があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- MySQL < `8.0.3`
- MariaDB < `10.5.2`
- SQLite < `3.25.0`
-->
- MySQL < `8.0.3`
- マリアDB < `10.5.2`
- SQLite < `3.25.0`

<!-- </div> -->
</div>

<a name="dropping-columns"></a>
<!-- ### Dropping Columns -->
### Dropping Columns

<!-- To drop a column, you may use the `dropColumn` method on the schema builder: -->
列を削除するには、スキーマ ビルダで `dropColumn` メソッドを使用できます。

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

<!-- You may drop multiple columns from a table by passing an array of column names to the `dropColumn` method: -->
列名の配列を `dropColumn` メソッドに渡すことで、テーブルから複数の列を削除できます。

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```


<a name="dropping-columns-on-legacy-databases"></a>
<!-- #### Dropping Columns On Legacy Databases -->
#### Dropping Columns On Legacy Databases

<!-- If you are running a version of SQLite prior to `3.35.0`, you must install the `doctrine/dbal` package via the Composer package manager before the `dropColumn` method may be used. Dropping or modifying multiple columns within a single migration while using this package is not supported. -->
`3.35.0` より前のバージョンの SQLite を実行している場合は、`dropColumn` メソッドを使用する前に、Composer パッケージ マネージャーを介して `doctrine/dbal` パッケージをインストールする必要があります。このパッケージの使用中に、1 回の移行内で複数の列を削除または変更することはサポートされていません。

<a name="available-command-aliases"></a>
<!-- #### Available Command Aliases -->
#### Available Command Aliases

<!-- Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below: -->
Laravel は、一般的なタイプの列の削除に関連する便利なメソッドをいくつか提供しています。これらの各方法については、次の表で説明します。

<!--
Command  |  Description
-------  |  -----------
`$table->dropMorphs('morphable');`  |  Drop the `morphable_id` and `morphable_type` columns.
`$table->dropRememberToken();`  |  Drop the `remember_token` column.
`$table->dropSoftDeletes();`  |  Drop the `deleted_at` column.
`$table->dropSoftDeletesTz();`  |  Alias of `dropSoftDeletes()` method.
`$table->dropTimestamps();`  |  Drop the `created_at` and `updated_at` columns.
`$table->dropTimestampsTz();` |  Alias of `dropTimestamps()` method.
-->
コマンド |  説明
-------  |  -----------
`$table->dropMorphs('morphable');` |  `morphable_id` 列と `morphable_type` 列を削除します。
`$table->dropRememberToken();` |  `remember_token` 列を削除します。
`$table->dropSoftDeletes();` |  `deleted_at` 列を削除します。
`$table->dropSoftDeletesTz();` |  `dropSoftDeletes()` メソッドの別名。
`$table->dropTimestamps();` |  `created_at` 列と `updated_at` 列を削除します。
`$table->dropTimestampsTz();` |  `dropTimestamps()` メソッドの別名。

<a name="indexes"></a>
<!-- ## Indexes -->
## Indexes

<a name="creating-indexes"></a>
<!-- ### Creating Indexes -->
### Creating Indexes

<!-- The Laravel schema builder supports several types of indexes. The following example creates a new `email` column and specifies that its values should be unique. To create the index, we can chain the `unique` method onto the column definition: -->
Laravel スキーマ ビルダは、いくつかの種類のインデックスをサポートしています。次の例では、新しい `email` 列を作成し、その値が一意である必要があることを指定します。インデックスを作成するには、`unique` メソッドを列定義に連鎖させます。

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

<!-- Alternatively, you may create the index after defining the column. To do so, you should call the `unique` method on the schema builder blueprint. This method accepts the name of the column that should receive a unique index: -->
あるいは、列を定義した後にインデックスを作成することもできます。これを行うには、スキーマ ビルダ ブループリントで `unique` メソッドを呼び出す必要があります。このメソッドは、一意のインデックスを受け取る列の名前を受け入れます。

```
$table->unique('email');
```

<!-- You may even pass an array of columns to an index method to create a compound (or composite) index: -->
列の配列をインデックス メソッドに渡して、複合 (または複合) インデックスを作成することもできます。

```
$table->index(['account_id', 'created_at']);
```

<!-- When creating an index, Laravel will automatically generate an index name based on the table, column names, and the index type, but you may pass a second argument to the method to specify the index name yourself: -->
インデックスを作成するとき、Laravel はテーブル、列名、インデックスの種類に基づいてインデックス名を自動的に生成しますが、メソッドに 2 番目の引数を渡してインデックス名を自分で指定することもできます。

```
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
<!-- #### Available Index Types -->
#### Available Index Types

<!-- Laravel's schema builder blueprint class provides methods for creating each type of index supported by Laravel. Each index method accepts an optional second argument to specify the name of the index. If omitted, the name will be derived from the names of the table and column(s) used for the index, as well as the index type. Each of the available index methods is described in the table below: -->
Laravel のスキーマ ビルダ ブループリント クラスは、Laravel でサポートされる各タイプのインデックスを作成するためのメソッドを提供します。各インデックス メソッドは、オプションの 2 番目の引数を受け入れてインデックスの名前を指定します。省略した場合、名前はインデックスに使用されるテーブルと列の名前、およびインデックス タイプから派生します。使用可能な各インデックス方法については、次の表で説明します。

<!--
Command  |  Description
-------  |  -----------
`$table->primary('id');`  |  Adds a primary key.
`$table->primary(['id', 'parent_id']);`  |  Adds composite keys.
`$table->unique('email');`  |  Adds a unique index.
`$table->index('state');`  |  Adds an index.
`$table->fullText('body');`  |  Adds a full text index (MySQL/PostgreSQL).
`$table->fullText('body')->language('english');`  |  Adds a full text index of the specified language (PostgreSQL).
`$table->spatialIndex('location');`  |  Adds a spatial index (except SQLite).
-->
コマンド |  説明
-------  |  -----------
`$table->primary('id');` |  主キーを追加します。
`$table->primary(['id', 'parent_id']);` |  複合キーを追加します。
`$table->unique('email');` |  一意のインデックスを追加します。
`$table->index('state');` |  インデックスを追加します。
`$table->fullText('body');` |  全文インデックスを追加します (MySQL/PostgreSQL)。
`$table->fullText('body')->language('english');` |  指定した言語 (PostgreSQL) の全文インデックスを追加します。
`$table->spatialIndex('location');` |  空間インデックスを追加します (SQLite を除く)。

<a name="index-lengths-mysql-mariadb"></a>
<!-- #### Index Lengths & MySQL / MariaDB -->
#### Index Lengths & MySQL / MariaDB

<!-- By default, Laravel uses the `utf8mb4` character set. If you are running a version of MySQL older than the 5.7.7 release or MariaDB older than the 10.2.2 release, you may need to manually configure the default string length generated by migrations in order for MySQL to create indexes for them. You may configure the default string length by calling the `Schema::defaultStringLength` method within the `boot` method of your `App\Providers\AppServiceProvider` class: -->
デフォルトでは、Laravel は `utf8mb4` 文字セットを使用します。 5.7.7 リリースより古いバージョンの MySQL または 10.2.2 リリースより古い MariaDB を実行している場合、MySQL がインデックスを作成できるように、移行によって生成されるデフォルトの文字列の長さを手動で構成する必要がある場合があります。 `App\Providers\AppServiceProvider` クラスの `boot` メソッド内で `Schema::defaultStringLength` メソッドを呼び出すことで、デフォルトの文字列の長さを構成できます。

```
use Illuminate\Support\Facades\Schema;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Schema::defaultStringLength(191);
}
```

<!-- Alternatively, you may enable the `innodb_large_prefix` option for your database. Refer to your database's documentation for instructions on how to properly enable this option. -->
あるいは、データベースの `innodb_large_prefix` オプションを有効にすることもできます。このオプションを適切に有効にする方法については、データベースのドキュメントを参照してください。

<a name="renaming-indexes"></a>
<!-- ### Renaming Indexes -->
### Renaming Indexes

<!-- To rename an index, you may use the `renameIndex` method provided by the schema builder blueprint. This method accepts the current index name as its first argument and the desired name as its second argument: -->
インデックスの名前を変更するには、スキーマ ビルダ ブループリントによって提供される `renameIndex` メソッドを使用できます。このメソッドは、現在のインデックス名を最初の引数として受け入れ、目的の名前を 2 番目の引数として受け入れます。

```
$table->renameIndex('from', 'to')
```

> [!WARNING]
> アプリケーションが SQLite データベースを利用している場合は、`renameIndex` メソッドを使用する前に、Composer パッケージ マネージャーを介して `doctrine/dbal` パッケージをインストールする必要があります。

<a name="dropping-indexes"></a>
<!-- ### Dropping Indexes -->
### Dropping Indexes

<!-- To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples: -->
インデックスを削除するには、インデックスの名前を指定する必要があります。デフォルトでは、Laravel はテーブル名、インデックス付き列の名前、インデックスタイプに基づいてインデックス名を自動的に割り当てます。以下にいくつかの例を示します。

<!--
Command  |  Description
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  Drop a primary key from the "users" table.
`$table->dropUnique('users_email_unique');`  |  Drop a unique index from the "users" table.
`$table->dropIndex('geo_state_index');`  |  Drop a basic index from the "geo" table.
`$table->dropFullText('posts_body_fulltext');`  |  Drop a full text index from the "posts" table.
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  Drop a spatial index from the "geo" table  (except SQLite).
-->
コマンド |  説明
-------  |  -----------
`$table->dropPrimary('users_id_primary');` |  「users」テーブルから主キーを削除します。
`$table->dropUnique('users_email_unique');` |  「users」テーブルから一意のインデックスを削除します。
`$table->dropIndex('geo_state_index');` |  「geo」テーブルから基本インデックスを削除します。
`$table->dropFullText('posts_body_fulltext');` |  「posts」テーブルから全文インデックスを削除します。
`$table->dropSpatialIndex('geo_location_spatialindex');` |  「geo」テーブルから空間インデックスを削除します (SQLite を除く)。

<!-- If you pass an array of columns into a method that drops indexes, the conventional index name will be generated based on the table name, columns, and index type: -->
インデックスを削除するメソッドに列の配列を渡すと、テーブル名、列、インデックス タイプに基づいて従来のインデックス名が生成されます。

```
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a name="foreign-key-constraints"></a>
<!-- ### Foreign Key Constraints -->
### Foreign Key Constraints

<!-- Laravel also provides support for creating foreign key constraints, which are used to force referential integrity at the database level. For example, let's define a `user_id` column on the `posts` table that references the `id` column on a `users` table: -->
Laravel は、データベース レベルで参照整合性を強制するために使用される外部キー制約の作成のサポートも提供します。たとえば、`users` テーブルの `id` 列を参照する `posts` テーブルの `user_id` 列を定義してみましょう。

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

<!-- Since this syntax is rather verbose, Laravel provides additional, terser methods that use conventions to provide a better developer experience. When using the `foreignId` method to create your column, the example above can be rewritten like so: -->
この構文はかなり冗長であるため、Laravel では、より良い開発者エクスペリエンスを提供するために、規則を使用する追加の簡潔なメソッドが提供されています。 `foreignId` メソッドを使用して列を作成する場合、上記の例は次のように書き換えることができます。

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column, while the `constrained` method will use conventions to determine the table and column name being referenced. If your table name does not match Laravel's conventions, you may specify the table name by passing it as an argument to the `constrained` method: -->
`foreignId` メソッドは `UNSIGNED BIGINT` と同等の列を作成しますが、`constrained` メソッドは規則を使用して参照されるテーブルと列の名前を決定します。テーブル名が Laravel の規則と一致しない場合は、引数としてテーブル名を `constrained` メソッドに渡すことでテーブル名を指定できます。

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained('users');
});
```

<!-- You may also specify the desired action for the "on delete" and "on update" properties of the constraint: -->
制約の「削除時」プロパティと「更新時」プロパティに必要なアクションを指定することもできます。

```
$table->foreignId('user_id')
      ->constrained()
      ->onUpdate('cascade')
      ->onDelete('cascade');
```

<!-- An alternative, expressive syntax is also provided for these actions: -->
これらのアクションには、代替の表現力豊かな構文も提供されています。

<!--
Method  |  Description
-------  |  -----------
`$table->cascadeOnUpdate();` | Updates should cascade.
`$table->restrictOnUpdate();`| Updates should be restricted.
`$table->cascadeOnDelete();` | Deletes should cascade.
`$table->restrictOnDelete();`| Deletes should be restricted.
`$table->nullOnDelete();`    | Deletes should set the foreign key value to null.
-->
方法 |  説明
-------  |  -----------
`$table->cascadeOnUpdate();` |更新はカスケードする必要があります。
`$table->restrictOnUpdate();`|更新は制限されるべきです。
`$table->cascadeOnDelete();` |削除はカスケードする必要があります。
`$table->restrictOnDelete();`|削除は制限する必要があります。
`$table->nullOnDelete();` |削除では、外部キーの値を null に設定する必要があります。

<!-- Any additional [column modifiers](#column-modifiers) must be called before the `constrained` method: -->
追加の [column modifiers](#column-modifiers) は、`constrained` メソッドの前に呼び出す必要があります。

```
$table->foreignId('user_id')
      ->nullable()
      ->constrained();
```

<a name="dropping-foreign-keys"></a>
<!-- #### Dropping Foreign Keys -->
#### Dropping Foreign Keys

<!-- To drop a foreign key, you may use the `dropForeign` method, passing the name of the foreign key constraint to be deleted as an argument. Foreign key constraints use the same naming convention as indexes. In other words, the foreign key constraint name is based on the name of the table and the columns in the constraint, followed by a "\_foreign" suffix: -->
外部キーを削除するには、`dropForeign` メソッドを使用して、削除する外部キー制約の名前を引数として渡します。外部キー制約では、インデックスと同じ命名規則が使用されます。つまり、外部キー制約名は、制約内のテーブル名と列名に基づいて、その後に「\_foreign」サフィックスが付加されます。

```
$table->dropForeign('posts_user_id_foreign');
```

<!-- Alternatively, you may pass an array containing the column name that holds the foreign key to the `dropForeign` method. The array will be converted to a foreign key constraint name using Laravel's constraint naming conventions: -->
あるいは、外部キーを保持する列名を含む配列を `dropForeign` メソッドに渡すこともできます。配列は、Laravel の制約命名規則を使用して外部キー制約名に変換されます。

```
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
<!-- #### Toggling Foreign Key Constraints -->
#### Toggling Foreign Key Constraints

<!-- You may enable or disable foreign key constraints within your migrations by using the following methods: -->
次の方法を使用して、移行内で外部キー制約を有効または無効にすることができます。

```
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> [!WARNING]
> SQLite はデフォルトで外部キー制約を無効にします。 SQLite を使用する場合は、移行で SQLite を作成する前に、データベース構成で [enable foreign key support](/docs/9.x/database#configuration) を実行してください。さらに、SQLite はテーブルおよび [not when tables are altered](https://www.sqlite.org/omitted.html) の作成時に外部キーのみをサポートします。

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- For convenience, each migration operation will dispatch an [event](/docs/9.x/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class: -->
便宜上、各移行操作では [event](/docs/9.x/events) がディスパッチされます。次のイベントはすべて、基本 `Illuminate\Database\Events\MigrationEvent` クラスを拡張します。

<!--
 Class | Description
-------|-------
-->
クラス |説明
-------|-------
| `Illuminate\Database\Events\MigrationsStarted` | 移行のバッチが実行されようとしています。 |
| `Illuminate\Database\Events\MigrationsEnded` | 移行のバッチの実行が終了しました。 |
| `Illuminate\Database\Events\MigrationStarted` | 単一の移行が実行されようとしています。 |
| `Illuminate\Database\Events\MigrationEnded` | 1 つの移行の実行が終了しました。 |
| `Illuminate\Database\Events\SchemaDumped` | データベース スキーマ ダンプが完了しました。 |
| `Illuminate\Database\Events\SchemaLoaded` | 既存のデータベース スキーマ ダンプがロードされました。 |

