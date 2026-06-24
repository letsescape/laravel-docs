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
아티즌(Artisan)은 Laravel에 기본 포함된 명령줄 인터페이스입니다. 아티즌은 애플리케이션의 루트 디렉터리에 `artisan` 스크립트 파일로 존재하며, 애플리케이션을 개발할 때 유용하게 활용할 수 있는 여러 가지 명령어를 제공합니다. 사용 가능한 모든 아티즌 명령어 목록을 확인하려면 `list` 명령어를 사용할 수 있습니다.

```shell
php artisan list
```

<!-- Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`: -->
각 명령어에는 해당 명령어에서 사용할 수 있는 인수와 옵션을 보여주고 설명하는 "도움말" 화면이 포함되어 있습니다. 명령어의 도움말을 확인하려면, 명령어 이름 앞에 `help`를 붙여 실행하면 됩니다.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
<!-- #### Laravel Sail -->
#### Laravel Sail

<!-- If you are using [Laravel Sail](/docs/11.x/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers: -->
로컬 개발 환경으로 [Laravel Sail](/docs/11.x/sail)을 사용하고 있다면, 아티즌 명령어를 실행할 때 `sail` 커맨드 라인을 이용해야 한다는 점을 기억하세요. Sail을 통해 실행하는 경우, 명령어는 애플리케이션의 Docker 컨테이너 내에서 동작합니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
<!-- ### Tinker (REPL) -->
### Tinker (REPL)

<!-- Laravel Tinker is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package. -->
Laravel Tinker는 Laravel 프레임워크에서 사용할 수 있는 강력한 REPL 환경으로, [PsySH](https://github.com/bobthecow/psysh) 패키지를 기반으로 동작합니다.

<a name="installation"></a>
<!-- #### Installation -->
#### Installation

<!-- All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application: -->
모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 만약 Tinker를 제거했다면, Composer를 이용해 다시 설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션을 조작할 때 핫 리로딩, 여러 줄 코드 편집, 자동 완성 기능이 필요하다면 [Tinkerwell](https://tinkerwell.app)도 참고해 보세요!

<a name="usage"></a>
<!-- #### Usage -->
#### Usage

<!-- Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command: -->
Tinker를 이용하면 Eloquent 모델, 잡(jobs), 이벤트 등 Laravel 애플리케이션 전체를 명령줄에서 직접 조작할 수 있습니다. Tinker 환경에 진입하려면 `tinker` 아티즌 명령어를 실행하세요.

```shell
php artisan tinker
```

<!-- You can publish Tinker's configuration file using the `vendor:publish` command: -->
`vendor:publish` 명령어를 이용해 Tinker의 설정 파일을 공개(publish)할 수도 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수와 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣기 위해 가비지 컬렉션에 의존합니다. 따라서 Tinker를 사용할 때는 잡을 큐에 추가할 때 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
<!-- #### Command Allow List -->
#### Command Allow List

<!-- Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, and `optimize` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file: -->
Tinker는 쉘 안에서 어떤 아티즌 명령어를 실행할 수 있는지를 "허용 리스트"로 제한합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령어를 실행할 수 있습니다. 만약 더 많은 명령어를 허용하고 싶다면, `tinker.php` 설정 파일의 `commands` 배열에 추가할 수 있습니다.

```
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
<!-- #### Classes That Should Not Be Aliased -->
#### Classes That Should Not Be Aliased

<!-- Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file: -->
Tinker는 일반적으로 Tinker에서 사용되는 클래스에 자동으로 별칭을 지정합니다. 하지만 일부 클래스는 별칭으로 등록하고 싶지 않을 수 있습니다. 이럴 때는 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스명을 추가하면 됩니다.

