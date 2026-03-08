# 데이터베이스: 시작하기 (Database: Getting Started)

- [소개](#introduction)
    - [설정](#configuration)
    - [읽기 및 쓰기 연결](#read-and-write-connections)
- [SQL 쿼리 실행하기](#running-queries)
    - [여러 데이터베이스 연결 사용하기](#using-multiple-database-connections)
    - [쿼리 이벤트 리스닝](#listening-for-query-events)
    - [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 연결](#connecting-to-the-database-cli)
- [데이터베이스 검사](#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개 (Introduction)

대부분의 현대 웹 애플리케이션은 데이터베이스와 상호작용합니다. Laravel은 다양한 지원 데이터베이스들과의 상호작용을 매우 간단하게 만들어 줍니다. 원시 SQL, [플루언트 쿼리 빌더](/docs/12.x/queries), 그리고 [Eloquent ORM](/docs/12.x/eloquent)을 모두 사용할 수 있습니다. 현재 Laravel은 다음 5가지 데이터베이스를 공식적으로 1차 지원합니다:

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([버전 정책](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ ([버전 정책](https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+ ([버전 정책](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

추가적으로, MongoDB는 공식적으로 MongoDB에서 유지보수하는 `mongodb/laravel-mongodb` 패키지를 통해 지원합니다. 자세한 정보는 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 문서를 참고하세요.

<a name="configuration"></a>
### 설정 (Configuration)

Laravel의 데이터베이스 서비스 설정은 애플리케이션의 `config/database.php` 설정 파일에 위치합니다. 이 파일에서 모든 데이터베이스 연결을 정의할 수 있으며, 기본으로 사용할 연결도 지정할 수 있습니다. 이 파일의 대부분의 설정 옵션들은 애플리케이션의 환경 변수 값에 의해 제어됩니다. 대부분의 Laravel이 지원하는 데이터베이스 시스템 예제들이 이 파일에 포함되어 있습니다.

기본적으로, Laravel의 샘플 [환경 설정](/docs/12.x/configuration#environment-configuration)은 [Laravel Sail](/docs/12.x/sail)과 바로 사용할 수 있도록 준비되어 있습니다. 이는 로컬 머신에서 Laravel 애플리케이션을 개발하기 위한 Docker 설정입니다. 그러나, 필요시 로컬 데이터베이스에 맞게 설정을 자유롭게 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 설정

SQLite 데이터베이스는 파일 시스템의 단일 파일에 저장됩니다. 터미널에서 `touch` 명령어로 새로운 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성된 후, `DB_DATABASE` 환경 변수에 데이터베이스의 절대 경로를 지정하면 환경 변수 설정이 완료됩니다:

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```

기본적으로 SQLite 연결에서는 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정하면 됩니다:

```ini
DB_FOREIGN_KEYS=false
```

> [!NOTE]
> [Laravel 인스톨러](/docs/12.x/installation#creating-a-laravel-project)로 Laravel 애플리케이션을 생성하고 데이터베이스로 SQLite를 선택하면, Laravel이 자동으로 `database/database.sqlite` 파일을 생성하고 기본 [데이터베이스 마이그레이션](/docs/12.x/migrations)을 실행합니다.

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 설정

Microsoft SQL Server 데이터베이스를 사용하려면, `sqlsrv` 및 `pdo_sqlsrv` PHP 확장과, 이들이 필요로 하는 Microsoft SQL ODBC 드라이버와 같은 의존성이 설치되어 있어야 합니다.

<a name="configuration-using-urls"></a>
#### URL을 활용한 설정

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등 여러 설정값을 통해 구성합니다. 각각의 값은 해당하는 환경 변수로 관리합니다. 즉, 프로덕션 서버에서 데이터베이스 연결 정보를 설정할 때 여러 환경 변수를 관리해야 합니다.

AWS, Heroku와 같은 일부 매니지드 데이터베이스 제공 업체는 모든 연결 정보를 하나의 문자열로 담은 데이터베이스 "URL"을 제공합니다. 예시 데이터베이스 URL은 다음과 같습니다:

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```

이들 URL은 일반적으로 아래와 같은 표준 스키마를 따릅니다:

```html
driver://username:password@host:port/database?options
```

편의상, Laravel에서는 여러 설정값 대신 이러한 URL로 데이터베이스를 연결할 수 있습니다. `url`(또는 환경 변수 `DB_URL`) 옵션이 존재한다면, 해당 값을 통해 연결 및 인증 정보를 추출해 사용합니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결 (Read and Write Connections)

가끔 SELECT 쿼리에는 한 데이터베이스 연결을, INSERT/UPDATE/DELETE 쿼리에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel은 이 구성을 손쉽게 지원하며, 원시 쿼리나 쿼리 빌더, Eloquent ORM을 사용할 때도 항상 올바른 연결을 사용합니다.

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

위 구성 배열에는 `read`, `write`, `sticky`라는 세 개의 키가 있으며, `read`와 `write` 안에는 각각 `host`가 존재합니다. `read` 및 `write` 연결의 그 외 데이터베이스 옵션은 메인 `mysql` 배열에서 병합됩니다.

만약 메인 `mysql` 배열의 값을 덮어쓰고자 할 때만 `read`, `write` 배열에 값을 지정하면 됩니다. 이 예제에서는 `"read"` 연결에는 `192.168.1.1`이, `"write"` 연결에는 `192.168.1.3`이 사용됩니다. 데이터베이스 자격증명, prefix, 문자셋 등 나머지 옵션은 메인 배열과 공유합니다. `host`가 여러 값으로 배열에 정의되어 있다면, 각 요청마다 무작위로 선택된 호스트가 사용됩니다.

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 *선택적인* 값으로, 현재 요청 사이클에서 데이터베이스에 쓰기 작업이 발생한 경우 곧바로 읽기 작업도 `"write"` 연결을 사용하도록 합니다. 즉, 한 요청 내에서 데이터가 저장되면 즉시 해당 데이터를 동일한 연결에서 읽을 수 있습니다. 이 행동이 애플리케이션에 필요한지 여부는 직접 판단해서 설정하면 됩니다.

<a name="running-queries"></a>
## SQL 쿼리 실행하기 (Running SQL Queries)

데이터베이스 연결을 설정한 후에는 `DB` 파사드(facade)를 이용해 쿼리를 실행할 수 있습니다. `DB` 파사드는 각 쿼리 유형별로 `select`, `update`, `insert`, `delete`, `statement` 메서드를 제공합니다.

<a name="running-a-select-query"></a>
#### SELECT 쿼리 실행하기

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

`select` 메서드의 첫 번째 인수는 SQL 쿼리, 두 번째 인수는 쿼리에 바인딩할 파라미터입니다. 일반적으로 WHERE 절 제약 조건의 값을 의미합니다. 파라미터 바인딩을 통해 SQL 인젝션 공격 위험을 방지할 수 있습니다.

`select` 메서드는 항상 결과값을 배열로 반환합니다. 배열의 각 요소는 데이터베이스의 레코드를 나타내는 PHP의 `stdClass` 객체입니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```

<a name="selecting-scalar-values"></a>
#### 단일 값(스칼라) 조회

쿼리 결과가 단일값(스칼라)인 경우, Laravel에서는 `scalar` 메서드를 통해 객체에서 값을 추출하지 않고 바로 값을 얻을 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```

<a name="selecting-multiple-result-sets"></a>
#### 다중 결과셋 조회

저장 프로시저 호출로 여러 결과셋이 반환되는 경우, `selectResultSets` 메서드를 사용해 모든 결과셋을 가져올 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```

<a name="using-named-bindings"></a>
#### 이름 바인딩 사용하기

파라미터 바인딩 시 `?` 대신 이름 바인딩을 사용할 수 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```

<a name="running-an-insert-statement"></a>
#### INSERT문 실행하기

`insert` 메서드를 사용해 INSERT 쿼리를 실행할 수 있습니다. 인자 구조는 `select`와 동일합니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```

<a name="running-an-update-statement"></a>
#### UPDATE문 실행하기

`update` 메서드는 기존 레코드의 값을 변경할 때 사용합니다. 영향받은 행(row)의 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```

<a name="running-a-delete-statement"></a>
#### DELETE문 실행하기

`delete` 메서드는 레코드 삭제에 사용하며, 마찬가지로 영향받은 행의 수를 반환합니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```

<a name="running-a-general-statement"></a>
#### 일반 쿼리 실행하기

일부 데이터베이스 쿼리는 반환값이 없습니다. 이런 경우에는 `statement` 메서드를 사용합니다:

```php
DB::statement('drop table users');
```

<a name="running-an-unprepared-statement"></a>
#### Unprepared 쿼리 실행하기

값을 바인딩하지 않고 SQL 쿼리를 직접 실행하고 싶을 때는 `unprepared` 메서드를 사용합니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```

> [!WARNING]
> unprepared 쿼리는 파라미터를 바인딩하지 않으므로 SQL 인젝션 공격에 취약할 수 있습니다. 사용자 입력이 포함된 unprepared 쿼리는 절대 사용해서는 안 됩니다.

<a name="implicit-commits-in-transactions"></a>
#### 암시적 커밋(Implicit Commits)

트랜잭션 내에서 `statement`나 `unprepared` 메서드를 사용할 때는 [암시적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 발생시키는 쿼리를 주의하세요. 이런 쿼리는 데이터베이스 엔진이 트랜잭션 전체를 간접적으로 커밋하여, Laravel이 트랜잭션 레벨을 제대로 인지하지 못하게 됩니다. 예를 들어, 테이블을 생성하는 쿼리 등이 이에 해당합니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```

암시적 커밋을 발생시키는 명령어의 전체 목록은 MySQL 매뉴얼의 [관련 문서](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)를 참고하세요.

<a name="using-multiple-database-connections"></a>
### 여러 데이터베이스 연결 사용하기

애플리케이션의 `config/database.php` 파일에 여러 연결이 정의되어 있다면, `DB` 파사드의 `connection` 메서드를 통해 각 연결을 사용할 수 있습니다. `connection` 메서드에 지정하는 연결명은 설정 파일에 정의되어 있거나, 런타임에 `config` 헬퍼로 설정한 값이어야 합니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```

각 연결 인스턴스의 `getPdo` 메서드를 사용하면, 원시 PDO 인스턴스에 직접 접근할 수 있습니다:

```php
$pdo = DB::connection()->getPdo();
```

<a name="listening-for-query-events"></a>
### 쿼리 이벤트 리스닝

애플리케이션의 모든 SQL 쿼리 실행 시마다 클로저를 호출하고 싶다면, `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 기능은 쿼리 로깅이나 디버깅에 유용합니다. 쿼리 리스너 클로저는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 등록 가능합니다:

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

웹 애플리케이션의 주요 성능 병목지점 중 하나는 데이터베이스 쿼리에 소요되는 시간입니다. Laravel에서는 한 요청 내에서 쿼리 수행 시간이 너무 길어질 때, 지정한 클로저나 콜백을 호출할 수 있습니다. 설정 방법은 `whenQueryingForLongerThan` 메서드에 임계 시간(밀리초 단위)과 클로저를 전달하는 것입니다. 이 메서드는 [서비스 프로바이더](/docs/12.x/providers)의 `boot` 메서드에서 사용할 수 있습니다:

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

`DB` 파사드의 `transaction` 메서드를 이용하여 여러 데이터베이스 작업을 트랜잭션으로 묶어 실행할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 트랜잭션이 자동 롤백되고 예외가 다시 발생합니다. 클로저가 성공적으로 실행될 경우 자동으로 커밋됩니다. 별도로 롤백 또는 커밋을 신경 쓸 필요가 없습니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```

<a name="handling-deadlocks"></a>
#### 데드락(교착상태) 처리

`transaction` 메서드는 두 번째 인자로 데드락 발생 시 재시도할 횟수를 지정할 수 있습니다. 지정한 횟수만큼 재시도 후에도 실패하면 예외가 발생합니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, attempts: 5);
```

<a name="manually-using-transactions"></a>
#### 트랜잭션 수동 관리

트랜잭션을 직접 시작하고 커밋/롤백을 세밀하게 제어하고 싶다면 `beginTransaction` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```

트랜잭션을 롤백하려면 `rollBack` 메서드를 사용하십시오:

```php
DB::rollBack();
```

마지막으로 트랜잭션을 커밋하려면 `commit` 메서드를 사용합니다:

```php
DB::commit();
```

> [!NOTE]
> `DB` 파사드의 트랜잭션 관련 메서드는 [쿼리 빌더](/docs/12.x/queries)와 [Eloquent ORM](/docs/12.x/eloquent) 모두의 트랜잭션을 제어합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI 연결 (Connecting to the Database CLI)

데이터베이스의 CLI에 연결하려면 `db` 아티즌 명령어를 사용할 수 있습니다:

```shell
php artisan db
```

필요하다면, 기본 연결이 아닌 다른 데이터베이스 연결명을 명령 인자로 지정할 수 있습니다:

```shell
php artisan db mysql
```

<a name="inspecting-your-databases"></a>
## 데이터베이스 검사 (Inspecting Your Databases)

`db:show` 및 `db:table` 아티즌 명령어를 사용하여 데이터베이스와 해당 테이블 정보를 상세히 확인할 수 있습니다. 데이터베이스의 개요(크기, 종류, 활성 연결 수, 테이블 요약 등)를 확인하려면 다음 명령어를 사용하세요:

```shell
php artisan db:show
```

확인할 데이터베이스 연결명을 `--database` 옵션으로 지정할 수도 있습니다:

```shell
php artisan db:show --database=pgsql
```

명령 출력에 테이블 행(row) 개수나 데이터베이스 뷰 정보를 포함하려면 `--counts` 또는 `--views` 옵션을 사용할 수 있습니다. 대형 데이터베이스의 경우 행 개수나 뷰 정보 확인이 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```

추가로, `Schema`의 다음 메서드들을 통해 데이터베이스 구조를 코드로도 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```

애플리케이션의 기본 연결이 아닌 데이터베이스를 검사하려면 `connection` 메서드를 사용할 수 있습니다:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```

<a name="table-overview"></a>
#### 테이블 개요

특정 테이블의 정보를 확인하려면 `db:table` 아티즌 명령어를 사용할 수 있습니다. 이 명령은 컬럼, 타입, 속성, 키, 인덱스 등 테이블의 일반 정보를 제공합니다:

```shell
php artisan db:table users
```

<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링 (Monitoring Your Databases)

`db:monitor` 아티즌 명령어를 사용하면 데이터베이스의 열린 연결 수가 지정된 수를 초과할 때 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 Laravel이 발생시킵니다.

시작하려면, `db:monitor` 명령어를 [매 분마다 실행](/docs/12.x/scheduling)하도록 스케줄링하세요. 이 명령은 모니터링할 데이터베이스 연결명과, 이벤트 발생 전 견딜 수 있는 최대 열린 연결 수를 인자로 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```

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