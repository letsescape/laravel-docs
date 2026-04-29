# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의하기](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [셸 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 주기 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중복 실행 방지](#preventing-task-overlaps)
    - [하나의 서버에서 작업 실행하기](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [유지보수 모드](#maintenance-mode)
    - [스케줄된 작업 일시 중지하기](#pausing-scheduled-tasks)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행하기](#running-the-scheduler)
    - [분 단위 미만으로 스케줄된 작업](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행하기](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

이전에는 서버에서 스케줄링해야 하는 각 작업마다 cron 설정 항목을 작성했을 수 있습니다. 하지만 이렇게 하면 작업 스케줄이 더 이상 소스 관리에 포함되지 않고, 기존 cron 항목을 확인하거나 새 항목을 추가하려면 서버에 SSH로 접속해야 하므로 금방 번거로워질 수 있습니다.

Laravel의 명령어 스케줄러는 서버의 스케줄된 작업을 관리하는 새로운 방식을 제공합니다. 스케줄러를 사용하면 Laravel 애플리케이션 안에서 명령어 스케줄을 유창하고 표현력 있게 정의할 수 있습니다. 스케줄러를 사용할 때 서버에는 하나의 cron 항목만 필요합니다. 작업 스케줄은 일반적으로 애플리케이션의 `routes/console.php` 파일에 정의합니다.

<a name="defining-schedules"></a>
## 스케줄 정의하기 (Defining Schedules)

스케줄된 모든 작업은 애플리케이션의 `routes/console.php` 파일에 정의할 수 있습니다. 먼저 예제를 살펴보겠습니다. 이 예제에서는 매일 자정에 호출될 클로저를 스케줄링합니다. 클로저 안에서는 테이블을 비우기 위해 데이터베이스 쿼리를 실행합니다.

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 사용한 스케줄링 외에도 [호출 가능한 객체](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 스케줄링할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 포함하는 간단한 PHP 클래스입니다.

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

`routes/console.php` 파일을 명령어 정의 전용으로만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용하여 스케줄된 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 전달받는 클로저를 인수로 받습니다.

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

스케줄된 작업의 개요와 다음 실행 예정 시간을 확인하려면 `schedule:list` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저를 스케줄링하는 것 외에도 [Artisan 명령어](/docs/13.x/artisan)와 시스템 명령어를 스케줄링할 수 있습니다. 예를 들어 `command` 메서드를 사용하면 명령어 이름 또는 클래스 중 하나로 Artisan 명령어를 스케줄링할 수 있습니다.

명령어 클래스 이름을 사용하여 Artisan 명령어를 스케줄링할 때는, 명령어가 호출될 때 전달할 추가 명령줄 인수를 배열로 넘길 수 있습니다.

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### Artisan 클로저 명령어 스케줄링

클로저로 정의된 Artisan 명령어를 스케줄링하려면, 명령어 정의 뒤에 스케줄링 관련 메서드를 체이닝할 수 있습니다.

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인수를 전달해야 한다면, `schedule` 메서드에 인수를 제공할 수 있습니다.

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

`job` 메서드는 [큐 작업](/docs/13.x/queues)을 스케줄링하는 데 사용할 수 있습니다. 이 메서드는 작업을 큐에 넣기 위해 `call` 메서드로 클로저를 정의하지 않고도 큐 작업을 스케줄링할 수 있는 편리한 방법을 제공합니다.

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

`job` 메서드에는 선택적으로 두 번째와 세 번째 인수를 제공할 수 있으며, 각각 작업을 큐에 넣을 때 사용할 큐 이름과 큐 연결을 지정합니다.

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 셸 명령어 스케줄링

`exec` 메서드는 운영체제에 명령어를 실행하도록 지시하는 데 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 주기 옵션

지정된 간격으로 작업을 실행하도록 설정하는 몇 가지 예제를 이미 살펴보았습니다. 하지만 작업에 지정할 수 있는 스케줄 주기는 훨씬 더 다양합니다.

<div class="overflow-auto">

| Method                             | Description                                              |
| ---------------------------------- | -------------------------------------------------------- |
| `->cron('* * * * *');`             | 사용자 정의 cron 스케줄로 작업을 실행합니다.                  |
| `->everySecond();`                 | 매초 작업을 실행합니다.                               |
| `->everyTwoSeconds();`             | 2초마다 작업을 실행합니다.                          |
| `->everyFiveSeconds();`            | 5초마다 작업을 실행합니다.                         |
| `->everyTenSeconds();`             | 10초마다 작업을 실행합니다.                          |
| `->everyFifteenSeconds();`         | 15초마다 작업을 실행합니다.                      |
| `->everyTwentySeconds();`          | 20초마다 작업을 실행합니다.                       |
| `->everyThirtySeconds();`          | 30초마다 작업을 실행합니다.                       |
| `->everyMinute();`                 | 매분 작업을 실행합니다.                               |
| `->everyTwoMinutes();`             | 2분마다 작업을 실행합니다.                          |
| `->everyThreeMinutes();`           | 3분마다 작업을 실행합니다.                        |
| `->everyFourMinutes();`            | 4분마다 작업을 실행합니다.                         |
| `->everyFiveMinutes();`            | 5분마다 작업을 실행합니다.                         |
| `->everyTenMinutes();`             | 10분마다 작업을 실행합니다.                          |
| `->everyFifteenMinutes();`         | 15분마다 작업을 실행합니다.                      |
| `->everyThirtyMinutes();`          | 30분마다 작업을 실행합니다.                       |
| `->hourly();`                      | 매시간 작업을 실행합니다.                                 |
| `->hourlyAt(17);`                  | 매시간 정각에서 17분이 지난 시점에 작업을 실행합니다.     |
| `->everyOddHour($minutes = 0);`    | 홀수 시간마다 작업을 실행합니다.                             |
| `->everyTwoHours($minutes = 0);`   | 2시간마다 작업을 실행합니다.                            |
| `->everyThreeHours($minutes = 0);` | 3시간마다 작업을 실행합니다.                          |
| `->everyFourHours($minutes = 0);`  | 4시간마다 작업을 실행합니다.                           |
| `->everySixHours($minutes = 0);`   | 6시간마다 작업을 실행합니다.                            |
| `->daily();`                       | 매일 자정에 작업을 실행합니다.                      |
| `->dailyAt('13:00');`              | 매일 13:00에 작업을 실행합니다.                         |
| `->twiceDaily(1, 13);`             | 매일 1:00와 13:00에 작업을 실행합니다.                      |
| `->twiceDailyAt(1, 13, 15);`       | 매일 1:15와 13:15에 작업을 실행합니다.                      |
| `->daysOfMonth([1, 10, 20]);`      | 매월 특정 날짜에 작업을 실행합니다.              |
| `->weekly();`                      | 매주 일요일 00:00에 작업을 실행합니다.                      |
| `->weeklyOn(1, '8:00');`           | 매주 월요일 8:00에 작업을 실행합니다.               |
| `->monthly();`                     | 매월 첫째 날 00:00에 작업을 실행합니다.   |
| `->monthlyOn(4, '15:00');`         | 매월 4일 15:00에 작업을 실행합니다.            |
| `->twiceMonthly(1, 16, '13:00');`  | 매월 1일과 16일 13:00에 작업을 실행합니다.       |
| `->lastDayOfMonth('15:00');`       | 매월 마지막 날 15:00에 작업을 실행합니다.      |
| `->quarterly();`                   | 매분기 첫째 날 00:00에 작업을 실행합니다. |
| `->quarterlyOn(4, '14:00');`       | 매분기 4일 14:00에 작업을 실행합니다.          |
| `->yearly();`                      | 매년 첫째 날 00:00에 작업을 실행합니다.    |
| `->yearlyOn(6, 1, '17:00');`       | 매년 6월 1일 17:00에 작업을 실행합니다.            |
| `->timezone('America/New_York');`  | 작업의 타임존을 설정합니다.                           |

</div>

이러한 메서드는 추가 제약 조건과 조합하여, 특정 요일에만 실행되는 더욱 세밀한 스케줄을 만들 수 있습니다. 예를 들어 매주 월요일에 명령어가 실행되도록 스케줄링할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

// Run once per week on Monday at 1 PM...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// Run hourly from 8 AM to 5 PM on weekdays...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

추가 스케줄 제약 조건 목록은 아래에서 확인할 수 있습니다.

<div class="overflow-auto">

| Method                                   | Description                                            |
| ---------------------------------------- | ------------------------------------------------------ |
| `->weekdays();`                          | 작업을 평일로 제한합니다.                            |
| `->weekends();`                          | 작업을 주말로 제한합니다.                            |
| `->sundays();`                           | 작업을 일요일로 제한합니다.                              |
| `->mondays();`                           | 작업을 월요일로 제한합니다.                              |
| `->tuesdays();`                          | 작업을 화요일로 제한합니다.                             |
| `->wednesdays();`                        | 작업을 수요일로 제한합니다.                           |
| `->thursdays();`                         | 작업을 목요일로 제한합니다.                            |
| `->fridays();`                           | 작업을 금요일로 제한합니다.                              |
| `->saturdays();`                         | 작업을 토요일로 제한합니다.                            |
| `->days(array\|mixed);`                  | 작업을 특정 요일로 제한합니다.                       |
| `->between($startTime, $endTime);`       | 작업을 시작 시간과 종료 시간 사이에만 실행되도록 제한합니다.     |
| `->unlessBetween($startTime, $endTime);` | 작업을 시작 시간과 종료 시간 사이에는 실행되지 않도록 제한합니다. |
| `->when(Closure);`                       | 진리 검사 결과에 따라 작업을 제한합니다.                  |
| `->environments($env);`                  | 작업을 특정 환경으로 제한합니다.               |

</div>

<a name="day-constraints"></a>
#### 요일 제약 조건

`days` 메서드는 작업 실행을 특정 요일로 제한하는 데 사용할 수 있습니다. 예를 들어 일요일과 수요일마다 매시간 명령어가 실행되도록 스케줄링할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또는 작업이 실행될 요일을 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스에서 제공하는 상수를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간 범위 제약 조건

`between` 메서드는 하루 중 특정 시간대를 기준으로 작업 실행을 제한하는 데 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

마찬가지로 `unlessBetween` 메서드는 특정 시간 동안 작업 실행을 제외하는 데 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 진리 검사 제약 조건

`when` 메서드는 주어진 진리 검사 결과를 기준으로 작업 실행을 제한하는 데 사용할 수 있습니다. 즉, 주어진 클로저가 `true`를 반환하면 작업 실행을 막는 다른 제약 조건이 없는 한 해당 작업이 실행됩니다.

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`의 반대 개념으로 볼 수 있습니다. `skip` 메서드가 `true`를 반환하면 스케줄된 작업은 실행되지 않습니다.

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

`when` 메서드를 체이닝하여 사용할 때는 모든 `when` 조건이 `true`를 반환해야만 스케줄된 명령어가 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약 조건

`environments` 메서드는 지정된 환경(`APP_ENV` [환경 변수](/docs/13.x/configuration#environment-configuration)에 정의된 환경)에서만 작업을 실행하는 데 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존

`timezone` 메서드를 사용하면 스케줄된 작업의 시간이 지정된 타임존을 기준으로 해석되도록 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

모든 스케줄된 작업에 같은 타임존을 반복해서 지정하고 있다면, 애플리케이션의 `app` 설정 파일에 `schedule_timezone` 옵션을 정의하여 모든 스케줄에 적용할 타임존을 지정할 수 있습니다.

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 타임존은 일광 절약 시간제를 사용한다는 점을 기억하세요. 일광 절약 시간이 변경될 때 스케줄된 작업이 두 번 실행되거나 전혀 실행되지 않을 수 있습니다. 이러한 이유로 가능하면 타임존 스케줄링은 피하는 것을 권장합니다.

<a name="preventing-task-overlaps"></a>
### 작업 중복 실행 방지

기본적으로 스케줄된 작업은 이전 작업 인스턴스가 아직 실행 중이어도 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

이 예제에서 `emails:send` [Artisan 명령어](/docs/13.x/artisan)는 이미 실행 중이 아니라면 매분 실행됩니다. `withoutOverlapping` 메서드는 실행 시간이 크게 달라져 특정 작업이 얼마나 오래 걸릴지 정확히 예측하기 어려운 작업이 있을 때 특히 유용합니다.

필요하다면 "중복 실행 방지" 잠금이 만료되기까지 몇 분이 지나야 하는지 지정할 수 있습니다. 기본적으로 잠금은 24시간 후에 만료됩니다.

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

내부적으로 `withoutOverlapping` 메서드는 잠금을 얻기 위해 애플리케이션의 [캐시](/docs/13.x/cache)를 사용합니다. 필요한 경우 `schedule:clear-cache` Artisan 명령어를 사용하여 이러한 캐시 잠금을 지울 수 있습니다. 일반적으로 이는 예기치 못한 서버 문제로 작업이 멈춘 경우에만 필요합니다.

<a name="running-tasks-on-one-server"></a>
### 하나의 서버에서 작업 실행하기

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션이 기본 캐시 드라이버로 `database`, `memcached`, `dynamodb`, 또는 `redis` 캐시 드라이버를 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

애플리케이션의 스케줄러가 여러 서버에서 실행 중이라면, 스케줄된 작업이 하나의 서버에서만 실행되도록 제한할 수 있습니다. 예를 들어 매주 금요일 밤에 새 보고서를 생성하는 스케줄된 작업이 있다고 가정해 보겠습니다. 작업 스케줄러가 세 대의 워커 서버에서 실행 중이라면, 스케줄된 작업은 세 서버 모두에서 실행되어 보고서가 세 번 생성됩니다. 좋지 않습니다!

작업이 하나의 서버에서만 실행되어야 함을 나타내려면, 스케줄된 작업을 정의할 때 `onOneServer` 메서드를 사용하세요. 작업을 처음 획득한 서버가 해당 작업에 대한 원자적 잠금을 확보하여 다른 서버가 같은 작업을 동시에 실행하지 못하도록 합니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

단일 서버 작업에 필요한 원자적 잠금을 얻을 때 스케줄러가 사용할 캐시 저장소를 사용자 정의하려면 `useCache` 메서드를 사용할 수 있습니다.

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업에 이름 지정하기

때로는 같은 작업을 서로 다른 매개변수로 디스패치하도록 스케줄링하면서도, 각 작업의 변형이 하나의 서버에서만 실행되도록 Laravel에 지시해야 할 수 있습니다. 이를 위해 `name` 메서드를 통해 각 스케줄 정의에 고유한 이름을 지정할 수 있습니다.

```php
Schedule::job(new CheckUptime('https://laravel.com'))
    ->name('check_uptime:laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();

Schedule::job(new CheckUptime('https://vapor.laravel.com'))
    ->name('check_uptime:vapor.laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();
```

마찬가지로 스케줄된 클로저를 하나의 서버에서 실행하려면 이름을 지정해야 합니다.

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업
기본적으로 같은 시간에 예약된 여러 작업은 `schedule` 메서드에 정의된 순서에 따라 순차적으로 실행됩니다. 오래 실행되는 작업이 있다면, 그 뒤의 작업들이 예상보다 훨씬 늦게 시작될 수 있습니다. 작업을 백그라운드에서 실행하여 모두 동시에 실행되도록 하려면 `runInBackground` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command` 및 `exec` 메서드로 작업을 예약할 때만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지 관리 모드

애플리케이션이 [유지 관리 모드](/docs/13.x/configuration#maintenance-mode)에 있으면 애플리케이션의 예약 작업은 실행되지 않습니다. 서버에서 아직 완료되지 않은 유지 관리 작업을 수행하는 동안 예약 작업이 방해되지 않도록 하기 위해서입니다. 하지만 유지 관리 모드에서도 작업을 강제로 실행하고 싶다면, 작업을 정의할 때 `evenInMaintenanceMode` 메서드를 호출할 수 있습니다.

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="pausing-scheduled-tasks"></a>
### 예약 작업 일시 중지

배포된 코드를 변경하지 않고도 `schedule:pause` Artisan 명령어를 사용하여 예약 작업 처리를 일시적으로 중지할 수 있습니다.

```shell
php artisan schedule:pause
```

스케줄러가 일시 중지된 동안에는 어떤 예약 작업도 실행되지 않습니다. `schedule:continue` 명령어를 사용하여 예약 작업 처리를 다시 시작할 수 있습니다.

```shell
php artisan schedule:continue
```

스케줄러가 일시 중지된 상태에서도 특정 작업이 계속 실행되어야 한다면, `evenWhenPaused` 메서드로 해당 작업을 표시할 수 있습니다.

```php
Schedule::command('emails:send')->evenWhenPaused();
```

<a name="schedule-groups"></a>
### 스케줄 그룹

비슷한 설정을 가진 여러 예약 작업을 정의할 때, 각 작업마다 같은 설정을 반복하지 않도록 Laravel의 작업 그룹화 기능을 사용할 수 있습니다. 작업을 그룹화하면 코드가 단순해지고 관련 작업 간의 일관성을 유지할 수 있습니다.

예약 작업 그룹을 만들려면 원하는 작업 설정 메서드들을 호출한 뒤 `group` 메서드를 호출합니다. `group` 메서드는 지정된 설정을 공유하는 작업을 정의하는 클로저를 인수로 받습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::daily()
    ->onOneServer()
    ->timezone('America/New_York')
    ->group(function () {
        Schedule::command('emails:send --force');
        Schedule::command('emails:prune');
    });
```

<a name="running-the-scheduler"></a>
## 스케줄러 실행 (Running the Scheduler)

이제 예약 작업을 정의하는 방법을 배웠으므로, 서버에서 실제로 이를 실행하는 방법을 살펴보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가하고, 서버의 현재 시간을 기준으로 해당 작업을 실행해야 하는지 판단합니다.

따라서 Laravel 스케줄러를 사용할 때는 서버에 cron 설정 항목을 하나만 추가하면 됩니다. 이 항목은 매분 `schedule:run` 명령어를 실행합니다. 서버에 cron 항목을 추가하는 방법을 모른다면, 예약 작업 실행을 대신 관리해 줄 수 있는 [Laravel Cloud](https://cloud.laravel.com) 같은 관리형 플랫폼을 사용하는 것도 고려해 보십시오.

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 예약 작업

대부분의 운영체제에서 cron 작업은 최대 1분에 한 번만 실행되도록 제한됩니다. 하지만 Laravel 스케줄러를 사용하면 작업을 더 짧은 간격으로, 심지어 1초에 한 번까지도 실행되도록 예약할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

애플리케이션 안에 1분 미만 작업이 정의되어 있으면, `schedule:run` 명령어는 즉시 종료되지 않고 현재 분이 끝날 때까지 계속 실행됩니다. 이를 통해 해당 분 동안 필요한 모든 1분 미만 작업을 호출할 수 있습니다.

예상보다 오래 걸리는 1분 미만 작업은 이후의 1분 미만 작업 실행을 지연시킬 수 있습니다. 따라서 모든 1분 미만 작업은 실제 작업 처리를 큐 작업이나 백그라운드 명령어에 맡기는 것이 좋습니다.

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 중단

1분 미만 작업이 정의되어 있으면 `schedule:run` 명령어는 호출된 해당 1분 동안 계속 실행됩니다. 따라서 애플리케이션을 배포할 때 이 명령어를 중단해야 할 때가 있습니다. 그렇지 않으면 이미 실행 중인 `schedule:run` 명령어 인스턴스가 현재 분이 끝날 때까지 이전에 배포된 애플리케이션 코드를 계속 사용하게 됩니다.

진행 중인 `schedule:run` 호출을 중단하려면 애플리케이션 배포 스크립트에 `schedule:interrupt` 명령어를 추가할 수 있습니다. 이 명령어는 애플리케이션 배포가 완료된 뒤 호출해야 합니다.

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행

일반적으로 로컬 개발 머신에는 스케줄러 cron 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 실행되며, 명령어를 종료할 때까지 매분 스케줄러를 호출합니다. 1분 미만 작업이 정의되어 있으면, 스케줄러는 각 분 안에서 계속 실행되며 해당 작업들을 처리합니다.

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 (Task Output)

Laravel 스케줄러는 예약 작업에서 생성된 출력을 다루기 위한 편리한 메서드를 여러 가지 제공합니다. 먼저 `sendOutputTo` 메서드를 사용하면 나중에 확인할 수 있도록 출력을 파일로 보낼 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

출력을 지정한 파일에 추가하고 싶다면 `appendOutputTo` 메서드를 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면 원하는 이메일 주소로 출력을 이메일로 보낼 수 있습니다. 작업의 출력을 이메일로 보내기 전에 Laravel의 [이메일 서비스](/docs/13.x/mail)를 설정해야 합니다.

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료된 경우에만 출력을 이메일로 보내고 싶다면 `emailOutputOnFailure` 메서드를 사용하십시오.

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 및 `exec` 메서드에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 훅 (Task Hooks)

`before` 및 `after` 메서드를 사용하면 예약 작업이 실행되기 전과 실행된 후에 실행할 코드를 지정할 수 있습니다.

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // The task is about to execute...
    })
    ->after(function () {
        // The task has executed...
    });
```

`onSuccess` 및 `onFailure` 메서드를 사용하면 예약 작업이 성공하거나 실패했을 때 실행할 코드를 지정할 수 있습니다. 실패는 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료되었음을 의미합니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // The task succeeded...
    })
    ->onFailure(function () {
        // The task failed...
    });
```

명령어에서 출력이 제공되는 경우, 훅 클로저 정의의 `$output` 인수에 `Illuminate\Support\Stringable` 인스턴스를 타입 힌트로 지정하여 `after`, `onSuccess`, `onFailure` 훅에서 해당 출력에 접근할 수 있습니다.

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // The task succeeded...
    })
    ->onFailure(function (Stringable $output) {
        // The task failed...
    });
```

<a name="pinging-urls"></a>
#### URL에 ping 보내기

`pingBefore` 및 `thenPing` 메서드를 사용하면 스케줄러가 작업 실행 전이나 실행 후에 지정한 URL로 자동으로 ping 요청을 보낼 수 있습니다. 이 메서드는 [Envoyer](https://envoyer.io) 같은 외부 서비스에 예약 작업이 시작되었거나 실행이 완료되었음을 알릴 때 유용합니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess` 및 `pingOnFailure` 메서드는 작업이 성공하거나 실패한 경우에만 지정한 URL로 ping 요청을 보내는 데 사용할 수 있습니다. 실패는 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료되었음을 의미합니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 지정한 조건이 `true`인 경우에만 지정한 URL로 ping 요청을 보내는 데 사용할 수 있습니다.

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBeforeIf($condition, $url)
    ->thenPingIf($condition, $url);

Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccessIf($condition, $successUrl)
    ->pingOnFailureIf($condition, $failureUrl);
```

<a name="events"></a>
## 이벤트 (Events)

Laravel은 스케줄링 과정에서 다양한 [이벤트](/docs/13.x/events)를 디스패치합니다. 다음 이벤트에 대해 [리스너를 정의](/docs/13.x/events)할 수 있습니다.

<div class="overflow-auto">

| 이벤트 이름                                                 |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

</div>