```
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
<!-- ## Writing Commands -->
## Writing Commands

<!-- In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as your commands can be loaded by Composer. -->
아티즌에 기본으로 내장된 명령어 외에도, 직접 커스텀 명령어를 만들어 사용할 수 있습니다. 명령어는 보통 `app/Console/Commands` 디렉터리에 저장하지만, Composer로 로딩할 수 있는 위치라면 어디든 자유롭게 저장할 수 있습니다.

<a name="generating-commands"></a>
<!-- ### Generating Commands -->
### Generating Commands

<!-- To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command: -->
새로운 명령어를 만들려면 `make:command` 아티즌 명령어를 사용할 수 있습니다. 이 명령어를 실행하면 `app/Console/Commands` 디렉터리에 새 명령어 클래스가 생성됩니다. 해당 디렉터리가 없는 경우에도, `make:command` 명령어를 처음 실행할 때 자동 생성됩니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
<!-- ### Command Structure -->
### Command Structure

<!-- After generating your command, you should define appropriate values for the `signature` and `description` properties of the class. These properties will be used when displaying your command on the `list` screen. The `signature` property also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method. -->
명령어를 생성한 다음에는 클래스의 `signature`와 `description` 속성(property)에 적절한 값을 지정해야 합니다. 이 속성들은 `list` 화면에서 명령어를 표시할 때 활용됩니다. 특히 `signature` 속성은 [your command's input expectations](#defining-input-expectations)도 함께 정의합니다. 명령어가 실행되면 `handle` 메서드가 호출되며, 이 메서드 안에 해당 명령어의 동작 로직을 작성하면 됩니다.

<!-- Let's take a look at an example command. Note that we are able to request any dependencies we need via the command's `handle` method. The Laravel [service container](/docs/11.x/container) will automatically inject all dependencies that are type-hinted in this method's signature: -->
예시 명령어를 함께 살펴보겠습니다. 아래 예제에서는 명령어의 `handle` 메서드를 통해 필요한 의존성을 주입받을 수 있습니다. Laravel의 [service container](/docs/11.x/container)가 이 메서드의 시그니처에 타입힌트된 모든 의존성을 자동으로 주입해줍니다.

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
> 코드의 재사용성을 높이려면, 콘솔 명령어 자체는 되도록 단순하게 유지하고, 실제 작업은 애플리케이션 서비스에 위임하는 것이 좋은 습관입니다. 위 예제에서도 이메일 전송의 실제 처리는 서비스 클래스에 맡기고 있습니다.

<a name="exit-codes"></a>
<!-- #### Exit Codes -->
#### Exit Codes

<!-- If nothing is returned from the `handle` method and the command executes successfully, the command will exit with a `0` exit code, indicating success. However, the `handle` method may optionally return an integer to manually specify command's exit code: -->
`handle` 메서드에서 아무 값도 반환하지 않고 정상적으로 명령어를 실행하면, 종료 코드 `0`으로 성공을 나타냅니다. 하지만 필요하다면 `handle` 메서드에서 정수형 값을 반환하여 명령어의 종료 코드를 수동으로 지정할 수도 있습니다.

```
$this->error('Something went wrong.');

