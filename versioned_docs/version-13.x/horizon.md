<!-- # Laravel Horizon -->
# Laravel Horizon

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Dashboard Authorization](#dashboard-authorization)
    - [Max Job Attempts](#max-job-attempts)
    - [Job Timeout](#job-timeout)
    - [Job Backoff](#job-backoff)
    - [Other Worker Options](#other-worker-options)
    - [Silenced Jobs](#silenced-jobs)
- [Balancing Strategies](#balancing-strategies)
    - [Auto Balancing](#auto-balancing)
    - [Simple Balancing](#simple-balancing)
    - [No Balancing](#no-balancing)
- [Upgrading Horizon](#upgrading-horizon)
- [Running Horizon](#running-horizon)
    - [Deploying Horizon](#deploying-horizon)
- [Tags](#tags)
- [Notifications](#notifications)
- [Metrics](#metrics)
- [Deleting Failed Jobs](#deleting-failed-jobs)
- [Clearing Jobs From Queues](#clearing-jobs-from-queues)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!NOTE]
> Laravel Horizon을 살펴보기 전에 먼저 Laravel의 기본 [queue services](/docs/13.x/queues)에 익숙해져야 합니다. Horizon은 Laravel의 큐에 추가 기능을 제공하므로, Laravel이 제공하는 기본 큐 기능을 아직 잘 모른다면 혼란스러울 수 있습니다.

<!-- [Laravel Horizon](https://github.com/laravel/horizon) provides a beautiful dashboard and code-driven configuration for your Laravel powered [Redis queues](/docs/13.x/queues). Horizon allows you to easily monitor key metrics of your queue system such as job throughput, runtime, and job failures. -->
[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis queues](/docs/13.x/queues)를 위한 아름다운 대시보드와 코드 기반 설정을 제공합니다. Horizon을 사용하면 잡 처리량, 실행 시간, 잡 실패와 같은 큐 시스템의 주요 메트릭을 손쉽게 모니터링할 수 있습니다.

<!-- When using Horizon, all of your queue worker configuration is stored in a single, simple configuration file. By defining your application's worker configuration in a version controlled file, you may easily scale or modify your application's queue workers when deploying your application. -->
Horizon을 사용하면 모든 큐 워커 설정이 하나의 단순한 설정 파일에 저장됩니다. 애플리케이션의 워커 구성을 버전 관리되는 파일에 정의함으로써, 배포 시 손쉽게 큐 워커의 스케일 조정이나 설정 변경이 가능합니다.

<img src="https://laravel.com/img/docs/horizon-example.png"/>

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Laravel Horizon을 사용하려면 큐를 구동하는 데 [Redis](https://redis.io)를 사용해야 합니다. 따라서 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 설정되어 있는지 확인해야 합니다. 현재 Horizon은 Redis Cluster와 호환되지 않습니다.

<!-- You may install Horizon into your project using the Composer package manager: -->
Composer 패키지 매니저를 사용하여 Horizon을 프로젝트에 설치할 수 있습니다.

```shell
composer require laravel/horizon
```

<!-- After installing Horizon, publish its assets using the `horizon:install` Artisan command: -->
설치 후에는 `horizon:install` Artisan 명령어로 Horizon의 에셋을 퍼블리시합니다.

```shell
php artisan horizon:install
```

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After publishing Horizon's assets, its primary configuration file will be located at `config/horizon.php`. This configuration file allows you to configure the queue worker options for your application. Each configuration option includes a description of its purpose, so be sure to thoroughly explore this file. -->
에셋을 퍼블리시한 후, Horizon의 주요 설정 파일은 `config/horizon.php`에 생성됩니다. 이 파일에서는 애플리케이션의 큐 워커 옵션을 세부적으로 설정할 수 있습니다. 각 설정에는 목적에 대한 설명이 달려 있으니, 이 파일을 꼼꼼히 살펴보는 것이 좋습니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 Redis 연결 이름은 예약되어 있으므로 `database.php` 설정 파일에서 다른 Redis 연결에 할당하거나 `horizon.php` 설정 파일에서 `use` 옵션의 값으로 지정해서는 안 됩니다.

<a name="content-security-policy-csp-nonce"></a>
<!-- #### Content Security Policy (CSP) Nonce -->
#### Content Security Policy (CSP) Nonce

<!-- If you would like to use a [nonce attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/nonce) on the script and style tags used in Horizon views as part of your [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP), you may use the `Horizon::cspNonce` method to specify the nonce to use. This method should typically be invoked within middleware so that a new nonce is assigned for each request: -->
Horizon 뷰에서 사용하는 script 및 style 태그에 [nonce attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/nonce)를 [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일부로 사용하려면 `Horizon::cspNonce` 메서드를 사용해 사용할 nonce를 지정할 수 있습니다. 일반적으로 이 메서드는 미들웨어에서 호출하여 각 요청에 새로운 nonce가 할당되도록 해야 합니다:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Horizon\Horizon;
use Symfony\Component\HttpFoundation\Response;

public function handle(Request $request, Closure $next): Response
{
    Horizon::cspNonce('csp-nonce');

    return $next($request);
}
```

<!-- You may add this middleware to the `middleware` option in your application's `config/horizon.php` configuration file: -->
애플리케이션의 `config/horizon.php` 설정 파일에서 `middleware` 옵션에 이 미들웨어를 추가할 수 있습니다:

```php
'middleware' => [
    'web',
    App\Http\Middleware\AddHorizonCspNonce::class,
],
```

<a name="environments"></a>
<!-- #### Environments -->
#### Environments

<!-- After installation, the primary Horizon configuration option that you should familiarize yourself with is the `environments` configuration option. This configuration option is an array of environments that your application runs on and defines the worker process options for each environment. By default, this entry contains a `production` and `local` environment. However, you are free to add more environments as needed: -->
Horizon 설치 후 가장 먼저 제어해야 하는 주요 옵션은 `environments` 설정입니다. 이 옵션은 애플리케이션이 동작하는 여러 환경(environment)에 따라 각 워커 프로세스 옵션을 정의합니다. 기본적으로는 `production`과 `local` 환경이 정의되어 있지만, 필요한 만큼 환경을 추가할 수 있습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],

    'local' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

<!-- You may also define a wildcard environment (`*`) which will be used when no other matching environment is found: -->
다음과 같이 와일드카드 환경(`*`)도 정의할 수 있으며, 일치하는 환경이 없을 때 사용됩니다.

```php
'environments' => [
    // ...

    '*' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

<!-- When you start Horizon, it will use the worker process configuration options for the environment that your application is running on. Typically, the environment is determined by the value of the `APP_ENV` [environment variable](/docs/13.x/configuration#determining-the-current-environment). For example, the default `local` Horizon environment is configured to start three worker processes and automatically balance the number of worker processes assigned to each queue. The default `production` environment is configured to start a maximum of 10 worker processes and automatically balance the number of worker processes assigned to each queue. -->
Horizon을 시작하면 애플리케이션이 실행 중인 환경에 대한 워커 프로세스 설정 옵션을 사용합니다. 일반적으로 환경은 `APP_ENV` [environment variable](/docs/13.x/configuration#determining-the-current-environment)의 값으로 결정됩니다. 예를 들어 기본 `local` Horizon 환경은 워커 프로세스 3개를 시작하고 각 큐에 할당된 워커 프로세스 수를 자동으로 균형 조정하도록 설정되어 있습니다. 기본 `production` 환경은 최대 10개의 워커 프로세스를 시작하고 각 큐에 할당된 워커 프로세스 수를 자동으로 균형 조정하도록 설정되어 있습니다.

> [!WARNING]
> Horizon을 실행하려는 각 [environment](/docs/13.x/configuration#environment-configuration)에 대한 항목이 `horizon` 설정 파일의 `environments` 부분에 포함되어 있는지 확인해야 합니다.

<a name="supervisors"></a>
<!-- #### Supervisors -->
#### Supervisors

<!-- As you can see in Horizon's default configuration file, each environment can contain one or more "supervisors". By default, the configuration file defines this supervisor as `supervisor-1`; however, you are free to name your supervisors whatever you want. Each supervisor is essentially responsible for "supervising" a group of worker processes and takes care of balancing worker processes across queues. -->
Horizon의 기본 설정 파일을 살펴보면, 각 환경에는 하나 이상의 "supervisor(감독자)"를 포함할 수 있습니다. 기본적으로 `supervisor-1`이라는 이름이 설정되어 있지만, 원하는 대로 이름을 지정할 수 있습니다. 각 supervisor는 하나의 워커 프로세스 그룹을 "감독하고", 큐 간 워커 프로세스의 적절한 분배를 관리합니다.

<!-- You may add additional supervisors to a given environment if you would like to define a new group of worker processes that should run in that environment. You may choose to do this if you would like to define a different balancing strategy or worker process count for a given queue used by your application. -->
특정 환경 내에서 추가 supervisor를 정의하면, 새로운 워커 프로세스 그룹을 생성하여 각기 다른 큐에 서로 다른 분산 전략이나 워커 수를 적용할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- #### Maintenance Mode -->
#### Maintenance Mode

<!-- While your application is in [maintenance mode](/docs/13.x/configuration#maintenance-mode), queued jobs will not be processed by Horizon unless the supervisor's `force` option is defined as `true` within the Horizon configuration file: -->
애플리케이션이 [maintenance mode](/docs/13.x/configuration#maintenance-mode) 상태인 동안에는 Horizon 설정 파일에서 supervisor의 `force` 옵션을 `true`로 설정하지 않는 한 Horizon이 큐에 대기 중인 잡을 처리하지 않습니다:

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'force' => true,
        ],
    ],
],
```

<a name="default-values"></a>
<!-- #### Default Values -->
#### Default Values

<!-- Within Horizon's default configuration file, you will notice a `defaults` configuration option. This configuration option specifies the default values for your application's [supervisors](#supervisors). The supervisor's default configuration values will be merged into the supervisor's configuration for each environment, allowing you to avoid unnecessary repetition when defining your supervisors. -->
Horizon의 기본 설정 파일에는 `defaults`라는 옵션이 있습니다. 이 옵션은 [supervisors](#supervisors)에 대한 기본값을 지정합니다. supervisor의 기본값은 각 환경의 supervisor 설정에 병합되어, 중복 구성을 줄이고 관리가 편리해집니다.

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Horizon dashboard may be accessed via the `/horizon` route. By default, you will only be able to access this dashboard in the `local` environment. However, within your `app/Providers/HorizonServiceProvider.php` file, there is an [authorization gate](/docs/13.x/authorization#gates) definition. This authorization gate controls access to Horizon in **non-local** environments. You are free to modify this gate as needed to restrict access to your Horizon installation: -->
Horizon 대시보드는 `/horizon` 라우트를 통해 이용할 수 있습니다. 기본적으로는 `local` 환경에서만 이 대시보드에 액세스할 수 있습니다. 하지만 `app/Providers/HorizonServiceProvider.php` 파일에는 [authorization gate](/docs/13.x/authorization#gates) 정의가 있습니다. 이 authorization gate는 **로컬이 아닌** 환경에서 Horizon에 대한 액세스를 제어합니다. 필요에 따라 이 gate를 수정하여 Horizon 설치에 대한 액세스를 제한할 수 있습니다:

```php
/**
 * Register the Horizon gate.
 *
 * This gate determines who can access Horizon in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewHorizon', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}
```

<a name="alternative-authentication-strategies"></a>
<!-- #### Alternative Authentication Strategies -->
#### Alternative Authentication Strategies

<!-- Remember that Laravel automatically injects the authenticated user into the gate closure. If your application is providing Horizon security via another method, such as IP restrictions, then your Horizon users may not need to "login". Therefore, you will need to change `function (User $user)` closure signature above to `function (User $user = null)` in order to force Laravel to not require authentication. -->
Laravel은 게이트 클로저에 인증된 사용자를 자동으로 주입합니다. 만약 IP 제한 등 다른 방식으로 Horizon 보안을 설정 중이라면, 사용자가 굳이 "로그인"할 필요가 없을 수 있습니다. 이런 경우 위 클로저의 시그니처를 `function (User $user)`에서 `function (User $user = null)`로 변경하여 인증 요구를 없앨 수 있습니다.

<a name="max-job-attempts"></a>
<!-- ### Max Job Attempts -->
### Max Job Attempts

> [!NOTE]
> 이러한 옵션을 조정하기 전에 Laravel의 기본 [queue services](/docs/13.x/queues#max-job-attempts-and-timeout)와 'attempts' 개념을 숙지했는지 확인하세요.

<!-- You can define the maximum number of attempts a job can consume within a supervisor's configuration: -->
supervisor 설정 내에서 각 작업이 시도할 수 있는 최대 횟수를 지정할 수 있습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'tries' => 10,
        ],
    ],
],
```

> [!NOTE]
> 이 옵션은 Artisan 명령어로 큐를 처리할 때 사용하는 `--tries` 옵션과 유사합니다.

<!-- Adjusting the `tries` option is essential when using middlewares such as `WithoutOverlapping` or `RateLimited` because they consume attempts. To handle this, adjust the `tries` configuration value either at the supervisor level or by defining the `$tries` property on the job class. -->
`WithoutOverlapping`, `RateLimited`과 같은 미들웨어를 사용할 경우 시도 횟수를 소비하므로 `tries` 옵션을 조정하는 것이 중요합니다. 이를 처리하려면 supervisor 단위에서 `tries` 설정 값을 조정하거나, 작업 클래스에 `$tries` 속성을 정의하여 적절히 조정해야 합니다.

<!-- If you don't set the `tries` option, Horizon defaults to a single attempt, unless the job class defines `$tries`, which takes precedence over the Horizon configuration. -->
`tries` 옵션을 명시하지 않으면 Horizon 기본값은 한 번만 실행하며, 작업 클래스에 `$tries` 속성이 있으면 Horizon 설정보다 우선됩니다.

<!-- Setting `tries` or `$tries` to 0 allows unlimited attempts, which is ideal when the number of attempts is uncertain. To prevent endless failures, you can limit the number of exceptions allowed by setting the `$maxExceptions` property on the job class. -->
`tries`나 `$tries`를 0으로 설정하면 무한정 시도가 가능합니다. 시도 횟수에 제한이 불분명할 때 유용합니다. 단, 무한 반복 실패를 막으려면 작업 클래스에 `$maxExceptions` 속성을 설정하여 예외 허용 횟수를 제한할 수 있습니다.

<a name="job-timeout"></a>
<!-- ### Job Timeout -->
### Job Timeout

<!-- Similarly, you can set a `timeout` value at the supervisor level, which specifies how many seconds a worker process can run a job before it's forcefully terminated. Once terminated, the job will either be retried or marked as failed, depending on your queue configuration: -->
supervisor 단위로 `timeout` 값을 설정할 수 있습니다. 이 값은 워커 프로세스가 하나의 작업을 강제로 종료시키기 전까지 최대 수행할 수 있는 초단위 시간입니다. 제한 시간 초과 시, 작업은 큐 설정에 따라 재시도되거나 실패로 처리됩니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'timeout' => 60,
        ],
    ],
],
```

> [!WARNING]
> `auto` 밸런싱 전략을 사용할 때 Horizon은 진행 중인 워커를 "멈춘" 상태로 간주하며, 스케일 다운 중 Horizon 타임아웃이 지나면 해당 워커를 강제로 종료합니다. 항상 Horizon 타임아웃이 잡 수준의 타임아웃보다 긴지 확인해야 합니다. 그렇지 않으면 잡이 실행 중간에 종료될 수 있습니다. 또한 `timeout` 값은 `config/queue.php` 설정 파일에 정의된 `retry_after` 값보다 항상 몇 초 이상 짧아야 합니다. 그렇지 않으면 잡이 두 번 처리될 수 있습니다.

<a name="job-backoff"></a>
<!-- ### Job Backoff -->
### Job Backoff

<!-- You can define the `backoff` value at the supervisor level to specify how long Horizon should wait before retrying a job that encounters an unhandled exception: -->
supervisor 단위에서 `backoff` 값을 설정하면, 예외 발생 후 작업 재시도까지 대기할 시간을 지정할 수 있습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'backoff' => 10,
        ],
    ],
],
```

<!-- You may also configure "exponential" backoffs by using an array for the `backoff` value. In this example, the retry delay will be 1 second for the first retry, 5 seconds for the second retry, 10 seconds for the third retry, and 10 seconds for every subsequent retry if there are more attempts remaining: -->
`backoff` 값에 배열을 사용하면 "지수적(exponential)" 백오프 설정도 가능합니다. 예를 들어 아래처럼 배열로 설정한 경우, 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초를 대기하며, 이후엔 계속 10초 동안 대기합니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'backoff' => [1, 5, 10],
        ],
    ],
],
```

<a name="other-worker-options"></a>
<!-- ### Other Worker Options -->
### Other Worker Options

<!-- In addition to `tries`, `timeout`, and `backoff`, each supervisor accepts several other options that control how its worker processes behave and when they are automatically restarted. Periodically restarting workers is a good practice for long-running processes, as it helps guard against memory leaks: -->
`tries`, `timeout`, `backoff` 외에도 각 supervisor는 워커 프로세스의 동작 방식과 자동으로 재시작되는 시점을 제어하는 여러 옵션을 지원합니다. 메모리 누수를 방지하는 데 도움이 되므로 장시간 실행되는 프로세스에서는 워커를 주기적으로 재시작하는 것이 좋습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'memory' => 128,
            'maxJobs' => 1000,
            'maxTime' => 3600,
            'sleep' => 3,
            'rest' => 0,
            'nice' => 0,
        ],
    ],
],
```

<div class="content-list" markdown="1">

<!-- - `memory` defines the maximum amount of memory, in megabytes, that a single worker process may consume before it is restarted. By default, this value is `128`. - `maxJobs` defines the number of jobs a worker should process before restarting. A value of `0` indicates that workers should not be restarted based on the number of jobs processed. By default, this value is `0`. - `maxTime` defines the number of seconds a worker should run before restarting. A value of `0` indicates that workers should not be restarted based on time. By default, this value is `0`. - `sleep` defines the number of seconds a worker should wait when no job is available before polling the queue for new jobs again. By default, this value is `3`. - `rest` defines the number of seconds to pause between processing each job. By default, this value is `0`. - `nice` defines the "niceness" (scheduling priority) of the worker processes. A higher value gives the process a lower priority. By default, this value is `0`. -->
- `memory`는 단일 워커 프로세스가 재시작되기 전에 사용할 수 있는 최대 메모리 양을 메가바이트 단위로 정의합니다. 기본값은 `128`입니다.
- `maxJobs`는 워커가 재시작되기 전에 처리해야 하는 잡의 수를 정의합니다. `0`은 처리한 잡의 수를 기준으로 워커를 재시작하지 않음을 나타냅니다. 기본값은 `0`입니다.
- `maxTime`은 워커가 재시작되기 전에 실행되어야 하는 시간을 초 단위로 정의합니다. `0`은 시간을 기준으로 워커를 재시작하지 않음을 나타냅니다. 기본값은 `0`입니다.
- `sleep`은 사용 가능한 잡이 없을 때 워커가 새 잡을 다시 확인하기 전에 대기할 시간을 초 단위로 정의합니다. 기본값은 `3`입니다.
- `rest`는 각 잡을 처리하는 사이에 일시 중지할 시간을 초 단위로 정의합니다. 기본값은 `0`입니다.
- `nice`는 워커 프로세스의 "niceness"(스케줄링 우선순위)를 정의합니다. 값이 클수록 프로세스의 우선순위가 낮아집니다. 기본값은 `0`입니다.

</div>

<a name="silenced-jobs"></a>
<!-- ### Silenced Jobs -->
### Silenced Jobs

<!-- Sometimes, you may not be interested in viewing certain jobs dispatched by your application or third-party packages. Instead of these jobs taking up space in your "Completed Jobs" list, you can silence them. To get started, add the job's class name to the `silenced` configuration option in your application's `horizon` configuration file: -->
특정 작업이 대시보드의 "완료된 작업" 목록에 표시되는 것을 원하지 않는 경우, 해당 작업을 음소거(silence)할 수 있습니다. 이를 위해, 작업 클래스명을 `horizon` 설정 파일의 `silenced` 옵션에 추가하세요.

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

<!-- In addition to silencing individual job classes, Horizon also supports silencing jobs based on [tags](#tags). This can be useful if you want to hide multiple jobs that share a common tag: -->
개별 작업 클래스 외에도, [tags](#tags) 기반으로도 음소거를 지원합니다. 동일 태그를 가진 여러 작업을 숨길 때 유용합니다.

```php
'silenced_tags' => [
    'notifications'
],
```

<!-- Alternatively, the job you wish to silence can implement the `Laravel\Horizon\Contracts\Silenced` interface. If a job implements this interface, it will automatically be silenced, even if it is not present in the `silenced` configuration array: -->
또는, 음소거 대상 작업이 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하도록 할 수도 있습니다. 이 경우, `silenced` 설정 배열에 추가하지 않아도 자동으로 음소거됩니다.

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
<!-- ## Balancing Strategies -->
## Balancing Strategies

<!-- Each supervisor can process one or more queues but unlike Laravel's default queue system, Horizon allows you to choose from three worker balancing strategies: `auto`, `simple`, and `false`. -->
각 supervisor는 하나 이상의 큐를 처리할 수 있습니다. Laravel의 기본 큐 시스템과 달리, Horizon은 워커 분산 전략으로 `auto`, `simple`, `false` 중 하나를 선택할 수 있습니다.

<a name="auto-balancing"></a>
<!-- ### Auto Balancing -->
### Auto Balancing

<!-- The `auto` strategy, which is the default strategy, adjusts the number of worker processes per queue based on the current workload of the queue. For example, if your `notifications` queue has 1,000 pending jobs while your `default` queue is empty, Horizon will allocate more workers to your `notifications` queue until the queue is empty. -->
기본값인 `auto` 전략은 각 큐의 현재 작업량에 따라 워커 프로세스 수를 자동으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 작업이 대기 중이고, `default` 큐는 비어 있다면, Horizon은 `notifications` 큐에 더 많은 워커를 할당하여 큐를 빠르게 소화하도록 합니다.

<!-- When using the `auto` strategy, you may also configure the `minProcesses` and `maxProcesses` configuration options: -->
`auto` 전략을 사용할 때는 `minProcesses`와 `maxProcesses` 옵션도 설정할 수 있습니다.

<div class="content-list" markdown="1">

<!-- - `minProcesses` defines the minimum number of worker processes per queue. This value must be greater than or equal to 1. - `maxProcesses` defines the maximum total number of worker processes Horizon may scale up to across all queues. This value should typically be greater than the number of queues multiplied by the `minProcesses` value. To prevent the supervisor from spawning any processes, you may set this value to 0. -->
- `minProcesses`는 큐마다 필요한 최소 워커 프로세스 수를 정의합니다. 이 값은 1 이상이어야 합니다.
- `maxProcesses`는 Horizon이 모든 큐에 걸쳐 확장할 수 있는 워커 프로세스의 최대 총 개수를 정의합니다. 일반적으로 이 값은 큐의 수에 `minProcesses` 값을 곱한 수보다 커야 합니다. supervisor가 프로세스를 생성하지 않도록 하려면 이 값을 0으로 설정할 수 있습니다.

</div>

<!-- For example, you may configure Horizon to maintain at least one process per queue and scale up to a total of 10 worker processes: -->
예를 들어, 큐마다 최소 1개의 프로세스를 유지하면서, 전체 워커 수는 최대 10개로 제한할 수 있습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default', 'notifications'],
            'balance' => 'auto',
            'autoScalingStrategy' => 'time',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
        ],
    ],
],
```

<!-- The `autoScalingStrategy` configuration option determines how Horizon will assign more worker processes to queues. You can choose between two strategies: -->
`autoScalingStrategy` 옵션은 Horizon이 큐에 워커를 증설할 때 어떤 기준을 사용할지 결정합니다.

<div class="content-list" markdown="1">

<!-- - The `time` strategy will assign workers based on the total estimated amount of time it will take to clear the queue. - The `size` strategy will assign workers based on the total number of jobs on the queue. -->
- `time` 전략은 큐를 비우는 데 걸리는 총 예상 시간을 기준으로 워커를 할당합니다.
- `size` 전략은 큐에 있는 전체 잡 수를 기준으로 워커를 할당합니다.

</div>

<!-- The `balanceMaxShift` and `balanceCooldown` configuration values determine how quickly Horizon will scale to meet worker demand. In the example above, a maximum of one new process will be created or destroyed every three seconds. You are free to tweak these values as necessary based on your application's needs. -->
`balanceMaxShift`와 `balanceCooldown` 값으로 Horizon이 워커 수를 증/감하는 속도를 조절할 수 있습니다. 위 설정에서는 3초마다 최대 1개의 프로세스가 생성 또는 제거됩니다. 애플리케이션 특성에 맞게 이 값을 조절할 수 있습니다.

<a name="auto-queue-priorities"></a>
<!-- #### Queue Priorities and Auto Balancing -->
#### Queue Priorities and Auto Balancing

<!-- When using the `auto` balancing strategy, Horizon does not enforce strict priority between queues. The order of queues in a supervisor's configuration does not affect how worker processes are assigned. Instead, Horizon relies on the selected `autoScalingStrategy` to dynamically allocate worker processes based on queue load. -->
`auto` 전략 사용 시, supervisor 설정 내 큐의 나열 순서는 우선순위에 영향을 주지 않습니다. 각 큐의 부하에 따라 동적으로 워커가 할당되고, `autoScalingStrategy`에 의해 분배됩니다.

<!-- For example, in the following configuration, the high queue is not prioritized over the default queue, despite appearing first in the list: -->
예를 들어 아래와 같이 구성해도, high 큐가 default 큐보다 우선 처리되지 않습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['high', 'default'],
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
    ],
],
```

<!-- If you need to enforce a relative priority between queues, you may define multiple supervisors and explicitly allocate processing resources: -->
큐 간 처리 우선순위를 명확히 설정하려면, supervisor를 여러 개 만들어 각각 다른 큐에 자원을 명시적으로 할당하세요.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default'],
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
        'supervisor-2' => [
            // ...
            'queue' => ['images'],
            'minProcesses' => 1,
            'maxProcesses' => 1,
        ],
    ],
],
```

<!-- In this example, the default `queue` can scale up to 10 processes, while the `images` queue is limited to one process. This configuration ensures that your queues can scale independently. -->
이 예시에서는 기본 `queue`는 10개까지 확장 가능하고, `images` 큐는 1개의 프로세스만 사용하도록 보장됩니다. 이렇게 하면 각 큐별로 독립적 스케일링이 가능합니다.

> [!NOTE]
> 리소스를 많이 사용하는 잡을 디스패치할 때는 제한된 `maxProcesses` 값을 가진 전용 큐에 할당하는 것이 좋을 때가 있습니다. 그렇지 않으면 이러한 잡이 CPU 리소스를 과도하게 사용해 시스템에 과부하를 일으킬 수 있습니다.

<a name="simple-balancing"></a>
<!-- ### Simple Balancing -->
### Simple Balancing

<!-- The `simple` strategy distributes worker processes evenly across the specified queues. With this strategy, Horizon does not automatically scale the number of worker processes. Rather, it uses a fixed number of processes: -->
`simple` 전략은 지정된 큐에 워커 프로세스를 균등하게 분배합니다. 이 전략에서는 워커 프로세스가 고정되며 자동 확장이 없습니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default', 'notifications'],
            'balance' => 'simple',
            'processes' => 10,
        ],
    ],
],
```

<!-- In the example above, Horizon will assign 5 processes to each queue, splitting the total of 10 evenly. -->
위 예시에서는 10개의 프로세스가 2개 큐에 각 5개씩 균등 할당됩니다.

<!-- If you'd like to control the number of worker processes assigned to each queue individually, you can define multiple supervisors: -->
개별 큐별로 워커 수를 따로 조절하려면, supervisor를 여러 개 정의하면 됩니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default'],
            'balance' => 'simple',
            'processes' => 10,
        ],
        'supervisor-notifications' => [
            // ...
            'queue' => ['notifications'],
            'balance' => 'simple',
            'processes' => 2,
        ],
    ],
],
```

<!-- With this configuration, Horizon will assign 10 processes to the `default` queue and 2 processes to the `notifications` queue. -->
이렇게 하면 `default` 큐에는 10개, `notifications` 큐에는 2개의 프로세스가 할당됩니다.

<a name="no-balancing"></a>
<!-- ### No Balancing -->
### No Balancing

<!-- When the `balance` option is set to `false`, Horizon processes queues strictly in the order they're listed, similar to Laravel's default queue system. However, it will still scale the number of worker processes if jobs begin to accumulate: -->
`balance` 옵션을 `false`로 설정할 경우, Laravel 기본 큐 시스템과 마찬가지로 큐에 나열된 순서대로 작업을 처리합니다. 단, 작업이 누적되면 워커 수는 여전히 확장됩니다.

```php
'environments' => [
    'production' => [
        'supervisor-1' => [
            // ...
            'queue' => ['default', 'notifications'],
            'balance' => false,
            'minProcesses' => 1,
            'maxProcesses' => 10,
        ],
    ],
],
```

<!-- In the example above, jobs in the `default` queue are always prioritized over jobs in the `notifications` queue. For instance, if there are 1,000 jobs in `default` and only 10 in `notifications`, Horizon will fully process all `default` jobs before handling any from `notifications`. -->
위 예시에서는 `default` 큐 작업이 항상 `notifications` 큐 작업보다 우선 처리됩니다. 만약 `default` 큐에 1,000개 작업, `notifications` 큐에 10개가 있다면, `default` 큐의 작업을 모두 처리한 후에야 `notifications` 큐 작업을 처리하게 됩니다.

<!-- You can control Horizon's ability to scale worker processes using the `minProcesses` and `maxProcesses` options: -->
워커 확장 범위는 `minProcesses`와 `maxProcesses` 옵션으로 제어할 수 있습니다.

<div class="content-list" markdown="1">

<!-- - `minProcesses` defines the minimum number of worker processes in total. This value must be greater than or equal to 1. - `maxProcesses` defines the maximum total number of worker processes Horizon may scale up to. -->
- `minProcesses`는 전체 워커 프로세스의 최소 개수를 정의합니다. 이 값은 1 이상이어야 합니다.
- `maxProcesses`는 Horizon이 확장할 수 있는 전체 워커 프로세스의 최대 개수를 정의합니다.

</div>

<a name="upgrading-horizon"></a>
<!-- ## Upgrading Horizon -->
## Upgrading Horizon

<!-- When upgrading to a new major version of Horizon, it's important that you carefully review [the upgrade guide](https://github.com/laravel/horizon/blob/master/UPGRADE.md). -->
Horizon의 주요 버전을 업그레이드할 때는 반드시 [the upgrade guide](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다.

<a name="running-horizon"></a>
<!-- ## Running Horizon -->
## Running Horizon

<!-- Once you have configured your supervisors and workers in your application's `config/horizon.php` configuration file, you may start Horizon using the `horizon` Artisan command. This single command will start all of the configured worker processes for the current environment: -->
`config/horizon.php` 파일에서 supervisor와 worker를 모두 설정했다면, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 단일 명령어가 현재 환경에 맞는 모든 워커 프로세스를 구동합니다.

```shell
php artisan horizon
```

<!-- You may pause the Horizon process and instruct it to continue processing jobs using the `horizon:pause` and `horizon:continue` Artisan commands: -->
처리 중인 Horizon 프로세스를 일시정지 또는 재개하려면 `horizon:pause`와 `horizon:continue` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:pause

php artisan horizon:continue
```

<!-- You may also pause and continue specific Horizon [supervisors](#supervisors) using the `horizon:pause-supervisor` and `horizon:continue-supervisor` Artisan commands: -->
특정 Horizon [supervisors](#supervisors)를 일시정지하거나 재개하려면 `horizon:pause-supervisor`와 `horizon:continue-supervisor` Artisan 명령어를 사용하세요.

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

<!-- You may check the current status of the Horizon process using the `horizon:status` Artisan command: -->
현재 Horizon 프로세스 상태를 확인하려면 `horizon:status` Artisan 명령어를 사용하세요.

```shell
php artisan horizon:status
```

<!-- You may check the current status of a specific Horizon [supervisor](#supervisors) using the `horizon:supervisor-status` Artisan command: -->
특정 Horizon [supervisor](#supervisors)의 상태를 확인하려면 `horizon:supervisor-status` Artisan 명령어를 사용하세요.

```shell
php artisan horizon:supervisor-status supervisor-1
```

<!-- You may gracefully terminate the Horizon process using the `horizon:terminate` Artisan command. Any jobs that are currently being processed will be completed and then Horizon will stop executing: -->
Horizon 프로세스를 정상적으로 종료하려면 `horizon:terminate` Artisan 명령어를 사용할 수 있습니다. 현재 처리 중인 작업이 마무리되고 Horizon이 종료됩니다.

```shell
php artisan horizon:terminate
```

<a name="automatically-restarting-horizon"></a>
<!-- #### Automatically Restarting Horizon -->
#### Automatically Restarting Horizon

<!-- During local development, you may run the `horizon:listen` command. When using the `horizon:listen` command, you don't have to manually restart Horizon when you want to reload your updated code. Before using this feature, you should ensure that [Node](https://nodejs.org) is installed within your local development environment. In addition, you should install the [Chokidar](https://github.com/paulmillr/chokidar) file-watching library within your project: -->
로컬 개발 중에는 `horizon:listen` 명령어를 사용할 수 있습니다. `horizon:listen` 명령어를 사용하면, 코드가 변경될 때마다 Horizon을 수동으로 재시작하지 않아도 됩니다. 사용 전 반드시 [Node](https://nodejs.org)를 로컬 환경에 설치해야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리도 설치해야 합니다.

```shell
npm install --save-dev chokidar
```

<!-- Once Chokidar is installed, you may start Horizon using the `horizon:listen` command: -->
Chokidar 설치 후, `horizon:listen` 명령어로 Horizon을 시작할 수 있습니다.

```shell
php artisan horizon:listen
```

<!-- When running within Docker or Vagrant, you should use the `--poll` option: -->
Docker나 Vagrant 환경에서는 `--poll` 옵션을 사용하세요.

```shell
php artisan horizon:listen --poll
```

<!-- You may configure the directories and files that should be watched using the `watch` configuration option within your application's `config/horizon.php` configuration file: -->
감시할 파일 및 디렉터리는 애플리케이션의 `config/horizon.php`에서 `watch` 옵션으로 설정할 수 있습니다.

```php
'watch' => [
    'app',
    'bootstrap',
    'config',
    'database',
    'public/**/*.php',
    'resources/**/*.php',
    'routes',
    'composer.lock',
    '.env',
],
```

<a name="deploying-horizon"></a>
<!-- ### Deploying Horizon -->
### Deploying Horizon

<!-- When you're ready to deploy Horizon to your application's actual server, you should configure a process monitor to monitor the `php artisan horizon` command and restart it if it exits unexpectedly. Don't worry, we'll discuss how to install a process monitor below. -->
실제 서버에 Horizon을 배포할 때는 프로세스 모니터를 이용해 `php artisan horizon` 명령어를 관리하며, 예기치 않게 종료될 때 재시작하도록 설정하세요. 아래에서 프로세스 모니터 설치 방법을 안내합니다.

<!-- During your application's deployment process, you should instruct the Horizon process to terminate so that it will be restarted by your process monitor and receive your code changes: -->
배포 과정에서는 Horizon 프로세스가 종료되도록 지시하여, 프로세스 모니터가 이를 재시작하면서 코드 변경 사항을 반영하도록 해야 합니다.

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
<!-- #### Installing Supervisor -->
#### Installing Supervisor

<!-- Supervisor is a process monitor for the Linux operating system and will automatically restart your `horizon` process if it stops executing. To install Supervisor on Ubuntu, you may use the following command. If you are not using Ubuntu, you can likely install Supervisor using your operating system's package manager: -->
Supervisor는 Linux 운영체제용 프로세스 모니터로, `horizon` 프로세스가 중단될 경우 자동 재시작합니다. Ubuntu에 Supervisor를 설치하려면 아래 명령어를 사용할 수 있습니다. 다른 OS에서는 운영체제의 패키지 매니저로 Supervisor를 설치하세요.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor를 직접 설정하는 일이 부담스럽다면 Laravel 애플리케이션의 백그라운드 프로세스를 관리할 수 있는 [Laravel Cloud](https://cloud.laravel.com)를 사용해 보세요.

<a name="supervisor-configuration"></a>
<!-- #### Supervisor Configuration -->
#### Supervisor Configuration

<!-- Supervisor configuration files are typically stored within your server's `/etc/supervisor/conf.d` directory. Within this directory, you may create any number of configuration files that instruct supervisor how your processes should be monitored. For example, let's create a `horizon.conf` file that starts and monitors a `horizon` process: -->
Supervisor 설정 파일은 보통 서버의 `/etc/supervisor/conf.d` 디렉터리에 저장됩니다. 이 디렉터리 내에 여러 개의 설정 파일을 생성하여, 각 프로세스를 어떻게 모니터링할지 지정할 수 있습니다. 예시로, `horizon.conf` 파일을 생성해서 `horizon` 프로세스를 시작/모니터링합니다.

```ini
[program:horizon]
process_name=%(program_name)s
command=php /home/forge/example.com/artisan horizon
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/horizon.log
stopwaitsecs=3600
```

<!-- When defining your Supervisor configuration, you should ensure that the value of `stopwaitsecs` is greater than the number of seconds consumed by your longest running job. Otherwise, Supervisor may kill the job before it is finished processing. -->
`stopwaitsecs` 값은 최장 실행 작업의 소요 시간보다 항상 크게 지정해야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 프로세스를 강제로 종료할 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 기반 서버에서 유효하지만, 다른 서버 운영 체제에서는 Supervisor 설정 파일의 위치와 예상되는 파일 확장자가 다를 수 있습니다. 자세한 내용은 서버의 문서를 참고하세요.

<a name="starting-supervisor"></a>
<!-- #### Starting Supervisor -->
#### Starting Supervisor

<!-- Once the configuration file has been created, you may update the Supervisor configuration and start the monitored processes using the following commands: -->
설정 파일 생성 후, 다음 명령어로 Supervisor 설정을 갱신하고 모니터링을 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 실행에 관한 자세한 정보는 [Supervisor documentation](http://supervisord.org/index.html)을 참고하세요.

<a name="tags"></a>
<!-- ## Tags -->
## Tags

<!-- Horizon allows you to assign "tags" to jobs, including mailables, broadcast events, notifications, and queued event listeners. In fact, Horizon will intelligently and automatically tag most jobs depending on the Eloquent models that are attached to the job. For example, take a look at the following job: -->
Horizon은 작업, 메일(메일러블), 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등에 "태그"를 지정할 수 있습니다. Horizon은 대다수 작업을 대상으로 자동으로 태그를 지정하며, 이는 해당 작업에 연결된 Eloquent 모델을 기준으로 합니다. 예를 들어, 아래 작업 클래스를 살펴보세요.

```php
<?php

namespace App\Jobs;

use App\Models\Video;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class RenderVideo implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Video $video,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        // ...
    }
}
```

<!-- If this job is queued with an `App\Models\Video` instance that has an `id` attribute of `1`, it will automatically receive the tag `App\Models\Video:1`. This is because Horizon will search the job's properties for any Eloquent models. If Eloquent models are found, Horizon will intelligently tag the job using the model's class name and primary key: -->
이 작업이 `id` 속성값이 `1`인 `App\Models\Video` 인스턴스와 함께 큐에 등록된다면, 자동으로 `App\Models\Video:1`이라는 태그가 부여됩니다. Horizon이 작업 속성에서 Eloquent 모델을 찾아, 클래스명 및 기본 키(primary key) 조합으로 태그를 생성하기 때문입니다.

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
<!-- #### Manually Tagging Jobs -->
#### Manually Tagging Jobs

<!-- If you would like to manually define the tags for one of your queueable objects, you may define a `tags` method on the class: -->
큐 작업에 직접 지정할 태그를 정의하려면, 클래스에 `tags` 메서드를 정의하세요.

```php
class RenderVideo implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the job.
     *
     * @return array<int, string>
     */
    public function tags(): array
    {
        return ['render', 'video:'.$this->video->id];
    }
}
```

<a name="manually-tagging-event-listeners"></a>
<!-- #### Manually Tagging Event Listeners -->
#### Manually Tagging Event Listeners

<!-- When retrieving the tags for a queued event listener, Horizon will automatically pass the event instance to the `tags` method, allowing you to add event data to the tags: -->
이벤트 리스너가 큐에 등록되어 있을 때 Horizon이 태그를 가져오는 방식은, 이벤트 인스턴스를 `tags` 메서드에 전달하는 것입니다. 이를 이용해 이벤트 데이터를 이용한 태그 지정이 가능합니다.

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * Get the tags that should be assigned to the listener.
     *
     * @return array<int, string>
     */
    public function tags(VideoRendered $event): array
    {
        return ['video:'.$event->video->id];
    }
}
```

<a name="notifications"></a>
<!-- ## Notifications -->
## Notifications

> [!WARNING]
> Horizon에서 Slack 또는 SMS 알림을 전송하도록 구성할 때는 [prerequisites for the relevant notification channel](/docs/13.x/notifications)을 검토해야 합니다.

<!-- If you would like to be notified when one of your queues has a long wait time, you may use the `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, and `Horizon::routeSmsNotificationsTo` methods. You may call these methods from the `boot` method of your application's `App\Providers\HorizonServiceProvider`: -->
특정 큐의 대기 시간이 과도하게 길어졌을 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드는 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하세요.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    parent::boot();

    Horizon::routeSmsNotificationsTo('15556667777');
    Horizon::routeMailNotificationsTo('example@example.com');
    Horizon::routeSlackNotificationsTo('slack-webhook-url', '#channel');
}
```

<a name="configuring-notification-wait-time-thresholds"></a>
<!-- #### Configuring Notification Wait Time Thresholds -->
#### Configuring Notification Wait Time Thresholds

<!-- You may configure how many seconds are considered a "long wait" within your application's `config/horizon.php` configuration file. The `waits` configuration option within this file allows you to control the long wait threshold for each connection / queue combination. Any undefined connection / queue combinations will default to a long wait threshold of 60 seconds: -->
큐 대기 시간이 얼마나 길 경우를 "장시간 대기"로 간주할지, 애플리케이션의 `config/horizon.php`의 `waits` 옵션으로 지정할 수 있습니다. 각 연결/큐 조합별 임계값을 초 단위로 다음과 같이 조정하세요. 정의하지 않은 조합은 기본값 60초가 적용됩니다.

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<!-- Setting a queue's threshold to `0` will disable long wait notifications for that queue. -->
큐의 임계값을 `0`으로 설정하면 해당 큐에 대해 긴 대기 시간 알림이 비활성화됩니다.

<a name="metrics"></a>
<!-- ## Metrics -->
## Metrics

<!-- Horizon includes a metrics dashboard which provides information regarding your job and queue wait times and throughput. In order to populate this dashboard, you should configure Horizon's `snapshot` Artisan command to run every five minutes in your application's `routes/console.php` file: -->
Horizon은 작업 및 큐 대기 시간, 처리량 관련 정보를 확인할 수 있는 메트릭 대시보드를 제공합니다. 대시보드에 데이터를 채우려면, `routes/console.php` 파일에서 Horizon의 `snapshot` Artisan 명령어가 5분마다 실행되도록 스케줄링해야 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

<!-- You may configure how many snapshots Horizon retains for its metrics graphs using the `metrics.trim_snapshots` option in your application's `config/horizon.php` configuration file. Because this option limits the number of snapshots rather than their age, the retention period depends on how frequently the `horizon:snapshot` command runs: -->
애플리케이션의 `config/horizon.php` 설정 파일에서 `metrics.trim_snapshots` 옵션을 사용해 Horizon이 메트릭 그래프에 보관할 스냅샷 수를 설정할 수 있습니다. 이 옵션은 스냅샷의 보관 기간이 아니라 개수를 제한하므로, 보관 기간은 `horizon:snapshot` 명령어가 실행되는 빈도에 따라 달라집니다:

```php
'metrics' => [
    'trim_snapshots' => [
        'job' => 24,
        'queue' => 24,
    ],
],
```

<!-- If you would like to delete all metric data, you can invoke the `horizon:clear-metrics` Artisan command: -->
모든 메트릭 데이터를 삭제하고 싶다면, `horizon:clear-metrics` Artisan 명령어를 사용하세요.

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
<!-- ## Deleting Failed Jobs -->
## Deleting Failed Jobs

<!-- If you would like to delete a failed job, you may use the `horizon:forget` command. The `horizon:forget` command accepts the ID or UUID of the failed job as its only argument: -->
개별 실패 작업을 삭제하려면 `horizon:forget` 명령어를 사용하면 됩니다. `horizon:forget` 명령어는 실패한 작업의 ID 또는 UUID 하나만 인수로 받습니다.

```shell
php artisan horizon:forget 5
```

<!-- If you would like to delete all failed jobs, you may provide the `--all` option to the `horizon:forget` command: -->
모든 실패 작업을 삭제하려면, `horizon:forget` 명령어에 `--all` 옵션을 제공하세요.

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
<!-- ## Clearing Jobs From Queues -->
## Clearing Jobs From Queues

<!-- If you would like to delete all jobs from your application's default queue, you may do so using the `horizon:clear` Artisan command: -->
애플리케이션 기본 큐에 누적된 모든 작업을 삭제하고 싶다면, `horizon:clear` Artisan 명령어를 사용하세요.

```shell
php artisan horizon:clear
```

<!-- You may provide the `queue` option to delete jobs from a specific queue: -->
특정 큐의 작업만 삭제하려면 `queue` 옵션을 지정하세요.

```shell
php artisan horizon:clear --queue=emails
```
