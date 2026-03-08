# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [Isolatable 명령어](#isolatable-commands)
- [입력 값 정의](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [누락된 입력에 대한 프롬프트 처리](#prompting-for-missing-input)
- [명령어 입출력(I/O)](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력 프롬프트](#prompting-for-input)
    - [출력 작성](#writing-output)
- [명령어 등록](#registering-commands)
- [명령어의 코드 실행](#programmatically-executing-commands)
    - [명령어 내에서 다른 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁(stub) 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개 (Introduction)

Artisan(아티즌)은 Laravel에 내장되어 있는 명령줄 인터페이스입니다. Artisan은 애플리케이션의 루트에 `artisan` 스크립트로 존재하며, 여러분이 애플리케이션을 개발할 때 도움이 되는 다양한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 확인하려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

각 명령어에는 사용 가능한 인수와 옵션을 표시 및 설명하는 "도움말" 화면도 포함되어 있습니다. 도움말 화면을 보려면 명령어 앞에 `help`를 붙여 실행하면 됩니다:

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

로컬 개발 환경으로 [Laravel Sail](/docs/master/sail)을 사용하고 있다면, Artisan 명령어를 실행할 때 `sail` 명령줄을 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 안에서 Artisan 명령어를 실행해 줍니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 Laravel 프레임워크용 강력한 REPL 환경이며, [PsySH](https://github.com/bobthecow/psysh) 패키지 기반으로 동작합니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 이전에 애플리케이션에서 Tinker를 제거한 경우 Composer를 이용해 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 "핫 리로딩", 여러 줄 코드 편집, 자동완성 기능을 찾고 계신가요? [Tinkerwell](https://tinkerwell.app)도 확인해 보세요!

<a name="usage"></a>
#### 사용법

Tinker를 사용하면 명령줄에서 전체 Laravel 애플리케이션, 즉 Eloquent 모델, 잡(jobs), 이벤트 등을 자유롭게 다룰 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```

Tinker의 설정 파일은 `vendor:publish` 명령어를 이용하여 개별적으로 발행(publish)할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣기 위해 가비지 컬렉션(garbage collection)에 의존합니다. 따라서 Tinker를 사용할 때는 잡을 디스패치할 때 `Bus::dispatch` 또는 `Queue::push`를 사용하는 것이 좋습니다.

<a name="command-allow-list"></a>
#### Command 허용 목록

Tinker는 자신이 허용할 Artisan 명령어를 "allow" 리스트로 관리합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 사용할 수 있습니다. 더 많은 명령어를 허용하고 싶다면, `tinker.php` 설정 파일의 `commands` 배열에 추가하세요:

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 자동 alias가 되지 않아야 하는 클래스

일반적으로 Tinker는 상호작용 과정에서 클래스를 자동으로 alias 처리합니다. 그러나 특정 클래스는 자동 alias에서 제외하고 싶을 수 있습니다. 이럴 때는 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가하면 됩니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성 (Writing Commands)

Artisan이 기본 제공하는 명령어 외에도 직접 커스텀 명령어를 만들어 사용할 수 있습니다. 명령어는 보통 `app/Console/Commands` 디렉토리 아래에 저장되지만, [다른 디렉토리도 Artisan 명령어로 스캔하도록](#registering-commands) 지정할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성 (Generating Commands)

새로운 명령어를 만들려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉토리 안에 새로운 명령어 클래스를 생성합니다. 해당 디렉토리가 아직 없다면 명령어 실행 시 자동으로 생성됩니다:

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조 (Command Structure)

명령어를 생성한 후에는 `Signature`와 `Description` 속성을 사용하여 명령어의 시그니처와 설명을 정의해야 합니다. `Signature` 속성에서 [명령어의 입력값](#defining-input-expectations) 예상도 함께 지정할 수 있습니다. 명령어가 실행될 때는 `handle` 메서드가 호출되며, 실제 명령어 로직을 이곳에 작성합니다.

아래 예제를 참고하세요. 명령어의 `handle` 메서드에서 원하는 의존성을 자유롭게 요청할 수 있으며, 이는 Laravel의 [서비스 컨테이너](/docs/master/container)가 자동으로 타입힌트된 모든 의존성을 주입합니다:

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;

#[Signature('mail:send {user}')]
#[Description('Send a marketing email to a user')]
class SendEmails extends Command
{
    /**
     * Execute the console command.
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]
> 더 나은 코드 재사용성을 위해, 콘솔 명령어 클래스는 최대한 가볍게 유지하고 실제 작업은 별도의 애플리케이션 서비스(서비스 클래스)에 위임하는 것이 좋은 방법입니다. 위 예시에서도 이메일 전송의 "무거운" 작업을 서비스 클래스에 맡기고 있습니다.

<a name="exit-codes"></a>
#### 종료 코드(Exit Codes)

`handle` 메서드에서 아무 값도 반환하지 않고 명령어가 정상적으로 실행되었다면 종료 코드 `0`으로 성공을 알립니다. 하지만, `handle` 메서드는 원하는 종료 코드를 정수로 직접 지정하여 반환할 수도 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내부에서 언제든지 명령어를 "실패"로 처리하려면 `fail` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 명령어 실행을 중단하고 종료 코드 `1`로 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어 (Closure Commands)

클로저 기반 명령어는 클래스로 명령어를 정의하는 대신 사용할 수 있는 대안 방식입니다. 라우트에서 컨트롤러 대신 클로저를 활용할 수 있듯, 콘솔 명령어도 클래스 대신 클로저로 정의할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션으로 진입하는 콘솔 기반 엔트리 포인트(라우트)를 정의합니다. 이 파일에서 `Artisan::command` 메서드를 이용해 클로저 기반 명령어를 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와, 인수와 옵션을 받는 클로저를 전달받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 해당 명령어 인스턴스에 바인딩되어 있으므로, 클래스 명령어에서 사용하던 모든 헬퍼 메서드를 동일하게 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

클로저 내에서도 명령어의 인수와 옵션 외에, [서비스 컨테이너](/docs/master/container)에서 의존성을 타입힌트로 바로 주입받을 수 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명 추가

클로저 기반 명령어를 정의할 때는 `purpose` 메서드를 사용해 명령어에 설명을 붙일 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 실행 시 표시됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Isolatable 명령어

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 하며, 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

어떤 상황에서는 명령어가 동시에 하나만 실행되도록 제한하고 싶을 수 있습니다. 이런 경우, 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```

`Isolatable`로 지정하면, 해당 명령어에 대해 Artisan이 자동으로 `--isolated` 옵션을 추가합니다(직접 옵션에 추가할 필요 없음). 이 옵션을 사용하여 명령어를 실행할 경우, Laravel은 명령이 이미 실행 중인지 확인하기 위해 애플리케이션의 기본 캐시 드라이버를 사용해 원자적(atomic) 락을 시도합니다. 이미 실행 중인 인스턴스가 있다면 명령어는 실행되지 않고, 성공 상태 코드로 종료합니다:

```shell
php artisan mail:send 1 --isolated
```

실행할 수 없을 때 명령어가 반환해야 하는 종료 코드를 지정하려면, `isolated` 옵션에 값을 전달하세요:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID(Lock ID)

기본적으로 Laravel은 명령어의 이름을 이용해 캐시에 저장될 원자적 락의 문자열 키를 생성합니다. 이 값을 커스터마이징하려면 Artisan 명령어 클래스에 `isolatableId` 메서드를 정의하면 되고, 여기서 명령어 인수나 옵션 등 원하는 값을 포함시킬 수 있습니다:

```php
/**
 * Get the isolatable ID for the command.
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```

<a name="lock-expiration-time"></a>
#### 락 만료 시간(Lock Expiration Time)

기본적으로 isolation 락은 명령어가 종료되면 해제됩니다. 만약 명령이 중단되어 완료되지 않을 경우에는 1시간 뒤에 만료됩니다. 락의 만료 시간을 조정하고 싶다면, 명령어 클래스에서 `isolationLockExpiresAt` 메서드를 정의하면 됩니다:

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->plus(minutes: 5);
}
```

<a name="defining-input-expectations"></a>
## 입력 값 정의 (Defining Input Expectations)

콘솔 명령어에서는 사용자로부터 인수(argument)나 옵션(option)을 통해 입력값을 받는 경우가 많습니다. Laravel은 `signature` 속성을 이용해 명령어에서 예상하는 입력값을 매우 쉽고 직관적인 라우트(route) 형태의 문법으로 정의할 수 있게 해줍니다.

<a name="arguments"></a>
### 인수 (Arguments)

모든 사용자 입력 인수와 옵션은 중괄호로 감쌉니다. 아래 예제는 필수 인수 `user` 하나를 정의하는 방식입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택적으로 만들거나 기본값을 지정할 수도 있습니다:

```php
// 선택 인수...
'mail:send {user?}'

// 선택 인수와 기본값...
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션 (Options)

옵션은 인수와 비슷하지만, 명령줄에서 두 개의 하이픈(`--`)을 붙여 전달하고, 입력값을 받을 수도 있고 그렇지 않을 수도 있습니다. 입력값이 없는 옵션은 boolean "스위치"로 동작합니다. 예시를 살펴보세요:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

여기서 `--queue` 스위치를 명령어 실행 시 지정하면 해당 옵션의 값은 `true`, 지정하지 않으면 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

옵션에 값을 입력받으려면 옵션 이름 뒤에 `=` 기호를 붙여줍니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이 경우, 아래처럼 값과 함께 옵션을 전달할 수 있으며, 옵션을 지정하지 않으면 기본값은 `null`입니다:

```shell
php artisan mail:send 1 --queue=default
```

또한, 옵션 이름 뒤에 기본값을 지정할 수도 있습니다. 사용자가 값을 전달하지 않으면 기본값이 적용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션에 단축키를 추가하고 싶으면, 옵션 정의 시 단축키를 옵션 이름 앞에 `|`로 구분해서 명시하면 됩니다:

```php
'mail:send {user} {--Q|queue=}'
```

명령줄에서 옵션 단축키를 사용할 때는 하이픈 하나(`-`)로 시작하며, 옵션 값에는 `=` 문자를 포함하지 않습니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열 (Input Arrays)

여러 값을 입력받는 인수 또는 옵션을 정의하고 싶다면 `*` 문자를 사용할 수 있습니다. 아래는 여러 사용자를 지정할 수 있는 인수 예제입니다:

```php
'mail:send {user*}'
```

아래와 같이 여러 인수를 순서대로 전달하면, `user` 값이 `[1, 2]`인 배열로 전달됩니다:

```shell
php artisan mail:send 1 2
```

`*` 문자는 선택 인수와 함께 조합하여 0개 이상의 값을 허용하는 배열 인수도 만들 수 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

옵션에 여러 값을 받고 싶다면, 옵션 정의에서 `=*`를 사용하고, 명령어 실행 시 각 값마다 옵션 이름을 붙여 전달하면 됩니다:

```php
'mail:send {--id=*}'
```

명령줄 사용 예시:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명 (Input Descriptions)

명령어의 인수나 옵션에 대한 설명을 입력 이름 뒤에 `:`로 구분하여 추가할 수 있습니다. 명령어 정의가 길어진다면 여러 줄로 나누어 작성해도 됩니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```

<a name="prompting-for-missing-input"></a>
### 누락된 입력에 대한 프롬프트 처리 (Prompting for Missing Input)

필수 인수가 누락된 경우, Laravel은 에러 메시지를 출력합니다. 이 대신, 사용자가 누락한 필수 인수를 자동으로 프롬프트할 수도 있는데, 이 기능은 `PromptsForMissingInput` 인터페이스를 구현하면 사용할 수 있습니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```

Laravel은 필수 인수를 사용자에게 물을 때, 인수 이름이나 설명을 사용해 적절하게 질문합니다. 질문을 직접 커스터마이즈하고 싶다면, `promptForMissingArgumentsUsing` 메서드를 구현하여 인수명에 매핑되는 질문 배열을 반환하면 됩니다:

```php
/**
 * Prompt for missing input arguments using the returned questions.
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => 'Which user ID should receive the mail?',
    ];
}
```

질문과 함께 플레이스홀더 문구도 추가하고 싶다면 튜플 형태로 반환하면 됩니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트를 완전히 제어하고 싶다면, 사용자를 안내하고 값을 반환하는 클로저를 제공합니다:

```php
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: 'Search for a user:',
        placeholder: 'E.g. Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> [!NOTE]
> [Laravel Prompts](/docs/master/prompts) 공식 문서에서는 사용 가능한 프롬프트 및 활용 예시에 대해 더욱 상세한 정보를 제공합니다.

[옵션](#options)을 선택하거나 입력받기 위한 프롬프트는 명령어의 `handle` 메서드에서 추가할 수 있습니다. 하지만, 필수 인수 프롬프트와 연계하여 특정 타이밍에만 옵션 프롬프트를 띄우고 싶다면 `afterPromptingForMissingArguments` 메서드를 구현하면 됩니다:

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * Perform actions after the user was prompted for missing arguments.
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output): void
{
    $input->setOption('queue', confirm(
        label: 'Would you like to queue the mail?',
        default: $this->option('queue')
    ));
}
```

<a name="command-io"></a>
## 명령어 입출력(I/O) (Command I/O)

<a name="retrieving-input"></a>
### 입력값 가져오기 (Retrieving Input)

명령어 실행 중, 인수와 옵션의 값이 필요하다면 `argument`와 `option` 메서드를 사용할 수 있습니다. 만약 해당 인수나 옵션이 없다면 `null`이 반환됩니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 한꺼번에 가져오고 싶다면 `arguments` 메서드를 사용하세요:

```php
$arguments = $this->arguments();
```

옵션 역시 `option` 메서드로 쉽게 가져올 수 있으며, 모두 배열로 받으려면 `options` 메서드를 사용합니다:

```php
// 특정 옵션만...
$queueName = $this->option('queue');

// 모든 옵션을 배열로...
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 프롬프트 (Prompting for Input)

> [!NOTE]
> [Laravel Prompts](/docs/master/prompts)는 명령줄 애플리케이션에 브라우저처럼 사용하기 편리한 입력 폼, 플레이스홀더, 유효성 검증 등을 지원하는 PHP 패키지입니다.

명령어 실행 중 사용자의 값을 직접 입력받고 싶다면, `ask` 메서드를 사용하여 원하는 질문을 던지고, 입력값을 받아올 수 있습니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $name = $this->ask('What is your name?');

    // ...
}
```

`ask` 메서드는 두 번째 인수로 기본값을 줄 수 있습니다. 사용자가 아무것도 입력하지 않을 경우 이 값이 입력값으로 채택됩니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

`secret` 메서드는 `ask`와 비슷하지만, 콘솔 입력 중 사용자가 친 값이 화면에 표시되지 않습니다. 비밀번호처럼 민감한 정보를 문의할 때 사용합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인(Confirmation) 요청

"예/아니오" 식으로 간단한 확인을 받고 싶을 때는 `confirm` 메서드를 사용할 수 있습니다. 기본적으로 사용자가 `y` 또는 `yes`를 입력하면 `true`, 그렇지 않으면 `false`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

기본값을 `true`로 지정하고 싶다면 두 번째 인수로 `true` 값을 넣으세요:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동완성(Auto-Completion)

`anticipate` 메서드는 여러 후보 중 입력값을 자동완성으로 제안할 수 있도록 도와줍니다. 사용자는 자동완성 힌트에 없는 답도 자유롭게 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인수로 클로저를 넘겨, 사용자가 입력하는 값마다 동적으로 후보 목록을 생성할 수도 있습니다:

```php
use App\Models\Address;

$name = $this->anticipate('What is your address?', function (string $input) {
    return Address::whereLike('name', "{$input}%")
        ->limit(5)
        ->pluck('name')
        ->all();
});
```

<a name="multiple-choice-questions"></a>
#### 다중 선택(Multiple Choice) 질문

정해진 후보 중에서 사용자가 하나를 선택하도록 안내할 때는 `choice` 메서드를 사용합니다. 기본값으로 반환할 후보 인덱스는 세 번째 인수로 지정합니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

네 번째, 다섯 번째 인수로는 유효한 답변을 입력할 수 있는 최대 시도 횟수, 다중 선택 가능 여부 등을 지정할 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```

<a name="writing-output"></a>
### 출력 작성 (Writing Output)

콘솔에 출력을 보내려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error` 등의 메서드를 사용할 수 있습니다. 각 메서드는 용도에 따라 적합한 ANSI 컬러로 동작합니다. 예를 들어, 사용자에게 일반적인 정보를 주고 싶으면 `info` 메서드를 사용하며, 출력은 녹색으로 표시되는 경우가 많습니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    // ...

    $this->info('The command was successful!');
}
```

에러 메시지를 출력하려면 `error` 메서드를 사용하면 되고, 텍스트는 주로 빨간색입니다:

```php
$this->error('Something went wrong!');
```

단순한(무색상) 출력을 원하면 `line` 메서드를 사용합니다:

```php
$this->line('Display this on the screen');
```

공백 줄을 출력하려면 `newLine`을 이용하세요:

```php
// 한 줄 공백 출력
$this->newLine();

// 세 줄 공백 출력
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블(Tables) 출력

`table` 메서드는 여러 행과 컬럼으로 구성된 데이터를 예쁘게 표 형식으로 출력하는 데 도움이 됩니다. 컬럼 이름과 데이터만 전달하면 Laravel이 적절한 테이블 폭과 높이를 계산해 표시해줍니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행 바(Progress Bars)

작업 실행 시간이 길어질 때, 사용자에게 진행률을 보여주는 것도 좋습니다. `withProgressBar` 메서드를 사용하면, 주어진 반복(iterable) 값을 순회하며 자동으로 진행 바가 출력됩니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

더 세밀하게 진행 바를 제어하고 싶으면, 전체 반복 횟수를 지정 후 항목 처리마다 수동으로 진행 바를 advance 하면 됩니다:

```php
$users = App\Models\User::all();

$bar = $this->output->createProgressBar(count($users));

$bar->start();

foreach ($users as $user) {
    $this->performTask($user);

    $bar->advance();
}

$bar->finish();
```

> [!NOTE]
> 좀 더 다양한 옵션은 [Symfony Progress Bar 컴포넌트 공식 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록 (Registering Commands)

Laravel은 기본적으로 `app/Console/Commands` 디렉토리 내의 모든 명령어를 자동으로 등록합니다. 하지만, `bootstrap/app.php` 파일의 `withCommands` 메서드에 경로를 추가하여 다른 디렉토리의 명령어도 Artisan이 인식하게 할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

필요하다면 명령어 클래스 이름을 직접 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 실행될 때, 모든 명령어는 [서비스 컨테이너](/docs/master/container)에 의해 해석되어 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 명령어의 코드 실행 (Programmatically Executing Commands)

CLI 이외의 코드(예: 라우트, 컨트롤러)에서 Artisan 명령어를 실행해야 할 때가 있습니다. 이 경우, `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. 첫 번째 인수로 명령어의 시그니처 또는 클래스 이름, 두 번째 인수로 명령어에 전달할 매개변수 배열을 넘기면, 종료 코드를 반환합니다:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

또는, 전체 Artisan 명령어 문자열을 전달할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 값 전달

명령어 옵션이 배열을 받도록 정의되어 있다면, 값 배열을 그대로 넘기면 됩니다:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```

<a name="passing-boolean-values"></a>
#### 불리언 값 전달

옵션이 문자열이 아닌 값을 요구할 경우(예: `migrate:refresh` 명령의 `--force` 플래그 등), `true` 또는 `false` 값을 직접 넘기면 됩니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉(Queueing)

`Artisan` 파사드의 `queue` 메서드를 이용하면 Artisan 명령어 실행 자체를 [큐 워커](/docs/master/queues)가 백그라운드에서 처리하도록 큐잉할 수 있습니다. 사용 전 큐 설정과 큐 리스너가 작동 중인지 확인하세요:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

`onConnection`, `onQueue` 메서드로 명령어가 디스패치될 연결과 큐 이름도 직접 지정할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 명령어 내에서 다른 명령어 호출 (Calling Commands From Other Commands)

기존 Artisan 명령어 내에서 또 다른 명령어를 호출해야 할 때가 있습니다. 이럴 때는 `call` 메서드를 사용하며, 첫 번째 인수로 명령어 이름, 두 번째 인수로 매개변수 배열을 넘깁니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```

다른 명령어의 출력을 숨기고 싶을 땐 `callSilently` 메서드를 사용하세요. 사용법은 `call` 메서드와 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리 (Signal Handling)

운영체제는 실행 중인 프로세스에 다양한 시그널을 보낼 수 있습니다. 예를 들어, `SIGTERM`은 프로그램에 종료를 요청하는 신호입니다. Artisan 콘솔 명령어에서 이런 시그널을 수신하고, 그에 맞춰 코드를 실행하고 싶다면 `trap` 메서드를 사용할 수 있습니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

여러 시그널을 동시에 감지하고자 한다면 배열로 전달하면 됩니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁(stub) 커스터마이징 (Stub Customization)

Artisan 콘솔의 `make` 계열 명령어는 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 자동 생성합니다. 이때 "스텁(stub)" 파일을 템플릿으로 사용해 여러분의 입력에 맞게 내용을 채워줍니다. 이런 스텁 파일을 직접 수정하고 싶다면, `stub:publish` 명령어를 통해 애플리케이션에 기본 스텁 파일을 발행할 수 있습니다:

```shell
php artisan stub:publish
```

발행된 스텁 파일은 애플리케이션 루트의 `stubs` 디렉토리에 저장됩니다. 수정한 내용은 Artisan의 관련 `make` 명령어 실행시 반영됩니다.

<a name="events"></a>
## 이벤트 (Events)

Artisan이 명령어를 실행할 때, 총 세 가지 이벤트가 발생합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.  
- `ArtisanStarting` 이벤트는 Artisan이 실행 시작 시 바로 발생합니다.  
- 그 다음, 각 명령어 실행 바로 직전에 `CommandStarting` 이벤트가 발생합니다.  
- 마지막으로 명령어 실행이 끝나면 `CommandFinished` 이벤트가 발생합니다.
