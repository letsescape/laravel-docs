<!-- # Configuration -->
# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
    - [Environment Variable Types](#environment-variable-types)
    - [Retrieving Environment Configuration](#retrieving-environment-configuration)
    - [Determining The Current Environment](#determining-the-current-environment)
- [Accessing Configuration Values](#accessing-configuration-values)
- [Configuration Caching](#configuration-caching)
- [Debug Mode](#debug-mode)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel フレームワークの構成ファイルはすべて、`config` ディレクトリに保存されます。各オプションは文書化されているので、ファイルに目を通して、利用可能なオプションをよく理解してください。

<!-- These configuration files allow you to configure things like your database connection information, your mail server information, as well as various other core configuration values such as your application timezone and encryption key. -->
これらの構成ファイルを使用すると、データベース接続情報、メール サーバー情報に加え、アプリケーションのタイムゾーンや暗号化キーなどのその他のさまざまなコア構成値などを構成できます。

<a name="environment-configuration"></a>
<!-- ## Environment Configuration -->
## Environment Configuration

<!-- It is often helpful to have different configuration values based on the environment where the application is running. For example, you may wish to use a different cache driver locally than you do on your production server. -->
多くの場合、アプリケーションが実行されている環境に基づいて異なる構成値を使用すると便利です。たとえば、運用サーバーとは異なるキャッシュ ドライバをローカルで使用したい場合があります。

<!-- To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file that defines many common environment variables. During the Laravel installation process, this file will automatically be copied to `.env`. -->
これを簡単にするために、Laravel は [DotEnv](https://github.com/vlucas/phpdotenv) PHP ライブラリを利用します。 Laravel を新規インストールすると、アプリケーションのルート ディレクトリに、多くの一般的な環境変数を定義する `.env.example` ファイルが含まれます。 Laravel のインストールプロセス中に、このファイルは自動的に `.env` にコピーされます。

<!-- Laravel's default `.env` file contains some common configuration values that may differ based on whether your application is running locally or on a production web server. These values are then retrieved from various Laravel configuration files within the `config` directory using Laravel's `env` function. -->
Laravel のデフォルトの `.env` ファイルには、アプリケーションがローカルで実行されているか実稼働 Web サーバーで実行されているかによって異なる可能性があるいくつかの一般的な構成値が含まれています。これらの値は、Laravel の `env` 関数を使用して、`config` ディレクトリ内のさまざまな Laravel 構成ファイルから取得されます。

<!-- If you are developing with a team, you may wish to continue including a `.env.example` file with your application. By putting placeholder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application. -->
チームで開発している場合は、引き続き `.env.example` ファイルをアプリケーションに含めることをお勧めします。サンプル構成ファイルにプレースホルダー値を入れることで、チームの他の開発者は、アプリケーションの実行にどの環境変数が必要かを明確に確認できます。

> [!TIP]
> `.env` ファイル内の変数は、サーバー レベルまたはシステム レベルの環境変数などの外部環境変数によってオーバーライドできます。

<a name="environment-file-security"></a>
<!-- #### Environment File Security -->
#### Environment File Security

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が漏洩してしまうため、セキュリティ リスクとなります。

<a name="additional-environment-files"></a>
<!-- #### Additional Environment Files -->
#### Additional Environment Files

<!-- Before loading your application's environment variables, Laravel determines if either the `APP_ENV` environment variable has been externally provided or if the `--env` CLI argument has been specified. If so, Laravel will attempt to load an `.env.[APP_ENV]` file if it exists. If it does not exist, the default `.env` file will be loaded. -->
アプリケーションの環境変数をロードする前に、Laravel は、`APP_ENV` 環境変数が外部から提供されているかどうか、または `--env` CLI 引数が指定されているかどうかを判断します。その場合、Laravel は `.env.[APP_ENV]` ファイルが存在する場合、そのファイルをロードしようとします。存在しない場合は、デフォルトの `.env` ファイルがロードされます。

<a name="environment-variable-types"></a>
<!-- ### Environment Variable Types -->
### Environment Variable Types

<!-- All variables in your `.env` files are typically parsed as strings, so some reserved values have been created to allow you to return a wider range of types from the `env()` function: -->
`.env` ファイル内のすべての変数は通常、文字列として解析されるため、`env()` 関数からより広範囲の型を返すことができるように、いくつかの予約値が作成されています。

<!--
`.env` Value  | `env()` Value
------------- | -------------
true | (bool) true
(true) | (bool) true
false | (bool) false
(false) | (bool) false
empty | (string) ''
(empty) | (string) ''
null | (null) null
(null) | (null) null
-->
`.env` 値 | `env()` 値
------------- | -------------
true | (bool) true
(true) | (bool) true
false | (bool) false
(false) | (bool) false
empty | (string) ''
(empty) | (string) ''
null | (null) null
(null) | (null) null

<!-- If you need to define an environment variable with a value that contains spaces, you may do so by enclosing the value in double quotes: -->
スペースを含む値を使用して環境変数を定義する必要がある場合は、値を二重引用符で囲むことで定義できます。

```
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
<!-- ### Retrieving Environment Configuration -->
### Retrieving Environment Configuration

<!-- All of the variables listed in this file will be loaded into the `$_ENV` PHP super-global when your application receives a request. However, you may use the `env` helper to retrieve values from these variables in your configuration files. In fact, if you review the Laravel configuration files, you will notice many of the options are already using this helper: -->
このファイルにリストされているすべての変数は、アプリケーションがリクエストを受信すると、`$_ENV` PHP スーパーグローバルにロードされます。ただし、`env` ヘルパを使用して、構成ファイル内のこれらの変数から値を取得することもできます。実際、Laravel 設定ファイルを確認すると、多くのオプションがすでにこのヘルパを使用していることがわかります。

```
'debug' => env('APP_DEBUG', false),
```

<!-- The second value passed to the `env` function is the "default value". This value will be returned if no environment variable exists for the given key. -->
`env` 関数に渡される 2 番目の値は「デフォルト値」です。指定されたキーに環境変数が存在しない場合、この値が返されます。

<a name="determining-the-current-environment"></a>
<!-- ### Determining The Current Environment -->
### Determining The Current Environment

<!-- The current application environment is determined via the `APP_ENV` variable from your `.env` file. You may access this value via the `environment` method on the `App` [facade](/docs/8.x/facades): -->
現在のアプリケーション環境は、`.env` ファイルの `APP_ENV` 変数によって決定されます。この値には、`App` [facade](/docs/8.x/facades) の `environment` メソッドを介してアクセスできます。

```
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

<!-- You may also pass arguments to the `environment` method to determine if the environment matches a given value. The method will return `true` if the environment matches any of the given values: -->
`environment` メソッドに引数を渡して、環境が指定された値と一致するかどうかを判断することもできます。環境が指定された値のいずれかに一致する場合、メソッドは `true` を返します。

```
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}
```

> [!TIP]
> 現在のアプリケーション環境の検出は、サーバーレベルの `APP_ENV` 環境変数を定義することで上書きできます。

<a name="accessing-configuration-values"></a>
<!-- ## Accessing Configuration Values -->
## Accessing Configuration Values

<!-- You may easily access your configuration values using the global `config` helper function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist: -->
グローバル `config` ヘルパ関数を使用すると、アプリケーションのどこからでも構成値に簡単にアクセスできます。設定値には、アクセスするファイル名とオプションを含む「ドット」構文を使用してアクセスできます。デフォルト値を指定することもでき、構成オプションが存在しない場合はデフォルト値が返されます。

```
$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');
```

<!-- To set configuration values at runtime, pass an array to the `config` helper: -->
実行時に構成値を設定するには、配列を `config` ヘルパに渡します。

```
config(['app.timezone' => 'America/Chicago']);
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework. -->
アプリケーションの速度を向上させるには、`config:cache` Artisan コマンドを使用して、すべての構成ファイルを 1 つのファイルにキャッシュする必要があります。これにより、アプリケーションのすべての構成オプションが 1 つのファイルに結合され、フレームワークによってすぐにロードできるようになります。

<!-- You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development. -->
通常、実稼働デプロイメント・プロセスの一部として `php artisan config:cache` コマンドを実行する必要があります。アプリケーションの開発中に構成オプションを頻繁に変更する必要があるため、ローカル開発中にこのコマンドを実行しないでください。

> [!NOTE]
> デプロイ プロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされません。したがって、`env` 関数は、外部のシステム レベルの環境変数のみを返します。

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 構成ファイルの `debug` オプションは、エラーに関する情報が実際にユーザーに表示される量を決定します。デフォルトでは、このオプションは、`.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

<!-- For local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the variable is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.** -->
ローカル開発の場合は、`APP_DEBUG` 環境変数を `true` に設定する必要があります。 **実稼働環境では、この値は常に `false` である必要があります。運用環境で変数が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="maintenance-mode"></a>
<!-- ## Maintenance Mode -->
## Maintenance Mode

<!-- When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503. -->
アプリケーションがメンテナンス モードの場合、アプリケーションへのすべてのリクエストに対してカスタム ビューが表示されます。これにより、更新中またはメンテナンスの実行中にアプリケーションを簡単に「無効化」できます。メンテナンス モード チェックは、アプリケーションのデフォルトのミドルウェア スタックに含まれています。アプリケーションがメンテナンス モードの場合、`Symfony\Component\HttpKernel\Exception\HttpException` インスタンスがステータス コード 503 でスローされます。

<!-- To enable maintenance mode, execute the `down` Artisan command: -->
メンテナンス モードを有効にするには、`down` Artisan コマンドを実行します。

```
php artisan down
```

<!-- If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds: -->
すべてのメンテナンス モード応答とともに `Refresh` HTTP ヘッダーを送信したい場合は、`down` コマンドを呼び出すときに `refresh` オプションを指定できます。 `Refresh` ヘッダーは、指定された秒数の後にページを自動的に更新するようにブラウザーに指示します。

```
php artisan down --refresh=15
```

<!-- You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header: -->
`retry` オプションを `down` コマンドに指定することもできます。これは、`Retry-After` HTTP ヘッダーの値として設定されますが、通常、ブラウザーはこのヘッダーを無視します。

```
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
<!-- #### Bypassing Maintenance Mode -->
#### Bypassing Maintenance Mode

<!-- Even while in maintenance mode, you may use the `secret` option to specify a maintenance mode bypass token: -->
メンテナンス モード中であっても、`secret` オプションを使用してメンテナンス モード バイパス トークンを指定できます。

```
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
アプリケーションをメンテナンス モードにした後、このトークンに一致するアプリケーション URL に移動すると、Laravel はブラウザにメンテナンス モード バイパス Cookie を発行します。

<!--     https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515 -->
    https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
この非表示のルートにアクセスすると、アプリケーションの `/` ルートにリダイレクトされます。ブラウザに Cookie が発行されると、メンテナンス モードでないかのようにアプリケーションを通常どおり閲覧できるようになります。

> [!TIP]
> メンテナンス モードのシークレットは通常、英数字と、必要に応じてダッシュで構成されます。 URL では、`?` や `&` などの特別な意味を持つ文字を使用しないでください。

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering The Maintenance Mode View -->
#### Pre-Rendering The Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
デプロイメント中に `php artisan down` コマンドを使用する場合でも、Composer の依存関係または他のインフラストラクチャ コンポーネントの更新中にユーザーがアプリケーションにアクセスすると、エラーが発生することがあります。これは、アプリケーションがメンテナンス モードであることを判断し、テンプレート エンジンを使用してメンテナンス モード ビューをレンダリングするために、Laravel フレームワークの重要な部分を起動する必要があるために発生します。

<!-- For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
このため、Laravel では、リクエスト サイクルの最初に返されるメンテナンス モード ビューを事前にレンダリングできます。このビューは、アプリケーションの依存関係が読み込まれる前にレンダリングされます。 `down` コマンドの `render` オプションを使用して、選択したテンプレートを事前レンダリングできます。

```
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
<!-- #### Redirecting Maintenance Mode Requests -->
#### Redirecting Maintenance Mode Requests

<!-- While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI: -->
メンテナンスモードの間、LaravelはユーザーがアクセスしようとしているすべてのアプリケーションURLに対してメンテナンスモードビューを表示します。必要に応じて、すべてのリクエストを特定の URL にリダイレクトするように Laravel に指示できます。これは、`redirect` オプションを使用して実現できます。たとえば、すべてのリクエストを `/` URI にリダイレクトしたい場合があります。

```
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
<!-- #### Disabling Maintenance Mode -->
#### Disabling Maintenance Mode

<!-- To disable maintenance mode, use the `up` command: -->
メンテナンス モードを無効にするには、`up` コマンドを使用します。

```
php artisan up
```

> [!TIP]
> `resources/views/errors/503.blade.php` で独自のテンプレートを定義することで、デフォルトのメンテナンス モード テンプレートをカスタマイズできます。

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode & Queues -->
#### Maintenance Mode & Queues

<!-- While your application is in maintenance mode, no [queued jobs](/docs/8.x/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
アプリケーションがメンテナンス モードの間は、[queued jobs](/docs/8.x/queues) は処理されません。アプリケーションがメンテナンス モードを終了しても、ジョブは通常どおり処理され続けます。

<a name="alternatives-to-maintenance-mode"></a>
<!-- #### Alternatives To Maintenance Mode -->
#### Alternatives To Maintenance Mode

<!-- Since maintenance mode requires your application to have several seconds of downtime, consider alternatives like [Laravel Vapor](https://vapor.laravel.com) and [Envoyer](https://envoyer.io) to accomplish zero-downtime deployment with Laravel. -->
メンテナンスモードではアプリケーションに数秒のダウンタイムが必要なため、Laravel でゼロダウンタイムのデプロイメントを実現するには、[Laravel Vapor](https://vapor.laravel.com) や [Envoyer](https://envoyer.io) などの代替手段を検討してください。

