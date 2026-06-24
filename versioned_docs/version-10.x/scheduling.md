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
과거에는 서버에서 예약해야 할 각 작업마다 별도의 cron 설정을 직접 추가하시곤 했을 것입니다. 하지만 이 방법은 금방 관리가 번거로워집니다. 작업 일정이 소스 코드로 관리되지 않고, 기존의 cron 항목을 확인하거나 새로운 항목을 추가하려면 매번 서버에 SSH로 접속해야 하기 때문입니다.

<!-- Laravel's command scheduler offers a fresh approach to managing scheduled tasks on your server. The scheduler allows you to fluently and expressively define your command schedule within your Laravel application itself. When using the scheduler, only a single cron entry is needed on your server. Your task schedule is defined in the `app/Console/Kernel.php` file's `schedule` method. To help you get started, a simple example is defined within the method. -->
Laravel의 명령어 스케줄러(Command Scheduler)는 서버의 예약 작업을 효율적으로 관리할 수 있는 새로운 방식을 제공합니다. 이 스케줄러를 사용하면 Laravel 애플리케이션 내에서 손쉽고 직관적으로 작업 일정을 정의할 수 있습니다. 스케줄러를 활용할 때 서버에는 오직 하나의 cron 항목만 추가하면 됩니다. 실제 예약에 관한 코드는 `app/Console/Kernel.php` 파일의 `schedule` 메서드에 정의하며, 시작에 도움이 될 수 있도록 간단한 예제가 이미 포함되어 있습니다.

<a name="defining-schedules"></a>
<!-- ## Defining Schedules -->
## Defining Schedules

<!-- You may define all of your scheduled tasks in the `schedule` method of your application's `App\Console\Kernel` class. To get started, let's take a look at an example. In this example, we will schedule a closure to be called every day at midnight. Within the closure we will execute a database query to clear a table: -->
애플리케이션의 `App\Console\Kernel` 클래스 안의 `schedule` 메서드에서 모든 예약 작업을 정의할 수 있습니다. 먼저 예제를 살펴보겠습니다. 다음 예제에서는 매일 자정에 호출되는 클로저를 예약하고, 클로저 내부에서 데이터베이스 쿼리를 실행하여 테이블을 비웁니다.

```
<?php

namespace App\Console;

use Illuminate\Console\Scheduling\Schedule;
use Illuminate\Foundation\Console\Kernel as ConsoleKernel;
use Illuminate\Support\Facades\DB;

class Kernel extends ConsoleKernel
{
    /**
     * Define the application's command schedule.
     */
    protected function schedule(Schedule $schedule): void
    {
        $schedule->call(function () {
            DB::table('recent_users')->delete();
        })->daily();
    }
}
```

