<!-- # Task Scheduling -->
# Task Scheduling

- [Introduction](#introduction)
- [Defining Schedules](#defining-schedules)
    - [Scheduling Artisan Commands](#scheduling-artisan-commands)
    - [Scheduling Queued Jobs](#scheduling-queued-jobs)
    - [Scheduling Shell Commands](#scheduling-shell-commands)
    - [Schedule Frequency Options](#schedule-frequency-options)
    - [Timezones](#timezones)
    - [Preventing Task Overlaps](#preventing-task-overlaps)
    - [Running Tasks on One Server](#running-tasks-on-one-server)
    - [Background Tasks](#background-tasks)
    - [Maintenance Mode](#maintenance-mode)
    - [Schedule Groups](#schedule-groups)
- [Running the Scheduler](#running-the-scheduler)
    - [Sub-Minute Scheduled Tasks](#sub-minute-scheduled-tasks)
    - [Running the Scheduler Locally](#running-the-scheduler-locally)
- [Task Output](#task-output)
- [Task Hooks](#task-hooks)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In the past, you may have written a cron configuration entry for each task you needed to schedule on your server. However, this can quickly become a pain because your task schedule is no longer in source control and you must SSH into your server to view your existing cron entries or add additional entries. -->
과거에는 서버에서 예약해야 하는 각 작업마다 cron 설정 항목을 따로 작성해야 했을 것입니다. 하지만 이렇게 하면 작업 스케줄이 버전 관리 대상에서 벗어나 관리가 어려워지고, 기존 cron 항목을 확인하거나 새로운 항목을 추가하려면 서버에 SSH로 접속해야 하는 번거로움이 생깁니다.

<!-- Laravel's command scheduler offers a fresh approach to managing scheduled tasks on your server. The scheduler allows you to fluently and expressively define your command schedule within your Laravel application itself. When using the scheduler, only a single cron entry is needed on your server. Your task schedule is typically defined in your application's `routes/console.php` file. -->
Laravel의 명령어 스케줄러는 서버의 예약 작업을 더 쉽게 관리할 수 있도록 해줍니다. 스케줄러를 사용하면 Laravel 애플리케이션 내부에서 손쉽게 예약 명령어를 정의할 수 있습니다. 이때 서버에는 오직 하나의 cron 항목만 필요합니다. 일반적으로 예약 작업 스케줄은 애플리케이션의 `routes/console.php` 파일에서 정의합니다.

<a name="defining-schedules"></a>
<!-- ## Defining Schedules -->
## Defining Schedules

<!-- You may define all of your scheduled tasks in your application's `routes/console.php` file. To get started, let's take a look at an example. In this example, we will schedule a closure to be called every day at midnight. Within the closure we will execute a database query to clear a table: -->
애플리케이션의 `routes/console.php` 파일에서 모든 예약 작업을 정의할 수 있습니다. 우선, 다음과 같은 간단한 예시를 살펴보겠습니다. 이 예시에서는 클로저를 매일 0시에 실행해서 데이터베이스 쿼리를 수행하여 테이블을 비우는 작업을 예약합니다:

```
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```

<!-- In addition to scheduling using closures, you may also schedule [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke). Invokable objects are simple PHP classes that contain an `__invoke` method: -->
클로저를 이용한 예약뿐 아니라, [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)도 스케줄링할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 포함하는 단순 PHP 클래스를 말합니다:

```
Schedule::call(new DeleteRecentUsers)->daily();
```

<!-- If you prefer to reserve your `routes/console.php` file for command definitions only, you may use the `withSchedule` method in your application's `bootstrap/app.php` file to define your scheduled tasks. This method accepts a closure that receives an instance of the scheduler: -->
만약 `routes/console.php` 파일을 명령어 정의 전용으로만 사용하고 싶을 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용해 예약 작업을 정의할 수 있습니다. 이 메서드는 스케줄러 인스턴스를 받는 클로저를 인자로 제공합니다:

```
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```

<!-- If you would like to view an overview of your scheduled tasks and the next time they are scheduled to run, you may use the `schedule:list` Artisan command: -->
정의된 예약 작업의 개요와 다음 실행 예정 시각을 확인하려면 `schedule:list` Artisan 명령어를 사용할 수 있습니다:

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
<!-- ### Scheduling Artisan Commands -->
### Scheduling Artisan Commands

<!-- In addition to scheduling closures, you may also schedule [Artisan commands](/docs/11.x/artisan) and system commands. For example, you may use the `command` method to schedule an Artisan command using either the command's name or class. -->
클로저 외에도 [Artisan commands](/docs/11.x/artisan)와 시스템 명령어도 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용하여 명령어의 문자열 이름 또는 클래스명으로 Artisan 명령어를 스케줄링할 수 있습니다.

<!-- When scheduling Artisan commands using the command's class name, you may pass an array of additional command-line arguments that should be provided to the command when it is invoked: -->
클래스명을 사용해 Artisan 명령어를 예약할 때는 명령어 실행 시 전달할 추가 명령줄 인수를 배열로 지정할 수 있습니다:

```
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-artisan-closure-commands"></a>
<!-- #### Scheduling Artisan Closure Commands -->
#### Scheduling Artisan Closure Commands

<!-- If you want to schedule an Artisan command defined by a closure, you may chain the scheduling related methods after the command's definition: -->
클로저로 정의된 Artisan 명령어를 예약하고 싶다면, 명령어 정의 부분 바로 뒤에 예약 관련 메서드를 연결해서 사용할 수 있습니다:

```
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```

<!-- If you need to pass arguments to the closure command, you may provide them to the `schedule` method: -->
클로저 명령어에 인수를 전달해야 할 경우, `schedule` 메서드에 인수 배열을 넘겨주면 됩니다:

```
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
<!-- ### Scheduling Queued Jobs -->
### Scheduling Queued Jobs

<!-- The `job` method may be used to schedule a [queued job](/docs/11.x/queues). This method provides a convenient way to schedule queued jobs without using the `call` method to define closures to queue the job: -->
`job` 메서드를 사용하면 [queued job](/docs/11.x/queues)을 예약할 수 있습니다. 이 메서드는 `call` 메서드로 클로저를 정의해 큐 작업을 디스패치하지 않고도 직접 큐 작업을 예약하는 편리한 방법을 제공합니다:

```
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```

<!-- Optional second and third arguments may be provided to the `job` method which specifies the queue name and queue connection that should be used to queue the job: -->
`job` 메서드에는 선택적으로 두 번째와 세 번째 인자를 지정해 작업이 실행될 큐의 이름과 연결(connection)을 설정할 수 있습니다:

```
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
<!-- ### Scheduling Shell Commands -->
### Scheduling Shell Commands

<!-- The `exec` method may be used to issue a command to the operating system: -->
`exec` 메서드를 사용하면 운영체제에 직접 명령을 실행할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
<!-- ### Schedule Frequency Options -->
### Schedule Frequency Options

<!-- We've already seen a few examples of how you may configure a task to run at specified intervals. However, there are many more task schedule frequencies that you may assign to a task: -->
지금까지 작업을 정해진 간격으로 실행하도록 예약하는 몇 가지 방법을 살펴보았습니다. 하지만, 작업 예약 주기는 이외에도 다양하게 지정할 수 있습니다:

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 메서드                              | 설명                                                         |
| ---------------------------------- | ----------------------------------------------------------- |
| `->cron('* * * * *');`             | 커스텀 cron 주기로 작업을 실행합니다.                        |
| `->everySecond();`                 | 매초마다 작업을 실행합니다.                                  |
| `->everyTwoSeconds();`             | 2초마다 작업을 실행합니다.                                   |
| `->everyFiveSeconds();`            | 5초마다 작업을 실행합니다.                                   |
| `->everyTenSeconds();`             | 10초마다 작업을 실행합니다.                                  |
| `->everyFifteenSeconds();`         | 15초마다 작업을 실행합니다.                                  |
| `->everyTwentySeconds();`          | 20초마다 작업을 실행합니다.                                  |
| `->everyThirtySeconds();`          | 30초마다 작업을 실행합니다.                                  |
| `->everyMinute();`                 | 1분마다 작업을 실행합니다.                                   |
| `->everyTwoMinutes();`             | 2분마다 작업을 실행합니다.                                   |
| `->everyThreeMinutes();`           | 3분마다 작업을 실행합니다.                                   |
| `->everyFourMinutes();`            | 4분마다 작업을 실행합니다.                                   |
| `->everyFiveMinutes();`            | 5분마다 작업을 실행합니다.                                   |
| `->everyTenMinutes();`             | 10분마다 작업을 실행합니다.                                  |
| `->everyFifteenMinutes();`         | 15분마다 작업을 실행합니다.                                  |
| `->everyThirtyMinutes();`          | 30분마다 작업을 실행합니다.                                  |
| `->hourly();`                      | 1시간마다 작업을 실행합니다.                                 |
| `->hourlyAt(17);`                  | 매 시각, 17분에 작업을 실행합니다.                           |
| `->everyOddHour($minutes = 0);`    | 홀수 시간마다 작업을 실행합니다.                             |
| `->everyTwoHours($minutes = 0);`   | 2시간마다 작업을 실행합니다.                                 |
| `->everyThreeHours($minutes = 0);` | 3시간마다 작업을 실행합니다.                                 |
| `->everyFourHours($minutes = 0);`  | 4시간마다 작업을 실행합니다.                                 |
| `->everySixHours($minutes = 0);`   | 6시간마다 작업을 실행합니다.                                 |
| `->daily();`                       | 매일 0시에 작업을 실행합니다.                                |
| `->dailyAt('13:00');`              | 매일 13:00에 작업을 실행합니다.                              |
| `->twiceDaily(1, 13);`             | 매일 1:00, 13:00에 작업을 실행합니다.                        |
| `->twiceDailyAt(1, 13, 15);`       | 매일 1:15, 13:15에 작업을 실행합니다.                        |
| `->weekly();`                      | 매주 일요일 0:00에 작업을 실행합니다.                        |
| `->weeklyOn(1, '8:00');`           | 매주 월요일 8:00에 작업을 실행합니다.                        |
| `->monthly();`                     | 매월 1일 0:00에 작업을 실행합니다.                           |
| `->monthlyOn(4, '15:00');`         | 매월 4일 15:00에 작업을 실행합니다.                          |
| `->twiceMonthly(1, 16, '13:00');`  | 매월 1일, 16일 13:00에 작업을 실행합니다.                    |
| `->lastDayOfMonth('15:00');`       | 매월 마지막 날 15:00에 작업을 실행합니다.                     |
| `->quarterly();`                   | 매 분기 첫째 날 0:00에 작업을 실행합니다.                    |
| `->quarterlyOn(4, '14:00');`       | 매 분기 4일 14:00에 작업을 실행합니다.                       |
| `->yearly();`                      | 매년 1월 1일 0:00에 작업을 실행합니다.                      |
| `->yearlyOn(6, 1, '17:00');`       | 매년 6월 1일 17:00에 작업을 실행합니다.                      |
| `->timezone('America/New_York');`  | 작업의 시간대를 지정합니다.                                  |

<!-- </div> -->
</div>

<!-- These methods may be combined with additional constraints to create even more finely tuned schedules that only run on certain days of the week. For example, you may schedule a command to run weekly on Monday: -->
이러한 메서드들은 추가 제약 조건과 결합하여 더 세밀하게 특정 주중에만 실행되는 스케줄을 구성할 수 있습니다. 예를 들어, 다음과 같이 월요일마다 명령어를 예약할 수 있습니다:

```
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

<!-- A list of additional schedule constraints may be found below: -->
아래는 사용 가능한 추가 스케줄 제약 조건 목록입니다:

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 메서드                                       | 설명                                               |
| ------------------------------------------ | ------------------------------------------------- |
| `->weekdays();`                            | 평일에만 작업을 제한적으로 실행합니다.              |
| `->weekends();`                            | 주말에만 작업을 제한적으로 실행합니다.              |
| `->sundays();`                             | 일요일에만 작업을 제한적으로 실행합니다.            |
| `->mondays();`                             | 월요일에만 작업을 제한적으로 실행합니다.            |
| `->tuesdays();`                            | 화요일에만 작업을 제한적으로 실행합니다.            |
| `->wednesdays();`                          | 수요일에만 작업을 제한적으로 실행합니다.            |
| `->thursdays();`                           | 목요일에만 작업을 제한적으로 실행합니다.            |
| `->fridays();`                             | 금요일에만 작업을 제한적으로 실행합니다.            |
| `->saturdays();`                           | 토요일에만 작업을 제한적으로 실행합니다.            |
| `->days(array\|mixed);`                    | 특정 요일에만 작업을 제한적으로 실행합니다.         |
| `->between($startTime, $endTime);`         | 지정된 시간 사이에만 작업을 실행합니다.             |
| `->unlessBetween($startTime, $endTime);`   | 지정된 시간 사이에는 작업을 실행하지 않습니다.      |
| `->when(Closure);`                         | 주어진 진위(closed) 테스트 결과에 따라 실행합니다.   |
| `->environments($env);`                    | 특정 환경에서만 작업을 실행합니다.                  |

<!-- </div> -->
</div>

<a name="day-constraints"></a>
<!-- #### Day Constraints -->
#### Day Constraints

<!-- The `days` method may be used to limit the execution of a task to specific days of the week. For example, you may schedule a command to run hourly on Sundays and Wednesdays: -->
`days` 메서드를 활용하면 특정 요일에만 작업 실행을 제한할 수 있습니다. 예를 들어, 일요일과 수요일마다 매 시간 명령어를 예약할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```

<!-- Alternatively, you may use the constants available on the `Illuminate\Console\Scheduling\Schedule` class when defining the days on which a task should run: -->
또는, 작업이 실행될 요일을 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스에서 제공하는 상수를 사용할 수도 있습니다:

```
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
<!-- #### Between Time Constraints -->
#### Between Time Constraints

<!-- The `between` method may be used to limit the execution of a task based on the time of day: -->
`between` 메서드를 사용하면 작업이 특정 시간대에만 실행되도록 제한할 수 있습니다:

```
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```

<!-- Similarly, the `unlessBetween` method can be used to exclude the execution of a task for a period of time: -->
반대로 `unlessBetween` 메서드는 특정 시간대에는 실행하지 않도록 제한합니다:

```
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
<!-- #### Truth Test Constraints -->
#### Truth Test Constraints

<!-- The `when` method may be used to limit the execution of a task based on the result of a given truth test. In other words, if the given closure returns `true`, the task will execute as long as no other constraining conditions prevent the task from running: -->
`when` 메서드는 주어진 조건을 클로저로 전달했을 때, 클로저가 `true`를 반환하면 작업이 실행되도록 제한합니다. (다른 제약 조건이 없을 때):

```
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```

<!-- The `skip` method may be seen as the inverse of `when`. If the `skip` method returns `true`, the scheduled task will not be executed: -->
`skip` 메서드는 `when`과 반대로 동작합니다. `skip` 메서드가 `true`를 반환하면 예약된 작업이 실행되지 않습니다:

```
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```

<!-- When using chained `when` methods, the scheduled command will only execute if all `when` conditions return `true`. -->
`when` 메서드를 여러 번 연결하여 사용할 수 있으며, 이 경우 모든 `when` 조건이 `true`일 때만 작업이 실행됩니다.

<a name="environment-constraints"></a>
<!-- #### Environment Constraints -->
#### Environment Constraints

<!-- The `environments` method may be used to execute tasks only on the given environments (as defined by the `APP_ENV` [environment variable](/docs/11.x/configuration#environment-configuration)): -->
`environments` 메서드는 작업이 실행될 환경(예: `APP_ENV` [environment variable](/docs/11.x/configuration#environment-configuration))을 지정할 때 사용합니다:

```
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```

<a name="timezones"></a>
<!-- ### Timezones -->
### Timezones

<!-- Using the `timezone` method, you may specify that a scheduled task's time should be interpreted within a given timezone: -->
`timezone` 메서드를 사용하면 예약 작업의 실행 시각을 특정 시간대로 해석하도록 지정할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00')
```

<!-- If you are repeatedly assigning the same timezone to all of your scheduled tasks, you can specify which timezone should be assigned to all schedules by defining a `schedule_timezone` option within your application's `app` configuration file: -->
여러 예약 작업에 계속해서 동일한 시간대를 지정하고 있다면, 애플리케이션의 `app` 설정 파일에 `schedule_timezone` 옵션을 추가하여 전체 스케줄 기본 시간대를 지정할 수도 있습니다:

```
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```

> [!WARNING]
> 일부 시간대는 일광절약시간제(DST)를 사용하니 유의해야 합니다. 일광절약시간이 변경될 경우, 예약 작업이 두 번 실행되거나 아예 실행되지 않는 문제가 발생할 수 있습니다. 이런 문제를 방지하기 위해서라면 시간대 스케줄링은 되도록 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
<!-- ### Preventing Task Overlaps -->
### Preventing Task Overlaps

<!-- By default, scheduled tasks will be run even if the previous instance of the task is still running. To prevent this, you may use the `withoutOverlapping` method: -->
기본적으로 예약 작업은 이전 인스턴스가 아직 실행 중이어도 중복 실행될 수 있습니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```

<!-- In this example, the `emails:send` [Artisan command](/docs/11.x/artisan) will be run every minute if it is not already running. The `withoutOverlapping` method is especially useful if you have tasks that vary drastically in their execution time, preventing you from predicting exactly how long a given task will take. -->
이 예시에서는 `emails:send` [Artisan command](/docs/11.x/artisan)가 이미 실행 중이지 않을 경우에만 매 분마다 실행됩니다. `withoutOverlapping` 메서드는 작업 실행 시간이 매번 크게 다를 때 유용합니다.

<!-- If needed, you may specify how many minutes must pass before the "without overlapping" lock expires. By default, the lock will expire after 24 hours: -->
필요하다면 "중복 방지" 락이 만료되기까지 대기할 시간(분 단위)을 지정할 수 있습니다. 기본적으로 이 락은 24시간 후 만료됩니다:

```
Schedule::command('emails:send')->withoutOverlapping(10);
```

<!-- Behind the scenes, the `withoutOverlapping` method utilizes your application's [cache](/docs/11.x/cache) to obtain locks. If necessary, you can clear these cache locks using the `schedule:clear-cache` Artisan command. This is typically only necessary if a task becomes stuck due to an unexpected server problem. -->
내부적으로 `withoutOverlapping`은 애플리케이션의 [cache](/docs/11.x/cache)를 이용해 락을 관리합니다. 만약 예상치 못한 서버 문제로 작업이 멈춰 락이 해제되지 않는 경우, Artisan 명령어 `schedule:clear-cache`를 이용해 락을 직접 해제할 수 있습니다. 일반적으로 이 기능은 특수 상황에서만 필요합니다.

<a name="running-tasks-on-one-server"></a>
<!-- ### Running Tasks on One Server -->
### Running Tasks on One Server

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, 또는 `redis`여야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<!-- If your application's scheduler is running on multiple servers, you may limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good! -->
스케줄러가 여러 서버에서 동작하는 환경이라면, 예약 작업이 오직 하나의 서버에서 한 번만 실행되도록 제한할 수 있습니다. 예를 들어, 매주 금요일 밤 리포트를 생성하는 예약 작업이 있을 때, 스케줄러가 3개의 워커 서버에서 동시에 실행된다면 3번 중복 생성될 수도 있습니다. 바람직하지 않습니다.

<!-- To indicate that the task should run on only one server, use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task at the same time: -->
이 작업이 한 서버에서만 실행되도록 하려면 예약 작업 정의 시 `onOneServer` 메서드를 사용합니다. 가장 먼저 작업 락을 획득한 서버가 atomic lock을 확보하여 다른 서버가 같은 작업을 동시에 실행하지 못하게 합니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```

<a name="naming-unique-jobs"></a>
<!-- #### Naming Single Server Jobs -->
#### Naming Single Server Jobs

<!-- Sometimes you may need to schedule the same job to be dispatched with different parameters, while still instructing Laravel to run each permutation of the job on a single server. To accomplish this, you may assign each schedule definition a unique name via the `name` method: -->
동일한 작업을 서로 다른 인자로 여러 번 예약하면서, 각 조합이 반드시 한 서버에서만 실행되도록 하고 싶을 때가 있습니다. 이럴 때는, 각 작업 예약 정의에 `name` 메서드를 이용해 고유한 이름을 지정하세요:

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

<!-- Similarly, scheduled closures must be assigned a name if they are intended to be run on one server: -->
마찬가지로, 클로저로 예약된 작업도 한 서버에서만 실행하고자 한다면 반드시 이름을 부여해야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
<!-- ### Background Tasks -->
### Background Tasks

<!-- By default, multiple tasks scheduled at the same time will execute sequentially based on the order they are defined in your `schedule` method. If you have long-running tasks, this may cause subsequent tasks to start much later than anticipated. If you would like to run tasks in the background so that they may all run simultaneously, you may use the `runInBackground` method: -->
기본적으로 동시에 예약된 여러 작업은 `schedule` 메서드에 정의된 순서대로 순차적으로 실행됩니다. 장시간 실행되는 작업이 있다면, 이후 작업이 예상보다 많이 늦게 실행될 수 있습니다. 여러 작업을 동시에 백그라운드로 실행하고 싶다면 `runInBackground` 메서드를 사용하세요:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command` 및 `exec` 메서드로 예약된 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- ### Maintenance Mode -->
### Maintenance Mode

<!-- Your application's scheduled tasks will not run when the application is in [maintenance mode](/docs/11.x/configuration#maintenance-mode), since we don't want your tasks to interfere with any unfinished maintenance you may be performing on your server. However, if you would like to force a task to run even in maintenance mode, you may call the `evenInMaintenanceMode` method when defining the task: -->
애플리케이션이 [maintenance mode](/docs/11.x/configuration#maintenance-mode)일 때는 예약된 작업이 실행되지 않습니다. 이는 서버에서 진행 중인 유지보수 작업에 영향을 주지 않으려는 의도입니다. 그러나 유지보수 모드에서도 강제로 작업을 실행하고 싶다면, 해당 작업 정의에 `evenInMaintenanceMode` 메서드를 추가하세요:

```
Schedule::command('emails:send')->evenInMaintenanceMode();
```

<a name="schedule-groups"></a>
<!-- ### Schedule Groups -->
### Schedule Groups

<!-- When defining multiple scheduled tasks with similar configurations, you can use Laravel’s task grouping feature to avoid repeating the same settings for each task. Grouping tasks simplifies your code and ensures consistency across related tasks. -->
비슷한 설정을 가진 여러 예약 작업을 정의할 때, Laravel의 작업 그룹화 기능을 사용하면 중복 코드를 줄이고 관련 작업들의 일관성을 쉽게 유지할 수 있습니다.

<!-- To create a group of scheduled tasks, invoke the desired task configuration methods, followed by the `group` method. The `group` method accepts a closure that is responsible for defining the tasks that share the specified configuration: -->
스케줄 그룹을 만들려면, 원하는 작업 설정 메서드 호출 뒤에 `group` 메서드를 연결하세요. `group` 메서드는 지정된 설정을 공유하는 작업들을 정의하는 클로저를 전달받습니다:

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
<!-- ## Running the Scheduler -->
## Running the Scheduler

<!-- Now that we have learned how to define scheduled tasks, let's discuss how to actually run them on our server. The `schedule:run` Artisan command will evaluate all of your scheduled tasks and determine if they need to run based on the server's current time. -->
이제 예약 작업을 정의하는 방법을 알았으니, 서버에서 실제로 작업을 실행하는 방법을 살펴보겠습니다. `schedule:run` Artisan 명령어는 모든 예약 작업을 평가하여, 서버의 현재 시간에 맞게 실행할 작업이 있는지 판단합니다.

<!-- So, when using Laravel's scheduler, we only need to add a single cron configuration entry to our server that runs the `schedule:run` command every minute. If you do not know how to add cron entries to your server, consider using a service such as [Laravel Forge](https://forge.laravel.com) which can manage the cron entries for you: -->
즉, Laravel의 스케줄러를 사용할 때는 `schedule:run` 명령을 매 분마다 실행하는 단 하나의 cron 항목만 서버에 추가하면 됩니다. 서버에 cron 항목을 추가하는 방법을 잘 모른다면, [Laravel Forge](https://forge.laravel.com)와 같이 cron 관리를 대신해 주는 서비스를 사용하는 것도 고려해 볼 수 있습니다:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
<!-- ### Sub-Minute Scheduled Tasks -->
### Sub-Minute Scheduled Tasks

<!-- On most operating systems, cron jobs are limited to running a maximum of once per minute. However, Laravel's scheduler allows you to schedule tasks to run at more frequent intervals, even as often as once per second: -->
대부분의 운영체제에서 cron 작업은 최소 1분 단위로만 실행할 수 있습니다. 하지만 Laravel 스케줄러는 작업을 1초마다 실행하는 등, 더 짧은 간격으로도 예약할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

<!-- When sub-minute tasks are defined within your application, the `schedule:run` command will continue running until the end of the current minute instead of exiting immediately. This allows the command to invoke all required sub-minute tasks throughout the minute. -->
애플리케이션에 1분 미만 간격의 작업이 정의되어 있으면, `schedule:run` 명령은 즉시 종료하지 않고 해당 분이 끝날 때까지 계속 실행됩니다. 이 과정에서 필요한 모든 1분 미만 주기의 작업이 올바른 타이밍에 실행됩니다.

<!-- Since sub-minute tasks that take longer than expected to run could delay the execution of later sub-minute tasks, it is recommended that all sub-minute tasks dispatch queued jobs or background commands to handle the actual task processing: -->
실행 시간이 예상보다 오래 걸리는 1분 미만 간격의 작업이 이후 작업들까지 지연시키는 것을 방지하기 위해, 이들 작업은 큐 작업을 디스패치하거나 백그라운드 명령어를 사용해 실제 처리를 하는 것이 좋습니다:

```
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
<!-- #### Interrupting Sub-Minute Tasks -->
#### Interrupting Sub-Minute Tasks

<!-- As the `schedule:run` command runs for the entire minute of invocation when sub-minute tasks are defined, you may sometimes need to interrupt the command when deploying your application. Otherwise, an instance of the `schedule:run` command that is already running would continue using your application's previously deployed code until the current minute ends. -->
1분 미만 간격의 작업이 정의되어 있을 때, `schedule:run` 명령은 한 번 호출될 때마다 1분 내내 계속 실행됩니다. 배포 과정에서 이 명령을 강제로 중단해야 하는 경우도 있습니다. 그렇지 않으면 이미 실행 중이던 `schedule:run` 명령이 현재 분이 끝날 때까지 기존 코드로 계속 실행될 수 있기 때문입니다.

<!-- To interrupt in-progress `schedule:run` invocations, you may add the `schedule:interrupt` command to your application's deployment script. This command should be invoked after your application is finished deploying: -->
이 경우 배포 스크립트에서 `schedule:interrupt` 명령을 추가해 실행 중인 `schedule:run`을 중단할 수 있습니다. 이 명령어는 배포가 끝난 후에 실행하면 됩니다:

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
<!-- ### Running the Scheduler Locally -->
### Running the Scheduler Locally

<!-- Typically, you would not add a scheduler cron entry to your local development machine. Instead, you may use the `schedule:work` Artisan command. This command will run in the foreground and invoke the scheduler every minute until you terminate the command. When sub-minute tasks are defined, the scheduler will continue running within each minute to process those tasks: -->
일반적으로 로컬 개발 환경에는 별도의 스케줄러 cron 항목을 추가하지 않습니다. 대신, `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 계속 실행되며, 매분마다 스케줄러를 호출합니다. 1분 미만 간격의 작업이 정의되어 있다면, 각 분 동안에도 이 작업들이 계속 실행됩니다:

```shell
php artisan schedule:work
```

<a name="task-output"></a>
<!-- ## Task Output -->
## Task Output

<!-- The Laravel scheduler provides several convenient methods for working with the output generated by scheduled tasks. First, using the `sendOutputTo` method, you may send the output to a file for later inspection: -->
Laravel 스케줄러는 예약 작업에서 생성된 출력(Output)을 쉽게 관리할 수 있는 여러 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드를 사용하면 작업 출력을 파일로 남겨 이후에 확인할 수 있습니다:

```
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```

<!-- If you would like to append the output to a given file, you may use the `appendOutputTo` method: -->
출력을 파일에 이어서(append) 기록하고 싶다면, `appendOutputTo` 메서드를 활용하세요:

```
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```

<!-- Using the `emailOutputTo` method, you may email the output to an email address of your choice. Before emailing the output of a task, you should configure Laravel's [email services](/docs/11.x/mail): -->
`emailOutputTo` 메서드를 이용하면, 원하는 이메일 주소로 작업 출력을 전송할 수도 있습니다. 이 기능을 사용하려면 Laravel의 [email services](/docs/11.x/mail)를 먼저 설정해야 합니다:

```
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```

<!-- If you only want to email the output if the scheduled Artisan or system command terminates with a non-zero exit code, use the `emailOutputOnFailure` method: -->
작업이 비정상적으로 종료(즉, non-zero 종료 코드)된 경우에만 출력물을 이메일로 받고 싶을 때는 `emailOutputOnFailure` 메서드를 사용하세요:

```
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command`와 `exec`로 예약된 작업에만 사용할 수 있습니다.

<a name="task-hooks"></a>
<!-- ## Task Hooks -->
## Task Hooks

<!-- Using the `before` and `after` methods, you may specify code to be executed before and after the scheduled task is executed: -->
`before`와 `after` 메서드로 예약 작업 실행 전후에 수행할 코드를 지정할 수 있습니다:

```
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

<!-- The `onSuccess` and `onFailure` methods allow you to specify code to be executed if the scheduled task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`onSuccess`와 `onFailure` 메서드를 사용하면 예약 작업이 정상적으로 실행/실패한 경우에만 특정 코드를 실행할 수 있습니다. 실패란, 예약된 Artisan 혹은 시스템 명령어가 non-zero 종료 코드로 종료된 경우를 의미합니다:

```
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // The task succeeded...
    })
    ->onFailure(function () {
        // The task failed...
    });
```

<!-- If output is available from your command, you may access it in your `after`, `onSuccess` or `onFailure` hooks by type-hinting an `Illuminate\Support\Stringable` instance as the `$output` argument of your hook's closure definition: -->
명령어에서 출력을 반환했다면, `after`, `onSuccess`, `onFailure` 후크의 클로저 정의에서 `$output` 인자를 `Illuminate\Support\Stringable` 타입으로 지정해 출력 값을 받을 수 있습니다:

```
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
<!-- #### Pinging URLs -->
#### Pinging URLs

<!-- Using the `pingBefore` and `thenPing` methods, the scheduler can automatically ping a given URL before or after a task is executed. This method is useful for notifying an external service, such as [Envoyer](https://envoyer.io), that your scheduled task is beginning or has finished execution: -->
`pingBefore`와 `thenPing` 메서드를 활용하면, 작업 실행 전 또는 후에 지정된 URL로 자동으로 핑(ping)을 보낼 수 있습니다. 이 기능은 [Envoyer](https://envoyer.io)와 같은 외부 서비스에 예약 작업이 시작 또는 종료되었음을 알리는 데 유용합니다:

```
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```

<!-- The `pingOnSuccess` and `pingOnFailure` methods may be used to ping a given URL only if the task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`pingOnSuccess`와 `pingOnFailure`는 작업 성공/실패 시에만 지정한 URL로 핑을 전송합니다. 실패는 예약된 Artisan 명령어나 시스템 명령어가 non-zero 종료 코드로 끝난 경우를 의미합니다:

```
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```

<!-- The `pingBeforeIf`,`thenPingIf`,`pingOnSuccessIf`, and `pingOnFailureIf` methods may be used to ping a given URL only if a given condition is `true`: -->
`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, `pingOnFailureIf` 메서드로 조건이 `true`일 때만 URL로 핑을 보내도록 할 수도 있습니다:

```
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
<!-- ## Events -->
## Events

<!-- Laravel dispatches a variety of [events](/docs/11.x/events) during the scheduling process. You may [define listeners](/docs/11.x/events) for any of the following events: -->
Laravel은 스케줄링 과정에서 다양한 [events](/docs/11.x/events)를 발생시킵니다. 다음의 이벤트에 대해 [define listeners](/docs/11.x/events)할 수 있습니다:

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 이벤트 이름 |
| --- |
| `Illuminate\Console\Events\ScheduledTaskStarting` |
| `Illuminate\Console\Events\ScheduledTaskFinished` |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped` |
| `Illuminate\Console\Events\ScheduledTaskFailed` |

<!-- </div> -->
</div>
