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
아티즌(Artisan)은 Laravel에 기본 포함된 명령줄 인터페이스입니다. 아티즌은 애플리케이션 최상위 디렉터리에 `artisan` 스크립트로 위치하며, 개발 중에 유용한 다양한 명령어를 제공합니다. 사용 가능한 모든 아티즌 명령어를 보려면 `list` 명령어를 실행하면 됩니다.

```shell
php artisan list
```

<!-- Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`: -->
각 명령어에는 해당 명령어의 인수와 옵션을 보여주고 설명하는 "도움말" 화면이 포함되어 있습니다. 도움말을 보려면 명령어 이름 앞에 `help`를 붙여 실행하세요.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
<!-- #### Laravel Sail -->
#### Laravel Sail

<!-- If you are using [Laravel Sail](/docs/10.x/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers: -->
로컬 개발 환경으로 [Laravel Sail](/docs/10.x/sail)을 사용한다면, 아티즌 명령어를 실행할 때 `sail` 커맨드 라인을 활용해야 합니다. Sail은 애플리케이션의 Docker 컨테이너 내부에서 아티즌 명령어를 실행해줍니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
<!-- ### Tinker (REPL) -->
### Tinker (REPL)

<!-- Laravel Tinker is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package. -->
Laravel Tinker는 Laravel 프레임워크를 위한 강력한 REPL을 제공합니다. 이 기능은 [PsySH](https://github.com/bobthecow/psysh) 패키지로 구동됩니다.

<a name="installation"></a>
<!-- #### Installation -->
#### Installation

<!-- All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application: -->
모든 Laravel 애플리케이션에는 Tinker가 기본적으로 포함되어 있습니다. 만약 애플리케이션에서 Tinker를 제거했다면, Composer로 다시 설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션을 사용하면서 핫 리로딩, 여러 줄 코드 편집, 자동 완성 기능이 필요하다면 [Tinkerwell](https://tinkerwell.app)을 참고하세요!

<a name="usage"></a>
<!-- #### Usage -->
#### Usage

<!-- Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command: -->
Tinker를 이용하면 Eloquent 모델, 작업(jobs), 이벤트 등 전체 Laravel 애플리케이션을 커맨드라인에서 직접 다룰 수 있습니다. Tinker 환경에 진입하려면 `tinker` 아티즌 명령어를 실행하세요.

```shell
php artisan tinker
```

<!-- You can publish Tinker's configuration file using the `vendor:publish` command: -->
또한 `vendor:publish` 명령어로 Tinker의 설정 파일을 공개(publish)할 수 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수 및 `Dispatchable` 클래스의 `dispatch` 메서드는 가비지 컬렉션에 의존해 작업을 큐에 올립니다. 따라서 tinker 사용 시에는 `Bus::dispatch`나 `Queue::push`를 활용해 작업을 큐로 전달해야 합니다.

<a name="command-allow-list"></a>
<!-- #### Command Allow List -->
#### Command Allow List

<!-- Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, and `up` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file: -->
Tinker는 "허용(allow)" 목록을 사용해, 쉘에서 실행할 수 있는 아티즌 명령어를 결정합니다. 기본적으로는 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 명령어만 실행할 수 있습니다. 더 많은 명령어를 허용하고 싶다면, `tinker.php` 설정 파일의 `commands` 배열에 추가하면 됩니다.

```
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
<!-- #### Classes That Should Not Be Aliased -->
#### Classes That Should Not Be Aliased

<!-- Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file: -->
보통 Tinker는 상호작용 시점에 클래스를 자동으로 별칭(alias) 처리합니다. 하지만 절대로 별칭을 만들고 싶지 않은 클래스가 있다면, `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 지정하면 됩니다.

```
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
<!-- ## Writing Commands -->
## Writing Commands

<!-- In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as your commands can be loaded by Composer. -->
아티즌이 기본 제공하는 명령어 외에도, 직접 커스텀 명령어를 만들 수 있습니다. 명령어 클래스는 보통 `app/Console/Commands` 디렉터리에 저장되지만, Composer가 로드 가능한 위치라면 자유롭게 저장 경로를 지정해도 됩니다.

<a name="generating-commands"></a>
<!-- ### Generating Commands -->
### Generating Commands

