<!-- # Upgrade Guide -->
# Upgrade Guide

- [Upgrading to 10.0 from 9.x](#upgrade-10.0)

<a name="high-impact-changes"></a>
<!-- ## High Impact Changes -->
## High Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Updating Dependencies](#updating-dependencies)
- [Updating Minimum Stability](#updating-minimum-stability)

<!-- </div> -->
</div>

<a name="medium-impact-changes"></a>
<!-- ## Medium Impact Changes -->
## Medium Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Database Expressions](#database-expressions)
- [Model "Dates" Property](#model-dates-property)
- [Monolog 3](#monolog-3)
- [Redis Cache Tags](#redis-cache-tags)
- [Service Mocking](#service-mocking)
- [The Language Directory](#language-directory)

<!-- </div> -->
</div>

<a name="low-impact-changes"></a>
<!-- ## Low Impact Changes -->
## Low Impact Changes

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [Closure Validation Rule Messages](#closure-validation-rule-messages)
- [Form Request `after` Method](#form-request-after-method)
- [Public Path Binding](#public-path-binding)
- [Query Exception Constructor](#query-exception-constructor)
- [Rate Limiter Return Values](#rate-limiter-return-values)
- [The `Redirect::home` Method](#redirect-home)
- [The `Bus::dispatchNow` Method](#dispatch-now)
- [The `registerPolicies` Method](#register-policies)
- [ULID Columns](#ulid-columns)

<!-- </div> -->
</div>

<a name="upgrade-10.0"></a>
<!-- ## Upgrading to 10.0 from 9.x -->
## Upgrading to 10.0 from 9.x

<a name="estimated-upgrade-time-??-minutes"></a>
<!-- #### Estimated Upgrade Time: 10 Minutes -->
#### Estimated Upgrade Time: 10 Minutes

> [!NOTE]
> 가능한 모든 주요 변경사항을 문서화하려 노력했습니다. 다만, 일부 변경사항은 프레임워크의 드물게 쓰이는 부분에 해당하므로 실제로 여러분의 애플리케이션에 영향을 주는 경우는 일부일 수 있습니다. 시간을 절약하고 싶으시다면 [Laravel Shift](https://laravelshift.com/)를 이용해 애플리케이션 업그레이드를 자동화하실 수 있습니다.

<a name="updating-dependencies"></a>
<!-- ### Updating Dependencies -->
### Updating Dependencies

<!-- **Likelihood Of Impact: High** -->
**영향도: 높음**

<!-- #### PHP 8.1.0 Required -->
#### PHP 8.1.0 Required

<!-- Laravel now requires PHP 8.1.0 or greater. -->
이제 Laravel은 PHP 8.1.0 이상이 필요합니다.

<!-- #### Composer 2.2.0 Required -->
#### Composer 2.2.0 Required

<!-- Laravel now requires [Composer](https://getcomposer.org) 2.2.0 or greater. -->
이제 Laravel은 [Composer](https://getcomposer.org) 2.2.0 이상을 요구합니다.

<!-- #### Composer Dependencies -->
#### Composer Dependencies

<!-- You should update the following dependencies in your application's `composer.json` file: -->
애플리케이션의 `composer.json` 파일에서 아래 의존성들을 업데이트해야 합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `laravel/framework` to `^10.0`
- `laravel/sanctum` to `^3.2`
- `doctrine/dbal` to `^3.0`
- `spatie/laravel-ignition` to `^2.0`
- `laravel/passport` to `^11.0` ([Upgrade Guide](https://github.com/laravel/passport/blob/11.x/UPGRADE.md))
- `laravel/ui` to `^4.0`
-->
- `laravel/framework`를 `^10.0`으로
- `laravel/sanctum`을 `^3.2`로
- `doctrine/dbal`을 `^3.0`으로
- `spatie/laravel-ignition`을 `^2.0`으로
- `laravel/passport`를 `^11.0`으로 ([Upgrade Guide](https://github.com/laravel/passport/blob/11.x/UPGRADE.md) 참고)
- `laravel/ui`를 `^4.0`으로

<!-- </div> -->
</div>

<!-- If you are upgrading to Sanctum 3.x from the 2.x release series, please consult the [Sanctum upgrade guide](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md). -->
만약 Sanctum 2.x에서 3.x로 업그레이드하시는 경우, [Sanctum upgrade guide](https://github.com/laravel/sanctum/blob/3.x/UPGRADE.md)를 반드시 참고하시기 바랍니다.

<!-- Furthermore, if you wish to use [PHPUnit 10](https://phpunit.de/announcements/phpunit-10.html), you should delete the `processUncoveredFiles` attribute from the `<coverage>` section of your application's `phpunit.xml` configuration file. Then, update the following dependencies in your application's `composer.json` file: -->
또한, [PHPUnit 10](https://phpunit.de/announcements/phpunit-10.html)을 사용하고 싶은 경우, 애플리케이션의 `phpunit.xml` 설정 파일에서 `<coverage>` 섹션의 `processUncoveredFiles` 속성을 삭제해야 합니다. 이후, 다음 의존성도 `composer.json`에서 업데이트해주시기 바랍니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- `nunomaduro/collision` to `^7.0`
- `phpunit/phpunit` to `^10.0`
-->
- `nunomaduro/collision`을 `^7.0`으로
- `phpunit/phpunit`을 `^10.0`으로

<!-- </div> -->
</div>

<!-- Finally, examine any other third-party packages consumed by your application and verify you are using the proper version for Laravel 10 support. -->
그리고, 애플리케이션에서 사용하는 기타 서드파티 패키지들도 Laravel 10을 지원하는 버전을 사용하고 있는지 반드시 확인해야 합니다.

<a name="updating-minimum-stability"></a>
<!-- #### Minimum Stability -->
#### Minimum Stability

<!-- You should update the `minimum-stability` setting in your application's `composer.json` file to `stable`. Or, since the default value of `minimum-stability` is `stable`, you may delete this setting from your application's `composer.json` file: -->
애플리케이션의 `composer.json` 파일 내 `minimum-stability` 설정값을 `stable`로 변경해야 합니다. 또는, `minimum-stability`의 기본값이 `stable`이므로 이 설정을 애플리케이션의 `composer.json` 파일에서 삭제해도 무방합니다.

```json
"minimum-stability": "stable",
```

<!-- ### Application -->
### Application

<a name="public-path-binding"></a>
<!-- #### Public Path Binding -->
#### Public Path Binding

<!-- **Likelihood Of Impact: Low** -->
**영향도: 낮음**

<!-- If your application is customizing its "public path" by binding `path.public` into the container, you should instead update your code to invoke the `usePublicPath` method offered by the `Illuminate\Foundation\Application` object: -->
애플리케이션에서 `path.public` 을 컨테이너에 바인딩하여 "public 경로"를 커스터마이즈하고 있다면, 이제는 `Illuminate\Foundation\Application` 객체에서 제공하는 `usePublicPath` 메서드를 사용하는 방식으로 코드를 수정해야 합니다.

```php
app()->usePublicPath(__DIR__.'/public');
```

<!-- ### Authorization -->
### Authorization

<a name="register-policies"></a>
<!-- ### The `registerPolicies` Method -->
### The `registerPolicies` Method

<!-- **Likelihood Of Impact: Low** -->
**영향도: 낮음**

<!-- The `registerPolicies` method of the `AuthServiceProvider` is now invoked automatically by the framework. Therefore, you may remove the call to this method from the `boot` method of your application's `AuthServiceProvider`. -->
`AuthServiceProvider`의 `registerPolicies` 메서드는 이제 프레임워크에서 자동으로 호출됩니다. 따라서, 여러분의 애플리케이션의 `AuthServiceProvider`의 `boot` 메서드에서 해당 메서드 호출을 제거해도 됩니다.

<!-- ### Cache -->
### Cache

<a name="redis-cache-tags"></a>
<!-- #### Redis Cache Tags -->
#### Redis Cache Tags

<!-- **Likelihood Of Impact: Medium** -->
**영향도: 중간**

<!-- Usage of `Cache::tags()` is only recommended for applications using Memcached. If you are using Redis as your application's cache driver, you should consider moving to Memcached or upgrade your application to Laravel [12.30.0](https://github.com/laravel/framework/pull/57098). -->
`Cache::tags()` 기능은 Memcached를 사용하는 애플리케이션에서만 권장합니다. 애플리케이션이 Redis를 캐시 드라이버로 사용하고 있다면, Memcached로의 이전이나 Laravel [12.30.0](https://github.com/laravel/framework/pull/57098) 버전으로 업그레이드하는 방안을 고려해야 합니다.

<!-- ### Database -->
### Database

<a name="database-expressions"></a>
<!-- #### Database Expressions -->
#### Database Expressions

<!-- **Likelihood Of Impact: Medium** -->
**영향도: 중간**

<!-- Database "expressions" (typically generated via `DB::raw`) have been rewritten in Laravel 10.x to offer additional functionality in the future. Notably, the grammar's raw string value must now be retrieved via the expression's `getValue(Grammar $grammar)` method. Casting an expression to a string using `(string)` is no longer supported. -->
데이터베이스의 "표현식(Expressions)"(주로 `DB::raw`로 생성됨)은 향후 더 많은 기능을 제공하기 위해 Laravel 10.x에서 내부적으로 다시 설계되었습니다. 중요한 변경점으로, 이제 표현식의 원시 문자열 값을 얻으려면 해당 표현식의 `getValue(Grammar $grammar)` 메서드를 호출해야 합니다. `(string)` casting으로 문자열을 얻는 방식은 더 이상 지원하지 않습니다.

<!-- **Typically, this does not affect end-user applications**; however, if your application is manually casting database expressions to strings using `(string)` or invoking the `__toString` method on the expression directly, you should update your code to invoke the `getValue` method instead: -->
**이 변경은 일반적인 사용 환경에는 보통 영향을 주지 않습니다.** 다만, 애플리케이션 코드에서 데이터베이스 표현식을 `(string)` 으로 직접 casting하거나, `__toString` 메서드를 직접 호출하고 있다면, 반드시 `getValue` 메서드를 사용하도록 수정해야 합니다.

```php
use Illuminate\Support\Facades\DB;

$expression = DB::raw('select 1');

$string = $expression->getValue(DB::connection()->getQueryGrammar());
```

<a name="query-exception-constructor"></a>
<!-- #### Query Exception Constructor -->
#### Query Exception Constructor

<!-- **Likelihood Of Impact: Very Low** -->
**영향도: 매우 낮음**

<!-- The `Illuminate\Database\QueryException` constructor now accepts a string connection name as its first argument. If your application is manually throwing this exception, you should adjust your code accordingly. -->
`Illuminate\Database\QueryException` 생성자는 이제 첫 번째 인수로 문자열 타입의 커넥션 이름을 받습니다. 만약 해당 예외를 직접 발생시키는 경우, 이 변경에 맞추어 코드를 수정해야 합니다.

<a name="ulid-columns"></a>
<!-- #### ULID Columns -->
#### ULID Columns

<!-- **Likelihood Of Impact: Low** -->
**영향도: 낮음**

<!-- When migrations invoke the `ulid` method without any arguments, the column will now be named `ulid`. In previous releases of Laravel, invoking this method without any arguments created a column erroneously named `uuid`: -->
마이그레이션에서 `ulid` 메서드를 인수 없이 호출할 경우, 이제 컬럼명이 `ulid`로 지정됩니다. 이전 Laravel 버전에서는 인수 없이 호출 시 컬럼명이 잘못하여 `uuid`로 지정되었습니다.

```
$table->ulid();
```

<!-- To explicitly specify a column name when invoking the `ulid` method, you may pass the column name to the method: -->
`ulid` 메서드 호출 시 명시적으로 컬럼명을 지정하고 싶다면, 인수로 컬럼명을 전달하면 됩니다.

```
$table->ulid('ulid');
```

<!-- ### Eloquent -->
### Eloquent

<a name="model-dates-property"></a>
<!-- #### Model "Dates" Property -->
#### Model "Dates" Property

<!-- **Likelihood Of Impact: Medium** -->
**영향도: 중간**

<!-- The Eloquent model's deprecated `$dates` property has been removed. Your application should now use the `$casts` property: -->
Eloquent 모델에서 사용되던 `$dates` 속성은 더 이상 지원되지 않습니다. 이제는 `$casts` 속성을 사용해야 합니다.

```php
protected $casts = [
    'deployed_at' => 'datetime',
];
```

<!-- ### Localization -->
### Localization

<a name="language-directory"></a>
<!-- #### The Language Directory -->
#### The Language Directory

<!-- **Likelihood Of Impact: None** -->
**영향도: 없음**

<!-- Though not relevant to existing applications, the Laravel application skeleton no longer contains the `lang` directory by default. Instead, when writing new Laravel applications, it may be published using the `lang:publish` Artisan command: -->
기존 애플리케이션에는 해당되지 않지만, Laravel 애플리케이션 스켈레톤에는 이제 기본적으로 `lang` 디렉터리가 포함되어 있지 않습니다. 신규 Laravel 프로젝트에서는 필요시 `lang:publish` 아티즌 명령어로 해당 디렉터리를 생성할 수 있습니다.

```shell
php artisan lang:publish
```

<!-- ### Logging -->
### Logging

<a name="monolog-3"></a>
<!-- #### Monolog 3 -->
#### Monolog 3

<!-- **Likelihood Of Impact: Medium** -->
**영향도: 중간**

<!-- Laravel's Monolog dependency has been updated to Monolog 3.x. If you are directly interacting with Monolog within your application, you should review Monolog's [upgrade guide](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md). -->
Laravel의 Monolog 의존성은 Monolog 3.x로 업데이트되었습니다. 애플리케이션 코드에서 Monolog을 직접 사용하는 경우, Monolog의 [upgrade guide](https://github.com/Seldaek/monolog/blob/main/UPGRADE.md)를 반드시 참고하시기 바랍니다.

<!-- If you are using third-party logging services such as BugSnag or Rollbar, you may need to upgrade those third-party packages to a version that supports Monolog 3.x and Laravel 10.x. -->
버그스냅(BugSnag)이나 롤바(Rollbar)처럼 서드파티 로깅 서비스를 사용하는 경우, 해당 패키지 역시 Monolog 3.x 및 Laravel 10.x를 지원하는 버전으로 업그레이드해야 할 수 있습니다.

<!-- ### Queues -->
### Queues

<a name="dispatch-now"></a>
<!-- #### The `Bus::dispatchNow` Method -->
#### The `Bus::dispatchNow` Method

<!-- **Likelihood Of Impact: Low** -->
**영향도: 낮음**

<!-- The deprecated `Bus::dispatchNow` and `dispatch_now` methods have been removed. Instead, your application should use the `Bus::dispatchSync` and `dispatch_sync` methods, respectively. -->
더 이상 지원되지 않는 `Bus::dispatchNow` 및 `dispatch_now` 메서드는 삭제되었습니다. 대신 각각 `Bus::dispatchSync` 및 `dispatch_sync` 메서드를 사용해야 합니다.

<a name="dispatch-return"></a>
<!-- #### The `dispatch()` Helper Return Value -->
#### The `dispatch()` Helper Return Value

<!-- **Likelihood Of Impact: Low** -->
**영향도: 낮음**

<!-- Invoking `dispatch` with a class that does not implement `Illuminate\Contracts\Queue` would previously return the result of the class's `handle` method. However, this will now return an `Illuminate\Foundation\Bus\PendingBatch` instance. You may use `dispatch_sync()` to replicate the previous behavior. -->
이전에는 `Illuminate\Contracts\Queue`를 구현하지 않은 클래스를 `dispatch`할 때 해당 클래스의 `handle` 메서드 반환값을 그대로 반환받았습니다. 이제는 `Illuminate\Foundation\Bus\PendingBatch` 인스턴스를 반환합니다. 이전과 같이 동기 방식의 반환값을 얻고 싶다면, `dispatch_sync()`를 사용해야 합니다.

<!-- ### Routing -->
### Routing

<a name="middleware-aliases"></a>
<!-- #### Middleware Aliases -->
#### Middleware Aliases

<!-- **Likelihood Of Impact: Optional** -->
**영향도: 선택적 적용**

<!-- In new Laravel applications, the `$routeMiddleware` property of the `App\Http\Kernel` class has been renamed to `$middlewareAliases` to better reflect its purpose. You are welcome to rename this property in your existing applications; however, it is not required. -->
신규 Laravel 애플리케이션에서는 `App\Http\Kernel` 클래스의 `$routeMiddleware` 속성이 `$middlewareAliases`로 이름이 변경되었습니다. 기존 애플리케이션에서 해당 속성명을 변경해도 되고, 변경하지 않아도 무방합니다.

<a name="rate-limiter-return-values"></a>
<!-- #### Rate Limiter Return Values -->
#### Rate Limiter Return Values

<!-- **Likelihood Of Impact: Low** -->
**영향도: 낮음**

<!-- When invoking the `RateLimiter::attempt` method, the value returned by the provided closure will now be returned by the method. If nothing or `null` is returned, the `attempt` method will return `true`: -->
`RateLimiter::attempt` 메서드를 호출할 때, 클로저에서 반환한 값이 이제 메서드의 반환값으로 그대로 사용됩니다. 아무것도 반환하지 않거나 `null`을 반환하면, `attempt` 메서드는 `true`를 반환합니다.

```php
$value = RateLimiter::attempt('key', 10, fn () => ['example'], 1);

$value; // ['example']
```

<a name="redirect-home"></a>
<!-- #### The `Redirect::home` Method -->
#### The `Redirect::home` Method

<!-- **Likelihood Of Impact: Very Low** -->
**영향도: 매우 낮음**

<!-- The deprecated `Redirect::home` method has been removed. Instead, your application should redirect to an explicitly named route: -->
더 이상 지원되지 않는 `Redirect::home` 메서드는 삭제되었습니다. 대신, 명시적으로 이름이 지정된 라우트로 리다이렉트 하시면 됩니다.

```php
return Redirect::route('home');
```

<!-- ### Testing -->
### Testing

<a name="service-mocking"></a>
<!-- #### Service Mocking -->
#### Service Mocking

<!-- **Likelihood Of Impact: Medium** -->
**영향도: 중간**

<!-- The deprecated `MocksApplicationServices` trait has been removed from the framework. This trait provided testing methods such as `expectsEvents`, `expectsJobs`, and `expectsNotifications`. -->
프레임워크에서 `MocksApplicationServices` 트레이트는 더 이상 제공되지 않습니다. 이 트레이트는 `expectsEvents`, `expectsJobs`, `expectsNotifications`와 같은 테스트 용도 메서드를 제공했습니다.

<!-- If your application uses these methods, we recommend you transition to `Event::fake`, `Bus::fake`, and `Notification::fake`, respectively. You can learn more about mocking via fakes in the corresponding documentation for the component you are attempting to fake. -->
이제는 각각 `Event::fake`, `Bus::fake`, `Notification::fake`를 사용하기를 권장합니다. 각 컴포넌트의 문서에서 fakes를 활용한 모킹 방법에 대해 더 확인할 수 있습니다.

<!-- ### Validation -->
### Validation

<a name="closure-validation-rule-messages"></a>
<!-- #### Closure Validation Rule Messages -->
#### Closure Validation Rule Messages

<!-- **Likelihood Of Impact: Very Low** -->
**영향도: 매우 낮음**

<!-- When writing closure based custom validation rules, invoking the `$fail` callback more than once will now append the messages to an array instead of overwriting the previous message. Typically, this will not affect your application. -->
클로저 기반의 커스텀 유효성 검증 규칙에서 `$fail` 콜백을 여러 번 호출할 경우, 이제 메시지를 덮어쓰는 대신 메시지 배열에 추가됩니다. 일반적으로는 애플리케이션에 영향을 주지 않습니다.

<!-- In addition, the `$fail` callback now returns an object. If you were previously type-hinting the return type of your validation closure, this may require you to update your type-hint: -->
또한, `$fail` 콜백이 이제 객체를 반환하게 변경되었습니다. 만약 이전에 유효성 검증 클로저의 반환값 타입을 명시하고 있었다면 타입힌트 업데이트가 필요할 수 있습니다.

```php
public function rules()
{
    'name' => [
        function ($attribute, $value, $fail) {
            $fail('validation.translation.key')->translate();
        },
    ],
}
```

<a name="validation-messages-and-closure-rules"></a>
<!-- #### Validation Messages and Closure Rules -->
#### Validation Messages and Closure Rules

<!-- **Likelihood Of Impact: Very Low** -->
**영향도: 매우 낮음**

<!-- Previously, you could assign a failure message to a different key by providing an array to the `$fail` callback injected into Closure based validation rules. However, you should now provide the key as the first argument and the failure message as the second argument: -->
이전에는 유효성 검증 클로저에서, `$fail` 콜백에 배열을 전달하여 실패 메시지를 다른 키로 할당할 수 있었습니다. 이제는 첫 번째 인자로 키, 두 번째 인자로 실패 메시지를 전달하는 방식으로 변경해야 합니다.

```php
Validator::make([
    'foo' => 'string',
    'bar' => [function ($attribute, $value, $fail) {
        $fail('foo', 'Something went wrong!');
    }],
]);
```

<a name="form-request-after-method"></a>
<!-- #### Form Request After Method -->
#### Form Request After Method

<!-- **Likelihood Of Impact: Very Low** -->
**영향도: 매우 낮음**

<!-- Within form requests, the `after` method is now [reserved by Laravel](https://github.com/laravel/framework/pull/46757). If your form requests define an `after` method, the method should be renamed or modified to utilize the new "after validation" feature of Laravel's form requests. -->
폼 요청 클래스에서 정의할 수 있는 `after` 메서드는 이제 [reserved by Laravel](https://github.com/laravel/framework/pull/46757)입니다. 이미 `after` 메서드를 사용하는 경우, 메서드명을 변경하거나 Laravel의 새로운 "after validation" 기능을 이용해 코드를 변환해야 합니다.

<a name="miscellaneous"></a>
<!-- ### Miscellaneous -->
### Miscellaneous

<!-- We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. -->
`laravel/laravel` [GitHub repository](https://github.com/laravel/laravel)의 변경사항도 함께 참고하는 것을 권장합니다. 이 변경사항 중 상당수는 선택적으로 적용할 수 있으나, 애플리케이션의 파일과 동기화를 맞추고 싶을 수 있습니다. 이 가이드에서 다루는 변경사항 외에도 구성 파일이나 주석 등 다양한 변경점이 포함되어 있으니 참고하시기 바랍니다.

<!-- You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/9.x...10.x) and choose which updates are important to you. However, many of the changes shown by the GitHub comparison tool are due to our organization's adoption of PHP native types. These changes are backwards compatible and the adoption of them during the migration to Laravel 10 is optional. -->
[GitHub comparison tool](https://github.com/laravel/laravel/compare/9.x...10.x)를 사용하면 변경사항을 쉽게 확인하고, 중요한 업데이트만 선택적으로 반영할 수 있습니다. 다만, 대부분의 변경점은 PHP 네이티브 타입 도입에 따른 것으로, 이 변경들은 하위 호환성이 보장되므로 Laravel 10 마이그레이션 시 필수 반영 사항은 아닙니다.
