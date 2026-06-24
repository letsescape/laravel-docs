<!-- # Console Tests -->
# Console Tests

- [Introduction](#introduction)
- [Success / Failure Expectations](#success-failure-expectations)
- [Input / Output Expectations](#input-output-expectations)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- In addition to simplifying HTTP testing, Laravel provides a simple API for testing your application's [custom console commands](/docs/8.x/artisan). -->
HTTP 테스트를 간소화하는 기능 외에도, Laravel은 애플리케이션의 [custom console commands](/docs/8.x/artisan)를 테스트할 수 있는 간편한 API도 제공합니다.

<a name="success-failure-expectations"></a>
<!-- ## Success / Failure Expectations -->
## Success / Failure Expectations

<!-- To get started, let's explore how to make assertions regarding an Artisan command's exit code. To accomplish this, we will use the `artisan` method to invoke an Artisan command from our test. Then, we will use the `assertExitCode` method to assert that the command completed with a given exit code: -->
먼저, Artisan 명령어의 종료 코드(exit code)에 대해 어떻게 assert(확인)할 수 있는지 살펴보겠습니다. 테스트에서 `artisan` 메서드를 사용하여 Artisan 명령어를 실행하고, `assertExitCode` 메서드를 이용해 명령어가 특정 종료 코드로 종료되었는지 검사할 수 있습니다.

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
반대로, 명령어가 특정 종료 코드로 종료되지 않았음을 확인하고 싶다면 `assertNotExitCode` 메서드를 사용할 수 있습니다.

```
$this->artisan('inspire')->assertNotExitCode(1);
```

<!-- Of course, all terminal commands typically exit with a status code of `0` when they are successful and a non-zero exit code when they are not successful. Therefore, for convenience, you may utilize the `assertSuccessful` and `assertFailed` assertions to assert that a given command exited with a successful exit code or not: -->
일반적으로, 모든 터미널 명령어는 성공하면 종료 코드가 `0`이고, 실패하면 0이 아닌 값을 반환합니다. 이를 좀 더 편리하게 확인할 수 있도록, Laravel에서는 `assertSuccessful`과 `assertFailed`와 같은 assertion을 제공하여 명령어가 정상적으로 종료되었는지 또는 실패했는지를 간편하게 검사할 수 있습니다.

```
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();
```

<a name="input-output-expectations"></a>
<!-- ## Input / Output Expectations -->
## Input / Output Expectations

<!-- Laravel allows you to easily "mock" user input for your console commands using the `expectsQuestion` method. In addition, you may specify the exit code and text that you expect to be output by the console command using the `assertExitCode` and `expectsOutput` methods. For example, consider the following console command: -->
Laravel에서는 콘솔 명령어 테스트 시 `expectsQuestion` 메서드를 사용하여 사용자 입력을 손쉽게 "모킹(mock)"할 수 있습니다. 또한, 콘솔 명령어가 출력할 것으로 기대하는 종료 코드와 텍스트를 각각 `assertExitCode`와 `expectsOutput` 메서드로 설정 및 검증할 수 있습니다. 예시로, 아래와 같은 콘솔 명령어가 있다고 가정해 보겠습니다.

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

<!-- You may test this command with the following test which utilizes the `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, and `assertExitCode` methods: -->
위 콘솔 명령어는 다음과 같은 테스트로 확인할 수 있습니다. 이 테스트에서는 `expectsQuestion`, `expectsOutput`, `doesntExpectOutput`, `assertExitCode` 메서드를 활용합니다.

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
         ->assertExitCode(0);
}
```

<a name="confirmation-expectations"></a>
<!-- #### Confirmation Expectations -->
#### Confirmation Expectations

<!-- When writing a command which expects confirmation in the form of a "yes" or "no" answer, you may utilize the `expectsConfirmation` method: -->
만약 명령어가 "예" 또는 "아니오" 형식의 확인(confirmation) 입력을 요구한다면, `expectsConfirmation` 메서드를 사용할 수 있습니다.

```
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);
```

<a name="table-expectations"></a>
<!-- #### Table Expectations -->
#### Table Expectations

<!-- If your command displays a table of information using Artisan's `table` method, it can be cumbersome to write output expectations for the entire table. Instead, you may use the `expectsTable` method. This method accepts the table's headers as its first argument and the table's data as its second argument: -->
명령어에서 Artisan의 `table` 메서드를 사용해 정보 테이블을 출력할 경우, 전체 테이블 출력 결과에 대한 예상 값을 작성하는 것이 번거로울 수 있습니다. 이럴 때는 `expectsTable` 메서드를 활용하면 됩니다. 이 메서드는 첫 번째 인자로 테이블 헤더, 두 번째 인자로 테이블 데이터를 받습니다.

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