<!-- To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command: -->
새 명령어를 생성하려면, `make:command` 아티즌 명령어를 사용하세요. 이 명령어는 `app/Console/Commands` 디렉터리에 새 명령어 클래스를 만들어줍니다. 만약 이 디렉터리가 없더라도, `make:command` 아티즌 명령어를 최초로 실행할 때 자동으로 생성됩니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
<!-- ### Command Structure -->
### Command Structure

<!-- After generating your command, you should define appropriate values for the `signature` and `description` properties of the class. These properties will be used when displaying your command on the `list` screen. The `signature` property also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method. -->
명령어를 생성했다면, 클래스의 `signature`와 `description` 속성(property)에 알맞은 값을 지정해야 합니다. 이 속성 값들은 `list` 화면에 명령어를 표시할 때 사용됩니다. 또한, `signature` 속성에서는 [your command's input expectations](#defining-input-expectations)도 정의할 수 있습니다. 명령어가 실행되면 `handle` 메서드가 호출되므로, 이 안에 명령어의 주요 로직을 작성하면 됩니다.

<!-- Let's take a look at an example command. Note that we are able to request any dependencies we need via the command's `handle` method. The Laravel [service container](/docs/10.x/container) will automatically inject all dependencies that are type-hinted in this method's signature: -->
예시 명령어를 살펴보겠습니다. 여기서는 의존성이 필요한 경우 `handle` 메서드의 파라미터로 자유롭게 의존성 주입(Dependency Injection)이 가능함을 보여주고 있습니다. Laravel [service container](/docs/10.x/container)는 타입 힌트가 지정된 모든 의존성을 자동으로 주입해줍니다.

```
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
> 코드의 재사용성을 높이려면, 콘솔 명령어 클래스 자체는 가볍게 유지하고 실제 작업은 애플리케이션 서비스로 위임하는 것이 좋습니다. 위의 예시처럼 "이메일 발송"과 같은 주요 로직을 서비스 클래스로 분리하는 방식을 권장합니다.

<a name="closure-commands"></a>
<!-- ### Closure Commands -->
### Closure Commands

<!-- Closure based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. Within the `commands` method of your `app/Console/Kernel.php` file, Laravel loads the `routes/console.php` file: -->
클로저(Closure) 기반 명령어는 클래스 대신 클로저 형태로 콘솔 명령어를 정의하는 또 다른 방법입니다. 마치 라우트 클로저(route closure)가 컨트롤러를 대체하는 것과 비슷하게, 명령어 클로저는 명령어 클래스를 대체할 수 있습니다. `app/Console/Kernel.php` 파일의 `commands` 메서드 안에서 Laravel은 `routes/console.php` 파일을 불러들입니다.

```
/**
 * Register the closure based commands for the application.
 */
protected function commands(): void
{
    require base_path('routes/console.php');
}
```

<!-- Even though this file does not define HTTP routes, it defines console based entry points (routes) into your application. Within this file, you may define all of your closure based console commands using the `Artisan::command` method. The `command` method accepts two arguments: the [command signature](#defining-input-expectations) and a closure which receives the command's arguments and options: -->
이 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션에 콘솔 진입점(명령어 루트)을 정의합니다. 이 안에서 `Artisan::command` 메서드를 사용해 클로저 기반 콘솔 명령어를 등록할 수 있습니다. `command` 메서드는 [command signature](#defining-input-expectations)와 명령어의 인수, 옵션을 받는 클로저를 전달받습니다.

```
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

<!-- The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class. -->
이 클로저는 내부적으로 실제 명령어 인스턴스에 바인딩 되므로, 일반 명령어 클래스에서 사용할 수 있는 모든 헬퍼 메서드에도 접근할 수 있습니다.

<a name="type-hinting-dependencies"></a>
<!-- #### Type-Hinting Dependencies -->
#### Type-Hinting Dependencies

<!-- In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/10.x/container): -->
명령어의 인수와 옵션 외에도, 클로저 명령어에서는 [service container](/docs/10.x/container)에서 해결 가능한 추가 의존성도 타입 힌트로 주입받을 수 있습니다.