return 1;
```

<!-- If you would like to "fail" the command from any method within the command, you may utilize the `fail` method. The `fail` method will immediately terminate execution of the command and return an exit code of `1`: -->
명령어 클래스 내부의 어느 메서드에서든 명령어를 "실패" 상태로 종료하고 싶다면 `fail` 메서드를 사용할 수 있습니다. `fail` 메서드를 실행하면 즉시 명령어 동작을 중단하고, 종료 코드 `1`을 반환합니다.

```
$this->fail('Something went wrong.');
```

<a name="closure-commands"></a>
<!-- ### Closure Commands -->
### Closure Commands

<!-- Closure based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. -->
클로저 기반 명령어는 클래스로 명령어를 정의하는 대신, 클로저로 콘솔 명령어를 정의할 수 있는 대안을 제공합니다. 마치 라우트의 컨트롤러 대신 라우트 클로저를 사용하는 것처럼, 콘솔 명령어를 클래스 대신 클로저로도 만들 수 있습니다.

<!-- Even though the `routes/console.php` file does not define HTTP routes, it defines console based entry points (routes) into your application. Within this file, you may define all of your closure based console commands using the `Artisan::command` method. The `command` method accepts two arguments: the [command signature](#defining-input-expectations) and a closure which receives the command's arguments and options: -->
`routes/console.php` 파일에서는 HTTP 라우트를 정의하지 않지만, 애플리케이션 진입점 역할을 하는 콘솔 기반 라우트(엔트리)를 정의합니다. 이 파일에서는 `Artisan::command` 메서드를 통해 클로저 기반 콘솔 명령어를 모두 정의할 수 있습니다. `command` 메서드는 두 개의 인자(아규먼트)를 받으며, 첫 번째는 [command signature](#defining-input-expectations), 두 번째는 명령어 인수와 옵션을 받는 클로저입니다.

```
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```

<!-- The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class. -->
클로저는 내부적으로 해당 명령어 인스턴스에 바인딩되어, 클래스 기반 명령어에서 접근할 수 있던 헬퍼 메서드를 그대로 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
<!-- #### Type-Hinting Dependencies -->
#### Type-Hinting Dependencies

<!-- In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/11.x/container): -->
명령어 인수와 옵션뿐만 아니라, 클로저로 만든 명령어에서도 추가로 필요한 의존성을 [service container](/docs/11.x/container)로부터 타입힌트로 받아올 수 있습니다.

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
클로저 기반 명령어를 정의할 때, `purpose` 메서드를 사용하면 해당 명령어에 대한 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 명령어를 실행할 때 표시됩니다.

```
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
<!-- ### Isolatable Commands -->
### Isolatable Commands

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 드라이버 중 하나를 선택해야 합니다. 또한 모든 서버가 동일한 중앙 캐시 서버와 통신해야 합니다.

<!-- Sometimes you may wish to ensure that only one instance of a command can run at a time. To accomplish this, you may implement the `Illuminate\Contracts\Console\Isolatable` interface on your command class: -->
동일한 명령어가 한 번에 단 하나만 실행되도록 제한하고 싶을 때가 있습니다. 이럴 때는 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다.

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
명령어에 `Isolatable`이 표시되어 있으면, Laravel은 해당 명령어에 자동으로 `--isolated` 옵션을 추가합니다. 이 옵션과 함께 명령어를 실행하면, 동일한 명령어가 이미 실행 중인 경우 중복으로 실행되지 않도록 Laravel이 관리합니다. Laravel은 기본 캐시 드라이버를 사용해 원자적 락(atomic lock)을 시도하여 이를 구현합니다. 만약 이미 실행 중인 명령어가 있으면, 실제 명령어 동작은 실행되지 않지만, 종료 상태 코드는 성공으로 반환됩니다.

```shell
php artisan mail:send 1 --isolated
```

<!-- If you would like to specify the exit status code that the command should return if it is not able to execute, you may provide the desired status code via the `isolated` option: -->
명령어가 실행되지 않았을 때 반환할 종료 상태 코드를 직접 지정하려면, `isolated` 옵션에 원하는 코드를 입력할 수 있습니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-id"></a>
<!-- #### Lock ID -->
#### Lock ID

