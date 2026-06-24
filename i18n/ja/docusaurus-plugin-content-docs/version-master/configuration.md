<!-- # Configuration -->
# Configuration

- [Introduction](#introduction)
- [Environment Configuration](#environment-configuration)
    - [Environment Variable Types](#environment-variable-types)
    - [Retrieving Environment Configuration](#retrieving-environment-configuration)
    - [Determining the Current Environment](#determining-the-current-environment)
    - [Encrypting Environment Files](#encrypting-environment-files)
- [Accessing Configuration Values](#accessing-configuration-values)
- [Configuration Caching](#configuration-caching)
- [Configuration Publishing](#configuration-publishing)
- [Debug Mode](#debug-mode)
- [Maintenance Mode](#maintenance-mode)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you. -->
Laravel フレームワークの構成ファイルはすべて、`config` ディレクトリに保存されます。各オプションは文書化されているので、ファイルに目を通して、利用可能なオプションをよく理解してください。

<!-- These configuration files allow you to configure things like your database connection information, your mail server information, as well as various other core configuration values such as your application URL and encryption key. -->
これらの構成ファイルを使用すると、データベース接続情報、メール サーバー情報、さらにアプリケーション URL や暗号化キーなどのその他のさまざまなコア構成値などを構成できます。

<a name="the-about-command"></a>
<!-- #### The `about` Command -->
#### The `about` Command

<!-- Laravel can display an overview of your application's configuration, drivers, and environment via the `about` Artisan command. -->
Laravel は、`about` Artisan コマンドを使用して、アプリケーションの構成、ドライバ、環境の概要を表示できます。

```shell
php artisan about
```

<!-- If you're only interested in a particular section of the application overview output, you may filter for that section using the `--only` option: -->
アプリケーション概要出力の特定のセクションのみに興味がある場合は、`--only` オプションを使用してそのセクションをフィルターできます。

```shell
php artisan about --only=environment
```

<!-- Or, to explore a specific configuration file's values in detail, you may use the `config:show` Artisan command: -->
または、特定の構成ファイルの値を詳細に調べるには、`config:show` Artisan コマンドを使用できます。

```shell
php artisan config:show database
```

<a name="environment-configuration"></a>
<!-- ## Environment Configuration -->
## Environment Configuration

<!-- It is often helpful to have different configuration values based on the environment where the application is running. For example, you may wish to use a different cache driver locally than you do on your production server. -->
多くの場合、アプリケーションが実行されている環境に基づいて異なる構成値を使用すると便利です。たとえば、運用サーバーとは異なるキャッシュ ドライバをローカルで使用したい場合があります。

<!-- To make this a cinch, Laravel utilizes the [DotEnv](https://github.com/vlucas/phpdotenv) PHP library. In a fresh Laravel installation, the root directory of your application will contain a `.env.example` file that defines many common environment variables. During the Laravel installation process, this file will automatically be copied to `.env`. -->
これを簡単にするために、Laravel は [DotEnv](https://github.com/vlucas/phpdotenv) PHP ライブラリを利用します。 Laravel を新規インストールすると、アプリケーションのルート ディレクトリに、多くの一般的な環境変数を定義する `.env.example` ファイルが含まれます。 Laravel のインストールプロセス中に、このファイルは自動的に `.env` にコピーされます。

<!-- Laravel's default `.env` file contains some common configuration values that may differ based on whether your application is running locally or on a production web server. These values are then read by the configuration files within the `config` directory using Laravel's `env` function. -->
Laravel のデフォルトの `.env` ファイルには、アプリケーションがローカルで実行されているか実稼働 Web サーバーで実行されているかによって異なる可能性があるいくつかの一般的な構成値が含まれています。これらの値は、Laravel の `env` 関数を使用して、`config` ディレクトリ内の構成ファイルによって読み取られます。

<!-- If you are developing with a team, you may wish to continue including and updating the `.env.example` file with your application. By putting placeholder values in the example configuration file, other developers on your team can clearly see which environment variables are needed to run your application. -->
チームで開発している場合は、アプリケーションに `.env.example` ファイルを含めて更新し続けることができます。サンプル構成ファイルにプレースホルダー値を入れることで、チームの他の開発者は、アプリケーションの実行にどの環境変数が必要かを明確に確認できます。

> [!NOTE]
> `.env` ファイル内の変数は、サーバー レベルまたはシステム レベルの環境変数などの外部環境変数によってオーバーライドできます。

<a name="environment-file-security"></a>
<!-- #### Environment File Security -->
#### Environment File Security

<!-- Your `.env` file should not be committed to your application's source control, since each developer / server using your application could require a different environment configuration. Furthermore, this would be a security risk in the event an intruder gains access to your source control repository, since any sensitive credentials would get exposed. -->
アプリケーションを使用する各開発者/サーバーは異なる環境構成を必要とする可能性があるため、`.env` ファイルをアプリケーションのソース管理にコミットしないでください。さらに、侵入者がソース管理リポジトリにアクセスした場合、機密の資格情報が漏洩してしまうため、セキュリティ リスクとなります。

<!-- However, it is possible to encrypt your environment file using Laravel's built-in [environment encryption](#encrypting-environment-files). Encrypted environment files may be placed in source control safely. -->
ただし、Laravel の組み込み [environment encryption](#encrypting-environment-files) を使用して環境ファイルを暗号化することは可能です。暗号化された環境ファイルはソース管理に安全に配置できます。

<a name="additional-environment-files"></a>
<!-- #### Additional Environment Files -->
#### Additional Environment Files

<!-- Before loading your application's environment variables, Laravel determines if an `APP_ENV` environment variable has been externally provided or if the `--env` CLI argument has been specified. If so, Laravel will attempt to load an `.env.[APP_ENV]` file if it exists. If it does not exist, the default `.env` file will be loaded. -->
アプリケーションの環境変数をロードする前に、Laravel は、`APP_ENV` 環境変数が外部から提供されているかどうか、または `--env` CLI 引数が指定されているかどうかを判断します。その場合、Laravel は `.env.[APP_ENV]` ファイルが存在する場合、そのファイルをロードしようとします。存在しない場合は、デフォルトの `.env` ファイルがロードされます。

<a name="environment-variable-types"></a>
<!-- ### Environment Variable Types -->
### Environment Variable Types

<!-- All variables in your `.env` files are typically parsed as strings, so some reserved values have been created to allow you to return a wider range of types from the `env()` function: -->
`.env` ファイル内のすべての変数は通常、文字列として解析されるため、`env()` 関数からより広範囲の型を返すことができるように、いくつかの予約値が作成されています。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| `.env` 値 | `env()` 値 |
| ------------ | ------------- |
| true         | (bool) true   |
| (true)       | (bool) true   |
| false        | (bool) false  |
| (false)      | (bool) false  |
| empty        | (string) ''   |
| (empty)      | (string) ''   |
| null         | (null) null   |
| (null)       | (null) null   |

<!-- </div> -->
</div>

<!-- If you need to define an environment variable with a value that contains spaces, you may do so by enclosing the value in double quotes: -->
スペースを含む値を使用して環境変数を定義する必要がある場合は、値を二重引用符で囲むことで定義できます。

```ini
APP_NAME="My Application"
```

<a name="retrieving-environment-configuration"></a>
<!-- ### Retrieving Environment Configuration -->
### Retrieving Environment Configuration

<!-- All of the variables listed in the `.env` file will be loaded into the `$_ENV` PHP super-global when your application receives a request. However, you may use the `env` function to retrieve values from these variables in your configuration files. In fact, if you review the Laravel configuration files, you will notice many of the options are already using this function: -->
`.env` ファイルにリストされているすべての変数は、アプリケーションがリクエストを受信すると、`$_ENV` PHP スーパーグローバルにロードされます。ただし、`env` 関数を使用して、構成ファイル内のこれらの変数から値を取得することもできます。実際、Laravel 設定ファイルを確認すると、多くのオプションがすでにこの関数を使用していることがわかります。

```php
'debug' => (bool) env('APP_DEBUG', false),
```

<!-- The second value passed to the `env` function is the "default value". This value will be returned if no environment variable exists for the given key. -->
`env` 関数に渡される 2 番目の値は「デフォルト値」です。指定されたキーに環境変数が存在しない場合、この値が返されます。

<a name="determining-the-current-environment"></a>
<!-- ### Determining the Current Environment -->
### Determining the Current Environment

<!-- The current application environment is determined via the `APP_ENV` variable from your `.env` file. You may access this value via the `environment` method on the `App` [facade](/docs/master/facades): -->
現在のアプリケーション環境は、`.env` ファイルの `APP_ENV` 変数によって決定されます。この値には、`App` [facade](/docs/master/facades) の `environment` メソッドを介してアクセスできます。

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();
```

<!-- You may also pass arguments to the `environment` method to determine if the environment matches a given value. The method will return `true` if the environment matches any of the given values: -->
`environment` メソッドに引数を渡して、環境が指定された値と一致するかどうかを判断することもできます。環境が指定された値のいずれかに一致する場合、メソッドは `true` を返します。

```php
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}
```

> [!NOTE]
> 現在のアプリケーション環境の検出は、サーバーレベルの `APP_ENV` 環境変数を定義することで上書きできます。

<a name="encrypting-environment-files"></a>
<!-- ### Encrypting Environment Files -->
### Encrypting Environment Files

<!-- Unencrypted environment files should never be stored in source control. However, Laravel allows you to encrypt your environment files so that they may safely be added to source control with the rest of your application. -->
暗号化されていない環境ファイルはソース管理に保存しないでください。ただし、Laravel を使用すると、環境ファイルを暗号化して、アプリケーションの残りの部分とともにソース管理に安全に追加できるようになります。

<a name="encryption"></a>
<!-- #### Encryption -->
#### Encryption

<!-- To encrypt an environment file, you may use the `env:encrypt` command: -->
環境ファイルを暗号化するには、`env:encrypt` コマンドを使用できます。

```shell
php artisan env:encrypt
```

<!-- Running the `env:encrypt` command will encrypt your `.env` file and place the encrypted contents in an `.env.encrypted` file. The decryption key is presented in the output of the command and should be stored in a secure password manager. If you would like to provide your own encryption key you may use the `--key` option when invoking the command: -->
`env:encrypt` コマンドを実行すると、`.env` ファイルが暗号化され、暗号化されたコンテンツが `.env.encrypted` ファイルに配置されます。復号化キーはコマンドの出力に表示され、安全なパスワード マネージャーに保存する必要があります。独自の暗号化キーを提供したい場合は、コマンドを呼び出すときに `--key` オプションを使用できます。

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

> [!NOTE]
> 提供されるキーの長さは、使用されている暗号化方式で必要なキーの長さと一致する必要があります。デフォルトでは、Laravel は 32 文字のキーを必要とする `AES-256-CBC` 暗号を使用します。コマンドを呼び出すときに `--cipher` オプションを渡すことで、Laravel の [encrypter](/docs/master/encryption) でサポートされている暗号を自由に使用できます。

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be encrypted by providing the environment name via the `--env` option: -->
アプリケーションに `.env` や `.env.staging` などの複数の環境ファイルがある場合は、`--env` オプションで環境名を指定することで、暗号化する環境ファイルを指定できます。

```shell
php artisan env:encrypt --env=staging
```

<a name="readable-variable-names"></a>
<!-- #### Readable Variable Names -->
#### Readable Variable Names

<!-- When encrypting your environment file, you may use the `--readable` option to retain visible variable names while encrypting their values: -->
環境ファイルを暗号化する場合、`--readable` オプションを使用して、値を暗号化しながら表示される変数名を保持できます。

```shell
php artisan env:encrypt --readable
```

<!-- This will produce an encrypted file with the following format: -->
これにより、次の形式の暗号化されたファイルが生成されます。

```ini
APP_NAME=eyJpdiI6...
APP_ENV=eyJpdiI6...
APP_KEY=eyJpdiI6...
APP_DEBUG=eyJpdiI6...
APP_URL=eyJpdiI6...
```

<!-- Using the readable format allows you to see which environment variables exist without exposing sensitive data. It also makes reviewing pull requests much easier since you can see which variables were added, removed, or renamed without needing to decrypt the file. -->
読み取り可能な形式を使用すると、機密データを公開することなく、どの環境変数が存在するかを確認できます。また、ファイルを復号化することなく、どの変数が追加、削除、または名前変更されたかを確認できるため、プル リクエストのレビューが非常に簡単になります。

<!-- When decrypting environment files, Laravel automatically detects which format was used, so no additional options are needed for the `env:decrypt` command. -->
環境ファイルを復号化するときに、Laravel は使用された形式を自動的に検出するため、`env:decrypt` コマンドに追加のオプションは必要ありません。

> [!NOTE]
> `--readable` オプションを使用する場合、元の環境ファイルのコメントと空白行は暗号化された出力に含まれません。

<a name="decryption"></a>
<!-- #### Decryption -->
#### Decryption

<!-- To decrypt an environment file, you may use the `env:decrypt` command. This command requires a decryption key, which Laravel will retrieve from the `LARAVEL_ENV_ENCRYPTION_KEY` environment variable: -->
環境ファイルを復号化するには、`env:decrypt` コマンドを使用できます。このコマンドには、Laravel が `LARAVEL_ENV_ENCRYPTION_KEY` 環境変数から取得する復号キーが必要です。

```shell
php artisan env:decrypt
```

<!-- Or, the key may be provided directly to the command via the `--key` option: -->
または、`--key` オプションを使用してキーをコマンドに直接指定することもできます。

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF
```

<!-- When the `env:decrypt` command is invoked, Laravel will decrypt the contents of the `.env.encrypted` file and place the decrypted contents in the `.env` file. -->
`env:decrypt` コマンドが呼び出されると、Laravel は `.env.encrypted` ファイルの内容を復号化し、復号化された内容を `.env` ファイルに配置します。

<!-- The `--cipher` option may be provided to the `env:decrypt` command in order to use a custom encryption cipher: -->
カスタム暗号化暗号を使用するために、`--cipher` オプションを `env:decrypt` コマンドに指定できます。

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC
```

<!-- If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be decrypted by providing the environment name via the `--env` option: -->
アプリケーションに `.env` や `.env.staging` などの複数の環境ファイルがある場合は、`--env` オプションで環境名を指定することで、復号化する環境ファイルを指定できます。

```shell
php artisan env:decrypt --env=staging
```

<!-- In order to overwrite an existing environment file, you may provide the `--force` option to the `env:decrypt` command: -->
既存の環境ファイルを上書きするには、`--force` オプションを `env:decrypt` コマンドに指定します。

```shell
php artisan env:decrypt --force
```

<a name="accessing-configuration-values"></a>
<!-- ## Accessing Configuration Values -->
## Accessing Configuration Values

<!-- You may easily access your configuration values using the `Config` facade or global `config` function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist: -->
`Config` ファサードまたはグローバル `config` 関数を使用すると、アプリケーションのどこからでも構成値に簡単にアクセスできます。設定値には、アクセスするファイル名とオプションを含む「ドット」構文を使用してアクセスできます。デフォルト値を指定することもでき、構成オプションが存在しない場合はデフォルト値が返されます。

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');
```

<!-- To set configuration values at runtime, you may invoke the `Config` facade's `set` method or pass an array to the `config` function: -->
実行時に構成値を設定するには、`Config` ファサードの `set` メソッドを呼び出すか、配列を `config` 関数に渡します。

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);
```

<!-- To assist with static analysis, the `Config` facade also provides typed configuration retrieval methods. If the retrieved configuration value does not match the expected type, an exception will be thrown: -->
静的分析を支援するために、`Config` ファサードは、型付き構成の取得メソッドも提供します。取得した構成値が予期されるタイプと一致しない場合、例外がスローされます。

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
Config::collection('config-key');
```

<a name="configuration-caching"></a>
<!-- ## Configuration Caching -->
## Configuration Caching

<!-- To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework. -->
アプリケーションの速度を向上させるには、`config:cache` Artisan コマンドを使用して、すべての構成ファイルを 1 つのファイルにキャッシュする必要があります。これにより、アプリケーションのすべての構成オプションが 1 つのファイルに結合され、フレームワークによってすぐにロードできるようになります。

<!-- You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development. -->
通常、実稼働デプロイメント・プロセスの一部として `php artisan config:cache` コマンドを実行する必要があります。アプリケーションの開発中に構成オプションを頻繁に変更する必要があるため、ローカル開発中にこのコマンドを実行しないでください。

<!-- Once the configuration has been cached, your application's `.env` file will not be loaded by the framework during requests or Artisan commands; therefore, the `env` function will only return external, system level environment variables. -->
構成がキャッシュされると、アプリケーションの `.env` ファイルは、リクエストまたはArtisan コマンド中にフレームワークによってロードされなくなります。したがって、`env` 関数は、外部のシステム レベルの環境変数のみを返します。

<!-- For this reason, you should ensure you are only calling the `env` function from within your application's configuration (`config`) files. You can see many examples of this by examining Laravel's default configuration files. Configuration values may be accessed from anywhere in your application using the `config` function [described above](#accessing-configuration-values). -->
このため、アプリケーションの構成 (`config`) ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。 Laravel のデフォルト設定ファイルを調べると、この例を数多く確認できます。構成値には、`config` 関数 [described above](#accessing-configuration-values) を使用して、アプリケーション内のどこからでもアクセスできます。

<!-- The `config:clear` command may be used to purge the cached configuration: -->
`config:clear` コマンドを使用して、キャッシュされた構成を削除できます。

```shell
php artisan config:clear
```

> [!WARNING]
> デプロイメントプロセス中に `config:cache` コマンドを実行する場合は、構成ファイル内からのみ `env` 関数を呼び出していることを確認する必要があります。構成がキャッシュされると、`.env` ファイルはロードされません。したがって、`env` 関数は、外部のシステム レベルの環境変数のみを返します。

<a name="configuration-publishing"></a>
<!-- ## Configuration Publishing -->
## Configuration Publishing

<!-- Most of Laravel's configuration files are already published in your application's `config` directory; however, certain configuration files like `cors.php` and `view.php` are not published by default, as most applications will never need to modify them. -->
Laravel の設定ファイルのほとんどは、アプリケーションの `config` ディレクトリにすでに公開されています。ただし、`cors.php` や `view.php` などの特定の構成ファイルは、ほとんどのアプリケーションで変更する必要がないため、デフォルトでは公開されません。

<!-- However, you may use the `config:publish` Artisan command to publish any configuration files that are not published by default: -->
ただし、`config:publish` Artisan コマンドを使用して、デフォルトでは公開されない構成ファイルを公開できます。

```shell
php artisan config:publish

php artisan config:publish --all
```

<a name="debug-mode"></a>
<!-- ## Debug Mode -->
## Debug Mode

<!-- The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file. -->
`config/app.php` 構成ファイルの `debug` オプションは、エラーに関する情報が実際にユーザーに表示される量を決定します。デフォルトでは、このオプションは、`.env` ファイルに保存されている `APP_DEBUG` 環境変数の値を尊重するように設定されています。

> [!WARNING]
> ローカル開発の場合は、`APP_DEBUG` 環境変数を `true` に設定する必要があります。 **実稼働環境では、この値は常に `false` である必要があります。運用環境で変数が `true` に設定されている場合、機密の構成値がアプリケーションのエンド ユーザーに公開される危険があります。**

<a name="maintenance-mode"></a>
<!-- ## Maintenance Mode -->
## Maintenance Mode

<!-- When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503. -->
アプリケーションがメンテナンス モードの場合、アプリケーションへのすべてのリクエストに対してカスタム ビューが表示されます。これにより、更新中またはメンテナンスの実行中にアプリケーションを簡単に「無効化」できます。メンテナンス モード チェックは、アプリケーションのデフォルトのミドルウェア スタックに含まれています。アプリケーションがメンテナンス モードの場合、`Symfony\Component\HttpKernel\Exception\HttpException` インスタンスがステータス コード 503 でスローされます。

<!-- To enable maintenance mode, execute the `down` Artisan command: -->
メンテナンス モードを有効にするには、`down` Artisan コマンドを実行します。

```shell
php artisan down
```

<!-- If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds: -->
すべてのメンテナンス モード応答とともに `Refresh` HTTP ヘッダーを送信したい場合は、`down` コマンドを呼び出すときに `refresh` オプションを指定できます。 `Refresh` ヘッダーは、指定された秒数の後にページを自動的に更新するようにブラウザーに指示します。

```shell
php artisan down --refresh=15
```

<!-- You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header: -->
`retry` オプションを `down` コマンドに指定することもできます。これは、`Retry-After` HTTP ヘッダーの値として設定されますが、通常、ブラウザーはこのヘッダーを無視します。

```shell
php artisan down --retry=60
```

<a name="bypassing-maintenance-mode"></a>
<!-- #### Bypassing Maintenance Mode -->
#### Bypassing Maintenance Mode

<!-- To allow maintenance mode to be bypassed using a secret token, you may use the `secret` option to specify a maintenance mode bypass token: -->
シークレット トークンを使用してメンテナンス モードをバイパスできるようにするには、`secret` オプションを使用してメンテナンス モード バイパス トークンを指定できます。

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"
```

<!-- After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser: -->
アプリケーションをメンテナンス モードにした後、このトークンに一致するアプリケーション URL に移動すると、Laravel はブラウザにメンテナンス モード バイパス Cookie を発行します。

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515
```

<!-- If you would like Laravel to generate the secret token for you, you may use the `with-secret` option. The secret will be displayed to you once the application is in maintenance mode: -->
Laravel にシークレットトークンを生成してもらいたい場合は、`with-secret` オプションを使用できます。アプリケーションがメンテナンス モードになると、シークレットが表示されます。

```shell
php artisan down --with-secret
```

<!-- When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode. -->
この非表示のルートにアクセスすると、アプリケーションの `/` ルートにリダイレクトされます。ブラウザに Cookie が発行されると、メンテナンス モードでないかのようにアプリケーションを通常どおり閲覧できるようになります。

> [!NOTE]
> メンテナンス モードのシークレットは通常、英数字と、必要に応じてダッシュで構成されます。 URL では、`?` や `&` などの特別な意味を持つ文字を使用しないでください。

<a name="maintenance-mode-on-multiple-servers"></a>
<!-- #### Maintenance Mode on Multiple Servers -->
#### Maintenance Mode on Multiple Servers

<!-- By default, Laravel determines if your application is in maintenance mode using a file-based system. This means to activate maintenance mode, the `php artisan down` command has to be executed on each server hosting your application. -->
デフォルトでは、Laravel はファイルベースのシステムを使用してアプリケーションがメンテナンスモードであるかどうかを判断します。これは、メンテナンス モードをアクティブにするには、アプリケーションをホストしている各サーバーで `php artisan down` コマンドを実行する必要があることを意味します。

<!-- Alternatively, Laravel offers a cache-based method for handling maintenance mode. This method requires running the `php artisan down` command on just one server. To use this approach, modify the maintenance mode variables in your application's `.env` file. You should select a cache `store` that is accessible by all of your servers. This ensures the maintenance mode status is consistently maintained across every server: -->
あるいは、Laravel はメンテナンス モードを処理するためのキャッシュベースの方法を提供します。この方法では、1 つのサーバー上で `php artisan down` コマンドを実行する必要があります。このアプローチを使用するには、アプリケーションの `.env` ファイル内のメンテナンス モード変数を変更します。すべてのサーバーからアクセスできるキャッシュ `store` を選択する必要があります。これにより、メンテナンス モードのステータスがすべてのサーバーにわたって一貫して維持されます。

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database
```

<a name="pre-rendering-the-maintenance-mode-view"></a>
<!-- #### Pre-Rendering the Maintenance Mode View -->
#### Pre-Rendering the Maintenance Mode View

<!-- If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine. -->
デプロイメント中に `php artisan down` コマンドを使用する場合でも、Composer の依存関係または他のインフラストラクチャ コンポーネントの更新中にユーザーがアプリケーションにアクセスすると、エラーが発生することがあります。これは、アプリケーションがメンテナンス モードであることを判断し、テンプレート エンジンを使用してメンテナンス モード ビューをレンダリングするために、Laravel フレームワークの重要な部分を起動する必要があるために発生します。

<!-- For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option: -->
このため、Laravel では、リクエスト サイクルの最初に返されるメンテナンス モード ビューを事前にレンダリングできます。このビューは、アプリケーションの依存関係が読み込まれる前にレンダリングされます。 `down` コマンドの `render` オプションを使用して、選択したテンプレートを事前レンダリングできます。

```shell
php artisan down --render="errors::503"
```

<a name="redirecting-maintenance-mode-requests"></a>
<!-- #### Redirecting Maintenance Mode Requests -->
#### Redirecting Maintenance Mode Requests

<!-- While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI: -->
メンテナンスモードの間、LaravelはユーザーがアクセスしようとしているすべてのアプリケーションURLに対してメンテナンスモードビューを表示します。必要に応じて、すべてのリクエストを特定の URL にリダイレクトするように Laravel に指示できます。これは、`redirect` オプションを使用して実現できます。たとえば、すべてのリクエストを `/` URI にリダイレクトしたい場合があります。

```shell
php artisan down --redirect=/
```

<a name="disabling-maintenance-mode"></a>
<!-- #### Disabling Maintenance Mode -->
#### Disabling Maintenance Mode

<!-- To disable maintenance mode, use the `up` command: -->
メンテナンス モードを無効にするには、`up` コマンドを使用します。

```shell
php artisan up
```

> [!NOTE]
> `resources/views/errors/503.blade.php` で独自のテンプレートを定義することで、デフォルトのメンテナンス モード テンプレートをカスタマイズできます。

<a name="maintenance-mode-queues"></a>
<!-- #### Maintenance Mode and Queues -->
#### Maintenance Mode and Queues

<!-- While your application is in maintenance mode, no [queued jobs](/docs/master/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode. -->
アプリケーションがメンテナンス モードの間は、[queued jobs](/docs/master/queues) は処理されません。アプリケーションがメンテナンス モードを終了しても、ジョブは通常どおり処理され続けます。

<a name="alternatives-to-maintenance-mode"></a>
<!-- #### Alternatives to Maintenance Mode -->
#### Alternatives to Maintenance Mode

<!-- Since maintenance mode requires your application to have several seconds of downtime, consider running your applications on a fully-managed platform like [Laravel Cloud](https://cloud.laravel.com) to accomplish zero-downtime deployment with Laravel. -->
メンテナンスモードではアプリケーションに数秒のダウンタイムが必要なため、Laravel でゼロダウンタイムのデプロイメントを実現するには、[Laravel Cloud](https://cloud.laravel.com) のような完全に管理されたプラットフォームでアプリケーションを実行することを検討してください。