```
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
<!-- #### Closure Command Descriptions -->
#### Closure Command Descriptions

<!-- When defining a closure based command, you may use the `purpose` method to add a description to the command. This description will be displayed when you run the `php artisan list` or `php artisan help` commands: -->
클로저 기반 명령어를 정의할 때, `purpose` 메서드를 이용해 명령어에 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 실행 시 표시됩니다.

```
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
<!-- ### Isolatable Commands -->
### Isolatable Commands

> [!WARNING]
> 이 기능을 사용하려면 애플리케이션의 기본 캐시 드라이버가 `memcached`, `redis`, `dynamodb`, `database`, `file`, `array` 중 하나여야 합니다. 또한 모든 서버가 같은 중앙 캐시 서버에 연결되어 있어야 합니다.

<!-- Sometimes you may wish to ensure that only one instance of a command can run at a time. To accomplish this, you may implement the `Illuminate\Contracts\Console\Isolatable` interface on your command class: -->
어떤 경우에는 특정 명령어의 인스턴스가 한 번에 하나만 실행되도록 제한하고 싶을 수 있습니다. 이를 위해, 명령어 클래스에서 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다.

```
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```

<!-- When a command is marked as `Isolatable`, Laravel will automatically add an `--isolated` option to the command. When the command is invoked with that option, Laravel will ensure that no other instances of that command are already running. Laravel accomplishes this by attempting to acquire an atomic lock using your application's default cache driver. If other instances of the command are running, the command will not execute; however, the command will still exit with a successful exit status code: -->
명령어가 `Isolatable`로 표시되면 Laravel은 자동으로 명령어에 `--isolated` 옵션을 추가합니다. 이 옵션과 함께 명령어를 실행하면, 동일 명령어의 다른 인스턴스가 실행 중이지 않은지 확인한 후 실행합니다. 이를 위해 애플리케이션의 기본 캐시 드라이버로 원자적 잠금(atomic lock)을 시도합니다. 만약 다른 명령어 인스턴스가 이미 실행 중이라면, 새 명령어는 실행되지 않고 성공(exit code 0) 상태로 종료됩니다.

```shell
php artisan mail:send 1 --isolated
```

<!-- If you would like to specify the exit status code that the command should return if it is not able to execute, you may provide the desired status code via the `isolated` option: -->
명령어 실행이 불가능할 경우 반환할 종료 코드를 지정하고 싶다면, `isolated` 옵션에 원하는 상태 코드를 전달하면 됩니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
<!-- #### Lock ID -->
#### Lock ID

<!-- By default, Laravel will use the command's name to generate the string key that is used to acquire the atomic lock in your application's cache. However, you may customize this key by defining an `isolatableId` method on your Artisan command class, allowing you to integrate the command's arguments or options into the key: -->
기본적으로 Laravel은 명령어의 이름을 이용해 캐시에 원자적 잠금에 사용할 문자열 키를 생성합니다. 하지만 명령어 클래스에 `isolatableId` 메서드를 정의해, 인수나 옵션 등을 통합한 커스텀 키를 지정할 수도 있습니다.

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

<!-- By default, isolation locks expire after the command is finished. Or, if the command is interrupted and unable to finish, the lock will expire after one hour. However, you may adjust the lock expiration time by defining a `isolationLockExpiresAt` method on your command: -->
기본적으로는 명령어가 끝나면 isolation lock이 해제됩니다. 또는 명령어가 중단(interrupt)되어 종료에 실패한 경우, 1시간 후에 lock이 만료됩니다. 만료 시간을 커스터마이징 하려면, 명령어 클래스에 `isolationLockExpiresAt` 메서드를 정의하면 됩니다.

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
<!-- ## Defining Input Expectations -->
## Defining Input Expectations

<!-- When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax. -->
콘솔 명령어를 만들 때, 사용자로부터 인수(argument)나 옵션(option) 등 입력값을 받아야 하는 경우가 흔합니다. Laravel에서는 명령어 클래스의 `signature` 속성을 사용해, 사용자에게 기대하는 입력값을 매우 편리하게 정의할 수 있습니다. `signature` 속성을 사용하면 명령어의 이름, 인수, 옵션을 하나의 직관적인 "라우트 문법"으로 표현할 수 있습니다.

