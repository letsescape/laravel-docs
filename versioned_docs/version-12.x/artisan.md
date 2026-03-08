# 아티즌 콘솔 (Artisan Console)

- [소개](#introduction)
    - [Tinker (REPL)](#tinker)
- [명령어 작성](#writing-commands)
    - [명령어 생성](#generating-commands)
    - [명령어 구조](#command-structure)
    - [클로저 명령어](#closure-commands)
    - [Isolatable 명령어](#isolatable-commands)
- [입력 기대 정의](#defining-input-expectations)
    - [인수](#arguments)
    - [옵션](#options)
    - [입력 배열](#input-arrays)
    - [입력 설명](#input-descriptions)
    - [입력 누락 시 프롬프트](#prompting-for-missing-input)
- [명령어 I/O](#command-io)
    - [입력값 가져오기](#retrieving-input)
    - [입력 요청](#prompting-for-input)
    - [출력 작성](#writing-output)
- [명령어 등록](#registering-commands)
- [프로그램적으로 명령어 실행](#programmatically-executing-commands)
    - [명령어에서 명령어 호출](#calling-commands-from-other-commands)
- [시그널 처리](#signal-handling)
- [스텁(stub) 커스터마이징](#stub-customization)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

Artisan은 Laravel에 기본 포함된 커맨드 라인 인터페이스입니다. Artisan은 애플리케이션의 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 구축하는 동안 도움을 줄 수 있는 다양한 유용한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 확인하려면 `list` 명령어를 사용할 수 있습니다:

```shell
php artisan list
```

각 명령어에는 도움말 화면이 포함되어 있으며, 명령어에서 사용할 수 있는 인수 및 옵션을 표시하고 설명합니다. 도움말 화면을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
#### Laravel Sail

[Laravel Sail](/docs/12.x/sail)을 로컬 개발 환경으로 사용하는 경우, Artisan 명령어를 실행할 땐 반드시 `sail` 커맨드를 사용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
### Tinker (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 Laravel 프레임워크용 강력한 REPL(Read–Eval–Print Loop)로, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 합니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 Tinker가 기본으로 포함되어 있습니다. 하지만 애플리케이션에서 Tinker를 삭제한 경우에는 Composer로 다시 설치할 수 있습니다:

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 **핫 리로딩**, 멀티라인 코드 에디팅, 자동완성 등 편리한 기능이 필요하다면 [Tinkerwell](https://tinkerwell.app)을 참고해 보세요!

<a name="usage"></a>
#### 사용법

Tinker를 통해 Eloquent 모델, 작업(jobs), 이벤트 등 애플리케이션 전체와 커맨드 라인에서 상호작용할 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행하세요.

```shell
php artisan tinker
```

`vendor:publish` 명령어를 통해 Tinker의 설정 파일을 퍼블리시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 Tinker에서 잡을 디스패치할 때는 `Bus::dispatch`나 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 허용 명령어 목록(Allow List)

Tinker는 쉘 내에서 실행할 수 있는 Artisan 명령어를 "허용 목록"을 통해 제한합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어만 실행할 수 있습니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가하세요.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
#### 에일리어싱하지 않을 클래스 지정

일반적으로 Tinker는 상호작용하는 클래스들을 자동으로 에일리어싱(별칭)합니다. 하지만 특정 클래스는 절대로 에일리어싱하지 않도록 제한할 수도 있습니다. `tinker.php` 설정 파일의 `dont_alias` 배열에 클래스를 추가해 지정할 수 있습니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
## 명령어 작성

Artisan이 기본 제공하는 명령어 외에도, 직접 커스텀 명령어를 만들 수 있습니다. 명령어 클래스는 보통 `app/Console/Commands` 디렉터리에 저장하지만, [다른 디렉터리에서도 Artisan 명령어를 스캔](#registering-commands)하도록 지정하면 자유롭게 경로를 설정할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성

새로운 명령어를 생성하려면 `make:command` Artisan 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리 아래에 새로운 명령어 클래스를 만듭니다. 이 디렉터리가 없다면 처음 명령어를 생성할 때 자동으로 생성됩니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
### 명령어 구조

명령어를 생성한 후에는, 클래스의 `signature`와 `description` 속성에 알맞은 값을 지정해야 합니다. 이 속성들은 `list` 명령어로 명령어 목록을 표시할 때 사용됩니다. 또한 `signature` 속성을 통해 [명령어의 입력 기대값](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행되면 `handle` 메서드가 호출되며, 명령어 로직은 이 메서드에 작성합니다.

다음은 명령어 예시입니다. `handle` 메서드에서 필요한 의존성을 요청할 수 있다는 점에 주목하세요. Laravel의 [서비스 컨테이너](/docs/12.x/container)는 명시적으로 타입힌트된 모든 의존성을 자동으로 주입합니다:

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Command;

class SendEmails extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Send a marketing email to a user';

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
> 코드 재사용성을 높이기 위해, 콘솔 명령어는 최대한 간결하게 작성하고 애플리케이션 서비스에 실제 작업을 위임하는 것이 좋습니다. 위 예제에서 이메일 전송의 “실제 작업”을 서비스 클래스에 맡긴 모습을 볼 수 있습니다.

<a name="exit-codes"></a>
#### 종료 코드(Exit Codes)

`handle` 메서드에서 아무것도 반환하지 않고 정상적으로 명령어가 실행된 경우, 명령어는 ‘0’ 종료 코드(성공)를 반환합니다. 하지만 필요하다면 `handle` 메서드에서 직접 정수형 반환값을 지정해 종료 코드를 컨트롤할 수 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```

명령어 내 모든 메서드에서 명시적으로 실패 처리하려면 `fail` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 명령어의 실행을 중단하고 종료 코드 1을 반환합니다:

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
### 클로저 명령어

클로저(익명 함수) 기반 명령어는 명령어 클래스를 정의하는 대신 사용할 수 있는 대체 방식입니다. 라우트 클로저가 컨트롤러의 대체 용도인 것과 유사하게, 클로저 명령어도 명령어 클래스의 대안입니다.

`routes/console.php` 파일은 HTTP 라우트가 아닌, 콘솔을 통한 애플리케이션 진입점(라우트)을 정의합니다. 이 파일에서 `Artisan::command` 메서드를 사용해 모든 클로저 기반 콘솔 명령어를 정의할 수 있습니다. `command` 메서드는 [명령어 시그니처](#defining-input-expectations)와 명령어 인수 및 옵션을 받는 클로저를 인자로 받습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

클로저는 내부적으로 명령어 인스턴스에 바인딩되기 때문에, 명령어 클래스에서 사용 가능한 모든 헬퍼 메서드를 그대로 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 의존성 타입힌트

클로저 명령어에서도 명령어 인수 및 옵션 외에 추가적인 의존성을 [서비스 컨테이너](/docs/12.x/container)에서 타입힌트 방식으로 주입받을 수 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
#### 클로저 명령어 설명

클로저 기반 명령어 정의 시 `purpose` 메서드를 사용해 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help`로 확인할 수 있습니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
### Isolatable 명령어

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나를 사용해야 하며, 모든 서버가 같은 중앙 캐시 서버와 통신해야 합니다.

하나의 명령어 인스턴스만 동시 실행되도록 보장하고 싶을 때가 있습니다. 이 경우 명령어 클래스에서 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하세요:

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

명령어를 `Isolatable`로 표시하면 해당 명령어의 옵션에 `--isolated`가 자동으로 추가되며, 이 옵션을 명시적으로 선언할 필요가 없습니다. 해당 옵션으로 명령어를 실행하면, Laravel은 해당 명령어가 이미 실행 중인지 확인하여, 실행 중이 아니라면 원자적(atomic) 락을 기본 캐시 드라이버를 통해 획득합니다. 이미 다른 인스턴스가 실행 중이면 명령어는 실행되지 않지만, 성공 상태 코드로 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```

명령어 실행 불가 시 반환할 상태 코드를 지정하고자 한다면 `isolated` 옵션에 원하는 코드를 전달하세요:

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
#### 락 ID 지정

기본적으로 라라벨은 명령어 이름을 기반으로 락에 사용할 문자열 키를 생성합니다. 하지만 `isolatableId` 메서드를 명령어 클래스에 정의하면, 인수나 옵션 값을 포함하여 이 키를 커스터마이징할 수 있습니다:

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
#### 락 만료 시간

기본적으로 isolation 락은 명령어가 종료될 때 만료되며, 만약 중단 등으로 정상 종료되지 않으면 1시간 후 만료됩니다. 락 만료 시간을 커스터마이징하려면 `isolationLockExpiresAt` 메서드를 정의하세요:

```php
use DateTimeInterface;
use DateInterval;

/**
 * 락의 만료 시점 반환
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->plus(minutes: 5);
}
```

<a name="defining-input-expectations"></a>
## 입력 기대 정의

콘솔 명령어 작성 시에는, 사용자의 입력을 인수(argument)나 옵션(option)으로 받아야 할 때가 많습니다. Laravel은 명령어의 `signature` 속성을 통해 입력의 이름, 인수, 옵션을 라우트 시그니처와 유사한 문법으로 일관성 있게 정의할 수 있도록 지원합니다.

<a name="arguments"></a>
### 인수

모든 사용자 입력 인수와 옵션은 중괄호로 감싸서 정의합니다. 아래 예제에서 명령어는 필수 인수 `user`를 정의하고 있습니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

인수를 선택적으로 만들거나 기본값을 설정할 수도 있습니다:

```php
// 선택적 인수
'mail:send {user?}'

// 선택적 인수 + 기본값
'mail:send {user=foo}'
```

<a name="options"></a>
### 옵션

옵션도 인수와 마찬가지로 사용자 입력의 한 방식입니다. 옵션은 명령줄에서 두 개의 하이픈(`--`)으로 접두됩니다. 옵션에는 값을 받는 타입과, 값을 받지 않는 부울(boolean) “스위치” 타입 두 가지가 있습니다. 아래는 스위치 타입 옵션의 예시입니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

위 예시에서는 명령어 실행 시 `--queue` 스위치를 지정할 수 있습니다. 전달되면 옵션 값은 `true`, 누락 시에는 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
#### 값이 있는 옵션

다음은 값을 필요로 하는 옵션 예시입니다. 옵션 이름 뒤에 등호(`=`)를 붙여 정의하면 사용자가 값을 반드시 지정해야 합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

이 경우 명령어 실행 시 다음과 같이 값을 전달해야 하며, 옵션이 생략되면 값은 `null`이 됩니다:

```shell
php artisan mail:send 1 --queue=default
```

옵션에 기본값을 지정하려면 옵션 이름 뒤에 기본값을 추가하세요. 사용자가 값을 전달하지 않으면 이 값이 적용됩니다:

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션 정의 시, `|` 구분자를 이용해 전체 옵션 이름 앞에 단축키(한 글자)를 지정할 수 있습니다:

```php
'mail:send {user} {--Q|queue=}'
```

터미널에서 옵션 단축키를 사용할 때는 하이픈 하나만 붙이고, 값에는 `=` 없이 바로 이어서 씁니다:

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
### 입력 배열

인수나 옵션이 복수의 입력값을 받기를 원한다면, `*` 문자를 이용하세요. 아래는 인수에 대해 배열 형태로 입력을 받을 때 예시입니다:

```php
'mail:send {user*}'
```

이 경우, 명령어 실행 시 여러 개 인수를 연속적으로 전달할 수 있고, 명령어에서는 `user`가 `[1, 2]`와 같이 배열로 전달됩니다:

```shell
php artisan mail:send 1 2
```

`*` 문자를 선택적 인수와 함께 사용하면, 인수의 개수를 0개 이상으로 허용할 수 있습니다:

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
#### 옵션 배열

복수의 값을 받는 옵션 역시, 전달할 옵션 이름마다 개별적으로 값을 붙여서 여러 번 전달하면 됩니다:

```php
'mail:send {--id=*}'
```

명령어 실행 시 아래와 같이 각각 값을 붙여 전달할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
### 입력 설명

입력 인수나 옵션에 설명을 추가할 때는 인수/옵션 이름과 설명을 콜론(`:`)으로 구분하면 됩니다. 명령어 정의가 길어질 경우, 여러 줄로 나누어 작성해도 무방합니다:

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
### 입력 누락 시 프롬프트

명령어에 필수 인수가 있을 때 사용자가 입력하지 않으면, 일반적으로 에러 메시지가 표시됩니다. 그러나 명령어에서 `PromptsForMissingInput` 인터페이스를 구현하면, 누락된 필수 인수에 대해 자동으로 프롬프트가 표시되어 사용자의 입력을 유도할 수 있습니다:

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

Laravel이 필수 인수를 직접 받아야 할 때, 인수 이름이나 설명에 기반하여 자동으로 질문을 생성해 사용자의 입력을 요청합니다. 질문을 커스터마이징하고 싶다면 `promptForMissingArgumentsUsing` 메서드를 구현하여, 인수 이름을 키로 가지는 질문 문자열의 배열을 반환하세요:

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

질문과 함께 플레이스홀더도 제공하려면, 질문 – 플레이스홀더를 튜플 형태(배열)로 지정할 수 있습니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

프롬프트 동작 전체를 완전히 제어하고 싶다면 사용자를 프롬프트하고 값을 반환하는 클로저를 사용할 수 있습니다:

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
> [Laravel Prompts](/docs/12.x/prompts) 공식 문서에서 사용 가능한 프롬프트 유형들과 더 많은 옵션을 확인할 수 있습니다.

[옵션](#options)을 선택 또는 입력받는 프롬프트를 제공하려면 명령어의 `handle` 메서드 안에서 직접 프롬프트 코드를 작성하면 됩니다. 하지만, 누락된 인수 자동 프롬프트가 끝난 직후에만 별도 프롬프트를 띄우고 싶다면 `afterPromptingForMissingArguments` 메서드를 구현할 수 있습니다:

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
## 명령어 I/O

<a name="retrieving-input"></a>
### 입력값 가져오기

명령어 실행 중에는 정의한 인수와 옵션의 값을 얻어야 할 필요가 있습니다. 이때는 `argument`와 `option` 메서드를 사용하세요. 해당 인수 또는 옵션이 없으면 `null`을 반환합니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

모든 인수를 배열로 한 번에 얻으려면 `arguments` 메서드를 호출하세요:

```php
$arguments = $this->arguments();
```

옵션도 마찬가지로 단일 옵션 값을 `option`으로, 전체 옵션을 배열로는 `options` 메서드로 얻을 수 있습니다:

```php
// 특정 옵션 값 조회
$queueName = $this->option('queue');

// 모든 옵션값 배열로 조회
$options = $this->options();
```

<a name="prompting-for-input"></a>
### 입력 요청

> [!NOTE]
> [Laravel Prompts](/docs/12.x/prompts)는 커맨드라인 애플리케이션에서 플레이스홀더, 유효성검사 등 브라우저와 유사한 사용자 경험을 제공하는 아름답고 사용하기 쉬운 폼 생성을 도와주는 PHP 패키지입니다.

콘솔에 메시지를 출력하는 것 외에도, 실행 중인 명령어에서 사용자의 입력을 직접 요청할 수도 있습니다. `ask` 메서드는 질문을 출력, 사용자의 입력을 받아, 반환합니다:

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

`ask` 메서드는 두 번째 인수로 기본값을 받을 수 있습니다. 사용자가 입력을 생략하면 이 값이 반환됩니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```

민감한 정보를 받아야 한다면 `secret` 메서드를 사용하세요. 이 메서드는 입력한 내용이 터미널에 표시되지 않으므로 비밀번호 등 용도에 적합합니다:

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
#### 확인 요청

사용자에게 "예/아니요" 식의 간단한 확인을 요청해야 하는 경우 `confirm` 메서드를 사용하세요. 이 메서드는 기본적으로 `false`를 반환하지만, 사용자가 `y` 또는 `yes`를 입력하면 `true`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

두 번째 인수로 `true`를 전달하면, 별도 입력 없이 엔터를 누를 경우 기본값을 `true`로 간주합니다:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
#### 자동완성(Auto-Completion)

`anticipate` 메서드는 사용자가 입력 중일 때 자동완성 힌트를 제공할 수 있습니다. 사용자는 힌트와 무관하게 아무 값이나 입력할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

또는 두 번째 인자로 클로저를 전달해, 사용자가 입력할 때마다 해당 입력값을 기반으로 동적으로 자동완성 리스트를 반환할 수도 있습니다:

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
#### 다중 선택(선택지 제공) 질문

사용자에게 미리 정해진 선택지 중에서 선택을 요청하려면 `choice` 메서드를 사용하세요. 세 번째 인수로 선택지에서 기본값으로 표시할 인덱스를 전달할 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

또한, `choice` 메서드는 최대 시도 횟수(4번째 인수), 복수 선택 허용 여부(5번째 인수)를 추가적으로 지정할 수 있습니다:

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
### 출력 작성

콘솔에 메시지를 출력하려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error`와 같은 다양한 메서드를 사용할 수 있습니다. 각 메서드는 용도에 맞는 ANSI 컬러가 적용됩니다. 예를 들면, `info`는 일반적으로 초록색으로 표시되어 정보를 알릴 때 사용합니다:

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

에러 메시지는 `error` 메서드를 사용하며, 일반적으로 빨간색으로 출력됩니다:

```php
$this->error('Something went wrong!');
```

단순 텍스트를 컬러 없이 출력하려면 `line` 메서드를 사용합니다:

```php
$this->line('Display this on the screen');
```

공백 줄을 생성하고 싶으면 `newLine` 메서드를 사용하세요:

```php
// 한 줄 공백
$this->newLine();

// 세 줄 공백
$this->newLine(3);
```

<a name="tables"></a>
#### 테이블 출력

`table` 메서드를 사용하면 여러 행/열로 이루어진 데이터를 보기 좋게 테이블 형태로 출력할 수 있습니다. 컬럼 명과 데이터만 넘겨주면 적절한 크기의 테이블로 자동 정렬됩니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
#### 진행률 표시줄(Progress Bar)

실행 시간이 긴 작업에서는 진행 상황을 시각적으로 보여주면 좋습니다. `withProgressBar`를 사용하면, 지정한 이터러블 값을 순회할 때마다 진행률이 자동으로 표시됩니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

직접 진행률 바의 제어가 필요할 경우, 먼저 전체 스텝 개수를 정의하고, 각 아이템 처리 후 바를 수동으로 advance 하세요:

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
> 더 고급 기능이 필요하다면 [Symfony Progress Bar 컴포넌트 공식 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
## 명령어 등록

기본적으로 Laravel은 `app/Console/Commands` 디렉터리에 있는 모든 명령어를 자동으로 등록합니다. 하지만 필요에 따라 `bootstrap/app.php` 파일의 `withCommands` 메서드를 이용해 다른 디렉터리도 스캔하도록 지정할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

또는, 특정 명령어 클래스를 명시적으로 배열에 추가하여 수동으로 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

Artisan이 부팅되면, 애플리케이션의 모든 명령어가 [서비스 컨테이너](/docs/12.x/container)에서 해결(resolve)되어 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그램적으로 명령어 실행

CLI 환경이 아닌 곳에서 Artisan 명령어를 실행하고자 할 때도 있습니다. 예를 들어 라우트나 컨트롤러 내부에서 Artisan 명령어를 호출하고 싶을 때, `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. `call` 메서드는 첫 번째 인수로 명령어 시그니처명 또는 클래스명, 두 번째 인수로 파라미터 배열을 받으며, 반환값은 종료 코드입니다:

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

또는, 전체 Artisan 명령어를 문자열로 넘겨 사용할 수도 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
#### 배열 입력값 전달

명령어에서 배열을 받는 옵션이 정의되어 있다면, 배열 값을 옵션에 전달할 수 있습니다:

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
#### 불리언 입력값 전달

문자열 값이 필요한 옵션이 아닌, 예를 들어 `migrate:refresh` 명령어의 `--force` 플래그와 동시에 사용하고 싶다면, 옵션 값을 `true` 혹은 `false`로 전달할 수 있습니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
#### Artisan 명령어 큐잉

`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 [큐 워커](/docs/12.x/queues)에서 백그라운드로 처리하게 할 수 있습니다. 사용전에 큐 환경 설정과 큐 리스너 동작을 반드시 확인하세요:

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

`onConnection`, `onQueue` 메서드를 사용하면 명령어를 보낼 연결(connection)이나 큐(queue)를 지정할 수도 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
### 명령어에서 명령어 호출

기존 Artisan 명령어에서 다른 명령어를 실행하고 싶을 때가 있습니다. 이럴 때는 `call` 메서드를 사용하세요. 명령어 이름, 인수/옵션 배열을 전달합니다:

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

다른 콘솔 명령어를 호출할 때 출력까지 모두 숨기고 싶다면, `callSilently` 메서드를 사용하세요. 사용법은 `call`과 동일합니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
## 시그널 처리

운영체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어 `SIGTERM`은 프로그램에 종료를 요청할 때 사용됩니다. Artisan 콘솔 명령어에서 이런 시그널을 감지하고 특정 코드를 실행하려면 `trap` 메서드를 사용할 수 있습니다:

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

여러 개 시그널을 동시에 감지하려면 배열로 전달하면 됩니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
## 스텁(stub) 커스터마이징

Artisan 콘솔의 `make` 명령어들은 컨트롤러, 잡(jobs), 마이그레이션, 테스트 등 다양한 클래스를 생성하는 데 사용됩니다. 이 클래스 생성은 미리 작성된 "stub" 파일을 기반으로, 입력에 따라 값이 채워져 만들어집니다. 보다 세밀하게 Artisan에서 생성하는 파일을 조정하고 싶다면, `stub:publish` 명령어로 가장 일반적인 스텁파일을 애플리케이션으로 복사해 수정할 수 있습니다:

```shell
php artisan stub:publish
```

퍼블리시된 스텁은 애플리케이션 루트에 `stubs` 디렉터리로 저장됩니다. 이 파일들을 수정하면, 해당 `make` 명령어로 생성하는 클래스에 곧바로 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령어 실행 시 세 가지 이벤트를 디스패치합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`.  
`ArtisanStarting` 이벤트는 Artisan이 시작하는 즉시 디스패치됩니다. 이어서 명령어 실행 직전에는 `CommandStarting`, 명령어 실행이 끝나면 `CommandFinished` 이벤트가 각각 디스패치됩니다.
