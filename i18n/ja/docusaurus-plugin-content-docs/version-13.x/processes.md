# プロセス (Processes)

- [Introduction](#introduction)
- [プロセスの呼び出し](#invoking-processes)
    - [プロセスオプション](#process-options)
    - [プロセス出力](#process-output)
    - [Pipelines](#process-pipelines)
- [非同期プロセス](#asynchronous-processes)
    - [プロセス ID とシグナル](#process-ids-and-signals)
    - [非同期プロセスの出力](#asynchronous-process-output)
    - [非同期プロセスのタイムアウト](#asynchronous-process-timeouts)
- [同時プロセス](#concurrent-processes)
    - [ネーミングプールプロセス](#naming-pool-processes)
    - [プールのプロセス ID とシグナル](#pool-process-ids-and-signals)
- [Testing](#testing)
    - [偽装プロセス](#faking-processes)
    - [特定のプロセスを偽装する](#faking-specific-processes)
    - [プロセスシーケンスの偽装](#faking-process-sequences)
    - [非同期プロセスのライフサイクルを偽装する](#faking-asynchronous-process-lifecycles)
    - [利用可能なアサーション](#available-assertions)
    - [迷走プロセスの防止](#preventing-stray-processes)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、[Symfony プロセスコンポーネント](https://symfony.com/doc/current/components/process.html) を中心とした表現力豊かな最小限の API を提供し、Laravel アプリケーションから外部プロセスを簡単に呼び出すことができます。 Laravel のプロセス機能は、最も一般的なユースケースと素晴らしい開発者エクスペリエンスに焦点を当てています。

<a name="invoking-processes"></a>
## プロセスの呼び出し (Invoking Processes)

プロセスを呼び出すには、`Process` ファサードによって提供される `run` メソッドと `start` メソッドを使用できます。 `run` メソッドはプロセスを呼び出し、プロセスの実行が完了するまで待機しますが、`start` メソッドは非同期プロセスの実行に使用されます。このドキュメントでは両方のアプローチを検討します。まず、基本的な同期プロセスを呼び出してその結果を検査する方法を調べてみましょう。

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

もちろん、`run` メソッドによって返される `Illuminate\Contracts\Process\ProcessResult` インスタンスには、プロセス結果の検査に使用できるさまざまな便利なメソッドが用意されています。

```php
$result = Process::run('ls -la');

$result->command();
$result->successful();
$result->failed();
$result->output();
$result->errorOutput();
$result->exitCode();
```

<a name="throwing-exceptions"></a>
#### 例外のスロー

処理結果があり、終了コードがゼロより大きい (つまり失敗を示す) 場合に `Illuminate\Process\Exceptions\ProcessFailedException` のインスタンスをスローしたい場合は、`throw` メソッドと `throwIf` メソッドを使用できます。プロセスが失敗しなかった場合は、`ProcessResult` インスタンスが返されます。

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### プロセスオプション

もちろん、プロセスを呼び出す前にプロセスの動作をカスタマイズする必要がある場合があります。ありがたいことに、Laravel では作業ディレクトリ、タイムアウト、環境変数などのさまざまなプロセス機能を調整できます。

<a name="working-directory-path"></a>
#### 作業ディレクトリのパス

`path` メソッドを使用して、プロセスの作業ディレクトリを指定できます。このメソッドが呼び出されない場合、プロセスは現在実行中の PHP スクリプトの作業ディレクトリを継承します。

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 入力

`input` メソッドを使用して、プロセスの「標準入力」経由で入力を提供できます。

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### タイムアウト

デフォルトでは、プロセスは 60 秒以上実行された後に `Illuminate\Process\Exceptions\ProcessTimedOutException` のインスタンスをスローします。ただし、`timeout` メソッドを使用してこの動作をカスタマイズできます。

```php
$result = Process::timeout(120)->run('bash import.sh');
```

`timeout` メソッドと `idleTimeout` メソッドは、`CarbonInterval` インスタンスも受け入れます。

```php
use function Illuminate\Support\minutes;

$result = Process::timeout(minutes(2))->run('bash import.sh');
```

または、プロセス タイムアウトを完全に無効にしたい場合は、`forever` メソッドを呼び出します。

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` メソッドは、出力を返さずにプロセスを実行できる最大秒数を指定するために使用できます。

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 環境変数

環境変数は、`env` メソッドを介してプロセスに提供できます。呼び出されたプロセスは、システムによって定義されたすべての環境変数も継承します。

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

呼び出されたプロセスから継承された環境変数を削除したい場合は、その環境変数に値 `false` を指定できます。

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTYモード

`tty` メソッドを使用して、プロセスの TTY モードを有効にすることができます。 TTY モードは、プロセスの入出力をプログラムの入出力に接続し、プロセスが Vim や Nano などのエディターをプロセスとして開くことができるようにします。

```php
Process::forever()->tty()->run('vim');
```

> [!WARNING]
> TTY モードは Windows ではサポートされていません。

<a name="process-output"></a>
### プロセス出力

前述したように、プロセス出力には、プロセス結果の `output` (stdout) および `errorOutput` (stderr) メソッドを使用してアクセスできます。

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

ただし、`run` メソッドの 2 番目の引数としてクロージャーを渡すことによって、出力をリアルタイムで収集することもできます。クロージャーは 2 つの引数を受け取ります: 出力の「タイプ」 (`stdout` または `stderr`) と出力文字列自体です。

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel では、`seeInOutput` メソッドと `seeInErrorOutput` メソッドも提供しています。これらは、特定の文字列がプロセスの出力に含まれているかどうかを判断する便利な方法を提供します。

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### プロセス出力の無効化

プロセスが興味のない大量の出力を書き込んでいる場合は、出力の取得を完全に無効にすることでメモリを節約できます。これを実現するには、プロセスの構築中に `quietly` メソッドを呼び出します。

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### パイプライン

場合によっては、あるプロセスの出力を別のプロセスの入力にしたい場合があります。これは、プロセスの出力を別のプロセスに「パイプする」と呼ばれることがよくあります。 `Process` ファサードによって提供される `pipe` メソッドを使用すると、これを簡単に実現できます。 `pipe` メソッドは、パイプされたプロセスを同期的に実行し、パイプラインの最後のプロセスの処理結果を返します。

```php
use Illuminate\Process\Pipe;
use Illuminate\Support\Facades\Process;

$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
});

if ($result->successful()) {
    // ...
}
```

パイプラインを構成する個々のプロセスをカスタマイズする必要がない場合は、コマンド文字列の配列を `pipe` メソッドに渡すだけで済みます。

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

プロセス出力は、`pipe` メソッドの 2 番目の引数としてクロージャを渡すことによってリアルタイムで収集できます。クロージャーは 2 つの引数を受け取ります: 出力の「タイプ」 (`stdout` または `stderr`) と出力文字列自体です。

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

Laravel では、`as` メソッドを使用して、パイプライン内の各プロセスに文字列キーを割り当てることもできます。このキーは、`pipe` メソッドに提供される出力クロージャにも渡され、出力がどのプロセスに属するかを判断できるようになります。

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
}, function (string $type, string $output, string $key) {
    // ...
});
```

<a name="asynchronous-processes"></a>
## 非同期プロセス (Asynchronous Processes)

`run` メソッドはプロセスを同期的に呼び出しますが、`start` メソッドを使用してプロセスを非同期に呼び出すこともできます。これにより、プロセスがバックグラウンドで実行されている間、アプリケーションは他のタスクを実行し続けることができます。プロセスが呼び出されたら、`running` メソッドを使用して、プロセスがまだ実行中かどうかを確認できます。

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

お気づきかもしれませんが、`wait` メソッドを呼び出して、プロセスの実行が完了するまで待機し、`ProcessResult` インスタンスを取得できます。

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### プロセス ID とシグナル

`id` メソッドは、オペレーティング システムに割り当てられた、実行中のプロセスのプロセス ID を取得するために使用できます。

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` メソッドを使用して、実行中のプロセスに「シグナル」を送信できます。事前定義された信号定数のリストは、[PHP ドキュメント](https://www.php.net/manual/en/pcntl.constants.php) 内にあります。

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 非同期プロセスの出力

非同期プロセスの実行中は、`output` メソッドと `errorOutput` メソッドを使用して、その現在の出力全体にアクセスできます。ただし、`latestOutput` および `latestErrorOutput` を利用して、出力が最後に取得されてから発生したプロセスからの出力にアクセスすることもできます。

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

`run` メソッドと同様に、`start` メソッドの 2 番目の引数としてクロージャを渡すことにより、非同期プロセスから出力をリアルタイムで収集することもできます。クロージャは、出力の「タイプ」(`stdout` または `stderr`) と出力文字列自体の 2 つの引数を受け取ります。

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

プロセスが終了するまで待つ代わりに、`waitUntil` メソッドを使用して、プロセスの出力に基づいて待機を停止することができます。 `waitUntil` メソッドに与えられたクロージャが `true` を返すと、Laravel はプロセスが終了するのを待つのを停止します。

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 非同期プロセスのタイムアウト

非同期プロセスの実行中に、`ensureNotTimedOut` メソッドを使用してプロセスがタイムアウトしていないことを確認できます。プロセスがタイムアウトした場合、このメソッドは [タイムアウト例外](#timeouts) をスローします。

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    $process->ensureNotTimedOut();

    // ...

    sleep(1);
}
```

<a name="concurrent-processes"></a>
## 同時プロセス (Concurrent Processes)

Laravel を使用すると、同時非同期プロセスのプールを簡単に管理できるため、多くのタスクを同時に簡単に実行できます。まず、`pool` メソッドを呼び出します。このメソッドは、`Illuminate\Process\Pool` のインスタンスを受け取るクロージャーを受け入れます。

このクロージャ内で、プールに属するプロセスを定義できます。 `start` メソッドを介してプロセス プールが開始されると、`running` メソッドを介して実行中のプロセスの [collection](/docs/{{version}}/collections) にアクセスできます。

```php
use Illuminate\Process\Pool;
use Illuminate\Support\Facades\Process;

$pool = Process::pool(function (Pool $pool) {
    $pool->path(__DIR__)->command('bash import-1.sh');
    $pool->path(__DIR__)->command('bash import-2.sh');
    $pool->path(__DIR__)->command('bash import-3.sh');
})->start(function (string $type, string $output, int $key) {
    // ...
});

while ($pool->running()->isNotEmpty()) {
    // ...
}

$results = $pool->wait();
```

ご覧のとおり、すべてのプール プロセスの実行が完了するまで待機し、`wait` メソッドを介して結果を解決できます。 `wait` メソッドは、キーによってプール内の各プロセスの `ProcessResult` インスタンスにアクセスできるようにする配列アクセス可能なオブジェクトを返します。

```php
$results = $pool->wait();

echo $results[0]->output();
```

または、便宜上、`concurrently` メソッドを使用して非同期プロセス プールを開始し、その結果をすぐに待機することもできます。これを PHP の配列分割機能と組み合わせると、特に表現力豊かな構文を提供できます。

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### ネーミングプールプロセス

数値キーを使用してプロセス プールの結果にアクセスすることは、あまり表現力がありません。したがって、Laravelでは、`as`メソッドを介してプール内の各プロセスに文字列キーを割り当てることができます。このキーは、`start` メソッドに提供されたクロージャにも渡され、出力がどのプロセスに属しているかを判断できるようになります。

```php
$pool = Process::pool(function (Pool $pool) {
    $pool->as('first')->command('bash import-1.sh');
    $pool->as('second')->command('bash import-2.sh');
    $pool->as('third')->command('bash import-3.sh');
})->start(function (string $type, string $output, string $key) {
    // ...
});

$results = $pool->wait();

return $results['first']->output();
```

<a name="pool-process-ids-and-signals"></a>
### プールのプロセス ID とシグナル

プロセス プールの `running` メソッドは、プール内で呼び出されたすべてのプロセスのコレクションを提供するため、基になるプールのプロセス ID に簡単にアクセスできます。

```php
$processIds = $pool->running()->each->id();
```

また、便宜上、プロセス プールで `signal` メソッドを呼び出して、プール内のすべてのプロセスにシグナルを送信することもできます。

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## テスト (Testing)

多くの Laravel サービスは、テストを簡単かつ表現力豊かに作成できるようにする機能を提供しており、Laravel のプロセス サービスも例外ではありません。 `Process` ファサードの `fake` メソッドを使用すると、プロセスが呼び出されたときにスタブ/ダミーの結果を返すように Laravel に指示できます。

<a name="faking-processes"></a>
### 偽装プロセス

Laravel のプロセスを偽装する機能を調べるために、プロセスを呼び出すルートを想像してみましょう。

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

このルートをテストするとき、引数なしで `Process` ファサードの `fake` メソッドを呼び出すことで、呼び出されたすべてのプロセスに対して偽の成功したプロセス結果を返すように Laravel に指示できます。さらに、特定のプロセスが「実行」されたことを [assert](#available-assertions) で確認することもできます。

```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // Simple process assertion...
    Process::assertRan('bash import.sh');

    // Or, inspecting the process configuration...
    Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
        return $process->command === 'bash import.sh' &&
               $process->timeout === 60;
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_process_is_invoked(): void
    {
        Process::fake();

        $response = $this->get('/import');

        // Simple process assertion...
        Process::assertRan('bash import.sh');

        // Or, inspecting the process configuration...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

説明したように、`Process` ファサードで `fake` メソッドを呼び出すと、出力なしで常に成功したプロセス結果を返すように Laravel に指示されます。ただし、`Process` ファサードの `result` メソッドを使用すると、偽のプロセスの出力コードと終了コードを簡単に指定できます。

```php
Process::fake([
    '*' => Process::result(
        output: 'Test output',
        errorOutput: 'Test error output',
        exitCode: 1,
    ),
]);
```

<a name="faking-specific-processes"></a>
### 特定のプロセスを偽装する

前の例でお気づきかと思いますが、`Process` ファサードでは、配列を `fake` メソッドに渡すことで、プロセスごとに異なる偽の結果を指定できます。

配列のキーは、偽装したいコマンド パターンとそれに関連する結果を表す必要があります。 `*` 文字はワイルドカード文字として使用できます。偽装されていないプロセス コマンドは実際に呼び出されます。 `Process` ファサードの `result` メソッドを使用して、次のコマンドのスタブ/偽の結果を構築できます。

```php
Process::fake([
    'cat *' => Process::result(
        output: 'Test "cat" output',
    ),
    'ls *' => Process::result(
        output: 'Test "ls" output',
    ),
]);
```

偽のプロセスの終了コードやエラー出力をカスタマイズする必要がない場合は、偽のプロセスの結果を単純な文字列として指定する方が便利な場合があります。

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### プロセスシーケンスの偽装

テストしているコードが同じコマンドで複数のプロセスを呼び出す場合、各プロセス呼び出しに異なる偽のプロセス結果を割り当てることができます。これは、`Process` ファサードの `sequence` メソッドを通じて実行できます。

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 非同期プロセスのライフサイクルを偽装する

これまで、主に、`run` メソッドを使用して同期的に呼び出される偽装プロセスについて説明してきました。ただし、`start` 経由で呼び出される非同期プロセスと対話するコードをテストしようとしている場合は、偽のプロセスを記述するためのより洗練されたアプローチが必要になる場合があります。

たとえば、非同期プロセスと対話する次のルートを想像してみましょう。

```php
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    $process = Process::start('bash import.sh');

    while ($process->running()) {
        Log::info($process->latestOutput());
        Log::info($process->latestErrorOutput());
    }

    return 'Done';
});
```

このプロセスを適切に偽装するには、`running` メソッドが `true` を返す回数を記述できる必要があります。さらに、順番に返される複数行の出力を指定したい場合があります。これを実現するには、`Process` ファサードの `describe` メソッドを使用します。

```php
Process::fake([
    'bash import.sh' => Process::describe()
        ->output('First line of standard output')
        ->errorOutput('First line of error output')
        ->output('Second line of standard output')
        ->exitCode(0)
        ->iterations(3),
]);
```

上の例を詳しく見てみましょう。 `output` メソッドと `errorOutput` メソッドを使用すると、順番に返される複数行の出力を指定できます。 `exitCode` メソッドを使用して、偽のプロセスの最終終了コードを指定できます。最後に、`iterations` メソッドを使用して、`running` メソッドが `true` を返す回数を指定できます。

<a name="available-assertions"></a>
### 利用可能なアサーション

[以前に議論した](#faking-processes) として、Laravel は機能テスト用にいくつかのプロセス アサーションを提供します。これらの各主張については、以下で説明します。

<a name="assert-process-ran"></a>
#### アサートラン

指定されたプロセスが呼び出されたことをアサートします。

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` メソッドは、プロセスのインスタンスとプロセス結果を受け取るクロージャーも受け入れます。これにより、プロセスの構成されたオプションを検査できるようになります。このクロージャが `true` を返す場合、アサーションは「合格」します。

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`assertRan` クロージャに渡される `$process` は `Illuminate\Process\PendingProcess` のインスタンスであり、`$result` は `Illuminate\Contracts\Process\ProcessResult` のインスタンスです。

<a name="assert-process-didnt-run"></a>
#### アサートしませんでした

指定されたプロセスが呼び出されなかったことをアサートします。

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertRan` メソッドと同様、`assertDidntRun` メソッドもクロージャを受け入れます。クロージャはプロセスのインスタンスとプロセス結果を受け取り、プロセスの構成されたオプションを検査できます。このクロージャが `true` を返す場合、アサーションは「失敗」します。

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### アサートRanTimes

指定されたプロセスが指定された回数呼び出されたことをアサートします。

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` メソッドはクロージャーも受け入れます。これにより、`PendingProcess` および `ProcessResult` のインスタンスを受け取り、プロセスの構成されたオプションを検査できるようになります。このクロージャが `true` を返し、プロセスが指定された回数呼び出された場合、アサーションは「合格」します。

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 迷走プロセスの防止

個々のテストまたはテスト スイート全体を通じて、呼び出されたすべてのプロセスが偽装されていることを確認したい場合は、`preventStrayProcesses` メソッドを呼び出すことができます。このメソッドを呼び出した後、対応する偽の結果を持たないプロセスは、実際のプロセスを開始するのではなく、例外をスローします。

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// Fake response is returned...
Process::run('ls -la');

// An exception is thrown...
Process::run('bash import.sh');
```

