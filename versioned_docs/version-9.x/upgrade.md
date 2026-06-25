<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading To 9.0 From 8.x](#upgrade-9.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Flysystem 3.x](#flysystem-3)
- [Symfony Mailer](#symfony-mailer)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods](#belongs-to-many-first-or-new)
- [Custom Casts & `null`](#custom-casts-and-null)
- [Default HTTP Client Timeout](#http-client-default-timeout)
- [PHP Return Types](#php-return-types)
- [Postgres "Schema" Configuration](#postgres-schema-configuration)
- [The `assertDeleted` Method](#the-assert-deleted-method)
- [The `lang` Directory](#the-lang-directory)
- [The `password` Rule](#the-password-rule)
- [The `when` / `unless` Methods](#when-and-unless-methods)
- [Unvalidated Array Keys](#unvalidated-array-keys)

<!-- </div> -->
</div>

<a name="upgrade-9.0"></a>
<!-- ## Upgrading To 9.0 From 8.x -->
## Upgrading To 9.0 From 8.x

<a name="estimated-upgrade-time-30-minutes"></a>
<!-- #### Estimated Upgrade Time: 30 Minutes -->
#### Estimated Upgrade Time: 30 Minutes

> [!NOTE]
> 가능한 모든 중요한 변경 사항(breaking change)을 문서화하려고 노력했으나, 일부 변경 사항은 프레임워크의 잘 사용하지 않는 부분에 영향을 줄 수 있으므로 실제로는 일부만이 여러분의 애플리케이션에 영향을 줄 수 있습니다. 시간을 절약하고 싶다면, [Laravel Shift](https://laravelshift.com/)를 활용하여 업그레이드 작업을 자동화할 수 있습니다.

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- #### PHP 8.0.2 Required -->
#### PHP 8.0.2 Required

<!-- Laravel now requires PHP 8.0.2 or greater. -->
Laravel은 이제 PHP 8.0.2 이상 버전이 필요합니다.

<!-- #### Composer Dependencies -->
#### Composer Dependencies

<!-- You should update the following dependencies in your application's `composer.json` file: -->
애플리케이션의 `composer.json` 파일에서 다음 의존성들을 업데이트해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `laravel/framework` to `^9.0`
- `nunomaduro/collision` to `^6.1`
-->
- `laravel/framework`를 `^9.0`으로
- `nunomaduro/collision`을 `^6.1`로

<!-- </div> -->
</div>

<!-- In addition, please replace `facade/ignition` with `"spatie/laravel-ignition": "^1.0"` and `pusher/pusher-php-server` (if applicable) with `"pusher/pusher-php-server": "^5.0"` in your application's `composer.json` file. -->
또한, 애플리케이션의 `composer.json` 파일에서 `facade/ignition`을 `"spatie/laravel-ignition": "^1.0"`으로, 그리고(사용 중이라면) `pusher/pusher-php-server`를 `"pusher/pusher-php-server": "^5.0"`으로 교체해 주시기 바랍니다.

<!-- Furthermore, the following first-party packages have received new major releases to support Laravel 9.x. If applicable, you should read their individual upgrade guides before upgrading: -->
추가적으로, 아래와 같은 Laravel 9.x 지원을 위해 새로운 주요 버전(major release)이 배포된 1차 제공 패키지들이 있습니다. 해당 패키지들을 사용 중이라면, 업그레이드 전 각 패키지의 업그레이드 가이드를 참고해 주세요.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!-- - [Vonage Notification Channel (v3.0)](https://github.com/laravel/vonage-notification-channel/blob/3.x/UPGRADE.md) (Replaces Nexmo) -->
- [Vonage Notification Channel (v3.0)](https://github.com/laravel/vonage-notification-channel/blob/3.x/UPGRADE.md) (Nexmo를 대체)

<!-- </div> -->
</div>

<!-- Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 9 support. -->
마지막으로, 애플리케이션에서 사용하는 기타 써드파티 패키지들의 버전도 확인하여 Laravel 9 지원 버전이 맞는지 검토하시기 바랍니다.

<a name="php-return-types"></a>
<!-- #### PHP Return Types -->
#### PHP Return Types

<!-- PHP is beginning to transition to requiring return type definitions on PHP methods such as `offsetGet`, `offsetSet`, etc. In light of this, Laravel 9 has implemented these return types in its code base. Typically, this should not affect user written code; however, if you are overriding one of these methods by extending Laravel's core classes, you will need to add these return types to your own application or package code: -->
PHP는 이제 `offsetGet`, `offsetSet` 등과 같은 일부 메서드에서 반환 타입 명시를 점진적으로 요구하고 있습니다. 이에 따라 Laravel 9에서도 해당 메서드들에 반환 타입이 추가되었습니다. 일반적으로 사용자 코드에는 영향을 주지 않으나, 만약 Laravel의 코어 클래스를 확장(extends)하여 해당 메서드를 오버라이딩하고 있다면, 동일한 반환 타입 명시를 코드에 추가해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `count(): int`
- `getIterator(): Traversable`
- `getSize(): int`
- `jsonSerialize(): array`
- `offsetExists($key): bool`
- `offsetGet($key): mixed`
- `offsetSet($key, $value): void`
- `offsetUnset($key): void`
-->
- `count(): int`
- `getIterator(): Traversable`
- `getSize(): int`
- `jsonSerialize(): array`
- `offsetExists($key): bool`
- `offsetGet($key): mixed`
- `offsetSet($key, $value): void`
- `offsetUnset($key): void`

<!-- </div> -->
</div>

<!-- In addition, return types were added to methods implementing PHP's `SessionHandlerInterface`. Again, it is unlikely that this change affects your own application or package code: -->
또한, PHP의 `SessionHandlerInterface`를 구현하는 메서드에도 반환 타입이 추가되었습니다. 일반 애플리케이션이나 패키지 코드에는 영향을 주지 않겠지만, 혹시 오버라이딩 중인 경우에만 아래 타입을 반영해야 합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `open($savePath, $sessionName): bool`
- `close(): bool`
- `read($sessionId): string|false`
- `write($sessionId, $data): bool`
- `destroy($sessionId): bool`
- `gc($lifetime): int`
-->
- `open($savePath, $sessionName): bool`
- `close(): bool`
- `read($sessionId): string|false`
- `write($sessionId, $data): bool`
- `destroy($sessionId): bool`
- `gc($lifetime): int`

<!-- </div> -->
</div>

<a name="application"></a>
<!-- ### Application -->
### Application

<a name="the-application-contract"></a>
<!-- #### The `Application` Contract -->
#### The `Application` Contract

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `storagePath` method of the `Illuminate\Contracts\Foundation\Application` interface has been updated to accept a `$path` argument. If you are implementing this interface you should update your implementation accordingly: -->
`Illuminate\Contracts\Foundation\Application` 인터페이스의 `storagePath` 메서드는 `$path` 인수를 받도록 변경되었습니다. 이 인터페이스를 직접 구현하고 있다면, 구현체도 아래와 같이 변경해야 합니다.

```
public function storagePath($path = '');

```
<!-- Similarly, the `langPath` method of the `Illuminate\Foundation\Application` class has been updated to accept a `$path` argument: -->
마찬가지로, `Illuminate\Foundation\Application` 클래스의 `langPath` 메서드도 `$path` 인수를 받도록 변경되었습니다.

```
public function langPath($path = '');
```

<!-- #### Exception Handler `ignore` Method -->
#### Exception Handler `ignore` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The exception handler's `ignore` method is now `public` instead of `protected`. This method is not included in the default application skeleton; however, if you have manually defined this method you should update its visibility to `public`: -->
예외 핸들러의 `ignore` 메서드는 이제 `protected`가 아니라 `public`으로 선언되어야 합니다. 이 메서드는 기본 애플리케이션 스켈레톤에는 포함되어 있지 않지만, 직접 구현한 경우 `public` 가시성으로 변경해 주세요.

```php
public function ignore(string $class);
```

<!-- #### Exception Handler Contract Binding -->
#### Exception Handler Contract Binding

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 아주 낮음**

<!-- Previously, in order to override the default Laravel exception handler, custom implementations were bound into the service container using the `\App\Exceptions\Handler::class` type. However, you should now bind custom implementations using the `\Illuminate\Contracts\Debug\ExceptionHandler::class` type. -->
기존에는 Laravel의 기본 예외 핸들러를 오버라이드할 때, `\App\Exceptions\Handler::class` 타입으로 서비스 컨테이너에 바인딩하였습니다. 이제는 `\Illuminate\Contracts\Debug\ExceptionHandler::class` 타입으로 바인딩해야 합니다.

<!-- ### Blade -->
### Blade

<!-- #### Lazy Collections & The `$loop` Variable -->
#### Lazy Collections & The `$loop` Variable

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- When iterating over a `LazyCollection` instance within a Blade template, the `$loop` variable is no longer available, as accessing this variable causes the entire `LazyCollection` to be loaded into memory, thus rendering the usage of lazy collections pointless in this scenario. -->
Blade 템플릿 내에서 `LazyCollection` 인스턴스를 반복(iterate)할 때, 더 이상 `$loop` 변수를 사용할 수 없습니다. 이 변수에 접근하면 전체 `LazyCollection`이 메모리로 로드되어, 원래의 lazy 처리 목적이 사라지기 때문입니다.

<!-- #### Checked / Disabled / Selected Blade Directives -->
#### Checked / Disabled / Selected Blade Directives

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The new `@checked`, `@disabled`, and `@selected` Blade directives may conflict with Vue events of the same name. You may use `@@` to escape the directives and avoid this conflict: `@@selected`. -->
새로운 `@checked`, `@disabled`, `@selected` Blade 디렉티브는 동일한 이름의 Vue 이벤트와 충돌할 수 있습니다. 충돌을 피하려면 디렉티브 앞에 `@@`를 붙여 이스케이프 해주세요: `@@selected`.

<!-- ### Collections -->
### Collections

<!-- #### The `Enumerable` Contract -->
#### The `Enumerable` Contract

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Illuminate\Support\Enumerable` contract now defines a `sole` method. If you are manually implementing this interface, you should update your implementation to reflect this new method: -->
`Illuminate\Support\Enumerable` 인터페이스에 `sole` 메서드가 추가되었습니다. 이 인터페이스를 직접 구현하는 경우, 반드시 해당 메서드를 추가해주세요.

```php
public function sole($key = null, $operator = null, $value = null);
```

<!-- #### The `reduceWithKeys` Method -->
#### The `reduceWithKeys` Method

<!-- The `reduceWithKeys` method has been removed as the `reduce` method provides the same functionality. You may simply update your code to call `reduce` instead of `reduceWithKeys`. -->
`reduceWithKeys` 메서드는 삭제되었습니다. `reduce` 메서드가 동일한 기능을 제공하므로, 기존 코드에서 `reduceWithKeys` 대신 `reduce`를 호출하도록 교체해 주시면 됩니다.

<!-- #### The `reduceMany` Method -->
#### The `reduceMany` Method

<!-- The `reduceMany` method has been renamed to `reduceSpread` for naming consistency with other similar methods. -->
`reduceMany` 메서드가 `reduceSpread`로 이름이 바뀌었습니다. 비슷한 역할의 다른 메서드들과 네이밍 일관성을 맞추기 위함입니다.

<!-- ### Container -->
### Container

<!-- #### The `Container` Contract -->
#### The `Container` Contract

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 아주 낮음**

<!-- The `Illuminate\Contracts\Container\Container` contract has received two method definitions: `scoped` and `scopedIf`. If you are manually implementing this contract, you should update your implementation to reflect these new methods. -->
`Illuminate\Contracts\Container\Container` 인터페이스에 `scoped`, `scopedIf`라는 메서드가 추가되었습니다. 만약 이 컨트랙트를 직접 구현 중이라면, 해당 메서드들도 추가해주셔야 합니다.

<!-- #### The `ContextualBindingBuilder` Contract -->
#### The `ContextualBindingBuilder` Contract

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 아주 낮음**

<!-- The `Illuminate\Contracts\Container\ContextualBindingBuilder` contract now defines a `giveConfig` method. If you are manually implementing this interface, you should update your implementation to reflect this new method: -->
`Illuminate\Contracts\Container\ContextualBindingBuilder` 인터페이스에 `giveConfig`라는 메서드가 추가되었습니다. 직접 구현한다면 아래와 같이 메서드를 추가해주세요.

```php
public function giveConfig($key, $default = null);
```

<!-- ### Database -->
### Database

<a name="postgres-schema-configuration"></a>
<!-- #### Postgres "Schema" Configuration -->
#### Postgres "Schema" Configuration

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- The `schema` configuration option used to configure Postgres connection search paths in your application's `config/database.php` configuration file should be renamed to `search_path`. -->
애플리케이션의 `config/database.php`에서 Postgres 연결의 검색 경로(search path)를 설정하는 `schema` 옵션의 이름이 `search_path`로 변경되었습니다.

<a name="schema-builder-doctrine-method"></a>
<!-- #### Schema Builder `registerCustomDoctrineType` Method -->
#### Schema Builder `registerCustomDoctrineType` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `registerCustomDoctrineType` method has been removed from the `Illuminate\Database\Schema\Builder` class. You may use the `registerDoctrineType` method on the `DB` facade instead, or register custom Doctrine types in the `config/database.php` configuration file. -->
`Illuminate\Database\Schema\Builder` 클래스의 `registerCustomDoctrineType` 메서드는 제거되었습니다. 대신, `DB` 파사드의 `registerDoctrineType` 메서드를 사용하거나, `config/database.php`의 설정 파일에서 커스텀 Doctrine 타입을 등록할 수 있습니다.

<!-- ### Eloquent -->
### Eloquent

<a name="custom-casts-and-null"></a>
<!-- #### Custom Casts & `null` -->
#### Custom Casts & `null`

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- In previous releases of Laravel, the `set` method of custom cast classes was not invoked if the cast attribute was being set to `null`. However, this behavior was inconsistent with the Laravel documentation. In Laravel 9.x, the `set` method of the cast class will be invoked with `null` as the provided `$value` argument. Therefore, you should ensure your custom casts are able to sufficiently handle this scenario: -->
기존 Laravel에서는 커스텀 cast 클래스의 `set` 메서드는 해당 속성(attribute)에 `null`이 할당될 때 호출되지 않았습니다. 그러나 이 동작은 Laravel 공식문서의 설명과 일치하지 않았습니다. Laravel 9.x부터는 `set` 메서드가 항상 호출되며, 이때 `$value` 인자는 `null`이 전달될 수 있습니다. 따라서 커스텀 cast 클래스를 작성할 때 null 값을 올바르게 처리하도록 주의해야 합니다.

```php
/**
 * Prepare the given value for storage.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  AddressModel  $value
 * @param  array  $attributes
 * @return array
 */
public function set($model, $key, $value, $attributes)
{
    if (! $value instanceof AddressModel) {
        throw new InvalidArgumentException('The given value is not an Address instance.');
    }

    return [
        'address_line_one' => $value->lineOne,
        'address_line_two' => $value->lineTwo,
    ];
}
```

<a name="belongs-to-many-first-or-new"></a>
<!-- #### Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` Methods -->
#### Belongs To Many `firstOrNew`, `firstOrCreate`, and `updateOrCreate` Methods

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- The `belongsToMany` relationship's `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods all accept an array of attributes as their first argument. In previous releases of Laravel, this array of attributes was compared against the "pivot" / intermediate table for existing records. -->
`belongsToMany` 관계의 `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드는 첫 번째 인수로 속성 배열을 받습니다. 기존 Laravel에서는 이 배열을 연결 테이블(피벗 테이블)과 비교하여 기존 레코드를 확인했습니다.

<!-- However, this behavior was unexpected and typically unwanted. Instead, these methods now compare the array of attributes against the table of the related model: -->
그러나 이 동작은 예상치 못한 것이었고 일반적으로 원하는 동작이 아니었습니다. 이제부터는 이 메서드들이 속성 배열을 **관계된 모델 테이블**과 비교합니다.

```php
$user->roles()->updateOrCreate([
    'name' => 'Administrator',
]);
```

<!-- In addition, the `firstOrCreate` method now accepts a `$values` array as its second argument. This array will be merged with the first argument to the method (`$attributes`) when creating the related model if one does not already exist. This change makes this method consistent with the `firstOrCreate` methods offered by other relationship types: -->
또한, `firstOrCreate` 메서드는 두 번째 인수로 `$values` 배열을 받을 수 있게 되었습니다. 해당 모델이 존재하지 않을 때 모델 생성 시 첫 번째 인수(`$attributes`)와 두 번째 인수 값이 병합되어 사용됩니다. 이 방식은 다른 관계에서의 `firstOrCreate`와 일관성을 맞추기 위함입니다.

```php
$user->roles()->firstOrCreate([
    'name' => 'Administrator',
], [
    'created_by' => $user->id,
]);
```

<!-- #### The `touch` Method -->
#### The `touch` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `touch` method now accepts an attribute to touch. If you were previously overwriting this method, you should update your method signature to reflect this new argument: -->
`touch` 메서드는 이제 업데이트할 속성명을 인수로 받을 수 있습니다. 만약 이 메서드를 오버라이딩하고 있었다면 시그니처를 아래와 같이 바꿔야 합니다.

```php
public function touch($attribute = null);
```

<!-- ### Encryption -->
### Encryption

<!-- #### The Encrypter Contract -->
#### The Encrypter Contract

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Illuminate\Contracts\Encryption\Encrypter` contract now defines a `getKey` method. If you are manually implementing this interface, you should update your implementation accordingly: -->
`Illuminate\Contracts\Encryption\Encrypter` 인터페이스에 `getKey` 메서드가 추가되었습니다. 해당 인터페이스를 직접 구현 중이라면 다음과 같이 메서드를 추가하세요.

```php
public function getKey();
```

<!-- ### Facades -->
### Facades

<!-- #### The `getFacadeAccessor` Method -->
#### The `getFacadeAccessor` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `getFacadeAccessor` method must always return a container binding key. In previous releases of Laravel, this method could return an object instance; however, this behavior is no longer supported. If you have written your own facades, you should ensure that this method returns a container binding string: -->
`getFacadeAccessor` 메서드는 반드시 컨테이너 바인딩 키(문자열)를 반환해야 합니다. 이전 버전에서는 객체 인스턴스를 반환해도 동작했지만, 이제는 지원되지 않습니다. 커스텀 파사드를 직접 작성했다면, 반환값이 반드시 문자열인지 확인해야 합니다.

```php
/**
 * Get the registered name of the component.
 *
 * @return string
 */
protected static function getFacadeAccessor()
{
    return Example::class;
}
```

<!-- ### Filesystem -->
### Filesystem

<!-- #### The `FILESYSTEM_DRIVER` Environment Variable -->
#### The `FILESYSTEM_DRIVER` Environment Variable

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `FILESYSTEM_DRIVER` environment variable has been renamed to `FILESYSTEM_DISK` to more accurately reflect its usage. This change only affects the application skeleton; however, you are welcome to update your own application's environment variables to reflect this change if you wish. -->
`FILESYSTEM_DRIVER` 환경 변수명이 `FILESYSTEM_DISK`로 변경되어 더 정확한 의미를 표현합니다. 이 변경은 Laravel 기본 스켈레톤에만 영향을 미치며, 원한다면 자신의 애플리케이션 환경 변수도 동일하게 바꿀 수 있습니다.

<!-- #### The "Cloud" Disk -->
#### The "Cloud" Disk

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `cloud` disk configuration option was removed from the default application skeleton in November of 2020. This change only affects the application skeleton. If you are using the `cloud` disk within your application, you should leave this configuration value in your own application's skeleton. -->
`cloud` 디스크 설정 옵션은 2020년 11월부터 기본 애플리케이션 스켈레톤에서 삭제되었습니다. 만약 애플리케이션에서 `cloud` 디스크를 사용하고 있다면, 해당 설정을 계속 유지하셔야 합니다.

<a name="flysystem-3"></a>
<!-- ### Flysystem 3.x -->
### Flysystem 3.x

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- Laravel 9.x has migrated from [Flysystem](https://flysystem.thephpleague.com/v2/docs/) 1.x to 3.x. Under the hood, Flysystem powers all of the file manipulation methods provided by the `Storage` facade. In light of this, some changes may be required within your application; however, we have tried to make this transition as seamless as possible. -->
Laravel 9.x는 [Flysystem](https://flysystem.thephpleague.com/v2/docs/) 1.x에서 3.x로 업그레이드되었습니다. `Storage` 파사드가 제공하는 파일 조작 메서드들은 모두 Flysystem을 기반으로 하므로, 아래 변경점들에 주의하여 코드를 점검해 주시기 바랍니다.

<!-- #### Driver Prerequisites -->
#### Driver Prerequisites

<!-- Before using the S3, FTP, or SFTP drivers, you will need to install the appropriate package via the Composer package manager: -->
S3, FTP, SFTP 드라이버를 사용하려면 Composer로 아래 패키지를 설치해야 합니다.

<!--
- Amazon S3: `composer require -W league/flysystem-aws-s3-v3 "^3.0"`
- FTP: `composer require league/flysystem-ftp "^3.0"`
- SFTP: `composer require league/flysystem-sftp-v3 "^3.0"`
-->
- Amazon S3: `composer require -W league/flysystem-aws-s3-v3 "^3.0"`
- FTP: `composer require league/flysystem-ftp "^3.0"`
- SFTP: `composer require league/flysystem-sftp-v3 "^3.0"`

<!-- #### Overwriting Existing Files -->
#### Overwriting Existing Files

<!-- Write operations such as `put`, `write`, and `writeStream` now overwrite existing files by default. If you do not want to overwrite existing files, you should manually check for the file's existence before performing the write operation. -->
`put`, `write`, `writeStream` 등 파일 저장 계열 메서드는 이제 기존 파일을 기본적으로 **덮어씁니다**. 기존 파일을 덮어쓰기 싫다면 직접 파일 존재 여부를 체크 후 쓰기 작업을 수행해야 합니다.

<!-- #### Write Exceptions -->
#### Write Exceptions

<!-- Write operations such as `put`, `write`, and `writeStream` no longer throw an exception when a write operation fails. Instead, `false` is returned. If you would like to preserve the previous behavior which threw exceptions, you may define the `throw` option within a filesystem disk's configuration array: -->
`put`, `write`, `writeStream` 등의 쓰기 작업이 실패할 때 더 이상 예외가 발생하지 않고, **`false`를 반환**합니다. 기존처럼 예외 발생을 원한다면 디스크 설정 배열에 `throw` 옵션을 추가하세요.

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

<!-- #### Reading Missing Files -->
#### Reading Missing Files

<!-- Attempting to read from a file that does not exist now returns `null`. In previous releases of Laravel, an `Illuminate\Contracts\Filesystem\FileNotFoundException` would have been thrown. -->
존재하지 않는 파일을 읽으려고 하면 예외(`Illuminate\Contracts\Filesystem\FileNotFoundException`) 대신 `null`이 반환됩니다.

<!-- #### Deleting Missing Files -->
#### Deleting Missing Files

<!-- Attempting to `delete` a file that does not exist now returns `true`. -->
존재하지 않는 파일을 `delete`할 때, 이제는 항상 `true`를 반환합니다.

<!-- #### Cached Adapters -->
#### Cached Adapters

<!-- Flysystem no longer supports "cached adapters". Thus, they have been removed from Laravel and any relevant configuration (such as the `cache` key within disk configurations) can be removed. -->
Flysystem 3.x부터는 **캐시 어댑터** 기능이 지원되지 않습니다. 따라서 Laravel과 설정 파일에서도 관련된 옵션(예: 디스크 설정 내 `cache` 키)은 제거할 수 있습니다.

<!-- #### Custom Filesystems -->
#### Custom Filesystems

<!-- Slight changes have been made to the steps required to register custom filesystem drivers. Therefore, if you were defining your own custom filesystem drivers, or using packages that define custom drivers, you should update your code and dependencies. -->
커스텀 파일 시스템 드라이버를 등록하는 방식에 약간의 변경이 있습니다. 직접 커스텀 드라이버를 구현하거나, 해당 기능을 가진 패키지를 사용하는 경우 아래 가이드를 참고하여 코드 및 의존성을 수정해 주세요.

<!-- For example, in Laravel 8.x, a custom filesystem driver might be registered like so: -->
Laravel 8.x에서의 예시:

```php
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

Storage::extend('dropbox', function ($app, $config) {
    $client = new DropboxClient(
        $config['authorization_token']
    );

    return new Filesystem(new DropboxAdapter($client));
});
```

<!-- However, in Laravel 9.x, the callback given to the `Storage::extend` method should return an instance of `Illuminate\Filesystem\FilesystemAdapter` directly: -->
Laravel 9.x에서는 `Storage::extend` 콜백에서 반드시 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 직접 반환해야 합니다.

```php
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

Storage::extend('dropbox', function ($app, $config) {
    $adapter = new DropboxAdapter(
        new DropboxClient($config['authorization_token'])
    );

    return new FilesystemAdapter(
        new Filesystem($adapter, $config),
        $adapter,
        $config
    );
});
```

<!-- #### SFTP Private-Public Key Passphrase -->
#### SFTP Private-Public Key Passphrase

<!-- If your application is using Flysystem's SFTP adapter and private-public key authentication, the `password` configuration item that is used to decrypt the private key should be renamed to `passphrase`. -->
애플리케이션에서 Flysystem의 SFTP 어댑터와 개인-공개 키 인증을 사용한다면, 프라이빗 키를 복호화할 때 쓰는 `password` 설정 항목의 이름이 `passphrase`로 변경되었습니다.

<!-- ### Helpers -->
### Helpers

<a name="data-get-function"></a>
<!-- #### The `data_get` Helper & Iterable Objects -->
#### The `data_get` Helper & Iterable Objects

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 아주 낮음**

<!-- Previously, the `data_get` helper could be used to retrieve nested data on arrays and `Collection` instances; however, this helper can now retrieve nested data on all iterable objects. -->
`data_get` 헬퍼는 기존엔 배열과 `Collection` 인스턴스에서만 중첩 데이터 접근이 가능했습니다. 이제는 **모든 이터러블 객체**에서 중첩 데이터에 접근할 수 있습니다.

<a name="str-function"></a>
<!-- #### The `str` Helper -->
#### The `str` Helper

<!-- **Likelihood Of Impact: Very Low** -->
**영향 가능성: 아주 낮음**

<!-- Laravel 9.x now includes a global `str` [helper function](/docs/9.x/helpers#method-str). If you are defining a global `str` helper in your application, you should rename or remove it so that it does not conflict with Laravel's own `str` helper. -->
Laravel 9.x에 글로벌 `str` [helper function](/docs/9.x/helpers#method-str)가 추가되었습니다. 만약 애플리케이션에서 동일한 이름의 글로벌 `str` 헬퍼를 정의해두었다면, Laravel 자체의 `str` 헬퍼와 충돌하지 않도록 이름을 변경하거나 제거해야 합니다.

<a name="when-and-unless-methods"></a>
<!-- #### The `when` / `unless` Methods -->
#### The `when` / `unless` Methods

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- As you may know, `when` and `unless` methods are offered by various classes throughout the framework. These methods can be used to conditionally perform an action if the boolean value of the first argument to the method evaluates to `true` or `false`: -->
`when`과 `unless` 메서드는 프레임워크 전반 다양한 클래스에서 조건부 동작을 위해 제공됩니다. 이 메서드의 첫 번째 인수의 불리언 값이 `true` 또는 `false`일 때만 해당 함수를 실행합니다.

```php
$collection->when(true, function ($collection) {
    $collection->merge([1, 2, 3]);
});
```

<!-- Therefore, in previous releases of Laravel, passing a closure to the `when` or `unless` methods meant that the conditional operation would always execute, since a loose comparison against a closure object (or any other object) always evaluates to `true`. This often led to unexpected outcomes because developers expect the **result** of the closure to be used as the boolean value that determines if the conditional action executes. -->
따라서 기존 Laravel에서는 `when`이나 `unless` 메서드에 클로저를 전달하면, 클로저 객체(또는 다른 모든 객체)에 대한 느슨한 비교(loose comparison)가 항상 `true`로 평가되기 때문에 조건부 동작이 항상 실행되었습니다. 개발자들은 클로저의 **결과값**이 조건부 동작 실행 여부를 결정하는 불리언 값으로 사용되기를 기대했기 때문에, 이는 종종 예상치 못한 결과로 이어졌습니다.

<!-- So, in Laravel 9.x, any closures passed to the `when` or `unless` methods will be executed and the value returned by the closure will be considered the boolean value used by the `when` and `unless` methods: -->
그래서 Laravel 9.x에서는 `when` 또는 `unless` 메서드에 전달된 클로저가 실제로 실행되고, 그 반환값이 `when` 및 `unless` 메서드에서 사용되는 불리언 값으로 간주됩니다.

```php
$collection->when(function ($collection) {
    // This closure is executed...
    return false;
}, function ($collection) {
    // Not executed since first closure returned "false"...
    $collection->merge([1, 2, 3]);
});
```

<!-- ### HTTP Client -->
### HTTP Client

<a name="http-client-default-timeout"></a>
<!-- #### Default Timeout -->
#### Default Timeout

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- The [HTTP client](/docs/9.x/http-client) now has a default timeout of 30 seconds. In other words, if the server does not respond within 30 seconds, an exception will be thrown. Previously, no default timeout length was configured on the HTTP client, causing requests to sometimes "hang" indefinitely. -->
[HTTP client](/docs/9.x/http-client)에 기본 타임아웃이 **30초**로 설정되었습니다. 즉, 서버가 30초 내로 응답하지 않으면 예외가 발생합니다. 이전에는 별도 제한이 없어 요청이 무한정 "멈춤" 상태가 되는 경우가 있었습니다.

<!-- If you wish to specify a longer timeout for a given request, you may do so using the `timeout` method: -->
더 긴 타임아웃이 필요하다면 `timeout` 메서드로 개별 요청마다 지정 가능합니다.

```
$response = Http::timeout(120)->get(/* ... */);
```

<!-- #### HTTP Fake & Middleware -->
#### HTTP Fake & Middleware

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Previously, Laravel would not execute any provided Guzzle HTTP middleware when the [HTTP client](/docs/9.x/http-client) was "faked". However, in Laravel 9.x, Guzzle HTTP middleware will be executed even when the HTTP client is faked. -->
기존에는 [HTTP client](/docs/9.x/http-client)가 "faked"될 때 Guzzle HTTP 미들웨어가 실행되지 않았지만, 9.x에서는 **faked 상태에서도 Guzzle 미들웨어가 실행**됩니다.

<!-- #### HTTP Fake & Dependency Injection -->
#### HTTP Fake & Dependency Injection

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- In previous releases of Laravel, invoking the `Http::fake()` method would not affect instances of the `Illuminate\Http\Client\Factory` that were injected into class constructors. However, in Laravel 9.x, `Http::fake()` will ensure fake responses are returned by HTTP clients injected into other services via dependency injection. This behavior is more consistent with the behavior of other facades and fakes. -->
이전에는 `Http::fake()` 호출 후에도 생성자(inject) 등을 통해 주입된 `Illuminate\Http\Client\Factory` 인스턴스에는 영향을 주지 않았지만, Laravel 9.x에서는 `Http::fake()`가 **의존성 주입된 클라이언트에도 fake 응답이 동작**하도록 보장합니다. 이는 다른 파사드 및 fake 객체와 일관성을 맞춘 동작입니다.

<a name="symfony-mailer"></a>
<!-- ### Symfony Mailer -->
### Symfony Mailer

<!-- **Likelihood Of Impact: High** -->
**영향 가능성: 높음**

<!-- One of the largest changes in Laravel 9.x is the transition from SwiftMailer, which is no longer maintained as of December 2021, to Symfony Mailer. However, we have tried to make this transition as seamless as possible for your applications. That being said, please thoroughly review the list of changes below to ensure your application is fully compatible. -->
Laravel 9.x의 가장 큰 변화 중 하나는, 2021년 12월 이후로 유지보수가 중단된 SwiftMailer 대신 Symfony Mailer로 전환되었다는 점입니다. 이 변화는 최대한 사용자 입장에서 매끄럽게 진행되도록 노력했으나, 아래 내용을 꼼꼼히 확인하여 호환성 문제를 예방하시길 권장합니다.

<!-- #### Driver Prerequisites -->
#### Driver Prerequisites

<!-- To continue using the Mailgun transport, your application should require the `symfony/mailgun-mailer` and `symfony/http-client` Composer packages: -->
Mailgun 전송 방식을 계속 사용하려면 `symfony/mailgun-mailer`와 `symfony/http-client` Composer 패키지를 설치해야 합니다.

```shell
composer require symfony/mailgun-mailer symfony/http-client
```

<!-- The `wildbit/swiftmailer-postmark` Composer package should be removed from your application. Instead, your application should require the `symfony/postmark-mailer` and `symfony/http-client` Composer packages: -->
`wildbit/swiftmailer-postmark` Composer 패키지는 제거해야 하며, 대신 `symfony/postmark-mailer`와 `symfony/http-client` Composer 패키지를 설치해야 합니다.

```shell
composer require symfony/postmark-mailer symfony/http-client
```

<!-- #### Updated Return Types -->
#### Updated Return Types

<!-- The `send`, `html`, `raw`, and `plain` methods on `Illuminate\Mail\Mailer` no longer return `void`. Instead, an instance of `Illuminate\Mail\SentMessage` is returned. This object contains an instance of `Symfony\Component\Mailer\SentMessage` that is accessible via the `getSymfonySentMessage` method or by dynamically invoking methods on the object. -->
`Illuminate\Mail\Mailer`의 `send`, `html`, `raw`, `plain` 메서드는 이제 **`void`가 아니라 `Illuminate\Mail\SentMessage` 인스턴스**를 반환합니다. 이 객체에는 `getSymfonySentMessage` 메서드 또는 다이내믹 메서드로 접근할 수 있는 `Symfony\Component\Mailer\SentMessage` 인스턴스가 포함되어 있습니다.

<!-- #### Renamed "Swift" Methods -->
#### Renamed "Swift" Methods

<!-- Various SwiftMailer related methods, some of which were undocumented, have been renamed to their Symfony Mailer counterparts. For example, the `withSwiftMessage` method has been renamed to `withSymfonyMessage`: -->
SwiftMailer와 관련된 다양한 메서드들은 Symfony Mailer 네이밍으로 변경되었습니다. 예를 들어, `withSwiftMessage`는 `withSymfonyMessage`로 이름이 바뀌었습니다.

```
// Laravel 8.x...
$this->withSwiftMessage(function ($message) {
    $message->getHeaders()->addTextHeader(
        'Custom-Header', 'Header Value'
    );
});

// Laravel 9.x...
use Symfony\Component\Mime\Email;

$this->withSymfonyMessage(function (Email $message) {
    $message->getHeaders()->addTextHeader(
        'Custom-Header', 'Header Value'
    );
});
```

> [!WARNING]
> 모든 가능한 `Symfony\Component\Mime\Email` 객체의 인터랙션을 위해 [Symfony Mailer documentation](https://symfony.com/doc/6.0/mailer.html#creating-sending-messages)를 반드시 확인하세요.

<!-- The list below contains a more thorough overview of renamed methods. Many of these methods are low-level methods used to interact with SwiftMailer / Symfony Mailer directly, so may not be commonly used within most Laravel applications: -->
아래는 이름이 변경된 주요 메서드 목록입니다. 대부분 SwiftMailer 혹은 Symfony Mailer와 직접 연동하는 저수준 메서드이므로, 일반적인 Laravel 애플리케이션은 크게 영향 없을 수 있습니다.

```
Message::getSwiftMessage();
Message::getSymfonyMessage();

Mailable::withSwiftMessage($callback);
Mailable::withSymfonyMessage($callback);

MailMessage::withSwiftMessage($callback);
MailMessage::withSymfonyMessage($callback);

Mailer::getSwiftMailer();
Mailer::getSymfonyTransport();

Mailer::setSwiftMailer($swift);
Mailer::setSymfonyTransport(TransportInterface $transport);

MailManager::createTransport($config);
MailManager::createSymfonyTransport($config);
```

<!-- #### Proxied `Illuminate\Mail\Message` Methods -->
#### Proxied `Illuminate\Mail\Message` Methods

<!-- The `Illuminate\Mail\Message` typically proxied missing methods to the underlying `Swift_Message` instance. However, missing methods are now proxied to an instance of `Symfony\Component\Mime\Email` instead. So, any code that was previously relying on missing methods to be proxied to SwiftMailer should be updated to their corresponding Symfony Mailer counterparts. -->
이전에는 `Illuminate\Mail\Message` 클래스가 정의되지 않은(missing) 메서드를 내부의 `Swift_Message` 인스턴스에 프락시 하였으나, 이제는 정의되지 않은 메서드를 `Symfony\Component\Mime\Email` 인스턴스에 프락시합니다. 따라서 이전에 정의되지 않은 메서드가 SwiftMailer로 프락시되는 방식에 의존하던 코드가 있다면, 그에 대응하는 Symfony Mailer 메서드로 수정해야 합니다.

<!-- Again, many applications may not be interacting with these methods, as they are not documented within the Laravel documentation: -->
다시 말하지만, 이 메서드들은 Laravel 공식 문서에 기재되어 있지 않으므로 많은 애플리케이션에서는 사용하지 않을 수 있습니다.

```
// Laravel 8.x...
$message
    ->setFrom('taylor@laravel.com')
    ->setTo('example@example.org')
    ->setSubject('Order Shipped')
    ->setBody('<h1>HTML</h1>', 'text/html')
    ->addPart('Plain Text', 'text/plain');

// Laravel 9.x...
$message
    ->from('taylor@laravel.com')
    ->to('example@example.org')
    ->subject('Order Shipped')
    ->html('<h1>HTML</h1>')
    ->text('Plain Text');
```

<!-- #### Generated Messages IDs -->
#### Generated Messages IDs

<!-- SwiftMailer offered the ability to define a custom domain to include in generated Message IDs via the `mime.idgenerator.idright` configuration option. This is not supported by Symfony Mailer. Instead, Symfony Mailer will automatically generate a Message ID based on the sender. -->
SwiftMailer는 생성되는 메시지 ID에 사용되는 도메인을 설정할 수 있도록 `mime.idgenerator.idright` 옵션을 제공했으나, Symfony Mailer에서는 해당 기능을 지원하지 않습니다. 대신, 메시지 ID는 자동으로 **발신자(sender)** 정보를 기반으로 생성됩니다.

<!-- #### `MessageSent` Event Changes -->
#### `MessageSent` Event Changes

<!-- The `message` property of the `Illuminate\Mail\Events\MessageSent` event now contains an instance of `Symfony\Component\Mime\Email` instead of an instance of `Swift_Message`. This message represents the email **before** it is sent. -->
`Illuminate\Mail\Events\MessageSent` 이벤트의 `message` 속성에는 이제 `Swift_Message` 대신 **`Symfony\Component\Mime\Email` 인스턴스**가 저장됩니다. 이 객체는 메일 전송 **이전**의 이메일을 나타냅니다.

<!-- Additionally, a new `sent` property has been added to the `MessageSent` event. This property contains an instance of `Illuminate\Mail\SentMessage` and contains information about the sent email, such as the message ID. -->
또한, `MessageSent` 이벤트에 새로 추가된 `sent` 속성에는 `Illuminate\Mail\SentMessage` 인스턴스가 저장되어, 보낸 이메일의 Message ID 등 추가 정보도 확인할 수 있습니다.

<!-- #### Forced Reconnections -->
#### Forced Reconnections

<!-- It is no longer possible to force a transport reconnection (for example when the mailer is running via a daemon process). Instead, Symfony Mailer will attempt to reconnect to the transport automatically and throw an exception if the reconnection fails. -->
메일러가 데몬 프로세스 등에서 동작할 때 **트랜스포트의 강제 재연결**이 더 이상 불가능합니다. 대신, Symfony Mailer가 자동으로 재연결을 시도하고, 실패하면 예외를 발생시킵니다.

<!-- #### SMTP Stream Options -->
#### SMTP Stream Options

<!-- Defining stream options for the SMTP transport is no longer supported. Instead, you must define the relevant options directly within the configuration if they are supported. For example, to disable TLS peer verification: -->
SMTP 트랜스포트의 스트림 관련 옵션 설정이 더 이상 지원되지 않습니다. 지원되는 옵션만 설정 파일에 직접 명시해주어야 합니다. 예를 들어, TLS 피어 검증 비활성화는 아래와 같이 설정할 수 있습니다.

```
'smtp' => [
    // Laravel 8.x...
    'stream' => [
        'ssl' => [
            'verify_peer' => false,
        ],
    ],

    // Laravel 9.x...
    'verify_peer' => false,
],
```

<!-- To learn more about the available configuration options, please review the [Symfony Mailer documentation](https://symfony.com/doc/6.0/mailer.html#transport-setup). -->
자세한 옵션은 [Symfony Mailer documentation](https://symfony.com/doc/6.0/mailer.html#transport-setup)를 참고하세요.

> [!WARNING]
> 위 예시(SSL 검증 비활성화)는 보안상 안전하지 않으므로, "중간자 공격" 위험이 있으니 실사용 시 권장하지 않습니다.

<!-- #### SMTP `auth_mode` -->
#### SMTP `auth_mode`

<!-- Defining the SMTP `auth_mode` in the `mail` configuration file is no longer required. The authentication mode will be automatically negotiated between Symfony Mailer and the SMTP server. -->
`mail` 설정 파일에서 SMTP의 `auth_mode`를 명시적으로 지정할 필요가 없어졌습니다. 인증 방식은 Symfony Mailer가 SMTP 서버와 자동으로 협상합니다.

<!-- #### Failed Recipients -->
#### Failed Recipients

<!-- It is no longer possible to retrieve a list of failed recipients after sending a message. Instead, a `Symfony\Component\Mailer\Exception\TransportExceptionInterface` exception will be thrown if a message fails to send. Instead of relying on retrieving invalid email addresses after sending a message, we recommend that you validate email addresses before sending the message instead. -->
이제 메일 전송 후 실패한 수신자 목록을 조회할 수 없습니다. 만약 메시지 전송이 실패하면 `Symfony\Component\Mailer\Exception\TransportExceptionInterface` 예외가 발생합니다. 실패한 이메일을 확인하려면, 메일 전송 전 수신자 이메일 주소의 유효성을 반드시 검증하는 것을 권장합니다.

<!-- ### Packages -->
### Packages

<a name="the-lang-directory"></a>
<!-- #### The `lang` Directory -->
#### The `lang` Directory

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- In new Laravel applications, the `resources/lang` directory is now located in the root project directory (`lang`). If your package is publishing language files to this directory, you should ensure that your package is publishing to `app()->langPath()` instead of a hard-coded path. -->
새로운 Laravel 애플리케이션에서는 `resources/lang` 디렉터리가 루트 프로젝트 디렉터리(`lang`)로 옮겨졌습니다. 패키지에서 언어 파일을 배포하는 경우, 하드코딩된 경로 대신 반드시 `app()->langPath()` 메서드를 사용해 새로운 경로에 파일을 배포하도록 수정해야 합니다.

<a name="queue"></a>
<!-- ### Queue -->
### Queue

<a name="the-opis-closure-library"></a>
<!-- #### The `opis/closure` Library -->
#### The `opis/closure` Library

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- Laravel's dependency on `opis/closure` has been replaced by `laravel/serializable-closure`. This should not cause any breaking change in your application unless you are interacting with the `opis/closure` library directly. In addition, the previously deprecated `Illuminate\Queue\SerializableClosureFactory` and `Illuminate\Queue\SerializableClosure` classes have been removed. If you are interacting with `opis/closure` library directly or using any of the removed classes, you may use [Laravel Serializable Closure](https://github.com/laravel/serializable-closure) instead. -->
Laravel의 `opis/closure` 의존성이 `laravel/serializable-closure`로 대체되었습니다. 애플리케이션에서 `opis/closure` 라이브러리를 직접 다루지 않는 한 기존 코드를 그대로 사용하는 대부분의 경우 특별한 문제는 없습니다. 단, 직접 `opis/closure` 라이브러리를 직접적으로 사용하거나, 기존에 deprecated된 `Illuminate\Queue\SerializableClosureFactory` 또는 `Illuminate\Queue\SerializableClosure` 클래스를 사용 중이라면, [Laravel Serializable Closure](https://github.com/laravel/serializable-closure)로 전환해 주셔야 합니다.

<!-- #### The Failed Job Provider `flush` Method -->
#### The Failed Job Provider `flush` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `flush` method defined by the `Illuminate\Queue\Failed\FailedJobProviderInterface` interface now accepts an `$hours` argument which determines how old a failed job must be (in hours) before it is flushed by the `queue:flush` command. If you are manually implementing the `FailedJobProviderInterface` you should ensure that your implementation is updated to reflect this new argument: -->
`Illuminate\Queue\Failed\FailedJobProviderInterface` 인터페이스의 `flush` 메서드는 이제 `$hours` 인수를 받아, 실패한 작업을 `queue:flush` 명령으로 삭제할 때 해당 작업이 **몇 시간 이상 된 것인지(시간 단위)**를 지정할 수 있습니다. `FailedJobProviderInterface`를 직접 구현 중이라면 아래와 같이 시그니처를 변경해 주세요.

```php
public function flush($hours = null);
```

<!-- ### Session -->
### Session

<!-- #### The `getSession` Method -->
#### The `getSession` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `Symfony\Component\HttpFoundaton\Request` class that is extended by Laravel's own `Illuminate\Http\Request` class offers a `getSession` method to get the current session storage handler. This method is not documented by Laravel as most Laravel applications interact with the session through Laravel's own `session` method. -->
Laravel의 `Illuminate\Http\Request` 클래스가 확장한 `Symfony\Component\HttpFoundaton\Request` 클래스에는 현재 세션 스토리지를 가져오는 `getSession` 메서드가 존재합니다. 이는 Laravel 공식 문서에는 언급되지 않으며, 대부분의 사용자는 Laravel 자체의 `session` 메서드를 사용할 것입니다.

<!-- The `getSession` method previously returned an instance of `Illuminate\Session\Store` or `null`; however, due to the Symfony 6.x release enforcing a return type of `Symfony\Component\HttpFoundation\Session\SessionInterface`, the `getSession` now correctly returns a `SessionInterface` implementation or throws an `\Symfony\Component\HttpFoundation\Exception\SessionNotFoundException` exception when no session is available. -->
이제 `getSession` 메서드는 `Illuminate\Session\Store` 또는 `null`을 반환하는 대신, **`Symfony\Component\HttpFoundation\Session\SessionInterface` 구현체**를 반환하거나, 더 정확히는 `getSession`이 `SessionInterface` 구현체를 반환합니다. 세션이 없을 경우에는 `\Symfony\Component\HttpFoundation\Exception\SessionNotFoundException` 예외를 던집니다.

<!-- ### Testing -->
### Testing

<a name="the-assert-deleted-method"></a>
<!-- #### The `assertDeleted` Method -->
#### The `assertDeleted` Method

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- All calls to the `assertDeleted` method should be updated to `assertModelMissing`. -->
모든 `assertDeleted` 호출을 **`assertModelMissing`으로 바꿔야** 합니다.

<!-- ### Trusted Proxies -->
### Trusted Proxies

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- If you are upgrading your Laravel 8 project to Laravel 9 by importing your existing application code into a totally new Laravel 9 application skeleton, you may need to update your application's "trusted proxy" middleware. -->
Laravel 8 프로젝트의 코드를 새 Laravel 9 애플리케이션 스켈레톤으로 이전하는 경우, **신뢰된 프록시 미들웨어**를 업데이트해야 할 수 있습니다.

<!-- Within your `app/Http/Middleware/TrustProxies.php` file, update `use Fideloper\Proxy\TrustProxies as Middleware` to `use Illuminate\Http\Middleware\TrustProxies as Middleware`. -->
`app/Http/Middleware/TrustProxies.php` 파일에서 `use Fideloper\Proxy\TrustProxies as Middleware`를 `use Illuminate\Http\Middleware\TrustProxies as Middleware`로 변경하세요.

<!-- Next, within `app/Http/Middleware/TrustProxies.php`, you should update the `$headers` property definition: -->
다음으로, `app/Http/Middleware/TrustProxies.php`에서 `$headers` 프로퍼티 정의를 아래와 같이 수정해야 합니다.

```php
// Before...
protected $headers = Request::HEADER_X_FORWARDED_ALL;

// After...
protected $headers =
    Request::HEADER_X_FORWARDED_FOR |
    Request::HEADER_X_FORWARDED_HOST |
    Request::HEADER_X_FORWARDED_PORT |
    Request::HEADER_X_FORWARDED_PROTO |
    Request::HEADER_X_FORWARDED_AWS_ELB;
```

<!-- Finally, you can remove the `fideloper/proxy` Composer dependency from your application: -->
마지막으로, 아래 명령어로 `fideloper/proxy` Composer 의존성을 제거할 수 있습니다.

```shell
composer remove fideloper/proxy
```

<!-- ### Validation -->
### Validation

<!-- #### Form Request `validated` Method -->
#### Form Request `validated` Method

<!-- **Likelihood Of Impact: Low** -->
**영향 가능성: 낮음**

<!-- The `validated` method offered by form requests now accepts `$key` and `$default` arguments. If you are manually overwriting the definition of this method, you should update your method's signature to reflect these new arguments: -->
폼 리퀘스트에서 제공하는 `validated` 메서드는 이제 `$key`, `$default` 인수를 받을 수 있게 되었습니다. 직접 오버라이딩하는 경우 시그니처를 아래와 같이 수정해야 합니다.

```php
public function validated($key = null, $default = null)
```

<a name="the-password-rule"></a>
<!-- #### The `password` Rule -->
#### The `password` Rule

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- The `password` rule, which validates that the given input value matches the authenticated user's current password, has been renamed to `current_password`. -->
입력값이 현재 인증된 사용자의 비밀번호와 일치하는지 검사하는 `password` 규칙의 이름이 **`current_password`**로 변경되었습니다.

<a name="unvalidated-array-keys"></a>
<!-- #### Unvalidated Array Keys -->
#### Unvalidated Array Keys

<!-- **Likelihood Of Impact: Medium** -->
**영향 가능성: 중간**

<!-- In previous releases of Laravel, you were required to manually instruct Laravel's validator to exclude unvalidated array keys from the "validated" data it returns, especially in combination with an `array` rule that does not specify a list of allowed keys. -->
기존 Laravel에서는 validator가 반환하는 "validated" 데이터에서 검증되지 않은 배열 키를 제외하도록 직접 지시해야 했으며, 특히 허용 키 목록을 지정하지 않은 `array` 규칙과 함께 사용할 때 그러했습니다.

<!-- However, in Laravel 9.x, unvalidated array keys are always excluded from the "validated" data even when no allowed keys have been specified via the `array` rule. Typically, this behavior is the most expected behavior and the previous `excludeUnvalidatedArrayKeys` method was only added to Laravel 8.x as a temporary measure in order to preserve backwards compatibility. -->
그러나 Laravel 9.x에서는 `array` 규칙으로 허용 키를 지정하지 않은 경우에도 검증되지 않은 배열 키는 항상 "validated" 데이터에서 제외됩니다. 일반적으로 이 동작이 가장 기대되는 동작이며, 이전의 `excludeUnvalidatedArrayKeys` 메서드는 하위 호환성을 유지하기 위한 임시 조치로 Laravel 8.x에만 추가되었던 것입니다.

<!-- Although it is not recommended, you may opt-in to the previous Laravel 8.x behavior by invoking a new `includeUnvalidatedArrayKeys` method within the `boot` method of one of your application's service providers: -->
권장하지는 않지만, 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드에서 새로운 `includeUnvalidatedArrayKeys` 메서드를 호출하면 이전 Laravel 8.x 동작 방식을 선택적으로 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

/**
 * Register any application services.
 *
 * @return void
 */
public function boot()
{
    Validator::includeUnvalidatedArrayKeys();
}
```

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/8.x...9.x) and choose which updates are important to you. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel)의 변경점도 확인해보시길 바랍니다. 이들 중 다수는 필수 항목은 아니지만, 필요에 따라 애플리케이션의 설정 파일이나 주석 등도 동기화할 수 있습니다. [GitHub comparison tool](https://github.com/laravel/laravel/compare/8.x...9.x)를 이용하면 어떤 변경 사항이 있는지 한눈에 비교할 수 있습니다.
