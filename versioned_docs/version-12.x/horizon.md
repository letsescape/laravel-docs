# Laravel Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [대시보드 인가](#dashboard-authorization)
    - [최대 작업 시도 횟수](#max-job-attempts)
    - [작업 타임아웃](#job-timeout)
    - [작업 백오프](#job-backoff)
    - [음소거된 작업](#silenced-jobs)
- [부하 분산 전략](#balancing-strategies)
    - [자동 부하 분산](#auto-balancing)
    - [단순 부하 분산](#simple-balancing)
    - [부하 분산 미사용](#no-balancing)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 삭제](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개

> [!NOTE]
> Laravel Horizon을 본격적으로 다루기 전에, 반드시 Laravel의 기본 [큐 서비스](/docs/12.x/queues)에 익숙해지는 것이 좋습니다. Horizon은 Laravel 큐 기능 위에 추가적인 기능을 더해주므로, 기본 큐 기능에 미숙한 경우 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Redis 기반의 Laravel [큐](/docs/12.x/queues)를 위한 아름다운 대시보드와 코드 기반의 설정을 제공합니다. Horizon을 통해 큐 시스템의 주요 지표(작업 처리량, 실행 시간, 작업 실패 등)를 손쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 워커 설정이 하나의 단순한 설정 파일에 저장됩니다. 애플리케이션의 워커 구성을 버전 관리되는 파일에 정의함으로써, 배포 시 손쉽게 큐 워커의 스케일 조정이나 설정 변경이 가능합니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치

> [!WARNING]
> Laravel Horizon을 사용하기 위해서는 큐가 반드시 [Redis](https://redis.io) 기반이어야 합니다. 따라서, 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결이 `redis`로 지정되어 있는지 반드시 확인해야 합니다. 현재 Horizon은 Redis Cluster와 호환되지 않습니다.

Composer 패키지 매니저를 사용하여 Horizon을 프로젝트에 설치할 수 있습니다.

```shell
composer require laravel/horizon
```

설치 후에는 `horizon:install` Artisan 명령어로 Horizon의 에셋을 퍼블리시합니다.

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

에셋을 퍼블리시한 후, Horizon의 주요 설정 파일은 `config/horizon.php`에 생성됩니다. 이 파일에서는 애플리케이션의 큐 워커 옵션을 세부적으로 설정할 수 있습니다. 각 설정에는 목적에 대한 설명이 달려 있으니, 이 파일을 꼼꼼히 살펴보는 것이 좋습니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 Redis 연결명을 사용합니다. 이 연결명은 예약된 것이므로, `database.php`의 다른 Redis 연결이나 `horizon.php`의 `use` 옵션에 이 이름을 사용해서는 안 됩니다.

<a name="environments"></a>
#### 환경 설정

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

Horizon을 시작하면, 현재 애플리케이션이 동작하는 환경에 맞는 워커 프로세스 설정이 적용됩니다. 일반적으로 환경은 `APP_ENV` [환경 변수](/docs/12.x/configuration#determining-the-current-environment)의 값에 따라 결정됩니다. 예를 들어, 기본 `local` 환경에서는 워커 프로세스 3개를 시작하고, 각 큐별로 워커가 자동으로 분배(balancing)됩니다. 기본 `production` 환경에서는 최대 10개의 워커 프로세스를 시작하며 마찬가지로 자동 분산이 이루어집니다.

> [!WARNING]
> Horizon을 실행할 각 [환경](/docs/12.x/configuration#environment-configuration)에 대해 `horizon` 설정 파일의 `environments` 항목에 반드시 엔트리를 정의해야 합니다.

<a name="supervisors"></a>
#### Supervisor(감독자)

Horizon의 기본 설정 파일을 살펴보면, 각 환경에는 하나 이상의 "supervisor(감독자)"를 포함할 수 있습니다. 기본적으로 `supervisor-1`이라는 이름이 설정되어 있지만, 원하는 대로 이름을 지정할 수 있습니다. 각 supervisor는 하나의 워커 프로세스 그룹을 "감독하고", 큐 간 워커 프로세스의 적절한 분배를 관리합니다.

특정 환경 내에서 추가 supervisor를 정의하면, 새로운 워커 프로세스 그룹을 생성하여 각기 다른 큐에 서로 다른 분산 전략이나 워커 수를 적용할 수 있습니다.

<a name="maintenance-mode"></a>
#### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/12.x/configuration#maintenance-mode)일 때, supervisor의 `force` 옵션이 Horizon 설정 파일에 `true`로 지정되어 있지 않다면 큐 대기 작업이 처리되지 않습니다.

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
#### 기본값

Horizon의 기본 설정 파일에는 `defaults`라는 옵션이 있습니다. 이 옵션은 [supervisor](#supervisors)에 대한 기본값을 지정합니다. supervisor의 기본값은 각 환경의 supervisor 설정에 병합되어, 중복 구성을 줄이고 관리가 편리해집니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가

Horizon 대시보드는 `/horizon` 경로를 통해 접근 가능합니다. 기본적으로는 `local` 환경에서만 이 대시보드를 사용할 수 있습니다. 그러나 `app/Providers/HorizonServiceProvider.php` 파일에는 [인가 게이트(gate)](/docs/12.x/authorization#gates)가 정의되어 있습니다. 이 게이트는 **로컬 환경 이외**에서 Horizon 접근을 제어합니다. 필요하다면 아래처럼 적절히 제한을 수정할 수 있습니다.

```php
/**
 * Horizon 게이트 등록.
 *
 * 이 게이트는 비로컬 환경에서 Horizon 접근 권한을 결정합니다.
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
#### 대체 인증 전략

Laravel은 게이트 클로저에 인증된 사용자를 자동으로 주입합니다. 만약 IP 제한 등 다른 방식으로 Horizon 보안을 설정 중이라면, 사용자가 굳이 "로그인"할 필요가 없을 수 있습니다. 이런 경우 위 클로저의 시그니처를 `function (User $user = null)`로 변경하여 인증 요구를 없앨 수 있습니다.

<a name="max-job-attempts"></a>
### 최대 작업 시도 횟수

> [!NOTE]
> 아래 옵션을 세부적으로 조정하기에 앞서, 먼저 Laravel의 기본 [큐 서비스](/docs/12.x/queues#max-job-attempts-and-timeout)와 '시도(attempts)' 개념에 익숙해지는 것이 좋습니다.

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
> 이 옵션은 Artisan 명령어로 큐를 처리할 때의 `--tries` 옵션과 유사합니다.

`WithoutOverlapping`, `RateLimited`과 같은 미들웨어를 사용할 경우, 미들웨어도 시도 횟수를 소비합니다. 따라서 supervisor 단위의 `tries` 값을 설정하거나, 작업 클래스에 `$tries` 속성을 정의하여 적절히 조정해야 합니다.

`tries` 옵션을 명시하지 않으면 Horizon 기본값은 한 번만 실행하며, 작업 클래스에 `$tries` 속성이 있으면 Horizon 설정보다 우선됩니다.

`tries`나 `$tries`를 0으로 설정하면 무한정 시도가 가능합니다. 시도 횟수에 제한이 불분명할 때 유용합니다. 단, 무한 반복 실패를 막으려면 작업 클래스에 `$maxExceptions` 속성을 설정하여 예외 허용 횟수를 제한할 수 있습니다.

<a name="job-timeout"></a>
### 작업 타임아웃

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
> `auto` 분산 전략을 사용할 때, Horizon은 스케일 다운 과정에서 프로세스 타임아웃만큼 진행 중인 워커가 "멈춤" 상태로 간주하게 됩니다. 작업 레벨의 타임아웃보다 Horizon의 타임아웃 값이 무조건 더 커야 하며, 그렇지 않으면 작업이 실행 도중 강제로 종료될 수 있습니다. 또, 이 값은 반드시 `config/queue.php`의 `retry_after` 값보다 몇 초 더 짧게 설정해야 합니다. 그렇지 않으면, 동일 작업이 중복 처리될 수 있습니다.

<a name="job-backoff"></a>
### 작업 백오프(재시도 지연)

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

"지수적(exponential)" 백오프 설정도 가능합니다. 예를 들어 아래처럼 배열로 설정한 경우, 첫 번째 재시도는 1초, 두 번째는 5초, 세 번째는 10초를 대기하며, 이후엔 계속 10초 동안 대기합니다.

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

<a name="silenced-jobs"></a>
### 음소거된 작업

특정 작업이 대시보드의 "완료된 작업" 목록에 표시되는 것을 원하지 않는 경우, 해당 작업을 음소거(silence)할 수 있습니다. 이를 위해, 작업 클래스명을 `horizon` 설정 파일의 `silenced` 옵션에 추가하세요.

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

개별 작업 클래스 외에도, [태그](#tags) 기반으로도 음소거를 지원합니다. 동일 태그를 가진 여러 작업을 숨길 때 유용합니다.

```php
'silenced_tags' => [
    'notifications'
],
```

또는, 음소거 대상 작업이 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하도록 할 수도 있습니다. 이 경우, 설정 파일에 추가하지 않아도 자동으로 음소거됩니다.

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## 부하 분산 전략

각 supervisor는 하나 이상의 큐를 처리할 수 있습니다. Laravel의 기본 큐 시스템과 달리, Horizon은 워커 분산 전략으로 `auto`, `simple`, `false` 중 하나를 선택할 수 있습니다.

<a name="auto-balancing"></a>
### 자동 부하 분산

기본값인 `auto` 전략은 각 큐의 현재 작업량에 따라 워커 프로세스 수를 자동으로 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 작업이 대기 중이고, `default` 큐는 비어 있다면, Horizon은 `notifications` 큐에 더 많은 워커를 할당하여 큐를 빠르게 소화하도록 합니다.

`auto` 전략을 사용할 때는 `minProcesses`와 `maxProcesses` 옵션도 설정할 수 있습니다.

<div class="content-list" markdown="1">

- `minProcesses`: 각 큐별 최소 워커 프로세스 수를 정의합니다. 1 이상이어야 합니다.
- `maxProcesses`: 모든 큐에 걸쳐 Horizon이 확장할 수 있는 최대 워커 프로세스 총합을 정의합니다. `minProcesses` * 큐 개수보다 크게 설정하는 것이 일반적입니다. 값을 0으로 설정하면 프로세스를 생성하지 않습니다.

</div>

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

`autoScalingStrategy` 옵션은 Horizon이 큐에 워커를 증설할 때 어떤 기준을 사용할지 결정합니다.

<div class="content-list" markdown="1">

- `time`: 큐를 모두 소화하는 데 걸리는 총 예상 시간을 기준으로 워커를 할당합니다.
- `size`: 큐에 남아있는 작업 개수를 기준으로 워커를 할당합니다.

</div>

`balanceMaxShift`와 `balanceCooldown` 값으로 Horizon이 워커 수를 증/감하는 속도를 조절할 수 있습니다. 위 설정에서는 3초마다 최대 1개의 프로세스가 생성 또는 제거됩니다. 애플리케이션 특성에 맞게 이 값을 조절할 수 있습니다.

<a name="auto-queue-priorities"></a>
#### 큐 우선순위와 자동 분산

`auto` 전략 사용 시, supervisor 설정 내 큐의 나열 순서는 우선순위에 영향을 주지 않습니다. 각 큐의 부하에 따라 동적으로 워커가 할당되고, `autoScalingStrategy`에 의해 분배됩니다.

예를 들어 아래와 같이 구성해도, `high` 큐가 `default` 큐보다 우선 처리되지 않습니다.

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

이 예시에서는 `default` 큐는 10개까지 확장 가능하고, `images` 큐는 1개의 프로세스만 사용하도록 보장됩니다. 이렇게 하면 각 큐별로 독립적 스케일링이 가능합니다.

> [!NOTE]
> 리소스 소모가 큰 작업은 별도 큐로 분리하고 `maxProcesses`를 제한하는 것이 바람직합니다. 규정 없이 무한 확장하면 시스템 과부하가 발생할 수 있습니다.

<a name="simple-balancing"></a>
### 단순 부하 분산

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

위 예시에서는 10개의 프로세스가 2개 큐에 각 5개씩 균등 할당됩니다.

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

이렇게 하면 `default` 큐에는 10개, `notifications` 큐에는 2개의 프로세스가 할당됩니다.

<a name="no-balancing"></a>
### 부하 분산 미사용

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

위 예시에서는 `default` 큐 작업이 항상 `notifications` 큐 작업보다 우선 처리됩니다. 만약 `default` 큐에 1,000개 작업, `notifications` 큐에 10개가 있다면, `default` 큐의 작업을 모두 처리한 후에야 `notifications` 큐 작업을 처리하게 됩니다.

워커 확장 범위는 `minProcesses`와 `maxProcesses` 옵션으로 제어할 수 있습니다.

<div class="content-list" markdown="1">

- `minProcesses`: 전체 최소 워커 프로세스 수. 1 이상이어야 합니다.
- `maxProcesses`: 전체 최대 워커 프로세스 수

</div>

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 주요 버전을 업그레이드할 때는 반드시 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 꼼꼼히 검토해야 합니다.

<a name="running-horizon"></a>
## Horizon 실행

`config/horizon.php` 파일에서 supervisor와 worker를 모두 설정했다면, `horizon` Artisan 명령어로 Horizon을 시작할 수 있습니다. 이 단일 명령어가 현재 환경에 맞는 모든 워커 프로세스를 구동합니다.

```shell
php artisan horizon
```

처리 중인 Horizon 프로세스를 일시정지 또는 재개하려면 다음과 같은 Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 Horizon [supervisor](#supervisors)를 일시정지하거나 재개하려면 다음 명령어를 사용하세요.

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

현재 Horizon 프로세스 상태를 확인하려면 다음 명령어를 사용하세요.

```shell
php artisan horizon:status
```

특정 Horizon [supervisor](#supervisors)의 상태를 확인하려면 아래와 같이 합니다.

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상적으로 종료하려면 `horizon:terminate` Artisan 명령어를 사용할 수 있습니다. 현재 처리 중인 작업이 마무리되고 Horizon이 종료됩니다.

```shell
php artisan horizon:terminate
```

<a name="automatically-restarting-horizon"></a>
#### Horizon 자동 재시작

로컬 개발 중에는 `horizon:listen` 명령어를 사용할 수 있습니다. 이 명령어를 사용하면, 코드가 변경될 때마다 Horizon을 수동으로 재시작하지 않아도 됩니다. 사용 전 반드시 [Node](https://nodejs.org)를 로컬 환경에 설치해야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리도 설치해야 합니다.

```shell
npm install --save-dev chokidar
```

Chokidar 설치 후, `horizon:listen` 명령어로 Horizon을 시작할 수 있습니다.

```shell
php artisan horizon:listen
```

Docker나 Vagrant 환경에서는 `--poll` 옵션을 사용하세요.

```shell
php artisan horizon:listen --poll
```

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
### Horizon 배포

실제 서버에 Horizon을 배포할 때는 프로세스 모니터를 이용해 `php artisan horizon` 명령어를 관리하며, 예기치 않게 종료될 때 재시작하도록 설정하세요. 아래에서 프로세스 모니터 설치 방법을 안내합니다.

배포 과정에서는 `horizon:terminate` 명령어로 Horizon 프로세스를 종료시키고, 프로세스 모니터가 코드 변경을 반영한 채로 자동 재시작하도록 해야 합니다.

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 Linux 운영체제용 프로세스 모니터로, `horizon` 프로세스가 중단될 경우 자동 재시작합니다. Ubuntu에 Supervisor를 설치하려면 아래 명령어를 사용할 수 있습니다. 다른 OS에서는 운영체제의 패키지 매니저로 Supervisor를 설치하세요.

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정이 어렵다면, [Laravel Cloud](https://cloud.laravel.com)를 활용하면 Laravel 애플리케이션의 백그라운드 프로세스를 관리할 수 있습니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

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

`stopwaitsecs` 값은 최장 실행 작업의 소요 시간보다 항상 크게 지정해야 합니다. 그렇지 않으면 Supervisor가 작업이 끝나기 전에 프로세스를 강제로 종료할 수 있습니다.

> [!WARNING]
> 위 예제는 Ubuntu 환경 기준입니다. 다른 운영체제에서는 Supervisor 설정 파일 위치와 확장자가 다를 수 있으니, 서버 문서를 반드시 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일 생성 후, 다음 명령어로 Supervisor 설정을 갱신하고 모니터링을 시작할 수 있습니다.

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 실행에 관한 추가 정보는 [Supervisor 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

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

이 작업이 `id` 속성값이 1인 `App\Models\Video` 인스턴스와 함께 큐에 등록된다면, 자동으로 `App\Models\Video:1`이라는 태그가 부여됩니다. Horizon이 작업 속성에서 Eloquent 모델을 찾아, 클래스명 및 기본 키(primary key) 조합으로 태그를 생성하기 때문입니다.

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업에 태그 수동 지정

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
#### 이벤트 리스너에 태그 수동 지정

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
## 알림

> [!WARNING]
> Horizon에서 Slack 또는 SMS 알림을 사용하려면, 반드시 관련 [알림 채널의 사전 요건](/docs/12.x/notifications)을 확인하세요.

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
#### 알림 대기 시간 임계값 설정

큐 대기 시간이 얼마나 길 경우를 "장시간 대기"로 간주할지, 애플리케이션의 `config/horizon.php`의 `waits` 옵션으로 지정할 수 있습니다. 각 연결/큐 조합별 임계값을 초 단위로 다음과 같이 조정하세요. 정의하지 않은 조합은 기본값 60초가 적용됩니다.

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

0으로 임계값을 설정하면 해당 큐에 대해 긴 대기 시간 알림이 비활성화됩니다.

<a name="metrics"></a>
## 메트릭

Horizon은 작업 및 큐 대기 시간, 처리량 관련 정보를 확인할 수 있는 메트릭 대시보드를 제공합니다. 대시보드에 데이터를 채우려면, `routes/console.php` 파일에서 Horizon의 `snapshot` Artisan 명령어가 5분마다 실행되도록 스케줄링해야 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

모든 메트릭 데이터를 삭제하고 싶다면, `horizon:clear-metrics` Artisan 명령어를 사용하세요.

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

개별 실패 작업을 삭제하려면 `horizon:forget` 명령어를 사용하면 됩니다. 이 명령어는 실패한 작업의 ID 또는 UUID 하나만 인수로 받습니다.

```shell
php artisan horizon:forget 5
```

모든 실패 작업을 삭제하려면, `--all` 옵션을 제공하세요.

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 삭제

애플리케이션 기본 큐에 누적된 모든 작업을 삭제하고 싶다면, 다음 Artisan 명령어를 사용하세요.

```shell
php artisan horizon:clear
```

특정 큐의 작업만 삭제하려면 `queue` 옵션을 지정하세요.

```shell
php artisan horizon:clear --queue=emails
```