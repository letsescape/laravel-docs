<!-- # Console Tests -->
# Console Tests

- [Introduction](#introduction)
- [Success / Failure Expectations](#success-failure-expectations)
- [Input / Output Expectations](#input-output-expectations)
- [Console Events](#console-events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's [custom console commands](/docs/13.x/artisan). -->
HTTP 테스트를 단순화하는 것 외에도, Laravel은 애플리케이션에서 작성한 [custom console commands](/docs/13.x/artisan)를 테스트할 수 있도록 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
<!-- ## Success / Failure Expectations -->
## Success / Failure Expectations

<!-- To get started, let's explore how to make assertions regarding an Artisan command's exit code. To accomplish this, we will use the `artisan` method to invoke an Artisan command from our test. Then, we will use the `assertExitCode` method to assert that the command completed with a given exit code: -->
먼저, Artisan 명령어의 종료 코드(exit code)에 대한 검증(assertion)을 어떻게 작성하는지 살펴보겠습니다. 이를 위해 테스트 내에서 `artisan` 메서드를 사용해 Artisan 명령어를 실행한 뒤, `assertExitCode` 메서드를 이용하여명령어가 특정 종료 코드로 완료되었는지 검증할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('inspire')->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

<!-- You may use the `assertNotExitCode` method to assert that the command did not exit with a given exit code: -->
`assertNotExitCode` 메서드를 사용하면 명령어가 특정 종료 코드로 종료되지 않았음을 검증할 수도 있습니다:

```php
$this->artisan('inspire')->assertNotExitCode(1);
```

<!-- Of course, all terminal commands typically exit with a status code of `0` when they are successful and a non-zero exit code when they are not successful. Therefore, for convenience, you may utilize the `assertSuccessful` and `assertFailed` assertions to assert that a given command exited with a successful exit code or not: -->
일반적으로 모든 터미널 명령어는 성공적으로 실행되면 `0` 상태 코드로 종료되고, 실패하면 0이 아닌 종료 코드로 종료됩니다. 이에 따라, 더 간편하게 사용할 수 있도록 `assertSuccessful`과 `assertFailed` 메서드를 사용하여 명령어가 성공적으로 또는 실패로 종료되었음을 검증할 수 있습니다:

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
<!-- ## Input / Output Expectations -->
## Input / Output Expectations

<!-- Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command: -->
Laravel에서는 콘솔 명령어에서 사용자 입력을 쉽게 "모킹(mock)"할 수 있도록 `expectsQuestion` 메서드를 제공합니다. 또한, 명령어가 출력할 것으로 기대되는 종료 코드와 텍스트를 각각 `assertExitCode`와 `expectsOutput` 메서드로 지정할 수 있습니다. 예를 들어, 다음과 같은 콘솔 명령어를 생각해보세요:

```php
Artisan::command('question', function () {
    $name = $this->ask('What is your name?');

    $language = $this->choice('Which language do you prefer?', [
        'PHP',
        'Ruby',
        'Python',
    ]);

    $this->line('Your name is '.$name.' and you prefer '.$language.'.');
});
```

<!-- You may test this command with the following test: -->
이 명령어는 아래와 같이 테스트할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
}
```

<!-- If you are utilizing the `search` or `multisearch` functions provided by [Laravel Prompts](/docs/13.x/prompts), you may use the `expectsSearch` assertion to mock the user's input, search results, and selection: -->
[Laravel Prompts](/docs/13.x/prompts)에서 제공하는 `search` 또는 `multisearch` 기능을 사용하는 경우, `expectsSearch` 검증 메서드를 통해 사용자 입력, 검색 결과, 선택값을 모킹할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
}
```

<!-- You may also assert that a console command does not generate any output using the `doesntExpectOutput` method: -->
`doesntExpectOutput` 메서드를 활용하면 콘솔 명령어가 아무런 출력도 생성하지 않았음을 검증할 수도 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
}
```

<!-- The `expectsOutputToContain` and `doesntExpectOutputToContain` methods may be used to make assertions against a portion of the output: -->
`expectsOutputToContain` 및 `doesntExpectOutputToContain` 메서드는 출력 결과 중 일부 문자열만을 포함하거나 포함하지 않는지 검증할 때 사용할 수 있습니다:

```php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
});
```

```php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
<!-- #### Confirmation Expectations -->
#### Confirmation Expectations

<!-- When writing a command which expects confirmation in the form of a "yes" or "no" answer, you may utilize the `expectsConfirmation` method: -->
"예/아니오" 형태의 확인 답변을 기대하는 명령어를 작성할 때는 `expectsConfirmation` 메서드를 사용할 수 있습니다:

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
<!-- #### Table Expectations -->
#### Table Expectations

<!-- If your command displays a table of information using Artisan's `table` method, it can be cumbersome to write output expectations for the entire table. Instead, you may use the `expectsTable` method. This method accepts the table's headers as its first argument and the table's data as its second argument: -->
명령어에서 Artisan의 `table` 메서드를 사용하여 정보를 테이블 형태로 출력하는 경우, 전체 테이블에 대해 출력 예측을 작성하는 것은 번거로울 수 있습니다. 이럴 때는 `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블의 헤더, 두 번째 인자로 테이블 데이터를 전달받습니다:

```php
$this->artisan('users:all')
    ->expectsTable([
        'ID',
        'Email',
    ], [
        [1, 'taylor@example.com'],
        [2, 'abigail@example.com'],
    ]);
```

<a name="console-events"></a>
<!-- ## Console Events -->
## Console Events

<!-- By default, the `Illuminate\Console\Events\CommandStarting` and `Illuminate\Console\Events\CommandFinished` events are not dispatched while running your application's tests. However, you can enable these events for a given test class by adding the `Illuminate\Foundation\Testing\WithConsoleEvents` trait to the class: -->
기본적으로, `Illuminate\Console\Events\CommandStarting` 및 `Illuminate\Console\Events\CommandFinished` 이벤트는 애플리케이션의 테스트를 실행할 때 발생하지 않습니다. 그러나 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트(trait)를 추가하면 이 이벤트들을 활성화할 수 있습니다:

```php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithConsoleEvents;

pest()->use(WithConsoleEvents::class);

// ...
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithConsoleEvents;
use Tests\TestCase;

class ConsoleEventTest extends TestCase
{
    use WithConsoleEvents;

    // ...
}
```