<a name="arguments"></a>
<!-- ### Arguments -->
### Arguments

<!-- All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`: -->
사용자가 입력하는 모든 인수와 옵션은 중괄호로 감쌉니다. 아래 예시에서는 `user`라는 필수 인수 하나를 정의합니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

<!-- You may also make arguments optional or define default values for arguments: -->
또한 인수를 선택적으로 만들거나, 기본값도 지정할 수 있습니다.

```
// Optional argument...
'mail:send {user?}'

// Optional argument with default value...
'mail:send {user=foo}'
```

<a name="options"></a>
<!-- ### Options -->
### Options

<!-- Options, like arguments, are another form of user input. Options are prefixed by two hyphens (`--`) when they are provided via the command line. There are two types of options: those that receive a value and those that don't. Options that don't receive a value serve as a boolean "switch". Let's take a look at an example of this type of option: -->
옵션은 인수와 같이 사용자 입력의 또 다른 형태입니다. 명령줄에서는 두 개의 하이픈(`--`)으로 옵션을 구분합니다. 옵션에는 값을 받지 않는(불리언 스위치 역할), 받는 두 가지 타입이 있습니다. 먼저 값이 없는 옵션(불리언 스위치) 예시를 보겠습니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

<!-- In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`: -->
이 예시에서 `--queue` 스위치는 아티즌 명령어를 호출할 때 지정할 수 있습니다. `--queue` 스위치를 전달하면 옵션 값이 `true`가 되고, 전달하지 않으면 `false`가 됩니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
<!-- #### Options With Values -->
#### Options With Values

<!-- Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign: -->
값을 받아야 하는 옵션 예시를 봅시다. 값이 필요하다면 옵션명 뒤에 `=` 기호를 붙입니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

<!-- In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`: -->
이 경우, 아래와 같이 옵션에 값을 전달할 수 있습니다. 옵션이 전달되지 않으면 기본값은 `null`입니다.

```shell
php artisan mail:send 1 --queue=default
```

<!-- You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used: -->
옵션에 기본값을 설정하려면, 옵션명 다음에 해당 값을 지정합니다. 사용자가 옵션값을 입력하지 않으면 기본값이 사용됩니다.

```
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
<!-- #### Option Shortcuts -->
#### Option Shortcuts

<!-- To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name: -->
옵션 정의 시, `|` 기호를 이용해 단축키(shortcut)를 명시할 수 있습니다.

```
'mail:send {user} {--Q|queue}'
```

<!-- When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen and no `=` character should be included when specifying a value for the option: -->
터미널에서 명령어를 실행할 때, 단축키는 한 개의 하이픈과 함께 값에는 `=` 기호를 사용하지 않고 바로 붙입니다.

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
<!-- ### Input Arrays -->
### Input Arrays

<!-- If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument: -->
인수나 옵션에서 복수의 입력값을 받을 필요가 있다면, `*` 문자를 사용합니다. 먼저 인수에 대해 예시를 봅니다.

```
'mail:send {user*}'
```

<!-- When calling this method, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `1` and `2` as its values: -->
이와 같이 설정하면, 명령어 호출 시 `user` 인수를 명령줄에 순서대로 넘길 수 있습니다. 예를 들어 아래 커맨드는 `user` 값을 `1`과 `2`를 원소로 가지는 배열로 설정합니다.

```shell
php artisan mail:send 1 2
```

<!-- This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument: -->
`*` 문자와 선택적 인수(물음표)를 함께 쓰면 0개 이상의 입력값도 허용할 수 있습니다.

```
'mail:send {user?*}'
```

<a name="option-arrays"></a>
<!-- #### Option Arrays -->
#### Option Arrays

<!-- When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name: -->
여러 입력값이 필요한 옵션을 정의할 땐, 각각의 옵션값에 옵션명을 붙여 전달해야 합니다.

```
'mail:send {--id=*}'
```

<!-- Such a command may be invoked by passing multiple `--id` arguments: -->
다음과 같이 여러 개의 `--id` 옵션을 전달할 수 있습니다.

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
<!-- ### Input Descriptions -->
### Input Descriptions

