<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 11](#laravel-11)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel과 그 외의 공식 패키지들은 [Semantic Versioning](https://semver.org)을 따릅니다. 주요 프레임워크 릴리스는 매년(대략 1분기)에, 마이너 및 패치 릴리스는 매주 나올 수 있습니다. 마이너 버전과 패치 버전에는 **절대로** 하위 호환성이 깨지는 변경 사항이 포함되어서는 안 됩니다.

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^11.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 구성 요소를 참조할 때는 반드시 `^11.0`과 같이 버전 제약 조건을 사용해야 합니다. 이는 Laravel의 주요 버전 업데이트에는 호환성에 영향을 주는 변경이 포함될 수 있기 때문입니다. 하지만, 새로운 주요 릴리스로의 마이그레이션이 하루 이내에 끝날 수 있도록 항상 최선을 다하고 있습니다.

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 가이드라인에 포함되지 않습니다. Laravel 코드베이스의 개선을 위해 필요하다면 함수 인수명의 변경이 있을 수 있습니다. 따라서, Laravel 메서드를 호출할 때 네임드 인수를 사용하는 경우 인수명이 향후 변경될 수 있음을 반드시 인지하고 신중히 사용해야 합니다.

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/11.x/database#introduction). -->
모든 Laravel 릴리스에 대해 버그 수정은 18개월, 보안 패치는 2년 동안 제공됩니다. Lumen을 포함한 추가 라이브러리들은 최신 주요 릴리스만 버그 수정을 받습니다. 또한, Laravel이 지원하는 데이터베이스 버전에 대해서는 [supported by Laravel](/docs/11.x/database#introduction)에서 반드시 확인하세요.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 버전 | PHP (*) | 출시일 | 버그 수정 지원 종료 | 보안 패치 지원 종료 |
| --- | --- | --- | --- | --- |
| 9 | 8.0 - 8.2 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12 | 8.2 - 8.4 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |

<!-- </div> -->
</div>

<!--
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>
-->
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

<!-- (*) Supported PHP versions -->
(*) 지원되는 PHP 버전

<a name="laravel-11"></a>
<!-- ## Laravel 11 -->
## Laravel 11

<!-- Laravel 11 continues the improvements made in Laravel 10.x by introducing a streamlined application structure, per-second rate limiting, health routing, graceful encryption key rotation, queue testing improvements, [Resend](https://resend.com) mail transport, Prompt validator integration, new Artisan commands, and more. In addition, Laravel Reverb, a first-party, scalable WebSocket server has been introduced to provide robust real-time capabilities to your applications. -->
Laravel 11은 간결해진 애플리케이션 구조, 초 단위의 속도 제한, 헬스 라우팅, 안전한 암호화 키 교체, 큐 테스트 기능 개선, [Resend](https://resend.com) 메일 전송 지원, Prompt 유효성 검증 통합, 새로운 아티즌 명령어 등 다양한 개선을 통해 Laravel 10.x에서 더욱 진화하였습니다. 또한, 공식적으로 확장 가능한 웹소켓 서버인 Laravel Reverb가 도입되어, 애플리케이션에 강력한 실시간 기능을 제공합니다.

<a name="php-8"></a>
<!-- ### PHP 8.2 -->
### PHP 8.2

<!-- Laravel 11.x requires a minimum PHP version of 8.2. -->
Laravel 11.x는 최소 PHP 8.2 버전이 필요합니다.

<a name="structure"></a>
<!-- ### Streamlined Application Structure -->
### Streamlined Application Structure

<!-- _Laravel's streamlined application structure was developed by [Taylor Otwell](https://github.com/taylorotwell) and [Nuno Maduro](https://github.com/nunomaduro)_. -->
_이 간결한 애플리케이션 구조는 [Taylor Otwell](https://github.com/taylorotwell)과 [Nuno Maduro](https://github.com/nunomaduro)가 개발했습니다._

<!-- Laravel 11 introduces a streamlined application structure for **new** Laravel applications, without requiring any changes to existing applications. The new application structure is intended to provide a leaner, more modern experience, while retaining many of the concepts that Laravel developers are already familiar with. Below we will discuss the highlights of Laravel's new application structure. -->
Laravel 11에서는 **새로운** Laravel 애플리케이션을 위한 더욱 간결한 프로젝트 구조가 도입되었습니다. 기존 애플리케이션의 수정 없이 적용 가능하며, Laravel 개발자들이 익숙한 주요 개념들을 그대로 유지하면서도 더 현대적이고 가벼운 개발 경험을 제공합니다. 아래에서는 Laravel의 새로운 애플리케이션 구조의 핵심 사항을 살펴봅니다.

<!-- #### The Application Bootstrap File -->
#### The Application Bootstrap File

<!-- The `bootstrap/app.php` file has been revitalized as a code-first application configuration file. From this file, you may now customize your application's routing, middleware, service providers, exception handling, and more. This file unifies a variety of high-level application behavior settings that were previously scattered throughout your application's file structure: -->
`bootstrap/app.php` 파일은 코드 기반의 애플리케이션 설정 파일로 새롭게 개선되었습니다. 이제 이 파일에서 라우팅, 미들웨어, 서비스 프로바이더, 예외 처리 등 애플리케이션의 다양한 요소를 직접 구성할 수 있습니다. 이 파일을 통해 기존에는 애플리케이션 파일 구조 곳곳에 분산되어 있던 여러 상위 수준의 설정들을 한 곳에서 관리하게 되었습니다.

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        //
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
```

<a name="service-providers"></a>
<!-- #### Service Providers -->
#### Service Providers

<!-- Instead of the default Laravel application structure containing five service providers, Laravel 11 only includes a single `AppServiceProvider`. The functionality of the previous service providers has been incorporated into the `bootstrap/app.php`, is handled automatically by the framework, or may be placed in your application's `AppServiceProvider`. -->
이전에는 Laravel 기본 애플리케이션 구조에 5개의 서비스 프로바이더가 포함되어 있었으나, Laravel 11에서는 이제 하나의 `AppServiceProvider`만 포함됩니다. 나머지 프로바이더들의 기능은 `bootstrap/app.php`로 통합되었거나, 프레임워크에서 자동 처리되며, 필요한 경우 `AppServiceProvider`에 직접 작성할 수 있습니다.

<!-- For example, event discovery is now enabled by default, largely eliminating the need for manual registration of events and their listeners. However, if you do need to manually register events, you may simply do so in the `AppServiceProvider`. Similarly, route model bindings or authorization gates you may have previously registered in the `AuthServiceProvider` may also be registered in the `AppServiceProvider`. -->
예를 들어, 이벤트 디스커버리(event discovery)는 기본적으로 활성화되어 있어, 이벤트와 리스너의 수동 등록이 거의 필요하지 않습니다. 하지만 수동 등록이 필요한 경우에는 `AppServiceProvider`에 추가하면 됩니다. 이와 마찬가지로, 이전에 `AuthServiceProvider`에 등록하던 라우트 모델 바인딩 또는 인가 게이트(Gate)도 이제 `AppServiceProvider`에서 처리할 수 있습니다.

<a name="opt-in-routing"></a>
<!-- #### Opt-in API and Broadcast Routing -->
#### Opt-in API and Broadcast Routing

<!-- The `api.php` and `channels.php` route files are no longer present by default, as many applications do not require these files. Instead, they may be created using simple Artisan commands: -->
이제 `api.php`와 `channels.php` 라우트 파일은 기본적으로 포함되지 않으며, 많은 애플리케이션에서 필요하지 않기 때문입니다. 이 파일들이 필요할 경우, 아래와 같이 간단한 아티즌 명령어로 생성할 수 있습니다.

```shell
php artisan install:api

php artisan install:broadcasting
```

<a name="middleware"></a>
<!-- #### Middleware -->
#### Middleware

<!-- Previously, new Laravel applications included nine middleware. These middleware performed a variety of tasks such as authenticating requests, trimming input strings, and validating CSRF tokens. -->
이전에는 새 Laravel 애플리케이션에 9개의 미들웨어가 포함되어 있었으며, 이는 인증, 입력 문자열 트림, CSRF 토큰 검증 등 다양한 작업을 수행했습니다.

<!-- In Laravel 11, these middleware have been moved into the framework itself, so that they do not add bulk to your application's structure. New methods for customizing the behavior of these middleware have been added to the framework and may be invoked from your application's `bootstrap/app.php` file: -->
Laravel 11에서는 이 미들웨어들이 프레임워크 내부로 이동하여, 애플리케이션 구조를 단순화하였습니다. 미들웨어 동작을 커스터마이즈하는 새로운 메서드가 추가되어, 애플리케이션의 `bootstrap/app.php` 파일에서 쉽게 설정할 수 있습니다.

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->validateCsrfTokens(
        except: ['stripe/*']
    );

    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ])
})
```

<!-- Since all middleware can be easily customized via your application's `bootstrap/app.php`, the need for a separate HTTP "kernel" class has been eliminated. -->
이제 모든 미들웨어를 `bootstrap/app.php`에서 손쉽게 커스터마이즈할 수 있으므로, 별도의 HTTP "커널" 클래스가 필요하지 않습니다.

<a name="scheduling"></a>
<!-- #### Scheduling -->
#### Scheduling

<!-- Using a new `Schedule` facade, scheduled tasks may now be defined directly in your application's `routes/console.php` file, eliminating the need for a separate console "kernel" class: -->
새로운 `Schedule` 파사드를 이용하면, 스케줄된 작업을 애플리케이션의 `routes/console.php` 파일에 직접 정의할 수 있게 되어, 별도의 콘솔 "커널" 클래스가 필요 없어졌습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->daily();
```

<a name="exception-handling"></a>
<!-- #### Exception Handling -->
#### Exception Handling

<!-- Like routing and middleware, exception handling can now be customized from your application's `bootstrap/app.php` file instead of a separate exception handler class, reducing the overall number of files included in a new Laravel application: -->
라우팅이나 미들웨어와 마찬가지로, 예외 처리 역시 기존의 독립적인 예외 처리기 클래스를 사용하는 대신, 이제 `bootstrap/app.php` 파일에서 직접 커스터마이즈할 수 있어, 새 애플리케이션의 파일 수가 줄어듭니다.

```php
->withExceptions(function (Exceptions $exceptions) {
    $exceptions->dontReport(MissedFlightException::class);

    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```

<a name="base-controller-class"></a>
<!-- #### Base `Controller` Class -->
#### Base `Controller` Class

<!-- The base controller included in new Laravel applications has been simplified. It no longer extends Laravel's internal `Controller` class, and the `AuthorizesRequests` and `ValidatesRequests` traits have been removed, as they may be included in your application's individual controllers if desired: -->
새로운 Laravel 애플리케이션에 포함되는 기본 컨트롤러가 간소화되었습니다. 더 이상 Laravel 내부의 `Controller` 클래스를 상속하지 않으며, `AuthorizesRequests` 및 `ValidatesRequests` 트레잇도 제거되었습니다. 이 트레잇들은 필요할 경우 개별 컨트롤러에서 직접 사용하면 됩니다.

```
<?php

namespace App\Http\Controllers;

abstract class Controller
{
    //
}
```

<a name="application-defaults"></a>
<!-- #### Application Defaults -->
#### Application Defaults

<!-- By default, new Laravel applications use SQLite for database storage, as well as the `database` driver for Laravel's session, cache, and queue. This allows you to begin building your application immediately after creating a new Laravel application, without being required to install additional software or create additional database migrations. -->
이제 새로 생성하는 Laravel 애플리케이션은 기본적으로 데이터베이스 저장소로 SQLite를, 그리고 세션, 캐시, 큐에는 `database` 드라이버를 사용합니다. 이를 통해 추가 소프트웨어 설치나 별도의 데이터베이스 마이그레이션을 진행하지 않고도 바로 개발을 시작할 수 있습니다.

<!-- In addition, over time, the `database` drivers for these Laravel services have become robust enough for production usage in many application contexts; therefore, they provide a sensible, unified choice for both local and production applications. -->
또한 시간이 흐르면서, 이러한 Laravel 서비스의 `database` 드라이버들도 실제 운영 환경에서 충분히 사용할 수 있을 정도로 견고해졌기 때문에, 로컬 개발 뿐만 아니라 프로덕션에서도 일관된 선택지가 됩니다.

<a name="reverb"></a>
<!-- ### Laravel Reverb -->
### Laravel Reverb

<!-- _Laravel Reverb was developed by [Joe Dixon](https://github.com/joedixon)_. -->
_Laravel Reverb는 [Joe Dixon](https://github.com/joedixon)이 개발했습니다._

<!-- [Laravel Reverb](https://reverb.laravel.com) brings blazing-fast and scalable real-time WebSocket communication directly to your Laravel application, and provides seamless integration with Laravel’s existing suite of event broadcasting tools, such as Laravel Echo. -->
[Laravel Reverb](https://reverb.laravel.com)는 놀라울 정도로 빠르고 확장 가능한 실시간 WebSocket 통신을 Laravel 애플리케이션에 직접 제공하며, Laravel의 기존 이벤트 브로드캐스팅 도구인 Laravel Echo와도 매끄럽게 통합됩니다.

```shell
php artisan reverb:start
```

<!-- In addition, Reverb supports horizontal scaling via Redis's publish / subscribe capabilities, allowing you to distribute your WebSocket traffic across multiple backend Reverb servers all supporting a single, high-demand application. -->
또한, Reverb는 Redis의 발행/구독 기능을 이용한 수평 확장(horizontally scaling)을 지원합니다. 이로써 여러 대의 백엔드 Reverb 서버가 하나의 대규모 애플리케이션의 WebSocket 트래픽을 분산 처리할 수 있습니다.

<!-- For more information on Laravel Reverb, please consult the complete [Reverb documentation](/docs/11.x/reverb). -->
자세한 내용은 [Reverb documentation](/docs/11.x/reverb)를 참고하세요.

<a name="rate-limiting"></a>
<!-- ### Per-Second Rate Limiting -->
### Per-Second Rate Limiting

<!-- _Per-second rate limiting was contributed by [Tim MacDonald](https://github.com/timacdonald)_. -->
_초 단위 속도 제한 기능은 [Tim MacDonald](https://github.com/timacdonald)가 기여했습니다._

<!-- Laravel now supports "per-second" rate limiting for all rate limiters, including those for HTTP requests and queued jobs. Previously, Laravel's rate limiters were limited to "per-minute" granularity: -->
Laravel은 이제 모든 속도 제한기(HTTP 요청, 큐 작업 등)에서 "초 단위" 속도 제한을 지원합니다. 이전까지는 분 단위로만 제한할 수 있었습니다.

```php
RateLimiter::for('invoices', function (Request $request) {
    return Limit::perSecond(1);
});
```

<!-- For more information on rate limiting in Laravel, check out the [rate limiting documentation](/docs/11.x/routing#rate-limiting). -->
Laravel의 속도 제한에 대한 자세한 내용은 [rate limiting documentation](/docs/11.x/routing#rate-limiting)를 참고하세요.

<a name="health"></a>
<!-- ### Health Routing -->
### Health Routing

<!-- _Health routing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_헬스 라우팅 기능은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

<!-- New Laravel 11 applications include a `health` routing directive, which instructs Laravel to define a simple health-check endpoint that may be invoked by third-party application health monitoring services or orchestration systems like Kubernetes. By default, this route is served at `/up`: -->
새로운 Laravel 11 애플리케이션에는 `health` 라우팅 지시문이 포함되어, Kubernetes와 같은 오케스트레이션 시스템 또는 외부 애플리케이션 헬스 모니터링 서비스가 호출할 수 있는 간단한 헬스 체크 엔드포인트(`/up` 경로)를 제공합니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up',
)
```

<!-- When HTTP requests are made to this route, Laravel will also dispatch a `DiagnosingHealth` event, allowing you to perform additional health checks that are relevant to your application. -->
이 라우트에 HTTP 요청이 오면 Laravel은 `DiagnosingHealth` 이벤트도 디스패치하므로, 애플리케이션별로 추가적인 헬스 체크를 수행할 수도 있습니다.

<a name="encryption"></a>
<!-- ### Graceful Encryption Key Rotation -->
### Graceful Encryption Key Rotation

<!-- _Graceful encryption key rotation was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_안전한 암호화 키 교체 기능은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

<!-- Since Laravel encrypts all cookies, including your application's session cookie, essentially every request to a Laravel application relies on encryption. However, because of this, rotating your application's encryption key would log all users out of your application. In addition, decrypting data that was encrypted by the previous encryption key becomes impossible. -->
Laravel은 세션 쿠키를 포함해 모든 쿠키를 암호화합니다. 즉, Laravel 애플리케이션에 들어오는 거의 모든 요청이 암호화에 의존합니다. 이런 구조에서 암호화 키를 교체하면 모든 사용자가 로그아웃되고, 이전 키로 암호화된 데이터는 복호화가 불가능해집니다.

<!-- Laravel 11 allows you to define your application's previous encryption keys as a comma-delimited list via the `APP_PREVIOUS_KEYS` environment variable. -->
Laravel 11에서는 `APP_PREVIOUS_KEYS` 환경변수에 이전 암호화 키들을 쉼표로 구분해 지정할 수 있습니다.

<!-- When encrypting values, Laravel will always use the "current" encryption key, which is within the `APP_KEY` environment variable. When decrypting values, Laravel will first try the current key. If decryption fails using the current key, Laravel will try all previous keys until one of the keys is able to decrypt the value. -->
값을 암호화할 때는 항상 `APP_KEY` 환경변수에 있는 현재 키가 사용됩니다. 값을 복호화할 때는 먼저 현재 키로 시도하고, 실패할 경우 이전 키들을 순차적으로 시도해 복호화가 성공하면 그 값을 사용합니다.

<!-- This approach to graceful decryption allows users to keep using your application uninterrupted even if your encryption key is rotated. -->
이 방식 덕분에, 암호화 키를 교체하더라도 사용자는 로그아웃되지 않고 기존 데이터를 계속 사용할 수 있습니다.

<!-- For more information on encryption in Laravel, check out the [encryption documentation](/docs/11.x/encryption). -->
Laravel의 암호화 기능에 대한 자세한 내용은 [encryption documentation](/docs/11.x/encryption)를 참고하세요.

<a name="automatic-password-rehashing"></a>
<!-- ### Automatic Password Rehashing -->
### Automatic Password Rehashing

<!-- _Automatic password rehashing was contributed by [Stephen Rees-Carter](https://github.com/valorin)_. -->
_자동 비밀번호 재해시 기능은 [Stephen Rees-Carter](https://github.com/valorin)가 기여했습니다._

<!-- Laravel's default password hashing algorithm is bcrypt. The "work factor" for bcrypt hashes can be adjusted via the `config/hashing.php` configuration file or the `BCRYPT_ROUNDS` environment variable. -->
Laravel의 기본 비밀번호 해시 알고리즘은 bcrypt입니다. bcrypt 해시의 "work factor"(연산 횟수)는 `config/hashing.php` 파일이나 `BCRYPT_ROUNDS` 환경변수로 조절할 수 있습니다.

<!-- Typically, the bcrypt work factor should be increased over time as CPU / GPU processing power increases. If you increase the bcrypt work factor for your application, Laravel will now gracefully and automatically rehash user passwords as users authenticate with your application. -->
보통 CPU나 GPU 성능이 발전함에 따라 bcrypt work factor를 높여 주어야 합니다. Laravel 11에서는 애플리케이션의 work factor가 변경된 경우, 사용자가 인증할 때마다 자동으로 비밀번호를 재해시합니다.

<a name="prompt-validation"></a>
<!-- ### Prompt Validation -->
### Prompt Validation

<!-- _Prompt validator integration was contributed by [Andrea Marco Sartori](https://github.com/cerbero90)_. -->
_Prompt 유효성 검증 통합은 [Andrea Marco Sartori](https://github.com/cerbero90)가 기여했습니다._

<!-- [Laravel Prompts](/docs/11.x/prompts) is a PHP package for adding beautiful and user-friendly forms to your command-line applications, with browser-like features including placeholder text and validation. -->
[Laravel Prompts](/docs/11.x/prompts)는 명령줄 애플리케이션에서 아름답고 직관적인 폼을 만들 수 있게 해주는 PHP 패키지로, 플레이스홀더 텍스트 및 유효성 검증 등 브라우저와 유사한 기능을 지원합니다.

<!-- Laravel Prompts supports input validation via closures: -->
Laravel Prompts는 클로저를 통한 입력값 검증을 지원합니다.

```php
$name = text(
    label: 'What is your name?',
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

<!-- However, this can become cumbersome when dealing with many inputs or complicated validation scenarios. Therefore, in Laravel 11, you may utilize the full power of Laravel's [validator](/docs/11.x/validation) when validating prompt inputs: -->
하지만 많은 입력값이나 복잡한 유효성 검증이 필요한 경우 이 방식이 번거로울 수 있습니다. 이에 따라, Laravel 11에서는 프롬프트 입력값 유효성 검증에 [validator](/docs/11.x/validation)의 전체 기능을 그대로 사용할 수 있습니다.

```php
$name = text('What is your name?', validate: [
    'name' => 'required|min:3|max:255',
]);
```

<a name="queue-interaction-testing"></a>
<!-- ### Queue Interaction Testing -->
### Queue Interaction Testing

<!-- _Queue interaction testing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_큐 상호작용 테스트 기능은 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

<!-- Previously, attempting to test that a queued job was released, deleted, or manually failed was cumbersome and required the definition of custom queue fakes and stubs. However, in Laravel 11, you may easily test for these queue interactions using the `withFakeQueueInteractions` method: -->
이전에는 큐에 등록된 작업이 다시 반환, 삭제, 수동 실패 처리됐는지를 테스트하기 위해 커스텀 큐 페이크(fake)와 스텁을 작성해야 했습니다. 이제 Laravel 11에서는 `withFakeQueueInteractions` 메서드를 통해 이러한 큐 동작을 손쉽게 테스트할 수 있습니다.

```php
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
```

<!-- For more information on testing queued jobs, check out the [queue documentation](/docs/11.x/queues#testing). -->
큐에 등록된 작업 테스트에 대한 더 자세한 정보는 [queue documentation](/docs/11.x/queues#testing)를 참고하세요.

<a name="new-artisan-commands"></a>
<!-- ### New Artisan Commands -->
### New Artisan Commands

<!-- _Class creation Artisan commands were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_클래스 생성 관련 아티즌 명령어는 [Taylor Otwell](https://github.com/taylorotwell)이 기여했습니다._

<!-- New Artisan commands have been added to allow the quick creation of classes, enums, interfaces, and traits: -->
아티즌에서 클래스, 열거형(Enum), 인터페이스, 트레잇을 빠르게 생성할 수 있는 새로운 명령어들이 추가되었습니다.

```shell
php artisan make:class
php artisan make:enum
php artisan make:interface
php artisan make:trait
```

<a name="model-cast-improvements"></a>
<!-- ### Model Casts Improvements -->
### Model Casts Improvements

<!-- _Model casts improvements were contributed by [Nuno Maduro](https://github.com/nunomaduro)_. -->
_모델 cast 개선은 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

<!-- Laravel 11 supports defining your model's casts using a method instead of a property. This allows for streamlined, fluent cast definitions, especially when using casts with arguments: -->
Laravel 11부터는 모델의 cast(cast)를 속성이 아니라 메서드로 정의할 수 있습니다. 이를 통해, 특히 인수(arguments)를 사용하는 cast 정의가 훨씬 더 간결하고 직관적으로 바뀝니다.

```
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::using(OptionCollection::class),
                  // AsEncryptedCollection::using(OptionCollection::class),
                  // AsEnumArrayObject::using(OptionEnum::class),
                  // AsEnumCollection::using(OptionEnum::class),
    ];
}
```

<!-- For more information on attribute casting, review the [Eloquent documentation](/docs/11.x/eloquent-mutators#attribute-casting). -->
attribute casting에 대한 자세한 내용은 [Eloquent documentation](/docs/11.x/eloquent-mutators#attribute-casting)를 참고하세요.

<a name="the-once-function"></a>
<!-- ### The `once` Function -->
### The `once` Function

<!-- _The `once` helper was contributed by [Taylor Otwell](https://github.com/taylorotwell)_ and _[Nuno Maduro](https://github.com/nunomaduro)_. -->
_`once` 헬퍼 함수는 [Taylor Otwell](https://github.com/taylorotwell)과 [Nuno Maduro](https://github.com/nunomaduro)가 기여했습니다._

<!-- The `once` helper function executes the given callback and caches the result in memory for the duration of the request. Any subsequent calls to the `once` function with the same callback will return the previously cached result: -->
`once` 헬퍼 함수는 주어진 콜백을 실행하고 해당 요청이 진행되는 동안 그 결과를 메모리에 캐싱합니다. 같은 콜백으로 `once` 함수를 다시 호출하면 이전에 캐시된 결과를 그대로 반환합니다.

```
function random(): int
{
    return once(function () {
        return random_int(1, 1000);
    });
}

random(); // 123
random(); // 123 (cached result)
random(); // 123 (cached result)
```

<!-- For more information on the `once` helper, check out the [helpers documentation](/docs/11.x/helpers#method-once). -->
`once` 헬퍼에 대한 자세한 정보는 [helpers documentation](/docs/11.x/helpers#method-once)를 참고하세요.

<a name="database-performance"></a>
<!-- ### Improved Performance When Testing With In-Memory Databases -->
### Improved Performance When Testing With In-Memory Databases

<!-- _Improved in-memory database testing performance was contributed by [Anders Jenbo](https://github.com/AJenbo)_ -->
_인메모리 데이터베이스 테스트 성능 개선은 [Anders Jenbo](https://github.com/AJenbo)가 기여했습니다._

<!-- Laravel 11 offers a significant speed boost when using the `:memory:` SQLite database during testing. To accomplish this, Laravel now maintains a reference to PHP's PDO object and reuses it across connections, often cutting total test run time in half. -->
Laravel 11에서는 테스트 시 `:memory:` SQLite 데이터베이스를 사용할 때 성능이 크게 향상되었습니다. 이는 Laravel이 PHP의 PDO 객체 참조를 유지하고, 여러 커넥션 간에 재사용하도록 개선했기 때문입니다. 실제로 전체 테스트 실행 시간이 절반가량 단축되는 경우도 많습니다.

<a name="mariadb"></a>
<!-- ### Improved Support for MariaDB -->
### Improved Support for MariaDB

<!-- _Improved support for MariaDB was contributed by [Jonas Staudenmeir](https://github.com/staudenmeir) and [Julius Kiekbusch](https://github.com/Jubeki)_ -->
_MariaDB 지원 개선은 [Jonas Staudenmeir](https://github.com/staudenmeir)와 [Julius Kiekbusch](https://github.com/Jubeki)가 기여했습니다._

<!-- Laravel 11 includes improved support for MariaDB. In previous Laravel releases, you could use MariaDB via Laravel's MySQL driver. However, Laravel 11 now includes a dedicated MariaDB driver which provides better defaults for this database system. -->
Laravel 11에서는 MariaDB 지원이 더욱 발전했습니다. 이전 버전에서는 MySQL 드라이버를 통해 MariaDB를 사용할 수 있었지만, 이제는 전용 MariaDB 드라이버가 새로 도입되어 해당 데이터베이스에 더 적합한 기본 설정을 제공합니다.

<!-- For more information on Laravel's database drivers, check out the [database documentation](/docs/11.x/database). -->
Laravel의 데이터베이스 드라이버에 대해 더 알아보려면 [database documentation](/docs/11.x/database)를 참고하세요.

<a name="inspecting-database"></a>
<!-- ### Inspecting Databases and Improved Schema Operations -->
### Inspecting Databases and Improved Schema Operations

<!-- _Improved schema operations and database inspection was contributed by [Hafez Divandari](https://github.com/hafezdivandari)_ -->
_스키마 작업 및 데이터베이스 인스펙션 개선은 [Hafez Divandari](https://github.com/hafezdivandari)가 기여했습니다._

<!-- Laravel 11 provides additional database schema operation and inspection methods, including the native modifying, renaming, and dropping of columns. Furthermore, advanced spatial types, non-default schema names, and native schema methods for manipulating tables, views, columns, indexes, and foreign keys are provided: -->
Laravel 11에는 데이터베이스 스키마 작업과 인스펙션 관련 다양한 새 메서드가 추가되었습니다. 이제 컬럼의 직접 수정/이름 변경/삭제 등이 기본적으로 지원되며, 고급 공간 타입(spatial type), 기본값이 아닌 스키마명, 테이블/뷰/컬럼/인덱스/외래키 등 다양한 객체에 대한 네이티브 스키마 메서드도 사용할 수 있습니다.

```
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```
