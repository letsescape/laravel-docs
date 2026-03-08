# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행](#running-queries)
    - [여러 데이터베이스 연결 사용](#using-multiple-database-connections)
    - [쿼리 이벤트 리스닝](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결](#connecting-to-the-database-cli)
- [데이터베이스 검사](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개 (Introduction)

거의 모든 최신 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 데이터베이스를 지원하며, 원시 SQL, [플루언트 쿼리 빌더](/docs/master/queries), [Eloquent ORM](/docs/master/eloquent)를 통해 데이터베이스와 매우 쉽게 연동할 수 있도록 해줍니다. 현재 Laravel은 다음 다섯 가지 데이터베이스에 대해 1차 지원을 제공합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([지원 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([지원 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([지원 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([지원 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

추가적으로, MongoDB는 `mongodb/laravel-mongodb` 패키지를 통해 지원되며, 이 패키지는 MongoDB에서 공식적으로 관리하고 있습니다. 자세한 내용은 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 데이터베이스 서비스 설정 파일은 애플리케이션의 `config/database.php`에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의하고, 기본으로 사용할 연결을 지정할 수 있습니다. 이 파일의 대부분의 설정 옵션은 애플리케이션 환경 변수의 값에 의해 제어됩니다. Laravel이 지원하는 대부분의 데이터베이스 시스템에 대한 예시도 이 파일에 포함되어 있습니다.

기본적으로 Laravel의 샘플 [환경 설정](/docs/master/configuration#environment-configuration)은 [Laravel Sail](/docs/master/sail)과 함께 바로 사용할 수 있습니다. Sail은 로컬 개발을 위한 Docker 기반 Laravel 애플리케이션 개발 환경입니다. 그러나 로컬 데이터베이스 환경에 맞게 데이터베이스 설정을 자유롭게 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템의 단일 파일에 저장됩니다. 터미널에서 `touch` 명령어로 새로운 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성된 후, 절대 경로를 `DB_DATABASE` 환경 변수에 지정하여 해당 데이터베이스를 사용할 수 있도록 설정합니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로, SQLite 연결에서는 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하세요:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel 설치 도구](/docs/master/installation#creating-a-laravel-project)를 사용해 Laravel 애플리케이션을 생성하고 데이터베이스로 SQLite를 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하고 기본 [데이터베이스 마이그레이션](/docs/master/migrations)도 실행해 줍니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv` 및 `pdo_sqlsrv` PHP 확장 모듈, 그리고 Microsoft SQL ODBC 드라이버 등 필요한 의존성이 모두 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 사용한 설정 (Configuration Using URLs)

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 개의 설정 값으로 구성합니다. 각각의 설정 값은 별도의 환경 변수를 가집니다. 즉, 운영 서버에서 데이터베이스 연결 정보를 설정할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku 등 일부 매니지드 데이터베이스 제공업체는 데이터베이스 연결 정보를 하나의 문자열로 담은 "URL"을 제공하기도 합니다. 예시 데이터베이스 URL은 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이러한 URL은 일반적으로 다음과 같은 표준 스키마를 따릅니다:

```html
driver://username:password@host:port/database?options
```

Laravel은 편의성을 위해, 여러 설정 값을 따로 분리하지 않고 이러한 URL 하나로 데이터베이스를 설정할 수 있는 기능을 제공합니다. 만약 `url` (또는 `DB_URL` 환경 변수) 설정 값이 존재하면 Laravel은 이 URL에서 데이터베이스 연결 정보와 자격 증명을 추출해 사용합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결 (Read and Write Connections)

경우에 따라 SELECT 구문 등 읽기 작업에는 한 데이터베이스 연결을, INSERTㆍUPDATEㆍDELETE 같은 쓰기 작업에는 다른 연결을 사용할 수 있습니다. Laravel에서는 아주 간단하게 이러한 설정이 가능하며, 쿼리 빌더나 Eloquent ORM, 원시 쿼리 어느 경우에도 적절한 연결이 항상 사용됩니다.

읽기/쓰기 연결을 어떻게 설정해야 하는지 아래 예시를 통해 살펴보겠습니다:

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

위 예시에서, 설정 배열에 `read`, `write`, `sticky` 키가 추가된 것을 볼 수 있습니다. `read`, `write` 키에는 각각 `host`라는 키가 있고, 나머지 데이터베이스 옵션들은 기본 `mysql` 설정 배열에서 병합되어 사용됩니다.

`read`, `write` 배열에는 오버라이드가 필요한 값만 지정하면 됩니다. 위 경우 "읽기" 연결의 호스트로 `192.168.1.1`, "쓰기" 연결의 호스트로는 `192.168.1.3`이 사용됩니다. 데이터베이스 인증 정보, 프리픽스, 문자셋 등 나머지 옵션은 두 연결 모두 기본 `mysql` 배열 값이 공유됩니다. 만약 `host`에 값이 여러 개인 배열이라면, 각 요청마다 임의로 데이터베이스 호스트가 선택됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택적*이며, 현재 요청 주기에서 데이터베이스에 쓰기 작업이 수행된 뒤 곧바로 읽기 작업을 실행할 때 읽기 연결 대신 쓰기 연결을 사용하도록 해줍니다. 즉, `sticky`가 활성화되어 있고 현재 요청에서 "쓰기" 작업이 한 번이라도 발생했다면, 이후 "읽기" 작업은 계속 "쓰기" 연결을 통해 이루어집니다. 이를 통해 같은 요청 내에서 업데이트된 데이터를 바로 읽어올 수 있습니다. 이런 동작이 애플리케이션에 필요한지 여부는 직접 판단해서 설정해야 합니다.

<a name="running-queries"></a>
## SQL 쿼리 실행 (Running SQL Queries)

데이터베이스 연결을 설정한 후에는 `DB` 파사드(Facade)를 사용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 쿼리 종류마다 `select`, `update`, `insert`, `delete`, `statement` 등의 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### Select 쿼리 실행

기본 SELECT 쿼리를 실행하려면 `DB` 파사드의 `select` 메서드를 사용합니다:

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

`select` 메서드의 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 쿼리에 바인딩되어야 할 매개변수(인자)입니다. 일반적으로 이는 WHERE 절 조건 값이 들어갑니다. 파라미터 바인딩을 통해 SQL 인젝션 공격을 방지할 수 있습니다.

`select` 메서드는 항상 결과가 담긴 `array`를 반환합니다. 배열의 각 요소는 데이터베이스 레코드를 나타내는 PHP의 `stdClass` 객체입니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택

때로는 데이터베이스 쿼리 결과가 단일 스칼라(숫자, 문자 등) 값일 수 있습니다. 이때 레코드 객체에서 값을 꺼내지 않고, Laravel의 `scalar` 메서드를 사용해 값을 바로 반환받을 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### 다중 결과 집합 선택

저장 프로시저를 호출해 다중 결과 집합을 반환받는 경우, `selectResultSets` 메서드를 사용해 반환된 모든 결과 집합을 가져올 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### 이름 있는 바인딩 사용

`?` 대신 명명된 바인딩을 사용할 수도 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### Insert 구문 실행

`insert` 문을 실행하려면, `DB` 파사드의 `insert` 메서드를 사용합니다. 기본적으로 `select`와 마찬가지로 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 바인딩 값입니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### Update 구문 실행

`update` 메서드는 데이터베이스 내 기존 레코드를 업데이트할 때 사용합니다. 해당 쿼리로 영향을 받는 행(row)의 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### Delete 구문 실행

`delete` 메서드는 레코드를 삭제할 때 사용합니다. 영향을 받은 행의 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반 구문 실행

반환값이 없는 SQL 구문에 대해서는 `statement` 메서드를 사용할 수 있습니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### 바인딩 없이 SQL 실행

간혹 바인딩 없는 SQL 구문을 그대로 실행해야 할 때는 `unprepared` 메서드를 사용할 수 있습니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> unprepared 구문은 파라미터 바인딩을 지원하지 않으므로 SQL 인젝션에 취약할 수 있습니다. 사용자 입력이 직접적으로 들어가는 경우에는 절대 사용하지 마십시오.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋 (Implicit Commits)

트랜잭션 내에서 `DB` 파사드의 `statement`, `unprepared` 메서드를 사용할 때, 암묵적으로 커밋을 발생시키는 쿼리를 주의해야 합니다. 이 경우 데이터베이스 엔진이 트랜잭션을 묵시적으로 커밋하게 돼, Laravel은 트랜잭션 상태를 인식하지 못할 수 있습니다. 예를 들어, 테이블 생성과 같은 구문이 이에 해당합니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

암묵적으로 커밋을 발생시키는 모든 구문의 목록은 MySQL 설명서를 참고하세요: [암묵적 커밋 구문 목록](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)

<a name="using-multiple-database-connections"></a>
### 여러 데이터베이스 연결 사용

`config/database.php`에서 여러 연결을 정의한 경우, `DB` 파사드의 `connection` 메서드로 각 연결에 접근할 수 있습니다. 인수로 넘기는 연결명은 `config/database.php` 파일에 정의되어 있거나, 런타임 시 `config` 헬퍼로 설정한 것이어야 합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

해당 연결의 원시 PDO 인스턴스에 접근하려면 `getPdo` 메서드를 사용할 수 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝

애플리케이션 내에서 실행되는 각 SQL 쿼리마다 호출되는 클로저를 지정할 수도 있습니다. 이 기능은 쿼리 로깅이나 디버깅에 유용하게 사용할 수 있습니다. 쿼리 리스너 클로저는 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 등록할 수 있습니다:

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
### 누적 쿼리 시간 모니터링

현대 웹 애플리케이션에서 자주 발생하는 성능 병목 중 하나는 데이터베이스 쿼리에 소요되는 시간입니다. Laravel은 단일 요청에서 너무 긴 쿼리 시간이 감지되면 지정한 콜백이나 클로저를 호출해 이를 감지할 수 있습니다. 시작하려면 쿼리 시간 임계값(밀리초 단위)과 클로저를 `whenQueryingForLongerThan` 메서드에 지정하면 됩니다. 이 메서드 역시 [서비스 프로바이더](/docs/master/providers)의 `boot` 메서드에서 호출할 수 있습니다:

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
            // 개발팀에 알림 전송 등...
        });
    }
}
```

<a name="database-transactions"></a>
## 데이터베이스 트랜잭션 (Database Transactions)

여러 데이터베이스 작업을 하나의 트랜잭션으로 묶으려면 `DB` 파사드의 `transaction` 메서드를 사용할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 전체 트랜잭션은 자동으로 롤백되고, 예외는 다시 던져집니다. 클로저가 정상적으로 실행된다면 자동으로 커밋이 이루어집니다. 즉, `transaction` 메서드를 사용하면 직접 롤백이나 커밋을 명시적으로 관리할 필요가 없습니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 교착 상태(Deadlock) 처리

`transaction` 메서드는 선택적으로 두 번째 인수를 받아, 교착 상태가 발생할 때 트랜잭션이 재시도될 횟수를 지정할 수 있습니다. 정해진 횟수만큼 재시도해도 문제가 해결되지 않으면 예외가 발생합니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, attempts: 5);
```

<a name="manually-using-transactions"></a>
#### 수동 트랜잭션 처리

트랜잭션을 수동으로 시작해 커밋과 롤백을 직접 제어하려면, `DB` 파사드의 `beginTransaction` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

롤백은 `rollBack` 메서드로 수행할 수 있습니다:

```php
DB::rollBack();
```

커밋은 `commit` 메서드를 활용하세요:

```php
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/master/queries)와 [Eloquent ORM](/docs/master/eloquent) 모두에서 동작합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결 (Connecting to the Database CLI)

데이터베이스의 CLI에 접속하려면, `db` 아티즌(Artisan) 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

필요한 경우, 기본 접속이 아닌 별도의 데이터베이스 연결명을 명시해 접속할 수도 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사 (Inspecting Your Databases)

`db:show` 및 `db:table` 아티즌 명령어를 활용해 데이터베이스와 테이블에 대한 유용한 정보를 확인할 수 있습니다. 데이터베이스의 크기, 타입, 열린 연결 수, 테이블 요약 등의 개요를 보려면 `db:show` 명령어를 사용할 수 있습니다:

```shell
php artisan db:show
```

`--database` 옵션에 데이터베이스 연결명을 지정해 점검할 대상을 지정할 수도 있습니다:

```shell
php artisan db:show --database=pgsql
```

테이블의 행 수(row count) 및 데이터베이스 뷰(view) 정보까지 포함하고 싶다면, 각각 `--counts`, `--views` 옵션을 추가할 수 있습니다. 단, 대용량 데이터베이스에서는 이 작업이 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

또한, 아래와 같이 `Schema` 메서드를 사용해 코드 내에서 데이터베이스를 검사할 수 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

기본 연결이 아닌 다른 데이터베이스의 정보를 조회하려면 `connection` 메서드를 사용하면 됩니다:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### 테이블 개요

특정 테이블의 개요 정보를 보고 싶을 때는 `db:table` 아티즌 명령어를 실행합니다. 이 명령어는 테이블의 컬럼, 타입, 속성, 키, 인덱스 등을 포함한 일반적인 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링 (Monitoring Your Databases)

`db:monitor` 아티즌 명령어를 사용하면, 열려 있는 연결 수가 지정한 수치를 초과하는 경우 Laravel에서 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 발생시킬 수 있습니다.

먼저, `db:monitor` 명령어를 [1분마다 실행되도록 예약](/docs/master/scheduling)해야 합니다. 명령어는 모니터링할 데이터베이스 연결명과 이벤트 발생 임계치를 옵션으로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

이 명령어만 예약한다고 바로 알림을 받을 수 있는 것은 아닙니다. 명령어가 임계치 이상으로 연결이 열린 데이터베이스를 발견하면 `DatabaseBusy` 이벤트를 발생시킵니다. 이 이벤트를 애플리케이션의 `AppServiceProvider`에서 리스닝해 직접 자신(또는 개발팀)에게 알림을 전송하도록 구현해야 합니다:

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