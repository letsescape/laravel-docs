# 프로세스 (Processes)

- [소개](#introduction)
- [프로세스 호출](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID 및 시그널](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
    - [비동기 프로세스 타임아웃](#asynchronous-process-timeouts)
- [동시 프로세스](#concurrent-processes)
    - [풀 내 프로세스 명명](#naming-pool-processes)
    - [풀 프로세스 ID 및 시그널](#pool-process-ids-and-signals)
- [테스트](#testing)
    - [프로세스 페이크 처리](#faking-processes)
    - [특정 프로세스 페이크](#faking-specific-processes)
    - [프로세스 시퀀스 페이크](#faking-process-sequences)
    - [비동기 프로세스 생명주기 페이크](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 Assertion](#available-assertions)
    - [낙오 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html)를 기반으로 한 표현력 있고 최소한의 API를 제공합니다. 이를 통해 Laravel 애플리케이션에서 외부 프로세스를 간편하게 호출할 수 있습니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례에 초점을 맞추었으며, 훌륭한 개발 경험을 제공합니다.

<a name="invoking-processes"></a>
## 프로세스 호출 (Invoking Processes)

프로세스를 호출하려면, `Process` 파사드에서 제공하는 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 호출하고 완료될 때까지 대기하는 동기 실행 방식을 제공합니다. 반면, `start` 메서드는 비동기 방식으로 프로세스를 실행할 때 사용합니다. 이 문서에서는 두 가지 방식을 모두 다룹니다. 우선, 기본적인 동기 프로세스를 호출하고 결과를 확인하는 방법을 살펴보겠습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스에는 프로세스 결과를 확인할 수 있는 다양한 유용한 메서드가 포함되어 있습니다:

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
#### 예외 던지기

프로세스 결과를 가지고 있으며, 종료 코드가 0보다 큰 경우(즉, 실패를 나타냄) `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 던지고 싶다면, `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면, `ProcessResult` 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션 (Process Options)

프로세스를 호출하기 전에 동작을 사용자 정의해야 할 수도 있습니다. Laravel에서는 작업 디렉터리, 타임아웃, 환경 변수와 같은 다양한 프로세스 옵션을 손쉽게 조정할 수 있습니다.

<a name="working-directory-path"></a>
#### 작업 디렉터리 경로 지정

`path` 메서드를 사용하여 프로세스의 작업 디렉터리를 지정할 수 있습니다. 이 메서드를 사용하지 않으면, 프로세스는 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속합니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력값 지정

`input` 메서드를 사용하여 프로세스의 "표준 입력"을 통해 값을 전달할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로, 프로세스는 60초 이상 실행되면 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 던집니다. 이 동작은 `timeout` 메서드를 통해 조정할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```

또한, 프로세스 타임아웃을 완전히 비활성화하려면 `forever` 메서드를 호출하면 됩니다:

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드는 프로세스가 아무 출력 없이 실행될 수 있는 최대 초를 지정할 때 사용합니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수(Environment Variables)

`env` 메서드를 사용하여 프로세스에 환경 변수를 제공할 수 있습니다. 호출된 프로세스는 시스템에 정의된 모든 환경 변수도 상속합니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속받은 환경 변수를 프로세스에서 제거하고 싶다면 해당 환경 변수의 값을 `false`로 지정하면 됩니다:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드(TTY Mode)

`tty` 메서드를 사용하면 프로세스에 TTY 모드를 활성화할 수 있습니다. 이를 통해 프로세스의 입력 및 출력을 프로그램의 입력 및 출력에 연결할 수 있어, Vim, Nano와 같은 에디터를 프로세스로 열 수도 있습니다:

```php
Process::forever()->tty()->run('vim');
```

> [!WARNING]
> TTY 모드는 Windows에서 지원되지 않습니다.

<a name="process-output"></a>
### 프로세스 출력 (Process Output)

앞서 설명했듯이, 프로세스 결과의 `output`(stdout), `errorOutput`(stderr) 메서드를 통해 프로세스 출력을 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

한편, `run` 메서드의 두 번째 인수로 클로저를 전달하면 실시간으로 출력을 받아올 수도 있습니다. 클로저는 "출력 유형"(`stdout` 혹은 `stderr`)과 출력 문자열을 각각 전달받습니다:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 또한 주어진 문자열이 프로세스 출력에 포함되어 있는지 손쉽게 확인할 수 있도록 `seeInOutput` 및 `seeInErrorOutput` 메서드를 제공합니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

프로세스가 관심 없는 많은 양의 출력을 생성한다면, 메모리를 절약하기 위해 출력 수집 자체를 비활성화할 수 있습니다. 이를 위해 `quietly` 메서드를 과정 빌드 시 호출하면 됩니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인 (Pipelines)

때로는 한 프로세스의 출력을 다른 프로세스의 입력으로 삼고 싶을 때가 있습니다. 이를 일반적으로 "파이핑"이라 합니다. `Process` 파사드에서 제공하는 `pipe` 메서드는 이 작업을 매우 쉽게 처리할 수 있습니다. `pipe` 메서드는 파이프 내의 프로세스들을 동기적으로 실행하고, 파이프라인의 마지막 프로세스 결과를 반환합니다:

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

파이프라인을 구성하는 각 프로세스를 커스터마이징할 필요가 없다면, 단순히 명령어 문자열 배열만 전달할 수도 있습니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

파이프라인의 실시간 출력도 두 번째 인수로 클로저를 전달해 받아올 수 있습니다. 클로저는 "출력 유형"(`stdout` 혹은 `stderr`)과 출력 문자열을 전달받습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

Laravel은 파이프라인 내 각 프로세스에 `as` 메서드를 통해 문자열 키를 지정할 수 있도록 지원합니다. 이 키는 `pipe` 메서드에 전달한 출력 클로저의 세 번째 인수로도 전달되어, 어떤 프로세스의 출력인지 구분할 수 있습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
}, function (string $type, string $output, string $key) {
    // ...
});
```

<a name="asynchronous-processes"></a>
## 비동기 프로세스 (Asynchronous Processes)

`run` 메서드는 프로세스를 동기적으로 호출하지만, `start` 메서드는 프로세스를 비동기적으로 호출할 때 사용합니다. 비동기로 실행하면 애플리케이션이 프로세스가 실행되는 동안 다른 작업을 계속 수행할 수 있습니다. 프로세스를 호출한 후에는 `running` 메서드를 이용해 프로세스가 아직 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

보시는 바와 같이, `wait` 메서드를 호출하여 프로세스가 끝날 때까지 대기하고, `ProcessResult` 인스턴스를 받아올 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID 및 시그널

`id` 메서드를 사용하면 실행 중인 프로세스의 운영체제에서 할당된 프로세스 ID를 조회할 수 있습니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드를 사용해 실행 중인 프로세스에 "시그널"을 보낼 수도 있습니다. 미리 정의된 시그널 상수는 [PHP 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다:

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행되는 동안 `output` 및 `errorOutput` 메서드를 호출해 현재까지의 전체 출력을 확인할 수 있습니다. 혹은, `latestOutput`과 `latestErrorOutput`를 이용해 마지막으로 호출된 이후 달라진(새로 추가된) 부분만 확인할 수도 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

동기 방식의 `run` 메서드와 마찬가지로, 비동기 프로세스의 출력을 실시간으로 수집하려면 `start` 메서드의 두 번째 인수로 클로저를 넘기면 됩니다. 이 클로저는 출력 유형과 출력 문자열을 인수로 받습니다:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 끝날 때까지 기다리는 대신, `waitUntil` 메서드를 이용해 출력 조건이 만족될 때 대기를 중단할 수 있습니다. 클로저가 `true`를 반환하면 Laravel은 프로세스 종료를 기다리는 것을 중지합니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스 실행 중, `ensureNotTimedOut` 메서드로 프로세스가 타임아웃되지 않았는지 확인할 수 있습니다. 타임아웃 상태라면 [타임아웃 예외](#timeouts)가 발생합니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    $process->ensureNotTimedOut();

    // ...

    sleep(1);
}
```

<a name="concurrent-processes"></a>
## 동시 프로세스 (Concurrent Processes)

Laravel에서는 여러 개의 비동기 프로세스 풀(Pool)을 손쉽게 관리할 수 있어, 여러 작업을 동시에 실행할 수 있습니다. 시작하려면, 클로저를 인수로 받는 `pool` 메서드를 호출합니다. 이 클로저에서는 풀에 포함될 프로세스들을 정의할 수 있습니다. 프로세스 풀을 `start` 메서드로 시작하면, `running` 메서드를 통해 실행 중인 프로세스의 [컬렉션](/docs/12.x/collections)을 확인할 수 있습니다:

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

위에서 알 수 있듯, `wait` 메서드를 이용해 풀에 포함된 모든 프로세스가 끝날 때까지 대기하고, 각각의 결과를 확인할 수 있습니다. `wait` 메서드는 배열처럼 접근할 수 있는 객체를 반환하며, 각 풀 프로세스의 `ProcessResult` 인스턴스에 키로 접근할 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```

좀 더 간결하게, `concurrently` 메서드를 사용하면 비동기 프로세스 풀을 시작하고 즉시 결과를 기다릴 수 있습니다. 이는 PHP의 배열 디스트럭처링 기능과 결합해 특히 간결하고 표현력 있는 문법을 제공합니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 내 프로세스 명명

숫자 인덱스로 프로세스 풀 결과에 접근하는 것은 직관적이지 않으므로, Laravel에서는 `as` 메서드를 통해 각 프로세스에 문자열 키를 지정할 수 있습니다. 이 키는 `start` 메서드에 전달한 클로저에도 전달되어, 어떤 프로세스에 해당 결과가 속하는지 쉽게 구분할 수 있습니다:

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
### 풀 프로세스 ID 및 시그널

프로세스 풀의 `running` 메서드는 풀 내의 모든 실행 중인 프로세스의 컬렉션을 제공하므로, 각 프로세스의 ID도 쉽게 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```

또한, 프로세스 풀에 대해 `signal` 메서드를 호출하면 풀 모든 프로세스에 동일한 시그널을 보낼 수 있습니다:

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트 (Testing)

Laravel의 많은 서비스는 테스트를 쉽게 작성할 수 있도록 기능을 제공합니다. 프로세스 서비스 역시 예외가 아닙니다. `Process` 파사드의 `fake` 메서드를 이용해, 프로세스 호출 시 스텁/더미 결과를 반환하도록 Laravel에 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 페이크 처리

Laravel의 프로세스 페이크 기능을 살펴보기 위해, 예를 들어 다음과 같이 프로세스를 호출하는 라우트가 있다고 가정해 보겠습니다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드를 인수 없이 호출하면 모든 프로세스 호출에 대해 가짜(성공) 결과를 반환하도록 할 수 있습니다. 또한, 주어진 프로세스가 "실행"되었는지 [assert](#available-assertions)로 검증할 수도 있습니다:

```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 간단한 프로세스 assertion...
    Process::assertRan('bash import.sh');

    // 혹은 프로세스 설정값을 검사...
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

        // 간단한 프로세스 assertion...
        Process::assertRan('bash import.sh');

        // 혹은 프로세스 설정값을 검사...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

위에서 설명했듯, `Process` 파사드의 `fake` 메서드를 호출하면 항상 성공한 프로세스 결과(출력 없음)를 반환하도록 지시합니다. 하지만, `Process` 파사드의 `result` 메서드를 이용해 페이크 프로세스의 출력과 종료 코드를 쉽게 지정할 수 있습니다:

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
### 특정 프로세스 페이크

앞서 예시에서 볼 수 있듯, `Process` 파사드는 `fake` 메서드에 배열을 넘겨 프로세스별로 다른 가짜 결과를 지정할 수 있습니다.

배열의 키는 가짜 결과를 적용하고자 하는 명령어 패턴이며, 값은 해당 명령어의 결과입니다. `*` 문자를 와일드카드로 사용할 수 있으며, 페이크되지 않은 프로세스 명령어는 실제로 실행됩니다. 각 명령어에 대한 페이크 결과는 `Process` 파사드의 `result` 메서드로 쉽게 생성할 수 있습니다:

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

만약 종료 코드나 에러 출력을 커스터마이징할 필요가 없다면, 단순히 문자열로 페이크 결과를 지정할 수도 있습니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 페이크

테스트 코드가 같은 명령어로 여러 번 프로세스를 호출한다면, 각 호출에 대해 서로 다른 페이크 결과를 지정할 수 있습니다. 이를 위해 `Process` 파사드의 `sequence` 메서드를 사용할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 생명주기 페이크

지금까지는 동기 방식(`run` 메서드)으로 호출한 프로세스의 페이크 방법에 집중했습니다. 하지만, `start`로 실행된 비동기 프로세스에 대해 상호작용하는 코드를 테스트한다면, 더 세밀하게 페이크 동작을 기술해야 할 수도 있습니다.

예를 들어, 다음과 같이 비동기 프로세스로 동작하는 라우트를 생각해 보겠습니다:

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

이 경우, `running` 메서드가 몇 번 `true`를 반환할 것인지 지정할 수 있어야 하며, 여러 줄의 출력을 순차적으로 반환하도록 할 수도 있습니다. 이런 세밀한 설정은 `Process` 파사드의 `describe` 메서드로 해결할 수 있습니다:

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

위 예시를 살펴보면, `output` 및 `errorOutput` 메서드로 여러 줄의 출력값을 순서대로 지정할 수 있습니다. `exitCode`로 마지막 종료 코드를, `iterations`로 `running` 메서드가 `true`를 반환할 횟수를 지정합니다.

<a name="available-assertions"></a>
### 사용 가능한 Assertion

[앞에서 설명한 대로](#faking-processes), Laravel에서는 여러 가지 프로세스 assertion을 이용해 기능 테스트를 작성할 수 있습니다. 아래에서는 각 assertion에 대해 살펴봅니다.

<a name="assert-process-ran"></a>
#### assertRan

주어진 프로세스가 호출되었는지 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저도 인수로 받을 수 있으며, 이때 프로세스 인스턴스와 프로세스 결과를 받아 설정값을 검사할 수 있습니다. 클로저가 `true`를 반환하면 단언이 "성공"합니다:

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

`$process`는 `Illuminate\Process\PendingProcess` 인스턴스, `$result`는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

주어진 프로세스가 호출되지 않았음을 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertRan`과 마찬가지로, `assertDidntRun` 도 클로저를 받아 설정값 검사 후 `true`을 반환하면 assertion이 "실패"합니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

주어진 프로세스가 지정한 횟수만큼 호출되었는지 단언합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` 역시 클로저를 받을 수 있으며, 클로저가 `true`를 반환하고, 프로세스가 지정한 횟수만큼 실행되었다면 단언이 "성공"합니다:

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 낙오 프로세스 방지

테스트 전체 또는 개별 테스트에서 호출된 모든 프로세스가 반드시 페이크로 처리되도록 보장하려면, `preventStrayProcesses` 메서드를 사용할 수 있습니다. 이 메서드 호출 이후, 페이크 결과가 없는 프로세스는 실제로 실행되지 않고 예외가 발생하게 됩니다:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 페이크 결과 반환...
Process::run('ls -la');

// 예외 발생...
Process::run('bash import.sh');
```