<!-- By default, Laravel will use the command's name to generate the string key that is used to acquire the atomic lock in your application's cache. However, you may customize this key by defining an `isolatableId` method on your Artisan command class, allowing you to integrate the command's arguments or options into the key: -->
기본적으로 Laravel은 원자적 락의 문자열 키를 생성할 때 명령어 이름을 사용합니다. 하지만, `isolatableId` 메서드를 아티즌 명령어 클래스에 정의하면, 필요한 경우 명령어 인수나 옵션을 락 키에 추가하는 등 값을 직접 커스터마이즈할 수 있습니다.

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
기본적으로, 격리 락(isolation lock)은 명령어 실행이 끝나면 바로 만료됩니다. 명령어 실행이 중단되어 끝나지 못했다면, 락은 한 시간 후 자동으로 만료됩니다. 만약 이 만료 시간을 직접 조정하고 싶으면, 명령어 클래스에 `isolationLockExpiresAt` 메서드를 정의할 수 있습니다.

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
콘솔 명령어를 작성할 때, 사용자로부터 인수 또는 옵션 등의 입력값을 받는 일이 많습니다. Laravel에서는 명령어의 `signature` 속성을 사용해 입력 기대값을 매우 직관적이고 선언적으로 정의할 수 있습니다. `signature` 속성에서 명령어의 이름, 인수, 옵션을 하나의 명령어 시그니처(라우트처럼 표현)로 정의합니다.

<a name="arguments"></a>
<!-- ### Arguments -->
### Arguments

<!-- All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`: -->
사용자로부터 입력받는 모든 인수와 옵션은 중괄호로 감쌉니다. 아래 예제에서 명령어는 `user`라는 이름의 필수 인수를 정의합니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

<!-- You may also make arguments optional or define default values for arguments: -->
인수를 선택적으로 만들거나, 기본값을 정의할 수도 있습니다.

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
옵션 역시 인수와 같이 사용자 입력을 받는 또 다른 방식입니다. 옵션은 커맨드 라인에서 두 개의 하이픈(`--`)을 붙여 지정합니다. 옵션에는 값이 필요한 경우와 값이 없는 경우(스위치형)이 있습니다. 값이 없는 옵션은 불리언(boolean) 스위치 역할을 합니다. 아래 예시는 불리언 스위치형 옵션입니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

<!-- In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`: -->
이 예에서는 `--queue` 스위치를 아티즌 명령어 실행 시 지정할 수 있습니다. `--queue` 스위치가 전달되면 옵션 값은 `true`, 전달되지 않으면 `false`가 됩니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
<!-- #### Options With Values -->
#### Options With Values

<!-- Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign: -->
이번에는 값이 반드시 필요한 옵션을 살펴보겠습니다. 값을 꼭 지정해야 하는 옵션에는 옵션명 뒤에 `=`(등호)를 붙여 표현합니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

<!-- In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`: -->
이 예제에서, 사용자는 아래와 같이 옵션 값을 넘길 수 있습니다. 만약 옵션 없이 명령어를 실행하면 해당 옵션 값은 `null`입니다.

```shell
php artisan mail:send 1 --queue=default
```

<!-- You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used: -->
옵션에도 기본값을 지정할 수 있으며, 값을 넘기지 않은 경우에는 기본값이 사용됩니다.

```
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
<!-- #### Option Shortcuts -->
#### Option Shortcuts

<!-- To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name: -->
옵션에 단축키를 부여하려면 옵션명 앞에 단축키를 쓰고, `|`(파이프)로 구분하면 됩니다.

```
'mail:send {user} {--Q|queue}'
```

<!-- When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen and no `=` character should be included when specifying a value for the option: -->
터미널에서 명령어를 실행할 때는 옵션 단축키 앞에 하이픈 하나만 붙이고, 값을 지정할 경우 등호(`=`) 없이 바로 이어 붙이면 됩니다.

```shell
php artisan mail:send 1 -Qdefault
```

<a name="input-arrays"></a>
<!-- ### Input Arrays -->
### Input Arrays

<!-- If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument: -->
여러 개의 입력값(인수 또는 옵션)을 받고 싶을 때는 `*` 문자로 정의하면 됩니다. 먼저 인수 예시를 보겠습니다.

```
'mail:send {user*}'
```

<!-- When calling this method, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `1` and `2` as its values: -->
이 방식으로 명령어를 실행할 때, `user` 인수는 명령줄에 순서대로 전달할 수 있습니다. 예를 들어 아래 명령어를 실행하면, `user`의 값은 `1`과 `2`를 원소로 가지는 배열이 됩니다.

