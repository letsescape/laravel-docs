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

마이그레이션(Migration)은 데이터베이스를 위한 버전 관리 시스템과 유사한 기능을 제공합니다. 이를 통해 팀이 애플리케이션의 데이터베이스 스키마 정의를 공유하고 관리할 수 있습니다.  

예를 들어, 소스 코드를 pull 받은 후 팀원에게 "로컬 데이터베이스에 컬럼을 하나 수동으로 추가해 주세요"라고 요청한 경험이 있다면, 바로 이런 문제를 해결하기 위해 데이터베이스 마이그레이션이 존재합니다.

Laravel의 `Schema` [facade](/docs/master/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블을 생성하거나 수정할 수 있도록 데이터베이스에 종속되지 않는 기능을 제공합니다. 일반적으로 마이그레이션에서는 이 facade를 사용하여 데이터베이스 테이블과 컬럼을 생성하거나 수정합니다.

<a name="generating-migrations"></a>
## 마이그레이션 생성 (Generating Migrations)

`make:migration` [Artisan 명령어](/docs/master/artisan)를 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새로 생성된 마이그레이션 파일은 `database/migrations` 디렉토리에 저장됩니다.  

각 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있으며, Laravel은 이를 통해 마이그레이션 실행 순서를 결정합니다.

```shell
php artisan make:migration create_flights_table
```

Laravel은 마이그레이션 이름을 기반으로 테이블 이름과 새 테이블 생성 여부를 자동으로 추측합니다. 만약 테이블 이름을 추론할 수 있다면, 생성된 마이그레이션 파일에 해당 테이블이 미리 설정됩니다. 그렇지 않은 경우에는 마이그레이션 파일에서 직접 테이블을 지정할 수 있습니다.

생성된 마이그레이션 파일의 저장 경로를 직접 지정하고 싶다면 `make:migration` 명령 실행 시 `--path` 옵션을 사용할 수 있습니다. 이 경로는 애플리케이션의 기본 경로(base path)를 기준으로 한 상대 경로여야 합니다.

> [!NOTE]
> Migration 스텁(stub)은 [stub publishing](/docs/master/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="squashing-migrations"></a>
### 마이그레이션 스쿼싱 (Squashing Migrations)

애플리케이션을 개발하다 보면 시간이 지남에 따라 마이그레이션 파일이 계속 누적됩니다. 이로 인해 `database/migrations` 디렉토리에 수백 개의 마이그레이션 파일이 쌓일 수 있습니다.

이 경우 여러 마이그레이션을 하나의 SQL 파일로 "스쿼시(squash)"할 수 있습니다. 먼저 `schema:dump` 명령어를 실행합니다.

```shell
php artisan schema:dump

# 현재 데이터베이스 스키마를 덤프하고 기존 마이그레이션을 모두 제거...
php artisan schema:dump --prune
```

이 명령을 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉토리에 "schema" 파일을 생성합니다. 파일 이름은 데이터베이스 연결(connection) 이름과 동일합니다.

이후 데이터베이스 마이그레이션을 실행할 때 아직 어떤 마이그레이션도 실행되지 않은 상태라면, Laravel은 먼저 해당 데이터베이스 연결에 맞는 schema 파일의 SQL을 실행합니다. 이후 schema dump에 포함되지 않은 나머지 마이그레이션을 실행합니다.

테스트 환경에서 사용하는 데이터베이스 연결이 로컬 개발 환경에서 사용하는 연결과 다르다면, 테스트용 데이터베이스 연결로도 schema dump 파일을 생성해야 합니다. 예를 들어 다음과 같이 실행할 수 있습니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

팀의 다른 개발자들이 애플리케이션의 초기 데이터베이스 구조를 빠르게 생성할 수 있도록 데이터베이스 schema 파일은 소스 코드 저장소에 커밋하는 것이 좋습니다.

> [!WARNING]
> Migration 스쿼싱 기능은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며, 데이터베이스의 커맨드라인 클라이언트를 사용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조 (Migration Structure)

마이그레이션 클래스에는 두 개의 메서드가 포함됩니다: `up`과 `down`.

- `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가할 때 사용합니다.
- `down` 메서드는 `up` 메서드에서 수행한 작업을 되돌리는 역할을 합니다.

이 두 메서드 안에서 Laravel의 스키마 빌더(schema builder)를 사용하여 테이블을 생성하거나 수정할 수 있습니다. `Schema` 빌더에서 제공하는 모든 메서드에 대해서는 [공식 문서](#creating-tables)를 참고하십시오.

예를 들어 다음 마이그레이션은 `flights` 테이블을 생성합니다.

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

마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 연결을 사용해야 한다면, 마이그레이션 클래스에 `$connection` 속성을 설정해야 합니다.

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

일부 마이그레이션은 아직 활성화되지 않은 기능을 지원하기 위해 미리 작성될 수 있습니다. 이런 경우 아직 실행되지 않도록 하고 싶을 수 있습니다.

이때 마이그레이션에 `shouldRun` 메서드를 정의할 수 있습니다. `shouldRun` 메서드가 `false`를 반환하면 해당 마이그레이션은 실행되지 않습니다.

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

이미 실행된 마이그레이션과 아직 실행되지 않은 마이그레이션을 확인하려면 `migrate:status` 명령어를 사용할 수 있습니다.

```shell
php artisan migrate:status
```

`migrate` 명령어에 `--step` 옵션을 사용하면 각 마이그레이션이 개별 배치(batch)로 실행됩니다. 이렇게 하면 이후 `migrate:rollback` 명령어로 개별 마이그레이션을 롤백할 수 있습니다.

```shell
php artisan migrate --step
```

실제로 실행하지 않고 마이그레이션이 실행할 SQL 문을 확인하고 싶다면 `--pretend` 옵션을 사용할 수 있습니다.

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
#### 마이그레이션 실행 격리

애플리케이션을 여러 서버에 배포하면서 배포 과정에서 마이그레이션을 실행한다면, 두 서버가 동시에 마이그레이션을 실행하는 상황을 피하고 싶을 수 있습니다.

이 경우 `migrate` 명령어 실행 시 `--isolated` 옵션을 사용할 수 있습니다.

```shell
php artisan migrate --isolated
```

이 옵션을 사용하면 Laravel은 마이그레이션 실행 전에 애플리케이션의 캐시 드라이버를 이용해 원자적 잠금(atomic lock)을 획득합니다. 잠금이 유지되는 동안 다른 서버에서 실행된 `migrate` 명령어는 실제로 마이그레이션을 실행하지 않지만, 명령어는 성공 상태 코드로 종료됩니다.

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 합니다. 또한 모든 서버는 동일한 중앙 캐시 서버를 사용해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 프로덕션 환경에서 강제로 마이그레이션 실행

일부 마이그레이션 작업은 파괴적(destructive)일 수 있으며, 데이터 손실을 발생시킬 수 있습니다. 이러한 이유로 프로덕션 데이터베이스에서 명령을 실행하기 전에 확인 메시지가 표시됩니다.

확인 메시지 없이 강제로 실행하려면 `--force` 옵션을 사용합니다.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
### 마이그레이션 롤백 (Rolling Back Migrations)

최근에 실행된 마이그레이션 작업을 롤백하려면 `rollback` Artisan 명령어를 사용합니다. 이 명령어는 마지막 배치(batch)의 마이그레이션을 롤백합니다.

```shell
php artisan migrate:rollback
```

`step` 옵션을 사용하면 롤백할 마이그레이션 개수를 제한할 수 있습니다.

```shell
php artisan migrate:rollback --step=5
```

특정 배치(batch)의 마이그레이션을 롤백하려면 `batch` 옵션을 사용할 수 있습니다. `batch` 값은 애플리케이션의 `migrations` 데이터베이스 테이블에 저장된 배치 번호와 동일해야 합니다.

```shell
php artisan migrate:rollback --batch=3
```

실제로 실행하지 않고 롤백 시 실행될 SQL 문을 확인하려면 `--pretend` 옵션을 사용할 수 있습니다.

```shell
php artisan migrate:rollback --pretend
```

`migrate:reset` 명령어는 애플리케이션의 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
#### 단일 명령어로 롤백 후 재마이그레이션

`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 후 다시 `migrate` 명령어를 실행합니다. 즉, 전체 데이터베이스를 새로 생성하는 것과 같습니다.

```shell
php artisan migrate:refresh

# 데이터베이스를 새로 생성하고 모든 시드 실행...
php artisan migrate:refresh --seed
```

`step` 옵션을 사용하면 특정 개수의 마이그레이션만 롤백 후 다시 실행할 수 있습니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 후 마이그레이션

`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 후 `migrate` 명령어를 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

기본적으로 `migrate:fresh`는 기본 데이터베이스 연결에 있는 테이블만 삭제합니다. `--database` 옵션을 사용하면 특정 데이터베이스 연결을 지정할 수 있습니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 테이블 prefix 여부와 관계없이 모든 테이블을 삭제합니다. 다른 애플리케이션과 공유하는 데이터베이스에서 사용할 때는 특히 주의해야 합니다.

<a name="tables"></a>
## 테이블 (Tables)

<a name="creating-tables"></a>
### 테이블 생성 (Creating Tables)

새 데이터베이스 테이블을 생성하려면 `Schema` facade의 `create` 메서드를 사용합니다.

`create` 메서드는 두 개의 인수를 받습니다.

1. 테이블 이름  
2. 테이블 구조를 정의하기 위한 `Blueprint` 객체를 전달받는 클로저

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

테이블을 생성할 때는 스키마 빌더의 [컬럼 메서드](#creating-columns)를 사용하여 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용하여 테이블, 컬럼, 인덱스의 존재 여부를 확인할 수 있습니다.

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
#### 데이터베이스 연결 및 테이블 옵션

기본 데이터베이스 연결이 아닌 다른 연결에서 스키마 작업을 수행하려면 `connection` 메서드를 사용합니다.

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

또한 테이블 생성 시 몇 가지 추가 속성과 메서드를 사용할 수 있습니다.

MariaDB 또는 MySQL을 사용할 경우 `engine` 속성을 통해 테이블의 스토리지 엔진을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

`charset`과 `collation` 속성은 테이블의 문자 집합과 정렬 방식을 지정할 때 사용합니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

`temporary` 메서드를 사용하면 임시 테이블을 생성할 수 있습니다. 임시 테이블은 현재 연결된 데이터베이스 세션에서만 보이며 연결이 종료되면 자동으로 삭제됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

테이블에 설명(comment)을 추가하려면 `comment` 메서드를 사용할 수 있습니다. 현재 테이블 주석은 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
### 테이블 수정 (Updating Tables)

기존 테이블을 수정하려면 `Schema` facade의 `table` 메서드를 사용합니다.

이 메서드는 두 개의 인수를 받습니다.

1. 테이블 이름  
2. `Blueprint` 인스턴스를 전달받는 클로저

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제 (Renaming / Dropping Tables)

기존 테이블의 이름을 변경하려면 `rename` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다.

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에 해당 테이블의 외래 키 제약 조건이 마이그레이션 파일에서 명시적인 이름을 가지고 있는지 확인해야 합니다.  

Laravel이 자동으로 생성한 규칙 기반 이름을 사용할 경우, 외래 키 이름이 기존 테이블 이름을 참조하게 될 수 있습니다.

<a name="columns"></a>
## 컬럼 (Columns)

<a name="creating-columns"></a>
### 컬럼 생성 (Creating Columns)

기존 테이블에 컬럼을 추가하려면 `Schema` facade의 `table` 메서드를 사용합니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### 사용 가능한 컬럼 타입 (Available Column Types)

스키마 빌더의 `Blueprint` 클래스는 데이터베이스 테이블에 다양한 컬럼 타입을 추가할 수 있는 메서드를 제공합니다.

아래에는 사용 가능한 주요 컬럼 타입이 나열되어 있습니다.

#### Boolean 타입

- `boolean`

#### 문자열 및 텍스트 타입

- `char`
- `longText`
- `mediumText`
- `string`
- `text`
- `tinyText`

#### 숫자 타입

- `bigIncrements`
- `bigInteger`
- `decimal`
- `double`
- `float`
- `id`
- `increments`
- `integer`
- `mediumIncrements`
- `mediumInteger`
- `smallIncrements`
- `smallInteger`
- `tinyIncrements`
- `tinyInteger`
- `unsignedBigInteger`
- `unsignedInteger`
- `unsignedMediumInteger`
- `unsignedSmallInteger`
- `unsignedTinyInteger`

#### 날짜 및 시간 타입

- `dateTime`
- `dateTimeTz`
- `date`
- `time`
- `timeTz`
- `timestamp`
- `timestamps`
- `timestampsTz`
- `softDeletes`
- `softDeletesTz`
- `year`

#### Binary 타입

- `binary`

#### Object 및 JSON 타입

- `json`
- `jsonb`

#### UUID 및 ULID 타입

- `ulid`
- `ulidMorphs`
- `uuid`
- `uuidMorphs`
- `nullableUlidMorphs`
- `nullableUuidMorphs`

#### Spatial 타입

- `geography`
- `geometry`

#### 연관관계(Relationship) 타입

- `foreignId`
- `foreignIdFor`
- `foreignUlid`
- `foreignUuid`
- `morphs`
- `nullableMorphs`

#### 특수 타입

- `enum`
- `set`
- `macAddress`
- `ipAddress`
- `rememberToken`
- `vector`

(이후 각 컬럼 메서드 설명과 예제 코드들은 원문과 동일하게 유지됩니다.)