# 작업 스케줄링 (Task Scheduling)

- [소개](#introduction)
- [스케줄 정의](#defining-schedules)
    - [Artisan 명령어 스케줄링](#scheduling-artisan-commands)
    - [큐 작업 스케줄링](#scheduling-queued-jobs)
    - [셸 명령어 스케줄링](#scheduling-shell-commands)
    - [스케줄 빈도 옵션](#schedule-frequency-options)
    - [타임존](#timezones)
    - [작업 중첩 방지](#preventing-task-overlaps)
    - [단일 서버에서 작업 실행](#running-tasks-on-one-server)
    - [백그라운드 작업](#background-tasks)
    - [메인터넌스 모드](#maintenance-mode)
    - [스케줄 그룹](#schedule-groups)
- [스케줄러 실행](#running-the-scheduler)
    - [1분 미만 간격 작업 스케줄링](#sub-minute-scheduled-tasks)
    - [로컬에서 스케줄러 실행](#running-the-scheduler-locally)
- [작업 출력](#task-output)
- [작업 훅(Hook)](#task-hooks)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

예전에는 서버에서 실행할 각 작업마다 크론(cron) 설정을 직접 작성했을 것입니다. 하지만 이 방식은 곧 번거로워집니다. 작업 스케줄이 더 이상 소스 관리 하에 있지 않게 되고, 기존 크론 항목을 확인하거나 새로운 작업을 추가하려면 서버에 SSH로 접속해야 하기 때문입니다.

Laravel의 명령어 스케줄러는 서버의 예약 작업을 더욱 손쉽게 관리할 수 있도록 새로운 방식을 제공합니다. 이 스케줄러를 사용하면, Laravel 애플리케이션 내에서 명령어 스케줄을 유연하게 정의할 수 있습니다. 스케줄러를 사용할 때는 서버에 단 하나의 크론 항목만 등록하면 되며, 실제 예약 작업들은 애플리케이션의 `routes/console.php` 파일에서 보통 정의합니다.

<a name="defining-schedules"></a>
## 스케줄 정의 (Defining Schedules)

모든 예약 작업은 애플리케이션의 `routes/console.php` 파일에서 정의할 수 있습니다. 우선 간단한 예제를 살펴보겠습니다. 아래 예제에서는 매일 자정마다 호출되는 클로저를 예약하고, 이 클로저에서 데이터베이스 쿼리를 실행하여 테이블을 비웁니다:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

클로저를 사용한 예약 외에도, [호출 가능한 객체(invokable objects)](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)도 예약할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 가진 간단한 PHP 클래스입니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```

만약 `routes/console.php` 파일을 명령어 정의로만 사용하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용하여 예약 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 전달하는 클로저를 인자로 받습니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

예약된 작업과 다음 실행 예정 시간을 한눈에 확인하고 싶다면 `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan 명령어 스케줄링

클로저뿐 아니라, [Artisan 명령어](/docs/12.x/artisan)와 시스템 명령어도 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용해 명령어의 이름 또는 클래스명을 전달하여 Artisan 명령어를 스케줄링할 수 있습니다.

명령어의 클래스명을 사용하여 Artisan 명령어를 예약할 때는, 명령어 실행 시에 제공할 추가 커맨드 라인 인수들을 배열 형태로 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
#### 클로저 기반 Artisan 명령어 스케줄링

클로저로 정의된 Artisan 명령어를 예약하려면, 명령어 정의 후 바로 스케줄 관련 메서드를 체이닝하세요:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

클로저 명령어에 인수를 전달해야 한다면, `schedule` 메서드에 인수 배열을 넘겨 사용할 수 있습니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
### 큐 작업 스케줄링

`job` 메서드를 사용하면 [큐 작업(queued job)](/docs/12.x/queues)을 쉽게 예약할 수 있습니다. 이 방법을 이용하면, 작업을 큐에 넣기 위해 클로저로 감싸는 번거로움 없이 간편하게 예약할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

추가로 두 번째와 세 번째 인수로 큐 이름과 큐 연결명을 지정할 수 있습니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// "heartbeats" 큐와 "sqs" 연결을 사용하여 작업을 디스패치
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
### 셸 명령어 스케줄링

`exec` 메서드는 운영체제에 명령어를 직접 실행시킬 수 있게 해줍니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 스케줄 빈도 옵션

앞에서 특정 주기로 작업을 실행하도록 설정하는 방법을 몇 가지 살펴보았습니다. 하지만 더욱 다양한 예약주기 메서드들이 존재합니다:

<div class="overflow-auto">

| 메서드                                  | 설명                                                      |
| -------------------------------------- | --------------------------------------------------------- |
| `->cron('* * * * *');`                 | 커스텀 크론 스케줄로 작업을 실행합니다.                       |
| `->everySecond();`                     | 매초마다 작업을 실행합니다.                                   |
| `->everyTwoSeconds();`                 | 2초마다 작업을 실행합니다.                                    |
| `->everyFiveSeconds();`                | 5초마다 작업을 실행합니다.                                    |
| `->everyTenSeconds();`                 | 10초마다 작업을 실행합니다.                                   |
| `->everyFifteenSeconds();`             | 15초마다 작업을 실행합니다.                                   |
| `->everyTwentySeconds();`              | 20초마다 작업을 실행합니다.                                   |
| `->everyThirtySeconds();`              | 30초마다 작업을 실행합니다.                                   |
| `->everyMinute();`                     | 매 분마다 작업을 실행합니다.                                   |
| `->everyTwoMinutes();`                 | 2분마다 작업을 실행합니다.                                    |
| `->everyThreeMinutes();`               | 3분마다 작업을 실행합니다.                                    |
| `->everyFourMinutes();`                | 4분마다 작업을 실행합니다.                                    |
| `->everyFiveMinutes();`                | 5분마다 작업을 실행합니다.                                    |
| `->everyTenMinutes();`                 | 10분마다 작업을 실행합니다.                                   |
| `->everyFifteenMinutes();`             | 15분마다 작업을 실행합니다.                                   |
| `->everyThirtyMinutes();`              | 30분마다 작업을 실행합니다.                                   |
| `->hourly();`                          | 1시간마다 작업을 실행합니다.                                   |
| `->hourlyAt(17);`                      | 매 시간 17분에 작업을 실행합니다.                              |
| `->everyOddHour($minutes = 0);`        | 홀수 시간마다 작업을 실행합니다.                               |
| `->everyTwoHours($minutes = 0);`       | 2시간마다 작업을 실행합니다.                                   |
| `->everyThreeHours($minutes = 0);`     | 3시간마다 작업을 실행합니다.                                   |
| `->everyFourHours($minutes = 0);`      | 4시간마다 작업을 실행합니다.                                   |
| `->everySixHours($minutes = 0);`       | 6시간마다 작업을 실행합니다.                                   |
| `->daily();`                           | 매일 자정에 작업을 실행합니다.                                 |
| `->dailyAt('13:00');`                  | 매일 13:00에 작업을 실행합니다.                               |
| `->twiceDaily(1, 13);`                 | 매일 1:00, 13:00에 작업을 실행합니다.                          |
| `->twiceDailyAt(1, 13, 15);`           | 매일 1:15, 13:15에 작업을 실행합니다.                          |
| `->daysOfMonth([1, 10, 20]);`          | 매월 지정된 날짜에 작업을 실행합니다.                           |
| `->weekly();`                          | 매주 일요일 00:00에 작업을 실행합니다.                          |
| `->weeklyOn(1, '8:00');`               | 매주 월요일 8:00에 작업을 실행합니다.                           |
| `->monthly();`                         | 매월 1일 00:00에 작업을 실행합니다.                             |
| `->monthlyOn(4, '15:00');`             | 매월 4일 15:00에 작업을 실행합니다.                             |
| `->twiceMonthly(1, 16, '13:00');`      | 매월 1일, 16일 13:00에 작업을 실행합니다.                        |
| `->lastDayOfMonth('15:00');`           | 매월 마지막 날 15:00에 작업을 실행합니다.                        |
| `->quarterly();`                       | 분기 첫날 00:00에 작업을 실행합니다.                             |
| `->quarterlyOn(4, '14:00');`           | 매 분기 4일 14:00에 작업을 실행합니다.                           |
| `->yearly();`                          | 매년 1월 1일 00:00에 작업을 실행합니다.                          |
| `->yearlyOn(6, 1, '17:00');`           | 매년 6월 1일 17:00에 작업을 실행합니다.                          |
| `->timezone('America/New_York');`      | 작업의 타임존을 설정합니다.                                      |

</div>

이러한 메서드들은 추가 제약 조건과 조합하여, 특정 요일에만 실행되는 세밀한 스케줄을 만들 수 있습니다. 예를 들어, 매주 월요일에 명령어가 실행되도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// 매주 월요일 오후 1시에 한 번 실행
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// 평일 08:00~17:00 시간대에 매시간 실행
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```

아래는 추가적인 스케줄 제약 조건의 목록입니다:

<div class="overflow-auto">

| 메서드                                       | 설명                                                 |
| -------------------------------------------- | --------------------------------------------------- |
| `->weekdays();`                              | 평일(월~금요일)에만 작업을 제한합니다.                 |
| `->weekends();`                              | 주말(토,일)에만 작업을 제한합니다.                    |
| `->sundays();`                               | 일요일에만 작업을 제한합니다.                         |
| `->mondays();`                               | 월요일에만 작업을 제한합니다.                         |
| `->tuesdays();`                              | 화요일에만 작업을 제한합니다.                         |
| `->wednesdays();`                            | 수요일에만 작업을 제한합니다.                         |
| `->thursdays();`                             | 목요일에만 작업을 제한합니다.                         |
| `->fridays();`                               | 금요일에만 작업을 제한합니다.                         |
| `->saturdays();`                             | 토요일에만 작업을 제한합니다.                         |
| `->days(array\|mixed);`                      | 지정한 요일에만 작업을 제한합니다.                     |
| `->between($startTime, $endTime);`           | 시작~종료 시간 사이에만 작업을 실행합니다.             |
| `->unlessBetween($startTime, $endTime);`     | 지정 시간대에는 작업을 실행하지 않습니다.              |
| `->when(Closure);`                           | 조건 클로저가 true인 경우에만 작업을 실행합니다.        |
| `->environments($env);`                      | 지정한 환경에서만 작업을 실행합니다.                   |

</div>

<a name="day-constraints"></a>
#### 요일 제약

`days` 메서드는 특정 요일에만 작업이 실행되도록 설정할 때 사용합니다. 예를 들어, 매주 일요일과 수요일에 매시간 명령어를 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

또한, 작업이 실행될 요일을 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스의 상수를 사용할 수도 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
#### 시간대 제약

`between` 메서드는 작업 실행 시간을 특정 시간대로 제한할 때 사용합니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

반대로, `unlessBetween` 메서드는 특정 시간대에는 작업을 제외시키는 방법입니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
#### 조건(Truth Test) 제약

`when` 메서드는 주어진 조건(클로저의 반환값이 true)일 때만 작업을 실행하도록 제어할 수 있습니다. 다른 제약 조건에 걸리지 않는다면, 조건이 true이면 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

`skip` 메서드는 `when`의 반대 개념으로, 클로저가 true를 반환하면 예약된 작업을 실행하지 않습니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

`when` 메서드를 연속적으로 체이닝하면, 모든 조건이 true를 반환할 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
#### 환경(Environment) 제약

`environments` 메서드는 지정된 환경에서만 작업을 실행하게 하는 방법입니다. 환경은 [APP_ENV 환경 변수](/docs/12.x/configuration#environment-configuration)로 정의됩니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
### 타임존

`timezone` 메서드를 사용하면, 예약 작업이 특정 타임존 기준으로 실행되도록 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

만약 모든 예약 작업에 동일한 타임존을 반복적으로 부여한다면, 애플리케이션의 `app` 설정 파일에서 `schedule_timezone` 옵션을 지정할 수 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 타임존은 서머타임(일광 절약 시간제)을 사용합니다. 이로 인한 변화가 있을 때 예약된 작업이 한 번 더 실행되거나 아예 실행되지 않을 수 있습니다. 따라서 가능하면 타임존 스케줄링 사용을 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
### 작업 중첩 방지

기본적으로 예약한 작업은 이전 실행 인스턴스가 아직 완료되지 않은 경우에도 계속 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

위 예제는 `emails:send` [Artisan 명령어](/docs/12.x/artisan)를 매분마다 실행하되, 이전 실행이 끝나지 않았다면 새로 실행하지 않습니다. 이 메서드는 실행 시간이 불규칙한 작업의 중첩 실행을 막아주어 유용합니다.

필요하다면, 중첩 방지 락(lock)이 만료되는 시간(분 단위)을 지정할 수도 있습니다. 기본값은 24시간입니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```

`withoutOverlapping` 메서드는 내부적으로 애플리케이션의 [캐시](/docs/12.x/cache)를 활용해 락을 얻습니다. 예상치 못한 서버 문제로 작업이 중단되어 락이 남았다면, `schedule:clear-cache` Artisan 명령어로 이 락을 삭제할 수 있습니다. 보통 작업이 ‘멈춘’ 특이한 경우에 한해서만 필요합니다.

<a name="running-tasks-on-one-server"></a>
### 단일 서버에서 작업 실행

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis`여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

스케줄러가 여러 대의 서버에서 실행 중일 때, 예약 작업을 한 서버에서만 실행하도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤마다 새 보고서를 생성하는 예약 작업이 있고, 세 대의 워커 서버에서 각각 스케줄러가 실행된다면, 세 서버 모두에서 동일 작업이 실행되어 중복 보고서가 생성될 수 있습니다.

이럴 때 `onOneServer` 메서드를 사용하면, 먼저 락을 획득한 서버만 작업을 실행하게 됩니다(원자적 락):

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

스케줄러가 단일 서버 작업에 사용할 캐시 스토어를 지정하고 싶다면 `useCache` 메서드를 사용할 수 있습니다:

```php
Schedule::useCache('database');
```

<a name="naming-unique-jobs"></a>
#### 단일 서버 작업 이름 지정

매개변수가 다른 동일한 작업을 여러 번 예약하면서도 각각을 단일 서버에서만 실행하고 싶을 때는, 각 스케줄 정의에 고유한 이름을 `name` 메서드로 부여하세요:

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

마찬가지로, 클로저로 예약한 작업도 단일 서버 실행을 원한다면 이름을 반드시 지정해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로 동시에 예약된 여러 작업은 `schedule` 메서드에 정의한 순서대로, 순차적으로 실행됩니다. 장시간 실행되는 작업이 있다면, 이후 작업이 예정보다 늦게 시작될 수 있습니다. 모든 작업을 동시에 실행하고 싶다면, `runInBackground` 메서드를 사용하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command`와 `exec` 메서드를 통해 예약된 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 메인터넌스 모드

애플리케이션이 [메인터넌스 모드](/docs/12.x/configuration#maintenance-mode)인 경우, 예약 작업은 실행되지 않습니다. 이는 메인터넌스 도중 예약 작업이 서버의 상태에 영향을 끼치는 것을 방지하기 위한 조치입니다. 그러나, 메인터넌스 모드 중에도 특정 작업을 강제로 실행하려면 `evenInMaintenanceMode` 메서드를 사용할 수 있습니다:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
### 스케줄 그룹

비슷한 설정을 가진 여러 예약 작업을 정의할 때는, 라라벨의 작업 그룹 기능을 사용해 같은 설정을 반복 입력하지 않고 코드를 간결하게 작성할 수 있습니다. 그룹화로 연관된 작업들의 일관성을 유지할 수 있습니다.

예약 작업 그룹을 만들려면, 먼저 원하는 작업 설정 메서드들을 호출한 후, `group` 메서드 뒤에 그 설정을 공유할 작업들을 정의하는 클로저를 넘기세요:

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

이제 예약 작업을 정의하는 방법을 배웠으니, 실제 서버에서 어떻게 스케줄러를 실행하는지 알아보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가하여 현재 실행되어야 하는지 판단합니다.

따라서, Laravel 스케줄러를 사용할 때는 서버에 단 하나의 크론 항목만 등록하면 되고, 이 항목에서 매분마다 `schedule:run` 명령어를 실행하면 됩니다. 만약 크론 항목을 직접 설정하는 법이 어렵다면, [Laravel Cloud](https://cloud.laravel.com)와 같은 관리형 플랫폼에서 예약 작업 실행을 쉽게 관리할 수 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 간격 작업 스케줄링

대부분의 운영체제에서 크론 작업은 1분에 한 번만 실행 가능합니다. 그러나 라라벨 스케줄러는 1초 단위 등, 그보다 더 짧은 간격으로 작업을 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

애플리케이션 내에 1분 미만 간격 작업이 정의되면, `schedule:run` 명령어는 실행 후 즉시 종료되지 않고 해당 분이 끝날 때까지 계속 동작합니다. 이를 통해 매분 내내 모든 짧은 주기의 예약 작업이 올바르게 수행됩니다.

예상보다 시간이 오래 걸리는 1분 미만 작업으로 이후 작업 실행이 지연될 수 있으므로, 이러한 경우에는 실제 처리는 큐 작업 디스패치나 백그라운드 명령으로 분리하는 것이 좋습니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 중단

1분 미만 작업이 정의되어 있으면, `schedule:run` 명령어는 전체 분마다 계속 실행됩니다. 배포(deploy) 중에는 이미 실행 중인 schedule:run 인스턴스를 중단해야 할 수도 있습니다. 그렇지 않으면 이미 실행 중이던 명령어가 이전 배포된 코드로 계속 실행될 수 있습니다.

이 경우, 배포가 끝난 뒤에 `schedule:interrupt` 명령어를 배포 스크립트에 추가해서 실행 중인 명령어를 중단할 수 있습니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행

보통 로컬 개발 환경에는 크론 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 실행되며 사용자가 중단하기 전까지 매분마다 스케줄러를 실행합니다. 1분 미만 작업이 있을 때도 각각 해당 시간 내에서 반복 실행됩니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## 작업 출력 (Task Output)

라라벨 스케줄러는 예약 작업의 출력 결과를 다루기 위한 다양한 편의 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드를 사용해 출력 결과를 파일로 남길 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

파일에 내용을 이어붙이고 싶다면, `appendOutputTo` 메서드를 사용하세요:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

`emailOutputTo` 메서드를 사용하면 출력 결과를 지정한 이메일 주소로 보낼 수도 있습니다. 이 기능을 사용하기 전에 반드시 라라벨의 [메일 서비스](/docs/12.x/mail)를 설정해야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

예약 Artisan 명령어나 시스템 명령어가 종료 코드가 0이 아닌 경우에만 이메일을 받고 싶다면, `emailOutputOnFailure` 메서드를 사용하세요:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo`는 `command` 및 `exec` 메서드로 예약된 작업에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
## 작업 훅(Hook) (Task Hooks)

`before`와 `after` 메서드를 이용하면, 예약 작업 실행 전/후에 별도 코드를 실행시킬 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // 작업이 곧 실행됩니다...
    })
    ->after(function () {
        // 작업이 실행 완료되었습니다...
    });
```

`onSuccess`와 `onFailure` 메서드는 작업이 성공적으로 완료되거나 실패했을 때(실패: 종료 코드가 0이 아님)에 실행할 코드를 등록할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // 작업이 성공적으로 완료됨
    })
    ->onFailure(function () {
        // 작업이 실패함
    });
```

만약 명령어의 출력 결과를 활용하고 싶다면, 훅의 클로저에서 `Illuminate\Support\Stringable` 타입을 `$output` 인수로 받도록 선언할 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // 작업이 성공적으로 완료됨
    })
    ->onFailure(function (Stringable $output) {
        // 작업이 실패함
    });
```

<a name="pinging-urls"></a>
#### URL 핑(Ping) 보내기

`pingBefore`와 `thenPing` 메서드를 활용하면 작업 실행 전후에 특정 URL로 자동으로 핑(ping)을 보낼 수 있습니다. 이 기능은 [Envoyer](https://envoyer.io) 같은 외부 서비스에 예약 작업의 시작/종료를 알릴 때 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

`pingOnSuccess`와 `pingOnFailure`는 작업 성공 시 또는 실패 시에만 지정된 URL로 핑을 보냅니다(실패는 종료 코드가 0이 아닐 때입니다):

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드는 특정 조건이 true일 때만 핑을 보냅니다:

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

라라벨은 스케줄링 과정에서 다양한 [이벤트](/docs/12.x/events)를 발생시킵니다. 아래 이벤트들에 대해 [리스너를 정의](/docs/12.x/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                                  |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

</div>
