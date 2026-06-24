<!-- # Laravel Telescope -->
# Laravel Telescope

- [Introduction](#introduction)
- [Installation](#installation)
    - [Local Only Installation](#local-only-installation)
    - [Configuration](#configuration)
    - [Data Pruning](#data-pruning)
    - [Dashboard Authorization](#dashboard-authorization)
- [Upgrading Telescope](#upgrading-telescope)
- [Filtering](#filtering)
    - [Entries](#filtering-entries)
    - [Batches](#filtering-batches)
- [Tagging](#tagging)
- [Available Watchers](#available-watchers)
    - [Batch Watcher](#batch-watcher)
    - [Cache Watcher](#cache-watcher)
    - [Command Watcher](#command-watcher)
    - [Dump Watcher](#dump-watcher)
    - [Event Watcher](#event-watcher)
    - [Exception Watcher](#exception-watcher)
    - [Gate Watcher](#gate-watcher)
    - [HTTP Client Watcher](#http-client-watcher)
    - [Job Watcher](#job-watcher)
    - [Log Watcher](#log-watcher)
    - [Mail Watcher](#mail-watcher)
    - [Model Watcher](#model-watcher)
    - [Notification Watcher](#notification-watcher)
    - [Query Watcher](#query-watcher)
    - [Redis Watcher](#redis-watcher)
    - [Request Watcher](#request-watcher)
    - [Schedule Watcher](#schedule-watcher)
    - [View Watcher](#view-watcher)
- [Displaying User Avatars](#displaying-user-avatars)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Telescope](https://github.com/laravel/telescope) makes a wonderful companion to your local Laravel development environment. Telescope provides insight into the requests coming into your application, exceptions, log entries, database queries, queued jobs, mail, notifications, cache operations, scheduled tasks, variable dumps, and more. -->
[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 Laravel 개발 환경에서 매우 유용한 도구입니다. Telescope는 애플리케이션으로 들어오는 요청, 예외, 로그 엔트리, 데이터베이스 쿼리, 큐에 등록된 작업, 메일, 알림, 캐시 동작, 예약된 작업, 변수 덤프 등 다양한 정보를 한눈에 파악할 수 있게 해줍니다.

<!-- <img src="https://laravel.com/img/docs/telescope-example.png"/> -->
<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may use the Composer package manager to install Telescope into your Laravel project: -->
Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope
```

<!-- After installing Telescope, publish its assets and migrations using the `telescope:install` Artisan command. After installing Telescope, you should also run the `migrate` command in order to create the tables needed to store Telescope's data: -->
Telescope 설치 후, `telescope:install` Artisan 명령어로 에셋과 마이그레이션 파일을 퍼블리시해야 합니다. Telescope 설치가 끝나면, Telescope의 데이터를 저장하는 데 필요한 테이블을 생성하기 위해 `migrate` 명령어도 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

<!-- Finally, you may access the Telescope dashboard via the `/telescope` route. -->
설치가 완료되면 `/telescope` 경로를 통해 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
<!-- ### Local Only Installation -->
### Local Only Installation

<!-- If you plan to only use Telescope to assist your local development, you may install Telescope using the `--dev` flag: -->
Telescope를 로컬 개발 환경에서만 사용하려는 경우, `--dev` 플래그를 사용하여 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

<!-- After running `telescope:install`, you should remove the `TelescopeServiceProvider` service provider registration from your application's `bootstrap/providers.php` configuration file. Instead, manually register Telescope's service providers in the `register` method of your `App\Providers\AppServiceProvider` class. We will ensure the current environment is `local` before registering the providers: -->
`telescope:install` 실행 후에는, 애플리케이션의 `bootstrap/providers.php` 설정 파일에서 `TelescopeServiceProvider`의 자동 등록을 제거해야 합니다. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 Telescope 서비스 프로바이더를 수동으로 등록합니다. 아래와 같이 현재 환경이 `local`일 때만 프로바이더가 등록되도록 작성합니다:

```php
/**
 * Register any application services.
 */
public function register(): void
{
    if ($this->app->environment('local') && class_exists(\Laravel\Telescope\TelescopeServiceProvider::class)) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

<!-- Finally, you should also prevent the Telescope package from being [auto-discovered](/docs/12.x/packages#package-discovery) by adding the following to your `composer.json` file: -->
마지막으로, Telescope 패키지가 [auto-discovered](/docs/12.x/packages#package-discovery)되지 않도록 아래 설정을 `composer.json` 파일의 extra 섹션에 추가해야 합니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "laravel/telescope"
        ]
    }
},
```

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After publishing Telescope's assets, its primary configuration file will be located at `config/telescope.php`. This configuration file allows you to configure your [watcher options](#available-watchers). Each configuration option includes a description of its purpose, so be sure to thoroughly explore this file. -->
Telescope의 에셋을 퍼블리시하면, 주요 설정 파일이 `config/telescope.php` 경로에 생성됩니다. 이 파일에서 [watcher options](#available-watchers) 등을 세부적으로 설정할 수 있습니다. 각 옵션에는 상세 설명이 주석으로 달려 있으니, 꼼꼼히 확인하는 것이 좋습니다.

<!-- If desired, you may disable Telescope's data collection entirely using the `enabled` configuration option: -->
필요하다면, 가장 상단의 `enabled` 옵션을 사용하여 Telescope의 데이터 수집 기능을 완전히 비활성화할 수 있습니다:

```php
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
<!-- ### Data Pruning -->
### Data Pruning

<!-- Without pruning, the `telescope_entries` table can accumulate records very quickly. To mitigate this, you should [schedule](/docs/12.x/scheduling) the `telescope:prune` Artisan command to run daily: -->
데이터 정리를 하지 않으면 `telescope_entries` 테이블에 레코드가 빠르게 쌓일 수 있습니다. 이를 방지하기 위해서는 [schedule](/docs/12.x/scheduling)를 이용하여 `telescope:prune` Artisan 명령어를 매일 실행되도록 해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

<!-- By default, all entries older than 24 hours will be pruned. You may use the `hours` option when calling the command to determine how long to retain Telescope data. For example, the following command will delete all records created over 48 hours ago: -->
기본적으로 24시간이 지난 엔트리는 자동으로 삭제됩니다. 엔트리의 보관 기간을 조정하고 싶다면, 명령어 호출 시 `hours` 옵션을 사용할 수 있습니다. 아래 예시는 48시간이 넘은 레코드를 모두 삭제합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Telescope dashboard may be accessed via the `/telescope` route. By default, you will only be able to access this dashboard in the `local` environment. Within your `app/Providers/TelescopeServiceProvider.php` file, there is an [authorization gate](/docs/12.x/authorization#gates) definition. This authorization gate controls access to Telescope in **non-local** environments. You are free to modify this gate as needed to restrict access to your Telescope installation: -->
Telescope 대시보드는 `/telescope` 경로에서 접근할 수 있습니다. 기본적으로 `local` 환경에서만 접근이 허용되어 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일 내에서는 [authorization gate](/docs/12.x/authorization#gates)를 정의해두었습니다. 이 게이트를 이용하면 **로컬 환경이 아닌** 곳에서의 Telescope 접근 권한을 제어할 수 있습니다. 이 부분의 코드는 필요에 따라 수정해 특정 사용자만 접근 가능하게 제한할 수 있습니다:

```php
use App\Models\User;

/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewTelescope', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

> [!WARNING]
> 운영 환경에서는 반드시 `APP_ENV` 환경 변수를 `production`으로 변경해야 합니다. 그렇지 않으면 Telescope 설치가 외부에 공개될 위험이 있습니다.

<a name="upgrading-telescope"></a>
<!-- ## Upgrading Telescope -->
## Upgrading Telescope

<!-- When upgrading to a new major version of Telescope, it's important that you carefully review [the upgrade guide](https://github.com/laravel/telescope/blob/master/UPGRADE.md). -->
Telescope의 새로운 주요 버전으로 업그레이드할 때는 반드시 [the upgrade guide](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 확인해야 합니다.

<!-- In addition, when upgrading to any new Telescope version, you should re-publish Telescope's assets: -->
또한, 새로운 Telescope 버전으로 업그레이드할 때마다 다음과 같이 Telescope의 에셋을 다시 퍼블리시해야 합니다:

```shell
php artisan telescope:publish
```

<!-- To keep the assets up-to-date and avoid issues in future updates, you may add the `vendor:publish --tag=laravel-assets` command to the `post-update-cmd` scripts in your application's `composer.json` file: -->
에셋을 항상 최신 상태로 유지하고 향후 업데이트에서의 문제를 예방하려면, 애플리케이션의 `composer.json` 파일 내 `post-update-cmd` 스크립트에 아래와 같이 `vendor:publish --tag=laravel-assets` 명령어를 추가하는 것이 좋습니다:

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a name="filtering"></a>
<!-- ## Filtering -->
## Filtering

<a name="filtering-entries"></a>
<!-- ### Entries -->
### Entries

<!-- You may filter the data that is recorded by Telescope via the `filter` closure that is defined in your `App\Providers\TelescopeServiceProvider` class. By default, this closure records all data in the `local` environment and exceptions, failed jobs, scheduled tasks, and data with monitored tags in all other environments: -->
Telescope가 기록하는 데이터를 `App\Providers\TelescopeServiceProvider` 클래스의 `filter` 클로저를 통해 필터링할 수 있습니다. 기본값으로, 이 클로저는 `local` 환경에서는 모든 데이터를 기록하며, 그 외 환경에서는 예외, 실패한 작업, 예약된 작업, 모니터 태그가 걸린 데이터만 기록합니다:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filter(function (IncomingEntry $entry) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entry->isReportableException() ||
            $entry->isFailedJob() ||
            $entry->isScheduledTask() ||
            $entry->isSlowQuery() ||
            $entry->hasMonitoredTag();
    });
}
```

<a name="filtering-batches"></a>
<!-- ### Batches -->
### Batches

<!-- While the `filter` closure filters data for individual entries, you may use the `filterBatch` method to register a closure that filters all data for a given request or console command. If the closure returns `true`, all of the entries are recorded by Telescope: -->
`filter` 클로저가 개별 엔트리에 대한 데이터 필터링이라면, `filterBatch` 메서드는 하나의 요청 혹은 콘솔 명령 전체의 데이터를 필터링하기 위한 클로저를 등록할 수 있습니다. 이 클로저가 `true`를 반환하면 해당 엔트리 전체가 Telescope에 기록됩니다:

```php
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function (IncomingEntry $entry) {
            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->isSlowQuery() ||
                $entry->hasMonitoredTag();
            });
    });
}
```

<a name="tagging"></a>
<!-- ## Tagging -->
## Tagging

<!-- Telescope allows you to search entries by "tag". Often, tags are Eloquent model class names or authenticated user IDs which Telescope automatically adds to entries. Occasionally, you may want to attach your own custom tags to entries. To accomplish this, you may use the `Telescope::tag` method. The `tag` method accepts a closure which should return an array of tags. The tags returned by the closure will be merged with any tags Telescope would automatically attach to the entry. Typically, you should call the `tag` method within the `register` method of your `App\Providers\TelescopeServiceProvider` class: -->
Telescope는 "태그"를 활용해 엔트리를 검색할 수 있습니다. 보통 태그는 Eloquent 모델 클래스명이나 인증된 사용자 ID 등이며, 이는 Telescope가 자동으로 부여합니다. 상황에 따라 직접 커스텀 태그를 추가하고 싶은 경우, `Telescope::tag` 메서드를 사용할 수 있습니다. `tag` 메서드는 태그 배열을 반환하는 클로저를 인수로 받으며, 반환된 태그는 Telescope가 기본적으로 부여하는 태그와 합쳐집니다. 일반적으로 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 `tag` 메서드를 호출합니다:

```php
use Laravel\Telescope\EntryType;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::tag(function (IncomingEntry $entry) {
        return $entry->type === EntryType::REQUEST
            ? ['status:'.$entry->content['response_status']]
            : [];
    });
}
```

<a name="available-watchers"></a>
<!-- ## Available Watchers -->
## Available Watchers

<!-- Telescope "watchers" gather application data when a request or console command is executed. You may customize the list of watchers that you would like to enable within your `config/telescope.php` configuration file: -->
Telescope의 "워처"는 요청 또는 콘솔 명령이 실행될 때 애플리케이션의 다양한 정보를 수집합니다. 활성화할 워처 목록은 `config/telescope.php` 설정 파일에서 자유롭게 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],
```

<!-- Some watchers also allow you to provide additional customization options: -->
일부 워처는 세부 옵션 설정도 가능합니다:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    // ...
],
```

<a name="batch-watcher"></a>
<!-- ### Batch Watcher -->
### Batch Watcher

<!-- The batch watcher records information about queued [batches](/docs/12.x/queues#job-batching), including the job and connection information. -->
배치 워처는 큐에 등록된 [batches](/docs/12.x/queues#job-batching)의 정보(작업 단위와 연결 정보 등)를 기록합니다.

<a name="cache-watcher"></a>
<!-- ### Cache Watcher -->
### Cache Watcher

<!-- The cache watcher records data when a cache key is hit, missed, updated and forgotten. -->
캐시 워처는 캐시 키를 적중, 미스, 갱신, 삭제하는 등의 캐시 관련 동작을 기록합니다.

<a name="command-watcher"></a>
<!-- ### Command Watcher -->
### Command Watcher

<!-- The command watcher records the arguments, options, exit code, and output whenever an Artisan command is executed. If you would like to exclude certain commands from being recorded by the watcher, you may specify the command in the `ignore` option within your `config/telescope.php` file: -->
명령어 워처는 Artisan 명령어가 실행될 때마다 인수, 옵션, 종료 코드, 출력 결과를 기록합니다. 특정 명령어를 기록에서 제외하려면 `config/telescope.php` 파일의 `ignore` 옵션에 명령어를 추가할 수 있습니다:

```php
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    // ...
],
```

<a name="dump-watcher"></a>
<!-- ### Dump Watcher -->
### Dump Watcher

<!-- The dump watcher records and displays your variable dumps in Telescope. When using Laravel, variables may be dumped using the global `dump` function. The dump watcher tab must be open in a browser for the dump to be recorded, otherwise, the dumps will be ignored by the watcher. -->
덤프 워처는 변수 덤프(dump)를 기록하고 Telescope 내에서 표시합니다. Laravel의 글로벌 `dump` 함수를 사용할 때 덤프 내용이 추적됩니다. 이 워처는 브라우저에서 덤프 탭이 열려 있어야 덤프가 기록되며, 탭이 닫혀 있을 경우 해당 덤프는 워처에 의해 무시됩니다.

<a name="event-watcher"></a>
<!-- ### Event Watcher -->
### Event Watcher

<!-- The event watcher records the payload, listeners, and broadcast data for any [events](/docs/12.x/events) dispatched by your application. The Laravel framework's internal events are ignored by the Event watcher. -->
이벤트 워처는 애플리케이션에서 발생한 [events](/docs/12.x/events)의 페이로드, 리스너, 브로드캐스트 데이터를 기록합니다. Laravel 프레임워크에서 내부적으로 발생하는 이벤트는 워처가 기록하지 않습니다.

<a name="exception-watcher"></a>
<!-- ### Exception Watcher -->
### Exception Watcher

<!-- The exception watcher records the data and stack trace for any reportable exceptions that are thrown by your application. -->
예외 워처는 애플리케이션에서 throw된 보고 가능한(reportable) 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
<!-- ### Gate Watcher -->
### Gate Watcher

<!-- The gate watcher records the data and result of [gate and policy](/docs/12.x/authorization) checks by your application. If you would like to exclude certain abilities from being recorded by the watcher, you may specify those in the `ignore_abilities` option in your `config/telescope.php` file: -->
게이트 워처는 애플리케이션의 [gate and policy](/docs/12.x/authorization) 검사 결과 및 관련 데이터를 기록합니다. 특정 권한 검사를 기록에서 제외하려면, `config/telescope.php`의 `ignore_abilities` 옵션에 추가할 수 있습니다:

```php
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    // ...
],
```

<a name="http-client-watcher"></a>
<!-- ### HTTP Client Watcher -->
### HTTP Client Watcher

<!-- The HTTP client watcher records outgoing [HTTP client requests](/docs/12.x/http-client) made by your application. -->
HTTP 클라이언트 워처는 애플리케이션에서 발생한 외부 [HTTP client requests](/docs/12.x/http-client)을 기록합니다.

<a name="job-watcher"></a>
<!-- ### Job Watcher -->
### Job Watcher

<!-- The job watcher records the data and status of any [jobs](/docs/12.x/queues) dispatched by your application. -->
작업 워처는 애플리케이션에서 디스패치된 [jobs](/docs/12.x/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
<!-- ### Log Watcher -->
### Log Watcher

<!-- The log watcher records the [log data](/docs/12.x/logging) for any logs written by your application. -->
로그 워처는 애플리케이션이 기록한 [log data](/docs/12.x/logging)를 기록합니다.

<!-- By default, Telescope will only record logs at the `error` level and above. However, you can modify the `level` option in your application's `config/telescope.php` configuration file to modify this behavior: -->
기본적으로 Telescope는 `error` 레벨 이상의 로그만 기록합니다. 이 동작을 변경하려면, `config/telescope.php`에서 `level` 옵션 값을 수정할 수 있습니다:

```php
'watchers' => [
    Watchers\LogWatcher::class => [
        'enabled' => env('TELESCOPE_LOG_WATCHER', true),
        'level' => 'debug',
    ],

    // ...
],
```

<a name="mail-watcher"></a>
<!-- ### Mail Watcher -->
### Mail Watcher

<!-- The mail watcher allows you to view an in-browser preview of [emails](/docs/12.x/mail) sent by your application along with their associated data. You may also download the email as an `.eml` file. -->
메일 워처를 사용하면 애플리케이션에서 보낸 [emails](/docs/12.x/mail)을 브라우저에서 직접 미리 볼 수 있으며, 관련 데이터도 함께 확인할 수 있습니다. 또한 이메일을 `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
<!-- ### Model Watcher -->
### Model Watcher

<!-- The model watcher records model changes whenever an Eloquent [model event](/docs/12.x/eloquent#events) is dispatched. You may specify which model events should be recorded via the watcher's `events` option: -->
모델 워처는 Eloquent [model event](/docs/12.x/eloquent#events)가 디스패치될 때마다 해당 모델 변경 사항을 기록합니다. 워처의 `events` 옵션을 사용하여 어떤 이벤트를 기록할지 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],
```

<!-- If you would like to record the number of models hydrated during a given request, enable the `hydrations` option: -->
특정 요청 중 하이드레이션된 모델의 수를 기록하고 싶을 때는, `hydrations` 옵션을 활성화합니다:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    // ...
],
```

<a name="notification-watcher"></a>
<!-- ### Notification Watcher -->
### Notification Watcher

<!-- The notification watcher records all [notifications](/docs/12.x/notifications) sent by your application. If the notification triggers an email and you have the mail watcher enabled, the email will also be available for preview on the mail watcher screen. -->
알림 워처는 애플리케이션에서 전송된 모든 [notifications](/docs/12.x/notifications)을 기록합니다. 만약 알림이 이메일을 트리거하고 메일 워처가 활성화되어 있다면, 해당 이메일도 메일 워처 화면에서 미리보기가 제공됩니다.

<a name="query-watcher"></a>
<!-- ### Query Watcher -->
### Query Watcher

<!-- The query watcher records the raw SQL, bindings, and execution time for all queries that are executed by your application. The watcher also tags any queries slower than 100 milliseconds as `slow`. You may customize the slow query threshold using the watcher's `slow` option: -->
쿼리 워처는 애플리케이션에서 실행된 모든 쿼리의 원본 SQL, 바인딩, 실행 시간을 기록합니다. 100ms보다 느린 쿼리는 자동으로 `slow` 태그가 부여됩니다. 워처의 `slow` 옵션을 사용하면 느린 쿼리의 임계값을 원하는 대로 조정할 수 있습니다:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    // ...
],
```

<a name="redis-watcher"></a>
<!-- ### Redis Watcher -->
### Redis Watcher

<!-- The Redis watcher records all [Redis](/docs/12.x/redis) commands executed by your application. If you are using Redis for caching, cache commands will also be recorded by the Redis watcher. -->
Redis 워처는 애플리케이션에서 실행된 모든 [Redis](/docs/12.x/redis) 명령어를 기록합니다. 캐싱에 Redis를 사용하는 경우, 캐시 관련 명령어도 Redis 워처에 기록됩니다.

<a name="request-watcher"></a>
<!-- ### Request Watcher -->
### Request Watcher

<!-- The request watcher records the request, headers, session, and response data associated with any requests handled by the application. You may limit your recorded response data via the `size_limit` (in kilobytes) option: -->
요청 워처는 애플리케이션에서 처리한 각 요청의 요청 본문, 헤더, 세션, 그리고 응답 데이터를 기록합니다. 기록하는 응답 데이터의 크기를 제어하려면, `size_limit`(킬로바이트 단위) 옵션을 사용할 수 있습니다:

```php
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    // ...
],
```

<a name="schedule-watcher"></a>
<!-- ### Schedule Watcher -->
### Schedule Watcher

<!-- The schedule watcher records the command and output of any [scheduled tasks](/docs/12.x/scheduling) run by your application. -->
스케줄 워처는 애플리케이션에서 실행된 [scheduled tasks](/docs/12.x/scheduling)의 명령어와 출력 결과를 기록합니다.

<a name="view-watcher"></a>
<!-- ### View Watcher -->
### View Watcher

<!-- The view watcher records the [view](/docs/12.x/views) name, path, data, and "composers" used when rendering views. -->
뷰 워처는 렌더링된 [view](/docs/12.x/views)의 이름, 경로, 데이터, 사용된 "composer" 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
<!-- ## Displaying User Avatars -->
## Displaying User Avatars

<!-- The Telescope dashboard displays the user avatar for the user that was authenticated when a given entry was saved. By default, Telescope will retrieve avatars using the Gravatar web service. However, you may customize the avatar URL by registering a callback in your `App\Providers\TelescopeServiceProvider` class. The callback will receive the user's ID and email address and should return the user's avatar image URL: -->
Telescope 대시보드는 저장된 각 엔트리별로, 해당 시점에 인증된 사용자의 아바타 이미지를 보여줍니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 그러나 아바타 URL을 사용자 지정하려면, `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록할 수 있습니다. 이 콜백은 사용자 ID와 이메일을 받아, 해당 사용자의 아바타 이미지 URL을 반환해야 합니다:

```php
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (?string $id, ?string $email) {
        return ! is_null($id)
            ? '/avatars/'.User::find($id)->avatar_path
            : '/generic-avatar.jpg';
    });
}
```