```shell
php artisan mail:send 1 2
```

<!-- This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument: -->
`*` 문자는 선택적 인수 옵션과 함께 사용해 인수 값을 0개 이상 받을 수도 있습니다.

```
'mail:send {user?*}'
```

<a name="option-arrays"></a>
<!-- #### Option Arrays -->
#### Option Arrays

<!-- When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name: -->
옵션도 여러 값이 필요한 경우, 값마다 옵션명을 반복해서 넘기면 됩니다.

```
'mail:send {--id=*}'
```

<!-- Such a command may be invoked by passing multiple `--id` arguments: -->
이렇게 정의하면 명령어 실행 시 여러 `--id` 옵션을 넘길 수 있습니다.

```shell
php artisan mail:send --id=1 --id=2
```

<a name="input-descriptions"></a>
<!-- ### Input Descriptions -->
### Input Descriptions

<!-- You may assign descriptions to input arguments and options by separating the argument name from the description using a colon. If you need a little extra room to define your command, feel free to spread the definition across multiple lines: -->
명령어 인수와 옵션에 콜론을 사용해 이름과 설명을 구분하여 설명을 추가할 수 있습니다. 명령어 시그니처가 길어질 경우 여러 줄에 걸쳐 정의해도 괜찮습니다.

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
명령어에 필수 인수가 있을 때, 사용자가 입력하지 않으면 에러 메시지가 표시됩니다. 대신, 필수 인수가 누락된 경우 사용자에게 입력을 자동으로 요청하도록 설정할 수도 있습니다. 이를 위해 `PromptsForMissingInput` 인터페이스를 구현하면 됩니다.

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
Laravel이 필수 인수를 입력받아야 하는 상황이라면, 자동으로 인수의 이름이나 설명을 기반으로 적절한 질문을 생성해 사용자에게 입력을 요청합니다. 만약 입력 요청에 사용할 질문을 직접 지정하고 싶으면, `promptForMissingArgumentsUsing` 메서드를 구현해 각 인수 이름별로 질문 배열을 반환하면 됩니다.

```
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
질문과 함께 플레이스홀더(placeholder) 텍스트도 튜플 형태로 제공할 수 있습니다.

```
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```

<!-- If you would like complete control over the prompt, you may provide a closure that should prompt the user and return their answer: -->
프롬프트 전체를 커스터마이징하고 싶다면, 사용자 입력을 요청하고 그 답을 반환하는 클로저를 지정할 수도 있습니다.

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
> <!-- The comprehensive [Laravel Prompts](/docs/11.x/prompts) documentation includes additional information on the available prompts and their usage. -->
> 자세한 프롬프트 활용법은 [Laravel Prompts](/docs/11.x/prompts) 공식 문서를 참고하세요.

<!-- If you wish to prompt the user to select or enter [options](#options), you may include prompts in your command's `handle` method. However, if you only wish to prompt the user when they have also been automatically prompted for missing arguments, then you may implement the `afterPromptingForMissingArguments` method: -->
사용자에게 [options](#options)을 선택하거나 직접 입력하도록 프롬프트를 띄우고 싶다면, 프롬프트를 명령어의 `handle` 메서드에서 실행하면 됩니다. 하지만 누락된 인수 프롬프트가 자동으로 띄워진 뒤에만 추가로 질의를 하고 싶다면, `afterPromptingForMissingArguments` 메서드를 구현해 활용할 수 있습니다.

```
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
명령어가 실행되는 동안, 사용자가 넘긴 인수나 옵션 값을 코드에서 사용할 일이 많습니다. 이럴 때는 `argument`와 `option` 메서드를 사용할 수 있습니다. 해당 인수 또는 옵션이 존재하지 않는 경우 `null`이 반환됩니다.

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
모든 인수값을 `array`로 한꺼번에 가져오려면 `arguments` 메서드를 호출하면 됩니다.

