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
[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 환경에서 Laravel 애플리케이션을 개발할 때 뛰어난 동반자가 되어줍니다. Telescope는 애플리케이션에 들어오는 요청, 예외, 로그 엔트리, 데이터베이스 쿼리, 큐에 등록된 잡, 메일, 알림, 캐시 작업, 예약된 작업, 변수 덤프 등 다양한 정보를 자세하게 확인할 수 있게 도와줍니다.

<!-- <img src="https://laravel.com/img/docs/telescope-example.png"/> -->
<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may use the Composer package manager to install Telescope into your Laravel project: -->
Telescope를 Laravel 프로젝트에 설치하려면 Composer 패키지 매니저를 사용할 수 있습니다:

```shell
composer require laravel/telescope
```

<!-- After installing Telescope, publish its assets and migrations using the `telescope:install` Artisan command. After installing Telescope, you should also run the `migrate` command in order to create the tables needed to store Telescope's data: -->
Telescope를 설치한 뒤, `telescope:install` 아티즌 명령어로 에셋 및 마이그레이션을 게시합니다. 이후, Telescope가 데이터를 저장하는 데 필요한 테이블을 생성하기 위해 `migrate` 명령어도 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

<!-- Finally, you may access the Telescope dashboard via the `/telescope` route. -->
마지막으로, `/telescope` 경로로 접속해 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
<!-- ### Local Only Installation -->
### Local Only Installation

<!-- If you plan to only use Telescope to assist your local development, you may install Telescope using the `--dev` flag: -->
Telescope를 개발용 로컬 환경에서만 사용할 계획이라면, 설치 시 `--dev` 플래그를 사용할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

<!-- After running `telescope:install`, you should remove the `TelescopeServiceProvider` service provider registration from your application's `bootstrap/providers.php` configuration file. Instead, manually register Telescope's service providers in the `register` method of your `App\Providers\AppServiceProvider` class. We will ensure the current environment is `local` before registering the providers: -->
`telescope:install` 명령을 실행한 후에는, 애플리케이션의 `bootstrap/providers.php` 설정 파일에 등록된 `TelescopeServiceProvider` 서비스 프로바이더를 제거하는 것이 좋습니다. 대신, Telescope의 서비스 프로바이더를 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 직접 등록하십시오. 아래와 같이 현재 환경이 `local`일 때만 프로바이더를 등록하도록 작성합니다:

```
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

<!-- Finally, you should also prevent the Telescope package from being [auto-discovered](/docs/11.x/packages#package-discovery) by adding the following to your `composer.json` file: -->
또한, Telescope 패키지가 [auto-discovered](/docs/11.x/packages#package-discovery)에 포함되지 않도록 `composer.json` 파일에 다음 내용을 추가하여 auto-discover 기능을 비활성화해야 합니다:

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
Telescope의 에셋을 게시한 후, 기본 설정 파일은 `config/telescope.php`에 위치하게 됩니다. 이 설정 파일에서는 [watcher options](#available-watchers) 등 다양한 설정을 변경할 수 있습니다. 각 옵션에는 해당 기능의 목적에 대한 설명이 포함되어 있으므로, 꼭 내용을 꼼꼼히 살펴보시는 것이 좋습니다.

<!-- If desired, you may disable Telescope's data collection entirely using the `enabled` configuration option: -->
필요에 따라 Telescope의 데이터 수집 자체를 `enabled` 설정 옵션을 사용해 완전히 비활성화할 수도 있습니다:

```
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
<!-- ### Data Pruning -->
### Data Pruning

<!-- Without pruning, the `telescope_entries` table can accumulate records very quickly. To mitigate this, you should [schedule](/docs/11.x/scheduling) the `telescope:prune` Artisan command to run daily: -->
데이터 정리를 하지 않으면 `telescope_entries` 테이블에 기록이 빠르게 쌓일 수 있습니다. 이를 방지하려면, [schedule](/docs/11.x/scheduling) 기능을 활용해 `telescope:prune` 아티즌 명령어를 매일 실행하도록 예약할 것을 권장합니다.

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();
```

<!-- By default, all entries older than 24 hours will be pruned. You may use the `hours` option when calling the command to determine how long to retain Telescope data. For example, the following command will delete all records created over 48 hours ago: -->
기본적으로 24시간이 지난 엔트리는 모두 삭제됩니다. 명령어 실행 시 `hours` 옵션을 사용해 데이터 보관 기간을 조정할 수도 있습니다. 예를 들어 아래와 같이 48시간 이상 된 데이터를 삭제하는 것도 가능합니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Telescope dashboard may be accessed via the `/telescope` route. By default, you will only be able to access this dashboard in the `local` environment. Within your `app/Providers/TelescopeServiceProvider.php` file, there is an [authorization gate](/docs/11.x/authorization#gates) definition. This authorization gate controls access to Telescope in **non-local** environments. You are free to modify this gate as needed to restrict access to your Telescope installation: -->
Telescope 대시보드는 `/telescope` 경로에서 접근할 수 있습니다. 기본적으로 `local` 환경에서만 대시보드에 접속할 수 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일에는 [authorization gate](/docs/11.x/authorization#gates) 정의가 포함되어 있으며, 이 게이트는 **non-local**(로컬 이외) 환경에서의 Telescope 접근 권한을 제어합니다. 필요에 따라 아래와 같이 접근 조건을 변경하여 Telescope 설치본에 대한 접근을 제한할 수 있습니다:

```
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
> 실제 운영 환경에서는 반드시 `APP_ENV` 환경 변수 값을 `production`으로 변경해야 합니다. 그렇지 않으면, Telescope 대시보드가 외부에 공개될 수 있습니다.

<a name="upgrading-telescope"></a>
<!-- ## Upgrading Telescope -->
## Upgrading Telescope

<!-- When upgrading to a new major version of Telescope, it's important that you carefully review [the upgrade guide](https://github.com/laravel/telescope/blob/master/UPGRADE.md). -->
Telescope의 메이저 버전으로 업그레이드할 때는, 반드시 [the upgrade guide](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼히 확인하셔야 합니다.

<!-- In addition, when upgrading to any new Telescope version, you should re-publish Telescope's assets: -->
또한, Telescope를 어떤 새 버전으로 업그레이드할 때마다 Telescope의 에셋을 다시 게시해주는 것이 좋습니다:

```shell
php artisan telescope:publish
```

<!-- To keep the assets up-to-date and avoid issues in future updates, you may add the `vendor:publish --tag=laravel-assets` command to the `post-update-cmd` scripts in your application's `composer.json` file: -->
에셋을 항상 최신으로 유지하고, 향후 업데이트 시 발생할 수 있는 문제를 예방하려면, 애플리케이션 `composer.json` 파일의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령어를 추가할 것을 추천합니다:

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
Telescope가 기록하는 데이터를 `App\Providers\TelescopeServiceProvider` 클래스에 정의한 `filter` 클로저를 통해 필터링할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서는 모든 데이터를 기록하고, 그 외 환경에서는 예외, 실패한 잡, 예약된 작업, 느린 쿼리, 모니터링 태그가 추가된 데이터만 기록합니다:

```
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
`filter` 클로저가 개별 엔트리를 필터링하는 반면, `filterBatch` 메서드를 사용하면 하나의 요청 또는 콘솔 명령 단위로 전체 데이터를 필터링하는 클로저를 등록할 수 있습니다. 이 클로저가 `true`를 반환하면, 해당 배치의 모든 엔트리가 기록됩니다:

```
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
Telescope는 엔트리에 "태그(tag)"를 붙여 검색할 수 있도록 지원합니다. 보통 태그는 Eloquent 모델의 클래스명이나 인증된 사용자 ID 등으로 자동 추가됩니다. 때에 따라서 직접 원하는 커스텀 태그를 엔트리에 붙이고 싶다면, `Telescope::tag` 메서드를 사용할 수 있습니다. `tag` 메서드는 태그 배열을 반환하는 클로저를 인수로 받으며, 반환된 태그는 Telescope가 자동으로 추가하는 태그와 합쳐서 저장됩니다. 주로 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드에서 `tag` 메서드를 호출하면 좋습니다:

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::tag(function (IncomingEntry $entry) {
        return $entry->type === 'request'
            ? ['status:'.$entry->content['response_status']]
            : [];
    });
 }
```

<a name="available-watchers"></a>
<!-- ## Available Watchers -->
## Available Watchers

<!-- Telescope "watchers" gather application data when a request or console command is executed. You may customize the list of watchers that you would like to enable within your `config/telescope.php` configuration file: -->
Telescope의 "워처(Watcher)"는 웹 요청이나 콘솔 명령 실행 시 발생하는 애플리케이션 데이터를 수집하는 역할을 합니다. 어떤 워처를 활성화할 것인지는 `config/telescope.php` 설정 파일에서 지정할 수 있습니다:

```
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    ...
],
```

<!-- Some watchers also allow you to provide additional customization options: -->
일부 워처는 추가적인 옵션 설정도 가능합니다:

```
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    ...
],
```

<a name="batch-watcher"></a>
<!-- ### Batch Watcher -->
### Batch Watcher

<!-- The batch watcher records information about queued [batches](/docs/11.x/queues#job-batching), including the job and connection information. -->
배치 워처는 큐에 등록된 [batches](/docs/11.x/queues#job-batching)에 대한 정보(잡, 연결 정보 등)를 기록합니다.

<a name="cache-watcher"></a>
<!-- ### Cache Watcher -->
### Cache Watcher

<!-- The cache watcher records data when a cache key is hit, missed, updated and forgotten. -->
캐시 워처는 캐시 키의 조회(hit), 미스(miss), 갱신, 삭제 등이 발생할 때 데이터를 기록합니다.

<a name="command-watcher"></a>
<!-- ### Command Watcher -->
### Command Watcher

<!-- The command watcher records the arguments, options, exit code, and output whenever an Artisan command is executed. If you would like to exclude certain commands from being recorded by the watcher, you may specify the command in the `ignore` option within your `config/telescope.php` file: -->
커맨드 워처는 아티즌 명령어가 실행될 때 넘겨진 인수, 옵션, 종료 코드, 실행 결과 출력 등의 정보를 기록합니다. 특정 명령어를 워처로부터 제외하고 싶을 경우, `config/telescope.php` 파일 내 `ignore` 옵션에 명령어명을 지정하면 됩니다:

```
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    ...
],
```

<a name="dump-watcher"></a>
<!-- ### Dump Watcher -->
### Dump Watcher

<!-- The dump watcher records and displays your variable dumps in Telescope. When using Laravel, variables may be dumped using the global `dump` function. The dump watcher tab must be open in a browser for the dump to be recorded, otherwise, the dumps will be ignored by the watcher. -->
덤프 워처는 변수 덤프 값을 Telescope 내에서 기록하고 보여줍니다. Laravel에서 `dump` 글로벌 함수를 사용해 변수를 덤프할 수 있습니다. 단, 덤프 워처 탭이 브라우저에서 열려 있어야만 덤프 데이터가 기록되며, 그렇지 않은 경우 워처는 덤프를 무시합니다.

<a name="event-watcher"></a>
<!-- ### Event Watcher -->
### Event Watcher

<!-- The event watcher records the payload, listeners, and broadcast data for any [events](/docs/11.x/events) dispatched by your application. The Laravel framework's internal events are ignored by the Event watcher. -->
이벤트 워처는 애플리케이션에서 발생한 [events](/docs/11.x/events)의 페이로드, 리스너, 브로드캐스트 데이터 등을 기록합니다. Laravel 프레임워크 내부 이벤트는 기본적으로 무시됩니다.

<a name="exception-watcher"></a>
<!-- ### Exception Watcher -->
### Exception Watcher

<!-- The exception watcher records the data and stack trace for any reportable exceptions that are thrown by your application. -->
예외 워처는 애플리케이션에서 발생한 보고 가능한 예외와 관련된 데이터, 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
<!-- ### Gate Watcher -->
### Gate Watcher

<!-- The gate watcher records the data and result of [gate and policy](/docs/11.x/authorization) checks by your application. If you would like to exclude certain abilities from being recorded by the watcher, you may specify those in the `ignore_abilities` option in your `config/telescope.php` file: -->
게이트 워처는 애플리케이션에서 [gate and policy](/docs/11.x/authorization) 검사가 수행될 때의 데이터와 결과를 기록합니다. 특정 권한(ability)을 레코딩 대상에서 제외하려면, `config/telescope.php` 파일의 `ignore_abilities` 옵션에 해당 권한명을 지정할 수 있습니다:

```
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    ...
],
```

<a name="http-client-watcher"></a>
<!-- ### HTTP Client Watcher -->
### HTTP Client Watcher

<!-- The HTTP client watcher records outgoing [HTTP client requests](/docs/11.x/http-client) made by your application. -->
HTTP 클라이언트 워처는 애플리케이션에서 발생한 [HTTP client requests](/docs/11.x/http-client) 내역을 기록합니다.

<a name="job-watcher"></a>
<!-- ### Job Watcher -->
### Job Watcher

<!-- The job watcher records the data and status of any [jobs](/docs/11.x/queues) dispatched by your application. -->
잡 워처는 애플리케이션에서 큐에 전달된 [jobs](/docs/11.x/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
<!-- ### Log Watcher -->
### Log Watcher

<!-- The log watcher records the [log data](/docs/11.x/logging) for any logs written by your application. -->
로그 워처는 애플리케이션에서 기록한 [log data](/docs/11.x/logging)를 수집합니다.

<!-- By default, Telescope will only record logs at the `error` level and above. However, you can modify the `level` option in your application's `config/telescope.php` configuration file to modify this behavior: -->
기본적으로 Telescope는 `error` 레벨 이상의 로그만 기록합니다. 이 동작을 바꾸고 싶다면, `config/telescope.php` 설정 파일 내 `level` 옵션을 수정하면 됩니다:

```
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

