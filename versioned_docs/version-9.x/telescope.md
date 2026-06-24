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
[Laravel Telescope](https://github.com/laravel/telescope)는 로컬 환경에서 Laravel 개발을 도와주는 훌륭한 도구입니다. 텔레스코프는 애플리케이션으로 들어오는 요청, 예외, 로그 기록, 데이터베이스 쿼리, 큐 잡, 메일, 알림, 캐시 동작, 예약 작업, 변수 덤프 등 다양한 정보를 실시간으로 확인할 수 있는 기능을 제공합니다.

<!-- <img src="https://laravel.com/img/docs/telescope-example.png"/> -->
<img src="https://laravel.com/img/docs/telescope-example.png" />

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- You may use the Composer package manager to install Telescope into your Laravel project: -->
Composer 패키지 관리자를 사용하여 텔레스코프를 Laravel 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/telescope
```

<!-- After installing Telescope, publish its assets using the `telescope:install` Artisan command. After installing Telescope, you should also run the `migrate` command in order to create the tables needed to store Telescope's data: -->
설치가 완료되면, `telescope:install` 아티즌 명령어로 텔레스코프의 에셋을 배포합니다. 그리고 나서, 텔레스코프가 데이터를 저장하는 데 필요한 테이블을 생성하기 위해 `migrate` 명령어를 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate
```

<a name="migration-customization"></a>
<!-- #### Migration Customization -->
#### Migration Customization

<!-- If you are not going to use Telescope's default migrations, you should call the `Telescope::ignoreMigrations` method in the `register` method of your application's `App\Providers\AppServiceProvider` class. You may export the default migrations using the following command: `php artisan vendor:publish --tag=telescope-migrations` -->
기본적으로 제공되는 텔레스코프의 마이그레이션을 사용하지 않으려면, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 `Telescope::ignoreMigrations` 메서드를 호출해야 합니다. 기본 마이그레이션 파일을 내보내려면 다음 명령어를 사용할 수 있습니다: `php artisan vendor:publish --tag=telescope-migrations`

<a name="local-only-installation"></a>
<!-- ### Local Only Installation -->
### Local Only Installation

<!-- If you plan to only use Telescope to assist your local development, you may install Telescope using the `--dev` flag: -->
로컬 개발에서만 텔레스코프를 사용하려면, `--dev` 플래그를 활용해 설치하는 것이 좋습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate
```

<!-- After running `telescope:install`, you should remove the `TelescopeServiceProvider` service provider registration from your application's `config/app.php` configuration file. Instead, manually register Telescope's service providers in the `register` method of your `App\Providers\AppServiceProvider` class. We will ensure the current environment is `local` before registering the providers: -->
`telescope:install` 실행 후, `config/app.php` 파일에서 `TelescopeServiceProvider` 서비스 프로바이더 등록을 제거해야 합니다. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 아래와 같이 직접 프로바이더를 등록해야 합니다. 이때 현재 환경이 `local`일 때만 프로바이더를 등록하도록 처리합니다:

```
/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    if ($this->app->environment('local')) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}
```

<!-- Finally, you should also prevent the Telescope package from being [auto-discovered](/docs/9.x/packages#package-discovery) by adding the following to your `composer.json` file: -->
마지막으로, `composer.json` 파일 내의 extra 항목에 아래와 같이 추가하여 텔레스코프 패키지가 [auto-discovered](/docs/9.x/packages#package-discovery) 되지 않도록 해야 합니다:

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
텔레스코프의 에셋을 배포한 후에는 주 설정 파일이 `config/telescope.php`에 위치하게 됩니다. 이 설정 파일에서는 [watcher options](#available-watchers) 등 다양한 옵션을 조정할 수 있습니다. 각 설정 항목에는 용도에 대한 설명이 충분히 포함되어 있으니, 자세히 살펴보시기 바랍니다.

<!-- If desired, you may disable Telescope's data collection entirely using the `enabled` configuration option: -->
원한다면 전체적으로 텔레스코프의 데이터 수집 기능을 `enabled` 옵션으로 비활성화할 수도 있습니다:

```
'enabled' => env('TELESCOPE_ENABLED', true),
```

<a name="data-pruning"></a>
<!-- ### Data Pruning -->
### Data Pruning

<!-- Without pruning, the `telescope_entries` table can accumulate records very quickly. To mitigate this, you should [schedule](/docs/9.x/scheduling) the `telescope:prune` Artisan command to run daily: -->
데이터를 정리하지 않으면 `telescope_entries` 테이블에 레코드가 빠르게 쌓일 수 있습니다. 이를 방지하기 위해 [schedule](/docs/9.x/scheduling) 기능을 이용하여 매일 `telescope:prune` 아티즌 명령어가 실행되도록 해야 합니다:

```
$schedule->command('telescope:prune')->daily();
```

<!-- By default, all entries older than 24 hours will be pruned. You may use the `hours` option when calling the command to determine how long to retain Telescope data. For example, the following command will delete all records created over 48 hours ago: -->
기본적으로 24시간이 지난 모든 엔트리가 자동으로 삭제됩니다. 만약 더 긴 기간 데이터를 보관하고 싶다면, `hours` 옵션을 추가해서 유지 기간을 조정할 수 있습니다. 예를 들어, 아래와 같이 하면 48시간이 지난 데이터가 삭제됩니다:

```
$schedule->command('telescope:prune --hours=48')->daily();
```

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Telescope dashboard may be accessed at the `/telescope` route. By default, you will only be able to access this dashboard in the `local` environment. Within your `app/Providers/TelescopeServiceProvider.php` file, there is an [authorization gate](/docs/9.x/authorization#gates) definition. This authorization gate controls access to Telescope in **non-local** environments. You are free to modify this gate as needed to restrict access to your Telescope installation: -->
텔레스코프 대시보드는 `/telescope` 경로에서 접근할 수 있습니다. 기본적으로는 `local` 환경에서만 접속할 수 있습니다. 운영 환경 등 **로컬이 아닌** 환경에서의 접근을 통제하는 [authorization gate](/docs/9.x/authorization#gates) 정의가 `app/Providers/TelescopeServiceProvider.php` 파일에 포함되어 있습니다. 이 게이트를 원하는 대로 수정하여 텔레스코프 대시보드 접근을 제한할 수 있습니다:

```
/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
 *
 * @return void
 */
