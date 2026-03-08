# 데이터베이스: 마이그레이션 (Database: Migrations)

- [소개](#introduction)
- [마이그레이션 생성](#generating-migrations)
    - [마이그레이션 스쿼싱](#squashing-migrations)
- [마이그레이션 구조](#migration-structure)
- [마이그레이션 실행](#running-migrations)
    - [마이그레이션 롤백](#rolling-back-migrations)
- [테이블](#tables)
    - [테이블 생성](#creating-tables)
    - [테이블 수정](#updating-tables)
    - [테이블 이름 변경 / 삭제](#renaming-and-dropping-tables)
- [컬럼](#columns)
    - [컬럼 생성](#creating-columns)
    - [사용 가능한 컬럼 타입](#available-column-types)
    - [컬럼 수정자](#column-modifiers)
    - [컬럼 수정](#modifying-columns)
    - [컬럼 이름 변경](#renaming-columns)
    - [컬럼 삭제](#dropping-columns)
- [인덱스](#indexes)
    - [인덱스 생성](#creating-indexes)
    - [인덱스 이름 변경](#renaming-indexes)
    - [인덱스 삭제](#dropping-indexes)
    - [외래 키 제약 조건](#foreign-key-constraints)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

마이그레이션(Migrations)은 데이터베이스를 위한 버전 관리 시스템과 같은 역할을 합니다. 이를 통해 팀이 애플리케이션의 데이터베이스 스키마 정의를 함께 관리하고 공유할 수 있습니다.  

예를 들어, 소스 코드를 pull 한 뒤 동료에게 “로컬 데이터베이스에 컬럼 하나를 수동으로 추가해야 한다”고 말해야 했던 경험이 있다면, 바로 이러한 문제를 해결하기 위해 데이터베이스 마이그레이션이 존재합니다.

Laravel의 `Schema` [facade](/docs/12.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블을 생성하고 수정할 수 있도록 데이터베이스에 종속되지 않는 기능을 제공합니다. 일반적으로 마이그레이션에서는 이 facade를 사용하여 데이터베이스 테이블과 컬럼을 생성하거나 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성 (Generating Migrations)

데이터베이스 마이그레이션을 생성하려면 `make:migration` [Artisan 명령어](/docs/12.x/artisan)를 사용할 수 있습니다. 새로 생성된 마이그레이션은 `database/migrations` 디렉토리에 저장됩니다. 각 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있으며, 이를 통해 Laravel은 마이그레이션 실행 순서를 결정합니다.

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름을 기반으로 테이블 이름과 새 테이블 생성 여부를 추측합니다. 만약 Laravel이 마이그레이션 이름에서 테이블 이름을 정확히 판단할 수 있다면, 생성된 마이그레이션 파일에 해당 테이블이 미리 설정됩니다. 그렇지 않은 경우에는 마이그레이션 파일에서 직접 테이블을 지정하면 됩니다.

생성되는 마이그레이션의 경로를 사용자 지정하고 싶다면 `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 이 경로는 애플리케이션의 base path를 기준으로 한 상대 경로여야 합니다.

> [!NOTE]
> 마이그레이션 스텁(Migration stub)은 [stub publishing](/docs/12.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱 (Squashing Migrations)

애플리케이션을 개발하다 보면 시간이 지남에 따라 마이그레이션 파일이 계속 누적됩니다. 그 결과 `database/migrations` 디렉토리에 수백 개의 마이그레이션 파일이 쌓일 수 있습니다. 이런 경우 여러 마이그레이션을 하나의 SQL 파일로 "스쿼싱(squash)"할 수 있습니다.

먼저 `schema:dump` 명령어를 실행합니다.

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션을 모두 정리...
php artisan schema:dump --prune
```

이 명령어를 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉토리에 "schema" 파일을 생성합니다. 이 파일의 이름은 데이터베이스 연결 이름과 동일하게 생성됩니다.

이후 데이터베이스 마이그레이션을 실행할 때, 아직 어떤 마이그레이션도 실행되지 않은 상태라면 Laravel은 먼저 현재 사용 중인 데이터베이스 연결에 해당하는 schema 파일의 SQL 문을 실행합니다. 그 다음 schema dump에 포함되지 않은 나머지 마이그레이션들을 실행합니다.

만약 애플리케이션 테스트에서 로컬 개발 환경과 다른 데이터베이스 연결을 사용한다면, 테스트 데이터베이스 연결로도 schema dump 파일을 생성해야 합니다. 일반적으로 로컬 개발용 데이터베이스를 덤프한 후 다음과 같이 실행할 수 있습니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

팀의 다른 개발자가 빠르게 초기 데이터베이스 구조를 생성할 수 있도록 데이터베이스 schema 파일을 소스 코드 저장소에 커밋하는 것이 좋습니다.

> [!WARNING]
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며 데이터베이스의 커맨드라인 클라이언트를 사용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스에는 두 개의 메서드가 있습니다: `up`과 `down`.

- `up` 메서드: 새로운 테이블, 컬럼, 인덱스를 데이터베이스에 추가
- `down` 메서드: `up` 메서드에서 수행한 작업을 되돌림

이 두 메서드 안에서는 Laravel의 schema builder를 사용하여 테이블을 생성하거나 수정할 수 있습니다. `Schema` builder에서 사용할 수 있는 모든 메서드는 [해당 문서](#creating-tables)를 참고하십시오.

다음 예제는 `flights` 테이블을 생성하는 마이그레이션입니다.

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
#### 마이그레이션 데이터베이스 연결 설정

마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 연결을 사용해야 한다면, 마이그레이션 클래스의 `$connection` 속성을 설정해야 합니다.

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
#### 마이그레이션 건너뛰기

특정 마이그레이션이 아직 활성화되지 않은 기능을 지원하기 위한 것이라면, 지금 당장 실행되지 않도록 할 수도 있습니다. 이 경우 마이그레이션에 `shouldRun` 메서드를 정의할 수 있습니다.

`shouldRun` 메서드가 `false`를 반환하면 해당 마이그레이션은 실행되지 않습니다.

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
## 마이그레이션 실행 (Running Migrations)

아직 실행되지 않은 모든 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 사용합니다.

```shell
php artisan migrate
```

이미 실행된 마이그레이션과 아직 실행되지 않은 마이그레이션의 상태를 확인하려면 `migrate:status` 명령어를 사용할 수 있습니다.

```shell
php artisan migrate:status
```

`migrate` 명령어에 `--step` 옵션을 사용하면 각 마이그레이션을 별도의 batch로 실행합니다. 이렇게 하면 이후 `migrate:rollback` 명령어를 통해 개별 마이그레이션을 롤백할 수 있습니다.

```shell
php artisan migrate --step
```

마이그레이션을 실제로 실행하지 않고 실행될 SQL 문만 확인하고 싶다면 `--pretend` 옵션을 사용할 수 있습니다.

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
#### 마이그레이션 실행 격리

여러 서버에 애플리케이션을 배포하고 배포 과정에서 마이그레이션을 실행한다면, 동시에 두 서버가 데이터베이스 마이그레이션을 실행하는 상황을 피해야 합니다.

이를 방지하기 위해 `migrate` 명령어 실행 시 `--isolated` 옵션을 사용할 수 있습니다.

```shell
php artisan migrate --isolated
```

이 옵션을 사용하면 Laravel은 마이그레이션 실행 전에 애플리케이션의 캐시 드라이버를 사용하여 atomic lock을 획득합니다. 이 lock이 유지되는 동안 다른 서버에서 실행된 `migrate` 명령어는 실제 마이그레이션을 실행하지 않고 종료됩니다. 단, 종료 상태 코드는 성공으로 반환됩니다.

> [!WARNING]
> 이 기능을 사용하려면 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버를 사용해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 강제로 마이그레이션 실행

일부 마이그레이션 작업은 데이터 손실을 초래할 수 있습니다. 따라서 실수로 프로덕션 데이터베이스에서 실행되는 것을 방지하기 위해 실행 전에 확인 메시지가 표시됩니다.

확인 메시지 없이 강제로 실행하려면 `--force` 옵션을 사용합니다.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

가장 최근에 실행된 마이그레이션을 롤백하려면 `rollback` Artisan 명령어를 사용합니다. 이 명령어는 마지막 "batch"에 포함된 마이그레이션을 모두 롤백합니다.

```shell
php artisan migrate:rollback
```

특정 개수만 롤백하려면 `step` 옵션을 사용할 수 있습니다.

```shell
php artisan migrate:rollback --step=5
```

특정 batch 번호를 지정하여 롤백할 수도 있습니다.

```shell
php artisan migrate:rollback --batch=3
```

실제로 롤백하지 않고 실행될 SQL 문만 확인하려면 `--pretend` 옵션을 사용합니다.

```shell
php artisan migrate:rollback --pretend
```

모든 마이그레이션을 롤백하려면 다음 명령어를 사용합니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 하나의 명령어로 롤백 후 재실행

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 후 다시 `migrate` 명령어를 실행합니다. 즉, 데이터베이스 전체를 다시 생성하는 효과가 있습니다.

```shell
php artisan migrate:refresh

# 데이터베이스를 새로 생성하고 모든 seed 실행
php artisan migrate:refresh --seed
```

일부 마이그레이션만 대상으로 실행할 수도 있습니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션 실행

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 후 `migrate` 명령어를 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh`는 기본 데이터베이스 연결의 테이블만 삭제합니다. 다른 데이터베이스 연결을 지정하려면 `--database` 옵션을 사용합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 테이블 prefix와 상관없이 모든 테이블을 삭제합니다. 다른 애플리케이션과 공유되는 데이터베이스에서는 매우 주의해서 사용해야 합니다.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성

새로운 데이터베이스 테이블을 생성하려면 `Schema` facade의 `create` 메서드를 사용합니다.  

`create` 메서드는 두 개의 인수를 받습니다.

1. 테이블 이름  
2. `Blueprint` 객체를 받는 클로저 — 테이블 구조 정의

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

테이블 생성 시 schema builder의 [컬럼 메서드](#creating-columns)를 사용하여 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용하여 존재 여부를 확인할 수 있습니다.

```php
if (Schema::hasTable('users')) {
    // "users" 테이블이 존재합니다...
}

if (Schema::hasColumn('users', 'email')) {
    // "users" 테이블에 "email" 컬럼이 존재합니다...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // "email" 컬럼에 unique 인덱스가 존재합니다...
}
```

<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

기본 데이터베이스 연결이 아닌 다른 연결에서 schema 작업을 수행하려면 `connection` 메서드를 사용합니다.

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

MariaDB 또는 MySQL을 사용하는 경우 `engine` 속성을 사용하여 테이블 스토리지 엔진을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

또한 `charset`과 `collation` 속성을 사용하여 문자 집합과 정렬 규칙을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

`temporary` 메서드를 사용하면 임시 테이블을 생성할 수 있습니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

임시 테이블은 현재 데이터베이스 세션에서만 보이며, 연결이 종료되면 자동으로 삭제됩니다.

테이블에 주석(comment)을 추가하려면 `comment` 메서드를 사용할 수 있습니다. 이 기능은 MariaDB, MySQL, PostgreSQL에서 지원됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```