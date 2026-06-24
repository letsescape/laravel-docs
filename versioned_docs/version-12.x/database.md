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
대부분의 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 지원 데이터베이스들과의 상호작용을 매우 간단하게 만들어 줍니다. 원시 SQL, [fluent query builder](/docs/12.x/queries), 그리고 [Eloquent ORM](/docs/12.x/eloquent)을 모두 사용할 수 있습니다. 현재 Laravel은 다음 5가지 데이터베이스를 공식적으로 1차 지원합니다:

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
추가적으로, MongoDB는 공식적으로 MongoDB에서 유지보수하는 `mongodb/laravel-mongodb` 패키지를 통해 지원합니다. 자세한 정보는 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- The configuration for Laravel's database services is located in your application's `config/database.php` configuration file. In this file, you may define all of your database connections, as well as specify which connection should be used by default. Most of the configuration options within this file are driven by the values of your application's environment variables. Examples for most of Laravel's supported database systems are provided in this file. -->
Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의할 수 있으며, 기본으로 사용할 연결도 지정할 수 있습니다. 이 파일의 대부분의 설정 옵션들은 애플리케이션의 환경 변수 값에 의해 제어됩니다. 대부분의 Laravel이 지원하는 데이터베이스 시스템 예제들이 이 파일에 포함되어 있습니다.

