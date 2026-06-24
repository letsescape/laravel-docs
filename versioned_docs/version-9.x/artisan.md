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
- [Command I/O](#command-io)
    - [Retrieving Input](#retrieving-input)
    - [Prompting For Input](#prompting-for-input)
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
Artisan은 Laravel에 기본 포함된 명령줄 인터페이스입니다. Artisan은 애플리케이션의 루트 디렉터리에 `artisan` 스크립트로 위치하며, 애플리케이션을 개발할 때 유용하게 사용할 수 있는 다양한 명령어를 제공합니다. 사용 가능한 모든 Artisan 명령어를 확인하려면 `list` 명령어를 사용하십시오.

```shell
php artisan list
```

<!-- Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, precede the name of the command with `help`: -->
각 명령어에는 해당 명령어에서 사용할 수 있는 인수와 옵션을 보여주는 "도움말" 화면이 함께 제공됩니다. 도움말 화면을 확인하려면 명령어 이름 앞에 `help`를 붙여 실행하면 됩니다.

```shell
php artisan help migrate
```

<a name="laravel-sail"></a>
<!-- #### Laravel Sail -->
#### Laravel Sail

<!-- If you are using [Laravel Sail](/docs/9.x/sail) as your local development environment, remember to use the `sail` command line to invoke Artisan commands. Sail will execute your Artisan commands within your application's Docker containers: -->
[Laravel Sail](/docs/9.x/sail)을 로컬 개발 환경으로 사용 중이라면, Artisan 명령어를 실행할 때 반드시 `sail` 커맨드라인을 사용해야 합니다. Sail은 해당 Artisan 명령어를 애플리케이션의 Docker 컨테이너 안에서 실행합니다.

```shell
./vendor/bin/sail artisan list
```

<a name="tinker"></a>
<!-- ### Tinker (REPL) -->
### Tinker (REPL)

<!-- Laravel Tinker is a powerful REPL for the Laravel framework, powered by the [PsySH](https://github.com/bobthecow/psysh) package. -->
Laravel Tinker는 Laravel 프레임워크에서 강력한 REPL 환경을 제공하며, [PsySH](https://github.com/bobthecow/psysh) 패키지로 구동됩니다.

<a name="installation"></a>
<!-- #### Installation -->
#### Installation

<!-- All Laravel applications include Tinker by default. However, you may install Tinker using Composer if you have previously removed it from your application: -->
Tinker는 모든 Laravel 애플리케이션에 기본 포함되어 있습니다. 하지만, 이전에 Tinker를 애플리케이션에서 제거했다면 Composer를 사용해 다시 설치할 수 있습니다.

```shell
composer require laravel/tinker
```

> [!NOTE]
> Laravel 애플리케이션과 상호작용할 수 있는 그래픽 UI가 필요하신가요? [Tinkerwell](https://tinkerwell.app)을 확인해 보세요!

<a name="usage"></a>
<!-- #### Usage -->
#### Usage

<!-- Tinker allows you to interact with your entire Laravel application on the command line, including your Eloquent models, jobs, events, and more. To enter the Tinker environment, run the `tinker` Artisan command: -->
Tinker를 사용하면 명령줄에서 Laravel 애플리케이션 전체와, Eloquent 모델, 잡(jobs), 이벤트 등 다양한 부분과 상호작용할 수 있습니다. Tinker 환경에 진입하려면 `tinker` Artisan 명령어를 실행합니다.

```shell
php artisan tinker
```

<!-- You can publish Tinker's configuration file using the `vendor:publish` command: -->
Tinker의 설정 파일은 `vendor:publish` 명령어로 배포할 수 있습니다.

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```

> [!WARNING]
> `dispatch` 헬퍼 함수나 `Dispatchable` 클래스의 `dispatch` 메서드는 잡을 큐에 넣을 때 가비지 컬렉션에 의존합니다. 따라서 Tinker를 사용할 때는 `Bus::dispatch` 또는 `Queue::push`를 이용해 잡을 디스패치해야 합니다.

<a name="command-allow-list"></a>
<!-- #### Command Allow List -->
#### Command Allow List

<!-- Tinker utilizes an "allow" list to determine which Artisan commands are allowed to be run within its shell. By default, you may run the `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, and `up` commands. If you would like to allow more commands you may add them to the `commands` array in your `tinker.php` configuration file: -->
Tinker는 쉘 안에서 어떤 Artisan 명령어를 실행할 수 있는지 "허용(allow)" 리스트를 사용해 결정합니다. 기본적으로 `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `optimize`, `up` 명령어는 실행할 수 있습니다. 허용할 명령어를 추가하고 싶다면 `tinker.php` 설정 파일의 `commands` 배열에 추가하세요.

```
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```

<a name="classes-that-should-not-be-aliased"></a>
<!-- #### Classes That Should Not Be Aliased -->
#### Classes That Should Not Be Aliased

<!-- Typically, Tinker automatically aliases classes as you interact with them in Tinker. However, you may wish to never alias some classes. You may accomplish this by listing the classes in the `dont_alias` array of your `tinker.php` configuration file: -->
대부분의 경우 Tinker는 클래스와 상호작용할 때 자동으로 alias를 생성해줍니다. 하지만 일부 클래스는 alias를 생성하지 않도록 예외를 둘 수 있습니다. 이때는 `tinker.php` 설정 파일의 `dont_alias` 배열에 해당 클래스를 추가하면 됩니다.

```
'dont_alias' => [
    App\Models\User::class,
],
```

<a name="writing-commands"></a>
<!-- ## Writing Commands -->
## Writing Commands

<!-- In addition to the commands provided with Artisan, you may build your own custom commands. Commands are typically stored in the `app/Console/Commands` directory; however, you are free to choose your own storage location as long as your commands can be loaded by Composer. -->
Artisan이 기본 제공하는 명령어 외에도 직접 커스텀 명령어를 개발할 수 있습니다. 명령어 클래스는 보통 `app/Console/Commands` 디렉터리에 저장합니다. 하지만 Composer로 로드될 수 있다면 다른 위치에 자유롭게 저장해도 무방합니다.

<a name="generating-commands"></a>
<!-- ### Generating Commands -->
### Generating Commands

<!-- To create a new command, you may use the `make:command` Artisan command. This command will create a new command class in the `app/Console/Commands` directory. Don't worry if this directory does not exist in your application - it will be created the first time you run the `make:command` Artisan command: -->
새 명령어를 만들 때는 `make:command` Artisan 명령어를 사용하면 됩니다. 이 명령어를 실행하면 `app/Console/Commands` 디렉터리에 새로운 명령어 클래스가 생성됩니다. 이 디렉터리가 애플리케이션에 없더라도, `make:command` Artisan 명령어를 처음 실행할 때 자동으로 만들어집니다.

```shell
php artisan make:command SendEmails
```

<a name="command-structure"></a>
<!-- ### Command Structure -->
### Command Structure

<!-- After generating your command, you should define appropriate values for the `signature` and `description` properties of the class. These properties will be used when displaying your command on the `list` screen. The `signature` property also allows you to define [your command's input expectations](#defining-input-expectations). The `handle` method will be called when your command is executed. You may place your command logic in this method. -->
명령어를 생성했다면, 해당 클래스의 `signature`와 `description` 속성(property)에 적절한 값을 정의해야 합니다. 이 값들은 명령어를 `list` 화면에서 표시할 때 사용됩니다. 또한 `signature` 속성을 활용해 [your command's input expectations](#defining-input-expectations)도 함께 정의할 수 있습니다. `handle` 메서드는 명령어가 실제 실행될 때 호출됩니다. 이 메서드 안에서 명령어의 실행 로직을 작성하면 됩니다.

<!-- Let's take a look at an example command. Note that we are able to request any dependencies we need via the command's `handle` method. The Laravel [service container](/docs/9.x/container) will automatically inject all dependencies that are type-hinted in this method's signature: -->
예시 명령어를 살펴보겠습니다. `handle` 메서드에서 의존성이 필요한 경우, Laravel [service container](/docs/9.x/container)가 타입힌트로 지정된 의존성을 자동으로 주입해줍니다.

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
     *
     * @param  \App\Support\DripEmailer  $drip
     * @return mixed
     */
    public function handle(DripEmailer $drip)
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```

> [!NOTE]
> 코드 재사용성을 높이기 위해, 콘솔 명령어의 본문은 최대한 가볍게 유지하고 실제 주요 로직은 애플리케이션 서비스에 위임하는 것이 좋습니다. 위 예시에서도 이메일 발송의 "주요 작업"을 별도의 서비스 클래스에 맡기고 있습니다.

<a name="closure-commands"></a>
<!-- ### Closure Commands -->
### Closure Commands

<!-- Closure based commands provide an alternative to defining console commands as classes. In the same way that route closures are an alternative to controllers, think of command closures as an alternative to command classes. Within the `commands` method of your `app/Console/Kernel.php` file, Laravel loads the `routes/console.php` file: -->
클래스로 명령어를 정의하지 않고, 클로저(익명함수) 기반으로 명령어를 정의할 수도 있습니다. 라우트에서 클로저가 컨트롤러의 대안인 것처럼, 클로저 명령어도 클래스 기반 명령어의 다른 방식으로 활용할 수 있습니다. `app/Console/Kernel.php` 파일의 `commands` 메서드에서는 `routes/console.php` 파일을 로드하게 되어 있습니다.

```
/**
 * Register the closure based commands for the application.
 *
 * @return void
 */
protected function commands()
{
    require base_path('routes/console.php');
}
```

<!-- Even though this file does not define HTTP routes, it defines console based entry points (routes) into your application. Within this file, you may define all of your closure based console commands using the `Artisan::command` method. The `command` method accepts two arguments: the [command signature](#defining-input-expectations) and a closure which receives the command's arguments and options: -->
이 파일은 HTTP 라우트를 정의하는 것이 아니라, 애플리케이션으로 진입할 수 있는 콘솔 기반의 "엔트리 포인트(라우트)"를 정의하는 파일입니다. 이곳에서 `Artisan::command` 메서드를 사용해 클로저 기반 명령어를 정의할 수 있습니다. `command` 메서드는 [command signature](#defining-input-expectations)와 인수, 옵션을 받을 클로저를 받습니다.

```
Artisan::command('mail:send {user}', function ($user) {
    $this->info("Sending email to: {$user}!");
});
```

<!-- The closure is bound to the underlying command instance, so you have full access to all of the helper methods you would typically be able to access on a full command class. -->
클로저는 해당 명령어 인스턴스에 바인딩되어 있으므로, 명령어 클래스에서 사용 가능한 모든 헬퍼 메서드를 그대로 사용할 수 있습니다.

<a name="type-hinting-dependencies"></a>
<!-- #### Type-Hinting Dependencies -->
#### Type-Hinting Dependencies

<!-- In addition to receiving your command's arguments and options, command closures may also type-hint additional dependencies that you would like resolved out of the [service container](/docs/9.x/container): -->
명령어 시그니처에 정의된 인수와 옵션뿐만 아니라, [service container](/docs/9.x/container)에서 자동으로 해결되는 다른 의존성도 클로저에서 타입힌트로 지정할 수 있습니다.

```
use App\Models\User;
use App\Support\DripEmailer;

Artisan::command('mail:send {user}', function (DripEmailer $drip, $user) {
    $drip->send(User::find($user));
});
```

<a name="closure-command-descriptions"></a>
<!-- #### Closure Command Descriptions -->
#### Closure Command Descriptions

<!-- When defining a closure based command, you may use the `purpose` method to add a description to the command. This description will be displayed when you run the `php artisan list` or `php artisan help` commands: -->
클로저 기반 명령어를 정의할 때, `purpose` 메서드를 이용해 명령어 설명을 추가할 수 있습니다. 이 설명은 `php artisan list`나 `php artisan help` 실행 시 표시됩니다.

```
Artisan::command('mail:send {user}', function ($user) {
    // ...
})->purpose('Send a marketing email to a user');
```

<a name="isolatable-commands"></a>
<!-- ### Isolatable Commands -->
### Isolatable Commands

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션의 기본 캐시 드라이버로 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 중 하나를 사용해야 합니다. 그리고 모든 서버가 동일한 중앙 캐시 서버와 통신하고 있어야 합니다.

<!-- Sometimes you may wish to ensure that only one instance of a command can run at a time. To accomplish this, you may implement the `Illuminate\Contracts\Console\Isolatable` interface on your command class: -->
하나의 명령어 인스턴스만 동시에 실행되도록 제한해야 할 상황이 있을 수 있습니다. 이 기능이 필요하다면 명령어 클래스에서 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현하면 됩니다.

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
명령어가 `Isolatable`로 마크되면, Laravel은 자동으로 해당 명령어에 `--isolated` 옵션을 추가해줍니다. 옵션을 포함해 명령어를 실행하면, Laravel은 동일한 명령어가 이미 실행 중인지 확인하여 중복 실행을 막아줍니다. 이 기능은 애플리케이션에서 기본 캐시 드라이버를 사용해 원자적(atomic) 락을 획득하는 방식으로 동작합니다. 만약 이미 명령어 인스턴스가 실행 중이라면, 명령어는 실행되지 않고, 정상 종료 상태(ex: 0)로 종료됩니다.

```shell
php artisan mail:send 1 --isolated
```

<!-- If you would like to specify the exit status code that the command should return if it is not able to execute, you may provide the desired status code via the `isolated` option: -->
명령어가 실행되지 못했을 때 반환할 종료 상태 코드를 지정하고 싶다면 `isolated` 옵션에 원하는 값을 전달할 수 있습니다.

```shell
php artisan mail:send 1 --isolated=12
```

<a name="lock-expiration-time"></a>
<!-- #### Lock Expiration Time -->
#### Lock Expiration Time

<!-- By default, isolation locks expire after the command is finished. Or, if the command is interrupted and unable to finish, the lock will expire after one hour. However, you may adjust the lock expiration time by defining a `isolationLockExpiresAt` method on your command: -->
기본적으로, isolation 락은 명령어 실행이 끝나면 바로 해제됩니다. 만약 명령어가 중단(interrupt)되어 정상적으로 종료되지 못할 경우, 락은 1시간 후에 만료됩니다. 락의 만료 시간을 변경하려면 명령어 클래스에 `isolationLockExpiresAt` 메서드를 정의하면 됩니다.

```php
/**
 * Determine when an isolation lock expires for the command.
 *
 * @return \DateTimeInterface|\DateInterval
 */
public function isolationLockExpiresAt()
{
    return now()->addMinutes(5);
}
```

<a name="defining-input-expectations"></a>
<!-- ## Defining Input Expectations -->
## Defining Input Expectations

<!-- When writing console commands, it is common to gather input from the user through arguments or options. Laravel makes it very convenient to define the input you expect from the user using the `signature` property on your commands. The `signature` property allows you to define the name, arguments, and options for the command in a single, expressive, route-like syntax. -->
콘솔 명령어를 작성할 때 사용자의 입력을 인수 또는 옵션 형태로 받는 일이 많습니다. Laravel은 각 명령어 클래스의 `signature` 속성을 통해 사용자에게 기대하는 입력값을 매우 편리하게 정의할 수 있도록 도와줍니다. `signature` 속성을 사용하면 명령어의 이름, 인수, 옵션을 하나의 간결한 라우트 시그니처와 유사한 형태로 정의할 수 있습니다.

<a name="arguments"></a>
<!-- ### Arguments -->
### Arguments

<!-- All user supplied arguments and options are wrapped in curly braces. In the following example, the command defines one required argument: `user`: -->
명령어에서 사용자 입력값(인수, 옵션)을 정의할 때는 중괄호로 감싸 표현합니다. 아래 예시에서는 필수 인수인 `user` 하나가 정의되어 있습니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```

<!-- You may also make arguments optional or define default values for arguments: -->
인수를 선택적으로 만들거나, 기본값을 정해줄 수도 있습니다.

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
옵션도 인수처럼 사용자 입력값의 일종입니다. 옵션은 커맨드라인에서 두 개의 하이픈(`--`)으로 시작합니다. 옵션에는 값을 받는 옵션과 받지 않는 옵션(불리언 "스위치")이 있습니다. 불리언 "스위치" 옵션의 예는 다음과 같습니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```

<!-- In this example, the `--queue` switch may be specified when calling the Artisan command. If the `--queue` switch is passed, the value of the option will be `true`. Otherwise, the value will be `false`: -->
이 예시에서는 Artisan 명령어를 실행할 때 `--queue` 스위치를 지정할 수 있습니다. `--queue` 스위치를 지정하면 옵션의 값은 `true`가 되고, 지정하지 않으면 `false`가 됩니다.

```shell
php artisan mail:send 1 --queue
```

<a name="options-with-values"></a>
<!-- #### Options With Values -->
#### Options With Values

<!-- Next, let's take a look at an option that expects a value. If the user must specify a value for an option, you should suffix the option name with a `=` sign: -->
값을 기대하는 옵션의 경우, 옵션 이름 뒤에 `=` 기호를 추가해야 합니다. 아래 예시처럼 사용할 수 있습니다.

```
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```

<!-- In this example, the user may pass a value for the option like so. If the option is not specified when invoking the command, its value will be `null`: -->
이 경우, 사용자는 아래와 같이 옵션에 값을 넘길 수 있고, 옵션이 생략되면 값은 `null`이 됩니다.

```shell
php artisan mail:send 1 --queue=default
```

<!-- You may assign default values to options by specifying the default value after the option name. If no option value is passed by the user, the default value will be used: -->
옵션에 기본값을 정해주고 싶다면, 옵션 이름 뒤에 기본값을 추가합니다. 사용자가 값을 입력하지 않으면 기본값이 적용됩니다.

```
'mail:send {user} {--queue=default}'
```

<a name="option-shortcuts"></a>
<!-- #### Option Shortcuts -->
#### Option Shortcuts

<!-- To assign a shortcut when defining an option, you may specify it before the option name and use the `|` character as a delimiter to separate the shortcut from the full option name: -->
옵션에 단축키를 지정하고 싶다면, 옵션 이름 앞에 단축키를 적고 `|` 문자를 구분자로 사용해 단축키와 전체 옵션 이름을 구분할 수 있습니다.

```
'mail:send {user} {--Q|queue}'
```

<!-- When invoking the command on your terminal, option shortcuts should be prefixed with a single hyphen: -->
명령어를 터미널에서 실행할 때는 단축키 옵션에 한 개의 하이픈을 붙여 씁니다.

```shell
php artisan mail:send 1 -Q
```

<a name="input-arrays"></a>
<!-- ### Input Arrays -->
### Input Arrays

<!-- If you would like to define arguments or options to expect multiple input values, you may use the `*` character. First, let's take a look at an example that specifies such an argument: -->
인수 또는 옵션에서 여러 개의 값을 받을 수 있도록 하려면 `*` 기호를 사용할 수 있습니다. 먼저 인수에 적용한 예를 살펴봅니다.

```
'mail:send {user*}'
```

<!-- When calling this method, the `user` arguments may be passed in order to the command line. For example, the following command will set the value of `user` to an array with `1` and `2` as its values: -->
이렇게 정의하면 명령줄에서 `user` 인수를 순서대로 입력할 수 있습니다. 예를 들면 아래 명령은 `user` 값을 `1`과 `2`를 원소로 가지는 배열로 설정합니다.

```shell
php artisan mail:send 1 2
```

<!-- This `*` character can be combined with an optional argument definition to allow zero or more instances of an argument: -->
`*` 문자를 선택적 인수와 조합하면 인수를 0개 이상 받아들일 수도 있습니다.

```
'mail:send {user?*}'
```

<a name="option-arrays"></a>
<!-- #### Option Arrays -->
#### Option Arrays

<!-- When defining an option that expects multiple input values, each option value passed to the command should be prefixed with the option name: -->
여러 입력값을 받는 옵션을 정의할 때는 각각의 옵션 값 앞에 옵션 이름을 붙여 사용해야 합니다.

```
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
인수 또는 옵션에 설명을 추가하려면, 이름 뒤에 콜론과 설명을 적어 구분할 수 있습니다. 좀 더 명확한 정의가 필요하다면 여러 줄에 걸쳐 나누어 쓸 수도 있습니다.

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

<a name="command-io"></a>
<!-- ## Command I/O -->
## Command I/O

<a name="retrieving-input"></a>
<!-- ### Retrieving Input -->
### Retrieving Input

<!-- While your command is executing, you will likely need to access the values for the arguments and options accepted by your command. To do so, you may use the `argument` and `option` methods. If an argument or option does not exist, `null` will be returned: -->
명령어가 실행되는 동안, 전달받은 인수와 옵션의 값을 가져와야 할 때가 있습니다. 이때는 `argument` 및 `option` 메서드를 사용할 수 있습니다. 인수 또는 옵션이 존재하지 않으면 `null`이 반환됩니다.

```
/**
 * Execute the console command.
 *
 * @return int
 */
public function handle()
{
    $userId = $this->argument('user');

    //
}
```

<!-- If you need to retrieve all of the arguments as an `array`, call the `arguments` method: -->
인수 전체를 `array`로 한 번에 가져오려면 `arguments` 메서드를 사용합니다.

```
$arguments = $this->arguments();
```

<!-- Options may be retrieved just as easily as arguments using the `option` method. To retrieve all of the options as an array, call the `options` method: -->
옵션도 마찬가지로, `option` 메서드로 개별 옵션을, `options` 메서드로 전체 옵션 배열을 받아올 수 있습니다.

```
// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
```

<a name="prompting-for-input"></a>
<!-- ### Prompting For Input -->
### Prompting For Input

<!-- In addition to displaying output, you may also ask the user to provide input during the execution of your command. The `ask` method will prompt the user with the given question, accept their input, and then return the user's input back to your command: -->
출력만 하는 것 외에도, 명령어 실행 도중 사용자에게 입력을 요청할 수도 있습니다. `ask` 메서드는 사용자가 입력한 값을 받아 반환하며, 원하는 질문을 함께 표시할 수 있습니다.

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $name = $this->ask('What is your name?');
}
```

<!-- The `secret` method is similar to `ask`, but the user's input will not be visible to them as they type in the console. This method is useful when asking for sensitive information such as passwords: -->
`secret` 메서드는 `ask`와 비슷하지만, 입력값이 콘솔에 노출되지 않습니다. 비밀번호 등 민감한 정보를 받을 때 유용합니다.

```
$password = $this->secret('What is the password?');
```

<a name="asking-for-confirmation"></a>
<!-- #### Asking For Confirmation -->
#### Asking For Confirmation

<!-- If you need to ask the user for a simple "yes or no" confirmation, you may use the `confirm` method. By default, this method will return `false`. However, if the user enters `y` or `yes` in response to the prompt, the method will return `true`. -->
사용자에게 간단하게 "예/아니오"로 확인을 받고 싶다면 `confirm` 메서드를 사용할 수 있습니다. 이 메서드는 기본적으로 `false`를 반환하지만, 사용자가 프롬프트에서 `y` 또는 `yes`를 입력하면 `true`를 반환합니다.

```
if ($this->confirm('Do you wish to continue?')) {
    //
}
```

<!-- If necessary, you may specify that the confirmation prompt should return `true` by default by passing `true` as the second argument to the `confirm` method: -->
필요하다면 `confirm` 메서드의 두 번째 인자로 `true`를 넘겨, 확인 프롬프트가 기본적으로 `true`를 반환하도록 지정할 수도 있습니다.

```
if ($this->confirm('Do you wish to continue?', true)) {
    //
}
```

<a name="auto-completion"></a>
<!-- #### Auto-Completion -->
#### Auto-Completion

<!-- The `anticipate` method can be used to provide auto-completion for possible choices. The user can still provide any answer, regardless of the auto-completion hints: -->
사용자 입력에 자동완성 힌트를 제공하고 싶다면 `anticipate` 메서드를 사용할 수 있습니다. 자동완성 힌트가 있어도 사용자는 임의의 값을 입력할 수 있습니다.

```
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```

<!-- Alternatively, you may pass a closure as the second argument to the `anticipate` method. The closure will be called each time the user types an input character. The closure should accept a string parameter containing the user's input so far, and return an array of options for auto-completion: -->
혹은 `anticipate` 메서드의 두 번째 인자로 클로저를 넘기면, 사용자가 문자를 입력할 때마다 해당 클로저가 호출됩니다. 클로저는 지금까지 입력한 내용을 받아, 자동완성 후보를 배열로 반환해야 합니다.

```
$name = $this->anticipate('What is your address?', function ($input) {
    // Return auto-completion options...
});
```

<a name="multiple-choice-questions"></a>
<!-- #### Multiple Choice Questions -->
#### Multiple Choice Questions

<!-- If you need to give the user a predefined set of choices when asking a question, you may use the `choice` method. You may set the array index of the default value to be returned if no option is chosen by passing the index as the third argument to the method: -->
사용자에게 미리 정해진 값 중에서 선택하게 하려면 `choice` 메서드를 사용할 수 있습니다. 선택지가 없으면 반환할 기본값의 배열 인덱스를 세 번째 인자로 넘길 수 있습니다.

```
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```

<!-- In addition, the `choice` method accepts optional fourth and fifth arguments for determining the maximum number of attempts to select a valid response and whether multiple selections are permitted: -->
또한 `choice` 메서드는 유효한 응답을 선택할 수 있는 최대 시도 횟수와 다중 선택 허용 여부를 결정하는 선택적 네 번째, 다섯 번째 인자를 받습니다.

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
콘솔로 출력 메시지를 보낼 때는 `line`, `info`, `comment`, `question`, `warn`, `error` 등의 메서드를 사용할 수 있습니다. 이 메서드들은 각각 목적에 맞는 ANSI 컬러가 적용됩니다. 예를 들어, 사용자에게 일반 정보를 표시할 때는 `info` 메서드를 쓰면 콘솔에 녹색 텍스트로 출력됩니다.

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    // ...

    $this->info('The command was successful!');
}
```

<!-- To display an error message, use the `error` method. Error message text is typically displayed in red: -->
에러 메시지는 `error` 메서드를 사용하면 됩니다. 에러 메시지는 보통 빨간색으로 표시됩니다.

```
$this->error('Something went wrong!');
```

<!-- You may use the `line` method to display plain, uncolored text: -->
색이 없는 평범한 텍스트를 출력하려면 `line` 메서드를 사용할 수 있습니다.

```
$this->line('Display this on the screen');
```

<!-- You may use the `newLine` method to display a blank line: -->
빈 줄을 출력하려면 `newLine` 메서드를 사용하면 됩니다.

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
`table` 메서드를 사용하면 여러 행/열로 구성된 데이터를 보기 좋게 자동으로 정렬해서 출력할 수 있습니다. 컬럼 이름과 테이블 데이터를 넘기기만 하면, Laravel이 알맞은 크기로 테이블을 그려줍니다.

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
실행 시간이 오래 걸리는 작업에는, 사용자가 진행 상태를 시각적으로 알 수 있도록 진행바를 표시할 수 있습니다. `withProgressBar` 메서드를 사용하면, 반복 처리되는 이터러블 입력값 수만큼 진행바를 표시할 수 있습니다.

```
use App\Models\User;

$users = $this->withProgressBar(User::all(), function ($user) {
    $this->performTask($user);
});
```

<!-- Sometimes, you may need more manual control over how a progress bar is advanced. First, define the total number of steps the process will iterate through. Then, advance the progress bar after processing each item: -->
진행바의 이동을 수동으로 제어하려면, 총 스텝 수를 미리 지정하고 각 아이템 처리 뒤 명시적으로 진행바를 이동시킬 수 있습니다.

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
> 더 다양한 옵션이 궁금하다면 [Symfony Progress Bar component documentation](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 참고하세요.

<a name="registering-commands"></a>
<!-- ## Registering Commands -->
## Registering Commands

<!-- All of your console commands are registered within your application's `App\Console\Kernel` class, which is your application's "console kernel". Within the `commands` method of this class, you will see a call to the kernel's `load` method. The `load` method will scan the `app/Console/Commands` directory and automatically register each command it contains with Artisan. You are even free to make additional calls to the `load` method to scan other directories for Artisan commands: -->
모든 콘솔 명령어는 애플리케이션의 "콘솔 커널"인 `App\Console\Kernel` 클래스 안에서 등록됩니다. 이 클래스의 `commands` 메서드에서는 `load` 메서드를 호출하고 있습니다. `load` 메서드는 `app/Console/Commands` 디렉터리를 스캔하여 그 안의 모든 명령어를 Artisan에 자동 등록합니다. 필요하다면 `load` 메서드를 추가로 호출해 다른 디렉터리의 명령어도 Artisan에 등록할 수 있습니다.

```
/**
 * Register the commands for the application.
 *
 * @return void
 */
protected function commands()
{
    $this->load(__DIR__.'/Commands');
    $this->load(__DIR__.'/../Domain/Orders/Commands');

    // ...
}
```

<!-- If necessary, you may manually register commands by adding the command's class name to a `$commands` property within your `App\Console\Kernel` class. If this property is not already defined on your kernel, you should define it manually. When Artisan boots, all the commands listed in this property will be resolved by the [service container](/docs/9.x/container) and registered with Artisan: -->
필요에 따라 직접 명령어를 수동 등록하려면, `App\Console\Kernel` 클래스의 `$commands` 프로퍼티에 명령어 클래스 이름을 추가하면 됩니다. 해당 프로퍼티가 정의되어 있지 않다면 직접 추가해주십시오. Artisan이 부팅되면 이 배열에 명시된 명령어들이 [service container](/docs/9.x/container)를 통해 자동으로 해석(resolved)되어 Artisan에 등록됩니다.

```
protected $commands = [
    Commands\SendEmails::class
];
```

<a name="programmatically-executing-commands"></a>
<!-- ## Programmatically Executing Commands -->
## Programmatically Executing Commands

<!-- Sometimes you may wish to execute an Artisan command outside of the CLI. For example, you may wish to execute an Artisan command from a route or controller. You may use the `call` method on the `Artisan` facade to accomplish this. The `call` method accepts either the command's signature name or class name as its first argument, and an array of command parameters as the second argument. The exit code will be returned: -->
CLI 환경이 아닌 곳에서도 Artisan 명령어를 실행하고 싶을 때가 있습니다. 예를 들어, 라우트나 컨트롤러에서 Artisan 명령어를 호출하고 싶을 때는 `Artisan` 파사드의 `call` 메서드를 사용하면 됩니다. `call` 메서드는 첫 번째 인자로 "명령어 시그니처 이름" 또는 "클래스명", 두 번째 인자로 명령어 파라미터 배열을 받으며, 종료 코드를 반환합니다.

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

<!-- Alternatively, you may pass the entire Artisan command to the `call` method as a string: -->
명령 전체를 문자열로 만들어 `call` 메서드에 그대로 넘길 수도 있습니다.

```
Artisan::call('mail:send 1 --queue=default');
```

<a name="passing-array-values"></a>
<!-- #### Passing Array Values -->
#### Passing Array Values

<!-- If your command defines an option that accepts an array, you may pass an array of values to that option: -->
명령어에서 배열 입력값을 받도록 옵션을 설정했다면, 해당 옵션에 값의 배열을 그대로 넘기면 됩니다.

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
`migrate:refresh` 명령어의 `--force` 플래그처럼 문자열 값을 받지 않는 옵션에 값을 지정하고 싶다면, 옵션의 값으로 `true` 또는 `false`를 넘기면 됩니다.

```
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```

<a name="queueing-artisan-commands"></a>
<!-- #### Queueing Artisan Commands -->
#### Queueing Artisan Commands

<!-- Using the `queue` method on the `Artisan` facade, you may even queue Artisan commands so they are processed in the background by your [queue workers](/docs/9.x/queues). Before using this method, make sure you have configured your queue and are running a queue listener: -->
`Artisan` 파사드의 `queue` 메서드를 사용하면, Artisan 명령어도 큐잉하여 백그라운드에서 [queue workers](/docs/9.x/queues)가 처리할 수 있게 만들 수 있습니다. 이 기능을 사용하기 전에 큐 설정을 완료하고 큐 리스너도 실행 중이어야 합니다.

```
use Illuminate\Support\Facades\Artisan;

Route::post('/user/{user}/mail', function ($user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    //
});
```

<!-- Using the `onConnection` and `onQueue` methods, you may specify the connection or queue the Artisan command should be dispatched to: -->
`onConnection`과 `onQueue` 메서드를 이용하면, Artisan 명령어가 특정 커넥션이나 큐로 디스패치되도록 지정할 수 있습니다.

```
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```

<a name="calling-commands-from-other-commands"></a>
<!-- ### Calling Commands From Other Commands -->
### Calling Commands From Other Commands

<!-- Sometimes you may wish to call other commands from an existing Artisan command. You may do so using the `call` method. This `call` method accepts the command name and an array of command arguments / options: -->
기존 Artisan 명령어에서 다른 명령어를 호출하고 싶을 때는 `call` 메서드를 사용할 수 있습니다. 이 `call` 메서드는 명령어 이름과 인수/옵션 배열을 받습니다.

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    //
}
```

<!-- If you would like to call another console command and suppress all of its output, you may use the `callSilently` method. The `callSilently` method has the same signature as the `call` method: -->
다른 콘솔 명령어를 호출하면서, 그 명령어의 출력을 모두 숨기고 싶다면 `callSilently` 메서드를 사용하세요. `callSilently` 메서드는 `call` 메서드와 동일한 시그니처를 가집니다.

```
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```

<a name="signal-handling"></a>
<!-- ## Signal Handling -->
## Signal Handling

<!-- As you may know, operating systems allow signals to be sent to running processes. For example, the `SIGTERM` signal is how operating systems ask a program to terminate. If you wish to listen for signals in your Artisan console commands and execute code when they occur, you may use the `trap` method: -->
운영체제(OS)는 실행중인 프로세스에 신호(signal)를 보낼 수 있습니다. 예를 들어 `SIGTERM` 신호를 보내 프로세스가 종료되도록 할 수 있습니다. Artisan 콘솔 명령어에서 이런 신호를 감지하여 특정 코드가 실행되게 하려면 `trap` 메서드를 이용하면 됩니다.

```
/**
 * Execute the console command.
 *
 * @return mixed
 */
public function handle()
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```

<!-- To listen for multiple signals at once, you may provide an array of signals to the `trap` method: -->
한 번에 여러 신호를 감지하고 싶다면, 신호 배열을 `trap` 메서드에 넘길 수 있습니다.

```
$this->trap([SIGTERM, SIGQUIT], function ($signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```

<a name="stub-customization"></a>
<!-- ## Stub Customization -->
## Stub Customization

<!-- The Artisan console's `make` commands are used to create a variety of classes, such as controllers, jobs, migrations, and tests. These classes are generated using "stub" files that are populated with values based on your input. However, you may want to make small changes to files generated by Artisan. To accomplish this, you may use the `stub:publish` command to publish the most common stubs to your application so that you can customize them: -->
Artisan 콘솔의 `make` 계열 명령어는 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성합니다. 이 클래스들은 "스텁(stub)" 파일을 기반으로, 입력값에 따라 일부 값이 자동으로 치환되어 생성됩니다. 만약 Artisan이 생성하는 파일의 형태를 약간 수정하고 싶다면, `stub:publish` 명령어로 가장 많이 쓰이는 스텁 파일들을 애플리케이션에 퍼블리시하여 직접 원하는 대로 수정할 수 있습니다.

```shell
php artisan stub:publish
```

<!-- The published stubs will be located within a `stubs` directory in the root of your application. Any changes you make to these stubs will be reflected when you generate their corresponding classes using Artisan's `make` commands. -->
퍼블리시된 스텁 파일은 애플리케이션의 루트 `stubs` 디렉터리에 위치합니다. 이 파일들을 변경하면 해당 클래스 유형을 Artisan의 `make` 명령어로 생성할 때 변경점이 반영됩니다.

<a name="events"></a>
<!-- ## Events -->
## Events

<!-- Artisan dispatches three events when running commands: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, and `Illuminate\Console\Events\CommandFinished`. The `ArtisanStarting` event is dispatched immediately when Artisan starts running. Next, the `CommandStarting` event is dispatched immediately before a command runs. Finally, the `CommandFinished` event is dispatched once a command finishes executing. -->
Artisan 명령어를 실행할 때 세 가지 이벤트가 발생합니다. `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, `Illuminate\Console\Events\CommandFinished`입니다. `ArtisanStarting` 이벤트는 Artisan 실행이 시작될 때 즉시 발생하고, `CommandStarting` 이벤트는 각 명령어가 실행되기 직전에, `CommandFinished` 이벤트는 명령어 실행이 완료된 뒤에 발생합니다.
