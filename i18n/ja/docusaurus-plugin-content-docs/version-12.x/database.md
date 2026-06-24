<!-- # Database: Getting Started -->
# Database: Getting Started

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [Read and Write Connections](#read-and-write-connections)
- [Running SQL Queries](#running-queries)
    - [Using Multiple Database Connections](#using-multiple-database-connections)
    - [Listening for Query Events](#listening-for-query-events)
    - [Monitoring Cumulative Query Time](#monitoring-cumulative-query-time)
- [Database Transactions](#database-transactions)
- [Connecting to the Database CLI](#connecting-to-the-database-cli)
- [Inspecting Your Databases](#inspecting-your-databases)
- [Monitoring Your Databases](#monitoring-your-databases)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Almost every modern web application interacts with a database. Laravel makes interacting with databases extremely simple across a variety of supported databases using raw SQL, a [fluent query builder](/docs/12.x/queries), and the [Eloquent ORM](/docs/12.x/eloquent). Currently, Laravel provides first-party support for five databases: -->
ほとんどすべての最新の Web アプリケーションはデータベースと対話します。 Laravel では、生の SQL、[fluent query builder](/docs/12.x/queries)、および [Eloquent ORM](/docs/12.x/eloquent) を使用して、サポートされているさまざまなデータベース間でデータベースとの対話を非常に簡単にします。現在、Laravel は次の 5 つのデータベースのファーストパーティ サポートを提供しています。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- MariaDB 10.3+ ([Version Policy](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([Version Policy](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([Version Policy](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([Version Policy](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))
-->
- MariaDB 10.3+ ([Version Policy](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([Version Policy](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([Version Policy](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([Version Policy](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

<!-- </div> -->
</div>

<!-- Additionally, MongoDB is supported via the `mongodb/laravel-mongodb` package, which is officially maintained by MongoDB. Check out the [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) documentation for more information. -->
さらに、MongoDB は、MongoDB によって公式に保守されている `mongodb/laravel-mongodb` パッケージを通じてサポートされています。詳細については、[Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) のドキュメントを参照してください。

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- The configuration for Laravel's database services is located in your application's `config/database.php` configuration file. In this file, you may define all of your database connections, as well as specify which connection should be used by default. Most of the configuration options within this file are driven by the values of your application's environment variables. Examples for most of Laravel's supported database systems are provided in this file. -->
Laravel のデータベース サービスの設定は、アプリケーションの `config/database.php` 設定ファイルにあります。このファイルでは、すべてのデータベース接続を定義したり、デフォルトで使用する接続を指定したりできます。このファイル内の構成オプションのほとんどは、アプリケーションの環境変数の値によって決まります。 Laravel でサポートされているほとんどのデータベース システムの例は、このファイルで提供されています。

<!-- By default, Laravel's sample [environment configuration](/docs/12.x/configuration#environment-configuration) is ready to use with [Laravel Sail](/docs/12.x/sail), which is a Docker configuration for developing Laravel applications on your local machine. However, you are free to modify your database configuration as needed for your local database. -->
デフォルトでは、Laravel のサンプル [environment configuration](/docs/12.x/configuration#environment-configuration) は、ローカル マシン上で Laravel アプリケーションを開発するための Docker 構成である [Laravel Sail](/docs/12.x/sail) で使用する準備ができています。ただし、ローカル データベースの必要に応じてデータベース構成を自由に変更できます。

<a name="sqlite-configuration"></a>
<!-- #### SQLite Configuration -->
#### SQLite Configuration

<!-- SQLite databases are contained within a single file on your filesystem. You can create a new SQLite database using the `touch` command in your terminal: `touch database/database.sqlite`. After the database has been created, you may easily configure your environment variables to point to this database by placing the absolute path to the database in the `DB_DATABASE` environment variable: -->
SQLite データベースは、ファイル システム上の単一のファイル内に含まれています。ターミナルで `touch` コマンド `touch database/database.sqlite` を使用して、新しい SQLite データベースを作成できます。データベースの作成後、`DB_DATABASE` 環境変数にデータベースへの絶対パスを指定することで、このデータベースを指すように環境変数を簡単に構成できます。

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

<!-- By default, foreign key constraints are enabled for SQLite connections. If you would like to disable them, you should set the `DB_FOREIGN_KEYS` environment variable to `false`: -->
デフォルトでは、SQLite 接続に対して外部キー制約が有効になっています。それらを無効にしたい場合は、`DB_FOREIGN_KEYS` 環境変数を `false` に設定する必要があります。

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel installer](/docs/12.x/installation#creating-a-laravel-project) を使用して Laravel アプリケーションを作成し、データベースとして SQLite を選択した場合、Laravel は自動的に `database/database.sqlite` ファイルを作成し、デフォルトの [database migrations](/docs/12.x/migrations) を実行します。

<a name="mssql-configuration"></a>
<!-- #### Microsoft SQL Server Configuration -->
#### Microsoft SQL Server Configuration

<!-- To use a Microsoft SQL Server database, you should ensure that you have the `sqlsrv` and `pdo_sqlsrv` PHP extensions installed as well as any dependencies they may require such as the Microsoft SQL ODBC driver. -->
Microsoft SQL Server データベースを使用するには、`sqlsrv` および `pdo_sqlsrv` PHP 拡張機能と、Microsoft SQL ODBC ドライバなどの必要な依存関係がインストールされていることを確認する必要があります。

<a name="configuration-using-urls"></a>
<!-- #### Configuration Using URLs -->
#### Configuration Using URLs

<!-- Typically, database connections are configured using multiple configuration values such as `host`, `database`, `username`, `password`, etc. Each of these configuration values has its own corresponding environment variable. This means that when configuring your database connection information on a production server, you need to manage several environment variables. -->
通常、データベース接続は、`host`、`database`、`username`、`password` などの複数の構成値を使用して構成されます。これらの各構成値には、対応する独自の環境変数があります。つまり、運用サーバーでデータベース接続情報を構成する場合は、いくつかの環境変数を管理する必要があります。

<!-- Some managed database providers such as AWS and Heroku provide a single database "URL" that contains all of the connection information for the database in a single string. An example database URL may look something like the following: -->
AWS や Heroku などの一部のマネージド データベース プロバイダは、データベースのすべての接続情報を単一の文字列に含む単一のデータベース "URL" を提供します。データベース URL の例は次のようになります。

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

<!-- These URLs typically follow a standard schema convention: -->
これらの URL は通常、標準のスキーマ規則に従っています。

```html
driver://username:password@host:port/database?options
```

<!-- For convenience, Laravel supports these URLs as an alternative to configuring your database with multiple configuration options. If the `url` (or corresponding `DB_URL` environment variable) configuration option is present, it will be used to extract the database connection and credential information. -->
便宜上、Laravel は複数の構成オプションを使用してデータベースを構成する代わりに、これらの URL をサポートしています。 `url` (または対応する `DB_URL` 環境変数) 構成オプションが存在する場合、データベース接続と資格情報の抽出に使用されます。

<a name="read-and-write-connections"></a>
<!-- ### Read and Write Connections -->
### Read and Write Connections

<!-- Sometimes you may wish to use one database connection for SELECT statements, and another for INSERT, UPDATE, and DELETE statements. Laravel makes this a breeze, and the proper connections will always be used whether you are using raw queries, the query builder, or the Eloquent ORM. -->
場合によっては、あるデータベース接続を SELECT ステートメントに使用し、別のデータベース接続を INSERT、UPDATE、および DELETE ステートメントに使用したい場合があります。 Laravel を使用するとこれが簡単になり、生のクエリ、クエリビルダ、または Eloquent ORM を使用しているかどうかに関係なく、常に適切な接続が使用されます。

<!-- To see how read / write connections should be configured, let's look at this example: -->
読み取り/書き込み接続をどのように構成する必要があるかを確認するには、次の例を見てみましょう。

```php
'mysql' => [
    'driver' => 'mysql',

    'read' => [
        'host' => [
            '192.168.1.1',
            '196.168.1.2',
        ],
    ],
    'write' => [
        'host' => [
            '192.168.1.3',
        ],
    ],
    'sticky' => true,

    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'laravel'),
    'username' => env('DB_USERNAME', 'root'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => env('DB_CHARSET', 'utf8mb4'),
    'collation' => env('DB_COLLATION', 'utf8mb4_unicode_ci'),
    'prefix' => '',
    'prefix_indexes' => true,
    'strict' => true,
    'engine' => null,
    'options' => extension_loaded('pdo_mysql') ? array_filter([
        (PHP_VERSION_ID >= 80500 ? \Pdo\Mysql::ATTR_SSL_CA : \PDO::MYSQL_ATTR_SSL_CA) => env('MYSQL_ATTR_SSL_CA'),
    ]) : [],
],
```

<!-- Note that three keys have been added to the configuration array: `read`, `write` and `sticky`. The `read` and `write` keys have array values containing a single key: `host`. The rest of the database options for the `read` and `write` connections will be merged from the main `mysql` configuration array. -->
3 つのキー (`read`、`write`、および `sticky`) が構成配列に追加されていることに注意してください。 `read` キーと `write` キーには、単一のキー `host` を含む配列値があります。 `read` および `write` 接続の残りのデータベース オプションは、メインの `mysql` 構成配列からマージされます。

<!-- You only need to place items in the `read` and `write` arrays if you wish to override the values from the main `mysql` array. So, in this case, `192.168.1.1` will be used as the host for the "read" connection, while `192.168.1.3` will be used for the "write" connection. The database credentials, prefix, character set, and all other options in the main `mysql` array will be shared across both connections. When multiple values exist in the `host` configuration array, a database host will be randomly chosen for each request. -->
メインの `mysql` 配列の値をオーバーライドする場合は、`read` 配列と `write` 配列に項目を配置するだけで済みます。したがって、この場合、`192.168.1.1` は「読み取り」接続のホストとして使用され、`192.168.1.3` は「書き込み」接続に使用されます。メインの `mysql` 配列内のデータベース資格情報、プレフィックス、文字セット、およびその他のすべてのオプションは、両方の接続間で共有されます。 `host` 構成配列に複数の値が存在する場合、リクエストごとにデータベース ホストがランダムに選択されます。

<a name="the-sticky-option"></a>
<!-- #### The `sticky` Option -->
#### The `sticky` Option

<!-- The `sticky` option is an *optional* value that can be used to allow the immediate reading of records that have been written to the database during the current request cycle. If the `sticky` option is enabled and a "write" operation has been performed against the database during the current request cycle, any further "read" operations will use the "write" connection. This ensures that any data written during the request cycle can be immediately read back from the database during that same request. It is up to you to decide if this is the desired behavior for your application. -->
`sticky` オプションは、現在のリクエスト サイクル中にデータベースに書き込まれたレコードの即時読み取りを許可するために使用できる *オプション* の値です。 `sticky` オプションが有効で、現在のリクエスト サイクル中にデータベースに対して「書き込み」操作が実行された場合、それ以降の「読み取り」操作では「書き込み」接続が使用されます。これにより、リクエスト サイクル中に書き込まれたデータは、同じリクエスト中にデータベースから即座に読み戻されることが保証されます。これがアプリケーションにとって望ましい動作であるかどうかを判断するのはあなた次第です。

<a name="running-queries"></a>
<!-- ## Running SQL Queries -->
## Running SQL Queries

<!-- Once you have configured your database connection, you may run queries using the `DB` facade. The `DB` facade provides methods for each type of query: `select`, `update`, `insert`, `delete`, and `statement`. -->
データベース接続を構成したら、`DB` ファサードを使用してクエリを実行できます。 `DB` ファサードは、`select`、`update`、`insert`、`delete`、および `statement` の各タイプのクエリのメソッドを提供します。

<a name="running-a-select-query"></a>
<!-- #### Running a Select Query -->
#### Running a Select Query

<!-- To run a basic SELECT query, you may use the `select` method on the `DB` facade: -->
基本的な SELECT クエリを実行するには、`DB` ファサードで `select` メソッドを使用できます。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```

<!-- The first argument passed to the `select` method is the SQL query, while the second argument is any parameter bindings that need to be bound to the query. Typically, these are the values of the `where` clause constraints. Parameter binding provides protection against SQL injection. -->
`select` メソッドに渡される最初の引数は SQL クエリで、2 番目の引数はクエリにバインドする必要があるパラメータ バインディングです。通常、これらは `where` 句制約の値です。パラメーター バインディングにより、SQL インジェクションに対する保護が提供されます。

<!-- The `select` method will always return an `array` of results. Each result within the array will be a PHP `stdClass` object representing a record from the database: -->
`select` メソッドは常に `array` の結果を返します。配列内の各結果は、データベースからのレコードを表す PHP `stdClass` オブジェクトになります。

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
<!-- #### Selecting Scalar Values -->
#### Selecting Scalar Values

<!-- Sometimes your database query may result in a single, scalar value. Instead of being required to retrieve the query's scalar result from a record object, Laravel allows you to retrieve this value directly using the `scalar` method: -->
場合によっては、データベース クエリの結果が単一のスカラー値になることがあります。 Laravel では、レコード オブジェクトからクエリのスカラー結果を取得する必要があるのではなく、`scalar` メソッドを使用してこの値を直接取得できます。

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
<!-- #### Selecting Multiple Result Sets -->
#### Selecting Multiple Result Sets

<!-- If your application calls stored procedures that return multiple result sets, you may use the `selectResultSets` method to retrieve all of the result sets returned by the stored procedure: -->
アプリケーションが複数の結果セットを返すストアド プロシージャを呼び出す場合、`selectResultSets` メソッドを使用して、ストアド プロシージャによって返されるすべての結果セットを取得できます。

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
<!-- #### Using Named Bindings -->
#### Using Named Bindings

<!-- Instead of using `?` to represent your parameter bindings, you may execute a query using named bindings: -->
`?` を使用してパラメーター バインディングを表す代わりに、名前付きバインディングを使用してクエリを実行できます。

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
<!-- #### Running an Insert Statement -->
#### Running an Insert Statement

<!-- To execute an `insert` statement, you may use the `insert` method on the `DB` facade. Like `select`, this method accepts the SQL query as its first argument and bindings as its second argument: -->
`insert` ステートメントを実行するには、`DB` ファサードで `insert` メソッドを使用できます。 `select` と同様、このメソッドは SQL クエリを最初の引数として受け入れ、バインディングを 2 番目の引数として受け入れます。

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
<!-- #### Running an Update Statement -->
#### Running an Update Statement

<!-- The `update` method should be used to update existing records in the database. The number of rows affected by the statement is returned by the method: -->
データベース内の既存のレコードを更新するには、`update` メソッドを使用する必要があります。ステートメントによって影響を受ける行の数は、次のメソッドによって返されます。

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
<!-- #### Running a Delete Statement -->
#### Running a Delete Statement

<!-- The `delete` method should be used to delete records from the database. Like `update`, the number of rows affected will be returned by the method: -->
データベースからレコードを削除するには、`delete` メソッドを使用する必要があります。 `update` と同様に、影響を受ける行数が次のメソッドによって返されます。

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
<!-- #### Running a General Statement -->
#### Running a General Statement

<!-- Some database statements do not return any value. For these types of operations, you may use the `statement` method on the `DB` facade: -->
一部のデータベース ステートメントは値を返しません。これらのタイプの操作の場合、`DB` ファサードで `statement` メソッドを使用できます。

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
<!-- #### Running an Unprepared Statement -->
#### Running an Unprepared Statement

<!-- Sometimes you may want to execute an SQL statement without binding any values. You may use the `DB` facade's `unprepared` method to accomplish this: -->
値をバインドせずに SQL ステートメントを実行したい場合があります。これを実現するには、`DB` ファサードの `unprepared` メソッドを使用できます。

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> 準備されていないステートメントはパラメーターをバインドしないため、SQL インジェクションに対して脆弱になる可能性があります。準備されていないステートメント内でユーザー制御の値を許可しないでください。

<a name="implicit-commits-in-transactions"></a>
<!-- #### Implicit Commits -->
#### Implicit Commits

<!-- When using the `DB` facade's `statement` and `unprepared` methods within transactions you must be careful to avoid statements that cause [implicit commits](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html). These statements will cause the database engine to indirectly commit the entire transaction, leaving Laravel unaware of the database's transaction level. An example of such a statement is creating a database table: -->
トランザクション内で `DB` ファサードの `statement` メソッドと `unprepared` メソッドを使用する場合は、[implicit commits](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) を引き起こすステートメントを避けるように注意する必要があります。これらのステートメントにより、データベース エンジンはトランザクション全体を間接的にコミットし、Laravel はデータベースのトランザクション レベルを認識しなくなります。このようなステートメントの例は、データベース テーブルの作成です。

```php
DB::unprepared('create table a (col varchar(1) null)');
```

<!-- Please refer to the MySQL manual for [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) that trigger implicit commits. -->
暗黙的なコミットをトリガーする [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) については、MySQL マニュアルを参照してください。

<a name="using-multiple-database-connections"></a>
<!-- ### Using Multiple Database Connections -->
### Using Multiple Database Connections

<!-- If your application defines multiple connections in your `config/database.php` configuration file, you may access each connection via the `connection` method provided by the `DB` facade. The connection name passed to the `connection` method should correspond to one of the connections listed in your `config/database.php` configuration file or configured at runtime using the `config` helper: -->
アプリケーションが `config/database.php` 構成ファイルで複数の接続を定義している場合、`DB` ファサードによって提供される `connection` メソッドを介して各接続にアクセスできます。 `connection` メソッドに渡される接続名は、`config/database.php` 構成ファイルにリストされている接続、または `config` ヘルパを使用して実行時に構成された接続の 1 つに対応する必要があります。

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

<!-- You may access the raw, underlying PDO instance of a connection using the `getPdo` method on a connection instance: -->
接続インスタンスで `getPdo` メソッドを使用して、接続の生の基礎となる PDO インスタンスにアクセスできます。

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
<!-- ### Listening for Query Events -->
### Listening for Query Events

<!-- If you would like to specify a closure that is invoked for each SQL query executed by your application, you may use the `DB` facade's `listen` method. This method can be useful for logging queries or debugging. You may register your query listener closure in the `boot` method of a [service provider](/docs/12.x/providers): -->
アプリケーションによって実行される SQL クエリごとに呼び出されるクロージャーを指定したい場合は、`DB` ファサードの `listen` メソッドを使用できます。このメソッドは、クエリのログ記録やデバッグに役立ちます。 [service provider](/docs/12.x/providers) の `boot` メソッドでクエリ リスナ クロージャを登録できます。

```php
<?php

namespace App\Providers;

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        DB::listen(function (QueryExecuted $query) {
            // $query->sql;
            // $query->bindings;
            // $query->time;
            // $query->toRawSql();
        });
    }
}
```

<a name="monitoring-cumulative-query-time"></a>
<!-- ### Monitoring Cumulative Query Time -->
### Monitoring Cumulative Query Time

<!-- A common performance bottleneck of modern web applications is the amount of time they spend querying databases. Thankfully, Laravel can invoke a closure or callback of your choice when it spends too much time querying the database during a single request. To get started, provide a query time threshold (in milliseconds) and closure to the `whenQueryingForLongerThan` method. You may invoke this method in the `boot` method of a [service provider](/docs/12.x/providers): -->
最新の Web アプリケーションの一般的なパフォーマンスのボトルネックは、データベースのクエリに費やす時間です。ありがたいことに、Laravel は、1 回のリクエスト中にデータベースのクエリに時間がかかりすぎる場合に、選択したクロージャまたはコールバックを呼び出すことができます。まず、クエリ時間のしきい値 (ミリ秒単位) とクロージャーを `whenQueryingForLongerThan` メソッドに指定します。このメソッドは、[service provider](/docs/12.x/providers) の `boot` メソッドで呼び出すことができます。

```php
<?php

namespace App\Providers;

use Illuminate\Database\Connection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;
use Illuminate\Database\Events\QueryExecuted;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // Notify development team...
        });
    }
}
```

<a name="database-transactions"></a>
<!-- ## Database Transactions -->
## Database Transactions

<!-- You may use the `transaction` method provided by the `DB` facade to run a set of operations within a database transaction. If an exception is thrown within the transaction closure, the transaction will automatically be rolled back and the exception is re-thrown. If the closure executes successfully, the transaction will automatically be committed. You don't need to worry about manually rolling back or committing while using the `transaction` method: -->
`DB` ファサードによって提供される `transaction` メソッドを使用して、データベース トランザクション内で一連の操作を実行できます。トランザクション クロージャ内で例外がスローされた場合、トランザクションは自動的にロールバックされ、例外が再スローされます。クロージャが正常に実行されると、トランザクションは自動的にコミットされます。 `transaction` メソッドを使用している間は、手動でのロールバックやコミットについて心配する必要はありません。

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
<!-- #### Handling Deadlocks -->
#### Handling Deadlocks

<!-- The `transaction` method accepts an optional second argument which defines the number of times a transaction should be retried when a deadlock occurs. Once these attempts have been exhausted, an exception will be thrown: -->
`transaction` メソッドは、デッドロックが発生したときにトランザクションを再試行する回数を定義するオプションの 2 番目の引数を受け入れます。これらの試行がすべて完了すると、例外がスローされます。

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, attempts: 5);
```

<a name="manually-using-transactions"></a>
<!-- #### Manually Using Transactions -->
#### Manually Using Transactions

<!-- If you would like to begin a transaction manually and have complete control over rollbacks and commits, you may use the `beginTransaction` method provided by the `DB` facade: -->
トランザクションを手動で開始し、ロールバックとコミットを完全に制御したい場合は、`DB` ファサードによって提供される `beginTransaction` メソッドを使用できます。

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

<!-- You can rollback the transaction via the `rollBack` method: -->
`rollBack` メソッドを使用してトランザクションをロールバックできます。

```php
DB::rollBack();
```

<!-- Lastly, you can commit a transaction via the `commit` method: -->
最後に、`commit` メソッドを使用してトランザクションをコミットできます。

```php
DB::commit();
```

> [!NOTE]
> `DB` ファサードのトランザクション メソッドは、[query builder](/docs/12.x/queries) と [Eloquent ORM](/docs/12.x/eloquent) の両方のトランザクションを制御します。

<a name="connecting-to-the-database-cli"></a>
<!-- ## Connecting to the Database CLI -->
## Connecting to the Database CLI

<!-- If you would like to connect to your database's CLI, you may use the `db` Artisan command: -->
データベースの CLI に接続したい場合は、`db` Artisan コマンドを使用できます。

```shell
php artisan db
```

<!-- If needed, you may specify a database connection name to connect to a database connection that is not the default connection: -->
必要に応じて、データベース接続名を指定して、デフォルトの接続ではないデータベース接続に接続できます。

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
<!-- ## Inspecting Your Databases -->
## Inspecting Your Databases

<!-- Using the `db:show` and `db:table` Artisan commands, you can get valuable insight into your database and its associated tables. To see an overview of your database, including its size, type, number of open connections, and a summary of its tables, you may use the `db:show` command: -->
`db:show` および `db:table` Artisan コマンドを使用すると、データベースとそれに関連するテーブルに関する貴重な洞察を得ることができます。データベースのサイズ、タイプ、開いている接続の数、テーブルの概要などのデータベースの概要を表示するには、`db:show` コマンドを使用します。

```shell
php artisan db:show
```

<!-- You may specify which database connection should be inspected by providing the database connection name to the command via the `--database` option: -->
`--database` オプションを使用してコマンドにデータベース接続名を指定することで、どのデータベース接続を検査するかを指定できます。

```shell
php artisan db:show --database=pgsql
```

<!-- If you would like to include table row counts and database view details within the output of the command, you may provide the `--counts` and `--views` options, respectively. On large databases, retrieving row counts and view details can be slow: -->
コマンドの出力にテーブルの行数とデータベース ビューの詳細を含めたい場合は、`--counts` オプションと `--views` オプションをそれぞれ指定できます。大規模なデータベースでは、行数の取得と詳細の表示が遅くなることがあります。

```shell
php artisan db:show --counts --views
```

<!-- In addition, you may use the following `Schema` methods to inspect your database: -->
さらに、次の `Schema` メソッドを使用してデータベースを検査することもできます。

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

<!-- If you would like to inspect a database connection that is not your application's default connection, you may use the `connection` method: -->
アプリケーションのデフォルト接続ではないデータベース接続を検査したい場合は、`connection` メソッドを使用できます。

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
<!-- #### Table Overview -->
#### Table Overview

<!-- If you would like to get an overview of an individual table within your database, you may execute the `db:table` Artisan command. This command provides a general overview of a database table, including its columns, types, attributes, keys, and indexes: -->
データベース内の個々のテーブルの概要を取得したい場合は、`db:table` Artisan コマンドを実行できます。このコマンドは、列、タイプ、属性、キー、インデックスなどのデータベース テーブルの概要を表示します。

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
<!-- ## Monitoring Your Databases -->
## Monitoring Your Databases

<!-- Using the `db:monitor` Artisan command, you can instruct Laravel to dispatch an `Illuminate\Database\Events\DatabaseBusy` event if your database is managing more than a specified number of open connections. -->
`db:monitor` Artisan コマンドを使用すると、データベースが指定された数を超えるオープン接続を管理している場合に `Illuminate\Database\Events\DatabaseBusy` イベントを送出するように Laravel に指示できます。

<!-- To get started, you should schedule the `db:monitor` command to [run every minute](/docs/12.x/scheduling). The command accepts the names of the database connection configurations that you wish to monitor as well as the maximum number of open connections that should be tolerated before dispatching an event: -->
まず、`db:monitor` コマンドを [run every minute](/docs/12.x/scheduling) にスケジュールする必要があります。このコマンドは、監視するデータベース接続構成の名前と、イベントを送出する前に許容されるオープン接続の最大数を受け入れます。

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

<!-- Scheduling this command alone is not enough to trigger a notification alerting you of the number of open connections. When the command encounters a database that has an open connection count that exceeds your threshold, a `DatabaseBusy` event will be dispatched. You should listen for this event within your application's `AppServiceProvider` in order to send a notification to you or your development team: -->
このコマンドをスケジュールするだけでは、開いている接続の数を警告する通知をトリガーするのに十分ではありません。コマンドが、オープン接続数がしきい値を超えるデータベースを検出すると、`DatabaseBusy` イベントが送出されます。あなたまたは開発チームに通知を送信するには、アプリケーションの `AppServiceProvider` 内でこのイベントをリッスンする必要があります。

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (DatabaseBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new DatabaseApproachingMaxConnections(
                $event->connectionName,
                $event->connections
            ));
    });
}
```

