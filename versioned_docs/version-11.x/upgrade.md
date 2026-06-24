<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 11.0 From 10.x](#upgrade-11.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Application Structure](#application-structure)
- [Floating-Point Types](#floating-point-types)
- [Modifying Columns](#modifying-columns)
- [SQLite Minimum Version](#sqlite-minimum-version)
- [Updating Sanctum](#updating-sanctum)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [Password Rehashing](#password-rehashing)
- [Per-Second Rate Limiting](#per-second-rate-limiting)
- [Spatie Once Package](#spatie-once-package)

<!-- </div> -->
</div>

<a name="low-impact-changes"></a>
<!-- ## Low Impact Changes -->
## Low Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Doctrine DBAL Removal](#doctrine-dbal-removal)
- [Eloquent Model `casts` Method](#eloquent-model-casts-method)
- [Spatial Types](#spatial-types)
- [The `Enumerable` Contract](#the-enumerable-contract)
- [The `UserProvider` Contract](#the-user-provider-contract)
- [The `Authenticatable` Contract](#the-authenticatable-contract)

<!-- </div> -->
</div>

<a name="upgrade-11.0"></a>
<!-- ## Upgrading To 11.0 From 10.x -->
## Upgrading To 11.0 From 10.x

<a name="estimated-upgrade-time-??-minutes"></a>
<!-- #### Estimated Upgrade Time: 15 Minutes -->
#### Estimated Upgrade Time: 15 Minutes

> [!NOTE]
> 가능한 모든 주요 변경 사항을 문서화하려고 노력했습니다. 다만 일부 주요 변경 사항은 프레임워크의 잘 알려지지 않은 부분에 해당하므로, 실제로는 이 변경 사항 중 일부만 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶다면 [Laravel Shift](https://laravelshift.com/)를 사용하여 애플리케이션 업그레이드를 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- #### PHP 8.2.0 Required -->
#### PHP 8.2.0 Required

<!-- Laravel now requires PHP 8.2.0 or greater. -->
Laravel은 이제 PHP 8.2.0 이상을 필요로 합니다.

<!-- #### curl 7.34.0 Required -->
#### curl 7.34.0 Required

<!-- Laravel's HTTP client now requires curl 7.34.0 or greater. -->
Laravel의 HTTP 클라이언트는 이제 curl 7.34.0 이상을 필요로 합니다.

<!-- #### Composer Dependencies -->
#### Composer Dependencies

<!-- You should update the following dependencies in your application's `composer.json` file: -->
애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `laravel/framework` to `^11.0`
- `nunomaduro/collision` to `^8.1`
- `laravel/breeze` to `^2.0` (If installed)
- `laravel/cashier` to `^15.0` (If installed)
- `laravel/dusk` to `^8.0` (If installed)
- `laravel/jetstream` to `^5.0` (If installed)
- `laravel/octane` to `^2.3` (If installed)
- `laravel/passport` to `^12.0` (If installed)
- `laravel/sanctum` to `^4.0` (If installed)
- `laravel/scout` to `^10.0` (If installed)
- `laravel/spark-stripe` to `^5.0` (If installed)
- `laravel/telescope` to `^5.0` (If installed)
- `livewire/livewire` to `^3.4` (If installed)
- `inertiajs/inertia-laravel` to `^1.0` (If installed)
-->
- `laravel/framework`를 `^11.0`으로
- `nunomaduro/collision`을 `^8.1`로
- `laravel/breeze`를 `^2.0`으로 (설치된 경우)
- `laravel/cashier`를 `^15.0`으로 (설치된 경우)
- `laravel/dusk`를 `^8.0`으로 (설치된 경우)
- `laravel/jetstream`을 `^5.0`으로 (설치된 경우)
- `laravel/octane`을 `^2.3`으로 (설치된 경우)
- `laravel/passport`를 `^12.0`으로 (설치된 경우)
- `laravel/sanctum`을 `^4.0`으로 (설치된 경우)
- `laravel/scout`를 `^10.0`으로 (설치된 경우)
- `laravel/spark-stripe`를 `^5.0`으로 (설치된 경우)
- `laravel/telescope`를 `^5.0`으로 (설치된 경우)
- `livewire/livewire`를 `^3.4`로 (설치된 경우)
- `inertiajs/inertia-laravel`을 `^1.0`으로 (설치된 경우)

<!-- </div> -->
</div>

<!-- If your application is using Laravel Cashier Stripe, Passport, Sanctum, Spark Stripe, or Telescope, you will need to publish their migrations to your application. Cashier Stripe, Passport, Sanctum, Spark Stripe, and Telescope **no longer automatically load migrations from their own migrations** directory. Therefore, you should run the following command to publish their migrations to your application: -->
애플리케이션에서 Laravel Cashier Stripe, Passport, Sanctum, Spark Stripe 또는 Telescope를 사용하고 있다면, 해당 패키지의 마이그레이션을 애플리케이션에 퍼블리시해야 합니다. Cashier Stripe, Passport, Sanctum, Spark Stripe, Telescope는 **더 이상 자체 migrations 디렉터리에서 마이그레이션을 자동으로 로드하지 않습니다**. 따라서 다음 명령어를 실행하여 해당 마이그레이션을 애플리케이션에 퍼블리시해야 합니다.

```bash
php artisan vendor:publish --tag=cashier-migrations
php artisan vendor:publish --tag=passport-migrations
php artisan vendor:publish --tag=sanctum-migrations
php artisan vendor:publish --tag=spark-migrations
php artisan vendor:publish --tag=telescope-migrations
```

<!-- In addition, you should review the upgrade guides for each of these packages to ensure you are aware of any additional breaking changes: -->
또한 추가적인 주요 변경 사항을 확인할 수 있도록 각 패키지의 업그레이드 가이드를 검토해야 합니다.

- [Laravel Cashier Stripe](#cashier-stripe)
- [Laravel Passport](#passport)
- [Laravel Sanctum](#sanctum)
- [Laravel Spark Stripe](#spark-stripe)
- [Laravel Telescope](#telescope)

<!-- If you have manually installed the Laravel installer, you should update the installer via Composer: -->
Laravel installer를 수동으로 설치했다면 Composer를 통해 installer를 업데이트해야 합니다.

```bash
composer global require laravel/installer:^5.6
```

<!-- Finally, you may remove the `doctrine/dbal` Composer dependency if you have previously added it to your application, as Laravel is no longer dependent on this package. -->
마지막으로, 이전에 애플리케이션에 `doctrine/dbal` Composer 의존성을 추가했다면 제거해도 됩니다. Laravel은 더 이상 이 패키지에 의존하지 않습니다.

<a name="application-structure"></a>
<!-- ### Application Structure -->
### Application Structure

<!-- Laravel 11 introduces a new default application structure with fewer default files. Namely, new Laravel applications contain fewer service providers, middleware, and configuration files. -->
Laravel 11은 기본 파일 수를 줄인 새로운 기본 애플리케이션 구조를 도입합니다. 즉, 새 Laravel 애플리케이션에는 service provider, middleware, 설정 파일이 더 적게 포함됩니다.

<!-- However, we do **not recommend** that Laravel 10 applications upgrading to Laravel 11 attempt to migrate their application structure, as Laravel 11 has been carefully tuned to also support the Laravel 10 application structure. -->
하지만 Laravel 11은 Laravel 10 애플리케이션 구조도 지원하도록 세심하게 조정되어 있으므로, Laravel 10 애플리케이션을 Laravel 11로 업그레이드할 때 애플리케이션 구조까지 마이그레이션하는 것은 **권장하지 않습니다**.

<a name="authentication"></a>
<!-- ### Authentication -->
### Authentication

<a name="password-rehashing"></a>
<!-- #### Password Rehashing -->
#### Password Rehashing

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Laravel 11 will automatically rehash your user's passwords during authentication if your hashing algorithm's "work factor" has been updated since the password was last hashed. -->
Laravel 11은 사용자의 비밀번호가 마지막으로 해싱된 이후 해싱 알고리즘의 "work factor"가 업데이트된 경우, 인증 과정에서 사용자의 비밀번호를 자동으로 다시 해싱합니다.

<!-- Typically, this should not disrupt your application; however, if your `User` model's "password" field has a name other than `password`, you should specify the field's name via the model's `authPasswordName` property: -->
일반적으로 이는 애플리케이션에 문제를 일으키지 않습니다. 하지만 `User` 모델의 "password" 필드명이 `password`가 아니라면, 모델의 `authPasswordName` 속성을 통해 필드명을 지정해야 합니다.

```
protected $authPasswordName = 'custom_password_field';
```

<!-- Alternatively, you may disable password rehashing by adding the `rehash_on_login` option to your application's `config/hashing.php` configuration file: -->
또는 애플리케이션의 `config/hashing.php` 설정 파일에 `rehash_on_login` 옵션을 추가하여 비밀번호 재해싱을 비활성화할 수 있습니다.

```
'rehash_on_login' => false,
```

<a name="the-user-provider-contract"></a>
<!-- #### The `UserProvider` Contract -->
#### The `UserProvider` Contract

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Illuminate\Contracts\Auth\UserProvider` contract has received a new `rehashPasswordIfRequired` method. This method is responsible for re-hashing and storing the user's password in storage when the application's hashing algorithm work factor has changed. -->
`Illuminate\Contracts\Auth\UserProvider` 계약에 새로운 `rehashPasswordIfRequired` 메서드가 추가되었습니다. 이 메서드는 애플리케이션의 해싱 알고리즘 work factor가 변경되었을 때 사용자의 비밀번호를 다시 해싱하고 저장소에 저장하는 역할을 합니다.

<!-- If your application or package defines a class that implements this interface, you should add the new `rehashPasswordIfRequired` method to your implementation. A reference implementation can be found within the `Illuminate\Auth\EloquentUserProvider` class: -->
애플리케이션이나 패키지에서 이 인터페이스를 구현하는 클래스를 정의하고 있다면, 구현체에 새로운 `rehashPasswordIfRequired` 메서드를 추가해야 합니다. 참고 구현은 `Illuminate\Auth\EloquentUserProvider` 클래스에서 확인할 수 있습니다.

```php
public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
```

<a name="the-authenticatable-contract"></a>
<!-- #### The `Authenticatable` Contract -->
#### The `Authenticatable` Contract

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Illuminate\Contracts\Auth\Authenticatable` contract has received a new `getAuthPasswordName` method. This method is responsible for returning the name of your authenticatable entity's password column. -->
`Illuminate\Contracts\Auth\Authenticatable` 계약에 새로운 `getAuthPasswordName` 메서드가 추가되었습니다. 이 메서드는 인증 가능한 엔티티의 비밀번호 컬럼 이름을 반환하는 역할을 합니다.

<!-- If your application or package defines a class that implements this interface, you should add the new `getAuthPasswordName` method to your implementation: -->
애플리케이션이나 패키지에서 이 인터페이스를 구현하는 클래스를 정의하고 있다면, 구현체에 새로운 `getAuthPasswordName` 메서드를 추가해야 합니다.

```php
public function getAuthPasswordName()
{
    return 'password';
}
```

<!-- The default `User` model included with Laravel receives this method automatically since the method is included within the `Illuminate\Auth\Authenticatable` trait. -->
Laravel에 포함된 기본 `User` 모델은 이 메서드를 자동으로 제공받습니다. 해당 메서드가 `Illuminate\Auth\Authenticatable` trait에 포함되어 있기 때문입니다.

<a name="the-authentication-exception-class"></a>
<!-- #### The `AuthenticationException` Class -->
#### The `AuthenticationException` Class

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `redirectTo` method of the `Illuminate\Auth\AuthenticationException` class now requires an `Illuminate\Http\Request` instance as its first argument. If you are manually catching this exception and calling the `redirectTo` method, you should update your code accordingly: -->
`Illuminate\Auth\AuthenticationException` 클래스의 `redirectTo` 메서드는 이제 첫 번째 인수로 `Illuminate\Http\Request` 인스턴스를 필요로 합니다. 이 예외를 수동으로 잡아 `redirectTo` 메서드를 호출하고 있다면, 이에 맞게 코드를 업데이트해야 합니다.

```php
if ($e instanceof AuthenticationException) {
    $path = $e->redirectTo($request);
}
```

<a name="email-verification-notification-on-registration"></a>
<!-- #### Email Verification Notification on Registration -->
#### Email Verification Notification on Registration

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `SendEmailVerificationNotification` listener is now automatically registered for the `Registered` event if it is not already registered by your application's `EventServiceProvider`. If your application's `EventServiceProvider` does not register this listener and you do not want Laravel to automatically register it for you, you should define an empty `configureEmailVerification` method in your application's `EventServiceProvider`: -->
`SendEmailVerificationNotification` 리스너가 애플리케이션의 `EventServiceProvider`에 이미 등록되어 있지 않은 경우, 이제 `Registered` 이벤트에 자동으로 등록됩니다. 애플리케이션의 `EventServiceProvider`에서 이 리스너를 등록하지 않고 있으며, Laravel이 자동으로 등록하는 것도 원하지 않는다면 애플리케이션의 `EventServiceProvider`에 비어 있는 `configureEmailVerification` 메서드를 정의해야 합니다.

```php
protected function configureEmailVerification()
{
    // ...
}
```

<a name="cache"></a>
<!-- ### Cache -->
### Cache

<a name="cache-key-prefixes"></a>
<!-- #### Cache Key Prefixes -->
#### Cache Key Prefixes

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- Previously, if a cache key prefix was defined for the DynamoDB, Memcached, or Redis cache stores, Laravel would append a `:` to the prefix. In Laravel 11, the cache key prefix does not receive the `:` suffix. If you would like to maintain the previous prefixing behavior, you can manually add the `:` suffix to your cache key prefix. -->
이전에는 DynamoDB, Memcached 또는 Redis 캐시 스토어에 캐시 키 접두사가 정의되어 있으면 Laravel이 접두사 뒤에 `:`를 추가했습니다. Laravel 11에서는 캐시 키 접두사에 `:` 접미사가 추가되지 않습니다. 이전의 접두사 동작을 유지하고 싶다면 캐시 키 접두사에 `:` 접미사를 수동으로 추가할 수 있습니다.

<a name="collections"></a>
<!-- ### Collections -->
### Collections

<a name="the-enumerable-contract"></a>
<!-- #### The `Enumerable` Contract -->
#### The `Enumerable` Contract

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `dump` method of the `Illuminate\Support\Enumerable` contract has been updated to accept a variadic `...$args` argument. If you are implementing this interface you should update your implementation accordingly: -->
`Illuminate\Support\Enumerable` 계약의 `dump` 메서드가 가변 인수 `...$args`를 받을 수 있도록 업데이트되었습니다. 이 인터페이스를 구현하고 있다면 구현체도 이에 맞게 업데이트해야 합니다.

```php
public function dump(...$args);
```

<a name="database"></a>
<!-- ### Database -->
### Database

<a name="sqlite-minimum-version"></a>
<!-- #### SQLite 3.26.0+ -->
#### SQLite 3.26.0+

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- If your application is utilizing an SQLite database, SQLite 3.26.0 or greater is required. -->
애플리케이션에서 SQLite 데이터베이스를 사용하고 있다면 SQLite 3.26.0 이상이 필요합니다.

<a name="eloquent-model-casts-method"></a>
<!-- #### Eloquent Model `casts` Method -->
#### Eloquent Model `casts` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The base Eloquent model class now defines a `casts` method in order to support the definition of attribute casts. If one of your application's models is defining a `casts` relationship, it may conflict with the `casts` method now present on the base Eloquent model class. -->
기본 Eloquent 모델 클래스는 이제 속성 cast 정의를 지원하기 위해 `casts` 메서드를 정의합니다. 애플리케이션의 모델 중 하나가 `casts` 연관관계를 정의하고 있다면, 이제 기본 Eloquent 모델 클래스에 존재하는 `casts` 메서드와 충돌할 수 있습니다.

<a name="modifying-columns"></a>
<!-- #### Modifying Columns -->
#### Modifying Columns

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- When modifying a column, you must now explicitly include all the modifiers you want to keep on the column definition after it is changed. Any missing attributes will be dropped. For example, to retain the `unsigned`, `default`, and `comment` attributes, you must call each modifier explicitly when changing the column, even if those attributes have been assigned to the column by a previous migration. -->
컬럼을 수정할 때는 변경 후에도 컬럼 정의에 유지하려는 모든 수정자를 명시적으로 포함해야 합니다. 누락된 속성은 제거됩니다. 예를 들어 `unsigned`, `default`, `comment` 속성을 유지하려면, 이전 마이그레이션에서 이미 해당 속성이 컬럼에 할당되었더라도 컬럼을 변경할 때 각 수정자를 명시적으로 호출해야 합니다.

<!-- For example, imagine you have a migration that creates a `votes` column with the `unsigned`, `default`, and `comment` attributes: -->
예를 들어 `unsigned`, `default`, `comment` 속성이 있는 `votes` 컬럼을 생성하는 마이그레이션이 있다고 가정해 보겠습니다.

```php
Schema::create('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('The vote count');
});
```

<!-- Later, you write a migration that changes the column to be `nullable` as well: -->
나중에 해당 컬럼을 `nullable`로도 변경하는 마이그레이션을 작성합니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->nullable()->change();
});
```

<!-- In Laravel 10, this migration would retain the `unsigned`, `default`, and `comment` attributes on the column. However, in Laravel 11, the migration must now also include all of the attributes that were previously defined on the column. Otherwise, they will be dropped: -->
Laravel 10에서는 이 마이그레이션이 컬럼의 `unsigned`, `default`, `comment` 속성을 유지했습니다. 하지만 Laravel 11에서는 이전에 컬럼에 정의되어 있던 모든 속성도 마이그레이션에 포함해야 합니다. 그렇지 않으면 해당 속성들이 제거됩니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')
        ->unsigned()
        ->default(1)
        ->comment('The vote count')
        ->nullable()
        ->change();
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

<!-- If you do not want to update all of the existing "change" migrations in your application to retain the column's existing attributes, you may simply [squash your migrations](/docs/11.x/migrations#squashing-migrations): -->
컬럼의 기존 속성을 유지하기 위해 애플리케이션의 기존 "change" 마이그레이션을 모두 업데이트하고 싶지 않다면, 간단히 [squash your migrations](/docs/11.x/migrations#squashing-migrations)할 수 있습니다.

```bash
php artisan schema:dump
```

<!-- Once your migrations have been squashed, Laravel will "migrate" the database using your application's schema file before running any pending migrations. -->
마이그레이션을 스쿼시한 후에는 Laravel이 대기 중인 마이그레이션을 실행하기 전에 애플리케이션의 스키마 파일을 사용하여 데이터베이스를 "마이그레이션"합니다.

<a name="floating-point-types"></a>
<!-- #### Floating-Point Types -->
#### Floating-Point Types

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- The `double` and `float` migration column types have been rewritten to be consistent across all databases. -->
`double` 및 `float` 마이그레이션 컬럼 타입은 모든 데이터베이스에서 일관되게 동작하도록 다시 작성되었습니다.

<!-- The `double` column type now creates a `DOUBLE` equivalent column without total digits and places (digits after decimal point), which is the standard SQL syntax. Therefore, you may remove the arguments for `$total` and `$places`: -->
`double` 컬럼 타입은 이제 전체 자릿수와 소수점 이하 자릿수 없이, 표준 SQL 문법에 맞는 `DOUBLE` 동등 컬럼을 생성합니다. 따라서 `$total` 및 `$places` 인수를 제거할 수 있습니다.

```php
$table->double('amount');
```

<!-- The `float` column type now creates a `FLOAT` equivalent column without total digits and places (digits after decimal point), but with an optional `$precision` specification to determine storage size as a 4-byte single-precision column or an 8-byte double-precision column. Therefore, you may remove the arguments for `$total` and `$places` and specify the optional `$precision` to your desired value and according to your database's documentation: -->
`float` 컬럼 타입은 이제 전체 자릿수와 소수점 이하 자릿수 없이 `FLOAT` 동등 컬럼을 생성합니다. 다만 저장 크기를 4바이트 단정밀도 컬럼 또는 8바이트 배정밀도 컬럼으로 결정하기 위한 선택적 `$precision` 지정은 지원합니다. 따라서 `$total` 및 `$places` 인수를 제거하고, 원하는 값과 데이터베이스 문서에 맞게 선택적 `$precision`을 지정할 수 있습니다.

```php
$table->float('amount', precision: 53);
```

<!-- The `unsignedDecimal`, `unsignedDouble`, and `unsignedFloat` methods have been removed, as the unsigned modifier for these column types has been deprecated by MySQL, and was never standardized on other database systems. However, if you wish to continue using the deprecated unsigned attribute for these column types, you may chain the `unsigned` method onto the column's definition: -->
`unsignedDecimal`, `unsignedDouble`, `unsignedFloat` 메서드는 제거되었습니다. 이러한 컬럼 타입에 대한 unsigned 수정자는 MySQL에서 더 이상 권장되지 않으며, 다른 데이터베이스 시스템에서도 표준화된 적이 없기 때문입니다. 하지만 이러한 컬럼 타입에 대해 더 이상 권장되지 않는 unsigned 속성을 계속 사용하고 싶다면, 컬럼 정의에 `unsigned` 메서드를 체이닝할 수 있습니다.

```php
$table->decimal('amount', total: 8, places: 2)->unsigned();
$table->double('amount')->unsigned();
$table->float('amount', precision: 53)->unsigned();
```

<a name="dedicated-mariadb-driver"></a>
<!-- #### Dedicated MariaDB Driver -->
#### Dedicated MariaDB Driver

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- Instead of always utilizing the MySQL driver when connecting to MariaDB databases, Laravel 11 adds a dedicated database driver for MariaDB. -->
MariaDB 데이터베이스에 연결할 때 항상 MySQL 드라이버를 사용하는 대신, Laravel 11은 MariaDB용 전용 데이터베이스 드라이버를 추가합니다.

<!-- If your application connects to a MariaDB database, you may update the connection configuration to the new `mariadb` driver to benefit from MariaDB specific features in the future: -->
애플리케이션이 MariaDB 데이터베이스에 연결한다면, 앞으로 MariaDB 전용 기능을 활용할 수 있도록 연결 설정을 새로운 `mariadb` 드라이버로 업데이트할 수 있습니다.

```
'driver' => 'mariadb',
'url' => env('DB_URL'),
'host' => env('DB_HOST', '127.0.0.1'),
'port' => env('DB_PORT', '3306'),
// ...
```

<!-- Currently, the new MariaDB driver behaves like the current MySQL driver with one exception: the `uuid` schema builder method creates native UUID columns instead of `char(36)` columns. -->
현재 새 MariaDB 드라이버는 한 가지 예외를 제외하면 기존 MySQL 드라이버처럼 동작합니다. 그 예외는 `uuid` 스키마 빌더 메서드가 `char(36)` 컬럼 대신 네이티브 UUID 컬럼을 생성한다는 점입니다.

<!-- If your existing migrations utilize the `uuid` schema builder method and you choose to use the new `mariadb` database driver, you should update your migration's invocations of the `uuid` method to `char` to avoid breaking changes or unexpected behavior: -->
기존 마이그레이션에서 `uuid` 스키마 빌더 메서드를 사용하고 있고 새 `mariadb` 데이터베이스 드라이버를 사용하기로 선택했다면, 주요 변경 사항이나 예상치 못한 동작을 피하기 위해 마이그레이션에서 `uuid` 메서드를 호출한 부분을 `char`로 업데이트해야 합니다.

```php
Schema::table('users', function (Blueprint $table) {
    $table->char('uuid', 36);

    // ...
});
```

<a name="spatial-types"></a>
<!-- #### Spatial Types -->
#### Spatial Types

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The spatial column types of database migrations have been rewritten to be consistent across all databases. Therefore, you may remove `point`, `lineString`, `polygon`, `geometryCollection`, `multiPoint`, `multiLineString`, `multiPolygon`, and `multiPolygonZ` methods from your migrations and use `geometry` or `geography` methods instead: -->
데이터베이스 마이그레이션의 공간 컬럼 타입은 모든 데이터베이스에서 일관되게 동작하도록 다시 작성되었습니다. 따라서 마이그레이션에서 `point`, `lineString`, `polygon`, `geometryCollection`, `multiPoint`, `multiLineString`, `multiPolygon`, `multiPolygonZ` 메서드를 제거하고 대신 `geometry` 또는 `geography` 메서드를 사용할 수 있습니다.

```php
$table->geometry('shapes');
$table->geography('coordinates');
```

<!-- To explicitly restrict the type or the spatial reference system identifier for values stored in the column on MySQL, MariaDB, and PostgreSQL, you may pass the `subtype` and `srid` to the method: -->
MySQL, MariaDB, PostgreSQL에서 컬럼에 저장되는 값의 타입이나 공간 참조 시스템 식별자를 명시적으로 제한하려면, 메서드에 `subtype` 및 `srid`를 전달할 수 있습니다.

```php
$table->geometry('dimension', subtype: 'polygon', srid: 0);
$table->geography('latitude', subtype: 'point', srid: 4326);
```

<!-- The `isGeometry` and `projection` column modifiers of the PostgreSQL grammar have been removed accordingly. -->
이에 따라 PostgreSQL grammar의 `isGeometry` 및 `projection` 컬럼 수정자가 제거되었습니다.

<a name="doctrine-dbal-removal"></a>
<!-- #### Doctrine DBAL Removal -->
#### Doctrine DBAL Removal

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The following list of Doctrine DBAL related classes and methods have been removed. Laravel is no longer dependent on this package and registering custom Doctrines types is no longer necessary for the proper creation and alteration of various column types that previously required custom types: -->
다음 Doctrine DBAL 관련 클래스와 메서드가 제거되었습니다. Laravel은 더 이상 이 패키지에 의존하지 않으며, 이전에 사용자 정의 타입이 필요했던 여러 컬럼 타입을 올바르게 생성하고 변경하기 위해 사용자 정의 Doctrine 타입을 등록할 필요도 더 이상 없습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `Illuminate\Database\Schema\Builder::$alwaysUsesNativeSchemaOperationsIfPossible` class property
- `Illuminate\Database\Schema\Builder::useNativeSchemaOperationsIfPossible()` method
- `Illuminate\Database\Connection::usingNativeSchemaOperations()` method
- `Illuminate\Database\Connection::isDoctrineAvailable()` method
- `Illuminate\Database\Connection::getDoctrineConnection()` method
- `Illuminate\Database\Connection::getDoctrineSchemaManager()` method
- `Illuminate\Database\Connection::getDoctrineColumn()` method
- `Illuminate\Database\Connection::registerDoctrineType()` method
- `Illuminate\Database\DatabaseManager::registerDoctrineType()` method
- `Illuminate\Database\PDO` directory
- `Illuminate\Database\DBAL\TimestampType` class
- `Illuminate\Database\Schema\Grammars\ChangeColumn` class
- `Illuminate\Database\Schema\Grammars\RenameColumn` class
- `Illuminate\Database\Schema\Grammars\Grammar::getDoctrineTableDiff()` method
-->
- `Illuminate\Database\Schema\Builder::$alwaysUsesNativeSchemaOperationsIfPossible` 클래스 속성
- `Illuminate\Database\Schema\Builder::useNativeSchemaOperationsIfPossible()` 메서드
- `Illuminate\Database\Connection::usingNativeSchemaOperations()` 메서드
- `Illuminate\Database\Connection::isDoctrineAvailable()` 메서드
- `Illuminate\Database\Connection::getDoctrineConnection()` 메서드
- `Illuminate\Database\Connection::getDoctrineSchemaManager()` 메서드
- `Illuminate\Database\Connection::getDoctrineColumn()` 메서드
- `Illuminate\Database\Connection::registerDoctrineType()` 메서드
- `Illuminate\Database\DatabaseManager::registerDoctrineType()` 메서드
- `Illuminate\Database\PDO` 디렉터리
- `Illuminate\Database\DBAL\TimestampType` 클래스
- `Illuminate\Database\Schema\Grammars\ChangeColumn` 클래스
- `Illuminate\Database\Schema\Grammars\RenameColumn` 클래스
- `Illuminate\Database\Schema\Grammars\Grammar::getDoctrineTableDiff()` 메서드

<!-- </div> -->
</div>

<!-- In addition, registering custom Doctrine types via `dbal.types` in your application's `database` configuration file is no longer required. -->
또한 애플리케이션의 `database` 설정 파일에서 `dbal.types`를 통해 사용자 정의 Doctrine 타입을 등록할 필요도 더 이상 없습니다.

<!-- If you were previously using Doctrine DBAL to inspect your database and its associated tables, you may use Laravel's new native schema methods (`Schema::getTables()`, `Schema::getColumns()`, `Schema::getIndexes()`, `Schema::getForeignKeys()`, etc.) instead. -->
이전에 Doctrine DBAL을 사용하여 데이터베이스와 관련 테이블을 검사하고 있었다면, 대신 Laravel의 새로운 네이티브 스키마 메서드(`Schema::getTables()`, `Schema::getColumns()`, `Schema::getIndexes()`, `Schema::getForeignKeys()` 등)를 사용할 수 있습니다.

<a name="deprecated-schema-methods"></a>
<!-- #### Deprecated Schema Methods -->
#### Deprecated Schema Methods
<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The deprecated, Doctrine based `Schema::getAllTables()`, `Schema::getAllViews()`, and `Schema::getAllTypes()` methods have been removed in favor of new Laravel native `Schema::getTables()`, `Schema::getViews()`, and `Schema::getTypes()` methods. -->
사용 중단된 Doctrine 기반 `Schema::getAllTables()`, `Schema::getAllViews()`, `Schema::getAllTypes()` 메서드는 새로운 Laravel 자체 `Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드로 대체되어 제거되었습니다.

<!-- When using PostgreSQL and SQL Server, none of the new schema methods will accept a three-part reference (e.g. `database.schema.table`). Therefore, you should use `connection()` to declare the database instead: -->
PostgreSQL과 SQL Server를 사용할 때 새 schema 메서드는 세 부분으로 된 참조(예: `database.schema.table`)를 허용하지 않습니다. 따라서 대신 `connection()`을 사용하여 database를 선언해야 합니다.

```php
Schema::connection('database')->hasTable('schema.table');
```

<a name="get-column-types"></a>
<!-- #### Schema Builder `getColumnType()` Method -->
#### Schema Builder `getColumnType()` Method

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `Schema::getColumnType()` method now always returns actual type of the given column, not the Doctrine DBAL equivalent type. -->
`Schema::getColumnType()` 메서드는 이제 Doctrine DBAL의 대응 타입이 아니라, 지정된 컬럼의 실제 타입을 항상 반환합니다.

<a name="database-connection-interface"></a>
<!-- #### Database Connection Interface -->
#### Database Connection Interface

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `Illuminate\Database\ConnectionInterface` interface has received a new `scalar` method. If you are defining your own implementation of this interface, you should add the `scalar` method to your implementation: -->
`Illuminate\Database\ConnectionInterface` 인터페이스에 새로운 `scalar` 메서드가 추가되었습니다. 이 인터페이스를 직접 구현하고 있다면, 구현 클래스에 `scalar` 메서드를 추가해야 합니다.

```php
public function scalar($query, $bindings = [], $useReadPdo = true);
```

<a name="dates"></a>
<!-- ### Dates -->
### Dates

<a name="carbon-3"></a>
<!-- #### Carbon 3 -->
#### Carbon 3

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- Laravel 11 supports both Carbon 2 and Carbon 3. Carbon is a date manipulation library utilized extensively by Laravel and packages throughout the ecosystem. If you upgrade to Carbon 3, be aware that `diffIn*` methods now return floating-point numbers and may return negative values to indicate time direction, which is a significant change from Carbon 2. Review Carbon's [change log](https://github.com/briannesbitt/Carbon/releases/tag/3.0.0) and [documentation](https://carbon.nesbot.com/guide/getting-started/migration.html) for detailed information on how to handle these and other changes. -->
Laravel 11은 Carbon 2와 Carbon 3을 모두 지원합니다. Carbon은 Laravel과 생태계 전반의 패키지에서 폭넓게 사용되는 날짜 조작 라이브러리입니다. Carbon 3으로 업그레이드하는 경우, `diffIn*` 메서드가 이제 부동소수점 숫자를 반환하며 시간 방향을 나타내기 위해 음수 값을 반환할 수도 있다는 점을 알아두어야 합니다. 이는 Carbon 2와 비교해 중요한 변경 사항입니다. 이러한 변경 사항과 그 밖의 변경 사항을 처리하는 방법에 대한 자세한 내용은 Carbon의 [change log](https://github.com/briannesbitt/Carbon/releases/tag/3.0.0)와 [documentation](https://carbon.nesbot.com/guide/getting-started/migration.html)를 검토하십시오.

<a name="mail"></a>
<!-- ### Mail -->
### Mail

<a name="the-mailer-contract"></a>
<!-- #### The `Mailer` Contract -->
#### The `Mailer` Contract

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `Illuminate\Contracts\Mail\Mailer` contract has received a new `sendNow` method. If your application or package is manually implementing this contract, you should add the new `sendNow` method to your implementation: -->
`Illuminate\Contracts\Mail\Mailer` 컨트랙트에 새로운 `sendNow` 메서드가 추가되었습니다. 애플리케이션이나 패키지에서 이 컨트랙트를 직접 구현하고 있다면, 구현 클래스에 새로운 `sendNow` 메서드를 추가해야 합니다.

```php
public function sendNow($mailable, array $data = [], $callback = null);
```

<a name="packages"></a>
<!-- ### Packages -->
### Packages

<a name="publishing-service-providers"></a>
<!-- #### Publishing Service Providers to the Application -->
#### Publishing Service Providers to the Application

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- If you have written a Laravel package that manually publishes a service provider to the application's `app/Providers` directory and manually modifies the application's `config/app.php` configuration file to register the service provider, you should update your package to utilize the new `ServiceProvider::addProviderToBootstrapFile` method. -->
Laravel 패키지를 작성하면서 service provider를 애플리케이션의 `app/Providers` 디렉터리에 직접 게시하고, service provider를 등록하기 위해 애플리케이션의 `config/app.php` 설정 파일을 직접 수정했다면, 새 `ServiceProvider::addProviderToBootstrapFile` 메서드를 사용하도록 패키지를 업데이트해야 합니다.

<!-- The `addProviderToBootstrapFile` method will automatically add the service provider you have published to the application's `bootstrap/providers.php` file, since the `providers` array does not exist within the `config/app.php` configuration file in new Laravel 11 applications. -->
`addProviderToBootstrapFile` 메서드는 게시한 service provider를 애플리케이션의 `bootstrap/providers.php` 파일에 자동으로 추가합니다. 새로운 Laravel 11 애플리케이션에서는 `config/app.php` 설정 파일 안에 `providers` 배열이 존재하지 않기 때문입니다.

```php
use Illuminate\Support\ServiceProvider;

ServiceProvider::addProviderToBootstrapFile(Provider::class);
```

<a name="queues"></a>
<!-- ### Queues -->
### Queues

<a name="the-batch-repository-interface"></a>
<!-- #### The `BatchRepository` Interface -->
#### The `BatchRepository` Interface

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `Illuminate\Bus\BatchRepository` interface has received a new `rollBack` method. If you are implementing this interface within your own package or application, you should add this method to your implementation: -->
`Illuminate\Bus\BatchRepository` 인터페이스에 새로운 `rollBack` 메서드가 추가되었습니다. 자체 패키지나 애플리케이션에서 이 인터페이스를 구현하고 있다면, 구현 클래스에 이 메서드를 추가해야 합니다.

```php
public function rollBack();
```

<a name="synchronous-jobs-in-database-transactions"></a>
<!-- #### Synchronous Jobs in Database Transactions -->
#### Synchronous Jobs in Database Transactions

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- Previously, synchronous jobs (jobs using the `sync` queue driver) would execute immediately, regardless of whether the `after_commit` configuration option of the queue connection was set to `true` or the `afterCommit` method was invoked on the job. -->
이전에는 동기 작업(`sync` queue driver를 사용하는 작업)이 queue connection의 `after_commit` 설정 옵션이 `true`로 설정되어 있거나 작업에서 `afterCommit` 메서드가 호출되었는지와 관계없이 즉시 실행되었습니다.

<!-- In Laravel 11, synchronous queue jobs will now respect the "after commit" configuration of the queue connection or job. -->
Laravel 11에서는 동기 queue 작업이 이제 queue connection 또는 작업의 "after commit" 설정을 따릅니다.

<a name="rate-limiting"></a>
<!-- ### Rate Limiting -->
### Rate Limiting

<a name="per-second-rate-limiting"></a>
<!-- #### Per-Second Rate Limiting -->
#### Per-Second Rate Limiting

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- Laravel 11 supports per-second rate limiting instead of being limited to per-minute granularity. There are a variety of potential breaking changes you should be aware of related to this change. -->
Laravel 11은 분 단위의 세밀도에 제한되지 않고 초 단위 rate limiting을 지원합니다. 이 변경과 관련해 알아두어야 할 잠재적인 breaking change가 여러 가지 있습니다.

<!-- The `GlobalLimit` class constructor now accepts seconds instead of minutes. This class is not documented and would not typically be used by your application: -->
`GlobalLimit` 클래스 생성자는 이제 분이 아니라 초를 받습니다. 이 클래스는 문서화되어 있지 않으며 일반적으로 애플리케이션에서 사용하지 않습니다.

```php
new GlobalLimit($attempts, 2 * 60);
```

<!-- The `Limit` class constructor now accepts seconds instead of minutes. All documented usages of this class are limited to static constructors such as `Limit::perMinute` and `Limit::perSecond`. However, if you are instantiating this class manually, you should update your application to provide seconds to the class's constructor: -->
`Limit` 클래스 생성자는 이제 분이 아니라 초를 받습니다. 이 클래스의 문서화된 모든 사용법은 `Limit::perMinute`, `Limit::perSecond` 같은 정적 생성자로 제한됩니다. 그러나 이 클래스를 직접 인스턴스화하고 있다면, 클래스 생성자에 초를 제공하도록 애플리케이션을 업데이트해야 합니다.

```php
new Limit($key, $attempts, 2 * 60);
```

<!-- The `Limit` class's `decayMinutes` property has been renamed to `decaySeconds` and now contains seconds instead of minutes. -->
`Limit` 클래스의 `decayMinutes` 속성은 `decaySeconds`로 이름이 변경되었으며, 이제 분이 아니라 초를 담습니다.

<!-- The `Illuminate\Queue\Middleware\ThrottlesExceptions` and `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` class constructors now accept seconds instead of minutes: -->
`Illuminate\Queue\Middleware\ThrottlesExceptions`와 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 클래스 생성자는 이제 분이 아니라 초를 받습니다.

```php
new ThrottlesExceptions($attempts, 2 * 60);
new ThrottlesExceptionsWithRedis($attempts, 2 * 60);
```

<a name="cashier-stripe"></a>
<!-- ### Cashier Stripe -->
### Cashier Stripe

<a name="updating-cashier-stripe"></a>
<!-- #### Updating Cashier Stripe -->
#### Updating Cashier Stripe

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- Laravel 11 no longer supports Cashier Stripe 14.x. Therefore, you should update your application's Laravel Cashier Stripe dependency to `^15.0` in your `composer.json` file. -->
Laravel 11은 더 이상 Cashier Stripe 14.x를 지원하지 않습니다. 따라서 애플리케이션의 Laravel Cashier Stripe 의존성을 `composer.json` 파일에서 `^15.0`으로 업데이트해야 합니다.

<!-- Cashier Stripe 15.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Cashier Stripe's migrations to your application: -->
Cashier Stripe 15.0은 더 이상 자체 migrations 디렉터리에서 migration을 자동으로 로드하지 않습니다. 대신 다음 명령어를 실행하여 Cashier Stripe의 migrations를 애플리케이션에 게시해야 합니다.

```shell
php artisan vendor:publish --tag=cashier-migrations
```

<!-- Please review the complete [Cashier Stripe upgrade guide](https://github.com/laravel/cashier-stripe/blob/15.x/UPGRADE.md) for additional breaking changes. -->
추가 breaking change는 전체 [Cashier Stripe upgrade guide](https://github.com/laravel/cashier-stripe/blob/15.x/UPGRADE.md)를 검토하십시오.

<a name="spark-stripe"></a>
<!-- ### Spark (Stripe) -->
### Spark (Stripe)

<a name="updating-spark-stripe"></a>
<!-- #### Updating Spark Stripe -->
#### Updating Spark Stripe

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- Laravel 11 no longer supports Laravel Spark Stripe 4.x. Therefore, you should update your application's Laravel Spark Stripe dependency to `^5.0` in your `composer.json` file. -->
Laravel 11은 더 이상 Laravel Spark Stripe 4.x를 지원하지 않습니다. 따라서 애플리케이션의 Laravel Spark Stripe 의존성을 `composer.json` 파일에서 `^5.0`으로 업데이트해야 합니다.

<!-- Spark Stripe 5.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Spark Stripe's migrations to your application: -->
Spark Stripe 5.0은 더 이상 자체 migrations 디렉터리에서 migration을 자동으로 로드하지 않습니다. 대신 다음 명령어를 실행하여 Spark Stripe의 migrations를 애플리케이션에 게시해야 합니다.

```shell
php artisan vendor:publish --tag=spark-migrations
```

<!-- Please review the complete [Spark Stripe upgrade guide](https://spark.laravel.com/docs/spark-stripe/upgrade.html) for additional breaking changes. -->
추가 breaking change는 전체 [Spark Stripe upgrade guide](https://spark.laravel.com/docs/spark-stripe/upgrade.html)를 검토하십시오.

<a name="passport"></a>
<!-- ### Passport -->
### Passport

<a name="updating-telescope"></a>
<!-- #### Updating Passport -->
#### Updating Passport

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- Laravel 11 no longer supports Laravel Passport 11.x. Therefore, you should update your application's Laravel Passport dependency to `^12.0` in your `composer.json` file. -->
Laravel 11은 더 이상 Laravel Passport 11.x를 지원하지 않습니다. 따라서 애플리케이션의 Laravel Passport 의존성을 `composer.json` 파일에서 `^12.0`으로 업데이트해야 합니다.

<!-- Passport 12.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Passport's migrations to your application: -->
Passport 12.0은 더 이상 자체 migrations 디렉터리에서 migration을 자동으로 로드하지 않습니다. 대신 다음 명령어를 실행하여 Passport의 migrations를 애플리케이션에 게시해야 합니다.

```shell
php artisan vendor:publish --tag=passport-migrations
```

<!-- In addition, the password grant type is disabled by default. You may enable it by invoking the `enablePasswordGrant` method in the `boot` method of your application's `AppServiceProvider`: -->
또한 password grant type은 기본적으로 비활성화되어 있습니다. 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하여 이를 활성화할 수 있습니다.

```
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```

<a name="sanctum"></a>
<!-- ### Sanctum -->
### Sanctum

<a name="updating-sanctum"></a>
<!-- #### Updating Sanctum -->
#### Updating Sanctum

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- Laravel 11 no longer supports Laravel Sanctum 3.x. Therefore, you should update your application's Laravel Sanctum dependency to `^4.0` in your `composer.json` file. -->
Laravel 11은 더 이상 Laravel Sanctum 3.x를 지원하지 않습니다. 따라서 애플리케이션의 Laravel Sanctum 의존성을 `composer.json` 파일에서 `^4.0`으로 업데이트해야 합니다.

<!-- Sanctum 4.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Sanctum's migrations to your application: -->
Sanctum 4.0은 더 이상 자체 migrations 디렉터리에서 migration을 자동으로 로드하지 않습니다. 대신 다음 명령어를 실행하여 Sanctum의 migrations를 애플리케이션에 게시해야 합니다.

```shell
php artisan vendor:publish --tag=sanctum-migrations
```

<!-- Then, in your application's `config/sanctum.php` configuration file, you should update the references to the `authenticate_session`, `encrypt_cookies`, and `validate_csrf_token` middleware to the following: -->
그런 다음 애플리케이션의 `config/sanctum.php` 설정 파일에서 `authenticate_session`, `encrypt_cookies`, `validate_csrf_token` middleware에 대한 참조를 다음과 같이 업데이트해야 합니다.

```
'middleware' => [
    'authenticate_session' => Laravel\Sanctum\Http\Middleware\AuthenticateSession::class,
    'encrypt_cookies' => Illuminate\Cookie\Middleware\EncryptCookies::class,
    'validate_csrf_token' => Illuminate\Foundation\Http\Middleware\ValidateCsrfToken::class,
],
```

<a name="telescope"></a>
<!-- ### Telescope -->
### Telescope

<a name="updating-telescope"></a>
<!-- #### Updating Telescope -->
#### Updating Telescope

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- Laravel 11 no longer supports Laravel Telescope 4.x. Therefore, you should update your application's Laravel Telescope dependency to `^5.0` in your `composer.json` file. -->
Laravel 11은 더 이상 Laravel Telescope 4.x를 지원하지 않습니다. 따라서 애플리케이션의 Laravel Telescope 의존성을 `composer.json` 파일에서 `^5.0`으로 업데이트해야 합니다.

<!-- Telescope 5.0 no longer automatically loads migrations from its own migrations directory. Instead, you should run the following command to publish Telescope's migrations to your application: -->
Telescope 5.0은 더 이상 자체 migrations 디렉터리에서 migration을 자동으로 로드하지 않습니다. 대신 다음 명령어를 실행하여 Telescope의 migrations를 애플리케이션에 게시해야 합니다.

```shell
php artisan vendor:publish --tag=telescope-migrations
```

<a name="spatie-once-package"></a>
<!-- ### Spatie Once Package -->
### Spatie Once Package

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- Laravel 11 now provides its own [`once` function](/docs/11.x/helpers#method-once) to ensure that a given closure is only executed once. Therefore, if your application has a dependency on the `spatie/once` package, you should remove it from your application's `composer.json` file to avoid conflicts. -->
Laravel 11은 이제 주어진 클로저가 한 번만 실행되도록 보장하는 자체 [`once` function](/docs/11.x/helpers#method-once)를 제공합니다. 따라서 애플리케이션이 `spatie/once` 패키지에 의존하고 있다면, 충돌을 피하기 위해 애플리케이션의 `composer.json` 파일에서 해당 패키지를 제거해야 합니다.

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/10.x...11.x) and choose which updates are important to you. -->
또한 `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel)의 변경 사항을 살펴보는 것을 권장합니다. 이러한 변경 사항 중 다수는 필수는 아니지만, 해당 파일들을 애플리케이션과 동기화해 두고 싶을 수 있습니다. 이 업그레이드 가이드에서는 일부 변경 사항을 다루지만, 설정 파일이나 주석 변경처럼 다루지 않는 변경 사항도 있습니다. [GitHub comparison tool](https://github.com/laravel/laravel/compare/10.x...11.x)를 사용하면 변경 사항을 쉽게 확인하고, 어떤 업데이트가 중요한지 선택할 수 있습니다.
