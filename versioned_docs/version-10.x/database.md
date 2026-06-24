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

<!-- Almost every modern web application interacts with a database. Laravel makes interacting with databases extremely simple across a variety of supported databases using raw SQL, a [fluent query builder](/docs/10.x/queries), and the [Eloquent ORM](/docs/10.x/eloquent). Currently, Laravel provides first-party support for five databases: -->
대부분의 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 지원하는 다양한 데이터베이스에 대해 원시 SQL, [fluent query builder](/docs/10.x/queries), [Eloquent ORM](/docs/10.x/eloquent) 등 여러 방식을 이용해 데이터베이스와 아주 쉽게 연동할 수 있도록 도와줍니다. 현재 Laravel은 아래 다섯 가지 데이터베이스를 공식적으로 지원합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- MariaDB 10.10+ ([Version Policy](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([Version Policy](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 11.0+ ([Version Policy](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([Version Policy](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))
-->
- MariaDB 10.10+ ([Version Policy](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([Version Policy](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 11.0+ ([Version Policy](https://www.postgresql.org/support/versioning/))
- SQLite 3.8.8+
- SQL Server 2017+ ([Version Policy](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

<!-- </div> -->
</div>

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- The configuration for Laravel's database services is located in your application's `config/database.php` configuration file. In this file, you may define all of your database connections, as well as specify which connection should be used by default. Most of the configuration options within this file are driven by the values of your application's environment variables. Examples for most of Laravel's supported database systems are provided in this file. -->
Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에서 관리합니다. 이 파일에서는 모든 데이터베이스 연결을 정의하고, 어떤 연결을 기본으로 사용할 것인지 지정할 수 있습니다. 이 설정 파일의 대부분의 옵션들은 애플리케이션 환경 변수의 값에 의해 결정됩니다. Laravel이 지원하는 여러 데이터베이스 시스템에 대한 예제 설정도 이 파일에 포함되어 있습니다.

<!-- By default, Laravel's sample [environment configuration](/docs/10.x/configuration#environment-configuration) is ready to use with [Laravel Sail](/docs/10.x/sail), which is a Docker configuration for developing Laravel applications on your local machine. However, you are free to modify your database configuration as needed for your local database. -->
기본적으로 Laravel의 샘플 [environment configuration](/docs/10.x/configuration#environment-configuration)은 [Laravel Sail](/docs/10.x/sail)에서 바로 사용할 수 있도록 준비되어 있습니다. Laravel Sail은 로컬 개발 환경에서 Laravel 애플리케이션을 실행할 수 있도록 제공되는 Docker 설정입니다. 하지만, 로컬 데이터베이스 환경에 맞게 설정을 자유롭게 변경할 수도 있습니다.

<a name="sqlite-configuration"></a>
<!-- #### SQLite Configuration -->
#### SQLite Configuration

<!-- SQLite databases are contained within a single file on your filesystem. You can create a new SQLite database using the `touch` command in your terminal: `touch database/database.sqlite`. After the database has been created, you may easily configure your environment variables to point to this database by placing the absolute path to the database in the `DB_DATABASE` environment variable: -->
SQLite 데이터베이스는 파일 시스템 내 하나의 파일로 존재합니다. 터미널에서 `touch` 명령어를 사용해 새로운 SQLite 데이터베이스 파일을 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성된 후에는, 해당 데이터베이스의 절대 경로를 `DB_DATABASE` 환경 변수에 지정해주면 됩니다.

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

<!-- To enable foreign key constraints for SQLite connections, you should set the `DB_FOREIGN_KEYS` environment variable to `true`: -->
SQLite 연결에서 외래 키 제약 조건을 활성화하려면, `DB_FOREIGN_KEYS` 환경 변수를 `true`로 설정해야 합니다.

```ini
DB_FOREIGN_KEYS=true
```

<a name="mssql-configuration"></a>
<!-- #### Microsoft SQL Server Configuration -->
#### Microsoft SQL Server Configuration

<!-- To use a Microsoft SQL Server database, you should ensure that you have the `sqlsrv` and `pdo_sqlsrv` PHP extensions installed as well as any dependencies they may require such as the Microsoft SQL ODBC driver. -->
Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv`와 `pdo_sqlsrv` PHP 확장 프로그램을 반드시 설치해야 하며, 추가적으로 Microsoft SQL ODBC 드라이버 등 필요한 의존성도 갖추어야 합니다.

<a name="configuration-using-urls"></a>
<!-- #### Configuration Using URLs -->
#### Configuration Using URLs

<!-- Typically, database connections are configured using multiple configuration values such as `host`, `database`, `username`, `password`, etc. Each of these configuration values has its own corresponding environment variable. This means that when configuring your database connection information on a production server, you need to manage several environment variables. -->
일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 개의 설정값을 조합해 구성합니다. 각 설정 값에 대응되는 환경 변수가 있어야 하므로, 실제 서버 환경에서는 여러 개의 환경 변수를 관리해야만 합니다.

<!-- Some managed database providers such as AWS and Heroku provide a single database "URL" that contains all of the connection information for the database in a single string. An example database URL may look something like the following: -->
AWS, Heroku 등 일부 관리형 데이터베이스 서비스에서는 모든 연결 정보를 하나의 문자열로 담아 제공하는 데이터베이스 "URL"을 지원합니다. 예를 들어 다음과 같은 형태입니다.

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

<!-- These URLs typically follow a standard schema convention: -->
이러한 URL은 일반적으로 정해진 스키마 규칙을 따릅니다.

```html
driver://username:password@host:port/database?options
```

<!-- For convenience, Laravel supports these URLs as an alternative to configuring your database with multiple configuration options. If the `url` (or corresponding `DATABASE_URL` environment variable) configuration option is present, it will be used to extract the database connection and credential information. -->
Laravel은 편의를 위해, 여러 설정 값을 별도로 지정하는 대신 위와 같은 단일 URL 형태의 연결 정보도 지원합니다. `url` (또는 `DATABASE_URL` 환경 변수) 설정 옵션이 제공된 경우, 이 값을 사용해 데이터베이스 연결 정보와 자격 증명을 추출하게 됩니다.

<a name="read-and-write-connections"></a>
<!-- ### Read and Write Connections -->
### Read and Write Connections

<!-- Sometimes you may wish to use one database connection for SELECT statements, and another for INSERT, UPDATE, and DELETE statements. Laravel makes this a breeze, and the proper connections will always be used whether you are using raw queries, the query builder, or the Eloquent ORM. -->
특정 상황에서는 SELECT 쿼리는 하나의 데이터베이스 연결을 사용하고, INSERT, UPDATE, DELETE와 같은 쿼리는 별도의 연결을 사용하고 싶을 수 있습니다. Laravel은 이처럼 읽기/쓰기 연결을 손쉽게 구성할 수 있도록 하며, 원시 쿼리, 쿼리 빌더, Eloquent ORM을 사용할 때도 항상 올바른 연결이 자동으로 사용됩니다.

<!-- To see how read / write connections should be configured, let's look at this example: -->
읽기/쓰기 연결을 어떻게 설정하는지 다음 예시를 참고해보세요.

```
'mysql' => [
    'read' => [
        'host' => [
            '192.168.1.1',
            '196.168.1.2',
        ],
    ],
    'write' => [
        'host' => [
            '196.168.1.3',
        ],
    ],
    'sticky' => true,
    'driver' => 'mysql',
    'database' => 'database',
    'username' => 'root',
    'password' => '',
    'charset' => 'utf8mb4',
    'collation' => 'utf8mb4_unicode_ci',
    'prefix' => '',
],
```

<!-- Note that three keys have been added to the configuration array: `read`, `write` and `sticky`. The `read` and `write` keys have array values containing a single key: `host`. The rest of the database options for the `read` and `write` connections will be merged from the main `mysql` configuration array. -->
설정 배열에 `read`, `write`, `sticky`라는 세 가지 키가 추가된 것에 주의하세요. `read`와 `write` 키는 각각 하나의 키(`host`)를 포함하는 배열입니다. `read`와 `write` 연결의 나머지 데이터베이스 옵션들은 기본 `mysql` 설정 배열에서 병합되어 사용됩니다.

<!-- You only need to place items in the `read` and `write` arrays if you wish to override the values from the main `mysql` array. So, in this case, `192.168.1.1` will be used as the host for the "read" connection, while `192.168.1.3` will be used for the "write" connection. The database credentials, prefix, character set, and all other options in the main `mysql` array will be shared across both connections. When multiple values exist in the `host` configuration array, a database host will be randomly chosen for each request. -->
`read`와 `write` 배열에는 기본 `mysql` 배열의 값을 오버라이드하고 싶은 항목만 입력하면 됩니다. 이 예시에서는 "읽기" 연결의 호스트로 `192.168.1.1`이, "쓰기" 연결의 호스트로는 `192.168.1.3`이 사용됩니다. 데이터베이스 자격 증명, 프리픽스, 문자셋 등 나머지 모든 옵션은 기본 `mysql` 배열이 공통적으로 사용됩니다. 만약 `host` 배열에 여러 값이 들어있다면, 요청 시마다 무작위로 한 개의 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
<!-- #### The `sticky` Option -->
#### The `sticky` Option

<!-- The `sticky` option is an *optional* value that can be used to allow the immediate reading of records that have been written to the database during the current request cycle. If the `sticky` option is enabled and a "write" operation has been performed against the database during the current request cycle, any further "read" operations will use the "write" connection. This ensures that any data written during the request cycle can be immediately read back from the database during that same request. It is up to you to decide if this is the desired behavior for your application. -->
`sticky` 옵션은 *선택적* 설정값으로, 현재 요청 사이클 동안 데이터베이스에 쓴(쓰기) 데이터를 즉시 읽을 수 있도록 도와줍니다. 만약 `sticky` 옵션이 활성화되어 있고, 현재 요청에서 "쓰기" 작업이 수행된 경우, 이후의 모든 "읽기" 쿼리는 "쓰기" 연결을 통해 처리됩니다. 이렇게 하면 한 번의 요청 내에서 바로 저장한 데이터를 바로 다시 읽어올 수 있습니다. 이 옵션이 필요한지 여부는 애플리케이션의 요구 사항에 따라 결정하시면 됩니다.

<a name="running-queries"></a>
<!-- ## Running SQL Queries -->
## Running SQL Queries

<!-- Once you have configured your database connection, you may run queries using the `DB` facade. The `DB` facade provides methods for each type of query: `select`, `update`, `insert`, `delete`, and `statement`. -->
데이터베이스 연결을 설정한 뒤에는, `DB` 파사드를 이용하여 쿼리를 실행할 수 있습니다. `DB` 파사드는 각각의 쿼리 타입에 맞는 메서드를 제공합니다: `select`, `update`, `insert`, `delete`, `statement`.

<a name="running-a-select-query"></a>
<!-- #### Running a Select Query -->
#### Running a Select Query

<!-- To run a basic SELECT query, you may use the `select` method on the `DB` facade: -->
기본적인 SELECT 쿼리를 실행하려면, `DB` 파사드의 `select` 메서드를 사용하면 됩니다.

```
<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
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
`select` 메서드의 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 쿼리에 바인딩될 파라미터 값들입니다. 일반적으로 이 값들은 `where` 조건 절의 값이 됩니다. 파라미터 바인딩을 이용하면 SQL 인젝션 공격을 방지할 수 있습니다.

<!-- The `select` method will always return an `array` of results. Each result within the array will be a PHP `stdClass` object representing a record from the database: -->
`select` 메서드는 항상 결과를 `array`로 반환합니다. 배열 안의 각 결과는 데이터베이스 레코드를 나타내는 PHP `stdClass` 객체로 반환됩니다.

```
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
가끔은 데이터베이스 쿼리 결과가 단일 값, 즉 스칼라 값일 때도 있습니다. 이럴 때는 결과 배열에서 값을 꺼낼 필요 없이, Laravel의 `scalar` 메서드를 사용해 바로 값을 얻을 수 있습니다.

```
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
<!-- #### Selecting Multiple Result Sets -->
#### Selecting Multiple Result Sets

<!-- If your application calls stored procedures that return multiple result sets, you may use the `selectResultSets` method to retrieve all of the result sets returned by the stored procedure: -->
스토어드 프로시저 등에서 여러 개의 결과 집합을 반환할 때는 `selectResultSets` 메서드를 사용해 각각의 결과 집합을 모두 받아올 수 있습니다.

```
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
<!-- #### Using Named Bindings -->
#### Using Named Bindings

<!-- Instead of using `?` to represent your parameter bindings, you may execute a query using named bindings: -->
파라미터 바인딩 시 `?` 대신, 이름이 지정된 바인딩을 사용할 수도 있습니다.

```
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
<!-- #### Running an Insert Statement -->
#### Running an Insert Statement

<!-- To execute an `insert` statement, you may use the `insert` method on the `DB` facade. Like `select`, this method accepts the SQL query as its first argument and bindings as its second argument: -->
`insert` 문을 실행하려면, `DB` 파사드의 `insert` 메서드를 사용할 수 있습니다. `select`와 마찬가지로 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 파라미터 바인딩 배열입니다.

```
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
<!-- #### Running an Update Statement -->
#### Running an Update Statement

<!-- The `update` method should be used to update existing records in the database. The number of rows affected by the statement is returned by the method: -->
`update` 메서드는 데이터베이스의 기존 레코드를 업데이트하는 데 사용합니다. 이 메서드는 영향받은(변경된) 행의 개수를 반환합니다.

```
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
`delete` 메서드는 레코드를 삭제할 때 사용합니다. `update`와 마찬가지로 영향받은 행의 수가 반환됩니다.

```
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
<!-- #### Running a General Statement -->
#### Running a General Statement

<!-- Some database statements do not return any value. For these types of operations, you may use the `statement` method on the `DB` facade: -->
특정 데이터베이스 명령문은 값을 반환하지 않을 때도 있습니다. 이런 작업에는 `DB` 파사드의 `statement` 메서드를 사용할 수 있습니다.

```
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
<!-- #### Running an Unprepared Statement -->
#### Running an Unprepared Statement

<!-- Sometimes you may want to execute an SQL statement without binding any values. You may use the `DB` facade's `unprepared` method to accomplish this: -->
어떤 경우에는 파라미터 바인딩 없이 SQL 문을 실행하고 싶을 수도 있습니다. 이럴 땐 `DB` 파사드의 `unprepared` 메서드를 사용할 수 있습니다.

```
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> unprepared 쿼리는 파라미터 바인딩을 사용하지 않기 때문에, SQL 인젝션에 취약할 수 있습니다. 사용자 입력값을 그대로 쿼리에 삽입하는 것은 절대 피해야 합니다.

<a name="implicit-commits-in-transactions"></a>
<!-- #### Implicit Commits -->
#### Implicit Commits

<!-- When using the `DB` facade's `statement` and `unprepared` methods within transactions you must be careful to avoid statements that cause [implicit commits](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html). These statements will cause the database engine to indirectly commit the entire transaction, leaving Laravel unaware of the database's transaction level. An example of such a statement is creating a database table: -->
트랜잭션 안에서 `DB` 파사드의 `statement` 또는 `unprepared` 메서드를 사용할 때, [implicit commits](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 발생시키는 명령문을 피해야 합니다. 이런 명령이 실행되면 데이터베이스 엔진이 트랜잭션을 강제 커밋하게 되어, Laravel이 더 이상 트랜잭션 상태를 인지하지 못하게 됩니다. 예를 들어, 테이블 생성 명령문이 이에 해당합니다.

```
DB::unprepared('create table a (col varchar(1) null)');
```

<!-- Please refer to the MySQL manual for [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html) that trigger implicit commits. -->
암묵적 커밋을 유발하는 모든 명령어 목록은 MySQL 메뉴얼의 [a list of all statements](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 참고하세요.

<a name="using-multiple-database-connections"></a>
<!-- ### Using Multiple Database Connections -->
### Using Multiple Database Connections

<!-- If your application defines multiple connections in your `config/database.php` configuration file, you may access each connection via the `connection` method provided by the `DB` facade. The connection name passed to the `connection` method should correspond to one of the connections listed in your `config/database.php` configuration file or configured at runtime using the `config` helper: -->
애플리케이션에서 `config/database.php` 파일에 여러 개의 연결을 정의했다면, `DB` 파사드의 `connection` 메서드를 통해 각 연결에 접근할 수 있습니다. `connection` 메서드에 전달하는 연결명은 `config/database.php` 파일에 정의된 연결 중 하나와 일치하거나, `config` 헬퍼를 통해 실행 시 동적으로 지정한 연결과 일치해야 합니다.

```
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

<!-- You may access the raw, underlying PDO instance of a connection using the `getPdo` method on a connection instance: -->
특정 연결 인스턴스의 내부 PDO 인스턴스에 직접 접근하고 싶다면, `getPdo` 메서드를 사용할 수 있습니다.

```
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
<!-- ### Listening for Query Events -->
### Listening for Query Events

<!-- If you would like to specify a closure that is invoked for each SQL query executed by your application, you may use the `DB` facade's `listen` method. This method can be useful for logging queries or debugging. You may register your query listener closure in the `boot` method of a [service provider](/docs/10.x/providers): -->
애플리케이션에서 실행되는 모든 SQL 쿼리에 대해 콜백을 지정하고 싶다면, `DB` 파사드의 `listen` 메서드를 이용할 수 있습니다. 이 기능은 쿼리 로깅 또는 디버깅에 유용하게 사용할 수 있습니다. 쿼리 리스너 콜백은 [service provider](/docs/10.x/providers)의 `boot` 메서드 등에서 등록하면 됩니다.

```
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
        });
    }
}
```

<a name="monitoring-cumulative-query-time"></a>
<!-- ### Monitoring Cumulative Query Time -->
### Monitoring Cumulative Query Time

<!-- A common performance bottleneck of modern web applications is the amount of time they spend querying databases. Thankfully, Laravel can invoke a closure or callback of your choice when it spends too much time querying the database during a single request. To get started, provide a query time threshold (in milliseconds) and closure to the `whenQueryingForLongerThan` method. You may invoke this method in the `boot` method of a [service provider](/docs/10.x/providers): -->
현대 웹 애플리케이션의 성능 병목 원인 중 하나는 데이터베이스 쿼리 수행에 소요되는 시간입니다. Laravel은 한 번의 요청 중 데이터베이스 쿼리 수행 시간이 너무 길어진 경우, 지정한 클로저나 콜백을 실행하게 할 수 있습니다. 시작하려면, `whenQueryingForLongerThan` 메서드에 시간 임계값(밀리초 단위)과 클로저를 지정하세요. 이 메서드는 [service provider](/docs/10.x/providers)의 `boot` 메서드에서 호출하면 됩니다.

```
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
여러 작업을 하나의 데이터베이스 트랜잭션 내에서 실행하려면, `DB` 파사드의 `transaction` 메서드를 사용할 수 있습니다. 트랜잭션 클로저 안에서 예외가 발생하면 트랜잭션이 자동으로 롤백되고, 예외가 다시 반환됩니다. 클로저가 문제없이 실행되면 트랜잭션은 자동으로 커밋됩니다. 즉, `transaction` 메서드를 사용할 때는 직접 롤백이나 커밋을 신경 쓸 필요가 없습니다.

```
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
`transaction` 메서드는 두 번째 인수로 트랜잭션 실행 도중 데드락이 발생할 경우 재시도할 횟수를 받을 수 있습니다. 지정한 횟수만큼 재시도한 뒤에도 데드락이 해소되지 않으면 예외가 발생합니다.

```
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, 5);
```

<a name="manually-using-transactions"></a>
<!-- #### Manually Using Transactions -->
#### Manually Using Transactions

<!-- If you would like to begin a transaction manually and have complete control over rollbacks and commits, you may use the `beginTransaction` method provided by the `DB` facade: -->
트랜잭션을 수동으로 시작하여 직접 롤백 및 커밋을 제어하고 싶다면, `DB` 파사드의 `beginTransaction` 메서드를 사용하세요.

```
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

<!-- You can rollback the transaction via the `rollBack` method: -->
트랜잭션을 롤백하려면 `rollBack` 메서드를 호출하세요.

```
DB::rollBack();
```

<!-- Lastly, you can commit a transaction via the `commit` method: -->
트랜잭션을 커밋하려면 `commit` 메서드를 호출하세요.

```
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 관련 메서드는 [query builder](/docs/10.x/queries)와 [Eloquent ORM](/docs/10.x/eloquent) 모두에서 동작합니다.

<a name="connecting-to-the-database-cli"></a>
<!-- ## Connecting to the Database CLI -->
## Connecting to the Database CLI

<!-- If you would like to connect to your database's CLI, you may use the `db` Artisan command: -->
데이터베이스의 CLI에 접속하고 싶다면, `db` Artisan 명령어를 사용하세요.

```shell
php artisan db
```

<!-- If needed, you may specify a database connection name to connect to a database connection that is not the default connection: -->
필요하다면, 기본 연결이 아니라 특정 데이터베이스 연결명을 지정할 수도 있습니다.

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
<!-- ## Inspecting Your Databases -->
## Inspecting Your Databases

<!-- Using the `db:show` and `db:table` Artisan commands, you can get valuable insight into your database and its associated tables. To see an overview of your database, including its size, type, number of open connections, and a summary of its tables, you may use the `db:show` command: -->
`db:show` 및 `db:table` Artisan 명령어를 활용하면, 데이터베이스와 관련 테이블에 대한 유용한 정보를 얻을 수 있습니다. 데이터베이스의 전체 개요(크기, 타입, 열린 연결 개수, 테이블 요약 등)를 보려면 `db:show` 명령어를 사용하세요.

```shell
php artisan db:show
```

<!-- You may specify which database connection should be inspected by providing the database connection name to the command via the `--database` option: -->
특정 데이터베이스 연결을 조회하려면 `--database` 옵션에 연결명을 지정하면 됩니다.

```shell
php artisan db:show --database=pgsql
```

<!-- If you would like to include table row counts and database view details within the output of the command, you may provide the `--counts` and `--views` options, respectively. On large databases, retrieving row counts and view details can be slow: -->
테이블의 행 개수 및 데이터베이스 뷰 세부 정보를 출력에 포함하고 싶다면, 각각 `--counts`와 `--views` 옵션을 추가하세요. 단, 큰 데이터베이스에서는 이 정보 추출이 다소 느릴 수 있습니다.

```shell
php artisan db:show --counts --views
```

<a name="table-overview"></a>
<!-- #### Table Overview -->
#### Table Overview

<!-- If you would like to get an overview of an individual table within your database, you may execute the `db:table` Artisan command. This command provides a general overview of a database table, including its columns, types, attributes, keys, and indexes: -->
특정 테이블의 개요 정보를 확인하려면, `db:table` Artisan 명령어를 실행하세요. 이 명령어는 테이블의 컬럼, 타입, 속성, 키, 인덱스 등 기본 정보를 요약하여 보여줍니다.

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
<!-- ## Monitoring Your Databases -->
## Monitoring Your Databases

<!-- Using the `db:monitor` Artisan command, you can instruct Laravel to dispatch an `Illuminate\Database\Events\DatabaseBusy` event if your database is managing more than a specified number of open connections. -->
`db:monitor` Artisan 명령어를 사용하면, 데이터베이스에서 관리하는 열린 연결 개수가 지정한 임계값을 초과하는 경우 `Illuminate\Database\Events\DatabaseBusy` 이벤트가 발생하도록 Laravel에 지시할 수 있습니다.

<!-- To get started, you should schedule the `db:monitor` command to [run every minute](/docs/10.x/scheduling). The command accepts the names of the database connection configurations that you wish to monitor as well as the maximum number of open connections that should be tolerated before dispatching an event: -->
먼저, `db:monitor` 명령어를 [run every minute](/docs/10.x/scheduling)되도록 스케줄링하세요. 이 명령어에는 모니터링할 데이터베이스 연결명들과, 이벤트가 발생하기 전까지 허용할 최대 연결 개수를 넘겨줄 수 있습니다.

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

<!-- Scheduling this command alone is not enough to trigger a notification alerting you of the number of open connections. When the command encounters a database that has an open connection count that exceeds your threshold, a `DatabaseBusy` event will be dispatched. You should listen for this event within your application's `EventServiceProvider` in order to send a notification to you or your development team: -->
이 명령어를 단순히 스케줄링하는 것만으로는 알림이 전송되거나 경고를 받을 수 없습니다. 명령어 실행 중 지정 임계값을 초과한 데이터베이스가 있으면, `DatabaseBusy` 이벤트가 발생합니다. 알림을 받고 싶다면, 애플리케이션의 `EventServiceProvider`에서 이 이벤트를 리스닝하여 여러분 또는 개발팀에 알림(예: 이메일 등)이 가도록 설정해야 합니다.

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Register any other events for your application.
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
