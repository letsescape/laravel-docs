<!-- # Laravel Envoy -->
# Laravel Envoy

- [Introduction](#introduction)
- [Installation](#installation)
- [Writing Tasks](#writing-tasks)
    - [Defining Tasks](#defining-tasks)
    - [Multiple Servers](#multiple-servers)
    - [Setup](#setup)
    - [Variables](#variables)
    - [Stories](#stories)
    - [Hooks](#completion-hooks)
- [Running Tasks](#running-tasks)
    - [Confirming Task Execution](#confirming-task-execution)
- [Notifications](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Envoy](https://github.com/laravel/envoy) is a tool for executing common tasks you run on your remote servers. Using [Blade](/docs/11.x/blade) style syntax, you can easily setup tasks for deployment, Artisan commands, and more. Currently, Envoy only supports the Mac and Linux operating systems. However, Windows support is achievable using [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 반복적으로 실행하는 태스크를 간편하게 처리하는 도구입니다. [Blade](/docs/11.x/blade) 스타일의 문법을 사용해, 배포 작업, Artisan 명령 실행 등 다양한 작업을 손쉽게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만 공식 지원합니다. 하지만 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 활용하면 Windows 환경에서도 사용이 가능합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Envoy into your project using the Composer package manager: -->
먼저, Composer 패키지 매니저를 이용해 프로젝트에 Envoy를 설치합니다:

```shell
composer require laravel/envoy --dev
```

<!-- Once Envoy has been installed, the Envoy binary will be available in your application's `vendor/bin` directory: -->
Envoy 설치 이후에는, Envoy 실행 파일이 애플리케이션의 `vendor/bin` 디렉토리에 위치하게 됩니다:

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
<!-- ## Writing Tasks -->
## Writing Tasks

<a name="defining-tasks"></a>
<!-- ### Defining Tasks -->
### Defining Tasks

<!-- Tasks are the basic building block of Envoy. Tasks define the shell commands that should execute on your remote servers when the task is invoked. For example, you might define a task that executes the `php artisan queue:restart` command on all of your application's queue worker servers. -->
태스크(task)는 Envoy의 가장 기본적인 구성 단위입니다. 태스크는 태스크가 실행될 때 원격 서버에서 실행되어야 할 쉘 명령어들을 정의합니다. 예를 들어, 모든 큐 워커 서버에서 `php artisan queue:restart` 명령어를 실행하는 태스크를 만들 수 있습니다.

<!-- All of your Envoy tasks should be defined in an `Envoy.blade.php` file at the root of your application. Here's an example to get you started: -->
모든 Envoy 태스크는 애플리케이션 루트에 위치한 `Envoy.blade.php` 파일에 정의해야 합니다. 아래는 기본적인 예시입니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

<!-- As you can see, an array of `@servers` is defined at the top of the file, allowing you to reference these servers via the `on` option of your task declarations. The `@servers` declaration should always be placed on a single line. Within your `@task` declarations, you should place the shell commands that should execute on your servers when the task is invoked. -->
위와 같이, 파일 맨 위에서 `@servers` 배열을 정의하여 각각의 서버를 이름으로 참조할 수 있도록 합니다. 태스크 선언 시 `on` 옵션을 통해 참조한 서버를 지정하며, 해당 태스크가 실행될 서버를 명확하게 지정할 수 있습니다. 참고로, `@servers` 선언은 항상 한 줄로 작성해야 합니다. 각 태스크(`@task`) 블록 내부에는 실행될 쉘 명령을 기재합니다.

<a name="local-tasks"></a>
<!-- #### Local Tasks -->
#### Local Tasks

<!-- You can force a script to run on your local computer by specifying the server's IP address as `127.0.0.1`: -->
스크립트를 내 컴퓨터(로컬)에서 실행하고 싶다면, 서버 IP를 `127.0.0.1`로 지정하면 됩니다:

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
<!-- #### Importing Envoy Tasks -->
#### Importing Envoy Tasks

<!-- Using the `@import` directive, you may import other Envoy files so their stories and tasks are added to yours. After the files have been imported, you may execute the tasks they contain as if they were defined in your own Envoy file: -->
`@import` 지시어를 사용하면, 다른 Envoy 파일을 불러와 해당 파일의 스토리(story) 및 태스크를 내 Envoy 파일에서 사용할 수 있습니다. 이렇게 가져온 태스크는 직접 정의한 것처럼 동일하게 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
<!-- ### Multiple Servers -->
### Multiple Servers

<!-- Envoy allows you to easily run a task across multiple servers. First, add additional servers to your `@servers` declaration. Each server should be assigned a unique name. Once you have defined your additional servers you may list each of the servers in the task's `on` array: -->
Envoy를 사용하면 하나의 태스크를 여러 서버에 걸쳐서 동시에 실행할 수 있습니다. 먼저, `@servers` 선언에 서버를 추가하고, 각 서버에 고유한 이름을 지정합니다. 이후 태스크의 `on` 배열에 실행될 서버의 이름을 나열합니다:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="parallel-execution"></a>
<!-- #### Parallel Execution -->
#### Parallel Execution

<!-- By default, tasks will be executed on each server serially. In other words, a task will finish running on the first server before proceeding to execute on the second server. If you would like to run a task across multiple servers in parallel, add the `parallel` option to your task declaration: -->
기본적으로 태스크는 지정된 서버에서 순차적으로(직렬로) 실행됩니다. 즉, 첫 번째 서버의 태스크가 끝나야 다음 서버에서 실행이 시작됩니다. 만약 복수의 서버에서 태스크를 병렬로 실행하고 싶다면, 태스크 선언에 `parallel` 옵션을 추가하십시오:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask
```

<a name="setup"></a>
<!-- ### Setup -->
### Setup

<!-- Sometimes, you may need to execute arbitrary PHP code before running your Envoy tasks. You may use the `@setup` directive to define a block of PHP code that should execute before your tasks: -->
경우에 따라, Envoy 태스크가 실행되기 전에 임의의 PHP 코드를 실행해야 할 수 있습니다. 이럴 때는 `@setup` 지시어를 사용하면 됩니다. 해당 블록 내부의 코드는 태스크 실행 전에 실행됩니다:

```php
@setup
    $now = new DateTime;
@endsetup
```

<!-- If you need to require other PHP files before your task is executed, you may use the `@include` directive at the top of your `Envoy.blade.php` file: -->
태스크 실행 전에 다른 PHP 파일이 필요하다면, `Envoy.blade.php` 파일 맨 위에 `@include` 지시어를 추가해 파일을 불러올 수 있습니다:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
<!-- ### Variables -->
### Variables

<!-- If needed, you may pass arguments to Envoy tasks by specifying them on the command line when invoking Envoy: -->
필요하다면, Envoy 태스크를 호출할 때 커맨드라인에서 인수를 넘길 수 있습니다:

```shell
php vendor/bin/envoy run deploy --branch=master
```

<!-- You may access the options within your tasks using Blade's "echo" syntax. You may also define Blade `if` statements and loops within your tasks. For example, let's verify the presence of the `$branch` variable before executing the `git pull` command: -->
이렇게 지정한 옵션 값은 Blade의 "echo" 문법을 이용해 태스크 내에서 사용할 수 있습니다. 또한, Blade의 `if`문이나 반복문도 자유롭게 사용할 수 있습니다. 아래는 `$branch` 변수가 있을 때에만 `git pull` 명령을 실행하는 코드입니다:

```blade
@servers(['web' => ['user@192.168.1.1']])

@task('deploy', ['on' => 'web'])
    cd /home/user/example.com

    @if ($branch)
        git pull origin {{ $branch }}
    @endif

    php artisan migrate --force
@endtask
```

<a name="stories"></a>
<!-- ### Stories -->
### Stories

<!-- Stories group a set of tasks under a single, convenient name. For instance, a `deploy` story may run the `update-code` and `install-dependencies` tasks by listing the task names within its definition: -->
스토리(story)는 여러 개의 태스크를 하나의 이름으로 묶어 관리할 수 있게 해줍니다. 예를 들어, `deploy`라는 스토리에 `update-code`와 `install-dependencies`라는 태스크를 등록하면, 한 번의 명령만으로 여러 태스크를 연속 실행할 수 있습니다:

```blade
@servers(['web' => ['user@192.168.1.1']])

@story('deploy')
    update-code
    install-dependencies
@endstory

@task('update-code')
    cd /home/user/example.com
    git pull origin master
@endtask

@task('install-dependencies')
    cd /home/user/example.com
    composer install
@endtask
```

<!-- Once the story has been written, you may invoke it in the same way you would invoke a task: -->
스토리를 작성한 뒤에는, 일반 태스크와 동일하게 아래와 같이 실행할 수 있습니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
<!-- ### Hooks -->
### Hooks

<!-- When tasks and stories run, a number of hooks are executed. The hook types supported by Envoy are `@before`, `@after`, `@error`, `@success`, and `@finished`. All of the code in these hooks is interpreted as PHP and executed locally, not on the remote servers that your tasks interact with. -->
태스크 및 스토리가 실행될 때 여러 종류의 후크(hook)가 함께 동작합니다. Envoy가 지원하는 후크 종류에는 `@before`, `@after`, `@error`, `@success`, `@finished`가 있습니다. 이 후크 블록 내의 코드는 모두 PHP로 해석되어, 원격 서버가 아닌 로컬에서 실행됩니다.

<!-- You may define as many of each of these hooks as you like. They will be executed in the order that they appear in your Envoy script. -->
이러한 각 후크는 원하는 만큼 여러 번 사용할 수 있으며, Envoy 스크립트에서 나타나는 순서대로 실행됩니다.

<a name="hook-before"></a>
<!-- #### `@before` -->
#### `@before`

<!-- Before each task execution, all of the `@before` hooks registered in your Envoy script will execute. The `@before` hooks receive the name of the task that will be executed: -->
각 태스크 실행 전에 Envoy 스크립트에 등록된 모든 `@before` 후크가 실행됩니다. `@before` 후크는 실행될 태스크의 이름을 받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
<!-- #### `@after` -->
#### `@after`

<!-- After each task execution, all of the `@after` hooks registered in your Envoy script will execute. The `@after` hooks receive the name of the task that was executed: -->
태스크 실행이 끝난 후에는, 등록된 모든 `@after` 후크가 실행됩니다. `@after` 후크는 실행된 태스크의 이름을 받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
<!-- #### `@error` -->
#### `@error`

<!-- After every task failure (exits with a status code greater than `0`), all of the `@error` hooks registered in your Envoy script will execute. The `@error` hooks receive the name of the task that was executed: -->
태스크가 실패(상태 코드가 `0`보다 큰 값으로 종료)하면, 등록된 모든 `@error` 후크가 실행됩니다. `@error` 후크는 실행된 태스크의 이름을 받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
<!-- #### `@success` -->
#### `@success`

<!-- If all tasks have executed without errors, all of the `@success` hooks registered in your Envoy script will execute: -->
모든 태스크가 에러 없이 정상적으로 실행되면, 등록된 모든 `@success` 후크가 실행됩니다:

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
<!-- #### `@finished` -->
#### `@finished`

<!-- After all tasks have been executed (regardless of exit status), all of the `@finished` hooks will be executed. The `@finished` hooks receive the status code of the completed task, which may be `null` or an `integer` greater than or equal to `0`: -->
모든 태스크가 실행된 후(성공/실패와 관계없이), 모든 `@finished` 후크가 실행됩니다. `@finished` 후크에서는 완료된 태스크의 상태 코드 값을 받아올 수 있으며, 이 값은 `null`이거나 `0` 이상의 `integer`일 수 있습니다:

```blade
@finished
    if ($exitCode > 0) {
        // There were errors in one of the tasks...
    }
@endfinished
```

<a name="running-tasks"></a>
<!-- ## Running Tasks -->
## Running Tasks

<!-- To run a task or story that is defined in your application's `Envoy.blade.php` file, execute Envoy's `run` command, passing the name of the task or story you would like to execute. Envoy will execute the task and display the output from your remote servers as the task is running: -->
애플리케이션의 `Envoy.blade.php` 파일에 정의된 태스크 또는 스토리를 실행하려면, Envoy의 `run` 명령에 실행할 태스크나 스토리의 이름을 인수로 전달하면 됩니다. Envoy는 해당 작업을 실행하고, 실행 중에 원격 서버에서 전달되는 출력을 실시간으로 보여줍니다:

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
<!-- ### Confirming Task Execution -->
### Confirming Task Execution

<!-- If you would like to be prompted for confirmation before running a given task on your servers, you should add the `confirm` directive to your task declaration. This option is particularly useful for destructive operations: -->
지정한 태스크를 서버에서 실행하기 전에 실행 여부를 한번 더 묻는(확인하는) 기능이 필요하다면, 태스크 선언에 `confirm` 지시어를 추가하면 됩니다. 이 옵션은 어떤 작업이 파괴적일(즉, 복구가 어려운 변경이 발생할) 때 매우 유용합니다:

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a name="notifications"></a>
<!-- ## Notifications -->
## Notifications

<a name="slack"></a>
<!-- ### Slack -->
### Slack

<!-- Envoy supports sending notifications to [Slack](https://slack.com) after each task is executed. The `@slack` directive accepts a Slack hook URL and a channel / user name. You may retrieve your webhook URL by creating an "Incoming WebHooks" integration in your Slack control panel. -->
Envoy는 각 태스크 실행 후 [Slack](https://slack.com)으로 알림을 전송하는 기능을 지원합니다. `@slack` 지시어에는 Slack의 웹후크(webhook) URL과 채널/사용자 이름을 전달해야 합니다. 웹후크 URL은 Slack 관리 화면에서 "Incoming WebHooks" 통합을 생성하여 얻을 수 있습니다.

<!-- You should pass the entire webhook URL as the first argument given to the `@slack` directive. The second argument given to the `@slack` directive should be a channel name (`#channel`) or a user name (`@user`): -->
`@slack` 지시어의 첫 번째 인자로 전체 웹후크 URL을 전달해야 합니다. `@slack` 지시어의 두 번째 인자로는 채널 이름(`#channel`) 또는 사용자 이름(`@user`)을 전달해야 합니다:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

<!-- By default, Envoy notifications will send a message to the notification channel describing the task that was executed. However, you may overwrite this message with your own custom message by passing a third argument to the `@slack` directive: -->
기본적으로 Envoy 알림은 실행된 태스크 정보를 담아 채널로 전송합니다. 하지만, `@slack` 지시어에 세 번째 인자로 직접 메시지를 지정하면, 자신만의 맞춤 메시지로 덮어쓸 수도 있습니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
<!-- ### Discord -->
### Discord

<!-- Envoy also supports sending notifications to [Discord](https://discord.com) after each task is executed. The `@discord` directive accepts a Discord hook URL and a message. You may retrieve your webhook URL by creating a "Webhook" in your Server Settings and choosing which channel the webhook should post to. You should pass the entire Webhook URL into the `@discord` directive: -->
Envoy는 [Discord](https://discord.com)에도 태스크 실행 후 알림을 보낼 수 있습니다. `@discord` 지시어는 Discord 웹후크 URL과 메시지를 받습니다. 웹후크 URL은 디스코드 서버의 "Webhook"을 생성해서 얻을 수 있습니다. 해당 URL을 `@discord` 지시어에 그대로 전달하면 됩니다:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
<!-- ### Telegram -->
### Telegram

<!-- Envoy also supports sending notifications to [Telegram](https://telegram.org) after each task is executed. The `@telegram` directive accepts a Telegram Bot ID and a Chat ID. You may retrieve your Bot ID by creating a new bot using [BotFather](https://t.me/botfather). You can retrieve a valid Chat ID using [@username_to_id_bot](https://t.me/username_to_id_bot). You should pass the entire Bot ID and Chat ID into the `@telegram` directive: -->
Envoy는 [Telegram](https://telegram.org) 알림도 지원합니다. `@telegram` 지시어는 텔레그램 봇 ID, 채팅 ID를 인자로 받습니다. 봇 ID는 [BotFather](https://t.me/botfather)로 새 봇을 만들어 얻을 수 있고, 채팅 ID는 [@username_to_id_bot](https://t.me/username_to_id_bot) 등으로 확인할 수 있습니다. 두 값을 `@telegram` 지시어에 전달하면 사용 가능합니다:

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
<!-- ### Microsoft Teams -->
### Microsoft Teams

<!-- Envoy also supports sending notifications to [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) after each task is executed. The `@microsoftTeams` directive accepts a Teams Webhook (required), a message, theme color (success, info, warning, error), and an array of options. You may retrieve your Teams Webhook by creating a new [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook). The Teams API has many other attributes to customize your message box like title, summary, and sections. You can find more information on the [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message). You should pass the entire Webhook URL into the `@microsoftTeams` directive: -->
Envoy는 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) 알림도 지원합니다. `@microsoftTeams` 지시어에는 Teams 웹후크(필수), 메시지, 테마 색상(success, info, warning, error), 옵션 배열을 인자로 전달할 수 있습니다. Teams 웹후크 URL은 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 생성해서 가져야 합니다. Teams API에서는 메시지 박스 타이틀, 요약, 섹션 등 다양한 속성도 커스터마이즈할 수 있습니다. 자세한 내용은 [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)를 참고하십시오. 웹후크 URL을 `@microsoftTeams` 지시어에 입력하면 됩니다:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```
