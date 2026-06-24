<!-- # Console Tests -->
# Console Tests

- [Introduction](#introduction)
- [Success / Failure Expectations](#success-failure-expectations)
- [Input / Output Expectations](#input-output-expectations)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's [custom console commands](/docs/9.x/artisan). -->
Laravel은 HTTP 테스트를 간편하게 할 수 있도록 도와줄 뿐만 아니라, 여러분이 작성한 [custom console commands](/docs/9.x/artisan)를 테스트할 수 있는 간단한 API도 제공합니다.

<a name="success-failure-expectations"></a>
<!-- ## Success / Failure Expectations -->
## Success / Failure Expectations

<!-- To get started, let's explore how to make assertions regarding an Artisan command's exit code. To accomplish this, we will use the `artisan` method to invoke an Artisan command from our test. Then, we will use the `assertExitCode` method to assert that the command completed with a given exit code: -->
먼저, Artisan 명령어의 종료 코드(Exit Code)에 대해 어떻게 assert(확인)할 수 있는지 살펴보겠습니다. 이를 위해 테스트에서 `artisan` 메서드를 사용해 Artisan 명령어를 호출한 뒤, `assertExitCode` 메서드를 사용해 명령어가 원하는 종료 코드로 완전히 실행되었는지 확인할 수 있습니다.

```
/**
 * Test a console command.
 *
 * @return void
 */
public function test_console_command()
{
    $this->artisan('inspire')->assertExitCode(0);
}
```

<!-- You may use the `assertNotExitCode` method to assert that the command did not exit with a given exit code: -->
명령어가 특정 종료 코드로 종료되지 않았는지 확인하려면 `assertNotExitCode` 메서드를 사용할 수 있습니다.

```
$this->artisan('inspire')->assertNotExitCode(1);
```

<!-- Of course, all terminal commands typically exit with a status code of `0` when they are successful and a non-zero exit code when they are not successful. Therefore, for convenience, you may utilize the `assertSuccessful` and `assertFailed` assertions to assert that a given command exited with a successful exit code or not: -->
보통 모든 터미널 명령어는 성공적으로 실행되면 `0` 상태 코드로 종료되고, 실패했을 때는 0이 아닌 다른 종료 코드를 반환합니다. 그래서 편의상, 명령어가 성공적으로, 또는 실패 상태로 종료되었는지 확인하는 데에는 `assertSuccessful`, `assertFailed` assertion을 사용할 수 있습니다.

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
<!-- ## Input / Output Expectations -->
## Input / Output Expectations

<!-- Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command: -->
Laravel에서는 콘솔 명령어 테스트 시 `expectsQuestion` 메서드를 이용해 사용자 입력을 손쉽게 "모킹(mock)"할 수 있습니다. 또한, 콘솔 명령어의 종료 코드와 출력되어야 하는 텍스트를 `assertExitCode`와 `expectsOutput` 메서드로 지정할 수 있습니다. 예를 들어, 아래와 같은 콘솔 명령어가 있다고 가정해보겠습니다.

```
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

<!-- You may test this command with the following test which utilizes the `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `expectsOutputToContain`, `doesntExpectOutputToContain`, and `assertExitCode` methods: -->
이 명령어는 아래와 같이 테스트할 수 있습니다. 테스트에서는 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `expectsOutputToContain`, `doesntExpectOutputToContain`, `assertExitCode` 등의 메서드를 사용할 수 있습니다.

```
/**
 * Test a console command.
 *
 * @return void
 */
public function test_console_command()
{
    $this->artisan('question')
         ->expectsQuestion('What is your name?', 'Taylor Otwell')
         ->expectsQuestion('Which language do you prefer?', 'PHP')
         ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
         ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
         ->expectsOutputToContain('Taylor Otwell')
         ->doesntExpectOutputToContain('you prefer Ruby')
         ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
<!-- #### Confirmation Expectations -->
#### Confirmation Expectations

<!-- When writing a command which expects confirmation in the form of a "yes" or "no" answer, you may utilize the `expectsConfirmation` method: -->
명령어에서 "yes" 또는 "no"로 답을 받는 확인 질문을 사용할 경우, `expectsConfirmation` 메서드를 활용할 수 있습니다.

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
<!-- #### Table Expectations -->
#### Table Expectations

<!-- If your command displays a table of information using Artisan's `table` method, it can be cumbersome to write output expectations for the entire table. Instead, you may use the `expectsTable` method. This method accepts the table's headers as its first argument and the table's data as its second argument: -->
만약 여러분의 명령어가 Artisan의 `table` 메서드를 사용해서 정보 테이블을 출력한다면, 전체 테이블 전체를 대상으로 출력 결과를 검사하는 코드를 작성하는 것은 다소 번거로울 수 있습니다. 이런 경우, `expectsTable` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 테이블의 헤더, 두 번째 인자로 테이블 데이터를 받습니다.

```
$this->artisan('users:all')
    ->expectsTable([
        'ID',
        'Email',
    ], [
        [1, 'taylor@example.com'],
        [2, 'abigail@example.com'],
    ]);
```