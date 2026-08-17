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
마이그레이션은 데이터베이스를 위한 버전 관리와 같습니다. 팀이 애플리케이션의 데이터베이스 스키마 정의를 함께 정의하고 공유할 수 있게 해 줍니다. 소스 컨트롤에서 변경 사항을 가져온 뒤, 팀원에게 로컬 데이터베이스 스키마에 컬럼을 수동으로 추가하라고 말해야 했던 적이 있다면, 이미 데이터베이스 마이그레이션이 해결하려는 문제를 겪어 본 것입니다.

<!-- The Laravel `Schema` [facade](/docs/13.x/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns. -->
Laravel의 `Schema` [facade](/docs/13.x/facades)는 Laravel이 지원하는 모든 데이터베이스 시스템에서 테이블을 생성하고 조작할 수 있도록 데이터베이스에 구애받지 않는 기능을 제공합니다. 일반적으로 마이그레이션은 이 파사드를 사용해 데이터베이스 테이블과 컬럼을 생성하고 수정합니다.

<a name="generating-migrations"></a>
<!-- ## Generating Migrations -->
## Generating Migrations

<!-- You may use the `make:migration` [Artisan command](/docs/13.x/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations: -->
`make:migration` [Artisan command](/docs/13.x/artisan)을 사용해 데이터베이스 마이그레이션을 생성할 수 있습니다. 새 마이그레이션은 `database/migrations` 디렉터리에 배치됩니다. 각 마이그레이션 파일 이름에는 Laravel이 마이그레이션 순서를 결정할 수 있도록 타임스탬프가 포함됩니다:

```shell
php artisan make:migration create_flights_table
```

<!-- Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually. -->
Laravel은 마이그레이션 이름을 사용하여 테이블 이름과, 해당 마이그레이션이 새 테이블을 생성하는지 여부를 추측하려고 시도합니다. Laravel이 마이그레이션 이름에서 테이블 이름을 확인할 수 있으면, 생성된 마이그레이션 파일에 지정된 테이블을 미리 채워 넣습니다. 그렇지 않은 경우에는 마이그레이션 파일에서 테이블을 직접 지정하면 됩니다.

<!-- If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path. -->
생성되는 마이그레이션의 사용자 지정 경로를 지정하려면 `make:migration` 명령어를 실행할 때 `--path` 옵션을 사용할 수 있습니다. 지정한 경로는 애플리케이션의 기본 경로를 기준으로 한 상대 경로여야 합니다.

> [!NOTE]
> 마이그레이션 스텁은 [stub publishing](/docs/13.x/artisan#stub-customization)을 사용하여 사용자 지정할 수 있습니다.

<a name="squashing-migrations"></a>
<!-- ### Squashing Migrations -->
### Squashing Migrations

<!-- As you build your application, you may accumulate more and more migrations over time. This can lead to your `database/migrations` directory becoming bloated with potentially hundreds of migrations. If you would like, you may "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command: -->
애플리케이션을 개발하다 보면 시간이 지나면서 마이그레이션이 점점 더 많이 쌓일 수 있습니다. 이로 인해 `database/migrations` 디렉터리가 수백 개의 마이그레이션으로 비대해질 수 있습니다. 원한다면 마이그레이션을 하나의 SQL 파일로 "스쿼싱"할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행합니다.

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

<!-- When you execute this command, Laravel will write a "schema" file to your application's `database/schema` directory. The schema file's name will correspond to the database connection. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will first execute the SQL statements in the schema file of the database connection you are using. After executing the schema file's SQL statements, Laravel will execute any remaining migrations that were not part of the schema dump. -->
이 명령어를 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉터리에 "schema" 파일을 작성합니다. 스키마 파일의 이름은 데이터베이스 연결에 대응됩니다. 이제 데이터베이스를 마이그레이션하려고 할 때 아직 실행된 다른 마이그레이션이 없다면, Laravel은 먼저 현재 사용하는 데이터베이스 연결의 스키마 파일에 있는 SQL 문을 실행합니다. 스키마 파일의 SQL 문을 실행한 뒤에는, 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 실행합니다.

<!-- If your application's tests use a different database connection than the one you typically use during local development, you should ensure you have dumped a schema file using that database connection so that your tests are able to build your database. You may wish to do this after dumping the database connection you typically use during local development: -->
애플리케이션의 테스트가 로컬 개발 중에 일반적으로 사용하는 것과 다른 데이터베이스 연결을 사용한다면, 테스트가 데이터베이스를 구성할 수 있도록 해당 데이터베이스 연결을 사용해 스키마 파일을 덤프해 두어야 합니다. 일반적으로 로컬 개발 중에 사용하는 데이터베이스 연결을 덤프한 뒤 다음 작업을 수행하는 것이 좋습니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

<!-- You should commit your database schema file to source control so that other new developers on your team may quickly create your application's initial database structure. -->
팀의 다른 신규 개발자가 애플리케이션의 초기 데이터베이스 구조를 빠르게 만들 수 있도록, 데이터베이스 스키마 파일을 소스 컨트롤에 커밋해야 합니다.

> [!WARNING]
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL, SQLite 데이터베이스에서만 사용할 수 있으며 데이터베이스의 명령줄 클라이언트를 사용합니다.

<a name="migration-structure"></a>
<!-- ## Migration Structure -->
## Migration Structure

<!-- A migration class contains two methods: `up` and `down`. The `up` method is used to add new tables, columns, or indexes to your database, while the `down` method should reverse the operations performed by the `up` method. -->
마이그레이션 클래스에는 `up`과 `down` 두 개의 메서드가 포함됩니다. `up` 메서드는 데이터베이스에 새 테이블, 컬럼 또는 인덱스를 추가하는 데 사용되며, `down` 메서드는 `up` 메서드가 수행한 작업을 되돌려야 합니다.

<!-- Within both of these methods, you may use the Laravel schema builder to expressively create and modify tables. To learn about all of the methods available on the `Schema` builder, [check out its documentation](#creating-tables). For example, the following migration creates a `flights` table: -->
이 두 메서드 안에서는 Laravel 스키마 빌더를 사용하여 테이블을 표현력 있게 생성하고 수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메서드를 알아보려면 [check out its documentation](#creating-tables). 예를 들어, 다음 마이그레이션은 `flights` 테이블을 생성합니다.

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
마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 데이터베이스 연결과 상호작용해야 한다면, 마이그레이션의 `$connection` 속성을 설정해야 합니다.

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
때로는 아직 활성화되지 않은 기능을 지원하기 위한 마이그레이션이 있을 수 있으며, 이 마이그레이션을 아직 실행하고 싶지 않을 수 있습니다. 이 경우 마이그레이션에 `shouldRun` 메서드를 정의할 수 있습니다. `shouldRun` 메서드가 `false`를 반환하면 해당 마이그레이션은 건너뜁니다.

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
아직 실행되지 않은 모든 마이그레이션을 실행하려면 `migrate` Artisan 명령어를 실행합니다.

```shell
php artisan migrate
```

<!-- If you would like to see which migrations have already run and which are still pending, you may use the `migrate:status` Artisan command: -->
이미 실행된 마이그레이션과 아직 대기 중인 마이그레이션을 확인하려면 `migrate:status` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan migrate:status
```

<!-- If you provide the `--step` option to the `migrate` command, the command will run each migration as its own batch, allowing you to roll back individual migrations later using the `migrate:rollback` command: -->
`migrate` 명령어에 `--step` 옵션을 제공하면, 명령어는 각 마이그레이션을 별도의 배치로 실행합니다. 이렇게 하면 나중에 `migrate:rollback` 명령어를 사용하여 개별 마이그레이션을 롤백할 수 있습니다.

```shell
php artisan migrate --step
```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate` command: -->
마이그레이션을 실제로 실행하지 않고 실행될 SQL 문만 확인하려면 `migrate` 명령어에 `--pretend` 플래그를 제공할 수 있습니다.

```shell
php artisan migrate --pretend
```

<a name="isolating-migration-execution"></a>
<!-- #### Isolating Migration Execution -->
#### Isolating Migration Execution

<!-- If you are deploying your application across multiple servers and running migrations as part of your deployment process, you likely do not want two servers attempting to migrate the database at the same time. To avoid this, you may use the `isolated` option when invoking the `migrate` command. -->
여러 서버에 애플리케이션을 배포하고, 배포 과정의 일부로 마이그레이션을 실행한다면 두 서버가 동시에 데이터베이스 마이그레이션을 시도하는 상황은 피하고 싶을 것입니다. 이를 방지하려면 `migrate` 명령어를 호출할 때 `isolated` 옵션을 사용할 수 있습니다.

<!-- When the `isolated` option is provided, Laravel will acquire an atomic lock using your application's cache driver before attempting to run your migrations. All other attempts to run the `migrate` command while that lock is held will not execute; however, the command will still exit with a successful exit status code: -->
`isolated` 옵션이 제공되면 Laravel은 마이그레이션 실행을 시도하기 전에 애플리케이션의 캐시 드라이버를 사용하여 atomic lock(원자적 잠금)을 획득합니다. 해당 잠금이 유지되는 동안 `migrate` 명령어를 실행하려는 다른 모든 시도는 실행되지 않습니다. 다만 명령어는 여전히 성공 종료 상태 코드로 종료됩니다.

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 캐시 드라이버를 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
<!-- #### Forcing Migrations to Run in Production -->
#### Forcing Migrations to Run in Production

<!-- Some migration operations are destructive, which means they may cause you to lose data. In order to protect you from running these commands against your production database, you will be prompted for confirmation before the commands are executed. To force the commands to run without a prompt, use the `--force` flag: -->
일부 마이그레이션 작업은 파괴적입니다. 즉, 데이터가 손실될 수 있습니다. 프로덕션 데이터베이스에 대해 이러한 명령어를 실행하는 것을 방지하기 위해, 명령어가 실행되기 전에 확인을 요청받게 됩니다. 프롬프트 없이 명령어를 강제로 실행하려면 `--force` 플래그를 사용합니다.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
<!-- ### Rolling Back Migrations -->
### Rolling Back Migrations

<!-- To roll back the latest migration operation, you may use the `rollback` Artisan command. This command rolls back the last "batch" of migrations, which may include multiple migration files: -->
가장 최근의 마이그레이션 작업을 롤백하려면 `rollback` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 마지막 마이그레이션 "배치"를 롤백하며, 여기에는 여러 마이그레이션 파일이 포함될 수 있습니다.

```shell
php artisan migrate:rollback
```

<!-- You may roll back a limited number of migrations by providing the `step` option to the `rollback` command. For example, the following command will roll back the last five migrations: -->
`rollback` 명령어에 `step` 옵션을 제공하여 제한된 수의 마이그레이션만 롤백할 수 있습니다. 예를 들어, 다음 명령어는 마지막 다섯 개의 마이그레이션을 롤백합니다.

```shell
php artisan migrate:rollback --step=5
```

<!-- You may roll back a specific "batch" of migrations by providing the `batch` option to the `rollback` command, where the `batch` option corresponds to a batch value within your application's `migrations` database table. For example, the following command will roll back all migrations in batch three: -->
`rollback` 명령어에 `batch` 옵션을 제공하여 특정 마이그레이션 "배치"를 롤백할 수 있습니다. 여기서 `batch` 옵션은 애플리케이션의 `migrations` 데이터베이스 테이블 안에 있는 배치 값에 대응됩니다. 예를 들어, 다음 명령어는 배치 3에 속한 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:rollback --batch=3
```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate:rollback` command: -->
마이그레이션을 실제로 실행하지 않고 실행될 SQL 문만 확인하려면 `migrate:rollback` 명령어에 `--pretend` 플래그를 제공할 수 있습니다.

```shell
php artisan migrate:rollback --pretend
```

<!-- The `migrate:reset` command will roll back all of your application's migrations: -->
`migrate:reset` 명령어는 애플리케이션의 모든 마이그레이션을 롤백합니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
<!-- #### Roll Back and Migrate Using a Single Command -->
#### Roll Back and Migrate Using a Single Command

<!-- The `migrate:refresh` command will roll back all of your migrations and then execute the `migrate` command. This command effectively re-creates your entire database: -->
`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 뒤 `migrate` 명령어를 실행합니다. 이 명령어는 사실상 전체 데이터베이스를 다시 생성합니다.

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

<!-- You may roll back and re-migrate a limited number of migrations by providing the `step` option to the `refresh` command. For example, the following command will roll back and re-migrate the last five migrations: -->
`refresh` 명령어에 `step` 옵션을 제공하여 제한된 수의 마이그레이션만 롤백하고 다시 마이그레이션할 수 있습니다. 예를 들어, 다음 명령어는 마지막 다섯 개의 마이그레이션을 롤백한 뒤 다시 마이그레이션합니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
<!-- #### Drop All Tables and Migrate -->
#### Drop All Tables and Migrate

<!-- The `migrate:fresh` command will drop all tables from the database and then execute the `migrate` command: -->
`migrate:fresh` 명령어는 데이터베이스에서 모든 테이블을 삭제한 뒤 `migrate` 명령어를 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

<!-- By default, the `migrate:fresh` command only drops tables from the default database connection. However, you may use the `--database` option to specify the database connection that should be migrated. The database connection name should correspond to a connection defined in your application's `database` [configuration file](/docs/13.x/configuration): -->
기본적으로 `migrate:fresh` 명령어는 기본 데이터베이스 연결의 테이블만 삭제합니다. 하지만 `--database` 옵션을 사용해 마이그레이션할 데이터베이스 연결을 지정할 수 있습니다. 데이터베이스 연결 이름은 애플리케이션의 `database` [configuration file](/docs/13.x/configuration)에 정의된 연결과 일치해야 합니다:

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 접두사가 무엇이든 관계없이 모든 데이터베이스 테이블을 삭제합니다. 다른 애플리케이션과 공유하는 데이터베이스를 사용해 개발할 때는 이 명령어를 주의해서 사용해야 합니다.

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<a name="creating-tables"></a>
<!-- ### Creating Tables -->
### Creating Tables

<!-- To create a new database table, use the `create` method on the `Schema` facade. The `create` method accepts two arguments: the first is the name of the table, while the second is a closure which receives a `Blueprint` object that may be used to define the new table: -->
새 데이터베이스 테이블을 생성하려면 `Schema` facade의 `create` 메서드를 사용합니다. `create` 메서드는 두 개의 인수를 받습니다. 첫 번째는 테이블 이름이고, 두 번째는 새 테이블을 정의하는 데 사용할 수 있는 `Blueprint` 객체를 전달받는 클로저입니다.

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
테이블을 생성할 때는 스키마 빌더의 [column methods](#creating-columns)를 사용하여 테이블의 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
<!-- #### Determining Table / Column Existence -->
#### Determining Table / Column Existence

<!-- You may determine the existence of a table, column, or index using the `hasTable`, `hasColumn`, and `hasIndex` methods: -->
`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용하여 테이블, 컬럼 또는 인덱스가 존재하는지 확인할 수 있습니다.

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
애플리케이션의 기본 연결이 아닌 데이터베이스 연결에서 스키마 작업을 수행하려면 `connection` 메서드를 사용합니다.

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

<!-- In addition, a few other properties and methods may be used to define other aspects of the table's creation. The `engine` property may be used to specify the table's storage engine when using MariaDB or MySQL: -->
또한 테이블 생성의 다른 측면을 정의하기 위해 몇 가지 다른 속성과 메서드를 사용할 수 있습니다. MariaDB 또는 MySQL을 사용할 때는 `engine` 속성을 사용하여 테이블의 스토리지 엔진을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```

<!-- The `charset` and `collation` properties may be used to specify the character set and collation for the created table when using MariaDB or MySQL: -->
MariaDB 또는 MySQL을 사용할 때는 `charset`과 `collation` 속성을 사용하여 생성되는 테이블의 문자 집합과 collation(정렬 규칙)을 지정할 수 있습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```

<!-- The `temporary` method may be used to indicate that the table should be "temporary". Temporary tables are only visible to the current connection's database session and are dropped automatically when the connection is closed: -->
`temporary` 메서드는 해당 테이블이 "임시" 테이블이어야 함을 나타내는 데 사용할 수 있습니다. 임시 테이블은 현재 연결의 데이터베이스 세션에서만 보이며, 연결이 닫히면 자동으로 삭제됩니다.

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

<!-- If you would like to add a "comment" to a database table, you may invoke the `comment` method on the table instance. Table comments are currently only supported by MariaDB, MySQL, and PostgreSQL: -->
데이터베이스 테이블에 "comment"를 추가하려면 테이블 인스턴스에서 `comment` 메서드를 호출할 수 있습니다. 테이블 주석은 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다.

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
`Schema` facade의 `table` 메서드는 기존 테이블을 수정하는 데 사용할 수 있습니다. `create` 메서드와 마찬가지로 `table` 메서드는 두 개의 인수를 받습니다. 테이블 이름과, 테이블에 컬럼이나 인덱스를 추가하는 데 사용할 수 있는 `Blueprint` 인스턴스를 전달받는 클로저입니다.

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
기존 데이터베이스 테이블의 이름을 변경하려면 `rename` 메서드를 사용합니다.

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```

<!-- To drop an existing table, you may use the `drop` or `dropIfExists` methods: -->
기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 메서드를 사용할 수 있습니다.

```php
Schema::drop('users');

Schema::dropIfExists('users');
```

<a name="renaming-tables-with-foreign-keys"></a>
<!-- #### Renaming Tables With Foreign Keys -->
#### Renaming Tables With Foreign Keys

<!-- Before renaming a table, you should verify that any foreign key constraints on the table have an explicit name in your migration files instead of letting Laravel assign a convention based name. Otherwise, the foreign key constraint name will refer to the old table name. -->
테이블 이름을 변경하기 전에, Laravel이 규칙 기반 이름을 자동으로 지정하도록 두지 말고 해당 테이블의 모든 외래 키 제약 조건에 명시적인 이름이 마이그레이션 파일에 지정되어 있는지 확인해야 합니다. 그렇지 않으면 외래 키 제약 조건 이름이 이전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
<!-- ## Columns -->
## Columns

<a name="creating-columns"></a>
<!-- ### Creating Columns -->
### Creating Columns

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives an `Illuminate\Database\Schema\Blueprint` instance you may use to add columns to the table: -->
`Schema` 파사드의 `table` 메서드는 기존 테이블을 업데이트할 때 사용할 수 있습니다. `create` 메서드와 마찬가지로 `table` 메서드는 두 개의 인수를 받습니다. 테이블 이름과, 테이블에 컬럼을 추가할 때 사용할 수 있는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저입니다.

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
스키마 빌더 블루프린트는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 대응하는 여러 메서드를 제공합니다. 사용 가능한 각 메서드는 아래 표에 나열되어 있습니다.

<a name="booleans-method-list"></a>
<!-- #### Boolean Types -->
#### Boolean Types

<div class="collection-method-list" markdown="1">

<!-- [boolean](#column-method-boolean) -->
[boolean](#column-method-boolean)

</div>

<a name="strings-and-texts-method-list"></a>
<!-- #### String & Text Types -->
#### String & Text Types

<div class="collection-method-list" markdown="1">

<!-- [char](#column-method-char) [longText](#column-method-longText) [mediumText](#column-method-mediumText) [string](#column-method-string) [text](#column-method-text) [tinyText](#column-method-tinyText) -->
[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

<a name="numbers--method-list"></a>
<!-- #### Numeric Types -->
#### Numeric Types

<div class="collection-method-list" markdown="1">

<!-- [bigIncrements](#column-method-bigIncrements) [bigInteger](#column-method-bigInteger) [decimal](#column-method-decimal) [double](#column-method-double) [float](#column-method-float) [id](#column-method-id) [increments](#column-method-increments) [integer](#column-method-integer) [mediumIncrements](#column-method-mediumIncrements) [mediumInteger](#column-method-mediumInteger) [smallIncrements](#column-method-smallIncrements) [smallInteger](#column-method-smallInteger) [tinyIncrements](#column-method-tinyIncrements) [tinyInteger](#column-method-tinyInteger) [unsignedBigInteger](#column-method-unsignedBigInteger) [unsignedInteger](#column-method-unsignedInteger) [unsignedMediumInteger](#column-method-unsignedMediumInteger) [unsignedSmallInteger](#column-method-unsignedSmallInteger) [unsignedTinyInteger](#column-method-unsignedTinyInteger) -->
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

</div>

<a name="dates-and-times-method-list"></a>
<!-- #### Date & Time Types -->
#### Date & Time Types

<div class="collection-method-list" markdown="1">

<!-- [dateTime](#column-method-dateTime) [dateTimeTz](#column-method-dateTimeTz) [date](#column-method-date) [time](#column-method-time) [timeTz](#column-method-timeTz) [timestamp](#column-method-timestamp) [timestamps](#column-method-timestamps) [timestampsTz](#column-method-timestampsTz) [softDeletes](#column-method-softDeletes) [softDeletesTz](#column-method-softDeletesTz) [year](#column-method-year) -->
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

</div>

<a name="binaries-method-list"></a>
<!-- #### Binary Types -->
#### Binary Types

<div class="collection-method-list" markdown="1">

<!-- [binary](#column-method-binary) -->
[binary](#column-method-binary)

</div>

<a name="object-and-jsons-method-list"></a>
<!-- #### Object & Json Types -->
#### Object & Json Types

<div class="collection-method-list" markdown="1">

<!-- [json](#column-method-json) [jsonb](#column-method-jsonb) -->
[json](#column-method-json)
[jsonb](#column-method-jsonb)

</div>

<a name="uuids-and-ulids-method-list"></a>
<!-- #### UUID & ULID Types -->
#### UUID & ULID Types

<div class="collection-method-list" markdown="1">

<!-- [ulid](#column-method-ulid) [ulidMorphs](#column-method-ulidMorphs) [uuid](#column-method-uuid) [uuidMorphs](#column-method-uuidMorphs) [nullableUlidMorphs](#column-method-nullableUlidMorphs) [nullableUuidMorphs](#column-method-nullableUuidMorphs) -->
[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

<a name="spatials-method-list"></a>
<!-- #### Spatial Types -->
#### Spatial Types

<div class="collection-method-list" markdown="1">

<!-- [geography](#column-method-geography) [geometry](#column-method-geometry) -->
[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

<a name="relationship-method-list"></a>
<!-- #### Relationship Types -->
#### Relationship Types

<div class="collection-method-list" markdown="1">

<!-- [foreignId](#column-method-foreignId) [foreignIdFor](#column-method-foreignIdFor) [foreignUlid](#column-method-foreignUlid) [foreignUuid](#column-method-foreignUuid) [foreignUuidFor](#column-method-foreignUuidFor) [morphs](#column-method-morphs) [nullableMorphs](#column-method-nullableMorphs) -->
[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[foreignUuidFor](#column-method-foreignUuidFor)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

<a name="specifics-method-list"></a>
<!-- #### Specialty Types -->
#### Specialty Types

<div class="collection-method-list" markdown="1">

<!-- [enum](#column-method-enum) [set](#column-method-set) [macAddress](#column-method-macAddress) [ipAddress](#column-method-ipAddress) [rememberToken](#column-method-rememberToken) [vector](#column-method-vector) -->
[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

<a name="column-method-bigIncrements"></a>
<!-- #### `bigIncrements()` -->
#### `bigIncrements()`

<!-- The `bigIncrements` method creates an auto-incrementing `UNSIGNED BIGINT` (primary key) equivalent column: -->
`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT`(기본 키)에 해당하는 컬럼을 생성합니다.

```php
$table->bigIncrements('id');
```

<a name="column-method-bigInteger"></a>
<!-- #### `bigInteger()` -->
#### `bigInteger()`

<!-- The `bigInteger` method creates a `BIGINT` equivalent column: -->
`bigInteger` 메서드는 `BIGINT`에 해당하는 컬럼을 생성합니다.

```php
$table->bigInteger('votes');
```

<a name="column-method-binary"></a>
<!-- #### `binary()` -->
#### `binary()`

<!-- The `binary` method creates a `BLOB` equivalent column: -->
`binary` 메서드는 `BLOB`에 해당하는 컬럼을 생성합니다.

```php
$table->binary('photo');
```

<!-- When utilizing MySQL, MariaDB, or SQL Server, you may pass `length` and `fixed` arguments to create `VARBINARY` or `BINARY` equivalent column: -->
MySQL, MariaDB 또는 SQL Server를 사용할 때는 `length`와 `fixed` 인수를 전달하여 `VARBINARY` 또는 `BINARY`에 해당하는 컬럼을 생성할 수 있습니다.

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```

<a name="column-method-boolean"></a>
<!-- #### `boolean()` -->
#### `boolean()`

<!-- The `boolean` method creates a `BOOLEAN` equivalent column: -->
`boolean` 메서드는 `BOOLEAN`에 해당하는 컬럼을 생성합니다.

```php
$table->boolean('confirmed');
```

<a name="column-method-char"></a>
<!-- #### `char()` -->
#### `char()`

<!-- The `char` method creates a `CHAR` equivalent column with of a given length: -->
`char` 메서드는 지정한 길이의 `CHAR`에 해당하는 컬럼을 생성합니다.

```php
$table->char('name', length: 100);
```

<a name="column-method-dateTimeTz"></a>
<!-- #### `dateTimeTz()` -->
#### `dateTimeTz()`

<!-- The `dateTimeTz` method creates a `DATETIME` (with timezone) equivalent column with an optional fractional seconds precision: -->
`dateTimeTz` 메서드는 선택적으로 초의 소수점 정밀도를 지정할 수 있는 `DATETIME`(타임존 포함)에 해당하는 컬럼을 생성합니다.

```php
$table->dateTimeTz('created_at', precision: 0);
```

<a name="column-method-dateTime"></a>
<!-- #### `dateTime()` -->
#### `dateTime()`

<!-- The `dateTime` method creates a `DATETIME` equivalent column with an optional fractional seconds precision: -->
`dateTime` 메서드는 선택적으로 초의 소수점 정밀도를 지정할 수 있는 `DATETIME`에 해당하는 컬럼을 생성합니다.

```php
$table->dateTime('created_at', precision: 0);
```

<a name="column-method-date"></a>
<!-- #### `date()` -->
#### `date()`

<!-- The `date` method creates a `DATE` equivalent column: -->
`date` 메서드는 `DATE`에 해당하는 컬럼을 생성합니다.

```php
$table->date('created_at');
```

<a name="column-method-decimal"></a>
<!-- #### `decimal()` -->
#### `decimal()`

<!-- The `decimal` method creates a `DECIMAL` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`decimal` 메서드는 지정한 정밀도(전체 자릿수)와 스케일(소수 자릿수)을 가진 `DECIMAL`에 해당하는 컬럼을 생성합니다.

```php
$table->decimal('amount', total: 8, places: 2);
```

<a name="column-method-double"></a>
<!-- #### `double()` -->
#### `double()`

<!-- The `double` method creates a `DOUBLE` equivalent column: -->
`double` 메서드는 `DOUBLE`에 해당하는 컬럼을 생성합니다.

```php
$table->double('amount');
```

<a name="column-method-enum"></a>
<!-- #### `enum()` -->
#### `enum()`

<!-- The `enum` method creates a `ENUM` equivalent column with the given valid values: -->
`enum` 메서드는 지정한 유효 값들을 가진 `ENUM`에 해당하는 컬럼을 생성합니다.

```php
$table->enum('difficulty', ['easy', 'hard']);
```

<!-- Of course, you may use the `Enum::cases()` method instead of manually defining an array of allowed values: -->
물론 허용 값 배열을 직접 정의하는 대신 `Enum::cases()` 메서드를 사용할 수도 있습니다.

```php
use App\Enums\Difficulty;

$table->enum('difficulty', Difficulty::cases());
```

<a name="column-method-float"></a>
<!-- #### `float()` -->
#### `float()`

<!-- The `float` method creates a `FLOAT` equivalent column with the given precision: -->
`float` 메서드는 지정한 정밀도를 가진 `FLOAT`에 해당하는 컬럼을 생성합니다.

```php
$table->float('amount', precision: 53);
```

<a name="column-method-foreignId"></a>
<!-- #### `foreignId()` -->
#### `foreignId()`

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column: -->
`foreignId` 메서드는 `UNSIGNED BIGINT`에 해당하는 컬럼을 생성합니다.

```php
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
<!-- #### `foreignIdFor()` -->
#### `foreignIdFor()`

<!-- The `foreignIdFor` method adds a `{column}_id` equivalent column for a given model class. The column type will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type: -->
`foreignIdFor` 메서드는 지정한 모델 클래스에 대해 `{column}_id`에 해당하는 컬럼을 추가합니다. 컬럼 타입은 모델 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)` 또는 `CHAR(26)`이 됩니다.

```php
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
<!-- #### `foreignUlid()` -->
#### `foreignUlid()`

<!-- The `foreignUlid` method creates a `ULID` equivalent column: -->
`foreignUlid` 메서드는 `ULID`에 해당하는 컬럼을 생성합니다.

```php
$table->foreignUlid('user_id');
```

<a name="column-method-foreignUuid"></a>
<!-- #### `foreignUuid()` -->
#### `foreignUuid()`

<!-- The `foreignUuid` method creates a `UUID` equivalent column: -->
`foreignUuid` 메서드는 `UUID`에 해당하는 컬럼을 생성합니다.

```php
$table->foreignUuid('user_id');
```

<a name="column-method-foreignUuidFor"></a>
<!-- #### `foreignUuidFor()` -->
#### `foreignUuidFor()`

<!-- The `foreignUuidFor` method adds a `{column}_id` UUID equivalent column for a given model class: -->
`foreignUuidFor` 메서드는 지정한 모델 클래스에 대해 `{column}_id` UUID에 해당하는 컬럼을 추가합니다.

```php
$table->foreignUuidFor(User::class);
```

<a name="column-method-geography"></a>
<!-- #### `geography()` -->
#### `geography()`

<!-- The `geography` method creates a `GEOGRAPHY` equivalent column with the given spatial type and SRID (Spatial Reference System Identifier): -->
`geography` 메서드는 지정한 공간 타입과 SRID(Spatial Reference System Identifier, 공간 참조 시스템 식별자)를 가진 `GEOGRAPHY`에 해당하는 컬럼을 생성합니다.

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```

> [!NOTE]
> 공간 타입 지원 여부는 데이터베이스 드라이버에 따라 달라집니다. 데이터베이스 문서를 참조하세요. 애플리케이션에서 PostgreSQL 데이터베이스를 사용한다면 `geography` 메서드를 사용하기 전에 [PostGIS](https://postgis.net) 확장 기능을 설치해야 합니다.

<a name="column-method-geometry"></a>
<!-- #### `geometry()` -->
#### `geometry()`

<!-- The `geometry` method creates a `GEOMETRY` equivalent column with the given spatial type and SRID (Spatial Reference System Identifier): -->
`geometry` 메서드는 지정한 공간 타입과 SRID(Spatial Reference System Identifier, 공간 참조 시스템 식별자)를 가진 `GEOMETRY`에 해당하는 컬럼을 생성합니다.

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```

> [!NOTE]
> 공간 타입 지원 여부는 데이터베이스 드라이버에 따라 달라집니다. 사용하는 데이터베이스의 문서를 참조하세요. 애플리케이션에서 PostgreSQL 데이터베이스를 사용한다면 `geometry` 메서드를 사용하기 전에 [PostGIS](https://postgis.net) 확장 기능을 설치해야 합니다.

<a name="column-method-id"></a>
<!-- #### `id()` -->
#### `id()`

<!-- The `id` method is an alias of the `bigIncrements` method. By default, the method will create an `id` column; however, you may pass a column name if you would like to assign a different name to the column: -->
`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 이 메서드는 `id` 컬럼을 생성합니다. 하지만 컬럼에 다른 이름을 지정하고 싶다면 컬럼 이름을 전달할 수 있습니다.

```php
$table->id();
```

<a name="column-method-increments"></a>
<!-- #### `increments()` -->
#### `increments()`

<!-- The `increments` method creates an auto-incrementing `UNSIGNED INTEGER` equivalent column as a primary key: -->
`increments` 메서드는 기본 키로 사용할 자동 증가 `UNSIGNED INTEGER`에 해당하는 컬럼을 생성합니다.

```php
$table->increments('id');
```

<a name="column-method-integer"></a>
<!-- #### `integer()` -->
#### `integer()`

<!-- The `integer` method creates an `INTEGER` equivalent column: -->
`integer` 메서드는 `INTEGER`에 해당하는 컬럼을 생성합니다.

```php
$table->integer('votes');
```

<a name="column-method-ipAddress"></a>
<!-- #### `ipAddress()` -->
#### `ipAddress()`

<!-- The `ipAddress` method creates a `VARCHAR` equivalent column: -->
`ipAddress` 메서드는 `VARCHAR`에 해당하는 컬럼을 생성합니다.

```php
$table->ipAddress('visitor');
```

<!-- When using PostgreSQL, an `INET` column will be created. -->
PostgreSQL을 사용할 때는 `INET` 컬럼이 생성됩니다.

<a name="column-method-json"></a>
<!-- #### `json()` -->
#### `json()`

<!-- The `json` method creates a `JSON` equivalent column: -->
`json` 메서드는 `JSON`에 해당하는 컬럼을 생성합니다.

```php
$table->json('options');
```

<!-- When using SQLite, a `TEXT` column will be created. -->
SQLite를 사용하는 경우 `TEXT` 컬럼이 생성됩니다.

<a name="column-method-jsonb"></a>
<!-- #### `jsonb()` -->
#### `jsonb()`

<!-- The `jsonb` method creates a `JSONB` equivalent column: -->
`jsonb` 메서드는 `JSONB`에 해당하는 컬럼을 생성합니다.

```php
$table->jsonb('options');
```

<!-- When using SQLite, a `TEXT` column will be created. -->
SQLite를 사용하는 경우 `TEXT` 컬럼이 생성됩니다.

<a name="column-method-longText"></a>
<!-- #### `longText()` -->
#### `longText()`

<!-- The `longText` method creates a `LONGTEXT` equivalent column: -->
`longText` 메서드는 `LONGTEXT`에 해당하는 컬럼을 생성합니다.

```php
$table->longText('description');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `LONGBLOB` equivalent column: -->
MySQL 또는 MariaDB를 사용할 때는 컬럼에 `binary` 문자 집합을 적용하여 `LONGBLOB`에 해당하는 컬럼을 생성할 수 있습니다.

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```

<a name="column-method-macAddress"></a>
<!-- #### `macAddress()` -->
#### `macAddress()`

<!-- The `macAddress` method creates a column that is intended to hold a MAC address. Some database systems, such as PostgreSQL, have a dedicated column type for this type of data. Other database systems will use a string equivalent column: -->
`macAddress` 메서드는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. PostgreSQL과 같은 일부 데이터베이스 시스템은 이런 데이터 전용 컬럼 타입을 제공합니다. 다른 데이터베이스 시스템에서는 문자열에 해당하는 컬럼을 사용합니다.

```php
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
<!-- #### `mediumIncrements()` -->
#### `mediumIncrements()`

<!-- The `mediumIncrements` method creates an auto-incrementing `UNSIGNED MEDIUMINT` equivalent column as a primary key: -->
`mediumIncrements` 메서드는 기본 키로 사용할 자동 증가 `UNSIGNED MEDIUMINT`에 해당하는 컬럼을 생성합니다.

```php
$table->mediumIncrements('id');
```

<a name="column-method-mediumInteger"></a>
<!-- #### `mediumInteger()` -->
#### `mediumInteger()`

<!-- The `mediumInteger` method creates a `MEDIUMINT` equivalent column: -->
`mediumInteger` 메서드는 `MEDIUMINT`에 해당하는 컬럼을 생성합니다.

```php
$table->mediumInteger('votes');
```

<a name="column-method-mediumText"></a>
<!-- #### `mediumText()` -->
#### `mediumText()`

<!-- The `mediumText` method creates a `MEDIUMTEXT` equivalent column: -->
`mediumText` 메서드는 `MEDIUMTEXT`에 해당하는 컬럼을 생성합니다.

```php
$table->mediumText('description');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `MEDIUMBLOB` equivalent column: -->
MySQL 또는 MariaDB를 사용할 때는 컬럼에 `binary` 문자 집합을 적용하여 `MEDIUMBLOB`에 해당하는 컬럼을 생성할 수 있습니다.

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```

<a name="column-method-morphs"></a>
<!-- #### `morphs()` -->
#### `morphs()`

<!-- The `morphs` method is a convenience method that adds a `{column}_type` `VARCHAR` equivalent column and a `{column}_id` equivalent column. The column type for the `{column}_id` will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type. -->
`morphs` 메서드는 `{column}_type` `VARCHAR`에 해당하는 컬럼과 `{column}_id`에 해당하는 컬럼을 추가하는 편의 메서드입니다. `{column}_id`의 컬럼 타입은 모델 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, 또는 `CHAR(26)`이 됩니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/13.x/eloquent-relationships). In the following example, `taggable_type` and `taggable_id` columns would be created: -->
이 메서드는 다형성 [Eloquent relationship](/docs/13.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용합니다. 다음 예시에서는 `taggable_type` 및 `taggable_id` 컬럼이 생성됩니다:

```php
$table->morphs('taggable');
```

<a name="column-method-nullableMorphs"></a>
<!-- #### `nullableMorphs()` -->
#### `nullableMorphs()`

<!-- The method is similar to the [morphs](#column-method-morphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [morphs](#column-method-morphs) 메서드와 비슷하지만, 생성되는 컬럼이 널을 허용합니다.

```php
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
<!-- #### `nullableUlidMorphs()` -->
#### `nullableUlidMorphs()`

<!-- The method is similar to the [ulidMorphs](#column-method-ulidMorphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [ulidMorphs](#column-method-ulidMorphs) 메서드와 비슷하지만, 생성되는 컬럼이 널을 허용합니다.

```php
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
<!-- #### `nullableUuidMorphs()` -->
#### `nullableUuidMorphs()`

<!-- The method is similar to the [uuidMorphs](#column-method-uuidMorphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [uuidMorphs](#column-method-uuidMorphs) 메서드와 비슷하지만, 생성되는 컬럼이 널을 허용합니다.

```php
$table->nullableUuidMorphs('taggable');
```

<a name="column-method-rememberToken"></a>
<!-- #### `rememberToken()` -->
#### `rememberToken()`

<!-- The `rememberToken` method creates a nullable, `VARCHAR(100)` equivalent column that is intended to store the current "remember me" [authentication token](/docs/13.x/authentication#remembering-users): -->
`rememberToken` 메서드는 현재 "로그인 상태 기억" [authentication token](/docs/13.x/authentication#remembering-users)을 저장하기 위한 nullable `VARCHAR(100)`과 동일한 컬럼을 생성합니다:

```php
$table->rememberToken();
```

<a name="column-method-set"></a>
<!-- #### `set()` -->
#### `set()`

<!-- The `set` method creates a `SET` equivalent column with the given list of valid values: -->
`set` 메서드는 주어진 유효한 값 목록을 가진 `SET`에 해당하는 컬럼을 생성합니다.

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
<!-- #### `smallIncrements()` -->
#### `smallIncrements()`

<!-- The `smallIncrements` method creates an auto-incrementing `UNSIGNED SMALLINT` equivalent column as a primary key: -->
`smallIncrements` 메서드는 기본 키로 사용할 자동 증가 `UNSIGNED SMALLINT`에 해당하는 컬럼을 생성합니다.

```php
$table->smallIncrements('id');
```

<a name="column-method-smallInteger"></a>
<!-- #### `smallInteger()` -->
#### `smallInteger()`

<!-- The `smallInteger` method creates a `SMALLINT` equivalent column: -->
`smallInteger` 메서드는 `SMALLINT`에 해당하는 컬럼을 생성합니다.

```php
$table->smallInteger('votes');
```

<a name="column-method-softDeletesTz"></a>
<!-- #### `softDeletesTz()` -->
#### `softDeletesTz()`

<!-- The `softDeletesTz` method adds a nullable `deleted_at` `TIMESTAMP` (with timezone) equivalent column with an optional fractional seconds precision. This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletesTz` 메서드는 선택적인 소수 초 정밀도를 가진, 널을 허용하는 `deleted_at` `TIMESTAMP`(시간대 포함)에 해당하는 컬럼을 추가합니다. 이 컬럼은 Eloquent의 "소프트 삭제" 기능에 필요한 `deleted_at` 타임스탬프를 저장하기 위한 것입니다.

```php
$table->softDeletesTz('deleted_at', precision: 0);
```

<a name="column-method-softDeletes"></a>
<!-- #### `softDeletes()` -->
#### `softDeletes()`

<!-- The `softDeletes` method adds a nullable `deleted_at` `TIMESTAMP` equivalent column with an optional fractional seconds precision. This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletes` 메서드는 선택적인 소수 초 정밀도를 가진, 널을 허용하는 `deleted_at` `TIMESTAMP`에 해당하는 컬럼을 추가합니다. 이 컬럼은 Eloquent의 "소프트 삭제" 기능에 필요한 `deleted_at` 타임스탬프를 저장하기 위한 것입니다.

```php
$table->softDeletes('deleted_at', precision: 0);
```

<a name="column-method-string"></a>
<!-- #### `string()` -->
#### `string()`

<!-- The `string` method creates a `VARCHAR` equivalent column of the given length: -->
`string` 메서드는 주어진 길이의 `VARCHAR`에 해당하는 컬럼을 생성합니다.

```php
$table->string('name', length: 100);
```

<a name="column-method-text"></a>
<!-- #### `text()` -->
#### `text()`

<!-- The `text` method creates a `TEXT` equivalent column: -->
`text` 메서드는 `TEXT`에 해당하는 컬럼을 생성합니다.

```php
$table->text('description');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `BLOB` equivalent column: -->
MySQL 또는 MariaDB를 사용할 때는 컬럼에 `binary` 문자 집합을 적용하여 `BLOB`에 해당하는 컬럼을 생성할 수 있습니다.

```php
$table->text('data')->charset('binary'); // BLOB
```

<a name="column-method-timeTz"></a>
<!-- #### `timeTz()` -->
#### `timeTz()`

<!-- The `timeTz` method creates a `TIME` (with timezone) equivalent column with an optional fractional seconds precision: -->
`timeTz` 메서드는 선택적인 소수 초 정밀도를 가진 `TIME`(시간대 포함)에 해당하는 컬럼을 생성합니다.

```php
$table->timeTz('sunrise', precision: 0);
```

<a name="column-method-time"></a>
<!-- #### `time()` -->
#### `time()`

<!-- The `time` method creates a `TIME` equivalent column with an optional fractional seconds precision: -->
`time` 메서드는 선택적인 소수 초 정밀도를 가진 `TIME`에 해당하는 컬럼을 생성합니다.

```php
$table->time('sunrise', precision: 0);
```

<a name="column-method-timestampTz"></a>
<!-- #### `timestampTz()` -->
#### `timestampTz()`

<!-- The `timestampTz` method creates a `TIMESTAMP` (with timezone) equivalent column with an optional fractional seconds precision: -->
`timestampTz` 메서드는 선택적인 소수 초 정밀도를 가진 `TIMESTAMP`(시간대 포함)에 해당하는 컬럼을 생성합니다.

```php
$table->timestampTz('added_at', precision: 0);
```

<a name="column-method-timestamp"></a>
<!-- #### `timestamp()` -->
#### `timestamp()`

<!-- The `timestamp` method creates a `TIMESTAMP` equivalent column with an optional fractional seconds precision: -->
`timestamp` 메서드는 선택적인 소수 초 정밀도를 가진 `TIMESTAMP`에 해당하는 컬럼을 생성합니다.

```php
$table->timestamp('added_at', precision: 0);
```

<a name="column-method-timestampsTz"></a>
<!-- #### `timestampsTz()` -->
#### `timestampsTz()`

<!-- The `timestampsTz` method creates `created_at` and `updated_at` `TIMESTAMP` (with timezone) equivalent columns with an optional fractional seconds precision: -->
`timestampsTz` 메서드는 선택적인 소수 초 정밀도를 가진 `created_at` 및 `updated_at` `TIMESTAMP`(시간대 포함)에 해당하는 컬럼을 생성합니다.

```php
$table->timestampsTz(precision: 0);
```

<a name="column-method-timestamps"></a>
<!-- #### `timestamps()` -->
#### `timestamps()`

<!-- The `timestamps` method creates `created_at` and `updated_at` `TIMESTAMP` equivalent columns with an optional fractional seconds precision: -->
`timestamps` 메서드는 선택적인 소수 초 정밀도를 가진 `created_at` 및 `updated_at` `TIMESTAMP`에 해당하는 컬럼을 생성합니다.

```php
$table->timestamps(precision: 0);
```

<a name="column-method-tinyIncrements"></a>
<!-- #### `tinyIncrements()` -->
#### `tinyIncrements()`

<!-- The `tinyIncrements` method creates an auto-incrementing `UNSIGNED TINYINT` equivalent column as a primary key: -->
`tinyIncrements` 메서드는 기본 키로 사용할 자동 증가 `UNSIGNED TINYINT`에 해당하는 컬럼을 생성합니다.

```php
$table->tinyIncrements('id');
```

<a name="column-method-tinyInteger"></a>
<!-- #### `tinyInteger()` -->
#### `tinyInteger()`

<!-- The `tinyInteger` method creates a `TINYINT` equivalent column: -->
`tinyInteger` 메서드는 `TINYINT`에 해당하는 컬럼을 생성합니다.

```php
$table->tinyInteger('votes');
```

<a name="column-method-tinyText"></a>
<!-- #### `tinyText()` -->
#### `tinyText()`

<!-- The `tinyText` method creates a `TINYTEXT` equivalent column: -->
`tinyText` 메서드는 `TINYTEXT`에 해당하는 컬럼을 생성합니다.

```php
$table->tinyText('notes');
```

<!-- When utilizing MySQL or MariaDB, you may apply a `binary` character set to the column in order to create a `TINYBLOB` equivalent column: -->
MySQL 또는 MariaDB를 사용할 때는 컬럼에 `binary` 문자 집합을 적용하여 `TINYBLOB`에 해당하는 컬럼을 생성할 수 있습니다.

```php
$table->tinyText('data')->charset('binary'); // TINYBLOB
```

<a name="column-method-unsignedBigInteger"></a>
<!-- #### `unsignedBigInteger()` -->
#### `unsignedBigInteger()`

<!-- The `unsignedBigInteger` method creates an `UNSIGNED BIGINT` equivalent column: -->
`unsignedBigInteger` 메서드는 `UNSIGNED BIGINT`에 해당하는 컬럼을 생성합니다.

```php
$table->unsignedBigInteger('votes');
```

<a name="column-method-unsignedInteger"></a>
<!-- #### `unsignedInteger()` -->
#### `unsignedInteger()`

<!-- The `unsignedInteger` method creates an `UNSIGNED INTEGER` equivalent column: -->
`unsignedInteger` 메서드는 `UNSIGNED INTEGER`에 해당하는 컬럼을 생성합니다.

```php
$table->unsignedInteger('votes');
```

<a name="column-method-unsignedMediumInteger"></a>
<!-- #### `unsignedMediumInteger()` -->
#### `unsignedMediumInteger()`

<!-- The `unsignedMediumInteger` method creates an `UNSIGNED MEDIUMINT` equivalent column: -->
`unsignedMediumInteger` 메서드는 `UNSIGNED MEDIUMINT`에 해당하는 컬럼을 생성합니다.

```php
$table->unsignedMediumInteger('votes');
```

<a name="column-method-unsignedSmallInteger"></a>
<!-- #### `unsignedSmallInteger()` -->
#### `unsignedSmallInteger()`

<!-- The `unsignedSmallInteger` method creates an `UNSIGNED SMALLINT` equivalent column: -->
`unsignedSmallInteger` 메서드는 `UNSIGNED SMALLINT`에 해당하는 컬럼을 생성합니다.

```php
$table->unsignedSmallInteger('votes');
```

<a name="column-method-unsignedTinyInteger"></a>
<!-- #### `unsignedTinyInteger()` -->
#### `unsignedTinyInteger()`

<!-- The `unsignedTinyInteger` method creates an `UNSIGNED TINYINT` equivalent column: -->
`unsignedTinyInteger` 메서드는 `UNSIGNED TINYINT`에 해당하는 컬럼을 생성합니다.

```php
$table->unsignedTinyInteger('votes');
```

<a name="column-method-ulidMorphs"></a>
<!-- #### `ulidMorphs()` -->
#### `ulidMorphs()`

<!-- The `ulidMorphs` method is a convenience method that adds a `{column}_type` `VARCHAR` equivalent column and a `{column}_id` `CHAR(26)` equivalent column. -->
`ulidMorphs` 메서드는 `{column}_type` `VARCHAR`에 해당하는 컬럼과 `{column}_id` `CHAR(26)`에 해당하는 컬럼을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/13.x/eloquent-relationships) that use ULID identifiers. In the following example, `taggable_type` and `taggable_id` columns would be created: -->
이 메서드는 ULID 식별자를 사용하는 다형성 [Eloquent relationship](/docs/13.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용합니다. 다음 예시에서는 `taggable_type` 및 `taggable_id` 컬럼이 생성됩니다:

```php
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
<!-- #### `uuidMorphs()` -->
#### `uuidMorphs()`

<!-- The `uuidMorphs` method is a convenience method that adds a `{column}_type` `VARCHAR` equivalent column and a `{column}_id` `CHAR(36)` equivalent column. -->
`uuidMorphs` 메서드는 `{column}_type` `VARCHAR`에 해당하는 컬럼과 `{column}_id` `CHAR(36)`에 해당하는 컬럼을 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a [polymorphic Eloquent relationship](/docs/13.x/eloquent-relationships#polymorphic-relationships) that use UUID identifiers. In the following example, `taggable_type` and `taggable_id` columns would be created: -->
이 메서드는 UUID 식별자를 사용하는 [polymorphic Eloquent relationship](/docs/13.x/eloquent-relationships#polymorphic-relationships)에 필요한 컬럼을 정의할 때 사용합니다. 다음 예시에서는 `taggable_type` 및 `taggable_id` 컬럼이 생성됩니다:

```php
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
<!-- #### `ulid()` -->
#### `ulid()`

<!-- The `ulid` method creates a `ULID` equivalent column: -->
`ulid` 메서드는 `ULID`에 해당하는 컬럼을 생성합니다.

```php
$table->ulid('id');
```

<a name="column-method-uuid"></a>
<!-- #### `uuid()` -->
#### `uuid()`

<!-- The `uuid` method creates a `UUID` equivalent column: -->
`uuid` 메서드는 `UUID`에 해당하는 컬럼을 생성합니다.

```php
$table->uuid('id');
```

<a name="column-method-vector"></a>
<!-- #### `vector()` -->
#### `vector()`

<!-- The `vector` method creates a `vector` equivalent column: -->
`vector` 메서드는 `vector`에 해당하는 컬럼을 생성합니다.

```php
$table->vector('embedding', dimensions: 100);
```

<!-- When utilizing PostgreSQL, the `pgvector` extension must be loaded before `vector` columns can be created: -->
PostgreSQL을 사용할 때는 `vector` 컬럼을 생성하기 전에 `pgvector` 확장을 로드해야 합니다.

```php
Schema::ensureVectorExtensionExists();
```

<a name="column-method-year"></a>
<!-- #### `year()` -->
#### `year()`

<!-- The `year` method creates a `YEAR` equivalent column: -->
`year` 메서드는 `YEAR`에 해당하는 컬럼을 생성합니다.

```php
$table->year('birth_year');
```

<a name="column-modifiers"></a>
<!-- ### Column Modifiers -->
### Column Modifiers

<!-- In addition to the column types listed above, there are several column "modifiers" you may use when adding a column to a database table. For example, to make the column "nullable", you may use the `nullable` method: -->
위에 나열된 컬럼 타입 외에도, 데이터베이스 테이블에 컬럼을 추가할 때 사용할 수 있는 여러 컬럼 "수정자(modifier)"가 있습니다. 예를 들어, 컬럼을 "nullable"로 만들려면 `nullable` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

<!-- The following table contains all of the available column modifiers. This list does not include [index modifiers](#creating-indexes): -->
다음 표에는 사용할 수 있는 모든 컬럼 수정자가 정리되어 있습니다. 이 목록에는 [index modifiers](#creating-indexes)가 포함되어 있지 않습니다.

<div class="overflow-auto">

<!-- | Modifier | Description | | ----------------------------------- | ---------------------------------------------------------------------------------------------- | | `->after('column')` | Place the column "after" another column (MariaDB / MySQL). | | `->autoIncrement()` | Set `INTEGER` columns as auto-incrementing (primary key). | | `->charset('utf8mb4')` | Specify a character set for the column (MariaDB / MySQL). | | `->collation('utf8mb4_unicode_ci')` | Specify a collation for the column. | | `->comment('my comment')` | Add a comment to a column (MariaDB / MySQL / PostgreSQL). | | `->default($value)` | Specify a "default" value for the column. | | `->first()` | Place the column "first" in the table (MariaDB / MySQL). | | `->from($integer)` | Set the starting value of an auto-incrementing field (MariaDB / MySQL / PostgreSQL). | | `->instant()` | Add or modify the column using an instant operation (MySQL). | | `->invisible()` | Make the column "invisible" to `SELECT *` queries (MariaDB / MySQL). | | `->lock($mode)` | Specify a lock mode for the column operation (MySQL). | | `->nullable($value = true)` | Allow `NULL` values to be inserted into the column. | | `->storedAs($expression)` | Create a stored generated column (MariaDB / MySQL / PostgreSQL / SQLite). | | `->unsigned()` | Set `INTEGER` columns as `UNSIGNED` (MariaDB / MySQL). | | `->using($expression)` | Specify a casting expression when changing the column type (PostgreSQL). | | `->useCurrent()` | Set `TIMESTAMP` columns to use `CURRENT_TIMESTAMP` as default value. | | `->useCurrentOnUpdate()` | Set `TIMESTAMP` columns to use `CURRENT_TIMESTAMP` when a record is updated (MariaDB / MySQL). | | `->virtualAs($expression)` | Create a virtual generated column (MariaDB / MySQL / SQLite). | | `->generatedAs($expression)` | Create an identity column with specified sequence options (PostgreSQL). | | `->always()` | Defines the precedence of sequence values over input for an identity column (PostgreSQL). | -->
| 수정자                              | 설명                                                                                       |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| `->after('column')`                 | 다른 컬럼 "뒤에" 컬럼을 배치합니다(MariaDB / MySQL).                                        |
| `->autoIncrement()`                 | `INTEGER` 컬럼을 자동 증가 컬럼으로 설정합니다(기본 키).                                   |
| `->charset('utf8mb4')`              | 컬럼의 문자 집합을 지정합니다(MariaDB / MySQL).                                             |
| `->collation('utf8mb4_unicode_ci')` | 컬럼의 데이터 정렬을 지정합니다.                                                            |
| `->comment('my comment')`           | 컬럼에 주석을 추가합니다(MariaDB / MySQL / PostgreSQL).                                     |
| `->default($value)`                 | 컬럼의 "기본값"을 지정합니다.                                                               |
| `->first()`                         | 테이블에서 컬럼을 "처음"에 배치합니다(MariaDB / MySQL).                                     |
| `->from($integer)`                  | 자동 증가 필드의 시작 값을 설정합니다(MariaDB / MySQL / PostgreSQL).                       |
| `->instant()`                       | 즉시 작업을 사용해 컬럼을 추가하거나 수정합니다(MySQL).                                    |
| `->invisible()`                     | `SELECT *` 쿼리에서 컬럼을 "보이지 않게" 설정합니다(MariaDB / MySQL).                       |
| `->lock($mode)`                     | 컬럼 작업의 잠금 모드를 지정합니다(MySQL).                                                  |
| `->nullable($value = true)`         | 컬럼에 `NULL` 값을 삽입할 수 있도록 합니다.                                                 |
| `->storedAs($expression)`           | 저장된 생성 컬럼을 생성합니다(MariaDB / MySQL / PostgreSQL / SQLite).                       |
| `->unsigned()`                      | `INTEGER` 컬럼을 `UNSIGNED`로 설정합니다(MariaDB / MySQL).                                  |
| `->using($expression)`              | 컬럼 타입을 변경할 때 사용할 캐스팅 표현식을 지정합니다(PostgreSQL).                       |
| `->useCurrent()`                    | `TIMESTAMP` 컬럼의 기본값으로 `CURRENT_TIMESTAMP`를 사용하도록 설정합니다.                  |
| `->useCurrentOnUpdate()`            | 레코드가 업데이트될 때 `TIMESTAMP` 컬럼에 `CURRENT_TIMESTAMP`를 사용하도록 설정합니다(MariaDB / MySQL). |
| `->virtualAs($expression)`          | 가상 생성 컬럼을 생성합니다(MariaDB / MySQL / SQLite).                                      |
| `->generatedAs($expression)`        | 지정된 시퀀스 옵션을 사용하는 identity 컬럼을 생성합니다(PostgreSQL).                      |
| `->always()`                        | identity 컬럼에서 입력값보다 시퀀스 값에 우선순위를 부여합니다(PostgreSQL).                 |

</div>

<a name="default-expressions"></a>
<!-- #### Default Expressions -->
#### Default Expressions

<!-- The `default` modifier accepts a value or an `Illuminate\Database\Query\Expression` instance. Using an `Expression` instance will prevent Laravel from wrapping the value in quotes and allow you to use database specific functions. One situation where this is particularly useful is when you need to assign default values to JSON columns: -->
`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 받을 수 있습니다. `Expression` 인스턴스를 사용하면 Laravel이 값을 따옴표로 감싸지 않으므로, 데이터베이스별 함수를 사용할 수 있습니다. 이 기능이 특히 유용한 경우는 JSON 컬럼에 기본값을 지정해야 할 때입니다.

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
> 기본 표현식 지원 여부는 데이터베이스 드라이버, 데이터베이스 버전 및 필드 타입에 따라 달라집니다. 사용 중인 데이터베이스의 문서를 참고하세요.

<a name="column-order"></a>
<!-- #### Column Order -->
#### Column Order

<!-- When using the MariaDB or MySQL database, the `after` method may be used to add columns after an existing column in the schema: -->
MariaDB 또는 MySQL 데이터베이스를 사용할 때는 `after` 메서드를 사용하여 스키마의 기존 컬럼 뒤에 컬럼을 추가할 수 있습니다.

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
MySQL을 사용할 때는 컬럼 정의에 `instant` 수정자를 연결하여 MySQL의 "instant" 알고리즘으로 컬럼을 추가하거나 수정하도록 지정할 수 있습니다. 이 알고리즘은 특정 스키마 변경을 전체 테이블 재구성 없이 수행할 수 있게 하므로, 테이블 크기와 관계없이 거의 즉시 처리됩니다.

```php
$table->string('name')->nullable()->instant();
```

<!-- Instant column additions can only append columns to the end of the table, so the `instant` modifier cannot be combined with the `after` or `first` modifiers. In addition, the algorithm does not support all column types or operations. If the requested operation is incompatible, MySQL will raise an error. -->
instant 컬럼 추가는 테이블 끝에 컬럼을 덧붙이는 경우에만 가능하므로, `instant` 수정자는 `after` 또는 `first` 수정자와 함께 사용할 수 없습니다. 또한 이 알고리즘은 모든 컬럼 타입이나 작업을 지원하지 않습니다. 요청한 작업이 호환되지 않으면 MySQL에서 오류가 발생합니다.

<!-- Please refer to [MySQL's documentation](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html) to determine which operations are compatible with instant column modifications. -->
어떤 작업이 instant 컬럼 수정과 호환되는지 확인하려면 [MySQL's documentation](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)를 참고하십시오.

<a name="ddl-locking"></a>
<!-- #### DDL Locking -->
#### DDL Locking

<!-- When using MySQL, you may chain the `lock` modifier onto column, index, or foreign key definitions to control table locking during schema operations. MySQL supports several lock modes: `none` allows concurrent reads and writes, `shared` allows concurrent reads but blocks writes, `exclusive` blocks all concurrent access, and `default` lets MySQL choose the most appropriate mode: -->
MySQL을 사용할 때는 컬럼, 인덱스, 외래 키 정의에 `lock` 수정자를 연결하여 스키마 작업 중 테이블 잠금을 제어할 수 있습니다. MySQL은 여러 잠금 모드를 지원합니다. `none`은 동시 읽기와 쓰기를 허용하고, `shared`는 동시 읽기는 허용하지만 쓰기는 차단하며, `exclusive`는 모든 동시 접근을 차단하고, `default`는 MySQL이 가장 적절한 모드를 선택하도록 합니다.

```php
$table->string('name')->lock('none');

$table->index('email')->lock('shared');
```

<!-- If the requested lock mode is incompatible with the operation, MySQL will raise an error. The `lock` modifier may be combined with the `instant` modifier to further optimize schema changes: -->
요청한 잠금 모드가 작업과 호환되지 않으면 MySQL에서 오류가 발생합니다. `lock` 수정자는 `instant` 수정자와 함께 사용하여 스키마 변경을 더 최적화할 수 있습니다.

```php
$table->string('name')->instant()->lock('none');
```

<a name="modifying-columns"></a>
<!-- ### Modifying Columns -->
### Modifying Columns

<!-- The `change` method allows you to modify the type and attributes of existing columns. For example, you may wish to increase the size of a `string` column. To see the `change` method in action, let's increase the size of the `name` column from 25 to 50. To accomplish this, we simply define the new state of the column and then call the `change` method: -->
`change` 메서드를 사용하면 기존 컬럼의 타입과 속성을 수정할 수 있습니다. 예를 들어 `string` 컬럼의 크기를 늘리고 싶을 수 있습니다. `change` 메서드가 어떻게 동작하는지 보기 위해 `name` 컬럼의 크기를 25에서 50으로 늘려 보겠습니다. 이를 위해서는 컬럼의 새로운 상태를 정의한 다음 `change` 메서드를 호출하면 됩니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

<!-- When modifying a column, you must explicitly include all the modifiers you want to keep on the column definition - any missing attribute will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column: -->
컬럼을 수정할 때는 컬럼 정의에 유지하고 싶은 모든 수정자를 명시적으로 포함해야 합니다. 누락된 속성은 제거됩니다. 예를 들어 `unsigned`, `default`, `comment` 속성을 유지하려면 컬럼을 변경할 때 각 수정자를 명시적으로 호출해야 합니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

<!-- The `change` method does not change the indexes of the column. Therefore, you may use index modifiers to explicitly add or drop an index when modifying the column: -->
`change` 메서드는 컬럼의 인덱스를 변경하지 않습니다. 따라서 컬럼을 수정할 때 인덱스 수정자를 사용하여 인덱스를 명시적으로 추가하거나 제거할 수 있습니다.

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```

<a name="postgresql-column-modifications"></a>
<!-- #### PostgreSQL Column Modifications -->
#### PostgreSQL Column Modifications

<!-- When changing a column's type on PostgreSQL, you may use the `using` modifier to specify the expression used to cast the existing values: -->
PostgreSQL에서 컬럼의 타입을 변경할 때 `using` 수정자를 사용해 기존 값을 캐스팅하는 데 사용할 표현식을 지정할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->date('birthday')->using('birthday::date')->change();
});
```

<a name="renaming-columns"></a>
<!-- ### Renaming Columns -->
### Renaming Columns

<!-- To rename a column, you may use the `renameColumn` method provided by the schema builder: -->
컬럼 이름을 변경하려면 스키마 빌더가 제공하는 `renameColumn` 메서드를 사용할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="dropping-columns"></a>
<!-- ### Dropping Columns -->
### Dropping Columns

<!-- To drop a column, you may use the `dropColumn` method on the schema builder: -->
컬럼을 삭제하려면 스키마 빌더에서 `dropColumn` 메서드를 사용할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

<!-- You may drop multiple columns from a table by passing an array of column names to the `dropColumn` method: -->
컬럼 이름 배열을 `dropColumn` 메서드에 전달하면 테이블에서 여러 컬럼을 삭제할 수 있습니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="available-command-aliases"></a>
<!-- #### Available Command Aliases -->
#### Available Command Aliases

<!-- Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below: -->
Laravel은 자주 사용되는 컬럼 타입을 삭제하기 위한 몇 가지 편리한 메서드를 제공합니다. 각 메서드는 아래 표에 설명되어 있습니다.

<div class="overflow-auto">

<!-- | Command | Description | | ----------------------------------- | ----------------------------------------------------- | | `$table->dropMorphs('morphable');` | Drop the `morphable_type` and `morphable_id` columns. | | `$table->dropRememberToken();` | Drop the `remember_token` column. | | `$table->dropSoftDeletes();` | Drop the `deleted_at` column. | | `$table->dropSoftDeletesTz();` | Alias of `dropSoftDeletes()` method. | | `$table->dropTimestamps();` | Drop the `created_at` and `updated_at` columns. | | `$table->dropTimestampsTz();` | Alias of `dropTimestamps()` method. | -->
| 명령어                            | 설명                                               |
| --------------------------------- | -------------------------------------------------- |
| `$table->dropMorphs('morphable');`  | `morphable_type` 및 `morphable_id` 컬럼을 삭제합니다. |
| `$table->dropRememberToken();`      | `remember_token` 컬럼을 삭제합니다.                  |
| `$table->dropSoftDeletes();`        | `deleted_at` 컬럼을 삭제합니다.                      |
| `$table->dropSoftDeletesTz();`      | `dropSoftDeletes()` 메서드의 별칭입니다.             |
| `$table->dropTimestamps();`         | `created_at` 및 `updated_at` 컬럼을 삭제합니다.      |
| `$table->dropTimestampsTz();`       | `dropTimestamps()` 메서드의 별칭입니다.              |

</div>

<a name="indexes"></a>
<!-- ## Indexes -->
## Indexes

<a name="creating-indexes"></a>
<!-- ### Creating Indexes -->
### Creating Indexes

<!-- The Laravel schema builder supports several types of indexes. The following example creates a new `email` column and specifies that its values should be unique. To create the index, we can chain the `unique` method onto the column definition: -->
Laravel 스키마 빌더는 여러 타입의 인덱스를 지원합니다. 다음 예제는 새로운 `email` 컬럼을 생성하고 그 값이 고유해야 한다고 지정합니다. 인덱스를 생성하려면 컬럼 정의에 `unique` 메서드를 연결하면 됩니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

<!-- Alternatively, you may create the index after defining the column. To do so, you should call the `unique` method on the schema builder blueprint. This method accepts the name of the column that should receive a unique index: -->
또는 컬럼을 정의한 뒤에 인덱스를 생성할 수도 있습니다. 이렇게 하려면 스키마 빌더 blueprint에서 `unique` 메서드를 호출해야 합니다. 이 메서드는 고유 인덱스를 적용할 컬럼 이름을 인수로 받습니다.

```php
$table->unique('email');
```

<!-- You may even pass an array of columns to an index method to create a compound (or composite) index: -->
인덱스 메서드에 컬럼 배열을 전달하여 compound index(복합 인덱스)를 생성할 수도 있습니다.

```php
$table->index(['account_id', 'created_at']);
```

<!-- When creating an index, Laravel will automatically generate an index name based on the table, column names, and the index type, but you may pass a second argument to the method to specify the index name yourself: -->
인덱스를 생성할 때 Laravel은 테이블명, 컬럼명, 인덱스 타입을 기반으로 인덱스 이름을 자동으로 생성합니다. 하지만 메서드의 두 번째 인수로 인덱스 이름을 직접 지정할 수도 있습니다.

```php
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
<!-- #### Available Index Types -->
#### Available Index Types

<!-- Laravel's schema builder blueprint class provides methods for creating each type of index supported by Laravel. Each index method accepts an optional second argument to specify the name of the index. If omitted, the name will be derived from the names of the table and column(s) used for the index, as well as the index type. Each of the available index methods is described in the table below: -->
Laravel의 스키마 빌더 blueprint 클래스는 Laravel이 지원하는 각 인덱스 타입을 생성하기 위한 메서드를 제공합니다. 각 인덱스 메서드는 선택 사항인 두 번째 인수를 받아 인덱스 이름을 지정할 수 있습니다. 생략하면 인덱스에 사용된 테이블명과 컬럼명, 그리고 인덱스 타입을 기반으로 이름이 만들어집니다. 사용할 수 있는 각 인덱스 메서드는 아래 표에 설명되어 있습니다.

<div class="overflow-auto">

<!-- | Command | Description | | ------------------------------------------------ | -------------------------------------------------------------- | | `$table->primary('id');` | Adds a primary key. | | `$table->primary(['id', 'parent_id']);` | Adds composite keys. | | `$table->unique('email');` | Adds a unique index. | | `$table->index('state');` | Adds an index. | | `$table->fullText('body');` | Adds a full text index (MariaDB / MySQL / PostgreSQL). | | `$table->fullText('body')->language('english');` | Adds a full text index of the specified language (PostgreSQL). | | `$table->spatialIndex('location');` | Adds a spatial index (except SQLite). | -->
| 명령어                                           | 설명                                                        |
| ------------------------------------------------ | ----------------------------------------------------------- |
| `$table->primary('id');`                         | 기본 키를 추가합니다.                                       |
| `$table->primary(['id', 'parent_id']);`          | 복합 키를 추가합니다.                                       |
| `$table->unique('email');`                       | 고유 인덱스를 추가합니다.                                   |
| `$table->index('state');`                        | 인덱스를 추가합니다.                                        |
| `$table->fullText('body');`                      | 전문 인덱스를 추가합니다(MariaDB / MySQL / PostgreSQL).     |
| `$table->fullText('body')->language('english');` | 지정한 언어의 전문 인덱스를 추가합니다(PostgreSQL).         |
| `$table->spatialIndex('location');`              | 공간 인덱스를 추가합니다(SQLite 제외).                      |

</div>

<a name="online-index-creation"></a>
<!-- #### Online Index Creation -->
#### Online Index Creation

<!-- By default, creating an index on a large table can lock the table and block reads or writes while the index is being built. When using PostgreSQL or SQL Server, you may chain the `online` method onto an index definition to create the index without locking the table, allowing your application to continue reading and writing data during index creation: -->
기본적으로 큰 테이블에 인덱스를 생성하면 인덱스가 만들어지는 동안 테이블이 잠기고 읽기 또는 쓰기가 차단될 수 있습니다. PostgreSQL 또는 SQL Server를 사용할 때는 인덱스 정의에 `online` 메서드를 연결하여 테이블을 잠그지 않고 인덱스를 생성할 수 있습니다. 이렇게 하면 인덱스 생성 중에도 애플리케이션이 계속 데이터를 읽고 쓸 수 있습니다.

```php
$table->string('email')->unique()->online();
```

<!-- When using PostgreSQL, this adds the `CONCURRENTLY` option to the index creation statement. When using SQL Server, this adds the `WITH (online = on)` option. -->
PostgreSQL을 사용할 때는 인덱스 생성 구문에 `CONCURRENTLY` 옵션이 추가됩니다. SQL Server를 사용할 때는 `WITH (online = on)` 옵션이 추가됩니다.

<a name="renaming-indexes"></a>
<!-- ### Renaming Indexes -->
### Renaming Indexes

<!-- To rename an index, you may use the `renameIndex` method provided by the schema builder blueprint. This method accepts the current index name as its first argument and the desired name as its second argument: -->
인덱스 이름을 변경하려면 스키마 빌더 blueprint가 제공하는 `renameIndex` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 현재 인덱스 이름을, 두 번째 인수로 원하는 이름을 받습니다.

```php
$table->renameIndex('from', 'to')
```

<a name="dropping-indexes"></a>
<!-- ### Dropping Indexes -->
### Dropping Indexes

<!-- To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples: -->
인덱스를 삭제하려면 인덱스 이름을 지정해야 합니다. 기본적으로 Laravel은 테이블명, 인덱스가 적용된 컬럼명, 인덱스 타입을 기반으로 인덱스 이름을 자동으로 지정합니다. 다음은 몇 가지 예입니다.

<div class="overflow-auto">

<!-- | Command | Description | | -------------------------------------------------------- | ----------------------------------------------------------- | | `$table->dropPrimary('users_id_primary');` | Drop a primary key from the "users" table. | | `$table->dropUnique('users_email_unique');` | Drop a unique index from the "users" table. | | `$table->dropIndex('geo_state_index');` | Drop a basic index from the "geo" table. | | `$table->dropFullText('posts_body_fulltext');` | Drop a full text index from the "posts" table. | | `$table->dropSpatialIndex('geo_location_spatialindex');` | Drop a spatial index from the "geo" table (except SQLite). | -->
| 명령어                                                  | 설명                                                   |
| -------------------------------------------------------- | ------------------------------------------------------ |
| `$table->dropPrimary('users_id_primary');`               | "users" 테이블에서 기본 키를 삭제합니다.              |
| `$table->dropUnique('users_email_unique');`              | "users" 테이블에서 고유 인덱스를 삭제합니다.          |
| `$table->dropIndex('geo_state_index');`                  | "geo" 테이블에서 기본 인덱스를 삭제합니다.            |
| `$table->dropFullText('posts_body_fulltext');`           | "posts" 테이블에서 전문 인덱스를 삭제합니다.          |
| `$table->dropSpatialIndex('geo_location_spatialindex');` | "geo" 테이블에서 공간 인덱스를 삭제합니다(SQLite 제외). |

</div>

<!-- If you pass an array of columns into a method that drops indexes, the conventional index name will be generated based on the table name, columns, and index type: -->
인덱스를 삭제하는 메서드에 컬럼 배열을 전달하면 테이블명, 컬럼, 인덱스 타입을 기반으로 관례적인 인덱스 이름이 생성됩니다.

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a name="foreign-key-constraints"></a>
<!-- ### Foreign Key Constraints -->
### Foreign Key Constraints

<!-- Laravel also provides support for creating foreign key constraints, which are used to force referential integrity at the database level. For example, let's define a `user_id` column on the `posts` table that references the `id` column on a `users` table: -->
Laravel은 데이터베이스 수준에서 참조 무결성을 강제하는 데 사용되는 외래 키 제약 조건 생성도 지원합니다. 예를 들어 `posts` 테이블에 `users` 테이블의 `id` 컬럼을 참조하는 `user_id` 컬럼을 정의해 보겠습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

<!-- Since this syntax is rather verbose, Laravel provides additional, terser methods that use conventions to provide a better developer experience. When using the `foreignId` method to create your column, the example above can be rewritten like so: -->
이 문법은 다소 장황하므로, Laravel은 더 나은 개발 경험을 제공하기 위해 관례를 활용하는 더 짧은 추가 메서드를 제공합니다. `foreignId` 메서드를 사용해 컬럼을 생성하면 위 예제는 다음과 같이 다시 작성할 수 있습니다.

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column, while the `constrained` method will use conventions to determine the table and column being referenced. If your table name does not match Laravel's conventions, you may manually provide it to the `constrained` method. In addition, the name that should be assigned to the generated index may be specified as well: -->
`foreignId` 메서드는 `UNSIGNED BIGINT`에 해당하는 컬럼을 생성하고, `constrained` 메서드는 관례를 사용하여 참조할 테이블과 컬럼을 결정합니다. 테이블명이 Laravel의 관례와 맞지 않는 경우 `constrained` 메서드에 직접 전달할 수 있습니다. 또한 생성되는 인덱스에 지정할 이름도 함께 지정할 수 있습니다.

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

<!-- You may also specify the desired action for the "on delete" and "on update" properties of the constraint: -->
제약 조건의 "on delete" 및 "on update" 속성에 원하는 동작을 지정할 수도 있습니다.

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```

<!-- An alternative, expressive syntax is also provided for these actions: -->
이러한 동작을 위한 더 표현력 있는 대체 문법도 제공됩니다.

<div class="overflow-auto">

<!-- | Method | Description | | ----------------------------- | ------------------------------------------------- | | `$table->cascadeOnUpdate();` | Updates should cascade. | | `$table->restrictOnUpdate();` | Updates should be restricted. | | `$table->nullOnUpdate();` | Updates should set the foreign key value to null. | | `$table->noActionOnUpdate();` | No action on updates. | | `$table->cascadeOnDelete();` | Deletes should cascade. | | `$table->restrictOnDelete();` | Deletes should be restricted. | | `$table->nullOnDelete();` | Deletes should set the foreign key value to null. | | `$table->noActionOnDelete();` | Prevents deletes if child records exist. | -->
| 메서드                        | 설명                                      |
| ----------------------------- | ----------------------------------------- |
| `$table->cascadeOnUpdate();`  | 업데이트가 연쇄적으로 적용됩니다.         |
| `$table->restrictOnUpdate();` | 업데이트가 제한됩니다.                    |
| `$table->nullOnUpdate();`     | 외래 키 값이 null로 설정됩니다.         |
| `$table->noActionOnUpdate();` | 업데이트에 아무 작업도 수행하지 않습니다. |
| `$table->cascadeOnDelete();`  | 삭제가 연쇄적으로 적용됩니다.             |
| `$table->restrictOnDelete();` | 삭제가 제한됩니다.                        |
| `$table->nullOnDelete();`     | 외래 키 값이 null로 설정됩니다.         |
| `$table->noActionOnDelete();` | 자식 레코드가 있으면 삭제를 방지합니다.   |

</div>

<!-- Any additional [column modifiers](#column-modifiers) must be called before the `constrained` method: -->
추가 [column modifiers](#column-modifiers)는 반드시 `constrained` 메서드보다 먼저 호출해야 합니다.

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```

<a name="dropping-foreign-keys"></a>
<!-- #### Dropping Foreign Keys -->
#### Dropping Foreign Keys

<!-- To drop a foreign key, you may use the `dropForeign` method, passing the name of the foreign key constraint to be deleted as an argument. Foreign key constraints use the same naming convention as indexes. In other words, the foreign key constraint name is based on the name of the table and the columns in the constraint, followed by a "\_foreign" suffix: -->
외래 키를 삭제하려면 삭제할 외래 키 제약 조건 이름을 인수로 전달하여 `dropForeign` 메서드를 사용할 수 있습니다. 외래 키 제약 조건은 인덱스와 동일한 이름 지정 관례를 사용합니다. 즉, 외래 키 제약 조건 이름은 테이블명과 제약 조건에 포함된 컬럼명을 기반으로 하며, 뒤에 "\_foreign" 접미사가 붙습니다.

```php
$table->dropForeign('posts_user_id_foreign');
```

<!-- Alternatively, you may pass an array containing the column name that holds the foreign key to the `dropForeign` method. The array will be converted to a foreign key constraint name using Laravel's constraint naming conventions: -->
또는 외래 키를 담고 있는 컬럼명을 포함한 배열을 `dropForeign` 메서드에 전달할 수 있습니다. 이 배열은 Laravel의 제약 조건 이름 지정 관례를 사용하여 외래 키 제약 조건 이름으로 변환됩니다.

```php
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
<!-- #### Toggling Foreign Key Constraints -->
#### Toggling Foreign Key Constraints

<!-- You may enable or disable foreign key constraints within your migrations by using the following methods: -->
마이그레이션 안에서 다음 메서드를 사용하여 외래 키 제약 조건을 활성화하거나 비활성화할 수 있습니다.

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약 조건을 비활성화합니다. SQLite를 사용할 때 마이그레이션에서 외래 키 제약 조건을 생성하기 전에 데이터베이스 설정에서 [enable foreign key support](/docs/13.x/database#configuration)를 활성화해야 합니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- For convenience, each migration operation will dispatch an [event](/docs/13.x/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class: -->
편의를 위해 각 마이그레이션 작업은 [event](/docs/13.x/events)를 디스패치합니다. 다음 이벤트는 모두 기본 `Illuminate\Database\Events\MigrationEvent` 클래스를 확장합니다:

<div class="overflow-auto">

<!-- | Class | Description | | ------------------------------------------------ | ------------------------------------------------ | | `Illuminate\Database\Events\DatabaseRefreshed` | The `migrate:refresh` command has finished. | | `Illuminate\Database\Events\MigrationsStarted` | A batch of migrations is about to be executed. | | `Illuminate\Database\Events\MigrationsEnded` | A batch of migrations has finished. | | `Illuminate\Database\Events\MigrationStarted` | A single migration is about to be executed. | | `Illuminate\Database\Events\MigrationEnded` | A single migration has finished. | | `Illuminate\Database\Events\NoPendingMigrations` | A migration command found no pending migrations. | | `Illuminate\Database\Events\SchemaDumped` | A database schema dump has finished. | | `Illuminate\Database\Events\SchemaLoaded` | An existing database schema dump has loaded. | -->
| 클래스                                           | 설명                                      |
| ------------------------------------------------ | ----------------------------------------- |
| `Illuminate\Database\Events\DatabaseRefreshed`   | `migrate:refresh` 명령어가 완료되었습니다. |
| `Illuminate\Database\Events\MigrationsStarted`   | 마이그레이션 배치를 실행하려고 합니다.    |
| `Illuminate\Database\Events\MigrationsEnded`     | 마이그레이션 배치가 완료되었습니다.       |
| `Illuminate\Database\Events\MigrationStarted`    | 단일 마이그레이션을 실행하려고 합니다.    |
| `Illuminate\Database\Events\MigrationEnded`      | 단일 마이그레이션이 완료되었습니다.       |
| `Illuminate\Database\Events\NoPendingMigrations` | 마이그레이션 명령어에서 보류 중인 마이그레이션을 찾지 못했습니다. |
| `Illuminate\Database\Events\SchemaDumped`        | 데이터베이스 스키마 덤프가 완료되었습니다. |
| `Illuminate\Database\Events\SchemaLoaded`        | 기존 데이터베이스 스키마 덤프를 로드했습니다. |

</div>
