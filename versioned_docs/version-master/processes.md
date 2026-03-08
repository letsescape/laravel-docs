# 프로세스 (Processes)

- [소개](#introduction)
- [프로세스 호출하기](#invoking-processes)
    - [프로세스 옵션](#process-options)
    - [프로세스 출력](#process-output)
    - [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
    - [프로세스 ID와 시그널](#process-ids-and-signals)
    - [비동기 프로세스 출력](#asynchronous-process-output)
    - [비동기 프로세스 타임아웃](#asynchronous-process-timeouts)
- [동시 프로세스](#concurrent-processes)
    - [풀 프로세스 명명하기](#naming-pool-processes)
    - [풀 프로세스 ID와 시그널](#pool-process-ids-and-signals)
- [테스트하기](#testing)
    - [프로세스 페이크하기](#faking-processes)
    - [특정 프로세스 페이크하기](#faking-specific-processes)
    - [프로세스 시퀀스 페이크하기](#faking-process-sequences)
    - [비동기 프로세스 생명주기 페이크하기](#faking-asynchronous-process-lifecycles)
    - [사용 가능한 어설션](#available-assertions)
    - [불필요한 프로세스 실행 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [Symfony Process 컴포넌트](https://symfony.com/doc/current/components/process.html) 위에 표현력이 뛰어나고 최소한의 API를 제공하여, Laravel 애플리케이션에서 외부 프로세스를 손쉽게 호출할 수 있도록 지원합니다. Laravel의 프로세스 기능은 가장 일반적인 사용 사례에 중점을 두고 있으며, 개발자 경험을 크게 향상시킵니다.

<a name="invoking-processes"></a>
## 프로세스 호출하기 (Invoking Processes)

프로세스를 실행하려면 `Process` 파사드에서 제공하는 `run`과 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 동기적으로 실행하고 완료될 때까지 대기하며, `start` 메서드는 비동기로 프로세스를 실행할 때 사용합니다. 이 문서에서는 두 방법 모두 살펴보겠습니다. 먼저, 기본적인 동기 프로세스를 호출하고 결과를 확인하는 방법을 살펴보겠습니다.

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```

물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스에는 프로세스 결과를 확인할 수 있는 다양한 유용한 메서드가 제공됩니다.

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
#### 예외 발생시키기

프로세스 결과가 있고, 만약 종료 코드가 0보다 크다면(즉, 실패를 의미) `Illuminate\Process\Exceptions\ProcessFailedException` 예외를 발생시키고 싶다면 `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면 해당 `ProcessResult` 인스턴스를 그대로 반환합니다.

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```

<a name="process-options"></a>
### 프로세스 옵션 (Process Options)

물론 프로세스를 실행하기 전에 동작을 세밀하게 제어해야 할 수도 있습니다. Laravel은 작업 디렉터리, 타임아웃, 환경 변수 등 다양한 프로세스 기능을 쉽게 조정할 수 있도록 지원합니다.

<a name="working-directory-path"></a>
#### 작업 디렉터리 경로

`path` 메서드를 사용해 프로세스의 작업 디렉터리를 지정할 수 있습니다. 이 메서드를 호출하지 않으면 프로세스는 현재 실행 중인 PHP 스크립트의 작업 디렉터리를 상속합니다.

```php
$result = Process::path(__DIR__)->run('ls -la');
```

<a name="input"></a>
#### 입력값 전달

`input` 메서드를 이용하여 프로세스의 "표준 입력"을 통해 입력값을 전달할 수 있습니다.

```php
$result = Process::input('Hello World')->run('cat');
```

<a name="timeouts"></a>
#### 타임아웃

기본적으로 프로세스는 60초 이상 실행될 경우 `Illuminate\Process\Exceptions\ProcessTimedOutException` 예외를 발생시킵니다. 그러나 `timeout` 메서드를 사용하여 이 동작을 원하는 대로 설정할 수 있습니다.

```php
$result = Process::timeout(120)->run('bash import.sh');
```

프로세스 타임아웃을 완전히 비활성화하고 싶다면 `forever` 메서드를 호출할 수 있습니다.

```php
$result = Process::forever()->run('bash import.sh');
```

`idleTimeout` 메서드를 사용하면 프로세스가 아무런 출력을 반환하지 않은 채로 동작할 수 있는 최대 시간을(초 단위) 지정할 수 있습니다.

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```

<a name="environment-variables"></a>
#### 환경 변수

`env` 메서드를 통해 프로세스에 환경 변수를 지정해 줄 수 있습니다. 호출된 프로세스는 시스템에 정의된 모든 환경 변수도 상속받게 됩니다.

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```

상속된 환경 변수 중 특정 변수를 프로세스에서 제거하고 싶을 경우, 해당 환경 변수 값으로 `false`를 지정하면 됩니다.

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```

<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드를 사용하면 프로세스에 대해 TTY 모드를 활성화할 수 있습니다. TTY 모드는 프로세스의 입력과 출력을 프로그램의 입력/출력과 연결해주므로, 예를 들어 Vim이나 Nano 같은 에디터를 프로세스로 열 때 활용할 수 있습니다.

```php
Process::forever()->tty()->run('vim');
```

> [!WARNING]
> TTY 모드는 Windows에서는 지원되지 않습니다.

<a name="process-output"></a>
### 프로세스 출력 (Process Output)

앞서 설명한대로, 프로세스의 출력은 `output`(표준 출력)과 `errorOutput`(표준 에러 출력) 메서드로 접근할 수 있습니다.

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```

하지만, 실시간으로 출력을 수집하고 싶다면 `run` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 이 클로저는 출력의 "타입"(`stdout` 또는 `stderr`)과, 해당 출력 문자열을 인수로 받게 됩니다.

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```

Laravel은 또한 `seeInOutput` 및 `seeInErrorOutput` 메서드를 제공하여, 프로세스의 출력에 지정한 문자열이 포함되어 있는지 쉽게 확인할 수 있도록 도와줍니다.

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```

<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

프로세스가 많은 양의 출력을 생성하지만 해당 출력이 불필요한 경우, 출력을 완전히 비활성화하여 메모리 사용량을 줄일 수 있습니다. 이를 위해 프로세스 빌드 과정에서 `quietly` 메서드를 호출하세요.

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```

<a name="process-pipelines"></a>
### 파이프라인 (Pipelines)

때로는 한 프로세스의 출력을 다른 프로세스의 입력값으로 사용하고 싶을 때가 있습니다. 이를 "파이핑"이라고 하며, `Process` 파사드가 제공하는 `pipe` 메서드를 사용하면 간단히 구현할 수 있습니다. `pipe` 메서드는 파이프라인으로 연결된 여러 프로세스를 동기적으로 실행하고, 파이프라인 마지막 프로세스의 결과를 반환합니다.

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

파이프라인을 구성하는 각 프로세스를 직접 커스터마이징할 필요가 없다면, 단순히 명령어 문자열의 배열을 `pipe` 메서드에 전달할 수도 있습니다.

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```

출력을 실시간으로 수집하고 싶을 경우, 두 번째 인수로 클로저를 넘기면 됩니다. 이 클로저는 출력의 "타입"(`stdout`/`stderr`)과 출력 문자열을 인수로 받게 됩니다.

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```

Laravel에서는 각 프로세스에 `as` 메서드를 이용해 문자열 키를 지정할 수도 있습니다. 이 키는 출력 클로저에도 함께 전달되어, 어떤 프로세스의 출력인지 구분할 수 있게 해줍니다.

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

`run` 메서드는 프로세스를 동기적으로 실행하지만, `start` 메서드는 프로세스를 비동기로 실행할 수 있도록 해줍니다. 덕분에 프로세스가 백그라운드에서 실행되는 동안 애플리케이션은 다른 작업을 계속 수행할 수 있습니다. 프로세스가 실행된 후에는 `running` 메서드를 이용해 아직 실행 중인지 확인할 수 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```

보시다시피, `wait` 메서드를 호출하면 프로세스가 완료될 때까지 대기하고, 이후 `ProcessResult` 인스턴스를 반환받을 수 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```

<a name="process-ids-and-signals"></a>
### 프로세스 ID와 시그널

`id` 메서드를 통해 실행 중인 프로세스의 운영체제가 할당한 프로세스 ID를 가져올 수 있습니다.

```php
$process = Process::start('bash import.sh');

return $process->id();
```

`signal` 메서드를 사용하면 실행 중인 프로세스에 시그널을 전달할 수 있습니다. 사전에 정의된 시그널 상수 목록은 [PHP 공식 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 확인할 수 있습니다.

```php
$process->signal(SIGUSR2);
```

<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행 중일 때, `output` 및 `errorOutput` 메서드를 활용해 현재까지의 전체 출력을 가져올 수 있습니다. 혹은 `latestOutput` 및 `latestErrorOutput` 메서드를 사용하면 마지막으로 출력을 가져온 이후 이후 추가된 새로운 출력만 가져올 수 있습니다.

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```

동기 실행 때와 마찬가지로, 비동기 상태에서도 `start` 메서드의 두 번째 인수로 클로저를 넘기면 실시간으로 출력을 수집할 수 있습니다. 이 클로저는 출력의 "타입"(`stdout`/`stderr`)과 출력 문자열을 인수로 받습니다.

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```

프로세스가 끝날 때까지 기다리지 않고, 프로세스의 출력에 따라 중간에 대기를 멈추고 싶다면 `waitUntil` 메서드를 사용할 수 있습니다. 이 메서드는 클로저를 인수로 받으며, 해당 클로저가 `true`를 반환하면 프로세스 대기를 중단합니다.

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```

<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스가 실행 중인 동안, `ensureNotTimedOut` 메서드를 호출해 프로세스가 타임아웃되지 않았는지 검증할 수 있습니다. 해당 메서드는 프로세스가 타임아웃된 경우 [타임아웃 예외](#timeouts)를 발생시킵니다.

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

Laravel은 동시 실행되는 여러 비동기 프로세스들의 풀(pool)을 쉽게 관리할 수 있는 기능도 제공합니다. 이를 통해 여러 작업을 동시에 처리할 수 있습니다. 가장 먼저, `Illuminate\Process\Pool` 인스턴스를 전달하는 클로저를 인수로 받는 `pool` 메서드를 호출합니다.

이 클로저 안에서 풀에 포함될 프로세스들을 정의할 수 있습니다. 풀을 `start` 메서드로 실행하면, 실행 중인 프로세스들의 [컬렉션](/docs/master/collections)을 `running` 메서드를 통해 확인할 수 있습니다.

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

보시다시피, 모든 풀 내 프로세스가 종료될 때까지 대기하고, 각 프로세스의 결과를 `wait` 메서드를 통해 받아올 수 있습니다. `wait` 메서드는 배열처럼 접근할 수 있는 객체를 반환하며, 풀 내 각 프로세스의 키를 통해 해당 `ProcessResult` 인스턴스에 접근할 수 있습니다.

```php
$results = $pool->wait();

echo $results[0]->output();
```

혹은, 더욱 간결하게 `concurrently` 메서드를 사용할 수도 있습니다. 이 메서드는 비동기 풀을 시작하고, 결과를 즉시 대기하여 받아옵니다. PHP 배열 디스트럭처링 문법과 함께 사용하면 매우 표현적이고 깔끔한 코드를 작성할 수 있습니다.

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```

<a name="naming-pool-processes"></a>
### 풀 프로세스 명명하기

프로세스 풀의 결과를 숫자 키로 접근하는 것은 다소 직관적이지 않습니다. 따라서 Laravel은 각 프로세스에 `as` 메서드를 사용해 문자열 키를 지정할 수 있도록 했습니다. 이 키는 `start` 메서드에 전달된 클로저에도 전달되어, 어떤 프로세스의 출력인지 식별할 수 있게 합니다.

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
### 풀 프로세스 ID와 시그널

풀의 `running` 메서드는 실행 중인 모든 프로세스들의 컬렉션을 반환하므로, 각 프로세스의 실제 프로세스 ID도 손쉽게 접근할 수 있습니다.

```php
$processIds = $pool->running()->each->id();
```

또한, 간편하게 풀 내 모든 프로세스에 시그널을 전달하려면 풀 자체에서 `signal` 메서드를 호출할 수 있습니다.

```php
$pool->signal(SIGUSR2);
```

<a name="testing"></a>
## 테스트하기 (Testing)

Laravel의 다양한 서비스는 쉽게 테스트를 작성할 수 있도록 여러 기능을 제공합니다. 프로세스 서비스 역시 예외가 아닙니다. `Process` 파사드의 `fake` 메서드는 프로세스가 실행될 때 가짜(stub) 결과 또는 더미 결과를 반환하도록 Laravel에 지시해줍니다.

<a name="faking-processes"></a>
### 프로세스 페이크하기

Laravel의 프로세스 페이크 기능을 살펴보기 위해, 프로세스를 호출하는 라우트 예제를 생각해보겠습니다.

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```

이 라우트를 테스트할 때, `Process` 파사드의 `fake` 메서드에 아무 인수도 주지 않으면 모든 프로세스 호출에 대해 성공적인 가짜 결과를 반환하도록 Laravel에 지시할 수 있습니다. 또한, [어설션](#available-assertions)을 사용해 특정 프로세스가 실행되었는지 확인할 수도 있습니다.

```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // 간단한 프로세스 어설션...
    Process::assertRan('bash import.sh');

    // 혹은 프로세스 구성 옵션까지 확인...
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

        // 간단한 프로세스 어설션...
        Process::assertRan('bash import.sh');

        // 혹은 프로세스 구성 옵션까지 확인...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```

설명한 대로, `Process` 파사드의 `fake` 메서드는 항상 출력 없이 성공적인 프로세스 결과를 반환하도록 동작합니다. 하지만 `Process` 파사드의 `result` 메서드를 사용해 가짜 프로세스의 출력과 종료 코드를 따로 지정할 수 있습니다.

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
### 특정 프로세스 페이크하기

앞선 예시에서 본 것처럼, `Process` 파사드는 배열 형태로 가짜 결과를 전달하여 명령어별로 서로 다른 가짜 결과를 지정할 수 있습니다.

배열의 키는 페이크하려는 명령어 패턴을 나타내야 하며, 그에 해당하는 결과 값을 지정합니다. `*` 문자로 와일드카드 패턴을 만들 수도 있습니다. 페이크되지 않은 명령어는 실제로 실행됩니다. 가짜 결과는 `Process` 파사드의 `result` 메서드를 사용해 만들 수 있습니다.

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

가짜 프로세스의 종료 코드나 에러 출력을 따로 커스터마이징할 필요가 없는 경우, 문자열만 지정해 더 간단히 사용할 수도 있습니다.

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```

<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 페이크하기

테스트 중 여러 번 동일한 명령어로 복수의 프로세스가 실행된다면, 각 실행마다 다른 결과가 반환되도록 하고 싶을 것입니다. 이런 경우 `Process` 파사드의 `sequence` 메서드를 사용할 수 있습니다.

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```

<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 생명주기 페이크하기

지금까지는 주로 `run` 메서드로 동기적으로 호출한 프로세스를 페이크하는 방법을 다뤘습니다. 하지만 `start`로 비동기 실행되는 프로세스와 상호작용하는 코드를 테스트하려면, 좀 더 복잡한 가짜 프로세스 설정이 필요할 수 있습니다.

예를 들어 다음과 같이 비동기 프로세스를 다루는 라우트를 생각해보겠습니다.

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

이러한 프로세스를 제대로 페이크하려면, `running` 메서드가 몇 번 `true`를 반환해야 하는지, 그리고 여러 출력을 순서대로 반환해야 하는지 등을 지정해야 합니다. 이를 위해선 `Process` 파사드의 `describe` 메서드를 사용할 수 있습니다.

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

위의 예제에서처럼, `output` 및 `errorOutput` 메서드로 각 라인을 순서대로 지정할 수 있습니다. `exitCode` 메서드로는 마지막 종료 코드를, `iterations` 메서드로는 `running` 메서드가 몇 번 `true`를 반환할지 지정합니다.

<a name="available-assertions"></a>
### 사용 가능한 어설션 (Available Assertions)

앞서 [설명한 대로](#faking-processes), Laravel은 기능 테스트를 위한 다양한 프로세스 어설션을 제공합니다. 아래에서 각각의 어설션을 자세히 설명합니다.

<a name="assert-process-ran"></a>
#### assertRan

특정 프로세스가 실행되었는지 어설션합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```

`assertRan` 메서드는 클로저도 인수로 받을 수 있습니다. 이 클로저는 프로세스와 프로세스 결과 인스턴스를 넘겨주며, 클로저가 `true`를 반환하면 어설션이 통과하게 됩니다.

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```

여기서 `$process`는 `Illuminate\Process\PendingProcess`의 인스턴스이고, `$result`는 `Illuminate\Contracts\Process\ProcessResult`의 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

특정 프로세스가 실행되지 않았는지 어설션합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```

`assertDidntRun` 역시 클로저를 인수로 받을 수 있으며, 이 클로저가 `true`를 반환하면 어설션이 실패합니다.

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```

<a name="assert-process-ran-times"></a>
#### assertRanTimes

특정 프로세스가 지정한 횟수만큼 실행되었는지 어설션합니다.

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```

`assertRanTimes` 역시 클로저를 인수로 받아, 해당 조건과 실행 횟수가 맞으면 어설션이 통과합니다.

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```

<a name="preventing-stray-processes"></a>
### 불필요한 프로세스 실행 방지 (Preventing Stray Processes)

개별 테스트 또는 전체 테스트 스위트 동안 모든 프로세스 실행이 반드시 페이크되어야만 한다면, `preventStrayProcesses` 메서드를 호출할 수 있습니다. 이 메서드를 호출하면, 페이크 결과가 지정되지 않은 모든 프로세스 실행 시 실제 실행 대신 예외가 발생합니다.

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// 페이크 결과가 반환됨
Process::run('ls -la');

// 예외 발생
Process::run('bash import.sh');
```