<!-- In addition to scheduling using closures, you may also schedule [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke). Invokable objects are simple PHP classes that contain an `__invoke` method: -->
클로저를 사용한 방식 외에도, [invokable objects](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 예약할 수도 있습니다. 호출 가능한 객체란 `__invoke` 메서드를 가진 간단한 PHP 클래스를 말합니다.

```
$schedule->call(new DeleteRecentUsers)->daily();
```

<!-- If you would like to view an overview of your scheduled tasks and the next time they are scheduled to run, you may use the `schedule:list` Artisan command: -->
예약해둔 작업들의 전체 목록과 다음 실행 예정 시각을 확인하고 싶다면, `schedule:list` Artisan 명령어를 사용할 수 있습니다.

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
<!-- ### Scheduling Artisan Commands -->
### Scheduling Artisan Commands

<!-- In addition to scheduling closures, you may also schedule [Artisan commands](/docs/10.x/artisan) and system commands. For example, you may use the `command` method to schedule an Artisan command using either the command's name or class. -->
클로저뿐만 아니라, [Artisan commands](/docs/10.x/artisan) 또는 시스템 명령어를 예약할 수도 있습니다. 예를 들어, `command` 메서드를 이용해 Artisan 명령어를 이름이나 클래스명을 통해 예약할 수 있습니다.

<!-- When scheduling Artisan commands using the command's class name, you may pass an array of additional command-line arguments that should be provided to the command when it is invoked: -->
명령어를 클래스명으로 예약할 때, 해당 명령어가 실행될 때 전달할 추가 커맨드라인 인수를 배열로 넘길 수 있습니다.

```
use App\Console\Commands\SendEmailsCommand;

$schedule->command('emails:send Taylor --force')->daily();

$schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```

<a name="scheduling-queued-jobs"></a>
<!-- ### Scheduling Queued Jobs -->
### Scheduling Queued Jobs

<!-- The `job` method may be used to schedule a [queued job](/docs/10.x/queues). This method provides a convenient way to schedule queued jobs without using the `call` method to define closures to queue the job: -->
`job` 메서드를 사용하면 [queued job](/docs/10.x/queues)을 예약할 수 있습니다. 이 방법을 이용하면 `call` 메서드로 클로저를 정의해 큐 작업을 적재하지 않고도, 간편하게 큐 작업을 예약할 수 있습니다.

```
use App\Jobs\Heartbeat;

$schedule->job(new Heartbeat)->everyFiveMinutes();
```

<!-- Optional second and third arguments may be provided to the `job` method which specifies the queue name and queue connection that should be used to queue the job: -->
또한, `job` 메서드에는 두 번째 인수와 세 번째 인수를 추가로 지정해서 어떤 큐 이름과 연결(connection)로 작업을 디스패치할지 설정할 수 있습니다.

```
use App\Jobs\Heartbeat;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
$schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```

<a name="scheduling-shell-commands"></a>
<!-- ### Scheduling Shell Commands -->
### Scheduling Shell Commands

<!-- The `exec` method may be used to issue a command to the operating system: -->
`exec` 메서드를 사용하면 OS에 직접 명령어를 실행시킬 수 있습니다.

```
$schedule->exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
<!-- ### Schedule Frequency Options -->
### Schedule Frequency Options

<!-- We've already seen a few examples of how you may configure a task to run at specified intervals. However, there are many more task schedule frequencies that you may assign to a task: -->
앞서 특정 간격으로 작업을 실행하는 방법의 예시를 살펴봤지만, Laravel의 예약 작업은 다양한 주기를 제공합니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

<!--
Method  | Description
------------- | -------------
`->cron('* * * * *');`  |  Run the task on a custom cron schedule
`->everySecond();`  |  Run the task every second
`->everyTwoSeconds();`  |  Run the task every two seconds
`->everyFiveSeconds();`  |  Run the task every five seconds
`->everyTenSeconds();`  |  Run the task every ten seconds
`->everyFifteenSeconds();`  |  Run the task every fifteen seconds
`->everyTwentySeconds();`  |  Run the task every twenty seconds
`->everyThirtySeconds();`  |  Run the task every thirty seconds
`->everyMinute();`  |  Run the task every minute
`->everyTwoMinutes();`  |  Run the task every two minutes
`->everyThreeMinutes();`  |  Run the task every three minutes
`->everyFourMinutes();`  |  Run the task every four minutes
`->everyFiveMinutes();`  |  Run the task every five minutes
`->everyTenMinutes();`  |  Run the task every ten minutes
`->everyFifteenMinutes();`  |  Run the task every fifteen minutes
`->everyThirtyMinutes();`  |  Run the task every thirty minutes
`->hourly();`  |  Run the task every hour
`->hourlyAt(17);`  |  Run the task every hour at 17 minutes past the hour
`->everyOddHour($minutes = 0);`  |  Run the task every odd hour
`->everyTwoHours($minutes = 0);`  |  Run the task every two hours
`->everyThreeHours($minutes = 0);`  |  Run the task every three hours
`->everyFourHours($minutes = 0);`  |  Run the task every four hours
`->everySixHours($minutes = 0);`  |  Run the task every six hours
`->daily();`  |  Run the task every day at midnight
`->dailyAt('13:00');`  |  Run the task every day at 13:00
`->twiceDaily(1, 13);`  |  Run the task daily at 1:00 & 13:00
`->twiceDailyAt(1, 13, 15);`  |  Run the task daily at 1:15 & 13:15
`->weekly();`  |  Run the task every Sunday at 00:00
`->weeklyOn(1, '8:00');`  |  Run the task every week on Monday at 8:00
`->monthly();`  |  Run the task on the first day of every month at 00:00
`->monthlyOn(4, '15:00');`  |  Run the task every month on the 4th at 15:00
`->twiceMonthly(1, 16, '13:00');`  |  Run the task monthly on the 1st and 16th at 13:00
`->lastDayOfMonth('15:00');` | Run the task on the last day of the month at 15:00
`->quarterly();` |  Run the task on the first day of every quarter at 00:00
`->quarterlyOn(4, '14:00');` |  Run the task every quarter on the 4th at 14:00
`->yearly();`  |  Run the task on the first day of every year at 00:00
`->yearlyOn(6, 1, '17:00');`  |  Run the task every year on June 1st at 17:00
`->timezone('America/New_York');` | Set the timezone for the task
-->
메서드  | 설명
------------- | -------------
`->cron('* * * * *');`  |  원하는 cron 스케줄로 작업 실행
`->everySecond();`  |  매초 작업 실행
`->everyTwoSeconds();`  |  2초마다 작업 실행
`->everyFiveSeconds();`  |  5초마다 작업 실행
`->everyTenSeconds();`  |  10초마다 작업 실행
`->everyFifteenSeconds();`  |  15초마다 작업 실행
`->everyTwentySeconds();`  |  20초마다 작업 실행
`->everyThirtySeconds();`  |  30초마다 작업 실행
`->everyMinute();`  |  매 분 작업 실행
`->everyTwoMinutes();`  |  2분마다 작업 실행
`->everyThreeMinutes();`  |  3분마다 작업 실행
`->everyFourMinutes();`  |  4분마다 작업 실행
`->everyFiveMinutes();`  |  5분마다 작업 실행
`->everyTenMinutes();`  |  10분마다 작업 실행
`->everyFifteenMinutes();`  |  15분마다 작업 실행
`->everyThirtyMinutes();`  |  30분마다 작업 실행
`->hourly();`  |  매시간 작업 실행
`->hourlyAt(17);`  |  매시 17분에 작업 실행
`->everyOddHour($minutes = 0);`  |  홀수 시간마다 작업 실행
`->everyTwoHours($minutes = 0);`  |  2시간마다 작업 실행
`->everyThreeHours($minutes = 0);`  |  3시간마다 작업 실행
`->everyFourHours($minutes = 0);`  |  4시간마다 작업 실행
`->everySixHours($minutes = 0);`  |  6시간마다 작업 실행
`->daily();`  |  매일 자정 작업 실행
`->dailyAt('13:00');`  |  매일 13:00에 작업 실행
`->twiceDaily(1, 13);`  |  매일 1:00, 13:00에 작업 실행
`->twiceDailyAt(1, 13, 15);`  |  매일 1:15, 13:15에 작업 실행
`->weekly();`  |  매주 일요일 00:00에 작업 실행
`->weeklyOn(1, '8:00');`  |  매주 월요일 8:00에 작업 실행
`->monthly();`  |  매월 1일 00:00에 작업 실행
`->monthlyOn(4, '15:00');`  |  매월 4일 15:00에 작업 실행
`->twiceMonthly(1, 16, '13:00');`  |  매월 1일, 16일 13:00에 작업 실행
`->lastDayOfMonth('15:00');` | 매월 마지막 날 15:00에 작업 실행
`->quarterly();` |  매 분기 첫날 00:00에 작업 실행
`->quarterlyOn(4, '14:00');` |  매 분기 4일 14:00에 작업 실행
`->yearly();`  |  매년 1월 1일 00:00에 작업 실행
`->yearlyOn(6, 1, '17:00');`  |  매년 6월 1일 17:00에 작업 실행
`->timezone('America/New_York');` | 작업에 사용할 타임존 지정

<!-- </div> -->
</div>

<!-- These methods may be combined with additional constraints to create even more finely tuned schedules that only run on certain days of the week. For example, you may schedule a command to run weekly on Monday: -->
위 메서드들은 추가 제약 조건과 조합해서, 특정 요일에만 작업을 실행하도록 정밀하게 설정할 수도 있습니다. 예를 들어, 특정 명령어를 매주 월요일에 실행하려면 다음과 같이 작성할 수 있습니다.

```
// Run once per week on Monday at 1 PM...
$schedule->call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// Run hourly from 8 AM to 5 PM on weekdays...
$schedule->command('foo')
          ->weekdays()
          ->hourly()
          ->timezone('America/Chicago')
          ->between('8:00', '17:00');
```

<!-- A list of additional schedule constraints may be found below: -->
아래는 추가적으로 사용할 수 있는 스케줄 제약 메서드 목록입니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

<!--
Method  | Description
------------- | -------------
`->weekdays();`  |  Limit the task to weekdays
`->weekends();`  |  Limit the task to weekends
`->sundays();`  |  Limit the task to Sunday
`->mondays();`  |  Limit the task to Monday
`->tuesdays();`  |  Limit the task to Tuesday
`->wednesdays();`  |  Limit the task to Wednesday
`->thursdays();`  |  Limit the task to Thursday
`->fridays();`  |  Limit the task to Friday
`->saturdays();`  |  Limit the task to Saturday
`->days(array\|mixed);`  |  Limit the task to specific days
`->between($startTime, $endTime);`  |  Limit the task to run between start and end times
`->unlessBetween($startTime, $endTime);`  |  Limit the task to not run between start and end times
`->when(Closure);`  |  Limit the task based on a truth test
`->environments($env);`  |  Limit the task to specific environments
-->
메서드  | 설명
------------- | -------------
`->weekdays();`  |  평일로 제한
`->weekends();`  |  주말로 제한
`->sundays();`  |  일요일로 제한
`->mondays();`  |  월요일로 제한
`->tuesdays();`  |  화요일로 제한
`->wednesdays();`  |  수요일로 제한
`->thursdays();`  |  목요일로 제한
`->fridays();`  |  금요일로 제한
`->saturdays();`  |  토요일로 제한
`->days(array\|mixed);`  |  특정 요일만 제한
`->between($startTime, $endTime);`  |  지정한 시간 범위 내에만 실행
`->unlessBetween($startTime, $endTime);`  |  지정한 시간 범위 외에만 실행
`->when(Closure);`  |  특정 조건(참/거짓)에 따라 실행
`->environments($env);`  |  특정 환경에서만 실행

<!-- </div> -->
</div>

<a name="day-constraints"></a>
<!-- #### Day Constraints -->
#### Day Constraints

<!-- The `days` method may be used to limit the execution of a task to specific days of the week. For example, you may schedule a command to run hourly on Sundays and Wednesdays: -->
`days` 메서드를 사용하면 특정 요일에만 작업을 실행하도록 제한할 수 있습니다. 예를 들어, 명령어를 일요일과 수요일에만 매시간 실행하려면 다음과 같이 작성합니다.

```
$schedule->command('emails:send')
                ->hourly()
                ->days([0, 3]);
```

<!-- Alternatively, you may use the constants available on the `Illuminate\Console\Scheduling\Schedule` class when defining the days on which a task should run: -->
또는, 어떤 요일에 작업을 실행할지 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스의 상수를 사용할 수도 있습니다.

```
use Illuminate\Console\Scheduling\Schedule;

$schedule->command('emails:send')
                ->hourly()
                ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```

<a name="between-time-constraints"></a>
<!-- #### Between Time Constraints -->
#### Between Time Constraints

<!-- The `between` method may be used to limit the execution of a task based on the time of day: -->
`between` 메서드를 사용하면 작업 실행을 하루 중 특정 시간대 내로 제한할 수 있습니다.

```
$schedule->command('emails:send')
                    ->hourly()
                    ->between('7:00', '22:00');
```

<!-- Similarly, the `unlessBetween` method can be used to exclude the execution of a task for a period of time: -->
반대로, `unlessBetween` 메서드를 활용하면 지정한 시간대에는 작업 실행을 제외할 수 있습니다.

```
$schedule->command('emails:send')
                    ->hourly()
                    ->unlessBetween('23:00', '4:00');
```

<a name="truth-test-constraints"></a>
<!-- #### Truth Test Constraints -->
#### Truth Test Constraints

<!-- The `when` method may be used to limit the execution of a task based on the result of a given truth test. In other words, if the given closure returns `true`, the task will execute as long as no other constraining conditions prevent the task from running: -->
`when` 메서드를 사용하면 주어진 조건 테스트의 결과에 따라 작업 실행을 제한할 수 있습니다. 즉, 지정한 클로저가 `true`를 반환하면, 다른 제약 조건이 작업 실행을 막지 않는 한 작업이 실행됩니다.

```
$schedule->command('emails:send')->daily()->when(function () {
    return true;
});
```

<!-- The `skip` method may be seen as the inverse of `when`. If the `skip` method returns `true`, the scheduled task will not be executed: -->
`skip` 메서드는 `when` 메서드와 반대로 동작합니다. `skip`의 클로저에서 `true`가 반환되면 예약 작업은 실행되지 않습니다.

```
$schedule->command('emails:send')->daily()->skip(function () {
    return true;
});
```

<!-- When using chained `when` methods, the scheduled command will only execute if all `when` conditions return `true`. -->
`when` 메서드를 체이닝해서 여러 개 지정한 경우, 모든 `when` 조건이 `true`를 반환할 때만 예약 명령어가 실행됩니다.

<a name="environment-constraints"></a>
<!-- #### Environment Constraints -->
#### Environment Constraints

<!-- The `environments` method may be used to execute tasks only on the given environments (as defined by the `APP_ENV` [environment variable](/docs/10.x/configuration#environment-configuration)): -->
`environments` 메서드를 이용하면 [environment variable](/docs/10.x/configuration#environment-configuration) `APP_ENV`의 값에 따라 특정 환경에서만 작업을 실행할 수 있습니다.

```
$schedule->command('emails:send')
            ->daily()
            ->environments(['staging', 'production']);
```

<a name="timezones"></a>
<!-- ### Timezones -->
### Timezones

<!-- Using the `timezone` method, you may specify that a scheduled task's time should be interpreted within a given timezone: -->
`timezone` 메서드를 활용하면, 지정한 타임존에서 예약 작업이 해석되도록 할 수 있습니다.

```
$schedule->command('report:generate')
         ->timezone('America/New_York')
         ->at('2:00')
```

<!-- If you are repeatedly assigning the same timezone to all of your scheduled tasks, you may wish to define a `scheduleTimezone` method in your `App\Console\Kernel` class. This method should return the default timezone that should be assigned to all scheduled tasks: -->
모든 예약 작업에 동일한 타임존을 반복 지정해야 할 경우, `App\Console\Kernel` 클래스에 `scheduleTimezone` 메서드를 만들어 기본 타임존을 지정할 수 있습니다.

```
use DateTimeZone;

/**
 * Get the timezone that should be used by default for scheduled events.
 */
protected function scheduleTimezone(): DateTimeZone|string|null
{
    return 'America/Chicago';
}
```

> [!WARNING]
> 일부 타임존에서는 서머타임(일광 절약 시간제)을 사용합니다. 이로 인해, 서머타임이 변경되는 시점에는 예약 작업이 두 번 실행되거나 아예 실행되지 않을 수도 있습니다. 이런 문제를 방지하려면 가능하면 타임존 기반 예약은 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
<!-- ### Preventing Task Overlaps -->
### Preventing Task Overlaps

<!-- By default, scheduled tasks will be run even if the previous instance of the task is still running. To prevent this, you may use the `withoutOverlapping` method: -->
기본적으로 예약된 작업은 이전 인스턴스가 아직 실행 중이더라도 새로운 인스턴스가 실행됩니다. 이를 방지하려면 `withoutOverlapping` 메서드를 사용하세요.

```
$schedule->command('emails:send')->withoutOverlapping();
```

<!-- In this example, the `emails:send` [Artisan command](/docs/10.x/artisan) will be run every minute if it is not already running. The `withoutOverlapping` method is especially useful if you have tasks that vary drastically in their execution time, preventing you from predicting exactly how long a given task will take. -->
이 예시에서 `emails:send` [Artisan command](/docs/10.x/artisan)는 이전 실행이 끝난 경우에만 1분마다 실행됩니다. `withoutOverlapping` 메서드는 실행 시간이 들쑥날쑥해 다음 실행 시간을 정확히 예측할 수 없는 작업에서 특히 유용합니다.

<!-- If needed, you may specify how many minutes must pass before the "without overlapping" lock expires. By default, the lock will expire after 24 hours: -->
필요하다면, "중복 방지" 락이 만료되기까지 대기할 분(minutes) 수를 지정할 수 있습니다. 기본 설정은 24시간 후 락이 만료됩니다.

```
$schedule->command('emails:send')->withoutOverlapping(10);
```

<!-- Behind the scenes, the `withoutOverlapping` method utilizes your application's [cache](/docs/10.x/cache) to obtain locks. If necessary, you can clear these cache locks using the `schedule:clear-cache` Artisan command. This is typically only necessary if a task becomes stuck due to an unexpected server problem. -->
내부적으로 `withoutOverlapping`은 애플리케이션의 [cache](/docs/10.x/cache)를 활용해 락을 관리합니다. 예기치 못한 서버 문제 등으로 작업이 막혀버리는 경우, `schedule:clear-cache` Artisan 명령어로 캐시 락을 수동으로 해제할 수 있습니다. 이런 조치는 주로 작업이 비정상적으로 멈춤 현상이 발생할 때만 필요합니다.

<a name="running-tasks-on-one-server"></a>
<!-- ### Running Tasks on One Server -->
### Running Tasks on One Server

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `database`, `memcached`, `dynamodb`, `redis` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<!-- If your application's scheduler is running on multiple servers, you may limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good! -->
예약 스케줄러가 여러 대의 서버에서 실행되는 경우, 특정 작업을 한 서버에서만 실행하고 싶을 수 있습니다. 예를 들어, 금요일 밤마다 새로운 리포트를 생성하는 예약 작업이 있다고 가정해보겠습니다. 작업 스케줄러가 워커 서버 세 대에서 동시에 동작하고 있다면, 해당 작업이 세 대 모두에서 실행되어 리포트가 세 번 생성될 수 있습니다. 이는 바람직하지 않은 결과입니다.

<!-- To indicate that the task should run on only one server, use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task at the same time: -->
`onOneServer` 메서드를 이용해 해당 작업이 단일 서버에서만 실행되도록 지정할 수 있습니다. 가장 먼저 락을 획득한 서버가 해당 작업을 단독 실행하며, 다른 서버에서는 동시에 작업이 실행되지 않습니다.

```
$schedule->command('report:generate')
                ->fridays()
                ->at('17:00')
                ->onOneServer();
```

<a name="naming-unique-jobs"></a>
<!-- #### Naming Single Server Jobs -->
#### Naming Single Server Jobs

<!-- Sometimes you may need to schedule the same job to be dispatched with different parameters, while still instructing Laravel to run each permutation of the job on a single server. To accomplish this, you may assign each schedule definition a unique name via the `name` method: -->
같은 작업을 서로 다른 인수로 여러 번 예약하고, 각 작업이 동일하게 단일 서버에서만 실행되게 하려면 `name` 메서드를 이용해 각 예약 작업마다 고유한 이름을 부여하세요.

```php
$schedule->job(new CheckUptime('https://laravel.com'))
            ->name('check_uptime:laravel.com')
            ->everyFiveMinutes()
            ->onOneServer();

$schedule->job(new CheckUptime('https://vapor.laravel.com'))
            ->name('check_uptime:vapor.laravel.com')
            ->everyFiveMinutes()
            ->onOneServer();
```

<!-- Similarly, scheduled closures must be assigned a name if they are intended to be run on one server: -->
마찬가지로, 클로저로 작성된 예약 작업 역시 단일 서버에서만 실행하려면 반드시 이름을 지정해야 합니다.

```php
$schedule->call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```

<a name="background-tasks"></a>
<!-- ### Background Tasks -->
### Background Tasks

<!-- By default, multiple tasks scheduled at the same time will execute sequentially based on the order they are defined in your `schedule` method. If you have long-running tasks, this may cause subsequent tasks to start much later than anticipated. If you would like to run tasks in the background so that they may all run simultaneously, you may use the `runInBackground` method: -->
기본적으로, 같은 시각에 예약된 여러 작업들은 `schedule` 메서드에 정의된 순서대로 차례대로 실행됩니다. 오래 걸리는 작업이 있다면 그 이후 작업이 실행되는 시간이 예정보다 늦어질 수 있습니다. 모든 작업을 동시에 실행하고 싶다면 `runInBackground` 메서드를 사용하세요.

```
$schedule->command('analytics:report')
         ->daily()
         ->runInBackground();
```

> [!WARNING]
> `runInBackground` 메서드는 `command`와 `exec` 메서드로 예약된 작업에서만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
<!-- ### Maintenance Mode -->
### Maintenance Mode

<!-- Your application's scheduled tasks will not run when the application is in [maintenance mode](/docs/10.x/configuration#maintenance-mode), since we don't want your tasks to interfere with any unfinished maintenance you may be performing on your server. However, if you would like to force a task to run even in maintenance mode, you may call the `evenInMaintenanceMode` method when defining the task: -->
애플리케이션이 [maintenance mode](/docs/10.x/configuration#maintenance-mode)에 들어가면, 예약 작업이 자동으로 중지됩니다. 이는 작업이 서버 유지보수 작업과 충돌하는 것을 방지하기 위해서입니다. 하지만, 꼭 유지보수 모드 중에도 특정 작업을 강제로 실행해야 한다면, 해당 작업 정의에 `evenInMaintenanceMode` 메서드를 추가하세요.

```
$schedule->command('emails:send')->evenInMaintenanceMode();
```

<a name="running-the-scheduler"></a>
<!-- ## Running the Scheduler -->
## Running the Scheduler

<!-- Now that we have learned how to define scheduled tasks, let's discuss how to actually run them on our server. The `schedule:run` Artisan command will evaluate all of your scheduled tasks and determine if they need to run based on the server's current time. -->
지금까지 예약 작업을 정의하는 방법을 살펴봤으니, 실제 서버에서 이를 실행하는 방법을 알아보겠습니다. `schedule:run` Artisan 명령어는 예약된 모든 작업을 평가하여 서버의 현재 시간 기준으로 실행 여부를 결정합니다.

<!-- So, when using Laravel's scheduler, we only need to add a single cron configuration entry to our server that runs the `schedule:run` command every minute. If you do not know how to add cron entries to your server, consider using a service such as [Laravel Forge](https://forge.laravel.com) which can manage the cron entries for you: -->
즉, Laravel 스케줄러를 사용할 때는 서버에 오직 하나의 cron 항목만 등록해두면 됩니다. 이 cron 항목은 매 분마다 `schedule:run` 명령어를 실행하면 됩니다. 서버에 cron 항목을 추가하는 방법을 잘 모른다면, [Laravel Forge](https://forge.laravel.com)처럼 cron 설정을 대신 관리해주는 서비스를 활용하는 것도 좋습니다.

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
<!-- ### Sub-Minute Scheduled Tasks -->
### Sub-Minute Scheduled Tasks

<!-- On most operating systems, cron jobs are limited to running a maximum of once per minute. However, Laravel's scheduler allows you to schedule tasks to run at more frequent intervals, even as often as once per second: -->
대부분의 운영체제에서 cron 작업은 최소 1분마다만 실행할 수 있습니다. 그러나 Laravel 스케줄러는 1초와 같이 더 짧은 간격으로도 작업을 예약할 수 있습니다.

```
$schedule->call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```

<!-- When sub-minute tasks are defined within your application, the `schedule:run` command will continue running until the end of the current minute instead of exiting immediately. This allows the command to invoke all required sub-minute tasks throughout the minute. -->
1분 미만 작업(sub-minute tasks)이 애플리케이션 내에 정의되어 있을 때, `schedule:run` 명령어는 즉시 종료되지 않고, 해당 분이 끝날 때까지 계속 실행됩니다. 이 방식은 1초 단위 등 짧은 간격의 예약 작업이 분 단위로 모두 실행될 수 있도록 도와줍니다.

<!-- Since sub-minute tasks that take longer than expected to run could delay the execution of later sub-minute tasks, it is recommend that all sub-minute tasks dispatch queued jobs or background commands to handle the actual task processing: -->
하지만 1분 미만 작업의 실행 시간이 길어지면 뒤따르는 다른 작업들이 지연될 수 있습니다. 이런 경우에는 1분 미만 작업에서는 실제 처리를 큐 작업 또는 백그라운드 명령어로 디스패치하는 것이 좋습니다.

```
use App\Jobs\DeleteRecentUsers;

$schedule->job(new DeleteRecentUsers)->everyTenSeconds();

$schedule->command('users:delete')->everyTenSeconds()->runInBackground();
```

<a name="interrupting-sub-minute-tasks"></a>
<!-- #### Interrupting Sub-Minute Tasks -->
#### Interrupting Sub-Minute Tasks

<!-- As the `schedule:run` command runs for the entire minute of invocation when sub-minute tasks are defined, you may sometimes need to interrupt the command when deploying your application. Otherwise, an instance of the `schedule:run` command that is already running would continue using your application's previously deployed code until the current minute ends. -->
1분 미만 작업이 정의된 경우 `schedule:run` 명령어가 전체 1분 동안 동작하기 때문에, 애플리케이션 배포(deploy) 시에 이 과정을 중단해야 할 필요가 있습니다. 그렇지 않으면 이미 실행 중이던 `schedule:run` 명령어가 현재 분이 끝날 때까지 이전 코드를 계속 사용할 수 있습니다.

<!-- To interrupt in-progress `schedule:run` invocations, you may add the `schedule:interrupt` command to your application's deployment script. This command should be invoked after your application is finished deploying: -->
이런 상황에서는 배포 스크립트의 마지막 단계에서 `schedule:interrupt` 명령어를 호출해 진행 중인 `schedule:run`을 안전하게 중단할 수 있습니다.

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
<!-- ### Running the Scheduler Locally -->
### Running the Scheduler Locally

<!-- Typically, you would not add a scheduler cron entry to your local development machine. Instead, you may use the `schedule:work` Artisan command. This command will run in the foreground and invoke the scheduler every minute until you terminate the command: -->
일반적으로, 개발환경(로컬)에서는 별도의 cron 항목을 추가하지 않습니다. 대신, `schedule:work` Artisan 명령어를 사용하세요. 이 명령어는 포그라운드에서 동작하며, 명령어를 중단할 때까지 1분마다 스케줄러를 실행해줍니다.

```shell
php artisan schedule:work
```

<a name="task-output"></a>
<!-- ## Task Output -->
## Task Output

<!-- The Laravel scheduler provides several convenient methods for working with the output generated by scheduled tasks. First, using the `sendOutputTo` method, you may send the output to a file for later inspection: -->
Laravel 스케줄러는 예약 작업의 출력을 다루는 여러 가지 편리한 메서드를 제공합니다. 먼저, `sendOutputTo` 메서드를 사용하면 작업 실행 결과를 파일로 남겨 나중에 확인할 수 있습니다.

```
$schedule->command('emails:send')
         ->daily()
         ->sendOutputTo($filePath);
```

<!-- If you would like to append the output to a given file, you may use the `appendOutputTo` method: -->
출력 파일에 새로운 내용을 추가(append)하려면 `appendOutputTo` 메서드를 사용합니다.

```
$schedule->command('emails:send')
         ->daily()
         ->appendOutputTo($filePath);
```

<!-- Using the `emailOutputTo` method, you may email the output to an email address of your choice. Before emailing the output of a task, you should configure Laravel's [email services](/docs/10.x/mail): -->
`emailOutputTo` 메서드는 작업 출력을 원하는 이메일 주소로 전송해줍니다. 이 기능을 사용하려면 먼저 Laravel의 [email services](/docs/10.x/mail)를 올바르게 설정해야 합니다.

```
$schedule->command('report:generate')
         ->daily()
         ->sendOutputTo($filePath)
         ->emailOutputTo('taylor@example.com');
```

<!-- If you only want to email the output if the scheduled Artisan or system command terminates with a non-zero exit code, use the `emailOutputOnFailure` method: -->
명령어가 0이 아닌 종료코드(실패)로 끝난 경우에만 이메일로 결과를 받고 싶을 때는 `emailOutputOnFailure` 메서드를 사용하세요.

```
$schedule->command('report:generate')
         ->daily()
         ->emailOutputOnFailure('taylor@example.com');
```

> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo`, `appendOutputTo` 메서드는 `command` 및 `exec` 메서드로 예약한 작업에서만 사용할 수 있습니다.

<a name="task-hooks"></a>
<!-- ## Task Hooks -->
## Task Hooks

<!-- Using the `before` and `after` methods, you may specify code to be executed before and after the scheduled task is executed: -->
`before` 및 `after` 메서드를 사용하면 예약 작업 실행 전후에 실행할 코드를 지정할 수 있습니다.

```
$schedule->command('emails:send')
         ->daily()
         ->before(function () {
             // The task is about to execute...
         })
         ->after(function () {
             // The task has executed...
         });
```

<!-- The `onSuccess` and `onFailure` methods allow you to specify code to be executed if the scheduled task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`onSuccess`와 `onFailure` 메서드는 작업이 성공 또는 실패할 때(즉, 예약된 Artisan 또는 시스템 명령어가 0 이외의 종료 코드로 종료될 때) 실행할 코드를 지정합니다.

```
$schedule->command('emails:send')
         ->daily()
         ->onSuccess(function () {
             // The task succeeded...
         })
         ->onFailure(function () {
             // The task failed...
         });
```

<!-- If output is available from your command, you may access it in your `after`, `onSuccess` or `onFailure` hooks by type-hinting an `Illuminate\Support\Stringable` instance as the `$output` argument of your hook's closure definition: -->
명령어에서 출력 결과를 사용할 수 있다면, 후킹 클로저의 `$output` 인자로 `Illuminate\Support\Stringable` 인스턴스를 타입힌트로 지정해 `after`, `onSuccess`, `onFailure` 후킹 내에서 출력에 접근할 수 있습니다.

```
use Illuminate\Support\Stringable;

$schedule->command('emails:send')
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
`pingBefore`, `thenPing` 메서드를 활용하면 스케줄러가 예약 작업 실행 전후에 지정한 URL을 자동으로 ping(HTTP 요청)할 수 있습니다. 이 방법은 [Envoyer](https://envoyer.io)와 같은 외부 서비스에 작업 시작/종료 알림을 보낼 때 유용합니다.

```
$schedule->command('emails:send')
         ->daily()
         ->pingBefore($url)
         ->thenPing($url);
```

<!-- The `pingBeforeIf` and `thenPingIf` methods may be used to ping a given URL only if a given condition is `true`: -->
`pingBeforeIf` 및 `thenPingIf` 메서드는 특정 조건이 `true`일 때에만 URL을 ping하도록 할 수 있습니다.

```
$schedule->command('emails:send')
         ->daily()
         ->pingBeforeIf($condition, $url)
         ->thenPingIf($condition, $url);
```

<!-- The `pingOnSuccess` and `pingOnFailure` methods may be used to ping a given URL only if the task succeeds or fails. A failure indicates that the scheduled Artisan or system command terminated with a non-zero exit code: -->
`pingOnSuccess`, `pingOnFailure` 메서드는 작업 성공 또는 실패 시에만 URL로 ping을 보냅니다. 실패란 예약된 Artisan 또는 시스템 명령어가 0이 아닌 종료 코드로 종료된 경우입니다.

```
$schedule->command('emails:send')
         ->daily()
         ->pingOnSuccess($successUrl)
         ->pingOnFailure($failureUrl);
```

<!-- All of the ping methods require the Guzzle HTTP library. Guzzle is typically installed in all new Laravel projects by default, but, you may manually install Guzzle into your project using the Composer package manager if it has been accidentally removed: -->
이러한 ping 메서드들은 모두 Guzzle HTTP 라이브러리를 필요로 합니다. Guzzle은 일반적으로 새로운 Laravel 프로젝트에 기본 탑재되어 있지만, 만약 삭제된 경우 Composer로 재설치할 수 있습니다.

```shell
composer require guzzlehttp/guzzle
```

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- If needed, you may listen to [events](/docs/10.x/events) dispatched by the scheduler. Typically, event listener mappings will be defined within your application's `App\Providers\EventServiceProvider` class: -->
필요하다면, 스케줄러가 발생시키는 [events](/docs/10.x/events)를 리스닝할 수 있습니다. 보통 이벤트 리스너 매핑은 애플리케이션의 `App\Providers\EventServiceProvider` 클래스 안에 정의합니다.

```
/**
 * The event listener mappings for the application.
 *
 * @var array
 */
protected $listen = [
    'Illuminate\Console\Events\ScheduledTaskStarting' => [
        'App\Listeners\LogScheduledTaskStarting',
    ],

    'Illuminate\Console\Events\ScheduledTaskFinished' => [
        'App\Listeners\LogScheduledTaskFinished',
    ],

    'Illuminate\Console\Events\ScheduledBackgroundTaskFinished' => [
        'App\Listeners\LogScheduledBackgroundTaskFinished',
    ],

    'Illuminate\Console\Events\ScheduledTaskSkipped' => [
        'App\Listeners\LogScheduledTaskSkipped',
    ],

    'Illuminate\Console\Events\ScheduledTaskFailed' => [
        'App\Listeners\LogScheduledTaskFailed',
    ],
];
```
