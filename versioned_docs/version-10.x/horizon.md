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
> Laravel Horizon을 본격적으로 사용하기 전에, Laravel의 기본 [queue services](/docs/10.x/queues)에 대해 먼저 이해하시기 바랍니다. Horizon은 Laravel 큐에 추가적인 기능을 제공하므로, Laravel이 제공하는 기본 큐 기능에 익숙하지 않다면 다소 혼란스러울 수 있습니다.

<!-- [Laravel Horizon](https://github.com/laravel/horizon) provides a beautiful dashboard and code-driven configuration for your Laravel powered [Redis queues](/docs/10.x/queues). Horizon allows you to easily monitor key metrics of your queue system such as job throughput, runtime, and job failures. -->
[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis queues](/docs/10.x/queues)를 위한 아름다운 대시보드와 코드 기반 설정을 제공합니다. Horizon을 활용하면 큐 시스템의 핵심 메트릭, 예를 들어 작업 처리량, 실행 시간, 작업 실패 건수 등을 손쉽게 모니터링할 수 있습니다.

<!-- When using Horizon, all of your queue worker configuration is stored in a single, simple configuration file. By defining your application's worker configuration in a version controlled file, you may easily scale or modify your application's queue workers when deploying your application. -->
Horizon을 사용할 때, 모든 큐 워커 설정은 하나의 간단한 설정 파일에 저장됩니다. 애플리케이션의 워커 구성을 버전 관리가 되는 파일에 정의하면, 배포 시 대규모로 확장하거나 구성을 쉽게 수정할 수 있습니다.

<!-- <img src="https://laravel.com/img/docs/horizon-example.png"/> -->
<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
<!-- ## Installation -->
## Installation

> [!WARNING]
> Laravel Horizon은 [Redis](https://redis.io)를 큐 엔진으로 반드시 사용해야 합니다. 따라서, 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 반드시 `redis`로 지정되어 있는지 확인해야 합니다.

<!-- You may install Horizon into your project using the Composer package manager: -->
Composer 패키지 매니저를 사용하여 프로젝트에 Horizon을 설치할 수 있습니다.

```shell
composer require laravel/horizon
```

<!-- After installing Horizon, publish its assets using the `horizon:install` Artisan command: -->
Horizon을 설치한 후에는, `horizon:install` 아티즌 명령어로 관련 에셋을 배포합니다.

```shell
php artisan horizon:install
```

<a name="configuration"></a>
<!-- ### Configuration -->
### Configuration

<!-- After publishing Horizon's assets, its primary configuration file will be located at `config/horizon.php`. This configuration file allows you to configure the queue worker options for your application. Each configuration option includes a description of its purpose, so be sure to thoroughly explore this file. -->
Horizon 에셋을 배포하면, 기본 설정 파일이 `config/horizon.php`에 위치하게 됩니다. 이 설정 파일에서 애플리케이션의 큐 워커 옵션을 구성할 수 있습니다. 각 옵션에는 용도에 대한 설명이 포함되어 있으니, 반드시 이 파일을 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 Redis 연결명을 사용합니다. 이 이름은 예약되어 있으므로, `database.php` 설정 파일이나 `horizon.php` 설정 파일의 `use` 옵션 값으로 다른 연결에 할당해서는 안 됩니다.

<a name="environments"></a>
<!-- #### Environments -->
#### Environments

<!-- After installation, the primary Horizon configuration option that you should familiarize yourself with is the `environments` configuration option. This configuration option is an array of environments that your application runs on and defines the worker process options for each environment. By default, this entry contains a `production` and `local` environment. However, you are free to add more environments as needed: -->
설치를 마친 후 가장 먼저 익숙해져야 하는 Horizon 설정 옵션은 `environments`입니다. 이 옵션은 애플리케이션이 실행되는 환경 목록과, 각 환경별 워커 프로세스 옵션을 배열로 정의합니다. 기본적으로 `production`과 `local` 환경이 포함되어 있지만, 필요에 따라 추가 환경을 자유롭게 지정할 수 있습니다.

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

<!-- When you start Horizon, it will use the worker process configuration options for the environment that your application is running on. Typically, the environment is determined by the value of the `APP_ENV` [environment variable](/docs/10.x/configuration#determining-the-current-environment). For example, the default `local` Horizon environment is configured to start three worker processes and automatically balance the number of worker processes assigned to each queue. The default `production` environment is configured to start a maximum of 10 worker processes and automatically balance the number of worker processes assigned to each queue. -->
Horizon을 실행하면, 현재 애플리케이션이 실행 중인 환경에 맞는 워커 프로세스 구성을 자동으로 사용합니다. 환경은 보통 `APP_ENV` [environment variable](/docs/10.x/configuration#determining-the-current-environment)의 값으로 결정됩니다. 예를 들어, 기본적으로 `local` 환경은 3개의 워커 프로세스를 실행하고, 각 큐에 할당된 워커 프로세스 수를 자동으로 조절합니다. `production` 환경의 경우, 최대 10개의 워커 프로세스를 실행하며, 이 역시 큐의 상황에 따라 자동으로 프로세스를 배분하도록 설정되어 있습니다.

> [!WARNING]
> Horizon을 실행할 계획인 각 [environment](/docs/10.x/configuration#environment-configuration)에 대해, 반드시 `horizon` 설정 파일의 `environments` 섹션에 해당 항목이 포함되어 있어야 합니다.

<a name="supervisors"></a>
<!-- #### Supervisors -->
#### Supervisors

<!-- As you can see in Horizon's default configuration file, each environment can contain one or more "supervisors". By default, the configuration file defines this supervisor as `supervisor-1`; however, you are free to name your supervisors whatever you want. Each supervisor is essentially responsible for "supervising" a group of worker processes and takes care of balancing worker processes across queues. -->
Horizon의 기본 설정 파일에서 볼 수 있듯, 각 환경에는 하나 이상의 "supervisor"를 포함할 수 있습니다. 기본적으로 이 supervisor의 이름은 `supervisor-1`로 지정되어 있지만, 원하는 대로 자유롭게 이름을 정할 수 있습니다. 각 supervisor는 여러 워커 프로세스로 구성된 집합을 "감독"하며, 큐 간 워커 프로세스의 균형을 자동으로 관리합니다.

<!-- You may add additional supervisors to a given environment if you would like to define a new group of worker processes that should run in that environment. You may choose to do this if you would like to define a different balancing strategy or worker process count for a given queue used by your application. -->
특정 환경에서 별도의 워커 프로세스 그룹을 운영하고 싶다면 supervisor를 추가할 수 있습니다. 예를 들어, 애플리케이션에서 사용하는 특정 큐에 대해 서로 다른 밸런싱 전략이나 워커 프로세스 수를 각각 부여하고 싶을 때 활용할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- #### Maintenance Mode -->
#### Maintenance Mode

<!-- While your application is in [maintainance mode](/docs/10.x/configuration#maintenance-mode), queued jobs will not be processed by Horizon unless the supervisor's `force` option is defined as `true` within the Horizon configuration file: -->
애플리케이션이 [maintainance mode](/docs/10.x/configuration#maintenance-mode)일 때에는, supervisor의 `force` 옵션이 Horizon 설정 파일에서 `true`로 명시되지 않았다면 Horizon이 큐 작업을 처리하지 않습니다.

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
Horizon 기본 설정 파일에는 `defaults` 옵션이 있습니다. 이 옵션은 [supervisors](#supervisors)들의 기본값을 지정합니다. supervisor의 설정값은 각 환경의 supervisor 설정에 병합되어, supervisor를 정의할 때 중복 설정을 피할 수 있습니다.

<a name="balancing-strategies"></a>
<!-- ### Balancing Strategies -->
### Balancing Strategies

<!-- Unlike Laravel's default queue system, Horizon allows you to choose from three worker balancing strategies: `simple`, `auto`, and `false`. The `simple` strategy splits incoming jobs evenly between worker processes: -->
Laravel의 기본 큐 시스템과 달리, Horizon에서는 세 가지 워커 밸런싱 전략 중에서 선택할 수 있습니다: `simple`, `auto`, `false`. `simple` 전략은 들어오는 작업을 워커 프로세스에 균등하게 분배합니다.

```
'balance' => 'simple',
```

<!-- The `auto` strategy, which is the configuration file's default, adjusts the number of worker processes per queue based on the current workload of the queue. For example, if your `notifications` queue has 1,000 pending jobs while your `render` queue is empty, Horizon will allocate more workers to your `notifications` queue until the queue is empty. -->
`auto` 전략은 설정 파일의 기본값으로, 각 큐의 현재 작업량에 따라 워커 프로세스 수를 자동으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고 `render` 큐는 비어 있다면, Horizon은 `notifications` 큐에 더 많은 워커를 배정하여 해당 큐가 비워질 때까지 처리하게 됩니다.

<!-- When using the `auto` strategy, you may define the `minProcesses` and `maxProcesses` configuration options to control the minimum and the maximum number of worker processes Horizon should scale up and down to: -->
`auto` 전략을 사용할 때는 `minProcesses`와 `maxProcesses` 옵션으로 Horizon이 확장/축소할 워커 프로세스의 최소/최대 값을 정의할 수 있습니다.

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
`autoScalingStrategy` 옵션은 Horizon이 큐를 얼마나 빨리 처리할지 결정할 때, 큐를 비우는 데 걸리는 총 시간( `time` 전략 )을 기준으로 할지, 아니면 큐에 쌓인 작업의 총 개수( `size` 전략 )를 기준으로 할지 결정합니다.

<!-- The `balanceMaxShift` and `balanceCooldown` configuration values determine how quickly Horizon will scale to meet worker demand. In the example above, a maximum of one new process will be created or destroyed every three seconds. You are free to tweak these values as necessary based on your application's needs. -->
`balanceMaxShift`와 `balanceCooldown` 설정은 Horizon이 워커 수를 얼마나 빠르게 조정할지를 정의합니다. 위 예시에서는 3초마다 최대 1개의 신규 프로세스가 생성되거나 종료됩니다. 이 값들은 애플리케이션의 필요에 맞게 조정할 수 있습니다.

<!-- When the `balance` option is set to `false`, the default Laravel behavior will be used, wherein queues are processed in the order they are listed in your configuration. -->
`balance` 옵션이 `false`로 설정된 경우에는 기본 Laravel 방식이 적용되어, 설정된 큐 순서대로 작업을 처리합니다.

<a name="dashboard-authorization"></a>
<!-- ### Dashboard Authorization -->
### Dashboard Authorization

<!-- The Horizon dashboard may be accessed via the `/horizon` route. By default, you will only be able to access this dashboard in the `local` environment. However, within your `app/Providers/HorizonServiceProvider.php` file, there is an [authorization gate](/docs/10.x/authorization#gates) definition. This authorization gate controls access to Horizon in **non-local** environments. You are free to modify this gate as needed to restrict access to your Horizon installation: -->
Horizon 대시보드는 `/horizon` 경로를 통해 접속할 수 있습니다. 기본적으로 `local` 환경에서만 이 대시보드에 접근할 수 있습니다. 하지만, `app/Providers/HorizonServiceProvider.php` 파일에는 [authorization gate](/docs/10.x/authorization#gates)가 정의되어 있습니다. 이 게이트는 **로컬 환경이 아닌** 경우 Horizon의 접근 권한을 제어합니다. 필요에 맞게 이 게이트를 수정하여 Horizon 대시보드 접근을 제한할 수 있습니다.

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
Laravel은 게이트 클로저 내부에 현재 인증된 사용자를 자동으로 주입합니다. 만약 Horizon의 보안을 IP 제한 등 다른 방식으로 제공한다면, Horizon 사용자가 “로그인”할 필요가 없을 수도 있습니다. 이 경우 위의 `function (User $user)` 시그니처를 `function (User $user = null)`로 변경하여 Laravel이 인증을 강제하지 않도록 처리해야 합니다.

<a name="silenced-jobs"></a>
<!-- ### Silenced Jobs -->
### Silenced Jobs

<!-- Sometimes, you may not be interested in viewing certain jobs dispatched by your application or third-party packages. Instead of these jobs taking up space in your "Completed Jobs" list, you can silence them. To get started, add the job's class name to the `silenced` configuration option in your application's `horizon` configuration file: -->
애플리케이션이나 외부 패키지에서 디스패치하는 특정 작업에 대해서는, 완료된 작업 목록에서 굳이 보이지 않아도 되는 경우가 있습니다. 이럴 때 작업이 "Completed Jobs" 목록에서 공간을 차지하지 않도록 숨김 처리할 수 있습니다. 우선, 숨기고 싶은 작업의 클래스명을 애플리케이션의 `horizon` 설정 파일 내 `silenced` 옵션에 추가하십시오.

```
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

<!-- Alternatively, the job you wish to silence can implement the `Laravel\Horizon\Contracts\Silenced` interface. If a job implements this interface, it will automatically be silenced, even if it is not present in the `silenced` configuration array: -->
또는, 해당 작업 클래스에서 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현할 수도 있습니다. 이 인터페이스를 구현하면, 위의 `silenced` 배열에 추가하지 않아도 자동으로 작업이 숨김 처리됩니다.

```
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    // ...
}
```

<a name="upgrading-horizon"></a>
<!-- ## Upgrading Horizon -->
## Upgrading Horizon

<!-- When upgrading to a new major version of Horizon, it's important that you carefully review [the upgrade guide](https://github.com/laravel/horizon/blob/master/UPGRADE.md). In addition, when upgrading to any new Horizon version, you should re-publish Horizon's assets: -->
Horizon을 새로운 주요 버전으로 업그레이드할 때에는 반드시 [the upgrade guide](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 세심하게 검토해야 합니다. 그리고 Horizon의 모든 새로운 버전으로 업그레이드할 때에는 에셋도 반드시 다시 배포해야 합니다.

```shell
php artisan horizon:publish
```

<!-- To keep the assets up-to-date and avoid issues in future updates, you may add the `vendor:publish --tag=laravel-assets` command to the `post-update-cmd` scripts in your application's `composer.json` file: -->
에셋을 항상 최신 상태로 유지하고, 추후 업데이트시 문제가 생기지 않도록, `composer.json` 파일의 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령어를 추가하는 것도 좋은 방법입니다.

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}
```

<a name="running-horizon"></a>
<!-- ## Running Horizon -->
## Running Horizon

<!-- Once you have configured your supervisors and workers in your application's `config/horizon.php` configuration file, you may start Horizon using the `horizon` Artisan command. This single command will start all of the configured worker processes for the current environment: -->
애플리케이션의 `config/horizon.php` 파일에서 supervisor와 worker 구성을 완료했다면, `horizon` 아티즌 명령어로 Horizon을 시작할 수 있습니다. 이 한 번의 명령으로 현재 환경에 맞게 모든 워커 프로세스가 실행됩니다.

```shell
php artisan horizon
```

<!-- You may pause the Horizon process and instruct it to continue processing jobs using the `horizon:pause` and `horizon:continue` Artisan commands: -->
Horizon 프로세스를 일시 중지하고 다시 작업 처리를 재개하려면 `horizon:pause` 및 `horizon:continue` 아티즌 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:pause

php artisan horizon:continue
```

<!-- You may also pause and continue specific Horizon [supervisors](#supervisors) using the `horizon:pause-supervisor` and `horizon:continue-supervisor` Artisan commands: -->
특정 Horizon [supervisors](#supervisors)를 개별적으로 일시 중지하거나 재개하려면, `horizon:pause-supervisor` 및 `horizon:continue-supervisor` 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

<!-- You may check the current status of the Horizon process using the `horizon:status` Artisan command: -->
현재 Horizon 프로세스의 상태는 `horizon:status` 아티즌 명령어로 확인할 수 있습니다.

```shell
php artisan horizon:status
```

<!-- You may gracefully terminate the Horizon process using the `horizon:terminate` Artisan command. Any jobs that are currently being processed by will be completed and then Horizon will stop executing: -->
Horizon 프로세스를 우아하게 종료하려면 `horizon:terminate` 명령어를 사용합니다. 이 명령을 실행하면, 현재 처리 중인 작업만 완료한 뒤 Horizon이 더 이상 실행을 멈춥니다.

```shell
php artisan horizon:terminate
```

<a name="deploying-horizon"></a>
<!-- ### Deploying Horizon -->
### Deploying Horizon

<!-- When you're ready to deploy Horizon to your application's actual server, you should configure a process monitor to monitor the `php artisan horizon` command and restart it if it exits unexpectedly. Don't worry, we'll discuss how to install a process monitor below. -->
Horizon을 실제 서버에 배포할 준비가 되었다면, 반드시 프로세스 모니터를 설정하여 `php artisan horizon` 명령이 비정상적으로 종료되었을 때 자동으로 재시작되도록 해야 합니다. 걱정하지 마세요, 아래에서 프로세스 모니터 설치 방법을 안내합니다.

<!-- During your application's deployment process, you should instruct the Horizon process to terminate so that it will be restarted by your process monitor and receive your code changes: -->
애플리케이션을 배포하는 과정에서는 Horizon 프로세스를 종료한 뒤, 프로세스 모니터가 자동으로 재시작하게 하여 코드 변경사항을 반영할 수 있도록 해야 합니다.

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
<!-- #### Installing Supervisor -->
#### Installing Supervisor

<!-- Supervisor is a process monitor for the Linux operating system and will automatically restart your `horizon` process if it stops executing. To install Supervisor on Ubuntu, you may use the following command. If you are not using Ubuntu, you can likely install Supervisor using your operating system's package manager: -->
Supervisor는 리눅스 운영체제에서 실행되는 프로세스 모니터로, 실행 중인 `horizon` 프로세스가 중지되면 자동으로 재시작해줍니다. Ubuntu 환경에서는 다음 명령어로 Supervisor를 설치할 수 있습니다. Ubuntu가 아니라면 운영체제 패키지 매니저를 사용하여 Supervisor를 설치할 수 있습니다.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 설정이 번거롭게 느껴진다면, Laravel 프로젝트에 대해 Supervisor 설치와 설정을 자동으로 처리해주는 [Laravel Forge](https://forge.laravel.com) 서비스를 고려해보세요.

<a name="supervisor-configuration"></a>
<!-- #### Supervisor Configuration -->
#### Supervisor Configuration

<!-- Supervisor configuration files are typically stored within your server's `/etc/supervisor/conf.d` directory. Within this directory, you may create any number of configuration files that instruct supervisor how your processes should be monitored. For example, let's create a `horizon.conf` file that starts and monitors a `horizon` process: -->
Supervisor 설정 파일은 일반적으로 서버의 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이 디렉터리 내에서, 모니터링할 프로세스에 대한 설정 파일을 원하는 만큼 만들 수 있습니다. 예를 들어, `horizon.conf` 파일을 만들어 `horizon` 프로세스를 시작 및 모니터링할 수 있습니다.

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
Supervisor 설정에서 `stopwaitsecs` 값이 가장 오래 걸리는 작업의 실행 시간(초)보다 커야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기도 전에 강제로 종료할 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 기반 서버에서 유효하며, Supervisor 설정 파일의 위치나 확장자는 운영체제마다 다를 수 있습니다. 자세한 내용은 서버 관련 공식 문서를 참고하세요.

<a name="starting-supervisor"></a>
<!-- #### Starting Supervisor -->
#### Starting Supervisor

<!-- Once the configuration file has been created, you may update the Supervisor configuration and start the monitored processes using the following commands: -->
설정 파일을 만들었다면, 아래 명령어로 Supervisor 설정을 갱신하고, 모니터링을 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 실행에 대한 더 자세한 내용은 [Supervisor documentation](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
<!-- ## Tags -->
## Tags

<!-- Horizon allows you to assign “tags” to jobs, including mailables, broadcast events, notifications, and queued event listeners. In fact, Horizon will intelligently and automatically tag most jobs depending on the Eloquent models that are attached to the job. For example, take a look at the following job: -->
Horizon에서는 작업(Job), 메일 발송, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등 다양한 작업에 “태그”를 부여할 수 있습니다. 실제로 Horizon은 작업에 연결되어 있는 Eloquent 모델을 분석하여, 대부분의 작업에 지능적으로 태그를 자동 부여합니다. 예를 들어, 아래 작업 코드를 보세요.

```
<?php

namespace App\Jobs;

use App\Models\Video;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class RenderVideo implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

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
이 작업이 `id` 속성이 `1`인 `App\Models\Video` 인스턴스와 함께 큐에 등록되면, 자동으로 태그 `App\Models\Video:1`이 부여됩니다. 이는 Horizon이 작업의 속성(property)에서 모든 Eloquent 모델을 찾아내고, 모델의 클래스명과 기본 키(primary key)를 조합하여 태그를 생성하기 때문입니다.

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
큐에 등록되는 객체에 대해 직접 태그를 지정하고 싶다면, 클래스에 `tags` 메서드를 정의하면 됩니다.

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
큐잉되는 이벤트 리스너의 태그를 가져올 때, Horizon은 자동으로 이벤트 인스턴스를 `tags` 메서드에 전달합니다. 이를 활용하면 이벤트 데이터를 기반으로 태그를 만들 수 있습니다.

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
> Horizon에서 Slack 또는 SMS 알림을 설정할 때는, 반드시 [prerequisites for the relevant notification channel](/docs/10.x/notifications)을 확인해야 합니다.

<!-- If you would like to be notified when one of your queues has a long wait time, you may use the `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, and `Horizon::routeSmsNotificationsTo` methods. You may call these methods from the `boot` method of your application's `App\Providers\HorizonServiceProvider`: -->
큐에 대기 중인 작업의 대기 시간이 오래 걸릴 경우 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드는 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하면 됩니다.

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
얼마나 긴 대기 시간을 “오래된 대기”로 간주할지, 애플리케이션의 `config/horizon.php` 파일에서 `waits` 옵션으로 지정할 수 있습니다. 각 커넥션/큐 조합별 임곗값을 초 단위로 제어할 수 있습니다. 설정되지 않은 조합은 기본적으로 60초가 적용됩니다.

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

<!-- Horizon includes a metrics dashboard which provides information regarding your job and queue wait times and throughput. In order to populate this dashboard, you should configure Horizon's `snapshot` Artisan command to run every five minutes via your application's [scheduler](/docs/10.x/scheduling): -->
Horizon에는 작업별 및 큐별 대기 시간과 처리량 정보를 제공하는 메트릭 대시보드가 포함되어 있습니다. 이 대시보드에 데이터가 수집되도록 하려면, [scheduler](/docs/10.x/scheduling)를 통해 5분마다 Horizon의 `snapshot` 아티즌 명령을 실행하도록 등록해야 합니다.

```
/**
 * Define the application's command schedule.
 */
protected function schedule(Schedule $schedule): void
{
    $schedule->command('horizon:snapshot')->everyFiveMinutes();
}
```

<a name="deleting-failed-jobs"></a>
<!-- ## Deleting Failed Jobs -->
## Deleting Failed Jobs

<!-- If you would like to delete a failed job, you may use the `horizon:forget` command. The `horizon:forget` command accepts the ID or UUID of the failed job as its only argument: -->
실패한 작업을 삭제하고 싶을 때는 `horizon:forget` 명령어를 사용할 수 있습니다. `horizon:forget` 명령은 삭제할 실패 작업의 ID 또는 UUID 값을 인자로 받습니다.

```shell
php artisan horizon:forget 5
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
특정 큐의 작업만 삭제하고 싶다면, `queue` 옵션을 함께 사용할 수 있습니다.

```shell
php artisan horizon:clear --queue=emails
```