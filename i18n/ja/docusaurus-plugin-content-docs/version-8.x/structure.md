<!-- # Directory Structure -->
# Directory Structure

- [Introduction](#introduction)
- [The Root Directory](#the-root-directory)
    - [The `app` Directory](#the-root-app-directory)
    - [The `bootstrap` Directory](#the-bootstrap-directory)
    - [The `config` Directory](#the-config-directory)
    - [The `database` Directory](#the-database-directory)
    - [The `public` Directory](#the-public-directory)
    - [The `resources` Directory](#the-resources-directory)
    - [The `routes` Directory](#the-routes-directory)
    - [The `storage` Directory](#the-storage-directory)
    - [The `tests` Directory](#the-tests-directory)
    - [The `vendor` Directory](#the-vendor-directory)
- [The App Directory](#the-app-directory)
    - [The `Broadcasting` Directory](#the-broadcasting-directory)
    - [The `Console` Directory](#the-console-directory)
    - [The `Events` Directory](#the-events-directory)
    - [The `Exceptions` Directory](#the-exceptions-directory)
    - [The `Http` Directory](#the-http-directory)
    - [The `Jobs` Directory](#the-jobs-directory)
    - [The `Listeners` Directory](#the-listeners-directory)
    - [The `Mail` Directory](#the-mail-directory)
    - [The `Models` Directory](#the-models-directory)
    - [The `Notifications` Directory](#the-notifications-directory)
    - [The `Policies` Directory](#the-policies-directory)
    - [The `Providers` Directory](#the-providers-directory)
    - [The `Rules` Directory](#the-rules-directory)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- The default Laravel application structure is intended to provide a great starting point for both large and small applications. But you are free to organize your application however you like. Laravel imposes almost no restrictions on where any given class is located - as long as Composer can autoload the class. -->
デフォルトの Laravel アプリケーション構造は、大規模なアプリケーションと小規模なアプリケーションの両方に優れた出発点を提供することを目的としています。ただし、アプリケーションを自由に編成できます。 Laravel では、Composer がクラスを自動ロードできる限り、特定のクラスの配置場所にほとんど制限がありません。

<a name="the-root-directory"></a>
<!-- ## The Root Directory -->
## The Root Directory

<a name="the-root-app-directory"></a>
<!-- #### The App Directory -->
#### The App Directory

<!-- The `app` directory contains the core code of your application. We'll explore this directory in more detail soon; however, almost all of the classes in your application will be in this directory. -->
`app` ディレクトリには、アプリケーションのコア コードが含まれています。このディレクトリについては、後ほど詳しく説明します。ただし、アプリケーション内のほとんどすべてのクラスはこのディレクトリにあります。

<a name="the-bootstrap-directory"></a>
<!-- #### The Bootstrap Directory -->
#### The Bootstrap Directory

<!-- The `bootstrap` directory contains the `app.php` file which bootstraps the framework. This directory also houses a `cache` directory which contains framework generated files for performance optimization such as the route and services cache files. You should not typically need to modify any files within this directory. -->
`bootstrap` ディレクトリには、フレームワークをブートストラップする `app.php` ファイルが含まれています。このディレクトリには、ルート キャッシュ ファイルやサービス キャッシュ ファイルなど、パフォーマンスを最適化するためにフレームワークで生成されたファイルが含まれる `cache` ディレクトリも格納されます。通常、このディレクトリ内のファイルを変更する必要はありません。

<a name="the-config-directory"></a>
<!-- #### The Config Directory -->
#### The Config Directory

<!-- The `config` directory, as the name implies, contains all of your application's configuration files. It's a great idea to read through all of these files and familiarize yourself with all of the options available to you. -->
`config` ディレクトリには、名前が示すように、アプリケーションのすべての構成ファイルが含まれています。これらのファイルをすべて読んで、利用可能なすべてのオプションをよく理解することをお勧めします。

<a name="the-database-directory"></a>
<!-- #### The Database Directory -->
#### The Database Directory

<!-- The `database` directory contains your database migrations, model factories, and seeds. If you wish, you may also use this directory to hold an SQLite database. -->
`database` ディレクトリには、データベースの移行、モデル ファクトリ、およびシードが含まれています。必要に応じて、このディレクトリを使用して SQLite データベースを保持することもできます。

<a name="the-public-directory"></a>
<!-- #### The Public Directory -->
#### The Public Directory

<!-- The `public` directory contains the `index.php` file, which is the entry point for all requests entering your application and configures autoloading. This directory also houses your assets such as images, JavaScript, and CSS. -->
`public` ディレクトリには、アプリケーションに入るすべてのリクエストのエントリ ポイントとなり、自動ロードを構成する `index.php` ファイルが含まれています。このディレクトリには、画像、JavaScript、CSS などのアセットも格納されます。

<a name="the-resources-directory"></a>
<!-- #### The Resources Directory -->
#### The Resources Directory

<!-- The `resources` directory contains your [views](/docs/8.x/views) as well as your raw, un-compiled assets such as CSS or JavaScript. This directory also houses all of your language files. -->
`resources` ディレクトリには、[views](/docs/8.x/views) と、CSS や JavaScript などの生の未コンパイル アセットが含まれています。このディレクトリには、すべての言語ファイルも格納されます。

<a name="the-routes-directory"></a>
<!-- #### The Routes Directory -->
#### The Routes Directory

<!-- The `routes` directory contains all of the route definitions for your application. By default, several route files are included with Laravel: `web.php`, `api.php`, `console.php`, and `channels.php`. -->
`routes` ディレクトリには、アプリケーションのすべてのルート定義が含まれています。デフォルトでは、Laravel にはいくつかのルートファイル (`web.php`、`api.php`、`console.php`、`channels.php`) が含まれています。

<!-- The `web.php` file contains routes that the `RouteServiceProvider` places in the `web` middleware group, which provides session state, CSRF protection, and cookie encryption. If your application does not offer a stateless, RESTful API then it is likely that all of your routes will most likely be defined in the `web.php` file. -->
`web.php` ファイルには、`RouteServiceProvider` が `web` ミドルウェア グループに配置するルートが含まれており、セッション状態、CSRF 保護、Cookie 暗号化が提供されます。アプリケーションがステートレスな RESTful API を提供していない場合は、すべてのルートが `web.php` ファイルで定義される可能性が高くなります。

<!-- The `api.php` file contains routes that the `RouteServiceProvider` places in the `api` middleware group. These routes are intended to be stateless, so requests entering the application through these routes are intended to be authenticated [via tokens](/docs/8.x/sanctum) and will not have access to session state. -->
`api.php` ファイルには、`RouteServiceProvider` が `api` ミドルウェア グループに配置するルートが含まれています。これらのルートはステートレスであることを目的としているため、これらのルートを介してアプリケーションに入るリクエストは [via tokens](/docs/8.x/sanctum) で認証されることを目的としており、セッション状態にはアクセスできません。

<!-- The `console.php` file is where you may define all of your closure based console commands. Each closure is bound to a command instance allowing a simple approach to interacting with each command's IO methods. Even though this file does not define HTTP routes, it defines console based entry points (routes) into your application. -->
`console.php` ファイルでは、クロージャ ベースのコンソール コマンドをすべて定義できます。各クロージャはコマンド インスタンスにバインドされており、各コマンドの IO メソッドと対話する簡単なアプローチが可能になります。このファイルは HTTP ルートを定義しませんが、アプリケーションへのコンソール ベースのエントリ ポイント (ルート) を定義します。

<!-- The `channels.php` file is where you may register all of the [event broadcasting](/docs/8.x/broadcasting) channels that your application supports. -->
`channels.php` ファイルには、アプリケーションがサポートするすべての [event broadcasting](/docs/8.x/broadcasting) チャネルを登録できます。

<a name="the-storage-directory"></a>
<!-- #### The Storage Directory -->
#### The Storage Directory

<!-- The `storage` directory contains your logs, compiled Blade templates, file based sessions, file caches, and other files generated by the framework. This directory is segregated into `app`, `framework`, and `logs` directories. The `app` directory may be used to store any files generated by your application. The `framework` directory is used to store framework generated files and caches. Finally, the `logs` directory contains your application's log files. -->
`storage` ディレクトリには、ログ、コンパイルされた Blade テンプレート、ファイル ベースのセッション、ファイル キャッシュ、およびフレームワークによって生成されたその他のファイルが含まれています。このディレクトリは、`app`、`framework`、および `logs` ディレクトリに分離されています。 `app` ディレクトリは、アプリケーションによって生成されたファイルを保存するために使用できます。 `framework` ディレクトリは、フレームワークで生成されたファイルとキャッシュを保存するために使用されます。最後に、`logs` ディレクトリにはアプリケーションのログ ファイルが含まれます。

<!-- The `storage/app/public` directory may be used to store user-generated files, such as profile avatars, that should be publicly accessible. You should create a symbolic link at `public/storage` which points to this directory. You may create the link using the `php artisan storage:link` Artisan command. -->
`storage/app/public` ディレクトリは、プロファイル アバターなど、パブリックにアクセスできる必要があるユーザー生成ファイルを保存するために使用できます。このディレクトリを指すシンボリック リンクを `public/storage` に作成する必要があります。 `php artisan storage:link` Artisan コマンドを使用してリンクを作成できます。

<a name="the-tests-directory"></a>
<!-- #### The Tests Directory -->
#### The Tests Directory

<!-- The `tests` directory contains your automated tests. Example [PHPUnit](https://phpunit.de/) unit tests and feature tests are provided out of the box. Each test class should be suffixed with the word `Test`. You may run your tests using the `phpunit` or `php vendor/bin/phpunit` commands. Or, if you would like a more detailed and beautiful representation of your test results, you may run your tests using the `php artisan test` Artisan command. -->
`tests` ディレクトリには自動テストが含まれています。 [PHPUnit](https://phpunit.de/) の単体テストと機能テストの例は、すぐに使用できるように提供されています。各テスト クラスには、`Test` という語の接尾辞を付ける必要があります。 `phpunit` または `php vendor/bin/phpunit` コマンドを使用してテストを実行できます。または、テスト結果をより詳細に美しく表現したい場合は、`php artisan test` Artisan コマンドを使用してテストを実行できます。

<a name="the-vendor-directory"></a>
<!-- #### The Vendor Directory -->
#### The Vendor Directory

<!-- The `vendor` directory contains your [Composer](https://getcomposer.org) dependencies. -->
`vendor` ディレクトリには、[Composer](https://getcomposer.org) 依存関係が含まれています。

<a name="the-app-directory"></a>
<!-- ## The App Directory -->
## The App Directory

<!-- The majority of your application is housed in the `app` directory. By default, this directory is namespaced under `App` and is autoloaded by Composer using the [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/). -->
アプリケーションの大部分は、`app` ディレクトリに格納されています。デフォルトでは、このディレクトリは `App` の下に名前空間が設定されており、[PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/) を使用して Composer によって自動ロードされます。

<!-- The `app` directory contains a variety of additional directories such as `Console`, `Http`, and `Providers`. Think of the `Console` and `Http` directories as providing an API into the core of your application. The HTTP protocol and CLI are both mechanisms to interact with your application, but do not actually contain application logic. In other words, they are two ways of issuing commands to your application. The `Console` directory contains all of your Artisan commands, while the `Http` directory contains your controllers, middleware, and requests. -->
`app` ディレクトリには、`Console`、`Http`、`Providers` などのさまざまな追加ディレクトリが含まれています。 `Console` ディレクトリと `Http` ディレクトリは、アプリケーションのコアに API を提供すると考えてください。 HTTP プロトコルと CLI はどちらもアプリケーションと対話するメカニズムですが、実際にはアプリケーション ロジックは含まれません。言い換えれば、これらはアプリケーションにコマンドを発行する 2 つの方法です。 `Console` ディレクトリにはすべての Artisan コマンドが含まれ、`Http` ディレクトリにはコントローラ、ミドルウェア、リクエストが含まれます。

<!-- A variety of other directories will be generated inside the `app` directory as you use the `make` Artisan commands to generate classes. So, for example, the `app/Jobs` directory will not exist until you execute the `make:job` Artisan command to generate a job class. -->
`make` Artisan コマンドを使用してクラスを生成すると、`app` ディレクトリ内に他のさまざまなディレクトリが生成されます。したがって、たとえば、`app/Jobs` ディレクトリは、`make:job` Artisan コマンドを実行してジョブ クラスを生成するまで存在しません。

> [!TIP]
> `app` ディレクトリ内のクラスの多くは、Artisan がコマンドを使用して生成できます。使用可能なコマンドを確認するには、ターミナルで `php artisan list make` コマンドを実行します。

<a name="the-broadcasting-directory"></a>
<!-- #### The Broadcasting Directory -->
#### The Broadcasting Directory

<!-- The `Broadcasting` directory contains all of the broadcast channel classes for your application. These classes are generated using the `make:channel` command. This directory does not exist by default, but will be created for you when you create your first channel. To learn more about channels, check out the documentation on [event broadcasting](/docs/8.x/broadcasting). -->
`Broadcasting` ディレクトリには、アプリケーションのすべてのブロードキャスト チャネル クラスが含まれています。これらのクラスは、`make:channel` コマンドを使用して生成されます。このディレクトリはデフォルトでは存在しませんが、最初のチャネルを作成するときに作成されます。チャネルの詳細については、[event broadcasting](/docs/8.x/broadcasting) のドキュメントを参照してください。

<a name="the-console-directory"></a>
<!-- #### The Console Directory -->
#### The Console Directory

<!-- The `Console` directory contains all of the custom Artisan commands for your application. These commands may be generated using the `make:command` command. This directory also houses your console kernel, which is where your custom Artisan commands are registered and your [scheduled tasks](/docs/8.x/scheduling) are defined. -->
`Console` ディレクトリには、アプリケーションのカスタム Artisan コマンドがすべて含まれています。これらのコマンドは、`make:command` コマンドを使用して生成できます。このディレクトリには、コンソール カーネルも格納されます。ここにカスタム Artisan コマンドが登録され、[scheduled tasks](/docs/8.x/scheduling) が定義されます。

<a name="the-events-directory"></a>
<!-- #### The Events Directory -->
#### The Events Directory

<!-- This directory does not exist by default, but will be created for you by the `event:generate` and `make:event` Artisan commands. The `Events` directory houses [event classes](/docs/8.x/events). Events may be used to alert other parts of your application that a given action has occurred, providing a great deal of flexibility and decoupling. -->
このディレクトリはデフォルトでは存在しませんが、`event:generate` および `make:event` Artisan コマンドによって作成されます。 `Events` ディレクトリには [event classes](/docs/8.x/events) が含まれています。イベントを使用して、特定のアクションが発生したことをアプリケーションの他の部分に警告することができ、大幅な柔軟性と分離が実現します。

<a name="the-exceptions-directory"></a>
<!-- #### The Exceptions Directory -->
#### The Exceptions Directory

<!-- The `Exceptions` directory contains your application's exception handler and is also a good place to place any exceptions thrown by your application. If you would like to customize how your exceptions are logged or rendered, you should modify the `Handler` class in this directory. -->
`Exceptions` ディレクトリにはアプリケーションの例外ハンドラーが含まれており、アプリケーションによってスローされた例外を配置するのにも適した場所です。例外のログ記録または表示方法をカスタマイズしたい場合は、このディレクトリ内の `Handler` クラスを変更する必要があります。

<a name="the-http-directory"></a>
<!-- #### The Http Directory -->
#### The Http Directory

<!-- The `Http` directory contains your controllers, middleware, and form requests. Almost all of the logic to handle requests entering your application will be placed in this directory. -->
`Http` ディレクトリには、コントローラ、ミドルウェア、フォーム リクエストが含まれています。アプリケーションに入るリクエストを処理するロジックのほとんどは、このディレクトリに配置されます。

<a name="the-jobs-directory"></a>
<!-- #### The Jobs Directory -->
#### The Jobs Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:job` Artisan command. The `Jobs` directory houses the [queueable jobs](/docs/8.x/queues) for your application. Jobs may be queued by your application or run synchronously within the current request lifecycle. Jobs that run synchronously during the current request are sometimes referred to as "commands" since they are an implementation of the [command pattern](https://en.wikipedia.org/wiki/Command_pattern). -->
このディレクトリはデフォルトでは存在しませんが、`make:job` Artisan コマンドを実行すると作成されます。 `Jobs` ディレクトリには、アプリケーションの [queueable jobs](/docs/8.x/queues) が格納されます。ジョブはアプリケーションによってキューに入れられるか、現在のリクエストのライフサイクル内で同期的に実行されます。現在のリクエスト中に同期的に実行されるジョブは、[command pattern](https://en.wikipedia.org/wiki/Command_pattern) の実装であるため、「コマンド」と呼ばれることがあります。

<a name="the-listeners-directory"></a>
<!-- #### The Listeners Directory -->
#### The Listeners Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `event:generate` or `make:listener` Artisan commands. The `Listeners` directory contains the classes that handle your [events](/docs/8.x/events). Event listeners receive an event instance and perform logic in response to the event being fired. For example, a `UserRegistered` event might be handled by a `SendWelcomeEmail` listener. -->
このディレクトリはデフォルトでは存在しませんが、`event:generate` または `make:listener` Artisan コマンドを実行すると作成されます。 `Listeners` ディレクトリには、[events](/docs/8.x/events) を処理するクラスが含まれています。イベント リスナはイベント インスタンスを受信し、発生したイベントに応答してロジックを実行します。たとえば、`UserRegistered` イベントは、`SendWelcomeEmail` リスナによって処理される場合があります。

<a name="the-mail-directory"></a>
<!-- #### The Mail Directory -->
#### The Mail Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:mail` Artisan command. The `Mail` directory contains all of your [classes that represent emails](/docs/8.x/mail) sent by your application. Mail objects allow you to encapsulate all of the logic of building an email in a single, simple class that may be sent using the `Mail::send` method. -->
このディレクトリはデフォルトでは存在しませんが、`make:mail` Artisan コマンドを実行すると作成されます。 `Mail` ディレクトリには、アプリケーションによって送信されたすべての [classes that represent emails](/docs/8.x/mail) が含まれています。メール オブジェクトを使用すると、電子メールを構築するすべてのロジックを、`Mail::send` メソッドを使用して送信できる単一の単純なクラスにカプセル化できます。

<a name="the-models-directory"></a>
<!-- #### The Models Directory -->
#### The Models Directory

<!-- The `Models` directory contains all of your [Eloquent model classes](/docs/8.x/eloquent). The Eloquent ORM included with Laravel provides a beautiful, simple ActiveRecord implementation for working with your database. Each database table has a corresponding "Model" which is used to interact with that table. Models allow you to query for data in your tables, as well as insert new records into the table. -->
`Models` ディレクトリには、[Eloquent model classes](/docs/8.x/eloquent) のすべてが含まれています。 Laravel に含まれる Eloquent ORM は、データベースを操作するための美しくシンプルな ActiveRecord 実装を提供します。各データベース テーブルには、そのテーブルと対話するために使用される対応する「モデル」があります。モデルを使用すると、テーブル内のデータをクエリしたり、テーブルに新しいレコードを挿入したりできます。

<a name="the-notifications-directory"></a>
<!-- #### The Notifications Directory -->
#### The Notifications Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:notification` Artisan command. The `Notifications` directory contains all of the "transactional" [notifications](/docs/8.x/notifications) that are sent by your application, such as simple notifications about events that happen within your application. Laravel's notification feature abstracts sending notifications over a variety of drivers such as email, Slack, SMS, or stored in a database. -->
このディレクトリはデフォルトでは存在しませんが、`make:notification` Artisan コマンドを実行すると作成されます。 `Notifications` ディレクトリには、アプリケーション内で発生するイベントに関する単純な通知など、アプリケーションによって送信されるすべての「トランザクション」[notifications](/docs/8.x/notifications) が含まれています。 Laravel の通知機能は、電子メール、Slack、SMS などのさまざまなドライバを介した、またはデータベースに保存された通知の送信を抽象化します。

<a name="the-policies-directory"></a>
<!-- #### The Policies Directory -->
#### The Policies Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:policy` Artisan command. The `Policies` directory contains the [authorization policy classes](/docs/8.x/authorization) for your application. Policies are used to determine if a user can perform a given action against a resource. -->
このディレクトリはデフォルトでは存在しませんが、`make:policy` Artisan コマンドを実行すると作成されます。 `Policies` ディレクトリには、アプリケーションの [authorization policy classes](/docs/8.x/authorization) が含まれています。ポリシーは、ユーザーがリソースに対して特定のアクションを実行できるかどうかを決定するために使用されます。

<a name="the-providers-directory"></a>
<!-- #### The Providers Directory -->
#### The Providers Directory

<!-- The `Providers` directory contains all of the [service providers](/docs/8.x/providers) for your application. Service providers bootstrap your application by binding services in the service container, registering events, or performing any other tasks to prepare your application for incoming requests. -->
`Providers` ディレクトリには、アプリケーションのすべての [service providers](/docs/8.x/providers) が含まれています。サービスプロバイダは、サービスコンテナーにサービスをバインドしたり、イベントを登録したり、その他のタスクを実行して、アプリケーションを受信リクエストに備えて準備したりすることによって、アプリケーションをブートストラップします。

<!-- In a fresh Laravel application, this directory will already contain several providers. You are free to add your own providers to this directory as needed. -->
新しい Laravel アプリケーションでは、このディレクトリにはすでに複数のプロバイダが含まれています。必要に応じて、このディレクトリに独自のプロバイダを自由に追加できます。

<a name="the-rules-directory"></a>
<!-- #### The Rules Directory -->
#### The Rules Directory

<!-- This directory does not exist by default, but will be created for you if you execute the `make:rule` Artisan command. The `Rules` directory contains the custom validation rule objects for your application. Rules are used to encapsulate complicated validation logic in a simple object. For more information, check out the [validation documentation](/docs/8.x/validation). -->
このディレクトリはデフォルトでは存在しませんが、`make:rule` Artisan コマンドを実行すると作成されます。 `Rules` ディレクトリには、アプリケーションのカスタム検証ルール オブジェクトが含まれています。ルールは、複雑な検証ロジックを単純なオブジェクトにカプセル化するために使用されます。詳細については、[validation documentation](/docs/8.x/validation) をご覧ください。

