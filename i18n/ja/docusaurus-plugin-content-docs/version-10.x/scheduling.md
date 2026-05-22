# タスクのスケジュール設定 (Task Scheduling)

- [Introduction](#introduction)
- [スケジュールの定義](#defining-schedules)
    - [Artisan コマンドのスケジュール設定](#scheduling-artisan-commands)
    - [キューに入れられたジョブのスケジュール設定](#scheduling-queued-jobs)
    - [シェルコマンドのスケジュール設定](#scheduling-shell-commands)
    - [スケジュール頻度のオプション](#schedule-frequency-options)
    - [Timezones](#timezones)
    - [タスクの重複を防ぐ](#preventing-task-overlaps)
    - [1 つのサーバーでタスクを実行する](#running-tasks-on-one-server)
    - [バックグラウンドタスク](#background-tasks)
    - [メンテナンスモード](#maintenance-mode)
- [スケジューラの実行](#running-the-scheduler)
    - [1分未満のスケジュールされたタスク](#sub-minute-scheduled-tasks)
    - [スケジューラをローカルで実行する](#running-the-scheduler-locally)
- [タスクの出力](#task-output)
- [タスクフック](#task-hooks)
- [Events](#events)

<a name="introduction"></a>
## 導入 (Introduction)

以前は、サーバー上でスケジュールする必要があるタスクごとに cron 構成エントリを作成したかもしれません。ただし、タスクスケジュールがソース管理に含まれなくなり、既存の cron エントリを表示したり追加のエントリを追加するにはサーバーに SSH 接続する必要があるため、これはすぐに面倒になる可能性があります。

Laravel のコマンド スケジューラは、サーバー上でスケジュールされたタスクを管理するための新しいアプローチを提供します。スケジューラを使用すると、Laravel アプリケーション自体内でコマンド スケジュールを流暢かつ表現力豊かに定義できます。スケジューラを使用する場合、サーバー上に必要な cron エントリは 1 つだけです。タスクスケジュールは、`app/Console/Kernel.php` ファイルの `schedule` メソッドで定義されます。開始しやすいように、メソッド内で簡単な例が定義されています。

<a name="defining-schedules"></a>
## スケジュールの定義 (Defining Schedules)

スケジュールされたタスクはすべて、アプリケーションの `App\Console\Kernel` クラスの `schedule` メソッドで定義できます。まず、例を見てみましょう。この例では、毎日深夜に呼び出されるクロージャをスケジュールします。クロージャ内でデータベース クエリを実行してテーブルをクリアします。

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

クロージャを使用したスケジュールに加えて、[呼び出し可能なオブジェクト](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke) をスケジュールすることもできます。呼び出し可能なオブジェクトは、`__invoke` メソッドを含む単純な PHP クラスです。

    $schedule->call(new DeleteRecentUsers)->daily();

スケジュールされたタスクの概要と次回の実行スケジュールを確認したい場合は、`schedule:list` Artisan コマンドを使用できます。

```bash
php artisan schedule:list
```

<a name="scheduling-artisan-commands"></a>
### Artisan コマンドのスケジュール設定

クロージャのスケジュールに加えて、[Artisan コマンド](/docs/{{version}}/artisan) およびシステム コマンドもスケジュールできます。たとえば、`command` メソッドを使用して、コマンドの名前またはクラスを使用してArtisan コマンドをスケジュールできます。

コマンドのクラス名を使用してArtisan コマンドをスケジュールする場合、コマンドの呼び出し時にコマンドに指定する必要がある追加のコマンドライン引数の配列を渡すことができます。

    use App\Console\Commands\SendEmailsCommand;

    $schedule->command('emails:send Taylor --force')->daily();

    $schedule->command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();

<a name="scheduling-queued-jobs"></a>
### キューに入れられたジョブのスケジュール設定

`job` メソッドは、[キューに入れられたジョブ](/docs/{{version}}/queues) をスケジュールするために使用できます。このメソッドは、ジョブをキューに入れるクロージャを定義する `call` メソッドを使用せずに、キューに入れられたジョブをスケジュールする便利な方法を提供します。

    use App\Jobs\Heartbeat;

    $schedule->job(new Heartbeat)->everyFiveMinutes();

オプションの 2 番目と 3 番目の引数を `job` メソッドに指定して、ジョブをキューに入れるために使用するキュー名とキュー接続を指定できます。

    use App\Jobs\Heartbeat;

    // Dispatch the job to the "heartbeats" queue on the "sqs" connection...
    $schedule->job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();

<a name="scheduling-shell-commands"></a>
### シェルコマンドのスケジュール設定

`exec` メソッドは、オペレーティング システムにコマンドを発行するために使用できます。

    $schedule->exec('node /home/forge/script.js')->daily();

<a name="schedule-frequency-options"></a>
### スケジュール頻度のオプション

指定した間隔でタスクを実行するように構成する方法の例をいくつか見てきました。ただし、タスクに割り当てることができるタスクスケジュールの頻度は他にもたくさんあります。

<div class="overflow-auto">

方法 |説明
------------- | -------------
`->cron('* * * * *');` |  カスタム cron スケジュールでタスクを実行する
`->everySecond();` |  タスクを毎秒実行する
`->everyTwoSeconds();` |  タスクを 2 秒ごとに実行する
`->everyFiveSeconds();` |  タスクを 5 秒ごとに実行する
`->everyTenSeconds();` |  10 秒ごとにタスクを実行する
`->everyFifteenSeconds();` |  15 秒ごとにタスクを実行する
`->everyTwentySeconds();` |  タスクを 20 秒ごとに実行する
`->everyThirtySeconds();` |  30 秒ごとにタスクを実行する
`->everyMinute();` |  タスクを毎分実行する
`->everyTwoMinutes();` |  タスクを 2 分ごとに実行する
`->everyThreeMinutes();` |  タスクを 3 分ごとに実行する
`->everyFourMinutes();` |  タスクを 4 分ごとに実行する
`->everyFiveMinutes();` |  タスクを 5 分ごとに実行する
`->everyTenMinutes();` |  タスクを 10 分ごとに実行する
`->everyFifteenMinutes();` |  タスクを 15 分ごとに実行する
`->everyThirtyMinutes();` |  タスクを 30 分ごとに実行する
`->hourly();` |  タスクを 1 時間ごとに実行する
`->hourlyAt(17);` |  タスクを毎時 17 分に実行します
`->everyOddHour($minutes = 0);` |  奇数時間ごとにタスクを実行する
`->everyTwoHours($minutes = 0);` |  タスクを 2 時間ごとに実行する
`->everyThreeHours($minutes = 0);` |  タスクを 3 時間ごとに実行する
`->everyFourHours($minutes = 0);` |  タスクを 4 時間ごとに実行する
`->everySixHours($minutes = 0);` |  タスクを 6 時間ごとに実行する
`->daily();` |  毎日深夜にタスクを実行する
`->dailyAt('13:00');` |  毎日 13:00 にタスクを実行します
`->twiceDaily(1, 13);` |  タスクを毎日 1:00 と 13:00 に実行します
`->twiceDailyAt(1, 13, 15);` |  毎日 1:15 と 13:15 にタスクを実行します
`->weekly();` |  タスクを毎週日曜日の 00:00 に実行します
`->weeklyOn(1, '8:00');` |  タスクを毎週月曜日の 8:00 に実行します
`->monthly();` |  タスクを毎月 1 日の 00:00 に実行します。
`->monthlyOn(4, '15:00');` |  毎月 4 日の 15:00 にタスクを実行します
`->twiceMonthly(1, 16, '13:00');` |  毎月 1 日と 16 日の 13:00 にタスクを実行します。
`->lastDayOfMonth('15:00');` |毎月の最終日の 15:00 にタスクを実行します。
`->quarterly();` |  各四半期の初日の 00:00 にタスクを実行します。
`->quarterlyOn(4, '14:00');` |  タスクを四半期ごとに 4 日の 14:00 に実行します。
`->yearly();` |  毎年初日の 00:00 にタスクを実行します。
`->yearlyOn(6, 1, '17:00');` |  毎年 6 月 1 日の 17:00 にタスクを実行します。
`->timezone('America/New_York');` |タスクのタイムゾーンを設定する

</div>

これらの方法を追加の制約と組み合わせて、特定の曜日にのみ実行するさらに細かく調整されたスケジュールを作成できます。たとえば、コマンドを毎週月曜日に実行するようにスケジュールできます。

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

追加のスケジュール制約のリストは以下にあります。

<div class="overflow-auto">

方法 |説明
------------- | -------------
`->weekdays();` |  タスクを平日に限定する
`->weekends();` |  タスクを週末に限定する
`->sundays();` |  タスクを日曜日に限定する
`->mondays();` |  タスクを月曜日に限定する
`->tuesdays();` |  タスクを火曜日に限定する
`->wednesdays();` |  タスクを水曜日に限定する
`->thursdays();` |  タスクを木曜日に限定する
`->fridays();` |  タスクを金曜日に限定する
`->saturdays();` |  タスクを土曜日に限定する
`->days(array\|mixed);`  |  タスクを特定の日に限定する
`->between($startTime, $endTime);` |  開始時間と終了時間の間に実行するタスクを制限する
`->unlessBetween($startTime, $endTime);` |  開始時間と終了時間の間にタスクが実行されないように制限する
`->when(Closure);` |  真実のテストに基づいてタスクを制限する
`->environments($env);` |  タスクを特定の環境に限定する

</div>

<a name="day-constraints"></a>
#### 曜日の制約

`days` メソッドを使用すると、タスクの実行を特定の曜日に制限できます。たとえば、日曜日と水曜日に 1 時間ごとにコマンドを実行するようにスケジュールできます。

    $schedule->command('emails:send')
                    ->hourly()
                    ->days([0, 3]);

あるいは、タスクを実行する日を定義するときに、`Illuminate\Console\Scheduling\Schedule` クラスで利用可能な定数を使用することもできます。

    use Illuminate\Console\Scheduling\Schedule;

    $schedule->command('emails:send')
                    ->hourly()
                    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);

<a name="between-time-constraints"></a>
#### 時間制約の間

`between` メソッドは、時刻に基づいてタスクの実行を制限するために使用できます。

    $schedule->command('emails:send')
                        ->hourly()
                        ->between('7:00', '22:00');

同様に、`unlessBetween` メソッドを使用して、一定期間タスクの実行を除外できます。

    $schedule->command('emails:send')
                        ->hourly()
                        ->unlessBetween('23:00', '4:00');

<a name="truth-test-constraints"></a>
#### 真実試験の制約

`when` メソッドは、指定された真理値テストの結果に基づいてタスクの実行を制限するために使用できます。つまり、指定されたクロージャが `true` を返す場合、他の制約条件によってタスクの実行が妨げられない限り、タスクは実行されます。

    $schedule->command('emails:send')->daily()->when(function () {
        return true;
    });

`skip` メソッドは、`when` の逆と見なすことができます。 `skip` メソッドが `true` を返した場合、スケジュールされたタスクは実行されません。

    $schedule->command('emails:send')->daily()->skip(function () {
        return true;
    });

連鎖した `when` メソッドを使用する場合、スケジュールされたコマンドは、すべての `when` 条件が `true` を返した場合にのみ実行されます。

<a name="environment-constraints"></a>
#### 環境の制約

`environments` メソッドは、指定された環境 (`APP_ENV` [環境変数](/docs/{{version}}/configuration#environment-configuration) で定義) でのみタスクを実行するために使用できます。

    $schedule->command('emails:send')
                ->daily()
                ->environments(['staging', 'production']);

<a name="timezones"></a>
### タイムゾーン

`timezone` メソッドを使用すると、スケジュールされたタスクの時間が特定のタイムゾーン内で解釈されるように指定できます。

    $schedule->command('report:generate')
             ->timezone('America/New_York')
             ->at('2:00')

スケジュールされたすべてのタスクに同じタイムゾーンを繰り返し割り当てる場合は、`App\Console\Kernel` クラスで `scheduleTimezone` メソッドを定義するとよいでしょう。このメソッドは、スケジュールされたすべてのタスクに割り当てる必要があるデフォルトのタイムゾーンを返す必要があります。

    use DateTimeZone;

    /**
     * Get the timezone that should be used by default for scheduled events.
     */
    protected function scheduleTimezone(): DateTimeZone|string|null
    {
        return 'America/Chicago';
    }

> [!WARNING]  
> 一部のタイムゾーンでは夏時間が採用されていることに注意してください。夏時間の変更が発生すると、スケジュールされたタスクが 2 回実行されるか、まったく実行されない場合があります。このため、可能な限りタイムゾーンのスケジュールを回避することをお勧めします。

<a name="preventing-task-overlaps"></a>
### タスクの重複を防ぐ

デフォルトでは、スケジュールされたタスクは、タスクの前のインスタンスがまだ実行中であっても実行されます。これを防ぐには、`withoutOverlapping` メソッドを使用します。

    $schedule->command('emails:send')->withoutOverlapping();

この例では、`emails:send` [Artisan コマンド](/docs/{{version}}/artisan) がまだ実行されていない場合、1 分ごとに実行されます。 `withoutOverlapping` メソッドは、実行時間が大幅に異なるタスクがあり、特定のタスクにかかる時間を正確に予測できない場合に特に便利です。

必要に応じて、「重複なし」ロックの有効期限が切れるまでに何分経過するかを指定できます。デフォルトでは、ロックは 24 時間後に期限切れになります。

    $schedule->command('emails:send')->withoutOverlapping(10);

バックグラウンドで、`withoutOverlapping` メソッドはアプリケーションの [cache](/docs/{{version}}/cache) を利用してロックを取得します。必要に応じて、`schedule:clear-cache` Artisan コマンドを使用してこれらのキャッシュ ロックをクリアできます。これは通常、予期しないサーバーの問題によりタスクが停止した場合にのみ必要になります。

<a name="running-tasks-on-one-server"></a>
### 1 つのサーバーでタスクを実行する

> [!WARNING]  
> この機能を利用するには、アプリケーションは、アプリケーションのデフォルトのキャッシュ ドライバとして `database`、`memcached`、`dynamodb`、または `redis` キャッシュ ドライバを使用している必要があります。さらに、すべてのサーバーが同じ中央キャッシュ サーバーと通信している必要があります。

アプリケーションのスケジューラが複数のサーバーで実行されている場合は、スケジュールされたジョブを単一のサーバーでのみ実行するように制限できます。たとえば、毎週金曜日の夜に新しいレポートを生成するスケジュールされたタスクがあるとします。タスク スケジューラが 3 台のワーカー サーバーで実行されている場合、スケジュールされたタスクは 3 台すべてのサーバーで実行され、レポートが 3 回生成されます。良くない！

タスクを 1 つのサーバー上でのみ実行する必要があることを示すには、スケジュールされたタスクを定義するときに `onOneServer` メソッドを使用します。タスクを取得した最初のサーバーは、ジョブのアトミック ロックを確保し、他のサーバーが同じタスクを同時に実行できないようにします。

    $schedule->command('report:generate')
                    ->fridays()
                    ->at('17:00')
                    ->onOneServer();

<a name="naming-unique-jobs"></a>
#### 単一サーバージョブの名前付け

場合によっては、単一サーバー上でジョブの各順列を実行するように Laravel に指示しながら、同じジョブを異なるパラメーターでディスパッチするようにスケジュールする必要がある場合があります。これを実現するには、`name` メソッドを使用して、各スケジュール定義に一意の名前を割り当てることができます。

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

同様に、スケジュールされたクロージャが 1 つのサーバー上で実行される場合は、名前を割り当てる必要があります。

```php
$schedule->call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```


<a name="background-tasks"></a>
### バックグラウンドタスク

デフォルトでは、同時にスケジュールされた複数のタスクは、`schedule` メソッドで定義された順序に基づいて順次実行されます。長時間実行されるタスクがある場合、後続のタスクの開始が予想より大幅に遅くなる可能性があります。タスクをバックグラウンドで実行してすべてを同時に実行したい場合は、`runInBackground` メソッドを使用できます。

    $schedule->command('analytics:report')
             ->daily()
             ->runInBackground();

> [!WARNING]  
> `runInBackground` メソッドは、`command` および `exec` メソッドを介してタスクをスケジュールする場合にのみ使用できます。

<a name="maintenance-mode"></a>
### メンテナンスモード

アプリケーションが [メンテナンスモード](/docs/{{version}}/configuration#maintenance-mode) にあるときは、アプリケーションのスケジュールされたタスクは実行されません。これは、サーバー上で実行している未完了のメンテナンスがタスクによって妨げられることが望ましくないためです。ただし、メンテナンス モードでもタスクを強制的に実行したい場合は、タスクを定義するときに `evenInMaintenanceMode` メソッドを呼び出すことができます。

    $schedule->command('emails:send')->evenInMaintenanceMode();

<a name="running-the-scheduler"></a>
## スケジューラの実行 (Running the Scheduler)

スケジュールされたタスクを定義する方法を学習したので、実際にサーバー上でタスクを実行する方法について説明します。 `schedule:run` Artisan コマンドは、スケジュールされたタスクをすべて評価し、サーバーの現在時刻に基づいて実行する必要があるかどうかを判断します。

したがって、Laravel のスケジューラーを使用する場合、`schedule:run` コマンドを毎分実行する単一の cron 構成エントリーをサーバーに追加するだけで済みます。サーバーに cron エントリを追加する方法がわからない場合は、cron エントリを管理できる [Laravel Forge](https://forge.laravel.com) などのサービスの使用を検討してください。

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```

<a name="sub-minute-scheduled-tasks"></a>
### 1分未満のスケジュールされたタスク

ほとんどのオペレーティング システムでは、cron ジョブの実行は 1 分あたり最大 1 回に制限されています。ただし、Laravel のスケジューラーを使用すると、タスクをより頻繁な間隔 (1 秒に 1 回など) で実行するようにスケジュールできます。

    $schedule->call(function () {
        DB::table('recent_users')->delete();
    })->everySecond();

アプリケーション内で 1 分未満のタスクが定義されている場合、`schedule:run` コマンドはすぐに終了するのではなく、現在の 1 分間が終了するまで実行を続けます。これにより、コマンドは 1 分を通して必要なすべてのサブタスク タスクを呼び出すことができます。

実行に予想よりも時間がかかる 1 分未満のタスクは、後続の 1 分未満のタスクの実行を遅らせる可能性があるため、すべての 1 分未満のタスクがキューに入れられたジョブまたはバックグラウンド コマンドをディスパッチして、実際のタスク処理を処理することをお勧めします。

    use App\Jobs\DeleteRecentUsers;

    $schedule->job(new DeleteRecentUsers)->everyTenSeconds();

    $schedule->command('users:delete')->everyTenSeconds()->runInBackground();

<a name="interrupting-sub-minute-tasks"></a>
#### 1 分未満のタスクの中断

`schedule:run` コマンドは、1 分未満のタスクが定義されている場合、呼び出しの 1 分間ずっと実行されるため、アプリケーションのデプロイ時にコマンドを中断する必要がある場合があります。それ以外の場合、すでに実行中の `schedule:run` コマンドのインスタンスは、現在の分が終了するまで、アプリケーションの以前にデプロイされたコードを使用し続けます。

進行中の `schedule:run` 呼び出しを中断するには、アプリケーションの展開スクリプトに `schedule:interrupt` コマンドを追加します。このコマンドは、アプリケーションのデプロイが完了した後に呼び出す必要があります。

```shell
php artisan schedule:interrupt
```

<a name="running-the-scheduler-locally"></a>
### スケジューラをローカルで実行する

通常、ローカル開発マシンにスケジューラ cron エントリを追加しません。代わりに、`schedule:work` Artisan コマンドを使用できます。このコマンドはフォアグラウンドで実行され、コマンドを終了するまで毎分スケジューラを呼び出します。

```shell
php artisan schedule:work
```

<a name="task-output"></a>
## タスクの出力 (Task Output)

Laravel スケジューラーは、スケジュールされたタスクによって生成された出力を操作するための便利なメソッドをいくつか提供します。まず、`sendOutputTo` メソッドを使用して、後で検査できるように出力をファイルに送信できます。

    $schedule->command('emails:send')
             ->daily()
             ->sendOutputTo($filePath);

出力を特定のファイルに追加したい場合は、`appendOutputTo` メソッドを使用できます。

    $schedule->command('emails:send')
             ->daily()
             ->appendOutputTo($filePath);

`emailOutputTo` メソッドを使用すると、出力を選択した電子メール アドレスに電子メールで送信できます。タスクの出力を電子メールで送信する前に、Laravel の [電子メールサービス](/docs/{{version}}/mail) を構成する必要があります。

    $schedule->command('report:generate')
             ->daily()
             ->sendOutputTo($filePath)
             ->emailOutputTo('taylor@example.com');

スケジュールされた Artisan またはシステム コマンドがゼロ以外の終了コードで終了した場合にのみ出力を電子メールで送信する場合は、`emailOutputOnFailure` メソッドを使用します。

    $schedule->command('report:generate')
             ->daily()
             ->emailOutputOnFailure('taylor@example.com');

> [!WARNING]  
> `emailOutputTo`、`emailOutputOnFailure`、`sendOutputTo`、および `appendOutputTo` メソッドは、`command` および `exec` メソッド専用です。

<a name="task-hooks"></a>
## タスクフック (Task Hooks)

`before` メソッドと `after` メソッドを使用すると、スケジュールされたタスクの実行前後に実行されるコードを指定できます。

    $schedule->command('emails:send')
             ->daily()
             ->before(function () {
                 // The task is about to execute...
             })
             ->after(function () {
                 // The task has executed...
             });

`onSuccess` メソッドと `onFailure` メソッドを使用すると、スケジュールされたタスクが成功または失敗した場合に実行されるコードを指定できます。失敗は、スケジュールされたArtisanまたはシステム コマンドがゼロ以外の終了コードで終了したことを示します。

    $schedule->command('emails:send')
             ->daily()
             ->onSuccess(function () {
                 // The task succeeded...
             })
             ->onFailure(function () {
                 // The task failed...
             });

コマンドから出力が利用可能な場合は、フックのクロージャ定義の `$output` 引数として `Illuminate\Support\Stringable` インスタンスをタイプヒントすることで、`after`、`onSuccess`、または `onFailure` フックで出力にアクセスできます。

    use Illuminate\Support\Stringable;

    $schedule->command('emails:send')
             ->daily()
             ->onSuccess(function (Stringable $output) {
                 // The task succeeded...
             })
             ->onFailure(function (Stringable $output) {
                 // The task failed...
             });

<a name="pinging-urls"></a>
#### URL の ping

`pingBefore` メソッドと `thenPing` メソッドを使用すると、スケジューラはタスクの実行前または実行後に、指定された URL に自動的に ping を送信できます。このメソッドは、スケジュールされたタスクの実行が開始または終了したことを [Envoyer](https://envoyer.io) などの外部サービスに通知するのに役立ちます。

    $schedule->command('emails:send')
             ->daily()
             ->pingBefore($url)
             ->thenPing($url);

`pingBeforeIf` メソッドと `thenPingIf` メソッドは、特定の条件が `true` の場合にのみ、特定の URL に ping を実行するために使用できます。

    $schedule->command('emails:send')
             ->daily()
             ->pingBeforeIf($condition, $url)
             ->thenPingIf($condition, $url);

`pingOnSuccess` メソッドと `pingOnFailure` メソッドは、タスクが成功または失敗した場合にのみ、特定の URL に ping を送信するために使用できます。失敗は、スケジュールされたArtisanまたはシステム コマンドがゼロ以外の終了コードで終了したことを示します。

    $schedule->command('emails:send')
             ->daily()
             ->pingOnSuccess($successUrl)
             ->pingOnFailure($failureUrl);

すべての ping メソッドには Guzzle HTTP ライブラリが必要です。 Guzzle は通常、デフォルトですべての新しい Laravel プロジェクトにインストールされますが、Guzzle が誤って削除された場合は、Composer パッケージ マネージャーを使用してプロジェクトに手動でインストールできます。

```shell
composer require guzzlehttp/guzzle
```

<a name="events"></a>
## イベント (Events)

必要に応じて、スケジューラによってディスパッチされた [events](/docs/{{version}}/events) を聞くことができます。通常、イベント リスナ マッピングはアプリケーションの `App\Providers\EventServiceProvider` クラス内で定義されます。

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

