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

<!-- The Laravel `Schema` [facade](/docs/11.x/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns. -->
Laravel `Schema` [facade](/docs/11.x/facades) は、Laravel でサポートされているすべてのデータベース システムにわたってテーブルを作成および操作するためのデータベースに依存しないサポートを提供します。通常、移行ではこのファサードを使用してデータベースのテーブルと列を作成および変更します。

<a name="generating-migrations"></a>
<!-- ## Generating Migrations -->
## Generating Migrations

<!-- You may use the `make:migration` [Artisan command](/docs/11.x/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations: -->
`make:migration` [Artisan command](/docs/11.x/artisan) を使用してデータベース移行を生成できます。新しい移行は、`database/migrations` ディレクトリに配置されます。各移行ファイル名には、Laravel が移行の順序を決定できるようにするタイムスタンプが含まれています。

```shell
php artisan make:migration create_flights_table
```

<!-- Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually. -->
Laravel は移行の名前を使用して、テーブルの名前と、移行によって新しいテーブルが作成されるかどうかを推測しようとします。 Laravel が移行名からテーブル名を決定できる場合、Laravel は生成された移行ファイルに指定されたテーブルを事前に入力します。それ以外の場合は、移行ファイルにテーブルを手動で指定するだけです。

<!-- If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path. -->
生成された移行のカスタム パスを指定したい場合は、`make:migration` コマンドを実行するときに `--path` オプションを使用できます。指定されたパスは、アプリケーションのベース パスに対する相対パスである必要があります。

> [!NOTE]
> 移行スタブは、[stub publishing](/docs/11.x/artisan#stub-customization) を使用してカスタマイズできます。

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

<!-- When you execute this command, Laravel will write a "schema" file to your application's `database/schema` directory. The schema file's name will correspond to the database connection. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will first execute the SQL statements in the schema file of the database connection you are using. After executing the schema file's SQL statements, Laravel will execute any remaining migrations that were not part of the schema dump. -->
このコマンドを実行すると、Laravel はアプリケーションの `database/schema` ディレクトリに「スキーマ」ファイルを書き込みます。スキーマ ファイルの名前はデータベース接続に対応します。ここで、他の移行が実行されていないときにデータベースを移行しようとすると、Laravel はまず、使用しているデータベース接続のスキーマ ファイル内の SQL ステートメントを実行します。スキーマファイルのSQLステートメントを実行した後、Laravelはスキーマダンプの一部ではなかった残りの移行を実行します。

<!-- If your application's tests use a different database connection than the one you typically use during local development, you should ensure you have dumped a schema file using that database connection so that your tests are able to build your database. You may wish to do this after dumping the database connection you typically use during local development: -->
アプリケーションのテストでローカル開発中に通常使用するデータベース接続とは異なるデータベース接続を使用する場合は、テストでデータベースを構築できるように、そのデータベース接続を使用してスキーマ ファイルをダンプしていることを確認する必要があります。ローカル開発中に通常使用するデータベース接続をダンプした後でこれを実行するとよいでしょう。

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

<!-- You should commit your database schema file to source control so that other new developers on your team may quickly create your application's initial database structure. -->
チームの他の新しい開発者がアプリケーションの初期データベース構造を迅速に作成できるように、データベース スキーマ ファイルをソース管理にコミットする必要があります。

> [!WARNING]
> 移行スカッシングは、MariaDB、MySQL、PostgreSQL、および SQLite データベースでのみ利用可能であり、データベースのコマンドライン クライアントを利用します。

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
<!-- #### Setting the Migration Connection -->
#### Setting the Migration Connection

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
 */
public function up(): void
{
    // ...
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
<!-- #### Forcing Migrations to Run in Production -->
#### Forcing Migrations to Run in Production

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

<!-- You may roll back a specific "batch" of migrations by providing the `batch` option to the `rollback` command, where the `batch` option corresponds to a batch value within your application's `migrations` database table. For example, the following command will roll back all migrations in batch three: -->
`rollback` コマンドに `batch` オプションを指定すると、移行の特定の「バッチ」をロールバックできます。`batch` オプションは、アプリケーションの `migrations` データベース テーブル内のバッチ値に対応します。たとえば、次のコマンドはバッチ 3 のすべての移行をロールバックします。

 ```shell
php artisan migrate:rollback --batch=3
 ```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate:rollback` command: -->
移行によって実行される SQL ステートメントを実際に実行せずに確認したい場合は、`--pretend` フラグを `migrate:rollback` コマンドに指定できます。

```shell
php artisan migrate:rollback --pretend
```

<!-- The `migrate:reset` command will roll back all of your application's migrations: -->
`migrate:reset` コマンドは、アプリケーションのすべての移行をロールバックします。

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
<!-- #### Roll Back and Migrate Using a Single Command -->
#### Roll Back and Migrate Using a Single Command

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
<!-- #### Drop All Tables and Migrate -->
#### Drop All Tables and Migrate

<!-- The `migrate:fresh` command will drop all tables from the database and then execute the `migrate` command: -->
`migrate:fresh` コマンドは、データベースからすべてのテーブルを削除してから、`migrate` コマンドを実行します。

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

<!-- By default, the `migrate:fresh` command only drops tables from the default database connection. However, you may use the `--database` option to specify the database connection that should be migrated. The database connection name should correspond to a connection defined in your application's `database` [configuration file](/docs/11.x/configuration): -->
デフォルトでは、`migrate:fresh` コマンドはデフォルトのデータベース接続からテーブルのみを削除します。ただし、`--database` オプションを使用して、移行するデータベース接続を指定できます。データベース接続名は、アプリケーションの `database` [configuration file](/docs/11.x/configuration) で定義された接続に対応する必要があります。

```shell
php artisan migrate:fresh --database=admin
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

<a name="determining-table-column-existence"></a>
<!-- #### Determining Table / Column Existence -->
#### Determining Table / Column Existence

<!-- You may determine the existence of a table, column, or index using the `hasTable`, `hasColumn`, and `hasIndex` methods: -->
`hasTable`、`hasColumn`、および `hasIndex` メソッドを使用して、テーブル、列、またはインデックスの存在を確認できます。

```
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
<!-- #### Database Connection and Table Options -->
#### Database Connection and Table Options

<!-- If you want to perform a schema operation on a database connection that is not your application's default connection, use the `connection` method: -->
アプリケーションのデフォルト接続ではないデータベース接続でスキーマ操作を実行する場合は、`connection` メソッドを使用します。

```
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

<!-- In addition, a few other properties and methods may be used to define other aspects of the table's creation. The `engine` property may be used to specify the table's storage engine when using MariaDB or MySQL: -->
さらに、他のいくつかのプロパティとメソッドを使用して、テーブル作成の他の側面を定義することもできます。 MariaDB または MySQL を使用する場合、`engine` プロパティを使用してテーブルのストレージ エンジンを指定できます。

```
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

<!-- The `charset` and `collation` properties may be used to specify the character set and collation for the created table when using MariaDB or MySQL: -->
MariaDB または MySQL を使用する場合、`charset` プロパティと `collation` プロパティを使用して、作成されたテーブルの文字セットと照合順序を指定できます。

```
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

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

<!-- If you would like to add a "comment" to a database table, you may invoke the `comment` method on the table instance. Table comments are currently only supported by MariaDB, MySQL, and PostgreSQL: -->
データベース テーブルに「コメント」を追加したい場合は、テーブル インスタンスで `comment` メソッドを呼び出します。テーブル コメントは現在、MariaDB、MySQL、および PostgreSQL でのみサポートされています。

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

<a name="booleans-method-list"></a>
<!-- #### Boolean Types -->
#### Boolean Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!-- [boolean](#column-method-boolean) -->
[boolean](#column-method-boolean)

<!-- </div> -->
</div>

<a name="strings-and-texts-method-list"></a>
<!-- #### String & Text Types -->
#### String & Text Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)
-->
[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

<!-- </div> -->
</div>

<a name="numbers--method-list"></a>
<!-- #### Numeric Types -->
#### Numeric Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
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
-->
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

<!-- </div> -->
</div>

<a name="dates-and-times-method-list"></a>
<!-- #### Date & Time Types -->
#### Date & Time Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
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
-->
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

<!-- </div> -->
</div>

<a name="binaries-method-list"></a>
<!-- #### Binary Types -->
#### Binary Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!-- [binary](#column-method-binary) -->
[binary](#column-method-binary)

<!-- </div> -->
</div>

<a name="object-and-jsons-method-list"></a>
<!-- #### Object & Json Types -->
#### Object & Json Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[json](#column-method-json)
[jsonb](#column-method-jsonb)
-->
[json](#column-method-json)
[jsonb](#column-method-jsonb)

<!-- </div> -->
</div>

<a name="uuids-and-ulids-method-list"></a>
<!-- #### UUID & ULID Types -->
#### UUID & ULID Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)
-->
[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

<!-- </div> -->
</div>

<a name="spatials-method-list"></a>
<!-- #### Spatial Types -->
#### Spatial Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[geography](#column-method-geography)
[geometry](#column-method-geometry)
-->
[geography](#column-method-geography)
[geometry](#column-method-geometry)

<!-- </div> -->
</div>

<!-- #### Relationship Types -->
#### Relationship Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)
-->
[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

<!-- </div> -->
</div>

<a name="spacifics-method-list"></a>
<!-- #### Specialty Types -->
#### Specialty Types

<!-- <div class="collection-method-list" markdown="1"> -->
<div class="collection-method-list" markdown="1">

<!--
[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)
-->
[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

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

<!-- When utilizing MySQL, MariaDB, or SQL Server, you may pass `length` and `fixed` arguments to create `VARBINARY` or `BINARY` equivalent column: -->
MySQL、MariaDB、または SQL Server を利用する場合、`length` および `fixed` 引数を渡して、`VARBINARY` または `BINARY` と同等の列を作成できます。

```
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
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
$table->char('name', length: 100);
```

<a name="column-method-dateTimeTz"></a>
<!-- #### `dateTimeTz()` -->
#### `dateTimeTz()`
<!-- The `dateTimeTz` method creates a `DATETIME` (with timezone) equivalent column with an optional fractional seconds precision: -->
`dateTimeTz` メソッドは、オプションの小数秒精度を持つ `DATETIME` (タイムゾーン付き) と同等の列を作成します。

```
$table->dateTimeTz('created_at', precision: 0);
```

<a name="column-method-dateTime"></a>
<!-- #### `dateTime()` -->
#### `dateTime()`
<!-- The `dateTime` method creates a `DATETIME` equivalent column with an optional fractional seconds precision: -->
`dateTime` メソッドは、オプションの小数秒精度を使用して、`DATETIME` と同等の列を作成します。

```
$table->dateTime('created_at', precision: 0);
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
$table->decimal('amount', total: 8, places: 2);
```

<a name="column-method-double"></a>
<!-- #### `double()` -->
#### `double()`
<!-- The `double` method creates a `DOUBLE` equivalent column: -->
`double` メソッドは、`DOUBLE` と同等の列を作成します。

```
$table->double('amount');
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
<!-- The `float` method creates a `FLOAT` equivalent column with the given precision: -->
`float` メソッドは、指定された精度で `FLOAT` と同等の列を作成します。

```
$table->float('amount', precision: 53);
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
<!-- The `foreignIdFor` method adds a `{column}_id` equivalent column for a given model class. The column type will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type: -->
`foreignIdFor` メソッドは、指定されたモデル クラスに `{column}_id` と同等の列を追加します。列のタイプは、モデルのキーのタイプに応じて、`UNSIGNED BIGINT`、`CHAR(36)`、または `CHAR(26)` になります。

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

<a name="column-method-geography"></a>
<!-- #### `geography()` -->
#### `geography()`
<!-- The `geography` method creates a `GEOGRAPHY` equivalent column with the given spatial type and SRID (Spatial Reference System Identifier): -->
`geography` メソッドは、指定された空間タイプと SRID (空間参照システム識別子) を使用して、`GEOGRAPHY` と同等の列を作成します。

```
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]
> 空間タイプのサポートは、データベース ドライバによって異なります。データベースのドキュメントを参照してください。アプリケーションが PostgreSQL データベースを利用している場合は、`geography` メソッドを使用する前に、[PostGIS](https://postgis.net) 拡張機能をインストールする必要があります。

<a name="column-method-geometry"></a>
<!-- #### `geometry()` -->
#### `geometry()`
<!-- The `geometry` method creates a `GEOMETRY` equivalent column with the given spatial type and SRID (Spatial Reference System Identifier): -->
`geometry` メソッドは、指定された空間タイプと SRID (空間参照システム識別子) を使用して、`GEOMETRY` と同等の列を作成します。

```
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]
> 空間タイプのサポートは、データベース ドライバによって異なります。データベースのドキュメントを参照してください。アプリケーションが PostgreSQL データベースを利用している場合は、`geometry` メソッドを使用する前に、[PostGIS](https://postgis.net) 拡張機能をインストールする必要があります。

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

<!-- When using PostgreSQL, an `INET` column will be created. -->
PostgreSQLを使用する場合、`INET`列が作成されます。

<a name="column-method-json"></a>
<!-- #### `json()` -->
#### `json()`
<!-- The `json` method creates a `JSON` equivalent column: -->
`json` メソッドは、`JSON` と同等の列を作成します。

```
$table->json('options');
```

<!-- When using SQLite, a `TEXT` column will be created. -->
SQLiteを使用する場合、`TEXT`列が作成されます。

<a name="column-method-jsonb"></a>
<!-- #### `jsonb()` -->
#### `jsonb()`
<!-- The `jsonb` method creates a `JSONB` equivalent column: -->
`jsonb` メソッドは、`JSONB` と同等の列を作成します。

```
$table->jsonb('options');
```

<!-- When using SQLite, a `TEXT` column will be created. -->
SQLiteを使用する場合、`TEXT`列が作成されます。

<a name="column-method-longText"></a>
<!-- #### `longText()` -->
#### `longText()`
<!-- The `longText` method creates a `LONGTEXT` equivalent column: -->
`longText` メソッドは、`LONGTEXT` と同等の列を作成します。

```
$table->longText('description');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `LONGBLOB` equivalent column: -->
MySQL または MariaDB を利用する場合、`LONGBLOB` と同等の列を作成するために、`binary` 文字セットを列に適用できます。

```
$table->longText('data')->charset('binary'); // LONGBLOB
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

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `MEDIUMBLOB` equivalent column: -->
MySQL または MariaDB を利用する場合、`MEDIUMBLOB` と同等の列を作成するために、`binary` 文字セットを列に適用できます。

```
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a name="column-method-morphs"></a>
<!-- #### `morphs()` -->
#### `morphs()`
<!-- The `morphs` method is a convenience method that adds a `{column}_id` equivalent column and a `{column}_type` `VARCHAR` equivalent column. The column type for the `{column}_id` will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type. -->
`morphs` メソッドは、`{column}_id` に相当する列と `{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。 `{column}_id` の列タイプは、モデルのキー タイプに応じて、`UNSIGNED BIGINT`、`CHAR(36)`、または `CHAR(26)` になります。

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/11.x/eloquent-relationships). In the following example, `taggable_id` and `taggable_type` columns would be created: -->
このメソッドは、多態性 [Eloquent relationship](/docs/11.x/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

```
$table->morphs('taggable');
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

<a name="column-method-rememberToken"></a>
<!-- #### `rememberToken()` -->
#### `rememberToken()`
<!-- The `rememberToken` method creates a nullable, `VARCHAR(100)` equivalent column that is intended to store the current "remember me" [authentication token](/docs/11.x/authentication#remembering-users): -->
`rememberToken` メソッドは、現在の「remember me」 [authentication token](/docs/11.x/authentication#remembering-users) を格納するための、null 許容の `VARCHAR(100)` と同等の列を作成します。

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
<!-- The `softDeletesTz` method adds a nullable `deleted_at` `TIMESTAMP` (with timezone) equivalent column with an optional fractional seconds precision. This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletesTz` メソッドは、オプションの小数秒精度を持つ、NULL 許容の `deleted_at` `TIMESTAMP` (タイムゾーンあり) と同等の列を追加します。この列は、Eloquent の「論理的な削除」機能に必要な `deleted_at` タイムスタンプを保存することを目的としています。

```
$table->softDeletesTz('deleted_at', precision: 0);
```

<a name="column-method-softDeletes"></a>
<!-- #### `softDeletes()` -->
#### `softDeletes()`
<!-- The `softDeletes` method adds a nullable `deleted_at` `TIMESTAMP` equivalent column with an optional fractional seconds precision. This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletes` メソッドは、オプションの小数秒精度を持つ、NULL 許容の `deleted_at` `TIMESTAMP` 同等の列を追加します。この列は、Eloquent の「論理的な削除」機能に必要な `deleted_at` タイムスタンプを保存することを目的としています。

```
$table->softDeletes('deleted_at', precision: 0);
```

<a name="column-method-string"></a>
<!-- #### `string()` -->
#### `string()`
<!-- The `string` method creates a `VARCHAR` equivalent column of the given length: -->
`string` メソッドは、指定された長さの `VARCHAR` と同等の列を作成します。

```
$table->string('name', length: 100);
```

<a name="column-method-text"></a>
<!-- #### `text()` -->
#### `text()`
<!-- The `text` method creates a `TEXT` equivalent column: -->
`text` メソッドは、`TEXT` と同等の列を作成します。

```
$table->text('description');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `BLOB` equivalent column: -->
MySQL または MariaDB を利用する場合、`BLOB` と同等の列を作成するために、`binary` 文字セットを列に適用できます。

```
$table->text('data')->charset('binary'); // BLOB
```

<a name="column-method-timeTz"></a>
<!-- #### `timeTz()` -->
#### `timeTz()`
<!-- The `timeTz` method creates a `TIME` (with timezone) equivalent column with an optional fractional seconds precision: -->
`timeTz` メソッドは、オプションの小数秒精度を持つ `TIME` (タイムゾーン付き) と同等の列を作成します。

```
$table->timeTz('sunrise', precision: 0);
```

<a name="column-method-time"></a>
<!-- #### `time()` -->
#### `time()`
<!-- The `time` method creates a `TIME` equivalent column with an optional fractional seconds precision: -->
`time` メソッドは、オプションの小数秒精度を使用して、`TIME` と同等の列を作成します。

```
$table->time('sunrise', precision: 0);
```

<a name="column-method-timestampTz"></a>
<!-- #### `timestampTz()` -->
#### `timestampTz()`
<!-- The `timestampTz` method creates a `TIMESTAMP` (with timezone) equivalent column with an optional fractional seconds precision: -->
`timestampTz` メソッドは、オプションの小数秒精度を持つ `TIMESTAMP` (タイムゾーン付き) と同等の列を作成します。

```
$table->timestampTz('added_at', precision: 0);
```

<a name="column-method-timestamp"></a>
<!-- #### `timestamp()` -->
#### `timestamp()`
<!-- The `timestamp` method creates a `TIMESTAMP` equivalent column with an optional fractional seconds precision: -->
`timestamp` メソッドは、オプションの小数秒精度を使用して、`TIMESTAMP` と同等の列を作成します。

```
$table->timestamp('added_at', precision: 0);
```

<a name="column-method-timestampsTz"></a>
<!-- #### `timestampsTz()` -->
#### `timestampsTz()`
<!-- The `timestampsTz` method creates `created_at` and `updated_at` `TIMESTAMP` (with timezone) equivalent columns with an optional fractional seconds precision: -->
`timestampsTz` メソッドは、オプションの小数秒精度を使用して、`created_at` および `updated_at` `TIMESTAMP` (タイムゾーン付き) と同等の列を作成します。

```
$table->timestampsTz(precision: 0);
```

<a name="column-method-timestamps"></a>
<!-- #### `timestamps()` -->
#### `timestamps()`
<!-- The `timestamps` method creates `created_at` and `updated_at` `TIMESTAMP` equivalent columns with an optional fractional seconds precision: -->
`timestamps` メソッドは、オプションの小数秒精度を使用して、`created_at` および `updated_at` `TIMESTAMP` と同等の列を作成します。

```
$table->timestamps(precision: 0);
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

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `TINYBLOB` equivalent column: -->
MySQL または MariaDB を利用する場合、`TINYBLOB` と同等の列を作成するために、`binary` 文字セットを列に適用できます。

```
$table->tinyText('data')->charset('binary'); // TINYBLOB
```

<a name="column-method-unsignedBigInteger"></a>
<!-- #### `unsignedBigInteger()` -->
#### `unsignedBigInteger()`
<!-- The `unsignedBigInteger` method creates an `UNSIGNED BIGINT` equivalent column: -->
`unsignedBigInteger` メソッドは、`UNSIGNED BIGINT` と同等の列を作成します。

```
$table->unsignedBigInteger('votes');
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

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/11.x/eloquent-relationships) that use ULID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
このメソッドは、ULID 識別子を使用する多態性 [Eloquent relationship](/docs/11.x/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

```
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
<!-- #### `uuidMorphs()` -->
#### `uuidMorphs()`
<!-- The `uuidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(36)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`uuidMorphs` メソッドは、`{column}_id` `CHAR(36)` に相当する列と、`{column}_type` `VARCHAR` に相当する列を追加する便利なメソッドです。

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/11.x/eloquent-relationships) that use UUID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
このメソッドは、UUID 識別子を使用する多態性 [Eloquent relationship](/docs/11.x/eloquent-relationships) に必要な列を定義するときに使用することを目的としています。次の例では、`taggable_id` 列と `taggable_type` 列が作成されます。

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

<a name="column-method-vector"></a>
<!-- #### `vector()` -->
#### `vector()`
<!-- The `vector` method creates a `vector` equivalent column: -->
`vector` メソッドは、`vector` と同等の列を作成します。

```
$table->vector('embedding', dimensions: 100);
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

<!-- <div class="overflow-auto"> -->
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
| `->invisible()`                     | 列を `SELECT *` クエリに対して「非表示」にします (MariaDB / MySQL)。                           |
| `->nullable($value = true)`         | `NULL` 値を列に挿入できるようにします。                                            |
| `->storedAs($expression)`           | 格納された生成列 (MariaDB / MySQL / PostgreSQL / SQLite) を作成します。                      |
| `->unsigned()`                      | `INTEGER` 列を `UNSIGNED` (MariaDB / MySQL) として設定します。                                         |
| `->useCurrent()`                    | `TIMESTAMP` 列をデフォルト値として `CURRENT_TIMESTAMP` を使用するように設定します。                           |
| `->useCurrentOnUpdate()`            | レコードの更新時に `CURRENT_TIMESTAMP` を使用するように `TIMESTAMP` 列を設定します (MariaDB / MySQL)。 |
| `->virtualAs($expression)`          | 仮想生成列 (MariaDB / MySQL / SQLite) を作成します。                                  |
| `->generatedAs($expression)`        | シーケンス オプションを指定して ID 列を作成します (PostgreSQL)。                        |
| `->always()`                        | ID 列の入力に対するシーケンス値の優先順位を定義します (PostgreSQL)。      |

<!-- </div> -->
</div>

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
<!-- #### Column Order -->
#### Column Order

<!-- When using the MariaDB or MySQL database, the `after` method may be used to add columns after an existing column in the schema: -->
MariaDB または MySQL データベースを使用する場合、`after` メソッドを使用して、スキーマ内の既存の列の後に列を追加できます。

```
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
<!-- ### Modifying Columns -->
### Modifying Columns

<!-- The `change` method allows you to modify the type and attributes of existing columns. For example, you may wish to increase the size of a `string` column. To see the `change` method in action, let's increase the size of the `name` column from 25 to 50. To accomplish this, we simply define the new state of the column and then call the `change` method: -->
`change` メソッドを使用すると、既存の列のタイプと属性を変更できます。たとえば、`string` 列のサイズを増やしたい場合があります。 `change` メソッドの動作を確認するには、`name` 列のサイズを 25 から 50 に増やしてみましょう。これを実現するには、単に列の新しい状態を定義してから、`change` メソッドを呼び出します。

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

<!-- When modifying a column, you must explicitly include all the modifiers you want to keep on the column definition - any missing attribute will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column: -->
列を変更するときは、列定義に保持したいすべての修飾子を明示的に含める必要があります。欠落している属性は削除されます。たとえば、`unsigned`、`default`、および `comment` 属性を保持するには、列を変更するときに各修飾子を明示的に呼び出す必要があります。

```
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

<!-- The `change` method does not change the indexes of the column. Therefore, you may use index modifiers to explicitly add or drop an index when modifying the column: -->
`change` メソッドは列のインデックスを変更しません。したがって、列を変更するときにインデックス修飾子を使用してインデックスを明示的に追加または削除できます。

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

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

<a name="available-command-aliases"></a>
<!-- #### Available Command Aliases -->
#### Available Command Aliases

<!-- Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below: -->
Laravel は、一般的なタイプの列の削除に関連する便利なメソッドをいくつか提供しています。これらの各方法については、次の表で説明します。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 指示                             | 説明                                           |
| ----------------------------------- | ----------------------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_id` 列と `morphable_type` 列を削除します。 |
| `$table->dropRememberToken();`      | `remember_token` 列を削除します。                     |
| `$table->dropSoftDeletes();`        | `deleted_at` 列を削除します。                         |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()` メソッドの別名。                  |
| `$table->dropTimestamps();`         | `created_at` 列と `updated_at` 列を削除します。       |
| `$table->dropTimestampsTz();`       | `dropTimestamps()` メソッドの別名。                   |

<!-- </div> -->
</div>

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

<!-- <div class="overflow-auto"> -->
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

<!-- </div> -->
</div>

<a name="renaming-indexes"></a>
<!-- ### Renaming Indexes -->
### Renaming Indexes

<!-- To rename an index, you may use the `renameIndex` method provided by the schema builder blueprint. This method accepts the current index name as its first argument and the desired name as its second argument: -->
インデックスの名前を変更するには、スキーマ ビルダ ブループリントによって提供される `renameIndex` メソッドを使用できます。このメソッドは、現在のインデックス名を最初の引数として受け入れ、目的の名前を 2 番目の引数として受け入れます。

```
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
<!-- ### Dropping Indexes -->
### Dropping Indexes

<!-- To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples: -->
インデックスを削除するには、インデックスの名前を指定する必要があります。デフォルトでは、Laravel はテーブル名、インデックス付き列の名前、インデックスタイプに基づいてインデックス名を自動的に割り当てます。以下にいくつかの例を示します。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 指示                                                  | 説明                                                 |
| -------------------------------------------------------- | ----------------------------------------------------------- |
| `$table->dropPrimary('users_id_primary');`               | 「users」テーブルから主キーを削除します。                  |
| `$table->dropUnique('users_email_unique');`              | 「users」テーブルから一意のインデックスを削除します。                 |
| `$table->dropIndex('geo_state_index');`                  | 「geo」テーブルから基本インデックスを削除します。                    |
| `$table->dropFullText('posts_body_fulltext');`           | 「posts」テーブルから全文インデックスを削除します。              |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | 「geo」テーブルから空間インデックスを削除します (SQLite を除く)。 |

<!-- </div> -->
</div>

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

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column, while the `constrained` method will use conventions to determine the table and column being referenced. If your table name does not match Laravel's conventions, you may manually provide it to the `constrained` method. In addition, the name that should be assigned to the generated index may be specified as well: -->
`foreignId` メソッドは `UNSIGNED BIGINT` と同等の列を作成しますが、`constrained` メソッドは規則を使用して参照されるテーブルと列を決定します。テーブル名が Laravel の規則と一致しない場合は、それを `constrained` メソッドに手動で指定できます。さらに、生成されたインデックスに割り当てる名前も指定できます。

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
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

<!-- <div class="overflow-auto"> -->
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

<!-- </div> -->
</div>

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
> SQLite はデフォルトで外部キー制約を無効にします。 SQLite を使用する場合は、移行で SQLite を作成する前に、データベース構成で [enable foreign key support](/docs/11.x/database#configuration) を実行してください。

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- For convenience, each migration operation will dispatch an [event](/docs/11.x/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class: -->
便宜上、各移行操作では [event](/docs/11.x/events) がディスパッチされます。次のイベントはすべて、基本 `Illuminate\Database\Events\MigrationEvent` クラスを拡張します。

<!-- <div class="overflow-auto"> -->
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

<!-- </div> -->
</div>

