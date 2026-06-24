<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
    - [Exceptions](#exceptions)
- [Support Policy](#support-policy)
- [Laravel 8](#laravel-8)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~February), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel 및 공식 서드파티 패키지는 [Semantic Versioning](https://semver.org)을 따릅니다. 프레임워크의 메이저 릴리스는 매년(대략 2월)에 제공되며, 마이너 및 패치 릴리스는 매주처럼 자주 나올 수 있습니다. 마이너 및 패치 릴리스에는 **절대** 하위 호환성을 깨뜨리는 변경 사항이 포함되어서는 안 됩니다.

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^8.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
애플리케이션이나 패키지에서 Laravel 프레임워크 또는 Laravel 컴포넌트를 참조할 때는 항상 `^8.0`과 같은 버전 제약 조건을 사용하는 것이 좋습니다. Laravel의 메이저 릴리스에는 하위 호환성을 깨뜨리는 변경이 포함될 수 있기 때문입니다. 물론, 새로운 메이저 릴리스로 하루 이내에 업데이트할 수 있도록 최대한 노력하고 있습니다.

<a name="exceptions"></a>
<!-- ### Exceptions -->
### Exceptions

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- At this time, PHP's [named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) functionality are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function parameters when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
현재 시점에서, PHP의 [named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) 기능은 Laravel의 하위 호환성 정책에 포함되어 있지 않습니다. Laravel 코드베이스의 품질 개선을 위해 필요에 따라 함수 매개변수명을 변경할 수 있습니다. 따라서, Laravel 메서드를 호출할 때 네임드 인수를 활용하는 경우, 앞으로 매개변수명이 변경될 수 있다는 점을 유의해서 신중하게 사용해야 합니다.

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, including Lumen, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/8.x/database#introduction). -->
모든 Laravel 릴리스에 대해 버그 수정은 18개월 동안, 보안 수정은 2년간 제공됩니다. 추가적인 라이브러리(예: Lumen)에는 가장 최신 메이저 릴리스만 버그가 수정됩니다. 또한, Laravel에서 [supported by Laravel](/docs/8.x/database#introduction)도 반드시 확인해 주세요.

| 버전 | PHP (*) | 출시일 | 버그 수정 종료일 | 보안 수정 종료일 |
| --- | --- | --- | --- | --- |
| 6 (LTS) | 7.2 - 8.0 | 2019년 9월 3일 | 2022년 1월 25일 | 2022년 9월 6일 |
| 7 | 7.2 - 8.0 | 2020년 3월 3일 | 2020년 10월 6일 | 2021년 3월 3일 |
| 8 | 7.3 - 8.1 | 2020년 9월 8일 | 2022년 7월 26일 | 2023년 1월 24일 |
| 9 | 8.0 - 8.1 | 2022년 2월 8일 | 2023년 8월 8일 | 2024년 2월 6일 |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |

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

<a name="laravel-8"></a>
<!-- ## Laravel 8 -->
## Laravel 8

<!-- Laravel 8 continues the improvements made in Laravel 7.x by introducing Laravel Jetstream, model factory classes, migration squashing, job batching, improved rate limiting, queue improvements, dynamic Blade components, Tailwind pagination views, time testing helpers, improvements to `artisan serve`, event listener improvements, and a variety of other bug fixes and usability improvements. -->
Laravel 8은 Laravel 7.x에서 이루어진 개선을 이어가며, Laravel Jetstream, 모델 팩토리 클래스, 마이그레이션 스쿼싱, 작업 배치(job batching), 향상된 요청 속도 제한(rate limiting), 큐(queue) 기능 개선, 동적 Blade 컴포넌트, Tailwind 기반 페이지네이션 뷰, 시간 테스트 헬퍼, `artisan serve` 개선, 이벤트 리스너 개선 및 다양한 버그 수정과 사용성 개선을 제공합니다.

<a name="laravel-jetstream"></a>
<!-- ### Laravel Jetstream -->
### Laravel Jetstream

<!-- _Laravel Jetstream was written by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_Laravel Jetstream은 [Taylor Otwell](https://github.com/taylorotwell)이 작성하였습니다._

<!-- [Laravel Jetstream](https://jetstream.laravel.com) is a beautifully designed application scaffolding for Laravel. Jetstream provides the perfect starting point for your next project and includes login, registration, email verification, two-factor authentication, session management, API support via Laravel Sanctum, and optional team management. Laravel Jetstream replaces and improves upon the legacy authentication UI scaffolding available for previous versions of Laravel. -->
[Laravel Jetstream](https://jetstream.laravel.com)은 Laravel을 위한 아름답게 설계된 애플리케이션 시작 템플릿(scaffolding)입니다. Jetstream은 새로운 프로젝트를 시작하기에 완벽한 출발점을 제공하며, 로그인, 회원가입, 이메일 인증, 2단계 인증, 세션 관리, Laravel Sanctum을 활용한 API 지원, 선택 가능한 팀 관리 기능을 기본으로 포함합니다. Laravel Jetstream은 이전 Laravel 버전에서 제공되던 레거시 인증 UI scaffolding을 대체하며 더 발전시켰습니다.

<!-- Jetstream is designed using [Tailwind CSS](https://tailwindcss.com) and offers your choice of [Livewire](https://laravel-livewire.com) or [Inertia](https://inertiajs.com) scaffolding. -->
Jetstream은 [Tailwind CSS](https://tailwindcss.com)로 디자인되어 있으며, [Livewire](https://laravel-livewire.com) 또는 [Inertia](https://inertiajs.com) 중 원하는 방식으로 scaffolding을 선택할 수 있습니다.

<a name="models-directory"></a>
<!-- ### Models Directory -->
### Models Directory

<!-- By overwhelming community demand, the default Laravel application skeleton now contains an `app/Models` directory. We hope you enjoy this new home for your Eloquent models! All relevant generator commands have been updated to assume models exist within the `app/Models` directory if it exists. If the directory does not exist, the framework will assume your models should be placed within the `app` directory. -->
많은 커뮤니티의 요청에 따라, 이제 기본 Laravel 애플리케이션 스캐폴딩에 `app/Models` 디렉토리가 포함됩니다. 이 디렉토리가 여러분의 Eloquent 모델을 위한 새로운 홈이 되길 바랍니다! 관련된 모든 제너레이터 명령어들도 이 디렉토리가 존재하면 모델을 `app/Models` 하위에 생성하도록 반영되었습니다. 만약 해당 디렉토리가 없다면, 프레임워크는 기존과 같이 `app` 디렉토리에 모델을 생성합니다.

<a name="model-factory-classes"></a>
<!-- ### Model Factory Classes -->
### Model Factory Classes

<!-- _Model factory classes were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_모델 팩토리 클래스는 [Taylor Otwell](https://github.com/taylorotwell)이 기여하였습니다._

<!-- Eloquent [model factories](/docs/8.x/database-testing#defining-model-factories) have been entirely re-written as class based factories and improved to have first-class relationship support. For example, the `UserFactory` included with Laravel is written like so: -->
Eloquent의 [model factories](/docs/8.x/database-testing#defining-model-factories)가 완전히 클래스 기반으로 새로 작성되었으며, 연관관계를 1급 시민으로서 지원하도록 개선되었습니다. 예를 들어, Laravel에서 기본 제공하는 `UserFactory`는 다음과 같이 작성됩니다.

```
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    /**
     * The name of the factory's corresponding model.
     *
     * @var string
     */
    protected $model = User::class;

    /**
     * Define the model's default state.
     *
     * @return array
     */
    public function definition()
    {
        return [
            'name' => $this->faker->name(),
            'email' => $this->faker->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'remember_token' => Str::random(10),
        ];
    }
}
```

<!-- Thanks to the new `HasFactory` trait available on generated models, the model factory may be used like so: -->
생성된 모델에서 사용할 수 있는 새로운 `HasFactory` 트레이트 덕분에, 모델 팩토리는 다음과 같이 손쉽게 사용할 수 있습니다.

```
use App\Models\User;

User::factory()->count(50)->create();
```

<!-- Since model factories are now simple PHP classes, state transformations may be written as class methods. In addition, you may add any other helper classes to your Eloquent model factory as needed. -->
모델 팩토리가 이제 단순한 PHP 클래스이므로, 상태(state) 변환(transform)도 클래스 메서드로 작성할 수 있습니다. 그리고 팩토리에서 필요한 경우, 다양한 헬퍼 메서드를 자유롭게 추가할 수 있습니다.

<!-- For example, your `User` model might have a `suspended` state that modifies one of its default attribute values. You may define your state transformations using the base factory's `state` method. You may name your state method anything you like. After all, it's just a typical PHP method: -->
예를 들어, `User` 모델에 기본 속성 값 중 하나를 변경하는 `suspended` 상태가 있다고 가정해봅시다. 이 상태 변환을 팩토리의 `state` 메서드를 활용해 정의할 수 있습니다. 상태 메서드명은 자유롭게 지정할 수 있으며, 결국 일반적인 PHP 메서드일 뿐입니다.

```
/**
 * Indicate that the user is suspended.
 *
 * @return \Illuminate\Database\Eloquent\Factories\Factory
 */
public function suspended()
{
    return $this->state([
        'account_status' => 'suspended',
    ]);
}
```

<!-- After defining the state transformation method, we may use it like so: -->
이렇게 상태 변환 메서드를 정의한 후에는, 아래와 같이 사용할 수 있습니다.

```
use App\Models\User;

User::factory()->count(5)->suspended()->create();
```

<!-- As mentioned, Laravel 8's model factories contain first class support for relationships. So, assuming our `User` model has a `posts` relationship method, we may simply run the following code to generate a user with three posts: -->
위에서 언급한 것처럼, Laravel 8의 모델 팩토리는 연관관계에 대한 1급 지원을 제공합니다. 예를 들어, `User` 모델에 `posts` 연관관계 메서드가 있다면, 아래 코드를 실행하여 3개의 포스트를 가진 사용자를 간단히 생성할 수 있습니다.

```
$users = User::factory()
            ->hasPosts(3, [
                'published' => false,
            ])
            ->create();
```

<!-- To ease the upgrade process, the [laravel/legacy-factories](https://github.com/laravel/legacy-factories) package has been released to provide support for the previous iteration of model factories within Laravel 8.x. -->
업그레이드를 용이하게 하기 위해 [laravel/legacy-factories](https://github.com/laravel/legacy-factories) 패키지가 공개되어, Laravel 8.x에서도 기존 구식(facade 기반) 모델 팩토리를 사용할 수 있습니다.

<!-- Laravel's re-written factories contain many more features that we think you will love. To learn more about model factories, please consult the [database testing documentation](/docs/8.x/database-testing#defining-model-factories). -->
Laravel의 새롭게 설계된 팩토리에는 더 많은 기능이 있으며, 분명히 만족하실 것입니다. 모델 팩토리에 대해 더 자세히 알고 싶다면 [database testing documentation](/docs/8.x/database-testing#defining-model-factories)를 참고해 주세요.

<a name="migration-squashing"></a>
<!-- ### Migration Squashing -->
### Migration Squashing

<!-- _Migration squashing was contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_마이그레이션 스쿼싱 기능은 [Taylor Otwell](https://github.com/taylorotwell)이 기여하였습니다._

<!-- As you build your application, you may accumulate more and more migrations over time. This can lead to your migration directory becoming bloated with potentially hundreds of migrations. If you're using MySQL or PostgreSQL, you may now "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command: -->
애플리케이션을 개발할수록 마이그레이션 파일이 점점 쌓이게 되어, 디렉토리가 수백 개의 마이그레이션으로 비대해질 수 있습니다. 이제 MySQL 또는 PostgreSQL을 사용할 경우, 여러 마이그레이션 파일을 하나의 SQL 파일로 "스쿼시(squash)"할 수 있습니다. 시작하려면 다음과 같이 `schema:dump` 명령어를 실행하면 됩니다.

```
php artisan schema:dump

// Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```

<!-- When you execute this command, Laravel will write a "schema" file to your `database/schema` directory. Now, when you attempt to migrate your database and no other migrations have been executed, Laravel will execute the schema file's SQL first. After executing the schema file's commands, Laravel will execute any remaining migrations that were not part of the schema dump. -->
이 명령어를 실행하면, Laravel은 `database/schema` 디렉토리에 "schema" 파일을 작성합니다. 이후 데이터베이스를 마이그레이션할 때 아직 실행된 마이그레이션이 없다면, Laravel은 이 스키마 파일의 SQL을 우선 실행합니다. 스키마 파일이 실행된 후에는 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 순차적으로 실행합니다.

<a name="job-batching"></a>
<!-- ### Job Batching -->
### Job Batching

<!-- _Job batching was contributed by [Taylor Otwell](https://github.com/taylorotwell) & [Mohamed Said](https://github.com/themsaid)_. -->
_작업 배치 기능은 [Taylor Otwell](https://github.com/taylorotwell) & [Mohamed Said](https://github.com/themsaid)가 기여하였습니다._

<!-- Laravel's job batching feature allows you to easily execute a batch of jobs and then perform some action when the batch of jobs has completed executing. -->
Laravel의 작업 배치(job batching) 기능을 활용하면, 여러 작업을 묶어서 실행하고 모든 작업 처리가 완료된 후 특정 동작을 수행할 수 있습니다.

<!-- The new `batch` method of the `Bus` facade may be used to dispatch a batch of jobs. Of course, batching is primarily useful when combined with completion callbacks. So, you may use the `then`, `catch`, and `finally` methods to define completion callbacks for the batch. Each of these callbacks will receive an `Illuminate\Bus\Batch` instance when they are invoked: -->
`Bus` 파사드의 새로운 `batch` 메서드를 이용해 여러 작업을 한번에 디스패치할 수 있습니다. 배치는 주로 완료 콜백과 함께 사용할 때 유용합니다. 따라서, `then`, `catch`, `finally` 메서드를 통해 배치 처리 완료 시 실행할 콜백을 정의할 수 있습니다. 이들 콜백은 모두 `Illuminate\Bus\Batch` 인스턴스를 인자로 받습니다.

```
use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;
use Throwable;

$batch = Bus::batch([
    new ProcessPodcast(Podcast::find(1)),
    new ProcessPodcast(Podcast::find(2)),
    new ProcessPodcast(Podcast::find(3)),
    new ProcessPodcast(Podcast::find(4)),
    new ProcessPodcast(Podcast::find(5)),
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->catch(function (Batch $batch, Throwable $e) {
    // First batch job failure detected...
})->finally(function (Batch $batch) {
    // The batch has finished executing...
})->dispatch();

return $batch->id;
```

<!-- To learn more about job batching, please consult the [queue documentation](/docs/8.x/queues#job-batching). -->
작업 배치에 대해 더 자세히 알고 싶다면 [queue documentation](/docs/8.x/queues#job-batching)를 참고해 주세요.

<a name="improved-rate-limiting"></a>
<!-- ### Improved Rate Limiting -->
### Improved Rate Limiting

<!-- _Rate limiting improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_요청 속도 제한(rate limiting) 기능은 [Taylor Otwell](https://github.com/taylorotwell)이 개선하였습니다._

<!-- Laravel's request rate limiter feature has been augmented with more flexibility and power, while still maintaining backwards compatibility with previous release's `throttle` middleware API. -->
Laravel의 요청 속도 제한 기능이 더 유연하고 강력해졌으며, 이전 버전의 `throttle` 미들웨어 API와의 하위 호환성도 유지됩니다.

<!-- Rate limiters are defined using the `RateLimiter` facade's `for` method. The `for` method accepts a rate limiter name and a closure that returns the limit configuration that should apply to routes that are assigned this rate limiter: -->
속도 제한기는 `RateLimiter` 파사드의 `for` 메서드로 정의합니다. `for` 메서드는 제한기 이름과, 해당 제한기를 적용할 라우트에 적용될 제한 설정을 반환하는 클로저를 받습니다.

```
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

RateLimiter::for('global', function (Request $request) {
    return Limit::perMinute(1000);
});
```

<!-- Since rate limiter callbacks receive the incoming HTTP request instance, you may build the appropriate rate limit dynamically based on the incoming request or authenticated user: -->
제한기 콜백은 들어오는 HTTP 요청 인스턴스를 받기 때문에, 요청 내용이나 인증된 사용자에 따라 동적으로 제한을 지정할 수 있습니다.

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100);
});
```

<!-- Sometimes you may wish to segment rate limits by some arbitrary value. For example, you may wish to allow users to access a given route 100 times per minute per IP address. To accomplish this, you may use the `by` method when building your rate limit: -->
경우에 따라 임의의 값에 따라 제한을 그룹핑하고 싶을 때가 있습니다. 예를 들어, 사용자가 지정한 경로로 분당 100회씩, 각 IP별로 요청하도록 제한하고 싶다면, 제한을 생성할 때 `by` 메서드를 사용할 수 있습니다.

```
RateLimiter::for('uploads', function (Request $request) {
    return $request->user()->vipCustomer()
                ? Limit::none()
                : Limit::perMinute(100)->by($request->ip());
});
```

<!-- Rate limiters may be attached to routes or route groups using the `throttle` [middleware](/docs/8.x/middleware). The throttle middleware accepts the name of the rate limiter you wish to assign to the route: -->
정의한 속도 제한기는 라우트나 라우트 그룹에서 `throttle` [middleware](/docs/8.x/middleware)를 통해 사용할 수 있습니다. 미들웨어의 인자로 제한기명을 전달하면 됩니다.

```
Route::middleware(['throttle:uploads'])->group(function () {
    Route::post('/audio', function () {
        //
    });

    Route::post('/video', function () {
        //
    });
});
```

<!-- To learn more about rate limiting, please consult the [routing documentation](/docs/8.x/routing#rate-limiting). -->
속도 제한 기능에 대해 더 자세히 알고 싶다면 [routing documentation](/docs/8.x/routing#rate-limiting)를 참고해 주세요.

<a name="improved-maintenance-mode"></a>
<!-- ### Improved Maintenance Mode -->
### Improved Maintenance Mode

<!-- _Maintenance mode improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell) with inspiration from [Spatie](https://spatie.be)_. -->
_유지보수 모드 관련 개선은 [Taylor Otwell](https://github.com/taylorotwell)이 기여하였으며, [Spatie](https://spatie.be)에서 영감을 받았습니다._

<!-- In previous releases of Laravel, the `php artisan down` maintenance mode feature may be bypassed using an "allow list" of IP addresses that were allowed to access the application. This feature has been removed in favor of a simpler "secret" / token solution. -->
기존 Laravel 릴리스에서는 `php artisan down` 유지보수 모드에서 허용된 IP 주소를 "허용 목록(allow list)"으로 지정하여 애플리케이션에 접속할 수 있었습니다. 이제 이 기능은 더 간단한 "시크릿(토큰)" 방식으로 변경되었습니다.

<!-- While in maintenance mode, you may use the `secret` option to specify a maintenance mode bypass token: -->
유지보수 모드에서 `secret` 옵션을 사용해 우회 토큰을 지정할 수 있습니다.

```
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
애플리케이션을 유지보수 모드로 변경한 후에는, 지정한 토큰이 포함된 애플리케이션 URL로 접속하면 Laravel이 브라우저에 유지보수 모드 우회 쿠키를 발급합니다.

<!--     https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515 -->
    https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
이 숨겨진 경로로 접속하면, 애플리케이션의 `/` 경로로 리다이렉션됩니다. 쿠키가 발급되면, 유지보수 모드가 해제된 것처럼 사이트를 정상적으로 탐색할 수 있습니다.

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering The Maintenance Mode View -->
#### Pre-Rendering The Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
배포 중에 `php artisan down` 명령어를 사용한다면, Composer 의존성이나 기타 인프라 구성이 갱신되는 사이에 사용자가 애플리케이션 접속 시 오류를 경험할 수 있습니다. 이는 Laravel 프레임워크의 주요 부분이 부팅되어야만 애플리케이션이 유지보수 모드임을 판별하고, 템플릿 엔진으로 유지보수 뷰를 렌더링하기 때문입니다.

<!-- For this reason, Laravel now allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
이 문제를 해결하기 위해, Laravel은 요청 초기에 반환할 유지보수 뷰를 미리 렌더링(pre-render)할 수 있도록 지원합니다. 이 뷰는 애플리케이션의 어떤 의존성도 로드되기 전에 렌더링되어 반환됩니다. 원하는 템플릿을 `down` 명령의 `render` 옵션에 지정하여 사전 렌더할 수 있습니다.

```
php artisan down --render="errors::503"
```

<a name="closure-dispatch-chain-catch"></a>
<!-- ### Closure Dispatch / Chain `catch` -->
### Closure Dispatch / Chain `catch`

<!-- _Catch improvements were contributed by [Mohamed Said](https://github.com/themsaid)_. -->
_Catch 개선 기능은 [Mohamed Said](https://github.com/themsaid)가 기여하였습니다._

<!-- Using the new `catch` method, you may now provide a closure that should be executed if a queued closure fails to complete successfully after exhausting all of your queue's configured retry attempts: -->
새로운 `catch` 메서드를 사용하면, 큐 처리 중인 클로저가 모든 재시도 횟수를 소모하고도 성공하지 못했을 때 실행할 클로저를 제공합니다.

```
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```

<a name="dynamic-blade-components"></a>
<!-- ### Dynamic Blade Components -->
### Dynamic Blade Components

<!-- _Dynamic Blade components were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_동적 Blade 컴포넌트는 [Taylor Otwell](https://github.com/taylorotwell)이 기여하였습니다._

<!-- Sometimes you may need to render a component but not know which component should be rendered until runtime. In this situation, you may now use Laravel's built-in `dynamic-component` component to render the component based on a runtime value or variable: -->
실행 시점에 어떤 컴포넌트를 렌더링할지 결정해야 할 때가 있습니다. 이런 경우, 내장 `dynamic-component` Blade 컴포넌트를 활용해 런타임 값 또는 변수에 따라 원하는 컴포넌트를 렌더링할 수 있습니다.

```
<x-dynamic-component :component="$componentName" class="mt-4" />
```

<!-- To learn more about Blade components, please consult the [Blade documentation](/docs/8.x/blade#components). -->
Blade 컴포넌트에 대해 더 자세히 알고 싶다면 [Blade documentation](/docs/8.x/blade#components)를 참고해 주세요.

<a name="event-listener-improvements"></a>
<!-- ### Event Listener Improvements -->
### Event Listener Improvements

<!-- _Event listener improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_이벤트 리스너 개선 기능은 [Taylor Otwell](https://github.com/taylorotwell)이 기여하였습니다._

<!-- Closure based event listeners may now be registered by only passing the closure to the `Event::listen` method. Laravel will inspect the closure to determine which type of event the listener handles: -->
이제 클로저 기반 이벤트 리스너를 등록할 때, `Event::listen` 메서드에 단순히 클로저만 전달하면 됩니다. Laravel은 해당 클로저가 어떤 타입의 이벤트를 처리하는지 자동으로 감지합니다.

```
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

Event::listen(function (PodcastProcessed $event) {
    //
});
```

<!-- In addition, closure based event listeners may now be marked as queueable using the `Illuminate\Events\queueable` function: -->
또한, 클로저 기반 이벤트 리스너를 `Illuminate\Events\queueable` 함수를 사용해 큐 처리가 가능하도록 등록할 수 있습니다.

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
}));
```

<!-- Like queued jobs, you may use the `onConnection`, `onQueue`, and `delay` methods to customize the execution of the queued listener: -->
큐에 등록된 작업처럼, `onConnection`, `onQueue`, `delay` 메서드를 활용하여 큐 리스너의 실행 방식을 커스터마이즈할 수 있습니다.

```
Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->onConnection('redis')->onQueue('podcasts')->delay(now()->addSeconds(10)));
```

<!-- If you would like to handle anonymous queued listener failures, you may provide a closure to the `catch` method while defining the `queueable` listener: -->
익명 큐 리스너 실패를 처리하고 싶다면, `queueable` 리스너를 정의할 때 `catch` 메서드에 클로저를 전달하면 됩니다.

```
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    //
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```

<a name="time-testing-helpers"></a>
<!-- ### Time Testing Helpers -->
### Time Testing Helpers

<!-- _Time testing helpers were contributed by [Taylor Otwell](https://github.com/taylorotwell) with inspiration from Ruby on Rails_. -->
_시간 테스트 헬퍼 기능은 [Taylor Otwell](https://github.com/taylorotwell)이 개발하였으며, Ruby on Rails에서 영감을 받았습니다._

<!-- When testing, you may occasionally need to modify the time returned by helpers such as `now` or `Illuminate\Support\Carbon::now()`. Laravel's base feature test class now includes helpers that allow you to manipulate the current time: -->
테스트를 작성하다 보면, `now` 혹은 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 조작해야 할 경우가 있습니다. Laravel의 기본 Feature Test 클래스에는 현재 시간을 간편하게 변경할 수 있는 헬퍼가 추가되어 있습니다.

```
public function testTimeCanBeManipulated()
{
    // Travel into the future...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->subHours(6));

    // Return back to the present time...
    $this->travelBack();
}
```

<a name="artisan-serve-improvements"></a>
<!-- ### Artisan `serve` Improvements -->
### Artisan `serve` Improvements

<!-- _Artisan `serve` improvements were contributed by [Taylor Otwell](https://github.com/taylorotwell)_. -->
_Artisan `serve` 개선 기능은 [Taylor Otwell](https://github.com/taylorotwell)이 기여하였습니다._

<!-- The Artisan `serve` command has been improved with automatic reloading when environment variable changes are detected within your local `.env` file. Previously, the command had to be manually stopped and restarted. -->
Artisan의 `serve` 명령어가, 로컬 `.env` 파일의 환경 변수 변경 사항을 자동으로 감지해서 서버를 자동 재시작하게 개선되었습니다. 기존에는 수동으로 서버를 중지하고 다시 시작해야 했습니다.

<a name="tailwind-pagination-views"></a>
<!-- ### Tailwind Pagination Views -->
### Tailwind Pagination Views

<!-- The Laravel paginator has been updated to use the [Tailwind CSS](https://tailwindcss.com) framework by default. Tailwind CSS is a highly customizable, low-level CSS framework that gives you all of the building blocks you need to build bespoke designs without any annoying opinionated styles you have to fight to override. Of course, Bootstrap 3 and 4 views remain available as well. -->
Laravel의 페이지네이터가 [Tailwind CSS](https://tailwindcss.com) 프레임워크를 기본적으로 사용하도록 업데이트되었습니다. Tailwind CSS는 매우 커스터마이즈가 쉽고, 필요한 디자인 컴포넌트를 자유롭게 조합할 수 있는 저수준 CSS 프레임워크입니다. (Bootstrap 3 및 4 기반의 뷰도 계속해서 사용할 수 있습니다.)

<a name="routing-namespace-updates"></a>
<!-- ### Routing Namespace Updates -->
### Routing Namespace Updates

<!-- In previous releases of Laravel, the `RouteServiceProvider` contained a `$namespace` property. This property's value would automatically be prefixed onto controller route definitions and calls to the `action` helper / `URL::action` method. In Laravel 8.x, this property is `null` by default. This means that no automatic namespace prefixing will be done by Laravel. Therefore, in new Laravel 8.x applications, controller route definitions should be defined using standard PHP callable syntax: -->
기존 Laravel 릴리스에서는 `RouteServiceProvider`에 `$namespace` 속성이 포함되어 있었으며, 이 값이 컨트롤러 라우트 정의나 `action` 헬퍼/`URL::action` 메서드 호출 시 자동으로 접두사로 추가되었습니다. Laravel 8.x에서는 이 속성값이 기본적으로 `null`로 세팅되어, Laravel이 자동으로 네임스페이스를 붙이지 않습니다. 따라서, 새로운 Laravel 8.x 애플리케이션에서는 아래와 같이 표준 PHP 콜러블(callable) 문법으로 컨트롤러 라우트를 정의해야 합니다.

```
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

<!-- Calls to the `action` related methods should use the same callable syntax: -->
`action` 관련 메서드 호출도 동일한 콜러블 문법을 사용해야 합니다.

```
action([UserController::class, 'index']);

return Redirect::action([UserController::class, 'index']);
```

<!-- If you prefer Laravel 7.x style controller route prefixing, you may simply add the `$namespace` property into your application's `RouteServiceProvider`. -->
만약, 기존 Laravel 7.x 스타일의 컨트롤러 네임스페이스 접두사를 선호한다면, 애플리케이션의 `RouteServiceProvider`에 `$namespace` 속성을 추가하면 됩니다.

> [!NOTE]
> 이 변경은 새로운 Laravel 8.x 애플리케이션에만 영향을 줍니다. Laravel 7.x에서 업그레이드하는 애플리케이션은 여전히 `RouteServiceProvider`에 `$namespace` 속성이 존재합니다.
