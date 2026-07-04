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
마이그레이션은 데이터베이스의 버전 제어와 유사하므로 팀이 애플리케이션의 데이터베이스 스키마 정의를 정의하고 공유할 수 있습니다. 소스 제어에서 변경 사항을 가져온 후 팀 동료에게 로컬 데이터베이스 스키마에 열을 수동으로 추가하라고 지시해야 한다면 데이터베이스 마이그레이션이 해결하는 문제에 직면한 것입니다.

<!-- The Laravel `Schema` [facade](/docs/master/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns. -->
Laravel `Schema` [facade](/docs/master/facades)는 Laravel가 지원하는 모든 데이터베이스 시스템에서 테이블을 생성하고 조작하기 위한 데이터베이스 독립적 지원을 제공합니다. 일반적으로 마이그레이션은 이 외관을 사용하여 데이터베이스 테이블과 열을 생성하고 수정합니다.

<a name="generating-migrations"></a>
<!-- ## Generating Migrations -->
## Generating Migrations

<!-- You may use the `make:migration` [Artisan command](/docs/master/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations: -->
`make:migration` [Artisan command](/docs/master/artisan)을 사용하여 데이터베이스 마이그레이션을 생성할 수 있습니다. 새로운 마이그레이션은 `database/migrations` 디렉토리에 배치됩니다. 각 마이그레이션 파일 이름에는 Laravel가 마이그레이션의 순서를 결정할 수 있도록 하는 타임스탬프가 포함되어 있습니다.

```shell
php artisan make:migration create_flights_table
```

<!-- Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually. -->
Laravel는 마이그레이션의 이름을 사용하여 테이블 이름과 마이그레이션이 새 테이블을 생성할지 여부를 추측합니다. Laravel가 마이그레이션 이름에서 테이블 이름을 확인할 수 있는 경우 Laravel는 생성된 마이그레이션 파일을 지정된 테이블로 미리 채웁니다. 그렇지 않으면 마이그레이션 파일에 테이블을 수동으로 지정할 수도 있습니다.

<!-- If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path. -->
생성된 마이그레이션에 대한 사용자 지정 경로를 지정하려면 `make:migration` 명령을 실행할 때 `--path` 옵션을 사용할 수 있습니다. 지정된 경로는 애플리케이션의 기본 경로에 상대적이어야 합니다.

> [!NOTE]
> 마이그레이션 스텁은 [stub publishing](/docs/master/artisan#stub-customization)를 사용하여 사용자 지정할 수 있습니다.

<a name="squashing-migrations"></a>
<!-- ### Squashing Migrations -->
### Squashing Migrations

<!-- As you build your application, you may accumulate more and more migrations over time. This can lead to your `database/migrations` directory becoming bloated with potentially hundreds of migrations. If you would like, you may "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command: -->
애플리케이션을 구축하면 시간이 지남에 따라 점점 더 많은 마이그레이션이 축적될 수 있습니다. 이로 인해 `database/migrations` 디렉토리가 잠재적으로 수백 개의 마이그레이션로 인해 부풀어오르게 될 수 있습니다. 원하는 경우 마이그레이션을 단일 SQL 파일로 "스쿼시"할 수 있습니다. 시작하려면 `schema:dump` 명령을 실행하십시오.

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

<!-- When you execute this command, Laravel will write a "schema" file to your application's `database/schema` directory. The schema file's name will correspond to the database connection. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will first execute the SQL statements in the schema file of the database connection you are using. After executing the schema file's SQL statements, Laravel will execute any remaining migrations that were not part of the schema dump. -->
이 명령을 실행하면 Laravel는 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 작성합니다. 스키마 파일의 이름은 데이터베이스 연결에 해당합니다. 이제 데이터베이스 마이그레이션을 시도하고 다른 마이그레이션이 실행되지 않은 경우 Laravel는 먼저 사용 중인 데이터베이스 연결의 스키마 파일에 있는 SQL 문을 실행합니다. 스키마 파일의 SQL 문을 실행한 후 Laravel는 스키마 덤프의 일부가 아닌 나머지 마이그레이션을 실행합니다.

<!-- If your application's tests use a different database connection than the one you typically use during local development, you should ensure you have dumped a schema file using that database connection so that your tests are able to build your database. You may wish to do this after dumping the database connection you typically use during local development: -->
애플리케이션의 테스트에서 로컬 개발 중에 일반적으로 사용하는 것과 다른 데이터베이스 연결을 사용하는 경우 테스트에서 데이터베이스를 구축할 수 있도록 해당 데이터베이스 연결을 사용하여 스키마 파일을 덤프했는지 확인해야 합니다. 로컬 개발 중에 일반적으로 사용하는 데이터베이스 연결을 덤프한 후 이 작업을 수행할 수 있습니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

<!-- You should commit your database schema file to source control so that other new developers on your team may quickly create your application's initial database structure. -->
팀의 다른 새로운 개발자가 애플리케이션의 초기 데이터베이스 구조를 신속하게 생성할 수 있도록 데이터베이스 스키마 파일을 소스 제어에 커밋해야 합니다.

> [!WARNING]
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL 및 SQLite 데이터베이스에만 사용할 수 있으며 데이터베이스의 명령줄 클라이언트를 활용합니다.

<a name="migration-structure"></a>
<!-- ## Migration Structure -->
## Migration Structure

<!-- A migration class contains two methods: `up` and `down`. The `up` method is used to add new tables, columns, or indexes to your database, while the `down` method should reverse the operations performed by the `up` method. -->
마이그레이션 클래스에는 `up` 및 `down`라는 두 가지 메서드가 포함되어 있습니다. `up` 방법은 데이터베이스에 새 테이블, 열 또는 인덱스를 추가하는 데 사용되는 반면, `down` 방법은 `up` 방법으로 수행된 작업을 반대로 해야 합니다.

<!-- Within both of these methods, you may use the Laravel schema builder to expressively create and modify tables. To learn about all of the methods available on the `Schema` builder, [check out its documentation](#creating-tables). For example, the following migration creates a `flights` table: -->
이 두 가지 방법 모두에서 Laravel 스키마 빌더를 사용하여 테이블을 명시적으로 생성하고 수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 방법에 대해 알아보려면 [check out its documentation](#creating-tables)하세요. 예를 들어, 다음 마이그레이션은 `flights` 테이블을 생성합니다.

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
<!-- #### Setting the Migration Connection -->
#### Setting the Migration Connection

<!-- If your migration will be interacting with a database connection other than your application's default database connection, you should set the `$connection` property of your migration: -->
마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 데이터베이스 연결과 상호 작용하는 경우 마이그레이션의 `$connection` 속성을 설정해야 합니다.

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
<!-- #### Skipping Migrations -->
#### Skipping Migrations

<!-- Sometimes a migration might be meant to support a feature that is not yet active and you do not want it to run yet. In this case you may define a `shouldRun` method on the migration. If the `shouldRun` method returns `false`, the migration will be skipped: -->
때로는 마이그레이션이 아직 활성화되지 않은 기능을 지원하고 아직 실행되기를 원하지 않을 수도 있습니다. 이 경우 마이그레이션에 `shouldRun` 메서드를 정의할 수 있습니다. `shouldRun` 메서드가 `false`를 반환하는 경우 마이그레이션은 건너뜁니다.

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
<!-- ## Running Migrations -->
## Running Migrations

<!-- To run all of your outstanding migrations, execute the `migrate` Artisan command: -->
미해결 마이그레이션을 모두 실행하려면 `migrate` Artisan 명령을 실행하세요.

```shell
php artisan migrate
```

<!-- If you would like to see which migrations have already run and which are still pending, you may use the `migrate:status` Artisan command: -->
이미 실행된 마이그레이션와 아직 보류 중인 마이그레이션을 확인하려면 `migrate:status` Artisan 명령을 사용할 수 있습니다.

```shell
php artisan migrate:status
```

<!-- If you provide the `--step` option to the `migrate` command, the command will run each migration as its own batch, allowing you to roll back individual migrations later using the `migrate:rollback` command: -->
`--step` 옵션을 `migrate` 명령에 제공하면 명령은 각 마이그레이션을 자체 배치로 실행하므로 나중에 `migrate:rollback` 명령을 사용하여 개별 마이그레이션을 롤백할 수 있습니다.

```shell
php artisan migrate --step
```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate` command: -->
실제로 실행하지 않고 마이그레이션에 의해 실행될 SQL 문을 보려면 `migrate` 명령에 `--pretend` 플래그를 제공할 수 있습니다.

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
<!-- #### Isolating Migration Execution -->
#### Isolating Migration Execution

<!-- If you are deploying your application across multiple servers and running migrations as part of your deployment process, you likely do not want two servers attempting to migrate the database at the same time. To avoid this, you may use the `isolated` option when invoking the `migrate` command. -->
여러 서버에 애플리케이션을 배포하고 배포 프로세스의 일부로 마이그레이션을 실행하는 경우 두 서버가 동시에 데이터베이스 마이그레이션을 시도하는 것을 원하지 않을 것입니다. 이를 방지하려면 `migrate` 명령을 호출할 때 `isolated` 옵션을 사용할 수 있습니다.

<!-- When the `isolated` option is provided, Laravel will acquire an atomic lock using your application's cache driver before attempting to run your migrations. All other attempts to run the `migrate` command while that lock is held will not execute; however, the command will still exit with a successful exit status code: -->
`isolated` 옵션이 제공되면 Laravel는 마이그레이션 실행을 시도하기 전에 애플리케이션의 캐시 드라이버를 사용하여 원자 잠금을 획득합니다. 해당 잠금이 유지되는 동안 `migrate` 명령을 실행하려는 다른 모든 시도는 실행되지 않습니다. 그러나 명령은 성공적인 종료 상태 코드로 종료됩니다.

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 활용하려면 애플리케이션에서 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 캐시 드라이버를 애플리케이션의 기본 캐시 드라이버로 사용해야 합니다. 또한 모든 서버는 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
<!-- #### Forcing Migrations to Run in Production -->
#### Forcing Migrations to Run in Production

<!-- Some migration operations are destructive, which means they may cause you to lose data. In order to protect you from running these commands against your production database, you will be prompted for confirmation before the commands are executed. To force the commands to run without a prompt, use the `--force` flag: -->
일부 마이그레이션 작업은 파괴적이므로 데이터가 손실될 수 있습니다. 프로덕션 데이터베이스에 대해 이러한 명령을 실행하지 못하도록 보호하기 위해 명령이 실행되기 전에 확인 메시지가 표시됩니다. 프롬프트 없이 명령을 강제로 실행하려면 `--force` 플래그를 사용하십시오.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
<!-- ### Rolling Back Migrations -->
### Rolling Back Migrations

<!-- To roll back the latest migration operation, you may use the `rollback` Artisan command. This command rolls back the last "batch" of migrations, which may include multiple migration files: -->
최신 마이그레이션 작업을 롤백하려면 `rollback` Artisan 명령을 사용할 수 있습니다. 이 명령은 여러 마이그레이션 파일을 포함할 수 있는 마이그레이션의 마지막 "배치"를 롤백합니다.

```shell
php artisan migrate:rollback
```

<!-- You may roll back a limited number of migrations by providing the `step` option to the `rollback` command. For example, the following command will roll back the last five migrations: -->
`rollback` 명령에 `step` 옵션을 제공하여 제한된 수의 마이그레이션을 롤백할 수 있습니다. 예를 들어 다음 명령은 마지막 5개의 마이그레이션을 롤백합니다.

```shell
php artisan migrate:rollback --step=5
```

<!-- You may roll back a specific "batch" of migrations by providing the `batch` option to the `rollback` command, where the `batch` option corresponds to a batch value within your application's `migrations` database table. For example, the following command will roll back all migrations in batch three: -->
`batch` 옵션을 `rollback` 명령에 제공하여 마이그레이션의 특정 "배치"를 롤백할 수 있습니다. 여기서 `batch` 옵션은 응용 프로그램의 `migrations` 데이터베이스 테이블 내의 배치 값에 해당합니다. 예를 들어 다음 명령은 배치 3개의 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:rollback --batch=3
```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate:rollback` command: -->
실제로 실행하지 않고 마이그레이션에 의해 실행될 SQL 문을 보려면 `migrate:rollback` 명령에 `--pretend` 플래그를 제공할 수 있습니다.

```shell
php artisan migrate:rollback --pretend
```

<!-- The `migrate:reset` command will roll back all of your application's migrations: -->
`migrate:reset` 명령은 애플리케이션의 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
<!-- #### Roll Back and Migrate Using a Single Command -->
#### Roll Back and Migrate Using a Single Command

<!-- The `migrate:refresh` command will roll back all of your migrations and then execute the `migrate` command. This command effectively re-creates your entire database: -->
`migrate:refresh` 명령은 모든 마이그레이션을 롤백한 다음 `migrate` 명령을 실행합니다. 이 명령은 전체 데이터베이스를 효과적으로 다시 생성합니다.

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

<!-- You may roll back and re-migrate a limited number of migrations by providing the `step` option to the `refresh` command. For example, the following command will roll back and re-migrate the last five migrations: -->
`refresh` 명령에 `step` 옵션을 제공하여 제한된 수의 마이그레이션을 롤백하고 다시 마이그레이션할 수 있습니다. 예를 들어 다음 명령은 마지막 5개의 마이그레이션을 롤백하고 다시 마이그레이션합니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
<!-- #### Drop All Tables and Migrate -->
#### Drop All Tables and Migrate

<!-- The `migrate:fresh` command will drop all tables from the database and then execute the `migrate` command: -->
`migrate:fresh` 명령은 데이터베이스에서 모든 테이블을 삭제한 다음 `migrate` 명령을 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

<!-- By default, the `migrate:fresh` command only drops tables from the default database connection. However, you may use the `--database` option to specify the database connection that should be migrated. The database connection name should correspond to a connection defined in your application's `database` [configuration file](/docs/master/configuration): -->
기본적으로 `migrate:fresh` 명령은 기본 데이터베이스 연결에서만 테이블을 삭제합니다. 그러나 `--database` 옵션을 사용하여 마이그레이션해야 하는 데이터베이스 연결을 지정할 수 있습니다. 데이터베이스 연결 이름은 애플리케이션의 `database` [configuration file](/docs/master/configuration)에 정의된 연결과 일치해야 합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령은 접두사에 관계없이 모든 데이터베이스 테이블을 삭제합니다. 이 명령은 다른 애플리케이션과 공유되는 데이터베이스에서 개발할 때 주의해서 사용해야 합니다.

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<a name="creating-tables"></a>
<!-- ### Creating Tables -->
### Creating Tables

<!-- To create a new database table, use the `create` method on the `Schema` facade. The `create` method accepts two arguments: the first is the name of the table, while the second is a closure which receives a `Blueprint` object that may be used to define the new table: -->
새 데이터베이스 테이블을 생성하려면 `Schema` 파사드에서 `create` 메소드를 사용하세요. `create` 메소드는 두 개의 인수를 허용합니다: 첫 번째는 테이블의 이름이고, 두 번째는 새 테이블을 정의하는 데 사용할 수 있는 `Blueprint` 객체를 받는 클로저입니다.

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

<!-- When creating the table, you may use any of the schema builder's [column methods](#creating-columns) to define the table's columns. -->
테이블을 생성할 때 스키마 빌더의 [column methods](#creating-columns) 중 하나를 사용하여 테이블의 열을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
<!-- #### Determining Table / Column Existence -->
#### Determining Table / Column Existence

<!-- You may determine the existence of a table, column, or index using the `hasTable`, `hasColumn`, and `hasIndex` methods: -->
`hasTable`, `hasColumn` 및 `hasIndex` 메서드를 사용하여 테이블, 열 또는 인덱스의 존재를 확인할 수 있습니다.

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
<!-- #### Database Connection and Table Options -->
#### Database Connection and Table Options

<!-- If you want to perform a schema operation on a database connection that is not your application's default connection, use the `connection` method: -->
애플리케이션의 기본 연결이 아닌 데이터베이스 연결에서 스키마 작업을 수행하려면 `connection` 메서드를 사용하세요.

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

<!-- In addition, a few other properties and methods may be used to define other aspects of the table's creation. The `engine` property may be used to specify the table's storage engine when using MariaDB or MySQL: -->
또한 몇 가지 다른 속성과 메서드를 사용하여 테이블 생성의 다른 측면을 정의할 수 있습니다. MariaDB 또는 MySQL을 사용할 때 `engine` 속성을 사용하여 테이블의 스토리지 엔진을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

<!-- The `charset` and `collation` properties may be used to specify the character set and collation for the created table when using MariaDB or MySQL: -->
`charset` 및 `collation` 속성은 MariaDB 또는 MySQL을 사용할 때 생성된 테이블에 대한 문자 집합 및 데이터 정렬을 지정하는 데 사용할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

<!-- The `temporary` method may be used to indicate that the table should be "temporary". Temporary tables are only visible to the current connection's database session and are dropped automatically when the connection is closed: -->
`temporary` 메소드는 테이블이 "임시"여야 함을 나타내는 데 사용될 수 있습니다. 임시 테이블은 현재 연결의 데이터베이스 세션에만 표시되며 연결이 닫히면 자동으로 삭제됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

<!-- If you would like to add a "comment" to a database table, you may invoke the `comment` method on the table instance. Table comments are currently only supported by MariaDB, MySQL, and PostgreSQL: -->
데이터베이스 테이블에 "주석"을 추가하려면 테이블 인스턴스에서 `comment` 메소드를 호출하면 됩니다. 테이블 주석은 현재 MariaDB, MySQL 및 PostgreSQL에서만 지원됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```

<a name="updating-tables"></a>
<!-- ### Updating Tables -->
### Updating Tables

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives a `Blueprint` instance you may use to add columns or indexes to the table: -->
`Schema` 파사드의 `table` 메소드는 기존 테이블을 업데이트하는 데 사용될 수 있습니다. `create` 메소드와 마찬가지로 `table` 메소드는 테이블 이름과 테이블에 열이나 인덱스를 추가하는 데 사용할 수 있는 `Blueprint` 인스턴스를 수신하는 클로저라는 두 가지 인수를 허용합니다.

```php
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
기존 데이터베이스 테이블의 이름을 바꾸려면 `rename` 메소드를 사용하십시오.

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

<!-- To drop an existing table, you may use the `drop` or `dropIfExists` methods: -->
기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메소드를 사용할 수 있습니다.

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
<!-- #### Renaming Tables With Foreign Keys -->
#### Renaming Tables With Foreign Keys

<!-- Before renaming a table, you should verify that any foreign key constraints on the table have an explicit name in your migration files instead of letting Laravel assign a convention based name. Otherwise, the foreign key constraint name will refer to the old table name. -->
테이블 이름을 바꾸기 전에 Laravel가 규칙 기반 이름을 할당하도록 하는 대신 테이블의 외래 키 제약 조건에 마이그레이션 파일에 명시적인 이름이 있는지 확인해야 합니다. 그렇지 않으면 외래 키 제약 조건 이름이 이전 테이블 이름을 참조합니다.

<a name="columns"></a>
<!-- ## Columns -->
## Columns

<a name="creating-columns"></a>
<!-- ### Creating Columns -->
### Creating Columns

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives an `Illuminate\Database\Schema\Blueprint` instance you may use to add columns to the table: -->
`Schema` 파사드의 `table` 메소드는 기존 테이블을 업데이트하는 데 사용될 수 있습니다. `create` 메서드와 마찬가지로 `table` 메서드는 테이블 이름과 테이블에 열을 추가하는 데 사용할 수 있는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 수신하는 클로저라는 두 가지 인수를 허용합니다.

```php
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
스키마 작성기 청사진은 데이터베이스 테이블에 추가할 수 있는 다양한 유형의 열에 해당하는 다양한 방법을 제공합니다. 사용 가능한 각 방법은 아래 표에 나열되어 있습니다.

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

<a name="relationship-method-list"></a>
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
`bigIncrements` 메소드는 자동 증가 `UNSIGNED BIGINT`(기본 키) 해당 열을 생성합니다.

```php
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
<!-- #### `bigInteger()` -->
#### `bigInteger()`

<!-- The `bigInteger` method creates a `BIGINT` equivalent column: -->
`bigInteger` 메소드는 `BIGINT` 해당 열을 생성합니다.

```php
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
<!-- #### `binary()` -->
#### `binary()`

<!-- The `binary` method creates a `BLOB` equivalent column: -->
`binary` 메소드는 `BLOB` 해당 열을 생성합니다.

```php
$table->binary('photo');
```

<!-- When utilizing MySQL, MariaDB, or SQL Server, you may pass `length` and `fixed` arguments to create `VARBINARY` or `BINARY` equivalent column: -->
MySQL, MariaDB 또는 SQL Server를 활용하는 경우 `length` 및 `fixed` 인수를 전달하여 `VARBINARY` 또는 `BINARY` 해당 열을 생성할 수 있습니다.

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```

<a name="column-method-boolean"></a>
<!-- #### `boolean()` -->
#### `boolean()`

<!-- The `boolean` method creates a `BOOLEAN` equivalent column: -->
`boolean` 메소드는 `BOOLEAN` 해당 열을 생성합니다.

```php
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
<!-- #### `char()` -->
#### `char()`

<!-- The `char` method creates a `CHAR` equivalent column with of a given length: -->
`char` 메소드는 주어진 길이의 `CHAR` 해당 열을 생성합니다.

```php
$table->char('name', length: 100);
```

<a name="column-method-dateTimeTz"></a>
<!-- #### `dateTimeTz()` -->
#### `dateTimeTz()`

<!-- The `dateTimeTz` method creates a `DATETIME` (with timezone) equivalent column with an optional fractional seconds precision: -->
`dateTimeTz` 메소드는 선택적 소수 초 정밀도를 사용하여 `DATETIME`(시간대 포함) 해당 열을 생성합니다.

```php
$table->dateTimeTz('created_at', precision: 0);
```

<a name="column-method-dateTime"></a>
<!-- #### `dateTime()` -->
#### `dateTime()`

<!-- The `dateTime` method creates a `DATETIME` equivalent column with an optional fractional seconds precision: -->
`dateTime` 메소드는 선택적 소수 초 정밀도를 사용하여 `DATETIME`에 해당하는 열을 생성합니다.

```php
$table->dateTime('created_at', precision: 0);
```

<a name="column-method-date"></a>
<!-- #### `date()` -->
#### `date()`

<!-- The `date` method creates a `DATE` equivalent column: -->
`date` 메소드는 `DATE` 해당 열을 생성합니다.

```php
$table->date('created_at');
```

<a name="column-method-decimal"></a>
<!-- #### `decimal()` -->
#### `decimal()`

<!-- The `decimal` method creates a `DECIMAL` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`decimal` 메소드는 주어진 정밀도(총 자릿수)와 소수 자릿수(십진수)를 사용하여 `DECIMAL`에 해당하는 열을 생성합니다.

```php
$table->decimal('amount', total: 8, places: 2);
```

<a name="column-method-double"></a>
<!-- #### `double()` -->
#### `double()`

<!-- The `double` method creates a `DOUBLE` equivalent column: -->
`double` 메소드는 `DOUBLE` 해당 열을 생성합니다.

```php
$table->double('amount');
```

<a name="column-method-enum"></a>
<!-- #### `enum()` -->
#### `enum()`

<!-- The `enum` method creates a `ENUM` equivalent column with the given valid values: -->
`enum` 메소드는 주어진 유효한 값을 사용하여 `ENUM`에 해당하는 열을 생성합니다.

```php
$table->enum('difficulty', ['easy', 'hard']);
```

<!-- Of course, you may use the `Enum::cases()` method instead of manually defining an array of allowed values: -->
물론 허용되는 값의 배열을 수동으로 정의하는 대신 `Enum::cases()` 메서드를 사용할 수도 있습니다.

```php
use App\Enums\Difficulty;

$table->enum('difficulty', Difficulty::cases());
```

<a name="column-method-float"></a>
<!-- #### `float()` -->
#### `float()`

<!-- The `float` method creates a `FLOAT` equivalent column with the given precision: -->
`float` 메소드는 지정된 정밀도로 `FLOAT`에 해당하는 열을 생성합니다.

```php
$table->float('amount', precision: 53);
```

<a name="column-method-foreignId"></a>
<!-- #### `foreignId()` -->
#### `foreignId()`

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column: -->
`foreignId` 메소드는 `UNSIGNED BIGINT` 해당 열을 생성합니다.

```php
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
<!-- #### `foreignIdFor()` -->
#### `foreignIdFor()`

<!-- The `foreignIdFor` method adds a `{column}_id` equivalent column for a given model class. The column type will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type: -->
`foreignIdFor` 메소드는 지정된 모델 클래스에 대해 `{column}_id` 해당 열을 추가합니다. 열 유형은 모델 키 유형에 따라 `UNSIGNED BIGINT`, `CHAR(36)` 또는 `CHAR(26)`입니다.

```php
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
<!-- #### `foreignUlid()` -->
#### `foreignUlid()`

<!-- The `foreignUlid` method creates a `ULID` equivalent column: -->
`foreignUlid` 메소드는 `ULID` 해당 열을 생성합니다.

```php
$table->foreignUlid('user_id');
```

<a name="column-method-foreignUuid"></a>
<!-- #### `foreignUuid()` -->
#### `foreignUuid()`

<!-- The `foreignUuid` method creates a `UUID` equivalent column: -->
`foreignUuid` 메소드는 `UUID` 해당 열을 생성합니다.

```php
$table->foreignUuid('user_id');
```

<a name="column-method-geography"></a>
<!-- #### `geography()` -->
#### `geography()`

<!-- The `geography` method creates a `GEOGRAPHY` equivalent column with the given spatial type and SRID (Spatial Reference System Identifier): -->
`geography` 메소드는 지정된 공간 유형 및 SRID(공간 참조 시스템 식별자)를 사용하여 `GEOGRAPHY`에 해당하는 열을 생성합니다.

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]
> 공간 유형 지원은 데이터베이스 드라이버에 따라 다릅니다. 데이터베이스 설명서를 참조하세요. 응용 프로그램이 PostgreSQL 데이터베이스를 활용하는 경우 `geography` 방법을 사용하기 전에 [PostGIS](https://postgis.net) 확장을 설치해야 합니다.

<a name="column-method-geometry"></a>
<!-- #### `geometry()` -->
#### `geometry()`

<!-- The `geometry` method creates a `GEOMETRY` equivalent column with the given spatial type and SRID (Spatial Reference System Identifier): -->
`geometry` 메소드는 지정된 공간 유형 및 SRID(공간 참조 시스템 식별자)를 사용하여 `GEOMETRY`에 해당하는 열을 생성합니다.

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]
> 공간 유형 지원은 데이터베이스 드라이버에 따라 다릅니다. 데이터베이스 설명서를 참조하세요. 응용 프로그램이 PostgreSQL 데이터베이스를 활용하는 경우 `geometry` 방법을 사용하기 전에 [PostGIS](https://postgis.net) 확장을 설치해야 합니다.

<a name="column-method-id"></a>
<!-- #### `id()` -->
#### `id()`

<!-- The `id` method is an alias of the `bigIncrements` method. By default, the method will create an `id` column; however, you may pass a column name if you would like to assign a different name to the column: -->
`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 이 메소드는 `id` 열을 생성합니다. 그러나 열에 다른 이름을 할당하려면 열 이름을 전달할 수 있습니다.

```php
$table->id();
```

<a name="column-method-increments"></a>
<!-- #### `increments()` -->
#### `increments()`

<!-- The `increments` method creates an auto-incrementing `UNSIGNED INTEGER` equivalent column as a primary key: -->
`increments` 메소드는 자동 증가 `UNSIGNED INTEGER` 해당 열을 기본 키로 생성합니다.

```php
$table->increments('id');
```

<a name="column-method-integer"></a>
<!-- #### `integer()` -->
#### `integer()`

<!-- The `integer` method creates an `INTEGER` equivalent column: -->
`integer` 메소드는 `INTEGER` 해당 열을 생성합니다.

```php
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
<!-- #### `ipAddress()` -->
#### `ipAddress()`

<!-- The `ipAddress` method creates a `VARCHAR` equivalent column: -->
`ipAddress` 메소드는 `VARCHAR` 해당 열을 생성합니다.

```php
$table->ipAddress('visitor');
```

<!-- When using PostgreSQL, an `INET` column will be created. -->
PostgreSQL를 사용하면 `INET` 열이 생성됩니다.

<a name="column-method-json"></a>
<!-- #### `json()` -->
#### `json()`

<!-- The `json` method creates a `JSON` equivalent column: -->
`json` 메소드는 `JSON` 해당 열을 생성합니다.

```php
$table->json('options');
```

<!-- When using SQLite, a `TEXT` column will be created. -->
SQLite를 사용하면 `TEXT` 열이 생성됩니다.

<a name="column-method-jsonb"></a>
<!-- #### `jsonb()` -->
#### `jsonb()`

<!-- The `jsonb` method creates a `JSONB` equivalent column: -->
`jsonb` 메소드는 `JSONB` 해당 열을 생성합니다.

```php
$table->jsonb('options');
```

<!-- When using SQLite, a `TEXT` column will be created. -->
SQLite를 사용하면 `TEXT` 열이 생성됩니다.

<a name="column-method-longText"></a>
<!-- #### `longText()` -->
#### `longText()`

<!-- The `longText` method creates a `LONGTEXT` equivalent column: -->
`longText` 메소드는 `LONGTEXT` 해당 열을 생성합니다.

```php
$table->longText('description');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `LONGBLOB` equivalent column: -->
MySQL 또는 MariaDB를 활용하는 경우 `LONGBLOB`에 해당하는 열을 생성하기 위해 열에 `binary` 문자 집합을 적용할 수 있습니다.

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```

<a name="column-method-macAddress"></a>
<!-- #### `macAddress()` -->
#### `macAddress()`

<!-- The `macAddress` method creates a column that is intended to hold a MAC address. Some database systems, such as PostgreSQL, have a dedicated column type for this type of data. Other database systems will use a string equivalent column: -->
`macAddress` 메소드는 MAC 주소를 보유하기 위한 열을 생성합니다. PostgreSQL와 같은 일부 데이터베이스 시스템에는 이러한 유형의 데이터에 대한 전용 열 유형이 있습니다. 다른 데이터베이스 시스템에서는 해당 문자열 열을 사용합니다.

```php
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
<!-- #### `mediumIncrements()` -->
#### `mediumIncrements()`

<!-- The `mediumIncrements` method creates an auto-incrementing `UNSIGNED MEDIUMINT` equivalent column as a primary key: -->
`mediumIncrements` 메소드는 자동 증가 `UNSIGNED MEDIUMINT` 해당 열을 기본 키로 생성합니다.

```php
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
<!-- #### `mediumInteger()` -->
#### `mediumInteger()`

<!-- The `mediumInteger` method creates a `MEDIUMINT` equivalent column: -->
`mediumInteger` 메소드는 `MEDIUMINT` 해당 열을 생성합니다.

```php
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
<!-- #### `mediumText()` -->
#### `mediumText()`

<!-- The `mediumText` method creates a `MEDIUMTEXT` equivalent column: -->
`mediumText` 메소드는 `MEDIUMTEXT` 해당 열을 생성합니다.

```php
$table->mediumText('description');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `MEDIUMBLOB` equivalent column: -->
MySQL 또는 MariaDB를 활용하는 경우 `MEDIUMBLOB`에 해당하는 열을 생성하기 위해 열에 `binary` 문자 집합을 적용할 수 있습니다.

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a name="column-method-morphs"></a>
<!-- #### `morphs()` -->
#### `morphs()`

<!-- The `morphs` method is a convenience method that adds a `{column}_id` equivalent column and a `{column}_type` `VARCHAR` equivalent column. The column type for the `{column}_id` will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type. -->
`morphs` 메소드는 `{column}_id` 해당 컬럼과 `{column}_type` `VARCHAR` 해당 컬럼을 추가하는 편의 메소드이다. `{column}_id`의 열 유형은 모델 키 유형에 따라 `UNSIGNED BIGINT`, `CHAR(36)` 또는 `CHAR(26)`입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/master/eloquent-relationships). In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 방법은 다형성 [Eloquent relationship](/docs/master/eloquent-relationships)에 필요한 열을 정의할 때 사용하기 위한 것입니다. 다음 예에서는 `taggable_id` 및 `taggable_type` 열이 생성됩니다.

```php
$table->morphs('taggable');
```

<a name="column-method-nullableMorphs"></a>
<!-- #### `nullableMorphs()` -->
#### `nullableMorphs()`

<!-- The method is similar to the [morphs](#column-method-morphs) method; however, the columns that are created will be "nullable": -->
이 방법은 [morphs](#column-method-morphs) 방법과 유사합니다. 그러나 생성된 열은 "nullable"입니다.

```php
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
<!-- #### `nullableUlidMorphs()` -->
#### `nullableUlidMorphs()`

<!-- The method is similar to the [ulidMorphs](#column-method-ulidMorphs) method; however, the columns that are created will be "nullable": -->
이 방법은 [ulidMorphs](#column-method-ulidMorphs) 방법과 유사합니다. 그러나 생성된 열은 "nullable"입니다.

```php
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
<!-- #### `nullableUuidMorphs()` -->
#### `nullableUuidMorphs()`

<!-- The method is similar to the [uuidMorphs](#column-method-uuidMorphs) method; however, the columns that are created will be "nullable": -->
이 방법은 [uuidMorphs](#column-method-uuidMorphs) 방법과 유사합니다. 그러나 생성된 열은 "nullable"입니다.

```php
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-rememberToken"></a>
<!-- #### `rememberToken()` -->
#### `rememberToken()`

<!-- The `rememberToken` method creates a nullable, `VARCHAR(100)` equivalent column that is intended to store the current "remember me" [authentication token](/docs/master/authentication#remembering-users): -->
`rememberToken` 메서드는 현재 "기억하기"[authentication token](/docs/master/authentication#remembering-users)을 저장하기 위한 nullable `VARCHAR(100)` 해당 열을 생성합니다.

```php
$table->rememberToken();
```

<a name="column-method-set"></a>
<!-- #### `set()` -->
#### `set()`

<!-- The `set` method creates a `SET` equivalent column with the given list of valid values: -->
`set` 메소드는 주어진 유효한 값 목록을 사용하여 `SET`에 해당하는 열을 생성합니다.

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
<!-- #### `smallIncrements()` -->
#### `smallIncrements()`

<!-- The `smallIncrements` method creates an auto-incrementing `UNSIGNED SMALLINT` equivalent column as a primary key: -->
`smallIncrements` 메소드는 자동 증가 `UNSIGNED SMALLINT` 해당 열을 기본 키로 생성합니다.

```php
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
<!-- #### `smallInteger()` -->
#### `smallInteger()`

<!-- The `smallInteger` method creates a `SMALLINT` equivalent column: -->
`smallInteger` 메소드는 `SMALLINT` 해당 열을 생성합니다.

```php
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
<!-- #### `softDeletesTz()` -->
#### `softDeletesTz()`

<!-- The `softDeletesTz` method adds a nullable `deleted_at` `TIMESTAMP` (with timezone) equivalent column with an optional fractional seconds precision. This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletesTz` 메소드는 선택적 소수 초 정밀도를 사용하여 null 허용 `deleted_at` `TIMESTAMP`(시간대 포함) 해당 열을 추가합니다. 이 열은 Eloquent의 "일시 삭제" 기능에 필요한 `deleted_at` 타임스탬프를 저장하기 위한 것입니다.

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

<a name="column-method-softDeletes"></a>
<!-- #### `softDeletes()` -->
#### `softDeletes()`

<!-- The `softDeletes` method adds a nullable `deleted_at` `TIMESTAMP` equivalent column with an optional fractional seconds precision. This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletes` 메서드는 선택적 소수 초 정밀도를 사용하여 null 허용 `deleted_at` `TIMESTAMP` 해당 열을 추가합니다. 이 열은 Eloquent의 "일시 삭제" 기능에 필요한 `deleted_at` 타임스탬프를 저장하기 위한 것입니다.

```php
$table->softDeletes('deleted_at', precision: 0);
```

<a name="column-method-string"></a>
<!-- #### `string()` -->
#### `string()`

<!-- The `string` method creates a `VARCHAR` equivalent column of the given length: -->
`string` 메소드는 지정된 길이의 `VARCHAR` 해당 열을 생성합니다.

```php
$table->string('name', length: 100);
```

<a name="column-method-text"></a>
<!-- #### `text()` -->
#### `text()`

<!-- The `text` method creates a `TEXT` equivalent column: -->
`text` 메소드는 `TEXT` 해당 열을 생성합니다.

```php
$table->text('description');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `BLOB` equivalent column: -->
MySQL 또는 MariaDB를 활용하는 경우 `BLOB`에 해당하는 열을 생성하기 위해 열에 `binary` 문자 집합을 적용할 수 있습니다.

```php
$table->text('data')->charset('binary'); // BLOB
```

<a name="column-method-timeTz"></a>
<!-- #### `timeTz()` -->
#### `timeTz()`

<!-- The `timeTz` method creates a `TIME` (with timezone) equivalent column with an optional fractional seconds precision: -->
`timeTz` 메소드는 선택적 소수 초 정밀도를 사용하여 `TIME`(시간대 포함) 해당 열을 생성합니다.

```php
$table->timeTz('sunrise', precision: 0);
```

<a name="column-method-time"></a>
<!-- #### `time()` -->
#### `time()`

<!-- The `time` method creates a `TIME` equivalent column with an optional fractional seconds precision: -->
`time` 메소드는 선택적 소수 초 정밀도를 사용하여 `TIME`에 해당하는 열을 생성합니다.

```php
$table->time('sunrise', precision: 0);
```

<a name="column-method-timestampTz"></a>
<!-- #### `timestampTz()` -->
#### `timestampTz()`

<!-- The `timestampTz` method creates a `TIMESTAMP` (with timezone) equivalent column with an optional fractional seconds precision: -->
`timestampTz` 메소드는 선택적 소수 초 정밀도를 사용하여 `TIMESTAMP`(시간대 포함) 해당 열을 생성합니다.

```php
$table->timestampTz('added_at', precision: 0);
```

<a name="column-method-timestamp"></a>
<!-- #### `timestamp()` -->
#### `timestamp()`

<!-- The `timestamp` method creates a `TIMESTAMP` equivalent column with an optional fractional seconds precision: -->
`timestamp` 메소드는 선택적 소수 초 정밀도를 사용하여 `TIMESTAMP`에 해당하는 열을 생성합니다.

```php
$table->timestamp('added_at', precision: 0);
```

<a name="column-method-timestampsTz"></a>
<!-- #### `timestampsTz()` -->
#### `timestampsTz()`

<!-- The `timestampsTz` method creates `created_at` and `updated_at` `TIMESTAMP` (with timezone) equivalent columns with an optional fractional seconds precision: -->
`timestampsTz` 메소드는 선택적 소수 초 정밀도를 사용하여 `created_at` 및 `updated_at` `TIMESTAMP`(시간대 포함) 해당 열을 생성합니다.

```php
$table->timestampsTz(precision: 0);
```

<a name="column-method-timestamps"></a>
<!-- #### `timestamps()` -->
#### `timestamps()`

<!-- The `timestamps` method creates `created_at` and `updated_at` `TIMESTAMP` equivalent columns with an optional fractional seconds precision: -->
`timestamps` 메소드는 선택적 소수 초 정밀도를 사용하여 `created_at` 및 `updated_at` `TIMESTAMP` 해당 열을 생성합니다.

```php
$table->timestamps(precision: 0);
```

<a name="column-method-tinyIncrements"></a>
<!-- #### `tinyIncrements()` -->
#### `tinyIncrements()`

<!-- The `tinyIncrements` method creates an auto-incrementing `UNSIGNED TINYINT` equivalent column as a primary key: -->
`tinyIncrements` 메소드는 자동 증가 `UNSIGNED TINYINT` 해당 열을 기본 키로 생성합니다.

```php
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
<!-- #### `tinyInteger()` -->
#### `tinyInteger()`

<!-- The `tinyInteger` method creates a `TINYINT` equivalent column: -->
`tinyInteger` 메소드는 `TINYINT` 해당 열을 생성합니다.

```php
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
<!-- #### `tinyText()` -->
#### `tinyText()`

<!-- The `tinyText` method creates a `TINYTEXT` equivalent column: -->
`tinyText` 메소드는 `TINYTEXT` 해당 열을 생성합니다.

```php
$table->tinyText('notes');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `TINYBLOB` equivalent column: -->
MySQL 또는 MariaDB를 활용하는 경우 `TINYBLOB`에 해당하는 열을 생성하기 위해 열에 `binary` 문자 집합을 적용할 수 있습니다.

```php
$table->tinyText('data')->charset('binary'); // TINYBLOB
```

<a name="column-method-unsignedBigInteger"></a>
<!-- #### `unsignedBigInteger()` -->
#### `unsignedBigInteger()`

<!-- The `unsignedBigInteger` method creates an `UNSIGNED BIGINT` equivalent column: -->
`unsignedBigInteger` 메소드는 `UNSIGNED BIGINT` 해당 열을 생성합니다.

```php
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedInteger"></a>
<!-- #### `unsignedInteger()` -->
#### `unsignedInteger()`

<!-- The `unsignedInteger` method creates an `UNSIGNED INTEGER` equivalent column: -->
`unsignedInteger` 메소드는 `UNSIGNED INTEGER` 해당 열을 생성합니다.

```php
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
<!-- #### `unsignedMediumInteger()` -->
#### `unsignedMediumInteger()`

<!-- The `unsignedMediumInteger` method creates an `UNSIGNED MEDIUMINT` equivalent column: -->
`unsignedMediumInteger` 메소드는 `UNSIGNED MEDIUMINT` 해당 열을 생성합니다.

```php
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
<!-- #### `unsignedSmallInteger()` -->
#### `unsignedSmallInteger()`

<!-- The `unsignedSmallInteger` method creates an `UNSIGNED SMALLINT` equivalent column: -->
`unsignedSmallInteger` 메소드는 `UNSIGNED SMALLINT` 해당 열을 생성합니다.

```php
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
<!-- #### `unsignedTinyInteger()` -->
#### `unsignedTinyInteger()`

<!-- The `unsignedTinyInteger` method creates an `UNSIGNED TINYINT` equivalent column: -->
`unsignedTinyInteger` 메소드는 `UNSIGNED TINYINT` 해당 열을 생성합니다.

```php
$table->unsignedTinyInteger('votes');
```

<a name="column-method-ulidMorphs"></a>
<!-- #### `ulidMorphs()` -->
#### `ulidMorphs()`

<!-- The `ulidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(26)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`ulidMorphs` 메서드는 `{column}_id` `CHAR(26)` 해당 열과 `{column}_type` `VARCHAR` 해당 열을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/master/eloquent-relationships) that use ULID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 방법은 ULID 식별자를 사용하는 다형성 [Eloquent relationship](/docs/master/eloquent-relationships)에 필요한 열을 정의할 때 사용하기 위한 것입니다. 다음 예에서는 `taggable_id` 및 `taggable_type` 열이 생성됩니다.

```php
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
<!-- #### `uuidMorphs()` -->
#### `uuidMorphs()`

<!-- The `uuidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(36)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`uuidMorphs` 메서드는 `{column}_id` `CHAR(36)` 해당 열과 `{column}_type` `VARCHAR` 해당 열을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a [polymorphic Eloquent relationship](/docs/master/eloquent-relationships#polymorphic-relationships) that use UUID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 방법은 UUID 식별자를 사용하는 [polymorphic Eloquent relationship](/docs/master/eloquent-relationships#polymorphic-relationships)에 필요한 열을 정의할 때 사용하기 위한 것입니다. 다음 예에서는 `taggable_id` 및 `taggable_type` 열이 생성됩니다.

```php
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
<!-- #### `ulid()` -->
#### `ulid()`

<!-- The `ulid` method creates a `ULID` equivalent column: -->
`ulid` 메소드는 `ULID` 해당 열을 생성합니다.

```php
$table->ulid('id');
```

<a name="column-method-uuid"></a>
<!-- #### `uuid()` -->
#### `uuid()`

<!-- The `uuid` method creates a `UUID` equivalent column: -->
`uuid` 메소드는 `UUID` 해당 열을 생성합니다.

```php
$table->uuid('id');
```

<a name="column-method-vector"></a>
<!-- #### `vector()` -->
#### `vector()`

<!-- The `vector` method creates a `vector` equivalent column: -->
`vector` 메소드는 `vector` 해당 열을 생성합니다.

```php
$table->vector('embedding', dimensions: 100);
```

<!-- When utilizing PostgreSQL, the `pgvector` extension must be loaded before `vector` columns can be created: -->
PostgreSQL를 활용하는 경우 `vector` 열을 생성하기 전에 `pgvector` 확장을 로드해야 합니다.

```php
Schema::ensureVectorExtensionExists();
```

<a name="column-method-year"></a>
<!-- #### `year()` -->
#### `year()`

<!-- The `year` method creates a `YEAR` equivalent column: -->
`year` 메소드는 `YEAR` 해당 열을 생성합니다.

```php
$table->year('birth_year');
```

<a name="column-modifiers"></a>
<!-- ### Column Modifiers -->
### Column Modifiers

<!-- In addition to the column types listed above, there are several column "modifiers" you may use when adding a column to a database table. For example, to make the column "nullable", you may use the `nullable` method: -->
위에 나열된 열 유형 외에도 데이터베이스 테이블에 열을 추가할 때 사용할 수 있는 여러 가지 열 "수정자"가 있습니다. 예를 들어, 열을 "nullable"로 만들려면 `nullable` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

<!-- The following table contains all of the available column modifiers. This list does not include [index modifiers](#creating-indexes): -->
다음 표에는 사용 가능한 모든 열 수정자가 포함되어 있습니다. 이 목록에는 [index modifiers](#creating-indexes)가 포함되지 않습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 수정자 | 설명 |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- |
| `->after('column')` | 다른 열(MariaDB / MySQL) "뒤에" 열을 배치합니다.                                     |
| `->autoIncrement()` | `INTEGER` 열을 자동 증가(기본 키)로 설정합니다.                                      |
| `->charset('utf8mb4')` | 열(MariaDB / MySQL)에 대한 문자 집합을 지정합니다.                                      |
| `->collation('utf8mb4_unicode_ci')` | 열의 데이터 정렬을 지정합니다.                                                            |
| `->comment('my comment')` | 열(MariaDB / MySQL / PostgreSQL)에 설명을 추가합니다.                                      |
| `->default($value)` | 열의 "기본값"을 지정합니다.                                                      |
| `->first()` | 테이블(MariaDB / MySQL)에 "첫 번째" 열을 배치합니다.                                       |
| `->from($integer)` | 자동 증가 필드(MariaDB / MySQL / PostgreSQL)의 시작 값을 설정합니다.           |
| `->instant()` | 인스턴트 작업(MySQL)을 사용하여 열을 추가하거나 수정합니다.                                   |
| `->invisible()` | 열을 `SELECT *` 쿼리 (MariaDB / MySQL)에 "보이지 않게" 만듭니다.                           |
| `->lock($mode)` | 컬럼 조작(MySQL)에 대한 잠금 모드를 지정하십시오.                                          |
| `->nullable($value = true)` | `NULL` 값이 열에 삽입되도록 허용합니다.                                            |
| `->storedAs($expression)` | 저장된 생성 열(MariaDB / MySQL / PostgreSQL / SQLite)을 만듭니다.                      |
| `->unsigned()` | `INTEGER` 열을 `UNSIGNED`(MariaDB / MySQL)로 설정합니다.                                         |
| `->useCurrent()` | `CURRENT_TIMESTAMP`를 기본값으로 사용하도록 `TIMESTAMP` 열을 설정합니다.                           |
| `->useCurrentOnUpdate()` | 레코드가 업데이트될 때 `CURRENT_TIMESTAMP`를 사용하도록 `TIMESTAMP` 열을 설정합니다(MariaDB / MySQL). |
| `->virtualAs($expression)` | 가상 생성 열(MariaDB / MySQL / SQLite)을 만듭니다.                                  |
| `->generatedAs($expression)` | 지정된 순서 옵션(PostgreSQL)을 사용하여 ID 열을 만듭니다.                        |
| `->always()` | ID 열(PostgreSQL)에 대한 입력보다 시퀀스 값의 우선순위를 정의합니다.      |

<!-- </div> -->
</div>

<a name="default-expressions"></a>
<!-- #### Default Expressions -->
#### Default Expressions

<!-- The `default` modifier accepts a value or an `Illuminate\Database\Query\Expression` instance. Using an `Expression` instance will prevent Laravel from wrapping the value in quotes and allow you to use database specific functions. One situation where this is particularly useful is when you need to assign default values to JSON columns: -->
`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 허용합니다. `Expression` 인스턴스를 사용하면 Laravel가 값을 따옴표로 묶는 것을 방지하고 데이터베이스 관련 기능을 사용할 수 있습니다. 이것이 특히 유용한 상황 중 하나는 JSON 열에 기본값을 할당해야 하는 경우입니다.

```php
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
> 기본 표현식 지원은 데이터베이스 드라이버, 데이터베이스 버전 및 필드 유형에 따라 다릅니다. 데이터베이스 설명서를 참조하세요.

<a name="column-order"></a>
<!-- #### Column Order -->
#### Column Order

<!-- When using the MariaDB or MySQL database, the `after` method may be used to add columns after an existing column in the schema: -->
MariaDB 또는 MySQL 데이터베이스를 사용하는 경우 `after` 메서드를 사용하여 스키마의 기존 열 뒤에 열을 추가할 수 있습니다.

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="instant-column-operations"></a>
<!-- #### Instant Column Operations -->
#### Instant Column Operations

<!-- When using MySQL, you may chain the `instant` modifier onto a column definition to indicate that the column should be added or modified using MySQL's "instant" algorithm. This algorithm allows certain schema changes to be performed without a full table rebuild, making them nearly instantaneous regardless of table size: -->
MySQL을 사용할 때 열 정의에 `instant` 수정자를 연결하여 MySQL의 "인스턴트" 알고리즘을 사용하여 열을 추가하거나 수정해야 함을 나타낼 수 있습니다. 이 알고리즘을 사용하면 전체 테이블을 다시 작성하지 않고도 특정 스키마 변경을 수행할 수 있으므로 테이블 크기에 관계없이 거의 즉시 변경이 가능합니다.

```php
$table->string('name')->nullable()->instant();
```

<!-- Instant column additions can only append columns to the end of the table, so the `instant` modifier cannot be combined with the `after` or `first` modifiers. In addition, the algorithm does not support all column types or operations. If the requested operation is incompatible, MySQL will raise an error. -->
즉각적인 열 추가는 테이블 끝에만 열을 추가할 수 있으므로 `instant` 수정자는 `after` 또는 `first` 수정자와 결합될 수 없습니다. 또한 알고리즘은 모든 열 유형이나 작업을 지원하지 않습니다. 요청한 작업이 호환되지 않으면 MySQL에서 오류가 발생합니다.

<!-- Please refer to [MySQL's documentation](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html) to determine which operations are compatible with instant column modifications. -->
즉각적인 컬럼 수정과 호환되는 작업을 확인하려면 [MySQL's documentation](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)를 참조하세요.

<a name="ddl-locking"></a>
<!-- #### DDL Locking -->
#### DDL Locking

<!-- When using MySQL, you may chain the `lock` modifier onto column, index, or foreign key definitions to control table locking during schema operations. MySQL supports several lock modes: `none` allows concurrent reads and writes, `shared` allows concurrent reads but blocks writes, `exclusive` blocks all concurrent access, and `default` lets MySQL choose the most appropriate mode: -->
MySQL을 사용하는 경우 `lock` 수정자를 열, 인덱스 또는 외래 키 정의에 연결하여 스키마 작업 중 테이블 잠금을 제어할 수 있습니다. MySQL는 여러 잠금 모드를 지원합니다. `none`는 동시 읽기 및 쓰기를 허용하고, `shared`는 동시 읽기를 허용하지만 쓰기를 차단하며, `exclusive`는 모든 동시 액세스를 차단하고, `default`는 MySQL가 가장 적절한 모드를 선택할 수 있도록 합니다.

```php
$table->string('name')->lock('none');

$table->index('email')->lock('shared');
```

<!-- If the requested lock mode is incompatible with the operation, MySQL will raise an error. The `lock` modifier may be combined with the `instant` modifier to further optimize schema changes: -->
요청된 잠금 모드가 작업과 호환되지 않으면 MySQL에서 오류가 발생합니다. `lock` 수정자는 `instant` 수정자와 결합되어 스키마 변경을 더욱 최적화할 수 있습니다.

```php
$table->string('name')->instant()->lock('none');
```

<a name="modifying-columns"></a>
<!-- ### Modifying Columns -->
### Modifying Columns

<!-- The `change` method allows you to modify the type and attributes of existing columns. For example, you may wish to increase the size of a `string` column. To see the `change` method in action, let's increase the size of the `name` column from 25 to 50. To accomplish this, we simply define the new state of the column and then call the `change` method: -->
`change` 방법을 사용하면 기존 열의 유형과 속성을 수정할 수 있습니다. 예를 들어, `string` 열의 크기를 늘릴 수 있습니다. `change` 메서드가 실제로 작동하는 모습을 보려면 `name` 열의 크기를 25에서 50으로 늘려 보겠습니다. 이를 달성하려면 열의 새 상태를 정의한 다음 `change` 메서드를 호출하기만 하면 됩니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

<!-- When modifying a column, you must explicitly include all the modifiers you want to keep on the column definition - any missing attribute will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column: -->
열을 수정할 때 열 정의에 유지하려는 모든 수정자를 명시적으로 포함해야 합니다. 누락된 속성은 삭제됩니다. 예를 들어, `unsigned`, `default` 및 `comment` 속성을 유지하려면 열을 변경할 때 각 수정자를 명시적으로 호출해야 합니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

<!-- The `change` method does not change the indexes of the column. Therefore, you may use index modifiers to explicitly add or drop an index when modifying the column: -->
`change` 메소드는 열의 인덱스를 변경하지 않습니다. 따라서 인덱스 수정자를 사용하여 열을 수정할 때 인덱스를 명시적으로 추가하거나 삭제할 수 있습니다.

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
열 이름을 바꾸려면 스키마 빌더에서 제공하는 `renameColumn` 메서드를 사용할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
<!-- ### Dropping Columns -->
### Dropping Columns

<!-- To drop a column, you may use the `dropColumn` method on the schema builder: -->
열을 삭제하려면 스키마 빌더에서 `dropColumn` 메서드를 사용할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

<!-- You may drop multiple columns from a table by passing an array of column names to the `dropColumn` method: -->
열 이름 배열을 `dropColumn` 메소드에 전달하여 테이블에서 여러 열을 삭제할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
<!-- #### Available Command Aliases -->
#### Available Command Aliases

<!-- Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below: -->
Laravel는 일반적인 유형의 열 삭제와 관련된 몇 가지 편리한 방법을 제공합니다. 각 방법은 아래 표에 설명되어 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 명령 | 설명 |
| ----------------------------------- | ----------------------------------------------------- |
| `$table->dropMorphs('morphable');` | `morphable_id` 및 `morphable_type` 열을 삭제합니다. |
| `$table->dropRememberToken();` | `remember_token` 열을 삭제합니다.                     |
| `$table->dropSoftDeletes();` | `deleted_at` 열을 삭제합니다.                         |
| `$table->dropSoftDeletesTz();` | `dropSoftDeletes()` 메소드의 별칭입니다.                  |
| `$table->dropTimestamps();` | `created_at` 및 `updated_at` 열을 삭제합니다.       |
| `$table->dropTimestampsTz();` | `dropTimestamps()` 메소드의 별칭입니다.                   |

<!-- </div> -->
</div>

<a name="indexes"></a>
<!-- ## Indexes -->
## Indexes

<a name="creating-indexes"></a>
<!-- ### Creating Indexes -->
### Creating Indexes

<!-- The Laravel schema builder supports several types of indexes. The following example creates a new `email` column and specifies that its values should be unique. To create the index, we can chain the `unique` method onto the column definition: -->
Laravel 스키마 빌더는 여러 유형의 인덱스를 지원합니다. 다음 예에서는 새 `email` 열을 생성하고 해당 값이 고유해야 함을 지정합니다. 인덱스를 생성하려면 `unique` 메서드를 열 정의에 연결할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

<!-- Alternatively, you may create the index after defining the column. To do so, you should call the `unique` method on the schema builder blueprint. This method accepts the name of the column that should receive a unique index: -->
또는 열을 정의한 후 인덱스를 생성할 수도 있습니다. 이렇게 하려면 스키마 빌더 청사진에서 `unique` 메서드를 호출해야 합니다. 이 메소드는 고유 인덱스를 수신해야 하는 열의 이름을 허용합니다.

```php
$table->unique('email');
```

<!-- You may even pass an array of columns to an index method to create a compound (or composite) index: -->
복합(또는 복합) 인덱스를 생성하기 위해 열 배열을 인덱스 메소드에 전달할 수도 있습니다:

```php
$table->index(['account_id', 'created_at']);
```

<!-- When creating an index, Laravel will automatically generate an index name based on the table, column names, and the index type, but you may pass a second argument to the method to specify the index name yourself: -->
인덱스를 생성할 때 Laravel는 테이블, 열 이름 및 인덱스 유형을 기반으로 인덱스 이름을 자동으로 생성하지만, 인덱스 이름을 직접 지정하기 위해 메서드에 두 번째 인수를 전달할 수도 있습니다.

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
<!-- #### Available Index Types -->
#### Available Index Types

<!-- Laravel's schema builder blueprint class provides methods for creating each type of index supported by Laravel. Each index method accepts an optional second argument to specify the name of the index. If omitted, the name will be derived from the names of the table and column(s) used for the index, as well as the index type. Each of the available index methods is described in the table below: -->
Laravel의 스키마 빌더 청사진 클래스는 Laravel에서 지원하는 각 유형의 인덱스를 생성하는 방법을 제공합니다. 각 인덱스 메소드는 인덱스 이름을 지정하기 위해 선택적 두 번째 인수를 허용합니다. 생략하면 인덱스에 사용된 테이블 및 열 이름과 인덱스 유형에서 이름이 파생됩니다. 사용 가능한 각 인덱스 방법은 아래 표에 설명되어 있습니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 명령 | 설명 |
| ------------------------------------------------ | -------------------------------------------------------------- |
| `$table->primary('id');` | 기본 키를 추가합니다.                                            |
| `$table->primary(['id', 'parent_id']);` | 복합 키를 추가합니다.                                           |
| `$table->unique('email');` | 고유 인덱스를 추가합니다.                                           |
| `$table->index('state');` | 인덱스를 추가합니다.                                                 |
| `$table->fullText('body');` | 전체 텍스트 색인(MariaDB / MySQL / PostgreSQL)을 추가합니다.         |
| `$table->fullText('body')->language('english');` | 지정된 언어(PostgreSQL)의 전체 텍스트 색인을 추가합니다. |
| `$table->spatialIndex('location');` | 공간 인덱스를 추가합니다(SQLite 제외).                          |

<!-- </div> -->
</div>

<a name="online-index-creation"></a>
<!-- #### Online Index Creation -->
#### Online Index Creation

<!-- By default, creating an index on a large table can lock the table and block reads or writes while the index is being built. When using PostgreSQL or SQL Server, you may chain the `online` method onto an index definition to create the index without locking the table, allowing your application to continue reading and writing data during index creation: -->
기본적으로 큰 테이블에 인덱스를 생성하면 테이블이 잠기고 인덱스가 작성되는 동안 읽기 또는 쓰기가 차단될 수 있습니다. PostgreSQL 또는 SQL Server를 사용하는 경우 `online` 메서드를 인덱스 정의에 연결하여 테이블을 잠그지 않고 인덱스를 생성할 수 있습니다. 그러면 애플리케이션이 인덱스 생성 중에 데이터를 계속 읽고 쓸 수 있습니다.

```php
$table->string('email')->unique()->online();
```

<!-- When using PostgreSQL, this adds the `CONCURRENTLY` option to the index creation statement. When using SQL Server, this adds the `WITH (online = on)` option. -->
PostgreSQL를 사용하는 경우 인덱스 생성 문에 `CONCURRENTLY` 옵션이 추가됩니다. SQL Server를 사용하는 경우 `WITH (online = on)` 옵션이 추가됩니다.

<a name="renaming-indexes"></a>
<!-- ### Renaming Indexes -->
### Renaming Indexes

<!-- To rename an index, you may use the `renameIndex` method provided by the schema builder blueprint. This method accepts the current index name as its first argument and the desired name as its second argument: -->
인덱스 이름을 바꾸려면 스키마 빌더 청사진에서 제공하는 `renameIndex` 방법을 사용할 수 있습니다. 이 메소드는 현재 인덱스 이름을 첫 번째 인수로, 원하는 이름을 두 번째 인수로 받아들입니다.

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
<!-- ### Dropping Indexes -->
### Dropping Indexes

<!-- To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples: -->
인덱스를 삭제하려면 인덱스 이름을 지정해야 합니다. 기본적으로 Laravel는 테이블 이름, 인덱싱된 열 이름 및 인덱스 유형을 기반으로 인덱스 이름을 자동으로 할당합니다. 다음은 몇 가지 예입니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 명령 | 설명 |
| -------------------------------------------------------- | ----------------------------------------------------------- |
| `$table->dropPrimary('users_id_primary');` | "users" 테이블에서 기본 키를 삭제합니다.                  |
| `$table->dropUnique('users_email_unique');` | "users" 테이블에서 고유 인덱스를 삭제합니다.                 |
| `$table->dropIndex('geo_state_index');` | "geo" 테이블에서 기본 인덱스를 삭제합니다.                    |
| `$table->dropFullText('posts_body_fulltext');` | "posts" 테이블에서 전체 텍스트 색인을 삭제합니다.              |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블에서 공간 인덱스를 삭제합니다(SQLite 제외). |

<!-- </div> -->
</div>

<!-- If you pass an array of columns into a method that drops indexes, the conventional index name will be generated based on the table name, columns, and index type: -->
인덱스를 삭제하는 메서드에 열 배열을 전달하면 테이블 이름, 열 및 인덱스 유형을 기반으로 기존 인덱스 이름이 생성됩니다.

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a name="foreign-key-constraints"></a>
<!-- ### Foreign Key Constraints -->
### Foreign Key Constraints

<!-- Laravel also provides support for creating foreign key constraints, which are used to force referential integrity at the database level. For example, let's define a `user_id` column on the `posts` table that references the `id` column on a `users` table: -->
Laravel는 또한 데이터베이스 수준에서 참조 무결성을 강제하는 데 사용되는 외래 키 제약 조건 생성을 지원합니다. 예를 들어, `users` 테이블의 `id` 열을 참조하는 `posts` 테이블에 `user_id` 열을 정의해 보겠습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

<!-- Since this syntax is rather verbose, Laravel provides additional, terser methods that use conventions to provide a better developer experience. When using the `foreignId` method to create your column, the example above can be rewritten like so: -->
이 구문은 다소 장황하므로 Laravel는 더 나은 개발자 환경을 제공하기 위해 규칙을 사용하는 더 간결한 추가 방법을 제공합니다. `foreignId` 메소드를 사용하여 열을 생성할 때 위의 예는 다음과 같이 다시 작성할 수 있습니다.

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column, while the `constrained` method will use conventions to determine the table and column being referenced. If your table name does not match Laravel's conventions, you may manually provide it to the `constrained` method. In addition, the name that should be assigned to the generated index may be specified as well: -->
`foreignId` 메서드는 `UNSIGNED BIGINT`에 해당하는 열을 생성하는 반면, `constrained` 메서드는 규칙을 사용하여 참조되는 테이블과 열을 결정합니다. 테이블 이름이 Laravel의 규칙과 일치하지 않는 경우 수동으로 `constrained` 메서드에 제공할 수 있습니다. 또한 생성된 인덱스에 할당되어야 하는 이름도 지정할 수 있습니다.

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

<!-- You may also specify the desired action for the "on delete" and "on update" properties of the constraint: -->
제약 조건의 "삭제 시" 및 "업데이트 시" 속성에 대해 원하는 작업을 지정할 수도 있습니다.

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

<!-- An alternative, expressive syntax is also provided for these actions: -->
다음 작업에 대한 대체 표현 구문도 제공됩니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 방법 | 설명 |
| ----------------------------- | ------------------------------------------------- |
| `$table->cascadeOnUpdate();` | 업데이트는 계단식으로 이루어져야 합니다.                           |
| `$table->restrictOnUpdate();` | 업데이트를 제한해야 합니다.                     |
| `$table->nullOnUpdate();` | 업데이트에서는 외래 키 값을 null로 설정해야 합니다. |
| `$table->noActionOnUpdate();` | 업데이트에 대한 조치가 없습니다.                             |
| `$table->cascadeOnDelete();` | 삭제는 계단식으로 이루어져야 합니다.                           |
| `$table->restrictOnDelete();` | 삭제는 제한되어야 합니다.                     |
| `$table->nullOnDelete();` | 삭제 시 외래 키 값을 null로 설정해야 합니다. |
| `$table->noActionOnDelete();` | 하위 레코드가 있는 경우 삭제를 방지합니다.          |

<!-- </div> -->
</div>

<!-- Any additional [column modifiers](#column-modifiers) must be called before the `constrained` method: -->
추가 [column modifiers](#column-modifiers)는 `constrained` 메서드 전에 호출되어야 합니다.

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
<!-- #### Dropping Foreign Keys -->
#### Dropping Foreign Keys

<!-- To drop a foreign key, you may use the `dropForeign` method, passing the name of the foreign key constraint to be deleted as an argument. Foreign key constraints use the same naming convention as indexes. In other words, the foreign key constraint name is based on the name of the table and the columns in the constraint, followed by a "\_foreign" suffix: -->
외래 키를 삭제하려면 `dropForeign` 메서드를 사용하여 삭제할 외래 키 제약 조건의 이름을 인수로 전달하면 됩니다. 외래 키 제약 조건은 인덱스와 동일한 명명 규칙을 사용합니다. 즉, 외래 키 제약 조건 이름은 테이블 이름과 제약 조건의 열을 기반으로 하며 그 뒤에 "\_foreign" 접미사가 옵니다.

```php
$table->dropForeign('posts_user_id_foreign');
```

<!-- Alternatively, you may pass an array containing the column name that holds the foreign key to the `dropForeign` method. The array will be converted to a foreign key constraint name using Laravel's constraint naming conventions: -->
또는 외래 키를 보유하는 열 이름이 포함된 배열을 `dropForeign` 메서드에 전달할 수도 있습니다. 배열은 Laravel의 제약 조건 명명 규칙을 사용하여 외래 키 제약 조건 이름으로 변환됩니다.

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
<!-- #### Toggling Foreign Key Constraints -->
#### Toggling Foreign Key Constraints

<!-- You may enable or disable foreign key constraints within your migrations by using the following methods: -->
다음 방법을 사용하여 마이그레이션 내에서 외래 키 제약 조건을 활성화하거나 비활성화할 수 있습니다.

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약 조건을 비활성화합니다. SQLite를 사용하는 경우 마이그레이션에서 생성을 시도하기 전에 데이터베이스 구성에서 [enable foreign key support](/docs/master/database#configuration)했는지 확인하세요.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- For convenience, each migration operation will dispatch an [event](/docs/master/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class: -->
편의상 각 마이그레이션 작업은 디스패치 및 [event](/docs/master/events)입니다. 다음 이벤트는 모두 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 확장합니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 클래스 | 설명 |
| ------------------------------------------------ | ------------------------------------------------ |
| `Illuminate\Database\Events\MigrationsStarted` | 마이그레이션의 배치가 실행되려고 합니다.   |
| `Illuminate\Database\Events\MigrationsEnded` | 마이그레이션의 배치가 실행을 완료했습니다.    |
| `Illuminate\Database\Events\MigrationStarted` | 단일 마이그레이션이 곧 실행될 예정입니다.      |
| `Illuminate\Database\Events\MigrationEnded` | 단일 마이그레이션 실행이 완료되었습니다.       |
| `Illuminate\Database\Events\NoPendingMigrations` | 마이그레이션 명령이 보류 중인 마이그레이션을 찾지 못했습니다. |
| `Illuminate\Database\Events\SchemaDumped` | 데이터베이스 스키마 덤프가 완료되었습니다.            |
| `Illuminate\Database\Events\SchemaLoaded` | 기존 데이터베이스 스키마 덤프가 로드되었습니다.     |

<!-- </div> -->
</div>
