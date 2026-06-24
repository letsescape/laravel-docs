<!-- # Laravel Pulse -->
# Laravel Pulse

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Dashboard](#dashboard)
    - [Authorization](#dashboard-authorization)
    - [Customization](#dashboard-customization)
    - [Resolving Users](#dashboard-resolving-users)
    - [Cards](#dashboard-cards)
- [Capturing Entries](#capturing-entries)
    - [Recorders](#recorders)
    - [Filtering](#filtering)
- [Performance](#performance)
    - [Using a Different Database](#using-a-different-database)
    - [Redis Ingest](#ingest)
    - [Sampling](#sampling)
    - [Trimming](#trimming)
    - [Handling Pulse Exceptions](#pulse-exceptions)
- [Custom Cards](#custom-cards)
    - [Card Components](#custom-card-components)
    - [Styling](#custom-card-styling)
    - [Data Capture and Aggregation](#custom-card-data)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Pulse](https://github.com/laravel/pulse) delivers at-a-glance insights into your application's performance and usage. With Pulse, you can track down bottlenecks like slow jobs and endpoints, find your most active users, and more. -->
[Laravel Pulse](https://github.com/laravel/pulse)는 애플리케이션의 성능과 사용 현황을 한눈에 파악할 수 있는 인사이트를 제공합니다. Pulse를 사용하면 느린 작업 및 엔드포인트와 같은 병목 현상을 추적하고, 가장 활발한 사용자를 찾아내는 등 다양한 정보를 확인할 수 있습니다.

<!-- For in-depth debugging of individual events, check out [Laravel Telescope](/docs/master/telescope). -->
개별 이벤트에 대한 심층적인 디버깅이 필요한 경우에는 [Laravel Telescope](/docs/master/telescope)를 참고하시기 바랍니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Pulse의 1차 저장소 구현에서는 현재 MySQL, MariaDB, PostgreSQL 데이터베이스가 필요합니다. 다른 데이터베이스 엔진을 사용하는 경우, Pulse 데이터를 위해 별도의 MySQL, MariaDB, 또는 PostgreSQL 데이터베이스를 준비해야 합니다.

<!-- You may install Pulse using the Composer package manager: -->
Composer 패키지 관리자를 사용하여 Pulse를 설치할 수 있습니다:

```shell
composer require laravel/pulse
```

<!-- Next, you should publish the Pulse configuration and migration files using the `vendor:publish` Artisan command: -->
다음으로 `vendor:publish` Artisan 명령어를 실행하여 Pulse 설정 및 마이그레이션 파일을 배포해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

<!-- Finally, you should run the `migrate` command in order to create the tables needed to store Pulse's data: -->
마지막으로, Pulse 데이터를 저장하기 위해 필요한 테이블을 생성하려면 `migrate` 명령어를 실행해야 합니다:

```shell
php artisan migrate
```

<!-- Once Pulse's database migrations have been run, you may access the Pulse dashboard via the `/pulse` route. -->
Pulse 데이터베이스 마이그레이션이 완료되면, `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스에 저장하고 싶지 않은 경우, [specify a dedicated database connection](#using-a-different-database)할 수 있습니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Many of Pulse's configuration options can be controlled using environment variables. To see the available options, register new recorders, or configure advanced options, you may publish the `config/pulse.php` configuration file: -->
Pulse의 많은 설정 옵션들은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나, 새로운 레코더를 등록하거나, 고급 설정을 구성하려면 `config/pulse.php` 설정 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
<!-- ## Dashboard -->
## Dashboard

<a name="dashboard-authorization"></a>
<!-- ### Authorization -->
### Authorization

<!-- The Pulse dashboard may be accessed via the `/pulse` route. By default, you will only be able to access this dashboard in the `local` environment, so you will need to configure authorization for your production environments by customizing the `'viewPulse'` authorization gate. You can accomplish this within your application's `app/Providers/AppServiceProvider.php` file: -->
Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 가능하므로, 운영 환경에서는 `'viewPulse'` 인가 게이트를 사용자 지정해야 합니다. 이는 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일 내에서 설정할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('viewPulse', function (User $user) {
        return $user->isAdmin();
    });

    // ...
}
```

<a name="dashboard-customization"></a>
<!-- ### Customization -->
### Customization

<!-- The Pulse dashboard cards and layout may be configured by publishing the dashboard view. The dashboard view will be published to `resources/views/vendor/pulse/dashboard.blade.php`: -->
Pulse 대시보드의 카드 및 레이아웃은 대시보드 뷰를 게시하여 구성할 수 있습니다. 대시보드 뷰는 `resources/views/vendor/pulse/dashboard.blade.php` 경로에 게시됩니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```

<!-- The dashboard is powered by [Livewire](https://livewire.laravel.com/), and allows you to customize the cards and layout without needing to rebuild any JavaScript assets. -->
대시보드는 [Livewire](https://livewire.laravel.com/)로 구동되며, 어떤 자바스크립트 에셋을 다시 빌드하지 않아도 카드와 레이아웃을 사용자 지정할 수 있습니다.

<!-- Within this file, the `<x-pulse>` component is responsible for rendering the dashboard and provides a grid layout for the cards. If you would like the dashboard to span the full width of the screen, you may provide the `full-width` prop to the component: -->
이 파일 내에서 `<x-pulse>` 컴포넌트가 대시보드 렌더링을 담당하며, 카드들을 위한 그리드 레이아웃을 제공합니다. 대시보드를 화면 전체 너비로 확장하려면 `full-width` prop을 추가하면 됩니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

<!-- By default, the `<x-pulse>` component will create a 12 column grid, but you may customize this using the `cols` prop: -->
기본적으로 `<x-pulse>` 컴포넌트는 12 컬럼 그리드를 생성하지만, `cols` prop을 사용해 컬럼 수를 변경할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

<!-- Each card accepts a `cols` and `rows` prop to control the space and positioning: -->
각 카드는 공간 및 위치를 제어하기 위해 `cols`와 `rows` prop을 지원합니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

<!-- Most cards also accept an `expand` prop to show the full card instead of scrolling: -->
대부분의 카드에서는 스크롤 대신 전체 카드를 표시할 수 있도록 `expand` prop을 지원합니다:

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
<!-- ### Resolving Users -->
### Resolving Users

<!-- For cards that display information about your users, such as the Application Usage card, Pulse will only record the user's ID. When rendering the dashboard, Pulse will resolve the `name` and `email` fields from your default `Authenticatable` model and display avatars using the Gravatar web service. -->
사용자 관련 정보를 표시하는 카드(예: Application Usage 카드)에서는 Pulse가 사용자의 ID만을 기록합니다. 대시보드를 렌더링할 때, Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 조회하고, 아바타는 Gravatar 웹 서비스를 사용해 표시합니다.

<!-- You may customize the fields and avatar by invoking the `Pulse::user` method within your application's `App\Providers\AppServiceProvider` class. -->
필드와 아바타를 변경하고 싶다면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `Pulse::user` 메서드를 호출하여 사용자 지정할 수 있습니다.

<!-- The `user` method accepts a closure which will receive the `Authenticatable` model to be displayed and should return an array containing `name`, `extra`, and `avatar` information for the user: -->
`user` 메서드는 `Authenticatable` 모델 인스턴스를 받아 `name`, `extra`, `avatar` 정보를 포함하는 배열을 반환하는 클로저를 받습니다:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::user(fn ($user) => [
        'name' => $user->name,
        'extra' => $user->email,
        'avatar' => $user->avatar_url,
    ]);

    // ...
}
```

> [!NOTE]
> 인증된 사용자를 캡처하고 조회하는 방법을 완전히 사용자 지정하려면 `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고, Laravel의 [service container](/docs/master/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
<!-- ### Cards -->
### Cards

<a name="servers-card"></a>
<!-- #### Servers -->
#### Servers

<!-- The `<livewire:pulse.servers />` card displays system resource usage for all servers running the `pulse:check` command. Please refer to the documentation regarding the [servers recorder](#servers-recorder) for more information on system resource reporting. -->
`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 리소스 사용량을 표시합니다. 시스템 리소스 리포팅에 대한 자세한 내용은 [servers recorder](#servers-recorder) 문서를 참고하세요.

<!-- If you replace a server in your infrastructure, you may wish to stop displaying the inactive server in the Pulse dashboard after a given duration. You may accomplish this using the `ignore-after` prop, which accepts the number of seconds after which inactive servers should be removed from the Pulse dashboard. Alternatively, you may provide a relative time formatted string, such as `1 hour` or `3 days and 1 hour`: -->
인프라에서 서버를 교체한 경우, Pulse 대시보드에 일정 시간 이후 비활성화된 서버를 표시하지 않도록 할 수 있습니다. 이 경우, 비활성 서버가 대시보드에서 제거되는 시간을 초 단위로 지정하는 `ignore-after` prop을 사용할 수 있습니다. 또는 `1 hour`, `3 days and 1 hour`와 같은 상대적 시간 형식의 문자열도 지정할 수 있습니다:

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
<!-- #### Application Usage -->
#### Application Usage

<!-- The `<livewire:pulse.usage />` card displays the top 10 users making requests to your application, dispatching jobs, and experiencing slow requests. -->
`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나, 작업을 디스패치하거나, 느린 요청을 경험한 상위 10명의 사용자를 표시합니다.

<!-- If you wish to view all usage metrics on screen at the same time, you may include the card multiple times and specify the `type` attribute: -->
화면에서 모든 사용량 지표를 동시에 보고 싶다면, 카드를 여러 번 포함하고 `type` 속성을 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

<!-- To learn how to customize how Pulse retrieves and displays user information, consult our documentation on [resolving users](#dashboard-resolving-users). -->
Pulse가 사용자 정보를 어떻게 조회하고 표시하는지 사용자 지정하는 방법은 [resolving users](#dashboard-resolving-users) 문서를 참고하세요.

> [!NOTE]
> 애플리케이션에 요청이 많이 들어오거나 작업이 자주 디스패치되는 경우, [sampling](#sampling) 기능을 활성화하는 것이 좋습니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="exceptions-card"></a>
<!-- #### Exceptions -->
#### Exceptions

<!-- The `<livewire:pulse.exceptions />` card shows the frequency and recency of exceptions occurring in your application. By default, exceptions are grouped based on the exception class and location where it occurred. See the [exceptions recorder](#exceptions-recorder) documentation for more information. -->
`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외의 빈도와 최신 발생 시점을 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치를 기준으로 그룹화됩니다. 자세한 내용은 [exceptions recorder](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
<!-- #### Queues -->
#### Queues

<!-- The `<livewire:pulse.queues />` card shows the throughput of the queues in your application, including the number of jobs queued, processing, processed, released, and failed. See the [queues recorder](#queues-recorder) documentation for more information. -->
`<livewire:pulse.queues />` 카드는 애플리케이션의 큐 처리량을 표시합니다. 대기, 처리 중, 처리 완료, 다시 대기, 실패한 작업 수 등을 포함합니다. 자세한 내용은 [queues recorder](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
<!-- #### Slow Requests -->
#### Slow Requests

<!-- The `<livewire:pulse.slow-requests />` card shows incoming requests to your application that exceed the configured threshold, which is 1,000ms by default. See the [slow requests recorder](#slow-requests-recorder) documentation for more information. -->
`<livewire:pulse.slow-requests />` 카드는 기본값으로 1,000ms 임계값을 초과한 애플리케이션의 요청을 보여줍니다. 자세한 내용은 [slow requests recorder](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
<!-- #### Slow Jobs -->
#### Slow Jobs

<!-- The `<livewire:pulse.slow-jobs />` card shows the queued jobs in your application that exceed the configured threshold, which is 1,000ms by default. See the [slow jobs recorder](#slow-jobs-recorder) documentation for more information. -->
`<livewire:pulse.slow-jobs />` 카드는 기본값으로 1,000ms 임계값을 초과한 대기 작업을 표시합니다. 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
<!-- #### Slow Queries -->
#### Slow Queries

<!-- The `<livewire:pulse.slow-queries />` card shows the database queries in your application that exceed the configured threshold, which is 1,000ms by default. -->
`<livewire:pulse.slow-queries />` 카드는 기본적으로 1,000ms 임계값을 초과한 데이터베이스 쿼리를 보여줍니다.

<!-- By default, slow queries are grouped based on the SQL query (without bindings) and the location where it occurred, but you may choose to not capture the location if you wish to group solely on the SQL query. -->
기본적으로 느린 쿼리는 SQL 쿼리(바인딩 제외)와 발생 위치 기준으로 그룹화됩니다. 쿼리 위치를 캡처하지 않고 SQL 쿼리 기준으로만 그룹화할 수도 있습니다.

<!-- If you encounter rendering performance issues due to extremely large SQL queries receiving syntax highlighting, you may disable highlighting by adding the `without-highlighting` prop: -->
아주 긴 SQL 쿼리에 구문 강조가 적용되어 렌더링 성능 문제가 발생한다면, `without-highlighting` prop을 추가해 강조를 비활성화할 수 있습니다:

```blade
<livewire:pulse.slow-queries without-highlighting />
```

<!-- See the [slow queries recorder](#slow-queries-recorder) documentation for more information. -->
자세한 내용은 [slow queries recorder](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
<!-- #### Slow Outgoing Requests -->
#### Slow Outgoing Requests

<!-- The `<livewire:pulse.slow-outgoing-requests />` card shows outgoing requests made using Laravel's [HTTP client](/docs/master/http-client) that exceed the configured threshold, which is 1,000ms by default. -->
`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP client](/docs/master/http-client)로 발생시킨 외부 요청 중 설정된 임계값(기본값 1,000ms)을 초과한 요청을 보여줍니다.

<!-- By default, entries will be grouped by the full URL. However, you may wish to normalize or group similar outgoing requests using regular expressions. See the [slow outgoing requests recorder](#slow-outgoing-requests-recorder) documentation for more information. -->
기본적으로 모든 엔트리를 전체 URL 기준으로 그룹화합니다. 그러나 정규 표현식을 사용해 유사한 요청을 그룹화하거나 정규화할 수도 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
<!-- #### Cache -->
#### Cache

<!-- The `<livewire:pulse.cache />` card shows the cache hit and miss statistics for your application, both globally and for individual keys. -->
`<livewire:pulse.cache />` 카드는 애플리케이션의 캐시 적중 및 실패 통계를 전역 및 키별로 보여줍니다.

<!-- By default, entries will be grouped by key. However, you may wish to normalize or group similar keys using regular expressions. See the [cache interactions recorder](#cache-interactions-recorder) documentation for more information. -->
기본적으로 엔트리는 키별로 그룹화되나, 정규 표현식을 사용해 유사한 키를 그룹화할 수도 있습니다. 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
<!-- ## Capturing Entries -->
## Capturing Entries

<!-- Most Pulse recorders will automatically capture entries based on framework events dispatched by Laravel. However, the [servers recorder](#servers-recorder) and some third-party cards must poll for information regularly. To use these cards, you must run the `pulse:check` daemon on all of your individual application servers: -->
대부분의 Pulse 레코더는 Laravel에서 발생하는 프레임워크 이벤트를 기반으로 자동으로 엔트리를 캡처합니다. 하지만 [servers recorder](#servers-recorder) 및 일부 서드파티 카드는 주기적으로 정보를 폴링해야 합니다. 이러한 카드들을 사용하려면 각 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다:

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 항상 백그라운드에서 실행하려면, Supervisor와 같은 프로세스 모니터를 사용하여 명령어가 멈추지 않도록 해야 합니다.

<!-- As the `pulse:check` command is a long-lived process, it will not see changes to your codebase without being restarted. You should gracefully restart the command by calling the `pulse:restart` command during your application's deployment process: -->
`pulse:check` 명령어는 장기 실행 프로세스이므로 코드베이스 변경을 감지하지 못합니다. 배포 과정에서 `pulse:restart` 명령어를 호출하여 프로세스를 정상적으로 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [cache](/docs/master/cache)를 사용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션에 캐시 드라이버가 제대로 구성되어 있는지 확인하세요.

<a name="recorders"></a>
<!-- ### Recorders -->
### Recorders

<!-- Recorders are responsible for capturing entries from your application to be recorded in the Pulse database. Recorders are registered and configured in the `recorders` section of the [Pulse configuration file](#configuration). -->
레코더는 애플리케이션에서 수집된 엔트리를 Pulse 데이터베이스에 저장하는 역할을 합니다. 레코더는 [Pulse configuration file](#configuration)의 `recorders` 섹션에 등록 및 구성됩니다.

<a name="cache-interactions-recorder"></a>
<!-- #### Cache Interactions -->
#### Cache Interactions

<!-- The `CacheInteractions` recorder captures information about the [cache](/docs/master/cache) hits and misses occurring in your application for display on the [Cache](#cache-card) card. -->
`CacheInteractions` 레코더는 [cache](/docs/master/cache)의 적중/실패 정보를 [Cache](#cache-card) 카드에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored key patterns. -->
[sample rate](#sampling)과 무시할 키 패턴을 선택적으로 조정할 수 있습니다.

<!-- You may also configure key grouping so that similar keys are grouped as a single entry. For example, you may wish to remove unique IDs from keys caching the same type of information. Groups are configured using a regular expression to "find and replace" parts of the key. An example is included in the configuration file: -->
비슷한 키를 하나의 엔트리로 그룹화하는 키 그룹화도 설정할 수 있습니다. 예를 들어, 동일한 유형의 정보를 캐싱하는 고유 ID를 키에서 제거할 수 있습니다. 그룹은 정규 표현식으로 키 일부를 "찾아 바꾸기" 방식으로 구성합니다. 설정 파일에 예시가 포함되어 있습니다:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

<!-- The first pattern that matches will be used. If no patterns match, then the key will be captured as-is. -->
일치하는 첫 번째 패턴이 사용됩니다. 일치하는 패턴이 없으면 키가 그대로 캡처됩니다.

<a name="exceptions-recorder"></a>
<!-- #### Exceptions -->
#### Exceptions

<!-- The `Exceptions` recorder captures information about reportable exceptions occurring in your application for display on the [Exceptions](#exceptions-card) card. -->
`Exceptions` 레코더는 애플리케이션에서 발생한 리포트 가능한 예외의 정보를 [Exceptions](#exceptions-card) 카드에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored exception patterns. You may also configure whether to capture the location that the exception originated from. The captured location will be displayed on the Pulse dashboard which can help to track down the exception origin; however, if the same exception occurs in multiple locations then it will appear multiple times for each unique location. -->
[sample rate](#sampling)과 무시할 예외 패턴을 선택적으로 조정할 수 있습니다. 예외가 발생한 위치를 캡처할지 여부도 설정할 수 있습니다. 캡처한 위치 정보는 Pulse 대시보드에 표시되어 예외의 근원을 추적하는 데 도움이 됩니다. 동일한 예외가 여러 위치에서 발생하면, 각각의 고유 위치마다 여러 번 나타납니다.

<a name="queues-recorder"></a>
<!-- #### Queues -->
#### Queues

<!-- The `Queues` recorder captures information about your application's queues for display on the [Queues](#queues-card). -->
`Queues` 레코더는 애플리케이션의 큐 정보를 [Queues](#queues-card) 카드에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored jobs patterns. -->
[sample rate](#sampling)과 무시할 작업 패턴을 선택적으로 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
<!-- #### Slow Jobs -->
#### Slow Jobs

<!-- The `SlowJobs` recorder captures information about slow jobs occurring in your application for display on the [Slow Jobs](#slow-jobs-recorder) card. -->
`SlowJobs` 레코더는 애플리케이션에서 발생한 느린 작업 정보를 [Slow Jobs](#slow-jobs-recorder) 카드에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the slow job threshold, [sample rate](#sampling), and ignored job patterns. -->
느린 작업 임계값, [sample rate](#sampling), 무시할 작업 패턴을 선택적으로 조정할 수 있습니다.

<!-- You may have some jobs that you expect to take longer than others. In those cases, you may configure per-job thresholds: -->
특정 작업이 다른 작업보다 오랜 시간이 걸릴 것으로 예상된다면, 작업별 임계값을 설정할 수 있습니다:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```

<!-- If no regular expression patterns match the job's classname, then the `'default'` value will be used. -->
정규 표현식 패턴이 작업 클래스명과 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
<!-- #### Slow Outgoing Requests -->
#### Slow Outgoing Requests

<!-- The `SlowOutgoingRequests` recorder captures information about outgoing HTTP requests made using Laravel's [HTTP client](/docs/master/http-client) that exceed the configured threshold for display on the [Slow Outgoing Requests](#slow-outgoing-requests-card) card. -->
`SlowOutgoingRequests` 레코더는 Laravel의 [HTTP client](/docs/master/http-client)를 사용해 발생한 외부 요청 중 임계값을 초과한 요청 정보를 [Slow Outgoing Requests](#slow-outgoing-requests-card) 카드에 표시합니다.

<!-- You may optionally adjust the slow outgoing request threshold, [sample rate](#sampling), and ignored URL patterns. -->
느린 외부 요청 임계값, [sample rate](#sampling), 무시할 URL 패턴을 선택적으로 조정할 수 있습니다.

<!-- You may have some outgoing requests that you expect to take longer than others. In those cases, you may configure per-request thresholds: -->
특정 요청이 다른 요청보다 오래 걸릴 것으로 예상된다면, 요청별 임계값을 설정할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```

<!-- If no regular expression patterns match the request's URL, then the `'default'` value will be used. -->
정규 표현식 패턴이 요청의 URL과 일치하지 않으면 `'default'` 값이 사용됩니다.

<!-- You may also configure URL grouping so that similar URLs are grouped as a single entry. For example, you may wish to remove unique IDs from URL paths or group by domain only. Groups are configured using a regular expression to "find and replace" parts of the URL. Some examples are included in the configuration file: -->
또한 유사한 URL을 하나의 엔트리로 그룹화할 수도 있습니다. 예를 들어, 고유 ID가 포함된 URL 경로나 도메인별로 그룹화할 수 있습니다. 그룹은 정규 표현식으로 URL 일부를 "찾아 바꾸기"하는 방식으로 구성합니다. 설정 파일에 몇 가지 예시가 포함되어 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'groups' => [
        // '#^https://api\.github\.com/repos/.*$#' => 'api.github.com/repos/*',
        // '#^https?://([^/]*).*$#' => '\1',
        // '#/\d+#' => '/*',
    ],
],
```

<!-- The first pattern that matches will be used. If no patterns match, then the URL will be captured as-is. -->
일치하는 첫 번째 패턴이 적용되며, 매칭되는 패턴이 없으면 URL이 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
<!-- #### Slow Queries -->
#### Slow Queries

<!-- The `SlowQueries` recorder captures any database queries in your application that exceed the configured threshold for display on the [Slow Queries](#slow-queries-card) card. -->
`SlowQueries` 레코더는 지정된 임계값을 초과하는 모든 데이터베이스 쿼리를 [Slow Queries](#slow-queries-card) 카드에 표시하기 위해 캡처합니다.

<!-- You may optionally adjust the slow query threshold, [sample rate](#sampling), and ignored query patterns. You may also configure whether to capture the query location. The captured location will be displayed on the Pulse dashboard which can help to track down the query origin; however, if the same query is made in multiple locations then it will appear multiple times for each unique location. -->
느린 쿼리 임계값, [sample rate](#sampling), 무시할 쿼리 패턴을 선택적으로 조정할 수 있습니다. 쿼리 위치를 캡처할지 여부도 설정이 가능합니다. 캡처한 위치 정보는 Pulse 대시보드에 나타나 쿼리의 근원을 추적하는 데 도움이 됩니다. 동일 쿼리가 여러 위치에서 발생하면 각 위치마다 별도 항목으로 표시됩니다.

<!-- You may have some queries that you expect to take longer than others. In those cases, you may configure per-query thresholds: -->
특정 쿼리가 다른 쿼리보다 오래 걸릴 것으로 예상되면 쿼리별 임계값을 설정할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```

<!-- If no regular expression patterns match the query's SQL, then the `'default'` value will be used. -->
정규 표현식 패턴이 쿼리 SQL과 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
<!-- #### Slow Requests -->
#### Slow Requests

<!-- The `Requests` recorder captures information about requests made to your application for display on the [Slow Requests](#slow-requests-card) and [Application Usage](#application-usage-card) cards. -->
`Requests` 레코더는 애플리케이션에 들어온 요청 정보를 [Slow Requests](#slow-requests-card) 및 [Application Usage](#application-usage-card) 카드에 표시하기 위해 캡처합니다.

<!-- You may optionally adjust the slow route threshold, [sample rate](#sampling), and ignored paths. -->
느린 경로 임계값, [sample rate](#sampling), 무시할 경로를 선택적으로 조정할 수 있습니다.

<!-- You may have some requests that you expect to take longer than others. In those cases, you may configure per-request thresholds: -->
특정 요청에 대해 더 긴 시간을 허용하고 싶을 때, 요청별 임계값을 설정할 수 있습니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```

<!-- If no regular expression patterns match the request's URL, then the `'default'` value will be used. -->
정규 표현식 패턴이 요청 URL과 일치하지 않으면 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
<!-- #### Servers -->
#### Servers

<!-- The `Servers` recorder captures CPU, memory, and storage usage of the servers that power your application for display on the [Servers](#servers-card) card. This recorder requires the [pulse:check command](#capturing-entries) to be running on each of the servers you wish to monitor. -->
`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 저장소 사용량을 [Servers](#servers-card) 카드에 표시하기 위해 캡처합니다. 이 레코더는 [pulse:check command](#capturing-entries)를 각 모니터링 대상 서버에서 실행해야 합니다.

<!-- Each reporting server must have a unique name. By default, Pulse will use the value returned by PHP's `gethostname` function. If you wish to customize this, you may set the `PULSE_SERVER_NAME` environment variable: -->
각 서버는 고유한 이름을 가져야 합니다. 기본적으로 Pulse는 PHP의 `gethostname` 함수로 반환되는 값을 사용합니다. 이를 사용자 지정하려면 `PULSE_SERVER_NAME` 환경 변수를 설정할 수 있습니다:

```env
PULSE_SERVER_NAME=load-balancer
```

<!-- The Pulse configuration file also allows you to customize the directories that are monitored. -->
Pulse 설정 파일에서 모니터링할 디렉터리도 사용자 지정할 수 있습니다.

<a name="user-jobs-recorder"></a>
<!-- #### User Jobs -->
#### User Jobs

<!-- The `UserJobs` recorder captures information about the users dispatching jobs in your application for display on the [Application Usage](#application-usage-card) card. -->
`UserJobs` 레코더는 사용자가 디스패치한 작업의 정보를 [Application Usage](#application-usage-card) 카드에 표시하기 위해 캡처합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored job patterns. -->
[sample rate](#sampling), 무시할 작업 패턴을 선택적으로 조정할 수 있습니다.

<a name="user-requests-recorder"></a>
<!-- #### User Requests -->
#### User Requests

<!-- The `UserRequests` recorder captures information about the users making requests to your application for display on the [Application Usage](#application-usage-card) card. -->
`UserRequests` 레코더는 사용자가 보낸 요청 정보를 [Application Usage](#application-usage-card) 카드에 표시하기 위해 캡처합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored URL patterns. -->
[sample rate](#sampling), 무시할 URL 패턴을 선택적으로 조정할 수 있습니다.

<a name="filtering"></a>
<!-- ### Filtering -->
### Filtering

<!-- As we have seen, many [recorders](#recorders) offer the ability to, via configuration, "ignore" incoming entries based on their value, such as a request's URL. But, sometimes it may be useful to filter out records based on other factors, such as the currently authenticated user. To filter out these records, you may pass a closure to Pulse's `filter` method. Typically, the `filter` method should be invoked within the `boot` method of your application's `AppServiceProvider`: -->
앞서 설명한 것처럼 많은 [recorders](#recorders)는 설정을 통해 요청의 URL 등 값에 기반해 엔트리를 "무시"하도록 할 수 있습니다. 그러나 때로는 현재 인증된 사용자 등 다른 조건을 기준으로 레코드를 필터링해야 할 수도 있습니다. 이 경우, Pulse의 `filter` 메서드에 클로저를 전달해 엔트리를 필터링할 수 있습니다. 일반적으로 `AppServiceProvider`의 `boot` 메서드 내에서 `filter` 메서드를 호출합니다:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::filter(function (Entry|Value $entry) {
        return Auth::user()->isNotAdmin();
    });

    // ...
}
```

<a name="performance"></a>
<!-- ## Performance -->
## Performance

<!-- Pulse has been designed to drop into an existing application without requiring any additional infrastructure. However, for high-traffic applications, there are several ways of removing any impact Pulse may have on your application's performance. -->
Pulse는 별도의 추가 인프라 없이 기존 애플리케이션에 바로 적용할 수 있도록 설계되었습니다. 하지만 트래픽이 많은 애플리케이션의 경우, Pulse가 애플리케이션 성능에 영향을 주지 않도록 여러 방법을 적용할 수 있습니다.

<a name="using-a-different-database"></a>
<!-- ### Using a Different Database -->
### Using a Different Database

<!-- For high-traffic applications, you may prefer to use a dedicated database connection for Pulse to avoid impacting your application database. -->
트래픽이 많은 애플리케이션에서는 Pulse 전용 데이터베이스 연결을 사용하여 애플리케이션 DB에 영향을 주지 않도록 할 수 있습니다.

<!-- You may customize the [database connection](/docs/master/database#configuration) used by Pulse by setting the `PULSE_DB_CONNECTION` environment variable. -->
Pulse에서 사용하는 [database connection](/docs/master/database#configuration)은 `PULSE_DB_CONNECTION` 환경 변수를 통해 지정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
<!-- ### Redis Ingest -->
### Redis Ingest

> [!WARNING]
> Redis 인제스트 기능은 Redis 6.2 이상과 애플리케이션의 Redis 클라이언트 드라이버로 `phpredis` 또는 `predis`가 필요합니다.

<!-- By default, Pulse will store entries directly to the [configured database connection](#using-a-different-database) after the HTTP response has been sent to the client or a job has been processed; however, you may use Pulse's Redis ingest driver to send entries to a Redis stream instead. This can be enabled by configuring the `PULSE_INGEST_DRIVER` environment variable: -->
기본적으로 Pulse는 클라이언트에 HTTP 응답을 보낸 후 또는 작업 처리 후 [configured database connection](#using-a-different-database)에 엔트리를 바로 저장합니다. 하지만 Pulse의 Redis 인제스트 드라이버를 이용하여 엔트리를 Redis 스트림으로 전송할 수도 있습니다. 이를 사용하려면 `PULSE_INGEST_DRIVER` 환경 변수를 설정합니다:

```ini
PULSE_INGEST_DRIVER=redis
```

<!-- Pulse will use your default [Redis connection](/docs/master/redis#configuration) by default, but you may customize this via the `PULSE_REDIS_CONNECTION` environment variable: -->
Pulse는 기본적으로 기본 [Redis connection](/docs/master/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수로 따로 지정할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```

> [!WARNING]
> Redis 인제스트 드라이버를 사용할 경우, Pulse 설치에는 반드시 Redis 기반 큐와 다른 Redis 연결을 사용해야 합니다(해당되는 경우).

<!-- When using the Redis ingest, you will need to run the `pulse:work` command to monitor the stream and move entries from Redis into Pulse's database tables. -->
Redis 인제스트를 사용할 때는 `pulse:work` 명령어를 실행해 스트림을 모니터링하고, Redis에서 Pulse의 데이터베이스 테이블로 엔트리를 옮겨야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 항상 백그라운드에서 실행하려면 Supervisor와 같은 프로세스 모니터를 이용해 Pulse 워커가 중단되지 않도록 해야 합니다.

<!-- As the `pulse:work` command is a long-lived process, it will not see changes to your codebase without being restarted. You should gracefully restart the command by calling the `pulse:restart` command during your application's deployment process: -->
`pulse:work` 명령어는 장기 실행 프로세스이므로 코드베이스 변경을 바로 감지하지 않습니다. 애플리케이션 배포 과정에서 `pulse:restart` 명령어를 호출해 프로세스를 정상적으로 재시작해야 합니다:

```shell
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [cache](/docs/master/cache)를 이용해 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 캐시 드라이버가 애플리케이션에 제대로 구성되어 있는지 확인하세요.

<a name="sampling"></a>
<!-- ### Sampling -->
### Sampling

<!-- By default, Pulse will capture every relevant event that occurs in your application. For high-traffic applications, this can result in needing to aggregate millions of database rows in the dashboard, especially for longer time periods. -->
기본적으로 Pulse는 애플리케이션에서 발생하는 모든 관련 이벤트를 수집합니다. 트래픽이 많은 애플리케이션에서는 긴 기간 동안 수백만 개의 데이터베이스 행이 대시보드에서 집계될 수 있습니다.

<!-- You may instead choose to enable "sampling" on certain Pulse data recorders. For example, setting the sample rate to `0.1` on the [User Requests](#user-requests-recorder) recorder will mean that you only record approximately 10% of the requests to your application. In the dashboard, the values will be scaled up and prefixed with a `~` to indicate that they are an approximation. -->
이 경우, 일부 Pulse 데이터 레코더에서 "샘플링"을 활성화할 수 있습니다. 예를 들어, [User Requests](#user-requests-recorder) 레코더의 샘플링 비율을 `0.1`로 설정하면 전체 요청 중 약 10%만 저장합니다. 대시보드에서는 값 앞에 `~`가 붙으며, 이는 값이 추정치임을 의미합니다.

<!-- In general, the more entries you have for a particular metric, the lower you can safely set the sample rate without sacrificing too much accuracy. -->
집계 데이터가 많을수록 샘플링 비율을 더 낮춰도 정확도에 크게 영향을 주지 않습니다.

<a name="trimming"></a>
<!-- ### Trimming -->
### Trimming

<!-- Pulse will automatically trim its stored entries once they are outside of the dashboard window. Trimming occurs when ingesting data using a lottery system which may be customized in the Pulse [configuration file](#configuration). -->
Pulse는 대시보드에서 설정한 기간을 벗어난 저장 엔트리를 자동으로 정리합니다. 트리밍은 데이터 인제스트 시 로터리 시스템을 통해 동작하며, Pulse [configuration file](#configuration)에서 사용자 지정할 수 있습니다.

<a name="pulse-exceptions"></a>
<!-- ### Handling Pulse Exceptions -->
### Handling Pulse Exceptions

<!-- If an exception occurs while capturing Pulse data, such as being unable to connect to the storage database, Pulse will silently fail to avoid impacting your application. -->
Pulse 데이터 수집 중, 예를 들어 저장소 데이터베이스 연결 실패 등 예외가 발생하면, 애플리케이션에 영향을 주지 않도록 Pulse는 조용히 실패합니다.

<!-- If you wish to customize how these exceptions are handled, you may provide a closure to the `handleExceptionsUsing` method: -->
이러한 예외 처리를 사용자 지정하고 싶을 때는 `handleExceptionsUsing` 메서드에 클로저를 전달할 수 있습니다.

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('An exception happened in Pulse', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```

<a name="custom-cards"></a>
<!-- ## Custom Cards -->
## Custom Cards

<!-- Pulse allows you to build custom cards to display data relevant to your application's specific needs. Pulse uses [Livewire](https://livewire.laravel.com), so you may want to [review its documentation](https://livewire.laravel.com/docs) before building your first custom card. -->
Pulse는 애플리케이션 특성에 맞는 데이터를 표시할 수 있도록 커스텀 카드를 제작할 수 있게 지원합니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 커스텀 카드를 처음 작성하기 전 [review its documentation](https://livewire.laravel.com/docs)를 참고하는 것이 좋습니다.

<a name="custom-card-components"></a>
<!-- ### Card Components -->
### Card Components

<!-- Creating a custom card in Laravel Pulse starts with extending the base `Card` Livewire component and defining a corresponding view: -->
Laravel Pulse에서 커스텀 카드를 만들려면, 기본 `Card` Livewire 컴포넌트를 상속하고 대응되는 뷰를 작성하면 됩니다:

```php
namespace App\Livewire\Pulse;

use Laravel\Pulse\Livewire\Card;
use Livewire\Attributes\Lazy;

#[Lazy]
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers');
    }
}
```

<!-- When using Livewire's [lazy loading](https://livewire.laravel.com/docs/lazy) feature, The `Card` component will automatically provide a placeholder that respects the `cols` and `rows` attributes passed to your component. -->
Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 사용할 때, `Card` 컴포넌트는 자동으로 `cols`, `rows` 속성이 전달된 플레이스홀더를 제공합니다.

<!-- When writing your Pulse card's corresponding view, you may leverage Pulse's Blade components for a consistent look and feel: -->
Pulse 카드의 대응 뷰를 작성할 때는, 일관된 디자인을 위해 Pulse에서 제공하는 Blade 컴포넌트를 활용할 수 있습니다:

```blade
<x-pulse::card :cols="$cols" :rows="$rows" :class="$class" wire:poll.5s="">
    <x-pulse::card-header name="Top Sellers">
        <x-slot:icon>
            ...
        </x-slot:icon>
    </x-pulse::card-header>

    <x-pulse::scroll :expand="$expand">
        ...
    </x-pulse::scroll>
</x-pulse::card>
```

<!-- The `$cols`, `$rows`, `$class`, and `$expand` variables should be passed to their respective Blade components so the card layout may be customized from the dashboard view. You may also wish to include the `wire:poll.5s=""` attribute in your view to have the card automatically update. -->
`$cols`, `$rows`, `$class`, `$expand` 변수는 각각 Blade 컴포넌트로 전달해야 대시보드 뷰에서 카드 레이아웃을 사용자 지정할 수 있습니다. 또한 `wire:poll.5s=""` 속성을 추가하면 카드가 주기적으로 자동 업데이트됩니다.

<!-- Once you have defined your Livewire component and template, the card may be included in your [dashboard view](#dashboard-customization): -->
Livewire 컴포넌트와 템플릿을 정의한 후, [dashboard view](#dashboard-customization)에서 카드를 포함할 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 패키지 내에 카드를 포함하는 경우, `Livewire::component` 메서드로 컴포넌트를 등록해야 합니다.

<a name="custom-card-styling"></a>
<!-- ### Styling -->
### Styling

<!-- If your card requires additional styling beyond the classes and components included with Pulse, there are a few options for including custom CSS for your cards. -->
카드가 Pulse에 포함된 클래스와 컴포넌트 외에 추가 스타일을 필요로 한다면, 카드별 커스텀 CSS를 적용할 몇 가지 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
<!-- #### Laravel Vite Integration -->
#### Laravel Vite Integration

<!-- If your custom card lives within your application's code base and you are using Laravel's [Vite integration](/docs/master/vite), you may update your `vite.config.js` file to include a dedicated CSS entry point for your card: -->
커스텀 카드가 애플리케이션 코드베이스 내에 있고, Laravel [Vite integration](/docs/master/vite)을 사용한다면, `vite.config.js` 파일에서 카드용 CSS 엔트리포인트를 추가할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

<!-- You may then use the `@vite` Blade directive in your [dashboard view](#dashboard-customization), specifying the CSS entrypoint for your card: -->
그런 다음, [dashboard view](#dashboard-customization)에서 `@vite` Blade 디렉티브를 사용해 카드용 CSS 엔트리포인트를 로드하면 됩니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```

<a name="custom-card-styling-css"></a>
<!-- #### CSS Files -->
#### CSS Files

<!-- For other use cases, including Pulse cards contained within a package, you may instruct Pulse to load additional stylesheets by defining a `css` method on your Livewire component that returns the file path to your CSS file: -->
Pulse 카드가 패키지에 포함된 등 다양한 경우, Livewire 컴포넌트에 `css` 메서드를 정의해 추가 스타일시트를 Pulse에 포함할 수 있습니다:

```php
class TopSellers extends Card
{
    // ...

    protected function css()
    {
        return __DIR__.'/../../dist/top-sellers.css';
    }
}
```

<!-- When this card is included on the dashboard, Pulse will automatically include the contents of this file within a `<style>` tag so it does not need to be published to the `public` directory. -->
이 카드가 대시보드에 포함되면, Pulse는 해당 파일 내용을 자동으로 `<style>` 태그로 인클루드하므로, 파일을 `public` 디렉터리에 별도로 게시할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
<!-- #### Tailwind CSS -->
#### Tailwind CSS

<!-- When using Tailwind CSS, you should create a dedicated CSS entrypoint. The following example excludes Tailwind's [Preflight](https://tailwindcss.com/docs/preflight) base styles which are already included by Pulse, and scopes Tailwind using a CSS selector to avoid conflicts with Pulse's Tailwind classes: -->
Tailwind CSS를 사용할 경우, 별도의 CSS 엔트리포인트를 만들어야 합니다. 아래 예시는 Tailwind의 [Preflight](https://tailwindcss.com/docs/preflight) 기본 스타일(이미 Pulse에 내장됨)을 제외하고, Pulse의 Tailwind 클래스와의 충돌을 막기 위해 CSS 선택자로 Tailwind를 범위지정하는 방식입니다:

```css
@import "tailwindcss/theme.css";

@custom-variant dark (&:where(.dark, .dark *));
@source "./../../views/livewire/pulse/top-sellers.blade.php";

@theme {
  /* ... */
}

#top-sellers {
  @import "tailwindcss/utilities.css" source(none);
}
```

<!-- You will also need to include an `id` or `class` attribute in your card's view that matches the CSS selector in your entrypoint: -->
또한 카드 뷰 내에 해당 CSS 선택자와 일치하는 `id` 또는 `class` 속성을 지정해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
<!-- ### Data Capture and Aggregation -->
### Data Capture and Aggregation

<!-- Custom cards may fetch and display data from anywhere; however, you may wish to leverage Pulse's powerful and efficient data recording and aggregation system. -->
커스텀 카드는 어디서든 데이터를 조회 및 표시할 수 있습니다. 그러나 Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 그대로 활용하는 것이 좋습니다.

<a name="custom-card-data-capture"></a>
<!-- #### Capturing Entries -->
#### Capturing Entries

<!-- Pulse allows you to record "entries" using the `Pulse::record` method: -->
Pulse는 `Pulse::record` 메서드를 통해 임의의 "엔트리"를 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

<!-- The first argument provided to the `record` method is the `type` for the entry you are recording, while the second argument is the `key` that determines how the aggregated data should be grouped. For most aggregation methods you will also need to specify a `value` to be aggregated. In the example above, the value being aggregated is `$sale->amount`. You may then invoke one or more aggregation methods (such as `sum`) so that Pulse may capture pre-aggregated values into "buckets" for efficient retrieval later. -->
`record` 메서드의 첫 번째 인자는 기록할 엔트리의 `type`, 두 번째 인자는 집계 데이터의 그룹화를 결정짓는 `key` 입니다. 대부분의 집계 메서드에서는 집계할 `value` 지정도 필요합니다. 위 예제에서는 `$sale->amount`가 집계 값입니다. 이후 `sum` 등 집계 메서드를 추가로 호출해, Pulse가 사전에 집계된 값을 "버킷"으로 저장하게 합니다.

<!-- The available aggregation methods are: -->
사용 가능한 집계 메서드는 다음과 같습니다:

<!--
* `avg`
* `count`
* `max`
* `min`
* `sum`
-->
* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> 현재 인증된 사용자 ID를 기록하는 카드 패키지를 만들 때는, 애플리케이션에서 [user resolver customizations](#dashboard-resolving-users)을 고려하여 반드시 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용해야 합니다.

<a name="custom-card-data-retrieval"></a>
<!-- #### Retrieving Aggregate Data -->
#### Retrieving Aggregate Data

<!-- When extending Pulse's `Card` Livewire component, you may use the `aggregate` method to retrieve aggregated data for the period being viewed in the dashboard: -->
Pulse의 `Card` Livewire 컴포넌트를 상속받으면, 대시보드에 표시할 기간에 대한 집계 데이터를 `aggregate` 메서드로 조회할 수 있습니다:

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count'])
        ]);
    }
}
```

<!-- The `aggregate` method returns a collection of PHP `stdClass` objects. Each object will contain the `key` property captured earlier, along with keys for each of the requested aggregates: -->
`aggregate` 메서드는 PHP의 `stdClass` 객체 컬렉션을 반환합니다. 각 객체에는 앞서 기록한 `key`와 요청한 집계 값이 포함되어 있습니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

<!-- Pulse will primarily retrieve data from the pre-aggregated buckets; therefore, the specified aggregates must have been captured up-front using the `Pulse::record` method. The oldest bucket will typically fall partially outside the period, so Pulse will aggregate the oldest entries to fill the gap and give an accurate value for the entire period, without needing to aggregate the entire period on each poll request. -->
Pulse는 주로 미리 집계된 버킷에서 데이터를 가져옵니다. 따라서 지정한 집계 값이 `Pulse::record` 메서드를 통해 미리 수집되어 있어야 합니다. 가장 오래된 버킷은 일반적으로 기간 경계에 일부 걸치므로, Pulse는 가장 오래된 엔트리를 집계해 이 구간을 채우고, 매 폴링 요청마다 전체 기간을 집계할 필요 없이 전체 기간에 대한 정확한 값을 제공합니다.

<!-- You may also retrieve a total value for a given type by using the `aggregateTotal` method. For example, the following method would retrieve the total of all user sales instead of grouping them by user. -->
특정 유형에 대한 전체 합계를 조회하고 싶다면 `aggregateTotal` 메서드를 사용합니다. 예를 들어, 모든 사용자 판매 총합을 집계할 수 있습니다:

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
<!-- #### Displaying Users -->
#### Displaying Users

<!-- When working with aggregates that record a user ID as the key, you may resolve the keys to user records using the `Pulse::resolveUsers` method: -->
키로 사용자 ID가 집계된 데이터와 함께 작업할 때는, `Pulse::resolveUsers` 메서드로 키를 사용자 레코드로 해석할 수 있습니다:

```php
$aggregates = $this->aggregate('user_sale', ['sum', 'count']);

$users = Pulse::resolveUsers($aggregates->pluck('key'));

return view('livewire.pulse.top-sellers', [
    'sellers' => $aggregates->map(fn ($aggregate) => (object) [
        'user' => $users->find($aggregate->key),
        'sum' => $aggregate->sum,
        'count' => $aggregate->count,
    ])
]);
```

<!-- The `find` method returns an object containing `name`, `extra`, and `avatar` keys, which you may optionally pass directly to the `<x-pulse::user-card>` Blade component: -->
`find` 메서드는 `name`, `extra`, `avatar` 키가 포함된 객체를 반환하며, `<x-pulse::user-card>` Blade 컴포넌트에 바로 전달할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
<!-- #### Custom Recorders -->
#### Custom Recorders

<!-- Package authors may wish to provide recorder classes to allow users to configure the capturing of data. -->
패키지 제작자는 데이터 수집을 설정할 수 있는 레코더 클래스를 별도로 제공할 수도 있습니다.

<!-- Recorders are registered in the `recorders` section of the application's `config/pulse.php` configuration file: -->
레코더는 애플리케이션의 `config/pulse.php` 설정 파일의 `recorders` 섹션에서 등록됩니다:

```php
[
    // ...
    'recorders' => [
        Acme\Recorders\Deployments::class => [
            // ...
        ],

        // ...
    ],
]
```

<!-- Recorders may listen to events by specifying a `$listen` property. Pulse will automatically register the listeners and call the recorders `record` method: -->
레코더는 `$listen` 프로퍼티에 이벤트를 지정하여 이벤트 리스닝이 가능합니다. Pulse는 리스너를 자동 등록하고, 레코더의 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * The events to listen for.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * Record the deployment.
     */
    public function record(Deployment $event): void
    {
        $config = Config::get('pulse.recorders.'.static::class);

        Pulse::record(
            // ...
        );
    }
}
```
