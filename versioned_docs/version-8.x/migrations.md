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
마이그레이션은 데이터베이스 버전 관리를 가능하게 해주는 도구로, 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 직접 작성하고 공유할 수 있게 해줍니다. 만약 소스 코드를 동기화한 후 동료에게 직접 컬럼을 추가하라고 수동 지시한 적이 있다면, 바로 그 문제가 데이터베이스 마이그레이션으로 해결되는 문제입니다.

<!-- The Laravel `Schema` [facade](/docs/8.x/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns. -->
Laravel의 `Schema` [facade](/docs/8.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블을 생성하고 다룰 수 있도록 특정 데이터베이스에 종속되지 않는(agnostic) 접근을 제공합니다. 일반적으로 마이그레이션은 이 파사드를 이용하여 데이터베이스의 테이블과 컬럼을 만들거나 수정합니다.

<a name="generating-migrations"></a>
<a id="writing-migrations" data-translation-alias="true"></a>
<!-- ## Generating Migrations -->
## Generating Migrations

<!-- You may use the `make:migration` [Artisan command](/docs/8.x/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations: -->
`make:migration` [Artisan command](/docs/8.x/artisan)를 사용해 데이터베이스 마이그레이션 파일을 생성할 수 있습니다. 새로 생성된 마이그레이션 파일은 `database/migrations` 디렉터리에 저장됩니다. 각각의 마이그레이션 파일명에는 타임스탬프가 포함되어 있어, Laravel이 마이그레이션 실행 순서를 정확히 파악할 수 있습니다.

```
php artisan make:migration create_flights_table
```

<!-- Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually. -->
Laravel은 마이그레이션의 이름을 분석하여 테이블명과 새 테이블 생성 여부를 추측하려 시도합니다. 만약 Laravel이 이름에서 테이블명을 알아낼 수 있다면, 생성된 마이그레이션 파일에 해당 테이블명을 미리 입력해 둡니다. 반면, 테이블명을 자동으로 인식하지 못할 때는 마이그레이션 파일에서 직접 테이블명을 지정하면 됩니다.

<!-- If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path. -->
생성된 마이그레이션의 경로를 원하는 곳으로 지정하고 싶다면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 이 경로는 애플리케이션의 루트 디렉터리로부터 상대적으로 지정해야 합니다.

> [!TIP]
> 마이그레이션의 스텁(stub, 템플릿). 파일은 [stub publishing](/docs/8.x/artisan#stub-customization)을 이용해 사용자 정의할 수 있습니다.

<a name="squashing-migrations"></a>
<!-- ### Squashing Migrations -->
### Squashing Migrations

<!-- As you build your application, you may accumulate more and more migrations over time. This can lead to your `database/migrations` directory becoming bloated with potentially hundreds of migrations. If you would like, you may "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command: -->
애플리케이션을 개발해가다 보면 점점 더 많은 마이그레이션 파일이 쌓이게 됩니다. 이로 인해 `database/migrations` 디렉터리가 수백 개의 마이그레이션 파일로 넘쳐날 수 있습니다. 이럴 때, 원한다면 여러 마이그레이션을 하나의 SQL 파일로 "스쿼싱(squash, 압축)"할 수 있습니다. 먼저, `schema:dump` 명령어를 실행해보세요.

```
php artisan schema:dump

// Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

<!-- When you execute this command, Laravel will write a "schema" file to your application's `database/schema` directory. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will execute the schema file's SQL statements first. After executing the schema file's statements, Laravel will execute any remaining migrations that were not part of the schema dump. -->
이 명령어를 실행하면, Laravel이 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 생성합니다. 이후 데이터베이스에 아직 어떤 마이그레이션도 실행된 이력이 없다면, Laravel이 이 스키마 파일의 SQL 문을 먼저 실행합니다. 그리고 스키마 파일에 포함되지 않은 남은 마이그레이션들만 별도로 실행하게 됩니다.

<!-- You should commit your database schema file to source control so that other new developers on your team may quickly create your application's initial database structure. -->
이 스키마 파일을 소스 코드 관리에 꼭 커밋해두세요. 그러면 새로 합류한 다른 팀원도 애플리케이션의 초기 데이터베이스 구조를 빠르게 만들 수 있습니다.

> [!NOTE]
> 마이그레이션 스쿼싱 기능은 MySQL, PostgreSQL, SQLite 데이터베이스에서만 제공되며, 데이터베이스의 커맨드라인 클라이언트를 활용합니다. 스키마 덤프는 메모리 기반 SQLite 데이터베이스에서는 복구가 지원되지 않습니다.

<a name="migration-structure"></a>
<!-- ## Migration Structure -->
## Migration Structure

<!-- A migration class contains two methods: `up` and `down`. The `up` method is used to add new tables, columns, or indexes to your database, while the `down` method should reverse the operations performed by the `up` method. -->
마이그레이션 클래스는 두 가지 메서드를 가집니다: `up`과 `down`. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스 등을 추가할 때 사용합니다. 그리고 `down` 메서드는 `up` 메서드에서 한 작업을 되돌릴 수 있게 정의해야 합니다.

<!-- Within both of these methods, you may use the Laravel schema builder to expressively create and modify tables. To learn about all of the methods available on the `Schema` builder, [check out its documentation](#creating-tables). For example, the following migration creates a `flights` table: -->
이 두 메서드 모두 Laravel의 스키마 빌더를 사용하여 테이블을 명확하고 직관적으로 생성 및 수정할 수 있습니다. `Schema` 빌더에서 제공하는 모든 메소드에 대해 알고 싶으시다면, [check out its documentation](#creating-tables)를 참고하세요. 아래 예시는 `flights` 테이블을 생성하는 마이그레이션의 예입니다.

```
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateFlightsTable extends Migration
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
}
```

<a name="anonymous-migrations"></a>
<!-- #### Anonymous Migrations -->
#### Anonymous Migrations

<!-- As you may have noticed in the example above, Laravel will automatically assign a class name to all of the migrations that you generate using the `make:migration` command. However, if you wish, you may return an anonymous class from your migration file. This is primarily useful if your application accumulates many migrations and two of them have a class name collision: -->
위의 예시에서 보았듯이, `make:migration` 명령어로 생성한 마이그레이션에는 Laravel이 클래스명을 자동으로 지정합니다. 하지만 필요에 따라 마이그레이션 파일에서 익명 클래스(anonymous class)를 반환하도록 선택할 수도 있습니다. 마이그레이션 파일이 매우 많아 클래스 이름이 겹칠 우려가 있을 때 특히 유용합니다.

```
<?php

use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    //
};
```

<a name="setting-the-migration-connection"></a>
<!-- #### Setting The Migration Connection -->
#### Setting The Migration Connection

<!-- If your migration will be interacting with a database connection other than your application's default database connection, you should set the `$connection` property of your migration: -->
마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 연결에서 실행되어야 할 경우, 마이그레이션 클래스의 `$connection` 프로퍼티를 설정해야 합니다.

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
모든 미실행 마이그레이션을 한 번에 실행하려면 `migrate` Artisan 명령어를 사용하세요.

```
php artisan migrate
```

<!-- If you would like to see which migrations have run thus far, you may use the `migrate:status` Artisan command: -->
지금까지 어떤 마이그레이션이 실행되었는지 확인하려면, `migrate:status` Artisan 명령어를 사용할 수 있습니다.

```
php artisan migrate:status
```

<a name="forcing-migrations-to-run-in-production"></a>
<!-- #### Forcing Migrations To Run In Production -->
#### Forcing Migrations To Run In Production

<!-- Some migration operations are destructive, which means they may cause you to lose data. In order to protect you from running these commands against your production database, you will be prompted for confirmation before the commands are executed. To force the commands to run without a prompt, use the `--force` flag: -->
일부 마이그레이션 작업은 파괴적이어서, 데이터 손실이 발생할 수도 있습니다. 이런 명령어를 프로덕션 데이터베이스에 실행하는 것을 방지하기 위해, 명령 실행 전 확인 메시지가 표시됩니다. 이 과정을 생략하고 강제로 실행하려면 `--force` 플래그를 사용하세요.

```
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
<!-- ### Rolling Back Migrations -->
### Rolling Back Migrations

<!-- To roll back the latest migration operation, you may use the `rollback` Artisan command. This command rolls back the last "batch" of migrations, which may include multiple migration files: -->
가장 최근에 실행된 마이그레이션을 롤백하려면 `rollback` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 "배치(batch)" 단위로 여러 개의 마이그레이션 파일을 한 번에 되돌립니다.

```
php artisan migrate:rollback
```

<!-- You may roll back a limited number of migrations by providing the `step` option to the `rollback` command. For example, the following command will roll back the last five migrations: -->
되돌리는 마이그레이션 개수를 제한하고 싶다면, `rollback` 명령어에 `step` 옵션을 추가하세요. 예를 들어, 아래 명령어는 최근 5개의 마이그레이션만 롤백합니다.

```
php artisan migrate:rollback --step=5
```

<!-- The `migrate:reset` command will roll back all of your application's migrations: -->
`migrate:reset` 명령어를 사용하면 애플리케이션의 모든 마이그레이션이 롤백됩니다.

```
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
<!-- #### Roll Back & Migrate Using A Single Command -->
#### Roll Back & Migrate Using A Single Command

<!-- The `migrate:refresh` command will roll back all of your migrations and then execute the `migrate` command. This command effectively re-creates your entire database: -->
`migrate:refresh` 명령어를 사용하면, 모든 마이그레이션을 롤백한 뒤 `migrate` 명령을 실행합니다. 이 명령어는 전체 데이터베이스를 효과적으로 재생성합니다.

```
php artisan migrate:refresh

// Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

<!-- You may roll back and re-migrate a limited number of migrations by providing the `step` option to the `refresh` command. For example, the following command will roll back and re-migrate the last five migrations: -->
`refresh` 명령어에도 `step` 옵션을 사용해, 최근 N개의 마이그레이션만 롤백 및 재실행할 수 있습니다. 예를 들어, 최근 5개의 마이그레이션만 대상으로 하고 싶다면 아래와 같이 사용하세요.

```
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
<!-- #### Drop All Tables & Migrate -->
#### Drop All Tables & Migrate

<!-- The `migrate:fresh` command will drop all tables from the database and then execute the `migrate` command: -->
`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제하고, 그 후에 다시 `migrate` 명령어를 실행합니다.

```
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

> [!NOTE]
> `migrate:fresh` 명령어는 프리픽스를 가진 테이블을 포함해 모든 데이터베이스 테이블을 삭제합니다. 다른 애플리케이션과 데이터베이스를 공유할 경우, 이 명령어는 신중하게 사용해야 합니다.

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<a name="creating-tables"></a>
<!-- ### Creating Tables -->
### Creating Tables

<!-- To create a new database table, use the `create` method on the `Schema` facade. The `create` method accepts two arguments: the first is the name of the table, while the second is a closure which receives a `Blueprint` object that may be used to define the new table: -->
새로운 데이터베이스 테이블을 생성하려면, `Schema` 파사드에서 `create` 메서드를 사용하세요. `create` 메서드는 두 개의 인수를 받는데, 첫 번째는 테이블 이름이고, 두 번째는 `Blueprint` 객체를 받아 테이블 구조를 정의하는 클로저입니다.

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
테이블을 생성할 때, 다양한 [column methods](#creating-columns)를 사용하여 컬럼을 정의할 수 있습니다.

<a name="checking-for-table-column-existence"></a>
<!-- #### Checking For Table / Column Existence -->
#### Checking For Table / Column Existence

<!-- You may check for the existence of a table or column using the `hasTable` and `hasColumn` methods: -->
`hasTable` 및 `hasColumn` 메서드를 이용해 테이블 또는 컬럼이 존재하는지 확인할 수 있습니다.

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
기본 데이터베이스 연결이 아닌 다른 연결에서 스키마 작업을 하려면, `connection` 메서드를 사용하세요.

```
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

<!-- In addition, a few other properties and methods may be used to define other aspects of the table's creation. The `engine` property may be used to specify the table's storage engine when using MySQL: -->
또한, 테이블 생성시 몇 가지 프로퍼티와 메서드로 추가적인 테이블 속성도 설정할 수 있습니다. MySQL에서 사용할 테이블의 스토리지 엔진을 지정하려면 `engine` 속성을 활용하세요.

```
Schema::create('users', function (Blueprint $table) {
    $table->engine = 'InnoDB';

    // ...
});
```

<!-- The `charset` and `collation` properties may be used to specify the character set and collation for the created table when using MySQL: -->
MySQL에서 생성할 테이블의 문자셋과 콜레이션을 지정하려면 `charset`, `collation` 속성을 사용할 수 있습니다.

```
Schema::create('users', function (Blueprint $table) {
    $table->charset = 'utf8mb4';
    $table->collation = 'utf8mb4_unicode_ci';

    // ...
});
```

<!-- The `temporary` method may be used to indicate that the table should be "temporary". Temporary tables are only visible to the current connection's database session and are dropped automatically when the connection is closed: -->
`temporary` 메서드를 이용하면 테이블을 "임시 테이블"로 만들 수 있습니다. 임시 테이블은 현재 연결된 데이터베이스 세션에서만 보이며, 연결이 종료되면 자동으로 삭제됩니다.

```
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

<a name="updating-tables"></a>
<!-- ### Updating Tables -->
### Updating Tables

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives a `Blueprint` instance you may use to add columns or indexes to the table: -->
기존 테이블을 수정하려면, `Schema` 파사드의 `table` 메서드를 사용할 수 있습니다. `create`와 마찬가지로, `table` 메서드는 테이블명과 `Blueprint` 인스턴스를 받는 클로저를 인수로 전달합니다. 이를 통해 컬럼이나 인덱스를 추가할 수 있습니다.

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
기존 데이터베이스 테이블의 이름을 변경하려면, `rename` 메서드를 사용하세요.

```
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

<!-- To drop an existing table, you may use the `drop` or `dropIfExists` methods: -->
기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다.

```
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
<!-- #### Renaming Tables With Foreign Keys -->
#### Renaming Tables With Foreign Keys

<!-- Before renaming a table, you should verify that any foreign key constraints on the table have an explicit name in your migration files instead of letting Laravel assign a convention based name. Otherwise, the foreign key constraint name will refer to the old table name. -->
테이블의 이름을 변경하기 전에, 마이그레이션 파일에서 해당 테이블에 부여된 외래 키 제약 조건이 반드시 명시적으로 지정되어 있는지 확인해야 합니다. 이름을 자동 생성(convention)으로 사용하면, 외래 키 제약 조건 이름이 이전 테이블명을 참조하게 될 수 있습니다.

<a name="columns"></a>
<!-- ## Columns -->
## Columns

<a name="creating-columns"></a>
<!-- ### Creating Columns -->
### Creating Columns

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives an `Illuminate\Database\Schema\Blueprint` instance you may use to add columns to the table: -->
기존 테이블을 수정하려면, `Schema` 파사드의 `table` 메서드를 사용할 수 있습니다. `create` 메서드와 마찬가지로, `table` 메서드는 두 개의 인수를 받는데, 첫 번째는 테이블명이고, 두 번째는 컬럼을 추가할 수 있는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저입니다.

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
스키마 빌더의 Blueprint는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 대응하는 메서드를 제공합니다. 아래의 표에 각 컬럼 타입에 대해 사용할 수 있는 메서드를 정리해놓았습니다.



<!-- <div id="collection-method-list" markdown="1"> -->
<div id="collection-method-list" markdown="1">

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
[uuidMorphs](#column-method-uuidMorphs)
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
[uuidMorphs](#column-method-uuidMorphs)
[uuid](#column-method-uuid)
[year](#column-method-year)

<!-- </div> -->
</div>

<a name="column-method-bigIncrements"></a>
<!-- #### `bigIncrements()` -->
#### `bigIncrements()`

<!-- The `bigIncrements` method creates an auto-incrementing `UNSIGNED BIGINT` (primary key) equivalent column: -->
`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT` (기본키) 타입의 컬럼을 생성합니다.

```
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
<!-- #### `bigInteger()` -->
#### `bigInteger()`

<!-- The `bigInteger` method creates a `BIGINT` equivalent column: -->
`bigInteger` 메서드는 `BIGINT` 타입의 컬럼을 생성합니다.

```
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
<!-- #### `binary()` -->
#### `binary()`

<!-- The `binary` method creates a `BLOB` equivalent column: -->
`binary` 메서드는 `BLOB` 타입의 컬럼을 생성합니다.

```
$table->binary('photo');
```

<a name="column-method-boolean"></a>
<!-- #### `boolean()` -->
#### `boolean()`

<!-- The `boolean` method creates a `BOOLEAN` equivalent column: -->
`boolean` 메서드는 `BOOLEAN` 타입의 컬럼을 생성합니다.

```
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
<!-- #### `char()` -->
#### `char()`

<!-- The `char` method creates a `CHAR` equivalent column with of a given length: -->
`char` 메서드는 지정한 길이의 `CHAR` 타입 컬럼을 생성합니다.

```
$table->char('name', 100);
```

<a name="column-method-dateTimeTz"></a>
<!-- #### `dateTimeTz()` -->
#### `dateTimeTz()`

<!-- The `dateTimeTz` method creates a `DATETIME` (with timezone) equivalent column with an optional precision (total digits): -->
`dateTimeTz` 메서드는 (옵션으로 정밀도 지정 가능) 시간대를 포함한 `DATETIME` 타입의 컬럼을 생성합니다.

```
$table->dateTimeTz('created_at', $precision = 0);
```

<a name="column-method-dateTime"></a>
<!-- #### `dateTime()` -->
#### `dateTime()`

<!-- The `dateTime` method creates a `DATETIME` equivalent column with an optional precision (total digits): -->
`dateTime` 메서드는 (옵션으로 정밀도 지정 가능) `DATETIME` 타입의 컬럼을 생성합니다.

```
$table->dateTime('created_at', $precision = 0);
```

<a name="column-method-date"></a>
<!-- #### `date()` -->
#### `date()`

<!-- The `date` method creates a `DATE` equivalent column: -->
`date` 메서드는 `DATE` 타입의 컬럼을 생성합니다.

```
$table->date('created_at');
```

<a name="column-method-decimal"></a>
<!-- #### `decimal()` -->
#### `decimal()`

<!-- The `decimal` method creates a `DECIMAL` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`decimal` 메서드는 지정한 정밀도(전체 자릿수) 및 소수 자릿수(스케일)를 기준으로 한 `DECIMAL` 타입 컬럼을 생성합니다.

```
$table->decimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-double"></a>
<!-- #### `double()` -->
#### `double()`

<!-- The `double` method creates a `DOUBLE` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`double` 메서드는 지정한 정밀도(전체 자릿수) 및 소수 자릿수(스케일)를 기준으로 한 `DOUBLE` 타입 컬럼을 생성합니다.

```
$table->double('amount', 8, 2);
```

<a name="column-method-enum"></a>
<!-- #### `enum()` -->
#### `enum()`

<!-- The `enum` method creates a `ENUM` equivalent column with the given valid values: -->
`enum` 메서드는 지정한 값 목록을 갖는 `ENUM` 타입 컬럼을 생성합니다.

```
$table->enum('difficulty', ['easy', 'hard']);
```

<a name="column-method-float"></a>
<!-- #### `float()` -->
#### `float()`

<!-- The `float` method creates a `FLOAT` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`float` 메서드는 지정한 정밀도(전체 자릿수) 및 소수 자릿수(스케일)를 기준으로 한 `FLOAT` 타입 컬럼을 생성합니다.

```
$table->float('amount', 8, 2);
```

<a name="column-method-foreignId"></a>
<!-- #### `foreignId()` -->
#### `foreignId()`

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column: -->
`foreignId` 메서드는 `UNSIGNED BIGINT` 타입의 컬럼을 생성합니다.

```
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
<!-- #### `foreignIdFor()` -->
#### `foreignIdFor()`

<!-- The `foreignIdFor` method adds a `{column}_id UNSIGNED BIGINT` equivalent column for a given model class: -->
`foreignIdFor` 메서드는 지정된 모델 클래스에 대한 `{column}_id UNSIGNED BIGINT` 타입의 컬럼을 추가합니다.

```
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUuid"></a>

<!-- #### `foreignUuid()` -->
#### `foreignUuid()`

<!-- The `foreignUuid` method creates a `UUID` equivalent column: -->
`foreignUuid` 메서드는 `UUID`와 동등한 컬럼을 생성합니다.

```
$table->foreignUuid('user_id');
```

<a name="column-method-geometryCollection"></a>
<!-- #### `geometryCollection()` -->
#### `geometryCollection()`

<!-- The `geometryCollection` method creates a `GEOMETRYCOLLECTION` equivalent column: -->
`geometryCollection` 메서드는 `GEOMETRYCOLLECTION`과 동등한 컬럼을 생성합니다.

```
$table->geometryCollection('positions');
```

<a name="column-method-geometry"></a>
<!-- #### `geometry()` -->
#### `geometry()`

<!-- The `geometry` method creates a `GEOMETRY` equivalent column: -->
`geometry` 메서드는 `GEOMETRY`와 동등한 컬럼을 생성합니다.

```
$table->geometry('positions');
```

<a name="column-method-id"></a>
<!-- #### `id()` -->
#### `id()`

<!-- The `id` method is an alias of the `bigIncrements` method. By default, the method will create an `id` column; however, you may pass a column name if you would like to assign a different name to the column: -->
`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로는 `id` 컬럼을 생성하지만, 다른 이름을 부여하고 싶다면 컬럼명을 인수로 전달할 수 있습니다.

```
$table->id();
```

<a name="column-method-increments"></a>
<!-- #### `increments()` -->
#### `increments()`

<!-- The `increments` method creates an auto-incrementing `UNSIGNED INTEGER` equivalent column as a primary key: -->
`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER`와 동등한 컬럼을 기본 키로 생성합니다.

```
$table->increments('id');
```

<a name="column-method-integer"></a>
<!-- #### `integer()` -->
#### `integer()`

<!-- The `integer` method creates an `INTEGER` equivalent column: -->
`integer` 메서드는 `INTEGER`와 동등한 컬럼을 생성합니다.

```
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
<!-- #### `ipAddress()` -->
#### `ipAddress()`

<!-- The `ipAddress` method creates a `VARCHAR` equivalent column: -->
`ipAddress` 메서드는 `VARCHAR`와 동등한 컬럼을 생성합니다.

```
$table->ipAddress('visitor');
```

<a name="column-method-json"></a>
<!-- #### `json()` -->
#### `json()`

<!-- The `json` method creates a `JSON` equivalent column: -->
`json` 메서드는 `JSON`과 동등한 컬럼을 생성합니다.

```
$table->json('options');
```

<a name="column-method-jsonb"></a>
<!-- #### `jsonb()` -->
#### `jsonb()`

<!-- The `jsonb` method creates a `JSONB` equivalent column: -->
`jsonb` 메서드는 `JSONB`와 동등한 컬럼을 생성합니다.

```
$table->jsonb('options');
```

<a name="column-method-lineString"></a>
<!-- #### `lineString()` -->
#### `lineString()`

<!-- The `lineString` method creates a `LINESTRING` equivalent column: -->
`lineString` 메서드는 `LINESTRING`과 동등한 컬럼을 생성합니다.

```
$table->lineString('positions');
```

<a name="column-method-longText"></a>
<!-- #### `longText()` -->
#### `longText()`

<!-- The `longText` method creates a `LONGTEXT` equivalent column: -->
`longText` 메서드는 `LONGTEXT`와 동등한 컬럼을 생성합니다.

```
$table->longText('description');
```

<a name="column-method-macAddress"></a>
<!-- #### `macAddress()` -->
#### `macAddress()`

<!-- The `macAddress` method creates a column that is intended to hold a MAC address. Some database systems, such as PostgreSQL, have a dedicated column type for this type of data. Other database systems will use a string equivalent column: -->
`macAddress` 메서드는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. PostgreSQL과 같은 일부 데이터베이스는 이 용도의 전용 컬럼 타입을 제공하며, 그 외의 데이터베이스 시스템은 문자열 타입 컬럼을 사용하게 됩니다.

```
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
<!-- #### `mediumIncrements()` -->
#### `mediumIncrements()`

<!-- The `mediumIncrements` method creates an auto-incrementing `UNSIGNED MEDIUMINT` equivalent column as a primary key: -->
`mediumIncrements` 메서드는 자동 증가하는 `UNSIGNED MEDIUMINT`와 동등한 컬럼을 기본 키로 생성합니다.

```
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
<!-- #### `mediumInteger()` -->
#### `mediumInteger()`

<!-- The `mediumInteger` method creates a `MEDIUMINT` equivalent column: -->
`mediumInteger` 메서드는 `MEDIUMINT`와 동등한 컬럼을 생성합니다.

```
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
<!-- #### `mediumText()` -->
#### `mediumText()`

<!-- The `mediumText` method creates a `MEDIUMTEXT` equivalent column: -->
`mediumText` 메서드는 `MEDIUMTEXT`와 동등한 컬럼을 생성합니다.

```
$table->mediumText('description');
```

<a name="column-method-morphs"></a>
<!-- #### `morphs()` -->
#### `morphs()`

<!-- The `morphs` method is a convenience method that adds a `{column}_id` `UNSIGNED BIGINT` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`morphs` 메서드는 `{column}_id` `UNSIGNED BIGINT`와 동등한 컬럼, 그리고 `{column}_type` `VARCHAR`와 동등한 컬럼을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/8.x/eloquent-relationships). In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 메서드는 다형적 [Eloquent relationship](/docs/8.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용합니다. 아래 예제에서는 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다.

```
$table->morphs('taggable');
```

<a name="column-method-multiLineString"></a>
<!-- #### `multiLineString()` -->
#### `multiLineString()`

<!-- The `multiLineString` method creates a `MULTILINESTRING` equivalent column: -->
`multiLineString` 메서드는 `MULTILINESTRING`과 동등한 컬럼을 생성합니다.

```
$table->multiLineString('positions');
```

<a name="column-method-multiPoint"></a>
<!-- #### `multiPoint()` -->
#### `multiPoint()`

<!-- The `multiPoint` method creates a `MULTIPOINT` equivalent column: -->
`multiPoint` 메서드는 `MULTIPOINT`와 동등한 컬럼을 생성합니다.

```
$table->multiPoint('positions');
```

<a name="column-method-multiPolygon"></a>
<!-- #### `multiPolygon()` -->
#### `multiPolygon()`

<!-- The `multiPolygon` method creates a `MULTIPOLYGON` equivalent column: -->
`multiPolygon` 메서드는 `MULTIPOLYGON`과 동등한 컬럼을 생성합니다.

```
$table->multiPolygon('positions');
```

<a name="column-method-nullableTimestamps"></a>
<!-- #### `nullableTimestamps()` -->
#### `nullableTimestamps()`

<!-- The `nullableTimestamps` method is an alias of the [timestamps](#column-method-timestamps) method: -->
`nullableTimestamps` 메서드는 [timestamps](#column-method-timestamps) 메서드의 별칭입니다.

```
$table->nullableTimestamps(0);
```

<a name="column-method-nullableMorphs"></a>
<!-- #### `nullableMorphs()` -->
#### `nullableMorphs()`

<!-- The method is similar to the [morphs](#column-method-morphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [morphs](#column-method-morphs) 메서드와 유사하지만, 생성되는 컬럼들이 "nullable"로 설정됩니다.

```
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
<!-- #### `nullableUuidMorphs()` -->
#### `nullableUuidMorphs()`

<!-- The method is similar to the [uuidMorphs](#column-method-uuidMorphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [uuidMorphs](#column-method-uuidMorphs) 메서드와 유사하지만, 생성되는 컬럼들이 "nullable"로 설정됩니다.

```
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-point"></a>
<!-- #### `point()` -->
#### `point()`

<!-- The `point` method creates a `POINT` equivalent column: -->
`point` 메서드는 `POINT`와 동등한 컬럼을 생성합니다.

```
$table->point('position');
```

<a name="column-method-polygon"></a>
<!-- #### `polygon()` -->
#### `polygon()`

<!-- The `polygon` method creates a `POLYGON` equivalent column: -->
`polygon` 메서드는 `POLYGON`과 동등한 컬럼을 생성합니다.

```
$table->polygon('position');
```

<a name="column-method-rememberToken"></a>
<!-- #### `rememberToken()` -->
#### `rememberToken()`

<!-- The `rememberToken` method creates a nullable, `VARCHAR(100)` equivalent column that is intended to store the current "remember me" [authentication token](/docs/8.x/authentication#remembering-users): -->
`rememberToken` 메서드는 현재 "remember me" [authentication token](/docs/8.x/authentication#remembering-users)을 저장하기 위한 nullable, `VARCHAR(100)`와 동등한 컬럼을 생성합니다.

```
$table->rememberToken();
```

<a name="column-method-set"></a>
<!-- #### `set()` -->
#### `set()`

<!-- The `set` method creates a `SET` equivalent column with the given list of valid values: -->
`set` 메서드는 주어진 유효 값 목록으로 `SET`과 동등한 컬럼을 생성합니다.

```
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
<!-- #### `smallIncrements()` -->
#### `smallIncrements()`

<!-- The `smallIncrements` method creates an auto-incrementing `UNSIGNED SMALLINT` equivalent column as a primary key: -->
`smallIncrements` 메서드는 자동 증가하는 `UNSIGNED SMALLINT`와 동등한 컬럼을 기본 키로 생성합니다.

```
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
<!-- #### `smallInteger()` -->
#### `smallInteger()`

<!-- The `smallInteger` method creates a `SMALLINT` equivalent column: -->
`smallInteger` 메서드는 `SMALLINT`와 동등한 컬럼을 생성합니다.

```
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
<!-- #### `softDeletesTz()` -->
#### `softDeletesTz()`

<!-- The `softDeletesTz` method adds a nullable `deleted_at` `TIMESTAMP` (with timezone) equivalent column with an optional precision (total digits). This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletesTz` 메서드는 nullable `deleted_at` `TIMESTAMP`(타임존 포함)과 동등한 컬럼을 선택적 정밀도(전체 자릿수)와 함께 추가합니다. 이 컬럼은 Eloquent의 "소프트 삭제" 기능에서 필요한 `deleted_at` 타임스탬프를 저장하기 위해 사용됩니다.

```
$table->softDeletesTz($column = 'deleted_at', $precision = 0);
```

<a name="column-method-softDeletes"></a>
<!-- #### `softDeletes()` -->
#### `softDeletes()`

<!-- The `softDeletes` method adds a nullable `deleted_at` `TIMESTAMP` equivalent column with an optional precision (total digits). This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletes` 메서드는 nullable `deleted_at` `TIMESTAMP`와 동등한 컬럼을 선택적 정밀도(전체 자릿수)와 함께 추가합니다. 이 컬럼은 Eloquent의 "소프트 삭제" 기능에서 필요한 `deleted_at` 타임스탬프를 저장하기 위해 사용됩니다.

```
$table->softDeletes($column = 'deleted_at', $precision = 0);
```

<a name="column-method-string"></a>
<!-- #### `string()` -->
#### `string()`

<!-- The `string` method creates a `VARCHAR` equivalent column of the given length: -->
`string` 메서드는 주어진 길이의 `VARCHAR`와 동등한 컬럼을 생성합니다.

```
$table->string('name', 100);
```

<a name="column-method-text"></a>
<!-- #### `text()` -->
#### `text()`

<!-- The `text` method creates a `TEXT` equivalent column: -->
`text` 메서드는 `TEXT`와 동등한 컬럼을 생성합니다.

```
$table->text('description');
```

<a name="column-method-timeTz"></a>
<!-- #### `timeTz()` -->
#### `timeTz()`

<!-- The `timeTz` method creates a `TIME` (with timezone) equivalent column with an optional precision (total digits): -->
`timeTz` 메서드는 선택적으로 정밀도(전체 자릿수)를 지정할 수 있는, 타임존 정보를 포함하는 `TIME`과 동등한 컬럼을 생성합니다.

```
$table->timeTz('sunrise', $precision = 0);
```

<a name="column-method-time"></a>
<!-- #### `time()` -->
#### `time()`

<!-- The `time` method creates a `TIME` equivalent column with an optional precision (total digits): -->
`time` 메서드는 선택적으로 정밀도(전체 자릿수)를 지정할 수 있는 `TIME`과 동등한 컬럼을 생성합니다.

```
$table->time('sunrise', $precision = 0);
```

<a name="column-method-timestampTz"></a>
<!-- #### `timestampTz()` -->
#### `timestampTz()`

<!-- The `timestampTz` method creates a `TIMESTAMP` (with timezone) equivalent column with an optional precision (total digits): -->
`timestampTz` 메서드는 선택적으로 정밀도(전체 자릿수)를 지정할 수 있는, 타임존 정보를 포함하는 `TIMESTAMP`와 동등한 컬럼을 생성합니다.

```
$table->timestampTz('added_at', $precision = 0);
```

<a name="column-method-timestamp"></a>
<!-- #### `timestamp()` -->
#### `timestamp()`

<!-- The `timestamp` method creates a `TIMESTAMP` equivalent column with an optional precision (total digits): -->
`timestamp` 메서드는 선택적으로 정밀도(전체 자릿수)를 지정할 수 있는 `TIMESTAMP`와 동등한 컬럼을 생성합니다.

```
$table->timestamp('added_at', $precision = 0);
```

<a name="column-method-timestampsTz"></a>
<!-- #### `timestampsTz()` -->
#### `timestampsTz()`

<!-- The `timestampsTz` method creates `created_at` and `updated_at` `TIMESTAMP` (with timezone) equivalent columns with an optional precision (total digits): -->
`timestampsTz` 메서드는 선택적으로 정밀도(전체 자릿수)를 지정할 수 있는 `created_at`과 `updated_at` 타임존 정보를 포함하는 `TIMESTAMP`와 동등한 컬럼을 생성합니다.

```
$table->timestampsTz($precision = 0);
```

<a name="column-method-timestamps"></a>
<!-- #### `timestamps()` -->
#### `timestamps()`

<!-- The `timestamps` method creates `created_at` and `updated_at` `TIMESTAMP` equivalent columns with an optional precision (total digits): -->
`timestamps` 메서드는 선택적으로 정밀도(전체 자릿수)를 지정할 수 있는 `created_at`과 `updated_at` `TIMESTAMP`와 동등한 컬럼을 생성합니다.

```
$table->timestamps($precision = 0);
```

<a name="column-method-tinyIncrements"></a>
<!-- #### `tinyIncrements()` -->
#### `tinyIncrements()`

<!-- The `tinyIncrements` method creates an auto-incrementing `UNSIGNED TINYINT` equivalent column as a primary key: -->
`tinyIncrements` 메서드는 자동 증가하는 `UNSIGNED TINYINT`와 동등한 컬럼을 기본 키로 생성합니다.

```
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
<!-- #### `tinyInteger()` -->
#### `tinyInteger()`

<!-- The `tinyInteger` method creates a `TINYINT` equivalent column: -->
`tinyInteger` 메서드는 `TINYINT`와 동등한 컬럼을 생성합니다.

```
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
<!-- #### `tinyText()` -->
#### `tinyText()`

<!-- The `tinyText` method creates a `TINYTEXT` equivalent column: -->
`tinyText` 메서드는 `TINYTEXT`와 동등한 컬럼을 생성합니다.

```
$table->tinyText('notes');
```

<a name="column-method-unsignedBigInteger"></a>
<!-- #### `unsignedBigInteger()` -->
#### `unsignedBigInteger()`

<!-- The `unsignedBigInteger` method creates an `UNSIGNED BIGINT` equivalent column: -->
`unsignedBigInteger` 메서드는 `UNSIGNED BIGINT`와 동등한 컬럼을 생성합니다.

```
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedDecimal"></a>
<!-- #### `unsignedDecimal()` -->
#### `unsignedDecimal()`

<!-- The `unsignedDecimal` method creates an `UNSIGNED DECIMAL` equivalent column with an optional precision (total digits) and scale (decimal digits): -->
`unsignedDecimal` 메서드는 선택적으로 정밀도(전체 자릿수)와 소수점 자릿수를 지정할 수 있는 `UNSIGNED DECIMAL`과 동등한 컬럼을 생성합니다.

```
$table->unsignedDecimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-unsignedInteger"></a>
<!-- #### `unsignedInteger()` -->
#### `unsignedInteger()`

<!-- The `unsignedInteger` method creates an `UNSIGNED INTEGER` equivalent column: -->
`unsignedInteger` 메서드는 `UNSIGNED INTEGER`와 동등한 컬럼을 생성합니다.

```
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
<!-- #### `unsignedMediumInteger()` -->
#### `unsignedMediumInteger()`

<!-- The `unsignedMediumInteger` method creates an `UNSIGNED MEDIUMINT` equivalent column: -->
`unsignedMediumInteger` 메서드는 `UNSIGNED MEDIUMINT`와 동등한 컬럼을 생성합니다.

```
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
<!-- #### `unsignedSmallInteger()` -->
#### `unsignedSmallInteger()`

<!-- The `unsignedSmallInteger` method creates an `UNSIGNED SMALLINT` equivalent column: -->
`unsignedSmallInteger` 메서드는 `UNSIGNED SMALLINT`와 동등한 컬럼을 생성합니다.

```
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
<!-- #### `unsignedTinyInteger()` -->
#### `unsignedTinyInteger()`

<!-- The `unsignedTinyInteger` method creates an `UNSIGNED TINYINT` equivalent column: -->
`unsignedTinyInteger` 메서드는 `UNSIGNED TINYINT`와 동등한 컬럼을 생성합니다.

```
$table->unsignedTinyInteger('votes');
```

<a name="column-method-uuidMorphs"></a>
<!-- #### `uuidMorphs()` -->
#### `uuidMorphs()`

<!-- The `uuidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(36)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`uuidMorphs` 메서드는 `{column}_id` `CHAR(36)`과 동등한 컬럼, 그리고 `{column}_type` `VARCHAR`와 동등한 컬럼을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/8.x/eloquent-relationships) that use UUID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 메서드는 UUID 식별자를 사용하는 다형적 [Eloquent relationship](/docs/8.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용합니다. 아래 예제에서는 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다.

```
$table->uuidMorphs('taggable');
```

<a name="column-method-uuid"></a>
<!-- #### `uuid()` -->
#### `uuid()`

<!-- The `uuid` method creates a `UUID` equivalent column: -->
`uuid` 메서드는 `UUID`와 동등한 컬럼을 생성합니다.

```
$table->uuid('id');
```

<a name="column-method-year"></a>
<!-- #### `year()` -->
#### `year()`

<!-- The `year` method creates a `YEAR` equivalent column: -->
`year` 메서드는 `YEAR`와 동등한 컬럼을 생성합니다.

```
$table->year('birth_year');
```

<a name="column-modifiers"></a>
<!-- ### Column Modifiers -->
### Column Modifiers

<!-- In addition to the column types listed above, there are several column "modifiers" you may use when adding a column to a database table. For example, to make the column "nullable", you may use the `nullable` method: -->
위에서 소개한 컬럼 타입 외에도, 데이터베이스 테이블에 컬럼을 추가할 때 사용할 수 있는 다양한 컬럼 "수정자(modifier)"가 있습니다. 예를 들어, 컬럼을 "nullable"로 만들고 싶다면 `nullable` 메서드를 사용할 수 있습니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

<!-- The following table contains all of the available column modifiers. This list does not include [index modifiers](#creating-indexes): -->
아래 표는 사용 가능한 모든 컬럼 수정자를 정리한 것입니다. (여기에는 [index modifiers](#creating-indexes)는 포함되지 않습니다.)

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
수정자         |  설명
--------      |  ----------
`->after('column')`           |  다른 컬럼 "뒤에" 컬럼을 배치합니다 (MySQL).
`->autoIncrement()`           |  INTEGER 컬럼을 자동 증가(기본 키)로 지정합니다.
`->charset('utf8mb4')`        |  컬럼의 문자셋을 지정합니다 (MySQL).
`->collation('utf8mb4_unicode_ci')` |  컬럼의 정렬 규칙(collation)을 지정합니다 (MySQL/PostgreSQL/SQL Server).
`->comment('my comment')`     |  컬럼에 주석을 추가합니다 (MySQL/PostgreSQL).
`->default($value)`           |  컬럼의 "기본값"을 지정합니다.
`->first()`                   |  테이블에서 컬럼을 "첫 번째" 위치에 배치합니다 (MySQL).
`->from($integer)`            |  자동 증가 필드(시퀀스)의 시작 값을 지정합니다 (MySQL / PostgreSQL).
`->invisible()`               |  `SELECT *` 쿼리에서 컬럼을 "안 보이게" 숨깁니다 (MySQL).
`->nullable($value = true)`   |  컬럼에 NULL 값 입력을 허용합니다.
`->storedAs($expression)`     |  저장된 생성 컬럼(Stored Generated Column)을 만듭니다 (MySQL / PostgreSQL).
`->unsigned()`                |  INTEGER 컬럼을 UNSIGNED로 지정합니다 (MySQL).
`->useCurrent()`              |  TIMESTAMP 컬럼의 기본값을 CURRENT_TIMESTAMP로 지정합니다.
`->useCurrentOnUpdate()`      |  레코드가 업데이트될 때 TIMESTAMP 컬럼 값을 CURRENT_TIMESTAMP로 지정합니다.
`->virtualAs($expression)`    |  가상 생성 컬럼(Virtual Generated Column)을 만듭니다 (MySQL / PostgreSQL / SQLite).
`->generatedAs($expression)`  |  명시적 시퀀스 옵션과 함께 식별자 컬럼을 생성합니다 (PostgreSQL).
`->always()`                  |  식별자 컬럼의 입력값과 시퀀스 값의 우선순위 규칙을 정합니다 (PostgreSQL).
`->isGeometry()`              |  공간 컬럼 타입을 `geometry`로 지정합니다. 기본 타입은 `geography`입니다 (PostgreSQL).

<a name="default-expressions"></a>
<!-- #### Default Expressions -->
#### Default Expressions

<!-- The `default` modifier accepts a value or an `Illuminate\Database\Query\Expression` instance. Using an `Expression` instance will prevent Laravel from wrapping the value in quotes and allow you to use database specific functions. One situation where this is particularly useful is when you need to assign default values to JSON columns: -->
`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 인수로 받을 수 있습니다. `Expression` 인스턴스를 사용하면 Laravel이 값을 따옴표로 감싸지 않고, 데이터베이스에서 제공하는 특수 함수나 표현식을 그대로 사용할 수 있습니다. 특히 JSON 컬럼에 기본값을 지정해야 할 때 유용합니다.

```
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

class CreateFlightsTable extends Migration
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
}
```

> [!NOTE]
> 기본값 표현식 지원 여부는 사용하는 데이터베이스 드라이버, 데이터베이스 버전, 그리고 해당 필드의 타입에 따라 달라집니다. 자세한 내용은 각 데이터베이스의 공식 문서를 참고하세요.

<a name="column-order"></a>
<!-- #### Column Order -->
#### Column Order

<!-- When using the MySQL database, the `after` method may be used to add columns after an existing column in the schema: -->
MySQL 데이터베이스를 사용하는 경우, `after` 메서드를 사용하여 기존 컬럼 "뒤에" 새로운 컬럼들을 추가할 수 있습니다.

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
컬럼을 수정하기 전에, Composer 패키지 매니저를 사용하여 `doctrine/dbal` 패키지를 설치해야 합니다. Doctrine DBAL 라이브러리는 컬럼의 현재 상태를 파악하고, 변경 요청에 맞는 SQL 쿼리를 생성하기 위해 필요합니다.

```
composer require doctrine/dbal
```

<!-- If you plan to modify columns created using the `timestamp` method, you must also add the following configuration to your application's `config/database.php` configuration file: -->
`timestamp` 메서드로 생성한 컬럼을 수정하려면, 애플리케이션의 `config/database.php` 설정 파일에 아래 내용을 추가해야 합니다.

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> [!NOTE]
> 애플리케이션에서 Microsoft SQL Server를 사용하고 있다면, 반드시 `doctrine/dbal:^3.0`을 설치했는지 확인하세요.

<a name="updating-column-attributes"></a>

<!-- #### Updating Column Attributes -->
#### Updating Column Attributes

<!-- The `change` method allows you to modify the type and attributes of existing columns. For example, you may wish to increase the size of a `string` column. To see the `change` method in action, let's increase the size of the `name` column from 25 to 50. To accomplish this, we simply define the new state of the column and then call the `change` method: -->
`change` 메서드를 사용하면 기존 컬럼의 타입이나 속성을 변경할 수 있습니다. 예를 들어, `string` 컬럼의 크기를 늘리고 싶을 때 사용할 수 있습니다. `change` 메서드의 동작 방식을 확인하기 위해, `name` 컬럼의 길이를 25에서 50으로 늘려보겠습니다. 이를 위해 컬럼의 새로운 상태를 정의한 후, `change` 메서드를 호출하면 됩니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

<!-- We could also modify a column to be nullable: -->
또한, 컬럼을 nullable(널 허용)로 변경하는 것도 가능합니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->nullable()->change();
});
```

> [!NOTE]
> 다음 컬럼 타입들에 대해 수정이 가능합니다: `bigInteger`, `binary`, `boolean`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `uuid`.  `timestamp` 컬럼 타입을 수정하려면 [Doctrine type must be registered](#prerequisites)해야 합니다.

<a name="renaming-columns"></a>
<!-- #### Renaming Columns -->
#### Renaming Columns

<!-- To rename a column, you may use the `renameColumn` method provided by the schema builder blueprint. Before renaming a column, ensure that you have installed the `doctrine/dbal` library via the Composer package manager: -->
컬럼명을 변경하려면, 스키마 빌더 블루프린트에서 제공하는 `renameColumn` 메서드를 사용할 수 있습니다. 컬럼명을 변경하기 전에, Composer 패키지 매니저로 `doctrine/dbal` 라이브러리를 설치했는지 반드시 확인하세요.

```
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

> [!NOTE]
> 현재 `enum` 컬럼의 이름 변경은 지원되지 않습니다.

<a name="dropping-columns"></a>
<!-- ### Dropping Columns -->
### Dropping Columns

<!-- To drop a column, you may use the `dropColumn` method on the schema builder blueprint. If your application is utilizing an SQLite database, you must install the `doctrine/dbal` package via the Composer package manager before the `dropColumn` method may be used: -->
컬럼을 삭제하려면, 스키마 빌더 블루프린트의 `dropColumn` 메서드를 사용합니다. 만약 SQLite 데이터베이스를 사용하는 애플리케이션이라면, `dropColumn` 메서드를 사용하기 전에 Composer 패키지 매니저로 `doctrine/dbal` 패키지를 반드시 설치해야 합니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

<!-- You may drop multiple columns from a table by passing an array of column names to the `dropColumn` method: -->
테이블에서 여러 개의 컬럼을 삭제하고 싶다면, 컬럼명들을 배열로 `dropColumn` 메서드에 전달하면 됩니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

> [!NOTE]
> SQLite 데이터베이스를 사용할 경우, 하나의 마이그레이션에서 여러 컬럼을 한 번에 삭제하거나 수정하는 작업은 지원되지 않습니다.

<a name="available-command-aliases"></a>
<!-- #### Available Command Aliases -->
#### Available Command Aliases

<!-- Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below: -->
Laravel은 자주 사용하는 컬럼 유형을 간단하게 삭제할 수 있는 여러 유틸리티 메서드를 제공합니다. 아래 표에서 각 메서드의 역할을 확인할 수 있습니다.

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
명령어  |  설명
-------  |  -----------
`$table->dropMorphs('morphable');`  |  `morphable_id`와 `morphable_type` 컬럼을 삭제합니다.
`$table->dropRememberToken();`  |  `remember_token` 컬럼을 삭제합니다.
`$table->dropSoftDeletes();`  |  `deleted_at` 컬럼을 삭제합니다.
`$table->dropSoftDeletesTz();`  |  `dropSoftDeletes()` 메서드의 에일리어스입니다.
`$table->dropTimestamps();`  |  `created_at`과 `updated_at` 컬럼을 삭제합니다.
`$table->dropTimestampsTz();` |  `dropTimestamps()` 메서드의 에일리어스입니다.

<a name="indexes"></a>
<!-- ## Indexes -->
## Indexes

<a name="creating-indexes"></a>
<!-- ### Creating Indexes -->
### Creating Indexes

<!-- The Laravel schema builder supports several types of indexes. The following example creates a new `email` column and specifies that its values should be unique. To create the index, we can chain the `unique` method onto the column definition: -->
Laravel 스키마 빌더는 다양한 유형의 인덱스를 지원합니다. 아래 예시는 새로운 `email` 컬럼을 생성하면서 해당 컬럼 값이 유일하도록 지정합니다. 인덱스를 생성하려면, 컬럼 정의에 `unique` 메서드를 체이닝하면 됩니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

<!-- Alternatively, you may create the index after defining the column. To do so, you should call the `unique` method on the schema builder blueprint. This method accepts the name of the column that should receive a unique index: -->
또는, 컬럼을 먼저 정의한 뒤 나중에 인덱스를 추가할 수도 있습니다. 이 경우, 스키마 빌더 블루프린트의 `unique` 메서드를 사용하면 됩니다. 인덱스를 적용할 컬럼명을 인자로 전달하면 됩니다.

```
$table->unique('email');
```

<!-- You may even pass an array of columns to an index method to create a compound (or composite) index: -->
또한, 인덱스 메서드에 컬럼명을 배열로 전달하면 조합(composite) 인덱스도 만들 수 있습니다.

```
$table->index(['account_id', 'created_at']);
```

<!-- When creating an index, Laravel will automatically generate an index name based on the table, column names, and the index type, but you may pass a second argument to the method to specify the index name yourself: -->
인덱스를 생성할 때, Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 유형을 결합하여 인덱스 이름을 자동 생성합니다. 하지만, 메서드에 두 번째 인자를 전달하여 직접 인덱스 이름을 지정할 수도 있습니다.

```
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
<!-- #### Available Index Types -->
#### Available Index Types

<!-- Laravel's schema builder blueprint class provides methods for creating each type of index supported by Laravel. Each index method accepts an optional second argument to specify the name of the index. If omitted, the name will be derived from the names of the table and column(s) used for the index, as well as the index type. Each of the available index methods is described in the table below: -->
Laravel의 스키마 빌더 블루프린트 클래스는 Laravel이 지원하는 각 인덱스 유형별로 메서드를 제공합니다. 각 인덱스 메서드는 인덱스 이름을 지정할 수 있는 두 번째 인자를 선택적으로 받을 수 있습니다. 만약 이름을 생략하면, 인덱스에 사용된 테이블명과 컬럼명, 인덱스 유형 등을 조합하여 자동 생성됩니다. 아래 표에서 각 인덱스 메서드에 대해 확인하실 수 있습니다.

<!--
Command  |  Description
-------  |  -----------
`$table->primary('id');`  |  Adds a primary key.
`$table->primary(['id', 'parent_id']);`  |  Adds composite keys.
`$table->unique('email');`  |  Adds a unique index.
`$table->index('state');`  |  Adds an index.
`$table->fulltext('body');`  |  Adds a fulltext index (MySQL/PostgreSQL).
`$table->fulltext('body')->language('english');`  |  Adds a fulltext index of the specified language (PostgreSQL).
`$table->spatialIndex('location');`  |  Adds a spatial index (except SQLite).
-->
명령어  |  설명
-------  |  -----------
`$table->primary('id');`  |  기본키(primary key)를 추가합니다.
`$table->primary(['id', 'parent_id']);`  |  복합키(composite key)를 추가합니다.
`$table->unique('email');`  |  유니크 인덱스를 추가합니다.
`$table->index('state');`  |  일반 인덱스를 추가합니다.
`$table->fulltext('body');`  |  전문(fulltext) 인덱스를 추가합니다 (MySQL/PostgreSQL).
`$table->fulltext('body')->language('english');`  |  특정 언어의 전문 인덱스를 추가합니다 (PostgreSQL).
`$table->spatialIndex('location');`  |  공간(spatial) 인덱스를 추가합니다 (SQLite 제외).

<a name="index-lengths-mysql-mariadb"></a>
<!-- #### Index Lengths & MySQL / MariaDB -->
#### Index Lengths & MySQL / MariaDB

<!-- By default, Laravel uses the `utf8mb4` character set. If you are running a version of MySQL older than the 5.7.7 release or MariaDB older than the 10.2.2 release, you may need to manually configure the default string length generated by migrations in order for MySQL to create indexes for them. You may configure the default string length by calling the `Schema::defaultStringLength` method within the `boot` method of your `App\Providers\AppServiceProvider` class: -->
Laravel은 기본적으로 `utf8mb4` 문자셋을 사용합니다. 만약 MySQL 5.7.7 미만 버전이나 MariaDB 10.2.2 미만 버전을 사용한다면, 마이그레이션이 생성하는 문자열의 기본 길이를 직접 지정해주어야 인덱스 생성에서 오류가 발생하지 않습니다. 이 경우, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 안에서 `Schema::defaultStringLength` 메서드를 사용해 기본 문자열 길이를 설정할 수 있습니다.

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
또 다른 대안으로, 데이터베이스의 `innodb_large_prefix` 옵션을 활성화할 수도 있습니다. 이 옵션 활성화 방법은 각 데이터베이스의 공식 문서를 참고하시기 바랍니다.

<a name="renaming-indexes"></a>
<!-- ### Renaming Indexes -->
### Renaming Indexes

<!-- To rename an index, you may use the `renameIndex` method provided by the schema builder blueprint. This method accepts the current index name as its first argument and the desired name as its second argument: -->
인덱스의 이름을 변경하려면, 스키마 빌더 블루프린트에서 제공하는 `renameIndex` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 기존 인덱스 이름, 두 번째 인자로 변경할 이름을 받습니다.

```
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
<!-- ### Dropping Indexes -->
### Dropping Indexes

<!-- To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples: -->
인덱스를 삭제하려면, 해당 인덱스의 이름을 지정해야 합니다. Laravel은 기본적으로 테이블명, 인덱싱된 컬럼명, 인덱스 유형을 조합하여 자동으로 인덱스 이름을 부여합니다. 다음 예시를 참고하세요.

<!--
Command  |  Description
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  Drop a primary key from the "users" table.
`$table->dropUnique('users_email_unique');`  |  Drop a unique index from the "users" table.
`$table->dropIndex('geo_state_index');`  |  Drop a basic index from the "geo" table.
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  Drop a spatial index from the "geo" table  (except SQLite).
-->
명령어  |  설명
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  "users" 테이블의 기본키를 삭제합니다.
`$table->dropUnique('users_email_unique');`  |  "users" 테이블의 유니크 인덱스를 삭제합니다.
`$table->dropIndex('geo_state_index');`  |  "geo" 테이블의 일반 인덱스를 삭제합니다.
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  "geo" 테이블의 공간 인덱스를 삭제합니다 (SQLite 제외).

<!-- If you pass an array of columns into a method that drops indexes, the conventional index name will be generated based on the table name, columns, and index type: -->
만약 컬럼 명 배열을 사용하여 인덱스를 삭제하는 메서드를 호출하면, Laravel은 테이블명, 컬럼명, 인덱스 유형을 결합해 관례에 따라 인덱스 이름을 생성하여 삭제합니다.

```
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a name="foreign-key-constraints"></a>
<!-- ### Foreign Key Constraints -->
### Foreign Key Constraints

<!-- Laravel also provides support for creating foreign key constraints, which are used to force referential integrity at the database level. For example, let's define a `user_id` column on the `posts` table that references the `id` column on a `users` table: -->
Laravel은 외래 키 제약조건 생성을 지원하여, 데이터베이스 수준에서 참조 무결성을 강제할 수 있습니다. 예를 들어, `posts` 테이블에 `user_id` 컬럼을 정의하고, 해당 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 설정할 수 있습니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

<!-- Since this syntax is rather verbose, Laravel provides additional, terser methods that use conventions to provide a better developer experience. When using the `foreignId` method to create your column, the example above can be rewritten like so: -->
이 방식은 다소 장황하므로, Laravel에서는 더 간편한 문법도 제공합니다. `foreignId` 메서드를 사용하여 컬럼을 생성하고, 예시처럼 코드를 간소화할 수 있습니다.

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column, while the `constrained` method will use conventions to determine the table and column name being referenced. If your table name does not match Laravel's conventions, you may specify the table name by passing it as an argument to the `constrained` method: -->
`foreignId` 메서드는 `UNSIGNED BIGINT`에 해당하는 컬럼을 생성하고, `constrained` 메서드는 관례에 따라 참조할 테이블과 컬럼명을 자동으로 결정합니다. 만약 테이블명이 Laravel의 관례와 다르다면, `constrained` 메서드에 테이블명을 인자로 전달할 수 있습니다.

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained('users');
});
```

<!-- You may also specify the desired action for the "on delete" and "on update" properties of the constraint: -->
또한, 외래 키 제약조건의 "on delete"와 "on update" 동작을 직접 지정할 수도 있습니다.

```
$table->foreignId('user_id')
      ->constrained()
      ->onUpdate('cascade')
      ->onDelete('cascade');
```

<!-- An alternative, expressive syntax is also provided for these actions: -->
이 동작을 위한 대체 문법도 제공됩니다.

<!--
Method  |  Description
-------  |  -----------
`$table->cascadeOnUpdate();` | Updates should cascade.
`$table->restrictOnUpdate();`| Updates should be restricted.
`$table->cascadeOnDelete();` | Deletes should cascade.
`$table->restrictOnDelete();`| Deletes should be restricted.
`$table->nullOnDelete();`    | Deletes should set the foreign key value to null.
-->
메서드  |  설명
-------  |  -----------
`$table->cascadeOnUpdate();` | 갱신 시(cascade on update) 연쇄적으로 반영합니다.
`$table->restrictOnUpdate();`| 갱신 시(restrict on update) 제한합니다.
`$table->cascadeOnDelete();` | 삭제 시(cascade on delete) 연쇄적으로 반영합니다.
`$table->restrictOnDelete();`| 삭제 시(restrict on delete) 제한합니다.
`$table->nullOnDelete();`    | 삭제 시 해당 컬럼 값을 null로 변경합니다.

<!-- Any additional [column modifiers](#column-modifiers) must be called before the `constrained` method: -->
추가적인 [column modifiers](#column-modifiers)는 반드시 `constrained` 메서드보다 먼저 호출해야 합니다.

```
$table->foreignId('user_id')
      ->nullable()
      ->constrained();
```

<a name="dropping-foreign-keys"></a>
<!-- #### Dropping Foreign Keys -->
#### Dropping Foreign Keys

<!-- To drop a foreign key, you may use the `dropForeign` method, passing the name of the foreign key constraint to be deleted as an argument. Foreign key constraints use the same naming convention as indexes. In other words, the foreign key constraint name is based on the name of the table and the columns in the constraint, followed by a "\_foreign" suffix: -->
외래 키 제약조건을 삭제하려면, 삭제할 외래 키의 이름을 인자로 하여 `dropForeign` 메서드를 사용하면 됩니다. 외래 키 제약조건의 이름은 인덱스 이름과 동일한 관례를 따릅니다. 즉, 테이블명과 컬럼명 조합 뒤에 "\_foreign"이 붙습니다.

```
$table->dropForeign('posts_user_id_foreign');
```

<!-- Alternatively, you may pass an array containing the column name that holds the foreign key to the `dropForeign` method. The array will be converted to a foreign key constraint name using Laravel's constraint naming conventions: -->
또는, 외래 키를 가진 컬럼명을 배열 형태로 `dropForeign` 메서드에 전달할 수도 있습니다. 이 배열은 Laravel의 제약조건 명명 규칙에 따라 외래 키 제약조건명으로 변환됩니다.

```
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
<!-- #### Toggling Foreign Key Constraints -->
#### Toggling Foreign Key Constraints

<!-- You may enable or disable foreign key constraints within your migrations by using the following methods: -->
마이그레이션 내부에서 아래 메서드들을 사용해 외래 키 제약조건을 활성화하거나 비활성화할 수 있습니다.

```
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();
```

> [!NOTE]
> SQLite는 기본적으로 외래 키 제약조건을 비활성화합니다. SQLite를 사용할 경우, 마이그레이션에서 외래 키를 생성하기 전에 반드시 [enable foreign key support](/docs/8.x/database#configuration)해야 합니다. 또한, SQLite에서는 테이블 생성 시에만 외래 키를 지원하며, [not when tables are altered](https://www.sqlite.org/omitted.html).

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- For convenience, each migration operation will dispatch an [event](/docs/8.x/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class: -->
편의를 위해, 각 마이그레이션 작업 시 아래와 같은 [event](/docs/8.x/events)가 발생합니다. 이들 이벤트는 모두 기본 클래스인 `Illuminate\Database\Events\MigrationEvent`를 확장합니다.

<!--
 Class | Description
-------|-------
-->
 클래스 | 설명
-------|-------
| `Illuminate\Database\Events\MigrationsStarted` | 여러 개의 마이그레이션이 실행되기 직전 발생합니다. |
| `Illuminate\Database\Events\MigrationsEnded` | 여러 개의 마이그레이션 실행이 끝난 시점에 발생합니다. |
| `Illuminate\Database\Events\MigrationStarted` | 단일 마이그레이션이 실행되기 직전 발생합니다. |
| `Illuminate\Database\Events\MigrationEnded` | 단일 마이그레이션 실행이 끝난 시점에 발생합니다. |
