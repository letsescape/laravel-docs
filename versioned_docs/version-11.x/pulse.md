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
[Laravel Pulse](https://github.com/laravel/pulse)는 여러분의 애플리케이션의 성능과 사용 현황을 한눈에 파악할 수 있도록 도와주는 툴입니다. Pulse를 사용하면 느린 작업이나 엔드포인트 등 병목 현상을 추적하고, 가장 활발하게 활동하는 사용자를 파악하는 등 다양한 인사이트를 얻을 수 있습니다.

<!-- For in-depth debugging of individual events, check out [Laravel Telescope](/docs/11.x/telescope). -->
개별 이벤트의 심층 디버깅이 필요하다면 [Laravel Telescope](/docs/11.x/telescope)를 참고해 보시기 바랍니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Pulse의 공식 스토리지 구현은 현재 MySQL, MariaDB, PostgreSQL 데이터베이스만 지원합니다. 만약 다른 데이터베이스 엔진을 사용하고 있다면, Pulse 데이터를 위한 별도의 MySQL, MariaDB 또는 PostgreSQL 데이터베이스가 필요합니다.

<!-- You may install Pulse using the Composer package manager: -->
Composer 패키지 관리자를 사용해서 Pulse를 설치할 수 있습니다.

```sh
composer require laravel/pulse
```

<!-- Next, you should publish the Pulse configuration and migration files using the `vendor:publish` Artisan command: -->
다음으로, `vendor:publish` 아티즌 명령어를 통해 Pulse의 환경설정 및 마이그레이션 파일을 게시해야 합니다.

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```

<!-- Finally, you should run the `migrate` command in order to create the tables needed to store Pulse's data: -->
마지막으로, Pulse 데이터를 저장하는 데 필요한 테이블을 생성하기 위해 `migrate` 명령어를 실행해야 합니다.

```shell
php artisan migrate
```

<!-- Once Pulse's database migrations have been run, you may access the Pulse dashboard via the `/pulse` route. -->
Pulse의 데이터베이스 마이그레이션이 모두 적용되면 `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스가 아닌 별도의 데이터베이스에 저장하고 싶다면, [specify a dedicated database connection](#using-a-different-database)할 수 있습니다.

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- Many of Pulse's configuration options can be controlled using environment variables. To see the available options, register new recorders, or configure advanced options, you may publish the `config/pulse.php` configuration file: -->
Pulse의 다양한 환경설정 옵션은 환경 변수로 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나, 새로운 레코더를 등록하거나, 고급 옵션을 설정하려면 `config/pulse.php` 환경설정 파일을 게시해야 합니다.

```sh
php artisan vendor:publish --tag=pulse-config
```

<a name="dashboard"></a>
<!-- ## Dashboard -->
## Dashboard

<a name="dashboard-authorization"></a>
<!-- ### Authorization -->
### Authorization

<!-- The Pulse dashboard may be accessed via the `/pulse` route. By default, you will only be able to access this dashboard in the `local` environment, so you will need to configure authorization for your production environments by customizing the `'viewPulse'` authorization gate. You can accomplish this within your application's `app/Providers/AppServiceProvider.php` file: -->
Pulse 대시보드는 `/pulse` 경로에서 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 가능하므로, 운영 환경에서는 `'viewPulse'` 인가 게이트를 커스터마이징하여 인가 설정을 추가해야 합니다. 이 작업은 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일에서 진행할 수 있습니다.

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
Pulse 대시보드의 카드와 레이아웃은 대시보드 뷰 파일을 게시하여 구성할 수 있습니다. 대시보드 뷰는 `resources/views/vendor/pulse/dashboard.blade.php`로 복사됩니다.

```sh
php artisan vendor:publish --tag=pulse-dashboard
```

<!-- The dashboard is powered by [Livewire](https://livewire.laravel.com/), and allows you to customize the cards and layout without needing to rebuild any JavaScript assets. -->
Pulse 대시보드는 [Livewire](https://livewire.laravel.com/)를 기반으로 하며, JavaScript 자산을 다시 빌드하지 않고도 카드와 레이아웃을 쉽게 커스터마이징할 수 있습니다.

<!-- Within this file, the `<x-pulse>` component is responsible for rendering the dashboard and provides a grid layout for the cards. If you would like the dashboard to span the full width of the screen, you may provide the `full-width` prop to the component: -->
이 뷰 파일에서 `<x-pulse>` 컴포넌트가 대시보드의 렌더링을 담당하며, 카드들을 위한 그리드 레이아웃을 제공합니다. 만약 대시보드를 화면 전체 너비로 표시하고 싶다면, 이 컴포넌트에 `full-width` 속성을 추가하면 됩니다.

```blade
<x-pulse full-width>
    ...
</x-pulse>
```

<!-- By default, the `<x-pulse>` component will create a 12 column grid, but you may customize this using the `cols` prop: -->
기본적으로 `<x-pulse>` 컴포넌트는 12컬럼 그리드를 사용하지만, `cols` 속성을 통해 원하는 컬럼 수로 변경할 수 있습니다.

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```

<!-- Each card accepts a `cols` and `rows` prop to control the space and positioning: -->
각 카드는 공간과 위치를 제어할 수 있도록 `cols`와 `rows` 속성을 받을 수 있습니다.

```blade
<livewire:pulse.usage cols="4" rows="2" />
```

<!-- Most cards also accept an `expand` prop to show the full card instead of scrolling: -->
대부분의 카드에서는 스크롤 대신 카드 전체 내용을 한 번에 보여주고 싶을 때 `expand` 속성을 사용할 수 있습니다.

```blade
<livewire:pulse.slow-queries expand />
```

<a name="dashboard-resolving-users"></a>
<!-- ### Resolving Users -->
### Resolving Users

<!-- For cards that display information about your users, such as the Application Usage card, Pulse will only record the user's ID. When rendering the dashboard, Pulse will resolve the `name` and `email` fields from your default `Authenticatable` model and display avatars using the Gravatar web service. -->
사용자 정보를 표시하는 카드(예: 애플리케이션 사용량 카드)의 경우, Pulse는 사용자의 ID만 저장합니다. 대시보드에서 Pulse는 기본 `Authenticatable` 모델에서 `name`과 `email` 필드를 가져와 보여주며, 아바타는 Gravatar 웹 서비스를 통해 표시합니다.

<!-- You may customize the fields and avatar by invoking the `Pulse::user` method within your application's `App\Providers\AppServiceProvider` class. -->
필드와 아바타 이미지는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `Pulse::user` 메서드를 호출하여 커스터마이즈할 수 있습니다.

<!-- The `user` method accepts a closure which will receive the `Authenticatable` model to be displayed and should return an array containing `name`, `extra`, and `avatar` information for the user: -->
`user` 메서드는 표시할 `Authenticatable` 모델을 인자로 받는 클로저를 인수로 받고, `name`, `extra`, `avatar` 정보를 담은 배열을 반환해야 합니다.

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
> 인증된 사용자 정보를 어떻게 수집하고 가져올지 완전히 커스터마이즈하고 싶다면, `Laravel\Pulse\Contracts\ResolvesUsers` 인터페이스를 구현해서 Laravel의 [service container](/docs/11.x/container#binding-a-singleton)에 바인딩할 수 있습니다.

<a name="dashboard-cards"></a>
<!-- ### Cards -->
### Cards

<a name="servers-card"></a>
<!-- #### Servers -->
#### Servers

<!-- The `<livewire:pulse.servers />` card displays system resource usage for all servers running the `pulse:check` command. Please refer to the documentation regarding the [servers recorder](#servers-recorder) for more information on system resource reporting. -->
`<livewire:pulse.servers />` 카드는 `pulse:check` 명령어를 실행 중인 모든 서버의 시스템 리소스 사용량을 보여줍니다. 시스템 리소스 보고에 관한 자세한 내용은 [servers recorder](#servers-recorder) 문서를 참고하세요.

<!-- If you replace a server in your infrastructure, you may wish to stop displaying the inactive server in the Pulse dashboard after a given duration. You may accomplish this using the `ignore-after` prop, which accepts the number of seconds after which inactive servers should be removed from the Pulse dashboard. Alternatively, you may provide a relative time formatted string, such as `1 hour` or `3 days and 1 hour`: -->
인프라에서 서버를 교체한 경우, 일정 시간이 지난 후 Pulse 대시보드에서 비활성 서버의 표시를 중지하고 싶을 수도 있습니다. 이럴 때는 `ignore-after` 속성을 사용하면 되며, 이 속성에는 비활성 서버를 대시보드에서 제거할 시간(초 단위) 또는 `1 hour`, `3 days and 1 hour`처럼 상대적인 시간 문자열도 사용할 수 있습니다.

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```

<a name="application-usage-card"></a>
<!-- #### Application Usage -->
#### Application Usage

<!-- The `<livewire:pulse.usage />` card displays the top 10 users making requests to your application, dispatching jobs, and experiencing slow requests. -->
`<livewire:pulse.usage />` 카드는 애플리케이션에 요청을 보내거나, 작업을 디스패치하거나, 느린 요청을 경험한 최상위 10명의 사용자 정보를 보여줍니다.

<!-- If you wish to view all usage metrics on screen at the same time, you may include the card multiple times and specify the `type` attribute: -->
대시보드에서 모든 사용 패턴을 한 번에 확인하고 싶다면, 카드를 여러 번 포함하고 각 카드에 `type` 속성을 지정할 수 있습니다.

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```

<!-- To learn how to customize how Pulse retrieves and displays user information, consult our documentation on [resolving users](#dashboard-resolving-users). -->
Pulse가 사용자 정보를 어떻게 조회하고 표시하는지 커스터마이즈하는 방법은 [resolving users](#dashboard-resolving-users) 섹션을 참고해 주세요.

> [!NOTE]
> 애플리케이션에 요청이나 작업이 많다면, [sampling](#sampling) 기능을 함께 사용하는 것이 좋습니다. 자세한 내용은 [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), [slow jobs recorder](#slow-jobs-recorder) 문서를 확인하세요.

<a name="exceptions-card"></a>
<!-- #### Exceptions -->
#### Exceptions

<!-- The `<livewire:pulse.exceptions />` card shows the frequency and recency of exceptions occurring in your application. By default, exceptions are grouped based on the exception class and location where it occurred. See the [exceptions recorder](#exceptions-recorder) documentation for more information. -->
`<livewire:pulse.exceptions />` 카드는 애플리케이션에서 발생한 예외의 빈도와 최근 발생 내역을 보여줍니다. 기본적으로 예외는 예외 클래스와 발생 위치를 기준으로 그룹화됩니다. 더 자세한 내용은 [exceptions recorder](#exceptions-recorder) 문서를 참고하세요.

<a name="queues-card"></a>
<!-- #### Queues -->
#### Queues

<!-- The `<livewire:pulse.queues />` card shows the throughput of the queues in your application, including the number of jobs queued, processing, processed, released, and failed. See the [queues recorder](#queues-recorder) documentation for more information. -->
`<livewire:pulse.queues />` 카드는 애플리케이션에서 큐된 작업의 처리량, 즉 대기중, 처리중, 완료됨, 반려됨, 실패된 작업 수를 보여줍니다. 자세한 정보는 [queues recorder](#queues-recorder) 문서를 참고하세요.

<a name="slow-requests-card"></a>
<!-- #### Slow Requests -->
#### Slow Requests

<!-- The `<livewire:pulse.slow-requests />` card shows incoming requests to your application that exceed the configured threshold, which is 1,000ms by default. See the [slow requests recorder](#slow-requests-recorder) documentation for more information. -->
`<livewire:pulse.slow-requests />` 카드는 기본 임계값(기본 1,000ms)을 초과하는 모든 들어오는 요청을 표시합니다. 자세한 내용은 [slow requests recorder](#slow-requests-recorder) 문서를 참고하세요.

<a name="slow-jobs-card"></a>
<!-- #### Slow Jobs -->
#### Slow Jobs

<!-- The `<livewire:pulse.slow-jobs />` card shows the queued jobs in your application that exceed the configured threshold, which is 1,000ms by default. See the [slow jobs recorder](#slow-jobs-recorder) documentation for more information. -->
`<livewire:pulse.slow-jobs />` 카드는 대기열에 추가된 작업 중에서 설정된 임계값(기본 1,000ms)을 초과한 작업을 보여줍니다. 자세한 내용은 [slow jobs recorder](#slow-jobs-recorder) 문서를 참고하세요.

<a name="slow-queries-card"></a>
<!-- #### Slow Queries -->
#### Slow Queries

<!-- The `<livewire:pulse.slow-queries />` card shows the database queries in your application that exceed the configured threshold, which is 1,000ms by default. -->
`<livewire:pulse.slow-queries />` 카드는 애플리케이션에서 임계값(기본 1,000ms)을 초과한 데이터베이스 쿼리를 표시합니다.

<!-- By default, slow queries are grouped based on the SQL query (without bindings) and the location where it occurred, but you may choose to not capture the location if you wish to group solely on the SQL query. -->
기본적으로 느린 쿼리는 SQL 구문(바인딩 제외)과 발생 위치를 기준으로 그룹화되지만, 만약 발생 위치 캡처 없이 SQL 쿼리만으로 그룹화하고 싶다면, 해당 옵션을 끌 수 있습니다.

<!-- If you encounter rendering performance issues due to extremely large SQL queries receiving syntax highlighting, you may disable highlighting by adding the `without-highlighting` prop: -->
매우 큰 SQL 쿼리에 문법 하이라이팅이 적용되어서 렌더링 성능에 영향을 준다면, `without-highlighting` 속성을 추가하여 하이라이팅을 비활성화할 수 있습니다.

```blade
<livewire:pulse.slow-queries without-highlighting />
```

<!-- See the [slow queries recorder](#slow-queries-recorder) documentation for more information. -->
자세한 내용은 [slow queries recorder](#slow-queries-recorder) 문서를 참고하세요.

<a name="slow-outgoing-requests-card"></a>
<!-- #### Slow Outgoing Requests -->
#### Slow Outgoing Requests

<!-- The `<livewire:pulse.slow-outgoing-requests />` card shows outgoing requests made using Laravel's [HTTP client](/docs/11.x/http-client) that exceed the configured threshold, which is 1,000ms by default. -->
`<livewire:pulse.slow-outgoing-requests />` 카드는 Laravel의 [HTTP client](/docs/11.x/http-client)로 보낸 요청 중 설정된 임계값(기본 1,000ms)을 초과한 아웃바운드(외부) 요청을 보여줍니다.

<!-- By default, entries will be grouped by the full URL. However, you may wish to normalize or group similar outgoing requests using regular expressions. See the [slow outgoing requests recorder](#slow-outgoing-requests-recorder) documentation for more information. -->
기본적으로 엔트리는 전체 URL을 기준으로 그룹화됩니다. 다만, 정규식을 이용해 유사한 외부 요청을 정규화하거나 그룹화할 수도 있습니다. 자세한 내용은 [slow outgoing requests recorder](#slow-outgoing-requests-recorder) 문서를 참고하세요.

<a name="cache-card"></a>
<!-- #### Cache -->
#### Cache

<!-- The `<livewire:pulse.cache />` card shows the cache hit and miss statistics for your application, both globally and for individual keys. -->
`<livewire:pulse.cache />` 카드는 애플리케이션 전체 및 개별 키별 캐시 적중/미적중 통계를 보여줍니다.

<!-- By default, entries will be grouped by key. However, you may wish to normalize or group similar keys using regular expressions. See the [cache interactions recorder](#cache-interactions-recorder) documentation for more information. -->
기본적으로 엔트리는 키(key)별로 그룹화되지만, 정규식을 활용해서 유사한 키를 그룹화할 수도 있습니다. 자세한 내용은 [cache interactions recorder](#cache-interactions-recorder) 문서를 참고하세요.

<a name="capturing-entries"></a>
<!-- ## Capturing Entries -->
## Capturing Entries

<!-- Most Pulse recorders will automatically capture entries based on framework events dispatched by Laravel. However, the [servers recorder](#servers-recorder) and some third-party cards must poll for information regularly. To use these cards, you must run the `pulse:check` daemon on all of your individual application servers: -->
대부분의 Pulse 레코더는 Laravel에서 발생한 프레임워크 이벤트를 자동으로 감지하여 엔트리를 수집합니다. 그러나 [servers recorder](#servers-recorder)와 일부 써드파티 카드는 정기적으로 정보를 폴링해야 합니다. 이런 카드를 사용하려면 각 애플리케이션 서버에서 `pulse:check` 데몬을 실행해야 합니다.

```php
php artisan pulse:check
```

> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 항상 실행 상태로 유지하려면, Supervisor 같은 프로세스 모니터를 활용해 명령어가 중단되지 않도록 설정해야 합니다.

<!-- As the `pulse:check` command is a long-lived process, it will not see changes to your codebase without being restarted. You should gracefully restart the command by calling the `pulse:restart` command during your application's deployment process: -->
`pulse:check` 명령어는 장기 실행 프로세스이므로, 코드 변경 사항을 인식하지 못합니다. 배포 과정에서 `pulse:restart` 명령어를 호출하여 해당 프로세스를 정상적으로 재시작해 주어야 합니다.

```sh
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [cache](/docs/11.x/cache)를 사용하여 재시작 신호를 저장하므로, 이 기능을 사용하기 전에 애플리케이션에 캐시 드라이버가 올바르게 설정되어 있는지 반드시 확인하세요.

<a name="recorders"></a>
<!-- ### Recorders -->
### Recorders

<!-- Recorders are responsible for capturing entries from your application to be recorded in the Pulse database. Recorders are registered and configured in the `recorders` section of the [Pulse configuration file](#configuration). -->
레코더는 Pulse 데이터베이스에 기록할 엔트리를 애플리케이션에서 수집하는 역할을 합니다. 레코더는 [Pulse configuration file](#configuration)의 `recorders` 섹션에서 등록 및 설정할 수 있습니다.

<a name="cache-interactions-recorder"></a>
<!-- #### Cache Interactions -->
#### Cache Interactions

<!-- The `CacheInteractions` recorder captures information about the [cache](/docs/11.x/cache) hits and misses occurring in your application for display on the [Cache](#cache-card) card. -->
`CacheInteractions` 레코더는 애플리케이션에서 발생한 [cache](/docs/11.x/cache) 적중 및 미적중 정보를 [Cache](#cache-card)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored key patterns. -->
샘플링 비율([sample rate](#sampling))과 무시할 키 패턴을 선택적으로 설정할 수 있습니다.

<!-- You may also configure key grouping so that similar keys are grouped as a single entry. For example, you may wish to remove unique IDs from keys caching the same type of information. Groups are configured using a regular expression to "find and replace" parts of the key. An example is included in the configuration file: -->
또한, 비슷한 키를 그룹화해서 하나의 엔트리로 표시하도록 그룹 설정을 할 수 있습니다. 예를 들어, 동일한 종류의 데이터를 캐싱하더라도 고유 ID 때문에 여러 키가 생성된다면, 정규식을 사용하여 키의 일부를 치환해 같은 키로 그룹화할 수 있습니다. 설정 파일에 예시가 포함되어 있습니다.

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```

<!-- The first pattern that matches will be used. If no patterns match, then the key will be captured as-is. -->
처음 매칭되는 패턴이 사용됩니다. 만약 어떤 패턴도 매칭되지 않으면, 키는 그대로 저장됩니다.

<a name="exceptions-recorder"></a>
<!-- #### Exceptions -->
#### Exceptions

<!-- The `Exceptions` recorder captures information about reportable exceptions occurring in your application for display on the [Exceptions](#exceptions-card) card. -->
`Exceptions` 레코더는 애플리케이션에서 발생한 신고 가능한 예외 정보를 [Exceptions](#exceptions-card)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored exceptions patterns. You may also configure whether to capture the location that the exception originated from. The captured location will be displayed on the Pulse dashboard which can help to track down the exception origin; however, if the same exception occurs in multiple locations then it will appear multiple times for each unique location. -->
샘플링 비율([sample rate](#sampling))과 무시할 예외 패턴을 선택적으로 조정할 수 있습니다. 또한 예외가 발생한 위치를 캡처할지 여부도 설정할 수 있습니다. 캡처된 위치 정보는 Pulse 대시보드에서 예외의 근원지 추적에 도움이 되지만, 동일한 예외가 여러 위치에서 발생할 경우 각각 개별적으로 표시될 수 있습니다.

<a name="queues-recorder"></a>
<!-- #### Queues -->
#### Queues

<!-- The `Queues` recorder captures information about your applications queues for display on the [Queues](#queues-card). -->
`Queues` 레코더는 애플리케이션의 큐 정보를 [Queues](#queues-card)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored jobs patterns. -->
샘플링 비율([sample rate](#sampling))과 무시할 작업 패턴을 선택적으로 조정할 수 있습니다.

<a name="slow-jobs-recorder"></a>
<!-- #### Slow Jobs -->
#### Slow Jobs

<!-- The `SlowJobs` recorder captures information about slow jobs occurring in your application for display on the [Slow Jobs](#slow-jobs-recorder) card. -->
`SlowJobs` 레코더는 애플리케이션에서 발생한 느린 작업 정보를 [Slow Jobs](#slow-jobs-recorder)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the slow job threshold, [sample rate](#sampling), and ignored job patterns. -->
느린 작업 임계값, 샘플링 비율([sample rate](#sampling)), 무시할 작업 패턴을 각각 조정할 수 있습니다.

<!-- You may have some jobs that you expect to take longer than others. In those cases, you may configure per-job thresholds: -->
특정 작업들이 일반적인 작업보다 오래 걸리는 것이 예상된다면, 작업별로 임계값을 개별 설정할 수 있습니다.

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
작업 클래스명이 어떤 정규식 패턴에도 매칭되지 않으면 `'default'` 값이 적용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
<!-- #### Slow Outgoing Requests -->
#### Slow Outgoing Requests

<!-- The `SlowOutgoingRequests` recorder captures information about outgoing HTTP requests made using Laravel's [HTTP client](/docs/11.x/http-client) that exceed the configured threshold for display on the [Slow Outgoing Requests](#slow-outgoing-requests-card) card. -->
`SlowOutgoingRequests` 레코더는 Laravel [HTTP client](/docs/11.x/http-client)를 사용해 임계값을 초과하는 외부 HTTP 요청 정보를 [Slow Outgoing Requests](#slow-outgoing-requests-card)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the slow outgoing request threshold, [sample rate](#sampling), and ignored URL patterns. -->
느린 외부 요청 임계값, 샘플링 비율([sample rate](#sampling)), 무시할 URL 패턴을 각각 조정할 수 있습니다.

<!-- You may have some outgoing requests that you expect to take longer than others. In those cases, you may configure per-request thresholds: -->
특정 외부 요청이 일반 요청보다 더 오래 걸릴 것으로 예상된다면, 요청별로 임계값을 개별 설정할 수 있습니다.

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
요청 URL이 어떠한 정규식 패턴에도 매칭되지 않으면 `'default'` 값이 사용됩니다.

<!-- You may also configure URL grouping so that similar URLs are grouped as a single entry. For example, you may wish to remove unique IDs from URL paths or group by domain only. Groups are configured using a regular expression to "find and replace" parts of the URL. Some examples are included in the configuration file: -->
또한, URL 경로나 도메인별로 비슷한 요청을 하나의 엔트리로 그룹화할 수 있습니다. 예를 들어, 고유 ID가 포함된 URL 경로나 도메인 단위로 그룹화할 수 있으며, 정규식을 사용해 URL의 일부를 치환하는 방식으로 구성할 수 있습니다. 설정 파일에 여러 예시가 포함되어 있습니다.

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
처음 매칭되는 패턴이 적용되며, 어느 패턴에도 매칭되지 않으면 URL이 그대로 저장됩니다.

<a name="slow-queries-recorder"></a>
<!-- #### Slow Queries -->
#### Slow Queries

<!-- The `SlowQueries` recorder captures any database queries in your application that exceed the configured threshold for display on the [Slow Queries](#slow-queries-card) card. -->
`SlowQueries` 레코더는 애플리케이션에서 임계값을 초과한 모든 데이터베이스 쿼리를 [Slow Queries](#slow-queries-card)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the slow query threshold, [sample rate](#sampling), and ignored query patterns. You may also configure whether to capture the query location. The captured location will be displayed on the Pulse dashboard which can help to track down the query origin; however, if the same query is made in multiple locations then it will appear multiple times for each unique location. -->
느린 쿼리 임계값, 샘플링 비율([sample rate](#sampling)), 무시할 쿼리 패턴을 각각 선택적으로 조정할 수 있습니다. 또한 쿼리 위치를 캡처할지 여부도 설정할 수 있습니다. 캡처된 위치 정보는 쿼리 발생 위치를 추적하는 데 도움이 되지만, 동일 쿼리가 여러 위치에서 발생하면 각각 개별적으로 표시될 수 있습니다.

<!-- You may have some queries that you expect to take longer than others. In those cases, you may configure per-query thresholds: -->
특정 쿼리가 일반 쿼리보다 더 오래 걸릴 것으로 예상된다면, 쿼리별로 임계값을 개별적으로 설정할 수 있습니다.

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
쿼리 SQL이 어떤 정규식 패턴에도 매칭되지 않으면 `'default'` 값이 적용됩니다.

<a name="slow-requests-recorder"></a>
<!-- #### Slow Requests -->
#### Slow Requests

<!-- The `Requests` recorder captures information about requests made to your application for display on the [Slow Requests](#slow-requests-card) and [Application Usage](#application-usage-card) cards. -->
`Requests` 레코더는 애플리케이션에 들어온 요청 정보를 [Slow Requests](#slow-requests-card)와 [Application Usage](#application-usage-card)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the slow route threshold, [sample rate](#sampling), and ignored paths. -->
느린 라우트 임계값, 샘플링 비율([sample rate](#sampling)), 무시할 경로를 각각 조정할 수 있습니다.

<!-- You may have some requests that you expect to take longer than others. In those cases, you may configure per-request thresholds: -->
특정 요청이 일반 요청보다 오래 걸릴 것으로 예상된다면, 요청별로 임계값을 개별적으로 설정할 수 있습니다.

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
요청 URL이 어떤 정규식 패턴에도 매칭되지 않으면 `'default'` 값이 적용됩니다.

<a name="servers-recorder"></a>
<!-- #### Servers -->
#### Servers

<!-- The `Servers` recorder captures CPU, memory, and storage usage of the servers that power your application for display on the [Servers](#servers-card) card. This recorder requires the [`pulse:check` command](#capturing-entries) to be running on each of the servers you wish to monitor. -->
`Servers` 레코더는 애플리케이션 서버의 CPU, 메모리, 저장 공간 사용량을 [Servers](#servers-card)에 표시하기 위해 수집합니다. 이 레코더는 각 모니터링 대상 서버에서 [`pulse:check` command](#capturing-entries)가 실행 중이어야 합니다.

<!-- Each reporting server must have a unique name. By default, Pulse will use the value returned by PHP's `gethostname` function. If you wish to customize this, you may set the `PULSE_SERVER_NAME` environment variable: -->
보고하는 각 서버는 고유 이름을 가져야 하며, 기본적으로 PHP의 `gethostname` 함수 값을 사용합니다. 직접 커스터마이즈하고 싶을 경우 `PULSE_SERVER_NAME` 환경변수를 설정할 수 있습니다.

```env
PULSE_SERVER_NAME=load-balancer
```

<!-- The Pulse configuration file also allows you to customize the directories that are monitored. -->
Pulse 환경설정 파일에서는 모니터링할 디렉토리도 추가로 커스터마이즈할 수 있습니다.

<a name="user-jobs-recorder"></a>
<!-- #### User Jobs -->
#### User Jobs

<!-- The `UserJobs` recorder captures information about the users dispatching jobs in your application for display on the [Application Usage](#application-usage-card) card. -->
`UserJobs` 레코더는 애플리케이션에서 작업을 디스패치한 사용자 정보를 [Application Usage](#application-usage-card)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored job patterns. -->
샘플링 비율([sample rate](#sampling))과 무시할 작업 패턴을 각각 조정할 수 있습니다.

<a name="user-requests-recorder"></a>
<!-- #### User Requests -->
#### User Requests

<!-- The `UserRequests` recorder captures information about the users making requests to your application for display on the [Application Usage](#application-usage-card) card. -->
`UserRequests` 레코더는 애플리케이션에 요청을 보낸 사용자 정보를 [Application Usage](#application-usage-card)에 표시하기 위해 수집합니다.

<!-- You may optionally adjust the [sample rate](#sampling) and ignored URL patterns. -->
샘플링 비율([sample rate](#sampling))과 무시할 URL 패턴을 각각 조정할 수 있습니다.

<a name="filtering"></a>
<!-- ### Filtering -->
### Filtering

<!-- As we have seen, many [recorders](#recorders) offer the ability to, via configuration, "ignore" incoming entries based on their value, such as a request's URL. But, sometimes it may be useful to filter out records based on other factors, such as the currently authenticated user. To filter out these records, you may pass a closure to Pulse's `filter` method. Typically, the `filter` method should be invoked within the `boot` method of your application's `AppServiceProvider`: -->
지금까지 살펴본 것처럼, 상당수 [recorders](#recorders)는 구성 옵션을 통해 특정 값(예: 요청 URL 등)을 기준으로 들어오는 엔트리를 무시하도록 설정할 수 있습니다. 그러나 때로는 현재 인증된 사용자 등 다른 조건으로 레코드를 필터링하고 싶을 수도 있습니다. 이런 경우 Pulse의 `filter` 메서드에 클로저를 전달하면 됩니다. 일반적으로 `filter` 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 안에서 호출하는 것이 좋습니다.

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
Pulse는 별도의 인프라를 추가 도입하지 않고 기존 애플리케이션에 바로 도입하여 사용할 수 있도록 설계되었습니다. 다만, 높은 트래픽의 애플리케이션에서는 Pulse가 성능에 미치는 영향을 최소화할 수 있는 여러 방법이 준비되어 있습니다.

<a name="using-a-different-database"></a>
<!-- ### Using a Different Database -->
### Using a Different Database

<!-- For high-traffic applications, you may prefer to use a dedicated database connection for Pulse to avoid impacting your application database. -->
고트래픽 애플리케이션의 경우, Pulse 전용 데이터베이스 연결을 사용해서 애플리케이션의 기본 데이터베이스에 부담을 주지 않도록 할 수 있습니다.

<!-- You may customize the [database connection](/docs/11.x/database#configuration) used by Pulse by setting the `PULSE_DB_CONNECTION` environment variable. -->
Pulse가 사용할 [database connection](/docs/11.x/database#configuration)은 `PULSE_DB_CONNECTION` 환경변수를 설정하여 지정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```

<a name="ingest"></a>
<!-- ### Redis Ingest -->
### Redis Ingest

> [!WARNING]
> Redis 입력 기능을 사용하려면 Redis 6.2 이상과 `phpredis` 또는 `predis`가 Laravel에서 설정된 Redis 클라이언트 드라이버로 필요합니다.

<!-- By default, Pulse will store entries directly to the [configured database connection](#using-a-different-database) after the HTTP response has been sent to the client or a job has been processed; however, you may use Pulse's Redis ingest driver to send entries to a Redis stream instead. This can be enabled by configuring the `PULSE_INGEST_DRIVER` environment variable: -->
Pulse는 기본적으로 [configured database connection](#using-a-different-database)에 HTTP 응답 전송 후나 작업이 처리된 후 직접 엔트리를 저장합니다. 그러나, Pulse의 Redis ingest 드라이버를 사용하면 엔트리를 Redis 스트림에 먼저 보낼 수 있습니다. 이 기능은 환경 변수 `PULSE_INGEST_DRIVER`를 설정하여 활성화할 수 있습니다.

```
PULSE_INGEST_DRIVER=redis
```

<!-- Pulse will use your default [Redis connection](/docs/11.x/redis#configuration) by default, but you may customize this via the `PULSE_REDIS_CONNECTION` environment variable: -->
기본적으로 Pulse는 [Redis connection](/docs/11.x/redis#configuration)도 기본 연결을 사용하지만, `PULSE_REDIS_CONNECTION` 환경변수로 별도 지정할 수 있습니다.

```
PULSE_REDIS_CONNECTION=pulse
```

<!-- When using the Redis ingest, you will need to run the `pulse:work` command to monitor the stream and move entries from Redis into Pulse's database tables. -->
Redis ingest를 사용할 때는 스트림을 모니터링하고 Redis에서 Pulse 데이터베이스 테이블로 엔트리를 이동시키는 `pulse:work` 명령어를 실행해야 합니다.

```php
php artisan pulse:work
```

> [!NOTE]
> `pulse:work` 프로세스를 백그라운드에서 항상 실행 상태로 유지하려면, Supervisor 등 프로세스 모니터링 툴을 통해 Pulse worker가 중단되지 않도록 관리해야 합니다.

<!-- As the `pulse:work` command is a long-lived process, it will not see changes to your codebase without being restarted. You should gracefully restart the command by calling the `pulse:restart` command during your application's deployment process: -->
`pulse:work` 역시 장기 실행 프로세스이므로, 코드 변경을 인식하지 못합니다. 배포할 때마다 `pulse:restart` 명령어를 호출해 해당 프로세스를 정상적으로 재시작해야 합니다.

```sh
php artisan pulse:restart
```

> [!NOTE]
> Pulse는 [cache](/docs/11.x/cache)를 사용해서 재시작 신호를 저장하므로, 이 기능 사용 전 애플리케이션에 캐시 드라이버가 제대로 설정되어 있는지 반드시 확인해야 합니다.

<a name="sampling"></a>
<!-- ### Sampling -->
### Sampling

<!-- By default, Pulse will capture every relevant event that occurs in your application. For high-traffic applications, this can result in needing to aggregate millions of database rows in the dashboard, especially for longer time periods. -->
기본적으로 Pulse는 애플리케이션 내 발생하는 모든 관련 이벤트를 빠짐없이 기록합니다. 하지만 고트래픽 환경에서는, 특히 대시보드에서 긴 기간 동안 집계할 경우 수백만 건의 데이터베이스 행을 다뤄야 할 수 있습니다.

<!-- You may instead choose to enable "sampling" on certain Pulse data recorders. For example, setting the sample rate to `0.1` on the [`User Requests`](#user-requests-recorder) recorder will mean that you only record approximately 10% of the requests to your application. In the dashboard, the values will be scaled up and prefixed with a `~` to indicate that they are an approximation. -->
이럴 때, Pulse의 일부 데이터 레코더에 "샘플링"을 활성화해 필요한 데이터만 일정 비율로 수집할 수 있습니다. 예를 들어, [`User Requests`](#user-requests-recorder) 레코더의 샘플 비율을 `0.1`로 설정하면, 실제 요청의 약 10%만 기록하게 됩니다. 대시보드에서 해당 값들은 대략치임을 의미하는 `~` 표시와 함께 업스케일되어 보여집니다.

<!-- In general, the more entries you have for a particular metric, the lower you can safely set the sample rate without sacrificing too much accuracy. -->
일반적으로, 특정 지표에 대해 수집된 데이터가 많을수록 샘플 비율을 더욱 낮추더라도 정확성에 큰 영향이 없습니다.

<a name="trimming"></a>
<!-- ### Trimming -->
### Trimming

<!-- Pulse will automatically trim its stored entries once they are outside of the dashboard window. Trimming occurs when ingesting data using a lottery system which may be customized in the Pulse [configuration file](#configuration). -->
Pulse는 대시보드에서 표시되는 기간을 벗어난 데이터 엔트리를 자동으로 정리합니다. 이 트리밍 작업은 데이터가 유입될 때마다 복권 기반(lottery) 방식으로 수행되며, Pulse [configuration file](#configuration)에서 해당 방식을 커스터마이즈할 수 있습니다.

<a name="pulse-exceptions"></a>
<!-- ### Handling Pulse Exceptions -->
### Handling Pulse Exceptions

<!-- If an exception occurs while capturing Pulse data, such as being unable to connect to the storage database, Pulse will silently fail to avoid impacting your application. -->
만약 Pulse 데이터 수집 중 스토리지 데이터베이스 연결 실패 등이 발생하여 예외가 던져지면, Pulse는 애플리케이션에 영향을 끼치지 않도록 해당 오류를 조용히 무시합니다.

<!-- If you wish to customize how these exceptions are handled, you may provide a closure to the `handleExceptionsUsing` method: -->
이러한 예외 처리를 커스터마이즈하고 싶다면 `handleExceptionsUsing` 메서드에 클로저를 전달할 수 있습니다.

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
Pulse는 여러분의 애플리케이션에 맞는 데이터를 표시할 수 있도록 커스텀 카드를 제작할 수 있습니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 직접 커스텀 카드를 만들기 전에 [review its documentation](https://livewire.laravel.com/docs)를 참고하시는 것이 좋습니다.

<a name="custom-card-components"></a>
<!-- ### Card Components -->
### Card Components

<!-- Creating a custom card in Laravel Pulse starts with extending the base `Card` Livewire component and defining a corresponding view: -->
Laravel Pulse에서 커스텀 카드를 만들려면 우선 기본 `Card` Livewire 컴포넌트를 확장하고, 뷰 파일을 정의해야 합니다.

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
Livewire의 [lazy loading](https://livewire.laravel.com/docs/lazy) 기능을 사용할 때, `Card` 컴포넌트는 `cols` 및 `rows` 속성 값을 반영하는 플레이스홀더도 자동으로 제공합니다.

<!-- When writing your Pulse card's corresponding view, you may leverage Pulse's Blade components for a consistent look and feel: -->
Pulse 카드의 뷰 파일을 작성할 때는 Pulse에서 제공하는 Blade 컴포넌트를 활용하면 일관된 스타일과 사용자 경험을 쉽게 구현할 수 있습니다.

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
`$cols`, `$rows`, `$class`, `$expand`와 같은 변수는 각각 Blade 컴포넌트에 전달하여 카드 레이아웃을 대시보드 뷰에서 커스터마이징할 수 있게 해야 합니다. 또한, 카드가 주기적으로 자동 업데이트되도록 `wire:poll.5s=""` 속성을 뷰에 포함하는 것도 추천드립니다.

<!-- Once you have defined your Livewire component and template, the card may be included in your [dashboard view](#dashboard-customization): -->
Livewire 컴포넌트와 템플릿을 정의한 뒤에는, [dashboard view](#dashboard-customization) 내에서 아래와 같이 카드를 포함할 수 있습니다.

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```

> [!NOTE]
> 만약 카드가 패키지에서 제공된다면, `Livewire::component` 메서드로 컴포넌트를 Livewire에 등록해야 합니다.

<a name="custom-card-styling"></a>

<!-- ### Styling -->
### Styling

<!-- If your card requires additional styling beyond the classes and components included with Pulse, there are a few options for including custom CSS for your cards. -->
여러분의 카드가 Pulse에서 제공하는 클래스 및 컴포넌트 이상의 추가 스타일링이 필요하다면, 카드에 커스텀 CSS를 적용하는 몇 가지 방법이 있습니다.

<a name="custom-card-styling-vite"></a>
<!-- #### Laravel Vite Integration -->
#### Laravel Vite Integration

<!-- If your custom card lives within your application's code base and you are using Laravel's [Vite integration](/docs/11.x/vite), you may update your `vite.config.js` file to include a dedicated CSS entry point for your card: -->
커스텀 카드가 애플리케이션 코드베이스 내에 위치해 있고, Laravel의 [Vite integration](/docs/11.x/vite)을 사용 중이라면, 카드 전용 CSS 엔트리포인트를 추가하도록 `vite.config.js` 파일을 수정할 수 있습니다.

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```

<!-- You may then use the `@vite` Blade directive in your [dashboard view](#dashboard-customization), specifying the CSS entrypoint for your card: -->
이제 [dashboard view](#dashboard-customization)에서 `@vite` Blade 디렉티브를 사용해 카드의 CSS 엔트리포인트를 명시할 수 있습니다.

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
Pulse 카드가 패키지 내에 포함되어 있는 등 다른 사용 사례의 경우, Livewire 컴포넌트에서 CSS 파일 경로를 반환하는 `css` 메서드를 정의해 Pulse가 추가 스타일시트를 로드하도록 할 수 있습니다.

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
이 카드가 대시보드에 포함될 경우, Pulse는 해당 파일의 내용을 `<style>` 태그 내에 자동으로 포함하므로, 별도로 `public` 디렉터리에 퍼블리시할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
<!-- #### Tailwind CSS -->
#### Tailwind CSS

<!-- When using Tailwind CSS, you should create a dedicated Tailwind configuration file to avoid loading unnecessary CSS or conflicting with Pulse's Tailwind classes: -->
Tailwind CSS를 사용할 때는 불필요한 CSS가 로딩되거나 Pulse의 Tailwind 클래스와 충돌이 발생하지 않도록, 전용 Tailwind 구성 파일을 생성하는 것이 좋습니다.

```js
export default {
    darkMode: 'class',
    important: '#top-sellers',
    content: [
        './resources/views/livewire/pulse/top-sellers.blade.php',
    ],
    corePlugins: {
        preflight: false,
    },
};
```

<!-- You may then specify the configuration file in your CSS entrypoint: -->
이제 CSS 엔트리포인트 파일에서 해당 구성 파일을 지정할 수 있습니다.

```css
@config "../../tailwind.top-sellers.config.js";
@tailwind base;
@tailwind components;
@tailwind utilities;
```

<!-- You will also need to include an `id` or `class` attribute in your card's view that matches the selector passed to Tailwind's [`important` selector strategy](https://tailwindcss.com/docs/configuration#selector-strategy): -->
그리고 카드 뷰 파일에서 Tailwind의 [`important` selector strategy](https://tailwindcss.com/docs/configuration#selector-strategy)에 전달한 셀렉터와 일치하는 `id` 혹은 `class` 속성을 추가해야 합니다.

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```

<a name="custom-card-data"></a>
<!-- ### Data Capture and Aggregation -->
### Data Capture and Aggregation

<!-- Custom cards may fetch and display data from anywhere; however, you may wish to leverage Pulse's powerful and efficient data recording and aggregation system. -->
커스텀 카드는 원하는 곳 어디에서든 데이터를 불러오고 출력할 수 있습니다. 하지만 Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 활용할 수도 있습니다.

<a name="custom-card-data-capture"></a>
<!-- #### Capturing Entries -->
#### Capturing Entries

<!-- Pulse allows you to record "entries" using the `Pulse::record` method: -->
Pulse에서는 `Pulse::record` 메서드를 사용해서 "엔트리"를 기록할 수 있습니다.

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```

<!-- The first argument provided to the `record` method is the `type` for the entry you are recording, while the second argument is the `key` that determines how the aggregated data should be grouped. For most aggregation methods you will also need to specify a `value` to be aggregated. In the example above, the value being aggregated is `$sale->amount`. You may then invoke one or more aggregation methods (such as `sum`) so that Pulse may capture pre-aggregated values into "buckets" for efficient retrieval later. -->
`record` 메서드의 첫 번째 인수는 기록할 엔트리의 `type`이며, 두 번째 인수는 집계된 데이터가 그룹화될 기준이 되는 `key`입니다. 대부분의 집계 메서드에서는 함께 집계할 `value`를 명시적으로 지정해야 합니다. 위 예제에서 집계될 값은 `$sale->amount`입니다. 이후 하나 이상의 집계 메서드(`sum` 등)를 연달아 호출해 Pulse가 효율적인 집계 저장소인 "버킷"에 미리 집계된 값을 기록하도록 할 수 있습니다.

<!-- The available aggregation methods are: -->
사용 가능한 집계 메서드는 다음과 같습니다.

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
> 현재 인증된 사용자 ID를 기록하는 카드 패키지를 만들 때는 `Pulse::resolveAuthenticatedUserId()` 메서드를 사용하는 것이 좋습니다. 이 메서드는 애플리케이션에서 [user resolver customizations](#dashboard-resolving-users)한 경우에도 정상적으로 동작합니다.

<a name="custom-card-data-retrieval"></a>
<!-- #### Retrieving Aggregate Data -->
#### Retrieving Aggregate Data

<!-- When extending Pulse's `Card` Livewire component, you may use the `aggregate` method to retrieve aggregated data for the period being viewed in the dashboard: -->
Pulse의 `Card` Livewire 컴포넌트를 확장하는 경우, 대시보드에서 보고 있는 기간에 대한 집계 데이터를 `aggregate` 메서드로 조회할 수 있습니다.

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
`aggregate` 메서드는 PHP의 `stdClass` 객체로 구성된 컬렉션을 반환합니다. 각 객체에는 앞서 기록한 `key` 속성과, 지정한 집계별로 키가 추가됩니다.

```
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```

<!-- Pulse will primarily retrieve data from the pre-aggregated buckets; therefore, the specified aggregates must have been captured up-front using the `Pulse::record` method. The oldest bucket will typically fall partially outside the period, so Pulse will aggregate the oldest entries to fill the gap and give an accurate value for the entire period, without needing to aggregate the entire period on each poll request. -->
Pulse는 주로 미리 집계해둔 버킷 데이터에서 값을 조회하므로, 집계 값을 반드시 사전에 `Pulse::record`로 기록해 두어야 합니다. 가장 오래된 집계 버킷 일부는 기간을 벗어날 수 있으므로 Pulse는 기간 전체에 대한 정확한 값을 위해 가장 오래된 엔트리들을 추가로 집계해서 누락 없이 처리합니다. 이렇게 하면 매번 전체 기간의 데이터를 집계하지 않고도 정확한 집계값을 빠르게 제공할 수 있습니다.

<!-- You may also retrieve a total value for a given type by using the `aggregateTotal` method. For example, the following method would retrieve the total of all user sales instead of grouping them by user. -->
특정 타입의 전체 합계를 조회하려면 `aggregateTotal` 메서드를 사용하세요. 예를 들어, 아래와 같이 하면 전체 사용자 판매 합계를 그룹 없이 가져올 수 있습니다.

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```

<a name="custom-card-displaying-users"></a>
<!-- #### Displaying Users -->
#### Displaying Users

<!-- When working with aggregates that record a user ID as the key, you may resolve the keys to user records using the `Pulse::resolveUsers` method: -->
key로 사용자 ID를 기록한 집계값이 있을 때는, `Pulse::resolveUsers` 메서드로 해당 key들을 실제 사용자 레코드로 변환할 수 있습니다.

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
`find` 메서드는 `name`, `extra`, `avatar` 키를 포함하는 객체를 반환합니다. 이 객체는 `<x-pulse::user-card>` Blade 컴포넌트에 바로 전달하여 사용자 정보를 표시할 수 있습니다.

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```

<a name="custom-recorders"></a>
<!-- #### Custom Recorders -->
#### Custom Recorders

<!-- Package authors may wish to provide recorder classes to allow users to configure the capturing of data. -->
패키지 제작자는 레코더 클래스를 제공하여 사용자가 데이터 기록 방식을 구성할 수 있도록 할 수 있습니다.

<!-- Recorders are registered in the `recorders` section of the application's `config/pulse.php` configuration file: -->
레코더는 애플리케이션의 `config/pulse.php` 설정 파일 내 `recorders` 섹션에 등록됩니다.

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
레코더는 `$listen` 속성을 지정해 이벤트를 감지할 수 있습니다. Pulse가 자동으로 해당 리스너를 등록하고, 레코더의 `record` 메서드를 호출합니다.

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
