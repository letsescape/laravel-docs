# Laravel Horizon (Laravel Horizon)

- [소개](#introduction)
- [설치](#installation)
    - [설정](#configuration)
    - [대시보드 인가](#dashboard-authorization)
    - [최대 작업 시도 횟수](#max-job-attempts)
    - [작업 제한 시간](#job-timeout)
    - [작업 대기 시간(backoff)](#job-backoff)
    - [무시되는 작업(Silenced Jobs)](#silenced-jobs)
- [부하 분배 전략](#balancing-strategies)
    - [자동 부하 분배](#auto-balancing)
    - [단순 부하 분배](#simple-balancing)
    - [부하 분배 없음](#no-balancing)
- [Horizon 업그레이드](#upgrading-horizon)
- [Horizon 실행](#running-horizon)
    - [Horizon 배포](#deploying-horizon)
- [태그](#tags)
- [알림](#notifications)
- [메트릭](#metrics)
- [실패한 작업 삭제](#deleting-failed-jobs)
- [큐에서 작업 비우기](#clearing-jobs-from-queues)

<a name="introduction"></a>
## 소개

> [!NOTE]
> Laravel Horizon을 학습하기 전에, 우선 Laravel의 기본 [큐 서비스](/docs/master/queues)에 익숙해지시기 바랍니다. Horizon은 라라벨의 큐에 다양한 부가 기능을 더해주므로, 기본 큐 기능을 알지 못한 상태에서는 혼란스러울 수 있습니다.

[Laravel Horizon](https://github.com/laravel/horizon)은 Laravel 기반 [Redis 큐](/docs/master/queues)를 위한 아름다운 대시보드와 코드 기반 설정 기능을 제공합니다. Horizon을 사용하면 작업 처리량, 실행 시간, 작업 실패 등 큐 시스템의 주요 지표를 쉽게 모니터링할 수 있습니다.

Horizon을 사용하면 모든 큐 워커 설정이 하나의 간단한 설정 파일에 저장됩니다. 애플리케이션의 워커 설정을 버전 관리된 파일로 관리할 수 있으므로, 애플리케이션 배포 시 손쉽게 큐 워커를 확장하거나 수정할 수 있습니다.

<img src="https://laravel.com/img/docs/horizon-example.png" />

<a name="installation"></a>
## 설치

> [!WARNING]
> Laravel Horizon은 큐 시스템으로 반드시 [Redis](https://redis.io)를 사용해야 합니다. 따라서, 애플리케이션의 `config/queue.php` 설정 파일에서 큐 연결을 `redis`로 지정해야 합니다. 현재 Horizon은 Redis Cluster와 호환되지 않습니다.

Composer 패키지 관리자를 사용하여 Horizon을 프로젝트에 설치할 수 있습니다:

```shell
composer require laravel/horizon
```

설치 후, 다음 Artisan 명령어로 Horizon의 에셋을 퍼블리시하세요:

```shell
php artisan horizon:install
```

<a name="configuration"></a>
### 설정

에셋 퍼블리시 후, 주요 설정 파일이 `config/horizon.php`에 위치합니다. 이 파일에서 애플리케이션의 큐 워커 옵션을 자유롭게 설정할 수 있습니다. 각 설정 옵션에는 그 목적에 대한 설명이 포함되어 있으므로, 반드시 이 파일을 꼼꼼히 살펴보시기 바랍니다.

> [!WARNING]
> Horizon은 내부적으로 `horizon`이라는 이름의 Redis 연결을 사용합니다. 이 이름은 예약되어 있으므로, `database.php` 설정 파일이나 `horizon.php` 설정 파일의 `use` 옵션 등에서 다른 Redis 연결 이름으로 사용해서는 안 됩니다.

<a name="environments"></a>
#### 환경

설치 후 가장 먼저 익혀야 할 Horizon의 주요 설정 옵션은 `environments` 옵션입니다. 이 옵션은 애플리케이션이 실행되는 환경의 목록이며, 각 환경별로 워커 프로세스 옵션을 정의합니다. 기본적으로 `production`과 `local` 환경이 포함되어 있지만, 필요에 따라 더 많은 환경을 추가할 수 있습니다:

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

별도의 환경이 일치하지 않을 때 사용될 와일드카드 환경(`*`)도 정의할 수 있습니다:

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

Horizon을 실행하면, 현재 애플리케이션이 동작하는 환경에 맞는 워커 프로세스 설정을 사용합니다. 일반적으로, 현재 환경은 `APP_ENV` [환경 변수](/docs/master/configuration#determining-the-current-environment)의 값에 따라 결정됩니다. 예를 들어, 기본 `local` 환경에서는 워커 프로세스 3개가 실행되며, 각 큐에 자동으로 프로세스를 배분합니다. `production` 환경은 최대 10개의 워커 프로세스가 실행되며, 역시 각 큐에 프로세스를 자동으로 배분하도록 설정되어 있습니다.

> [!WARNING]
> Horizon을 실행할 모든 [환경](/docs/master/configuration#environment-configuration)에 대한 항목이 `horizon` 설정 파일의 `environments` 부분에 반드시 포함되어 있는지 확인하세요.

<a name="supervisors"></a>
#### Supervisor

Horizon의 기본 설정 파일을 보면, 각 환경에는 하나 이상의 "supervisor"를 포함할 수 있습니다. 기본적으로 `supervisor-1`이라는 supervisor가 정의되어 있지만, 원하는 이름으로 supervisor를 지정할 수 있습니다. 각 supervisor는 하나 이상의 워커 프로세스 그룹을 "감독"하며, 큐간 워커 배분을 책임집니다.

추가적인 워커 프로세스 그룹을 만들고 싶다면, 해당 환경에 supervisor를 추가할 수 있습니다. 예를 들어, 특정 큐에 다른 부하 분배 전략이나 워커 프로세스 수를 적용하고 싶을 때 supervisor를 추가 및 설정하면 됩니다.

<a name="maintenance-mode"></a>
#### 점검 모드

애플리케이션이 [점검 모드](/docs/master/configuration#maintenance-mode)에 있을 때는, supervisor의 `force` 옵션이 `true`로 설정되지 않는 한 Horizon이 작업을 처리하지 않습니다:

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

Horizon의 기본 설정 파일에는 `defaults`라는 설정 옵션이 있습니다. 이 옵션은 [supervisor](#supervisors)의 기본값을 지정합니다. supervisor의 기본값은 각 환경의 supervisor 설정에 병합되어, supervisor를 정의할 때 불필요한 반복을 줄여줍니다.

<a name="dashboard-authorization"></a>
### 대시보드 인가

Horizon 대시보드는 `/horizon` 경로를 통해 접근할 수 있습니다. 기본적으로는 `local` 환경에서만 대시보드에 접근할 수 있습니다. 하지만, `app/Providers/HorizonServiceProvider.php` 파일에 [인가 게이트](/docs/master/authorization#gates) 정의가 포함되어 있습니다. 이 게이트는 **local 환경 이외**에서 Horizon 접근을 제어합니다. 필요에 따라 게이트 정의를 수정하여 Horizon에 대한 접근을 제한할 수 있습니다:

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
#### 대체 인증 방법

Laravel은 인가 게이트 클로저에 자동으로 인증된 사용자를 주입합니다. 만약 IP 제한 등 다른 방식으로 Horizon 접근을 통제한다면, 대시보드 이용자가 "로그인"할 필요가 없을 수 있습니다. 이 때에는, 예시의 클로저 시그니처를 `function (User $user)`에서 `function (User $user = null)`로 변경하여 Laravel이 인증을 강제하지 않도록 할 수 있습니다.

<a name="max-job-attempts"></a>
### 최대 작업 시도 횟수

> [!NOTE]
> 이 옵션을 다루기 전에, Laravel의 기본 [큐 서비스](/docs/master/queues#max-job-attempts-and-timeout)와 '시도 횟수' 개념을 충분히 익히세요.

supervisor 설정을 통해 작업당 최대 시도 횟수를 지정할 수 있습니다:

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
> 이 옵션은 Artisan 큐 처리 명령어의 `--tries` 옵션과 유사하게 동작합니다.

`WithoutOverlapping`이나 `RateLimited` 등 미들웨어를 사용할 때는 시도 횟수가 소비됩니다. 이런 경우 적절히 supervisor의 `tries` 값을 늘리거나, 작업 클래스에 `$tries` 속성을 정의해야 합니다.

`tries` 옵션을 지정하지 않으면 기본적으로 1회 시도가 적용되며, 작업 클래스에서 `$tries`를 정의한 경우에는 해당 설정이 우선 적용됩니다.

시도 횟수(`tries` 또는 `$tries`)를 0으로 설정하면 시도 횟수 제한 없이 무제한으로 작업을 재시도합니다. 시도 횟수를 특정할 수 없는 경우에 주로 사용하지만, 무한 반복 실패를 막으려면 작업 클래스의 `$maxExceptions` 속성을 통해 예외 허용 횟수를 제한하는 것이 바람직합니다.

<a name="job-timeout"></a>
### 작업 제한 시간

마찬가지로 supervisor 단위로 `timeout` 값을 설정하여, 워커 프로세스가 하나의 작업을 최대 몇 초 동안 실행할 수 있는지 지정할 수 있습니다. 제한 시간이 초과되면 워커 프로세스는 작업을 강제 종료하며, 큐 설정에 따라 해당 작업은 재시도되거나 실패로 처리됩니다:

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
> `auto` 부하 분배 전략을 사용할 때, Horizon은 진행 중인 워커들을 timeout 이후 "멈춤/hanging" 상태로 간주하며, 스케일 다운 시 강제 종료합니다. Horizon의 timeout이 각 작업의 제한 시간보다 항상 커야 하며, 그렇지 않으면 작업이 중간에 종료될 수 있습니다. 또한, `timeout` 값은 `config/queue.php`의 `retry_after` 값보다 몇 초 이상 짧아야 합니다. 그렇지 않으면 작업이 중복 처리될 수 있습니다.

<a name="job-backoff"></a>
### 작업 대기 시간(backoff)

supervisor 설정에서 `backoff` 값을 지정하면, 처리 중 예기치 않은 예외가 발생한 작업을 재시도하기 전 Horizon이 얼마나 대기할지 설정할 수 있습니다:

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

배열을 사용하여 "지수적" backoff도 설정할 수 있습니다. 다음 예시에서는 첫 번째 재시도는 1초 후, 두 번째는 5초 후, 세 번째 및 그 이후에는 10초 후에 재시도합니다:

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
### 무시되는 작업(Silenced Jobs)

애플리케이션 또는 외부 패키지에서 발생하는 일부 작업이 "완료 작업" 목록에 표시되지 않도록 무시 처리할 수 있습니다. 이를 위해, `horizon` 설정 파일의 `silenced` 항목에 작업 클래스명을 추가하세요:

```php
'silenced' => [
    App\Jobs\ProcessPodcast::class,
],
```

여러 작업에 공통적으로 적용하려면, [태그](#tags) 기준으로도 무시 정책을 지정할 수 있습니다:

```php
'silenced_tags' => [
    'notifications'
],
```

또는, 무시하려는 작업 클래스가 `Laravel\Horizon\Contracts\Silenced` 인터페이스를 구현하면, 해당 작업은 `silenced` 배열에 명시하지 않아도 자동으로 무시됩니다:

```php
use Laravel\Horizon\Contracts\Silenced;

class ProcessPodcast implements ShouldQueue, Silenced
{
    use Queueable;

    // ...
}
```

<a name="balancing-strategies"></a>
## 부하 분배 전략

각 supervisor는 하나 이상의 큐를 처리할 수 있으며, Laravel의 기본 큐 시스템과 달리 Horizon은 `auto`, `simple`, `false`의 세 가지 워커 부하 분배 전략 중에서 선택할 수 있습니다.

<a name="auto-balancing"></a>
### 자동 부하 분배

기본값인 `auto` 전략은 각 큐의 실시간 대기 작업 수에 따라 큐별 워커 프로세스 개수를 조정합니다. 예를 들어, `notifications` 큐에 1,000개의 대기 작업이 있고, `default` 큐는 비어 있다면, Horizon은 `notifications` 큐에 더 많은 워커를 배정시켜 큐가 빨리 비워지도록 합니다.

`auto` 전략에서는 `minProcesses` 및 `maxProcesses`도 설정할 수 있습니다:

- `minProcesses`는 큐별 최소 워커 프로세스 수(1 이상)입니다.
- `maxProcesses`는 전체 큐를 대상으로 Horizon이 스케일할 수 있는 최대 워커 프로세스 수입니다. 이 값은 일반적으로 `queue` 개수 × `minProcesses`보다 커야 하며, 0으로 설정하면 프로세스가 생성되지 않습니다.

예를 들어, 큐별 최소 1개 프로세스, 전체 최대 10개의 워커 프로세스를 설정할 수 있습니다:

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

`autoScalingStrategy` 항목은 Horizon이 워커 프로세스를 큐에 할당하는 전략을 지정합니다:

- `time` 전략: 큐가 모두 처리될 때까지 걸릴 예상 시간에 따라 워커를 할당합니다.
- `size` 전략: 큐에 쌓인 작업 개수를 기반으로 워커를 할당합니다.

`balanceMaxShift`, `balanceCooldown` 값은 Horizon이 워커 수를 얼마나 빠르게 조절할지 결정합니다. 위 예에서는 3초마다 1개 프로세스씩 생성/제거할 수 있습니다. 애플리케이션 특성에 맞게 값을 조정하십시오.

<a name="auto-queue-priorities"></a>
#### 큐 우선순위와 자동 부하 분배

`auto` 전략 사용 시, 큐 간 엄격한 우선순위는 적용되지 않습니다. supervisor 설정에서 큐를 나열하는 순서가 워커 배정에 영향을 주지 않고, Horizon은 `autoScalingStrategy`에 따라 실시간 부하 기반으로 동적으로 워커를 배분합니다.

예시 설정에서, `high` 큐가 `default`보다 먼저 나와도 실제로 `high`가 더 높은 우선순위를 가지지 않습니다:

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

특정 큐의 처리 우선순위를 명확히 주고 싶다면, 여러 supervisor를 활용해 워커 리소스를 명시적으로 분할하면 됩니다:

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

이 구성에서는 `default` 큐는 최대 10개의 프로세스로, `images` 큐는 최대 1개의 프로세스로 개별적으로 확장할 수 있습니다.

> [!NOTE]
> CPU를 많이 소모하는 작업은 별도의 큐에 `maxProcesses`를 제한하여 할당하는 것이 좋습니다. 그렇지 않으면 시스템이 과부하될 수 있습니다.

<a name="simple-balancing"></a>
### 단순 부하 분배

`simple` 전략은 고정된 프로세스 수를 큐별로 균등하게 분배합니다. 자동 확장 기능은 없으며, 총 워커 수만 지정할 수 있습니다:

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

위 예시에서는 `default`와 `notifications` 큐에 각각 5개의 프로세스가 할당됩니다(총 10개).

각 큐별로 워커 수를 별도로 통제하려면 supervisor를 여러 개 두면 됩니다:

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

위와 같은 구성에서는 `default` 큐에는 10개, `notifications` 큐에는 2개의 프로세스가 할당됩니다.

<a name="no-balancing"></a>
### 부하 분배 없음

`balance` 옵션이 `false`로 설정되면, Horizon은 큐를 나열된 순서대로만 처리하며, Laravel의 기본 큐 시스템과 비슷하게 동작합니다. 단, 작업이 쌓이기 시작하면 워커 프로세스는 여전히 확장될 수 있습니다:

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

이 예시에서는 `default` 큐 작업이 항상 `notifications` 큐 작업보다 우선 처리됩니다. 예를 들어 `default`에 1,000개, `notifications`에 10개 작업이 있는 경우, Horizon은 먼저 `default`의 작업을 모두 처리한 후에야 `notifications`로 넘어갑니다.

워크 프로세스의 최소/최대치를 `minProcesses`, `maxProcesses` 옵션으로 조절할 수 있습니다:

- `minProcesses`: 전체 워커 프로세스의 최소 수(1 이상)
- `maxProcesses`: 워커 프로세스가 최대 몇 개까지 확장 가능한지 지정

<a name="upgrading-horizon"></a>
## Horizon 업그레이드

Horizon의 메이저 버전 업그레이드 시에는 [업그레이드 가이드](https://github.com/laravel/horizon/blob/master/UPGRADE.md)를 반드시 꼼꼼히 확인하시기 바랍니다.

<a name="running-horizon"></a>
## Horizon 실행

`config/horizon.php`에서 supervisor/worker 구성을 마치면, `horizon` Artisan 명령어로 Horizon을 실행할 수 있습니다. 이 명령어 하나로, 현재 환경에 맞게 설정된 모든 워커 프로세스가 시작됩니다:

```shell
php artisan horizon
```

`horizon:pause` 명령어로 Horizon 처리를 일시 중지할 수 있고, `horizon:continue` 명령어로 처리를 재개할 수 있습니다:

```shell
php artisan horizon:pause

php artisan horizon:continue
```

특정 [supervisor](#supervisors) 단위로도 일시 중지 및 재개가 가능합니다:

```shell
php artisan horizon:pause-supervisor supervisor-1

php artisan horizon:continue-supervisor supervisor-1
```

Horizon의 현재 상태는 `horizon:status` 명령어로 확인할 수 있습니다:

```shell
php artisan horizon:status
```

특정 [supervisor](#supervisors)의 상태는 `horizon:supervisor-status` 명령어로 확인할 수 있습니다:

```shell
php artisan horizon:supervisor-status supervisor-1
```

Horizon 프로세스를 정상적으로 종료하려면 `horizon:terminate` 명령어를 사용하세요. 현재 처리 중인 작업이 모두 완료된 후 Horizon이 종료됩니다:

```shell
php artisan horizon:terminate
```

<a name="automatically-restarting-horizon"></a>
#### Horizon 자동 재시작

로컬 개발 시에는 `horizon:listen` 명령어를 사용할 수 있습니다. 이 명령어는 코드 변경 시 Horizon을 수동으로 재시작할 필요가 없게 해줍니다. 이 기능을 사용하기 전에, 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있어야 하며, 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리도 설치해야 합니다:

```shell
npm install --save-dev chokidar
```

Chokidar를 설치한 후, 다음 명령어로 Horizon을 실행합니다:

```shell
php artisan horizon:listen
```

도커(Docker)나 배거(Vagrant) 환경에서는 `--poll` 옵션을 사용하세요:

```shell
php artisan horizon:listen --poll
```

감시할 디렉토리 및 파일은 `config/horizon.php`의 `watch` 옵션에서 지정할 수 있습니다:

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

실제 운영 서버에 Horizon을 배포할 준비가 되면, `php artisan horizon` 명령어를 모니터링하며 Horizon 프로세스가 예기치 않게 종료될 경우 자동 재시작하는 프로세스 모니터를 구성해야 합니다. 아래에서 프로세스 모니터 설치 방법도 설명합니다.

배포 작업 중에는 Horizon 프로세스가 재시작하여 최신 코드 변경 사항을 반영하도록, 먼저 Horizon 프로세스를 종료해야 합니다:

```shell
php artisan horizon:terminate
```

<a name="installing-supervisor"></a>
#### Supervisor 설치

Supervisor는 리눅스 운영체제용 프로세스 모니터로, `horizon` 프로세스가 종료될 경우 자동으로 재시작합니다. Ubuntu에서는 아래와 같이 Supervisor를 설치할 수 있습니다. Ubuntu가 아니라면 해당 운영체제의 패키지 관리자를 사용하여 설치하세요:

```shell
sudo apt-get install supervisor
```

> [!NOTE]
> Supervisor 직접 설정이 부담스럽다면, [Laravel Cloud](https://cloud.laravel.com) 사용을 고려하세요. 이 서비스는 Laravel 애플리케이션 백그라운드 프로세스를 관리해줍니다.

<a name="supervisor-configuration"></a>
#### Supervisor 설정

Supervisor 설정 파일은 서버의 `/etc/supervisor/conf.d` 디렉터리에 저장하는 것이 일반적입니다. 이 디렉터리에, 모니터링할 각 프로세스 설정 파일(예: `horizon.conf`)을 생성할 수 있습니다:

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

Supervisor 설정 시, `stopwaitsecs` 값이 가장 오래 실행되는 작업의 소요 시간보다 커야 합니다. 그렇지 않으면 작업이 완료되기도 전에 Supervisor가 프로세스를 종료시킬 수 있습니다.

> [!WARNING]
> 위 예시는 Ubuntu 기반 서버에 대한 것이며, Supervisor 설정 파일의 위치 및 파일 확장자는 각 운영체제에 따라 다를 수 있습니다. 자세한 내용은 각 서버 OS의 문서를 참고하세요.

<a name="starting-supervisor"></a>
#### Supervisor 시작

설정 파일을 만들었다면, 아래 명령어로 Supervisor 설정을 반영하고, 지정된 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start horizon
```

> [!NOTE]
> Supervisor 운영에 대한 더 자세한 정보는 [Supervisor 공식 문서](http://supervisord.org/index.html)를 참고하세요.

<a name="tags"></a>
## 태그

Horizon은 작업(메일 발송, 브로드캐스트 이벤트, 알림, 큐에 등록된 이벤트 리스너 등)에 "태그"를 지정할 수 있습니다. 실제로 Horizon은 작업에 연결된 Eloquent 모델을 기반으로 지능적으로 자동 태깅을 합니다. 아래 예시 작업을 살펴보세요:

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

이 작업이 `id` 속성이 1인 `App\Models\Video` 인스턴스와 함께 큐에 등록된다면, 해당 작업은 자동으로 `App\Models\Video:1`이라는 태그가 부여됩니다. Horizon이 작업의 속성에서 Eloquent 모델 인스턴스를 찾아, 모델 클래스명과 기본키(primary key)로 태깅하기 때문입니다:

```php
use App\Jobs\RenderVideo;
use App\Models\Video;

$video = Video::find(1);

RenderVideo::dispatch($video);
```

<a name="manually-tagging-jobs"></a>
#### 작업 태그 수동 지정

큐에 들어가는 객체에 태그를 직접 지정하려면, 클래스에 `tags` 메서드를 정의하세요:

```php
class RenderVideo implements ShouldQueue
{
    /**
     * 작업에 적용할 태그를 반환합니다.
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
#### 이벤트 리스너 태그 수동 지정

큐에 등록된 이벤트 리스너의 경우, Horizon은 이벤트 인스턴스를 `tags` 메서드에 인자로 넘겨주므로, 이벤트 데이터를 활용해 태그에 추가할 수 있습니다:

```php
class SendRenderNotifications implements ShouldQueue
{
    /**
     * 리스너에 적용할 태그를 반환합니다.
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
> Horizon에서 Slack 또는 SMS 알림을 구성할 땐, [해당 알림 채널의 사전 준비사항](/docs/master/notifications)을 반드시 확인하세요.

큐 중 하나의 대기 시간이 길어졌을 때 알림을 받고 싶다면, `Horizon::routeMailNotificationsTo`, `Horizon::routeSlackNotificationsTo`, `Horizon::routeSmsNotificationsTo` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\HorizonServiceProvider`의 `boot` 메서드에서 호출하면 됩니다:

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

"대기 시간이 길다"라고 간주될 기준을 `config/horizon.php` 파일의 `waits` 설정으로 제어할 수 있습니다. 이 옵션을 통해 각 커넥션/큐 조합별로 임계값(초)을 지정합니다. 지정되지 않은 조합은 기본적으로 60초가 임계값으로 사용됩니다:

```php
'waits' => [
    'redis:critical' => 30,
    'redis:default' => 60,
    'redis:batch' => 120,
],
```

특정 큐의 임계값을 `0`으로 지정하면, 해당 큐는 장시간 대기 알림이 비활성화됩니다.

<a name="metrics"></a>
## 메트릭

Horizon에는 작업 및 큐의 대기 시간·처리량 등 여러 메트릭 정보를 제공하는 대시보드가 내장되어 있습니다. 이 대시보드가 정보를 채우려면, 애플리케이션의 `routes/console.php` 파일에 `horizon:snapshot` Artisan 명령어가 5분마다 실행되도록 지정해 주세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('horizon:snapshot')->everyFiveMinutes();
```

모든 메트릭 데이터를 삭제하고 싶을 경우, 다음 Artisan 명령어를 실행하세요:

```shell
php artisan horizon:clear-metrics
```

<a name="deleting-failed-jobs"></a>
## 실패한 작업 삭제

실패한 작업을 개별적으로 삭제하고 싶을 때는, `horizon:forget` 명령어를 사용하세요. 이 명령어는 실패한 작업의 ID나 UUID를 인수로 받습니다:

```shell
php artisan horizon:forget 5
```

모든 실패한 작업을 삭제하려면 `--all` 옵션을 추가하세요:

```shell
php artisan horizon:forget --all
```

<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 비우기

애플리케이션의 기본 큐에 쌓인 모든 작업을 지우고 싶을 경우, `horizon:clear` Artisan 명령어를 사용하세요:

```shell
php artisan horizon:clear
```

특정 큐의 작업만 지우고 싶다면 `queue` 옵션을 활용하세요:

```shell
php artisan horizon:clear --queue=emails
```