```
$arguments = $this->arguments();
```

<!-- Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method: -->
옵션 역시 `option` 메서드로 쉽게 값을 가져올 수 있으며, 전체 옵션 값을 배열로 가져오려면 `options` 메서드를 사용합니다.

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
> [Laravel Prompts](/docs/11.x/prompts)는 커맨드 라인 애플리케이션에 아름답고 사용자 친화적인 폼을 추가할 수 있는 PHP 패키지입니다. 이 패키지는 플레이스홀더 텍스트와 유효성 검증 등 브라우저와 비슷한 기능도 제공합니다.

<!-- In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command: -->
출력만 하는 것이 아니라, 명령어 실행 중 사용자에게 직접 입력을 요청할 수도 있습니다. `ask` 메서드를 사용하면 사용자가 입력해야 할 질문을 표시하고, 입력 값을 받아 명령어 내부에서 활용할 수 있습니다.

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
`ask` 메서드는 두 번째 인수로 기본값도 지정할 수 있습니다. 사용자가 아무 값도 입력하지 않으면 이 값이 반환됩니다.

```
$name = $this->ask('What is your name?', 'Taylor');
```

<!-- The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as passwords: -->
`secret` 메서드는 `ask`와 유사하지만, 사용자가 콘솔에 입력하는 내용을 화면에 표시하지 않습니다. 비밀번호 등 민감한 정보를 질문할 때 유용합니다.

```
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
<!-- #### Asking for Confirmation -->
#### Asking for Confirmation

<!-- If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`. -->
사용자에게 단순한 "예/아니오" 확인을 받고 싶을 때는 `confirm` 메서드를 사용할 수 있습니다. 이 메서드는 기본적으로 `false`를 반환하지만, 사용자가 `y` 혹은 `yes`를 입력하면 `true`를 반환합니다.

```
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```

<!-- If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method: -->
필요하다면, `confirm` 메서드의 두 번째 인수로 `true`를 전달해 기본값을 `true`로 설정할 수도 있습니다.

```
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```

<a name="auto-completion"></a>
<!-- #### Auto-Completion -->
#### Auto-Completion

<!-- The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
`anticipate` 메서드는 입력 값에 대한 자동 완성 기능을 제공합니다. 자동 완성 힌트와 관계없이 사용자는 어떤 값을 입력해도 됩니다.

