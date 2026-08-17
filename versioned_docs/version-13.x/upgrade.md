<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 13.0 From 12.x](#upgrade-13.0)
    - [Upgrading Using AI](#upgrading-using-ai)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating the Laravel Installer](#updating-the-laravel-installer)
- [Request Forgery Protection](#request-forgery-protection)

</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Cache `serializable_classes` Configuration](#cache-serializable_classes-configuration)
- [Database `upsert` With MySQL or MariaDB](#database-upsert-mariadb-mysql)

</div>

<a name="low-impact-changes"></a>
<!-- ## Low Impact Changes -->
## Low Impact Changes

<div class="content-list" markdown="1">

- [Cache Prefixes and Session Cookie Names](#cache-prefixes-and-session-cookie-names)
- [Collection Model Serialization Restores Eager-Loaded Relations](#collection-model-serialization-restores-eager-loaded-relations)
- [`Container::call` and Nullable Class Defaults](#containercall-and-nullable-class-defaults)
- [Domain Route Registration Precedence](#domain-route-registration-precedence)
- [`JobAttempted` Event Exception Payload](#jobattempted-event-exception-payload)
- [Manager `extend` Callback Binding](#manager-extend-callback-binding)
- [MySQL `DELETE` Queries With `JOIN`, `ORDER BY`, and `LIMIT`](#mysql-delete-queries-with-join-order-by-and-limit)
- [Pagination Bootstrap View Names](#pagination-bootstrap-view-names)
- [Polymorphic Pivot Table Name Generation](#polymorphic-pivot-table-name-generation)
- [`QueueBusy` Event Property Rename](#queuebusy-event-property-rename)
- [Session `serialization` Configuration](#session-serialization-configuration)
- [`Str` Factories Reset Between Tests](#str-factories-reset-between-tests)

</div>

<a name="upgrade-13.0"></a>
<!-- ## Upgrading To 13.0 From 12.x -->
## Upgrading To 13.0 From 12.x

<!-- #### Estimated Upgrade Time: 10 Minutes -->
#### Estimated Upgrade Time: 10 Minutes

> [!NOTE]
> 가능한 모든 하위 호환성 중단 변경 사항을 문서화하려고 노력하고 있습니다. 다만 일부 변경 사항은 프레임워크의 잘 드러나지 않는 부분에 있으므로, 이 중 일부만 실제 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하려면 [Shift](https://laravelshift.com)를 사용할 수 있습니다. Shift는 커뮤니티에서 관리하는 Laravel 업그레이드 자동화 서비스입니다.

<a name="upgrading-using-ai"></a>
<!-- ### Upgrading Using AI -->
### Upgrading Using AI

<!-- You can automate your upgrade using [Laravel Boost](https://github.com/laravel/boost). Boost is a first-party MCP server that provides your AI assistant with guided upgrade prompts — once installed in any Laravel 12 application, use the `/upgrade-laravel-v13` slash command in Claude Code, Cursor, OpenCode, Gemini, or VS Code to begin the upgrade to Laravel 13. This command requires Laravel Boost `^2.0`. -->
[Laravel Boost](https://github.com/laravel/boost)를 사용하여 업그레이드를 자동화할 수 있습니다. Boost는 AI 어시스턴트에 가이드형 업그레이드 프롬프트를 제공하는 공식 MCP 서버입니다. Laravel 12 애플리케이션에 설치한 뒤 Claude Code, Cursor, OpenCode, Gemini 또는 VS Code에서 `/upgrade-laravel-v13` 슬래시 명령어를 사용하면 Laravel 13으로 업그레이드를 시작할 수 있습니다. 이 명령어에는 Laravel Boost `^2.0`이 필요합니다.

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- You should update the following dependencies in your application's `composer.json` file: -->
애플리케이션의 `composer.json` 파일에서 다음 의존성을 업데이트해야 합니다.

<div class="content-list" markdown="1">

<!-- - `laravel/framework` to `^13.0` - `laravel/boost` to `^2.0` - `laravel/tinker` to `^3.0` - `phpunit/phpunit` to `^12.0` - `pestphp/pest` to `^4.0` -->
- `laravel/framework`를 `^13.0`으로
- `laravel/boost`를 `^2.0`으로
- `laravel/tinker`를 `^3.0`으로
- `phpunit/phpunit`를 `^12.0`으로
- `pestphp/pest`를 `^4.0`으로

</div>

<a name="updating-the-laravel-installer"></a>
<!-- ### Updating the Laravel Installer -->
### Updating the Laravel Installer

<!-- If you are using the Laravel installer CLI tool to create new Laravel applications, you should update your installer installation for Laravel 13.x compatibility. -->
Laravel 설치 프로그램 CLI 도구를 사용해 새 Laravel 애플리케이션을 만들고 있다면, Laravel 13.x 호환성을 위해 설치 프로그램을 업데이트해야 합니다.

<!-- If you installed the Laravel installer via `composer global require`, you may update the installer using `composer global update`: -->
`composer global require`로 Laravel 설치 프로그램을 설치했다면 `composer global update`를 사용해 설치 프로그램을 업데이트할 수 있습니다.

```shell
composer global update laravel/installer
```

<!-- Or, if you are using [Laravel Herd's](https://herd.laravel.com) bundled copy of the Laravel installer, you should update your Herd installation to the latest release. -->
또는 [Laravel Herd's](https://herd.laravel.com)에 포함된 Laravel 설치 프로그램 사본을 사용하고 있다면 Herd 설치본을 최신 릴리스로 업데이트해야 합니다.

<a name="cache"></a>
<!-- ### Cache -->
### Cache

<a name="cache-prefixes-and-session-cookie-names"></a>
<!-- #### Cache Prefixes and Session Cookie Names -->
#### Cache Prefixes and Session Cookie Names

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Laravel's default cache and Redis key prefixes now use hyphenated suffixes. -->
Laravel의 기본 캐시 및 Redis 키 접두사는 이제 하이픈으로 연결된 접미사를 사용합니다.

<!-- In most applications, this change will not apply because application-level configuration files already define these values. This primarily affects applications that rely on framework-level fallback configuration when corresponding application config values are not present. -->
대부분의 애플리케이션에서는 애플리케이션 수준 설정 파일이 이미 이러한 값을 정의하고 있으므로 이 변경 사항이 적용되지 않습니다. 이 변경은 주로 해당 애플리케이션 설정 값이 없을 때 프레임워크 수준의 fallback 설정에 의존하는 애플리케이션에 영향을 줍니다.

<!-- If your application relies on these generated defaults, cache keys and session cookie names may change after upgrading: -->
애플리케이션이 생성된 기본값에 의존한다면 업그레이드 후 캐시 키와 세션 쿠키 이름이 변경될 수 있습니다.

```php
// Laravel <= 12.x
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_cache_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_database_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_session';

// Laravel >= 13.x
Str::slug((string) env('APP_NAME', 'laravel')).'-cache-';
Str::slug((string) env('APP_NAME', 'laravel')).'-database-';
Str::slug((string) env('APP_NAME', 'laravel')).'-session';
```

<!-- To retain previous behavior, explicitly configure `CACHE_PREFIX`, `REDIS_PREFIX`, and `SESSION_COOKIE` in your environment. -->
이전 동작을 유지하려면 환경에서 `CACHE_PREFIX`, `REDIS_PREFIX`, `SESSION_COOKIE`를 명시적으로 설정하십시오.

<a name="store-and-repository-contracts-touch"></a>
<!-- #### `Store` and `Repository` Contracts: `touch` -->
#### `Store` and `Repository` Contracts: `touch`

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The cache contracts now include a `touch` method for extending item TTLs. If you maintain custom cache store implementations, you should add this method: -->
캐시 계약에는 이제 항목 TTL을 연장하는 `touch` 메서드가 포함됩니다. 사용자 정의 캐시 스토어 구현을 유지 관리하고 있다면 이 메서드를 추가해야 합니다.

```php
// Illuminate\Contracts\Cache\Store
public function touch($key, $seconds);
```

<a name="cache-serializable_classes-configuration"></a>
<!-- #### Cache `serializable_classes` Configuration -->
#### Cache `serializable_classes` Configuration

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- The default application `cache` configuration now includes a `serializable_classes` option set to `false`. This hardens cache unserialization behavior to help prevent PHP deserialization gadget chain attacks if your application's `APP_KEY` is leaked. If your application intentionally stores PHP objects in cache, you should explicitly list the classes that may be unserialized: -->
기본 애플리케이션 `cache` 설정에는 이제 `false`로 설정된 `serializable_classes` 옵션이 포함됩니다. 이 변경은 애플리케이션의 `APP_KEY`가 유출되었을 때 PHP 역직렬화 gadget chain 공격을 방지하는 데 도움이 되도록 캐시 역직렬화 동작을 강화합니다. 애플리케이션이 의도적으로 PHP 객체를 캐시에 저장한다면 역직렬화할 수 있는 클래스를 명시적으로 나열해야 합니다.

```php
'serializable_classes' => [
    App\Data\CachedDashboardStats::class,
    App\Support\CachedPricingSnapshot::class,
],
```

<!-- If your application previously relied on unserializing arbitrary cached objects, you will need to migrate that usage to explicit class allow-lists or to non-object cache payloads (such as arrays). -->
애플리케이션이 이전에 임의의 캐시된 객체 역직렬화에 의존했다면, 해당 사용 방식을 명시적인 클래스 allow-list 또는 객체가 아닌 캐시 페이로드(예: 배열)로 마이그레이션해야 합니다.

<a name="container"></a>
<!-- ### Container -->
### Container

<a name="containercall-and-nullable-class-defaults"></a>
<!-- #### `Container::call` and Nullable Class Defaults -->
#### `Container::call` and Nullable Class Defaults

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- `Container::call` now respects nullable class parameter defaults when no binding exists, matching constructor injection behavior introduced in Laravel 12: -->
`Container::call`은 이제 바인딩이 없을 때 nullable 클래스 매개변수 기본값을 존중합니다. 이는 Laravel 12에서 도입된 생성자 주입 동작과 일치합니다.

```php
$container->call(function (?Carbon $date = null) {
    return $date;
});

// Laravel <= 12.x: Carbon instance
// Laravel >= 13.x: null
```

<!-- If your method-call injection logic depended on the previous behavior, you may need to update it. -->
메서드 호출 주입 로직이 이전 동작에 의존했다면 해당 로직을 업데이트해야 할 수 있습니다.

<a name="contracts"></a>
<!-- ### Contracts -->
### Contracts

<a name="dispatcher-contract-dispatchafterresponse"></a>
<!-- #### `Dispatcher` Contract: `dispatchAfterResponse` -->
#### `Dispatcher` Contract: `dispatchAfterResponse`

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `Illuminate\Contracts\Bus\Dispatcher` contract now includes the `dispatchAfterResponse($command, $handler = null)` method. -->
`Illuminate\Contracts\Bus\Dispatcher` 계약에는 이제 `dispatchAfterResponse($command, $handler = null)` 메서드가 포함됩니다.

<!-- If you maintain a custom dispatcher implementation, add this method to your class. -->
사용자 정의 dispatcher 구현을 유지 관리하고 있다면 이 메서드를 클래스에 추가하십시오.

<a name="responsefactory-contract-eventstream"></a>
<!-- #### `ResponseFactory` Contract: `eventStream` -->
#### `ResponseFactory` Contract: `eventStream`

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `Illuminate\Contracts\Routing\ResponseFactory` contract now includes an `eventStream` signature. -->
`Illuminate\Contracts\Routing\ResponseFactory` 계약에는 이제 `eventStream` 시그니처가 포함됩니다.

<!-- If you maintain a custom implementation of this contract, you should add this method. -->
이 계약의 사용자 정의 구현을 유지 관리하고 있다면 이 메서드를 추가해야 합니다.

<a name="mustverifyemail-contract-markemailasunverified"></a>
<!-- #### `MustVerifyEmail` Contract: `markEmailAsUnverified` -->
#### `MustVerifyEmail` Contract: `markEmailAsUnverified`

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `Illuminate\Contracts\Auth\MustVerifyEmail` contract now includes `markEmailAsUnverified()`. -->
`Illuminate\Contracts\Auth\MustVerifyEmail` 계약에는 이제 `markEmailAsUnverified()`가 포함됩니다.

<!-- If you provide a custom implementation of this contract, add this method to remain compatible. -->
이 계약의 사용자 정의 구현을 제공한다면 호환성을 유지하기 위해 이 메서드를 추가하십시오.

<a name="database"></a>
<!-- ### Database -->
### Database

<a name="database-upsert-mariadb-mysql"></a>
<!-- #### Database `upsert` With MySQL or MariaDB -->
#### Database `upsert` With MySQL or MariaDB

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- Laravel now validates that the caller provides a non-empty value for `uniqueBy`, and will throw an `InvalidArgumentException` instead of generating invalid SQL. -->
Laravel은 이제 호출자가 `uniqueBy`에 비어 있지 않은 값을 제공했는지 검증하며, 잘못된 SQL을 생성하는 대신 `InvalidArgumentException`을 발생시킵니다.

<!-- Although the MariaDB and MySQL database drivers ignore the `uniqueBy` value and always use the table's primary and unique indexes to detect existing records, the validation still applies. An `InvalidArgumentException` will be thrown if `uniqueBy` is empty. -->
MariaDB 및 MySQL 데이터베이스 드라이버는 `uniqueBy` 값을 무시하고 항상 테이블의 primary 및 unique 인덱스를 사용해 기존 레코드를 감지하지만, 이 검증은 여전히 적용됩니다. `uniqueBy`가 비어 있으면 `InvalidArgumentException`이 발생합니다.

<a name="mysql-delete-queries-with-join-order-by-and-limit"></a>
<!-- #### MySQL `DELETE` Queries With `JOIN`, `ORDER BY`, and `LIMIT` -->
#### MySQL `DELETE` Queries With `JOIN`, `ORDER BY`, and `LIMIT`

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Laravel now compiles full `DELETE ... JOIN` queries including `ORDER BY` and `LIMIT` for MySQL grammar. -->
Laravel은 이제 MySQL grammar에서 `ORDER BY`와 `LIMIT`를 포함한 전체 `DELETE ... JOIN` 쿼리를 컴파일합니다.

<!-- In previous versions, `ORDER BY` / `LIMIT` clauses could be silently ignored on joined deletes. In Laravel 13, these clauses are included in the generated SQL. As a result, database engines that do not support this syntax (such as standard MySQL / MariaDB variants) may now throw a `QueryException` instead of executing an unbounded delete. -->
이전 버전에서는 joined delete에서 `ORDER BY` / `LIMIT` 절이 조용히 무시될 수 있었습니다. Laravel 13에서는 이러한 절이 생성된 SQL에 포함됩니다. 그 결과, 표준 MySQL / MariaDB 변형처럼 이 문법을 지원하지 않는 데이터베이스 엔진에서는 범위 제한 없는 delete를 실행하는 대신 `QueryException`이 발생할 수 있습니다.

<a name="eloquent"></a>
<!-- ### Eloquent -->
### Eloquent

<a name="model-booting-and-nested-instantiation"></a>
<!-- #### Model Booting and Nested Instantiation -->
#### Model Booting and Nested Instantiation

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- Creating a new model instance while that model is still booting is now disallowed and throws a `LogicException`. -->
모델이 아직 부팅 중일 때 새 모델 인스턴스를 생성하는 것은 이제 허용되지 않으며 `LogicException`이 발생합니다.

<!-- This affects code that instantiates models from inside model `boot` methods or trait `boot*` methods: -->
이는 모델 `boot` 메서드 또는 trait `boot*` 메서드 내부에서 모델을 인스턴스화하는 코드에 영향을 줍니다.

```php
protected static function boot()
{
    parent::boot();

    // No longer allowed during booting...
    (new static())->getTable();
}
```

<!-- Move this logic outside the boot cycle to avoid nested booting. -->
중첩 부팅을 피하려면 이 로직을 부팅 주기 밖으로 이동하십시오.

<a name="polymorphic-pivot-table-name-generation"></a>
<!-- #### Polymorphic Pivot Table Name Generation -->
#### Polymorphic Pivot Table Name Generation

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- When table names are inferred for polymorphic pivot models using custom pivot model classes, Laravel now generates pluralized names. -->
사용자 정의 pivot 모델 클래스를 사용하여 다형성 pivot 모델의 테이블 이름을 추론할 때, Laravel은 이제 복수형 이름을 생성합니다.

<!-- If your application depended on the previous singular inferred names for morph pivot tables and used custom pivot classes, you should explicitly define the table name on your pivot model. -->
애플리케이션이 이전의 단수형 추론 이름에 의존했고 morph pivot 테이블에 사용자 정의 pivot 클래스를 사용했다면, pivot 모델에 테이블 이름을 명시적으로 정의해야 합니다.

<a name="collection-model-serialization-restores-eager-loaded-relations"></a>
<!-- #### Collection Model Serialization Restores Eager-Loaded Relations -->
#### Collection Model Serialization Restores Eager-Loaded Relations

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- When Eloquent model collections are serialized and restored (such as in queued jobs), eager-loaded relations are now restored for the collection's models. -->
Eloquent 모델 컬렉션이 직렬화되고 복원될 때(예: 큐 작업에서), 컬렉션의 모델에 대해 즉시 로드된 연관관계가 이제 복원됩니다.

<!-- If your code depended on relations not being present after deserialization, you may need to adjust that logic. -->
역직렬화 후 연관관계가 존재하지 않는다는 점에 코드가 의존했다면 해당 로직을 조정해야 할 수 있습니다.

<a name="http-client"></a>
<!-- ### HTTP Client -->
### HTTP Client

<a name="http-client-response-throw-and-throwif-signatures"></a>
<!-- #### HTTP Client `Response::throw` and `throwIf` Signatures -->
#### HTTP Client `Response::throw` and `throwIf` Signatures

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The HTTP client response methods now declare their callback parameters in the method signatures: -->
HTTP 클라이언트 응답 메서드는 이제 메서드 시그니처에 콜백 매개변수를 선언합니다.

```php
public function throw($callback = null);
public function throwIf($condition, $callback = null);
```

<!-- If you override these methods in custom response classes, ensure your method signatures are compatible. -->
사용자 정의 응답 클래스에서 이 메서드를 오버라이드한다면 메서드 시그니처가 호환되는지 확인하십시오.

<a name="notifications"></a>
<!-- ### Notifications -->
### Notifications

<a name="default-password-reset-subject"></a>
<!-- #### Default Password Reset Subject -->
#### Default Password Reset Subject

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- Laravel's default password reset mail subject has changed: -->
Laravel의 기본 비밀번호 재설정 메일 제목이 변경되었습니다.

```text
// Laravel <= 12.x
Reset Password Notification

// Laravel >= 13.x
Reset your password
```

<!-- If your tests, assertions, or translation overrides depend on the previous default string, update them accordingly. -->
테스트, assertion 또는 번역 override가 이전 기본 문자열에 의존한다면 그에 맞게 업데이트하십시오.

<a name="queued-notifications-and-missing-models"></a>
<!-- #### Queued Notifications and Missing Models -->
#### Queued Notifications and Missing Models

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- Queued notifications now respect the `#[DeleteWhenMissingModels]` attribute and `$deleteWhenMissingModels` property defined on the notification class. -->
큐에 들어간 알림은 이제 알림 클래스에 정의된 `#[DeleteWhenMissingModels]` 속성과 `$deleteWhenMissingModels` 속성을 존중합니다.

<!-- In previous versions, missing models could still cause queued notification jobs to fail in cases where you expected them to be deleted. -->
이전 버전에서는 삭제될 것으로 예상한 경우에도 누락된 모델로 인해 큐에 들어간 알림 작업이 실패할 수 있었습니다.

<a name="queue"></a>
<!-- ### Queue -->
### Queue

<a name="jobattempted-event-exception-payload"></a>
<!-- #### `JobAttempted` Event Exception Payload -->
#### `JobAttempted` Event Exception Payload

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Illuminate\Queue\Events\JobAttempted` event now exposes the exception object (or `null`) via `$exception`, replacing the previous boolean `$exceptionOccurred` property: -->
`Illuminate\Queue\Events\JobAttempted` 이벤트는 이제 이전 boolean `$exceptionOccurred` 속성을 대체하여 `$exception`을 통해 예외 객체(또는 `null`)를 노출합니다.

```php
// Laravel <= 12.x
$event->exceptionOccurred;

// Laravel >= 13.x
$event->exception;
```

<!-- If you listen for this event, update your listener code accordingly. -->
이 이벤트를 수신하고 있다면 listener 코드를 그에 맞게 업데이트하십시오.

<a name="queuebusy-event-property-rename"></a>
<!-- #### `QueueBusy` Event Property Rename -->
#### `QueueBusy` Event Property Rename

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Illuminate\Queue\Events\QueueBusy` event property `$connection` has been renamed to `$connectionName` for consistency with other queue events. -->
`Illuminate\Queue\Events\QueueBusy` 이벤트 속성 `$connection`은 다른 큐 이벤트와의 일관성을 위해 `$connectionName`으로 이름이 변경되었습니다.

<!-- If your listeners reference `$connection`, update them to `$connectionName`. -->
listener가 `$connection`을 참조한다면 `$connectionName`으로 업데이트하십시오.

<a name="queue-contract-method-additions"></a>
<!-- #### `Queue` Contract Method Additions -->
#### `Queue` Contract Method Additions

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- The `Illuminate\Contracts\Queue\Queue` contract now includes queue size inspection methods that were previously only declared in docblocks. -->
`Illuminate\Contracts\Queue\Queue` 계약에는 이제 이전에 docblock에만 선언되어 있던 큐 크기 검사 메서드가 포함됩니다.

<!-- If you maintain custom queue driver implementations of this contract, add implementations for: -->
이 계약의 사용자 정의 큐 드라이버 구현을 유지 관리하고 있다면 다음 구현을 추가하십시오.

<div class="content-list" markdown="1">

- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`

</div>

<a name="routing"></a>
<!-- ### Routing -->
### Routing

<a name="domain-route-registration-precedence"></a>
<!-- #### Domain Route Registration Precedence -->
#### Domain Route Registration Precedence

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Routes with an explicit domain are now prioritized before non-domain routes in route matching. -->
명시적인 도메인이 있는 라우트는 이제 라우트 매칭에서 도메인이 없는 라우트보다 우선됩니다.

<!-- This allows catch-all subdomain routes to behave consistently even when non-domain routes are registered earlier. If your application relied on previous registration precedence between domain and non-domain routes, review route matching behavior. -->
이를 통해 도메인이 없는 라우트가 먼저 등록되어 있더라도 catch-all 서브도메인 라우트가 일관되게 동작할 수 있습니다. 애플리케이션이 도메인 라우트와 도메인이 없는 라우트 사이의 이전 등록 우선순위에 의존했다면 라우트 매칭 동작을 검토하십시오.

<a name="session"></a>
<!-- ### Session -->
### Session

<a name="session-serialization-configuration"></a>
<!-- #### Session `serialization` Configuration -->
#### Session `serialization` Configuration

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- To help prevent PHP deserialization gadget chain attacks, the default application skeleton now sets the session `serialization` option to `json` in the `config/session.php` file. -->
PHP 역직렬화 가젯 체인 공격을 방지하는 데 도움을 주기 위해 기본 애플리케이션 스켈레톤은 이제 `config/session.php` 파일에서 세션 `serialization` 옵션을 `json`으로 설정합니다.

<!-- If you are upgrading an existing application and syncing your configuration files with the Laravel 13 skeleton, updating this value from `php` to `json` will invalidate all active user sessions. -->
기존 애플리케이션을 업그레이드하면서 설정 파일을 Laravel 13 스켈레톤과 동기화하는 경우, 이 값을 `php`에서 `json`으로 변경하면 활성화된 모든 사용자 세션이 무효화됩니다.

<!-- If you wish to seamlessly maintain active sessions during your upgrade, you should ensure this value remains set to `php`. However, if your application does not store PHP objects in the session and you are comfortable requiring your users to re-authenticate, we recommend updating this value to `json` for improved security. -->
업그레이드 중 활성 세션을 원활하게 유지하려면 이 값을 `php`로 설정된 상태로 유지해야 합니다. 하지만 애플리케이션이 세션에 PHP 객체를 저장하지 않고 사용자에게 다시 인증하도록 요구해도 괜찮다면, 보안 강화를 위해 이 값을 `json`으로 변경하는 것을 권장합니다.

<a name="scheduling"></a>
<!-- ### Scheduling -->
### Scheduling

<a name="withscheduling-registration-timing"></a>
<!-- #### `withScheduling` Registration Timing -->
#### `withScheduling` Registration Timing

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- Schedules registered via `ApplicationBuilder::withScheduling()` are now deferred until `Schedule` is resolved. -->
`ApplicationBuilder::withScheduling()`을 통해 등록된 스케줄은 이제 `Schedule`이 resolve될 때까지 지연됩니다.

<!-- If your application relied on immediate schedule registration timing during bootstrap, you may need to adjust that logic. -->
애플리케이션이 bootstrap 중 즉시 스케줄이 등록되는 타이밍에 의존했다면 해당 로직을 조정해야 할 수 있습니다.

<a name="security"></a>
<!-- ### Security -->
### Security

<a name="request-forgery-protection"></a>
<!-- #### Request Forgery Protection -->
#### Request Forgery Protection

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- Laravel's CSRF middleware has been renamed from `VerifyCsrfToken` to `PreventRequestForgery`, and now includes request-origin verification using the `Sec-Fetch-Site` header. -->
Laravel의 CSRF middleware 이름이 `VerifyCsrfToken`에서 `PreventRequestForgery`로 변경되었으며, 이제 `Sec-Fetch-Site` 헤더를 사용한 요청 출처 검증이 포함됩니다.

<!-- `VerifyCsrfToken` and `ValidateCsrfToken` remain as deprecated aliases, but direct references should be updated to `PreventRequestForgery`, especially when excluding middleware in tests or route definitions: -->
`VerifyCsrfToken`과 `ValidateCsrfToken`은 deprecated alias로 남아 있지만, 특히 테스트나 라우트 정의에서 middleware를 제외할 때는 직접 참조를 `PreventRequestForgery`로 업데이트해야 합니다.

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

// Laravel <= 12.x
->withoutMiddleware([VerifyCsrfToken::class]);

// Laravel >= 13.x
->withoutMiddleware([PreventRequestForgery::class]);
```

<!-- The middleware configuration API now also provides `preventRequestForgery(...)`. -->
middleware 설정 API는 이제 `preventRequestForgery(...)`도 제공합니다.

<a name="support"></a>
<!-- ### Support -->
### Support

<a name="manager-extend-callback-binding"></a>
<!-- #### Manager `extend` Callback Binding -->
#### Manager `extend` Callback Binding

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Custom driver closures registered via manager `extend` methods are now bound to the manager instance. -->
manager `extend` 메서드를 통해 등록한 커스텀 드라이버 클로저는 이제 manager 인스턴스에 바인딩됩니다.

<!-- If you previously relied on another bound object (such as a service provider instance) as `$this` inside these callbacks, you should move those values into closure captures using `use (...)`. -->
이전에 이 콜백 안에서 `$this`가 다른 바인딩된 객체(예: 서비스 프로바이더 인스턴스)를 가리킨다고 가정했다면, 해당 값들을 `use (...)`를 사용해 클로저 캡처로 옮겨야 합니다.

<a name="str-factories-reset-between-tests"></a>
<!-- #### `Str` Factories Reset Between Tests -->
#### `Str` Factories Reset Between Tests

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Laravel now resets custom `Str` factories during test teardown. -->
Laravel은 이제 테스트 정리 단계에서 커스텀 `Str` 팩토리를 초기화합니다.

<!-- If your tests depended on custom UUID / ULID / random string factories persisting between test methods, you should set them in each relevant test or setup hook. -->
테스트가 커스텀 UUID / ULID / 랜덤 문자열 팩토리가 테스트 메서드 사이에서도 유지된다고 가정하고 있었다면, 각 관련 테스트나 setup 훅에서 다시 설정해야 합니다.

<a name="jsfrom-uses-unescaped-unicode-by-default"></a>
<!-- #### `Js::from` Uses Unescaped Unicode By Default -->
#### `Js::from` Uses Unescaped Unicode By Default

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 매우 낮음**

<!-- `Illuminate\Support\Js::from` now uses `JSON_UNESCAPED_UNICODE` by default. -->
`Illuminate\Support\Js::from`은 이제 기본적으로 `JSON_UNESCAPED_UNICODE`를 사용합니다.

<!-- If your tests or frontend output comparisons depended on escaped Unicode sequences (for example `\u00e8`), update your expectations. -->
테스트나 프론트엔드 출력 비교가 이스케이프된 Unicode 시퀀스(예: `\u00e8`)에 의존하고 있었다면, 기대값을 업데이트하십시오.

<a name="utilities"></a>
<!-- ### Utilities -->
### Utilities

<a name="symfony-polyfill"></a>
<!-- #### Symfony PHP 8.5 Polyfill and Global Function Conflicts -->
#### Symfony PHP 8.5 Polyfill and Global Function Conflicts

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Laravel 13 introduces a dependency on `symfony/polyfill-php85`. On PHP versions below 8.5, this polyfill defines global functions such as `array_first()` and `array_last()` unless they have already been defined earlier during bootstrap. -->
Laravel 13은 `symfony/polyfill-php85` 의존성을 도입합니다. PHP 8.5 미만 버전에서는 이 폴리필이 부트스트랩 과정에서 이미 먼저 정의되지 않은 경우 `array_first()`와 `array_last()` 같은 전역 함수를 정의합니다.

<!-- These functions may conflict with legacy helper packages like `laravel/helpers` or custom global helpers using the same names. For example, the historical `array_first()` helper accepted a callback to return the first matching element, while the polyfilled version only returns the first element of the array. -->
이 함수들은 `laravel/helpers` 같은 레거시 헬퍼 패키지나 같은 이름을 사용하는 커스텀 전역 헬퍼와 충돌할 수 있습니다. 예를 들어, 기존의 `array_first()` 헬퍼는 일치하는 첫 번째 요소를 반환하기 위해 콜백을 받을 수 있었지만, 폴리필 버전은 배열의 첫 번째 요소만 반환합니다.

<!-- To avoid conflicts and ensure consistent behavior across PHP versions, you should prefer the `Illuminate\Support\Arr` methods: -->
충돌을 피하고 PHP 버전 전반에서 일관된 동작을 보장하려면 `Illuminate\Support\Arr` 메서드를 사용하는 것이 좋습니다.

```php
use Illuminate\Support\Arr;

Arr::first($array, function ($value) {
  return /* condition */;
});
```

<a name="views"></a>
<!-- ### Views -->
### Views

<a name="pagination-bootstrap-view-names"></a>
<!-- #### Pagination Bootstrap View Names -->
#### Pagination Bootstrap View Names

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The internal pagination view names for Bootstrap 3 defaults are now explicit: -->
Bootstrap 3 기본값에 대한 내부 페이지네이션 뷰 이름이 이제 명시적으로 변경되었습니다.

```nothing
// Laravel <= 12.x
pagination::default
pagination::simple-default

// Laravel >= 13.x
pagination::bootstrap-3
pagination::simple-bootstrap-3
```

<!-- If your application references the old pagination view names directly, update those references. -->
애플리케이션에서 이전 페이지네이션 뷰 이름을 직접 참조하고 있다면, 해당 참조를 업데이트하십시오.

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/12.x...13.x) and choose which updates are important to you. -->
또한 `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel)의 변경 사항을 확인하는 것을 권장합니다. 이러한 변경 사항 중 상당수는 필수는 아니지만, 해당 파일들을 애플리케이션과 동기화해 두고 싶을 수 있습니다. 이 업그레이드 가이드에서 일부 변경 사항을 다루겠지만, 설정 파일이나 주석 변경과 같은 다른 변경 사항은 다루지 않습니다. [GitHub comparison tool](https://github.com/laravel/laravel/compare/12.x...13.x)을 사용하면 변경 사항을 쉽게 확인하고, 어떤 업데이트가 중요한지 선택할 수 있습니다.
