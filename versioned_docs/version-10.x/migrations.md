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
마이그레이션은 데이터베이스의 버전 관리를 가능하게 해주며, 팀원들이 애플리케이션의 데이터베이스 스키마 정의를 명확히 공유하도록 도와줍니다. 만약 여러분이 소스 컨트롤에서 변경 사항을 받은 동료에게 "데이터베이스에 컬럼을 직접 추가해 주세요"라고 안내했던 경험이 있다면, 바로 그 문제를 마이그레이션으로 해결할 수 있습니다.

<!-- The Laravel `Schema` [facade](/docs/10.x/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns. -->
Laravel의 `Schema` [facade](/docs/10.x/facades)는 Laravel에서 지원하는 모든 데이터베이스 시스템에서 데이터베이스 테이블을 생성하고 조작할 수 있도록 데이터베이스에 독립적인 기능을 제공합니다. 일반적으로 마이그레이션은 이 파사드를 활용하여 데이터베이스의 테이블과 컬럼을 생성 및 수정합니다.

<a name="generating-migrations"></a>
<a id="writing-migrations" data-translation-alias="true"></a>
<!-- ## Generating Migrations -->
## Generating Migrations

<!-- You may use the `make:migration` [Artisan command](/docs/10.x/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations: -->
`make:migration` [Artisan command](/docs/10.x/artisan)를 사용해 데이터베이스 마이그레이션 파일을 생성할 수 있습니다. 새로 생성된 마이그레이션 파일은 `database/migrations` 디렉터리에 저장됩니다. 각 마이그레이션 파일명에는 타임스탬프가 포함되어 있어 Laravel이 마이그레이션 실행 순서를 결정할 수 있습니다.

```shell
php artisan make:migration create_flights_table
```

<!-- Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually. -->
Laravel은 마이그레이션 파일의 이름을 참고하여 어떤 테이블을 대상으로 하는지, 그리고 새 테이블을 생성하는지 여부를 추론하려 시도합니다. Laravel이 마이그레이션 이름에서 테이블명을 알아낼 수 있다면, 생성된 마이그레이션 파일의 내용을 미리 채워줍니다. 만약 자동으로 추론되지 않는다면, 마이그레이션 파일에서 직접 테이블명을 지정하시면 됩니다.

<!-- If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path. -->
생성된 마이그레이션의 저장 경로를 따로 지정하고 싶다면, `make:migration` 명령어 실행 시 `--path` 옵션을 사용할 수 있습니다. 입력하는 경로는 애플리케이션의 최상위 경로에서 상대경로로 작성해야 합니다.

> [!NOTE]
> 마이그레이션 스텁(stub)은 [stub publishing](/docs/10.x/artisan#stub-customization)을 통해 커스터마이징할 수 있습니다.

<a name="squashing-migrations"></a>
<!-- ### Squashing Migrations -->
### Squashing Migrations

<!-- As you build your application, you may accumulate more and more migrations over time. This can lead to your `database/migrations` directory becoming bloated with potentially hundreds of migrations. If you would like, you may "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command: -->
애플리케이션을 개발하다 보면 시간이 지나면서 마이그레이션 파일이 점점 많아질 수 있습니다. 이로 인해 `database/migrations` 디렉터리에 수백 개의 마이그레이션이 쌓여 비대해질 수 있습니다. 이런 경우, 마이그레이션을 하나의 SQL 파일로 "스쿼시(squash)"하여 관리할 수 있습니다. 시작하려면 `schema:dump` 명령어를 실행하세요.

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

<!-- When you execute this command, Laravel will write a "schema" file to your application's `database/schema` directory. The schema file's name will correspond to the database connection. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will first execute the SQL statements in the schema file of the database connection you are using. After executing the schema file's SQL statements, Laravel will execute any remaining migrations that were not part of the schema dump. -->
이 명령어를 실행하면, Laravel은 애플리케이션의 `database/schema` 디렉터리에 "스키마" 파일을 생성합니다. 파일명은 데이터베이스 연결 이름과 일치합니다. 이제 데이터베이스에 마이그레이션을 적용하려고 할 때, 아직 마이그레이션이 실행된 적이 없다면 Laravel은 우선 해당 데이터베이스 연결의 스키마 파일에 들어 있는 SQL을 실행합니다. 스키마 파일 실행 후, 스키마 덤프에 포함되지 않은 나머지 마이그레이션만 추가로 실행합니다.

<!-- If your application's tests use a different database connection than the one you typically use during local development, you should ensure you have dumped a schema file using that database connection so that your tests are able to build your database. You may wish to do this after dumping the database connection you typically use during local development: -->
애플리케이션 테스트에서 로컬 개발 시 사용하는 데이터베이스와 다른 데이터베이스 연결을 사용한다면, 반드시 그 데이터베이스 연결을 사용해서도 스키마 파일을 덤프하세요. 이렇게 하면 테스트 실행 시 데이터베이스를 올바르게 구축할 수 있습니다. 일반적으로 로컬 개발용 연결의 스키마를 먼저 덤프한 후, 테스트용 연결에 대해 덤프를 진행합니다.

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```

<!-- You should commit your database schema file to source control so that other new developers on your team may quickly create your application's initial database structure. -->
생성한 데이터베이스 스키마 파일은 소스 컨트롤에 커밋하는 것이 좋습니다. 이렇게 하면 팀의 신규 개발자가 빠르게 초기 데이터베이스 구조를 생성할 수 있습니다.

> [!WARNING]
> 마이그레이션 스쿼싱 기능은 MySQL, PostgreSQL, SQLite 데이터베이스에서만 지원되며, 데이터베이스의 커맨드라인 클라이언트를 활용합니다.

<a name="migration-structure"></a>
<!-- ## Migration Structure -->
## Migration Structure

<!-- A migration class contains two methods: `up` and `down`. The `up` method is used to add new tables, columns, or indexes to your database, while the `down` method should reverse the operations performed by the `up` method. -->
마이그레이션 클래스는 `up`과 `down` 두 개의 메서드를 가집니다. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼, 인덱스를 추가하는 작업에 사용하며, `down` 메서드는 `up`에서 수행한 작업을 되돌릴 수 있도록 반대로 동작해야 합니다.

<!-- Within both of these methods, you may use the Laravel schema builder to expressively create and modify tables. To learn about all of the methods available on the `Schema` builder, [check out its documentation](#creating-tables). For example, the following migration creates a `flights` table: -->
이 두 메서드 내부에서는 Laravel 스키마 빌더(schema builder)를 사용하여 직관적으로 테이블을 생성하거나 수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메서드에 대해 더 자세한 정보가 필요하다면 [check out its documentation](#creating-tables)를 참고하시기 바랍니다. 예를 들어, 아래 마이그레이션에서는 `flights` 테이블을 생성합니다.

```
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
마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 데이터베이스 연결을 사용해야 한다면, 마이그레이션 클래스의 `$connection` 속성을 설정해 주세요.

```
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

<a name="running-migrations"></a>
<!-- ## Running Migrations -->
## Running Migrations

<!-- To run all of your outstanding migrations, execute the `migrate` Artisan command: -->
아직 실행하지 않은 모든 마이그레이션을 한 번에 적용하려면, `migrate` Artisan 명령어를 실행하세요.

```shell
php artisan migrate
```

<!-- If you would like to see which migrations have run thus far, you may use the `migrate:status` Artisan command: -->
지금까지 어떤 마이그레이션이 실행되었는지 확인하려면, `migrate:status` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan migrate:status
```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate` command: -->
마이그레이션이 실제로 실행되지는 않고, 어떤 SQL 문이 실행될지 미리 보고 싶다면, `migrate` 명령에 `--pretend` 플래그를 추가할 수 있습니다.

```shell
php artisan migrate --pretend
```

<!-- #### Isolating Migration Execution -->
#### Isolating Migration Execution

<!-- If you are deploying your application across multiple servers and running migrations as part of your deployment process, you likely do not want two servers attempting to migrate the database at the same time. To avoid this, you may use the `isolated` option when invoking the `migrate` command. -->
여러 서버에 애플리케이션을 배포하고, 배포 과정 중에 마이그레이션을 실행하는 경우, 두 서버가 동시에 같은 데이터베이스에 마이그레이션을 적용하는 상황을 피하고 싶을 수 있습니다. 이러한 경우, `migrate` 명령 실행 시 `isolated` 옵션을 사용할 수 있습니다.

<!-- When the `isolated` option is provided, Laravel will acquire an atomic lock using your application's cache driver before attempting to run your migrations. All other attempts to run the `migrate` command while that lock is held will not execute; however, the command will still exit with a successful exit status code: -->
`isolated` 옵션을 지정하면, Laravel이 마이그레이션을 실행하기 전에 애플리케이션의 캐시 드라이버를 활용하여 원자적(atomic) 락을 획득합니다. 락이 유지되는 동안 `migrate` 명령을 실행하려는 다른 모든 시도는 실제로 수행되지 않으며, 단지 성공적인 종료 코드와 함께 종료됩니다.

```shell
php artisan migrate --isolated
```

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 중 하나가 설정되어 있어야 합니다. 또한 모든 서버는 동일한 중앙 캐시 서버와 통신해야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
<!-- #### Forcing Migrations to Run in Production -->
#### Forcing Migrations to Run in Production

<!-- Some migration operations are destructive, which means they may cause you to lose data. In order to protect you from running these commands against your production database, you will be prompted for confirmation before the commands are executed. To force the commands to run without a prompt, use the `--force` flag: -->
일부 마이그레이션 작업은 파괴적일 수 있어 데이터 손실이 발생할 수도 있습니다. 이를 방지하기 위해, 프로덕션 데이터베이스에서 해당 명령을 실행하려고 하면 추가로 실행 여부를 확인하는 프롬프트가 표시됩니다. 프롬프트 없이 즉시 실행하려면 `--force` 플래그를 사용하세요.

```shell
php artisan migrate --force
```

<a name="rolling-back-migrations"></a>
<!-- ### Rolling Back Migrations -->
### Rolling Back Migrations

<!-- To roll back the latest migration operation, you may use the `rollback` Artisan command. This command rolls back the last "batch" of migrations, which may include multiple migration files: -->
가장 최근에 실행된 마이그레이션 작업을 되돌리려면 `rollback` Artisan 명령어를 사용할 수 있습니다. 이 명령은 하나의 "배치(batch)"에 해당하는(여러 마이그레이션 파일 포함 가능) 모든 작업을 롤백합니다.

```shell
php artisan migrate:rollback
```

<!-- You may roll back a limited number of migrations by providing the `step` option to the `rollback` command. For example, the following command will roll back the last five migrations: -->
`rollback` 명령어에 `step` 옵션을 추가하면 최근 N개의 마이그레이션만 롤백할 수도 있습니다. 예를 들어, 다음 명령은 마지막 5개의 마이그레이션만 롤백합니다.

```shell
php artisan migrate:rollback --step=5
```

<!-- You may roll back a specific "batch" of migrations by providing the `batch` option to the `rollback` command, where the `batch` option corresponds to a batch value within your application's `migrations` database table. For example, the following command will roll back all migrations in batch three: -->
특정 "배치(batch)"의 마이그레이션만 롤백하려면, `rollback` 명령어에 `batch` 옵션을 추가하면 됩니다. 이때 `batch` 값은 애플리케이션의 `migrations` 데이터베이스 테이블 내 배치 값에 해당합니다. 예를 들어, 다음 명령은 3번 배치에 속한 모든 마이그레이션만 롤백합니다.

 ```shell
 php artisan migrate:rollback --batch=3
 ```

<!-- If you would like to see the SQL statements that will be executed by the migrations without actually running them, you may provide the `--pretend` flag to the `migrate:rollback` command: -->
실제로 롤백을 실행하지 않고, 어떤 SQL 문이 실행될지 미리 확인하고 싶다면 `migrate:rollback` 명령에 `--pretend` 플래그를 추가하세요.

```shell
php artisan migrate:rollback --pretend
```

<!-- The `migrate:reset` command will roll back all of your application's migrations: -->
`migrate:reset` 명령어를 사용하면, 애플리케이션의 모든 마이그레이션을 한 번에 롤백할 수 있습니다.

```shell
php artisan migrate:reset
```

<a name="roll-back-migrate-using-a-single-command"></a>
<!-- #### Roll Back and Migrate Using a Single Command -->
#### Roll Back and Migrate Using a Single Command

<!-- The `migrate:refresh` command will roll back all of your migrations and then execute the `migrate` command. This command effectively re-creates your entire database: -->
`migrate:refresh` 명령어는 모든 마이그레이션을 롤백한 후 `migrate` 명령을 다시 실행합니다. 즉, 전체 데이터베이스를 한 번에 새로 만드는 효과가 있습니다.

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```

<!-- You may roll back and re-migrate a limited number of migrations by providing the `step` option to the `refresh` command. For example, the following command will roll back and re-migrate the last five migrations: -->
`refresh` 명령어에 `step` 옵션을 지정하면, 최근 N개의 마이그레이션만 롤백하고 다시 마이그레이션할 수 있습니다. 예를 들어, 아래 명령은 최근 5개의 마이그레이션만 롤백 후 재실행합니다.

```shell
php artisan migrate:refresh --step=5
```

<a name="drop-all-tables-migrate"></a>
<!-- #### Drop All Tables and Migrate -->
#### Drop All Tables and Migrate

<!-- The `migrate:fresh` command will drop all tables from the database and then execute the `migrate` command: -->
`migrate:fresh` 명령어는 데이터베이스의 모든 테이블을 삭제한 뒤, `migrate` 명령을 실행합니다.

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```

<!-- By default, the `migrate:fresh` command only drops tables from the default database connection. However, you may use the `--database` option to specify the database connection that should be migrated. The database connection name should correspond to a connection defined in your application's `database` [configuration file](/docs/10.x/configuration): -->
기본적으로 `migrate:fresh` 명령어는 기본 데이터베이스 연결의 테이블만 삭제합니다. 하지만 `--database` 옵션을 사용해 특정 데이터베이스 연결을 지정할 수도 있습니다. 연결명은 애플리케이션의 `database` [configuration file](/docs/10.x/configuration)에 정의된 값과 일치해야 합니다.

```shell
php artisan migrate:fresh --database=admin
```

> [!WARNING]
> `migrate:fresh` 명령어는 테이블의 접두사와 상관없이 데이터베이스의 모든 테이블을 삭제합니다. 다른 애플리케이션과 공유하는 데이터베이스에서 사용할 때는 각별히 주의하세요.

<a name="tables"></a>
<!-- ## Tables -->
## Tables

<a name="creating-tables"></a>
<!-- ### Creating Tables -->
### Creating Tables

<!-- To create a new database table, use the `create` method on the `Schema` facade. The `create` method accepts two arguments: the first is the name of the table, while the second is a closure which receives a `Blueprint` object that may be used to define the new table: -->
새로운 데이터베이스 테이블을 생성하려면, `Schema` 파사드의 `create` 메서드를 사용하세요. `create` 메서드는 두 개의 인자를 받습니다. 첫 번째는 생성할 테이블명, 두 번째는 신규 테이블을 정의할 수 있도록 `Blueprint` 오브젝트를 전달하는 클로저(익명 함수)입니다.

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
테이블 생성시, 스키마 빌더의 [column methods](#creating-columns)를 자유롭게 사용하여 테이블의 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
<!-- #### Determining Table / Column Existence -->
#### Determining Table / Column Existence

<!-- You may determine the existence of a table or column using the `hasTable` and `hasColumn` methods: -->
`hasTable`과 `hasColumn` 메서드를 사용하면, 테이블이나 컬럼이 존재하는지 확인할 수 있습니다.

```
if (Schema::hasTable('users')) {
    // The "users" table exists...
}

if (Schema::hasColumn('users', 'email')) {
    // The "users" table exists and has an "email" column...
}
```

<a name="database-connection-table-options"></a>
<!-- #### Database Connection and Table Options -->
#### Database Connection and Table Options

<!-- If you want to perform a schema operation on a database connection that is not your application's default connection, use the `connection` method: -->
기본 데이터베이스 연결이 아닌 다른 연결에 대해 스키마 작업을 수행하고 싶다면, `connection` 메서드를 사용하세요.

```
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```

<!-- In addition, a few other properties and methods may be used to define other aspects of the table's creation. The `engine` property may be used to specify the table's storage engine when using MySQL: -->
추가로, 테이블 생성 시 몇 가지 속성 및 메서드를 통해 다양한 옵션을 지정할 수 있습니다. MySQL에서 스토리지 엔진을 설정하려면 `engine` 속성을 사용하세요.

```
Schema::create('users', function (Blueprint $table) {
    $table->engine = 'InnoDB';

    // ...
});
```

<!-- The `charset` and `collation` properties may be used to specify the character set and collation for the created table when using MySQL: -->
MySQL에서 테이블의 문자셋 및 정렬방식을 지정하려면 `charset`과 `collation` 속성을 사용할 수 있습니다.

```
Schema::create('users', function (Blueprint $table) {
    $table->charset = 'utf8mb4';
    $table->collation = 'utf8mb4_unicode_ci';

    // ...
});
```

<!-- The `temporary` method may be used to indicate that the table should be "temporary". Temporary tables are only visible to the current connection's database session and are dropped automatically when the connection is closed: -->
테이블을 "임시(temporary)"로 만들고 싶다면, `temporary` 메서드를 사용하세요. 임시 테이블은 현재 연결의 데이터베이스 세션에서만 보이고, 연결을 종료하면 자동으로 삭제됩니다.

```
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```

<!-- If you would like to add a "comment" to a database table, you may invoke the `comment` method on the table instance. Table comments are currently only supported by MySQL and Postgres: -->
데이터베이스 테이블에 "코멘트(comment)"를 추가하고 싶다면, 테이블 인스턴스의 `comment` 메서드를 호출할 수 있습니다. 테이블 코멘트는 현재 MySQL과 Postgres에서만 지원됩니다.

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
기존 테이블을 수정하려면 `Schema` 파사드의 `table` 메서드를 사용하세요. `create` 메서드와 마찬가지로, `table` 메서드는 첫 번째 인자로 테이블명, 두 번째 인자로 컬럼이나 인덱스를 추가할 수 있는 `Blueprint` 인스턴스를 전달하는 클로저를 받습니다.

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
기존 데이터베이스 테이블의 이름을 바꾸려면 `rename` 메서드를 사용하세요.

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
테이블 이름을 변경하기 전에는, 해당 테이블의 외래 키 제약(foreign key constraint)에 대해 마이그레이션 파일 내에서 반드시 명시적으로 이름을 지정했는지 확인해야 합니다. 그렇지 않으면, 외래 키 제약 이름이 이전 테이블명을 참조할 수 있습니다.

<a name="columns"></a>
<!-- ## Columns -->
## Columns

<a name="creating-columns"></a>
<!-- ### Creating Columns -->
### Creating Columns

<!-- The `table` method on the `Schema` facade may be used to update existing tables. Like the `create` method, the `table` method accepts two arguments: the name of the table and a closure that receives an `Illuminate\Database\Schema\Blueprint` instance you may use to add columns to the table: -->
기존 테이블을 수정하려면 `Schema` 파사드의 `table` 메서드를 사용하세요. `create` 메서드와 마찬가지로, `table` 메서드는 첫 번째 인자로 테이블명, 두 번째 인자로 컬럼을 추가할 수 있는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 전달하는 클로저를 받습니다.

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
스키마 빌더(Blueprint)는 데이터베이스 테이블에 추가할 수 있는 다양한 컬럼 타입에 해당하는 여러 메서드를 제공합니다. 사용 가능한 각각의 메서드는 아래 표에 정리되어 있습니다.

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
`bigIncrements` 메서드는 자동 증가하는 `UNSIGNED BIGINT` (기본 키) 컬럼을 생성합니다.

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
`char` 메서드는 지정한 길이만큼의 `CHAR` 타입 컬럼을 생성합니다.

```
$table->char('name', 100);
```

<a name="column-method-dateTimeTz"></a>
<!-- #### `dateTimeTz()` -->
#### `dateTimeTz()`

<!-- The `dateTimeTz` method creates a `DATETIME` (with timezone) equivalent column with an optional precision (total digits): -->
`dateTimeTz` 메서드는(정밀도 지정 가능) 타임존이 포함된 `DATETIME` 타입의 컬럼을 생성합니다.

```
$table->dateTimeTz('created_at', $precision = 0);
```

<a name="column-method-dateTime"></a>
<!-- #### `dateTime()` -->
#### `dateTime()`

<!-- The `dateTime` method creates a `DATETIME` equivalent column with an optional precision (total digits): -->
`dateTime` 메서드는(정밀도 지정 가능) `DATETIME` 타입의 컬럼을 생성합니다.

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
`decimal` 메서드는 지정한 전체 자리수(precision)와 소수점 이하 자리수(scale)를 갖는 `DECIMAL` 타입의 컬럼을 생성합니다.

```
$table->decimal('amount', $precision = 8, $scale = 2);
```

<a name="column-method-double"></a>

<!-- #### `double()` -->
#### `double()`

<!-- The `double` method creates a `DOUBLE` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`double` 메서드는 지정한 precision(전체 자릿수)과 scale(소수 자릿수)로 `DOUBLE`과 동등한 컬럼을 생성합니다.

```
$table->double('amount', 8, 2);
```

<a name="column-method-enum"></a>
<!-- #### `enum()` -->
#### `enum()`

<!-- The `enum` method creates a `ENUM` equivalent column with the given valid values: -->
`enum` 메서드는 주어진 값 목록으로 제한되는 `ENUM`과 동등한 컬럼을 생성합니다.

```
$table->enum('difficulty', ['easy', 'hard']);
```

<a name="column-method-float"></a>
<!-- #### `float()` -->
#### `float()`

<!-- The `float` method creates a `FLOAT` equivalent column with the given precision (total digits) and scale (decimal digits): -->
`float` 메서드는 지정한 precision(전체 자릿수)과 scale(소수 자릿수)로 `FLOAT`과 동등한 컬럼을 생성합니다.

```
$table->float('amount', 8, 2);
```

<a name="column-method-foreignId"></a>
<!-- #### `foreignId()` -->
#### `foreignId()`

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column: -->
`foreignId` 메서드는 `UNSIGNED BIGINT`와 동등한 컬럼을 생성합니다.

```
$table->foreignId('user_id');
```

<a name="column-method-foreignIdFor"></a>
<!-- #### `foreignIdFor()` -->
#### `foreignIdFor()`

<!-- The `foreignIdFor` method adds a `{column}_id` equivalent column for a given model class. The column type will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type: -->
`foreignIdFor` 메서드는 주어진 모델 클래스에 대해 `{column}_id`와 동등한 컬럼을 추가합니다. 컬럼 타입은 모델의 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, 또는 `CHAR(26)`이 됩니다.

```
$table->foreignIdFor(User::class);
```

<a name="column-method-foreignUlid"></a>
<!-- #### `foreignUlid()` -->
#### `foreignUlid()`

<!-- The `foreignUlid` method creates a `ULID` equivalent column: -->
`foreignUlid` 메서드는 `ULID`와 동등한 컬럼을 생성합니다.

```
$table->foreignUlid('user_id');
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
`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 `id` 컬럼을 생성하지만, 다른 컬럼명을 지정하고 싶다면 이름을 직접 전달할 수 있습니다.

```
$table->id();
```

<a name="column-method-increments"></a>
<!-- #### `increments()` -->
#### `increments()`

<!-- The `increments` method creates an auto-incrementing `UNSIGNED INTEGER` equivalent column as a primary key: -->
`increments` 메서드는 자동 증가하는 `UNSIGNED INTEGER` 타입의 컬럼을 기본키로 생성합니다.

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
<!-- When using Postgres, an `INET` column will be created. -->
Postgres를 사용할 때는 `INET` 컬럼이 생성됩니다.

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
`macAddress` 메서드는 MAC 주소를 저장하기 위한 컬럼을 생성합니다. PostgreSQL 등 일부 데이터베이스는 이 용도를 위한 전용 컬럼 타입을 제공합니다. 그 외에는 문자열 타입 컬럼이 사용됩니다.

```
$table->macAddress('device');
```

<a name="column-method-mediumIncrements"></a>
<!-- #### `mediumIncrements()` -->
#### `mediumIncrements()`

<!-- The `mediumIncrements` method creates an auto-incrementing `UNSIGNED MEDIUMINT` equivalent column as a primary key: -->
`mediumIncrements` 메서드는 자동 증가하는 `UNSIGNED MEDIUMINT` 타입의 컬럼을 기본키로 생성합니다.

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

<!-- The `morphs` method is a convenience method that adds a `{column}_id` equivalent column and a `{column}_type` `VARCHAR` equivalent column. The column type for the `{column}_id` will be `UNSIGNED BIGINT`, `CHAR(36)`, or `CHAR(26)` depending on the model key type. -->
`morphs` 메서드는 `{column}_id`와 동등한 컬럼과 `{column}_type` `VARCHAR`와 동등한 컬럼을 함께 추가하는 편의 메서드입니다. `{column}_id` 타입은 모델의 키 타입에 따라 `UNSIGNED BIGINT`, `CHAR(36)`, 또는 `CHAR(26)`이 됩니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/10.x/eloquent-relationships). In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 메서드는 다형성 [Eloquent relationship](/docs/10.x/eloquent-relationships)를 만들 때 필요한 컬럼을 정의하기 위해 사용됩니다. 아래 예시에서는 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다.

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
이 메서드는 [morphs](#column-method-morphs) 메서드와 유사하지만, 생성되는 컬럼들이 "nullable"로 지정된다는 점이 다릅니다.

```
$table->nullableMorphs('taggable');
```

<a name="column-method-nullableUlidMorphs"></a>
<!-- #### `nullableUlidMorphs()` -->
#### `nullableUlidMorphs()`

<!-- The method is similar to the [ulidMorphs](#column-method-ulidMorphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [ulidMorphs](#column-method-ulidMorphs) 메서드와 유사하지만, 생성되는 컬럼들이 "nullable"로 지정됩니다.

```
$table->nullableUlidMorphs('taggable');
```

<a name="column-method-nullableUuidMorphs"></a>
<!-- #### `nullableUuidMorphs()` -->
#### `nullableUuidMorphs()`

<!-- The method is similar to the [uuidMorphs](#column-method-uuidMorphs) method; however, the columns that are created will be "nullable": -->
이 메서드는 [uuidMorphs](#column-method-uuidMorphs) 메서드와 유사하지만, 생성되는 컬럼들이 "nullable"로 지정됩니다.

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

<!-- The `rememberToken` method creates a nullable, `VARCHAR(100)` equivalent column that is intended to store the current "remember me" [authentication token](/docs/10.x/authentication#remembering-users): -->
`rememberToken` 메서드는 현 사용자의 "remember me" [authentication token](/docs/10.x/authentication#remembering-users)을 저장하기 위한 nullable, `VARCHAR(100)`과 동등한 컬럼을 생성합니다.

```
$table->rememberToken();
```

<a name="column-method-set"></a>
<!-- #### `set()` -->
#### `set()`

<!-- The `set` method creates a `SET` equivalent column with the given list of valid values: -->
`set` 메서드는 전달된 값 목록으로 제한되는 `SET`과 동등한 컬럼을 생성합니다.

```
$table->set('flavors', ['strawberry', 'vanilla']);
```

<a name="column-method-smallIncrements"></a>
<!-- #### `smallIncrements()` -->
#### `smallIncrements()`

<!-- The `smallIncrements` method creates an auto-incrementing `UNSIGNED SMALLINT` equivalent column as a primary key: -->
`smallIncrements` 메서드는 자동 증가하는 `UNSIGNED SMALLINT` 타입의 컬럼을 기본키로 생성합니다.

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
`softDeletesTz` 메서드는 nullable한 `deleted_at` `TIMESTAMP`(타임존 포함)과 동등한 컬럼을 precision(총 자릿수) 옵션과 함께 추가합니다. 이 컬럼은 Eloquent의 "soft delete" 기능에 필요한 `deleted_at` 타임스탬프 값을 저장하는 용도입니다.

```
$table->softDeletesTz($column = 'deleted_at', $precision = 0);
```

<a name="column-method-softDeletes"></a>
<!-- #### `softDeletes()` -->
#### `softDeletes()`

<!-- The `softDeletes` method adds a nullable `deleted_at` `TIMESTAMP` equivalent column with an optional precision (total digits). This column is intended to store the `deleted_at` timestamp needed for Eloquent's "soft delete" functionality: -->
`softDeletes` 메서드는 nullable한 `deleted_at` `TIMESTAMP`와 동등한 컬럼을 precision(총 자릿수) 옵션과 함께 추가합니다. 이 컬럼은 Eloquent의 "soft delete" 기능에 필요한 `deleted_at` 타임스탬프 값을 저장하는 용도입니다.

```
$table->softDeletes($column = 'deleted_at', $precision = 0);
```

<a name="column-method-string"></a>
<!-- #### `string()` -->
#### `string()`

<!-- The `string` method creates a `VARCHAR` equivalent column of the given length: -->
`string` 메서드는 지정한 길이의 `VARCHAR`와 동등한 컬럼을 생성합니다.

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
`timeTz` 메서드는 지정된 precision(총 자릿수) 옵션으로 타임존이 포함된 `TIME`과 동등한 컬럼을 생성합니다.

```
$table->timeTz('sunrise', $precision = 0);
```

<a name="column-method-time"></a>
<!-- #### `time()` -->
#### `time()`

<!-- The `time` method creates a `TIME` equivalent column with an optional precision (total digits): -->
`time` 메서드는 지정된 precision(총 자릿수) 옵션으로 `TIME`과 동등한 컬럼을 생성합니다.

```
$table->time('sunrise', $precision = 0);
```

<a name="column-method-timestampTz"></a>
<!-- #### `timestampTz()` -->
#### `timestampTz()`

<!-- The `timestampTz` method creates a `TIMESTAMP` (with timezone) equivalent column with an optional precision (total digits): -->
`timestampTz` 메서드는 지정된 precision(총 자릿수) 옵션으로 타임존이 포함된 `TIMESTAMP`와 동등한 컬럼을 생성합니다.

```
$table->timestampTz('added_at', $precision = 0);
```

<a name="column-method-timestamp"></a>
<!-- #### `timestamp()` -->
#### `timestamp()`

<!-- The `timestamp` method creates a `TIMESTAMP` equivalent column with an optional precision (total digits): -->
`timestamp` 메서드는 지정된 precision(총 자릿수) 옵션으로 `TIMESTAMP`와 동등한 컬럼을 생성합니다.

```
$table->timestamp('added_at', $precision = 0);
```

<a name="column-method-timestampsTz"></a>
<!-- #### `timestampsTz()` -->
#### `timestampsTz()`

<!-- The `timestampsTz` method creates `created_at` and `updated_at` `TIMESTAMP` (with timezone) equivalent columns with an optional precision (total digits): -->
`timestampsTz` 메서드는 지정된 precision(총 자릿수) 옵션으로 `created_at`과 `updated_at` 타임존이 있는 `TIMESTAMP`와 동등한 컬럼을 생성합니다.

```
$table->timestampsTz($precision = 0);
```

<a name="column-method-timestamps"></a>
<!-- #### `timestamps()` -->
#### `timestamps()`

<!-- The `timestamps` method creates `created_at` and `updated_at` `TIMESTAMP` equivalent columns with an optional precision (total digits): -->
`timestamps` 메서드는 지정된 precision(총 자릿수) 옵션으로 `created_at`과 `updated_at` `TIMESTAMP`와 동등한 컬럼을 생성합니다.

```
$table->timestamps($precision = 0);
```

<a name="column-method-tinyIncrements"></a>
<!-- #### `tinyIncrements()` -->
#### `tinyIncrements()`

<!-- The `tinyIncrements` method creates an auto-incrementing `UNSIGNED TINYINT` equivalent column as a primary key: -->
`tinyIncrements` 메서드는 자동 증가하는 `UNSIGNED TINYINT` 타입의 컬럼을 기본키로 생성합니다.

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
`unsignedDecimal` 메서드는 지정된 precision(총 자릿수) 및 scale(소수 자릿수)로 `UNSIGNED DECIMAL`과 동등한 컬럼을 생성합니다.

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

<a name="column-method-ulidMorphs"></a>
<!-- #### `ulidMorphs()` -->
#### `ulidMorphs()`

<!-- The `ulidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(26)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`ulidMorphs` 메서드는 `{column}_id` `CHAR(26)`과 동등한 컬럼과 `{column}_type` `VARCHAR`와 동등한 컬럼을 한 번에 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/10.x/eloquent-relationships) that use ULID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 메서드는 ULID 식별자를 사용하는 다형성 [Eloquent relationship](/docs/10.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용됩니다. 아래 예시에서는 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다.

```
$table->ulidMorphs('taggable');
```

<a name="column-method-uuidMorphs"></a>
<!-- #### `uuidMorphs()` -->
#### `uuidMorphs()`

<!-- The `uuidMorphs` method is a convenience method that adds a `{column}_id` `CHAR(36)` equivalent column and a `{column}_type` `VARCHAR` equivalent column. -->
`uuidMorphs` 메서드는 `{column}_id` `CHAR(36)`과 동등한 컬럼과 `{column}_type` `VARCHAR`와 동등한 컬럼을 한 번에 추가하는 편의 메서드입니다.

<!-- This method is intended to be used when defining the columns necessary for a polymorphic [Eloquent relationship](/docs/10.x/eloquent-relationships) that use UUID identifiers. In the following example, `taggable_id` and `taggable_type` columns would be created: -->
이 메서드는 UUID 식별자를 사용하는 다형성 [Eloquent relationship](/docs/10.x/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용됩니다. 아래 예시에서는 `taggable_id`와 `taggable_type` 컬럼이 생성됩니다.

```
$table->uuidMorphs('taggable');
```

<a name="column-method-ulid"></a>
<!-- #### `ulid()` -->
#### `ulid()`

<!-- The `ulid` method creates a `ULID` equivalent column: -->
`ulid` 메서드는 `ULID`와 동등한 컬럼을 생성합니다.

```
$table->ulid('id');
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
위에서 소개한 컬럼 타입 외에도, 데이터베이스 테이블에 컬럼을 추가할 때 사용할 수 있는 다양한 "컬럼 수정자(modifiers)"가 있습니다. 예를 들어 컬럼을 "nullable"로 지정하고 싶을 때는 `nullable` 메서드를 사용할 수 있습니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

<!-- The following table contains all of the available column modifiers. This list does not include [index modifiers](#creating-indexes): -->
아래 표는 사용 가능한 모든 컬럼 수정자를 정리한 것입니다. 이 목록에는 [index modifiers](#creating-indexes)는 포함되어 있지 않습니다.

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
`->useCurrentOnUpdate()`  |  Set TIMESTAMP columns to use CURRENT_TIMESTAMP when a record is updated (MySQL).
`->virtualAs($expression)`  |  Create a virtual generated column (MySQL / PostgreSQL / SQLite).
`->generatedAs($expression)`  |  Create an identity column with specified sequence options (PostgreSQL).
`->always()`  |  Defines the precedence of sequence values over input for an identity column (PostgreSQL).
`->isGeometry()`  |  Set spatial column type to `geometry` - the default type is `geography` (PostgreSQL).
-->
Modifier  |  설명
--------  |  -----------
`->after('column')`  |  지정한 컬럼 바로 "뒤"에 해당 컬럼을 배치합니다 (MySQL).
`->autoIncrement()`  |  INTEGER 컬럼을 auto-increment(기본키)로 설정합니다.
`->charset('utf8mb4')`  |  컬럼의 문자셋(charset)을 지정합니다 (MySQL).
`->collation('utf8mb4_unicode_ci')`  |  컬럼의 정렬 방식(collation)을 지정합니다 (MySQL/PostgreSQL/SQL Server).
`->comment('my comment')`  |  컬럼에 주석(comment)을 추가합니다 (MySQL/PostgreSQL).
`->default($value)`  |  컬럼의 "기본값(default)"을 지정합니다.
`->first()`  |  해당 컬럼을 테이블의 "가장 처음"에 배치합니다 (MySQL).
`->from($integer)`  |  자동증가 필드의 시작값을 지정합니다 (MySQL / PostgreSQL).
`->invisible()`  |  `SELECT *` 쿼리에서 해당 컬럼을 "감춤" 상태로 지정합니다 (MySQL).
`->nullable($value = true)`  |  이 컬럼에 NULL 값을 저장할 수 있도록 허용합니다.
`->storedAs($expression)`  |  저장된 계산 컬럼(stored generated column)을 생성합니다 (MySQL / PostgreSQL).
`->unsigned()`  |  INTEGER 컬럼을 UNSIGNED로 지정합니다 (MySQL).
`->useCurrent()`  |  TIMESTAMP 컬럼의 기본값을 CURRENT_TIMESTAMP로 지정합니다.
`->useCurrentOnUpdate()`  |  레코드가 수정될 때 TIMESTAMP 컬럼에 CURRENT_TIMESTAMP가 자동으로 반영되도록 합니다 (MySQL).
`->virtualAs($expression)`  |  가상 생성 컬럼(virtual generated column)을 생성합니다 (MySQL / PostgreSQL / SQLite).
`->generatedAs($expression)`  |  지정한 시퀀스 옵션으로 아이덴티티 컬럼(identity column)을 생성합니다 (PostgreSQL).
`->always()`  |  아이덴티티 컬럼에서 입력값보다 시퀀스 값을 우선적으로 지정합니다 (PostgreSQL).
`->isGeometry()`  |  공간 컬럼의 타입을 기본값인 `geography` 대신 `geometry`로 지정합니다 (PostgreSQL).

<a name="default-expressions"></a>

<!-- #### Default Expressions -->
#### Default Expressions

<!-- The `default` modifier accepts a value or an `Illuminate\Database\Query\Expression` instance. Using an `Expression` instance will prevent Laravel from wrapping the value in quotes and allow you to use database specific functions. One situation where this is particularly useful is when you need to assign default values to JSON columns: -->
`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 인수로 받을 수 있습니다. `Expression` 인스턴스를 사용하면 Laravel이 해당 값을 따옴표로 감싸지 않으므로 데이터베이스 고유의 함수를 사용할 수 있습니다. 이 기능이 특히 유용한 대표적인 사례는 JSON 컬럼에 기본값을 할당해야 할 때입니다.

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
> 기본 표현식의 지원 여부는 데이터베이스 드라이버, 데이터베이스 버전, 컬럼 타입에 따라 다릅니다. 반드시 본인의 데이터베이스 공식 문서를 확인하십시오.

<a name="column-order"></a>
<!-- #### Column Order -->
#### Column Order

<!-- When using the MySQL database, the `after` method may be used to add columns after an existing column in the schema: -->
MySQL 데이터베이스를 사용할 때, `after` 메서드를 활용하여 기존 컬럼 뒤에 새로운 컬럼들을 추가할 수 있습니다.

```
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```

<a name="modifying-columns"></a>
<!-- ### Modifying Columns -->
### Modifying Columns

<!-- The `change` method allows you to modify the type and attributes of existing columns. For example, you may wish to increase the size of a `string` column. To see the `change` method in action, let's increase the size of the `name` column from 25 to 50. To accomplish this, we simply define the new state of the column and then call the `change` method: -->
`change` 메서드를 사용하면 기존 컬럼의 타입과 속성을 자유롭게 수정할 수 있습니다. 예를 들어, `string` 타입 컬럼의 길이를 늘리고 싶을 때 사용할 수 있습니다. `change` 메서드의 실제 사용 예를 보겠습니다. 아래처럼 `name` 컬럼의 길이를 25에서 50으로 늘리려면, 해당 컬럼의 새로운 속성을 정의한 후 `change` 메서드를 호출하면 됩니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```

<!-- When modifying a column, you must explicitly include all of the modifiers you want to keep on the column definition - any missing attribute will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column: -->
컬럼을 수정할 때는, 해당 컬럼에 계속 적용하고 싶은 모든 수정자(modifier)를 명시적으로 포함해야 합니다. 명시하지 않은 속성은 삭제됩니다. 예를 들어, `unsigned`, `default`, `comment` 속성을 그대로 유지하려면 수정 시 각각의 수정자를 반드시 다시 선언해 주어야 합니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```

<a name="modifying-columns-on-sqlite"></a>
<!-- #### Modifying Columns on SQLite -->
#### Modifying Columns on SQLite

<!-- If your application is utilizing an SQLite database, you must install the `doctrine/dbal` package using the Composer package manager before modifying a column. The Doctrine DBAL library is used to determine the current state of the column and to create the SQL queries needed to make the requested changes to your column: -->
애플리케이션에서 SQLite 데이터베이스를 사용 중이라면, 컬럼을 수정하기 전에 Composer 패키지 매니저로 `doctrine/dbal` 패키지를 반드시 설치해야 합니다. Doctrine DBAL 라이브러리를 사용하면 컬럼의 현재 상태를 파악하고, 원하는 변경 작업에 필요한 SQL 쿼리를 생성하게 됩니다.

```
composer require doctrine/dbal
```

<!-- If you plan to modify columns created using the `timestamp` method, you must also add the following configuration to your application's `config/database.php` configuration file: -->
만약 `timestamp` 메서드로 생성한 컬럼을 수정하려는 경우, 애플리케이션의 `config/database.php` 설정 파일에 아래와 같은 구성을 추가해야 합니다.

```php
use Illuminate\Database\DBAL\TimestampType;

'dbal' => [
    'types' => [
        'timestamp' => TimestampType::class,
    ],
],
```

> [!WARNING]
> `doctrine/dbal` 패키지를 사용할 때 아래 컬럼 타입만 수정이 가능합니다: `bigInteger`, `binary`, `boolean`, `char`, `date`, `dateTime`, `dateTimeTz`, `decimal`, `double`, `integer`, `json`, `longText`, `mediumText`, `smallInteger`, `string`, `text`, `time`, `tinyText`, `unsignedBigInteger`, `unsignedInteger`, `unsignedSmallInteger`, `ulid`, `uuid`.

<a name="renaming-columns"></a>
<!-- ### Renaming Columns -->
### Renaming Columns

<!-- To rename a column, you may use the `renameColumn` method provided by the schema builder: -->
컬럼의 이름을 변경하려면, 스키마 빌더가 제공하는 `renameColumn` 메서드를 사용하면 됩니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```

<a name="renaming-columns-on-legacy-databases"></a>
<!-- #### Renaming Columns on Legacy Databases -->
#### Renaming Columns on Legacy Databases

<!-- If you are running a database installation older than one of the following releases, you should ensure that you have installed the `doctrine/dbal` library via the Composer package manager before renaming a column: -->
아래에 안내된 버전보다 낮은 데이터베이스 버전을 사용 중이라면, 컬럼 이름을 변경하기 전에 Composer 패키지 매니저를 통해 `doctrine/dbal` 라이브러리를 설치해야 합니다.

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
컬럼을 삭제하려면, 스키마 빌더에서 `dropColumn` 메서드를 사용할 수 있습니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```

<!-- You may drop multiple columns from a table by passing an array of column names to the `dropColumn` method: -->
여러 개의 컬럼을 한 번에 삭제하려면, 컬럼명 배열을 `dropColumn` 메서드에 전달하면 됩니다.

```
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```

<a name="dropping-columns-on-legacy-databases"></a>
<!-- #### Dropping Columns on Legacy Databases -->
#### Dropping Columns on Legacy Databases

<!-- If you are running a version of SQLite prior to `3.35.0`, you must install the `doctrine/dbal` package via the Composer package manager before the `dropColumn` method may be used. Dropping or modifying multiple columns within a single migration while using this package is not supported. -->
SQLite가 `3.35.0` 미만 버전이라면, `dropColumn` 메서드를 사용하기 전에 Composer로 `doctrine/dbal` 패키지를 설치해야 합니다. 이 패키지를 사용할 때 단일 마이그레이션 내에서 여러 컬럼을 동시에 삭제하거나 수정하는 작업은 지원되지 않습니다.

<a name="available-command-aliases"></a>
<!-- #### Available Command Aliases -->
#### Available Command Aliases

<!-- Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below: -->
Laravel은 자주 사용되는 컬럼을 삭제하기 위한 여러 편리한 메서드를 제공합니다. 아래 표에서 각 명령어의 기능을 확인할 수 있습니다.

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
Command  |  Description
-------  |  -----------
`$table->dropMorphs('morphable');`  |  `morphable_id`와 `morphable_type` 컬럼을 삭제합니다.
`$table->dropRememberToken();`  |  `remember_token` 컬럼을 삭제합니다.
`$table->dropSoftDeletes();`  |  `deleted_at` 컬럼을 삭제합니다.
`$table->dropSoftDeletesTz();`  |  `dropSoftDeletes()` 메서드의 별칭입니다.
`$table->dropTimestamps();`  |  `created_at`, `updated_at` 컬럼을 삭제합니다.
`$table->dropTimestampsTz();` |  `dropTimestamps()` 메서드의 별칭입니다.

<a name="indexes"></a>
<!-- ## Indexes -->
## Indexes

<a name="creating-indexes"></a>
<!-- ### Creating Indexes -->
### Creating Indexes

<!-- The Laravel schema builder supports several types of indexes. The following example creates a new `email` column and specifies that its values should be unique. To create the index, we can chain the `unique` method onto the column definition: -->
Laravel의 스키마 빌더는 여러 종류의 인덱스를 지원합니다. 아래 예제에서는 `email` 컬럼을 새로 추가하고 해당 컬럼 값이 유일해야 함을 명시합니다. 이때 `unique` 메서드를 컬럼 정의 뒤에 체이닝하면 인덱스가 생성됩니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```

<!-- Alternatively, you may create the index after defining the column. To do so, you should call the `unique` method on the schema builder blueprint. This method accepts the name of the column that should receive a unique index: -->
또는, 컬럼을 정의한 이후에 인덱스를 별도로 생성할 수도 있습니다. 이 경우, 스키마 블루프린트에서 `unique` 메서드를 호출하면 됩니다. 이 메서드는 유니크 인덱스를 적용할 컬럼명을 인수로 받습니다.

```
$table->unique('email');
```

<!-- You may even pass an array of columns to an index method to create a compound (or composite) index: -->
인덱스 메서드에 컬럼명 배열을 넘기면 복합(또는 조합) 인덱스도 생성할 수 있습니다.

```
$table->index(['account_id', 'created_at']);
```

<!-- When creating an index, Laravel will automatically generate an index name based on the table, column names, and the index type, but you may pass a second argument to the method to specify the index name yourself: -->
인덱스를 생성할 때 Laravel이 기본적으로 테이블명, 컬럼명, 인덱스 타입을 조합해 인덱스명을 자동 생성하지만, 두 번째 인수로 직접 인덱스명을 지정할 수도 있습니다.

```
$table->unique('email', 'unique_email');
```

<a name="available-index-types"></a>
<!-- #### Available Index Types -->
#### Available Index Types

<!-- Laravel's schema builder blueprint class provides methods for creating each type of index supported by Laravel. Each index method accepts an optional second argument to specify the name of the index. If omitted, the name will be derived from the names of the table and column(s) used for the index, as well as the index type. Each of the available index methods is described in the table below: -->
Laravel의 스키마 빌더 블루프린트 클래스는 Laravel에서 지원하는 모든 인덱스 타입을 메서드로 제공합니다. 각 인덱스 메서드는 옵션으로 인덱스명을 두 번째 인수로 받을 수 있습니다. 인덱스명을 생략하면, 테이블명과 컬럼명(들), 인덱스 타입을 조합해 인덱스명이 자동으로 생성됩니다. 아래 표에서 주요 인덱스 메서드를 확인할 수 있습니다.

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
Command  |  Description
-------  |  -----------
`$table->primary('id');`  |  기본키를 추가합니다.
`$table->primary(['id', 'parent_id']);`  |  복합 기본키를 추가합니다.
`$table->unique('email');`  |  유니크 인덱스를 추가합니다.
`$table->index('state');`  |  일반 인덱스를 추가합니다.
`$table->fullText('body');`  |  전문(full text) 인덱스를 추가합니다 (MySQL/PostgreSQL).
`$table->fullText('body')->language('english');`  |  지정한 언어의 전문 인덱스를 추가합니다 (PostgreSQL).
`$table->spatialIndex('location');`  |  공간 인덱스를 추가합니다 (SQLite 제외).

<a name="index-lengths-mysql-mariadb"></a>
<!-- #### Index Lengths and MySQL / MariaDB -->
#### Index Lengths and MySQL / MariaDB

<!-- By default, Laravel uses the `utf8mb4` character set. If you are running a version of MySQL older than the 5.7.7 release or MariaDB older than the 10.2.2 release, you may need to manually configure the default string length generated by migrations in order for MySQL to create indexes for them. You may configure the default string length by calling the `Schema::defaultStringLength` method within the `boot` method of your `App\Providers\AppServiceProvider` class: -->
Laravel은 기본적으로 `utf8mb4` 문자 집합을 사용합니다. MySQL이 5.7.7 미만 버전이거나 MariaDB가 10.2.2 미만 버전이라면, 마이그레이션에서 생성되는 문자열의 기본 길이를 수동으로 설정해야 인덱스를 정상적으로 생성할 수 있습니다. 이때 `App\Providers\AppServiceProvider`의 `boot` 메서드에서 `Schema::defaultStringLength` 메서드를 호출해 기본 문자열 길이를 설정할 수 있습니다.

```
use Illuminate\Support\Facades\Schema;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Schema::defaultStringLength(191);
}
```

<!-- Alternatively, you may enable the `innodb_large_prefix` option for your database. Refer to your database's documentation for instructions on how to properly enable this option. -->
또는 데이터베이스의 `innodb_large_prefix` 옵션을 활성화해서 사용할 수도 있습니다. 해당 옵션 활성화 방법은 데이터베이스 공식 문서를 참조하시기 바랍니다.

<a name="renaming-indexes"></a>
<!-- ### Renaming Indexes -->
### Renaming Indexes

<!-- To rename an index, you may use the `renameIndex` method provided by the schema builder blueprint. This method accepts the current index name as its first argument and the desired name as its second argument: -->
인덱스의 이름을 변경하려면, 스키마 빌더 블루프린트가 제공하는 `renameIndex` 메서드를 사용합니다. 첫 번째 인수로 현재 인덱스명, 두 번째 인수로 원하는 새 인덱스명을 전달하세요.

```
$table->renameIndex('from', 'to')
```

> [!WARNING]
> 애플리케이션이 SQLite 데이터베이스를 사용 중인 경우, `renameIndex` 메서드를 사용하기 전에 반드시 Composer로 `doctrine/dbal` 패키지를 설치해야 합니다.

<a name="dropping-indexes"></a>
<!-- ### Dropping Indexes -->
### Dropping Indexes

<!-- To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples: -->
인덱스를 삭제하려면, 반드시 인덱스명을 인수로 지정해야 합니다. Laravel은 테이블명, 인덱싱되는 컬럼명, 인덱스 타입을 조합해 인덱스명을 자동으로 부여합니다. 아래는 사용 예시입니다.

<!--
Command  |  Description
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  Drop a primary key from the "users" table.
`$table->dropUnique('users_email_unique');`  |  Drop a unique index from the "users" table.
`$table->dropIndex('geo_state_index');`  |  Drop a basic index from the "geo" table.
`$table->dropFullText('posts_body_fulltext');`  |  Drop a full text index from the "posts" table.
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  Drop a spatial index from the "geo" table  (except SQLite).
-->
Command  |  Description
-------  |  -----------
`$table->dropPrimary('users_id_primary');`  |  "users" 테이블의 기본키를 삭제합니다.
`$table->dropUnique('users_email_unique');`  |  "users" 테이블의 유니크 인덱스를 삭제합니다.
`$table->dropIndex('geo_state_index');`  |  "geo" 테이블의 일반 인덱스를 삭제합니다.
`$table->dropFullText('posts_body_fulltext');`  |  "posts" 테이블의 전문 인덱스를 삭제합니다.
`$table->dropSpatialIndex('geo_location_spatialindex');`  |  "geo" 테이블의 공간 인덱스를 삭제합니다 (SQLite 제외).

<!-- If you pass an array of columns into a method that drops indexes, the conventional index name will be generated based on the table name, columns, and index type: -->
여러 컬럼명을 배열로 전달해 인덱스를 삭제하면, 지정한 테이블명, 컬럼명, 인덱스 타입 기준으로 Laravel이 인덱스명을 자동으로 생성해 삭제하게 됩니다.

```
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```

<a name="foreign-key-constraints"></a>
<!-- ### Foreign Key Constraints -->
### Foreign Key Constraints

<!-- Laravel also provides support for creating foreign key constraints, which are used to force referential integrity at the database level. For example, let's define a `user_id` column on the `posts` table that references the `id` column on a `users` table: -->
Laravel은 데이터베이스 수준의 참조 무결성을 강제하는 외래 키(foreign key) 제약조건 기능도 제공합니다. 예를 들어, `posts` 테이블의 `user_id` 컬럼이 `users` 테이블의 `id` 컬럼을 참조하도록 정의할 수 있습니다.

```
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```

<!-- Since this syntax is rather verbose, Laravel provides additional, terser methods that use conventions to provide a better developer experience. When using the `foreignId` method to create your column, the example above can be rewritten like so: -->
이 문법은 다소 장황하므로, Laravel은 규약(convention)을 활용해 더 간결하게 작성할 수 있는 별도의 메서드도 제공합니다. `foreignId` 메서드를 사용하면 위 코드를 아래처럼 줄일 수 있습니다.

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```

<!-- The `foreignId` method creates an `UNSIGNED BIGINT` equivalent column, while the `constrained` method will use conventions to determine the table and column being referenced. If your table name does not match Laravel's conventions, you may manually provide it to the `constrained` method. In addition, the name that should be assigned to the generated index may be specified as well: -->
`foreignId` 메서드는 `UNSIGNED BIGINT`에 해당하는 컬럼을 생성하며, `constrained` 메서드는 규약에 따라 참조할 테이블과 컬럼을 자동으로 결정합니다. 만약 테이블명이 Laravel의 규약과 다르다면, `constrained` 메서드에 직접 테이블명을 지정할 수도 있습니다. 또한, 생성되는 인덱스명도 인수로 명시적으로 지정할 수 있습니다.

```
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```

<!-- You may also specify the desired action for the "on delete" and "on update" properties of the constraint: -->
제약조건의 "on delete", "on update" 행동도 아래처럼 지정할 수 있습니다.

```
$table->foreignId('user_id')
      ->constrained()
      ->onUpdate('cascade')
      ->onDelete('cascade');
```

<!-- An alternative, expressive syntax is also provided for these actions: -->
이러한 동작을 위한 더욱 명시적이고 직관적인 문법도 제공됩니다.

| Method                        | Description                                        |
|-------------------------------|---------------------------------------------------|
| `$table->cascadeOnUpdate();`  | 업데이트시 연결된 데이터도 함께 수정됩니다.             |
| `$table->restrictOnUpdate();` | 업데이트가 제한됩니다.                               |
| `$table->noActionOnUpdate();` | 업데이트 시 별도의 동작이 없습니다.                  |
| `$table->cascadeOnDelete();`  | 삭제 시 연결된 데이터도 함께 삭제됩니다.              |
| `$table->restrictOnDelete();` | 삭제가 제한됩니다.                                 |
| `$table->nullOnDelete();`     | 삭제 시 외래 키 값을 null로 설정합니다.              |

<!-- Any additional [column modifiers](#column-modifiers) must be called before the `constrained` method: -->
추가적인 [column modifiers](#column-modifiers)는 반드시 `constrained` 메서드 전에 호출해야 합니다.

```
$table->foreignId('user_id')
      ->nullable()
      ->constrained();
```

<a name="dropping-foreign-keys"></a>
<!-- #### Dropping Foreign Keys -->
#### Dropping Foreign Keys

<!-- To drop a foreign key, you may use the `dropForeign` method, passing the name of the foreign key constraint to be deleted as an argument. Foreign key constraints use the same naming convention as indexes. In other words, the foreign key constraint name is based on the name of the table and the columns in the constraint, followed by a "\_foreign" suffix: -->
외래 키를 삭제하려면, 삭제할 외래 키 제약조건명을 `dropForeign` 메서드에 인수로 전달하면 됩니다. 외래 키 제약조건명은 인덱스와 같은 규칙을 따르며, 테이블명-컬럼명_조합 뒤에 "\_foreign"이 붙는 형태입니다.

```
$table->dropForeign('posts_user_id_foreign');
```

<!-- Alternatively, you may pass an array containing the column name that holds the foreign key to the `dropForeign` method. The array will be converted to a foreign key constraint name using Laravel's constraint naming conventions: -->
또 다른 방법으로, 외래 키를 보유한 컬럼명을 배열로 `dropForeign` 메서드에 전달해도 됩니다. 이 배열은 Laravel의 제약조건 명명 규칙에 따라 외래 키 제약조건명으로 변환됩니다.

```
$table->dropForeign(['user_id']);
```

<a name="toggling-foreign-key-constraints"></a>
<!-- #### Toggling Foreign Key Constraints -->
#### Toggling Foreign Key Constraints

<!-- You may enable or disable foreign key constraints within your migrations by using the following methods: -->
마이그레이션 내에서 아래 메서드로 외래 키 제약조건을 전역적으로 활성화하거나 비활성화할 수 있습니다.

```
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> [!WARNING]
> SQLite는 기본적으로 외래 키 제약조건이 비활성화되어 있습니다. SQLite를 사용할 경우, 마이그레이션에서 외래 키를 생성하기 전에 [enable foreign key support](/docs/10.x/database#configuration)이 데이터베이스 설정에 활성화되어 있는지 반드시 확인하십시오. 또한, SQLite는 테이블 생성 시에만 외래 키 제약조건을 지원하며, [not when tables are altered](https://www.sqlite.org/omitted.html).

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- For convenience, each migration operation will dispatch an [event](/docs/10.x/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class: -->
각 마이그레이션 작업은 [event](/docs/10.x/events)를 자동으로 디스패치(dispatch)합니다. 아래 이벤트들은 모두 기본 클래스인 `Illuminate\Database\Events\MigrationEvent`를 상속합니다.

<!--
 Class | Description
-------|-------
-->
 Class | Description
-------|-------
| `Illuminate\Database\Events\MigrationsStarted` | 여러 개의 마이그레이션 실행이 곧 시작됨을 알립니다. |
| `Illuminate\Database\Events\MigrationsEnded` | 여러 개의 마이그레이션 실행이 모두 완료되었음을 알립니다. |
| `Illuminate\Database\Events\MigrationStarted` | 단일 마이그레이션 시작 직전 이벤트입니다. |
| `Illuminate\Database\Events\MigrationEnded` | 단일 마이그레이션 종료 후 이벤트입니다. |
| `Illuminate\Database\Events\SchemaDumped` | 데이터베이스 스키마 덤프가 완료되었음을 알립니다. |
| `Illuminate\Database\Events\SchemaLoaded` | 기존 데이터베이스 스키마 덤프가 로드되었음을 알립니다. |