<!-- By default, Laravel's sample [environment configuration](/docs/12.x/configuration#environment-configuration) is ready to use with [Laravel Sail](/docs/12.x/sail), which is a Docker configuration for developing Laravel applications on your local machine. However, you are free to modify your database configuration as needed for your local database. -->
기본적으로, Laravel의 샘플 [environment configuration](/docs/12.x/configuration#environment-configuration)은 [Laravel Sail](/docs/12.x/sail)과 바로 사용할 수 있도록 준비되어 있습니다. 이는 로컬 머신에서 Laravel 애플리케이션을 개발하기 위한 Docker 설정입니다. 그러나, 필요시 로컬 데이터베이스에 맞게 설정을 자유롭게 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
<!-- #### SQLite Configuration -->
#### SQLite Configuration

<!-- SQLite databases are contained within a single file on your filesystem. You can create a new SQLite database using the `touch` command in your terminal: `touch database/database.sqlite`. After the database has been created, you may easily configure your environment variables to point to this database by placing the absolute path to the database in the `DB_DATABASE` environment variable: -->
SQLite 데이터베이스는 파일 시스템의 단일 파일에 저장됩니다. 터미널에서 `touch` 명령어로 새로운 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성된 후, `DB_DATABASE` 환경 변수에 데이터베이스의 절대 경로를 지정하면 환경 변수 설정이 완료됩니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

<!-- By default, foreign key constraints are enabled for SQLite connections. If you would like to disable them, you should set the `DB_FOREIGN_KEYS` environment variable to `false`: -->
기본적으로 SQLite 연결에서는 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하면 됩니다:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel installer](/docs/12.x/installation#creating-a-laravel-project)로 Laravel 애플리케이션을 생성하고 데이터베이스로 SQLite를 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하고 기본 [database migrations](/docs/12.x/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
<!-- #### Microsoft SQL Server Configuration -->
#### Microsoft SQL Server Configuration

<!-- To use a Microsoft SQL Server database, you should ensure that you have the `sqlsrv` and `pdo_sqlsrv` PHP extensions installed as well as any dependencies they may require such as the Microsoft SQL ODBC driver. -->
Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv` 및 `pdo_sqlsrv` PHP 확장과, 이들이 필요로 하는 Microsoft SQL ODBC 드라이버와 같은 의존성이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
<!-- #### Configuration Using URLs -->
#### Configuration Using URLs

<!-- Typically, database connections are configured using multiple configuration values such as `host`, `database`, `username`, `password`, etc. Each of these configuration values has its own corresponding environment variable. This means that when configuring your database connection information on a production server, you need to manage several environment variables. -->
일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정값을 통해 구성합니다. 각각의 값은 해당하는 환경 변수로 관리합니다. 즉, 프로덕션 서버에서 데이터베이스 연결 정보를 설정할 때 여러 환경 변수를 관리해야 합니다.

<!-- Some managed database providers such as AWS and Heroku provide a single database "URL" that contains all of the connection information for the database in a single string. An example database URL may look something like the following: -->
AWS, Heroku와 같은 일부 매니지드 데이터베이스 제공 업체는 모든 연결 정보를 하나의 문자열로 담은 데이터베이스 "URL"을 제공합니다. 예시 데이터베이스 URL은 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

<!-- These URLs typically follow a standard schema convention: -->
이들 URL은 일반적으로 아래와 같은 표준 스키마를 따릅니다:

```html
driver://username:password@host:port/database?options
```

<!-- For convenience, Laravel supports these URLs as an alternative to configuring your database with multiple configuration options. If the `url` (or corresponding `DB_URL` environment variable) configuration option is present, it will be used to extract the database connection and credential information. -->
편의상, Laravel에서는 여러 설정값 대신 이러한 URL로 데이터베이스를 연결할 수 있습니다. `url`(또는 환경 변수 `DB_URL`) 옵션이 존재한다면, 해당 값을 통해 연결 및 인증 정보를 추출해 사용합니다.

<a name="read-and-write-connections"></a>
<!-- ### Read and Write Connections -->
### Read and Write Connections

<!-- Sometimes you may wish to use one database connection for SELECT statements, and another for INSERT, UPDATE, and DELETE statements. Laravel makes this a breeze, and the proper connections will always be used whether you are using raw queries, the query builder, or the Eloquent ORM. -->
가끔 SELECT 쿼리에는 한 데이터베이스 연결을, INSERT/UPDATE/DELETE 쿼리에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel은 이 구성을 손쉽게 지원하며, 원시 쿼리나 쿼리 빌더, Eloquent ORM을 사용할 때도 항상 올바른 연결을 사용합니다.

<!-- To see how read / write connections should be configured, let's look at this example: -->
읽기/쓰기 연결을 어떻게 구성하는지 아래 예제를 봅시다:

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
위 구성 배열에는 `read`, `write`, `sticky`라는 세 개의 키가 있으며, `read`와 `write` 안에는 각각 `host`가 존재합니다. `read` 및 `write` 연결의 그 외 데이터베이스 옵션은 메인 `mysql` 배열에서 병합됩니다.

<!-- You only need to place items in the `read` and `write` arrays if you wish to override the values from the main `mysql` array. So, in this case, `192.168.1.1` will be used as the host for the "read" connection, while `192.168.1.3` will be used for the "write" connection. The database credentials, prefix, character set, and all other options in the main `mysql` array will be shared across both connections. When multiple values exist in the `host` configuration array, a database host will be randomly chosen for each request. -->
만약 메인 `mysql` 배열의 값을 덮어쓰고자 할 때만 `read`, `write` 배열에 값을 지정하면 됩니다. 이 예제에서는 "read" 연결에는 `192.168.1.1`이, "write" 연결에는 `192.168.1.3`이 사용됩니다. 데이터베이스 자격증명, prefix, 문자셋 등 메인 `mysql` 배열의 나머지 모든 옵션은 두 연결이 공유합니다. `host`가 여러 값으로 배열에 정의되어 있다면, 각 요청마다 무작위로 선택된 호스트가 사용됩니다.

<a name="the-sticky-option"></a>
<!-- #### The `sticky` Option -->
#### The `sticky` Option

<!-- The `sticky` option is an *optional* value that can be used to allow the immediate reading of records that have been written to the database during the current request cycle. If the `sticky` option is enabled and a "write" operation has been performed against the database during the current request cycle, any further "read" operations will use the "write" connection. This ensures that any data written during the request cycle can be immediately read back from the database during that same request. It is up to you to decide if this is the desired behavior for your application. -->
`sticky` 옵션은 *선택적인* 값으로, 현재 요청 사이클 동안 데이터베이스에 기록한 레코드를 즉시 다시 읽을 수 있도록 해줍니다. `sticky` 옵션이 활성화되어 있고 현재 요청 사이클에서 "write" 작업이 수행되었다면, 이후의 모든 "read" 작업도 "write" 연결을 사용하게 됩니다. 이렇게 하면 한 요청 내에서 데이터가 저장되면 즉시 해당 데이터를 같은 요청 안에서 다시 읽을 수 있습니다. 이 동작이 애플리케이션에 필요한지 여부는 직접 판단해서 설정하면 됩니다.

<a name="running-queries"></a>
<!-- ## Running SQL Queries -->
## Running SQL Queries

<!-- Once you have configured your database connection, you may run queries using the `DB` facade. The `DB` facade provides methods for each type of query: `select`, `update`, `insert`, `delete`, and `statement`. -->
데이터베이스 연결을 설정한 후에는 `DB` 파사드(facade)를 이용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 각 쿼리 유형별로 `select`, `update`, `insert`, `delete`, `statement` 메서드를 제공합니다.

<a name="running-a-select-query"></a>
<!-- #### Running a Select Query -->
#### Running a Select Query

<!-- To run a basic SELECT query, you may use the `select` method on the `DB` facade: -->
기본적인 SELECT 쿼리는 `DB` 파사드의 `select` 메서드를 사용합니다:

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
`select` 메서드의 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 쿼리에 바인딩할 파라미터입니다. 일반적으로 `where` 절 제약 조건의 값을 의미합니다. 파라미터 바인딩을 통해 SQL 인젝션 공격 위험을 방지할 수 있습니다.

<!-- The `select` method will always return an `array` of results. Each result within the array will be a PHP `stdClass` object representing a record from the database: -->
`select` 메서드는 항상 결과값을 `array`로 반환합니다. 배열의 각 요소는 데이터베이스의 레코드를 나타내는 PHP의 `stdClass` 객체입니다:

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
쿼리 결과가 단일값(스칼라)인 경우, Laravel에서는 `scalar` 메서드를 통해 객체에서 값을 추출하지 않고 바로 값을 얻을 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
<!-- #### Selecting Multiple Result Sets -->
#### Selecting Multiple Result Sets

<!-- If your application calls stored procedures that return multiple result sets, you may use the `selectResultSets` method to retrieve all of the result sets returned by the stored procedure: -->
저장 프로시저 호출로 여러 결과셋이 반환되는 경우, `selectResultSets` 메서드를 사용해 모든 결과셋을 가져올 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
<!-- #### Using Named Bindings -->
#### Using Named Bindings

<!-- Instead of using `?` to represent your parameter bindings, you may execute a query using named bindings: -->
파라미터 바인딩 시 `?` 대신 이름 바인딩을 사용할 수 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
<!-- #### Running an Insert Statement -->
#### Running an Insert Statement

<!-- To execute an `insert` statement, you may use the `insert` method on the `DB` facade. Like `select`, this method accepts the SQL query as its first argument and bindings as its second argument: -->
`insert` 문을 실행하려면 `DB` 파사드의 `insert` 메서드를 사용할 수 있습니다. `select`와 마찬가지로, 이 메서드는 첫 번째 인수로 SQL 쿼리를, 두 번째 인수로 바인딩을 받습니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
<!-- #### Running an Update Statement -->
#### Running an Update Statement

<!-- The `update` method should be used to update existing records in the database. The number of rows affected by the statement is returned by the method: -->
`update` 메서드는 기존 레코드의 값을 변경할 때 사용합니다. 영향받은 행(row)의 수를 반환합니다:

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
`delete` 메서드는 레코드 삭제에 사용합니다. `update`와 마찬가지로 영향받은 행의 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
<!-- #### Running a General Statement -->
#### Running a General Statement

<!-- Some database statements do not return any value. For these types of operations, you may use the `statement` method on the `DB` facade: -->
일부 데이터베이스 쿼리는 반환값이 없습니다. 이런 경우에는 `DB` 파사드의 `statement` 메서드를 사용합니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
<!-- #### Running an Unprepared Statement -->
#### Running an Unprepared Statement

<!-- Sometimes you may want to execute an SQL statement without binding any values. You may use the `DB` facade's `unprepared` method to accomplish this: -->
값을 바인딩하지 않고 SQL 쿼리를 직접 실행하고 싶을 때는 `DB` 파사드의 `unprepared` 메서드를 사용합니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> unprepared 쿼리는 파라미터를 바인딩하지 않으므로 SQL 인젝션 공격에 취약할 수 있습니다. 사용자 입력이 포함된 unprepared 쿼리는 절대 사용해서는 안 됩니다.

<a name="implicit-commits-in-transactions"></a>
<!-- #### Implicit Commits -->
#### Implicit Commits

<!-- When using the `DB` facade's `statement` and `unprepared` methods within transactions you must be careful to avoid statements that cause [implicit commits](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html). These statements will cause the database engine to indirectly commit the entire transaction, leaving Laravel unaware of the database's transaction level. An example of such a statement is creating a database table: -->
트랜잭션 내에서 `DB` 파사드의 `statement`나 `unprepared` 메서드를 사용할 때는 [implicit commits](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 발생시키는 쿼리를 주의하세요. 이런 쿼리는 데이터베이스 엔진이 트랜잭션 전체를 간접적으로 커밋하여, Laravel이 트랜잭션 레벨을 제대로 인지하지 못하게 됩니다. 예를 들어, 테이블을 생성하는 쿼리 등이 이에 해당합니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

<!-- Please refer to the MySQL manual for [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) that trigger implicit commits. -->
암시적 커밋을 발생시키는 명령어의 전체 목록은 MySQL 매뉴얼의 [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 참고하세요.

<a name="using-multiple-database-connections"></a>
<!-- ### Using Multiple Database Connections -->
### Using Multiple Database Connections

<!-- If your application defines multiple connections in your `config/database.php` configuration file, you may access each connection via the `connection` method provided by the `DB` facade. The connection name passed to the `connection` method should correspond to one of the connections listed in your `config/database.php` configuration file or configured at runtime using the `config` helper: -->
애플리케이션의 `config/database.php` 파일에 여러 연결이 정의되어 있다면, `DB` 파사드의 `connection` 메서드를 통해 각 연결을 사용할 수 있습니다. `connection` 메서드에 지정하는 연결명은 `config/database.php` 설정 파일에 정의된 연결 중 하나이거나, 런타임에 `config` 헬퍼로 설정한 값이어야 합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

<!-- You may access the raw, underlying PDO instance of a connection using the `getPdo` method on a connection instance: -->
각 연결 인스턴스의 `getPdo` 메서드를 사용하면, 원시 PDO 인스턴스에 직접 접근할 수 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
<!-- ### Listening for Query Events -->
### Listening for Query Events

<!-- If you would like to specify a closure that is invoked for each SQL query executed by your application, you may use the `DB` facade's `listen` method. This method can be useful for logging queries or debugging. You may register your query listener closure in the `boot` method of a [service provider](/docs/12.x/providers): -->
애플리케이션의 모든 SQL 쿼리 실행 시마다 클로저를 호출하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 기능은 쿼리 로깅이나 디버깅에 유용합니다. 쿼리 리스너 클로저는 [service provider](/docs/12.x/providers)의 `boot` 메서드에서 등록 가능합니다:

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
웹 애플리케이션의 주요 성능 병목지점 중 하나는 데이터베이스 쿼리에 소요되는 시간입니다. Laravel에서는 한 요청 내에서 쿼리 수행 시간이 너무 길어질 때, 지정한 클로저나 콜백을 호출할 수 있습니다. 설정 방법은 `whenQueryingForLongerThan` 메서드에 임계 시간(밀리초 단위)과 클로저를 전달하는 것입니다. 이 메서드는 [service provider](/docs/12.x/providers)의 `boot` 메서드에서 사용할 수 있습니다:

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
`DB` 파사드의 `transaction` 메서드를 이용하여 여러 데이터베이스 작업을 트랜잭션으로 묶어 실행할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 트랜잭션이 자동 롤백되고 예외가 다시 발생합니다. 클로저가 성공적으로 실행될 경우 자동으로 커밋됩니다. `transaction` 메서드를 사용하면 별도로 롤백이나 커밋을 신경 쓸 필요가 없습니다:

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
`transaction` 메서드는 두 번째 인자로 데드락 발생 시 재시도할 횟수를 지정할 수 있습니다. 지정한 횟수만큼 재시도 후에도 실패하면 예외가 발생합니다:

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
트랜잭션을 직접 시작하고 커밋/롤백을 세밀하게 제어하고 싶다면 `DB` 파사드의 `beginTransaction` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

<!-- You can rollback the transaction via the `rollBack` method: -->
트랜잭션을 롤백하려면 `rollBack` 메서드를 사용하십시오:

```php
DB::rollBack();
```

<!-- Lastly, you can commit a transaction via the `commit` method: -->
마지막으로 트랜잭션을 커밋하려면 `commit` 메서드를 사용합니다:

```php
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 관련 메서드는 [query builder](/docs/12.x/queries)와 [Eloquent ORM](/docs/12.x/eloquent) 모두의 트랜잭션을 제어합니다.

<a name="connecting-to-the-database-cli"></a>
<!-- ## Connecting to the Database CLI -->
## Connecting to the Database CLI

<!-- If you would like to connect to your database's CLI, you may use the `db` Artisan command: -->
데이터베이스의 CLI에 연결하려면 `db` 아티즌 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

<!-- If needed, you may specify a database connection name to connect to a database connection that is not the default connection: -->
필요하다면, 기본 연결이 아닌 다른 데이터베이스 연결명을 명령 인자로 지정할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
<!-- ## Inspecting Your Databases -->
## Inspecting Your Databases

<!-- Using the `db:show` and `db:table` Artisan commands, you can get valuable insight into your database and its associated tables. To see an overview of your database, including its size, type, number of open connections, and a summary of its tables, you may use the `db:show` command: -->
`db:show` 및 `db:table` 아티즌 명령어를 사용하여 데이터베이스와 해당 테이블 정보를 상세히 확인할 수 있습니다. 데이터베이스의 개요(크기, 종류, 활성 연결 수, 테이블 요약 등)를 확인하려면 `db:show` 명령어를 사용하세요:

```shell
php artisan db:show
```

<!-- You may specify which database connection should be inspected by providing the database connection name to the command via the `--database` option: -->
확인할 데이터베이스 연결명을 `--database` 옵션으로 지정할 수도 있습니다:

```shell
php artisan db:show --database=pgsql
```

<!-- If you would like to include table row counts and database view details within the output of the command, you may provide the `--counts` and `--views` options, respectively. On large databases, retrieving row counts and view details can be slow: -->
명령 출력에 테이블 행(row) 개수나 데이터베이스 뷰 정보를 포함하려면 `--counts` 또는 `--views` 옵션을 사용할 수 있습니다. 대형 데이터베이스의 경우 행 개수나 뷰 정보 확인이 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

<!-- In addition, you may use the following `Schema` methods to inspect your database: -->
추가로, `Schema`의 다음 메서드들을 통해 데이터베이스 구조를 코드로도 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

<!-- If you would like to inspect a database connection that is not your application's default connection, you may use the `connection` method: -->
애플리케이션의 기본 연결이 아닌 데이터베이스를 검사하려면 `connection` 메서드를 사용할 수 있습니다:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
<!-- #### Table Overview -->
#### Table Overview

<!-- If you would like to get an overview of an individual table within your database, you may execute the `db:table` Artisan command. This command provides a general overview of a database table, including its columns, types, attributes, keys, and indexes: -->
특정 테이블의 정보를 확인하려면 `db:table` 아티즌 명령어를 사용할 수 있습니다. 이 명령은 컬럼, 타입, 속성, 키, 인덱스 등 테이블의 일반 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
<!-- ## Monitoring Your Databases -->
## Monitoring Your Databases

<!-- Using the `db:monitor` Artisan command, you can instruct Laravel to dispatch an `Illuminate\Database\Events\DatabaseBusy` event if your database is managing more than a specified number of open connections. -->
`db:monitor` 아티즌 명령어를 사용하면 데이터베이스의 열린 연결 수가 지정된 수를 초과할 때 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 Laravel이 발생시킵니다.

<!-- To get started, you should schedule the `db:monitor` command to [run every minute](/docs/12.x/scheduling). The command accepts the names of the database connection configurations that you wish to monitor as well as the maximum number of open connections that should be tolerated before dispatching an event: -->
시작하려면, `db:monitor` 명령어를 [run every minute](/docs/12.x/scheduling)하도록 스케줄링하세요. 이 명령은 모니터링할 데이터베이스 연결명과, 이벤트 발생 전 견딜 수 있는 최대 열린 연결 수를 인자로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

<!-- Scheduling this command alone is not enough to trigger a notification alerting you of the number of open connections. When the command encounters a database that has an open connection count that exceeds your threshold, a `DatabaseBusy` event will be dispatched. You should listen for this event within your application's `AppServiceProvider` in order to send a notification to you or your development team: -->
이 명령을 스케줄링하는 것만으로는 알림이 바로 전송되지 않습니다. 임계값을 초과한 경우 `DatabaseBusy` 이벤트가 발생되고, 이 이벤트를 애플리케이션의 `AppServiceProvider`에서 리스닝하여 본인이나 개발팀에 알림을 전송하면 됩니다:

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
