<!-- # Artisan Console -->
# Artisan Console

- [Introduction](#introduction)
    - [Tinker (REPL)](#tinker)
- [Writing Commands](#writing-commands)
    - [Generating Commands](#generating-commands)
    - [Command Structure](#command-structure)
    - [Closure Commands](#closure-commands)
    - [Isolatable Commands](#isolatable-commands)
- [Defining Input Expectations](#defining-input-expectations)
    - [Arguments](#arguments)
    - [Options](#options)
    - [Input Arrays](#input-arrays)
    - [Input Descriptions](#input-descriptions)
    - [Prompting for Missing Input](#prompting-for-missing-input)
- [Command I/O](#command-io)
    - [Retrieving Input](#retrieving-input)
    - [Prompting for Input](#prompting-for-input)
    - [Writing Output](#writing-output)
- [Registering Commands](#registering-commands)
- [Programmatically Executing Commands](#programmatically-executing-commands)
    - [Calling Commands From Other Commands](#calling-commands-from-other-commands)
- [Signal Handling](#signal-handling)
- [Stub Customization](#stub-customization)
- [Events](#events)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Artisan is the command line interface included with Laravel. Artisan exists at the root of your application as the `artisan` script and provides a number of helpful commands that can assist you while you build your application. To view a list of all available Artisan commands, you may use the `list` command: -->
Artisan은 Laravel에 포함된 명령줄 인터페이스입니다. Artisan은 애플리케이션 루트에 `artisan` 스크립트로 존재하며, 애플리케이션을 개발하는 동안 도움이 되는 여러 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어 목록을 보려면 `list` 명령어를 사용할 수 있습니다.

```shell
php artisan list
```

<!-- Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`: -->
모든 명령어에는 해당 명령어에서 사용할 수 있는 인수와 옵션을 표시하고 설명하는 "help" 화면도 포함되어 있습니다. help 화면을 보려면 명령어 이름 앞에 `help`를 붙입니다.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
<!-- #### Laravel Sail -->
#### Laravel Sail

<!-- If you are using [Laravel Sail](/docs/13.x/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers: -->
로컬 개발 환경으로 [Laravel Sail](/docs/13.x/sail)을 사용하고 있다면, Artisan 명령어를 호출할 때 `sail` 명령줄을 사용해야 한다는 점을 기억하세요. Sail은 애플리케이션의 Docker 컨테이너 안에서 Artisan 명령어를 실행합니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
<!-- ### Tinker (REPL) -->
### Tinker (REPL)

<!-- [Laravel Tinker](https://github.com/laravel/tinker) is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package. -->
[Laravel Tinker](https://github.com/laravel/tinker)는 [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 동작하는 Laravel 프레임워크용 강력한 REPL입니다.

<a name="installation"></a>
<!-- #### Installation -->
#### Installation

<!-- All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application: -->
모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 하지만 애플리케이션에서 Tinker를 이전에 제거했다면 Composer를 사용하여 다시 설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 핫 리로딩, 여러 줄 코드 편집, 자동 완성을 찾고 있나요? [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
<!-- #### Usage -->
#### Usage

<!-- Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command: -->
Tinker를 사용하면 명령줄에서 Eloquent 모델, 작업, 이벤트 등을 포함한 Laravel 애플리케이션 전체와 상호작용할 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행합니다.

```shell
php artisan tinker
```

<!-- You can publish Tinker's configuration file using the `vendor:publish` command: -->
`vendor:publish` 명령어를 사용하여 Tinker의 설정 파일을 게시할 수 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 작업을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 Tinker를 사용할 때는 작업을 디스패치하려면 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
<!-- #### Command Allow List -->
#### Command Allow List

<!-- Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, and `optimize` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file: -->
Tinker는 셸 안에서 실행할 수 있는 Artisan 명령어를 결정하기 위해 "allow" 목록을 사용합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 더 많은 명령어를 허용하려면 `tinker.php` 설정 파일의 `commands` 배열에 추가할 수 있습니다.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
<!-- #### Classes That Should Not Be Aliased -->
#### Classes That Should Not Be Aliased

<!-- Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file: -->
일반적으로 Tinker는 Tinker에서 클래스와 상호작용할 때 해당 클래스에 자동으로 별칭을 지정합니다. 하지만 일부 클래스는 절대 별칭으로 지정하지 않기를 원할 수 있습니다. 이 경우 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 나열하면 됩니다.

```php
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
<!-- ## Writing Commands -->
## Writing Commands

<!-- In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as you instruct Laravel to [scan other directories for Artisan commands](#registering-commands). -->
Artisan에서 제공하는 명령어 외에도 직접 커스텀 명령어를 만들 수 있습니다. 명령어는 일반적으로 `app/Console/Commands` 디렉터리에 저장되지만, Laravel에 [scan other directories for Artisan commands](#registering-commands) 지시한다면 원하는 저장 위치를 자유롭게 선택할 수 있습니다.

<a name="generating-commands"></a>
<!-- ### Generating Commands -->
### Generating Commands

<!-- To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command: -->
새 명령어를 생성하려면 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉터리에 새 명령어 클래스를 생성합니다. 애플리케이션에 이 디렉터리가 없어도 걱정하지 마세요. `make:command` Artisan 명령어를 처음 실행할 때 생성됩니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
<!-- ### Command Structure -->
### Command Structure

<!-- After generating your command, you should define the command's signature and description using the `Signature` and `Description` attributes. The `Signature` attribute also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method. -->
명령어를 생성한 후에는 `Signature`와 `Description` 속성을 사용하여 명령어의 시그니처와 설명을 정의해야 합니다. `Signature` 속성을 사용하면 [your command's input expectations](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행되면 `handle` 메서드가 호출됩니다. 이 메서드 안에 명령어 로직을 작성할 수 있습니다.

<!-- Let's take a look at an example command. Note that we are able to request any dependencies we need via the command's `handle` method. The Laravel [service container](/docs/13.x/container) will automatically inject all dependencies that are type-hinted in this method's signature: -->
예제 명령어를 살펴보겠습니다. 명령어의 `handle` 메서드를 통해 필요한 의존성을 요청할 수 있다는 점에 주목하세요. Laravel [service container](/docs/13.x/container)는 이 메서드의 시그니처에 타입 힌트된 모든 의존성을 자동으로 주입합니다.

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
> 코드를 더 잘 재사용하려면 콘솔 명령어는 가볍게 유지하고, 실제 작업은 애플리케이션 서비스에 위임하는 것이 좋습니다. 위 예제에서는 이메일 전송이라는 "무거운 작업"을 수행하기 위해 서비스 클래스를 주입한다는 점에 주목하세요.

<a name="exit-codes"></a>
<!-- #### Exit Codes -->
#### Exit Codes

<!-- If nothing is returned from the `handle` method and the command executes successfully, the command will exit with a `0` exit code, indicating success. However, the `handle` method may optionally return an integer to manually specify the command's exit code: -->
`handle` 메서드에서 아무것도 반환하지 않고 명령어가 성공적으로 실행되면, 명령어는 성공을 의미하는 `0` 종료 코드로 종료됩니다. 하지만 `handle` 메서드는 명령어의 종료 코드를 직접 지정하기 위해 선택적으로 정수를 반환할 수 있습니다.

```php
$this->error('Something went wrong.');

return 1;
```

<!-- If you would like to "fail" the command from any method within the command, you may utilize the `fail` method. The `fail` method will immediately terminate execution of the command and return an exit code of `1`: -->
명령어 안의 어떤 메서드에서든 명령어를 "실패" 처리하고 싶다면 `fail` 메서드를 사용할 수 있습니다. `fail` 메서드는 즉시 명령어 실행을 종료하고 `1` 종료 코드를 반환합니다.

```php
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
<!-- ### Closure Commands -->
### Closure Commands

<!-- Closure-based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. -->
클로저 기반 명령어는 콘솔 명령어를 클래스로 정의하는 방식의 대안입니다. 라우트 클로저가 컨트롤러의 대안인 것처럼, 명령어 클로저는 명령어 클래스의 대안이라고 생각하면 됩니다.

<!-- Even though the `routes/console.php` file does not define HTTP routes, it defines console-based entry points (routes) into your application. Within this file, you may define all of your closure-based console commands using the `Artisan::command` method. The `command` method accepts two arguments: the [command signature](#defining-input-expectations) and a closure which receives the command's arguments and options: -->
`routes/console.php` 파일은 HTTP 라우트를 정의하지는 않지만, 애플리케이션으로 진입하는 콘솔 기반 진입점(라우트)을 정의합니다. 이 파일 안에서 `Artisan::command` 메서드를 사용하여 모든 클로저 기반 콘솔 명령어를 정의할 수 있습니다. `command` 메서드는 두 개의 인수를 받습니다. [command signature](#defining-input-expectations)와 명령어의 인수 및 옵션을 받는 클로저입니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

<!-- The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class. -->
클로저는 내부 명령어 인스턴스에 바인딩되므로, 일반적인 전체 명령어 클래스에서 접근할 수 있는 모든 헬퍼 메서드에 그대로 접근할 수 있습니다.

<a name="type-hinting-dependencies"></a>
<!-- #### Type-Hinting Dependencies -->
#### Type-Hinting Dependencies

<!-- In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/13.x/container): -->
명령어의 인수와 옵션을 받는 것 외에도, 명령어 클로저는 [service container](/docs/13.x/container)에서 해결하고 싶은 추가 의존성을 타입 힌트할 수 있습니다.

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
<!-- #### Closure Command Descriptions -->
#### Closure Command Descriptions

<!-- When defining a closure-based command, you may use the `purpose` method to add a description to the command. This description will be displayed when you run the `php artisan list` or `php artisan help` commands: -->
클로저 기반 명령어를 정의할 때 `purpose` 메서드를 사용하여 명령어에 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령어를 실행할 때 표시됩니다.

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
<!-- ### Isolatable Commands -->
### Isolatable Commands

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 캐시 드라이버 중 하나를 사용해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<!-- Sometimes you may wish to ensure that only one instance of a command can run at a time. To accomplish this, you may implement the `Illuminate\Contracts\Console\Isolatable` interface on your command class: -->
때로는 명령어 인스턴스가 한 번에 하나만 실행되도록 보장하고 싶을 수 있습니다. 이를 위해 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현할 수 있습니다.

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

<!-- When you mark a command as `Isolatable`, Laravel automatically makes the `--isolated` option available for the command without needing to explicitly define it in the command's options. When the command is invoked with that option, Laravel will ensure that no other instances of that command are already running. Laravel accomplishes this by attempting to acquire an atomic lock using your application's default cache driver. If other instances of the command are running, the command will not execute; however, the command will still exit with a successful exit status code: -->
명령어를 `Isolatable`로 표시하면 Laravel은 명령어의 옵션에 명시적으로 정의하지 않아도 해당 명령어에서 `--isolated` 옵션을 자동으로 사용할 수 있게 합니다. 이 옵션과 함께 명령어를 호출하면 Laravel은 같은 명령어의 다른 인스턴스가 이미 실행 중이지 않은지 확인합니다. Laravel은 애플리케이션의 기본 캐시 드라이버를 사용해 원자적 잠금을 획득하려고 시도하여 이를 수행합니다. 명령어의 다른 인스턴스가 실행 중이라면 명령어는 실행되지 않습니다. 하지만 명령어는 여전히 성공 종료 상태 코드로 종료됩니다.

```shell
php artisan mail:send 1 --isolated
```

<!-- If you would like to specify the exit status code that the command should return if it is not able to execute, you may provide the desired status code via the `isolated` option: -->
명령어를 실행할 수 없을 때 반환할 종료 상태 코드를 지정하려면 `isolated` 옵션을 통해 원하는 상태 코드를 제공할 수 있습니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
<!-- #### Lock ID -->
#### Lock ID

<!-- By default, Laravel will use the command's name to generate the string key that is used to acquire the atomic lock in your application's cache. However, you may customize this key by defining an `isolatableId` method on your Artisan command class, allowing you to integrate the command's arguments or options into the key: -->
기본적으로 Laravel은 애플리케이션 캐시에서 원자적 잠금을 획득하는 데 사용할 문자열 키를 생성하기 위해 명령어 이름을 사용합니다. 하지만 Artisan 명령어 클래스에 `isolatableId` 메서드를 정의하여 이 키를 커스터마이징할 수 있으며, 이를 통해 명령어의 인수나 옵션을 키에 포함할 수 있습니다.

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
<!-- #### Lock Expiration Time -->
#### Lock Expiration Time

<!-- By default, isolation locks expire after the command is finished. Or, if the command is interrupted and unable to finish, the lock will expire after one hour. However, you may adjust the lock expiration time by defining an `isolationLockExpiresAt` method on your command: -->
기본적으로 격리 잠금은 명령어가 완료된 후 만료됩니다. 또는 명령어가 중단되어 완료되지 못한 경우 잠금은 한 시간 후에 만료됩니다. 하지만 명령어에 `isolationLockExpiresAt` 메서드를 정의하여 잠금 만료 시간을 조정할 수 있습니다.

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
<!-- ## Defining Input Expectations -->
## Defining Input Expectations

<!-- When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax. -->
콘솔 명령어를 작성할 때는 인수나 옵션을 통해 사용자로부터 입력을 수집하는 일이 흔합니다. Laravel은 명령어의 `signature` 속성을 사용하여 사용자에게 기대하는 입력을 매우 편리하게 정의할 수 있게 해 줍니다. `signature` 속성을 사용하면 명령어의 이름, 인수, 옵션을 하나의 표현력 있는 라우트와 비슷한 문법으로 정의할 수 있습니다.

<a name="arguments"></a>
<!-- ### Arguments -->
### Arguments

<!-- All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`: -->
사용자가 제공하는 모든 인수와 옵션은 중괄호로 감쌉니다. 다음 예제에서 명령어는 하나의 필수 인수인 `user`를 정의합니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

<!-- You may also make arguments optional or define default values for arguments: -->
인수를 선택 사항으로 만들거나 인수의 기본값을 정의할 수도 있습니다.

```php
// Optional argument...
'mail:send {user?}'

// Optional argument with default value...
'mail:send {user=foo}'
```

<a name="options"></a>
<!-- ### Options -->
### Options

<!-- Options, like arguments, are another form of user input. Options are prefixed by two hyphens (`--`) when they are provided via the command line. There are two types of options: those that receive a value and those that don't. Options that don't receive a value serve as a boolean "switch". Let's take a look at an example of this type of option: -->
옵션은 인수와 마찬가지로 사용자 입력의 또 다른 형태입니다. 명령줄을 통해 옵션을 제공할 때는 두 개의 하이픈(`--`)을 접두사로 붙입니다. 옵션에는 값을 받는 옵션과 값을 받지 않는 옵션, 두 가지 유형이 있습니다. 값을 받지 않는 옵션은 불리언 "스위치" 역할을 합니다. 이 유형의 옵션 예제를 살펴보겠습니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

<!-- In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`: -->
이 예제에서 Artisan 명령어를 호출할 때 `--queue` 스위치를 지정할 수 있습니다. `--queue` 스위치가 전달되면 옵션 값은 `true`가 됩니다. 그렇지 않으면 값은 `false`가 됩니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
<!-- #### Options With Values -->
#### Options With Values

<!-- Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign: -->
다음으로 값을 기대하는 옵션을 살펴보겠습니다. 사용자가 옵션에 값을 반드시 지정해야 한다면 옵션 이름 뒤에 `=` 기호를 붙여야 합니다.

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

<!-- In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`: -->
이 예제에서 사용자는 다음과 같이 옵션 값을 전달할 수 있습니다. 명령어를 호출할 때 옵션을 지정하지 않으면 해당 값은 `null`이 됩니다.

```shell
php artisan mail:send 1 --queue=default
```

<!-- You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used: -->
옵션 이름 뒤에 기본값을 지정하여 옵션에 기본값을 할당할 수 있습니다. 사용자가 옵션 값을 전달하지 않으면 기본값이 사용됩니다.

```php
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
<!-- #### Option Shortcuts -->
#### Option Shortcuts

<!-- To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name: -->
옵션을 정의할 때 단축키를 할당하려면 옵션 이름 앞에 단축키를 지정하고, `|` 문자를 구분자로 사용하여 단축키와 전체 옵션 이름을 구분할 수 있습니다.

```php
'mail:send {user} {--Q|queue=}'
```

<!-- When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen and no `=` character should be included when specifying a value for the option: -->
터미널에서 명령어를 호출할 때 옵션 단축키에는 하나의 하이픈을 접두사로 붙여야 하며, 옵션 값을 지정할 때 `=` 문자는 포함하지 않아야 합니다.

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
<!-- ### Input Arrays -->
### Input Arrays

<!-- If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument: -->
여러 입력 값을 기대하는 인수나 옵션을 정의하려면 `*` 문자를 사용할 수 있습니다. 먼저 이러한 인수를 지정하는 예제를 살펴보겠습니다.

```php
'mail:send {user*}'
```

<!-- When running this command, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `1` and `2` as its values: -->
이 명령어를 실행할 때 `user` 인수는 명령줄에 순서대로 전달할 수 있습니다. 예를 들어 다음 명령어는 `user` 값을 `1`과 `2`를 값으로 가지는 배열로 설정합니다.

```shell
php artisan mail:send 1 2
```

<!-- This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument: -->
이 `*` 문자는 선택적 인수 정의와 결합하여 인수가 0개 이상 올 수 있도록 허용할 수 있습니다.

```php
'mail:send {user?*}'
```

<a name="option-arrays"></a>
<!-- #### Option Arrays -->
#### Option Arrays

<!-- When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name: -->
여러 입력 값을 기대하는 옵션을 정의할 때는 명령어에 전달되는 각 옵션 값 앞에 옵션 이름을 붙여야 합니다.

```php
'mail:send {--id=*}'
```
<!-- Such a command may be invoked by passing multiple `--id` arguments: -->
이러한 명령어는 여러 개의 `--id` 인수를 전달하여 호출할 수 있습니다.

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
<!-- ### Input Descriptions -->
### Input Descriptions

<!-- You may assign descriptions to input arguments and options by separating the argument name from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines: -->
입력 인수와 옵션에는 인수 이름과 설명을 콜론으로 구분하여 설명을 지정할 수 있습니다. 명령어를 정의할 공간이 조금 더 필요하다면, 정의를 여러 줄로 나누어 작성해도 됩니다.

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
<!-- ### Prompting for Missing Input -->
### Prompting for Missing Input

<!-- If your command contains required arguments, the user will receive an error message when they are not provided. Alternatively, you may configure your command to automatically prompt the user when required arguments are missing by implementing the `PromptsForMissingInput` interface: -->
명령어에 필수 인수가 포함되어 있는데 사용자가 이를 제공하지 않으면 오류 메시지가 표시됩니다. 또는 `PromptsForMissingInput` 인터페이스를 구현하여 필수 인수가 누락되었을 때 명령어가 사용자에게 자동으로 입력을 요청하도록 설정할 수 있습니다.

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

<!-- If Laravel needs to gather a required argument from the user, it will automatically ask the user for the argument by intelligently phrasing the question using either the argument name or description. If you wish to customize the question used to gather the required argument, you may implement the `promptForMissingArgumentsUsing` method, returning an array of questions keyed by the argument names: -->
Laravel이 사용자로부터 필수 인수를 받아야 하는 경우, 인수 이름이나 설명을 활용해 질문 문장을 적절히 만들어 사용자에게 자동으로 해당 인수를 묻습니다. 필수 인수를 받기 위해 사용할 질문을 직접 지정하고 싶다면 `promptForMissingArgumentsUsing` 메서드를 구현하면 됩니다. 이 메서드는 인수 이름을 키로 하는 질문 배열을 반환해야 합니다.

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

<!-- You may also provide placeholder text by using a tuple containing the question and placeholder: -->
질문과 플레이스홀더를 포함하는 튜플을 사용하여 플레이스홀더 텍스트도 제공할 수 있습니다.

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

<!-- If you would like complete control over the prompt, you may provide a closure that should prompt the user and return their answer: -->
프롬프트를 완전히 직접 제어하고 싶다면, 사용자에게 입력을 요청하고 그 답변을 반환하는 클로저를 제공할 수 있습니다.

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
<!-- The comprehensive [Laravel Prompts](/docs/13.x/prompts) documentation includes additional information on the available prompts and their usage. -->
포괄적인 [Laravel Prompts](/docs/13.x/prompts) 문서에는 사용할 수 있는 프롬프트와 사용법에 대한 추가 정보가 포함되어 있습니다.

<!-- If you wish to prompt the user to select or enter [options](#options), you may include prompts in your command's `handle` method. However, if you only wish to prompt the user when they have also been automatically prompted for missing arguments, then you may implement the `afterPromptingForMissingArguments` method: -->
사용자가 [options](#options)를 선택하거나 입력하도록 요청하고 싶다면, 명령어의 `handle` 메서드 안에 프롬프트를 포함할 수 있습니다. 하지만 누락된 인수에 대해 자동으로 프롬프트가 표시된 경우에만 사용자에게 추가로 묻고 싶다면 `afterPromptingForMissingArguments` 메서드를 구현할 수 있습니다.

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
<!-- ## Command I/O -->
## Command I/O

<a name="retrieving-input"></a>
<!-- ### Retrieving Input -->
### Retrieving Input

<!-- While your command is executing, you will likely need to access the values for the arguments and options accepted by your command. To do so, you may use the `argument` and `option` methods. If an argument or option does not exist, `null` will be returned: -->
명령어가 실행되는 동안에는 명령어가 받는 인수와 옵션의 값에 접근해야 할 때가 많습니다. 이를 위해 `argument`와 `option` 메서드를 사용할 수 있습니다. 인수나 옵션이 존재하지 않으면 `null`이 반환됩니다.

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

<!-- If you need to retrieve all of the arguments as an `array`, call the `arguments` method: -->
모든 인수를 `array`로 가져와야 한다면 `arguments` 메서드를 호출하세요.

```php
$arguments = $this->arguments();
```

<!-- Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method: -->
옵션도 인수와 마찬가지로 `option` 메서드를 사용해 쉽게 가져올 수 있습니다. 모든 옵션을 배열로 가져오려면 `options` 메서드를 호출하세요.

```php
// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
```

<a name="prompting-for-input"></a>
<!-- ### Prompting for Input -->
### Prompting for Input

> [!NOTE]
> [Laravel Prompts](/docs/13.x/prompts)는 명령줄 애플리케이션에 아름답고 사용하기 쉬운 폼을 추가하기 위한 PHP 패키지입니다. 플레이스홀더 텍스트와 유효성 검증을 포함한 브라우저와 비슷한 기능을 제공합니다.

<!-- In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command: -->
출력을 표시하는 것뿐만 아니라, 명령어 실행 중에 사용자에게 입력을 요청할 수도 있습니다. `ask` 메서드는 주어진 질문을 사용자에게 표시하고, 사용자의 입력을 받은 뒤, 그 입력을 명령어로 반환합니다.

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

<!-- The `ask` method also accepts an optional second argument which specifies the default value that should be returned if no user input is provided: -->
`ask` 메서드는 선택적으로 두 번째 인수를 받을 수도 있습니다. 이 인수는 사용자가 아무 입력도 하지 않았을 때 반환할 기본값을 지정합니다.

```php
$name = $this->ask('What is your name?', 'Taylor');
```

<!-- The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as passwords: -->
`secret` 메서드는 `ask`와 비슷하지만, 사용자가 콘솔에 입력하는 동안 입력값이 화면에 보이지 않습니다. 이 메서드는 비밀번호처럼 민감한 정보를 요청할 때 유용합니다.

```php
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
<!-- #### Asking for Confirmation -->
#### Asking for Confirmation

<!-- If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`. -->
사용자에게 간단한 "예 또는 아니오" 확인을 요청해야 한다면 `confirm` 메서드를 사용할 수 있습니다. 기본적으로 이 메서드는 `false`를 반환합니다. 하지만 사용자가 프롬프트에 대한 응답으로 `y` 또는 `yes`를 입력하면 `true`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

<!-- If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method: -->
필요하다면 `confirm` 메서드의 두 번째 인수로 `true`를 전달하여 확인 프롬프트의 기본 반환값이 `true`가 되도록 지정할 수 있습니다.

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
<!-- #### Auto-Completion -->
#### Auto-Completion

<!-- The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`anticipate` 메서드는 가능한 선택지에 대한 자동 완성을 제공하는 데 사용할 수 있습니다. 사용자는 자동 완성 힌트와 관계없이 어떤 답변이든 입력할 수 있습니다.

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion: -->
또는 `anticipate` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 이 클로저는 사용자가 입력 문자를 하나씩 입력할 때마다 호출됩니다. 클로저는 지금까지의 사용자 입력을 담은 문자열 파라미터를 받아야 하며, 자동 완성 옵션 배열을 반환해야 합니다.

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
<!-- #### Multiple Choice Questions -->
#### Multiple Choice Questions

<!-- If you need to give the user a predefined set of choices when asking a question, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen by passing the index as the third argument to the method: -->
질문을 할 때 사용자에게 미리 정의된 선택지 목록을 제공해야 한다면 `choice` 메서드를 사용할 수 있습니다. 사용자가 아무 옵션도 선택하지 않았을 때 반환할 기본값은 해당 배열 인덱스를 메서드의 세 번째 인수로 전달하여 설정할 수 있습니다.

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

<!-- In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted: -->
또한 `choice` 메서드는 올바른 응답을 선택할 수 있는 최대 시도 횟수와 여러 선택을 허용할지 여부를 결정하기 위해 선택적인 네 번째와 다섯 번째 인수를 받습니다.

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
<!-- ### Writing Output -->
### Writing Output

<!-- To send output to the console, you may use the `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, and `error` methods. Each of these methods will use appropriate ANSI colors for their purpose. For example, let's display some general information to the user. Typically, the `info` method will display in the console as green colored text: -->
콘솔로 출력을 보내려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert`, `error` 메서드를 사용할 수 있습니다. 각 메서드는 목적에 맞는 ANSI 색상을 사용합니다. 예를 들어 사용자에게 일반적인 정보를 표시해 보겠습니다. 일반적으로 `info` 메서드는 콘솔에 초록색 텍스트로 표시됩니다.

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

<!-- To display an error message, use the `error` method. Error message text is typically displayed in red: -->
오류 메시지를 표시하려면 `error` 메서드를 사용하세요. 오류 메시지 텍스트는 일반적으로 빨간색으로 표시됩니다.

```php
$this->error('Something went wrong!');
```

<!-- You may use the `line` method to display plain, uncolored text: -->
`line` 메서드를 사용하면 색상이 없는 일반 텍스트를 표시할 수 있습니다.

```php
$this->line('Display this on the screen');
```

<!-- You may use the `newLine` method to display a blank line: -->
`newLine` 메서드를 사용하면 빈 줄을 표시할 수 있습니다.

```php
// Write a single blank line...
$this->newLine();

// Write three blank lines...
$this->newLine(3);
```

<a name="tables"></a>
<!-- #### Tables -->
#### Tables

<!-- The `table` method makes it easy to correctly format multiple rows / columns of data. All you need to do is provide the column names and the data for the table and Laravel will automatically calculate the appropriate width and height of the table for you: -->
`table` 메서드를 사용하면 여러 행 / 컬럼의 데이터를 올바른 형식으로 쉽게 출력할 수 있습니다. 컬럼 이름과 테이블 데이터를 제공하기만 하면 Laravel이 적절한 테이블 너비와 높이를 자동으로 계산해 줍니다.

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```

<a name="progress-bars"></a>
<!-- #### Progress Bars -->
#### Progress Bars

<!-- For long running tasks, it can be helpful to show a progress bar that informs users how complete the task is. Using the `withProgressBar` method, Laravel will display a progress bar and advance its progress for each iteration over a given iterable value: -->
오래 실행되는 작업에서는 작업이 얼마나 완료되었는지 사용자에게 알려 주는 진행률 표시줄을 보여 주면 도움이 됩니다. `withProgressBar` 메서드를 사용하면 Laravel이 진행률 표시줄을 표시하고, 주어진 반복 가능한 값의 각 반복마다 진행률을 앞으로 이동시킵니다.

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item: -->
때로는 진행률 표시줄이 어떻게 진행될지 더 직접적으로 제어해야 할 수 있습니다. 먼저 프로세스가 반복할 전체 단계 수를 정의합니다. 그런 다음 각 항목을 처리한 뒤 진행률 표시줄을 앞으로 이동시킵니다.

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
> 더 고급 옵션은 [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html)을 확인하세요.

<a name="registering-commands"></a>
<!-- ## Registering Commands -->
## Registering Commands

<!-- By default, Laravel automatically registers all commands within the `app/Console/Commands` directory. However, you can instruct Laravel to scan other directories for Artisan commands using the `withCommands` method in your application's `bootstrap/app.php` file: -->
기본적으로 Laravel은 `app/Console/Commands` 디렉터리 안의 모든 명령어를 자동으로 등록합니다. 하지만 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용하여 Laravel이 Artisan 명령어를 찾을 다른 디렉터리를 스캔하도록 지시할 수 있습니다.

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

<!-- If necessary, you may also manually register commands by providing the command's class name to the `withCommands` method: -->
필요하다면 명령어의 클래스 이름을 `withCommands` 메서드에 제공하여 명령어를 직접 등록할 수도 있습니다.

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

<!-- When Artisan boots, all the commands in your application will be resolved by the [service container](/docs/13.x/container) and registered with Artisan. -->
Artisan이 부팅될 때, 애플리케이션의 모든 명령어는 [service container](/docs/13.x/container)를 통해 해석되고 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
<!-- ## Programmatically Executing Commands -->
## Programmatically Executing Commands

<!-- Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned: -->
때로는 CLI 외부에서 Artisan 명령어를 실행하고 싶을 수 있습니다. 예를 들어 라우트나 컨트롤러에서 Artisan 명령어를 실행하고 싶을 수 있습니다. 이를 위해 `Artisan` 파사드의 `call` 메서드를 사용할 수 있습니다. `call` 메서드는 첫 번째 인수로 명령어의 시그니처 이름이나 클래스 이름을 받고, 두 번째 인수로 명령어 파라미터 배열을 받습니다. 종료 코드가 반환됩니다.

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

<!-- Alternatively, you may pass the entire Artisan command to the `call` method as a string: -->
또는 전체 Artisan 명령어를 문자열로 `call` 메서드에 전달할 수도 있습니다.

```php
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
<!-- #### Passing Array Values -->
#### Passing Array Values

<!-- If your command defines an option that accepts an array, you may pass an array of values to that option: -->
명령어가 배열을 받는 옵션을 정의한다면, 해당 옵션에 값 배열을 전달할 수 있습니다.

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
<!-- #### Passing Boolean Values -->
#### Passing Boolean Values
<!-- If you need to specify the value of an option that does not accept string values, such as the `--force` flag on the `migrate:refresh` command, you should pass `true` or `false` as the value of the option: -->
문자열 값을 받지 않는 옵션의 값을 지정해야 하는 경우가 있습니다. 예를 들어 `migrate:refresh` 명령어의 `--force` 플래그가 그렇습니다. 이 경우 옵션 값으로 `true` 또는 `false`를 전달해야 합니다.

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
<!-- #### Queueing Artisan Commands -->
#### Queueing Artisan Commands

<!-- Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/13.x/queues). Before using this method, make sure you have configured your queue and are running a queue listener: -->
`Artisan` facade의 `queue` 메서드를 사용하면 Artisan 명령어를 큐에 넣어 [queue workers](/docs/13.x/queues)가 백그라운드에서 처리하도록 할 수도 있습니다. 이 메서드를 사용하기 전에 큐를 설정하고 큐 리스너를 실행 중인지 확인하세요.

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

<!-- Using the `onConnection` and `onQueue` methods, you may specify the connection or queue the Artisan command should be dispatched to: -->
`onConnection` 및 `onQueue` 메서드를 사용하면 Artisan 명령어를 디스패치할 연결 또는 큐를 지정할 수 있습니다.

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
<!-- ### Calling Commands From Other Commands -->
### Calling Commands From Other Commands

<!-- Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options: -->
기존 Artisan 명령어 안에서 다른 명령어를 호출하고 싶을 때가 있습니다. 이 작업은 `call` 메서드를 사용하여 수행할 수 있습니다. 이 `call` 메서드는 명령어 이름과 명령어 인수 / 옵션 배열을 받습니다.

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

<!-- If you would like to call another console command and suppress all of its output, you may use the `callSilently` method. The `callSilently` method has the same signature as the `call` method: -->
다른 콘솔 명령어를 호출하면서 모든 출력을 표시하지 않으려면 `callSilently` 메서드를 사용할 수 있습니다. `callSilently` 메서드는 `call` 메서드와 동일한 시그니처를 가집니다.

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
<!-- ## Signal Handling -->
## Signal Handling

<!-- As you may know, operating systems allow signals to be sent to running processes. For example, the `SIGTERM` signal is how operating systems ask a program to terminate gracefully. If you wish to listen for signals in your Artisan console commands and execute code when they occur, you may use the `trap` method: -->
아시다시피 운영 체제는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어 `SIGTERM` 시그널은 운영 체제가 프로그램에 정상 종료를 요청하는 방식입니다. Artisan 콘솔 명령어에서 시그널을 감지하고 시그널이 발생했을 때 코드를 실행하고 싶다면 `trap` 메서드를 사용할 수 있습니다.

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

<!-- To listen for multiple signals at once, you may provide an array of signals to the `trap` method: -->
여러 시그널을 한 번에 감지하려면 `trap` 메서드에 시그널 배열을 전달하면 됩니다.

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
<!-- ## Stub Customization -->
## Stub Customization

<!-- The Artisan console's `make` commands are used to create a variety of classes, such as controllers, jobs, migrations, and tests. These classes are generated using "stub" files that are populated with values based on your input. However, you may want to make small changes to files generated by Artisan. To accomplish this, you may use the `stub:publish` command to publish the most common stubs to your application so that you can customize them: -->
Artisan 콘솔의 `make` 명령어는 컨트롤러, job, migration, 테스트 등 다양한 클래스를 생성하는 데 사용됩니다. 이러한 클래스는 입력값을 기반으로 채워지는 "stub" 파일을 사용해 생성됩니다. 하지만 Artisan이 생성하는 파일을 조금 수정하고 싶을 수 있습니다. 이를 위해 `stub:publish` 명령어를 사용하여 가장 자주 사용되는 stub을 애플리케이션에 게시하고 직접 커스터마이징할 수 있습니다.

```shell
php artisan stub:publish
```

<!-- The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands. -->
게시된 stub은 애플리케이션 루트의 `stubs` 디렉터리에 위치합니다. 이 stub에 변경한 내용은 Artisan의 `make` 명령어를 사용하여 해당 클래스를 생성할 때 반영됩니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing. -->
Artisan은 명령어를 실행할 때 세 가지 이벤트를 디스패치합니다. `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`입니다. `ArtisanStarting` 이벤트는 Artisan이 실행되기 시작하는 즉시 디스패치됩니다. 다음으로 `CommandStarting` 이벤트는 명령어가 실행되기 직전에 디스패치됩니다. 마지막으로 `CommandFinished` 이벤트는 명령어 실행이 완료되면 디스패치됩니다.