protected function gate()
{
    Gate::define('viewTelescope', function ($user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

> [!WARNING]
> 운영 환경에서는 `APP_ENV` 환경 변수를 반드시 `production`으로 설정해야 합니다. 그렇지 않으면 텔레스코프 대시보드가 외부에 공개될 수 있습니다.

<a name="upgrading-telescope"></a>
<!-- ## Upgrading Telescope -->
## Upgrading Telescope

<!-- When upgrading to a new major version of Telescope, it's important that you carefully review [the upgrade guide](https://github.com/laravel/telescope/blob/master/UPGRADE.md). -->
Telescope의 새 주요 버전으로 업그레이드할 때에는 반드시 [the upgrade guide](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 꼼꼼하게 확인해야 합니다.

<!-- In addition, when upgrading to any new Telescope version, you should re-publish Telescope's assets: -->
또한, 텔레스코프의 새 버전으로 업그레이드할 때마다 아래의 명령어로 관련 에셋을 항상 다시 배포해야 합니다:

```shell
php artisan telescope:publish
```

<!-- To keep the assets up-to-date and avoid issues in future updates, you may add the `vendor:publish --tag=laravel-assets` command to the `post-update-cmd` scripts in your application's `composer.json` file: -->
향후 업데이트 시 문제를 방지하고 에셋을 항상 최신 상태로 유지하기 위해, `composer.json`의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령어를 추가하는 것이 좋습니다:

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
`App\Providers\TelescopeServiceProvider` 클래스에서 정의된 `filter` 클로저를 사용하여 텔레스코프가 기록할 데이터를 세밀하게 제어할 수 있습니다. 기본적으로 이 클로저는 `local` 환경에서 모든 데이터를 기록하며, 그 외의 환경에서는 예외, 실패한 잡, 예약 작업, 모니터링된 태그가 포함된 데이터만 기록합니다:

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
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
`filter` 클로저가 개별 엔트리를 필터링하는 반면, `filterBatch` 메서드를 사용하면 하나의 요청 또는 콘솔 명령 전체에 대한 모든 데이터를 필터링할 수 있습니다. 클로저에서 `true`를 반환하면 해당 요청의 모든 엔트리가 텔레스코프에 기록됩니다:

```
use Illuminate\Support\Collection;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function ($entry) {
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
텔레스코프는 "태그"를 통해 엔트리를 검색할 수 있도록 지원합니다. 보통 태그는 Eloquent 모델 클래스명이나 인증된 사용자 ID 등 텔레스코프가 자동으로 엔트리에 추가하는 값입니다. 가끔 직접 원하는 사용자 정의 태그를 추가하고 싶을 때에는 `Telescope::tag` 메서드를 사용하면 됩니다. `tag` 메서드는 태그 배열을 반환해야 하는 클로저를 인수로 받으며, 반환된 태그는 텔레스코프가 자동으로 붙이는 태그와 합쳐집니다. 일반적으로 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 `tag`를 호출합니다:

```
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
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
텔레스코프의 "워처(watcher)"는 HTTP 요청 또는 콘솔 명령이 실행될 때 애플리케이션의 다양한 데이터를 수집합니다. 어떤 워처를 사용할지 `config/telescope.php` 설정 파일에서 자유롭게 조정할 수 있습니다:

```
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    ...
],
```

<!-- Some watchers also allow you to provide additional customization options: -->
몇몇 워처는 추가 옵션을 통해 세부 동작을 설정할 수도 있습니다:

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

<!-- The batch watcher records information about queued [batches](/docs/9.x/queues#job-batching), including the job and connection information. -->
배치 워처는 큐에 등록된 [batches](/docs/9.x/queues#job-batching)에 대한 정보(잡, 연결 정보 등)를 기록합니다.

<a name="cache-watcher"></a>
<!-- ### Cache Watcher -->
### Cache Watcher

<!-- The cache watcher records data when a cache key is hit, missed, updated and forgotten. -->
캐시 워처는 캐시 키가 적중, 미스(hit, miss), 업데이트, 삭제(포가튼)될 때의 데이터를 기록합니다.

<a name="command-watcher"></a>
<!-- ### Command Watcher -->
### Command Watcher

<!-- The command watcher records the arguments, options, exit code, and output whenever an Artisan command is executed. If you would like to exclude certain commands from being recorded by the watcher, you may specify the command in the `ignore` option within your `config/telescope.php` file: -->
명령어 워처는 Artisan 명령어가 실행될 때 인수, 옵션, 종료 코드, 출력 결과를 기록합니다. 특정 명령어를 기록 대상에서 제외하고 싶다면 `config/telescope.php` 파일의 `ignore` 옵션에 제외할 명령어 이름을 추가하면 됩니다:

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
덤프 워처는 변수 덤프를 기록하여 텔레스코프 대시보드에서 보여줍니다. Laravel에서 전역 `dump` 함수를 사용해 변수를 덤프할 수 있습니다. 이때 덤프 워처 탭이 브라우저에서 열려 있어야만 데이터가 기록됩니다. 탭이 열려 있지 않으면 덤프는 무시됩니다.

<a name="event-watcher"></a>
<!-- ### Event Watcher -->
### Event Watcher

<!-- The event watcher records the payload, listeners, and broadcast data for any [events](/docs/9.x/events) dispatched by your application. The Laravel framework's internal events are ignored by the Event watcher. -->
이벤트 워처는 애플리케이션에서 발생하는 [events](/docs/9.x/events)의 페이로드, 리스너, 브로드캐스트 데이터 등을 기록합니다. Laravel 프레임워크의 내부 이벤트는 기록 대상에서 제외됩니다.

<a name="exception-watcher"></a>
<!-- ### Exception Watcher -->
### Exception Watcher

<!-- The exception watcher records the data and stack trace for any reportable exceptions that are thrown by your application. -->
예외 워처는 애플리케이션에서 발생하는 예외 중 보고 가능한 예외의 데이터와 스택 트레이스를 기록합니다.

<a name="gate-watcher"></a>
<!-- ### Gate Watcher -->
### Gate Watcher

<!-- The gate watcher records the data and result of [gate and policy](/docs/9.x/authorization) checks by your application. If you would like to exclude certain abilities from being recorded by the watcher, you may specify those in the `ignore_abilities` option in your `config/telescope.php` file: -->
Gate 워처는 [gate and policy](/docs/9.x/authorization) 확인 시의 데이터와 결과를 기록합니다. 특정 능력을 기록에서 제외하고 싶다면 `config/telescope.php`의 `ignore_abilities` 옵션을 활용하면 됩니다:

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

<!-- The HTTP client watcher records outgoing [HTTP client requests](/docs/9.x/http-client) made by your application. -->
HTTP 클라이언트 워처는 애플리케이션에서 외부로 전송하는 [HTTP client requests](/docs/9.x/http-client)을 기록합니다.

<a name="job-watcher"></a>
<!-- ### Job Watcher -->
### Job Watcher

<!-- The job watcher records the data and status of any [jobs](/docs/9.x/queues) dispatched by your application. -->
잡 워처는 애플리케이션에서 발생하는 [jobs](/docs/9.x/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
<!-- ### Log Watcher -->
### Log Watcher

<!-- The log watcher records the [log data](/docs/9.x/logging) for any logs written by your application. -->
로그 워처는 애플리케이션에서 작성된 [log data](/docs/9.x/logging)를 모두 기록합니다.

<a name="mail-watcher"></a>
<!-- ### Mail Watcher -->
### Mail Watcher

<!-- The mail watcher allows you to view an in-browser preview of [emails](/docs/9.x/mail) sent by your application along with their associated data. You may also download the email as an `.eml` file. -->
메일 워처를 사용하면 애플리케이션에서 발송한 [emails](/docs/9.x/mail) 미리보기를 브라우저에서 확인할 수 있으며, 이메일 관련 데이터도 함께 볼 수 있습니다. 또한 이메일을 `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
<!-- ### Model Watcher -->
### Model Watcher

<!-- The model watcher records model changes whenever an Eloquent [model event](/docs/9.x/eloquent#events) is dispatched. You may specify which model events should be recorded via the watcher's `events` option: -->
모델 워처는 Eloquent [model event](/docs/9.x/eloquent#events)가 발생할 때마다 모델의 변경 내역을 기록합니다. 어떤 모델 이벤트를 기록할지 `events` 옵션으로 지정할 수 있습니다:

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
요청 중에 하이드레이션된(Eloquent로부터 인스턴스화된) 모델 개수까지 기록하려면 `hydrations` 옵션을 활성화하면 됩니다:

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

<!-- The notification watcher records all [notifications](/docs/9.x/notifications) sent by your application. If the notification triggers an email and you have the mail watcher enabled, the email will also be available for preview on the mail watcher screen. -->
알림 워처는 애플리케이션에서 발생하는 모든 [notifications](/docs/9.x/notifications)을 기록합니다. 해당 알림이 이메일을 포함하고, 메일 워처도 활성화되어 있다면 이메일 미리보기도 메일 워처 화면에서 볼 수 있습니다.

<a name="query-watcher"></a>
<!-- ### Query Watcher -->
### Query Watcher

<!-- The query watcher records the raw SQL, bindings, and execution time for all queries that are executed by your application. The watcher also tags any queries slower than 100 milliseconds as `slow`. You may customize the slow query threshold using the watcher's `slow` option: -->
쿼리 워처는 실행된 모든 쿼리의 원본 SQL, 바인딩 값, 실행 시간 정보를 기록합니다. 100밀리초보다 느린 쿼리는 자동으로 `slow` 태그가 붙습니다. 느린 쿼리의 기준 임계값은 `slow` 옵션으로 조정할 수 있습니다:

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

<!-- The Redis watcher records all [Redis](/docs/9.x/redis) commands executed by your application. If you are using Redis for caching, cache commands will also be recorded by the Redis watcher. -->
Redis 워처는 애플리케이션에서 실행하는 모든 [Redis](/docs/9.x/redis) 명령을 기록합니다. 만약 Redis를 캐시에 사용한다면 캐시 명령도 Redis 워처가 기록합니다.

<a name="request-watcher"></a>
<!-- ### Request Watcher -->
### Request Watcher

<!-- The request watcher records the request, headers, session, and response data associated with any requests handled by the application. You may limit your recorded response data via the `size_limit` (in kilobytes) option: -->
요청 워처는 요청, 헤더, 세션, 응답 데이터 등 애플리케이션에서 처리되는 요청과 관련된 다양한 정보를 기록합니다. 기록할 응답 데이터의 크기는 `size_limit`(킬로바이트 단위) 옵션으로 제한할 수 있습니다:

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

<!-- The schedule watcher records the command and output of any [scheduled tasks](/docs/9.x/scheduling) run by your application. -->
스케줄 워처는 애플리케이션에서 실행되는 [scheduled tasks](/docs/9.x/scheduling)의 명령어와 출력 결과를 기록합니다.

<a name="view-watcher"></a>
<!-- ### View Watcher -->
### View Watcher

<!-- The view watcher records the [view](/docs/9.x/views) name, path, data, and "composers" used when rendering views. -->
뷰 워처는 [view](/docs/9.x/views) 렌더링 시 사용된 뷰 이름, 경로, 데이터, "컴포저(composer)" 정보를 기록합니다.

<a name="displaying-user-avatars"></a>
<!-- ## Displaying User Avatars -->
## Displaying User Avatars

<!-- The Telescope dashboard displays the user avatar for the user that was authenticated when a given entry was saved. By default, Telescope will retrieve avatars using the Gravatar web service. However, you may customize the avatar URL by registering a callback in your `App\Providers\TelescopeServiceProvider` class. The callback will receive the user's ID and email address and should return the user's avatar image URL: -->
텔레스코프 대시보드는 각 엔트리가 기록될 당시 인증된 사용자의 아바타 이미지를 표시합니다. 기본적으로 텔레스코프는 Gravatar 웹 서비스를 이용해 아바타를 가져옵니다. 하지만, 필요하다면 `App\Providers\TelescopeServiceProvider` 클래스에 콜백을 등록해서 아바타 URL 방식을 커스터마이즈할 수 있습니다. 이 콜백은 사용자의 ID와 이메일을 받아 해당 아바타 이미지 URL을 반환해야 합니다:

```
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 *
 * @return void
 */
public function register()
{
    // ...

    Telescope::avatar(function ($id, $email) {
        return '/avatars/'.User::find($id)->avatar_path;
    });
}
```