<!-- You may assign descriptions to input arguments and options by separating the argument name from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines: -->
인수나 옵션에 이름과 설명을 콜론으로 구분하여 설명을 붙일 수 있습니다. 명령어 정의가 길어질 경우, 여러 줄로 나누어 작성해도 무방합니다.

```
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
필수 인수가 누락된 경우, 사용자는 에러 메시지를 보게 됩니다. 대신, 명령어에서 `PromptsForMissingInput` 인터페이스를 구현하면, 누락된 필수 인수에 대해 Laravel이 자동으로 프롬프트를 띄워 입력을 요청할 수 있습니다.

```
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
Laravel은 필수 인수 입력이 필요할 때, 인수명 또는 설명을 토대로 적절히 질문(프롬프트)을 만들어 사용자의 입력을 받습니다. 만약 질문 문구를 직접 지정하고 싶다면, `promptForMissingArgumentsUsing` 메서드를 구현해서 인수명을 key로, 질문을 value로 하여 배열을 반환하면 됩니다.

```
/**
 * Prompt for missing input arguments using the returned questions.
 *
 * @return array
 */
protected function promptForMissingArgumentsUsing()
{
    return [
        'user' => 'Which user ID should receive the mail?',
    ];
}
```

<!-- You may also provide placeholder text by using a tuple containing the question and placeholder: -->
질문과 함께 플레이스홀더도 지정하려면, 튜플(배열)로 반환하면 됩니다.

```
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

<!-- If you would like complete control over the prompt, you may provide a closure that should prompt the user and return their answer: -->
프롬프트 전체 로직을 직접 제어하고 싶다면, 사용자의 입력을 받고 반환하는 클로저를 사용할 수도 있습니다.

```
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: 'Search for a user:',
        placeholder: 'E.g. Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```

> [!NOTE]
> <!-- The comprehensive [Laravel Prompts](/docs/10.x/prompts) documentation includes additional information on the available prompts and their usage. -->
> [Laravel Prompts](/docs/10.x/prompts) 공식 문서에서는 지원하는 다양한 프롬프트와 상세 사용 방법을 확인할 수 있습니다.

