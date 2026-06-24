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
[Laravel Envoy](https://github.com/laravel/envoy) は、リモート サーバーで実行する一般的なタスクを実行するためのツールです。 [Blade](/docs/9.x/blade) スタイルの構文を使用すると、デプロイメントのタスクやArtisan コマンドなどを簡単にセットアップできます。現在、Envoy は Mac と Linux オペレーティング システムのみをサポートしています。ただし、Windows のサポートは、[WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10) を使用して実現できます。

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- First, install Envoy into your project using the Composer package manager: -->
まず、Composer パッケージ マネージャーを使用して Envoy をプロジェクトにインストールします。

```shell
composer require laravel/envoy --dev
```

<!-- Once Envoy has been installed, the Envoy binary will be available in your application's `vendor/bin` directory: -->
Envoy がインストールされると、Envoy バイナリがアプリケーションの `vendor/bin` ディレクトリで利用できるようになります。

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
タスクは Envoy の基本的な構成要素です。タスクは、タスクの呼び出し時にリモート サーバー上で実行するシェル コマンドを定義します。たとえば、アプリケーションのすべてのキューワーカー サーバーで `php artisan queue:restart` コマンドを実行するタスクを定義できます。

<!-- All of your Envoy tasks should be defined in an `Envoy.blade.php` file at the root of your application. Here's an example to get you started: -->
すべての Envoy タスクは、アプリケーションのルートにある `Envoy.blade.php` ファイルで定義する必要があります。始めるための例を次に示します。

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

<!-- As you can see, an array of `@servers` is defined at the top of the file, allowing you to reference these servers via the `on` option of your task declarations. The `@servers` declaration should always be placed on a single line. Within your `@task` declarations, you should place the shell commands that should execute on your servers when the task is invoked. -->
ご覧のとおり、`@servers` の配列がファイルの先頭で定義されており、タスク宣言の `on` オプションを介してこれらのサーバーを参照できるようになります。 `@servers` 宣言は常に 1 行に配置する必要があります。 `@task` 宣言内に、タスクの呼び出し時にサーバーで実行するシェル コマンドを配置する必要があります。

<a name="local-tasks"></a>
<!-- #### Local Tasks -->
#### Local Tasks

<!-- You can force a script to run on your local computer by specifying the server's IP address as `127.0.0.1`: -->
サーバーの IP アドレスを `127.0.0.1` として指定すると、ローカル コンピューターでスクリプトを強制的に実行できます。

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
<!-- #### Importing Envoy Tasks -->
#### Importing Envoy Tasks

<!-- Using the `@import` directive, you may import other Envoy files so their stories and tasks are added to yours. After the files have been imported, you may execute the tasks they contain as if they were defined in your own Envoy file: -->
`@import` ディレクティブを使用すると、他の Envoy ファイルをインポートして、そのストーリーとタスクを自分のファイルに追加できます。ファイルがインポートされたら、あたかも独自の Envoy ファイルで定義されているかのように、ファイルに含まれるタスクを実行できます。

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
<!-- ### Multiple Servers -->
### Multiple Servers

<!-- Envoy allows you to easily run a task across multiple servers. First, add additional servers to your `@servers` declaration. Each server should be assigned a unique name. Once you have defined your additional servers you may list each of the servers in the task's `on` array: -->
Envoy を使用すると、複数のサーバー間でタスクを簡単に実行できます。まず、`@servers` 宣言に追加のサーバーを追加します。各サーバーには一意の名前を割り当てる必要があります。追加のサーバーを定義したら、タスクの `on` 配列内の各サーバーをリストできます。

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
デフォルトでは、タスクは各サーバー上で順番に実行されます。つまり、タスクは 2 番目のサーバーでの実行に進む前に、1 番目のサーバーでの実行を終了します。複数のサーバー間でタスクを並行して実行したい場合は、タスク宣言に `parallel` オプションを追加します。

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
場合によっては、Envoy タスクを実行する前に任意の PHP コードを実行する必要がある場合があります。 `@setup` ディレクティブを使用して、タスクの前に実行する必要がある PHP コードのブロックを定義できます。

```php
@setup
    $now = new DateTime;
@endsetup
```

<!-- If you need to require other PHP files before your task is executed, you may use the `@include` directive at the top of your `Envoy.blade.php` file: -->
タスクの実行前に他の PHP ファイルが必要な場合は、`Envoy.blade.php` ファイルの先頭で `@include` ディレクティブを使用できます。

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
必要に応じて、Envoy を呼び出すときにコマンド ラインで引数を指定して、Envoy タスクに引数を渡すことができます。

```shell
php vendor/bin/envoy run deploy --branch=master
```

<!-- You may access the options within your tasks using Blade's "echo" syntax. You may also define Blade `if` statements and loops within your tasks. For example, let's verify the presence of the `$branch` variable before executing the `git pull` command: -->
Blade の「echo」構文を使用して、タスク内のオプションにアクセスできます。タスク内でBlade `if` ステートメントとループを定義することもできます。たとえば、`git pull` コマンドを実行する前に、`$branch` 変数の存在を確認してみましょう。

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
ストーリーは、一連のタスクを単一の便利な名前でグループ化します。たとえば、`deploy` ストーリーでは、その定義内にタスク名をリストすることで、`update-code` タスクと `install-dependencies` タスクを実行できます。

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
ストーリーを作成したら、タスクを呼び出すのと同じ方法でストーリーを呼び出すことができます。

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
<!-- ### Hooks -->
### Hooks

<!-- When tasks and stories run, a number of hooks are executed. The hook types supported by Envoy are `@before`, `@after`, `@error`, `@success`, and `@finished`. All of the code in these hooks is interpreted as PHP and executed locally, not on the remote servers that your tasks interact with. -->
タスクとストーリーが実行されると、多数のフックが実行されます。 Envoy でサポートされるフック タイプは、`@before`、`@after`、`@error`、`@success`、および `@finished` です。これらのフック内のコードはすべて PHP として解釈され、タスクが対話するリモート サーバーではなくローカルで実行されます。

<!-- You may define as many of each of these hooks as you like. They will be executed in the order that they appear in your Envoy script. -->
これらのフックはそれぞれ、好きなだけ定義できます。これらは、Envoy スクリプトに表示される順序で実行されます。

<a name="hook-before"></a>
<!-- #### `@before` -->
#### `@before`

<!-- Before each task execution, all of the `@before` hooks registered in your Envoy script will execute. The `@before` hooks receive the name of the task that will be executed: -->
各タスクの実行前に、Envoy スクリプトに登録されているすべての `@before` フックが実行されます。 `@before` フックは、実行されるタスクの名前を受け取ります。

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
各タスクの実行後、Envoy スクリプトに登録されているすべての `@after` フックが実行されます。 `@after` フックは、実行されたタスクの名前を受け取ります。

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
タスクが失敗するたびに (`0` より大きいステータス コードで終了する)、Envoy スクリプトに登録されているすべての `@error` フックが実行されます。 `@error` フックは、実行されたタスクの名前を受け取ります。

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
すべてのタスクがエラーなしで実行された場合、Envoy スクリプトに登録されているすべての `@success` フックが実行されます。

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
<!-- #### `@finished` -->
#### `@finished`

<!-- After all tasks have been executed (regardless of exit status), all of the `@finished` hooks will be executed. The `@finished` hooks receive the status code of the completed task, which may be `null` or an `integer` greater than or equal to `0`: -->
すべてのタスクが実行された後 (終了ステータスに関係なく)、すべての `@finished` フックが実行されます。 `@finished` フックは、完了したタスクのステータス コードを受け取ります。これは、`null` または `0` 以上の `integer` である可能性があります。

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
アプリケーションの `Envoy.blade.php` ファイルで定義されているタスクまたはストーリーを実行するには、実行するタスクまたはストーリーの名前を渡して、Envoy の `run` コマンドを実行します。 Envoy はタスクを実行し、タスクの実行中にリモート サーバーからの出力を表示します。

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
<!-- ### Confirming Task Execution -->
### Confirming Task Execution

<!-- If you would like to be prompted for confirmation before running a given task on your servers, you should add the `confirm` directive to your task declaration. This option is particularly useful for destructive operations: -->
サーバー上で特定のタスクを実行する前に確認を求めるプロンプトを表示したい場合は、タスク宣言に `confirm` ディレクティブを追加する必要があります。このオプションは、破壊的な操作に特に役立ちます。

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
Envoy は、各タスクの実行後に [Slack](https://slack.com) への通知の送信をサポートします。 `@slack` ディレクティブは、Slack フック URL とチャネル/ユーザー名を受け入れます。 Slack コントロール パネルで「受信 WebHook」統合を作成することで、Webhook URL を取得できます。

<!-- You should pass the entire webhook URL as the first argument given to the `@slack` directive. The second argument given to the `@slack` directive should be a channel name (`#channel`) or a user name (`@user`): -->
Webhook URL 全体を、`@slack` ディレクティブに指定する最初の引数として渡す必要があります。 `@slack` ディレクティブに指定する 2 番目の引数は、チャネル名 (`#channel`) またはユーザー名 (`@user`) である必要があります。

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

<!-- By default, Envoy notifications will send a message to the notification channel describing the task that was executed. However, you may overwrite this message with your own custom message by passing a third argument to the `@slack` directive: -->
デフォルトでは、Envoy 通知は、実行されたタスクを説明するメッセージを通知チャネルに送信します。ただし、`@slack` ディレクティブに 3 番目の引数を渡すことで、このメッセージを独自のカスタム メッセージで上書きできます。

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
<!-- ### Discord -->
### Discord

<!-- Envoy also supports sending notifications to [Discord](https://discord.com) after each task is executed. The `@discord` directive accepts a Discord hook URL and a message. You may retrieve your webhook URL by creating a "Webhook" in your Server Settings and choosing which channel the webhook should post to. You should pass the entire Webhook URL into the `@discord` directive: -->
Envoy は、各タスクの実行後に [Discord](https://discord.com) への通知の送信もサポートしています。 `@discord` ディレクティブは、Discord フック URL とメッセージを受け入れます。 Webhook URL を取得するには、サーバー設定で「Webhook」を作成し、Webhook を投稿するチャネルを選択します。 Webhook URL 全体を `@discord` ディレクティブに渡す必要があります。

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
<!-- ### Telegram -->
### Telegram

<!-- Envoy also supports sending notifications to [Telegram](https://telegram.org) after each task is executed. The `@telegram` directive accepts a Telegram Bot ID and a Chat ID. You may retrieve your Bot ID by creating a new bot using [BotFather](https://t.me/botfather). You can retrieve a valid Chat ID using [@username_to_id_bot](https://t.me/username_to_id_bot). You should pass the entire Bot ID and Chat ID into the `@telegram` directive: -->
Envoy は、各タスクの実行後に [Telegram](https://telegram.org) への通知の送信もサポートしています。 `@telegram` ディレクティブは、テレグラム ボット ID とチャット ID を受け入れます。 [BotFather](https://t.me/botfather) を使用して新しいボットを作成すると、ボット ID を取得できます。 [@username_to_id_bot](https://t.me/username_to_id_bot) を使用して有効なチャット ID を取得できます。ボット ID とチャット ID 全体を `@telegram` ディレクティブに渡す必要があります。

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
<!-- ### Microsoft Teams -->
### Microsoft Teams

<!-- Envoy also supports sending notifications to [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) after each task is executed. The `@microsoftTeams` directive accepts a Teams Webhook (required), a message, theme color (success, info, warning, error), and an array of options. You may retrieve your Teams Webhook by creating a new [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook). The Teams API has many other attributes to customize your message box like title, summary, and sections. You can find more information on the [Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message). You should pass the entire Webhook URL into the `@microsoftTeams` directive: -->
Envoy は、各タスクの実行後に [Microsoft Teams](https://www.microsoft.com/en-us/microsoft-teams) への通知の送信もサポートしています。 `@microsoftTeams` ディレクティブは、Teams Webhook (必須)、メッセージ、テーマの色 (成功、情報、警告、エラー)、およびオプションの配列を受け入れます。新しい [incoming webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) を作成することで、Teams Webhook を取得できます。 Teams API には、タイトル、概要、セクションなど、メッセージ ボックスをカスタマイズするための他の多くの属性があります。詳細については、[Microsoft Teams documentation](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message) をご覧ください。 Webhook URL 全体を `@microsoftTeams` ディレクティブに渡す必要があります。

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```

