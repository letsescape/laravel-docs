<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 12.0 From 11.x](#upgrade-12.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating the Laravel Installer](#updating-the-laravel-installer)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Models and UUIDv7](#models-and-uuidv7)

<!-- </div> -->
</div>

<a name="low-impact-changes"></a>
<!-- ## Low Impact Changes -->
## Low Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Carbon 3](#carbon-3)
- [Concurrency Result Index Mapping](#concurrency-result-index-mapping)
- [Container Class Dependency Resolution](#container-class-dependency-resolution)
- [Image Validation Now Excludes SVGs](#image-validation)
- [Local Filesystem Disk Default Root Path](#local-filesystem-disk-default-root-path)
- [Multi-Schema Database Inspecting](#multi-schema-database-inspecting)
- [Nested Array Request Merging](#nested-array-request-merging)

<!-- </div> -->
</div>

<a name="upgrade-12.0"></a>
<!-- ## Upgrading To 12.0 From 11.x -->
## Upgrading To 12.0 From 11.x

<!-- #### Estimated Upgrade Time: 5 Minutes -->
#### Estimated Upgrade Time: 5 Minutes

> [!NOTE]
> 가능한 모든 호환성 깨짐 변경 사항을 문서화하려고 노력합니다. 이 변경 사항 중 일부는 프레임워크의 잘 쓰이지 않는 부분에 있으므로, 실제로는 이 중 일부만 애플리케이션에 영향을 줄 수 있습니다. 시간을 아끼고 싶으신가요? [Laravel Shift](https://laravelshift.com/)를 사용하면 애플리케이션 업그레이드를 자동화하는 데 도움을 받을 수 있습니다.

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- You should update the following dependencies in your application's `composer.json` file: -->
애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `laravel/framework` to `^12.0`
- `phpunit/phpunit` to `^11.0`
- `pestphp/pest` to `^3.0`
-->
- `laravel/framework`를 `^12.0`으로
- `phpunit/phpunit`를 `^11.0`으로
- `pestphp/pest`를 `^3.0`으로

<!-- </div> -->
</div>

<a name="carbon-3"></a>
<!-- #### Carbon 3 -->
#### Carbon 3

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Support for Carbon 2.x has been removed. All Laravel 12 applications now require [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html). -->
Carbon 2.x 지원이 제거되었습니다. 모든 Laravel 12 애플리케이션은 이제 [Carbon 3.x](https://carbon.nesbot.com/guide/getting-started/migration.html)가 필요합니다.

<a name="updating-the-laravel-installer"></a>
<!-- ### Updating the Laravel Installer -->
### Updating the Laravel Installer

<!-- If you are using the Laravel installer CLI tool to create new Laravel applications, you should update your installer installation to be compatible with Laravel 12.x and the [new Laravel starter kits](https://laravel.com/starter-kits). If you installed the Laravel installer via `composer global require`, you may update the installer using `composer global update`: -->
Laravel installer CLI 도구를 사용하여 새 Laravel 애플리케이션을 만들고 있다면, Laravel 12.x 및 [new Laravel starter kits](https://laravel.com/starter-kits)와 호환되도록 installer 설치를 업데이트해야 합니다. `composer global require`로 Laravel installer를 설치했다면, `composer global update`를 사용하여 installer를 업데이트할 수 있습니다.

```shell
composer global update laravel/installer
```

<!-- If you originally installed PHP and Laravel via `php.new`, you may simply re-run the `php.new` installation commands for your operating system to install the latest version of PHP and the Laravel installer: -->
원래 `php.new`를 통해 PHP와 Laravel을 설치했다면, 운영체제에 맞는 `php.new` 설치 명령어를 다시 실행하여 최신 버전의 PHP와 Laravel installer를 설치할 수 있습니다.

```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.4)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.4'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.4)"
```

<!-- Or, if you are using [Laravel Herd's](https://herd.laravel.com) bundled copy of the Laravel installer, you should update your Herd installation to the latest release. -->
또는 [Laravel Herd's](https://herd.laravel.com)에 포함된 Laravel installer 사본을 사용하고 있다면, Herd 설치를 최신 릴리스로 업데이트해야 합니다.

<a name="authentication"></a>
<!-- ### Authentication -->
### Authentication

<a name="updated-databasetokenrepository-constructor-signature"></a>
<!-- #### Updated `DatabaseTokenRepository` Constructor Signature -->
#### Updated `DatabaseTokenRepository` Constructor Signature

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The constructor of the `Illuminate\Auth\Passwords\DatabaseTokenRepository` class now expects the `$expires` parameter to be given in seconds, rather than minutes. -->
`Illuminate\Auth\Passwords\DatabaseTokenRepository` 클래스의 생성자는 이제 `$expires` 파라미터를 분 단위가 아니라 초 단위로 받습니다.

<a name="concurrency"></a>
<!-- ### Concurrency -->
### Concurrency

<a name="concurrency-result-index-mapping"></a>
<!-- #### Concurrency Result Index Mapping -->
#### Concurrency Result Index Mapping

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- When invoking the `Concurrency::run` method with an associative array, the results of the concurrent operations are now returned with their associated keys: -->
연관 배열로 `Concurrency::run` 메서드를 호출하면, 동시 작업의 결과가 이제 해당 키와 함께 반환됩니다.

```php
$result = Concurrency::run([
    'task-1' => fn () => 1 + 1,
    'task-2' => fn () => 2 + 2,
]);

// ['task-1' => 2, 'task-2' => 4]
```

<a name="container"></a>
<!-- ### Container -->
### Container

<a name="container-class-dependency-resolution"></a>
<!-- #### Container Class Dependency Resolution -->
#### Container Class Dependency Resolution

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The dependency injection container now respects the default value of class properties when resolving a class instance. If you were previously relying on the container to resolve a class instance without the default value, you may need to adjust your application to account for this new behavior: -->
의존성 주입 컨테이너는 이제 클래스 인스턴스를 해결할 때 클래스 속성의 기본값을 존중합니다. 이전에 컨테이너가 기본값 없이 클래스 인스턴스를 해결하는 동작에 의존하고 있었다면, 이 새로운 동작을 고려하도록 애플리케이션을 조정해야 할 수 있습니다.

```php
class Example
{
    public function __construct(public ?Carbon $date = null) {}
}

$example = resolve(Example::class);

// <= 11.x
$example->date instanceof Carbon;

// >= 12.x
$example->date === null;
```

<a name="database"></a>
<!-- ### Database -->
### Database

<a name="multi-schema-database-inspecting"></a>
<!-- #### Multi-Schema Database Inspecting -->
#### Multi-Schema Database Inspecting

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Schema::getTables()`, `Schema::getViews()`, and `Schema::getTypes()` methods now include the results from all schemas by default. You may pass the `schema` argument to retrieve the result for the given schema only: -->
`Schema::getTables()`, `Schema::getViews()`, `Schema::getTypes()` 메서드는 이제 기본적으로 모든 스키마의 결과를 포함합니다. 특정 스키마의 결과만 가져오려면 `schema` 인수를 전달할 수 있습니다.

```php
// All tables on all schemas...
$tables = Schema::getTables();

// All tables on the 'main' schema...
$tables = Schema::getTables(schema: 'main');

// All tables on the 'main' and 'blog' schemas...
$tables = Schema::getTables(schema: ['main', 'blog']);
```

<!-- The `Schema::getTableListing()` method now returns schema-qualified table names by default. You may pass the `schemaQualified` argument to change the behavior as desired: -->
`Schema::getTableListing()` 메서드는 이제 기본적으로 스키마가 포함된 테이블 이름을 반환합니다. 원하는 동작으로 변경하려면 `schemaQualified` 인수를 전달할 수 있습니다.

```php
$tables = Schema::getTableListing();
// ['main.migrations', 'main.users', 'blog.posts']

$tables = Schema::getTableListing(schema: 'main');
// ['main.migrations', 'main.users']

$tables = Schema::getTableListing(schema: 'main', schemaQualified: false);
// ['migrations', 'users']
```

<!-- The `db:table` and `db:show` commands now output the results of all schemas on MySQL, MariaDB, and SQLite, just like PostgreSQL and SQL Server. -->
`db:table` 및 `db:show` 명령어는 이제 PostgreSQL 및 SQL Server와 마찬가지로 MySQL, MariaDB, SQLite에서도 모든 스키마의 결과를 출력합니다.

<a name="database-constructor-signature-changes"></a>
<!-- #### Database Constructor Signature Changes -->
#### Database Constructor Signature Changes

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- In Laravel 12, several low-level database classes now require an `Illuminate\Database\Connection` instance to be provided via their constructors. -->
Laravel 12에서는 여러 저수준 데이터베이스 클래스가 생성자를 통해 `Illuminate\Database\Connection` 인스턴스를 제공받아야 합니다.

<!-- **These changes are primarily applicable to database package maintainers - it is extremely unlikely any of these changes affect normal application development.** -->
**이 변경 사항은 주로 데이터베이스 패키지 유지보수자에게 적용됩니다. 일반적인 애플리케이션 개발에 영향을 줄 가능성은 극히 낮습니다.**

<!-- `Illuminate\Database\Schema\Blueprint` -->
`Illuminate\Database\Schema\Blueprint`

<!-- The constructor of the `Illuminate\Database\Schema\Blueprint` class now expects a `Connection` instance as its first argument. This primarily affects applications or packages that manually instantiate `Blueprint` instances. -->
`Illuminate\Database\Schema\Blueprint` 클래스의 생성자는 이제 첫 번째 인수로 `Connection` 인스턴스를 기대합니다. 이는 주로 `Blueprint` 인스턴스를 직접 생성하는 애플리케이션이나 패키지에 영향을 줍니다.

<!-- `Illuminate\Database\Grammar` -->
`Illuminate\Database\Grammar`

<!-- The constructor of the `Illuminate\Database\Grammar` class also now requires a `Connection` instance. In previous versions, the connection was assigned after construction using the `setConnection()` method. This method has been removed in Laravel 12: -->
`Illuminate\Database\Grammar` 클래스의 생성자도 이제 `Connection` 인스턴스가 필요합니다. 이전 버전에서는 생성 후 `setConnection()` 메서드를 사용하여 연결을 할당했습니다. 이 메서드는 Laravel 12에서 제거되었습니다.

```php
// Laravel <= 11.x
$grammar = new MySqlGrammar;
$grammar->setConnection($connection);

// Laravel >= 12.x
$grammar = new MySqlGrammar($connection);
````

<!-- In addition, the following APIs have been removed or deprecated: -->
또한 다음 API는 제거되었거나 사용 중단 예정입니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- The `Blueprint::getPrefix()` method is deprecated.
- The `Connection::withTablePrefix()` method has been removed.
- The `Grammar::getTablePrefix()` and `setTablePrefix()` methods are deprecated.
- The `Grammar::setConnection()` method has been removed.
-->
- `Blueprint::getPrefix()` 메서드는 사용 중단 예정입니다.
- `Connection::withTablePrefix()` 메서드는 제거되었습니다.
- `Grammar::getTablePrefix()` 및 `setTablePrefix()` 메서드는 사용 중단 예정입니다.
- `Grammar::setConnection()` 메서드는 제거되었습니다.

<!-- </div> -->
</div>

<!-- When working with table prefixes, you should now retrieve them directly from the database connection: -->
테이블 접두사를 다룰 때는 이제 데이터베이스 연결에서 직접 가져와야 합니다.

```php
$prefix = $connection->getTablePrefix();
```

<!-- If you maintain custom database drivers, schema builders, or grammar implementations, you should review their constructors and ensure a `Connection` instance is provided. -->
커스텀 데이터베이스 드라이버, 스키마 빌더, 또는 grammar 구현을 유지보수하고 있다면, 생성자를 검토하고 `Connection` 인스턴스가 제공되는지 확인해야 합니다.

<a name="eloquent"></a>
<!-- ### Eloquent -->
### Eloquent

<a name="models-and-uuidv7"></a>
<!-- #### Models and UUIDv7 -->
#### Models and UUIDv7

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- The `HasUuids` trait now returns UUIDs that are compatible with version 7 of the UUID spec (ordered UUIDs). If you would like to continue using ordered UUIDv4 strings for your model's IDs, you should now use the `HasVersion4Uuids` trait: -->
`HasUuids` trait는 이제 UUID 사양의 버전 7과 호환되는 UUID(정렬된 UUID)를 반환합니다. 모델 ID에 대해 정렬된 UUIDv4 문자열을 계속 사용하려면 이제 `HasVersion4Uuids` trait를 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids; // [tl! remove]
use Illuminate\Database\Eloquent\Concerns\HasVersion4Uuids as HasUuids; // [tl! add]
```

<!-- The `HasVersion7Uuids` trait has been removed. If you were previously using this trait, you should use the `HasUuids` trait instead, which now provides the same behavior. -->
`HasVersion7Uuids` trait는 제거되었습니다. 이전에 이 trait를 사용하고 있었다면, 이제 동일한 동작을 제공하는 `HasUuids` trait를 대신 사용해야 합니다.

<a name="requests"></a>
<!-- ### Requests -->
### Requests

<a name="nested-array-request-merging"></a>
<!-- #### Nested Array Request Merging -->
#### Nested Array Request Merging

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `$request->mergeIfMissing()` method now allows merging nested array data using "dot" notation. If you were previously relying on this method to create a top-level array key containing the "dot" notation version of the key, you may need to adjust your application to account for this new behavior: -->
`$request->mergeIfMissing()` 메서드는 이제 "dot" 표기법을 사용하여 중첩 배열 데이터를 병합할 수 있습니다. 이전에 이 메서드가 "dot" 표기법 버전의 키를 포함하는 최상위 배열 키를 생성하는 동작에 의존하고 있었다면, 이 새로운 동작을 고려하도록 애플리케이션을 조정해야 할 수 있습니다.

```php
$request->mergeIfMissing([
    'user.last_name' => 'Otwell',
]);
```

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<a name="route-precedence"></a>
<!-- #### Route Precedence -->
#### Route Precedence

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The routing behavior when multiple routes have the same name has been unified between cached and uncached routing. This means that uncached routing now matches the first route registered with a given name instead of the last one. -->
동일한 이름을 가진 여러 라우트가 있을 때의 라우팅 동작이 캐시된 라우팅과 캐시되지 않은 라우팅 사이에서 통일되었습니다. 즉, 캐시되지 않은 라우팅은 이제 특정 이름으로 등록된 마지막 라우트가 아니라 첫 번째 라우트와 매칭됩니다.

<a name="storage"></a>
<!-- ### Storage -->
### Storage

<a name="local-filesystem-disk-default-root-path"></a>
<!-- #### Local Filesystem Disk Default Root Path -->
#### Local Filesystem Disk Default Root Path

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- If your application does not explicitly define a `local` disk in your filesystems configuration, Laravel will now default the local disk's root to `storage/app/private`. In previous releases, this defaulted to `storage/app`. As a result, calls to `Storage::disk('local')` will read from and write to `storage/app/private` unless otherwise configured. To restore the previous behavior, you may define the `local` disk manually and set the desired root path. -->
애플리케이션의 filesystems 설정에서 `local` 디스크를 명시적으로 정의하지 않은 경우, Laravel은 이제 로컬 디스크의 루트를 기본적으로 `storage/app/private`로 설정합니다. 이전 릴리스에서는 기본값이 `storage/app`이었습니다. 따라서 별도로 설정하지 않으면 `Storage::disk('local')` 호출은 `storage/app/private`에서 읽고 이 위치에 씁니다. 이전 동작으로 되돌리려면 `local` 디스크를 직접 정의하고 원하는 루트 경로를 설정하면 됩니다.

<a name="validation"></a>
<!-- ### Validation -->
### Validation

<a name="image-validation"></a>
<!-- #### Image Validation Now Excludes SVGs -->
#### Image Validation Now Excludes SVGs

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `image` validation rule no longer allows SVG images by default. If you would like to allow SVGs when using the `image` rule, you must explicitly allow them: -->
`image` 유효성 검증 규칙은 더 이상 기본적으로 SVG 이미지를 허용하지 않습니다. `image` 규칙을 사용할 때 SVG를 허용하려면 명시적으로 허용해야 합니다.

```php
use Illuminate\Validation\Rules\File;

'photo' => 'required|image:allow_svg'

// Or...
'photo' => ['required', File::image(allowSvg: true)],
```

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/11.x...12.x) and choose which updates are important to you. -->
또한 `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel)의 변경 사항도 확인해 보시기를 권장합니다. 이러한 변경 사항 중 많은 부분은 필수는 아니지만, 애플리케이션의 파일을 최신 상태로 맞춰 두고 싶을 수 있습니다. 이 업그레이드 가이드에서 일부 변경 사항을 다루지만, 설정 파일이나 주석 변경과 같은 다른 변경 사항은 다루지 않습니다. [GitHub comparison tool](https://github.com/laravel/laravel/compare/11.x...12.x)를 사용하면 변경 사항을 쉽게 확인하고, 어떤 업데이트가 자신에게 중요한지 선택할 수 있습니다.