<!-- If you wish to prompt the user to select or enter [options](#options), you may include prompts in your command's `handle` method. However, if you only wish to prompt the user when they have also been automatically prompted for missing arguments, then you may implement the `afterPromptingForMissingArguments` method: -->
사용자에게 [options](#options)값 입력을 받도록 프롬프트를 실행하고 싶다면, 명령어의 `handle` 메서드에서 프롬프트를 직접 호출할 수 있습니다. 하지만 누락된 인수에 대한 프롬프트가 자동으로 동작할 때만 옵션 프롬프트도 동작시키고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현하면 됩니다.

```
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * Perform actions after the user was prompted for missing arguments.
 *
 * @param  \Symfony\Component\Console\Input\InputInterface  $input
 * @param  \Symfony\Component\Console\Output\OutputInterface  $output
 * @return void
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output)
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
명령어 실행 중, 명령어에서 받은 인수와 옵션값을 조회해야 할 때가 많습니다. 이 경우, `argument` 및 `option` 메서드를 사용하면 됩니다. 만약 해당 인수나 옵션이 없으면 `null`이 반환됩니다.

```
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```

<!-- If you need to retrieve all of the arguments as an `array`, call the `arguments` method: -->
모든 인수를 배열(`array`)로 받으려면 `arguments` 메서드를 이용하세요.

```
$arguments = $this->arguments();
```

<!-- Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method: -->
옵션도 동일하게 `option` 메서드로 조회할 수 있으며, 전체 옵션 값을 배열로 받으려면 `options` 메서드를 사용하면 됩니다.

```
// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
```

<a name="prompting-for-input"></a>
<!-- ### Prompting for Input -->
### Prompting for Input

> [!NOTE]
> [Laravel Prompts](/docs/10.x/prompts)는 브라우저처럼 플레이스홀더 텍스트, 유효성 검사 등을 지원하는, 아름답고 사용자 친화적인 폼 입력을 콘솔 애플리케이션에 제공하는 PHP 패키지입니다.

<!-- In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command: -->
출력만 제공하는 것이 아니라, 명령어 실행 중에 사용자로부터 입력값을 입력받을 수도 있습니다. `ask` 메서드는 지정한 질문을 통해 사용자의 입력을 받아 반환합니다.

```
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
`ask` 메서드는 두 번째 인수로, 사용자가 입력하지 않았을 때 반환할 기본값을 지정할 수 있습니다.

```
$name = $this->ask('What is your name?', 'Taylor');
```

<!-- The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as passwords: -->
`secret` 메서드는 `ask`와 비슷하지만, 입력하는 값이 콘솔 화면에 보이지 않습니다. 비밀번호 등 민감한 값을 묻고 싶을 때 유용합니다.

```
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
<!-- #### Asking for Confirmation -->
#### Asking for Confirmation

<!-- If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`. -->
사용자에게 예/아니오(yes/no)와 같이 단순히 확인하도록 요청하고 싶다면, `confirm` 메서드를 사용할 수 있습니다. 이 메서드는 기본적으로 `false`를 반환합니다. 하지만 사용자가 프롬프트에 `y` 또는 `yes`라고 입력하면 `true`를 반환합니다.

```
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

<!-- If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method: -->
필요하다면 `confirm` 메서드의 두 번째 인수로 `true`를 전달해, 확인 프롬프트가 기본적으로 `true`를 반환하도록 지정할 수도 있습니다.

```
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
<!-- #### Auto-Completion -->
#### Auto-Completion

<!-- The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`anticipate` 메서드를 사용하면 사용자 입력에 따라 선택지 자동 완성을 지원할 수 있습니다. 자동 완성 목록이 표시되지만, 사용자는 그 외 값도 자유롭게 입력할 수 있습니다.

```
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion: -->
또는, `anticipate` 메서드의 두 번째 인수로 클로저를 전달하면 사용자가 입력할 때마다 호출되어 자동 완성 옵션을 동적으로 반환할 수 있습니다.

```
$name = $this->anticipate('What is your address?', function (string $input) {
    // Return auto-completion options...
});
```

<a name="multiple-choice-questions"></a>
<!-- #### Multiple Choice Questions -->
#### Multiple Choice Questions

<!-- If you need to give the user a predefined set of choices when asking a question, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen by passing the index as the third argument to the method: -->
사용자에게 미리 정의된 선택지를 제시하여 질문하고 싶다면, `choice` 메서드를 사용하면 됩니다. 세 번째 인수로 배열에서 기본 선택값의 index를 전달할 수 있습니다(입력하지 않을 경우 반환될 값).

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

<!-- In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted: -->
또한 `choice` 메서드는 유효한 응답을 선택할 수 있는 최대 시도 횟수와 복수 선택 허용 여부를 결정하는 선택적 네 번째, 다섯 번째 인수를 받습니다.

```
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

<!-- To send output to the console, you may use the `line`, `info`, `comment`, `question`, `warn`, and `error` methods. Each of these methods will use appropriate ANSI colors for their purpose. For example, let's display some general information to the user. Typically, the `info` method will display in the console as green colored text: -->
콘솔에 메시지를 출력하려면, `line`, `info`, `comment`, `question`, `warn`, `error` 등의 메서드를 사용할 수 있습니다. 각각의 메서드는 목적에 맞는 ANSI 색상으로 메시지를 표시해줍니다. 예를 들어, 일반 정보를 출력하고 싶다면 `info` 메서드를 사용하세요. (보통 초록색으로 표시됨)

```
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
에러 메시지를 표시하려면 `error` 메서드를 이용하세요. 빨간색 텍스트로 출력됩니다.

```
$this->error('Something went wrong!');
```

<!-- You may use the `line` method to display plain, uncolored text: -->
색상 없는 일반(Plain) 텍스트를 보여주고 싶다면 `line` 메서드를 씁니다.

```
$this->line('Display this on the screen');
```

<!-- You may use the `newLine` method to display a blank line: -->
빈 줄을 추가하려면 `newLine` 메서드를 사용하세요.

```
// Write a single blank line...
$this->newLine();

// Write three blank lines...
$this->newLine(3);
```

<a name="tables"></a>
<!-- #### Tables -->
#### Tables

<!--
The `table` method makes it easy to correctly format multiple rows / columns of data. All you need to do is provide the column names and the data for the table and Laravel will
automatically calculate the appropriate width and height of the table for you:
-->
`table` 메서드를 사용하면 여러 행/열로 구성된 데이터를 보기 좋게 콘솔에 표시할 수 있습니다. 컬럼 이름과 데이터 배열만 넘기면, Laravel이 적절한 크기와 정렬로 출력해줍니다.

```
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
실행 시간이 오래 걸리는 작업이라면, 진행 상태를 보여주는 프로그레스 바를 표시하는 것이 좋습니다. `withProgressBar` 메서드는 전달받은 반복 가능한 데이터(Iterable)에 대해 반복할 때마다 진행 상태를 콘솔에 표시해줍니다.

```
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item: -->
더 세밀한 제어가 필요하다면, 먼저 전체 단계 수를 지정하고, 각 단계마다 프로그레스 바를 수동으로 갱신할 수도 있습니다.

```
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
> 좀 더 고급 옵션이 필요하다면, [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
<!-- ## Registering Commands -->
## Registering Commands

<!-- All of your console commands are registered within your application's `App\Console\Kernel` class, which is your application's "console kernel". Within the `commands` method of this class, you will see a call to the kernel's `load` method. The `load` method will scan the `app/Console/Commands` directory and automatically register each command it contains with Artisan. You are even free to make additional calls to the `load` method to scan other directories for Artisan commands: -->
모든 콘솔 명령어는 애플리케이션의 `App\Console\Kernel` 클래스(즉, 콘솔 커널)에서 등록됩니다. 이 클래스의 `commands` 메서드에서 커널의 `load` 메서드를 호출합니다. `load` 메서드는 `app/Console/Commands` 디렉터리를 스캔하여, 해당 폴더의 모든 클래스를 자동으로 아티즌에 등록합니다. 필요하다면 여러 디렉터리를 추가로 스캔하도록 `load` 메서드를 여러 번 호출할 수도 있습니다.

```
/**
 * Register the commands for the application.
 */
protected function commands(): void
{
    $this->load(__DIR__.'/Commands');
    $this->load(__DIR__.'/../Domain/Orders/Commands');

    // ...
}
```

<!-- If necessary, you may manually register commands by adding the command's class name to a `$commands` property within your `App\Console\Kernel` class. If this property is not already defined on your kernel, you should define it manually. When Artisan boots, all the commands listed in this property will be resolved by the [service container](/docs/10.x/container) and registered with Artisan: -->
필요하다면, `App\Console\Kernel` 클래스 내의 `$commands` 속성(property)에 명령어 클래스를 직접 명시적으로 추가하여 수동으로 등록할 수도 있습니다. 이 속성이 이미 없다면, 직접 선언해야 합니다. 아티즌이 부팅될 때 이 속성의 모든 명령어가 [service container](/docs/10.x/container)를 통해 resolve되고 아티즌에 자동 등록됩니다.

```
protected $commands = [
    Commands\SendEmails::class
];
```

<a name="programmatically-executing-commands"></a>
<!-- ## Programmatically Executing Commands -->
## Programmatically Executing Commands

<!-- Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned: -->
CLI 이외의 곳에서 아티즌 명령어를 실행해야 할 때가 있습니다. 예를 들어, 라우트나 컨트롤러에서 아티즌 명령어를 실행하고 싶을 수 있습니다. 이 때는 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. `call` 메서드는 첫 번째 인수로 명령어의 시그니처(이름) 또는 클래스 이름, 두 번째 인수로 명령어의 파라미터 배열을 받습니다. 리턴값은 종료 코드(exit code)입니다.

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

<!-- Alternatively, you may pass the entire Artisan command to the `call` method as a string: -->
또는, 전체 아티즌 명령어를 문자열로 `call` 메서드에 전달할 수도 있습니다.

```
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
<!-- #### Passing Array Values -->
#### Passing Array Values

<!-- If your command defines an option that accepts an array, you may pass an array of values to that option: -->
만약 어떤 옵션이 배열을 받을 수 있으면, 해당 옵션에 배열로 값을 전달하면 됩니다.

```
use Illuminate\Support\Facades\Artisan;

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
문자열 값을 받지 않는 옵션(예: `migrate:refresh`의 `--force` 플래그 등)에는 `true` 또는 `false`를 넘기면 됩니다.

```
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
<!-- #### Queueing Artisan Commands -->
#### Queueing Artisan Commands

<!-- Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/10.x/queues). Before using this method, make sure you have configured your queue and are running a queue listener: -->
`Artisan` 파사드의 `queue` 메서드를 사용하면, 아티즌 명령어를 큐에 등록해서 백그라운드의 [queue workers](/docs/10.x/queues)에서 실행할 수도 있습니다. 사용하려면 먼저 큐 설정 후 queue 리스너를 실행하고 있어야 합니다.

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```

<!-- Using the `onConnection` and `onQueue` methods, you may specify the connection or queue the Artisan command should be dispatched to: -->
`onConnection`, `onQueue` 메서드를 체이닝하면, 커맨드를 어떤 연결(connection)이나 큐(queue)에 전달할지 지정할 수 있습니다.

```
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
<!-- ### Calling Commands From Other Commands -->
### Calling Commands From Other Commands

<!-- Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options: -->
기존 아티즌 명령어에서 다른 명령어를 불러 실행하고 싶을 때가 있습니다. 이럴 때는 `call` 메서드를 활용하면 됩니다. 이 `call` 메서드는 명령어 이름과 인수/옵션 배열을 인수로 받습니다.

```
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
만약, 다른 콘솔 명령어를 호출하되 모든 출력까지 숨기고 싶다면, `callSilently` 메서드를 사용하세요. `callSilently` 메서드는 `call` 메서드와 동일한 시그니처를 가집니다.

```
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
<!-- ## Signal Handling -->
## Signal Handling

<!-- As you may know, operating systems allow signals to be sent to running processes. For example, the `SIGTERM` signal is how operating systems ask a program to terminate. If you wish to listen for signals in your Artisan console commands and execute code when they occur, you may use the `trap` method: -->
운영체제에서는 실행 중인 프로세스에 시그널을 보낼 수 있습니다. 예를 들어, `SIGTERM` 시그널은 운영체제가 프로그램에 "종료하라"는 신호를 보내는 방식입니다. 아티즌 콘솔 명령어에서 이런 시그널을 감지해 특정 코드가 실행되도록 하려면, `trap` 메서드를 사용하면 됩니다.

```
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
한 번에 여러 시그널을 감지하고 싶다면, `trap` 메서드에 시그널 배열을 넘기세요.

```
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
<!-- ## Stub Customization -->
## Stub Customization

<!-- The Artisan console's `make` commands are used to create a variety of classes, such as controllers, jobs, migrations, and tests. These classes are generated using "stub" files that are populated with values based on your input. However, you may want to make small changes to files generated by Artisan. To accomplish this, you may use the `stub:publish` command to publish the most common stubs to your application so that you can customize them: -->
아티즌 콘솔의 `make` 계열 명령어들은 컨트롤러, 작업, 마이그레이션, 테스트 등 다양한 클래스를 만들어줍니다. 이 때 생성되는 클래스 파일은 "스텁(stub)" 파일을 기반으로 하며, 입력값에 따라 알맞은 값으로 채워져서 생성됩니다. 그러나 때로는 stub 파일을 수정하고 싶을 때가 있습니다. 그럴 땐 `stub:publish` 명령어로 대표적인 스텁 파일들을 애플리케이션에 공개(publish)할 수 있습니다.

```shell
php artisan stub:publish
```

<!-- The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands. -->
공개된 스텁 파일들은 애플리케이션 루트의 `stubs` 디렉터리에 저장됩니다. 그리고 이 파일을 수정하면, 이후 아티즌의 `make` 명령어로 생성하는 클래스에 해당 내용이 반영됩니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing. -->
아티즌 명령어가 실행될 때는 세 가지 이벤트가 발생합니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`입니다. `ArtisanStarting` 이벤트는 아티즌이 실제로 실행을 시작할 때 즉시 발생하고, `CommandStarting` 이벤트는 각 명령어가 실행 직전에, 마지막으로 `CommandFinished` 이벤트는 명령어 실행이 종료된 직후 발생합니다.