<!-- The mail watcher allows you to view an in-browser preview of [emails](/docs/11.x/mail) sent by your application along with their associated data. You may also download the email as an `.eml` file. -->
메일 워처는 애플리케이션이 보낸 [emails](/docs/11.x/mail)의 미리보기(브라우저에서 확인 가능) 및 관련 데이터를 보여줍니다. 또한, 이메일을 `.eml` 파일로 다운로드 받을 수도 있습니다.

<a name="model-watcher"></a>
<!-- ### Model Watcher -->
### Model Watcher

<!-- The model watcher records model changes whenever an Eloquent [model event](/docs/11.x/eloquent#events) is dispatched. You may specify which model events should be recorded via the watcher's `events` option: -->
모델 워처는 Eloquent [model event](/docs/11.x/eloquent#events)가 발생할 때 모델 변경 내역을 기록합니다. 기록할 모델 이벤트는 워처의 `events` 옵션을 통해 지정할 수 있습니다:

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    ...
],
```

<!-- If you would like to record the number of models hydrated during a given request, enable the `hydrations` option: -->
특정 요청 중에 하이드레이트(hydrate)된 모델 수까지 기록하려면 `hydrations` 옵션을 활성화하세요:

```
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    ...
],
```

<a name="notification-watcher"></a>
<!-- ### Notification Watcher -->
### Notification Watcher

<!-- The notification watcher records all [notifications](/docs/11.x/notifications) sent by your application. If the notification triggers an email and you have the mail watcher enabled, the email will also be available for preview on the mail watcher screen. -->
알림 워처는 애플리케이션에서 보낸 모든 [notifications](/docs/11.x/notifications)을 기록합니다. 만약 알림이 이메일을 트리거하면서 메일 워처가 활성화되어 있다면, 해당 이메일도 메일 워처 화면에서 미리보기로 볼 수 있습니다.

<a name="query-watcher"></a>
<!-- ### Query Watcher -->
### Query Watcher

<!-- The query watcher records the raw SQL, bindings, and execution time for all queries that are executed by your application. The watcher also tags any queries slower than 100 milliseconds as `slow`. You may customize the slow query threshold using the watcher's `slow` option: -->
쿼리 워처는 애플리케이션에서 실행된 모든 쿼리의 원본 SQL, 바인딩, 실행 시간 등을 기록합니다. 기본적으로 100밀리초를 초과하는 쿼리는 `slow` 태그가 붙습니다. 느린 쿼리 임계값은 워처의 `slow` 옵션으로 조정할 수 있습니다:

```
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    ...
],
```

<a name="redis-watcher"></a>
<!-- ### Redis Watcher -->
### Redis Watcher

<!-- The Redis watcher records all [Redis](/docs/11.x/redis) commands executed by your application. If you are using Redis for caching, cache commands will also be recorded by the Redis watcher. -->
Redis 워처는 애플리케이션에서 실행한 모든 [Redis](/docs/11.x/redis) 명령을 기록합니다. 캐시 스토리지로 Redis를 사용하는 경우, 캐시 관련 명령도 이 워처에 기록됩니다.

<a name="request-watcher"></a>
<!-- ### Request Watcher -->
### Request Watcher

<!-- The request watcher records the request, headers, session, and response data associated with any requests handled by the application. You may limit your recorded response data via the `size_limit` (in kilobytes) option: -->
요청 워처는 애플리케이션에서 처리된 요청, 헤더, 세션, 응답 데이터 등을 기록합니다. 기록되는 응답 데이터의 크기는 `size_limit` 옵션(단위: KB)으로 제한할 수 있습니다:

```
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    ...
],
```

<a name="schedule-watcher"></a>
<!-- ### Schedule Watcher -->
### Schedule Watcher

<!-- The schedule watcher records the command and output of any [scheduled tasks](/docs/11.x/scheduling) run by your application. -->
스케줄 워처는 애플리케이션이 실행하는 [scheduled tasks](/docs/11.x/scheduling)의 명령과 출력값을 기록합니다.

<a name="view-watcher"></a>
<!-- ### View Watcher -->
### View Watcher

<!-- The view watcher records the [view](/docs/11.x/views) name, path, data, and "composers" used when rendering views. -->
뷰 워처는 뷰의 [view](/docs/11.x/views), 경로, 뷰 데이터, 렌더링 시 사용된 "컴포저" 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
<!-- ## Displaying User Avatars -->
## Displaying User Avatars

<!-- The Telescope dashboard displays the user avatar for the user that was authenticated when a given entry was saved. By default, Telescope will retrieve avatars using the Gravatar web service. However, you may customize the avatar URL by registering a callback in your `App\Providers\TelescopeServiceProvider` class. The callback will receive the user's ID and email address and should return the user's avatar image URL: -->
Telescope 대시보드는 각 엔트리가 저장될 당시 인증된 사용자의 아바타 이미지를 표시합니다. 기본적으로 Gravatar 웹 서비스를 통해 아바타를 가져오지만, 원하는 경우 `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록해 아바타 URL을 직접 지정할 수 있습니다. 콜백에는 사용자 ID와 이메일이 전달되며, 해당 사용자의 아바타 이미지 URL을 반환하면 됩니다:

```
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (string $id, string $email) {
        return '/avatars/'.User::find($id)->avatar_path;
    });
}
```