```
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion: -->
또는, `anticipate` 메서드의 두 번째 인수로 클로저를 넘길 수도 있습니다. 이 클로저는 사용자가 문자를 입력할 때마다 호출되며, 입력한 내용을 인수로 받아 자동 완성 옵션의 배열을 반환해야 합니다.

```
$name = $this->anticipate('What is your address?', function (string $input) {
    // Return auto-completion options...
});
```

<a name="multiple-choice-questions"></a>
<!-- #### Multiple Choice Questions -->
#### Multiple Choice Questions

<!-- If you need to give the user a predefined set of choices when asking a question, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen by passing the index as the third argument to the method: -->
사용자에게 미리 정해진 여러 선택지 중 하나를 선택하도록 하려면 `choice` 메서드를 사용할 수 있습니다. 세 번째 인수로 기본값에 해당하는 배열의 인덱스를 지정할 수도 있습니다. 사용자가 아무것도 선택하지 않으면 이 인덱스의 값이 반환됩니다.

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

<!-- In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted: -->
또한, `choice` 메서드는 유효한 값을 선택할 수 있는 최대 시도 횟수와 다중 선택 허용 여부를 결정하는 선택적 네 번째, 다섯 번째 인수를 받습니다.

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
콘솔로 메시지를 출력하려면 `line`, `info`, `comment`, `question`, `warn`, `error` 등의 메서드를 사용할 수 있습니다. 이 메서드들은 각각에 맞는 ANSI 색상을 사용해 텍스트를 표시합니다. 예를 들어, 일반적인 정보를 사용자에게 보여 주고 싶으면 `info` 메서드를 사용합니다. 이때는 보통 콘솔에 초록색 글자로 출력됩니다.

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
오류 메시지를 출력하려면 `error` 메서드를 사용합니다. 오류 메시지는 보통 빨간색으로 표시됩니다.

```
$this->error('Something went wrong!');
```

<!-- You may use the `line` method to display plain, uncolored text: -->
색상 없이 일반 텍스트를 출력하고 싶을 때는 `line` 메서드를 사용합니다.

```
$this->line('Display this on the screen');
```

<!-- You may use the `newLine` method to display a blank line: -->
빈 줄을 출력하려면 `newLine` 메서드를 사용합니다.

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
`table` 메서드는 여러 행과 컬럼으로 이루어진 데이터를 보기 좋게 테이블 형식으로 출력할 수 있도록 도와줍니다. 컬럼명과 데이터만 넘겨주면, Laravel이 테이블의 너비와 높이를 자동으로 계산해서 출력해 줍니다.

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
처리 시간이 오래 걸리는 작업을 할 때, 현재 완료된 정도를 사용자에게 보여주면 좋습니다. `withProgressBar` 메서드를 사용하면, Laravel이 주어진 반복 가능한 값에 대해 순회할 때 자동으로 진행률 바를 표시하고 진행 상황을 갱신합니다.

```
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item: -->
좀 더 세밀하게 진행률 바의 동작을 제어하려면, 먼저 전체 단계 수를 지정해서 진행률 바를 만들고, 각 항목을 처리할 때마다 직접 진행 상황을 갱신하면 됩니다.

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
> 더 많은 고급 옵션이 궁금하다면 [Symfony Progress Bar component documentation](https://symfony.com/doc/7.0/components/console/helpers/progressbar.html)를 참고하십시오.

<a name="registering-commands"></a>
<!-- ## Registering Commands -->
## Registering Commands

<!-- By default, Laravel automatically registers all commands within the `app/Console/Commands` directory. However, you can instruct Laravel to scan other directories for Artisan commands using the `withCommands` method in your application's `bootstrap/app.php` file: -->
기본적으로 Laravel은 `app/Console/Commands` 디렉토리 안에 있는 모든 명령어를 자동으로 등록합니다. 하지만, 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용해 다른 디렉토리에서 Artisan 명령어를 검색하도록 지시할 수도 있습니다.

```
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```

<!-- If necessary, you may also manually register commands by providing the command's class name to the `withCommands` method: -->
필요하다면, 명령어 클래스 이름을 직접 지정해서 `withCommands` 메서드로 수동 등록할 수도 있습니다.

```
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```

<!-- When Artisan boots, all the commands in your application will be resolved by the [service container](/docs/11.x/container) and registered with Artisan. -->
Artisan이 부팅될 때, 애플리케이션의 모든 명령어는 [service container](/docs/11.x/container)에 의해 resolve(해결)되고 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
<!-- ## Programmatically Executing Commands -->
## Programmatically Executing Commands

<!-- Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned: -->
CLI가 아닌 곳에서 Artisan 명령어를 실행하고 싶을 때가 있습니다. 예를 들어, 라우트나 컨트롤러 내부에서 Artisan 명령어를 실행하고자 할 수 있습니다. 이럴 때는 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. `call` 메서드의 첫 번째 인수에는 명령어 시그니처 이름이나 클래스 이름을 넣고, 두 번째 인수로는 명령어 파라미터의 배열을 넘깁니다. 반환값은 종료 코드(exit code)입니다.

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
또는 전체 Artisan 명령어를 문자열로 `call` 메서드에 전달할 수도 있습니다.

```
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
<!-- #### Passing Array Values -->
#### Passing Array Values

<!-- If your command defines an option that accepts an array, you may pass an array of values to that option: -->
명령어에서 배열을 인수로 받도록 옵션을 정의한 경우, 해당 옵션에 값의 배열을 넘길 수 있습니다.

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
`migrate:refresh` 명령어의 `--force` 플래그처럼 문자열이 아닌 값을 받아야 하는 옵션에는 값으로 `true`나 `false`를 지정할 수 있습니다.

```
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
<!-- #### Queueing Artisan Commands -->
#### Queueing Artisan Commands

<!-- Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/11.x/queues). Before using this method, make sure you have configured your queue and are running a queue listener: -->
`Artisan` 파사드의 `queue` 메서드를 사용하면 Artisan 명령어를 큐에 넣어서, [queue workers](/docs/11.x/queues)가 백그라운드에서 처리하도록 할 수 있습니다. 이 기능을 사용하기 전에 큐 설정을 마치고 큐 리스너가 실행 중인지 확인해야 합니다.

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
`onConnection`과 `onQueue` 메서드를 사용하면 해당 Artisan 명령어가 전송될 큐 커넥션이나 큐 이름도 직접 지정할 수 있습니다.

