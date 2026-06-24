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

<!-- [Laravel Envoy](https://github.com/laravel/envoy) is a tool for executing common tasks you run on your remote servers. Using [Blade](/docs/9.x/blade) style syntax, you can easily setup tasks for deployment, Artisan commands, and more. Currently, Envoy only supports the Mac and Linux operating systems. However, Windows support is achievable using [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10). -->
[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 자주 실행하는 작업들을 손쉽게 실행할 수 있게 해주는 도구입니다. [Blade](/docs/9.x/blade) 스타일의 문법을 사용하여 배포, Artisan 명령어 실행 등 여러 작업을 쉽고 간단하게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만 공식적으로 지원합니다. 하지만 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용하면 Windows 환경에서도 사용할 수 있습니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Envoy into your project using the Composer package manager: -->
먼저, Composer 패키지 관리자를 이용해 프로젝트에 Envoy를 설치합니다.

```shell
composer require laravel/envoy --dev
```

<!-- Once Envoy has been installed, the Envoy binary will be available in your application's `vendor/bin` directory: -->
Envoy 설치가 완료되면, Envoy 실행 파일이 애플리케이션의 `vendor/bin` 디렉터리에 생성됩니다.

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
작업(Task)은 Envoy의 기본 구성 단위입니다. 작업은 특정 시점에 원격 서버에서 실행되어야 하는 쉘 명령어를 정의합니다. 예를 들어, 모든 큐 작업자 서버에서 `php artisan queue:restart` 명령을 실행하는 작업을 정의할 수 있습니다.

<!-- All of your Envoy tasks should be defined in an `Envoy.blade.php` file at the root of your application. Here's an example to get you started: -->
모든 Envoy 작업은 애플리케이션 루트 디렉터리에 위치한 `Envoy.blade.php` 파일에 정의하면 됩니다. 다음은 예시입니다.

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

<!-- As you can see, an array of `@servers` is defined at the top of the file, allowing you to reference these servers via the `on` option of your task declarations. The `@servers` declaration should always be placed on a single line. Within your `@task` declarations, you should place the shell commands that should execute on your servers when the task is invoked. -->
위 예시에서 볼 수 있듯이, 파일 상단에 `@servers` 배열을 정의하여 작업 선언의 `on` 옵션을 통해 각 서버를 참조할 수 있습니다. `@servers` 선언문은 항상 한 줄로 작성해야 합니다. 각 `@task` 선언 내부에는 작업 실행 시 서버에서 수행할 쉘 명령어들을 작성합니다.

<a name="local-tasks"></a>
<!-- #### Local Tasks -->
#### Local Tasks

<!-- You can force a script to run on your local computer by specifying the server's IP address as `127.0.0.1`: -->
서버의 IP 주소를 `127.0.0.1`로 지정하면, 해당 스크립트를 로컬 컴퓨터에서 직접 실행하도록 강제할 수 있습니다.

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
<!-- #### Importing Envoy Tasks -->
#### Importing Envoy Tasks

<!-- Using the `@import` directive, you may import other Envoy files so their stories and tasks are added to yours. After the files have been imported, you may execute the tasks they contain as if they were defined in your own Envoy file: -->
`@import` 지시문을 사용하면, 다른 Envoy 파일을 가져와서 그 안의 스토리와 작업들을 사용할 수 있습니다. 임포트된 파일들의 작업 역시 마치 자신의 Envoy 파일에 정의된 것처럼 실행할 수 있습니다.

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
<!-- ### Multiple Servers -->
### Multiple Servers

<!-- Envoy allows you to easily run a task across multiple servers. First, add additional servers to your `@servers` declaration. Each server should be assigned a unique name. Once you have defined your additional servers you may list each of the servers in the task's `on` array: -->
Envoy를 이용하면 작업을 여러 서버에서 한 번에 실행할 수 있습니다. 먼저, 추가로 실행할 서버를 `@servers` 선언문에 나열합니다. 각 서버에는 고유한 이름을 붙여야 하며, 이렇게 추가된 서버들을 작업의 `on` 배열에 넣어 여러 서버에서 한 번에 작업을 실행할 수 있습니다.

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
기본적으로 작업은 각 서버에서 순차적으로(직렬로) 실행됩니다. 즉, 첫 번째 서버에서 작업이 끝난 후 다음 서버로 넘어갑니다. 만약 여러 서버에 작업을 동시에 병렬로 실행하고 싶다면, 작업 선언문에 `parallel` 옵션을 추가하면 됩니다.

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
Envoy 작업을 실행하기 전에 임의의 PHP 코드를 먼저 실행해야 할 경우 `@setup` 지시문을 사용하면 됩니다. 이 블록 내부에는 작업 실행 전에 수행할 PHP 코드를 작성할 수 있습니다.

```php
@setup
    $now = new DateTime;
@endsetup
```

<!-- If you need to require other PHP files before your task is executed, you may use the `@include` directive at the top of your `Envoy.blade.php` file: -->
작업 실행 전에 다른 PHP 파일을 불러와야 한다면, `Envoy.blade.php` 파일 맨 위에 `@include` 지시문을 사용할 수 있습니다.

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
필요하다면, Envoy 작업 실행 시 인수를 명령행에서 넘길 수 있습니다.

```shell
php vendor/bin/envoy run deploy --branch=master
```

<!-- You may access the options within your tasks using Blade's "echo" syntax. You may also define Blade `if` statements and loops within your tasks. For example, let's verify the presence of the `$branch` variable before executing the `git pull` command: -->
작업 내부에서는 이러한 옵션 값을 Blade의 'echo' 문법으로 사용할 수 있습니다. 또한, 작업 내에서 Blade의 `if` 문이나 반복문을 사용할 수도 있습니다. 예를 들어, `$branch` 변수가 있을 때만 `git pull` 명령을 실행하도록 할 수 있습니다.

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
스토리는 여러 개의 작업을 하나의 이름 아래 묶어서 한 번에 실행할 수 있는 기능입니다. 예를 들어, `deploy` 스토리는 `update-code` 작업과 `install-dependencies` 작업을 연달아 실행하도록 할 수 있습니다.

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
스토리를 작성했다면, 일반 작업과 똑같이 명령행에서 호출하여 실행할 수 있습니다.

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
<!-- ### Hooks -->
### Hooks

<!-- When tasks and stories run, a number of hooks are executed. The hook types supported by Envoy are `@before`, `@after`, `@error`, `@success`, and `@finished`. All of the code in these hooks is interpreted as PHP and executed locally, not on the remote servers that your tasks interact with. -->
작업과 스토리가 실행될 때, 여러 종류의 후크(hook)가 동작합니다. Envoy가 지원하는 후크는 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 이 후크 내부의 코드는 모두 PHP로 해석되어 원격 서버가 아니라 **로컬 환경**에서 실행됩니다.

<!-- You may define as many of each of these hooks as you like. They will be executed in the order that they appear in your Envoy script. -->
각 후크는 여러 번 정의해도 되며, Envoy 스크립트에 나오는 순서대로 차례대로 실행됩니다.

<a name="hook-before"></a>
<!-- #### `@before` -->
#### `@before`

<!-- Before each task execution, all of the `@before` hooks registered in your Envoy script will execute. The `@before` hooks receive the name of the task that will be executed: -->
각 작업이 실행되기 전에는, 스크립트에 등록된 모든 `@before` 후크가 실행됩니다. `@before` 후크는 실행될 작업의 이름을 인수로 받습니다.

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
각 작업 실행이 끝난 후에는, 등록된 모든 `@after` 후크가 실행됩니다. `@after` 후크는 실행된 작업의 이름을 인수로 받습니다.

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
작업 실행에 실패하여 종료 상태 코드가 `0`보다 클 때, 등록된 모든 `@error` 후크가 실행됩니다. `@error` 후크는 실행된 작업의 이름을 인수로 받습니다.

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
모든 작업이 에러 없이 정상적으로 완료된 경우, 등록된 모든 `@success` 후크가 실행됩니다.

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
<!-- #### `@finished` -->
#### `@finished`

<!-- After all tasks have been executed (regardless of exit status), all of the `@finished` hooks will be executed. The `@finished` hooks receive the status code of the completed task, which may be `null` or an `integer` greater than or equal to `0`: -->
모든 작업 실행이 끝나고(성공/실패와 관계없이), 등록된 모든 `@finished` 후크가 실행됩니다. `@finished` 후크는 완료된 작업의 종료 코드를 인수로 받으며, 이 값은 `null`이거나 `0` 이상의 `integer`일 수 있습니다.

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
애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업이나 스토리를 실행하려면 Envoy의 `run` 명령을 사용하고, 실행할 작업 또는 스토리의 이름을 인수로 전달하면 됩니다. Envoy는 실행되는 동안 해당 작업의 실행 결과를 원격 서버로부터 받아 출력해줍니다.

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
<!-- ### Confirming Task Execution -->
### Confirming Task Execution

<!-- If you would like to be prompted for confirmation before running a given task on your servers, you should add the `confirm` directive to your task declaration. This option is particularly useful for destructive operations: -->
특정 작업을 서버에서 실행하기 전에 매번 확인 메시지로 사용자의 승인을 받고 싶다면, 작업 선언문에 `confirm` 옵션을 추가합니다. 이는 파괴적이거나 위험한 작업을 실행할 때 유용하게 사용할 수 있습니다.

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
Envoy는 각 작업 실행이 끝난 후 [Slack](https://slack.com)으로 알림 메시지를 보낼 수 있습니다. `@slack` 지시문은 Slack의 웹훅 URL과 채널 또는 사용자 이름을 인수로 받습니다. 웹훅 URL은 Slack 관리 패널에서 "Incoming WebHooks" 연동을 만들어 받을 수 있습니다.

<!-- You should pass the entire webhook URL as the first argument given to the `@slack` directive. The second argument given to the `@slack` directive should be a channel name (`#channel`) or a user name (`@user`): -->
`@slack` 지시문의 첫 번째 인자로 전체 웹훅 URL을 전달해야 합니다. `@slack` 지시문의 두 번째 인자로는 채널명(`#channel`)이나 사용자명(`@user`)을 전달해야 합니다.

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

<!-- By default, Envoy notifications will send a message to the notification channel describing the task that was executed. However, you may overwrite this message with your own custom message by passing a third argument to the `@slack` directive: -->
기본적으로 Envoy 알림은 실행된 작업 내용을 포함한 메시지를 알림 채널로 전송합니다. 하지만, `@slack` 지시문에 세 번째 인수로 원하는 메시지를 지정해서 직접 메시지 내용을 덮어쓸 수도 있습니다.

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
<!-- ### Discord -->
### Discord

<!-- Envoy also supports sending notifications to [Discord](https://discord.com) after each task is executed. The `@discord` directive accepts a Discord hook URL and a message. You may retrieve your webhook URL by creating a "Webhook" in your Server Settings and choosing which channel the webhook should post to. You should pass the entire Webhook URL into the `@discord` directive: -->
Envoy는 [Discord](https://discord.com)로도 알림 메시지를 보낼 수 있습니다. `@discord` 지시문은 Discord 웹훅 URL과 알림 메시지를 인수로 받습니다. 웹훅 URL은 Discord 서버 설정에서 "Webhook"을 만들어 원하는 채널에 연결하면 얻을 수 있습니다. 전체 웹훅 URL을 `@discord` 지시문에 넣으면 됩니다.

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
<!-- ### Telegram -->
### Telegram

<!-- Envoy also supports sending notifications to [Telegram](https://telegram.org) after each task is executed. The `@telegram` directive accepts a Telegram Bot ID and a Chat ID. You may retrieve your Bot ID by creating a new bot using [BotFather](https://t.me/botfather). You can retrieve a valid Chat ID using [@username_to_id_bot](https://t.me/username_to_id_bot). You should pass the entire Bot ID and Chat ID into the `@telegram` directive: -->
Envoy는 [Telegram](https://telegram.org)에도 작업 실행 이후 알림 메시지를 보낼 수 있습니다. `@telegram` 지시문은 Telegram Bot ID와 Chat ID를 인수로 받으며, Bot ID는 [BotFather](https://t.me/botfather)로 새로운 봇을 생성하고, Chat ID는 [@username_to_id_bot](https://t.me/username_to_id_bot)으로 확인할 수 있습니다. 두 값을 모두 직접 `@telegram` 지시문에 전달하면 됩니다.

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
<!-- ### Microsoft Teams -->
### Microsoft Teams

<!-- Envoy also supports sending notifications to [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) after each task is executed. The `@microsoftTeams` directive accepts a Teams Webhook (required), a message, theme color (success, info, warning, error), and an array of options. You may retrieve your Teams Webhook by creating a new [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook). The Teams API has many other attributes to customize your message box like title, summary, and sections. You can find more information on the [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message). You should pass the entire Webhook URL into the `@microsoftTeams` directive: -->
Envoy는 [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams)로도 알림을 전송할 수 있습니다. `@microsoftTeams` 지시문은 필수로 Teams Webhook URL을 받고, 메시지, 테마 색상(예: success, info, warning, error), 옵션 배열 등을 추가로 받을 수 있습니다. Teams Webhook URL은 [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)을 생성하여 얻을 수 있습니다. Teams API는 메시지 상자의 제목, 요약, 섹션 등 다양한 옵션을 지원합니다. 더 자세한 내용은 [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)에서 확인할 수 있습니다. 전체 Webhook URL을 `@microsoftTeams` 지시문에 전달하면 됩니다.

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```
