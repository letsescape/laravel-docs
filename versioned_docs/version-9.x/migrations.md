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
마이그레이션은 데이터베이스 버전 관리 시스템과 비슷하여, 팀원들이 애플리케이션의 데이터베이스 스키마를 정의하고 공유할 수 있게 해줍니다. 예를 들어, 소스 컨트롤에서 변경사항을 받은 후 동료에게 로컬 데이터베이스의 컬럼을 수동으로 추가하라고 안내한 적이 있다면, 그때 마이그레이션이 해결해 주는 문제를 경험한 것입니다.

<!-- The Laravel `Schema` [facade](/docs/9.x/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns. -->
Laravel의 `Schema` [facade](/docs/9.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 데이터베이스에 독립적으로 테이블을 생성하고 조작할 수 있도록 지원합니다. 일반적으로 마이그레이션에서는 이 파사드를 사용하여 데이터베이스 테이블과 컬럼을 만들거나 수정하게 됩니다.

<a name="generating-migrations"></a>
<a id="writing-migrations" data-translation-alias="true"></a>
<!-- ## Generating Migrations -->
## Generating Migrations

<!-- You may use the `make:migration` [Artisan command](/docs/9.x/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations: -->
데이터베이스 마이그레이션을 생성하려면 `make:migration` [Artisan command](/docs/9.x/artisan)를 사용할 수 있습니다. 새로 생성된 마이그레이션 파일은 `database/migrations` 디렉토리에 저장됩니다. 각 마이그레이션 파일 이름에는 타임스탬프가 포함되어 있어, Laravel이 마이그레이션의 실행 순서를 판단하는 데 사용됩니다.

```shell
php artisan make:migration create_flights_table
```

<!-- Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually. -->
Laravel은 마이그레이션의 이름을 바탕으로, 어떤 테이블을 대상으로 하는지 그리고 새로운 테이블을 생성하려는 것인지 추측을 시도합니다. 만약 Laravel이 마이그레이션 이름에서 테이블명을 파악할 수 있다면, 해당 테이블로 미리 채워진 마이그레이션 파일이 생성됩니다. 그렇지 않은 경우, 마이그레이션 파일에서 직접 테이블명을 지정하면 됩니다.

<!-- If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path. -->
마이그레이션을 생성할 때, 원하는 경로를 직접 지정하고 싶다면 `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 지정하는 경로는 애플리케이션의 기본 경로를 기준으로 상대 경로여야 합니다.

> [!NOTE]
> 마이그레이션 스텁은 [stub publishing](/docs/9.x/artisan#stub-customization)을 통해 직접 커스터마이징 할 수 있습니다.

<a name="squashing-migrations"></a>
<!-- ### Squashing Migrations -->
### Squashing Migrations

<!-- As you build your application, you may accumulate more and more migrations over time. This can lead to your `database/migrations` directory becoming bloated with potentially hundreds of migrations. If you would like, you may "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command: -->
애플리케이션을 개발할수록 시간에 따라 점점 더 많은 마이그레이션 파일이 쌓일 수 있습니다. 이렇게 되면 `database/migrations` 디렉토리가 수백 개의 파일로 인해 너무 복잡해질 수 있습니다. 이럴 때는 여러 마이그레이션을 하나의 SQL 파일로 "병합(squash)"할 수 있습니다. 먼저, `schema:dump` 명령어를 실행해보세요.

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

<!-- When you execute this command, Laravel will write a "schema" file to your application's `database/schema` directory. The schema file's name will correspond to the database connection. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will execute first the SQL statements of the schema file of the database connection you are using. After executing the schema file's statements, Laravel will execute any remaining migrations that were not part of the schema dump. -->
이 명령어를 실행하면, Laravel이 애플리케이션의 `database/schema` 디렉토리에 "스키마" 파일을 생성합니다. 이 파일의 이름은 데이터베이스 커넥션과 매칭됩니다. 이제 데이터베이스에 아직 실행된 마이그레이션이 없을 때 마이그레이션을 시도하면, Laravel은 먼저 사용하는 데이터베이스 커넥션에 맞는 스키마 파일의 SQL 구문을 실행합니다. 그리고 나서, 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 차례로 실행합니다.

<!-- If your application's tests use a different database connection than the one you typically use during local development, you should ensure you have dumped a schema file using that database connection so that your tests are able to build your database. You may wish to do this after dumping the database connection you typically use during local development: -->
애플리케이션의 테스트가 로컬 개발에 사용하는 데이터베이스 커넥션과 다른 커넥션을 사용한다면, 해당 커넥션으로도 스키마 파일을 덤프해 테스트 환경에서도 데이터베이스를 올릴 수 있도록 해야 합니다. 이 경우, 로컬 개발용 커넥션의 스키마를 덤프한 후 아래와 같이 테스트용 커넥션도 추가로 덤프할 수 있습니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

<!-- You should commit your database schema file to source control so that other new developers on your team may quickly create your application's initial database structure. -->
생성된 데이터베이스 스키마 파일은 반드시 소스 컨트롤에 커밋하여 팀의 다른 신규 개발자들도 빠르게 애플리케이션의 초기 데이터베이스 구조를 만들 수 있도록 해야 합니다.

> [!WARNING]
> 마이그레이션 병합(Squashing)은 MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며, 각 데이터베이스의 커맨드 라인 클라이언트를 활용합니다. 스키마 덤프 파일은 메모리 기반 SQLite 데이터베이스로는 복원할 수 없습니다.

<a name="migration-structure"></a>
<!-- ## Migration Structure -->
## Migration Structure

<!-- A migration class contains two methods: `up` and `down`. The `up` method is used to add new tables, columns, or indexes to your database, while the `down` method should reverse the operations performed by the `up` method. -->
마이그레이션 클래스에는 `up`과 `down` 두 가지 메서드가 들어 있습니다. `up` 메서드는 데이터베이스에 새 테이블, 컬럼, 인덱스를 추가할 때 사용하고, `down` 메서드는 `up` 메서드에서 실행한 작업을 되돌릴 때 사용합니다.

<!-- Within both of these methods, you may use the Laravel schema builder to expressively create and modify tables. To learn about all of the methods available on the `Schema` builder, [check out its documentation](#creating-tables). For example, the following migration creates a `flights` table: -->
이 두 메서드 안에서는 Laravel의 스키마 빌더(schema builder)를 활용해 테이블을 간결하게 만들고 수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메서드가 궁금하다면 [check out its documentation](#creating-tables)를 참고하세요. 예를 들어, 다음 마이그레이션은 `flights` 테이블을 생성합니다.

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
마이그레이션이 애플리케이션의 기본 데이터베이스 커넥션이 아닌 다른 커넥션을 대상으로 동작해야 한다면, 마이그레이션 클래스 내에 `$connection` 속성을 설정해야 합니다.

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
모든 미실행 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 실행하세요.

```shell
php artisan migrate
```

<!-- If you would like to see which migrations have run thus far, you may use the `migrate:status` Artisan command: -->
지금까지 수행된 마이그레이션 목록을 확인하고 싶다면 `migrate:status` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan migrate:status
```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate` command: -->
마이그레이션을 실제로 실행하지 않고 어떤 SQL문이 실행될지 미리 확인하려면, `migrate` 명령에 `--pretend` 플래그를 추가하세요.

```shell
php artisan migrate --pretend
```

<!-- #### Isolating Migration Execution -->
#### Isolating Migration Execution

<!-- If you are deploying your application across multiple servers and running migrations as part of your deployment process, you likely do not want two servers attempting to migrate the database at the same time. To avoid this, you may use the `isolated` option when invoking the `migrate` command. -->
여러 서버에 애플리케이션을 배포하면서 마이그레이션을 자동으로 실행하는 경우, 두 서버가 동시에 마이그레이션을 시도하지 않도록 하고 싶을 수 있습니다. 이럴 땐 `migrate` 명령 실행 시 `isolated` 옵션을 사용할 수 있습니다.

<!-- When the `isolated` option is provided, Laravel will acquire an atomic lock using your application's cache driver before attempting to run your migrations. All other attempts to run the `migrate` command while that lock is held will not execute; however, the command will still exit with a successful exit status code: -->
`isolated` 옵션을 전달하면, Laravel은 마이그레이션 실행 전에 애플리케이션의 캐시 드라이버를 이용해서 원자적(atomic) 락을 획득합니다. 락이 걸린 동안 `migrate` 명령을 실행하려는 다른 모든 시도는 실행되지 않지만, 명령은 정상 종료 상태로 마무리됩니다.

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 합니다. 게다가, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
<!-- #### Forcing Migrations To Run In Production -->
#### Forcing Migrations To Run In Production

<!-- Some migration operations are destructive, which means they may cause you to lose data. In order to protect you from running these commands against your production database, you will be prompted for confirmation before the commands are executed. To force the commands to run without a prompt, use the `--force` flag: -->
일부 마이그레이션 작업은 데이터 손실을 유발할 수 있으므로, 실수로 운영 데이터베이스에 실행하는 것을 방지하기 위해 명령이 수행되기 전에 확인을 요청합니다. 확인 없이 명령을 강제로 실행하려면 `--force` 플래그를 사용하세요.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
<!-- ### Rolling Back Migrations -->
### Rolling Back Migrations

<!-- To roll back the latest migration operation, you may use the `rollback` Artisan command. This command rolls back the last "batch" of migrations, which may include multiple migration files: -->
가장 최근에 수행한 마이그레이션 작업을 되돌리려면 `rollback` Artisan 명령어를 사용할 수 있습니다. 이 명령은 가장 마지막 "배치(batch)"의 마이그레이션을 롤백하는데, 한 번에 여러 파일을 포함할 수 있습니다.

```shell
php artisan migrate:rollback
```

<!-- You may roll back a limited number of migrations by providing the `step` option to the `rollback` command. For example, the following command will roll back the last five migrations: -->
`rollback` 명령에 `step` 옵션을 추가하면 되돌릴 마이그레이션 수를 제한할 수 있습니다. 예를 들어, 다음 명령은 최근 5개의 마이그레이션만 롤백합니다.

```shell
php artisan migrate:rollback --step=5
```

<!-- The `migrate:reset` command will roll back all of your application's migrations: -->
`migrate:reset` 명령은 애플리케이션의 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
<!-- #### Roll Back & Migrate Using A Single Command -->
#### Roll Back & Migrate Using A Single Command

<!-- The `migrate:refresh` command will roll back all of your migrations and then execute the `migrate` command. This command effectively re-creates your entire database: -->
`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤 `migrate` 명령을 실행합니다. 이 명령을 통해 애플리케이션의 전체 데이터베이스를 새로 구축할 수 있습니다.

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

<!-- You may roll back and re-migrate a limited number of migrations by providing the `step` option to the `refresh` command. For example, the following command will roll back and re-migrate the last five migrations: -->
`refresh` 명령에도 `step` 옵션을 추가하여, 최근 N개의 마이그레이션만 롤백 후 재실행할 수 있습니다. 예를 들어, 최근 5개의 마이그레이션만 롤백하고 다시 마이그레이트하려면 아래와 같이 실행하세요.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
<!-- #### Drop All Tables & Migrate -->
#### Drop All Tables & Migrate

<!-- The `migrate:fresh` command will drop all tables from the database and then execute the `migrate` command: -->
`migrate:fresh` 명령어는 데이터베이스 내의 모든 테이블을 삭제하고, 그 후에 `migrate` 명령을 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

> [!WARNING]
> `migrate:fresh` 명령은 테이블 프리픽스와 관계없이 데이터베이스의 모든 테이블을 삭제합니다. 여러 애플리케이션에서 공유하는 데이터베이스를 개발 환경에서 사용할 때는 주의하여 사용해야 합니다.

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<a name="creating-tables"></a>
<!-- ### Creating Tables -->
### Creating Tables

<!-- To create a new database table, use the `create` method on the `Schema` facade. The `create` method accepts two arguments: the first is the name of the table, while the second is a closure which receives a `Blueprint` object that may be used to define the new table: -->
새 데이터베이스 테이블을 생성하려면 `Schema` 파사드에서 `create` 메서드를 사용하세요. `create` 메서드는 두 개의 인수를 받는데, 첫 번째는 테이블 이름이고, 두 번째는 새 테이블을 정의할 수 있도록 `Blueprint` 객체를 받는 클로저입니다.

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
테이블을 만들 때는, 스키마 빌더의 [column methods](#creating-columns)를 자유롭게 사용해 테이블의 컬럼을 정의할 수 있습니다.

<a name="checking-for-table-column-existence"></a>
<!-- #### Checking For Table / Column Existence -->
#### Checking For Table / Column Existence

<!-- You may check for the existence of a table or column using the `hasTable` and `hasColumn` methods: -->
테이블이나 컬럼이 존재하는지 확인하려면, `hasTable`과 `hasColumn` 메서드를 사용할 수 있습니다.

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
기본 커넥션이 아닌 다른 데이터베이스 커넥션에 대해 스키마 작업을 하고 싶다면, `connection` 메서드를 사용하세요.

```
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

<!-- In addition, a few other properties and methods may be used to define other aspects of the table's creation. The `engine` property may be used to specify the table's storage engine when using MySQL: -->
추가적으로, 테이블 생성 방식에 영향을 주는 몇 가지 속성과 메서드가 있습니다. MySQL을 사용할 때는 `engine` 속성으로 스토리지 엔진을 지정할 수 있습니다.

```
Schema::create('users', function (Blueprint $table) {
    $table->engine = 'InnoDB';

    // ...
});
```

<!-- The `charset` and `collation` properties may be used to specify the character set and collation for the created table when using MySQL: -->
MySQL에서 테이블의 문자셋과 콜레이션을 지정하려면, `charset`과 `collation` 속성을 사용할 수 있습니다.

```
Schema::create('users', function (Blueprint $table) {
    $table->charset = 'utf8mb4';
    $table->collation = 'utf8mb4_unicode_ci';

    // ...
});
```

<!-- The `temporary` method may be used to indicate that the table should be "temporary". Temporary tables are only visible to the current connection's database session and are dropped automatically when the connection is closed: -->
테이블을 "임시 테이블"로 만들고 싶다면, `temporary` 메서드를 사용할 수 있습니다. 임시 테이블은 현재 커넥션의 세션에서만 보이고, 커넥션이 종료되면 자동으로 삭제됩니다.

```
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

<!-- If you would like to add a "comment" to a database table, you may invoke the `comment` method on the table instance. Table comments are currently only supported by MySQL and Postgres: -->
테이블에 "주석(comment)"을 추가하고 싶다면, 테이블 인스턴스에서 `comment` 메서드를 호출하면 됩니다. 테이블 주석은 현재 MySQL과 Postgres에서만 지원됩니다.

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
기존 테이블을 수정하려면 `Schema` 파사드에서 `table` 메서드를 사용할 수 있습니다. `create` 메서드와 마찬가지로 `table` 메서드는 두 개의 인수를 받는데, 첫 번째 인수에는 테이블명을, 두 번째 인수로는 컬럼이나 인덱스를 추가할 수 있는 `Blueprint` 인스턴스를 받는 클로저를 전달합니다.

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
기존 데이터베이스 테이블의 이름을 변경하려면 `rename` 메서드를 사용하세요.

```
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

<!-- To drop an existing table, you may use the `drop` or `dropIfExists` methods: -->
테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다.

```
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
<!-- #### Renaming Tables With Foreign Keys -->
#### Renaming Tables With Foreign Keys

<!-- Before renaming a table, you should verify that any foreign key constraints on the table have an explicit name in your migration files instead of letting Laravel assign a convention based name. Otherwise, the foreign key constraint name will refer to the old table name. -->
테이블 이름을 변경하기 전에는, 해당 테이블의 외래 키 제약조건이 마이그레이션 파일에서 명시적으로 이름이 지정되어 있는지 반드시 확인해야 합니다. 만약 그렇지 않고 Laravel의 기본 관례(convention)대로 이름이 부여되었다면, 외래 키 제약조건 이름이 이전 테이블명을 그대로 참조하게 됩니다.

<a name="columns"></a>
<!-- ## Columns -->
## Columns

<a name="creating-columns"></a>
<!-- ### Creating Columns -->
### Creating Columns

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives an `Illuminate\Database\Schema\Blueprint` instance you may use to add columns to the table: -->
기존 테이블을 수정하려면 `Schema` 파사드의 `table` 메서드를 사용할 수 있습니다. `create` 메서드와 마찬가지로 `table` 메서드는 두 개의 인수를 받는데, 첫 번째 인수에는 테이블명을, 두 번째 인수에는 컬럼을 추가할 수 있도록 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저를 전달합니다.

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
스키마 빌더의 Blueprint에서는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 해당하는 메서드를 제공합니다. 다음 표에서 사용할 수 있는 메서드들을 확인할 수 있습니다.

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
`bigIncrements` 메서드는 자동 증가 `UNSIGNED BIGINT`(기본키) 타입의 컬럼을 생성합니다.

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
`char` 메서드는 지정된 길이의 `CHAR` 타입 컬럼을 생성합니다.

```
$table->char('name', 100);
```

<a name="column-method-dateTimeTz"></a>
<!-- #### `dateTimeTz()` -->
#### `dateTimeTz()`

<!-- The `dateTimeTz` method creates a `DATETIME` (with timezone) equivalent column with an optional precision (total digits): -->
`dateTimeTz` 메서드는 선택적으로 정밀도를 지정할 수 있는(전체 자릿수) `DATETIME` (타임존 포함) 타입의 컬럼을 생성합니다.

```
$table->dateTimeTz('created_at', $precision = 0);
```

<a name="column-method-dateTime"></a>
<!-- #### `dateTime()` -->
#### `dateTime()`

<!-- The `dateTime` method creates a `DATETIME` equivalent column with an optional precision (total digits): -->
`dateTime` 메서드는 선택적으로 정밀도를 지정할 수 있는(전체 자릿수) `DATETIME` 타입의 컬럼을 생성합니다.

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
`decimal` 메서드는 지정한 전체 자릿수(precision) 및 소수 자릿수(scale)로 이루어진 `DECIMAL` 타입의 컬럼을 생성합니다.

```
$table->decimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-double"></a>
<!-- #### `double()` -->
#### `double()`

<!-- The `double` method creates a `DOUBLE` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`double` 메서드는 지정한 전체 자릿수(precision) 및 소수 자릿수(scale)로 이루어진 `DOUBLE` 타입의 컬럼을 생성합니다.

```
$table->double('amount', 8, 2);
```

<a name="column-method-enum"></a>
<!-- #### `enum()` -->
#### `enum()`

<!-- The `enum` method creates a `ENUM` equivalent column with the given valid values: -->
`enum` 메서드는 지정한 유효값 배열로 `ENUM` 타입의 컬럼을 생성합니다.

```
$table->enum('difficulty', ['easy', 'hard']);
```

<a name="column-method-float"></a>

<!-- #### `float()` -->
#### `float()`

<!-- The `float` method creates a `FLOAT` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`float` 메서드는 지정한 정밀도(총 자릿수)와 소수점 자릿수(스케일)을 가지는 `FLOAT` 컬럼을 생성합니다.

```
$table->float('amount', 8, 2);
```

<a name="column-method-foreignId"></a>
<!-- #### `foreignId()` -->
#### `foreignId()`

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column: -->
`foreignId` 메서드는 `UNSIGNED BIGINT`에 해당하는 컬럼을 생성합니다.

```
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
<!-- #### `foreignIdFor()` -->
#### `foreignIdFor()`

<!-- The `foreignIdFor` method adds a `{column}_id UNSIGNED BIGINT` equivalent column for a given model class: -->
`foreignIdFor` 메서드는 지정한 모델 클래스에 대해 `{column}_id UNSIGNED BIGINT`에 해당하는 컬럼을 추가합니다.

```
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
<!-- #### `foreignUlid()` -->
#### `foreignUlid()`

<!-- The `foreignUlid` method creates a `ULID` equivalent column: -->
`foreignUlid` 메서드는 `ULID`에 해당하는 컬럼을 생성합니다.

```
$table->foreignUlid('user_id');
```

<a name="column-method-foreignUuid"></a>
<!-- #### `foreignUuid()` -->
#### `foreignUuid()`

<!-- The `foreignUuid` method creates a `UUID` equivalent column: -->
`foreignUuid` 메서드는 `UUID`에 해당하는 컬럼을 생성합니다.

```
$table->foreignUuid('user_id');
```

<a name="column-method-geometryCollection"></a>
<!-- #### `geometryCollection()` -->
#### `geometryCollection()`

<!-- The `geometryCollection` method creates a `GEOMETRYCOLLECTION` equivalent column: -->
`geometryCollection` 메서드는 `GEOMETRYCOLLECTION`에 해당하는 컬럼을 생성합니다.

```
$table->geometryCollection('positions');
```

<a name="column-method-geometry"></a>
<!-- #### `geometry()` -->
#### `geometry()`

<!-- The `geometry` method creates a `GEOMETRY` equivalent column: -->
`geometry` 메서드는 `GEOMETRY`에 해당하는 컬럼을 생성합니다.

```
$table->geometry('positions');
```

<a name="column-method-id"></a>
<!-- #### `id()` -->
#### `id()`

<!-- The `id` method is an alias of the `bigIncrements` method. By default, the method will create an `id` column; however, you may pass a column name if you would like to assign a different name to the column: -->
`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 `id`라는 컬럼이 생성되지만, 컬럼 이름을 바꾸고 싶다면 다른 이름을 인수로 전달할 수 있습니다.

```
$table->id();
```

<a name="column-method-increments"></a>
<!-- #### `increments()` -->
#### `increments()`

<!-- The `increments` method creates an auto-incrementing `UNSIGNED INTEGER` equivalent column as a primary key: -->
`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER`(기본키) 컬럼을 생성합니다.

```
$table->increments('id');
```

<a name="column-method-integer"></a>
<!-- #### `integer()` -->
#### `integer()`

<!-- The `integer` method creates an `INTEGER` equivalent column: -->
`integer` 메서드는 `INTEGER`에 해당하는 컬럼을 생성합니다.

```
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
<!-- #### `ipAddress()` -->
#### `ipAddress()`

<!-- The `ipAddress` method creates a `VARCHAR` equivalent column: -->
`ipAddress` 메서드는 `VARCHAR`에 해당하는 컬럼을 생성합니다.

```
$table->ipAddress('visitor');
```

<a name="column-method-json"></a>
<!-- #### `json()` -->
#### `json()`

<!-- The `json` method creates a `JSON` equivalent column: -->
`json` 메서드는 `JSON`에 해당하는 컬럼을 생성합니다.

```
$table->json('options');
```

<a name="column-method-jsonb"></a>
<!-- #### `jsonb()` -->
#### `jsonb()`

<!-- The `jsonb` method creates a `JSONB` equivalent column: -->
`jsonb` 메서드는 `JSONB`에 해당하는 컬럼을 생성합니다.

```
$table->jsonb('options');
```

<a name="column-method-lineString"></a>
<!-- #### `lineString()` -->
#### `lineString()`

<!-- The `lineString` method creates a `LINESTRING` equivalent column: -->
`lineString` 메서드는 `LINESTRING`에 해당하는 컬럼을 생성합니다.

```
$table->lineString('positions');
```

<a name="column-method-longText"></a>
<!-- #### `longText()` -->
#### `longText()`

<!-- The `longText` method creates a `LONGTEXT` equivalent column: -->
`longText` 메서드는 `LONGTEXT`에 해당하는 컬럼을 생성합니다.

```
$table->longText('description');
```

<a name="column-method-macAddress"></a>
<!-- #### `macAddress()` -->
#### `macAddress()`

<!-- The `macAddress` method creates a column that is intended to hold a MAC address. Some database systems, such as PostgreSQL, have a dedicated column type for this type of data. Other database systems will use a string equivalent column: -->
`macAddress` 메서드는 MAC 주소를 저장할 컬럼을 생성합니다. PostgreSQL과 같은 일부 데이터베이스 시스템은 이 타입을 위한 전용 컬럼 타입을 제공하며, 다른 데이터베이스 시스템은 문자열 컬럼으로 대체합니다.

```
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
<!-- #### `mediumIncrements()` -->
#### `mediumIncrements()`

<!-- The `mediumIncrements` method creates an auto-incrementing `UNSIGNED MEDIUMINT` equivalent column as a primary key: -->
`mediumIncrements` 메서드는 자동 증가하는 `UNSIGNED MEDIUMINT`(기본키) 컬럼을 생성합니다.

```
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
<!-- #### `mediumInteger()` -->
#### `mediumInteger()`

<!-- The `mediumInteger` method creates a `MEDIUMINT` equivalent column: -->
`mediumInteger` 메서드는 `MEDIUMINT`에 해당하는 컬럼을 생성합니다.

```
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
<!-- #### `mediumText()` -->
#### `mediumText()`

<!-- The `mediumText` method creates a `MEDIUMTEXT` equivalent column: -->
`mediumText` 메서드는 `MEDIUMTEXT`에 해당하는 컬럼을 생성합니다.

```
$table->mediumText('description');
```

<a name="column-method-morphs"></a>
<!-- #### `morphs()` -->
#### `morphs()`

<!-- The `morphs` method is a convenience method that adds a `{column}_id` `UNSIGNED BIGINT` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`morphs` 메서드는 `{column}_id` `UNSIGNED BIGINT`에 해당하는 컬럼과 `{column}_type` `VARCHAR`에 해당하는 컬럼을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/9.x/eloquent-relationships). In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 메서드는 다형성 [Eloquent relationship](/docs/9.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용합니다. 아래 예시에서는 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다.

```
$table->morphs('taggable');
```

<a name="column-method-multiLineString"></a>
<!-- #### `multiLineString()` -->
#### `multiLineString()`

<!-- The `multiLineString` method creates a `MULTILINESTRING` equivalent column: -->
`multiLineString` 메서드는 `MULTILINESTRING`에 해당하는 컬럼을 생성합니다.

```
$table->multiLineString('positions');
```

<a name="column-method-multiPoint"></a>
<!-- #### `multiPoint()` -->
#### `multiPoint()`

<!-- The `multiPoint` method creates a `MULTIPOINT` equivalent column: -->
`multiPoint` 메서드는 `MULTIPOINT`에 해당하는 컬럼을 생성합니다.

```
$table->multiPoint('positions');
```

<a name="column-method-multiPolygon"></a>
<!-- #### `multiPolygon()` -->
#### `multiPolygon()`

<!-- The `multiPolygon` method creates a `MULTIPOLYGON` equivalent column: -->
`multiPolygon` 메서드는 `MULTIPOLYGON`에 해당하는 컬럼을 생성합니다.

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
이 메서드는 [morphs](#column-method-morphs) 메서드와 유사하나, 생성되는 컬럼들이 "nullable" 처리됩니다.

```
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
<!-- #### `nullableUlidMorphs()` -->
#### `nullableUlidMorphs()`

<!-- The method is similar to the [ulidMorphs](#column-method-ulidMorphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [ulidMorphs](#column-method-ulidMorphs) 메서드와 유사하나, 생성되는 컬럼들이 "nullable" 처리됩니다.

```
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
<!-- #### `nullableUuidMorphs()` -->
#### `nullableUuidMorphs()`

<!-- The method is similar to the [uuidMorphs](#column-method-uuidMorphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [uuidMorphs](#column-method-uuidMorphs) 메서드와 유사하나, 생성되는 컬럼들이 "nullable" 처리됩니다.

```
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-point"></a>
<!-- #### `point()` -->
#### `point()`

<!-- The `point` method creates a `POINT` equivalent column: -->
`point` 메서드는 `POINT`에 해당하는 컬럼을 생성합니다.

```
$table->point('position');
```

<a name="column-method-polygon"></a>
<!-- #### `polygon()` -->
#### `polygon()`

<!-- The `polygon` method creates a `POLYGON` equivalent column: -->
`polygon` 메서드는 `POLYGON`에 해당하는 컬럼을 생성합니다.

```
$table->polygon('position');
```

<a name="column-method-rememberToken"></a>
<!-- #### `rememberToken()` -->
#### `rememberToken()`

<!-- The `rememberToken` method creates a nullable, `VARCHAR(100)` equivalent column that is intended to store the current "remember me" [authentication token](/docs/9.x/authentication#remembering-users): -->
`rememberToken` 메서드는 현재 "remember me" [authentication token](/docs/9.x/authentication#remembering-users)을 저장하기 위한 nullable `VARCHAR(100)` 컬럼을 생성합니다.

```
$table->rememberToken();
```

<a name="column-method-set"></a>
<!-- #### `set()` -->
#### `set()`

<!-- The `set` method creates a `SET` equivalent column with the given list of valid values: -->
`set` 메서드는 지정한 값 목록으로 `SET` 타입의 컬럼을 생성합니다.

```
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
<!-- #### `smallIncrements()` -->
#### `smallIncrements()`

<!-- The `smallIncrements` method creates an auto-incrementing `UNSIGNED SMALLINT` equivalent column as a primary key: -->
`smallIncrements` 메서드는 자동 증가하는 `UNSIGNED SMALLINT`(기본키) 컬럼을 생성합니다.

```
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
<!-- #### `smallInteger()` -->
#### `smallInteger()`

<!-- The `smallInteger` method creates a `SMALLINT` equivalent column: -->
`smallInteger` 메서드는 `SMALLINT`에 해당하는 컬럼을 생성합니다.

```
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
<!-- #### `softDeletesTz()` -->
#### `softDeletesTz()`

<!-- The `softDeletesTz` method adds a nullable `deleted_at` `TIMESTAMP` (with timezone) equivalent column with an optional precision (total digits). This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletesTz` 메서드는 nullable `deleted_at` `TIMESTAMP`(타임존 포함) 컬럼을 추가하며, 선택적으로 정밀도(총 자릿수)를 지정할 수 있습니다. 이 컬럼은 Eloquent의 "소프트 삭제" 기능에서 필요한 `deleted_at` 타임스탬프를 저장하는 데 사용됩니다.

```
$table->softDeletesTz($column = 'deleted_at', $precision = 0);
```

<a name="column-method-softDeletes"></a>
<!-- #### `softDeletes()` -->
#### `softDeletes()`

<!-- The `softDeletes` method adds a nullable `deleted_at` `TIMESTAMP` equivalent column with an optional precision (total digits). This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletes` 메서드는 nullable `deleted_at` `TIMESTAMP` 컬럼을 추가하며, 선택적으로 정밀도(총 자릿수)를 지정할 수 있습니다. 이 컬럼은 Eloquent의 "소프트 삭제" 기능에서 필요한 `deleted_at` 타임스탬프를 저장하는 데 사용됩니다.

```
$table->softDeletes($column = 'deleted_at', $precision = 0);
```

<a name="column-method-string"></a>
<!-- #### `string()` -->
#### `string()`

<!-- The `string` method creates a `VARCHAR` equivalent column of the given length: -->
`string` 메서드는 지정한 길이의 `VARCHAR` 컬럼을 생성합니다.

```
$table->string('name', 100);
```

<a name="column-method-text"></a>
<!-- #### `text()` -->
#### `text()`

<!-- The `text` method creates a `TEXT` equivalent column: -->
`text` 메서드는 `TEXT`에 해당하는 컬럼을 생성합니다.

```
$table->text('description');
```

<a name="column-method-timeTz"></a>
<!-- #### `timeTz()` -->
#### `timeTz()`

<!-- The `timeTz` method creates a `TIME` (with timezone) equivalent column with an optional precision (total digits): -->
`timeTz` 메서드는 타임존을 포함한 `TIME` 컬럼을 생성하며, 선택적으로 정밀도(총 자릿수)를 지정할 수 있습니다.

```
$table->timeTz('sunrise', $precision = 0);
```

<a name="column-method-time"></a>
<!-- #### `time()` -->
#### `time()`

<!-- The `time` method creates a `TIME` equivalent column with an optional precision (total digits): -->
`time` 메서드는 정밀도(총 자릿수)를 선택적으로 지정할 수 있는 `TIME` 컬럼을 생성합니다.

```
$table->time('sunrise', $precision = 0);
```

<a name="column-method-timestampTz"></a>
<!-- #### `timestampTz()` -->
#### `timestampTz()`

<!-- The `timestampTz` method creates a `TIMESTAMP` (with timezone) equivalent column with an optional precision (total digits): -->
`timestampTz` 메서드는 타임존을 포함한 `TIMESTAMP` 컬럼을 생성하며, 선택적으로 정밀도(총 자릿수)를 지정할 수 있습니다.

```
$table->timestampTz('added_at', $precision = 0);
```

<a name="column-method-timestamp"></a>
<!-- #### `timestamp()` -->
#### `timestamp()`

<!-- The `timestamp` method creates a `TIMESTAMP` equivalent column with an optional precision (total digits): -->
`timestamp` 메서드는 선택적으로 정밀도(총 자릿수)를 지정할 수 있는 `TIMESTAMP` 컬럼을 생성합니다.

```
$table->timestamp('added_at', $precision = 0);
```

<a name="column-method-timestampsTz"></a>
<!-- #### `timestampsTz()` -->
#### `timestampsTz()`

<!-- The `timestampsTz` method creates `created_at` and `updated_at` `TIMESTAMP` (with timezone) equivalent columns with an optional precision (total digits): -->
`timestampsTz` 메서드는 `created_at`과 `updated_at` 타임존이 포함된 `TIMESTAMP` 컬럼을 각각 생성하며, 선택적으로 정밀도(총 자릿수)를 지정할 수 있습니다.

```
$table->timestampsTz($precision = 0);
```

<a name="column-method-timestamps"></a>
<!-- #### `timestamps()` -->
#### `timestamps()`

<!-- The `timestamps` method creates `created_at` and `updated_at` `TIMESTAMP` equivalent columns with an optional precision (total digits): -->
`timestamps` 메서드는 `created_at`과 `updated_at`에 해당하는 `TIMESTAMP` 컬럼을 각각 생성하며, 선택적으로 정밀도(총 자릿수)를 지정할 수 있습니다.

```
$table->timestamps($precision = 0);
```

<a name="column-method-tinyIncrements"></a>
<!-- #### `tinyIncrements()` -->
#### `tinyIncrements()`

<!-- The `tinyIncrements` method creates an auto-incrementing `UNSIGNED TINYINT` equivalent column as a primary key: -->
`tinyIncrements` 메서드는 자동 증가하는 `UNSIGNED TINYINT`(기본키) 컬럼을 생성합니다.

```
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
<!-- #### `tinyInteger()` -->
#### `tinyInteger()`

<!-- The `tinyInteger` method creates a `TINYINT` equivalent column: -->
`tinyInteger` 메서드는 `TINYINT`에 해당하는 컬럼을 생성합니다.

```
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
<!-- #### `tinyText()` -->
#### `tinyText()`

<!-- The `tinyText` method creates a `TINYTEXT` equivalent column: -->
`tinyText` 메서드는 `TINYTEXT`에 해당하는 컬럼을 생성합니다.

```
$table->tinyText('notes');
```

<a name="column-method-unsignedBigInteger"></a>
<!-- #### `unsignedBigInteger()` -->
#### `unsignedBigInteger()`

<!-- The `unsignedBigInteger` method creates an `UNSIGNED BIGINT` equivalent column: -->
`unsignedBigInteger` 메서드는 `UNSIGNED BIGINT`에 해당하는 컬럼을 생성합니다.

```
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedDecimal"></a>
<!-- #### `unsignedDecimal()` -->
#### `unsignedDecimal()`

<!-- The `unsignedDecimal` method creates an `UNSIGNED DECIMAL` equivalent column with an optional precision (total digits) and scale (decimal digits): -->
`unsignedDecimal` 메서드는 선택적으로 정밀도(총 자릿수)와 소수점 자릿수(스케일)를 지정할 수 있는 `UNSIGNED DECIMAL` 컬럼을 생성합니다.

```
$table->unsignedDecimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-unsignedInteger"></a>
<!-- #### `unsignedInteger()` -->
#### `unsignedInteger()`

<!-- The `unsignedInteger` method creates an `UNSIGNED INTEGER` equivalent column: -->
`unsignedInteger` 메서드는 `UNSIGNED INTEGER`에 해당하는 컬럼을 생성합니다.

```
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
<!-- #### `unsignedMediumInteger()` -->
#### `unsignedMediumInteger()`

<!-- The `unsignedMediumInteger` method creates an `UNSIGNED MEDIUMINT` equivalent column: -->
`unsignedMediumInteger` 메서드는 `UNSIGNED MEDIUMINT`에 해당하는 컬럼을 생성합니다.

```
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
<!-- #### `unsignedSmallInteger()` -->
#### `unsignedSmallInteger()`

<!-- The `unsignedSmallInteger` method creates an `UNSIGNED SMALLINT` equivalent column: -->
`unsignedSmallInteger` 메서드는 `UNSIGNED SMALLINT`에 해당하는 컬럼을 생성합니다.

```
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
<!-- #### `unsignedTinyInteger()` -->
#### `unsignedTinyInteger()`

<!-- The `unsignedTinyInteger` method creates an `UNSIGNED TINYINT` equivalent column: -->
`unsignedTinyInteger` 메서드는 `UNSIGNED TINYINT`에 해당하는 컬럼을 생성합니다.

```
$table->unsignedTinyInteger('votes');
```

<a name="column-method-ulidMorphs"></a>
<!-- #### `ulidMorphs()` -->
#### `ulidMorphs()`

<!-- The `ulidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(26)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`ulidMorphs` 메서드는 `{column}_id` `CHAR(26)` 컬럼과 `{column}_type` `VARCHAR` 컬럼을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/9.x/eloquent-relationships) that use ULID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 메서드는 ULID 식별자를 사용하는 다형성 [Eloquent relationship](/docs/9.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용합니다. 아래 예시에서는 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다.

```
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
<!-- #### `uuidMorphs()` -->
#### `uuidMorphs()`

<!-- The `uuidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(36)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`uuidMorphs` 메서드는 `{column}_id` `CHAR(36)` 컬럼과 `{column}_type` `VARCHAR` 컬럼을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/9.x/eloquent-relationships) that use UUID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 메서드는 UUID 식별자를 사용하는 다형성 [Eloquent relationship](/docs/9.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용합니다. 아래 예시에서는 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다.

```
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
<!-- #### `ulid()` -->
#### `ulid()`

<!-- The `ulid` method creates a `ULID` equivalent column: -->
`ulid` 메서드는 `ULID`에 해당하는 컬럼을 생성합니다.

```
$table->ulid('id');
```

<a name="column-method-uuid"></a>
<!-- #### `uuid()` -->
#### `uuid()`

<!-- The `uuid` method creates a `UUID` equivalent column: -->
`uuid` 메서드는 `UUID`에 해당하는 컬럼을 생성합니다.

```
$table->uuid('id');
```

<a name="column-method-year"></a>
<!-- #### `year()` -->
#### `year()`

<!-- The `year` method creates a `YEAR` equivalent column: -->
`year` 메서드는 `YEAR`에 해당하는 컬럼을 생성합니다.

```
$table->year('birth_year');
```

<a name="column-modifiers"></a>
<!-- ### Column Modifiers -->
### Column Modifiers

<!-- In addition to the column types listed above, there are several column "modifiers" you may use when adding a column to a database table. For example, to make the column "nullable", you may use the `nullable` method: -->
위의 컬럼 타입 외에도, 데이터베이스 테이블에 컬럼을 추가할 때 사용할 수 있는 다양한 컬럼 "수정자"가 있습니다. 예를 들어, 컬럼을 "널 허용"으로 지정하고 싶을 때는 `nullable` 메서드를 사용할 수 있습니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

<!-- The following table contains all of the available column modifiers. This list does not include [index modifiers](#creating-indexes): -->
아래 표는 사용 가능한 모든 컬럼 수정자를 정리한 것입니다. 이 목록에는 [index modifiers](#creating-indexes)는 포함되지 않습니다.

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
수정자     |  설명
--------  |  -----------------------------------
`->after('column')`  |  다른 컬럼 "뒤"에 이 컬럼을 배치합니다 (MySQL).
`->autoIncrement()`  |  INTEGER 컬럼을 자동 증가(기본키)로 설정합니다.
`->charset('utf8mb4')`  |  이 컬럼의 문자셋을 지정합니다 (MySQL).
`->collation('utf8mb4_unicode_ci')`  |  이 컬럼의 정렬(collation)을 지정합니다 (MySQL/PostgreSQL/SQL Server).
`->comment('my comment')`  |  컬럼에 주석을 추가합니다 (MySQL/PostgreSQL).
`->default($value)`  |  이 컬럼의 "기본값"을 지정합니다.
`->first()`  |  테이블에서 해당 컬럼을 "첫 번째" 위치에 배치합니다 (MySQL).
`->from($integer)`  |  자동 증가 필드의 시작 값을 지정합니다 (MySQL / PostgreSQL).
`->invisible()`  |  이 컬럼을 `SELECT *` 쿼리에서 "숨김" 처리합니다 (MySQL).
`->nullable($value = true)`  |  컬럼 값에 NULL을 허용하도록 설정합니다.
`->storedAs($expression)`  |  생성 컬럼을 저장형(stored)으로 만듭니다 (MySQL / PostgreSQL).
`->unsigned()`  |  INTEGER 컬럼을 UNSIGNED로 설정합니다 (MySQL).
`->useCurrent()`  |  TIMESTAMP 컬럼의 기본값을 CURRENT_TIMESTAMP로 지정합니다.
`->useCurrentOnUpdate()`  |  레코드가 수정될 때 TIMESTAMP 컬럼의 값을 CURRENT_TIMESTAMP로 갱신합니다.
`->virtualAs($expression)`  |  생성 컬럼을 가상형(virtual)으로 만듭니다 (MySQL / PostgreSQL / SQLite).
`->generatedAs($expression)`  |  지정한 시퀀스 옵션으로 ID 컬럼을 생성합니다 (PostgreSQL).
`->always()`  |  ID 컬럼에 대해 시퀀스 값이 입력값보다 우선하도록 지정합니다 (PostgreSQL).
`->isGeometry()`  |  공간 컬럼 타입을 `geometry`로 지정합니다(기본값은 `geography`) (PostgreSQL).

<a name="default-expressions"></a>
<!-- #### Default Expressions -->
#### Default Expressions

<!-- The `default` modifier accepts a value or an `Illuminate\Database\Query\Expression` instance. Using an `Expression` instance will prevent Laravel from wrapping the value in quotes and allow you to use database specific functions. One situation where this is particularly useful is when you need to assign default values to JSON columns: -->
`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 사용할 경우, Laravel은 해당 값을 따옴표로 감싸지 않고 데이터베이스 고유의 함수를 사용할 수 있도록 처리합니다. 이 방식은 특히 JSON 컬럼에 기본값을 할당해야 할 때 유용합니다.

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
> 기본값 표현식 지원 여부는 사용 중인 데이터베이스 드라이버, 데이터베이스 버전, 그리고 필드 타입에 따라 다릅니다. 자세한 내용은 각 데이터베이스의 공식 문서를 참고하시기 바랍니다. 또한, 원시 `default` 표현식(`DB::raw` 사용)을 컬럼 변경과 동시에 `change` 메서드로 조합하는 것은 불가능합니다.

<a name="column-order"></a>

<!-- #### Column Order -->
#### Column Order

<!-- When using the MySQL database, the `after` method may be used to add columns after an existing column in the schema: -->
MySQL 데이터베이스를 사용할 때는 `after` 메서드를 이용하여 기존 컬럼 뒤에 새 컬럼을 추가할 수 있습니다.

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
컬럼을 수정하기 전에 Composer 패키지 매니저를 사용하여 `doctrine/dbal` 패키지를 설치해야 합니다. Doctrine DBAL 라이브러리는 컬럼의 현재 상태를 파악하고, 요청한 변경을 적용하기 위한 SQL 쿼리를 생성하는 데 사용됩니다.

```
composer require doctrine/dbal
```

<!-- If you plan to modify columns created using the `timestamp` method, you must also add the following configuration to your application's `config/database.php` configuration file: -->
`timestamp` 메서드를 사용해 생성한 컬럼을 수정할 계획이 있다면, 애플리케이션의 `config/database.php` 설정 파일에 다음 구성을 추가해야 합니다.

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> [!WARNING]
> 애플리케이션에서 Microsoft SQL Server를 사용하는 경우에는 반드시 `doctrine/dbal:^3.0`을 설치해야 합니다.

<a name="updating-column-attributes"></a>
<!-- #### Updating Column Attributes -->
#### Updating Column Attributes

<!-- The `change` method allows you to modify the type and attributes of existing columns. For example, you may wish to increase the size of a `string` column. To see the `change` method in action, let's increase the size of the `name` column from 25 to 50. To accomplish this, we simply define the new state of the column and then call the `change` method: -->
`change` 메서드를 사용하면 기존 컬럼의 타입과 속성을 변경할 수 있습니다. 예를 들어, `string` 컬럼의 길이를 늘리고 싶을 수 있습니다. `change` 메서드의 동작을 살펴보기 위해, `name` 컬럼의 크기를 25에서 50으로 늘려보겠습니다. 이를 위해서는 컬럼의 새 상태를 정의한 뒤, `change` 메서드를 호출하면 됩니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

<!-- We could also modify a column to be nullable: -->
또한, 컬럼을 nullable로 변경할 수도 있습니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->nullable()->change();
});
```

> [!WARNING]
> 아래와 같은 컬럼 타입만 변경이 가능합니다: `bigInteger`, `binary`, `boolean`, `char`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `double`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `tinyText`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `uuid`. `timestamp` 타입 컬럼은 [Doctrine type must be registered](#prerequisites)이 필요합니다.

<a name="renaming-columns"></a>
<!-- ### Renaming Columns -->
### Renaming Columns

<!-- To rename a column, you may use the `renameColumn` method provided by the schema builder: -->
컬럼의 이름을 바꾸려면 스키마 빌더의 `renameColumn` 메서드를 사용할 수 있습니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="renaming-columns-on-legacy-databases"></a>
<!-- #### Renaming Columns On Legacy Databases -->
#### Renaming Columns On Legacy Databases

<!-- If you are running a database installation older than one of the following releases, you should ensure that you have installed the `doctrine/dbal` library via the Composer package manager before renaming a column: -->
아래 버전보다 오래된 데이터베이스를 사용하고 있다면, 컬럼 이름을 변경하기 전에 반드시 Composer 패키지 매니저를 통해 `doctrine/dbal` 라이브러리를 설치해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- MySQL < `8.0.3`
- MariaDB < `10.5.2`
- SQLite < `3.25.0`
-->
- MySQL < `8.0.3`
- MariaDB < `10.5.2`
- SQLite < `3.25.0`

<!-- </div> -->
</div>

<a name="dropping-columns"></a>
<!-- ### Dropping Columns -->
### Dropping Columns

<!-- To drop a column, you may use the `dropColumn` method on the schema builder: -->
컬럼을 삭제하려면, 스키마 빌더의 `dropColumn` 메서드를 사용하면 됩니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

<!-- You may drop multiple columns from a table by passing an array of column names to the `dropColumn` method: -->
`dropColumn` 메서드에 컬럼명 배열을 인자로 전달하여 테이블에서 여러 컬럼을 한 번에 삭제할 수도 있습니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="dropping-columns-on-legacy-databases"></a>
<!-- #### Dropping Columns On Legacy Databases -->
#### Dropping Columns On Legacy Databases

<!-- If you are running a version of SQLite prior to `3.35.0`, you must install the `doctrine/dbal` package via the Composer package manager before the `dropColumn` method may be used. Dropping or modifying multiple columns within a single migration while using this package is not supported. -->
SQLite `3.35.0` 버전 이전을 사용하고 있는 경우, `dropColumn` 메서드를 사용하기 전에 Composer 패키지 매니저로 `doctrine/dbal` 패키지를 반드시 설치해야 합니다. 또한, 이 패키지 사용 시 하나의 마이그레이션에서 여러 컬럼을 삭제하거나 수정하는 것은 지원되지 않습니다.

<a name="available-command-aliases"></a>
<!-- #### Available Command Aliases -->
#### Available Command Aliases

<!-- Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below: -->
Laravel에서는 자주 사용되는 타입의 컬럼을 삭제할 때 쓸 수 있는 여러 편리한 별칭 메서드를 제공합니다. 각 메서드는 아래 표와 같습니다.

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
`$table->dropSoftDeletesTz();`  |  `dropSoftDeletes()` 메서드의 별칭입니다.
`$table->dropTimestamps();`  |  `created_at`와 `updated_at` 컬럼을 삭제합니다.
`$table->dropTimestampsTz();` |  `dropTimestamps()` 메서드의 별칭입니다.

<a name="indexes"></a>
<!-- ## Indexes -->
## Indexes

<a name="creating-indexes"></a>
<!-- ### Creating Indexes -->
### Creating Indexes

<!-- The Laravel schema builder supports several types of indexes. The following example creates a new `email` column and specifies that its values should be unique. To create the index, we can chain the `unique` method onto the column definition: -->
Laravel의 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 아래 예제에서는 새 `email` 컬럼을 만들고, 해당 컬럼 값이 유일하도록 지정합니다. 인덱스를 생성하려면, 컬럼 정의에 `unique` 메서드를 체이닝하면 됩니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

<!-- Alternatively, you may create the index after defining the column. To do so, you should call the `unique` method on the schema builder blueprint. This method accepts the name of the column that should receive a unique index: -->
또는, 컬럼을 정의한 후에 인덱스를 따로 생성할 수 있습니다. 이때는 스키마 빌더 Blueprint에서 `unique` 메서드를 호출하며, 인덱스를 생성할 컬럼의 이름을 전달합니다.

```
$table->unique('email');
```

<!-- You may even pass an array of columns to an index method to create a compound (or composite) index: -->
복수 컬럼에 대해 복합(혹은 조합) 인덱스를 만들 때는, 인덱스 메서드에 컬럼명 배열을 전달하면 됩니다.

```
$table->index(['account_id', 'created_at']);
```

<!-- When creating an index, Laravel will automatically generate an index name based on the table, column names, and the index type, but you may pass a second argument to the method to specify the index name yourself: -->
인덱스를 생성할 때 Laravel은 기본적으로 테이블명, 컬럼명, 인덱스 타입을 기반으로 인덱스 이름을 자동 생성합니다. 직접 인덱스 이름을 지정하고 싶다면, 메서드의 두 번째 인자로 이름을 전달할 수 있습니다.

```
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
<!-- #### Available Index Types -->
#### Available Index Types

<!-- Laravel's schema builder blueprint class provides methods for creating each type of index supported by Laravel. Each index method accepts an optional second argument to specify the name of the index. If omitted, the name will be derived from the names of the table and column(s) used for the index, as well as the index type. Each of the available index methods is described in the table below: -->
Laravel의 스키마 빌더 Blueprint 클래스에서는 Laravel에서 지원하는 각 인덱스 타입별로 메서드를 제공합니다. 각 인덱스 메서드는 두 번째 인자로 인덱스 이름을 지정할 수 있으며, 생략하면 기본적으로 테이블명, 컬럼명, 인덱스 타입을 조합하여 이름이 만들어집니다. 아래 표는 지원되는 인덱스 메서드입니다.

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
명령어  |  설명
-------  |  -----------
`$table->primary('id');`  |  기본키(primary key)를 추가합니다.
`$table->primary(['id', 'parent_id']);`  |  복합 키(composite key)를 추가합니다.
`$table->unique('email');`  |  유니크 인덱스를 추가합니다.
`$table->index('state');`  |  일반 인덱스를 추가합니다.
`$table->fullText('body');`  |  전문(Full text) 인덱스를 추가합니다 (MySQL/PostgreSQL).
`$table->fullText('body')->language('english');`  |  특정 언어로 전문 인덱스를 추가합니다 (PostgreSQL).
`$table->spatialIndex('location');`  |  공간(Spatial) 인덱스를 추가합니다 (SQLite 제외).

<a name="index-lengths-mysql-mariadb"></a>
<!-- #### Index Lengths & MySQL / MariaDB -->
#### Index Lengths & MySQL / MariaDB

<!-- By default, Laravel uses the `utf8mb4` character set. If you are running a version of MySQL older than the 5.7.7 release or MariaDB older than the 10.2.2 release, you may need to manually configure the default string length generated by migrations in order for MySQL to create indexes for them. You may configure the default string length by calling the `Schema::defaultStringLength` method within the `boot` method of your `App\Providers\AppServiceProvider` class: -->
기본적으로 Laravel은 `utf8mb4` 문자셋을 사용합니다. 만약 MySQL 5.7.7 미만이나 MariaDB 10.2.2 미만 버전을 사용한다면, 인덱스 생성을 위해 마이그레이션에서 생성되는 기본 문자열 길이를 수동으로 지정해야 할 수 있습니다. 이때는 `App\Providers\AppServiceProvider`의 `boot` 메서드 내에서 `Schema::defaultStringLength` 메서드를 호출하여 기본 문자열 길이를 지정할 수 있습니다.

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
또는, 데이터베이스의 `innodb_large_prefix` 옵션을 활성화해도 됩니다. 관련 설정은 사용 중인 데이터베이스의 공식 문서를 참고해 주세요.

<a name="renaming-indexes"></a>
<!-- ### Renaming Indexes -->
### Renaming Indexes

<!-- To rename an index, you may use the `renameIndex` method provided by the schema builder blueprint. This method accepts the current index name as its first argument and the desired name as its second argument: -->
인덱스의 이름을 변경하려면 스키마 빌더 Blueprint에서 제공하는 `renameIndex` 메서드를 사용할 수 있습니다. 첫 번째 인수로 현재 인덱스 이름, 두 번째 인수로 변경할 이름을 전달합니다.

```
$table->renameIndex('from', 'to')
```

> [!WARNING]
> SQLite 데이터베이스를 사용할 경우, `renameIndex` 메서드를 사용하기 전에 Composer 패키지 매니저로 `doctrine/dbal` 패키지를 반드시 설치해야 합니다.

<a name="dropping-indexes"></a>
<!-- ### Dropping Indexes -->
### Dropping Indexes

<!-- To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples: -->
인덱스를 삭제하려면 삭제할 인덱스의 이름을 지정해야 합니다. 기본적으로 Laravel은 테이블명, 컬럼명, 인덱스 타입을 조합해 인덱스 이름을 자동 부여합니다. 다음은 몇 가지 예시입니다.

<!--
Command  |  Description
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  Drop a primary key from the "users" table.
`$table->dropUnique('users_email_unique');`  |  Drop a unique index from the "users" table.
`$table->dropIndex('geo_state_index');`  |  Drop a basic index from the "geo" table.
`$table->dropFullText('posts_body_fulltext');`  |  Drop a full text index from the "posts" table.
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  Drop a spatial index from the "geo" table  (except SQLite).
-->
명령어  |  설명
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  "users" 테이블에서 기본키를 삭제합니다.
`$table->dropUnique('users_email_unique');`  |  "users" 테이블에서 유니크 인덱스를 삭제합니다.
`$table->dropIndex('geo_state_index');`  |  "geo" 테이블에서 일반 인덱스를 삭제합니다.
`$table->dropFullText('posts_body_fulltext');`  |  "posts" 테이블에서 전문 인덱스를 삭제합니다.
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  "geo" 테이블에서 공간 인덱스를 삭제합니다 (SQLite 제외).

<!-- If you pass an array of columns into a method that drops indexes, the conventional index name will be generated based on the table name, columns, and index type: -->
여러 컬럼을 인자로 전달해 인덱스를 삭제할 경우, 일반 인덱스 이름 생성 규칙에 따라 이름이 자동 조합되어 삭제됩니다.

```
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a name="foreign-key-constraints"></a>
<!-- ### Foreign Key Constraints -->
### Foreign Key Constraints

<!-- Laravel also provides support for creating foreign key constraints, which are used to force referential integrity at the database level. For example, let's define a `user_id` column on the `posts` table that references the `id` column on a `users` table: -->
Laravel은 데이터베이스 레벨에서 참조 무결성을 보장하는 외래 키 제약 조건 생성도 지원합니다. 예를 들어, `posts` 테이블에 `users` 테이블의 `id` 컬럼을 참조하는 `user_id` 컬럼을 추가하려면 다음과 같이 작성합니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

<!-- Since this syntax is rather verbose, Laravel provides additional, terser methods that use conventions to provide a better developer experience. When using the `foreignId` method to create your column, the example above can be rewritten like so: -->
이 문법이 다소 장황할 수 있어, Laravel은 더 짧고 관습적인 방법을 제공합니다. `foreignId` 메서드를 사용하면 위 코드를 아래와 같이 간결하게 만들 수 있습니다.

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column, while the `constrained` method will use conventions to determine the table and column name being referenced. If your table name does not match Laravel's conventions, you may specify the table name by passing it as an argument to the `constrained` method: -->
`foreignId` 메서드는 `UNSIGNED BIGINT` 타입과 동일한 컬럼을 생성하며, `constrained` 메서드는 관습에 따라 참조할 테이블과 컬럼 이름을 자동으로 결정합니다. 테이블 이름이 Laravel의 관습과 다르다면, `constrained` 메서드에 참조할 테이블명을 인자로 전달할 수 있습니다.

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained('users');
});
```

<!-- You may also specify the desired action for the "on delete" and "on update" properties of the constraint: -->
또한, 외래 키의 "on delete"와 "on update" 속성에 원하는 동작을 지정할 수도 있습니다.

```
$table->foreignId('user_id')
      ->constrained()
      ->onUpdate('cascade')
      ->onDelete('cascade');
```

<!-- An alternative, expressive syntax is also provided for these actions: -->
이 동작을 위한 좀 더 표현적인 메서드들도 제공됩니다.

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
`$table->cascadeOnUpdate();` | 업데이트 시 참조 행도 함께 변경됩니다.
`$table->restrictOnUpdate();`| 업데이트가 제한됩니다.
`$table->cascadeOnDelete();` | 삭제 시 참조 행도 함께 삭제됩니다.
`$table->restrictOnDelete();`| 삭제가 제한됩니다.
`$table->nullOnDelete();`    | 삭제 시 외래 키 값을 null로 설정합니다.

<!-- Any additional [column modifiers](#column-modifiers) must be called before the `constrained` method: -->
[column modifiers](#column-modifiers)와 관련된 추가 메서드는 반드시 `constrained` 메서드 이전에 호출해야 합니다.

```
$table->foreignId('user_id')
      ->nullable()
      ->constrained();
```

<a name="dropping-foreign-keys"></a>
<!-- #### Dropping Foreign Keys -->
#### Dropping Foreign Keys

<!-- To drop a foreign key, you may use the `dropForeign` method, passing the name of the foreign key constraint to be deleted as an argument. Foreign key constraints use the same naming convention as indexes. In other words, the foreign key constraint name is based on the name of the table and the columns in the constraint, followed by a "\_foreign" suffix: -->
외래 키를 삭제할 때는 `dropForeign` 메서드를 사용하며, 삭제할 외래 키 제약 조건의 이름을 인자로 전달합니다. 외래 키 제약 조건의 이름은 인덱스의 명명 규칙과 동일하게, 테이블 이름과 컬럼명, 마지막에 "\_foreign"이 붙는 방식입니다.

```
$table->dropForeign('posts_user_id_foreign');
```

<!-- Alternatively, you may pass an array containing the column name that holds the foreign key to the `dropForeign` method. The array will be converted to a foreign key constraint name using Laravel's constraint naming conventions: -->
또 다른 방법으로, 외래 키가 걸려 있는 컬럼명을 배열로 `dropForeign`에 전달해도 됩니다. 배열은 Laravel의 제약 조건 네이밍 규칙에 따라 외래 키 제약 조건 이름으로 변환됩니다.

```
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
<!-- #### Toggling Foreign Key Constraints -->
#### Toggling Foreign Key Constraints

<!-- You may enable or disable foreign key constraints within your migrations by using the following methods: -->
마이그레이션 내에서 아래 메서드를 사용해 외래 키 제약 조건을 활성화하거나 비활성화할 수 있습니다.

```
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약 조건이 비활성화되어 있습니다. SQLite를 사용할 때는 마이그레이션에서 외래 키를 생성하기 전 데이터베이스 설정에서 [enable foreign key support](/docs/9.x/database#configuration)해야 합니다. 또한, SQLite는 테이블 생성시에만 외래 키를 지원하며 [not when tables are altered](https://www.sqlite.org/omitted.html).

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- For convenience, each migration operation will dispatch an [event](/docs/9.x/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class: -->
편의를 위해 각 마이그레이션 동작은 [event](/docs/9.x/events)를 발생시킵니다. 다음 모든 이벤트는 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 확장합니다.

<!--
 Class | Description
-------|-------
-->
 클래스 | 설명
-------|-------
| `Illuminate\Database\Events\MigrationsStarted` | 마이그레이션 일괄 작업이 곧 실행될 예정입니다. |
| `Illuminate\Database\Events\MigrationsEnded` | 마이그레이션 일괄 작업이 실행을 마쳤습니다. |
| `Illuminate\Database\Events\MigrationStarted` | 단일 마이그레이션이 곧 실행될 예정입니다. |
| `Illuminate\Database\Events\MigrationEnded` | 단일 마이그레이션이 실행을 마쳤습니다. |
| `Illuminate\Database\Events\SchemaDumped` | 데이터베이스 스키마 덤프가 완료되었습니다. |
| `Illuminate\Database\Events\SchemaLoaded` | 기존 데이터베이스 스키마 덤프를 로드했습니다. |