```
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
<!-- ### Calling Commands From Other Commands -->
### Calling Commands From Other Commands

<!-- Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options: -->
기존 Artisan 명령어 내부에서 또 다른 명령어를 호출해야 할 때가 있습니다. 이럴 때는 `call` 메서드를 사용할 수 있습니다. 이 `call` 메서드는 명령어 이름과 인수/옵션 배열을 인수로 받습니다.

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
기타 콘솔 명령어를 호출하면서 그 명령어의 모든 출력을 숨기고 싶으면, `callSilently` 메서드를 사용하면 됩니다. `callSilently` 메서드는 `call` 메서드와 동일한 시그니처를 가집니다.

```
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
<!-- ## Signal Handling -->
## Signal Handling

<!-- As you may know, operating systems allow signals to be sent to running processes. For example, the `SIGTERM` signal is how operating systems ask a program to terminate. If you wish to listen for signals in your Artisan console commands and execute code when they occur, you may use the `trap` method: -->
운영체제는 프로그램에 신호(signal)를 보낼 수 있습니다. 예를 들어, `SIGTERM` 신호는 운영체제가 프로그램에 종료를 요청할 때 전송합니다. Artisan 콘솔 명령어에서 이러한 신호를 감지해 신호가 도착했을 때 코드를 실행하고 싶다면, `trap` 메서드를 사용하면 됩니다.

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
여러 개의 신호를 동시에 감지하려면 `trap` 메서드에 신호들의 배열을 넘길 수 있습니다.

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
Artisan 콘솔의 `make` 명령어는 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이 클래스들은 입력 값에 따라 일부 값을 채워넣는 "스텁" 파일을 기반으로 만들어집니다. Artisan이 만들어주는 파일에 소소하게 변경을 가하고 싶다면, `stub:publish` 명령어로 가장 일반적으로 사용하는 스텁 파일을 애플리케이션에 공개한 뒤, 원하는 대로 수정할 수 있습니다.

```shell
php artisan stub:publish
```

<!-- The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands. -->
공개된 스텁 파일은 애플리케이션 루트의 `stubs` 디렉토리에 위치하게 됩니다. 이 파일을 수정하면, Artisan의 `make` 명령어로 해당 타입의 클래스를 만들 때마다 변경 내용이 반영됩니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing. -->
Artisan은 명령어 실행 시 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`입니다. `ArtisanStarting` 이벤트는 Artisan이 실행을 시작할 때 바로 발생하며, 그 다음엔서 각 명령어가 실행되기 직전에 `CommandStarting` 이벤트가 발생합니다. 마지막으로 명령어 실행이 끝나면 `CommandFinished` 이벤트가 발생합니다.