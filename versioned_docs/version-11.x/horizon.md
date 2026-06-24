<!-- # Laravel Horizon -->
# Laravel Horizon

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Balancing Strategies](#balancing-strategies)
    - [Dashboard Authorization](#dashboard-authorization)
    - [Silenced Jobs](#silenced-jobs)
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
> Laravel Horizon을 시작하기 전에, Laravel 기본 [queue services](/docs/11.x/queues)에 대해 충분히 숙지하는 것이 좋습니다. 호라이즌은 Laravel 큐에 추가적인 기능을 제공하므로, 기본 큐 기능을 잘 모르면 혼란스러울 수 있습니다.

<!-- [Laravel Horizon](https://github.com/laravel/horizon) provides a beautiful dashboard and code-driven configuration for your Laravel powered [Redis queues](/docs/11.x/queues). Horizon allows you to easily monitor key metrics of your queue system such as job throughput, runtime, and job failures. -->
[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis queues](/docs/11.x/queues)를 위한 보기 좋은 대시보드와 코드 기반 설정 방식을 제공합니다. 호라이즌을 사용하면 작업 처리량, 실행 시간, 작업 실패 등 큐 시스템의 핵심 지표를 손쉽게 모니터링할 수 있습니다.

<!-- When using Horizon, all of your queue worker configuration is stored in a single, simple configuration file. By defining your application's worker configuration in a version controlled file, you may easily scale or modify your application's queue workers when deploying your application. -->
호라이즌을 사용하면 모든 큐 워커 설정이 하나의 간단한 설정 파일에 저장됩니다. 애플리케이션의 워커 구성을 버전 관리 파일로 정의하면, 애플리케이션을 배포할 때 손쉽게 큐 워커를 확장하거나 변경할 수 있습니다.

<!-- <img src="https://laravel.com/img/docs/horizon-example.png"/> -->
<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Laravel Horizon은 큐 구동을 위해 [Redis](https://redis.io)를 필수로 사용합니다. 따라서, 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 반드시 `redis`로 지정되어 있는지 확인해야 합니다.

<!-- You may install Horizon into your project using the Composer package manager: -->
Composer 패키지 매니저를 사용하여 프로젝트에 호라이즌을 설치할 수 있습니다.

```shell
composer require laravel/horizon
```

<!-- After installing Horizon, publish its assets using the `horizon:install` Artisan command: -->
호라이즌 설치 후, `horizon:install` 아티즌 명령어로 자산을 배포해 주세요.

```shell
php artisan horizon:install
```

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After publishing Horizon's assets, its primary configuration file will be located at `config/horizon.php`. This configuration file allows you to configure the queue worker options for your application. Each configuration option includes a description of its purpose, so be sure to thoroughly explore this file. -->
호라이즌 자산을 배포하면 주 설정 파일이 `config/horizon.php`에 생성됩니다. 이 설정 파일에서 애플리케이션의 큐 워커 옵션을 설정할 수 있습니다. 각 옵션 옆에는 해당 옵션이 어떤 역할을 하는지 설명되어 있으니, 꼭 파일 전체를 꼼꼼히 확인해 보시기 바랍니다.

> [!WARNING]
> 호라이즌은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 연결 이름은 예약되어 있으므로, `database.php` 설정 파일의 다른 Redis 연결이나 `horizon.php` 설정 파일의 `use` 옵션 값에 이 이름을 할당해서는 안 됩니다.

<a name="environments"></a>
<!-- #### Environments -->
#### Environments

<!-- After installation, the primary Horizon configuration option that you should familiarize yourself with is the `environments` configuration option. This configuration option is an array of environments that your application runs on and defines the worker process options for each environment. By default, this entry contains a `production` and `local` environment. However, you are free to add more environments as needed: -->
설치 후 가장 먼저 알아야 할 중요한 설정이 `environments` 항목입니다. 이 설정 옵션은 애플리케이션이 실행되는 여러 환경별로 배열을 구성하고, 각 환경별로 워커 프로세스 옵션을 정의합니다. 기본적으로 `production`과 `local` 환경이 있으며, 필요에 따라 더 추가할 수 있습니다.

```
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
또한 와일드카드 환경(`*`)을 정의해, 다른 환경과 일치하지 않을 때 사용할 기본값을 지정할 수도 있습니다.

```
'environments' => [
    // ...

    '*' => [
        'supervisor-1' => [
            'maxProcesses' => 3,
        ],
    ],
],
```

<!-- When you start Horizon, it will use the worker process configuration options for the environment that your application is running on. Typically, the environment is determined by the value of the `APP_ENV` [environment variable](/docs/11.x/configuration#determining-the-current-environment). For example, the default `local` Horizon environment is configured to start three worker processes and automatically balance the number of worker processes assigned to each queue. The default `production` environment is configured to start a maximum of 10 worker processes and automatically balance the number of worker processes assigned to each queue. -->
호라이즌을 실행하면, 애플리케이션이 작동 중인 환경의 워커 프로세스 설정이 자동으로 적용됩니다. 주로 환경은 `APP_ENV` [environment variable](/docs/11.x/configuration#determining-the-current-environment)의 값에 따라 결정됩니다. 예를 들어, 기본값인 `local` 환경에서는 워커 프로세스가 3개로 시작되고, 각 큐에 할당된 워커 숫자를 자동으로 분산합니다. 기본 `production` 환경은 최대 10개의 워커 프로세스를 실행하며, 각 큐에 할당된 워커 수를 자동으로 조절합니다.

> [!WARNING]
> 호라이즌을 운영할 모든 [environment](/docs/11.x/configuration#environment-configuration)에 대해 `horizon` 설정 파일의 `environments` 항목에 반드시 값을 추가해야 합니다.

<a name="supervisors"></a>
<!-- #### Supervisors -->
#### Supervisors

<!-- As you can see in Horizon's default configuration file, each environment can contain one or more "supervisors". By default, the configuration file defines this supervisor as `supervisor-1`; however, you are free to name your supervisors whatever you want. Each supervisor is essentially responsible for "supervising" a group of worker processes and takes care of balancing worker processes across queues. -->
호라이즌의 기본 설정 파일을 보면, 각 환경 아래에 하나 이상의 "슈퍼바이저"를 둘 수 있습니다. 기본적으로 `supervisor-1`이라는 이름으로 정의되어 있지만, 원하는 이름으로 자유롭게 지정할 수 있습니다. 각각의 슈퍼바이저는 하나의 워커 그룹을 "감독"하며, 여러 큐들에 워커 프로세스를 적절히 분배하는 역할을 합니다.

<!-- You may add additional supervisors to a given environment if you would like to define a new group of worker processes that should run in that environment. You may choose to do this if you would like to define a different balancing strategy or worker process count for a given queue used by your application. -->
특정 환경에서 별도의 워커 그룹이 필요하다면, 슈퍼바이저를 추가로 정의할 수 있습니다. 예를 들어, 큐별로 다른 부하 분산 전략이나 워커 프로세스 수를 지정하고자 할 때 슈퍼바이저를 여러 개 생성할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- #### Maintenance Mode -->
#### Maintenance Mode

<!-- While your application is in [maintenance mode](/docs/11.x/configuration#maintenance-mode), queued jobs will not be processed by Horizon unless the supervisor's `force` option is defined as `true` within the Horizon configuration file: -->
애플리케이션이 [maintenance mode](/docs/11.x/configuration#maintenance-mode)인 동안에는, 호라이즌이 큐 작업을 처리하지 않습니다. 만약 유지보수 모드에서도 작업 처리가 필요하다면, 호라이즌 설정 파일의 슈퍼바이저에 `force` 옵션을 `true`로 추가해 주세요.

```
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
호라이즌 기본 설정 파일에는 `defaults`라는 옵션이 포함되어 있습니다. 이 옵션은 [supervisors](#supervisors)의 기본값을 지정합니다. 각 환경별 슈퍼바이저 설정에 기본값이 합쳐지므로, 같은 설정을 반복해서 작성할 필요가 없습니다.

<a name="balancing-strategies"></a>
<!-- ### Balancing Strategies -->
### Balancing Strategies

<!-- Unlike Laravel's default queue system, Horizon allows you to choose from three worker balancing strategies: `simple`, `auto`, and `false`. The `simple` strategy splits incoming jobs evenly between worker processes: -->
Laravel의 기본 큐 시스템과 달리, 호라이즌에서는 세 가지 워커 부하 분산 전략을 선택할 수 있습니다: `simple`, `auto`, `false`입니다. `simple` 전략은 들어오는 작업을 워커 프로세스에 고르게 나눠줍니다.

```
'balance' => 'simple',
```

<!-- The `auto` strategy, which is the configuration file's default, adjusts the number of worker processes per queue based on the current workload of the queue. For example, if your `notifications` queue has 1,000 pending jobs while your `render` queue is empty, Horizon will allocate more workers to your `notifications` queue until the queue is empty. -->
기본값인 `auto` 전략은 각각의 큐가 현재 얼마 만큼의 대기 작업을 가지고 있는지에 따라 큐별 워커 프로세스 수를 자동으로 조절합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고, `render` 큐가 비어 있다면, 호라이즌은 워커를 `notifications` 큐에 더 많이 할당하여 큐가 비워질 때까지 처리합니다.

<!-- When using the `auto` strategy, you may define the `minProcesses` and `maxProcesses` configuration options to control the minimum number of processes per queue and the maximum number of worker processes in total Horizon should scale up and down to: -->
`auto` 전략을 사용할 때는, 큐당 워커 최소/최대 수(`minProcesses`, `maxProcesses`)도 직접 지정할 수 있습니다. 이것은 각 큐에 할당될 워커의 최소 수와 호라이즌 전체 워커 수의 최대치로, 상황에 따라 워커 수를 자동으로 늘이거나 줄입니다.

```
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['default'],
            'balance' => 'auto',
            'autoScalingStrategy' => 'time',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
            'tries' => 3,
        ],
    ],
],
```

<!-- The `autoScalingStrategy` configuration value determines if Horizon will assign more worker processes to queues based on the total amount of time it will take to clear the queue (`time` strategy) or by the total number of jobs on the queue (`size` strategy). -->
`autoScalingStrategy` 옵션은 워커 프로세스를 얼마나 할당할지 판단할 때 전반적으로 큐를 비우는 데 걸릴 예상 시간(`time` 전략)이나 큐에 남아있는 작업 수(`size` 전략) 중 어떤 기준을 사용할지 결정합니다.

<!-- The `balanceMaxShift` and `balanceCooldown` configuration values determine how quickly Horizon will scale to meet worker demand. In the example above, a maximum of one new process will be created or destroyed every three seconds. You are free to tweak these values as necessary based on your application's needs. -->
`balanceMaxShift`와 `balanceCooldown` 옵션은 워커가 얼마나 빨리 늘어나거나 줄어들지 결정합니다. 예를 들어, 위 설정에서는 3초마다 최대 1개의 워커 프로세스만 추가되거나 제거됩니다. 애플리케이션에 맞게 이 값들을 자유롭게 조절하세요.

<!-- When the `balance` option is set to `false`, the default Laravel behavior will be used, wherein queues are processed in the order they are listed in your configuration. -->
`balance` 값을 `false`로 설정하면, Laravel 기본 동작대로 큐를 설정 파일에 나열된 순서로 처리합니다.

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Horizon dashboard may be accessed via the `/horizon` route. By default, you will only be able to access this dashboard in the `local` environment. However, within your `app/Providers/HorizonServiceProvider.php` file, there is an [authorization gate](/docs/11.x/authorization#gates) definition. This authorization gate controls access to Horizon in **non-local** environments. You are free to modify this gate as needed to restrict access to your Horizon installation: -->
호라이즌 대시보드는 `/horizon` 경로를 통해 접근할 수 있습니다. 기본적으로 `local` 환경일 때만 접근이 허용됩니다. 하지만 `app/Providers/HorizonServiceProvider.php` 파일에는 [authorization gate](/docs/11.x/authorization#gates)가 정의되어 있습니다. 이 게이트는 **local 이외 환경**에서 호라이즌 접근을 통제합니다. 필요에 맞게 게이트 코드를 수정하여 호라이즌 접근 권한을 제한할 수 있습니다.

```
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
Laravel은 위 게이트 클로저에 인증된 유저를 자동으로 주입합니다. 만약 호라이즌의 접근을 IP 제한 등 다른 방식으로 제어하고 있다면, 사용자가 "로그인"하지 않아도 되겠죠. 이럴 경우, 위 게이트 클로저의 시그니처를 `function (User $user)`에서 `function (User $user = null)`로 수정하여 인증이 없어도 접근이 가능하게 할 수 있습니다.

<a name="silenced-jobs"></a>
<!-- ### Silenced Jobs -->
### Silenced Jobs

<!-- Sometimes, you may not be interested in viewing certain jobs dispatched by your application or third-party packages. Instead of these jobs taking up space in your "Completed Jobs" list, you can silence them. To get started, add the job's class name to the `silenced` configuration option in your application's `horizon` configuration file: -->
애플리케이션이나 서드파티 패키지가 실행하는 일부 작업은 대시보드에서 굳이 눈여겨볼 필요가 없을 때가 있습니다. 이런 작업을 "무시"하면, "완료된 작업" 목록에 표시되지 않습니다. 무시하려는 작업의 클래스명을 `horizon` 설정 파일의 `silenced` 옵션에 추가하세요.

```
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

<!-- Alternatively, the job you wish to silence can implement the `Laravel\Horizon\Contracts\Silenced` interface. If a job implements this interface, it will automatically be silenced, even if it is not present in the `silenced` configuration array: -->
또는, 무시하고 싶은 작업에서 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하면, `silenced` 설정 배열에 추가하지 않아도 해당 작업이 자동으로 무시됩니다.

```
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="upgrading-horizon"></a>
<!-- ## Upgrading Horizon -->
## Upgrading Horizon

<!-- When upgrading to a new major version of Horizon, it's important that you carefully review [the upgrade guide](https://github.com/laravel/horizon/blob/master/UPGRADE.md). -->
호라이즌의 새 주요 버전으로 업그레이드할 경우, 반드시 [the upgrade guide](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 확인하시기 바랍니다.

<a name="running-horizon"></a>
<!-- ## Running Horizon -->
## Running Horizon

<!-- Once you have configured your supervisors and workers in your application's `config/horizon.php` configuration file, you may start Horizon using the `horizon` Artisan command. This single command will start all of the configured worker processes for the current environment: -->
애플리케이션의 `config/horizon.php` 파일에서 슈퍼바이저 및 워커 설정이 모두 완료되었다면, 아티즌의 `horizon` 명령어로 호라이즌을 실행할 수 있습니다. 이 단일 명령이면 현재 환경에 맞는 모든 워커 프로세스가 실행됩니다.

```shell
php artisan horizon
```

<!-- You may pause the Horizon process and instruct it to continue processing jobs using the `horizon:pause` and `horizon:continue` Artisan commands: -->
호라이즌 프로세스를 일시 중지하거나, 다시 작업 처리를 계속하려면 `horizon:pause`와 `horizon:continue` 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:pause

php artisan horizon:continue
```

<!-- You may also pause and continue specific Horizon [supervisors](#supervisors) using the `horizon:pause-supervisor` and `horizon:continue-supervisor` Artisan commands: -->
특정 호라이즌 [supervisors](#supervisors)만 일시 중지 또는 이어서 작업하게 하려면, `horizon:pause-supervisor` 및 `horizon:continue-supervisor` 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

<!-- You may check the current status of the Horizon process using the `horizon:status` Artisan command: -->
현재 호라이즌 프로세스의 상태는 `horizon:status` 명령어로 확인할 수 있습니다.

```shell
php artisan horizon:status
```

<!-- You may check the current status of a specific Horizon [supervisor](#supervisors) using the `horizon:supervisor-status` Artisan command: -->
특정 호라이즌 [supervisor](#supervisors)의 상태를 확인하려면 `horizon:supervisor-status` 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:supervisor-status supervisor-1
```

<!-- You may gracefully terminate the Horizon process using the `horizon:terminate` Artisan command. Any jobs that are currently being processed will be completed and then Horizon will stop executing: -->
호라이즌 프로세스를 정상적으로 종료하려면 `horizon:terminate` 명령어를 실행하세요. 이 경우, 현재 처리 중인 작업이 모두 완료된 후에 실행이 중단됩니다.

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
<!-- ### Deploying Horizon -->
### Deploying Horizon

<!-- When you're ready to deploy Horizon to your application's actual server, you should configure a process monitor to monitor the `php artisan horizon` command and restart it if it exits unexpectedly. Don't worry, we'll discuss how to install a process monitor below. -->
실제 서버에 호라이즌을 배포할 때는, `php artisan horizon` 명령어가 비정상적으로 종료되는 상황에 대비해 반드시 프로세스 모니터를 설정해야 합니다. 아래에서 프로세스 모니터 설치 방법을 다루니 참고하세요.

<!-- During your application's deployment process, you should instruct the Horizon process to terminate so that it will be restarted by your process monitor and receive your code changes: -->
애플리케이션을 배포할 때는, 호라이즌 프로세스를 먼저 종료하여 프로세스 모니터가 새로 재시작하고 변경된 코드를 적용받을 수 있도록 해야 합니다.

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
<!-- #### Installing Supervisor -->
#### Installing Supervisor

<!-- Supervisor is a process monitor for the Linux operating system and will automatically restart your `horizon` process if it stops executing. To install Supervisor on Ubuntu, you may use the following command. If you are not using Ubuntu, you can likely install Supervisor using your operating system's package manager: -->
Supervisor는 리눅스 운영체제에서 동작하는 프로세스 모니터 도구로, `horizon` 프로세스가 중단되면 자동으로 재시작해줍니다. 우분투 기준으로 Supervisor는 아래와 같이 설치할 수 있습니다. 우분투가 아닌 경우에도 운영체제의 패키지 관리자를 이용해 쉽게 설치할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> 직접 Supervisor를 설정하는 것이 부담스럽다면, [Laravel Forge](https://forge.laravel.com) 서비스를 이용하는 것도 좋은 방법입니다. Forge에서는 Laravel 프로젝트에 맞는 Supervisor를 자동으로 설치·설정해 줍니다.

<a name="supervisor-configuration"></a>
<!-- #### Supervisor Configuration -->
#### Supervisor Configuration

<!-- Supervisor configuration files are typically stored within your server's `/etc/supervisor/conf.d` directory. Within this directory, you may create any number of configuration files that instruct supervisor how your processes should be monitored. For example, let's create a `horizon.conf` file that starts and monitors a `horizon` process: -->
Supervisor 설정 파일은 일반적으로 서버의 `/etc/supervisor/conf.d` 디렉터리에 보관됩니다. 이 디렉터리 내에서 여러 설정 파일을 생성해 프로세스 감시 방법을 지정할 수 있습니다. 예를 들어, `horizon.conf` 파일을 만들어 `horizon` 프로세스를 시작·감시하도록 할 수 있습니다.

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
Supervisor 설정 시, `stopwaitsecs` 값이 가장 오래 걸리는 작업의 실행 시간보다 충분히 더 커야만 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 강제로 종료시킬 수 있습니다.

> [!WARNING]
> 위 예시는 우분투 계열 서버에 적합하며, 운영체제에 따라 Supervisor 설정 파일의 위치와 확장자가 다를 수 있습니다. 여러분의 서버 환경에 맞는 공식 문서를 반드시 참고해 주세요.

<a name="starting-supervisor"></a>
<!-- #### Starting Supervisor -->
#### Starting Supervisor

<!-- Once the configuration file has been created, you may update the Supervisor configuration and start the monitored processes using the following commands: -->
설정 파일을 만들었으면, 다음 명령어들로 Supervisor 설정을 갱신하고 감시 프로세스를 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor에 대한 더 자세한 내용은 [Supervisor documentation](http://supervisord.org/index.html)를 참고해 주세요.

<a name="tags"></a>
<!-- ## Tags -->
## Tags

<!-- Horizon allows you to assign “tags” to jobs, including mailables, broadcast events, notifications, and queued event listeners. In fact, Horizon will intelligently and automatically tag most jobs depending on the Eloquent models that are attached to the job. For example, take a look at the following job: -->
호라이즌은 작업, 메일러블, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등 다양한 종류의 작업에 "태그"를 붙일 수 있습니다. 실제로, 대부분의 작업에 대해 호라이즌이 Eloquent 모델을 참조하여 자동으로 적절한 태그를 붙입니다. 예를 들어, 아래와 같은 작업 클래스를 보겠습니다.

```
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
이 작업이 `id`가 `1`인 `App\Models\Video` 인스턴스와 함께 큐에 등록되면, 호라이즌은 자동으로 `App\Models\Video:1`이라는 태그를 붙입니다. 이는 호라이즌이 작업 속성에서 Eloquent 모델을 찾아, 모델의 클래스명과 기본 키(Primary Key)를 조합하여 태그로 생성하기 때문입니다.

```
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
<!-- #### Manually Tagging Jobs -->
#### Manually Tagging Jobs

<!-- If you would like to manually define the tags for one of your queueable objects, you may define a `tags` method on the class: -->
특정 큐 작업에 직접 태그를 지정하고 싶다면, 해당 클래스에 `tags` 메서드를 정의하면 됩니다.

```
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
큐에 등록된 이벤트 리스너의 태그를 정의할 때, 호라이즌은 이벤트 인스턴스를 `tags` 메서드로 자동 전달합니다. 이를 이용해 이벤트의 속성 값으로 태그를 만들 수 있습니다.

```
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
> 호라이즌에서 Slack 또는 SMS 알림을 설정할 경우, [prerequisites for the relevant notification channel](/docs/11.x/notifications)을 반드시 확인하세요.

<!-- If you would like to be notified when one of your queues has a long wait time, you may use the `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, and `Horizon::routeSmsNotificationsTo` methods. You may call these methods from the `boot` method of your application's `App\Providers\HorizonServiceProvider`: -->
특정 큐의 대기 시간이 길어질 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하면 됩니다.

```
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
어느 정도의 대기 시간이 "긴 대기"에 해당하는지, `config/horizon.php` 설정 파일의 `waits` 옵션에서 큐별로 지정할 수 있습니다. 여기에 정의되지 않은 연결/큐 조합은 기본적으로 60초가 임계값으로 적용됩니다.

```
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

<a name="metrics"></a>
<!-- ## Metrics -->
## Metrics

<!-- Horizon includes a metrics dashboard which provides information regarding your job and queue wait times and throughput. In order to populate this dashboard, you should configure Horizon's `snapshot` Artisan command to run every five minutes in your application's `routes/console.php` file: -->
호라이즌에는 작업의 대기 시간 및 처리량 관련 정보를 보여주는 메트릭 대시보드가 포함되어 있습니다. 이 대시보드를 채우려면, 애플리케이션의 `routes/console.php` 파일에서 `snapshot` 아티즌 명령을 5분마다 주기적으로 실행되도록 예약해야 합니다.

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

<a name="deleting-failed-jobs"></a>
<!-- ## Deleting Failed Jobs -->
## Deleting Failed Jobs

<!-- If you would like to delete a failed job, you may use the `horizon:forget` command. The `horizon:forget` command accepts the ID or UUID of the failed job as its only argument: -->
실패한 작업을 삭제하려면 `horizon:forget` 명령어를 사용할 수 있습니다. `horizon:forget` 명령어는 삭제하려는 실패한 작업의 ID 또는 UUID를 인수로 받습니다.

```shell
php artisan horizon:forget 5
```

<!-- If you would like to delete all failed jobs, you may provide the `--all` option to the `horizon:forget` command: -->
모든 실패한 작업을 삭제하려면 `horizon:forget` 명령어에 `--all` 옵션을 사용할 수 있습니다.

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
<!-- ## Clearing Jobs From Queues -->
## Clearing Jobs From Queues

<!-- If you would like to delete all jobs from your application's default queue, you may do so using the `horizon:clear` Artisan command: -->
애플리케이션의 기본 큐에서 모든 작업을 삭제하고 싶다면, `horizon:clear` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:clear
```

<!-- You may provide the `queue` option to delete jobs from a specific queue: -->
특정 큐의 작업만 삭제하려면 `queue` 옵션을 지정하세요.

```shell
php artisan horizon:clear --queue=emails
```
