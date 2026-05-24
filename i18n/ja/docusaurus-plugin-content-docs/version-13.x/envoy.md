# Laravel特使 (Laravel Envoy)

- [Introduction](#introduction)
- [Installation](#installation)
- [タスクを書く](#writing-tasks)
    - [タスクの定義](#defining-tasks)
    - [複数のサーバー](#multiple-servers)
    - [Setup](#setup)
    - [Variables](#variables)
    - [Stories](#stories)
    - [Hooks](#completion-hooks)
- [タスクの実行](#running-tasks)
    - [タスクの実行を確認する](#confirming-task-execution)
- [Notifications](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [マイクロソフトチーム](#microsoft-teams)

<a name="introduction"></a>
## 導入 (Introduction)

[Laravel特使](https://github.com/laravel/envoy) は、リモート サーバーで実行する一般的なタスクを実行するためのツールです。 [Blade](/docs/{{version}}/blade) スタイルの構文を使用すると、デプロイメントのタスクやArtisan コマンドなどを簡単にセットアップできます。現在、Envoy は Mac と Linux オペレーティング システムのみをサポートしています。ただし、Windows のサポートは、[WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10) を使用して実現できます。

<a name="installation"></a>
## インストール (Installation)

まず、Composer パッケージ マネージャーを使用して Envoy をプロジェクトにインストールします。

```shell
composer require laravel/envoy --dev
```

Envoy がインストールされると、Envoy バイナリがアプリケーションの `vendor/bin` ディレクトリで利用できるようになります。

```shell
php vendor/bin/envoy
```

<a name="writing-tasks"></a>
## タスクを書く (Writing Tasks)

<a name="defining-tasks"></a>
### タスクの定義

タスクは Envoy の基本的な構成要素です。タスクは、タスクの呼び出し時にリモート サーバー上で実行するシェル コマンドを定義します。たとえば、アプリケーションのすべてのキューワーカー サーバーで `php artisan queue:restart` コマンドを実行するタスクを定義できます。

すべての Envoy タスクは、アプリケーションのルートにある `Envoy.blade.php` ファイルで定義する必要があります。始めるための例を次に示します。

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask
```

ご覧のとおり、`@servers` の配列がファイルの先頭で定義されており、タスク宣言の `on` オプションを介してこれらのサーバーを参照できるようになります。 `@servers` 宣言は常に 1 行に配置する必要があります。 `@task` 宣言内に、タスクの呼び出し時にサーバーで実行するシェル コマンドを配置する必要があります。

<a name="local-tasks"></a>
#### ローカルタスク

サーバーの IP アドレスを `127.0.0.1` として指定すると、ローカル コンピューターでスクリプトを強制的に実行できます。

```blade
@servers(['localhost' => '127.0.0.1'])
```

<a name="importing-envoy-tasks"></a>
#### Envoy タスクのインポート

`@import` ディレクティブを使用すると、他の Envoy ファイルをインポートして、そのストーリーとタスクを自分のファイルに追加できます。ファイルがインポートされたら、あたかも独自の Envoy ファイルで定義されているかのように、ファイルに含まれるタスクを実行できます。

```blade
@import('vendor/package/Envoy.blade.php')
```

<a name="multiple-servers"></a>
### 複数のサーバー

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
#### 並列実行

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
### 設定

場合によっては、Envoy タスクを実行する前に任意の PHP コードを実行する必要がある場合があります。 `@setup` ディレクティブを使用して、タスクの前に実行する必要がある PHP コードのブロックを定義できます。

```php
@setup
    $now = new DateTime;
@endsetup
```

タスクの実行前に他の PHP ファイルが必要な場合は、`Envoy.blade.php` ファイルの先頭で `@include` ディレクティブを使用できます。

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask
```

<a name="variables"></a>
### 変数

必要に応じて、Envoy を呼び出すときにコマンド ラインで引数を指定して、Envoy タスクに引数を渡すことができます。

```shell
php vendor/bin/envoy run deploy --branch=master
```

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
### ストーリー

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

ストーリーを作成したら、タスクを呼び出すのと同じ方法でストーリーを呼び出すことができます。

```shell
php vendor/bin/envoy run deploy
```

<a name="completion-hooks"></a>
### フック

タスクとストーリーが実行されると、多数のフックが実行されます。 Envoy でサポートされるフック タイプは、`@before`、`@after`、`@error`、`@success`、および `@finished` です。これらのフック内のコードはすべて PHP として解釈され、タスクが対話するリモート サーバーではなくローカルで実行されます。

これらのフックはそれぞれ、好きなだけ定義できます。これらは、Envoy スクリプトに表示される順序で実行されます。

<a name="hook-before"></a>
#### `@before`

各タスクの実行前に、Envoy スクリプトに登録されているすべての `@before` フックが実行されます。 `@before` フックは、実行されるタスクの名前を受け取ります。

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore
```

<a name="completion-after"></a>
#### `@after`

各タスクの実行後、Envoy スクリプトに登録されているすべての `@after` フックが実行されます。 `@after` フックは、実行されたタスクの名前を受け取ります。

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter
```

<a name="completion-error"></a>
#### `@error`

タスクが失敗するたびに (`0` より大きいステータス コードで終了する)、Envoy スクリプトに登録されているすべての `@error` フックが実行されます。 `@error` フックは、実行されたタスクの名前を受け取ります。

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror
```

<a name="completion-success"></a>
#### `@success`

すべてのタスクがエラーなしで実行された場合、Envoy スクリプトに登録されているすべての `@success` フックが実行されます。

```blade
@success
    // ...
@endsuccess
```

<a name="completion-finished"></a>
#### `@finished`

すべてのタスクが実行された後 (終了ステータスに関係なく)、すべての `@finished` フックが実行されます。 `@finished` フックは、完了したタスクのステータス コードを受け取ります。これは、`null` または `0` 以上の `integer` である可能性があります。

```blade
@finished
    if ($exitCode > 0) {
        // There were errors in one of the tasks...
    }
@endfinished
```

<a name="running-tasks"></a>
## タスクの実行 (Running Tasks)

アプリケーションの `Envoy.blade.php` ファイルで定義されているタスクまたはストーリーを実行するには、実行するタスクまたはストーリーの名前を渡して、Envoy の `run` コマンドを実行します。 Envoy はタスクを実行し、タスクの実行中にリモート サーバーからの出力を表示します。

```shell
php vendor/bin/envoy run deploy
```

<a name="confirming-task-execution"></a>
### タスクの実行を確認する

サーバー上で特定のタスクを実行する前に確認を求めるプロンプトを表示したい場合は、タスク宣言に `confirm` ディレクティブを追加する必要があります。このオプションは、破壊的な操作に特に役立ちます。

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask
```

<a name="notifications"></a>
## 通知 (Notifications)

<a name="slack"></a>
### スラック

Envoy は、各タスクの実行後に [Slack](https://slack.com) への通知の送信をサポートします。 `@slack` ディレクティブは、Slack フック URL とチャネル/ユーザー名を受け入れます。 Slack コントロール パネルで「受信 WebHook」統合を作成することで、Webhook URL を取得できます。

Webhook URL 全体を、`@slack` ディレクティブに指定する最初の引数として渡す必要があります。 `@slack` ディレクティブに指定する 2 番目の引数は、チャネル名 (`#channel`) またはユーザー名 (`@user`) である必要があります。

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished
```

デフォルトでは、Envoy 通知は、実行されたタスクを説明するメッセージを通知チャネルに送信します。ただし、`@slack` ディレクティブに 3 番目の引数を渡すことで、このメッセージを独自のカスタム メッセージで上書きできます。

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished
```

<a name="discord"></a>
### 不和

Envoy は、各タスクの実行後に [Discord](https://discord.com) への通知の送信もサポートしています。 `@discord` ディレクティブは、Discord フック URL とメッセージを受け入れます。 Webhook URL を取得するには、サーバー設定で「Webhook」を作成し、Webhook を投稿するチャネルを選択します。 Webhook URL 全体を `@discord` ディレクティブに渡す必要があります。

```blade
@finished
    @discord('discord-webhook-url')
@endfinished
```

<a name="telegram"></a>
### 電報

Envoy は、各タスクの実行後に [Telegram](https://telegram.org) への通知の送信もサポートしています。 `@telegram` ディレクティブは、テレグラム ボット ID とチャット ID を受け入れます。 [BotFather](https://t.me/botfather) を使用して新しいボットを作成すると、ボット ID を取得できます。 [@username_to_id_bot](https://t.me/username_to_id_bot) を使用して有効なチャット ID を取得できます。ボット ID とチャット ID 全体を `@telegram` ディレクティブに渡す必要があります。

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished
```

<a name="microsoft-teams"></a>
### マイクロソフトチーム

Envoy は、各タスクの実行後に [マイクロソフトチーム](https://www.microsoft.com/en-us/microsoft-teams) への通知の送信もサポートしています。 `@microsoftTeams` ディレクティブは、Teams Webhook (必須)、メッセージ、テーマの色 (成功、情報、警告、エラー)、およびオプションの配列を受け入れます。新しい [受信 Webhook](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook) を作成することで、Teams Webhook を取得できます。 Teams API には、タイトル、概要、セクションなど、メッセージ ボックスをカスタマイズするための他の多くの属性があります。詳細については、[Microsoft Teams のドキュメント](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message) をご覧ください。 Webhook URL 全体を `@microsoftTeams` ディレクティブに渡す必要があります。

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished
```

